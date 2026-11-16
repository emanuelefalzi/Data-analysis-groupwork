#!/usr/bin/env python3
"""compila.py — compila latex/main.tex e controlla il limite di pagine del corpo.

    python3 tools/compila.py

latexmk (pdflatex + biber) in build/latex/, PDF copiato in out/paper.pdf. Poi:
- pagine del corpo = pagina della label `corpo-fine` (il corpo parte da pagina 1, con titolo e
  abstract); deve essere <= pagine_corpo_max;
- riferimenti o citazioni non risolti, chiavi bib mancanti, overfull box > 10pt;
- parole per pagina misurate (per ricalibrare `parole_per_pagina` in progetto.json).
Esce con 1 se il corpo supera il limite o restano riferimenti non risolti.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, LATEX, OUT, cfg, conta_parole, die, draft_di, leggi_json  # noqa: E402


def main():
    if not shutil.which("latexmk"):
        die("latexmk non trovato. Su Debian/Ubuntu: apt-get install texlive-latex-extra "
            "texlive-bibtex-extra biber latexmk")
    c = cfg()
    if not (LATEX / "gen" / "corpo.tex").exists():
        die("manca latex/gen/corpo.tex: lancia prima tools/assemble.py")
    outdir = BUILD / "latex"
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = ["latexmk", "-pdf", "-g", "-interaction=nonstopmode", "-halt-on-error",
           f"-outdir={outdir}", "main.tex"]
    r = subprocess.run(cmd, cwd=LATEX, capture_output=True, text=True, timeout=600)
    log = (outdir / "main.log").read_text(encoding="utf-8", errors="ignore") if (outdir / "main.log").exists() else ""
    if r.returncode != 0:
        err = re.findall(r"^! .*(?:\n.*){0,3}", log, re.M)
        print("\n".join(err[:5]) or r.stdout[-2000:])
        die("compilazione fallita (log completo: build/latex/main.log)")
    pdf = outdir / "main.pdf"
    OUT.mkdir(exist_ok=True)
    dest = OUT / Path(c["latex"]["pdf"]).name
    shutil.copy(pdf, dest)

    aux = (outdir / "main.aux").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\\newlabel\{corpo-fine\}\{\{[^}]*\}\{(\d+)\}", aux)
    corpo = int(m.group(1)) if m else None
    tot = None
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    mt = re.search(r"Pages:\s+(\d+)", info.stdout)
    if mt:
        tot = int(mt.group(1))

    problemi = []
    if re.search(r"There were undefined references|Reference `[^']+' on page \d+ undefined", log):
        problemi.append("riferimenti non risolti: " + ", ".join(sorted(set(re.findall(r"Reference `([^']+)'", log)))))
    blg = outdir / "main.blg"
    if blg.exists():
        mancanti = re.findall(r"I didn't find a database entry for '([^']+)'", blg.read_text(errors="ignore"))
        if mancanti:
            problemi.append("chiavi assenti dal .bib: " + ", ".join(sorted(set(mancanti))))
    if re.search(r"Citation '[^']+' .*undefined", log):
        problemi.append("citazioni non risolte")
    overfull = [float(x) for x in re.findall(r"Overfull \\hbox \((\d+\.?\d*)pt too wide\)", log)]
    grossi = [x for x in overfull if x > 10]

    sezioni = leggi_json(BUILD / "sezioni.json") or []
    parole = sum(conta_parole(draft_di(s["id"]) or "") for s in sezioni if not s.get("appendice"))
    print(f"PDF: {dest}")
    print(f"Pagine del corpo: {corpo} (max {c['pagine_corpo_max']}); totale con references e appendice: {tot}")
    if corpo:
        print(f"Prosa del corpo: {parole} parole, {parole / corpo:.0f} per pagina floats compresi "
              f"(piano: {c['parole_per_pagina']} di sola prosa)")
    if grossi:
        print(f"⚠ {len(grossi)} overfull hbox oltre 10pt (il piu' largo {max(grossi):.0f}pt): tabelle o URL da sistemare")
    for x in problemi:
        print("⚠", x)
    fallito = bool(problemi)
    if corpo is None:
        print("⚠ label corpo-fine non trovata: main.tex e' stato modificato?")
        fallito = True
    elif corpo > c["pagine_corpo_max"]:
        print(f"✗ Il corpo supera il limite di {corpo - c['pagine_corpo_max']} pagine: si taglia "
              "(floats o parole), e i tagli di affermazioni li decide il gruppo.")
        fallito = True
    sys.exit(1 if fallito else 0)


if __name__ == "__main__":
    main()
