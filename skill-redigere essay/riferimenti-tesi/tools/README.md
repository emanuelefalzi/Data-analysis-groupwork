# `tools/` — script deterministici della pipeline di stesura

Otto script Python, nessuno dei quali scrive sull'Excel. Vanno lanciati con
**`/usr/bin/python3`** (ha `openpyxl` 3.1.5 e `python-docx`; il `python3` di
default e' miniconda e non li ha), da qualunque cartella — usano tutti
percorsi assoluti, mai `cd`. Ogni script ha `--help` e restituisce un exit
code diverso da zero in caso di errore o di finding bloccante.

Riferimento: `PROMPT-orchestratore-tesi.md` (specifica), `CLAUDE.md` (regole
sempre attive), `CONTESTO-EXCEL-per-orchestratore.md` (colonne dell'Excel).
Stile e convenzioni riprese da `FONTI/pipeline/dossier.py`.

**`assemble.py` non e' in questa cartella.** Dipende da decisioni ancora
aperte al GATE 1 (§10 del prompt orchestratore): dove vivono abstract,
introduzione e reference list (nodi nuovi in `iTOC` o appendice tecnica), e
il budget di pagine definitivo. Finche' l'autore non risponde, un
`assemble.py` scritto ora assemblerebbe un documento con `[[CIT-*]]` che
puntano a una reference list inesistente. Va scritto dopo GATE 1.

## Ordine d'uso (rispecchia §10 del prompt orchestratore)

```
ingest.py               (una volta, dopo GATE 0)
gap.py                  (GATE 1, prima di scrivere)
patch_lint_glossario.py (una volta, quando l'autore lo lancia — vedi sotto)
[node-writer scrive nodes/<id>.md]
lint_numeri.py, lint_budget.py, lint_ngrammi.py, glossario/lint.py   (per nodo, ogni /tesi-audit)
ledger_renumber.py      (dopo ogni fix)
resync.py               (quando l'Excel cambia dopo l'ingest)
```

---

## 1. `ingest.py`

Legge i 7 fogli di `iTOC master.xlsx` (foglio **`DOSSIER`**, non `iTOC` +
`Estratti` ricombinati a mano) e produce lo stato iniziale della pipeline.

- **Input**: `iTOC master.xlsx` (fogli `iTOC`, `DOSSIER`, `Fonti`, `Estratti`).
- **Output**: `build/nodes.json`, `build/estratti.json`, `build/metrics.json`,
  `nodes/<id>.md` (uno per nodo, solo `## DRAFT` e `## LEDGER` vuote).
- **Non scrive** su un `nodes/<id>.md` che contiene gia' del testo oltre lo
  scheletro vuoto: idempotente in sicurezza, non sovrascrive lavoro fatto.
- `--dry-run`: legge e stampa il report (conteggi, blocchi `[OFF-RECORD]`
  rimossi), non scrive niente. **Il conteggio dei blocchi `[OFF-RECORD]`
  rimossi (iTOC!F + DOSSIER!O) e' sempre stampato; se il totale e' zero lo
  script esce con errore** (il filtro non ha agganciato niente).
- Si ferma senza scrivere se trova un file di lock `~$*` (Word/Excel aperti).

## 2. `gap.py`

Il gap report di §7: per capitolo, struttura in pagine (stimata dai titoli),
capacita' in parole, materiale, `fit_ratio`, `regime`; per nodo,
`target_words` derivato con l'algoritmo a cinque passi di §4.1; l'elenco dei
nodi senza materiale e le domande del GATE 1.

- **Input**: `build/nodes.json` se esiste, altrimenti ricalcola al volo
  dall'Excel (sola lettura, stesso codice di `ingest.py`); budget pp letto
  sempre fresco dall'Excel.
- **Output**: stdout + `reports/gap.md` (non scritto con `--dry-run`).
- `--chapter N`: limita il report a un capitolo.
- Espone le funzioni di derivazione (`chapter_metrics`,
  `derive_targets_for_chapter`, `load_nodes`, `load_budget_pp`) — **importato
  da `lint_budget.py`** cosi' la formula di `target_words` vive in un solo
  posto.
- **Approssimazione dichiarata**: la struttura in pagine dei titoli
  (`struttura_pp`) e' stimata con un conteggio a caratteri (soglia 80
  caratteri/riga per un titolo, incluso il numero), calibrato sulla misura
  nota del 2026-09-07 (100 titoli in perimetro → 115 righe fisiche → 4,94
  pagine — riprodotta esattamente in aggregato). Non e' un renderer di
  Word: se il template cambia, ricalibrare rifacendo la procedura manuale
  di §10 e aggiornando le due costanti `TITLE_CHARS_PER_LINE` e
  `TITLE_PP_PER_LINE` in testa al file.

## 3. `lint_numeri.py`

Ogni cifra, percentuale, data, importo e nome proprio del DRAFT deve
comparire *verbatim* nella whitelist: l'unione di tutti i `source_desc` in
perimetro + `Fonti` + `Estratti`. Fuori da li' = finding `high` (bloccante).
Dentro la whitelist ma fuori dal nodo/dai suoi antenati = solo un avviso.

- **Input**: testo (posizionale, `--file` o `--text`; se assente legge
  `## DRAFT` da `nodes/<id>.md`) + whitelist da `build/nodes.json` (se
  esiste) o dall'Excel, piu' `Fonti`/`Estratti` letti sempre dall'Excel.
- **Output**: stdout, elenco dei finding. Exit 2 se c'e' almeno un `high`.
- Estrazione euristica (regex su numeri/date/importi, maiuscole fuori
  inizio-frase per i nomi propri): non e' un NER, non ci sono librerie NLP
  fra i prerequisiti (§9). Match verbatim per sottostringa, case-sensitive
  sui nomi propri: un numero corto (es. "87") puo' risultare "in whitelist"
  solo perche' e' sottostringa di un numero piu' lungo altrove — limite
  noto di un controllo a sottostringa, non risolvibile senza tokenizzazione
  posizionale che il progetto non richiede.

## 4. `lint_budget.py`

Parole scritte contro la **capacita'** del nodo (`target_words` ±15%,
nessun pavimento): non contro un pavimento fisso, che non esiste piu'.

