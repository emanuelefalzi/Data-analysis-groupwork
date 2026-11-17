---
name: paper-scrivi
description: Stesura - subagent paper-writer (model sonnet) su una sezione alla volta, in ordine di scaletta, con tools/verifica.py dopo ciascuna. /paper-scrivi <id> per una sezione, /paper-scrivi per tutte quelle mancanti (pilota 5.1), /paper-scrivi abstract alla fine.
---

# /paper-scrivi [<id>]

Esegui il passo 3 di `ROUTINE.md` (tutte le sezioni mancanti, o solo `<id>`). Sequenziale, mai
in parallelo; subagent sempre con `model: "sonnet"` esplicito; la prosa la corregge il writer,
non tu.
