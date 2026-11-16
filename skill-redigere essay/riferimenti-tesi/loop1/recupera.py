#!/usr/bin/env python3
"""Loop 1 - Recupero fonti.

Identifica ogni fonte citata nella scaletta (nota solo come Autore, anno)
tramite API bibliografiche gratuite, scarica il PDF quando e' ad accesso
aperto, e riporta tutto nel foglio 'Fonti' di iTOC master.xlsx.

Uso tipico:
    python3 recupera.py                          # dry-run su tutte le fonti da_cercare
    python3 recupera.py --only agrawal2018        # debug su una sola fonte
    python3 recupera.py --limit 8                  # dry-run sulle prime 8
    python3 recupera.py --commit                   # scrive davvero nell'Excel

Senza --commit lo script NON scrive nell'Excel e NON scarica nulla: stampa
soltanto cosa farebbe. Vedi README.md per i dettagli.
"""
from __future__ import annotations

import argparse
import os
import datetime as dt
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import excelio, scoring, sources, textutil
from lib.cache import SourceCache
from lib.download import download_pdf
from lib.httpclient import PoliteSession

DEFAULT_EXCEL_PATH = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/iTOC master.xlsx"
DEFAULT_CONTACT_EMAIL = "lele.falzi@gmail.com"
CANDIDATES_PER_API = 5
ARXIV_YEAR_THRESHOLD = 2024
MAX_CANDIDATES_IN_DISAMBIGUATION = 3

log = logging.getLogger("loop1")


# ---------------------------------------------------------------------------
# Fase 1+2: risoluzione dell'identita' e punteggio
# ---------------------------------------------------------------------------

def _query_api_cached(cache: SourceCache, fonte_id: str, api_name: str, query: str,
                       fetch_fn) -> list[dict]:
    """Interroga un'API con cache su file. Non solleva mai: un errore su
    una singola API viene loggato e restituisce lista vuota, cosi' una
    fonte non manda in crash l'intero run.
    """
    if cache.has_api_result(fonte_id, api_name):
        cached = cache.get_api_result(fonte_id, api_name)
        log.info("  [%s] cache hit (query: %r) -> %d candidati", api_name, cached["query"],
                  len(cached["candidates"]))
        return cached["candidates"]
    try:
        candidates = fetch_fn()
        cache.set_api_result(fonte_id, api_name, query, candidates)
        log.info("  [%s] query %r -> %d candidati", api_name, query, len(candidates))
        return candidates
    except Exception as exc:  # noqa: BLE001 - una fonte che fallisce non deve fermare il run
        log.warning("  [%s] fallita per %r: %s", api_name, query, exc)
        cache.set_api_result(fonte_id, api_name, query, [], error=str(exc))
        return []


def resolve_identity(session: PoliteSession, cache: SourceCache, fonte_id: str,
                      query: str, source_surname_norm: str, source_year: int | None,
                      similarity_text: str) -> tuple[str, list, str]:
    """Fase 1 + 2. Ritorna (stato, scored_candidates_ordinati, motivazione)."""
    raw: list[dict] = []

    raw += _query_api_cached(cache, fonte_id, "crossref", query,
                              lambda: sources.search_crossref(session, query, CANDIDATES_PER_API))
    raw += _query_api_cached(cache, fonte_id, "openalex", query,
                              lambda: sources.search_openalex(session, query, CANDIDATES_PER_API))
    # Semantic Scholar richiede una API key: senza chiave risponde 429 in modo
    # sistematico e il backoff costa ~25s per fonte senza restituire nulla.
    # Disattivato di default; riattivabile con USE_SEMANTIC_SCHOLAR=1 quando
    # sara' disponibile una chiave.
    if os.environ.get("USE_SEMANTIC_SCHOLAR") == "1":
        raw += _query_api_cached(cache, fonte_id, "semanticscholar", query,
                                  lambda: sources.search_semanticscholar(session, query, CANDIDATES_PER_API))

    need_arxiv = (len(raw) == 0) or (source_year is not None and source_year >= ARXIV_YEAR_THRESHOLD)
    if need_arxiv:
        raw += _query_api_cached(cache, fonte_id, "arxiv", query,
                                  lambda: sources.search_arxiv(session, query, CANDIDATES_PER_API))

    scored = scoring.score_candidates(source_surname_norm, source_year, similarity_text, raw)
    stato, chosen, motivo = scoring.decide(scored)
    return stato, scored, motivo, chosen


