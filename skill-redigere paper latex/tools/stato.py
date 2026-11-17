#!/usr/bin/env python3
"""stato.py — a che punto e' il paper e cosa viene dopo.

    python3 tools/stato.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, OUT, REPORTS, ROOT, cfg, conta_parole, draft_di, leggi_json, p  # noqa: E402


def main():
    c = cfg()
    print(f"# {c['titolo']}\n")
    for k in ("scaletta", "piano", "appendice_testo", "glossario", "bib", "figure_zip"):
        print(f"{'✓' if p(k).exists() else '✗'} {k}: {c[k]}")
    for alias, path in c["tabelle_rtf"].items():
        print(f"{'✓' if (ROOT / path).exists() else '✗'} tabelle_rtf[{alias}]: {path}")
    sez = leggi_json(BUILD / "sezioni.json")
    inv = leggi_json(BUILD / "floats.json")
    print()
    if sez is None:
        print("Prossimo passo: ROUTINE.md, passo 2")
        return
    if inv is None:
        print("Prossimo passo: python3 tools/floats.py  (tools/floats.py)")
        return
    senza = [f["id"] for f in inv if f["dove"] == "corpo" and f["tipo"] == "tabella-testo" and not f.get("tex")]
    if senza:
        print(f"⚠ tabelle di testo da scrivere: {', '.join(senza)}  (tools/floats.py)")
    scrivibili = [s for s in sez if s["contenuto"]]
    fatte = [s for s in scrivibili if draft_di(s["id"]) is not None]
    buchi = 0
    print(f"\nSezioni scritte: {len(fatte)}/{len(scrivibili)}  (+ abstract: {'sì' if draft_di('abstract') else 'no'})")
    for s in scrivibili:
        d = draft_di(s["id"])
        if d is None:
            continue
        b = len(re.findall(r"\[\[(?:GAP|CIT-NEEDED):", d))
        buchi += b
        print(f"  {s['id']:<6} {conta_parole(d):>5}/{s['parole']:<5} parole" + (f"  {b} buchi" if b else ""))
    report = sorted(x.name for x in REPORTS.glob("*.md")) if REPORTS.exists() else []
    print(f"\nBuchi aperti: {buchi}. Report: {', '.join(report) or 'nessuno'}")
    pdf = (ROOT / c["latex"]["pdf"]).resolve()
    print(f"PDF: {pdf if pdf.exists() else 'non ancora compilato'}")
    if len(fatte) < len(scrivibili):
        nxt = next(s for s in scrivibili if draft_di(s["id"]) is None)
        print(f"\nProssimo passo: stesura dalla sezione {nxt['id']} (ROUTINE.md, passo 3)")
    elif not draft_di("abstract"):
        print("\nProssimo passo: abstract (ROUTINE.md, passo 3)")
    elif not report:
        print("\nProssimo passo: controlli (ROUTINE.md, passo 4)")
    else:
        print("\nProssimo passo: LaTeX (ROUTINE.md, passo 5)")


if __name__ == "__main__":
    main()
