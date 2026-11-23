#!/usr/bin/env python3
"""compila.py — compila il paper e controlla il limite di pagine del corpo.

    python3 tools/compila.py

Portabile: non usa latexmk ne' pdfinfo. Copia `latex/` in `build/latex/` e lancia
pdflatex → biber (o bibtex, secondo `latex/gen/bib.tex`) → pdflatex → pdflatex. Funziona con
TeX Live (Linux), MacTeX/BasicTeX (Mac) e MiKTeX (Windows), purche' `pdflatex` sia nel PATH.
Poi:
- pagine del corpo = pagina della label `corpo-fine` (il corpo parte da pagina 1, con titolo e
  abstract); deve essere <= pagine_corpo_max;
- riferimenti o citazioni non risolti, chiavi bib mancanti, overfull box > 10pt;
- parole per pagina misurate (per ricalibrare `parole_per_pagina` in progetto.json).
Il PDF va dove dice progetto.json (latex.pdf). Esce con 1 se il corpo sfora o restano errori.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, LATEX, ROOT, cfg, conta_parole, die, draft_di, leggi_json  # noqa: E402


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="ignore", timeout=600)


def main():
    tectonic = not shutil.which("pdflatex") and shutil.which("tectonic")
    if not shutil.which("pdflatex") and not tectonic:
        die("pdflatex non trovato: installa una distribuzione LaTeX (vedi LEGGIMI.md, Requisiti)")
    if tectonic:
        print("pdflatex assente: compilo con tectonic (bibtex incluso)")
    c = cfg()
    if not (LATEX / "gen" / "corpo.tex").exists():
        die("manca latex/gen/corpo.tex: lancia prima tools/assemble.py")
    wd = BUILD / "latex"
    if wd.exists():
        shutil.rmtree(wd)
    shutil.copytree(LATEX, wd)
    backend = "biber" if "backend: biber" in (wd / "gen" / "bib.tex").read_text() else "bibtex"
    if not tectonic and not shutil.which(backend):
        die(f"{backend} non trovato nel PATH")
    pdflatex = (["tectonic", "--keep-logs", "--keep-intermediates", "main.tex"] if tectonic
                else ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    passi = (pdflatex,) if tectonic else (pdflatex, [backend, "main"], pdflatex, pdflatex)
    for passo in passi:
        r = run(passo, wd)
        if r.returncode != 0 and passo is pdflatex:
            log = (wd / "main.log").read_text(errors="ignore") if (wd / "main.log").exists() else r.stdout
            err = re.findall(r"^! .*(?:\n.*){0,3}", log, re.M)
            print("\n".join(err[:5]) or log[-2000:])
            die("compilazione fallita (log completo: build/latex/main.log)")
        if r.returncode != 0:
            print(f"⚠ {backend} ha segnalato errori:\n{r.stdout[-1500:]}")
    log = (wd / "main.log").read_text(errors="ignore")
    dest = (ROOT / c["latex"]["pdf"]).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(wd / "main.pdf", dest)

    aux = (wd / "main.aux").read_text(errors="ignore")
    m = re.search(r"\\newlabel\{corpo-fine\}\{\{[^}]*\}\{(\d+)\}", aux)
    corpo = int(m.group(1)) if m else None
    mt = re.search(r"Output written on main\.pdf \((\d+) page", log)
    tot = int(mt.group(1)) if mt else None
    if tot is None and shutil.which("pdfinfo"):
        mi = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", "main.pdf"], wd).stdout)
        tot = int(mi.group(1)) if mi else None

    problemi = []
    nonris = sorted(set(re.findall(r"Reference `([^']+)' on page \d+ undefined", log)))
    if nonris:
        problemi.append("riferimenti non risolti: " + ", ".join(nonris))
    cit = sorted(set(re.findall(r"Citation `?'?([^'` ]+)'? (?:on page \d+ )?undefined", log)))
    if cit:
        problemi.append("citazioni non risolte: " + ", ".join(cit))
    for blg in ("main.blg",):
        if (wd / blg).exists():
            mancanti = re.findall(r"(?:I didn't find a database entry for|entry) ['\"]([^'\"]+)['\"]",
                                  (wd / blg).read_text(errors="ignore"))
            if mancanti:
                problemi.append("chiavi assenti dal .bib: " + ", ".join(sorted(set(mancanti))))
    for tipo, fid, num in re.findall(r"\\newlabel\{(tab|fig):[TF](\d+)\}\{\{(\d+)\}", aux):
        if fid != num:                    # T7 deve uscire come Table 7, come nel paper v4
            problemi.append(f"{tipo} {fid} del paper v4 esce con il numero {num}: controllare l'ordine dei richiami")
    overfull = [float(x) for x in re.findall(r"Overfull \\hbox \((\d+\.?\d*)pt too wide\)", log)]
    grossi = [x for x in overfull if x > 10]

    sezioni = leggi_json(BUILD / "sezioni.json") or []
    parole = sum(conta_parole(draft_di(s["id"]) or "") for s in sezioni)
    print(f"PDF: {dest}")
    print(f"Pagine del corpo: {corpo} (max {c['pagine_corpo_max']}); totale con references e appendice: {tot}")
    print(f"Bibliografia: {backend}")
    if corpo and parole:
        print(f"Prosa del corpo: {parole} parole su {corpo} pagine floats compresi "
              f"(piano: {c['parole_per_pagina']} parole per pagina di sola prosa)")
    if grossi:
        print(f"⚠ {len(grossi)} overfull hbox oltre 10pt (il piu' largo {max(grossi):.0f}pt)")
    for x in problemi:
        print("⚠", x)
    fallito = bool(problemi)
    if corpo is None:
        print("⚠ label corpo-fine non trovata: main.tex e' stato modificato?")
        fallito = True
    elif corpo > c["pagine_corpo_max"]:
        print(f"✗ Il corpo supera il limite di {corpo - c['pagine_corpo_max']} pagine: si riduce la "
              "prosa nel piano (input/piano.md), i floats restano tutti.")
        fallito = True
    sys.exit(1 if fallito else 0)


if __name__ == "__main__":
    main()
