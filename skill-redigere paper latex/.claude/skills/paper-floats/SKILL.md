---
name: paper-floats
description: Fase 2 - prepara figure (figures.zip) e tabelle (RQ1_tables.doc) in LaTeX secondo input/piano.md, e scrive le tabelle di testo (ipotesi, campione, verdetti) dalla scaletta. Usala dopo /paper-avvio e ogni volta che cambia il piano dei floats.
---

# /paper-floats

1. `python3 "<radice>/tools/floats.py"`: estrae i PNG in `build/figures/`, converte le 6
   tabelle del do-file in `build/tabelle/t<n>.tex` (forma compatta: i dummy del lead investor
   diventano una riga «Yes»; **nessuna cella ricalcolata**), scrive `build/floats.json`.
2. Guarda almeno una tabella generata e un PNG per float `corpo` con didascalia incerta
   (piano, decisione P4): la didascalia deve descrivere cio' che il grafico mostra davvero.
   Se non torna, proponi la correzione al gruppo; non cambiare il piano da solo.
3. **Tabelle di testo** (`tipo = tabella-testo`, es. x1 ipotesi, x3 campione, x13 verdetti):
   se il file in `latex/tabelle-testo/<id>.tex` manca, scrivilo tu **solo** dal materiale della
   scaletta della sezione di casa (e, per i numeri del campione, dalla tabella di
   `construction.pdf` che la scaletta cita). Ambiente `table` con `\caption{}` e
   `\label{tab:<id>}`, booktabs. Verdetti con le parole esatte del paper. Ogni cella che non
   sai riempire dal materiale: `\buco{...}`. Poi mostrala al gruppo: entra solo approvata.
4. Riporta: floats nel corpo, spazio stimato (`tools/piano.py`), floats del piano senza file.

Prossima fase: `/paper-appendice` (se l'appendice e' vuota) o `/paper-scrivi`.
