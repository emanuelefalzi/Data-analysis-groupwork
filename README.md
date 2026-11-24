# Fundraising speed, market hype and startup exit (Group 21)

Group project for **21072 Data Analysis Module I (Data Lab for Entrepreneurship)**, Bocconi University, 2026/27.

**Research question.** Is the time between a startup's first and second VC round associated with its probability of exit, and does this association differ between hot and cold funding markets?

**Data.** PitchBook course sample: US startups founded 2012–2019. We keep 28,478 startups with a disclosed first VC round. 15,518 raised a second round; 12,960 did not.

**Deliverable.** A slide deck of about 25 minutes (no written report; code is optional). Final presentations run 27/11–04/12/2026.

> Working with Claude or another AI? Read **[`RULES.md`](RULES.md)** first. `CLAUDE.md` loads it automatically in Claude Code.

## Repository map

```
0. dati iniziali/               raw PitchBook files, zipped: pitchbook_course.dta, Deal.csv,
                                DealInvestorRelation.csv, Investor.csv
1. python/dataset.py            raw PitchBook files -> dataset (v2)
1. python/dataset_v4.py         v2 + 7 team and lead-age variables -> dataset v4 (used by the do-file)
2. dataset/dataset.dta          the dataset v2: 28,478 startups x 57 variables
2. dataset/dataset_v4.dta       dataset v4: the same 57 columns + 7 new (28,478 x 64); construction_v4.pdf
2. dataset/construction.pdf     how the dataset is built, plus every variable with its role
2. dataset/construction.txt     text of construction.pdf (pdftotext -layout), so tables can cite its lines
3. stata/group_21_regressions.do   main Stata analysis, one file (20/11/2026): sections 1-9 as v2,
                                10 extra controls, 11 figures n2-n4, 12 hype as raw VC share (TA),
                                13 non-linear gap (ln and months, squared), 14 correlation heatmap
                                (section 15, lagged hype, removed 24/11: group decision, not used)
3. stata/regression_analysis.log   its Stata log (23/11/2026): source of every number (every "log L…" points here)
3. stata/RQ1_tables.rtf         its RTF tables (23/11/2026)
4. risultati/regression_analysis.txt    Stata log of the 20/11 do-file: superseded 24/11 (same numbers,
                                line numbers 1 to 20 lower), kept for history
4. risultati/not_in_log_checks.txt      log of rq1_addon_not_in_log_checks.do (17/11; do-file removed 23/11):
                                Table 12, Figures 8, 17, 19, Section 5.4 checks, N of the AMEs
4. risultati/RQ1_tables.doc     Word/RTF Tables 1-12 from the do-file (9-12 new: raw VC share, squared gap)
4. risultati/figures.zip        figures of both do-files (new: c1 heatmap, q1-q2 non-linear gap, n2-n4)
4. risultati/tables testuali/   paper Tables 1, 2, 3, 4, 7, 13, 14: one source per cell, checked by
                                skill-redigere paper latex/tools/tabelle_testo.py (tracciabilita.md)
5. paper e documentazione di percorso/paper_group21.pdf   group paper v4 (15/11/2026): the base for the deck
5. paper e documentazione di percorso/main_important_stuff_ig.docx   early notes on cleaning and literature (partly outdated)
fonti/                          literature: PDFs, txt, fonti.bib, download fonti.md
registers/                      results (R-xx), inferences (I-xx), open points
scaletta.md                     draft outline of the deck
RULES.md                        rules for members and their AIs
CLAUDE.md, .claude/             Claude Code configuration
```

## Pipeline

1. **Build the dataset (Python, pandas).** The raw PitchBook files are zipped in `0. dati iniziali/` (`pitchbook_course.dta`, `Deal.csv`, `DealInvestorRelation.csv`, `Investor.csv`). The script still reads them from `data/`, so unzip them into a `data/` folder next to where you run it. Then run:
   ```bash
   python "1. python/dataset.py"
   ```
   It writes `output/rq1_two_group_dataset_v2.dta` and `.csv`, which is the file in this repo as `2. dataset/dataset.dta`.
2. **Run the analysis (Stata 17).** `group_21_regressions.do` opens `group_21_dataset.dta`, so first copy `2. dataset/dataset_v4.dta` under that name into the Stata working directory (section 10 needs the v4 team variables). It needs `esttab` (estout) and `coefplot`; section 14 installs `heatplot`, `palettes` and `colrspace` if missing. Outputs: `regression_analysis.log`, `RQ1_tables.rtf` (in the repo: `3. stata/`) and `figures/*.png` (in the repo: `4. risultati/figures.zip`).
3. **Checks not in the main log.** `rq1_addon_not_in_log_checks.do` was removed from the repo on 23/11/2026 and cannot be rerun from here (it is still in the git history, commit `732d21b~1`). Its outputs stay: `4. risultati/not_in_log_checks.txt`, `4. risultati/RQ1_tables_not_in_log_checks.rtf` and `figures/x1…x3_*.png`.

## Design in short

| Element | Variable | Definition |
|---|---|---|
| Group | `two_rounds` | 1 if a second VC round closed by 30/06/2022, else 0 |
| Gap | `log_gap_r2` | ln(1 + months between rounds 1 and 2) for two-round startups, 0 otherwise |
| Hype | `heat` | the sector's share of all VC $ in the year of round 1, z-scored within the sector |
| Main outcome | `exit_5y` | IPO or acquisition within 5 years of the window start (round 2, or round 1 if there is no round 2) |
| Other outcomes | `failure_5y`, `delta_v` | failure within 5 years; post-money valuation at round 2 / post-money at round 1 |
| Sample | `full_window == 1` | startups whose 5-year window is fully observed (9,263) |
| Controls | round 1 only | round-1 size, deal number, startup age, lead-investor type |
| Fixed effects / SE | | year-quarter, sector and state FE; SEs clustered by sector × year of round 1 |

Hypotheses: **H1** a longer gap goes with less exit; **H1b** a longer gap goes with more failure; **H2** (key) the gap penalty is weaker in hot markets; **H3** a longer gap goes with a smaller valuation step. The verdicts are in paper v4, Table 13. All results are associations, not causal effects.

## Status (23/11/2026)

- Dataset v4, do-file (sections 12-14 added on 20/11 after the TA's comments), log and paper v4 are done.
- `6. Presentazione/group21_deck_v9.pptx`: first full draft of the deck, new structure asked by the TA (per hypothesis: theory, model, main findings, robustness; then limitations to causality).
- **Next:** the deck outline `6. Presentazione/scalettaprese.md` and paper v5 (`skill-redigere paper latex/`). See `registers/open points.md` for what is still unresolved.
