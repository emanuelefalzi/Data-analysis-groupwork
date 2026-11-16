---
name: paper-stato
description: Dice a che punto e' il paper LaTeX (input, floats, sezioni scritte, buchi, PDF, pagine) e qual e' il prossimo passo.
---

# /paper-stato

`python3 "<radice>/tools/stato.py"` e riporta l'output all'utente, spiegando per esteso i
problemi segnalati (niente ID nudi). Se c'e' un PDF, aggiungi le pagine del corpo da
`python3 "<radice>/tools/compila.py"` solo se l'utente lo chiede (ricompila).
