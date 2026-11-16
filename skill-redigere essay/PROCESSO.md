# Il processo — dalle fonti al Word

Questo documento spiega **cosa fa la pipeline, in che ordine, e perché ogni pezzo esiste**.
Il perché conta più del come: quasi ogni regola è nata da un difetto trovato davvero scrivendo
la tesi da cui questa cartella deriva. Chi capisce il perché sa applicare la regola anche nel
caso che la regola non prevede.

## 0. Da dove viene

La tesi triennale dell'autore (Economia e Management, 2026, ~12.000 parole, 129 nodi, 65 fonti)
è stata scritta da una pipeline di agenti con due loop principali:

1. **loop fonti**: recuperare le fonti citate (loop 1) e verificare, con due lettori indipendenti
   e un validatore meccanico, che ogni fonte sostenesse davvero ciò che la tesi le attribuiva (loop 2);
2. **loop di stesura**: da una scaletta Excel di 129 nodi (ciascuno con una `Descrizione` già
   argomentata), un glossario vincolante e i risultati del loop fonti, un writer per nodo, quattro
   lint deterministici, auditor in doppia istanza, correzioni, e l'assemblaggio nel template Word
   d'ateneo.

Questa cartella è quella pipeline **ridotta e rovesciata** per un lavoro piccolo:

| | Tesi | Essay |
|---|---|---|
| scaletta | Excel di 129 nodi, scritto prima delle fonti | markdown, scritto **dopo** le fonti, dall'autore con Claude |
| loop fonti | **verifica** di claim già scritti (nodo × fonte) | **estrazione per domande** (fonte × domande del brief) |
| fonti ammesse | foglio `DOSSIER` colonna H | punti validati elencati dalla sezione |
| bibliografia | agente `bibliography-builder` | script deterministico `tools/bib.py` |
| auditor | sempre doppia istanza + arbitraggio | una istanza, doppia se `doppio_auditor` |
| controlli | 6 script separati | un solo `verifica.py` |
| documenti intermedi | nessuno (c'era l'Excel) | schede, matrice, sintesi per domanda |

Cosa **non** è cambiato: la regola sovrana, la verifica meccanica dei verbatim, la regola della
cucitura e quella del connettivo, il LEDGER, il divieto di pavimento di parole, il template obbligatorio.

## Lo schema

```
 input/brief.md ──(domande)──┐
 input/fonti.csv ─┐          │
                  ▼          ▼
 FASE 1  recupero ─► PDF ─► testi (2 rese) ─► fonti.bib
                                  │
 FASE 2  estrazione: lettore A ║ lettore B (NLM, facoltativo) ─► valida.py ─► build/estratti.json
                                                                                │  (punti fonte#n)
 FASE 3  intermedi: schede · matrice · punti.md · sintesi per domanda ◄─────────┘
                                  │
 FASE 4  SCALETTA (autore + Claude) ─► leggi_scaletta.py ─► build/sezioni.json
                                  │
 FASE 5  glossario (facoltativo) ─► lint terminologico
                                  │
 FASE 6  stesura: ctx.py ─► section-writer ─► verifica.py   (una sezione per volta, in ordine)
                                  │
 FASE 7  controlli: verifica --tutte ─► claim-auditor ─► fix / riscrittura / escalation ─► prose-auditor
                                  │
 FASE 8  Word: assemble.py (template dell'autore + APA dal .bib) ─► controlla_docx.py ─► out/
```

Ogni fase ha una skill (`/essay-…`) che la esegue. `python3 tools/stato.py` dice a che fase si è.

---

## Fase 0 — preparazione (`/essay-avvio`)

L'autore riempie `progetto.json`, `input/brief.md`, `input/fonti.csv`, e mette il template Word in
`input/template.docx`. Il brief ha una sezione che uno script legge davvero: **«Domande per le
fonti»**, un elenco puntato. Sono le domande a cui ogni lettore cercherà risposta in ogni fonte.

**Perché le domande e non i claim.** Nella tesi le affermazioni esistevano prima delle fonti, e il
rischio era confermare un claim che la fonte non regge. Qui le affermazioni non esistono ancora:
il rischio è far dire alla fonte ciò che servirebbe all'essay. Le domande tengono il lettore sul
contenuto della fonte: estrae ciò che risponde, e dichiara le domande senza risposta.

