# Red team su loop2/scrivi.py — proposte di validazione (non implementate)

Contesto: 6 JSON avversariali costruiti a mano contro 3 coppie reali (`0.2.2__brynjolfsson2021`,
`1__agrawal2018`, `1__chokimkim2026`) sono stati eseguiti contro `scrivi.py` in dry-run. **Tutti e 6
sono passati** (nessuno scartato). Le difese immediate sono andate nel prompt (vedi
`A - lettore ESEGUIBILE.md`, regole 7 e 11, e i nuovi punti 6-9 dell'AUTOCONTROLLO). Qui propongo
solo le difese che il prompt non può dare da solo perché richiedono confronto meccanico con dati
che il subagent non rilegge da sé.

## V1 — Coerenza con l'ATTRIBUZIONE INCERTA del task originale (priorità alta)

**Buco**: `scrivi.py` valida il JSON del subagent isolatamente. Non legge mai
`pipeline/loop2/task/<nodo>__<id_fonte>.json`, quindi non può accorgersi che il `claim` di origine iniziava
con `ATTRIBUZIONE INCERTA:` — un caso in cui la regola 7 vieta esplicitamente `esito: "usabile"`.
Ho verificato empiricamente (attacco A4) che un `usabile` su un claim così flaggato passa senza
alcun avviso.

**Criterio**: in `valida_a`, se esiste `pipeline/loop2/task/<nodo>__<id_fonte>.json` e il suo campo `claim`
inizia con `ATTRIBUZIONE INCERTA:`, allora:
- `esito` non può essere `"usabile"` (altrimenti scarto con errore esplicito);
- `note` deve iniziare con la stringa `ATTRIBUZIONE INCERTA:` (altrimenti scarto).

Costo: una lettura file in più per riga, nessun falso positivo prevedibile (la condizione è binaria
e il campo `claim` non cambia dopo la generazione del task).

## V2 — Blocklist per citazioni da "front matter" (priorità media)

**Buco**: `quote_presente()` controlla solo che la stringa esista nel testo sorgente, non che
appartenga al corpo argomentativo. Un `citazione_verbatim` vera ma presa da ringraziamenti,
finanziamento, affiliazioni o nota di copyright passa senza problemi (attacco A1).

**Criterio**: prima di accettare la citazione per `usabile`/`da riformulare`, verificare che non
matchi un pattern da un piccolo blocklist regex case-insensitive, es.:
`r"\b(we thank|financial relationship|all rights reserved|copyright|correspondence to|nber working papers? are circulated|jel no|working paper no)\b"`.
Se matcha, scarto con messaggio "citazione da front-matter, non da corpo argomentativo — verificare
a mano". Basso rischio di falsi positivi: sono frasi tipiche del boilerplate NBER/rivista che quasi
mai contengono l'argomento sostanziale di un claim.

## V3 — Simmetria fra `valida_a` e `valida_b` (già segnalato in REVISIONE.md §6, lo confermo)

`valida_b` non chiama mai `quote_presente()` sulla citazione del lettore NotebookLM prima del
controllo — lo fa solo indirettamente per declassare l'esito. Nessun attacco nuovo di questa sessione
lo riguarda direttamente (ho testato solo il lettore A), ma è la stessa famiglia di buco di V1/V2 e
vale la pena chiuderlo nello stesso giro di modifiche.

## Cosa NON propongo

- Un controllo automatico di "pertinenza semantica" fra `citazione_verbatim` e `cosa_dice_davvero`
  (paraphrase-of-claim, attacco A2; lit-review misattribution, attacco A3; mentions-only, attacco A5):
  richiederebbe NLP/giudizio, non un criterio meccanico — l'ho lasciato al prompt (regole 7/11,
  AUTOCONTROLLO 6-9) e alla revisione umana a campione, non a `scrivi.py`.
- Un controllo automatico sulla scappatoia `non verificabile` (attacco A6): non c'è modo economico
  di distinguere meccanicamente una rinuncia pigra da una legittima senza rileggere la fonte — ho
  rinforzato solo la dichiarazione richiesta in `note` lato prompt.
