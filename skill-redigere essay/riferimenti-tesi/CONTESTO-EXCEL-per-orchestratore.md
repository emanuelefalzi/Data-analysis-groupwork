# L'Excel della tesi: cosa contiene, colonna per colonna

**A chi è rivolto.** Alla sessione che dovrà costruire l'orchestratore di stesura. Leggi
questo file prima di `PROMPT-orchestratore-tesi.md`: quello descrive la macchina da
costruire, questo descrive i dati su cui dovrà girare.

**Cosa sostituisce.** Questo file sostituisce `CONTESTO-per-orchestratore.md` per la parte
che riguarda l'Excel. Quel file è fermo alle 11:48 del 2026-09-07 e i suoi numeri sono
sbagliati per difetto (dichiara 58 fonti e 82 coppie: sono 66 e 107). Non usarlo per i
conteggi.

**Data di questo file: 2026-09-07, sera.** I numeri qui sotto erano veri al momento della
scrittura. Prima di fidartene, rifalli: bastano dieci secondi e ti risparmiano il problema
che ha ucciso il file precedente.

```bash
/usr/bin/python3 -c "
import openpyxl
wb=openpyxl.load_workbook('iTOC master.xlsx',read_only=True,data_only=True)
print([(w.title, w.max_row-1) for w in wb.worksheets])"
```

Usa **`/usr/bin/python3`** (ha openpyxl 3.1.5). Il `python3` di default punta a miniconda e
openpyxl non ce l'ha.

---

## 1. Il modello dati in una pagina

`iTOC master.xlsx` è l'unica fonte di verità del progetto. Sette fogli:

| Foglio | Righe | Cos'è | Si legge / si scrive |
|---|---|---|---|
| `iTOC` | 128 nodi | La tesi: un nodo per sezione, con la Descrizione argomentata già scritta | **sorgente**, si scrive a mano o con script mirati |
| `Fonti` | 66 | Una riga per fonte bibliografica | **sorgente**, scritta dai loop di recupero |
| `Estratti` | 107 | Una riga per **coppia nodo × fonte**, col verdetto dei due lettori | **sorgente**, scritta dai loop di verifica |
| `DOSSIER` | 128 | Vista derivata: unisce i tre fogli sopra e risolve già l'esito | **sola lettura**, rigenerata da script |
| `Legenda` | — | Documentazione di tutte le colonne, scritta dall'autore | riferimento |
| `AUDIT 2026-09-07` | 50 | I rilievi dell'audit, con chi li può chiudere | si aggiorna la colonna di stato |
| `PROSSIMI PASSI` | 30 | La checklist in ordine di esecuzione | si aggiorna la colonna di stato |

**La regola che conta più di tutte: per scrivere un nodo si legge il `DOSSIER`, non
`iTOC` + `Estratti` a mano.** Il DOSSIER esiste apposta: ha già applicato la regola
dell'esito effettivo e ti dice, per quel nodo, quali fonti puoi citare e quali no. Chi
legge `iTOC` colonna D da sola cita fonti che sono state escluse.

Stato attuale della stesura: **zero righe di tesi scritte**. `Stato` è vuoto su 99 nodi e
vale `bozza` sui 29 del Cap. 5, compilati dall'intervista del 6 settembre. Le Descrizioni
sommano 12.435 parole contro un budget di 32 pagine.

---

## 2. Foglio `iTOC` — la tesi

Un nodo per riga, indice gerarchico da `0` a `7.4.8`. L'ultima riga è `TOTALE pp attese`,
una formula: non è un nodo, saltala.

