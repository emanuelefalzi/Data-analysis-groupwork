---
name: paper-latex
description: Fase 5 - assembla il sorgente LaTeX dai DRAFT (citazioni biblatex-apa da fonti.bib, floats al primo richiamo), compila il PDF e controlla che il corpo stia in 20 pagine (references e Appendix A fuori conteggio). --bozza per un PDF di lavoro con i buchi visibili.
---

# /paper-latex [--bozza]

1. `python3 "<radice>/tools/assemble.py" --dry-run`: se rifiuta, l'elenco e' cio' che manca.
   Con buchi aperti o sezioni mancanti il gruppo puo' volere comunque una bozza: `--bozza`
   (i buchi escono in riquadri rossi).
2. `python3 "<radice>/tools/assemble.py" [--bozza]` → `latex/gen/` (derivato: non si tocca a mano;
   titolo, autori, preambolo stanno in `latex/main.tex` e `latex/preambolo.tex`, del gruppo).
3. `python3 "<radice>/tools/compila.py"` → `out/paper.pdf`. Controlla l'output:
   - **pagine del corpo ≤ 20**. Se sfora, **non tagliare tu**: proponi al gruppo le opzioni in
     ordine di costo (affiancare due figure; spostare un float a `escluso`; ridurre le parole
     di una sezione nel piano). Tagliare affermazioni lo decide il gruppo;
   - riferimenti o citazioni non risolti, overfull box larghi (tabelle troppo larghe);
   - parole per pagina misurate: se diverse da `parole_per_pagina`, proponi di ricalibrarlo.
4. Guarda il PDF (pdftoppm su 2–3 pagine con floats): un float lontano dal suo richiamo o una
   pagina mezza vuota si segnala.
5. Consegna: percorso del PDF, pagine del corpo, cosa resta aperto. La cartella `latex/` (con
   `gen/` e `figures/`) si carica cosi' com'e' su Overleaf.
