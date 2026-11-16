---
name: tesi-ingest
description: Legge l'Excel congelato (fogli iTOC, DOSSIER, Estratti) e produce build/nodes.json, build/estratti.json, build/metrics.json e nodes/*.md. Invocala una sola volta dopo GATE 0; dopo, usa /tesi-resync.
---

# /tesi-ingest

Esegue `tools/ingest.py` (già scritto, verificato riga per riga in questa nota — non
riscriverlo, chiamalo). È **idempotente**: rieseguirlo con l'Excel invariato riproduce
lo stesso `nodes.json`/`metrics.json` (a parte `generated_at`) e non sovrascrive un
`nodes/<id>.md` che contiene già del testo oltre lo scheletro vuoto.

Non scrive mai sull'Excel. Non calcola `target_words`, `fit_ratio` o `regime`: quel
calcolo vive **solo** in `tools/gap.py` (`/tesi-gap`), per non duplicare la formula in
due posti — leggi bene la sezione "Cosa NON produce" più sotto, è la parte che sorprende
di più chi si aspetta uno schema diverso.

## Precondizioni — verificale tu stesso prima di lanciare lo script, in quest'ordine

1. **Nessun lock file.** `tools/ingest.py` la verifica anche da sé e si ferma con
   `SystemExit` se trova un `~$*`, ma verificalo anche tu prima, per dare un messaggio
   chiaro invece di uno stack trace:
   ```bash
   find "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura" -maxdepth 1 -name '~$*'
   ```
   Se non è vuoto, fermati e segnala quale file è aperto. Non cancellarlo.

2. **`/usr/bin/python3` ha `openpyxl`**:
   ```bash
   /usr/bin/python3 -c "import openpyxl; print(openpyxl.__version__)"
   ```

3. **Il foglio `DOSSIER` non riporta incoerenze** — `tools/ingest.py` non lo verifica da
   sé (legge `DOSSIER` solo per le colonne H/I/O), quindi questo controllo lo fai tu,
   prima:
   ```bash
   /usr/bin/python3 -c "
   import openpyxl
   wb=openpyxl.load_workbook('/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/iTOC master.xlsx', read_only=True, data_only=True)
   ws=wb['DOSSIER']
   bad=[(r[0], r[10]) for r in ws.iter_rows(min_row=2, values_only=True) if r[10]]
   print(len(bad))
   for x in bad[:20]: print(x)
   "
   ```
   Se il conteggio è **> 0**, fermati e riporta nodi e messaggi: il `DOSSIER` non
   riflette l'ultimo stato di `iTOC`/`Fonti`/`Estratti`, oppure una modifica ha rotto
   qualcosa. Non ingerire un `DOSSIER` incoerente. Non rigenerarlo tu — `FONTI/pipeline/dossier.py` è vietato dopo GATE 0 (§1 del prompt orchestratore): la
   correzione è dell'autore, in FASE 0, non tua.

4. **Snapshot delle sorgenti** (§1 del prompt orchestratore — `tools/ingest.py` **non
   lo fa**, lo fai tu come primo atto, prima di invocare lo script):
   ```bash
   /usr/bin/python3 -c "
   import hashlib, json, shutil, os, datetime
   BASE = '/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/'
   SRC = BASE + 'source/'
   os.makedirs(SRC, exist_ok=True)
   files = ['iTOC master.xlsx', 'LF3236167.docx', 'FONTI/tesi.bib']
   manifest = {'snapshot_at': datetime.datetime.now().isoformat(timespec='seconds'), 'file': {}}
   for rel in files:
       src = BASE + rel
       dst = SRC + os.path.basename(rel)
       shutil.copy2(src, dst)
       h = hashlib.sha256(open(src,'rb').read()).hexdigest()
       manifest['file'][rel] = {'sha256': h, 'mtime': os.path.getmtime(src), 'size': os.path.getsize(src)}
   json.dump(manifest, open(SRC + 'manifest.json','w'), indent=2)
   print(json.dumps(manifest, indent=2))
   "
   ```
   Dichiara questo output nel report finale (punto 3 sotto). `source/` è in
   `.gitignore`.

