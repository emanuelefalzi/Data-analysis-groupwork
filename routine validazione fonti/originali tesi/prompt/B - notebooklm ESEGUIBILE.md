# Prompt B — Secondo lettore su NotebookLM (ESEGUIBILE)

Serve ad avere **due letture indipendenti** della stessa fonte sullo stesso claim. Dove i due lettori concordano il dato è solido; dove divergono decide la persona.

Strato metodologico completo in `pipeline/prompt/B - secondo lettore notebooklm.md`, da leggere prima di iniziare. Se quel file e questo divergono sul formato di output, vince sempre questo file: la sua sezione «CONTRATTO DI OUTPUT» descrive un formato precedente (`lettura`/`fonte_citata`/`sufficiente`) superato dal contratto qui sotto (`esito_nlm`/`risposta_sintetica`/`citazione_verbatim_nlm`/`fonte_citata_corretta`) — ignorala.

Notebook di destinazione: quello che l'utente indicherà al momento del lancio. **Le fonti vanno caricate lì prima**, altrimenti questo passaggio non ha senso.

---

## VINCOLO CARDINE

La domanda posta a NotebookLM deve essere **sostanzialmente la stessa** posta al lettore A. Se le due domande divergono, la divergenza degli esiti non significa più nulla e la colonna M del foglio diventa rumore.

Quindi: stesso `claim` verbatim, stessa richiesta di implicazione, portata e livello di forza, stessa richiesta di citazione testuale. Le quattro domande della query qui sotto sono la traduzione diretta dei tre test del prompt A: implicazione bidirezionale → domande 1-2, confronto di portata → domanda 3, dimostra/menziona/assume → domanda 4. Se in futuro modifichi la query, modifica in parallelo anche il prompt A (o viceversa): altrimenti la colonna M smette di misurare quello che dovrebbe misurare.

## ANTI-CONTAMINAZIONE

NotebookLM interroga un corpus, non un singolo file: può rispondere pescando da un'altra fonte del notebook e attribuire alla fonte sbagliata. Due difese, entrambe obbligatorie:

1. **Tecnica, prioritaria:** restringi le sorgenti attive con il parametro `source_ids`, passando solo l'id della fonte in esame.
2. **Testuale:** ripeti nella query che la risposta deve fondarsi esclusivamente su quel documento.

A valle, **verifica sempre** che la citazione allegata da NotebookLM provenga davvero dalla fonte in esame. Se proviene da un'altra, l'esito è `non verificabile` con nota di contaminazione. Nessuno script controlla questo dopo di te — a differenza del lettore A, qui non c'è una rete di sicurezza meccanica sulla citazione: questa verifica a valle è l'unico presidio, quindi eseguila sempre, anche quando la risposta "sembra" già corretta.

## TESTO DELLA QUERY

> Rispondi esclusivamente sulla base del documento indicato, senza usare altre fonti del notebook e senza conoscenza generale.
>
> Il documento è: **{citazione}**.
>
> Un lavoro accademico gli attribuisce questa affermazione:
> "{claim}"
>
> Rispondi a queste quattro domande, separatamente:
> 1. Il contenuto del documento implica questa affermazione?
> 2. L'affermazione dice più di quanto il documento sostenga — aggiunge condizioni, generalità, causalità o forza che nel testo non ci sono?
> 3. La portata coincide? Stessa popolazione, stesso contesto, stesse condizioni al contorno?
> 4. Il documento **dimostra** questo punto, lo **menziona** di passaggio, o lo **assume** senza affermarlo?
>
> Concludi riportando una **citazione testuale verbatim** dal documento che sostiene o smentisce l'affermazione, con l'indicazione della sezione.
>
> Se il documento non è caricato fra le sorgenti, o se non riesci a produrre una citazione verbatim, scrivi esattamente "NON POSSO CITARE: FONTE NON CARICATA" e fermati.

## CONVERSIONE IN ESITO

NotebookLM non deve produrre i quattro valori: quel vocabolario appartiene al lettore A. **Sei tu a convertire** la sua risposta sostantiva, applicando gli stessi criteri del prompt A:

- implicazione piena, portata coincidente, livello "dimostra" → `usabile`
- implicazione presente ma portata diversa, forza minore, o livello "menziona"/"assume" → `da riformulare`
- nessuna implicazione, o contraddizione → `non usabile`
- fonte non isolabile, citazione non verificabile, contaminazione da altre fonti → `non verificabile`

## OUTPUT — contratto rigido

Un JSON per coppia, in `estrazioni/estratti_nlm/<nodo>__<id_fonte>.json`:

```json
{
  "nodo": "3.1.1",
  "id_fonte": "akerlof1970",
  "esito_nlm": "usabile | da riformulare | non usabile | non verificabile",
  "risposta_sintetica": "…",
  "citazione_verbatim_nlm": "…",
  "fonte_citata_corretta": true,
  "note": "…"
}
```

`fonte_citata_corretta` è `false` se la citazione restituita proviene da un documento diverso da quello in esame: in quel caso `esito_nlm` deve essere `non verificabile`.

Lo scrittore finale riversa `esito_nlm` nella **colonna L** del foglio `Estratti`. La colonna M calcola da sola la divergenza con la colonna H.

## ORDINE DI ESECUZIONE

Questo passaggio va **dopo** il lettore A, mai prima e mai insieme. Serve un confronto fra due letture indipendenti: se conoscessi già l'esito di A saresti influenzato. Non leggere il contenuto delle colonne H-K prima di aver prodotto il tuo.
