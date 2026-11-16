---
name: essay-estrai
description: Fase 2, loop 2 — estrazione per domande. Per ogni fonte con testo, un lettore Sonnet in contesto pulito estrae cio' che risponde alle domande del brief, ogni punto con citazione verbatim; facoltativo un secondo lettore NotebookLM; uno script valida tutto e produce build/estratti.json. Usala dopo /essay-fonti o quando cambiano le domande o arrivano fonti nuove.
---

# /essay-estrai

Origine: il loop 2 della tesi (doppio lettore + validatore unico), girato da «verifica di claim
gia' scritti» a «estrazione per domande». Vedi `PROCESSO.md`, fase 2.

1. `python3 "<radice>/tools/fonti/prepara.py"` → un task per fonte in `fonti/task/`. Se dice che
   non ci sono domande, fermati: vanno scritte nel brief.
2. **Lettore A, in parallelo**: un subagent `lettore-fonti` per fonte, tutti nello stesso messaggio
   (fino a ~6-8 per volta). Prompt a ciascuno: «Leggi il task `<radice>/fonti/task/<id>.json` e
   applica il tuo contratto». Nessun lettore vede gli altri.
3. **Secondo lettore** (solo se `secondo_lettore_nlm` e' true in `progetto.json`): le fonti devono
   essere caricate nel notebook `notebook_nlm`. Un `secondo-lettore-nlm` per fonte, **dopo** che il
   lettore A di quella fonte ha finito, senza passargli la scheda A.
4. `python3 "<radice>/tools/fonti/valida.py"` → `build/estratti.json` + `reports/estrazione.md`.
   - **schede rifiutate intere** (chiavi sbagliate, domande non coperte, `cosa_ho_cercato` scarno):
     si rilancia il lettore su quella fonte, dandogli gli errori del validatore;
   - **punti scartati** (citazione non ritrovata, numero assente, front matter): se una domanda
     resta scoperta per uno scarto, rilancia il lettore con l'errore; altrimenti lo scarto resta;
   - **«solo NLM»**: il secondo lettore ha trovato con citazione riscontrata cio' che A dichiara
     assente. Non decidi tu: rilanci A su quella domanda, o lo porti all'autore.
5. Ripeti 2-4 sulle sole fonti da rifare finche' il report non ha schede rifiutate.

Mai: correggere a mano una citazione perche' passi il validatore; scrivere tu una scheda al
posto del lettore; abbassare le soglie del validatore.

Chiudi con la copertura per domanda (dal report) e le domande scoperte: sono il primo dato utile
per l'autore. Prossima fase: `/essay-intermedi`.
