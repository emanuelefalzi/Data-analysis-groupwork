# Prompt B — Secondo lettore su NotebookLM, per pagine web

Adattamento per siti web di `originali tesi/prompt/B - notebooklm ESEGUIBILE.md` e
`originali tesi/loop2/ISTRUZIONI_NOTEBOOKLM.md`.

Serve una **seconda lettura indipendente** della stessa pagina sullo stesso claim: dove i due
lettori concordano il dato è solido, dove divergono decide il gruppo.

## Ordine

Gira **dopo** il lettore A, mai insieme. Non leggere `lavoro/estratti/` prima di aver prodotto il
tuo output: se conosci l'esito di A sei influenzato.

## Preparazione del notebook (una volta sola, la fa l'orchestratore)

1. `notebook_create` con il nome del progetto, oppure il notebook indicato dall'utente.
2. Carica **il testo congelato, non l'URL**: `source_add` con `source_type="file"` e
   `file_path` = `lavoro/testi/<id_fonte>.txt`. Così NotebookLM legge esattamente la stessa
   versione del lettore A. L'URL dal vivo va usato solo se l'utente lo chiede, e allora una
   divergenza può dipendere dalla pagina cambiata: annotalo.
3. `notebook_get` e salva in `lavoro/nlm_map.json` la mappa `id_fonte -> source_id`.
4. Se compare un errore di autenticazione: lanciare `nlm login` da terminale.

## Procedimento per ogni coppia

1. Prendi `source_id` da `lavoro/nlm_map.json`.
2. `notebook_query` passando **`source_ids` con il SOLO id di quella fonte**. Senza, NotebookLM
   pesca dalle altre pagine del notebook e il confronto non vale più nulla.
3. Query, sostituendo `{citazione}` e `{claim}` dal task:

> Rispondi esclusivamente sulla base del documento indicato, senza usare altre fonti del notebook
> e senza conoscenza generale.
>
> Il documento è: **{citazione}**.
>
> Un lavoro universitario gli attribuisce questa affermazione:
> "{claim}"
>
> Rispondi a queste cinque domande, separatamente:
> 1. Il contenuto del documento implica questa affermazione?
> 2. L'affermazione dice più di quanto il documento sostenga — aggiunge condizioni, generalità,
>    causalità o forza che nel testo non ci sono?
> 3. La portata coincide? Stesso soggetto, stesso periodo, stesse condizioni?
> 4. Il documento **dimostra** questo punto, lo **menziona** di passaggio, o lo **assume**?
> 5. Il documento lo presenta come un fatto verificabile o come una dichiarazione di chi scrive
>    (autopresentazione, marketing)?
>
> Concludi riportando una **citazione testuale verbatim** dal documento che sostiene o smentisce
> l'affermazione.
>
> Se il documento non è fra le sorgenti, o non riesci a produrre una citazione verbatim, scrivi
> esattamente "NON POSSO CITARE: FONTE NON CARICATA" e fermati.

4. **Converti tu** la risposta in `esito_nlm`, con gli stessi criteri del prompt A:
   implicazione piena, portata coincidente, «dimostra» → `usabile`; portata diversa, forza minore,
   «menziona»/«assume», o autodichiarazione presentata come fatto → `da riformulare`; nessuna
   implicazione o contraddizione → `non usabile`; fonte non isolabile o contaminazione →
   `non verificabile`.
5. Se la citazione restituita non viene da quella pagina: `fonte_citata_corretta: false` ed esito
   `non verificabile`.

## Output

Un JSON per coppia in `lavoro/estratti_nlm/<sezione>__<id_fonte>.json`, esattamente 7 chiavi:

```json
{
  "sezione": "2.1",
  "id_fonte": "acme_chi_siamo",
  "esito_nlm": "usabile | da riformulare | non usabile | non verificabile",
  "risposta_sintetica": "…",
  "citazione_verbatim_nlm": "…",
  "fonte_citata_corretta": true,
  "note": "…"
}
```

**`citazione_verbatim_nlm` contiene SOLO il passaggio, uno solo, con le parole esatte.** Niente
involucro («Dalla sezione X: "…"»), niente passaggi multipli concatenati: `valida.py` la cerca nel
testo congelato e, se non la ritrova, declassa a `non verificabile`. Nella tesi questo errore di
formato ha declassato per sbaglio tre verdetti corretti su tre.

## Report in chat

Massimo 10 righe: per ogni coppia l'esito e se la citazione veniva dalla fonte giusta. Segnala se
`source_ids` non ha funzionato.