| Col. | Nome | Cosa contiene | Come si usa |
|---|---|---|---|
| **A** | `Indice` | Numerazione gerarchica (`1.2.3`). Stringa, non numero | Chiave del nodo. Non modificare |
| **B** | `Titolo nodo` | Titolo della sezione, senza numerazione | Correggere solo refusi |
| **C** | `Descrizione` | **Il testo argomentato del nodo, in inglese.** È la base della stesura, migrata fedelmente dal Word | Non riassumere, non riscrivere, non inventare. Si espande, non si sostituisce |
| **D** | `Fonti + ruolo` | Per ogni fonte citata nella Descrizione: cosa porta e con che ruolo (`mattone stretto` / `sfondo`), più i vincoli d'uso decisi | **Non basta da sola**: dice cosa il nodo *vorrebbe* citare, non cosa può. L'autorità è il DOSSIER |
| **E** | `Ruolo argomentativo` | Cosa il nodo deve dimostrare e come si aggancia al precedente e al successivo, in forma `Deve dimostrare: … / Aggancio: …` | È la guida di scrittura del paragrafo. Presente in forma estesa su 51 nodi |
| **F** | `Note` | Annotazioni. Tre prefissi hanno valore vincolante: `[DECISIONE AUTORE <data>]`, `[OFF-RECORD]`, `[AUDIT 2026-09-07]` | **Le decisioni dell'autore battono qualunque referto e qualunque altro file.** Leggile sempre prima di scrivere il nodo |
| **G** | `Trappole / rischi` | Rischi concreti su quel nodo: attribuzioni improprie, over-claim, stime spacciate per dati, termini da definire | Da rileggere prima di considerare il nodo finito. Spesso il nodo si autodenuncia qui |
| **H** | `Stato` | Avanzamento redazionale: vuoto / `bozza` / `rivisto` / `ok` | |
| **I** | `Budget pp` | Pagine attese. **Valorizzata solo sulle righe di capitolo** | `0→1 1→4 2→3 3→4 4→8 5→7 6→3 7→2`, totale 32. L'autore ha deciso che resta così: la riallocazione a 31 pagine che trovi nel prompt orchestratore è un appunto storico, non una regola |

47 nodi su 128 hanno fonti; 47 hanno Note. Gli altri sono nodi di sintesi o di raccordo.

---

## 3. Foglio `Fonti` — una riga per fonte

| Col. | Nome | Cosa contiene |
|---|---|---|
| **A** | `ID` | Chiave bibliografica (`agrawal2018`). **È la chiave che collega tutto**: `Estratti`, `tesi.bib`, i nomi dei file in `FONTI/pipeline/testi estratti/` |
| **B** | `Citazione` | Forma autore-data già pronta, `(Agrawal, Gans & Goldfarb, 2018)` |
| **C**, **D** | `Autori`, `Anno` | |
| **E** | `Ruolo` | `mattone stretto` (sostiene direttamente un'affermazione originale: se cade, l'argomento crolla) o `sfondo` (inquadramento: se cade, indebolisce ma non invalida). 52 mattoni stretti, 14 sfondi |
| **F** | `Priorità` | Calcolata come ruolo × numero di nodi che la usano |
| **G**, **H** | `Nodi che la usano`, `N. usi` | Elenco degli indici, separati da `;` |
| **I** | `Query di ricerca` | Stringa usata dal loop di recupero. Solo diagnostica |
| **J** | `Contesto d'uso` | Le frasi della tesi in cui la fonte compare, numerate per nodo |
| **K** | `Claim da verificare` | Cosa si chiedeva di verificare ai lettori. Può portare marcatori tipo `ATTRIBUZIONE INCERTA` |
| **L** | `Stato acquisizione` | `scaricata` (64) o `abbandonata` (2). Le abbandonate restano come record storico: non cancellarle, non citarle |
| **M**–**O** | `Titolo`, `Tipo`, `Sede / editore` | Metadati bibliografici |
| **P**, **Q**, **R** | `DOI`, `URL`, `Open access` | |
| **S** | `PDF locale` | Percorso assoluto del PDF in `FONTI/fonti def/`. 64 fonti su 66 ce l'hanno |
| **T** | `Peer-reviewed` | 52 sì, 14 no. Rilevante: una fonte non peer-reviewed non può reggere da sola un passaggio portante |
| **U**, **V** | `Stato verifica`, `Cosa dice davvero` | Reduci del primo giro di verifica, oggi in gran parte vuote: **la verifica vera sta in `Estratti`**, per coppia, non per fonte |
| **W** | `Note` | Annotazioni del recupero |
| **X** | *(senza nome)* | Colonna vuota di separazione |
| **Y**, **Z** | `AVANZAMENTO` | Blocco di contatori. **Non usarli: gli intervalli sono fermi a riga 52 su un foglio di 66 righe, quindi sottostimano.** Vedi rilievo `AG-10` |

---

## 4. Foglio `Estratti` — una riga per coppia nodo × fonte

È il cuore probatorio del lavoro. Ogni riga è una fonte letta **in funzione di uno
specifico nodo**: la stessa fonte compare più volte se serve a nodi diversi, e può essere
usabile in uno e no in un altro.

