# Fundraising speed, market hype and startup exit (Group 21)

Group project for **21072 Data Analysis Module I (Data Lab for Entrepreneurship)**, Bocconi University, 2026/27.

**Research question.** Is the time between a startup's first and second VC round associated with its probability of exit, and does this association differ between hot and cold funding markets?

**Data.** PitchBook course sample: US startups founded 2012–2019. We keep 28,478 startups with a disclosed first VC round. 15,518 raised a second round; 12,960 did not.

**Deliverable.** A slide deck of about 25 minutes (no written report; code is optional). Final presentations run 27/11–04/12/2026.

> Working with Claude or another AI? Read **[`RULES.md`](RULES.md)** first. `CLAUDE.md` loads it automatically in Claude Code.

## Repository map

```
dataset.py                      raw PitchBook files -> dataset (v2)
dataset.dta                     the dataset: 28,478 startups x 57 variables
rq1_two_group_analysis_v2.do    main Stata analysis (descriptives, models, figures, tables)
rq1_addon_extra_controls.do     robustness: team and lead-investor-age controls
regression_analysis.txt         Stata log of the do-file (15/11/2026): source of every number
RQ1_tables.doc                  Word/RTF tables from the do-file
paper_group21.pdf               group paper v4 (15/11/2026): the base for the deck
construction.pdf                how the dataset is built, plus every variable with its role
main_important_stuff_ig.docx    early notes on cleaning and literature (partly outdated)
registers/                      results (R-xx), inferences (I-xx), open points
RULES.md                        rules for members and their AIs
CLAUDE.md, .claude/             Claude Code configuration
```

## Pipeline

1. **Build the dataset (Python, pandas).** Put the raw PitchBook files from Blackboard in `data/`: `pitchbook_course.dta`, `Deal.csv`, `DealInvestorRelation.csv` and `Investor.csv`. Then run:
   ```bash
   python dataset.py
   ```
   It writes `output/rq1_two_group_dataset_v2.dta` and `.csv`, which is the file in this repo as `dataset.dta`.
2. **Run the analysis (Stata 17).** The do-file opens `group_21_dataset.dta`, so first copy `dataset.dta` under that name into the Stata working directory. It needs `esttab` (estout) and `coefplot`. The add-on also needs `pitchbook_course.dta` in the same folder. Outputs: `regression_analysis.log`, `RQ1_tables.rtf` and `figures/*.png`.

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

## Status (16/11/2026)

- Dataset v2, do-file, log and paper v4 are done.
- **Next:** the slide outline (`slide outline.md`), built from paper v4. See `registers/open points.md` for what is still unresolved.
