# Tesi Falzi — memoria di progetto

Regole sempre attive per ogni sessione e ogni agente che lavora in questa cartella.
Il design completo della pipeline sta in `PROMPT-orchestratore-tesi.md` (rev. 2026-09-08).
Questo file è il riassunto vincolante: se contraddice quel documento, vince quel documento;
se contraddice una `[DECISIONE AUTORE]` nell'Excel, vince la decisione dell'autore.

## Cos'è questo progetto

Tesi triennale in Economia e Management, in inglese, sulla differenziazione competitiva
nello sviluppo software custom sotto AI generativa, con il caso aziendale ELFO.
Il lavoro **non** è scrivere la tesi a mano: è far girare una pipeline di agenti che va da
`iTOC master.xlsx` (129 nodi con `Descrizione` già argomentata) a `out/tesi.docx`.

## La regola sovrana

Il testo della tesi non contiene alcuna affermazione che non sia già presente,
esplicitamente o come conseguenza diretta, nella colonna `Descrizione` dell'`iTOC` o nel
foglio `Estratti`. Tutto il resto si **chiede all'autore**, non si colma.
**Un buco dichiarato vale infinitamente più di un buco riempito bene.**

Nessun agente inventa fonti, numeri, date o fatti su ELFO. Mai.

## Le cinque regole che si rompono più spesso

1. **Si cita dal `DOSSIER`, mai da `Estratti`.** Una fonte è citabile in un nodo se e solo
   se la sua chiave compare in `DOSSIER` colonna H `Fonti AMMESSE`. La colonna I
   `Fonti VIETATE` è un divieto assoluto. Oggi: 100 coppie ammesse, 8 vietate.
   Chi legge `Estratti` colonna `Esito` cita fonti che l'autore ha rimosso per iscritto.
2. **I blocchi `[OFF-RECORD]` non si ingeriscono e non si passano ad alcun agente.**
   Oggi ce n'è uno solo, nel nodo `5.1.4`, e `dossier.py` lo copia verbatim in `DOSSIER`
   colonna O: il filtro va applicato in ingest, non dato per scontato.
3. **Le `[DECISIONE AUTORE]` nella colonna `Note` e le `Risoluzione` in `Estratti!S` sono
   vincolanti** e battono qualunque referto, qualunque file di stato e questo file.
   Oggi: `Note` piena su 48 nodi, 14 con `[DECISIONE AUTORE]`; `Estratti!S` su 30 coppie.
4. **Niente citazioni testuali.** Solo parafrasi attribuita: le linee guida d'ateneo
   impongono il numero di pagina per le citazioni dirette e nessuno dei 103 verbatim di
   `Estratti` ce l'ha. Quei verbatim sono testo copiato dai PDF: se finissero in tesi senza
   virgolette li troverebbe l'antiplagio. Servono alla verifica, non alla stesura.
5. **Su una coppia `da riformulare` vince `Cosa dice davvero`: il claim si restringe, mai
   si allarga.** Se la restrizione fa cadere l'affermazione della `Descrizione`, il nodo va
   in `[[GAP: …]]` e si porta all'autore — non si riscrive.

## Il connettivo trasporta l'attribuzione — la regola scoperta scrivendo

La regola della cucitura dice che il periodo con la citazione contiene solo cio' che la fonte
sostiene. **Chiudere il periodo pero' non chiude l'attribuzione**: un connettivo inferenziale la
riapre e la porta nella frase successiva. E' il difetto piu' ricorrente della tesi, trovato in
**otto nodi di cinque capitoli**, sempre nella stessa forma e mai riconosciuto da chi scriveva:

- «A sharply defined identity may **accordingly** limit access…» (`4.2.3`)
- «…preserve flexibility [CIT], **which** for the supplier means…» (`2.2.3`)
- «… [CIT]**;** the same holds for an offering…» (`2.1.4`, `3.2.3`)
- «Governance **thus** becomes a source of differentiation» (`2.2.2`)

Il **punto e virgola** e' il caso peggiore, perche' nessuno lo percepisce come connettivo.

**La prova, da fare su ogni frase che segue una citazione:** togli la citazione dal paragrafo e
rileggi. Se la frase seguente resta sospesa o incomprensibile, era retta dalla fonte e non puo'
contenere l'estensione della tesi. La formula di derivazione va **all'inizio** della frase.

Vale identica sui **rimandi interni**: «as section 6.1 argues» in coda a un elenco si legge come
se coprisse l'elenco intero (`7.3.5`, `7.3.6`).

## Il regime è di compressione, non di espansione