## Passi

### 1. Lancia l'ingest

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/ingest.py"
```

Flag disponibili (verificati sullo script reale): `--excel <path>` (default l'Excel di
progetto), `--dry-run` (sola lettura, stampa il report, **non** scrive `build/` né
`nodes/` — usalo per verificare i numeri prima di committare all'ingest vero),
`--help`.

Lo script, in ordine:

1. Verifica lock file da sé (ridondante con la tua precondizione 1, ma non fa male).
2. Legge `iTOC`, `DOSSIER`, `Fonti`, `Estratti` con `openpyxl` in sola lettura.
3. Per ogni nodo (`iTOC!Indice` non vuoto, la riga `TOTALE pp attese` è esclusa perché
   ha `Indice` vuoto): applica il filtro `[OFF-RECORD]` **sia** su `iTOC!Note` **sia**
   su `DOSSIER!"Note autore"` (righe che iniziano, dopo strip, con `[OFF-RECORD]`,
   rimosse per intero), conta le rimozioni **separatamente** per le due colonne e le
   somma in un totale.
4. **Se il totale è 0, lo script si ferma da solo** (`SystemExit`, exit code ≠ 0): non
   serve che tu lo verifichi a parte, ma **verifica comunque che l'exit code sia 0**
   prima di considerare l'ingest riuscito — uno script che si ferma per questo motivo
   non ha scritto `build/` né `nodes/`.
5. Costruisce `fonti_ammesse`/`fonti_vietate` dalle colonne H/I del `DOSSIER` (mai da
   `Estratti!Esito`), e `risoluzioni[]` da `Estratti!S` per le coppie del nodo.
6. Scrive `build/nodes.json`, `build/estratti.json`, `build/metrics.json`,
   `nodes/<id>.md` (solo se non già popolato).

### 2. Verifica l'esito

```bash
echo $?
```

Se diverso da 0, leggi lo stderr: o è il filtro `[OFF-RECORD]` a 0 (fermati, non è un
bug tuo da correggere — segui la procedura di escalation, non inventare un filtro
diverso), o un altro errore esplicito (`ERRORE: ...`).

### 3. Report

Riporta **testualmente** l'output di stdout dello script (contiene già tutto quello che
serve: nodi letti, coppie Estratti, fonti, righe DOSSIER, il conteggio `[OFF-RECORD]`
per le due colonne e il totale, nodi con almeno una fonte ammessa, nodi in perimetro con
`Descrizione` vuota, `nodes/*.md` scritti vs già popolati), **più** l'output dello
snapshot del passo di precondizione 4.

## Formato esatto dei file prodotti — verificato sul codice reale, non presunto

`build/nodes.json`:
```json
{
  "words_per_page": 350,
  "words_per_page_band": [310, 380],
  "generated_at": "2026-09-08T10:00:00",
  "nodes": {
    "3.1.1": {
      "id": "3.1.1", "level": 3, "chapter": "3", "parent": "3.1",
      "perimetro": true, "is_leaf": true,
      "title": "...", "source_desc": "...", "fonti": "...", "ruolo": "...",
      "trappole": "...", "note": "... (già filtrata [OFF-RECORD])",
      "risoluzioni": [{"fonte": "akerlof1970", "risoluzione": ""}],
      "fonti_ammesse": [{"fonte": "akerlof1970", "regime": "usabile"}],
      "fonti_vietate": ["dierickxcool1989"],
      "fonti_vietate_dettaglio": [{"fonte": "dierickxcool1989", "motivo": "ESCLUSA (superata)"}],
      "regime": null,
      "sha": {"desc": "...", "fonti": "...", "ruolo": "...", "trappole": "...", "note": "..."},
      "stato": "vuoto",
      "target_words": 0,
      "source_words": 175
    }
  }
}
```

**`regime: null` e `target_words: 0` sono placeholder**, non dati mancanti per errore:
`/tesi-gap` li deriva ogni volta che gira, a partire da `source_words`, `ruolo`, e il
`budget_pp`/`k_c` del capitolo — e **non li riscrive qui dentro** (§ sotto). Non trattare
uno `0`/`null` in questi due campi come un bug dell'ingest. **`expansion_ratio` è
ritirato dalla specifica (§3)**: non compare più nello schema, nemmeno come placeholder
morto — il rapporto si chiama `fit_ratio` e lo calcola solo `/tesi-gap`, e vive solo in
`reports/gap.md`, mai in `nodes.json`.

`build/estratti.json` — **dizionario piatto**, chiave `"<nodo>|<id_fonte>"` (non
nidificato per nodo):
```json
{
  "3.1.1|akerlof1970": {
    "nodo": "3.1.1", "id_fonte": "akerlof1970", "citazione": "(Akerlof, 1970)",
    "ruolo": "mattone stretto", "peer_review": "sì", "pdf": "...",
    "claim_da_verificare": "...", "esito": "usabile", "cosa_dice_davvero": "...",
    "citazione_verbatim": "...", "sezione": "p. 3", "esito_notebooklm": "usabile",
    "divergenza": "", "note": "...", "esito_arbitrato": "nessun arbitrato",
    "risoluzione": ""
  }
}
```

`build/metrics.json` — **aggregati grezzi**, non il gap report:
```json
{
  "generated_at": "2026-09-08T10:00:00",
  "n_nodi_totale": 129, "n_fonti": 67, "n_coppie_estratti": 108,
  "words_per_page": 350, "words_per_page_band": [310, 380],
  "source_words_totale": 12574, "source_words_perimetro": 12019,
  "per_capitolo": {
    "5": {"n_nodi": 29, "n_foglie": 23, "source_words": 6436, "budget_pp": 9}
  }
}
```
Non contiene `struttura_pp`, `capacità`, `k_c`: `tools/gap.py` li ricalcola ogni volta
che gira, a partire da questi numeri grezzi, così la formula vive in un solo file.

## Postcondizioni

- Lo script è uscito con **exit code 0**.
- Il totale `[OFF-RECORD]` dichiarato (somma delle due colonne) è **> 0**. Verificato
  oggi sul nodo `5.1.4`: contiene due blocchi in `iTOC!Note`, e altrettanti (verbatim)
  in `DOSSIER!"Note autore"` — un totale sano su questo solo nodo è quindi 4 (2+2), non
  2: lo script conta le due colonne **separatamente e le somma**, non deduplica.
- `build/nodes.json → nodes` contiene esattamente le chiavi `Indice` lette da `iTOC`
  (oggi 129), nessuna in più, nessuna in meno.
- `nodes/*.md` esistono per tutti i 129 nodi (non solo per il perimetro: lo script non
  filtra per `perimetro` quando scrive gli scheletri) — è `/tesi-draft` a non scriverci
  mai per il Cap. 7, non `/tesi-ingest` a ometterli.
- Rieseguendo senza toccare l'Excel, `nodes.json`/`estratti.json`/`metrics.json` sono
  identici salvo `generated_at`.

## Cosa NON produce (e chi lo fa davvero)

- **Non calcola `target_words`, `fit_ratio`, `regime` per nessun nodo.** Questi vivono
  solo nell'output di `tools/gap.py`, ricalcolato a ogni invocazione da `nodes.json` +
  `metrics.json` — mai persistito su `nodes.json`. Se ti serve il `target_words` di un
  nodo per scriverlo (`/tesi-draft`), non cercarlo in `nodes.json`: gira
  `tools/gap.py --chapter <c> --dry-run` e leggi la tabella "Per nodo foglia" del suo
  output.
- **Non aggiorna mai `stato` a `"scritto"`**: quello lo fa `/tesi-draft` dopo aver
  scritto un nodo (script minimo separato, non `tools/ingest.py`).
- **Non fa lo snapshot in `source/`**: è un passo che fai tu, prima di lanciarlo
  (precondizione 4).
- **Non verifica `⚠ COERENZA`**: lo fai tu, prima (precondizione 3).
- **Non genera `build/matrici.json`**: le 4 matrici e le tabelle del Cap. 5 le estrae
  l'orchestratore stesso (§4.6 del prompt), non questa skill.
- Non scrive sull'Excel, non tocca `out/`, non genera prosa.
