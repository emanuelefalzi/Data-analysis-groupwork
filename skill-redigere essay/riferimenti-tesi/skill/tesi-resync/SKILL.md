---
name: tesi-resync
description: Rilegge l'Excel dopo una modifica dell'autore, confronta gli sha per colonna con nodes.json e riporta cosa è cambiato. Fallisce con errore esplicito se l'insieme delle chiavi Indice è cambiato. Usala al posto di /tesi-ingest dopo la prima esecuzione.
---

# /tesi-resync

Non è un canale di modifica dell'Excel: **non sa riconoscere righe aggiunte o
rimosse** in modo sicuro (le rifiuta esplicitamente, vedi sotto) e una modifica a un
nodo padre non invalida da sola i figli, che restano agganciati a una versione che non
esiste più — è un limite dichiarato, non un bug da correggere qui.

## Precondizioni

1. `build/nodes.json` esiste già (questa skill presuppone almeno un `/tesi-ingest`
   precedente: se non esiste, di' all'utente di usare `/tesi-ingest`, non provare a
   simularlo qui).
2. Nessun lock file (`~$*`) su Excel o Word — stessa verifica di `/tesi-ingest`.
3. La colonna `⚠ COERENZA` del `DOSSIER` è vuota su ogni riga — stessa verifica di
   `/tesi-ingest`, perché `/tesi-resync` legge lo stesso foglio.