# ---------------------------------------------------------------------------
# Fase 3: acquisizione del PDF
# ---------------------------------------------------------------------------

def peer_reviewed_from_type(type_str: str | None) -> str:
    if not type_str:
        return "n.d."
    t = type_str.lower()
    if any(k in t for k in ("journal-article", "proceedings-article", "book-chapter", "review-article", "journalarticle")):
        return "sì"
    if any(k in t for k in ("posted-content", "preprint", "working-paper")):
        return "no"
    return "n.d."


def acquire(session: PoliteSession, cache: SourceCache, fonte_id: str,
            chosen, dest_dir: Path, dry_run: bool) -> dict:
    """Fase 3. Ritorna un dict con tutti i valori da scrivere nell'Excel e
    lo stato finale ('scaricata' | 'paywall' | 'trovata').
    """
    c = chosen.candidate
    doi = c.get("doi")
    oa_pdf_url = c.get("oa_pdf_url")
    landing_url = c.get("url")
    is_oa = c.get("is_oa")

    if doi:
        unpaywall = _query_api_cached(
            cache, fonte_id, "unpaywall", doi,
            lambda: [sources.get_unpaywall(session, doi) or {}],
        )
        upw = unpaywall[0] if unpaywall else {}
        if upw:
            oa_pdf_url = oa_pdf_url or upw.get("pdf_url")
            landing_url = landing_url or upw.get("landing_url")
            if is_oa is None:
                is_oa = upw.get("is_oa")

    if not landing_url and doi:
        landing_url = f"https://doi.org/{doi}"

    values = {
        "M": c.get("title") or "",
        "N": c.get("type") or "",
        "O": c.get("venue") or "",
        "P": doi or "",
        "R": ("sì" if is_oa else "no") if is_oa is not None else "",
        "T": peer_reviewed_from_type(c.get("type")),
    }

    if oa_pdf_url:
        dest_path = dest_dir / f"{fonte_id}.pdf"
        if dry_run:
            log.info("  [dry-run] scaricherei %s -> %s", oa_pdf_url, dest_path)
            values["Q"] = oa_pdf_url
            values["S"] = str(dest_path)
            values["_stato_finale"] = "scaricata (simulata, dry-run)"
            values["L"] = "scaricata"
            return values
        ok, msg = download_pdf(session, oa_pdf_url, dest_path)
        if ok:
            values["Q"] = oa_pdf_url
            values["S"] = str(dest_path)
            values["L"] = "scaricata"
            values["_stato_finale"] = "scaricata"
            log.info("  download ok: %s", msg)
            return values
        log.warning("  download fallito (%s), tratto come non scaricato", msg)

    if landing_url:
        values["Q"] = landing_url
        values["S"] = ""
        values["L"] = "paywall"
        values["_stato_finale"] = "paywall"
        return values

    values["Q"] = ""
    values["S"] = ""
    values["L"] = "trovata"
    values["_stato_finale"] = "trovata"
    return values


# ---------------------------------------------------------------------------
# Orchestrazione
# ---------------------------------------------------------------------------

