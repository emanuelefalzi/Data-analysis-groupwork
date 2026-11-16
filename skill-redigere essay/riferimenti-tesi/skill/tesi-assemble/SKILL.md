---
name: tesi-assemble
description: Genera out/tesi.docx da LF3236167.docx inserendo i DRAFT dei nodi, le matrici e la bibliografia. Rifiuta se un nodo in perimetro non ha DRAFT, se GATE 1 (domanda 3, sede di abstract/introduzione/reference list) non ha risposta, o se tools/assemble.py non esiste ancora. Usala solo dopo GATE 3-bis.
---

# /tesi-assemble

Scrive **solo** `out/tesi.docx`. Non tocca `LF3236167.docx` (lo copia), non tocca
`nodes/`, non tocca l'Excel.

## PREREQUISITO MANCANTE — leggi prima di tutto

**`tools/assemble.py` non esiste.** `tools/README.md` lo dichiara esplicitamente e
spiega perché: dipende da decisioni ancora aperte a GATE 1 (dove vivono abstract,
introduzione e reference list; il budget di pagine definitivo). Uno script scritto
prima di quella risposta assemblerebbe un documento che punta a una reference list o a
una sede di abstract inesistente. **Va scritto dopo GATE 1, non prima.**

Finché `tools/assemble.py` non esiste su disco, questa skill **si ferma al primo passo**
e non tenta di sostituirlo con logica improvvisata dentro la conversazione: il contratto
sotto ("Passi", punto 2) descrive cosa quello script dovrà fare quando qualcuno lo
scriverà, non una ricetta da eseguire a mano nel frattempo. Verifica sempre prima di
procedere:

```bash
test -f "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/assemble.py" \
  && echo "assemble.py trovato" || echo "assemble.py assente — fermati, vedi tools/README.md"
```

Se manca, il formato output è il rifiuto della sezione "Formato output" sotto, motivo
`tools/assemble.py non esiste ancora (vedi tools/README.md)`, e non si procede oltre.

## Precondizioni — verificale in quest'ordine, fermati alla prima che fallisce

0. **`tools/assemble.py` esiste** (vedi sopra). Se manca, fermati qui: nessuna delle
   precondizioni seguenti va nemmeno controllata.
1. **Nessun lock file** su `LF3236167.docx` (`~$LF3236167.docx`): se esiste, fermati,
   Word ha il template aperto.
2. **Ogni nodo in perimetro (capitoli 0-6, esclusi quelli senza materiale) ha un
   `## DRAFT` non vuoto** in `nodes/<id>.md`. `nodes.json → stato` vale solo
   `"vuoto"`/`"scritto"` (non esiste un valore `"⚠ RICHIESTA AUTORE"` scritto da
   nessuno script): un nodo senza materiale si riconosce da `source_words == 0`, non
   dallo `stato`. Verifica con:
   ```bash
   /usr/bin/python3 -c "
   import json, re, pathlib
   BASE = pathlib.Path('/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura')
   nodes = json.load(open(BASE/'build/nodes.json'))['nodes']
   mancanti = []
   for idx, n in nodes.items():
       if n['chapter'] == '7': continue
       if n.get('source_words', 0) == 0: continue
       p = BASE / 'nodes' / f'{idx}.md'
       txt = p.read_text() if p.exists() else ''
       m = re.search(r'## DRAFT\s*\n(.*?)(?=\n## LEDGER|\Z)', txt, re.S)
       if not m or not m.group(1).strip():
           mancanti.append(idx)
   print(len(mancanti), mancanti)
   "
   ```
   Se `mancanti` non è vuoto, **rifiuta** l'assemblaggio e elenca i nodi mancanti. Non
   assemblare un documento parziale "per vedere come viene".
3. **GATE 1 domanda 3 ha risposta** (`decisions/DECISIONS.md` dichiara dove vivono
   abstract, introduzione e reference list). Se manca, **rifiuta**: non c'è una sede nel
   documento dove collocare la reference list già prodotta da `bibliography-builder`.
4. **GATE 3-bis chiuso**: `reports/escalation.md` non ha voci senza una delle tre
   etichette di chiusura (`fonte trovata`, `claim ritirato`,
   `dichiarato come estensione teorica`). Se ne trovi anche una sola aperta, **rifiuta**.
5. **Le citazioni sono già risolte, non lo fai qui**: in tutti i `nodes/*.md` in
   perimetro non deve comparire più nessun `[[CIT-N:` o `[[CIT-P:` — quel lavoro è
   dell'agente `bibliography-builder`, che gira per capitolo subito dopo che quel
   capitolo ha superato il proprio audit, **prima** di arrivare qui. Se ne trovi ancora
   uno, **non lo risolvi tu**: significa che `bibliography-builder` non è ancora passato
   su quel capitolo — fermati e invocalo lì, non dentro questa skill. Restano ammessi, e
   bloccano comunque l'assemblaggio, `[[GAP:` e `[[CIT-NEEDED:`: verificalo prima di
   scrivere il `.docx`, non dopo — `final-check` lo riverifica sul file generato, ma qui
   è più economico fermarsi prima.