Misurato sul template a norma (Times New Roman 12, interlinea esatta 23 pt, ~350
parole/pagina, banda 310-380): in perimetro ci sono **12.434 parole di materiale** (dopo la
riscrittura dei nodi bloccati dell'8 settembre) contro **8.771 di capacità** a 30 pagine. Il Cap. 5 da solo eccede di
3.743 parole (10,7 pagine): contiene il 53,5% del materiale e ha il 30% del budget.

Conseguenze operative:
- **il pavimento di parole non esiste più**: in compressione un pavimento è un divieto di
  tagliare;
- `target_words` si deriva dal materiale e dal budget, non da una costante;
- **`1 riga:` nel campo `Ruolo` è una specifica di lunghezza e vale 130 parole**
  ([DECISIONE AUTORE 2026-09-08], documentata in fondo al foglio `Legenda`). Il target del
  nodo è `min(parole della Descrizione, 130)`, il `Ruolo` batte il budget, e questi nodi non
  assorbono il residuo del capitolo. 28 nodi foglia in perimetro sono sopra il tetto e
  lasciano fuori 2.435 parole, **di cui 2.346 nel solo Cap. 5**: fuori da lì il tetto quasi
  non morde. Dove toglie più della metà del materiale — otto nodi, il peggiore è `5.2.3` con
  −268 parole su 398 — **il writer deve dichiarare quali affermazioni lascia fuori**: è
  selezione, non compressione;
- **tagliare affermazioni è una decisione dell'autore, non del writer.** La compressione del
  Cap. 5 si propone e si fa approvare prima di scriverlo.

## Modelli

**Tutti gli agenti girano su Sonnet, senza eccezioni** (decisione dell'autore, 2026-09-08).
La capacità di controllo si compra con **più agenti indipendenti e più giri**, non con un
modello più grande: ogni auditor gira come due istanze separate in contesto pulito che non
si vedono fra loro, i finding concordi passano, i discordi li arbitra l'orchestratore.
È lo schema del doppio lettore già validato sul loop di verifica delle fonti.
Opus resta solo per l'orchestratore, che non scrive né corregge mai una riga di tesi.

## Convenzioni di stesura già chiuse

- **Citazioni**: APA 7 autore-data inline, reference list finale alfabetica generata da
  `FONTI/tesi.bib` (65 voci), mai a mano. Token sdoppiato: `[[CIT-N:chiave]]` per la forma
  narrativa (`Akerlof (1970) shows that …`), `[[CIT-P:chiave]]` per la parentetica
  (`… (Akerlof, 1970).`). Mancanze: `[[CIT-NEEDED: motivo]]`. Buchi: `[[GAP: motivo]]`.
- **Niente frasi-cerniera di annuncio** in chiusura di cappello: *«The following two
  sections treat them in turn…»* e simili non affermano nulla, l'ordine lo dicono le
  intestazioni, e la stessa sagoma esce identica da ogni cappello. Trovata in tre cappelli
  su tre nel pilota del Cap. 3, rimossa e vietata. **Il divieto colpisce la frase che
  annuncia l'ordine espositivo, non quella che dice di cosa si tratta**: se togliendola il
  lettore perde un'informazione, va riformulata in forma assertiva, non cancellata — è già
  successo di sbagliare su `3.2`. Il campo `Aggancio` è ancora un'altra cosa: chiede una
  transizione argomentativa, non un sommario.
- **Tempi e persona** (GATE 2, chiuso — testo integrale nel rilievo `AG-04` del foglio
  `AUDIT 2026-09-07`): presente semplice per la teoria, passato semplice per il disegno e i
  risultati dei singoli studi e per i fatti ELFO. **Mai la prima persona**, né singolare né
  plurale. **Metadiscorso ridotto al minimo**: `This thesis…` solo nel Cap. 0 e
  nell'abstract, `This chapter…` solo nel primo e nell'ultimo paragrafo di un capitolo.
  Altrove il soggetto grammaticale non è mai il documento: è il meccanismo, l'attore di
  mercato, la fonte. Sostituire il metadiscorso col passivo impersonale non è impersonalità,
  è la stessa frase peggiorata. **L'azienda è sempre ELFO, mai «the company».**

## Trappole operative — costano ore quando si dimenticano

- **Usa `/usr/bin/python3`**: ha `openpyxl` 3.1.5 e `python-docx`. Il `python3` di default
  è miniconda e non li ha.
- **Non fare `cd` in questa cartella** dagli script della pipeline: rompe gli import
  relativi. Percorsi assoluti.
- **Chiudi Excel e Word prima di scriverci.** Un salvataggio dell'autore con il file già
  aperto ha cancellato un foglio intero. Se esiste un file `~$*`, fermati e segnalalo: non
  cancellarlo.
- **Backup con timestamp prima di ogni modifica non banale**, in `iTOC master backup/`:
  `iTOC master.<AAAAMMGG_HHMMSS>_<motivo>.xlsx`.
- **`dossier.py` fa `wb.save()` sullo stesso Excel** e cancella e ricrea il foglio
  `DOSSIER`: non scriverci mai a mano, e rigeneralo come **ultimo atto prima dello
  snapshot** in `source/`, mai dopo.
- **`scrivi.py` riscrive `Estratti` H, I, J, K, L, N** a ogni giro: non metterci decisioni.
  R e S sono fuori dalla sua portata, ed è per questo che stanno in fondo.
- **I contatori laterali di `Fonti` (Y-Z) ed `Estratti` (P-Q) sottostimano**: gli intervalli
  sono fermi a righe che non esistono più. Non citare quei numeri.
- **`iTOC master copy.xlsx` e i backup non sono fonti di verità.** L'unico file vero è
  `iTOC master.xlsx`.
- **Più sessioni lavorano in parallelo qui.** Ricarica il file prima di scrivere.

## I numeri veri, al 2026-09-08

129 nodi (**tutti e 129 in perimetro**: il Cap. 7 e' rientrato) · 7 fogli
nell'Excel · 67 righe in `Fonti` (64 `scaricata`, 2 `abbandonata`, 1 `da_cercare`) · 108 coppie in `Estratti` · 100 ammesse,
8 vietate · 65 voci in `tesi.bib` · 12.938 parole di `Descrizione`, 12.434 in perimetro · 47 nodi con almeno una
fonte ammessa, 82 senza · 52 nodi con `Aggancio` · 50 nodi con `Trappole` in perimetro ·
7 nodi in perimetro con `Descrizione` vuota (`0.1`, `0.1.1`-`0.1.4`, `0.2.3`, `1.2`) ·
`Budget pp` = `0→2 1→5 2→5 3→4 4→5 5→13 6→2 7→3` = **39 di budget**, ~40 pagine reali
contando le code di pagina dei `pageBreakBefore` (accettato dall'autore). Ogni capitolo in regime di resa (k fra 0,95 e 1,20) tranne il Cap. 5, in
compressione a k = 0,64.

**La tesi e' scritta**: 124 nodi su 126 scrivibili, ~11.950 parole contro 11.880 di capienza
(101%). Restano fermi due nodi soli, entrambi su una decisione dell'autore: `0.2.4` (la
definizione di «generative AI», la cui fonte e' vietata dal gate perche' non letta) e `7.4.8`
(dove un errore di estrazione dal Word ha depositato la chiusura dell'intera tesi).

**Il Cap. 7 non e' piu' sospeso**: budget `7->3`, 23 nodi scritti, in perimetro anche nel codice
(`PERIMETRO_CAPITOLI` in `ingest.py` era rimasto indietro, e teneva le sue 504 parole fuori dalla
whitelist di `lint_numeri`).

**Audit fatti**, ciascuno in doppia istanza indipendente: `claim-auditor` sui capitoli 1-7,
`citation-auditor` su 1, 2, 3, 4, `chapter-auditor` sul Cap. 5. Tutti i rilievi confermati sono
stati applicati; gli arbitraggi stanno in `reports/arbitraggio-*.md`. **Non ha ancora girato il
`prose-auditor`**, che e' l'unico stadio mai eseguito.

**`tools/assemble.py` e `build/matrici.json` esistono** (scritti il 2026-09-08, il primo mancava
del tutto). `assemble.py` gira e rifiuta finche' il GATE 3-bis e' aperto: il suo rifiuto e'
l'elenco esatto di cio' che manca, e si riproduce con `--dry-run`.

**Il GATE 3-bis e' aperto** e il suo ordine del giorno sta in fondo a `reports/escalation.md`:
due nodi fermi, quattro `[[CIT-NEEDED:]]` dichiarati nel testo, sette decisioni di merito.

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Design della pipeline | `PROMPT-orchestratore-tesi.md` |
| L'Excel, unica fonte di verità | `iTOC master.xlsx` |
| Il foglio da cui si scrive | foglio `DOSSIER` |
| Cosa resta da fare | fogli `AUDIT 2026-09-07` e `PROSSIMI PASSI` |
| Stato del progetto | `FONTI/pipeline/referti/STATO E PROSSIMI PASSI.md` (unico) |
| Fonti da recuperare | `FONTI/pipeline/referti/DA SCARICARE.md` (unica) |
| Linee guida d'ateneo | `info & contesto/guide.pdf` e `…/Linee-guida_per_la_citazione…pdf` |
| Template Word | `LF3236167.docx` |
| Bibliografia | `FONTI/tesi.bib` |
| Testi dei PDF, per grep | `FONTI/pipeline/testi estratti/` (67 file) |
| Glossario e linter | `FONTI/pipeline/glossario/` |
| Matrici del Cap. 5 | `FONTI/pipeline/tabelle-cap5.md` |

Non scrivere mai un nuovo file di stato o di recupero fonti: aggiorna i due canonici.
