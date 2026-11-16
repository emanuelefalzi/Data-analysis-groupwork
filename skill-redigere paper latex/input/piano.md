# Piano del paper — pagine e floats

> **Stato: PROPOSTA di Claude (16/11/2026), da decidere nel gruppo.** Niente qui è approvato.
> `tools/piano.py` legge le due tabelle qui sotto (non cambiare i nomi delle colonne).
> Paper v4: 34 pagine, 21 figure, 14 tabelle. Il corpo qui deve stare in **20 pagine**:
> references e Appendix A sono fuori conteggio. Quindi la maggior parte dei floats esce.

## Sezioni

`pagine` = pagine di corpo assegnate alla sezione, floats compresi. Le parole obiettivo le
calcola lo script: (pagine − spazio dei floats della sezione) × `parole_per_pagina`.
Una sezione-cappello (2, 5, 6) ha solo il paragrafo d'apertura.

| id | pagine | note |
|---|---|---|
| abstract | 0.3 | 150 parole circa, sotto il titolo |
| 1 | 1.0 | |
| 2 | 0.1 | apertura: una frase + rimando alla tabella delle ipotesi |
| 2.1 | 0.9 | |
| 2.2 | 0.6 | |
| 2.3 | 0.8 | |
| 2.4 | 0.6 | |
| 2.5 | 0.7 | |
| 3.1 | 0.7 | |
| 3.2 | 0.9 | |
| 3.3 | 2.0 | qui stanno 4 floats |
| 4.1 | 0.9 | |
| 4.2 | 0.4 | |
| 4.3 | 0.5 | |
| 5 | 0.5 | apertura: come si leggono i coefficienti |
| 5.1 | 1.8 | |
| 5.2 | 1.4 | |
| 5.3 | 1.2 | |
| 5.4 | 1.0 | |
| 5.5 | 0.8 | |
| 5.6 | 0.5 | |
| 6 | 0.1 | apertura |
| 6.1 | 0.5 | |
| 6.2 | 0.3 | |
| 6.3 | 0.4 | |
| 6.4 | 0.4 | |
| 7 | 0.7 | |

## Floats

`dove`: `corpo` (entra nel PDF, nella sezione `sezione`), `escluso` (non entra). L'appendice
ospita **solo** la costruzione del dataset (decisione di Lele, 16/11), quindi nessun float va
in appendice. `altezza` = frazione di pagina stimata (serve al budget prima di compilare; dopo
la compilazione conta il PDF). `affianca`: due figure con lo stesso valore vanno in una riga
sola, mezza larghezza ciascuna (risparmia circa 0.2 pagine a coppia).

Le tabelle `t1`–`t6` sono quelle di `RQ1_tables.doc` (do-file), in ordine. `tools/floats.py`
le converte in LaTeX in forma compatta: righe chiave, i 16 dummy del lead investor e i controlli
fissi diventano righe «Yes». Le tabelle `x*` non esistono nel do-file: sono tabelle di testo
del paper v4 (contenuto dalla scaletta), da scrivere in `latex/tabelle-testo/<id>.tex`.

