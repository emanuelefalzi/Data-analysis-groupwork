---
name: essay-glossario
description: Fase 5, facoltativa — glossario dei termini vincolanti, applicato poi da un linter a ogni sezione scritta. Consigliata quando l'essay costruisce concetti vicini che non sono sinonimi o supera ~3000 parole. Usala dopo la scaletta e prima di /essay-scrivi.
---

# /essay-glossario

Origine: il «mini-loop glossario» della tesi (`riferimenti-tesi/prompt-fonti/D - loop glossario.md`).

1. **Candidatura** (deterministica): `python3 "<radice>/tools/glossario/candidati.py"` → elenco di
   n-grammi con frequenza, sezioni, presenza nei titoli.
2. **Gruppi** (giudizio tuo, da mostrare all'autore): raggruppa i termini imparentati, quelli che
   rischiano di essere confusi (es. knowledge / expertise / capability). Per ciascun gruppo:
   `python3 "<radice>/tools/glossario/candidati.py" --gruppo <nome> "termine 1" "termine 2" …`
3. **Redazione, in parallelo**: un `redattore-glossario` per gruppo.
4. **Consolidamento**: `python3 "<radice>/tools/glossario/consolida.py"` (varianti simmetriche,
   definizione prima dell'uso), poi `python3 "<radice>/tools/glossario/lint.py" --autotest` (atteso 0).
5. Porta all'autore: i termini «usati ma non definiti» (buchi della scaletta: vanno definiti nel
   contenuto di una sezione) e le distinzioni piu' pericolose. Lui approva il glossario.

Da qui in poi `tools/stesura/verifica.py` applica il glossario a ogni sezione da solo.