- **Input**: come sopra per il testo; `target_words` non e' ricalcolato qui,
  **importa `gap.py`** e ne riusa `chapter_metrics` /
  `derive_targets_for_chapter` sul solo capitolo del nodo richiesto.
- **Output**: stdout (target, banda, parole scritte, esito). Exit 2 se fuori
  banda. Se il nodo non ha materiale (`source_words=0`) o il suo capitolo e'
  bloccato (`k_c` fuori `[0.55, 1.50]`), lo dice in una nota invece di
  fingere un target.
- `--from-excel`: ignora `build/nodes.json`, ricalcola dall'Excel.

## 5. `lint_ngrammi.py`

Controllo antiplagio a n-grammi di 8 parole. **Per nodo** (default): il
DRAFT contro le sole `Citazione verbatim` (`Estratti` colonna J) delle
coppie di quel nodo — girato per nodo, non solo alla fine. **`--whole`**:
contro tutti i file di `FONTI/pipeline/testi estratti/` — il controllo
finale sul documento intero.

- **Input**: testo + (per nodo) `Estratti` dall'Excel, oppure (`--whole`)
  tutti i file di `FONTI/pipeline/testi estratti/`.
- **Output**: stdout, n-grammi copiati verbatim con la fonte. Exit 2 se ce
  n'e' almeno uno.
- Match case-insensitive su token alfanumerici: la punteggiatura non conta.

## 6. `ledger_renumber.py`

Dopo ogni fix rinumera i `¶N` del LEDGER e verifica che le righe del LEDGER
siano tante quante i paragrafi del DRAFT (disallineamento = errore, non
scrive). Verifica anche che la prima frase di ogni `SOURCE["..."]` esista
davvero nel `source_desc` del nodo, con `str.find()` — niente offset di
carattere, il LEDGER non li porta piu' (§6).

- **Input**: `nodes/<id>.md` (o `--path` per un file diverso) + `source_desc`
  del nodo da `build/nodes.json` (o Excel).
- **Output**: riscrive la sezione `## LEDGER` del file in place, a meno di
  `--check-only`. Exit 2 su disallineamento o su una prima-frase non
  trovata (in nessuno dei due casi scrive).

## 7. `resync.py`

Rilegge l'Excel, confronta gli sha per colonna (`desc`, `fonti`, `ruolo`,
`trappole`, `note`) con `build/nodes.json`, riporta *cosa* e' cambiato e
riporta a `vuoto` i soli nodi toccati.

- **Input**: `build/nodes.json` (deve esistere: non e' un sostituto
  dell'ingest) + l'Excel.
- **Output**: aggiorna `build/nodes.json` in place (i nodi non toccati
  restano bit-per-bit identici, incluso il loro `stato` se un'altra fase
  della pipeline lo ha gia' avanzato oltre `vuoto`). `--dry-run`: solo
  report, non scrive.
- **Fallisce con errore esplicito (`exit 2`) se l'insieme delle chiavi
  `Indice` e' cambiato** (nodo aggiunto o rimosso): impone un `ingest.py`
  pulito, non tenta di indovinare cosa e' successo.
- Non tocca mai `nodes/<id>.md`: quello e' del node-writer/fix-applier.

## 8. `patch_lint_glossario.py`

**Non e' un lint**: e' la patch a `FONTI/pipeline/glossario/lint.py`
descritta in §4.7. Non modifica `lint.py` da sola: lo fa solo quando
l'autore lancia lo script (di default applica; `--dry-run` mostra solo il
diff).

- **Diagnosi verificata** (leggendo il codice, non solo il prompt):
  `_anticipazione_ammessa(nodo_uso, nodo_def)` ignora del tutto i campi
  `usabile_prima_del_nodo_definizione` e `anticipazioni_legittime` che
  `glossario.json` gia' porta su tutte le 48 voci. Effetto misurato prima
  della patch: `python3 lint.py --autotest` → **3 blocchi su 38** citazioni-
  ancora (`domain competence`, `co-specialized`, `costly signal`, tutti e
  tre falsi positivi risolti dai due campi ignorati). **Confermato dopo la
  patch, su una copia di `lint.py` in una cartella temporanea (mai sul file
  vero): l'autotest scende a 0.**
  La gravita' di `uso_prima_definizione` **resta hardcoded a `blocca`**:
  il prompt orchestratore la descrive come stato di fatto accettabile
  ("trattalo come un lint piu' severo del previsto, non come rotto"), non
  come qualcosa da cambiare qui — questa patch non la tocca.
- **Input**: `FONTI/pipeline/glossario/lint.py` (letto, mai scritto in
  questa consegna).
- **Output**: se lanciato senza `--dry-run`, riscrive `lint.py` in place
  dopo un backup timestampato (`lint.py.bak.<AAAAMMGG_HHMMSS>` nella stessa
  cartella) e stampa il comando per verificare l'autotest.
- Si ferma senza scrivere se il testo atteso non si trova piu' in `lint.py`
  (file gia' cambiato): non applica patch alla cieca.