## Passi

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/resync.py"
```

Contratto per `tools/resync.py` — **riusa `tools/ingest.py` come modulo** (stesso
pattern già usato da `tools/gap.py`, che fa `import ingest` invece di riscrivere la
lettura dell'Excel): chiama `ingest.load_workbook_rows()` e `ingest.build_nodes()` per
ottenere lo stato "fresco" dall'Excel, non reinventare il parsing.

### 1. Confronto dell'insieme delle chiavi

Estrai l'insieme di `Indice` da `iTOC` oggi (stessa fonte di `ingest.build_nodes`, non
il `DOSSIER`: è lì che `/tesi-ingest` legge le chiavi dei nodi), confrontalo con
l'insieme delle chiavi di `build/nodes.json → nodes`. Se **differiscono in qualunque
modo** (una chiave in più,
una in meno, mai un rename silenzioso — un rename appare come "una tolta, una
aggiunta"):

```
RESYNC — FALLITO
L'insieme delle chiavi Indice è cambiato rispetto all'ultimo /tesi-ingest.
Aggiunte: {'7.5'}
Rimosse: {}
Questo non è un caso che /tesi-resync gestisce: serve un /tesi-ingest pulito.
Attenzione: un /tesi-ingest pulito NON preserva gli stati "scritto" già presenti nei
nodes/*.md esistenti in nodes.json — verificalo prima di rilanciarlo, e valuta se
serva prima un backup di nodes/.
```

**Fermati qui.** Non procedere al confronto per colonna, non aggiornare nulla. Il
conteggio nodi è già passato da 128 a 129 una volta durante il progetto: non è un caso
di scuola.

### 2. Confronto sha per colonna, solo se l'insieme delle chiavi è invariato

Per ogni nodo, ricalcola gli sha delle cinque colonne — `desc` (`Descrizione`), `fonti`
(`Fonti + ruolo`), `ruolo` (`Ruolo argomentativo`), `trappole` (`Trappole / rischi`),
`note` (`Note`, **dopo lo stesso filtro `[OFF-RECORD]` di `/tesi-ingest`**) — e
confrontali con `nodes.json → nodes.<id>.sha`.

- Nodo con **tutti e cinque gli sha invariati** → non toccato, `stato` resta quello che
  ha oggi (anche `"scritto"`).
- Nodo con **almeno uno sha diverso** → il contenuto del nodo è cambiato. Riporta quale
  colonna, e:
  - se `stato` era `"vuoto"` → aggiorna il record (nuovo `source_desc`/`fonti`/
    `ruolo`/`trappole`/`note`, nuovo `sha`, nuovo `source_words`). **Non ricalcolare
    `target_words`/`fit_ratio`/`regime` qui**: quei campi restano i placeholder di
    `/tesi-ingest` (`0`/`0.0`/`null`) anche dopo un resync, esattamente come dopo un
    ingest — la formula vive solo in `tools/gap.py`, che li ricalcola da sé al
    prossimo `/tesi-gap` a partire dai nuovi `source_words`. Non serve (e non va)
    duplicarla qui.
  - se `stato` era `"scritto"` → **torna a `"vuoto"`**, aggiorna il record come sopra.
    **La vecchia bozza non si cancella**: resta nella storia di git (l'ultimo commit
    `draft(<id>): ...` la contiene). `nodes/<id>.md` **non viene toccato da questa
    skill**: resta con il vecchio DRAFT finché `/tesi-draft` non lo riscrive, ma
    `nodes.json` già segnala `"vuoto"`, quindi `/tesi-status` mostra la discrepanza
    (DRAFT presente, stato "vuoto") come cosa attesa, non come anomalia.
- **Fonti ammesse/vietate** (colonne H/I del `DOSSIER`) possono cambiare senza che
  `desc` cambi (es. l'autore arbitra una coppia in `Estratti!R`): tienile fuori dagli
  sha delle cinque colonne (non fanno parte delle 5), ma **ricontrollale sempre**, a
  ogni nodo, e aggiorna `fonti_ammesse[]`/`fonti_vietate[]`/`fonti_vietate_dettaglio[]`/
  `risoluzioni[]` indipendentemente dagli sha di `desc`/`fonti`/`ruolo`/`trappole`/
  `note`. Se cambiano e il nodo era `"scritto"`, riportalo come "fonti cambiate,
  contenuto DRAFT invariato — verifica manuale consigliata" ma **non forzarlo a
  `"vuoto"`** solo per questo (una fonte diventata vietata dopo la stesura è un caso
  per `claim-auditor` al prossimo `/tesi-audit`, non per un ri-ingest automatico).
- **Ricalcola `metrics.json`** per intero, con la stessa funzione `ingest.build_metrics`
  (aggregati grezzi: `source_words` per capitolo, non `C_c`/`k_c` — quelli restano un
  calcolo di `/tesi-gap`, mai persistito).

### 3. Aggiorna lo snapshot

Ripeti lo snapshot di `/tesi-ingest` passo 1 (`source/manifest.json` e le tre copie),
sovrascrivendo quello vecchio: la provenienza deve riflettere l'ultimo stato letto.

## Formato output

```
RESYNC — 2026-09-08
Chiavi Indice: invariate (129)
Nodi con almeno una colonna cambiata: 3
  - 3.2.2: desc cambiata (rimosso il quarto indicatore, decisione 2026-09-06) —
    stato: scritto → vuoto. Vecchia bozza in git, commit a1b2c3d.
  - 4.3.3: note cambiata ([DECISIONE AUTORE] aggiunta) — stato: vuoto → vuoto (invariato,
    non ancora scritto)
  - 1.2.3: fonti cambiata (sciolte le sei fonti affollate) — stato: vuoto → vuoto
Nodi con sole fonti_ammesse/vietate cambiate (desc invariata): 1
  - 3.2.4: dierickxcool1989 passata da ammessa a vietata — stato "scritto" invariato,
    verifica consigliata al prossimo /tesi-audit 3
metrics.json: ricalcolato (Cap. 3: source_words 1.060 → 1.072)
Ricorda: rilancia /tesi-gap prima del prossimo /tesi-draft, i target_words dei
capitoli toccati sono cambiati e reports/gap.md non lo sa ancora.
Snapshot aggiornato in source/
```

## Postcondizioni

- Se le chiavi `Indice` sono cambiate, l'unico output è il messaggio di fallimento:
  nessun file viene toccato oltre alla lettura.
- Se le chiavi sono invariate, `nodes.json`, `metrics.json` e `source/` sono aggiornati
  e coerenti fra loro (stesso `generated_at`).
- Ogni nodo il cui `stato` è tornato a `"vuoto"` compare esplicitamente nel report, con
  il motivo (quale colonna) e il riferimento al commit che contiene la vecchia bozza.
- Nessun `nodes/<id>.md` viene modificato o cancellato da questa skill.

## Cosa non fa mai

- Non gestisce righe aggiunte o rimosse: fallisce esplicitamente e basta.
- Non cancella un DRAFT esistente, nemmeno quando il nodo torna a `"vuoto"`.
- Non riscrive l'Excel.
- Non lancia `/tesi-draft` né alcun agente: si limita ad aggiornare lo stato.
- Non assume che un nodo padre invariato implichi figli invariati, né il contrario.
