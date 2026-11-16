# Redigere essay — memoria di progetto

Regole sempre attive per ogni sessione e ogni agente che lavora in questa cartella.
Il processo completo, fase per fase e con il perché di ogni pezzo, sta in `PROCESSO.md`:
**leggilo prima di fare qualunque cosa che non sia rispondere a una domanda.**
Se questo file contraddice `PROCESSO.md` sul come, vince `PROCESSO.md`; se qualunque file
contraddice una decisione scritta dell'autore (nel brief, nella scaletta, in chat), vince l'autore.

## Cos'è questa cartella

Una pipeline di agenti e script per scrivere un **testo accademico breve** (essay, paper di
corso, relazione) dalle fonti al Word finale. È la versione generale e ridotta della pipeline
con cui è stata scritta la tesi triennale dell'autore (caso ELFO, 2026): i componenti originali
stanno in `riferimenti-tesi/`, solo come riferimento. **Non sono da eseguire.**

La cartella è un **modello**: per ogni nuovo lavoro si copia, si rinomina e si riempie `input/`.

Il lavoro non è scrivere l'essay a mano: è far girare la pipeline. Ma la **scaletta è
dell'autore** (la scrive lui, da solo o passo per passo con Claude): la pipeline lo aiuta prima
(fonti → documenti intermedi) e dopo (stesura → controlli → Word).

## La regola sovrana

Il testo dell'essay non contiene alcuna affermazione che non sia già presente, esplicitamente o
come conseguenza diretta, nel **contenuto della sua sezione della scaletta** o nei **punti
validati** che quella sezione elenca. Tutto il resto si chiede all'autore, non si colma.
**Un buco dichiarato vale infinitamente più di un buco riempito bene.**

Nessun agente inventa fonti, numeri, date o fatti. Mai.

## Le regole che si rompono più spesso

1. **Si cita solo un punto validato.** Una fonte è citabile in una sezione se e solo se la
   sezione elenca almeno un suo punto (`fonte#n`) e quel punto sta in `build/estratti.json`,
   cioè ha superato il validatore. Una fonte letta ma senza punti validi non si cita.
2. **Ogni citazione verbatim di un lettore si verifica con uno script**, mai a occhio: deve
   esistere nel testo della fonte, in un solo passaggio contiguo. Non si corregge mai una
   citazione a mano per farla passare.
3. **Niente citazioni testuali nell'essay.** Solo parafrasi attribuita. I verbatim servono alla
   verifica, non alla stesura: se finissero nel testo li troverebbe l'antiplagio
   (`verifica.py` cerca 8 parole consecutive).
4. **Il claim si restringe, mai si allarga.** Quando il contenuto della scaletta dice più del
   `cosa_dice` di un punto, vince il punto. Se restringere fa cadere l'affermazione, va in
   `[[GAP: …]]` e si porta all'autore.
5. **Il verbo segue la `forza` del punto**: `dimostra` → shows; `menziona` → notes;
   `assume` → presupposes. Mai più forte.
6. **Tagliare affermazioni è una decisione dell'autore**, non del writer. Non esiste un
   pavimento di parole: una sezione con poco materiale esce corta e si dichiara.

## Il connettivo trasporta l'attribuzione — la regola scoperta scrivendo la tesi

Il periodo con la citazione contiene solo ciò che la fonte sostiene. **Chiudere il periodo però
non chiude l'attribuzione**: un connettivo inferenziale la riapre e la porta nella frase dopo.
È stato il difetto più ricorrente della tesi (otto nodi, cinque capitoli), sempre nella stessa
forma e mai riconosciuto da chi scriveva:

- «A sharply defined identity may **accordingly** limit access…»
- «…preserve flexibility [CIT], **which** for the supplier means…»
- «… [CIT]**;** the same holds for an offering…» — il punto e virgola è il caso peggiore
- «Governance **thus** becomes a source of differentiation»

**La prova, su ogni frase che segue una citazione:** togli la citazione e rileggi. Se la frase
dopo resta sospesa, era retta dalla fonte e non può contenere l'estensione. La formula di
derivazione («Applied to…», «Building on…») va **all'inizio** della frase. Vale identica sui
rimandi interni in coda a un elenco.

## Convenzioni di stesura

