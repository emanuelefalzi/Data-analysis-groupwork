# Loop 1 - Recupero fonti

Script per identificare le fonti citate nella scaletta (note solo come
"Autore, anno") tramite API bibliografiche gratuite, scaricare i PDF ad
accesso aperto disponibili, e aggiornare il foglio "Fonti" di
`iTOC master.xlsx`.

## Come si lancia

```bash
cd "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/loop1"
python3 recupera.py                    # dry-run: stampa cosa farebbe, non tocca nulla
python3 recupera.py --only agrawal2018 # debug su una sola fonte
python3 recupera.py --limit 8          # dry-run sulle prime 8 fonti da_cercare
python3 recupera.py --commit           # scrive davvero nell'Excel e scarica i PDF
python3 recupera.py --commit --limit 5 # commit ma solo sulle prime 5
```

Nota: se la cartella della tesi non e' quella nel percorso di default, usa
`--excel "/percorso/a/iTOC master.xlsx"`.

Senza `--commit` lo script è in **dry-run** (default): interroga davvero le
API (serve per vedere che risultati darebbero), ma non scrive nulla
nell'Excel e non scarica nessun PDF - stampa e logga soltanto cosa farebbe.
Con `--commit` scrive per davvero: fa prima un **backup con timestamp**
dell'Excel, poi aggiorna riga per riga (cercando l'ID in colonna A) e
scarica i PDF ad accesso aperto trovati in `fonti def/<id>.pdf`.

## Cosa fa

1. **Identità**: per ogni fonte in stato `da_cercare` interroga Crossref,
   OpenAlex, Semantic Scholar (sempre) e arXiv (solo se le prime tre non
   trovano nulla o l'anno è >= 2024). Nessuna chiave API richiesta; usa il
   "polite pool" (`mailto=lele.falzi@gmail.com`) e uno User-Agent
   identificabile.
2. **Punteggio**: filtro rigido sul cognome del primo autore (normalizzato),
   filtro sull'anno (scarto di 1 anno tollerato con penalità, oltre si
   scarta), punteggio composito dove il peso maggiore va alla similarità
   testuale fra titolo+abstract del candidato e contesto d'uso/claim della
   fonte (TF-IDF + coseno; usa scikit-learn se presente, altrimenti un
   TF-IDF scritto in stdlib). Decide fra tre esiti: **identificata**
   (un candidato nettamente sopra gli altri), **ambigua** (candidati troppo
   vicini, non si sceglie), **non_trovata** (nessun candidato supera il
   filtro autore). Le soglie sono costanti documentate in cima a
   `lib/scoring.py`.
3. **Acquisizione**: per i candidati identificati con DOI, interroga
   Unpaywall e guarda `best_oa_location`/`open_access` di OpenAlex/Semantic
   Scholar/arXiv. Se trova un PDF open access lo scarica e verifica che sia
   davvero un PDF (magic bytes `%PDF`, non una pagina di errore HTML) prima
   di considerarlo `scaricata`. Se il paper è identificato ma non
   liberamente accessibile, stato `paywall` e l'URL della landing page (DOI
   resolver o editore) va in colonna Q, da aprire a mano.
4. **Scrittura Excel**: scrive solo nelle colonne L, M, N, O, P, Q, R, S, T
   e appende una riga di provenienza in W (quale API, quale query, quale
   data) senza mai cancellare le note esistenti. Non tocca mai A-K, U, V.
   Nessun valore bibliografico è inventato: titolo, sede, DOI, URL, tipo
   arrivano testualmente dal corpo della risposta API; se un campo non
   arriva, resta vuoto.
5. **Report**: genera `pipeline/loop1/report.md` (riepilogo leggibile), 
   `pipeline/loop1/da_disambiguare.json` (candidati per le fonti ambigue, da
   sottoporre a un umano) e `pipeline/loop1/log.jsonl` (una riga per fonte con tutte
   le decisioni prese).

## Cosa NON fa

- **Non copre l'accesso istituzionale via login** (biblioteca universitaria,
  EZproxy, Shibboleth, ecc.). Per le fonti in stato `paywall`, l'URL in
  colonna Q va aperto a mano nel browser, eventualmente passando dal login
  istituzionale, per verificare se l'ateneo ha un abbonamento.
- Non usa nessun LLM per decidere quale candidato è quello giusto: il
  punteggio è interamente deterministico (regole + TF-IDF).
- Non tocca mai le colonne A-K (dati della scaletta) né U-V (verifica del
  contenuto, che è un passo successivo del progetto).
- Non scarica nulla in modalità dry-run (default).

## Idempotenza e riavvio

Lo script lavora solo sulle righe con stato `da_cercare` in colonna L: una
volta che una fonte è stata scritta con `--commit` (stato diventato
`trovata`/`scaricata`/`paywall`/`ambigua`/`non_trovata`), i run successivi
la saltano automaticamente. Se il processo si interrompe a metà, i
risultati delle API già interrogate restano in una cache su file
(`pipeline/loop1/cache/<id>.json`, un file per fonte): un rilancio non rifà le
chiamate già fatte con successo, riparte dalla fase di punteggio.
In modalità `--commit` l'Excel viene salvato dopo ogni singola fonte
scritta con successo (workbook aperto una sola volta, un solo writer, ma
salvataggi incrementali), quindi il lavoro già fatto non si perde nemmeno
se lo script muore a metà.

## Dipendenze

Solo `requests` e `openpyxl` (già presenti) più la libreria standard.
`scikit-learn` è opzionale: se installato viene usato per il TF-IDF, altrimenti
c'è un fallback equivalente scritto in stdlib.

## Struttura

```
loop1/
  recupera.py       # eseguibile principale (CLI)
  lib/
    httpclient.py    # sessione HTTP con rate limit per host + backoff esponenziale
    sources.py       # client Crossref, OpenAlex, Semantic Scholar, arXiv, Unpaywall
    scoring.py        # filtro autore/anno, punteggio composito, decisione
    textutil.py        # normalizzazione nomi, TF-IDF (sklearn o fallback stdlib)
    cache.py            # cache su file dei risultati API, per fonte
    excelio.py           # apertura/backup/scrittura del foglio "Fonti"
    download.py           # download + verifica PDF
  cache/                    # (creata al primo run) cache API per fonte
  report.md                 # (generato a ogni run)
  da_disambiguare.json       # (generato a ogni run)
  log.jsonl                   # (append-only, una riga per fonte processata)
```
