# Contesto per ChatGPT — paper v5 del Group 21 (23/11/2026)

Cartella di partenza per i prompt manuali della routine «redigere paper» (Lele, 23/11: Codex fuori limite). ChatGPT legge da qui; non scrive nella repo.

| File | Cosa |
|---|---|
| `ctx/<id>.md` | Il materiale di ogni sezione, output di `tools/ctx.py <id>`: è tutto e solo ciò che il writer può usare |
| `regole-aggiuntive.md` | Regole per i writer aggiunte dopo la sezione pilota 5.1 |
| `rilievi/<id>.md` | Rilievi degli audit dei claim da correggere nelle riscritture |
| `../.claude/agents/paper-writer.md` | Istruzioni complete del writer |
| `../sezioni/<id>.md` | Versioni attuali delle sezioni (DRAFT + LEDGER) |
| `../../scaletta.md`, `../../3. stata/regression_analysis.log`, `../../fonti/fonti.bib`, `../input/piano.md` | Fonti a monte del contesto (scaletta, log Stata, bibliografia, piano): servono solo per controllare, il materiale vincolante è `ctx/` |

Ordine dei prompt: 01 (6.2) → 02 (6.3) → 03 (6.4) → 04 (7) → 15 (abstract) nella stessa chat; 05–14 riscritture indipendenti (10–14 facoltative).