6. **`build/bibliography.md` esiste**, prodotto da `bibliography-builder` (non da questa
   skill): la reference list già formattata in APA 7, limitata alle chiavi
   effettivamente citate. Se manca, fermati: non la rigeneri qui da `FONTI/tesi.bib`,
   sarebbe rifare a mano il lavoro di un agente che esiste apposta.
7. **`build/matrici.json` esiste**, prodotto dall'orchestratore (non da questa skill:
   §4.6 del prompt orchestratore assegna l'estrazione delle 4 matrici e delle 2 tabelle
   del Cap. 5 all'orchestratore stesso). Se manca, fermati e chiedi che venga prodotto
   prima: `table-inserter` lo consuma, non lo genera, e nemmeno questa skill lo fa.

## Passi

### 1. Verifica il prerequisito e le precondizioni sopra

Se una qualunque fallisce, rifiuta esplicitamente (vedi "Formato output"). Non procedere
"per vedere come viene" con una precondizione mancante.

### 2. Esegui `tools/assemble.py` (quando esiste)

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/assemble.py"
```

Contratto per `tools/assemble.py` — **solo struttura e testo già risolto, mai
citazioni o matrici**: quel lavoro è di `bibliography-builder` e `table-inserter`
(passo 3 sotto), non di questo script. Chi lo scrive dopo GATE 1 implementa:

1. **Copia** `LF3236167.docx` → `out/tesi.docx`. Non parte da un documento vuoto: il
   front matter, le 3 sezioni con i rispettivi `sectPr`, la numerazione romana della
   sezione indice e quella araba del corpo, i `footerReference` restano quelli del
   template, intatti.
2. **Rimuove i tre heading segnaposto vivi** (`Heading1` "Rq", `Heading2` "Ff",
   `Heading3` vuoto) da `document.xml` **prima** di inserire il corpo — altrimenti
   ereditano la numerazione dello stile e il primo `Heading 1` vero (Capitolo 1) diventa
   `2.` invece di `1.`.
3. **Inserisce il corpo solo fra il secondo section break e il `sectPr` finale**: non
   ricostruisce il documento, inserisce paragrafi. Per ogni nodo in perimetro, nell'ordine
   di `Indice`:
   - livello 1 → paragrafo `Heading 1`, testo = solo `title` (**mai** il numero:
     Word lo antepone da sé via `numId="3"`);
   - livello 2 → `Heading 2`; livello 3 → `Heading 3`; stessa regola sul numero;
   - corpo del DRAFT → paragrafi `Normal`, uno per paragrafo del DRAFT, **copiato così
     com'è** (il LEDGER **non** entra mai nel `.docx`: si rimuove in questo passo). Le
     citazioni sono già in forma `Autore (Anno)` / `(Autore, Anno)`: `bibliography-builder`
     le ha risolte nel `DRAFT` prima che questo script girasse, quindi qui non c'è
     nessun token `[[CIT-*]]` da interpretare — se ce n'è ancora uno, è una precondizione
     saltata (vedi sopra), non un caso da gestire qui;
   - sul nodo `0` e i suoi discendenti (se numerati come indice `0.x`), sopprimi la
     numerazione **a livello di paragrafo**: `<w:numPr><w:ilvl w:val="0"/><w:numId
     w:val="0"/></w:numPr>` nel `pPr` di quel titolo. È l'unica formattazione diretta
     ammessa oltre al corsivo delle didascalie (che aggiunge `table-inserter`, non
     questo script).
   - **non** inserire interruzioni di pagina manuali: `Heading 1` ha già
     `pageBreakBefore` nello stile.
4. **Inserisce la reference list** in coda al corpo, nella posizione decisa da GATE 1
   domanda 3, **copiando il contenuto già pronto di `build/bibliography.md`** — non lo
   rigenera da `FONTI/tesi.bib`: quel lavoro (alfabetizzazione, autori multipli,
   filtraggio alle sole chiavi citate) è già stato fatto da `bibliography-builder`.
5. **Svuota la cache del campo TOC** (`w:sdt` con `TOC \o "1-3" \h \z \u`): la cache
   salvata è di una versione precedente e contiene voci con `{N pp}` nei titoli. Dopo
   questo passo Word deve mostrare "aggiorna campo", non i dati vecchi. **Nessun agente
   scrive il TOC a mano.**
6. **Non tocca** stili, font, colori, margini, `sectPr`, header/footer. Nel corpo usa
   solo `Heading 1/2/3` e `Normal`. Non inserisce tabelle: quello è `table-inserter`
   (passo 3 sotto), che gira dopo, quando i paragrafi-ancora esistono già nel `.docx`.
7. **Non forza `en-GB` o alcun `w:lang` sui run**: lo stile `Normal` porta già
   `w:lang="en-US"`.

### 3. Invoca `table-inserter` per le 4 matrici e le 2 tabelle del Cap. 5

**Non reimplementare qui l'inserimento delle tabelle**: invoca l'agente
`table-inserter` (Sonnet, tool Agent/Task) con `build/matrici.json` e il
`out/tesi.docx` appena prodotto dal passo 2 — gli servono i paragrafi del corpo già
inseriti per trovare gli `anchor_node`. Se `build/matrici.json` non esiste ancora,
non lo generi tu: fermati e dillo (precondizione 7).

`table-inserter` aggiorna `out/tesi.docx` in place e scrive il proprio report in
`reports/table-inserter.md`. Riporta il suo esito (tabelle inserite, tabelle saltate e
perché) nel formato output finale di questa skill, non lo riscrivi con parole tue.

## Formato output

```
ASSEMBLE — 2026-09-08
out/tesi.docx generato da LF3236167.docx (copia, sha256 del template invariato)
Nodi inseriti: 100/100 in perimetro (Cap. 7 escluso, 29 nodi, per decisione)
Heading segnaposto rimossi: 3 (Rq, Ff, vuoto)
Reference list inserita da build/bibliography.md: 52 voci
Matrici (table-inserter): 4 + 2 tabelle Cap. 5 inserite, 0 saltate
Cache TOC svuotata: sì
Token residui: 0
```

Se il prerequisito o una qualunque precondizione fallisce, il formato output è un
rifiuto esplicito, non un documento parziale:

```
ASSEMBLE — RIFIUTATO
Motivo: tools/assemble.py non esiste ancora (vedi tools/README.md — dipende da GATE 1)
out/tesi.docx non toccato.
```

```
ASSEMBLE — RIFIUTATO
Motivo: 4 nodi senza DRAFT (0.1, 0.1.1, 1.2, 6 hanno source_words=0 — OK, esclusi;
ma 4.2.1 e 5.3.2 sono "vuoto" e non dovrebbero esserlo)
out/tesi.docx non toccato.
```

## Postcondizioni

- `out/tesi.docx` esiste, si apre (verificalo aprendo il file con `python-docx` in
  lettura, non serve Word per questo controllo minimo), e il numero di `Heading 1` nel
  corpo è **7** (capitoli 1-7 nell'Excel, ma solo 6 scritti — il conteggio reale atteso
  oggi è 6, perché il Cap. 7 non entra: verifica contro il numero di capitoli
  effettivamente in perimetro, non un 7 fisso).
- Nessun `[[` sopravvive nel testo del `.docx` (stessa verifica di `final-check`, qui
  in anticipo).
- Il file `LF3236167.docx` originale è bit-per-bit invariato (confronta sha256 prima e
  dopo l'esecuzione).
- Lo stile `Normal` del `.docx` generato ha ancora `w:line="460" w:lineRule="exact"` e
  font Times New Roman: se è cambiato, qualcosa ha toccato gli stili, e questa skill ha
  violato il proprio vincolo più importante.
- Le 4 matrici e le 2 tabelle del Cap. 5 sono tabelle Word vere (`TableNormal`), non
  prosa: inserite da `table-inserter`, mai da questa skill a mano.

## Cosa non fa mai

- Non gira se `tools/assemble.py` non esiste: non lo sostituisce con una ricetta manuale.
- Non genera un documento se anche un solo nodo in perimetro manca di DRAFT.
- Non assembla senza risposta a GATE 1 domanda 3.
- Non assembla con `reports/escalation.md` non chiuso.
- Non risolve un token `[[CIT-N:`/`[[CIT-P:` a mano: se ne trova uno significa che
  `bibliography-builder` non è ancora passato su quel capitolo, e va invocato lì, non
  qui.
- Non genera né rigenera `build/bibliography.md`: lo consuma, prodotto da
  `bibliography-builder`.
- Non inserisce matrici o tabelle a mano: le inserisce `table-inserter`, invocato al
  passo 3.
- Non tocca stili, `sectPr`, header, footer, margini, font del template.
- Non scrive il numero di capitolo/sezione dentro il testo del titolo.
- Non scrive un TOC a mano: si limita a svuotare la cache perché Word lo rigeneri con F9.
- Non genera `LF3236167.pdf`, non rimuove metadati, non conta le pagine reali: quelli
  sono passi manuali della FASE DI CONSEGNA (§10 del prompt orchestratore), fuori da
  questa skill.
- Non include il Capitolo 7.
- Non include l'abstract nel documento (va nel form d'ateneo, mai nel `.docx`).
