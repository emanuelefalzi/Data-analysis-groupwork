---
name: tesi-draft
description: Invoca l'agente node-writer sui nodi in stato "vuoto" di un capitolo o di un singolo nodo. Sequenziale dentro il capitolo, parallelo solo fra capitoli diversi. Usala solo dopo GATE 1 (e GATE 2 per lo stile) e, sul Cap. 5, solo dopo l'approvazione autore del taglio.
---

# /tesi-draft \<id|capitolo\>

Scrive prosa. È l'unica skill, insieme al percorso di riscrittura strutturale di
`/tesi-fix`, che produce testo di tesi. Chi scrive non giudica: questa skill non lancia
mai un auditor, non decide se il proprio output va bene.

Argomento: un `id` di nodo singolo (es. `3.1.1`) oppure un numero di capitolo
(es. `3`, che espande a tutti i nodi in `stato: "vuoto"` di quel capitolo, in ordine di
`Indice`).

## Precondizioni

1. **`build/nodes.json` esiste** ed è stato prodotto dopo l'ultimo `/tesi-resync`
   (confronta `generated_at` con l'mtime di `iTOC master.xlsx`: se l'Excel è più
   recente, fermati, serve un resync).
2. **GATE 1 superato**: esiste una risposta dell'autore alle 4 domande di
   `reports/gap.md`, registrata in `decisions/DECISIONS.md`. Se manca, fermati: non
   indovinare la risposta.
3. **Se il target include il Cap. 3**: nessuna precondizione ulteriore, è il pilota
   (§10). Per **tutti gli altri capitoli**, verifica che il Cap. 3 sia già stato scritto,
   auditato e che l'autore abbia dato l'OK di stile (GATE 3) — cercalo in
   `decisions/DECISIONS.md`. Se manca, fermati e segnalalo: l'ordine `3 → 1 → 2 → 4 →
   [taglio Cap.5] → 5 → 6` non è arbitrario, il Cap. 3 calibra lo stile per tutti gli
   altri.
4. **Se il target include il Cap. 5**: verifica che `decisions/DECISIONS.md` contenga
   un'approvazione esplicita dell'autore al taglio proposto per il Cap. 5. Se manca,
   **rifiuta di scrivere il Cap. 5** e dillo: "Cap. 5 in attesa di approvazione taglio,
   non scrivo." Non procedere "nel frattempo" su una sottoparte.
5. **Nessun nodo target è senza materiale o in conflitto non risolto**: `nodes.json`
   **non** porta uno stato di blocco (il campo `stato` resta sempre `"vuoto"` o
   `"scritto"` — vedi `/tesi-ingest`), quindi il blocco lo verifichi leggendo il gap
   report fresco (passo 0 sotto): un nodo con `source_words == 0` (elencato in "Nodi
   senza materiale") si salta sempre; un capitolo con `capitolo_bloccato_k: true` va
   scritto comunque **se** l'autore ha approvato il da farsi (per il Cap. 5, il taglio
   di precondizione 4) — il blocco a livello di capitolo non è un blocco per nodo.
6. Se l'`id` richiesto esplicitamente compare in "Nodi senza materiale" **o** in "Nodi
   bloccati da audit_aperto" nel gap report, **rifiuta** e spiega perché (cita il gap
   report). Un nodo in quella seconda lista porta almeno un rilievo `[AUDIT ...]`
   `bloccante` e ancora `aperto` nel foglio `AUDIT 2026-09-07` (§3): non è materia del
   `node-writer` scegliere fra le alternative che quel blocco lascia aperte, va a
   `⚠ RICHIESTA AUTORE` e resta fra le domande del GATE 1 finché l'autore non decide.

## Passi

### 0. Ottieni `target_words`/`fit_ratio`/`regime` freschi per il capitolo

`nodes.json` **non** li contiene (sono sempre `0`/`0.0`/`null`, placeholder di
`/tesi-ingest`): vanno letti dall'output di `tools/gap.py`, **con `--dry-run`** per non
sovrascrivere `reports/gap.md` (che resta il report ufficiale di GATE 1):

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/gap.py" --chapter <capitolo> --dry-run
```

Da questo output prendi, per ogni nodo del capitolo: `target_words`, `fit_ratio`,
`classe`, `regime` (uno fra `compressione`/`resa`/`espansione`, già calcolato: **non lo
ricalcoli tu né il writer**), `conflitto_ruolo`; e per il capitolo: `capitolo_bloccato_k`,
`capienza_strutturale_rotta`. Leggi anche la sezione "Nodi bloccati da audit_aperto":
qualunque id lì elencato è escluso dal passo 1, a prescindere da `stato`/`source_words`.
`--dry-run` forza anche la lettura diretta dell'Excel (non di `nodes.json`): verifica
quindi che non ci sia un lock file prima di lanciarlo, stessa precondizione di
`/tesi-ingest`.