def process_fonte(session: PoliteSession, cache: SourceCache, sheet: excelio.ExcelSheet,
                   fonte_id: str, dest_dir: Path, dry_run: bool) -> dict:
    row = sheet.get_row_dict(fonte_id)
    autori = str(row.get("C") or "")
    anno_raw = row.get("D")
    query = str(row.get("I") or "").strip()
    contesto = str(row.get("J") or "")
    claim = str(row.get("K") or "")

    try:
        source_year = int(str(anno_raw).strip()) if anno_raw not in (None, "") else None
    except ValueError:
        source_year = None

    source_surname_norm = textutil.first_author_surname(autori)
    similarity_text = f"{contesto} {claim}".strip()

    if not query:
        query = f"{autori} {anno_raw}".strip()

    log.info("--- %s (%s, %s) --- query: %r", fonte_id, autori, anno_raw, query)

    stato, scored, motivo, chosen = resolve_identity(
        session, cache, fonte_id, query, source_surname_norm, source_year, similarity_text)

    result = {
        "id": fonte_id,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "n_candidati_dopo_filtro": len(scored),
        "stato_identita": stato,
        "motivo": motivo,
        "candidati_top": [
            {
                "titolo": s.candidate.get("title"),
                "autori": s.candidate.get("authors"),
                "anno": s.candidate.get("year"),
                "sede": s.candidate.get("venue"),
                "doi": s.candidate.get("doi"),
                "url": s.candidate.get("url"),
                "abstract": (s.candidate.get("abstract") or "")[:500] or None,
                "punteggio": round(s.composite, 4),
                "sim_score": round(s.sim_score, 4),
                "year_score": round(s.year_score, 4),
                "fonti_api": s.source_apis,
            }
            for s in scored[:MAX_CANDIDATES_IN_DISAMBIGUATION]
        ],
    }

    excel_values: dict = {}
    note_line = None
    today = dt.date.today().isoformat()

    if stato == "identificata":
        acq = acquire(session, cache, fonte_id, chosen, dest_dir, dry_run)
        stato_finale = acq.pop("_stato_finale")
        excel_values = acq
        result["stato_finale"] = stato_finale
        result["scelto"] = {
            "titolo": chosen.candidate.get("title"),
            "doi": chosen.candidate.get("doi"),
            "anno": chosen.candidate.get("year"),
            "punteggio": round(chosen.composite, 4),
        }
        apis = "+".join(chosen.source_apis)
        note_line = (f"[loop1 {today}] identita' risolta via {apis} (query: \"{query}\") "
                     f"-> {stato_finale}. {motivo}")
    elif stato == "ambigua":
        excel_values = {"L": "ambigua"}
        result["stato_finale"] = "ambigua"
        note_line = f"[loop1 {today}] ambigua: {motivo} (query: \"{query}\")"
    else:  # non_trovata
        excel_values = {"L": "non_trovata"}
        result["stato_finale"] = "non_trovata"
        note_line = f"[loop1 {today}] non trovata: {motivo} (query: \"{query}\")"

    result["excel_values"] = {k: v for k, v in excel_values.items()}
    result["note_appesa"] = note_line

    if dry_run:
        log.info("  [dry-run] scriverei: %s", excel_values)
        log.info("  [dry-run] appenderei a W: %s", note_line)
    else:
        sheet.write_fields(fonte_id, excel_values)
        sheet.append_note(fonte_id, note_line)
        sheet.save()
        log.info("  scritto e salvato per %s", fonte_id)

    return result


