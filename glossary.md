# Glossary — Group 21

One canonical term per concept, for the paper, the slides and the speaker notes. Created 16/11/2026 (Claude, on Lele's request) from `scaletta.md` §3.1–3.2 and `RULES.md`. Changes go in `registers/changelog.md`.

**How to use it:** in prose, use the term in the *Use* column. The variants under *Do not use* are either wrong or ambiguous. Code names (`like_this`) appear only in tables, equations and notes on the data.

## Design and samples

| Use | Meaning | Code | Do not use |
|---|---|---|---|
| **two-round startups** / **one-round startups** | Startups that did / did not close a second VC round by 30 June 2022 | `two_rounds` = 1 / 0 (R in equations) | "survivors", "successful startups", "refinanced firms" (the last one is fine only once, as a definition) |
| **VC round** | A completed, dated Seed, Early Stage or Later Stage VC deal; same-day deals of one company merged | — | "funding round" for angel, grant, debt or accelerator deals (they are not VC rounds) |
| **full sample** | The 28,478 startups with a disclosed first VC round (15,518 two-round, 12,960 one-round) | — | "estimation sample" for this group (`construction.pdf` does, and it is superseded on this point) |
| **estimation sample** | The 9,263 startups whose five-year outcome window is fully observed (4,483 two-round, 4,780 one-round) | `full_window == 1` | "main sample", "final sample" |
| **valuation sample** | Two-round startups with both post-money valuations observed (7,574, per the scaletta; to be checked in the log) | — | — |
| **two-group design** | Keeping all startups and splitting them by `two_rounds`, instead of conditioning on round 2 | — | "treatment and control group" (nothing is assigned) |

## Key variables

| Use | Meaning | Code | Do not use |
|---|---|---|---|
| **gap** (first time: "the gap between the first and the second VC round") | Months between round 1 and round 2, entered as R × ln(1 + months) | `log_gap_r2` | "refinancing speed", "time to raise", "delay" (each implies a reading) |
| **long / short gap** | Higher / lower values of the gap | — | "slow / fast raisers" outside speaker notes; never "late" or "early" |
| **hype** | The sector's share of all VC dollars in the year of round 1, z-scored within the sector (2012–2022, seven sectors) | `heat` | "heat" in prose, "hotness", "market sentiment" |
| **hot / cold market** | Hype at +1 / −1 SD (in models and margins); terciles only in figures, and say so | — | Mixing the SD and the tercile meanings on one slide |
| **past-only hype**, **quarterly hype**, **hype index** | Robustness measures of hype | `heat_past`, `heat_quarter`, `hype_index_l` | Presenting any of them as the main measure |
| **exit** | The first IPO or acquisition | — | "success" (exit ≠ success for the founder) |
| **exit within five years** (main outcome) | Exit inside the five-year outcome window | `exit_5y` | "exit" alone when the main outcome is meant; `exit` (any time, no window) is robustness only |
| **failure** | PitchBook failure date inside the window | `failure_5y` | "death", "bankruptcy" (not all failures are bankruptcies) |
| **still private** | Neither exit nor failure inside the window: the third state | — | "no outcome" |
| **outcome window** | Five years (4 and 6 in robustness), opening at round 2 for two-round startups and at round 1 for one-round startups | — | "follow-up period" |
| **valuation step** | ln(post-money at round 2 / post-money at round 1) | — | "step-up" (ambiguous: also means the ratio), "return", "growth" (growth per year is a different quantity) |
| **round-1 controls** | Log round-1 amount, number of deals so far, age at round 1, lead-investor type (16 categories) | `log_round1_size`, `round1_number`, `startup_age_at_round1`, lead type | "pre-treatment controls" |
| **mediators** | Round-2 variables (size, valuation): used only in robustness and H3 | — | Calling them controls in the main model |

## Coefficients and methods

| Use | Meaning | Do not use |
|---|---|---|
| **β1** | Coefficient of the gap (`log_gap_r2`) in the exit model: tests H1 | — |
| **β3** | Coefficient of gap × hype: tests H2, the key hypothesis | "the interaction effect" (in a logit, the interaction effect is not the interaction coefficient, Ai & Norton 2003) |
| **ρ1** | Coefficient of `two_rounds` | Any reading as an effect: the group indicator uses information from after round 1 |
| **θ1, θ3** | Gap and gap × hype coefficients in the valuation-step model (H3) | — |
| **logit coefficient / odds ratio / AME (pp)** | Always say which one a number is; AME = average marginal effect, in percentage points | Bare numbers |
| **clustered SEs** (first time: "errors allowed to be correlated among startups funded in the same sector and year") | SEs clustered by sector × year of round 1 (41 clusters in the main exit models) | "robust SEs" for the clustered ones |
| **linear probability model (LPM)** | OLS on a 0/1 outcome, robustness | — |
| **look-ahead** | `two_rounds` is defined with information from after round 1 | "reverse causality" |
| **survivorship / conditioning on refinancing** | β1 and β3 describe only startups that reached round 2 | "selection bias" without saying which selection |
| **staging** | Financing a startup in successive rounds, with a refinancing decision at each | — |
| **real option / leash / signal extraction** | The three readings of the gap (scaletta §2.1, §2.3) | Mixing them in one sentence |

## Verdicts and causal language (RULES.md)

- Hypothesis verdicts use the paper's Table 13 wording only: **right sign, not significant** · **rejected, opposite sign** · **not supported**. Never "no effect" or "confirmed".
- About the gap or hype, never write *effect, impact, causes, leads to, reduces, increases, drives*. Write **is associated with**, **goes with**.
- "Stable in sign" across hype measures, not "stable": with past-only hype β3 is significant (log L2584).
