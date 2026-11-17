---
name: paper-floats
description: Rigenera figure e tabelle LaTeX (figures.zip, RTF del do-file) secondo input/piano.md e controlla le tabelle di testo in latex/testo/. Usala quando cambiano i risultati del do-file o il piano.
---

# /paper-floats

1. `python3 "<radice>/tools/floats.py"`: deve dire 35 floats nel corpo (21 figure, 14 tabelle).
2. Se il do-file ha cambiato numeri citati nelle tabelle di testo (`latex/testo/T7.tex`,
   `T13.tex`, `T14.tex`: ognuna dice in testa da quali righe del log vengono), aggiornale dal log
   e dillo. Le tabelle di testo seguono la scaletta: se la scaletta cambia una fonte o un
   segno, aggiorna anche T1, T2, T14.
3. Guarda un PNG per ogni coppia di figure se la didascalia è dubbia.
