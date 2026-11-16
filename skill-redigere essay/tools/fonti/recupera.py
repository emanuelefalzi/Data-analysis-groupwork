#!/usr/bin/env python3
"""Loop 1 - Recupero fonti.

Identifica ogni fonte elencata in `input/fonti.csv` (anche nota solo come
Autore, anno) tramite API bibliografiche gratuite, scarica il PDF quando e' ad
accesso aperto in `fonti/pdf/<id>.pdf`, e riporta tutto nel CSV.

Nato come loop 1 della tesi (che scriveva sul foglio 'Fonti' dell'Excel):
la logica di identificazione e punteggio e' identica, cambia solo l'I/O.

Uso tipico:
    python3 recupera.py                          # dry-run su tutte le fonti da_cercare
    python3 recupera.py --only agrawal2018        # debug su una sola fonte
    python3 recupera.py --limit 8                  # dry-run sulle prime 8
    python3 recupera.py --commit                   # scrive davvero nel CSV e scarica

Senza --commit lo script NON scrive nel CSV e NON scarica nulla: stampa
soltanto cosa farebbe. Vedi PROCESSO.md, fase 1.
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
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import comune  # noqa: E402
from lib import csvio, scoring, sources, textutil
from lib.cache import SourceCache
from lib.download import download_pdf
from lib.httpclient import PoliteSession

# L'email va nel "polite pool" di Crossref/OpenAlex/Unpaywall: si legge da
# progetto.json (campo "email_contatto"), non e' scritta qui.
DEFAULT_CONTACT_EMAIL = comune.config().get("email_contatto", "")
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
    """Fase 3. Ritorna un dict con tutti i valori da scrivere nel CSV e
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
        "titolo": c.get("title") or "",
        "tipo": c.get("type") or "",
        "sede": c.get("venue") or "",
        "doi": doi or "",
        "open_access": ("sì" if is_oa else "no") if is_oa is not None else "",
        "peer": peer_reviewed_from_type(c.get("type")),
    }

    if oa_pdf_url:
        dest_path = dest_dir / f"{fonte_id}.pdf"
        if dry_run:
            log.info("  [dry-run] scaricherei %s -> %s", oa_pdf_url, dest_path)
            values["url"] = oa_pdf_url
            values["pdf_locale"] = comune.rel(dest_path)
            values["_stato_finale"] = "scaricata (simulata, dry-run)"
            values["stato"] = "scaricata"
            return values
        ok, msg = download_pdf(session, oa_pdf_url, dest_path)
        if ok:
            values["url"] = oa_pdf_url
            values["pdf_locale"] = comune.rel(dest_path)
            values["stato"] = "scaricata"
            values["_stato_finale"] = "scaricata"
            log.info("  download ok: %s", msg)
            return values
        log.warning("  download fallito (%s), tratto come non scaricato", msg)

    if landing_url:
        values["url"] = landing_url
        values["pdf_locale"] = ""
        values["stato"] = "paywall"
        values["_stato_finale"] = "paywall"
        return values

    values["url"] = ""
    values["pdf_locale"] = ""
    values["stato"] = "trovata"
    values["_stato_finale"] = "trovata"
    return values


# ---------------------------------------------------------------------------
# Orchestrazione
# ---------------------------------------------------------------------------

def process_fonte(session: PoliteSession, cache: SourceCache, sheet: csvio.FontiCSV,
                   fonte_id: str, dest_dir: Path, dry_run: bool) -> dict:
    row = sheet.get(fonte_id)
    autori = row.get("autori") or ""
    anno_raw = row.get("anno")
    query = (row.get("query") or "").strip()
    contesto = row.get("contesto") or ""
    claim = ""

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

    valori_csv: dict = {}
    note_line = None
    today = dt.date.today().isoformat()

    if stato == "identificata":
        acq = acquire(session, cache, fonte_id, chosen, dest_dir, dry_run)
        stato_finale = acq.pop("_stato_finale")
        valori_csv = acq
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
        valori_csv = {"stato": "ambigua"}
        result["stato_finale"] = "ambigua"
        note_line = f"[loop1 {today}] ambigua: {motivo} (query: \"{query}\")"
    else:  # non_trovata
        valori_csv = {"stato": "non_trovata"}
        result["stato_finale"] = "non_trovata"
        note_line = f"[loop1 {today}] non trovata: {motivo} (query: \"{query}\")"

    result["valori_csv"] = {k: v for k, v in valori_csv.items()}
    result["note_appesa"] = note_line

    if dry_run:
        log.info("  [dry-run] scriverei: %s", valori_csv)
        log.info("  [dry-run] appenderei alle note: %s", note_line)
    else:
        sheet.write_fields(fonte_id, valori_csv)
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
        url = r.get("valori_csv", {}).get("url", "")
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
    p.add_argument("--csv", default=str(comune.FONTI_CSV), help="elenco fonti (default: input/fonti.csv)")
    p.add_argument("--commit", action="store_true", help="scrive davvero nel CSV e scarica i PDF (default: dry-run)")
    p.add_argument("--only", action="append", default=None, help="processa solo questo ID (ripetibile)")
    p.add_argument("--limit", type=int, default=None, help="ferma dopo N fonti")
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
    if not args.contact_email:
        log.error("manca l'email di contatto: mettila in progetto.json come \"email_contatto\" "
                  "(serve al polite pool delle API) oppure passa --contact-email")
        return 2

    out_dir = comune.FONTI / "recupero"
    cache_dir = out_dir / "cache"
    pdf_dir = comune.PDF_DIR
    pdf_dir.mkdir(parents=True, exist_ok=True)

    dry_run = not args.commit
    if dry_run:
        log.info("modalita' DRY-RUN: nessuna scrittura sul CSV, nessun download. Usa --commit per farlo davvero.")
    else:
        log.info("modalita' COMMIT: scrivera' sul CSV e scarichera' i PDF ad accesso aperto.")

    sheet = csvio.FontiCSV(Path(args.csv))
    if not dry_run:
        sheet.backup()
    sheet.open()

    if args.only:
        target_ids = list(args.only)
        for i in target_ids:
            if i not in sheet.all_ids():
                log.error("ID '%s' non trovato nel CSV", i)
                return 2
    else:
        target_ids = [i for i in sheet.all_ids() if sheet.stato(i) == "da_cercare"]

    if args.limit is not None:
        target_ids = target_ids[: args.limit]

    log.info("fonti da processare in questo run: %d", len(target_ids))

    session = PoliteSession(contact_email=args.contact_email, user_agent_app="essay-recupero")
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
