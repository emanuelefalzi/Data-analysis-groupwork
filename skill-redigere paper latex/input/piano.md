# Piano del paper — pagine e floats

> **Deciso da Claude su mandato di Lele (17/11/2026).** Corpo ≤ 20 pagine; references e
> Appendix A fuori conteggio. Figure e tabelle: **tutte quelle del paper v4** (21 figure,
> 14 tabelle), stessi numeri e stesso ordine. Per stare nelle pagine le figure vanno a coppie
> nello stesso float (ognuna con il suo numero). `tools/piano.py` legge le due tabelle qui sotto
> (non cambiare i nomi delle colonne). Dopo la prima compilazione `tools/compila.py` dice le
> pagine vere: se sfora, si riduce la prosa (colonna `pagine`), non i floats.

## Sezioni

`pagine` = parole di prosa / `parole_per_pagina` + spazio dei floats della sezione.
Totale pianificato: 19.38 pagine (stima; la misura vera la da' compila.py).

| id | pagine | note |
|---|---|---|
| abstract | 0.23 | 150 parole + floats 0.00 |
| 1 | 0.58 | 370 parole + floats 0.00 |
| 2 | 0.53 | 40 parole + floats 0.47 |
| 2.1 | 0.42 | 270 parole + floats 0.00 |
| 2.2 | 0.28 | 180 parole + floats 0.00 |
| 2.3 | 0.34 | 220 parole + floats 0.00 |
| 2.4 | 0.28 | 180 parole + floats 0.00 |
| 2.5 | 0.80 | 170 parole + floats 0.53 |
| 3.1 | 0.56 | 120 parole + floats 0.37 |
| 3.2 | 1.21 | 240 parole + floats 0.84 |
| 3.3 | 2.89 | 300 parole + floats 2.42 |
| 4.1 | 0.36 | 230 parole + floats 0.00 |
| 4.2 | 0.19 | 120 parole + floats 0.00 |
| 4.3 | 0.23 | 150 parole + floats 0.00 |
| 5 | 0.22 | 140 parole + floats 0.00 |
| 5.1 | 2.08 | 300 parole + floats 1.61 |
| 5.2 | 1.71 | 200 parole + floats 1.40 |
| 5.3 | 1.14 | 170 parole + floats 0.87 |
| 5.4 | 2.47 | 170 parole + floats 2.20 |
| 5.5 | 1.34 | 290 parole + floats 0.89 |
| 5.6 | 0.27 | 170 parole + floats 0.00 |
| 6 | 0.06 | 40 parole + floats 0.00 |
| 6.1 | 0.28 | 180 parole + floats 0.00 |
| 6.2 | 0.16 | 100 parole + floats 0.00 |
| 6.3 | 0.22 | 140 parole + floats 0.00 |
| 6.4 | 0.22 | 140 parole + floats 0.00 |
| 7 | 0.31 | 200 parole + floats 0.00 |

## Floats

`tipo`: `tabella` (dal do-file: `<alias>:<numero>`, alias in `progetto.json` → `tabelle_rtf`),
`figura` (PNG di `figures.zip`), `tabella-testo` / `figura-testo` (LaTeX scritto a mano in
`latex/testo/`, dalla scaletta e dal log). `dove`: `corpo` | `escluso`. `affianca`: figure con
la stessa lettera nello stesso float, mezza larghezza, ognuna con il suo numero. `tieni`: righe
di lead-investor type da mostrare (le altre diventano una riga «Yes»), separate da `;`.

| id | tipo | file | dove | sezione | altezza | affianca | tieni | didascalia | paper v4 |
|---|---|---|---|---|---|---|---|---|---|
| T1 | tabella-testo | ../4. risultati/tables testuali/T1.tex | corpo | 2 | 0.47 |  |  | The hypotheses and the competing predictions | Table 1 |
| T2 | tabella-testo | ../4. risultati/tables testuali/T2.tex | corpo | 2.5 | 0.53 |  |  | Round-1 controls, the mechanism behind each, and the expected sign | Table 2 |
| T3 | tabella-testo | ../4. risultati/tables testuali/T3.tex | corpo | 3.1 | 0.37 |  |  | Sample construction | Table 3 |
| F1 | figura-testo | latex/testo/F1.tex | corpo | 3.2 | 0.37 |  |  | The two-group design and the timing of each variable | Fig. 1 |
| T4 | tabella-testo | ../4. risultati/tables testuali/T4.tex | corpo | 3.2 | 0.47 |  |  | Variable definitions | Table 4 |
| T5 | tabella | main:1 | corpo | 3.3 | 0.29 |  |  | Descriptive statistics by group, estimation sample (5-year window) | Table 5 |
| F2 | figura | d1_gap_histogram.png | corpo | 3.3 | 0.40 | A |  | Months between rounds 1 and 2 | Fig. 2 |
| F3 | figura | d2_startups_by_year.png | corpo | 3.3 | 0.40 | A |  | Startups by year of round 1 and group | Fig. 3 |
| F4 | figura | d3_hype_by_sector.png | corpo | 3.3 | 0.53 |  |  | Hype at round 1 by sector and year | Fig. 4 |
| F5 | figura | d4_outcomes_by_sector.png | corpo | 3.3 | 0.40 | B |  | Exit and failure within 5 years by sector | Fig. 5 |
| F6 | figura | d5_exit_by_group_hype.png | corpo | 3.3 | 0.40 | B |  | Exit within 5 years by group and market hype | Fig. 6 |
| F7 | figura | d6_exit_by_gap_quintile.png | corpo | 3.3 | 0.40 | C |  | Exit within 5 years by gap quintile, cold and hot markets | Fig. 7 |
| F8 | figura | x1_outcomes_by_gap_quintile.png | corpo | 3.3 | 0.40 | C |  | Exit, failure and still private within 5 years, by gap quintile | Fig. 8 |
| F9 | figura | d7_round1_size.png | corpo | 3.3 | 0.40 | D |  | Distribution of the round-1 amount by group | Fig. 9 |
| F10 | figura | d8_exit_by_lead_type.png | corpo | 3.3 | 0.40 | D |  | Exit within 5 years by lead-investor type | Fig. 10 |
| T6 | tabella | main:2 | corpo | 5.1 | 0.60 |  | Accelerator/Incubator; Angel Group; Corporate Venture Capital; Venture Capital | Time between rounds, hype and exit within 5 years | Table 6 |
| T7 | tabella-testo | ../4. risultati/tables testuali/T7.tex | corpo | 5.1 | 0.21 |  |  | Average marginal effect of ln gap on the probability of exit and failure (two-round startups) | Table 7 |
| F11 | figura | m1_exit_effect_by_hype.png | corpo | 5.1 | 0.40 | E |  | Marginal effect of ln gap on exit, by market hype | Fig. 11 |
| F12 | figura | m2_exit_by_gap.png | corpo | 5.1 | 0.40 | E |  | Predicted probability of exit by months between rounds, cold and hot markets | Fig. 12 |
| F13 | figura | m3_exit_by_group.png | corpo | 5.1 | 0.40 | G |  | Predicted probability of exit for one-round and two-round startups, by market hype | Fig. 13 |
| F14 | figura | m4_exit_coefficients.png | corpo | 5.1 | 0.40 | G |  | Coefficients of the main exit model | Fig. 14 |
| T8 | tabella | main:3 | corpo | 5.2 | 0.53 |  |  | Time between rounds, hype and failure within 5 years | Table 8 |
| F15 | figura | m5_failure_effect_by_hype.png | corpo | 5.2 | 0.40 | H |  | Marginal effect of ln gap on failure, by market hype | Fig. 15 |
| F16 | figura | m6_failure_by_gap.png | corpo | 5.2 | 0.40 | H |  | Predicted probability of failure by months between rounds, cold and hot markets | Fig. 16 |
| F17 | figura | x2_fwl_outcomes_by_gap.png | corpo | 5.2 | 0.47 |  |  | Exit and failure against ln gap, net of controls and fixed effects | Fig. 17 |
| T9 | tabella | main:6 | corpo | 5.3 | 0.47 |  | Accelerator/Incubator | Time between rounds and the valuation step (two-round startups) | Table 9 |
| F18 | figura | m9_valuation_by_gap.png | corpo | 5.3 | 0.40 | I |  | Predicted valuation step by months between rounds, cold and hot markets | Fig. 18 |
| F19 | figura | x3_valuation_step_by_gap_quintile.png | corpo | 5.3 | 0.40 | I |  | Valuation step from round 1 to round 2: total and per year, by gap quintile | Fig. 19 |
| T10 | tabella | main:4 | corpo | 5.4 | 0.60 |  |  | Sensitivity to the length of the outcome window (logit, H2 specification) | Table 10 |
| T11 | tabella | main:5 | corpo | 5.4 | 0.60 |  |  | Robustness of the exit model | Table 11 |
| T12 | tabella | checks:12 | corpo | 5.4 | 0.60 |  |  | Adding team and lead-investor-age controls (logit, H2 specification) | Table 12 |
| F20 | figura | m7_windows_exit.png | corpo | 5.4 | 0.40 | L |  | β1 and β3 across outcome windows: exit | Fig. 20 |
| F21 | figura | m8_windows_failure.png | corpo | 5.4 | 0.40 | L |  | β1 and β3 across outcome windows: failure | Fig. 21 |
| T13 | tabella-testo | ../4. risultati/tables testuali/T13.tex | corpo | 5.5 | 0.29 |  |  | Summary of the hypotheses | Table 13 |
| T14 | tabella-testo | ../4. risultati/tables testuali/T14.tex | corpo | 5.5 | 0.60 |  |  | Our estimates against the literature | Table 14 |
