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
    for k in ("scaletta", "piano", "appendice", "bib", "validazione_fonti", "figure_zip", "tabelle_rtf"):
        print(f"{'✓' if p(k).exists() else '✗'} {k}: {c[k]}")
    piano_txt = p("piano").read_text(encoding="utf-8") if p("piano").exists() else ""
    if "PROPOSTA" in piano_txt[:600]:
        print("⚠ input/piano.md e' ancora una PROPOSTA: pagine e floats non approvati dal gruppo")
    sez = leggi_json(BUILD / "sezioni.json")
    inv = leggi_json(BUILD / "floats.json")
    print()
    if sez is None:
        print("Prossimo passo: python3 tools/leggi_scaletta.py  (/paper-avvio)")
        return
    if inv is None:
        print("Prossimo passo: python3 tools/floats.py  (/paper-floats)")
        return
    senza = [f["id"] for f in inv if f["dove"] == "corpo" and f["tipo"] == "tabella-testo" and not f.get("tex")]
    if senza:
        print(f"⚠ tabelle di testo da scrivere: {', '.join(senza)}  (/paper-floats)")
    app_vuota = [s["id"] for s in sez if s.get("appendice") and not s["contenuto"] and "." in s["id"]]
    if app_vuota:
        print(f"⚠ appendice senza contenuto: {', '.join(app_vuota)}  (/paper-appendice)")
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
    pdf = OUT / Path(c["latex"]["pdf"]).name
    print(f"PDF: {'out/' + pdf.name if pdf.exists() else 'non ancora compilato'}")
    if len(fatte) < len(scrivibili):
        nxt = next(s for s in scrivibili if draft_di(s["id"]) is None)
        print(f"\nProssimo passo: /paper-scrivi {nxt['id']}")
    elif not draft_di("abstract"):
        print("\nProssimo passo: /paper-scrivi abstract")
    elif not report:
        print("\nProssimo passo: /paper-controlla")
    else:
        print("\nProssimo passo: /paper-latex")


if __name__ == "__main__":
    main()
