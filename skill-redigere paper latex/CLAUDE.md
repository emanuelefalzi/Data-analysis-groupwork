# Redigere paper LaTeX — memoria di progetto

Regole sempre attive per ogni sessione e ogni agente che lavora in questa cartella. Valgono
**in aggiunta** a `../RULES.md` (binding per la repo: nomi, advisor mode, fonti dei numeri,
solo associazioni, decisioni del gruppo). Il processo fase per fase sta in `PROCESSO.md`.

## Cos'è

La pipeline che trasforma `../scaletta.md` nel **paper finale del Group 21 in LaTeX**: corpo di
**massimo 20 pagine** con **tutte le 21 figure e le 14 tabelle del paper v4**, poi References (da
`../fonti/fonti.bib`), Appendix A (già scritta in `../5. paper e documentazione di percorso/`) e
Appendix B (floats `appendice` di `input/piano.md`: Tables B1–B4, Figures B1–B3, dal 23/11), fuori conteggio. PDF: `../5. paper e documentazione di percorso/paper_group21_v5.pdf`.
Deriva da `../skill-redigere essay/` (la pipeline della tesi di Lele, ridotta), con tre
differenze: l'uscita è LaTeX e non Word; le fonti sono già state ristrette e verificate (le tesi
della scaletta sono vincolanti); c'è un **budget di pagine** che comprende i floats.

**Si lancia con un prompt solo, da qualunque computer: «lancia redigere paper» → `ROUTINE.md`.**

## La regola sovrana

Il testo non contiene alcuna affermazione che non sia già presente, esplicitamente o come
conseguenza diretta, nel **Content** della sua sezione della scaletta, nei suoi **Numbers (log)**,
nell'**estrazione validata** delle sue fonti o nelle **celle dei suoi floats**. Tutto il resto si
dichiara con `[[GAP: …]]` e si porta al gruppo. **Un buco dichiarato vale infinitamente più di un
buco riempito bene.** Nessun agente inventa fonti, numeri, date o fatti.

## Le regole che si rompono più spesso

1. **Si cita solo una fonte del blocco Sources della sezione**, presente in `fonti.bib`.
2. **Alla fonte si attribuisce solo la sua tesi nella scaletta** (dal 16/11 tutte ristrette sul
   txt). L'estrazione del lettore in `routine validazione fonti/tabella.csv` è contesto, non
   materiale. Il claim si restringe, mai si allarga.
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

`input/piano.md` (pagine per sezione; floats = tutti quelli del paper v4) l'ha deciso Claude su
mandato di Lele (17/11) e si cambia solo per stare nelle 20 pagine, riducendo la prosa. `latex/main.tex` e `latex/preambolo.tex` sono del
gruppo. Le scelte di contenuto restano in `scaletta.md`, che questa pipeline legge e non modifica.

## Modelli

**Ogni subagent con `model: "sonnet"` esplicito nella chiamata** (RULES.md). Se la sessione parte
dalla radice della repo, gli agenti di `.claude/agents/` di questa cartella non sono caricati:
si usa un subagent generico e gli si passa il testo del file dell'agente come istruzioni.

## Trappole operative

- Script con `python3` e percorsi assoluti, mai `cd` nella cartella. La radice la trovano da soli.
- `build/`, `latex/gen/`, `latex/figures/` sono **derivati**: si rigenerano, non si correggono a
  mano. Le correzioni vanno alla fonte (scaletta, piano, DRAFT della sezione, do-file).
- Serve solo Python 3 (libreria standard) e una distribuzione LaTeX con `pdflatex`. biber e
  biblatex-apa sono facoltativi (senza, natbib + bibtex). Niente LibreOffice, niente latexmk:
  gli RTF si leggono in Python (`tools/rtf_tabelle.py`). Installazione per sistema: `ROUTINE.md`.
- Il DRAFT è testo semplice con token: niente comandi LaTeX. Le conversioni le fa `assemble.py`.

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Scaletta (contratto del testo) | `../scaletta.md` → `build/sezioni.json` |
| Piano pagine e floats | `input/piano.md` (`tools/piano.py`) |
| Appendix A (già scritta) | `../5. paper e documentazione di percorso/appendix A - dataset construction.md` |
| Glossario (termini vincolanti) | `../glossary.md` |
| Contesto del lettore delle fonti | `../routine validazione fonti/tabella.csv` |
| Bibliografia | `../fonti/fonti.bib` |
| Figure, tabelle del do-file | `../4. risultati/figures.zip`, `RQ1_tables.doc`, `RQ1_tables_not_in_log_checks.rtf` → `build/` |
| Tabelle testuali (T1–T4, T7, T13, T14), una fonte per cella | `../4. risultati/tables testuali/<id>.md` → `tools/tabelle_testo.py` → `<id>.tex` + `tracciabilita.md` |
| Figura 1 (schema TikZ) | `latex/testo/F1.tex` |
| Sezioni scritte (DRAFT + LEDGER) | `sezioni/<id>.md` |
| Report dei controlli | `reports/` |
| Sorgente LaTeX | `latex/main.tex`, `latex/preambolo.tex` (del gruppo), `latex/gen/` (generato) |
| PDF | `../5. paper e documentazione di percorso/paper_group21_v5.pdf` |

Routine a un prompt: `ROUTINE.md`. Skill (solo se la sessione parte da questa cartella): `/paper-avvio`, `/paper-floats`, `/paper-appendice`, `/paper-scrivi`, `/paper-controlla`,
`/paper-latex`, `/paper-stato`. Agenti: `paper-writer`, `paper-claim-auditor` (più `fix-applier` e
`prose-auditor` di `../skill-redigere essay/`).