| Col. | Nome | Cosa contiene |
|---|---|---|
| **A**, **B** | `Nodo`, `ID fonte` | La coppia. Insieme sono la chiave |
| **C**, **D**, **E**, **F** | `Citazione`, `Ruolo`, `Peer-rev.`, `PDF` | Copiate da `Fonti` per comodità di lettura |
| **G** | `Claim da verificare` | L'affermazione che quel nodo fa poggiare su quella fonte |
| **H** | `Esito` | **Verdetto del lettore A** (agente locale su PDF): `usabile` / `da riformulare` / `non usabile` |
| **I** | `Cosa dice davvero` | Cosa la fonte sostiene realmente sul punto. **È la colonna che si legge prima di scrivere una frase citata** |
| **J** | `Citazione verbatim` | Estratto testuale a supporto del verdetto. Serve alla verifica, **non alla stesura**: le linee guida d'ateneo impongono il numero di pagina per le citazioni dirette e qui non c'è. Si parafrasa sempre |
| **K** | `Sezione` | Punto del paper da cui viene il verbatim |
| **L** | `Esito NotebookLM` | **Verdetto del lettore B**, indipendente. Include `non verificabile` e `non verificato` |
| **M** | `Divergenza` | Marcata quando i due lettori non concordano |
| **N** | `Note` | Note di verifica, spesso con la correzione già scritta |
| **O** | *(senza nome)* | Separazione |
| **P**, **Q** | `AVANZAMENTO VERIFICA` | Contatori. **Stessi intervalli scaduti del foglio `Fonti`: non usarli** |
| **R** | `Esito arbitrato` | La decisione dell'autore sulla coppia: `usabile` / `da riformulare` / `riformulata` / `non usabile` / `nessun arbitrato` / `chiusa nel nodo` / `superata` / `rimossa dal nodo` / `DA DECIDERE` |
| **S** | `Risoluzione (decisione autore)` | Il testo della decisione, con il motivo e **i vincoli d'uso vincolanti in stesura** |

**Perché R e S stanno in fondo e non accanto ad H.** `scrivi.py` riscrive H, I, J, K, L ed
N a ogni giro del loop: qualunque decisione scritta lì viene persa. R e S sono fuori dalla
sua portata e sopravvivono. Se scrivi uno script che tocca questo foglio, rispetta il
confine.

Verdetti attuali del lettore A: 42 `usabile`, 56 `da riformulare`, 7 `non usabile`.
Arbitrati registrati: 30.

---

## 5. Foglio `DOSSIER` — la vista da cui si scrive

Una riga per nodo, rigenerata da `iTOC` + `Fonti` + `Estratti`. **Non si compila a mano.**
Dopo qualunque modifica ai fogli sorgente:

```bash
/usr/bin/python3 "FONTI/pipeline/dossier.py"
```

| Col. | Nome | Cosa contiene |
|---|---|---|
| **A**–**D** | `Indice`, `Cap.`, `Liv.`, `Titolo nodo` | Identificazione del nodo |
| **E**, **F**, **G** | `Stato`, `Budget pp`, `Parole Descrizione` | Il conteggio parole serve a calcolare quanto va espanso il nodo |
| **H** | `Fonti AMMESSE (chiavi)` | **Le uniche fonti citabili in quel nodo**, con l'esito effettivo già risolto fra parentesi quadre: `fukui2026 [usabile] ; peng2023 [da riformulare]`. Separatore ` ; ` |
| **I** | `Fonti VIETATE (chiavi + motivo)` | Fonti escluse dal nodo, col motivo. **Citarle è un errore, anche se compaiono ancora in `iTOC` colonna D** |
| **J** | `N. coppie` | Quante coppie ha il nodo |
| **K** | `⚠ COERENZA` | Controllo automatico: fonti fantasma, fonti abbandonate ancora citate, coppie mancanti, nodi foglia senza fonti. **Oggi è vuota su tutti i 128 nodi.** Se dopo una tua modifica si popola, hai rotto qualcosa |
| **L**–**O** | `Descrizione (letterale)`, `Ruolo argomentativo`, `Trappole / rischi`, `Note autore` | Copiate da `iTOC` |
| **P** | `Fonti + ruolo (da iTOC)` | Copia della colonna D, per confronto |
| **Q** | `DOSSIER FONTI (Estratti, per coppia)` | Il dossier completo di ogni coppia: claim, cosa dice davvero, note, vincoli |

**La regola dell'esito effettivo**, implementata in `dossier.py` e corretta il 2026-09-07:

1. Un verdetto esplicito in R batte sia il lettore A sia NotebookLM.
2. `superata` e `rimossa dal nodo` → fonte **vietata**.
3. `nessun arbitrato` → **vale il lettore A**, non il peggiore dei due: il `non usabile` di
   NotebookLM è l'artefatto noto della citazione congiunta. Il claim va scomposto in stesura.
