---
name: paper-floats
description: Rigenera figure e tabelle LaTeX (figures.zip, RTF del do-file) secondo input/piano.md e controlla le tabelle di testo in latex/testo/. Usala quando cambiano i risultati del do-file o il piano.
---

# /paper-floats

1. `python3 "<radice>/tools/floats.py"`: deve dire 35 floats nel corpo (21 figure, 14 tabelle).
2. `python3 "<radice>/tools/tabelle_testo.py"`: costruisce e controlla le tabelle testuali di
   `4. risultati/tables testuali/` (una fonte per cella). Se fallisce, correggi il `.md`, mai
   togliendo una fonte; se la scaletta cambia una fonte o un segno, aggiorna T1, T2, T14.
3. Guarda un PNG per ogni coppia di figure se la didascalia è dubbia.
