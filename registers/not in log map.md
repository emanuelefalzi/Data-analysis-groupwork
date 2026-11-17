# Paper numbers not in the main log → block of `rq1_addon_not_in_log_checks.do`

Created 17/11/2026 (Claude for Lele). Log lines filled 17/11 from `4. risultati/not_in_log_checks.txt` (run by Lele 17/11); numbers moved to `registers/results register.md` (rule: the log wins over the paper; any difference goes to `registers/open points.md`).

The **Python check** column comes from a pandas/statsmodels rerun on `dataset.dta` and the raw PitchBook files, done on 17/11 to test the code's logic before the Stata run. **It is not a source** and must not be cited: it only says what the Stata log should show. If Stata gives something else, stop and look for the reason.

| Paper number (v4) | What it is | Do-file block | Python check (not a source) | Log line |
|---|---|---|---|---|
| Table 12: exit β1 = −0.100 (both columns), β3 = −0.035 | logit coefficients of `log_gap_r2` and `log_gap_r2 × heat`, startups with founder data | A | not rerun || L287, L290 (same sample); L472, L475 (+ extra): −0.100 / −0.035 both |
| Table 12: failure β1 −0.231 → −0.229 | logit coefficient of `log_gap_r2` | A | not rerun || L643 (−0.231), L809 (−0.229) |
| Table 12: young lead −0.334 (odds ratio 0.72), AI term −0.607 on failure | logit coefficients; odds ratio printed by `display` | A | not rerun || L587 (−0.334), L975 (OR 0.716), L923 (AI −0.607) |
| Table 12: N 7,591 (exit) and 7,685 (failure), 41 clusters | estimation samples | A | 7,719 startups with founder data before Stata drops perfect predictors || L270, L455 (7,591); L626, L792 (7,685); 41 clusters L275; 7,719 with founder data L200 |
| Figure 8: 14 startups with both exit and failure in the window | count | B | 14 || L997–998: 14 |
| Figure 8: exit 21–24%, failure 14% → 9%, still private 64% → 69%, about 895 per quintile | raw shares by `gap_q` | B | exit 0.21–0.24; failure 0.142 → 0.094; still private 0.637 → 0.692 (Q4 0.631); 896–897 per quintile || L1029–1053: exit 0.211–0.237; failure 0.141 → 0.094; private 0.637 → 0.692; 893–902 per quintile |
| Figure 8: one round 16% / 32% / 53% | raw shares | B | 0.156 / 0.315 / 0.529 (N 4,780) || L1051–1052: 0.156 / 0.315 / 0.529 |
| Figure 17: N = 4,483 | two-round startups, 5-year sample | C | **4,482**: one two-round startup has a negative age, set to missing by the main do-file || L1087: 4,482 |
| Figure 17: slope failure −0.030, exit −0.011 | OLS slope of residualised outcome on residualised ln gap (FWL) | C | failure −0.0304, exit −0.0112: the −0.030 **is** the binned slope; it equals β3 of the failure model (main log L1308) only by coincidence (see open point 16d) || L1121 (exit −0.0112), L1140 (failure −0.0304); L1391–1405 FWL check |
| Figure 19: N = 7,514 | two-round startups with both post-money values and gap ≥ 1 month | D | 7,514 || L1521: 7,514 |
| Figure 19: total step 1.06–1.08 (Q1–Q4), 1.18 (Q5) | mean ln(V2/V1) by gap quintile | D | 1.063, 1.083, 1.075, 1.063, 1.183 || L1552–1564: 1.063, 1.083, 1.075, 1.063, 1.183 |
| Figure 19: median per year 1.89 (Q1, gap 7 months) → 0.36 (Q5, 35 months) | median ln(V2/V1) / gap in years; median gap | D | 1.885 (6.8 months) → 0.363 (35.0 months) || L1568–1580: 1.885 → 0.363; L1536–1548 gap 6.77 → 34.95 months |
| §5.4: sector × quarter hype, 149 clusters | β3, p | E1 | β3 −0.036, p ≈ 0.41, 149 clusters || L1960: −0.036, p 0.405; 149 clusters L1945 |
| §5.4: industry group × year hype, 42 groups, 191 clusters | β3, p | E2a | β3 −0.070, p ≈ 0.28, 190 clusters (one startup has no group hype); 40 groups in the dataset, 38 in the 5-year sample || L2368: −0.070, p 0.280; 190 clusters L2353; 40 / 38 groups L2289–2294 |
| §5.4: industry group × quarter hype, 575 clusters | β3, p | E2b / E2c | **E2b** (same rule as `heat_quarter`, 2013–19 base): β3 −0.078, p ≈ 0.09, **outside** the paper's range (−0.033 to −0.071, p 0.28–0.44). **E2c** (all-quarter base): β3 −0.057, p ≈ 0.37. 570 clusters. The paper does not say which base it used || L2554 (E2b): −0.078, p 0.090; L2740 (E2c): −0.057, p 0.368; 570 clusters L2539 — open point 21 |
| §5.4: β3 between −0.033 and −0.071, p 0.28–0.44 | range over E1, E2a, E2b | E1, E2 | see the three rows above || L3579–3612 (summary table) |
| §5.4: exit-share control, β3 −0.035, p = 0.62 | β3, p | E3 | β3 −0.031, p ≈ 0.66 with our definition (exits of all course companies in the startup's 5-year window). The paper's definition is not known exactly || L3082: −0.031, p 0.656 — open point 21 |
| §5.4: robust SEs, p of β3 0.36 vs 0.35 | p-value | E4 (vs E0) | 0.358 (robust) vs 0.346 (clustered; Stata log L541 says 0.344) || L3267: p 0.358 (E0 L1774: 0.344) |
| §5.4: 367 one-round startups out within 13 months; β1 −0.065, β3 −0.056 | count; coefficients | E5 | 367; β1 −0.065, β3 −0.056 || L3389–3390 (367); L3463 β3 −0.056, p 0.339; β1 −0.065 (L3604) |
| §5.4: VIF controls < 2; R, gap, interactions 10–19; < 2.5 centred | `estat vif` after the LPM | E6 | not rerun || L3774–3782 (10.1–18.7; controls 1.01–1.52 L3783 ff.); centred L4041 ff. (max 2.44); β unchanged L4157 |
| Table 7 note: AMEs use N = 4,444, not 4,483 | count of two-round startups used by `exit_h2` | F | 4,483 − 1 (missing age) − 38 (lead type or state that predicts no exit perfectly) = 4,444 || L4375 (4,444); L4396–4440 (4,483 − 1 − 38) |
| Consistency: `exit_h2` β1 −0.071, β3 −0.056, N 9,124, 41 clusters | must equal main log L521–541 | E0 and F | equal (β1 −0.0714, β3 −0.0557, N 9,124) || L1754–1774 and L4235–4258 equal main log L521–541; AMEs L4386–4394 = main L672–676: **passed** |