4. `chiusa nel nodo` → la fonte resta **se `Fonti + ruolo` la elenca ancora**, e il vincolo
   d'uso in colonna S diventa obbligatorio.
5. Altrimenti vince il verdetto più severo fra i due lettori. `non verificabile` non conta.

Esito su 107 coppie: **33 usabili, 68 da riformulare, 6 vietate**. «Da riformulare» non
significa buco: significa che il nucleo regge ma il nodo generalizza il lessico o la
portata, e la correzione è già scritta in colonna.

---

## 6. Fogli `AUDIT 2026-09-07` e `PROSSIMI PASSI`

Prodotti dall'audit del 7 settembre. **Sono la risposta alla domanda «cosa resta da fare».**

`AUDIT 2026-09-07`, 50 rilievi: `ID` · `Data` · `Area` · `Tipo` · `Destinazione` (nodo o
file) · `Rilievo` (autoconsistente, si legge senza aprire altro) · `Stato epistemico` ·
`Azione richiesta` · `Priorità` · `Provenienza` · `Stato lavorazione` · **`Chi lo chiude`**.

`PROSSIMI PASSI`, 30 passi: `#` (ordine di esecuzione reale) · `Fase` · `Passo` · `Perché`
· `Dipende da` · `Output atteso` · `Priorità` · `Stato`.

**La colonna `Chi lo chiude` è il confine oltre il quale un agente non va da solo:**

- **`orchestratore` (32 rilievi, 10 bloccanti)** — lavoro meccanico o testuale, verificabile
  sui fogli. Applicare una decisione già registrata, restringere un claim alla clausola che
  la fonte regge davvero, scrivere un paragrafo di apertura da materiale già presente,
  correggere un refuso, riscrivere un documento disallineato, costruire uno script.
- **`orchestratore, poi approvazione autore` (4)** — l'orchestratore indaga, prepara e
  propone, ma non decide: la proposta va approvata prima di entrare nella tesi.
- **`autore` (14, di cui 4 bloccanti)** — decisioni di merito che nessun agente può prendere
  al posto suo, e informazioni che solo lui ha.

I quattro bloccanti che **restano all'autore**, e senza i quali la stesura non parte:

1. **Cap. 4** (`ST-01`): il capitolo ha 8 pagine di budget e il 32% del testo necessario. O
   si espande, o si riduce il budget. È allocazione di spazio: decide l'autore.
2. **Cap. 2** (`ST-10`): già al 92% del budget, con 22 nuove coppie fonte da integrare in
   prosa. Alzare il budget o comprimere `2.2.1`-`2.2.3`.
3. **Definizione di «generative AI»** (`ST-03`): nessuno dei 128 nodi la dà, e l'intera
   research question ci poggia sopra. Delimitare il costrutto cambia cosa la tesi afferma:
   non è una scelta redazionale.
4. **Tempi verbali e persona** (`AG-04`, GATE 2): senza questa convenzione gli auditor
   litigano su base stilistica a ogni giro. Il design lo dichiara esplicitamente.

Tutto il resto dei bloccanti è tuo. In particolare `CL-01` (nodo `3.2.2` afferma oggi una
cosa che Kahneman & Klein contraddicono, e la decisione di correggerlo è ferma dal 6
settembre in `Estratti` colonna S), `CL-09` (sciogliere le sei fonti affollate su `1.2.3`),
`ST-02` (scrivere il paragrafo di apertura del Cap. 6), `AG-02` (riscrivere il prompt
orchestratore, disallineato su sei punti), `RC-01` e `RC-02`.

---

## 7. Le regole che non si negoziano

1. **Nessun agente inventa fonti, numeri, date o fatti su ELFO.** I buchi si dichiarano
   all'autore, non si riempiono.
2. **Si scrive dal `DOSSIER`.** `iTOC` colonna D dice cosa il nodo vorrebbe citare; il
   DOSSIER dice cosa può.
3. **Le decisioni in `Note` e in `Estratti` colonna S sono vincolanti** e battono qualunque
   referto, qualunque file di stato e qualunque cosa scritta in questo file.
4. **Regola della cucitura.** Ogni periodo che porta una citazione deve contenere **solo**
   ciò che quella fonte sostiene, verificato come lookup nella colonna `Cosa dice davvero`
   della riga giusta di `Estratti`, mai a memoria. Le clausole che nessuna fonte regge
   restano senza citazione. È il difetto più diffuso dell'impianto: circa 30 nodi citano
   2-4 fonti insieme senza assegnare le clausole.