### 1. Determina l'ordine

Se l'argomento è un capitolo, elenca tutti i nodi di quel capitolo con
`stato: "vuoto"` in `nodes.json` **e** `source_words > 0` (non presenti in "Nodi senza
materiale" del passo 0) **e non presenti in "Nodi bloccati da audit_aperto" del passo
0**, **ordinati per `Indice`** (ordine gerarchico: un padre prima dei suoi figli, un
figlio prima del fratello successivo). Il flusso è sequenziale dentro il capitolo: il
nodo N+1 riceve come contesto la prosa già scritta del nodo N (per l'aggancio), quindi
non puoi scrivere N+1 prima che N esista.

Un nodo saltato perché bloccato da `audit_aperto` **non rompe la sequenza**: il nodo
successivo riceve come "fratello precedente" l'ultimo nodo effettivamente scritto, non
quello saltato — esattamente come già previsto al passo 2 per un fratello non ancora
scritto.

Se l'argomento è più di un capitolo (chiamate parallele di questa skill su capitoli
diversi), ciascuna chiamata è indipendente: i capitoli non si scrivono a coppie di
fratelli, ma l'uno non aspetta l'altro.

### 2. Per ogni nodo, nell'ordine

Costruisci il contesto per `node-writer` (agente Sonnet, non uno script: invocalo con
lo strumento Agent/Task, `subagent_type` o profilo `node-writer` se definito in
`.claude/agents/`, altrimenti passa questo stesso brief come prompt di un agente
generico su Sonnet — mai su Opus) con **esattamente**:

- il record del nodo da `nodes.json` (`source_desc`, `fonti_ammesse[]`,
  `fonti_vietate[]`, `ruolo`, `trappole`, `note`, `risoluzioni[]`);
- `target_words`, `fit_ratio`, `regime` del nodo, letti dal passo 0 (**non** dai
  placeholder di `nodes.json`);
- le righe di `estratti.json` per quel nodo — filtra il dizionario piatto per chiave
  che inizia per `"<id-nodo>|"` (i blocchi `Cosa dice davvero` e `Citazione verbatim` —
  quest'ultima solo come riferimento di verifica, mai da citare testualmente);
- il record del nodo padre (per continuità di registro, non da citare come fonte);
- il `## DRAFT` (prosa, non il LEDGER) dei fratelli precedente e successivo **già
  scritti** in questo giro — se il fratello precedente non è ancora scritto (perché
  bloccato o `⚠ RICHIESTA AUTORE`), passa solo il testo che esiste, non inventare un
  aggancio;
- `source_desc` e `title` (**mai la prosa**) del **nodo successivo nell'ordine di
  lettura**, con il divieto esplicito, nel prompt stesso: *"Usalo solo per costruire la
  frase di aggancio richiesta dal campo Aggancio, se presente. Non è materiale
  citabile: non contiene un'affermazione che tu possa attribuire a questo nodo."*
- il glossario (`FONTI/pipeline/glossario/glossario.json`), in sola lettura;
- le 12 regole di stesura di `CONTESTO-per-orchestratore.md` §5 e le convenzioni di
  `CLAUDE.md` (tempi verbali, persona, niente "the company").

**Istruzioni di regime**, testuali, da includere nel prompt dell'agente:

- `regime: "resa"` (`fit_ratio` 0,85-1,20) → rendi in prosa a lunghezza comparabile,
  la `Descrizione` è già prosa argomentata, non appunti da sviluppare.
- `regime: "compressione"` (`fit_ratio` 0,55-0,85) → **stessa sostanza, meno parole**:
  togli ridondanze, subordinate, riformulazioni. **Non cade mai un'affermazione.** Se non
  ci riesci senza perderne una, fermati sul nodo e scrivi nel `## DRAFT` (in cima, come
  commento HTML che `/tesi-assemble` scarterà) `<!-- ⚠ COMPRESSIONE NON RAGGIUNGIBILE -->`
  seguito dal motivo, e non produrre un draft parziale che nasconde il problema.
- `regime: "espansione"` (`fit_ratio` 1,20-1,50) → esplicita quello che la `Descrizione`
  implica, costruisci le transizioni degli "Aggancio", sviluppa il ragionamento
  presente. **Non aggiungere contenuto non derivabile dal materiale.**
- I due estremi di `fit_ratio` (`< 0,55` e `> 1,50`) non sono un quarto regime: sono
  stati. Un nodo lì non arriva a questo passo — è già `⚠ RICHIESTA AUTORE` con
  `target_words = 0` dal passo 0.
- **`target_words` ±15%, nessun pavimento.** Un nodo che finisce sotto banda anche dopo
  aver usato tutto il materiale disponibile si dichiara corto nel `## LEDGER` con
  `[[GAP: motivo]]`, non si allunga con materiale non presente in `source_desc`.

**Regola della cucitura** (§7, obbligatoria nel prompt): il periodo che porta una
citazione contiene solo ciò che `Cosa dice davvero` dice; l'estensione della tesi va in
un periodo separato o introdotta da *building on / applied to / transposed here / this
thesis operationalizes*. Sulle coppie `da riformulare`, il claim si restringe secondo
`Cosa dice davvero`, mai si allarga; se la restrizione fa cadere l'affermazione, il nodo
riceve `[[GAP: …]]`, non si riscrive a memoria.

**Divieto di fonti nuove**: solo le chiavi in `fonti_ammesse[]` del nodo. Mancanze:
`[[CIT-NEEDED: motivo]]`. Token citazione: `[[CIT-N:chiave]]` (narrativa) /
`[[CIT-P:chiave]]` (parentetica) — mai un token unico.

L'agente scrive **sia** il `## DRAFT` **sia** il `## LEDGER` nello stesso file
`nodes/<id>.md`, sovrascrivendo il file (che a questo punto ha solo le due intestazioni
vuote prodotte da `/tesi-ingest`). Formato LEDGER, esatto (§6):

```markdown
## LEDGER
- ¶1 ← SOURCE["prima frase esatta dello span in source_desc"] | RUOLO[deve_dimostrare]
- ¶2 ← SOURCE["..."] + ESTRATTI[<id_fonte>|<regime>]
- ¶3 ← ⚠ NESSUNA FONTE — collegamento inferito dall'Aggancio di <id successivo>. Da validare.
- ¶4 ← [[GAP: fatto su ELFO non presente nell'Excel]]
```

Ogni riga del LEDGER cita la **prima frase in chiaro** dello span di `source_desc`, mai
un offset di carattere.

### 3. Dopo aver scritto il nodo

Aggiorna `stato` in `nodes.json` da `"vuoto"` a `"scritto"` per quel nodo (script
minimo, non l'agente: l'agente non tocca `nodes.json`). Passa al nodo successivo
nell'ordine, ripetendo il passo 2 con il DRAFT appena prodotto disponibile come contesto
del fratello precedente.

### 4. Commit

Un commit per nodo (non per capitolo), messaggio `draft(<id>): prima stesura`. Se il
repo git non esiste ancora in questa cartella, inizializzalo (`git init`) prima del
primo commit — non è compito di questa skill creare `.gitignore`, che esiste già.

## Formato output

Al termine, riporta per il capitolo (o il nodo) processato:

```
DRAFT — capitolo 3, 2026-09-08
Scritti: 3.1, 3.1.1, 3.1.2, 3.2, 3.2.1, ... (8/8 foglie)
Saltati (senza materiale): nessuno
Saltati (bloccati da audit_aperto): nessuno   # es. capitolo con 3.2.2 in perimetro:
                                              # "3.2.2 (CL-01, bloccante+aperto)"
Nodi con [[GAP: ...]]: 3.2.4 (1 occorrenza)
Nodi sotto target_words: nessuno
Commit: 8, da <hash> a <hash>
```

## Postcondizioni

- Ogni nodo processato ha `## DRAFT` non vuoto e `## LEDGER` con tante righe `¶N` quanti
  sono i paragrafi del DRAFT (nessuno sfasamento).
- Nessun `nodes/<id>.md` contiene una citazione testuale (frase copiata parola per
  parola da `Citazione verbatim` senza parafrasarla): è compito del lint n-grammi
  verificarlo in `/tesi-audit`, ma non produrre deliberatamente ciò che sai che il lint
  bloccherà.
- Nessun nodo scritto supera ±15% di `target_words` senza una nota `[[GAP: …]]` che lo
  spieghi.
- `stato` è `"scritto"` per ogni nodo effettivamente processato, invariato per quelli
  saltati.

## Cosa non fa mai

- Non gira nessun auditor: non decide da sola se il proprio output è accettabile.
- Non scrive un nodo elencato in "Nodi senza materiale" nel gap report
  (`source_words == 0`), né uno elencato in "Nodi bloccati da audit_aperto"
  (rilievo `[AUDIT ...]` bloccante e ancora aperto in `AUDIT 2026-09-07`): li salta e li
  riporta, non li scrive.
- Non scrive il Cap. 5 senza l'approvazione esplicita del taglio in `decisions/DECISIONS.md`.
- Non scrive il Capitolo 7.
- Non usa il web, non cerca fonti nuove, non usa la propria conoscenza generale del
  dominio oltre a `source_desc` ed `Estratti`.
- Non tocca `def titolo C_EN.docx`: non è mai fra gli input passati all'agente.
- Non gira due nodi fratelli in parallelo dentro lo stesso capitolo.