| id | tipo | file | dove | sezione | altezza | affianca | didascalia | paper v4 |
|---|---|---|---|---|---|---|---|---|
| x1 | tabella-testo | latex/tabelle-testo/x1.tex | corpo | 2 | 0.35 | | The hypotheses and the competing predictions | Table 1 |
| x3 | tabella-testo | latex/tabelle-testo/x3.tex | corpo | 3.1 | 0.25 | | Sample construction | Table 3 |
| t1 | tabella | t1 | corpo | 3.3 | 0.25 | | Descriptive statistics by group (estimation sample) | Table 5 |
| d1 | figura | d1_gap_histogram.png | corpo | 3.3 | 0.40 | A | Months between rounds 1 and 2 | Fig. 2 |
| d2 | figura | d2_startups_by_year.png | corpo | 3.3 | 0.40 | A | Startups by year of round 1 and group | Fig. 3 |
| d3 | figura | d3_hype_by_sector.png | corpo | 3.3 | 0.40 | | Hype at round 1 by sector and year | Fig. 4 |
| d4 | figura | d4_outcomes_by_sector.png | escluso | 3.3 | 0.40 | | Exit and failure within 5 years by sector | Fig. 5 |
| d5 | figura | d5_exit_by_group_hype.png | escluso | 3.3 | 0.40 | | Exit within 5 years by group and market hype | Fig. 6 |
| d6 | figura | d6_exit_by_gap_quintile.png | escluso | 3.3 | 0.40 | | Exit within 5 years by gap quintile | Fig. 7 |
| d7 | figura | d7_round1_size.png | escluso | 3.3 | 0.40 | | Round-1 size by group | Fig. 9 |
| d8 | figura | d8_exit_by_lead_type.png | escluso | 3.3 | 0.40 | | Exit within 5 years by lead-investor type | Fig. 10 |
| t2 | tabella | t2 | corpo | 5.1 | 0.45 | | Time between rounds, hype and exit within 5 years | Table 6 |
| m1 | figura | m1_exit_effect_by_hype.png | escluso | 5.1 | 0.40 | | Marginal effect of ln gap on exit, by market hype | Fig. 11 |
| m2 | figura | m2_exit_by_gap.png | corpo | 5.1 | 0.40 | | Predicted probability of exit by months between rounds | Fig. 12 |
| m3 | figura | m3_exit_by_group.png | escluso | 5.1 | 0.40 | | Predicted probability of exit by group and market hype | Fig. 13 |
| m4 | figura | m4_exit_coefficients.png | escluso | 5.1 | 0.45 | | Coefficients of the main exit model | Fig. 14 |
| t3 | tabella | t3 | corpo | 5.2 | 0.40 | | Time between rounds, hype and failure within 5 years | Table 8 |
| m5 | figura | m5_failure_effect_by_hype.png | escluso | 5.2 | 0.40 | | Marginal effect of ln gap on failure, by market hype | Fig. 15 |
| m6 | figura | m6_failure_by_gap.png | corpo | 5.2 | 0.40 | | Predicted probability of failure by months between rounds | Fig. 16 |
| t6 | tabella | t6 | corpo | 5.3 | 0.35 | | Time between rounds and the valuation step (two-round startups) | Table 9 |
| m9 | figura | m9_valuation_by_gap.png | corpo | 5.3 | 0.40 | | Valuation step by months between rounds | Fig. 18 |
| t4 | tabella | t4 | escluso | 5.4 | 0.45 | | Sensitivity to the outcome window (logit) | Table 10 |
| t5 | tabella | t5 | corpo | 5.4 | 0.45 | | Robustness of the exit model | Table 11 |
| m7 | figura | m7_windows_exit.png | escluso | 5.4 | 0.40 | B | β1 and β3 across outcome windows: exit | Fig. 20 |
| m8 | figura | m8_windows_failure.png | escluso | 5.4 | 0.40 | B | β1 and β3 across outcome windows: failure | Fig. 21 |
| x13 | tabella-testo | latex/tabelle-testo/x13.tex | corpo | 7 | 0.30 | | Summary of the hypotheses | Table 13 |

## Decisioni aperte (da portare al gruppo)

- **P1.** Figura 8 del paper (exit / failure / still private per quintile di gap) è, per la
  scaletta (3.3), la più informativa, ma il do-file non la esporta: non è in `figures.zip`.
  O si esporta dal do-file, o 3.3 la descrive a parole senza numeri non tracciabili.
- **P2.** La scaletta 3.3 e 5.1 propone di spostare figure in appendice. Con l'appendice
  riservata al dataset, quelle figure qui sono `escluso`. Confermare.
- **P3.** Tabelle di testo (x1, x3, x13): contenuto preso dalla scaletta e dal paper v4. Le
  scrive Claude in `latex/tabelle-testo/`, il gruppo le approva prima dell'assemblaggio.
- **P4.** Didascalie delle figure: prese dai titoli del paper v4 dove la corrispondenza
  file → figura è chiara [Likely]; m9 e d7 da verificare guardando il PNG.