5. **Mattone stretto ≠ sfondo.** Un mattone stretto che cade obbliga a riscrivere
   l'argomento, non la frase. Verificalo prima di scrivere il nodo che lo usa.
6. **Niente citazioni testuali, solo parafrasi attribuita.** Le linee guida d'ateneo
   impongono il numero di pagina per le citazioni dirette, e i verbatim in `Estratti` non
   ce l'hanno.
7. **Citazioni autore-data APA 7 inline**, reference list finale alfabetica generata da
   `FONTI/tesi.bib` (64 voci), **mai a mano**. Il token va sdoppiato: `[[CIT-N:chiave]]`
   per la forma narrativa («Akerlof (1970) mostra che…»), `[[CIT-P:chiave]]` per la
   parentetica («… (Akerlof, 1970).»). Il prompt orchestratore usa ancora il vecchio
   `[[CIT:]]`: va corretto.
8. **Ciò che è deduzione dell'autore si dichiara.** Diverse definizioni-cardine (domain
   knowledge in `2.2.4`, execution/judgment in `1.2.1`, la cornice di `2.3.2`) e il
   meccanismo centrale di `4.3.3` sono costruzioni originali, non contenuto delle fonti. Si
   dichiarano come estensioni teoriche, sempre, con la stessa formula.

---

## 8. Le trappole operative di questo file Excel

- **Chiudi l'Excel prima di scriverci.** Un salvataggio dell'autore con il file già aperto
  ha cancellato un foglio intero.
- **Backup con timestamp prima di ogni modifica non banale.** Convenzione già in uso:
  `iTOC master.<AAAAMMGG_HHMMSS>_<motivo>.xlsx`. `scrivi.py` lo fa da solo.
- **Non fare `cd` nella cartella della tesi** dagli script della pipeline: rompe gli import
  di Python. Usa percorsi assoluti.
- **`scrivi.py` riscrive H, I, J, K, L, N di `Estratti`.** Non metterci decisioni.
- **`dossier.py` cancella e ricrea il foglio `DOSSIER`.** Non scriverci nulla a mano.
- **I contatori laterali di `Fonti` ed `Estratti` sottostimano** perché gli intervalli sono
  fermi a righe che non esistono più (rilievo `AG-10`). Conta dai fogli, non da lì.
- **`iTOC master copy.xlsx` e i `backup_*.xlsx` non sono fonti di verità.** L'unico file
  vero è `iTOC master.xlsx`.
- **Più sessioni lavorano in parallelo su questa cartella.** Ricarica il file prima di
  scrivere, non tenere in memoria uno stato vecchio.

---

## 9. Dove sta il resto

- **Stato del progetto:** `FONTI/pipeline/referti/STATO E PROSSIMI PASSI.md`. È l'unico
  file di stato valido. `FONTI/pipeline/STATO.md` e `referti/DA SCARICARE.md` sono superati
  nonostante si autodichiarino attuali.
- **Sintesi dell'audit:** `FONTI/pipeline/referti/AUDIT COMPLETO 2026-09-07.md`.
- **Design della macchina da costruire:** `PROMPT-orchestratore-tesi.md`. La logica
  (LEDGER, gate, gli 11 principi) è valida; i numeri e sei dettagli operativi no: leggi
  prima il rilievo `AG-02`.
- **Template d'ateneo:** `LF3236167.docx`, base dell'output impaginato.
- **Linee guida d'ateneo:** `info & contesto/guide.pdf` e
  `info & contesto/Linee-guida_per_la_citazione_bibliografica…pdf`. **Esistono**: i
  documenti che dicono il contrario cercano la cartella `info uni/`, che è stata rinominata.
- **PDF delle fonti:** `FONTI/fonti def/`. **Testi estratti** (uno per chiave, per grep):
  `FONTI/pipeline/testi estratti/`.
- **Bibliografia:** `FONTI/tesi.bib`, allineata al foglio `Fonti`.
- **Glossario:** `FONTI/pipeline/glossario/glossario.json`, 48 termini. `lint.py` gira e dà
  3 blocchi, tutti falsi positivi noti (rilievo `AG-07`).
- **Matrici del Cap. 5:** vivono nel Word `def titolo C_EN.docx`, non nell'Excel, e sono
  rimaste indietro rispetto all'intervista (rilievi `RC-03`, `RC-04`).
