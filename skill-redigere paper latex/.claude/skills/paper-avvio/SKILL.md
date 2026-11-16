---
name: paper-avvio
description: Fase 0-1 del paper LaTeX - controlla requisiti (LaTeX, LibreOffice, file della repo), legge scaletta.md e il piano delle pagine, e dice cosa manca prima di scrivere. Usala per prima, o quando scaletta.md o input/piano.md cambiano.
---

# /paper-avvio

`<radice>` = la cartella `skill-redigere paper latex/` (quella con `progetto.json`).

1. Requisiti. Se manca qualcosa, dillo e fermati (in una sessione cloud si installa con apt):
   - `latexmk`, `pdflatex`, `biber` → `apt-get install -y texlive-latex-recommended
     texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra biber latexmk lmodern`;
   - `soffice` (LibreOffice) per leggere `RQ1_tables.doc`; `pdftotext` per l'appendice.
2. `python3 "<radice>/tools/stato.py"`: i file di input esistono?
3. `python3 "<radice>/tools/piano.py"`: il piano sta in `pagine_corpo_max`? Se no, **non
   correggerlo tu**: mostra al gruppo di quanto sfora e quali sezioni o floats pesano di piu'.
4. `python3 "<radice>/tools/leggi_scaletta.py"` → `build/sezioni.json`. Riporta all'utente, con
   il contesto completo (RULES.md: niente ID nudi):
   - fonti nominate dalla scaletta ma non citabili (non in `fonti.bib`, esito «non usabile»,
     «solo rimando», nessuna riga di validazione per quella sezione);
   - sezioni corte (poco materiale per le parole del piano) e sezioni senza contenuto.
5. Ricorda gli stati: se `scaletta.md` o `input/piano.md` dicono ancora «DRAFT»/«PROPOSTA»,
   la stesura e' possibile solo come bozza di lavoro; decide il gruppo.

Prossima fase: `/paper-floats`.