## Fase 1 — recupero delle fonti (`/essay-fonti`, loop 1)

`recupera.py` identifica ogni fonte (anche nota solo come «Autore, anno») su Crossref, OpenAlex,
arXiv, con un punteggio **deterministico** (filtro rigido sul cognome, anno ±1, similarità
TF-IDF col contesto d'uso), decide fra identificata / ambigua / non trovata, e scarica il PDF se
Unpaywall lo dà open access. Dry-run di default, backup prima di scrivere, salvataggio dopo ogni
fonte, cache su file. I paywall li scarica l'autore.

`estrai_testi.py` **congela il testo** di ogni PDF in due rese di `pdftotext` (flusso e `-raw`).
**Perché due**: sui PDF a due colonne la resa di default a volte interfoglia le colonne riga per
riga e una frase vera non esiste come stringa contigua; `-raw` ricostruisce l'ordine di lettura ma
sbaglia altrove. Nessuna domina. Una citazione autentica si ritrova in almeno una, una inventata in
nessuna. Mai `-layout`.

**Perché congelare**: i due lettori, il validatore e l'antiplagio devono leggere lo stesso testo.

`genera_bib.py` scrive la prima stesura di `fonti/fonti.bib`. Ciò che le API non danno resta vuoto.

## Fase 2 — estrazione per domande (`/essay-estrai`, loop 2)

Per ogni fonte, un **lettore Sonnet in contesto pulito** (`lettore-fonti`) legge il testo con il
metodo di `prompt/metodo-lettura.md` e scrive una scheda JSON: sintesi, **punti** (uno per idea,
ciascuno con domanda, `cosa_dice`, `forza`, citazione verbatim, sezione, eventuale seconda mano),
domande senza risposta con cosa ha cercato, limiti.

Facoltativo, un **secondo lettore indipendente** su NotebookLM (`secondo-lettore-nlm`), con le
stesse domande, isolato sulla sola fonte (`source_ids`), che non vede la scheda del primo.

Poi `valida.py`, **l'unico processo che produce il file da cui il resto legge**
(`build/estratti.json`), applica meccanicamente ciò che ai lettori è stato solo chiesto:

- ogni verbatim esiste nel testo, in una delle due rese, ≥25 caratteri, un solo passaggio;
- nessun verbatim dal front matter (ringraziamenti, copyright);
- ogni numero del `cosa_dice` compare nel testo;
- ogni domanda è coperta o dichiarata senza risposta, con una motivazione non scarna;
- chi riporta un'idea altrui (`seconda_mano`) non può «dimostrarla».

Un punto che non passa è scartato; una scheda strutturalmente sbagliata è rifiutata e il lettore
si rilancia. Ogni punto valido riceve l'id **`fonte#n`**: è l'unità di materiale citabile.

**Perché due lettori e un validatore.** Il lettore è lo stesso tipo di modello che poi scriverà:
se allucina, allucina in modo plausibile. Lo script non si fa convincere. Il secondo lettore trova
ciò che il primo ha mancato («solo NLM»): nella tesi sono emerse così 13 divergenze vere su 72
coppie, che una persona ha arbitrato una per una.

**Perché la `forza`.** È la distinzione dimostra / menziona / assume del lettore della tesi. Arriva
fino al writer, che sceglie il verbo da lì: è il presidio contro l'over-claim.

## Fase 3 — documenti intermedi (`/essay-intermedi`)

La rielaborazione delle fonti in forma che l'autore può leggere per decidere cosa sostenere:

- `intermedi/schede/<fonte>.md` — una scheda leggibile per fonte;
- `intermedi/matrice.md` — domanda × fonte: chi risponde a cosa, con quale forza; buchi in vista;
- `intermedi/punti.md` — tutti i punti con il loro id, per domanda: il menu della scaletta;
- `intermedi/sintesi-D<n>.md` — una sintesi argomentata per domanda, scritta da `sintesi-domande`
  per posizioni (convergenze, divergenze, condizioni), **ogni paragrafo ancorato a `[P:fonte#n]`**
  o dichiarato come `Lacuna:`, `Tensione:`, `Nota:`; verificata da `verifica_sintesi.py`.

**Perché esistono** (nella tesi non c'erano): la tesi partiva da una scaletta già scritta; qui la
scaletta nasce dalle fonti, e l'autore ha bisogno di vederle ordinate prima di impostarla. Sono
già testo argomentato, quindi valgono le stesse regole del testo finale.

## Fase 4 — la scaletta (`/essay-scaletta`)

**La scrive l'autore**, da solo o passo per passo con Claude, in `scaletta/scaletta.md`. Ogni
sezione ha: id e titolo, `parole`, `ruolo` (cosa deve dimostrare), `punti` (i punti validati che
usa), `aggancio` (transizione verso la sezione dopo), `trappole` (rischi), e il **contenuto**:
tutto il testo libero, cioè le idee, gli argomenti e gli esempi dell'autore.

**La scaletta è il contratto del testo.** La regola sovrana dice che la prosa di una sezione non
contiene nulla che non stia nel suo contenuto o nei suoi punti. Per questo la scrive l'autore: se
la scrivesse Claude da solo, la regola sovrana proteggerebbe le idee di Claude. È la stessa
ragione per cui nella tesi le `Descrizione` erano dell'autore (nate in dialogo con Claude, ma sue).

`leggi_scaletta.py` la trasforma in `build/sezioni.json` e controlla: punti inesistenti, sezioni
senza materiale, **rapporto materiale/parole** (sotto 0,66 la sezione uscirà corta), somma delle
parole contro il totale, punti validati non usati.

**Perché il rapporto conta.** Nella tesi la misura sul template vero ha rovesciato il regime: da
espansione a compressione (12.434 parole di materiale per 8.771 di capacità). Il writer deve sapere
se sta rendendo, comprimendo o espandendo, e **non esiste un pavimento di parole**: in compressione
un pavimento è un divieto di tagliare, in espansione è un invito a inventare.

## Fase 5 — glossario (`/essay-glossario`, facoltativo)

Candidatura deterministica dei termini (n-grammi), raggruppamento dei termini imparentati,
redazione per gruppo (`redattore-glossario`: definizioni ricavate dal materiale, non da un
dizionario; varianti vietate in due classi, `forma_errata` che blocca e `vicino_confondibile` che
avvisa), consolidamento (simmetria, definizione prima dell'uso), autotest (un glossario sano non
blocca le proprie definizioni).

**Perché.** Un argomento accademico costruisce scale di concetti vicini che non sono sinonimi. Se
chi scrive mette «expertise» dove serve «capability», l'argomento salta. Con sezioni scritte
separatamente la deriva terminologica è il rischio numero uno. Il glossario non serve a essere
letto: lo applica `verifica.py`.

## Fase 6 — stesura (`/essay-scrivi`)

Per ogni sezione, **in ordine e una alla volta**: `ctx.py` rende il contesto (solo il materiale di
quella sezione, la precedente già scritta, la successiva solo per l'aggancio, convenzioni,
glossario); `section-writer` scrive `sezioni/<id>.md` con due blocchi, `## DRAFT` e `## LEDGER`;
`verifica.py` controlla.

**La prima sezione con argomento vero è un pilota**: l'autore la legge prima che si scrivano le
altre. Nella tesi il pilota ha trovato la frase-cerniera d'annuncio in tre cappelli su tre: quello
che passa nel pilota diventa il registro di tutto il testo.

Il **LEDGER** ha una riga per paragrafo e dice da dove viene: `CONTENUTO["prima frase…"]`,
`PUNTO[fonte#n]`, `⚠ NESSUNA FONTE — transizione`, `[[GAP: …]]`. **Non porta offset di carattere**
(un LLM li sbaglia quasi sempre, e uno span sbagliato produce falsi allarmi a catena). **Non è una
prova, è un indice**: lo scrive lo stesso modello della prosa. Nessun auditor parte da lì.

`verifica.py` (tutto deterministico): token ammessi e chiavi fra le fonti ammesse; antiplagio a 8
parole contro i verbatim; ogni numero nel materiale; parole come nel Word (un CIT vale 2, un GAP 0)
contro il target ±15%; LEDGER allineato; glossario; stile (prima persona, metadiscorso,
frasi-cerniera, trattini lunghi, **connettivo inferenziale subito dopo una citazione**).

## Fase 7 — controlli (`/essay-controlla`)

`verifica.py --tutte` (antiplagio contro tutti i testi delle fonti); poi il `claim-auditor`,
**span-first**: per ogni frase cerca da solo, nel contenuto intero e nei punti, ciò che la regge.
Bersagli: frase orfana, citazione fuori contesto, over-claim, claim allargato, numeri e fatti non
nel materiale, sintesi dell'autore attribuita a una fonte, **letteratura non attribuita** (sempre
escalation all'autore: è un rilievo di plagio, non di stile), violazione della cucitura,
connettivo, trappole. Non è un rilievo la frase di transizione che collega senza affermare.

Ogni finding ha un destino: sostituzione locale → `fix-applier`; riscrittura → `section-writer`;
decisione di merito → `reports/escalation.md`, all'autore. Poi `prose-auditor`, **una volta sul
documento intero** (i tic di un testo scritto a pezzi si vedono solo di fila), con il filtro
accademico: passivo, avverbi quantificati e hedging sono legittimi.

**Perché doppio auditor (opzione).** Nella tesi ogni auditor girava in due istanze indipendenti
in contesto pulito: i finding concordi passavano, i discordi li arbitrava l'orchestratore. È
servito in entrambe le direzioni: un'istanza segnalava come orfane sei frasi di cerniera legittime
(respinte), l'altra trovava connettivi che la prima non vedeva. Su un essay breve una istanza basta
quasi sempre; il doppio si accende su `progetto.json`.

## Fase 8 — Word (`/essay-word`)

`assemble.py` parte dal **template dell'autore** (obbligatorio: se manca si rifiuta, e si chiede),
sostituisce `{{TITOLO}}`/`{{AUTORE}}`, inserisce titoli negli stili Heading 1-3 e prosa nello stile
corpo al posto di `{{CORPO}}` (o in coda), risolve i token in APA 7 dal `.bib`, aggiunge la
reference list delle sole chiavi citate, chiede a Word di aggiornare l'indice. Non scrive numeri
nei titoli se il template li numera da sé. Rifiuta se restano buchi aperti (salvo `--bozza`).
`controlla_docx.py` fa l'ultimo controllo: token residui, titoli in ordine, numeri doppi, stili.

**Perché il template e non un documento nuovo**: frontespizio, margini, interlinea, stili sono a
norma nel template e l'autore li ha sistemati a mano. Ricostruirli è rifare un lavoro fatto.

---

## Lezioni della tesi che valgono per ogni progetto

1. **Il connettivo trasporta l'attribuzione.** Vedi `CLAUDE.md`. Il difetto più frequente.
2. **Un controllo saltato in silenzio è peggio di un controllo fallito.** Se uno script non gira,
   lo si dice; non lo si sostituisce con una lettura a occhio.
3. **Il token dichiara il buco, la prosa non lo commenta.** «no source supports this» non va nel testo.
4. **Le frasi-cerniera d'annuncio escono identiche da ogni sezione** e sono il tic più
   riconoscibile di un testo scritto a pezzi. Ma tolta la frase, se il lettore perde
   un'informazione, la si riformula, non la si cancella (è già successo di sbagliare).
5. **I file derivati non si correggono a mano.** Si corregge la fonte e si rigenera.
6. **Chiudi Word ed Excel prima di scriverci.** Un salvataggio con il file aperto ha cancellato
   un foglio intero della tesi.
7. **Ciò che decide l'autore non lo decide un agente**: tagli, budget, quale fonte usare, come
   sciogliere un conflitto fra fonti. L'agente prepara la domanda, l'autore risponde.

## Quando il lavoro cambia forma

- **Niente fonti** (riflessione personale, commento): si salta da 0 a 4; la scaletta non ha `punti`
  e ogni sezione è ragionamento dell'autore. Valgono comunque stesura, controlli e Word.
- **Fonti già lette e note scritte dall'autore**: si mettono come `fonti/testi/<id>.txt` (testo
  della fonte) e si fa comunque girare l'estrazione: è la verifica che serve.
- **Revisione di un Word già scritto** (non stesura): la logica si rovescia, la regola sovrana non
  vale più (un'affermazione assente dalla scaletta non è un rilievo, lo diventa se niente la
  sostiene). Nella tesi c'era una pipeline apposta: `riferimenti-tesi/revisione-da-word/`.
