# Prompt: costruzione dell'orchestratore di stesura tesi

> Da incollare in una sessione Claude Code **pulita**, aperta sulla cartella
> `/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura`.
> Questo prompt NON scrive la tesi: costruisce la macchina che la scrive.
> Leggi prima `CONTESTO-per-orchestratore.md`: dice a che punto è il lavoro.
> La stesura parte solo dopo i gate di §10.
>
> *Rev. 2026-09-08. Sostituisce la versione del 2026-09-03: quella versione dava per
> buoni numeri e file smentiti da un audit di coerenza e da una riconta puntuale — fogli
> dell'Excel, voci di `tesi.bib`, occorrenze in `def titolo C_EN.docx`, formato reale del
> `.docx` — e conteneva nove punti (gate delle fonti, note dell'autore, numerazione Word)
> su cui la macchina si sarebbe inceppata prima di scrivere una riga usabile. Copia di
> sicurezza in
> `iTOC master backup/PROMPT-orchestratore-tesi.20260908_000433_pre-riscrittura.md`.*

---

## 0. Ruolo e obiettivo

Sei l'architetto di una pipeline di scrittura accademica. Devi costruire, in questa
cartella, una struttura di orchestrazione (agenti + skill + file di stato) che porti da
`iTOC master.xlsx` a un file Word impaginato in inglese accademico. Il budget di pagine
vale oggi **32** (colonna `Budget pp` dell'`iTOC`, di cui 30 in perimetro e 2 al Cap. 7,
che non si scrive) ed è una delle domande del GATE 1: vedi §3 e §10.

Non scrivi tu i capitoli. Costruisci il sistema, poi ti fermi e riporti.

**Regola sovrana, valida per ogni agente che creerai:**
il testo della tesi non contiene alcuna affermazione che non sia già presente,
esplicitamente o come conseguenza diretta, nella colonna `Descrizione` o nel foglio
`Estratti`. Tutto il resto è materiale da *chiedere all'autore*, mai colmato dal
modello. Un buco dichiarato vale infinitamente più di un buco riempito bene.

Tu, Opus, orchestri e validi. **Tutti gli agenti che esegui — chi scrive e chi
controlla — girano su Sonnet, senza eccezioni.** La revisione precedente riservava
`claim-auditor` e `chapter-auditor` a Opus: decisione dell'autore del 2026-09-08, e
questa la sostituisce. La capacità di controllo che un modello più grande darebbe in più
non si compra con un modello più grande: si compra con **più agenti indipendenti e più
giri**. Ogni auditor gira come due istanze separate sullo stesso capitolo, in contesto
pulito, che non si vedono fra loro; i finding su cui le due istanze concordano passano,
i discordi li arbitri tu. È lo stesso schema del doppio lettore indipendente già in uso,
e già validato, sul loop di verifica delle fonti che ha prodotto `Estratti`. Opus resta
solo per te: tu non scrivi né correggi mai una riga di tesi.

---

## 1. Input, e cosa non si tocca

**L'Excel si modifica solo prima di `/tesi-ingest`, e solo a mano dall'autore
(FASE 0, §10).** `/tesi-resync` esiste per gli errori residui, non è un canale di
modifica: non sa riconoscere righe aggiunte o rimosse (fallisce esplicitamente se
l'insieme delle chiavi `Indice` è cambiato, §10), e una modifica a un nodo padre non
invalida da sola i figli, che restano agganciati a una versione che non esiste più.

**`FONTI/pipeline/dossier.py` fa `wb.save()` sullo stesso `iTOC master.xlsx`: la sua
ultima esecuzione è l'ultimo atto della FASE 0, prima dello snapshot in `source/`.**
Dopo GATE 0 rigirarlo è vietato: rigenerare il `DOSSIER` cambia lo sha del file che stai
per congelare, ed è il motivo per cui lo sha del file congelato è affidabile solo se
questo ordine è rispettato.

**Sorgenti (sola lettura, mai modificate in place):**

- `iTOC master.xlsx` — **sette** fogli: `iTOC` (129 nodi + 1 riga di totale
  `TOTALE pp attese`), `DOSSIER`, `Fonti` (67 righe: 64 `scaricata`, 2 `abbandonata`, 1 `da_cercare` — `giray2025`, che non ha ancora il PDF), `Estratti` (108 coppie
  nodo×fonte), `Legenda`, `AUDIT 2026-09-07`, `PROSSIMI PASSI`. Leggili tutti prima di
  qualunque altra cosa. **Il foglio da cui scrivi è `DOSSIER`, non `iTOC` + `Estratti`
  ricombinati a mano**: il `DOSSIER` è già la vista che incrocia i due, con colonna H
  `Fonti AMMESSE` e colonna I `Fonti VIETATE` a dare il verdetto per ogni coppia
  (nodo, fonte) — 100 ammesse, 8 vietate — e colonna O `Note autore` con le `Note` di
  `iTOC!F` copiate verbatim. Il gate delle fonti (§7) si legge da lì, mai da
  `Estratti!Esito`.
- `LF3236167.docx` — **base dell'output.** È un file di impaginazione dell'autore
  (`dc:creator = Emanuele Falzi`), non un template distribuito dall'ateneo: segue la
  convenzione di nome `LF<matricola>` richiesta per la consegna. L'autore lo ha
  alleggerito apposta. La conformità formale va verificata contro
  `info & contesto/guide.pdf` §10.3, non assunta — il file esiste in questa cartella,
  leggilo tu.
- `def titolo C_EN.docx` — materiale di lavoro, **mai passato a un agente che scrive
  testo di tesi.** Contiene le 4 matrici, il glossario, la research question, le
  sotto-domande e **un abstract già scritto**. Su quell'abstract la regola è precisa,
  perché altrimenti si contraddice con §4.6: **il file non si passa mai a
  `front-back-matter`**, come a nessun altro agente che scrive. Sei tu a leggerlo, a
  estrarne il contenuto e a passarlo all'agente come **materiale di partenza in chiaro**,
  ripulito dalle fonti fantasma. L'abstract che ne esce **non entra nel documento**: si
  digita nel form web dell'ateneo, massimo 4.000 caratteri (§10). Contiene anche un blocco `Additional notes`
  che nomina fonti fuori bibliografia con la forma "X (anno): To be cited in order
  to…" — **13 occorrenze, non 7** — ed è un vettore di iniezione di fonti: **lo
  consulti solo tu**, mai un writer. Il file è **arretrato rispetto all'Excel**:
  contiene ancora `ADD CLASSIFICATION CRITERIA` e `Medium/high` — i rilievi `RC-03` e
  `RC-04`, mai applicati — e non ha più la colonna `Where it lives` che una versione
  precedente di questo prompt descriveva. **Riconcilia le matrici con l'Excel prima di
  usarle** (dettaglio in §4.6): non copiarle così come stanno nel
  `.docx`.
- `def titolo C.docx` — versione italiana, superata. Ignora.
- `CONTESTO-per-orchestratore.md` — stato del lavoro, situazione fonti, regole di
  stesura §5 e decisioni dell'autore §6. **Vale solo per metodo, vincoli e intenzioni:
  sui numeri è superato e lo dichiara da sé nel cartiglio in testa.** Precedenza, quando
  divergono: l'**Excel** batte tutto, poi questo prompt, poi `CONTESTO`. Se trovi in
  `CONTESTO` una cifra diversa da quella del §1 di questo documento, è vecchia: non
  usarla e non fermarti a riconciliarla.
- `tesi.bib` — **65** voci BibTeX. Linee guida d'ateneo per le citazioni, entrambe in
  `info & contesto/`: `guide.pdf` e
  `Linee-guida_per_la_citazione_bibliografica…pdf` — esistono davvero, **non
  chiederle all'autore**: leggile tu prima di costruire `bibliography-builder` (§4.6).

**Vincoli di formattazione, non negoziabili:**

- Non modificare stili, font, colori, margini, `sectPr`, header/footer del `.docx`.
- Nel corpo puoi usare **soltanto** `Heading 1`, `Heading 2`, `Heading 3` e `Normal`.
  Niente `List Paragraph`, niente stili nuovi, niente formattazione diretta applicata
  ai run — con **una sola eccezione**: il corsivo per le didascalie delle tabelle (il
  template non ha uno stile `Caption`). **Non imporre `en-GB`, o qualunque `w:lang`,
  sui run**: lo stile `Normal` porta già `w:lang w:val="en-US"`, e forzarlo riga per
  riga è esattamente la formattazione diretta che questo punto vieta, oltre a produrre
  un documento a due lingue. Se un giorno serve `en-GB` si cambia lo stile `Normal` una
  volta sola, non i run. Gli stili restano quelli che sono: `Heading 1` è Arial
  grassetto quasi nero (`0D0D0D`), `Heading 2/3` sono Arial `0F4761`. È formattazione
  **di stile**, legittima.
- Il font del corpo è **Times New Roman**, non Aptos, con interlinea **esatta 23,00
  pt**, non 1,15: lo stile `Normal` sovrascrive il tema. Le capacità che ne derivano —
  parole per pagina, righe per pagina — si calcolano in §3: qui ti basta sapere che non
  si tocca.
- L'output va in `out/tesi.docx`, generato da una copia di `LF3236167.docx` lasciando
  intatti il front matter, le 3 sezioni con i rispettivi `sectPr`, la numerazione
  romana della sezione indice e quella araba del corpo, i `footerReference`. Il corpo
  si inserisce **solo** fra il secondo section break e il `sectPr` finale: non
  ricostruire il documento, inserisci paragrafi.
- **Prima dell'ingest, Word ed Excel devono essere chiusi.** Se esiste un file `~$*`,
  fermati e segnalalo: non cancellarlo. Copia le sorgenti in `source/` registrando
  sha256 e mtime, e dichiara lo snapshot nel report.

### Numerazione automatica — leggi due volte

`Heading 1/2/3` di `LF3236167.docx` hanno numerazione automatica, ma **non tramite
`w:numPr` nei paragrafi**: `document.xml` ne ha **zero occorrenze**. La numerazione sta
sugli **stili**: `styles.xml` collega `Heading1`, `Heading2` e `Heading3` a `numId="3"`
→ `abstractNum` 2, `numFmt="decimal"`, `lvlText` `%1.`, `%1.%2.`, `%1.%2.%3.` (`start`
assente su ilvl 0, vale 1 per default). Ogni paragrafo che usa uno di questi stili
eredita la numerazione: non esiste nel file un esempio di soppressione già pronto da
copiare. Conseguenze vincolanti:

- **Non scrivere mai il numero dentro il testo del titolo.** Il paragrafo Heading
  contiene solo il valore di `Titolo nodo`. Word antepone da sé `1.`, `1.1.`, `1.1.1.`.
  Scrivere "1.1 Titolo" produce "1.1. 1.1 Titolo".
- La numerazione parte da 1 e **non può produrre `0`**. Sul nodo `0` e sui suoi
  discendenti sopprimi la numerazione **a livello di paragrafo**, non di stile: nel
  `pPr` di quel titolo aggiungi `<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/>
  </w:numPr>`, che sovrascrive localmente il collegamento ereditato dallo stile. È
  l'unica formattazione diretta ammessa oltre al corsivo delle didascalie: qui non c'è
  alternativa, perché lo stesso stile `Heading 1/2/3` deve restare numerato per i
  capitoli 1-7. Con questa soppressione i capitoli 1-7 dell'Excel restano 1-7 anche in
  Word.
- **`document.xml` contiene tre heading segnaposto vivi**: un `Heading1` col solo
  testo «Rq», un `Heading2` col solo testo «Ff», un `Heading3` vuoto. **Rimuovili
  prima di inserire il corpo.** Se restano, ereditano la numerazione dello stile come
  qualunque altro paragrafo — `1.` / `1.1.` / `1.1.1.` — e il primo `Heading 1` vero,
  cioè il Capitolo 1, diventa `2.`. Non è un dettaglio cosmetico: sposta la
  numerazione dell'intera tesi.
- `Heading 1` ha `pageBreakBefore`: ogni capitolo parte da pagina nuova. **Non
  inserire mai interruzioni manuali.** Metti a bilancio ~0,5 pagine di spreco per
  capitolo dopo il primo.
- L'indice è un campo `TOC \o "1-3" \h \z \u` dentro un `w:sdt` e la cache salvata è
  di una versione precedente: dopo l'assemblaggio va rigenerato in Word con F9.
  **Nessun agente lo scrive a mano.**

**Mappatura indice → stile:** livello 1 (`1`…`7`) → `Heading 1`; livello 2 (`1.1`) →
`Heading 2`; livello 3 (`1.1.1`) → `Heading 3`; corpo → `Normal`.

---

## 2. Struttura da creare

```
.
├─ CLAUDE.md                     # memoria di progetto, regole sempre attive
├─ .claude/{agents,skills}/
├─ source/                       # snapshot delle sorgenti + sha
├─ build/
│  ├─ nodes.json                 # materiale immutabile dei 129 nodi
│  ├─ estratti.json              # il foglio Estratti, indicizzato (nodo, id_fonte)
│  ├─ matrici.json               # 4 matrici + 2 tabelle Cap. 5, riconciliate (§4.6)
│  └─ metrics.json               # parole, budget, ratio
├─ nodes/                        # un .md per nodo: SOLO DRAFT + LEDGER
├─ reports/
│  └─ escalation.md              # finding `high` non risolti — gate suo, §7
├─ decisions/DECISIONS.md
└─ out/tesi.docx
```

Inizializza `git` (la cartella non è un repo) e committa dopo ogni stage: serve a
vedere cosa ha cambiato ogni loop e a fare `revert` di un fix che peggiora.
`.gitignore`: `~$*`, `out/`, `source/`.

Riusa quello che esiste già invece di riscriverlo, ai percorsi reali:

- `FONTI/pipeline/glossario/lint.py` — **funziona, ma non come il design di §4.7
  assume**: la gravità di `uso_prima_definizione` è hardcoded a `blocca` (il toggle che
  il resto del prompt suppone non esiste), e i campi
  `usabile_prima_del_nodo_definizione` e `anticipazioni_legittime` di `glossario.json`,
  già popolati, sono ignorati da `_anticipazione_ammessa()`. Servono ~6 righe in quella
  funzione. Finché non ci sono, trattalo come un lint più severo del previsto — non
  come rotto: dettaglio e conseguenze in §4.7.
- `FONTI/pipeline/testi estratti/` — **67 file** di testo estratto dai PDF (non i PDF
  stessi), uno per fonte in `Fonti`.
- `iTOC master backup/` — cartella dei backup, inclusa la copia di sicurezza di questo
  stesso prompt fatta prima di questa riscrittura.

---

## 3. Modello dati

### `build/nodes.json`
Un record per nodo, **e nient'altro lo scrive dopo l'ingest**:

```json
{
  "id": "3.1.1", "level": 3, "chapter": 3, "parent": "3.1",
  "title": "...", "source_desc": "<colonna C, letterale>",
  "fonti": "<colonna D>", "ruolo": "<colonna E>", "trappole": "<colonna G>",
  "note": "<colonna F, privata dei blocchi [OFF-RECORD]>",
  "risoluzioni": [{"fonte": "<chiave>", "risoluzione": "<Estratti!S>"}],
  "fonti_ammesse": [
    {"fonte": "<chiave>", "regime": "usabile|da riformulare|da riformulare (vincolo in S)"}
  ],
  "fonti_vietate": ["<chiave>"],
  "regime": "espansione|resa|compressione",
  "audit_aperto": "<blocchi [AUDIT ...] della col. F, separati da note; mai materiale>",
  "sha": {"desc": "...", "fonti": "...", "ruolo": "...", "trappole": "...", "note": "..."},
  "stato": "vuoto", "source_words": 0,
  "target_words": null, "regime": null
}
```

**`target_words` e `regime` restano `null` in `nodes.json` e non ci vengono mai scritti.**
Li deriva `/tesi-gap` a ogni giro, e vivono solo in `reports/gap.md`. La ragione è che
dipendono dal budget e dal materiale, che cambiano: persisterli creerebbe una seconda
fonte di verità che invecchia in silenzio. Il writer li riceve dal gap report, non
dall'ingest. `expansion_ratio` è **ritirato**: il rapporto si chiama `fit_ratio` e lo
calcola solo `/tesi-gap` (§7).

In testa al file, non per nodo: **`words_per_page: 350`, `words_per_page_band: [310,
380]`**. Tutte le capacità di questo capitolo scalano linearmente su questo
valore; finché non è misurato in Word (procedura al §10), dichiaralo sempre come banda,
mai come numero secco.

`regime` prende **uno di tre valori** — `compressione`, `resa`, `espansione` — assegnato
**per capitolo dal gap report, mai dal writer**, secondo le soglie di `fit_ratio` del §7.
Non esiste un quarto valore: i due casi estremi (`fit_ratio < 0,55` e `> 1,50`) non sono
regimi ma **stati**, e il nodo va a `stato: "⚠ RICHIESTA AUTORE"` con `target_words = 0`.
Il writer riceve `regime` già calcolato e non lo ricalcola.

Lo sha va tenuto **per colonna**, ora cinque: `desc`, `fonti`, `ruolo`, `trappole`,
**`note`**. `/tesi-resync` rilegge l'Excel, confronta gli sha e riporta *cosa* è
cambiato; i nodi toccati tornano a `vuoto`, gli altri non si toccano. La vecchia bozza
resta nella storia di git.

`nodes/<id>.md` contiene **solo** `## DRAFT` e `## LEDGER`. Il materiale immutabile
vive in `nodes.json` e viene passato al writer come contesto renderizzato al volo: così
il writer non può toccare la propria fonte per costruzione, non per regola.

**Il divieto assoluto su `Note` è abrogato.** La regola vecchia — «`Note` è oggi vuota
su tutti i nodi, non ingerirla mai, il divieto è assoluto» — descriveva uno stato che
l'intervista ELFO del 6 settembre ha superato: `Note` è piena su **48 nodi**, e **14**
portano `[DECISIONE AUTORE]`. Sono le decisioni più alte del progetto — battono
qualunque referto, qualunque file di stato e qualunque riga di questo prompt — ed erano
fino a oggi invisibili a ogni agente: un writer costruito sulla regola vecchia
riscriverebbe `6.4` sulla cornice che l'autore ha vietato per iscritto e reintrodurrebbe
una fonte rimossa in `3.2.4`. **Nuova regola: ingerisci `Note`, scarta i soli blocchi
`[OFF-RECORD]`.**

Il filtro `[OFF-RECORD]` è un **passo esplicito e verificabile dell'ingest**, non
un'intenzione dichiarata: `/tesi-ingest` rimuove ogni blocco che comincia con
`[OFF-RECORD]` fino a fine riga, sia da `iTOC!F` sia da `DOSSIER!O` (dove `dossier.py`
lo ha già copiato verbatim), e **dichiara nel report quanti blocchi ha rimosso**. Oggi
la riga `5.1.4` ne contiene due. **Se il conteggio dichiarato è zero, il filtro è
rotto: fermati.**

**`Note` ha tre classi, non due, e la terza è quella che fa danno.** Oltre a
`[DECISIONE AUTORE]` (vincolante) e `[OFF-RECORD]` (escluso), **26 nodi in perimetro**
portano un blocco `[AUDIT 2026-09-07]`. Non è un'istruzione: è una **diagnosi con opzioni
aperte**, scritta da un agente, che spesso enumera due o tre strade alternative senza
sceglierne una. Un writer che la legge come un ordine sceglie al posto dell'autore.

> Regola: un blocco `[AUDIT …]` si ingerisce, si porta in `nodes.json` nel campo
> **`audit_aperto`** separato da `note`, e **non è mai materiale di stesura né
> un'istruzione**. Il writer non lo esegue, non sceglie fra le sue alternative e non lo
> cita: lo ignora come contenuto.
>
> **Quando quel blocco impedisce di scrivere il nodo si decide meccanicamente**, non a
> occhio. Estrai dal blocco gli id dei rilievi (`CL-06`, `ST-04`, …) e cercali nel foglio
> `AUDIT 2026-09-07`: se **almeno uno** ha `Priorità = bloccante` **e**
> `Stato lavorazione = aperto`, il nodo non si scrive — va a `stato:
> "⚠ RICHIESTA AUTORE"` e `/tesi-gap` lo elenca fra le domande del GATE 1. Se sono tutti
> `migliorativo`, o già `chiuso`, il nodo si scrive normalmente e il blocco resta solo in
> `audit_aperto`.

Oggi la regola blocca **cinque nodi in perimetro**: `1.2.3` (`CL-09`), `3.2.2` (`CL-01`),
`4.3.3` (`CL-02`, `ST-04`), `6` (`ST-02`) e `6.4` (`CL-03`). Sono pochi e sono i cinque
che l'audit aveva già marcato come bloccanti: la regola non paralizza la stesura, isola
esattamente i nodi su cui una decisione manca davvero.

Il caso è concreto e cade sul pilota: `3.1.1` porta `[AUDIT 2026-09-07] CL-06`, che
osserva che nessuna delle tre fonti del nodo copre la *hidden action* e lascia aperte tre
strade (restringere, trovare una fonte, dichiarare l'estensione). `CL-06` è
`migliorativo`, quindi il nodo **si scrive** — ma il writer non deve scegliere fra quelle
tre strade, che è esattamente ciò che farebbe leggendo la nota come un'istruzione. È il
secondo nodo che incontrerebbe al primo giro.

`risoluzioni[]` porta le celle `Estratti!S` delle coppie del nodo, con la chiave della
fonte: sono valorizzate su 20 coppie ammesse e vincolanti quanto le `Note` stesse.
`fonti_ammesse[]` e `fonti_vietate[]` vengono dal `DOSSIER`, colonne H e I: l'etichetta
fra parentesi quadre di `fonti_ammesse` (`usabile`, `da riformulare`, `da riformulare
(vincolo in S)`) è il **regime d'uso**, non il permesso — il permesso è l'appartenenza
alla lista stessa (§7).

**`Trappole / rischi` entra nel flusso.** Oggi è ingerita con sha e da lì in poi non la
legge nessuno: è valorizzata su **50 nodi in perimetro**, ed è **input vincolante del
`node-writer`** (§4.1) e **checklist di chiusura del `claim-auditor`** sul nodo (§4.2).

`Ruolo argomentativo` non è un record: ha il formato `Deve dimostrare / Aggancio` solo
su **52** nodi, sugli altri 77 è testo libero, quasi sempre nella forma `1 riga: …`.
Trattalo come stringa. Il campo "Aggancio" esiste su **52** nodi: dove manca, non
inventare una transizione.

### Budget pagine — misurato sul template del 2026-09-07

A4, margini 2,5 cm su quattro lati, corpo 12 pt. **Il font di corpo è Times New Roman,
non Aptos**: il tema dice Aptos ma lo stile `Normal` lo sovrascrive. **L'interlinea non è
1,15: è esatta 23,00 pt** (`w:line="460" w:lineRule="exact"`), scelta dall'autore per
rientrare nelle 26–30 righe imposte da `guide.pdf` §10.3. Ci rientra: **27–29 righe per
pagina**, massimo geometrico 30. `Normal` porta inoltre `before=2 pt` e `after=4 pt`, che
fanno **6 pt di stacco fra due capoversi, il 26% di una riga**.

> **La costante è 350 parole per pagina di prosa continua, con banda dichiarata 310–380.**
> Non è un numero secco e non va usata come tale. Deriva da: 700,10 × 453,50 pt di
> specchio (esatto), 13,84 parole per riga piena in Times New Roman 12 pt (misurato sui
> glifi reali del font di sistema e sul testo reale delle `Descrizione`), 27–29 righe per
> pagina (simulato, dipende dalla lunghezza dei capoversi). **Il valore 445 della versione
> precedente era calcolato sul template vecchio e va cancellato ovunque compaia.**
> La misura diretta è possibile — Word è installato — e la procedura è al §10: dieci
> minuti, una volta sola. Finché non è stata fatta, ogni capacità in questo documento va
> letta con la sua banda.

**La `Descrizione` somma oggi 12.574 parole**, 12.070 al netto del Cap. 7. Il valore
6.392 della versione precedente è di prima dell'intervista ELFO del 6 settembre. I nodi
sono **129**, non 128; le foglie in perimetro **75**, non 74.

#### Il regime si è rovesciato: non è più espansione, è compressione

Questo è il punto che cambia il mestiere della macchina, e va letto prima di tutto il
resto. In perimetro ci sono **12.019 parole di materiale e 8.770 parole di capacità**:
**eccedenza +3.249 parole, cioè +9,3 pagine**. Il problema non è più "poco materiale,
molte pagine, pressione a inventare". È l'opposto: **più materiale di quanto ci stia**, e
la pressione è a buttare via.

La conclusione non dipende dalla costante: regge su tutta la banda 310–380, e reggerebbe
**anche con il vecchio 445** (ratio 0,93×). Il ribaltamento l'ha prodotto l'intervista
ELFO, non l'errore di misura.

**Il Cap. 5 da solo eccede il proprio budget di 3.743 parole, cioè 10,7 pagine**: ne ha
9, gliene servono 19,7. Contiene il **53,5% di tutto il materiale in perimetro** e ha il
**30% del budget**. L'eccedenza del solo Cap. 5 è maggiore dell'eccedenza dell'intera
tesi, perché gli altri capitoli sono in leggero avanzo e la mascherano: **ogni numero
aggregato sulla tesi va sempre affiancato dal dato del Cap. 5**, altrimenti dice il
falso.

#### La struttura costa più di quanto si pensasse

I 100 titoli in perimetro occupano **115 righe fisiche** (15 titoli vanno a capo) e
costano **4,94 pagine su 30**, non 3,5: il conto precedente aveva dimenticato
`before`/`after`/bordo e l'andata a capo dei titoli. A queste vanno aggiunte le code non
riempite lasciate dal `pageBreakBefore` di ogni `Heading1`, 0–1 pagina per capitolo,
attesa **~3,5 pagine**. **Struttura totale: ~8,4 pagine su 30, il 28%.**

Le capacità nella tabella qui sotto **non deducono** le code: assumono che ogni capitolo
riempia la propria ultima pagina fino in fondo. Sono quindi un limite superiore, e ogni
ratio riportato è ottimistico.

#### Stato attuale — quello che c'è, non quello che si vorrebbe

| Cap | Nodi | Foglie | Righe tit. | Strutt. pp | `Budget pp` | Capacità parole | Materiale | Ratio | **Regime** |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 11 | 8 | 14 | 0,58 | 1 | 146 | 389 | 0,37× | **bloccato in compressione** |
| 1 | 14 | 10 | 19 | 0,78 | 4 | 1.125 | 1.139 | 0,99× | pari |
| 2 | 15 | 11 | 16 | 0,69 | 4 | 1.157 | 1.310 | 0,88× | pari |
| 3 | 11 | 8 | 12 | 0,52 | 4 | 1.219 | 1.060 | 1,15× | pari |
| 4 | 15 | 11 | 17 | 0,73 | 5 | 1.495 | 1.185 | 1,26× | espansione lieve |
| **5** | **29** | **23** | **30** | **1,31** | **9** | **2.693** | **6.436** | **0,42×** | **compressione grave** |
| 6 | 5 | 4 | 7 | 0,32 | 3 | 937 | 500 | 1,87× | espansione |
| **Perimetro** | **100** | **75** | **115** | **4,94** | **30** | **8.770** | **12.019** | **0,73×** | **compressione** |
| 7 | 29 | 24 | 29 | 1,25 | 2 | 262 | 504 | 0,52× | fuori perimetro |

**Il Cap. 0 non è stretto, è impossibile**: 11 titoli in 1 pagina consumano 0,58 pagine
di sola struttura e lasciano 146 parole per 6 nodi che ne contengono 389. Va portato a 2
pagine o va ridotto il numero di nodi. Non è un problema che il `node-writer` possa
risolvere scrivendo meglio.

#### Allocazione proposta — 34 pagine in perimetro

| Cap | Oggi | **Proposto** | Capacità parole | Materiale | **k** | Regime operativo |
|---|---|---|---|---|---|---|
| 0 | 1 | **2** | 496 | 389 | 1,27 | espansione |
| 1 | 4 | **4** | 1.125 | 1.139 | 0,99 | resa diretta |
| 2 | 4 | **4** | 1.157 | 1.310 | 0,88 | resa diretta |
| 3 | 4 | **3** | 869 | 1.060 | 0,82 | compressione lieve |
| 4 | 5 | **4** | 1.145 | 1.185 | 0,97 | resa diretta |
| **5** | **9** | **15** | **4.793** | **6.436** | **0,74** | **compressione** |
| 6 | 3 | **2** | 587 | 500 | 1,17 | resa diretta |
| **Totale** | **30** | **34** | **10.170** | **12.019** | **0,85** | |

Nessun capitolo esce dalla banda 0,74–1,27; un solo capitolo in vera compressione; 34
pagine stanno dentro il "~35 accettabile" già ammesso più sotto.

**Questa tabella porta il Cap. 5 dal 30% al 44% della tesi.** È l'aritmetica del fatto
che contiene il 53,5% del materiale, non un errore. La scelta fra *tesi con capitolo di
caso dominante* e *taglio del materiale ELFO* è dell'autore, va fatta prima del GATE 1 e
**non va presa da nessun agente**. Le alternative sono due sole:

- **tetto 30 pagine, allocazione invariata** → richiede di cancellare **3.249 parole** di
  materiale dell'autore, 3.743 dal solo Cap. 5. Non è editing, è scelta di contenuto.
- **34 pagine, tabella qui sopra** → nessuna affermazione va persa, il Cap. 5 pesa il 44%.

**Presenta questa tabella come proposta al GATE 1, mai come esecuzione: nessun agente
modifica la colonna `Budget pp` dell'Excel.** E resta la regola già decisa dall'autore:
**la stesura non si blocca in attesa della risposta al budget** — se un capitolo sfora,
lo dichiari nel gap report e vai avanti.

**Il budget resta indicativo nel totale e vincolante nella proporzione.** Uno scostamento
fino a ~36 pagine non va segnalato come problema. Quello che va segnalato è un capitolo
il cui `k` esce dalla banda 0,55–1,50, perché lì non è più una questione di misura.

#### Nodi senza materiale

**Otto nodi in perimetro hanno `Descrizione` vuota**: `0.1`, `0.1.1`, `0.1.2`, `0.1.3`,
`0.1.4`, `0.2.3` (tutto il Cap. 0 tranne due), `1.2`, `6`. Sotto la regola sovrana non
c'è niente da scrivere: sono `⚠ RICHIESTA AUTORE`, `target_words = 0`, non nodi da
riempire. **Il nodo `5` non è più fra questi**: l'intervista lo ha riempito con 126
parole. La lista precedente (`1.2`, `5`, `6`) è superata.

I quattro `0.1.x` sono inoltre **foglie**: sono le quattro sotto-domande della tesi, il
primo testo che il relatore legge, e gli unici quattro nodi in perimetro il cui `Ruolo`
non ha né `N righe` né `Deve dimostrare` — quindi senza `target_words` derivabile per la
via ordinaria del §4.1. `/tesi-gap` li calcola come `⚠ RICHIESTA AUTORE`, non li
elenca a mano, e `/tesi-assemble` rifiuta l'assemblaggio se uno di loro resta senza
DRAFT.

#### Il Cap. 7 resta fuori perimetro

Sospeso per decisione dell'autore. Non generarlo, non budgettizzarlo, non contarlo in
nessun aggregato, non segnalarlo come mancante a ogni giro. Per riferimento: 29 nodi in
2 pagine, di cui 1,25 di soli titoli — 262 parole per 24 foglie. Anche volendo non
starebbe.

---

## 4. Agenti in `.claude/agents/`

**Tutti gli agenti girano su Sonnet**. Sostituisce «`claim-auditor` e
`chapter-auditor` su Opus, eccezioni non negoziabili»: la capacità persa si compensa con
più agenti e più giri, non con un modello più grande. Ogni auditor gira come **due
istanze indipendenti** sullo stesso capitolo, in contesto pulito, che non si vedono fra
loro: i finding concordi passano, i discordi vanno all'orchestratore, che arbitra. È lo
stesso schema del doppio lettore già usato e già validato sul loop delle fonti. Nessuna
menzione di Opus resta in questo capitolo.

**Chi scrive non giudica, chi giudica non scrive.** Gli auditor sono read-only e
producono solo report. Le modifiche passano da due soli percorsi (§4.5).

### 4.1 `node-writer` — Sonnet — scrive
Espande un nodo da `source_desc` a prosa accademica inglese.
- Input: il record del nodo, il padre, i fratelli precedente/successivo **già scritti**,
  le righe di `Estratti` che lo riguardano, `note`, `risoluzioni[]`, `trappole`,
  `fonti_ammesse[]`, il glossario. Nient'altro. Niente web.
- Riceve inoltre, come contesto di sola lettura, `source_desc` e `title` del **nodo
  successivo** — mai la sua prosa, che non esiste ancora per costruzione (il flusso è
  sequenziale dentro il capitolo). **Divieto esplicito di usarlo come materiale**: serve
  solo a costruire la frase di aggancio richiesta da `Aggancio` (52 nodi su 129).
  Altrimenti quella frase di chiusura è per costruzione materiale senza fonte in alcun
  input del nodo che la scrive.
- **`target_words` ±15%. Nessun pavimento, in nessun caso.** Il pavimento di 120 parole
  era una difesa contro l'espansione a vuoto in un regime che non esiste più: oggi
  cinque capitoli su sette sono in compressione, e un pavimento lì è un divieto di
  tagliare. Un nodo che sta sotto il target si dichiara corto e va all'autore; non si
  allunga mai con materiale non presente nella `Descrizione`.
- **Il mestiere cambia con il regime del capitolo, e va detto al writer nel prompt.**
  Il `node-writer` riceve `regime` insieme a `target_words`:
  - `regime: "resa"` (0,85 ≤ k ≤ 1,20) — rendere in prosa accademica quello che c'è,
    a lunghezza comparabile. È il caso normale: la `Descrizione` **è già prosa**, non
    appunti.
  - `regime: "compressione"` (k < 0,85) — **stessa sostanza, meno parole**. Si tolgono
    ridondanze, subordinate e riformulazioni; **non si toglie mai un'affermazione**. Ogni
    affermazione della `Descrizione` deve restare individuabile nel DRAFT. Se il target
    non è raggiungibile senza far cadere un'affermazione, il nodo si ferma e va
    all'autore: `⚠ COMPRESSIONE NON RAGGIUNGIBILE`.
  - `regime: "espansione"` (k > 1,20) — si esplicita quello che la `Descrizione`
    implica, si costruiscono le transizioni dichiarate negli "Aggancio", si sviluppa il
    ragionamento già presente. **Non si aggiunge contenuto che non sia derivabile dal
    materiale.** Se il target non è raggiungibile, si chiede all'autore. Non si riempie.

#### Come si deriva `target_words` — cinque passi, per capitolo

Il calcolo gira una volta in `/tesi-ingest` e si rifà a ogni `/tesi-resync`.

```
C_c = ( budget_pp(c) − struttura_pp(c) ) × 350        capacità del capitolo, in parole
M_c = Σ source_words(i)  per i in c, con testo        materiale del capitolo
k_c = C_c / M_c                                        regime del capitolo
```

0. **`source_words` = 0** → `target_words = 0`, stato `⚠ RICHIESTA AUTORE`. Il nodo non
   viene mai passato al writer. Otto nodi in perimetro.
1. **base** `b_i = source_words(i)`. La `Descrizione` è già prosa: la resa finale non è
   un'espansione per costruzione, è una riscrittura a lunghezza comparabile.
2. **scalatura** `t_i = b_i × k_c`.
3. **clip** `t_i` in `[0,55 · b_i ; 1,50 · b_i]`. Sotto 0,55 non si comprime, si
   cancella; sopra 1,50 non si espande, si inventa. Entrambi gli estremi sono blocchi,
   non arrotondamenti.
4. **vincoli del `Ruolo`, che battono il budget** (§10 punto 4, invariato):
   - `Ruolo` `1 riga:` **e** `b_i ≤ 70` → `t_i = b_i`, banda 40–70, **escluso dalla
     scalatura**. Sono i nodi in cui l'autore ha voluto una riga e non ha scritto altro:
     12 su 51 in perimetro. Il vincolo vale pieno.
   - `Ruolo` `1 riga:` **e** `b_i > 70` → **`⚠ RUOLO/MATERIALE IN CONFLITTO`**. Vedi sotto.
   - `Ruolo` `Deve dimostrare:` → nessun tetto, vale solo il clip del passo 3.
   - **nodo non foglia con testo** → cappello: `t_i = b_i × k_c`, clip `[0,55 ; 1,20]`.
     Un cappello non si espande: introduce e basta.
5. **residuo**: se dopo i clip `Σ t_i ≠ C_c`, ridistribuire la differenza sui soli nodi
   non vincolati dal `Ruolo`, in proporzione a `b_i`. Se il residuo resta oltre ±5% di
   `C_c`, **il capitolo non chiude**: va nel gap report come blocco di capitolo, non di
   nodo, e la decisione è dell'autore.

#### `1 riga:` — cosa dice il campo e cosa non dice

La regola precedente assegnava 40–70 parole senza pavimento a ogni foglia il cui `Ruolo`
comincia con `1 riga:`, sulla base che quelle foglie avessero in media 50 parole di
`Descrizione`. **Oggi ne hanno in media 149,6, mediana 143, massimo 398, e 39 su 51
superano le 70.** Contengono **7.631 parole, il 63% del materiale in perimetro.**
Applicata alla lettera, quella regola **cancellerebbe 4.886 parole = 14,0 pagine** di
testo scritto dall'autore, di cui 5.198 → 1.210 nel solo Cap. 5, cioè la quasi totalità
dell'intervista.

Due fatti, entrambi verificabili, spiegano perché la coincidenza numerica si è rotta:

1. **Una riga di questo template contiene 13,84 parole.** La banda 40–70 vale già 3–5
   righe: `1 riga:` non era preso alla lettera nemmeno prima.
2. Nel nodo `5.2.1` il `Ruolo` recita `1 riga: ELFO vende capacita' tecnica, adattamento
   e problem solving attraverso progetti definiti in relazione ai bisogni del singolo
   cliente.` e la `Descrizione` dello stesso nodo comincia con la traduzione inglese
   della stessa frase, per poi svilupparla in 175 parole. **La stringa dopo `1 riga:` è
   l'enunciato in una riga del compito del nodo, non la lunghezza dell'output.**

**Questo non indebolisce la precedenza `ruolo` batte `budget`: la rende applicabile.**
Resta piena sui 12 nodi in cui il `Ruolo` chiede una riga e l'autore non ha scritto
altro. Sui 39 in cui l'autore ha poi scritto 150 o 400 parole per lo stesso nodo,
troncare a 55 parole è **riassumere la `Descrizione`**, che §11 vieta esplicitamente.

**La macchina non risolve il conflitto. Il writer non lo applica come regola.** I 39
nodi (4.886 parole in gioco) vanno nel gap report come **una domanda sola al GATE 1**:
*`1 riga:` è una specifica di lunghezza o l'enunciato del ruolo?* Fino alla risposta il
**default è non troncare** — `t_i` si calcola col passo 3 come per ogni altro nodo —
perché cancellare materiale è irreversibile e riempire spazio no.

- Segue `ruolo`: la prima frase si aggancia al precedente, l'ultima prepara il
  successivo, dove il campo "Aggancio" lo specifica (esiste su 52 nodi su 129: dove
  manca, non inventare una transizione, chiudi il paragrafo).
- Compila il `LEDGER` (§6) mentre scrive.
- Prosa continua, niente liste puntate. Le 4 matrici non si appiattiscono (§4.6).
- Applica **la regola della cucitura** (§7) mentre scrive: dove finisce la fonte e
  dove comincia la tesi dev'essere visibile nel testo, non ricostruibile a posteriori.
- Rispetta le **12 regole di stesura di `CONTESTO-per-orchestratore.md` §5**, che
  valgono come parte di questo prompt.

### 4.2 `claim-auditor` — Sonnet, doppia istanza — read-only
L'unico controllo fra la tesi e l'invenzione. Gira come **due istanze indipendenti**
sullo stesso capitolo, in contesto pulito, che non si vedono fra loro (premessa di §4):
i finding concordi passano, i discordi arbitra l'orchestratore.

Lavora **span-first**: per ogni frase del DRAFT deve trovare da sé il supporto in
`source_desc` o in `Estratti`, e consulta il LEDGER solo per spiegare i disaccordi. Non
parte mai dal LEDGER. **Lo script gli passa il `source_desc` intero, non uno span**: gli
offset di carattere sono spariti dal LEDGER, che ora cita solo la prima frase dello span
in chiaro, ritrovabile con un match esatto di stringa.

Bersagli: frasi orfane; citazioni assenti da `Estratti` o usate per dire altro;
over-claim (`demonstrates` dove la fonte dice `suggests`); stime spacciate per dati;
fatti su ELFO non ricavabili dall'Excel; sintesi originali attribuite a un autore;
**e il rovescio, che conta di più sui 53 nodi in perimetro senza alcuna fonte ammessa:
un'affermazione riconoscibilmente di letteratura presentata come propria** — "domain
knowledge is difficult to imitate" senza attribuzione è formalmente ragionamento
dell'autore e sostanzialmente Dierickx & Cool non citato, che in una triennale è un
rilievo di plagio, non di stile: finding `high`, va in escalation e non lo risolve il
writer; **violazioni della regola della cucitura** (§7), che sono la classe più
frequente.

**Checklist di chiusura del nodo: la colonna `Trappole`.** È valorizzata su 50 nodi in
perimetro e fino a oggi non la leggeva nessuno: prima di chiudere il nodo, l'auditor
verifica punto per punto che ogni rischio elencato lì sia stato evitato nel DRAFT.

### 4.3 `chapter-auditor` — Sonnet, doppia istanza — read-only
Fonde ridondanza e flusso: leggono entrambi il capitolo intero e una ripetizione è
quasi sempre un problema di flusso.
- **Ripetizioni dentro il capitolo**: figli dello stesso padre a coppie. Estrae
  *affermazioni*, non frasi. Per ogni finding: le due sedi, l'affermazione duplicata in
  una riga, e a chi appartiene secondo il `ruolo`. Risoluzione: resta dove il `ruolo`
  dice che va dimostrata, l'altro nodo la richiama in mezza riga. Mai cancellare
  entrambe.
- **Non segnalare**: i richiami previsti dagli "Aggancio" e la ripresa di un termine
  del glossario, che è obbligatoria.
- **Flusso**: che le transizioni dichiarate esistano e che la catena argomentativa del
  capitolo regga letta di fila.

**La ridondanza cross-capitolo non è rilevabile girando per capitolo, e ha un passo
suo**. Il `chapter-auditor` gira per capitolo, subito dopo la stesura: quando gira
sul Cap. 3 (il primo scritto, per il pilota) gli altri capitoli non esistono ancora, e
nessun giro successivo torna indietro a ricontrollarlo. Si aggiunge `/tesi-audit
--whole`: solo `chapter-auditor`, in modalità cross-capitolo, dopo l'ultimo capitolo e
prima di `/tesi-assemble` — stesso punto in cui il `prose-auditor` gira come stadio
finale (§4.4).

### 4.4 `prose-auditor` — Sonnet — read-only
Grammatica inglese accademica con attenzione agli errori tipici di un madrelingua
italiano (articoli, preposizioni, `-ing` vs infinito, falsi amici `eventually`
`actually` `argument` `competence`, calchi, `which/that`), periodi oltre le 45 parole,
catene di genitivi. **Più** i pattern da testo generato: coppie antitetiche, frasi-ponte
vuote, chiuse pseudo-profonde, avverbi di rinforzo usati al posto di un argomento,
em dash usati come pausa.
**Filtro accademico obbligatorio**: le librerie anti-slop di §9 vietano avverbi,
passivo e `which` in blocco, cosa sbagliata in una tesi. Usale come libreria di
pattern, non come regole. Non toccare mai l'hedging che protegge da un over-claim.

**Gira due volte, non una: una sul capitolo pilota e una alla fine sul documento
intero.** La versione precedente di questo prompt lo metteva solo alla fine, e sbagliava:
la ragione addotta — «la grammatica non peggiora se la controlli dopo» — vale per la
grammatica e non per la **voce**. Il pilota esiste per calibrare la voce una volta sola;
se i tic da testo generato si scoprono alla fine, vanno corretti su 129 nodi invece che
su undici, tutti scritti nello stesso registro sbagliato. La passata sul pilota risponde
a una domanda diversa da quella finale: non «questa frase è scorretta» ma «questo
capitolo detta la voce degli altri sei, e quella voce va bene?».

**A parte queste due passate è uno stadio separato, non parte di `/tesi-audit`**: `/tesi-audit <capitolo>` esegue solo i 3 lint deterministici più `claim-auditor`
e `chapter-auditor`. Il `prose-auditor` gira una volta sola, dopo l'ultimo capitolo,
insieme a `/tesi-audit --whole`.

### 4.5 I due percorsi di modifica
- **`fix-applier` — Sonnet — scrive.** Solo sostituzioni locali: grammatica, slop,
  terminologia. **Non tocca più il depotenziamento di un claim** (vedi sotto). Un
  report per volta, solo finding con id esplicito, lock **per capitolo** (i report sono
  per capitolo, i file per nodo). Un commit per fix. **Non aggiorna il LEDGER**: il
  LEDGER delle righe toccate lo rigenera lo script di rinumerazione, dopo ogni fix — non il fixer.
- **Riscritture strutturali → di nuovo `node-writer`**, con il finding come vincolo.
  Un finding di flusso o di ridondanza *richiede* di scrivere prosa nuova: fingere che
  sia una sostituzione locale produce rattoppi. **Il depotenziamento di un claim va qui,
  non nel `fix-applier`**: è una decisione su cosa la tesi afferma e può spostare
  una clausola dentro o fuori dal periodo citato (regola della cucitura, §7) — «chi
  scrive non giudica, chi giudica non scrive» lo impone.
- **Ogni riscrittura strutturale del `node-writer` fa scattare una ri-esecuzione
  obbligatoria del solo `claim-auditor` sul nodo toccato, fuori dal conteggio delle 2
  iterazioni** di §10. Oggi è l'unica modifica invasiva del loop che esce non
  verificata.

### 4.6 Gli owner che mancavano — e uno che si toglie
- **`matrix-carrier` si sopprime**. Contraddiceva §1 alla lettera (`def titolo
  C_EN.docx`: «lo consulti solo tu») e importava dati scaduti: `ADD CLASSIFICATION
  CRITERIA` e `Medium/high`, mai applicati; «To be cited» ricorre 13 volte, non 7; la
  colonna `Where it lives` non esiste più nel file. Al suo posto: **l'orchestratore**
  estrae le 4 matrici (5×6 capability, 6×3 glossario, 5×6 ELFO, 3×3 quadranti) **una
  volta sola** in `build/matrici.json`, riconciliate con l'Excel, e vi aggiunge **le due
  tabelle del Cap. 5** da `FONTI/pipeline/tabelle-cap5.md`, oggi senza proprietario. Un
  **inseritore meccanico** legge solo quel JSON e non vede mai il `.docx` di lavoro.
  Restano valide tutte le note tecniche sulle didascalie: il template **non ha uno
  stile `Caption`**, le didascalie sono `Normal` in corsivo, numerate a mano `Table
  1`…`Table 4`, sopra la tabella; le tabelle usano `TableNormal` con bordi espliciti,
  altrimenti escono senza griglia; il TOC è `\o "1-3"` e non raccoglie le tabelle — o si
  aggiunge un elenco a parte, o non si numerano.
- **`bibliography-builder` — Sonnet.** Resta, ma **il formato non è più una decisione
  aperta**: APA 7 autore-data inline, token sdoppiato `[[CIT-N:]]` (narrativa) /
  `[[CIT-P:]]` (parentetica), reference list generata da `FONTI/tesi.bib` (65 voci).
- **`front-back-matter` — Sonnet — nono agente.** Scrive abstract e introduzione, oggi
  promessi (§7/§8) e assenti da §4: nessun agente esistente li produce. L'abstract
  non va nel documento assemblato — si digita nel form d'ateneo, max 4.000 caratteri.
  Dove vive l'introduzione (nodo nuovo in `iTOC`, creato dall'autore, o appendice
  tecnica esente dal divieto di §11) resta domanda al GATE 1; **finché non risponde, la
  pipeline non assembla**, perché i `[[CIT-*]]` risolti punterebbero a una reference
  list che nel documento non c'è ancora.
- **`final-check` — Sonnet — read-only, dopo l'assemblaggio.** ⚠ **Non può contare le
  pagine reali con un tool automatico**: `soffice`/`libreoffice`/`pandoc` sono assenti.
  **Un renderer però c'è**: `/Applications/Microsoft Word.app`. Il conteggio pagine
  resta manuale — si apre il file in Word e si legge il contatore — ma la procedura di
  misura della costante parole/pagina esiste ed è descritta al §10. Verifica che non
  sopravviva nessun `[[`, che i rimandi ai capitoli corrispondano alla numerazione
  effettiva, che gli stili siano solo `Heading 1/2/3` + `Normal` + le tabelle, e che la
  lingua dei run sia inglese.

### 4.7 I controlli che non hanno bisogno di un modello
Sono script, girano prima degli auditor e costano zero:
- **lint numeri e nomi propri**: ogni cifra, percentuale, data, importo e nome proprio
  del DRAFT deve comparire *verbatim* nella whitelist, che è **l'unione di tutti i
  `source_desc` in perimetro più `Fonti` ed `Estratti`**, non più il nodo e i suoi
  antenati. Violazione fuori da questa unione = finding `high` automatico.
  **L'appartenenza al nodo o ai suoi antenati resta, ma solo come avviso, non come
  blocco.** Motivo: il Cap. 6 si scrive per deduzione dai Cap. 1-4, e l'unico antenato
  di `6.1`-`6.4` è il nodo `6`, che ha `Descrizione` vuota — ogni termine legittimamente
  ripreso dai capitoli precedenti sarebbe altrimenti un `high` automatico. Copre da solo
  la classe "dato fabbricato", il primo bersaglio del `claim-auditor`.
- **lint antiplagio**: il match di n-grammi da 8 parole si sposta **qui, fra i lint**,
  per nodo, contro le sole `Citazione verbatim` delle coppie di quel nodo — non più un
  controllo manuale in fondo alla consegna. Motivo: `DOSSIER` colonna Q consegna al
  writer **103 stringhe copiate parola per parola dai PDF**, con l'ordine di
  parafrasarle; se una sopravvive verbatim nel DRAFT il rischio nasce nel nodo, non in
  fondo al documento, ed è lì che va intercettato. Il controllo finale sul documento
  intero resta.
- **lint terminologico**: `pipeline/glossario/lint.py`, 48 termini, 38 definiti, con
  `varianti_vietate` motivate. Si chiama `lint(testo, nodo)` e va rigirato **dopo ogni
  fix**, non come stadio: il `prose-auditor` può rompere il glossario cercando varietà
  lessicale dopo che il controllo è già passato.
  ⚠ **`lint.py` ha la gravità di `uso_prima_definizione` hardcoded a `blocca`**: il
  toggle `avvisa` che il prompt precedente presumeva **non esiste**, non è né un flag né
  una voce di config. E ignora del tutto i campi `usabile_prima_del_nodo_definizione` e
  `anticipazioni_legittime` che `glossario.json` **già contiene**. Servono ~6 righe in
  `_anticipazione_ammessa()` per farli leggere. **Finché non ci sono, l'azione
  prescritta dal rilievo `AG-07` è un no-op e `python3 lint.py --autotest` resta a 3
  blocchi.** Esegui l'autotest prima di ogni uso: deve dare 0, non 3.
- **lint budget**: parole scritte contro `target_words`. Resta `wc`, ma ora confronta
  contro **una capacità derivata dal budget del capitolo**, non contro un pavimento
  fisso: il pavimento è abolito (§4.1).

---

## 5. Skill in `.claude/skills/`

| Comando | Cosa fa |
|---|---|
| `/tesi-ingest` | Legge il `DOSSIER` (non `iTOC` + `Estratti` a mano) → `nodes.json` + `estratti.json` + `nodes/*.md` + `metrics.json`. Applica il filtro `[OFF-RECORD]` su `iTOC!F` e `DOSSIER!O` e **dichiara nel report quante occorrenze ha rimosso**: zero significa filtro rotto, fermati. Idempotente. Lo `stato` iniziale è `vuoto` per ogni nodo, qualunque cosa dica la colonna `Stato`: quella colonna traccia la compilazione della `Descrizione`, non la stesura. |
| `/tesi-gap` | Gap report di §7. Prima di scrivere. |
| `/tesi-draft <id\|capitolo>` | `node-writer` sui nodi in `stato: vuoto`. |
| `/tesi-audit <capitolo>` | 3 lint deterministici + `claim-auditor` + `chapter-auditor`, **ciascuno in due istanze indipendenti**, in contesto pulito: i finding concordi passano, i discordi li arbitri tu. Il `prose-auditor` **non** ne fa parte: è uno stadio finale separato. |
| `/tesi-audit --whole` | Solo `chapter-auditor`, in modalità cross-capitolo sul documento intero: dopo l'ultimo capitolo, prima di `/tesi-assemble`. |
| `/tesi-fix <report-id>` | Applica un report. |
| `/tesi-frontmatter` | `front-back-matter` scrive introduzione e abstract. **Gira dopo l'ultimo capitolo e dopo `/tesi-audit --whole`**, mai prima: sono i due testi che riassumono ciò che la tesi dice, e prima che i capitoli esistano non c'è niente da riassumere. Bloccata finché il GATE 1 non ha detto **dove vivono** i tre pezzi (introduzione, abstract, reference list). |
| `/tesi-status` | Stato per nodo, parole vs budget, finding aperti per severità. |
| `/tesi-assemble` | Genera `out/tesi.docx`. **Rifiuta l'assemblaggio se un nodo in perimetro non ha `DRAFT`.** |
| `/tesi-resync` | Rilegge l'Excel, riporta cosa è cambiato. **Fallisce con un errore esplicito se l'insieme delle chiavi `Indice` è cambiato** e impone un `/tesi-ingest` pulito: il conteggio è già passato da 128 a 129 durante il progetto. |

`/tesi-verify` è tolto dalla tabella e da ogni rimando: misura la concordanza fra due
campionamenti dello stesso modello sullo stesso input, non definisce alcuna azione sul
diff, e duplica in peggio il `claim-auditor`.

**`/tesi-draft` è sequenziale dentro il capitolo** — i nodi fratelli non sono
indipendenti, l'aggancio richiede che il precedente esista già — e parallelo solo fra
capitoli.

---

## 6. Il LEDGER

Ogni paragrafo del DRAFT ha una riga. **Niente più offset di carattere**: `SOURCE[215:398]`
diventa la **prima frase dello span, in chiaro**, che uno `str.find()` ritrova nel
`source_desc`. Motivo: emettere offset di carattere è aritmetica su stringhe, un LLM la
sbaglia quasi sempre, e uno span sbagliato produce falsi «orfano» a catena.

```
## LEDGER
- ¶1 ← SOURCE["ELFO sells technical capability, adaptation and problem solving..."]
       | RUOLO[deve_dimostrare]
- ¶2 ← SOURCE["<prima frase dello span>"] + ESTRATTI[3.1.1|akerlof1970|usabile]
- ¶3 ← ⚠ NESSUNA FONTE — collegamento inferito dall'Aggancio di 3.1.2. Da validare.
- ¶4 ← [[GAP: fatto su ELFO non presente nell'Excel]]
```

**Due cose diverse che si somigliano, e non vanno confuse.** `⚠ RICHIESTA AUTORE` è uno
**stato del nodo**: vive in `nodes.json`, in `/tesi-gap` e in `/tesi-status`, e dice che il
nodo non si scrive finché l'autore non fornisce materiale. `[[GAP: motivo]]` è un **token
nel testo del DRAFT**: segna il punto esatto in cui manca qualcosa dentro un nodo che per
il resto si scrive. Il primo non entra mai in un DRAFT, il secondo non è mai uno stato.

Il token dei buchi nel testo è **`[[GAP: motivo]]`**, non `⚠ RICHIESTA AUTORE` in chiaro:
quella stringa passerebbe nel Word, perché `final-check` controlla che non sopravviva
nessun `[[`, e quella non è un token.

1. **Il LEDGER non è una prova, è un indice.** Lo scrive lo stesso modello che scrive la
   prosa: se allucina il testo può allucinare il puntatore. Nessun agente lo tratti come
   garanzia.
2. Il `claim-auditor` lavora span-first (§4.2) e **non parte mai dal LEDGER**: uno script
   gli passa **il `source_desc` intero del nodo**, non uno span e non gli offset del
   LEDGER, e il modello giudica frase-contro-`source_desc`. Consulta il LEDGER solo per
   spiegare un disaccordo, a posteriori. Se lo script leggesse gli span del LEDGER,
   l'auditor partirebbe da lì e lo span-first sarebbe violato — è la contraddizione che
   la versione precedente lasciava aperta fra questo punto e §4.2.
3. **Dopo ogni fix uno script rinumera i `¶N` e verifica che le righe del LEDGER siano
   tante quanti i paragrafi del DRAFT.** Una sostituzione che accorcia o fonde un
   paragrafo sfasa tutti i puntatori successivi. Disallineamento = finding `high`.
4. Il LEDGER indicizza paragrafi, il `claim-auditor` lavora su frasi: un paragrafo con
   quattro frasi e un solo puntatore soddisfa il LEDGER anche se tre sono orfane. È il
   motivo per cui il `claim-auditor` non deve mai partire dal LEDGER.
5. Il LEDGER non finisce nel Word: viene rimosso in assemblaggio.

---

## 7. Il gate delle fonti — il `DOSSIER` è vincolante

Questo è il pezzo che vale più di ogni auditor, ed è quello che cambia di più in questa
revisione.

**Una fonte è citabile in un nodo se e solo se la sua chiave compare in `DOSSIER` colonna
H `Fonti AMMESSE`.** L'etichetta fra parentesi quadre — `[usabile]`, `[da riformulare]`,
`[da riformulare (vincolo in S)]` — dà il **regime d'uso**, non il permesso: il permesso
lo dà solo la presenza in colonna H. La colonna I `Fonti VIETATE` è un divieto assoluto.
**Cancella ogni riferimento alla colonna `Esito` di `Estratti` come criterio di
citabilità**: non lo è più.

Le due liste divergono su **8 coppie**, e la regola vecchia — quella che guardava
`Estratti!H` — farebbe citare fonti che l'autore ha già rimosso per iscritto:
`4.1.3 × nidumoluknotts1998` (`Esito = da riformulare` in `Estratti`, ma rimossa dal nodo
per arbitrato dell'autore) e `3.2.4 × dierickxcool1989`, la cui reintroduzione è vietata
per iscritto nelle `Note` del nodo. Un writer che applicasse la regola vecchia alla
lettera citerebbe entrambe.

Numeri: **108 coppie in `Estratti`**, **100 ammesse e 8 vietate** nel `DOSSIER`, di cui
**33 `usabile`** e **67 `da riformulare`**.

**«Lookup, non giudizio» non è vero, e va detto.** Le celle `Cosa dice davvero` hanno
**mediana 135 parole** (min 83, max 199) e sono scritte da un agente lettore, non copiate
dal PDF: stabilire se una clausola «compare» in 135 parole di riassunto discorsivo è
esattamente il giudizio di implicazione che questa sezione dichiarava di escludere.
Vendere il criterio come meccanico fa saltare l'unica cautela che conta: quando il lookup
non riesce, il modello deve fermarsi, non stimare.

Il criterio si riformula come **regola di fallimento**:

> Se non riesci a puntare la frase esatta di `Cosa dice davvero` che regge la clausola, la
> clausola esce dal periodo citato. Non c'è terza via.

La sola parte davvero meccanica — il match di **numeri e nomi propri** fra la clausola e
`Cosa dice davvero` / `Citazione verbatim` — diventa uno script (§4.7).

**La regola della cucitura resta intatta**, perché è la parte migliore di questa sezione:

> Il periodo che porta la citazione contiene **solo** quello che la fonte sostiene.
> L'applicazione, l'estensione o la conseguenza che ne trae la tesi va in un periodo
> **separato**, senza citazione, oppure introdotta da una formula esplicita di
> derivazione: *building on*, *applied to*, *transposed here*, *this thesis
> operationalizes*.

Claim composto citato congiuntamente → si scompone: quello che una fonte sostiene resta
attribuito a lei, il resto no. Vale il verdetto più basso, mai il più alto. Le citazioni
testuali vengono **solo** dalla colonna `Citazione verbatim`, parola per parola, mai
riscritte a memoria.

**Sui 67 `da riformulare` il writer riceve due autorità che divergono per definizione — la
`Descrizione` sovrana e `Cosa dice davvero` — e finora nessuna regola diceva quale vince.**
Il conforto «la correzione è già scritta in colonna» è vero a metà: le `Note` di
`Estratti` sono 106, mediana 130 parole, e **solo 51 su 106 contengono un verbo
prescrittivo**; le altre sono diagnosi, non istruzioni. La regola:

> Su una coppia `da riformulare` vince `Cosa dice davvero`: il claim si **restringe, mai
> si allarga**. Se la restrizione fa cadere l'affermazione della `Descrizione`, il nodo va
> in `[[GAP: …]]` e si porta all'autore — non si riscrive.

**La `Descrizione` di 7 nodi contiene già citazioni autore-anno nel testo** (`1.1.1`,
`1.3`, `4.2.4`, `6.1`, `6.2`, `6.3`, `6.4`). Resta vincolante nel **contenuto, non nelle
attribuzioni**: se una citazione che vi compare non ha la chiave ammessa nel `DOSSIER`, va
tolta dal DRAFT e l'affermazione resta come ragionamento dell'autore. Riguarda in pieno i
quattro nodi del Cap. 6, che sono esattamente quelli il cui registro deve cambiare (vedi
gap report). Il LEDGER lo annota come `⚠ CITAZIONE RIMOSSA: <chiave> — vietata dal
DOSSIER`.

**GATE 3-bis.** La classe «letteratura presentata come propria» è `high`, va in
escalation e **non la risolve il writer** — ma nessun passo svuota
`reports/escalation.md`, e GATE 4 pretende zero finding `high`: senza un'uscita esplicita
il gate si blocca da solo. In perimetro **53 nodi non hanno alcuna fonte ammessa**: è lì
che la classe si concentra. Si aggiunge **GATE 3-bis**, fra l'ultimo `/tesi-audit` e
`/tesi-assemble`: `escalation.md` si legge con l'autore, e ogni voce si chiude con una di
tre etichette — `fonte trovata`, `claim ritirato`, `dichiarato come estensione teorica`.

`DOSSIER` colonna Q consegna **103 stringhe copiate parola per parola dai PDF** insieme
all'ordine di parafrasarle: sono materiale di verifica, non testo da citare. Il controllo
n-grammi si sposta **fra i lint, per nodo** (§4.7), contro le sole `Citazione verbatim`
del nodo: non resta un controllo manuale sul documento intero in fondo alla consegna.

Dei **129 nodi**, **47 hanno almeno una fonte ammessa nel `DOSSIER` e 82 no**: il gate
riguarda i 47, sugli altri vale la regola sovrana e basta. Tutti e 47 stanno in perimetro,
perché il Cap. 7 non ha alcuna coppia: quindi **53 dei 100 nodi in perimetro non hanno
alcuna fonte ammessa** — è la base su cui GATE 3-bis misura la classe sopra, ed è il
motivo per cui quella classe è la più numerosa attesa. Il vecchio conteggio «35 citano,
93 no» è di prima del loop fonti del 7 settembre: non usarlo.

Non è un controllo a posteriori, è una forma di scrittura: il `node-writer` la applica
mentre scrive, il `claim-auditor` la verifica. Corollario: dove non c'è nessuna fonte
ammessa non c'è niente da cucire, vale la regola sovrana e basta.

### Gap report — prima di scrivere una riga

Il gap report misura **quanto il materiale disponibile diverge dallo spazio disponibile,
in entrambe le direzioni**. La versione precedente misurava solo l'espansione, con soglie
`≤1,2× comprimere / ≤2× ok / ≤3× attenzione / >3× bloccato`: sono tarate su un regime che
non esiste più. Oggi tutti i 29 nodi del Cap. 5 finirebbero indistintamente nella casella
"comprimere" senza che nessuno dica di quanto, e i due blocchi veri — il Cap. 5 in
eccesso di 10,7 pagine e il Cap. 0 che non ci sta comunque — non verrebbero segnalati.

**`expansion_ratio` è ritirato. Al suo posto `fit_ratio = target_words / source_words`**,
che vale sotto 1 in compressione e sopra 1 in espansione, e la classificazione è
simmetrica:

| `fit_ratio` | Classe | Cosa fa il sistema |
|---|---|---|
| **< 0,55** | **BLOCCATO IN COMPRESSIONE** | Non si scrive. Il materiale non ci sta: la decisione su cosa esce è dell'autore, mai della macchina. |
| 0,55 – 0,85 | compressione | Si scrive con `regime: "compressione"`. Il `claim-auditor` verifica che nessuna affermazione della `Descrizione` sia caduta: in compressione il bersaglio non è ciò che è stato aggiunto, è ciò che è sparito. |
| 0,85 – 1,20 | resa diretta | Si scrive con `regime: "resa"`. È il caso normale. |
| 1,20 – 1,50 | espansione | Si scrive con `regime: "espansione"`. Il `claim-auditor` gira con attenzione doppia: è qui che sta la pressione a inventare. |
| **> 1,50** | **BLOCCATO IN ESPANSIONE** | Non si scrive. Manca materiale: domanda secca all'autore su **cosa** manca. Non proporre di riempire. |

Il gap report esce **a due livelli**, e questo è nuovo: un `fit_ratio` per nodo dice poco
se il capitolo nel suo complesso non chiude.

- **Per capitolo**: `C_c`, `M_c`, `k_c`, `Σ target` dopo i clip, e lo scarto residuo. Un
  capitolo il cui residuo supera ±5% di `C_c` è **un blocco di capitolo**, e va segnalato
  prima e più forte di qualunque blocco di nodo, perché nessuna riscrittura di nodo lo
  risolve.
- **Per nodo foglia**: `fit_ratio`, classe, e per i bloccati la domanda all'autore.

**Due controlli deterministici che prima non esistevano**, entrambi costano zero:

1. **capienza strutturale**: se `struttura_pp(c) > 0,45 × budget_pp(c)`, il capitolo ha
   più titoli di quanti ne regga il suo budget. Oggi scatta sul **Cap. 0** (0,58 su 1
   pagina, il 58%) e sul Cap. 7. Non è un problema di scrittura ed è inutile passarlo al
   writer.
2. **conflitto `Ruolo`/materiale**: foglie con `Ruolo` `1 riga:` e `source_words > 70`.
   Oggi **39 nodi in perimetro** (Cap. 5: 22 — Cap. 4: 5 — Cap. 2: 4 — Cap. 6: 3 —
   Cap. 3: 3 — Cap. 1: 2). Escono come **una domanda sola** al GATE 1, non come 39
   segnalazioni.

**Blocchi aperti sul budget, oggi:**

- **Capitolo 5 — eccesso di materiale, 10,7 pagine.** 6.436 parole disponibili contro
  2.693 di capacità: `k = 0,42`, sotto il pavimento di clip 0,55. **Non è più un blocco
  per mancanza di materiale**: l'intervista del 6 settembre lo ha sbloccato e poi
  ribaltato. Scegliere quali affermazioni dell'autore sopravvivono è merito, non
  superficie: non è un giudizio che spetti a un `node-writer`. Il percorso è **proposta,
  poi approvazione**: **tu proponi** l'elenco dei tagli con la cifra per nodo — portare il
  capitolo a 15 pagine (`k = 0,74`, dentro banda) oppure tagliarne il materiale di 3.743
  parole — **l'autore approva**, e solo dopo parte `/tesi-draft 5`. Fino alla decisione il
  Cap. 5 non si scrive, ma **la ragione va detta giusta nel report**: non manca niente, ce
  n'è troppo. Il testo che descriveva questo capitolo come "3.170 parole richieste, 860
  disponibili" è superato e va rimosso, altrimenti la pipeline cerca materiale che c'è già.
- **Capitolo 0 — capienza strutturale.** 11 titoli in 1 pagina: 146 parole residue per
  389 di materiale. Serve una seconda pagina o meno nodi. Cinque delle sue otto foglie
  hanno comunque `Descrizione` vuota e sono `[[GAP: …]]`.
- **Capitolo 6 — espansione, `k = 1,87`.** Sopra il clip 1,50. È l'unico capitolo in cui
  la vecchia pressione a inventare esiste ancora, e va trattato con la regola di
  espansione: 500 parole non ne fanno 937 senza aggiungere qualcosa. Portarlo a 2 pagine
  (`k = 1,17`) lo riporta in banda senza toccare il materiale.

**Blocchi non di budget, oggi** — il Cap. 2 esce da questa lista: il loop del 7 settembre
gli ha assegnato **22 nuove coppie** in `Estratti`, e con la ratio vera (`0,88×`) non è
più un capitolo scoperto. Restano aperti:

- **Capitolo 6, nodi `6.1`-`6.4`.** Il capitolo va scritto come **deduzione dell'apparato
  dei capitoli 1-4, non come sostegno bibliografico**: registro "dal modello segue", non
  "la letteratura mostra". Il nodo `6.4` contraddice la sua fonte (Liu & Ma 2024 dicono che
  il problema dei lemons *viene evitato*; il nodo lo presenta come fallimento di mercato) e
  richiede una decisione dell'autore prima di essere scritto.
- **Nodo `1.2.1`**: la distinzione execution/judgment è dell'autore, derivata da
  prediction/judgment di Agrawal et al. Va presentata esplicitamente come derivazione
  propria, mai come tassonomia della fonte.
- **Nodo `4.2.1`**: dipende da Ghemawat 1991, PDF non ancora recuperato.

### Cosa manca e non è nella scaletta

- **Una sezione di metodo.** Non è più un buco aperto: `5.1.4` è di fatto la sezione di
  metodo sul caso ELFO ed è sollevabile così com'è. La sezione di metodo generale (da dove
  vengono le informazioni, come sono state trattate) la cura l'autore per conto suo, fuori
  pipeline.
- **Abstract, introduzione e reference list.** §8 impone una reference list, §11 vieta di
  aggiungere sezioni non presenti nell'Excel, e in `iTOC` **non esiste alcun nodo
  bibliografia**. La domanda va al **GATE 1**: nodi nuovi in `iTOC` che crea l'autore,
  oppure appendice tecnica esente dal divieto di §11. **Fino alla risposta la pipeline non
  assembla**, perché i `[[CIT-*]]` risolti punterebbero a una lista che non c'è. L'agente
  che li scrive è `front-back-matter` (§4.6).
- **Tempi verbali e persona.** Non sono più una decisione aperta: **GATE 2 è chiuso**, la
  decisione dell'autore è per esteso nel rilievo `AG-04` del foglio `AUDIT 2026-09-07`
  dell'Excel. In tre righe: presente per la teoria, passato per studi e fatti ELFO, mai la
  prima persona, metadiscorso ridotto al minimo, l'azienda è sempre ELFO e mai «the
  company». Per il testo integrale, la cella `AG-04`.
- **Controllo di similarità.** Resta, ma cambia posto: n-grammi da 8 parole per nodo,
  contro le sole `Citazione verbatim` del nodo, fra i lint di §4.7 — non più un controllo
  manuale sul documento intero in fondo alla consegna.
- **Le due tabelle del Cap. 5** in `FONTI/pipeline/tabelle-cap5.md` oggi non hanno un
  proprietario: entrano in `build/matrici.json` insieme alle 4 matrici.

---

## 8. Come si citano le fonti

- **Il formato non è più una decisione aperta**: deciso il 2026-09-06, **APA 7 autore-data
  inline**, reference list finale alfabetica generata da `FONTI/tesi.bib` (**65 voci**),
  niente note a piè di pagina per le citazioni. Le linee guida d'ateneo sono in
  **`info & contesto/`**, non in `info uni/` che non esiste: il vincolo è verificabile
  subito, non è una domanda all'autore.
- **Il token si sdoppia**: `[[CIT-N:chiave]]` per la forma narrativa (`Akerlof (1970)
  shows that …`, quando il soggetto della frase è l'autore) e `[[CIT-P:chiave]]` per la
  parentetica (`… (Akerlof, 1970).`, quando l'affermazione è del testo e la fonte la
  sostiene). Con il token singolo la risoluzione automatica non sa quale forma produrre.
- **Niente citazioni testuali, solo parafrasi attribuita**: le linee guida impongono il
  numero di pagina per le citazioni dirette e nessuno dei verbatim di `Estratti` ce l'ha.
  Attenzione: sono testo copiato parola per parola dai PDF; se finissero in tesi senza
  virgolette li troverebbe l'antiplagio — il controllo n-grammi è ora fra i lint, **per
  nodo** (§4.7), non un passo manuale in fondo alla consegna.
- **Divieto assoluto di fonti nuove, in ogni agente**: solo quelle già in `Fonti` e
  ammesse dal `DOSSIER`. Le mancanze si dichiarano con `[[CIT-NEEDED: motivo]]`.
- Le chiavi si normalizzano all'ingest: forme equivalenti dello stesso autore e anno sono
  lo stesso lavoro.
- Una fonte con `Peer-reviewed = no` (**15 su 67** in `Fonti`) non regge una frase del
  tipo "research shows": attribuzione esplicita, non risultato acquisito.
- **La citabilità la decide il `DOSSIER`, non `Estratti`** (§7): una fonte è citabile in
  un nodo se e solo se la sua chiave compare in `DOSSIER` colonna H `Fonti AMMESSE`.
- Fonti a più autori: **`(Primo et al., Anno)` dalla terza in poi**, forma decisa una
  volta e tenuta uguale ovunque.

---

## 9. I prerequisiti

Il plugin **`academic-writing-agents` esce dal flusso**. Importarlo e poi neutralizzarlo
(«dove si sovrappone ai miei auditor, vincono i miei») non gli dava mai l'ultima parola, e
i suoi revisori non conoscono il LEDGER, `Estratti` né le colonne dell'Excel: possono
produrre solo rilievi di stile che il `prose-auditor` già copre. Resta come **lettura
facoltativa** dell'orchestratore, non come stadio della pipeline.

Le **tre skill anti-slop** (`unslop`, `no-ai-slop`, `stop-slop`) restano solo come
**libreria di pattern estratta** in `.claude/skills/tesi-slop/references/`, con marcate
le regole disattivate e il perché. Estratte le liste, le skill non servono più al
runtime: usale per costruire quel file, non installarle come stadio.

La skill **`docx` di Anthropic** genera il Word: verifica che preservi stili e `sectPr`
prima di fidartene per l'assemblaggio.

**Prerequisiti veri della macchina**, non elencati nella versione precedente:
- **`/usr/bin/python3`** con `openpyxl` **3.1.5** e `python-docx`: il `python3` di
  default è miniconda e non li ha. Ogni script che tocca l'Excel o il `.docx` va lanciato
  con il binario esplicito.
- **Nessun repo git** nella cartella: va inizializzato prima del primo commit isolato
  di §10.
- **Nessun renderer da riga di comando** (`soffice`, `libreoffice`, `pandoc` assenti), ma
  **Microsoft Word è installato**: la misura diretta delle parole per pagina (§10) è
  possibile a mano, anche se non è automatizzabile su questa macchina.

Comandi di installazione dei quattro prerequisiti precedenti, tenuti come record se un
giorno servisse rifarli. **`claude plugin install --url <repo>` non esiste** (il README
del plugin lo documenta ma la CLI risponde `unknown option '--url'`): il flusso reale è
marketplace + install.

```bash
claude plugin marketplace add andrehuang/academic-writing-agents && claude plugin install academic-writing-agents@andrehuang-academic-writing-agents
```
```bash
npx --yes skills add theclaymethod/unslop -g -a claude-code
```
```bash
npx --yes skills add petergyang/no-ai-slop --skill no-ai-slop --global --yes
```
```bash
git clone https://github.com/hardikpandya/stop-slop.git ~/dev/stop-slop && ln -s ~/dev/stop-slop ~/.claude/skills/stop-slop
```

---

## 10. Ordine di esecuzione e gate

```
FASE 0 — EDITING DELLA SCALETTA (nessun agente: autore + Excel a mano)
  a. backup in `iTOC master backup/`

  Bloccanti di contenuto ancora aperti (`PROSSIMI PASSI`, passi 1-8; l'intervista ELFO è
  fatta, i 13 arbitrati sono chiusi, non resta alcun `DA DECIDERE` residuo):
  b. nodo `3.2.2` — togliere il quarto indicatore "to explain the trade-offs specific to
     the sector": decisione già presa il 2026-09-06, oggi viva solo in `Estratti!S`
     (passo 1)
  c. nodo `4.3.3` — fissare per iscritto, in `Descrizione` o `Note`, che il meccanismo
     bidirezionale productization × profondità di dominio è un'estensione teorica per
     analogia, non un risultato delle fonti citate; formula unica, riusabile identica in
     Cap. 4, 5, 7 (passo 2)
  d. nodo `1.2.3` — sciogliere l'affollamento di sei fonti: una clausola per fonte, e
     dichiarare come deduzione il passaggio da guadagno di produttività a riduzione della
     differenziazione (passo 3)
  e. nodo `6` — scrivere il paragrafo di apertura in `Descrizione`, dal `Ruolo
     argomentativo` del nodo e dalla chiusura di `5.6` (azione già assegnata, `ST-02`;
     passo 4)
  f. nodi `5.2`-`5.5` — verificare se la capacità di integrazione custom di ELFO varia
     nei quattro casi e dichiararlo nelle `Note` del Cap. 5 (passo 8)
  g. `Stato` riportata a vuoto sulle **30 righe** oggi a `bozza` (29 nel Cap. 5, 1 nel
     Cap. 0)
  h. **ultimo atto, prima dello snapshot**: esegui
     `/usr/bin/python3 "FONTI/pipeline/dossier.py"`. Fa `wb.save()` sullo stesso Excel:
     rigenerarlo dopo GATE 0 cambierebbe lo sha del file che congeli subito dopo. **Dopo
     GATE 0 è vietato rieseguirlo.**
  === GATE 0: da qui l'Excel è congelato e in sola lettura. ===

[verifica §9]                 ← i prerequisiti della macchina ci sono: controlla e vai.
/tesi-ingest                  ← dichiara nel report quanti blocchi [OFF-RECORD] ha
                                 rimosso da `iTOC!F` e `DOSSIER!O` (zero = filtro rotto,
                                 fermati)
/tesi-gap                     ← GATE 1: gap report + domande (elenco sotto). Ti fermi.
[glossario]                   ← GATE 2: tempi verbali e persona sono già chiusi, la
                                 decisione integrale è nel rilievo `AG-04` di
                                 `AUDIT 2026-09-07`; qui mi fai approvare solo il
                                 glossario.
/tesi-draft 3                 ← PILOTA sul Cap. 3: ratio 1,15× (il piu' vicino alla
                                 parita') e tutte e 8 le foglie coperte da fonti
                                 ammesse. E' l'unico capitolo interamente coperto.
/tesi-audit 3 → /tesi-fix     ← 3 lint + claim-auditor + chapter-auditor, ciascuno in
                                 doppia istanza indipendente.
prose-auditor 3               ← passata di calibrazione della voce, solo sul pilota:
                                 quello che passa qui diventa il registro di 129 nodi.
                              ← GATE 3: leggo il Cap. 3 e dico se lo stile va.
/tesi-draft 1 → 2 → 4         ← dal più solido al più fragile.
/tesi-audit su ciascuno
[proposta di taglio del Cap. 5, approvata dall'autore] ← prima di /tesi-draft 5
/tesi-draft 5 → 6
/tesi-audit su ciascuno
/tesi-audit --whole            ← dopo l'ultimo capitolo: solo chapter-auditor in
                                 modalità cross-capitolo, per la ridondanza che per
                                 capitolo non si vede.
/tesi-frontmatter              ← introduzione e abstract, ora che i capitoli esistono.
                                 Bloccata se il GATE 1 non ha detto dove vivono.
prose-auditor                  ← stadio finale, sul documento intero. NB: gira gia' una
                                 prima volta sul solo capitolo pilota, subito dopo
                                 /tesi-draft 3, per calibrare la voce prima che diventi
                                 quella di tutti e sei i capitoli.
[escalation.md con l'autore]   ← GATE 3-bis, fra l'ultimo /tesi-audit e
                                 /tesi-assemble: ogni voce si chiude con `fonte trovata`,
                                 `claim ritirato` o `dichiarato come estensione teorica`. Senza questo gate, GATE 4 è in stallo per
                                 costruzione.
/tesi-assemble → final-check   ← GATE 4: nessun finding high, nessun token irrisolto.

FASE DI CONSEGNA (manuale, non automatizzabile su questa macchina)
  1. aprire out/tesi.docx in Word e rigenerare il TOC con F9. ⚠ La cache salvata nel
     `w:sdt` contiene voci della versione precedente con i budget `{N pp}` dentro i
     titoli: se non viene rigenerata finisce nel PDF consegnato, e `final-check` non può
     accorgersene perché è testo valido. In assemblaggio **svuota la cache del `w:sdt`**,
     così Word mostra "aggiorna campo" invece di dati vecchi.
  2. contare le pagine reali.
  3. esportare in PDF unico, nome `LF3236167.pdf`, max 10 MB.
  4. rimuovere il nome dell'autore dai metadati (`dc:creator`): le linee guida vietano
     riferimenti personali nel file.
  5. l'abstract NON va nel documento: si digita nel form web dell'ateneo, max 4.000
     caratteri. Ne esiste già uno scritto in `def titolo C_EN.docx`.
  6. controllo similarità: n-grammi di 8 parole del testo finale contro i file di
     `pipeline/testi estratti/`. Il grosso del rischio è già intercettato per nodo
     durante l'audit (§4.7); questo è il passaggio finale sul documento intero.
                              ← GATE 5: consegna.
```

**Nota sul formato.** `info & contesto/guide.pdf` §10.3 prescrive A4, margini 2,5 cm,
corpo 12 e **"battitura pagine: da 26 a 30 righe"**. **Il template li rispetta tutti**:
l'interlinea esatta 23 pt produce **27-29 righe per pagina**, massimo geometrico 30 —
dentro la finestra 26-30. La segnalazione precedente ("il template ne produce ~41 righe")
descrive il template vecchio ed è **superata**: va tolta, non ripetuta a ogni giro.
Resta un solo scostamento, ammesso: il carattere consigliato è Arial/Tahoma/Verdana, il
corpo è Times New Roman (i titoli sono Arial) — è un consiglio, non un obbligo.
**Segnalalo una volta nel report finale, non a ogni giro.** Frontespizio e dichiarazione
di originalità non vanno aggiunti: le linee guida li escludono e le 4 pagine iniziali del
template sono già corrette.

**Misura diretta delle parole per pagina — da fare una volta, in FASE 0 o subito dopo.**
Finché non è fatta, **usa 350 e dichiara sempre la banda 310-380**, mai un numero secco:
tutte le capacità di §3 scalano linearmente su quel valore. Procedura, dieci minuti:
incolla in stile `Normal`, dopo l'ultima pagina del template, un blocco di prosa inglese
di almeno 2.000 parole in capoversi di 5-7 righe (vanno bene le `Descrizione` dei Cap.
1-4 concatenate); annota la pagina piena iniziale e finale del blocco; conta le parole
del blocco con `Revisione → Conteggio parole`; **parole/pagina = parole del blocco ÷
pagine piene occupate**; verifica a mano che una pagina piena stia fra 26 e 30 righe;
scrivi il valore in `nodes.json` come `words_per_page` e rifai girare `/tesi-gap`. Non
ripetere la misura dopo, a meno che il template cambi.

**GATE 1 — domande all'autore**, in forma di elenco a cui rispondere in blocco:

1. il **budget**: allocazione proposta a **34 pagine** in perimetro
   (`0→2 1→4 2→4 3→3 4→4 5→15 6→2`) contro il tetto a 30 che costa la cancellazione di
   **3.249 parole** di materiale;
2. **`1 riga:`**: significa lunghezza o significa ruolo? **39 nodi** in conflitto,
   **4.886 parole** in gioco, **default: non troncare**;
3. dove vivono **abstract, introduzione e reference list** — nodi nuovi in `iTOC`
   (li crea l'autore) o appendice tecnica esente dal divieto di §11; l'abstract in ogni
   caso non entra nel documento, va nel form d'ateneo. Senza risposta la pipeline
   **non assembla**: i `[[CIT-*]]` risolti punterebbero a una lista che non c'è;
4. il **taglio del Cap. 5** (proposta: circa il 26% del capitolo), con l'elenco dei
   tagli proposti per nodo.

**Protocollo di convergenza** (ogni `/tesi-audit`):

1. Prima i 3 lint deterministici (§4.7). Poi `claim-auditor` e `chapter-auditor`,
   ciascuno in **doppia istanza indipendente**, in contesto pulito, che non si vedono fra
   loro: i finding concordi passano, i discordi li arbitra l'orchestratore. Il
   `prose-auditor` **non gira qui**: gira sul capitolo pilota e poi una volta sola alla
   fine, sul documento intero.
2. Fix nell'ordine: `claim` → `ridondanza` → **`budget`** → `flusso`. Il budget sta
   **prima** del lavoro di superficie: se metà nodo va tagliata, non ha senso averla
   levigata. (Tolto `prosa`: il `prose-auditor` non gira per capitolo.)
3. Il lint terminologico rigira dopo ogni fix, non come stadio.
4. **Precedenze in conflitto, non negoziabili**: `ruolo` batte `budget`; `claim` batte
   `prose`; `claim` batte `budget`; `budget` batte `ridondanza`; `flusso` batte
   `ridondanza` sulle transizioni dichiarate negli "Aggancio"; il glossario batte `prose`
   sempre. Si aggiungono: **`claim` batte `flusso`** — una transizione senza
   materiale non si scrive, si dichiara mancante, ed è il conflitto garantito dai **52
   nodi con `Aggancio`** — e **`ruolo` batte `flusso`** sui nodi che il `Ruolo` vuole di
   una riga.
5. Massimo **2 iterazioni** sui cicli di fix. Un finding che sopravvive va in
   `reports/escalation.md`, chiuso a GATE 3-bis. **Ogni riscrittura strutturale del
   `node-writer` fa scattare una ri-esecuzione obbligatoria del solo `claim-auditor` sul
   nodo toccato, fuori dal conteggio**: oggi è l'unica modifica del loop che esce
   non verificata.
6. Niente `git revert` automatico: i conflitti si risolvono con la tabella al punto 4.
   Ma **ogni modifica, anche una riscrittura strutturale del `node-writer`, è un commit
   isolato che cita il finding-id**, perché il revert manuale resti possibile.
7. Il `prose-auditor` gira **una volta sola**, alla fine, sul documento intero — stesso
   punto in cui gira `/tesi-audit --whole`. È la passata più numerosa e produce il
   rilievo meno rischioso, e la grammatica non peggiora se la controlli dopo.
8. **Il modello non si sceglie più per nodo.** Tutti gli agenti girano su **Sonnet**,
   orchestratore escluso. La vecchia selezione per `expansion_ratio > 2×` non
   seleziona più niente: in perimetro nessun capitolo arriva a 1,9×, e la difficoltà si è
   spostata sul taglio — il Cap. 5, `k = 0,74` — non sull'espansione. La capacità persa
   si compensa con **più agenti e più giri**: doppia istanza indipendente per ogni
   auditor, arbitrato dell'orchestratore sui discordi, lo stesso schema già validato sul
   doppio lettore delle fonti.

---

## 11. Cosa NON deve fare il sistema

- Non riassumere né riscrivere la `Descrizione`: è la base di stesura. In regime di
  **resa** si mette in prosa a lunghezza pari o inferiore **senza perdere affermazioni**:
  tagliare un'affermazione è una decisione dell'autore, non del writer.
- Non aggiungere sezioni o capitoli non presenti nell'Excel.
- Non scrivere il Capitolo 7: è sospeso per decisione dell'autore.
- Non citare una fonte che non compare in `DOSSIER` colonna H `Fonti AMMESSE` — mai
  `Estratti` colonna `Esito` (§7).
- Non ingerire né passare ad alcun agente i blocchi `[OFF-RECORD]`: oggi ce n'è uno solo,
  nel nodo `5.1.4`, e `dossier.py` lo copia verbatim in `DOSSIER` colonna O.
- Non appiattire in prosa le 4 matrici.
- Non inventare fonti, numeri, date, fatti su ELFO.
- Non attribuire a un autore una sintesi originale della tesi.
- Non attribuire a una fonte la posizione di un'opera che quella fonte cita in una
  rassegna.
- Non toccare la formattazione del `.docx` oltre `Heading 1/2/3` e `Normal`.
- Non scrivere il numero di capitolo dentro il testo del titolo.
- Non modificare la colonna `Budget pp`, e non riaprire la discussione sulle pagine: la
  stesura non si blocca in attesa.
- Non rimuovere l'hedging che protegge da un over-claim, e non allargare un claim su una
  coppia `da riformulare`.
- Non lasciare `⚠ RICHIESTA AUTORE` in chiaro nel testo di un nodo: il token è
  `[[GAP: motivo]]`, altrimenti passa nel Word.
- Non passare un gate senza la mia risposta esplicita.

---

## 12. Cosa consegni ora

Costruisci la struttura, poi fermati e riporta:

1. l'albero dei file creati;
2. `CLAUDE.md` e l'elenco degli agenti con una riga di brief e il modello assegnato;
3. l'output di `/tesi-ingest` e `/tesi-status`;
4. il gap report, con l'elenco esplicito delle domande a cui devo rispondere;
5. i punti in cui hai dovuto assumere qualcosa, e cosa hai assunto;
6. l'elenco delle **domande del GATE 1** (§10), in forma di elenco numerato, così che
   possa risponderti in blocco;
7. il **conteggio dei blocchi `[OFF-RECORD]`** rimossi dall'ingest: se è zero, il filtro
   è rotto e ti fermi.

Non scrivere alcun capitolo in questo giro.
