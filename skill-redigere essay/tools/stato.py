#!/usr/bin/env python3
"""A che punto e' il progetto. Sola lettura, non modifica nulla.

Guarda ogni fase nell'ordine del processo (PROCESSO.md) e dice, per ciascuna,
cosa c'e' e qual e' il prossimo passo. E' il primo comando da lanciare quando si
riapre il progetto in una chat nuova.

Uso:
    python3 tools/stato.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comune  # noqa: E402


def conta(cartella: Path, pattern="*.json") -> int:
    return len(list(cartella.glob(pattern))) if cartella.exists() else 0


def main() -> int:
    cfg = comune.config()
    prossimo = None
    print(f"# Stato — {cfg.get('titolo') or comune.ROOT.name}\n")

    def riga(ok, fase, dettaglio, passo):
        nonlocal prossimo
        print(f"{'✓' if ok else '·'} {fase:<22} {dettaglio}")
        if not ok and prossimo is None:
            prossimo = passo

    riga(comune.PROGETTO.exists() and bool(cfg.get("titolo")), "0 progetto.json",
         f"lingua {cfg['lingua']}, {cfg['parole_totali'] or '?'} parole", "compila progetto.json")
    dom = comune.domande_dal_brief()
    riga(comune.BRIEF.exists() and bool(dom), "0 brief", f"{len(dom)} domande per le fonti",
         "scrivi input/brief.md con la sezione «Domande per le fonti»")
    tmpl = comune.ROOT / cfg["template_docx"]
    riga(tmpl.exists(), "0 template Word", cfg["template_docx"] + ("" if tmpl.exists() else " — MANCA"),
         "chiedi il template Word all'autore e mettilo in " + cfg["template_docx"])

    n_csv, stati = 0, {}
    if comune.FONTI_CSV.exists():
        sys.path.insert(0, str(comune.ROOT / "tools" / "fonti"))
        from lib.csvio import FontiCSV
        c = FontiCSV(comune.FONTI_CSV); c.open()
        n_csv = len(c.all_ids())
        for i in c.all_ids():
            stati[c.stato(i)] = stati.get(c.stato(i), 0) + 1
    riga(n_csv > 0 and not stati.get("da_cercare"), "1 recupero fonti",
         f"{n_csv} fonti · " + ", ".join(f"{k} {v}" for k, v in sorted(stati.items())),
         "skill essay-fonti (recupera.py, poi i paywall a mano)")
    n_pdf, n_txt = conta(comune.PDF_DIR, "*.pdf"), conta(comune.TESTI, "*.txt")
    riga(n_txt > 0, "1 testi congelati", f"{n_pdf} PDF · {n_txt} testi", "tools/fonti/estrai_testi.py")
    from bib import leggi_bib
    n_bib = len(leggi_bib(comune.BIB)) if comune.BIB.exists() else 0
    riga(n_bib > 0, "1 fonti.bib", f"{n_bib} voci", "tools/fonti/genera_bib.py --commit, poi rileggi")

    n_sch, n_nlm = conta(comune.SCHEDE), conta(comune.SCHEDE_NLM)
    est = json.loads(comune.ESTRATTI_JSON.read_text(encoding="utf-8")) if comune.ESTRATTI_JSON.exists() else None
    riga(est is not None and not est.get("rifiutate") and n_sch >= n_txt, "2 estrazione",
         f"{n_sch} schede A · {n_nlm} schede NLM · "
         + (f"{len(est['punti'])} punti validi, {len(est['rifiutate'])} schede rifiutate" if est else "non validata"),
         "skill essay-estrai (lettori in parallelo, poi tools/fonti/valida.py)")
    n_int = conta(comune.INTERMEDI / "schede", "*.md")
    n_sin = conta(comune.INTERMEDI, "sintesi-*.md")
    riga(n_int > 0, "3 intermedi", f"{n_int} schede leggibili · {n_sin} sintesi per domanda",
         "skill essay-intermedi")

    sez = None
    if comune.SEZIONI_JSON.exists():
        sez = comune.sezioni()
    riga(sez is not None, "4 scaletta", f"{len(sez)} sezioni" if sez else "non letta",
         "skill essay-scaletta (con l'autore), poi tools/scaletta/leggi_scaletta.py")
    riga(comune.GLOSSARIO.exists(), "5 glossario", "presente" if comune.GLOSSARIO.exists() else
         "assente (facoltativo)", None)
    if sez:
        attive = [k for k, v in sez.items() if not v["escludi"]]
        scritte = [k for k in attive if comune.draft_di(k)]
        parole = sum(comune.parole_come_nel_word(comune.draft_di(k)) for k in scritte)
        buchi = sum(len(comune.TOKEN_BUCO.findall(comune.draft_di(k))) for k in scritte)
        riga(len(scritte) == len(attive), "6 stesura",
             f"{len(scritte)}/{len(attive)} sezioni · {parole} parole · {buchi} buchi dichiarati",
             f"skill essay-scrivi (prossima: {next((k for k in attive if not comune.draft_di(k)), '-')})")
        rep = sorted(comune.REPORTS.glob("claim-*.md"))
        riga(bool(rep), "7 controlli", f"{len(rep)} report claim-auditor", "skill essay-controlla")
    out = comune.ROOT / cfg["output_docx"]
    riga(out.exists(), "8 Word", comune.rel(out) if out.exists() else "non assemblato", "skill essay-word")

    print(f"\nProssimo passo: {prossimo or 'rilettura dell autore del Word finale'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
