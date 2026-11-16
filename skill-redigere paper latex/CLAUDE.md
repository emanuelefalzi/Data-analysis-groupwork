# Redigere paper LaTeX — memoria di progetto

Regole sempre attive per ogni sessione e ogni agente che lavora in questa cartella. Valgono
**in aggiunta** a `../RULES.md` (binding per la repo: nomi, advisor mode, fonti dei numeri,
solo associazioni, decisioni del gruppo). Il processo fase per fase sta in `PROCESSO.md`.

## Cos'è

La pipeline che trasforma `../scaletta.md` nel **paper finale del Group 21 in LaTeX**: corpo di
**massimo 20 pagine** con figure e tabelle dentro, poi References (da `../fonti/fonti.bib`) e
Appendix A (costruzione di `dataset.dta`), fuori conteggio. Deriva da `../skill-redigere essay/`
(la pipeline della tesi di Lele, ridotta), con tre differenze: l'uscita è LaTeX e non Word;
la verifica delle fonti è già fatta dalla `../routine validazione fonti/`; c'è un **budget di
pagine** che comprende i floats.

## La regola sovrana

Il testo non contiene alcuna affermazione che non sia già presente, esplicitamente o come
conseguenza diretta, nel **Content** della sua sezione della scaletta, nei suoi **Numbers (log)**,
nell'**estrazione validata** delle sue fonti o nelle **celle dei suoi floats**. Tutto il resto si
dichiara con `[[GAP: …]]` e si porta al gruppo. **Un buco dichiarato vale infinitamente più di un
buco riempito bene.** Nessun agente inventa fonti, numeri, date o fatti.

## Le regole che si rompono più spesso

1. **Si cita solo una fonte validata per quella sezione**: chiave nel blocco Sources della
   sezione, presente in `fonti.bib`, con esito `usabile` o `da riformulare` in
   `routine validazione fonti/tabella.csv` per quella stessa sezione.
2. **Per «da riformulare» vale l'estrazione del lettore, non la tesi della scaletta.** Il claim
   si restringe, mai si allarga.
3. **I numeri vengono dal log o dalle tabelle del do-file** (RULES.md). Un numero che non sta nel
   materiale della sezione è un HIGH di `verifica.py`.
4. **Solo associazioni**, verdetti con le parole del paper, ρ1 non è un effetto (RULES.md).
5. **Un numero in un float non si ripete nel testo**: si richiama il float e si citano due o tre
   celle. Ogni float del corpo ha **una sola sezione di casa** ed è richiamato lì.
6. **Il connettivo trasporta l'attribuzione**: niente thus / therefore / accordingly / «, which» /
   «;» subito dopo una citazione. Prova: togli la citazione e rileggi la frase dopo.
7. **Tagliare affermazioni o floats è una decisione del gruppo.** Il limite di 20 pagine si
   rispetta proponendo opzioni, non tagliando in silenzio.

## Decisioni da non prendere da soli

`input/piano.md` (pagine per sezione e quali floats entrano) e `input/appendice-A.md` sono
**proposte** finché il gruppo non le approva. `latex/main.tex` e `latex/preambolo.tex` sono del
gruppo. Le scelte di contenuto restano in `scaletta.md`, che questa pipeline legge e non modifica.

## Modelli

**Ogni subagent con `model: "sonnet"` esplicito nella chiamata** (RULES.md). Se la sessione parte
dalla radice della repo, gli agenti di `.claude/agents/` di questa cartella non sono caricati:
si usa un subagent generico e gli si passa il testo del file dell'agente come istruzioni.

## Trappole operative

- Script con `python3` e percorsi assoluti, mai `cd` nella cartella. La radice la trovano da soli.
- `build/`, `latex/gen/`, `latex/figures/` sono **derivati**: si rigenerano, non si correggono a
  mano. Le correzioni vanno alla fonte (scaletta, piano, DRAFT della sezione, do-file).
- Serve LaTeX con biber (`texlive-latex-extra`, `texlive-bibtex-extra`, `biber`, `latexmk`,
  `lmodern`) e LibreOffice (`soffice`) per leggere `RQ1_tables.doc`.
- Il DRAFT è testo semplice con token: niente comandi LaTeX. Le conversioni le fa `assemble.py`.

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Scaletta (contratto del testo) | `../scaletta.md` → `build/sezioni.json` |
| Piano pagine e floats | `input/piano.md` (`tools/piano.py`) |
| Contratto dell'appendice | `input/appendice-A.md` |
| Fonti validate | `../routine validazione fonti/tabella.csv` |
| Bibliografia | `../fonti/fonti.bib` |
| Figure, tabelle del do-file | `../4. risultati/figures.zip`, `../4. risultati/RQ1_tables.doc` → `build/` |
| Tabelle di testo | `latex/tabelle-testo/<id>.tex` |
| Sezioni scritte (DRAFT + LEDGER) | `sezioni/<id>.md` |
| Report dei controlli | `reports/` |
| Sorgente LaTeX | `latex/main.tex`, `latex/preambolo.tex` (del gruppo), `latex/gen/` (generato) |
| PDF | `out/paper.pdf` |

Skill: `/paper-avvio`, `/paper-floats`, `/paper-appendice`, `/paper-scrivi`, `/paper-controlla`,
`/paper-latex`, `/paper-stato`. Agenti: `paper-writer`, `paper-claim-auditor` (più `fix-applier` e
`prose-auditor` di `../skill-redigere essay/`).