- **Token**: `[[CIT-N:chiave]]` narrativa (`Akerlof (1970) shows…`), `[[CIT-P:chiave]]`
  parentetica (`… (Akerlof, 1970).`), `[[CIT-NEEDED: motivo]]`, `[[GAP: motivo]]`. Si risolvono
  solo in assemblaggio, da `fonti/fonti.bib`, in APA 7 (`tools/bib.py`). Reference list generata,
  mai scritta a mano.
- **Il token dichiara il buco, la prosa non lo commenta** («no source reviewed supports…» non si
  scrive mai: il motivo sta dentro il token).
- **Niente frasi-cerniera di annuncio dell'ordine** («The following sections…»). Il divieto
  colpisce la frase che annuncia l'ordine, non quella che dice di cosa si tratta: se togliendola
  il lettore perde un'informazione, si riformula in forma assertiva.
- **Lingua, tempi, persona, metadiscorso, nomi fissi**: in `progetto.json` (`convenzioni`,
  `nomi_fissi`). Sostituire il metadiscorso col passivo impersonale non è impersonalità, è la
  stessa frase peggiorata.
- Niente elenchi puntati nel testo, niente trattini lunghi come pausa.

## Modelli e controlli

**Tutti gli agenti girano su Sonnet** (come nella tesi, decisione dell'autore). La capacità di
controllo si compra con **più letture indipendenti in contesto pulito**, non con un modello più
grande. In questa versione ridotta: un solo `claim-auditor` di default, due istanze indipendenti
se `doppio_auditor` è `true`; un secondo lettore NotebookLM se `secondo_lettore_nlm` è `true`.
Gli script deterministici girano sempre.

## Trappole operative

- **Python**: usa `python3` (quello di miniconda ha `requests`, `openpyxl`, `python-docx`).
  `/usr/bin/python3` non ha `requests`: il loop 1 lì non parte. Serve anche `pdftotext`
  (`brew install poppler`).
- **Mai `cd` nella radice dagli script**: si lanciano con percorsi assoluti da qualunque cartella.
  Gli script trovano la radice da soli (è la cartella di `progetto.json`).
- **Chiudi Word prima di assemblare.** Se esiste un file `~$*`, fermati e segnalalo: non cancellarlo.
- **Il template Word è obbligatorio.** Se `input/template.docx` manca, chiedilo all'autore:
  non generarne uno.
- I file in `build/` e `intermedi/` (tranne le sintesi) sono **derivati**: si rigenerano, non si
  correggono a mano. Le correzioni vanno alla fonte (scheda del lettore, scaletta, sezione).
- `recupera.py` e `genera_bib.py` scrivono solo con `--commit` e fanno backup prima.

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Processo completo e motivazioni | `PROCESSO.md` |
| Istruzioni per l'autore | `LEGGIMI.md` |
| Configurazione | `progetto.json` |
| Brief dell'autore (consegna, tesi, **domande per le fonti**) | `input/brief.md` |
| Elenco fonti | `input/fonti.csv` |
| Template Word | `input/template.docx` |
| PDF e testi delle fonti | `fonti/pdf/`, `fonti/testi/`, `fonti/testi_raw/` |
| Schede dei lettori | `fonti/schede/` (A), `fonti/schede_nlm/` (B) |
| Punti validati (unica fonte di verità sulle fonti) | `build/estratti.json` |
| Documenti intermedi | `intermedi/` |
| **Scaletta = contratto del testo** | `scaletta/scaletta.md` → `build/sezioni.json` |
| Glossario | `glossario/glossario.json` |
| Sezioni scritte (DRAFT + LEDGER) | `sezioni/<id>.md` |
| Report di controllo, escalation | `reports/` |
| Word finale | `out/` |
| Stato del progetto | `python3 tools/stato.py` |
| Componenti originali della tesi | `riferimenti-tesi/` (leggi `riferimenti-tesi/LEGGIMI.md`) |

Skill: `/essay-avvio`, `/essay-fonti`, `/essay-estrai`, `/essay-intermedi`, `/essay-scaletta`,
`/essay-glossario`, `/essay-scrivi`, `/essay-controlla`, `/essay-word`, `/essay-stato`.
Agenti: `lettore-fonti`, `secondo-lettore-nlm`, `sintesi-domande`, `redattore-glossario`,
`section-writer`, `claim-auditor`, `fix-applier`, `prose-auditor`.