def write_report(results: list[dict], out_dir: Path) -> None:
    scaricate = [r for r in results if r.get("stato_finale") == "scaricata" or r.get("stato_finale", "").startswith("scaricata")]
    paywall = [r for r in results if r.get("stato_finale") == "paywall"]
    ambigue = [r for r in results if r.get("stato_finale") == "ambigua"]
    non_trovate = [r for r in results if r.get("stato_finale") == "non_trovata"]
    trovate = [r for r in results if r.get("stato_finale") == "trovata"]

    lines = ["# Loop 1 - Report recupero fonti", "",
             f"Generato: {dt.datetime.now().isoformat(timespec='seconds')}",
             f"Fonti processate in questo run: {len(results)}", "",
             f"- Scaricate: {len(scaricate)}",
             f"- Paywall (da aprire a mano): {len(paywall)}",
             f"- Trovate ma senza PDF/landing utile: {len(trovate)}",
             f"- Ambigue (serve disambiguazione umana): {len(ambigue)}",
             f"- Non trovate: {len(non_trovate)}", ""]

    lines.append("## Scaricate")
    lines.append("")
    for r in scaricate:
        lines.append(f"- **{r['id']}** ({r['query']}) - {r.get('scelto', {}).get('titolo', '')}")
    lines.append("")

    lines.append("## Paywall - da aprire manualmente")
    lines.append("")
    for r in paywall:
        url = r.get("excel_values", {}).get("Q", "")
        lines.append(f"- **{r['id']}**: {url}")
    lines.append("")

    lines.append("## Ambigue - servono candidati da disambiguare a mano")
    lines.append("")
    for r in ambigue:
        lines.append(f"- **{r['id']}** ({r['query']}) - {r['motivo']}")
    lines.append("")

    lines.append("## Non trovate")
    lines.append("")
    for r in non_trovate:
        lines.append(f"- **{r['id']}** ({r['query']}) - {r['motivo']}")
    lines.append("")

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")

    disambiguare = {
        r["id"]: {"query": r["query"], "motivo": r["motivo"], "candidati": r["candidati_top"]}
        for r in ambigue
    }
    (out_dir / "da_disambiguare.json").write_text(
        json.dumps(disambiguare, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("report scritto in %s", out_dir)


def append_log_jsonl(entry: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Loop 1 - Recupero fonti bibliografiche")
    p.add_argument("--excel", default=DEFAULT_EXCEL_PATH, help="percorso del file Excel (default: iTOC master.xlsx)")
    p.add_argument("--commit", action="store_true", help="scrive davvero nell'Excel e scarica i PDF (default: dry-run)")
    p.add_argument("--only", action="append", default=None, help="processa solo questo ID (ripetibile)")
    p.add_argument("--limit", type=int, default=None, help="ferma dopo N fonti")
    p.add_argument("--cache-dir", default=None, help="directory della cache API (default: <cartella excel>/loop1/cache)")
    p.add_argument("--out-dir", default=None, help="directory per report/log (default: <cartella excel>/loop1)")
    p.add_argument("--pdf-dir", default=None, help="directory di destinazione dei PDF (default: <cartella excel>/fonti def)")
    p.add_argument("--contact-email", default=DEFAULT_CONTACT_EMAIL)
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    excel_path = Path(args.excel)
    tesi_dir = excel_path.parent
    out_dir = Path(args.out_dir) if args.out_dir else tesi_dir / "loop1"
    cache_dir = Path(args.cache_dir) if args.cache_dir else out_dir / "cache"
    pdf_dir = Path(args.pdf_dir) if args.pdf_dir else tesi_dir / "fonti def"

    dry_run = not args.commit
    if dry_run:
        log.info("modalita' DRY-RUN: nessuna scrittura su Excel, nessun download. Usa --commit per farlo davvero.")
    else:
        log.info("modalita' COMMIT: scrivera' sull'Excel e scarichera' i PDF ad accesso aperto.")

    sheet = excelio.ExcelSheet(excel_path)
    if not dry_run:
        sheet.backup()
    sheet.open()

    if args.only:
        target_ids = [i for i in args.only]
        for i in target_ids:
            if i not in sheet.all_ids():
                log.error("ID '%s' non trovato nel foglio", i)
                return 2
    else:
        target_ids = [i for i in sheet.all_ids() if sheet.get_stato_acquisizione(i) == "da_cercare"]

    if args.limit is not None:
        target_ids = target_ids[: args.limit]

    log.info("fonti da processare in questo run: %d", len(target_ids))

    session = PoliteSession(contact_email=args.contact_email)
    cache = SourceCache(cache_dir)

    results = []
    for fonte_id in target_ids:
        try:
            r = process_fonte(session, cache, sheet, fonte_id, pdf_dir, dry_run)
        except Exception as exc:  # noqa: BLE001 - una fonte non deve far cadere il run
            log.exception("errore non gestito su %s: %s", fonte_id, exc)
            r = {"id": fonte_id, "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
                 "errore": str(exc)}
        results.append(r)
        append_log_jsonl(r, out_dir)

    write_report(results, out_dir)
    log.info("fine run. %d fonti processate.", len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
