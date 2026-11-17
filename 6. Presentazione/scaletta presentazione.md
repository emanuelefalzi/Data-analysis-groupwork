# Scaletta presentazione: the deck

**Group 21 · 21072 Data Analysis · final presentation, about 25 minutes · v1, 17/11/2026 (Lele)**

Derived from `scaletta.md` (v1, 16/11/2026), which stays the single source of truth for content, sources and numbers. This file holds **only what goes on the slides and what we say**. If a number here disagrees with `scaletta.md` or the registers, the Stata log wins (`4. risultati/regression_analysis.txt`, "log L…"; `4. risultati/not_in_log_checks.txt`, "add-on log L…").

**v1 status.** Each of the 21 slides plus 3 backup slides now has message, layout, on-slide text, visual, results and inferences (IDs from `registers/`), sources and a speech in points. Open points are marked ⚠ on the slide they belong to and summed up at the end.

## How each slide is written

```
### N · Claim title · SECTION · ⏱ time
Message      the one thing the audience remembers
Layout       how the slide is arranged
On slide     the only text that appears (besides the title)
Visual       figure / table, with its file
Results      R-xx (registers/results register.md) · Inferences: I-xx (approved only)
Sources      footer of the slide + literature with what it says
Speech       talking points, in order
⚠            open points (only if any)
```

## Rules for the whole deck

- **Titles are claims**, in English. **Associations only**: "goes with", "is associated with", never "effect / causes / leads to / reduces" for the gap or for hype.
- **Verdicts** use the wording of paper Table 13: H1 *right sign, not significant* · H1b *rejected, opposite sign* · H2 *not supported* · H3 *rejected, opposite sign*.
- **One message, one or two visuals per slide.** A number shown in a chart is not repeated in the slide text. Each result has **one home slide**; elsewhere only a pointer.
- **Every number** on a slide says what it is (odds ratio, average marginal effect in percentage points (pp), OLS coefficient), and the footer gives the sample and "SEs clustered by sector × year of round 1".
- **Words** as in `glossary.md`: *gap* (months between round 1 and round 2), *hype* (never `heat` on a slide), *two-round / one-round startups*, *estimation sample* (9,263), *valuation sample* (7,574).

## Visual style (proposal, to agree)

- White background, one sans-serif font, title at the top left as a full sentence, footer at the bottom left in small grey type: source + sample.
- **Fixed colours throughout:** two-round startups = dark blue, one-round = grey; hot market = orange, cold market = light blue; exit = green, failure = red, still private = grey. The colours of the Stata figures must be aligned to these, or the figures re-exported.
- Charts take at least 60% of the slide; at most three short lines of text next to them.
- **Paper figure → file** (`4. risultati/figures.zip`). This mapping follows the order of the do-file and the paper, [Likely]; check it visually before using: Fig. 2 `d1_gap_histogram`, Fig. 3 `d2_startups_by_year`, Fig. 4 `d3_hype_by_sector`, Fig. 6 `d5_exit_by_group_hype`, Fig. 8 `x1_outcomes_by_gap_quintile`, Fig. 10 `d8_exit_by_lead_type`, Fig. 11 `m1_exit_effect_by_hype`, Fig. 12 `m2_exit_by_gap`, Fig. 14 `m4_exit_coefficients`, Fig. 16 `m6_failure_by_gap`, Fig. 17 `x2_fwl_outcomes_by_gap`, Fig. 18 `m9_valuation_by_gap`, Fig. 19 `x3_valuation_step_by_gap_quintile`, Fig. 20–21 `m7_windows_exit`, `m8_windows_failure`.

## Timing

| Part | Slides | Time |
|---|---|---|
| A · Opening and motivation | 1–3 | 2:05 |
| B · Literature and hypotheses | 4–6 | 3:15 |
| C · Data and method | 7–10 | 4:20 |
| D · Results | 11–17 | 9:05 |
| E · Discussion, limits, conclusion | 18–21 | 4:10 |
| **Total** | **21** | **≈ 22:55**, about 2 minutes of buffer within 25 |

Results get a third of the time. Slide 13 (H2, the key hypothesis) gets the most.

---

## A · Opening and motivation

### 1 · Is a slow second VC round a bad sign? · TITLE · ⏱ 0:20

**Message:** what the talk is about, in one question.
**Layout:** title slide. Question as the title, subtitle below, group and course at the bottom.
**On slide:**
- *Time between VC rounds, exit and hot markets: evidence from US startups, 2012–2019*
- Group 21 · 21072 Data Analysis (Data Lab for Entrepreneurship) · Bocconi 2026/27 · member names
**Visual:** none, or a thin timeline line (round 1 → gap → round 2) as decoration.
**Results:** none · **Inferences:** none
**Sources:** none.
**Speech:**
- Who we are, in one line.
- "Today we ask whether waiting a long time for the second VC round is a warning sign."

### 2 · Two startups raise the same first round: one raises again in 6 months, the other in 24 · MOTIVATION · ⏱ 1:00

**Message:** the gap between round 1 and round 2 is one of the few signals an outsider can see, and it can be read in two opposite ways.
**Layout:** two parallel timelines, startup A and startup B. Same round-1 marker; round 2 at 6 months for A, at 24 months for B. A question mark at the end of each timeline (exit?).
**On slide:**
- VC arrives in stages: at each stage investors decide whether to refinance
- The time to round 2 is visible from outside
- Strength or distress?
**Visual:** custom diagram (to draw). The 6 and 24 months are **illustrative**, not data.
**Results:** none · **Inferences:** none
**Sources:** VC is staged and each stage is a refinancing decision (Gompers, 1995).
**Speech:**
- Imagine two startups with the same first round. One raises again after six months, the other after two years.
- Most people read the first as the winner. The investor saw progress fast.
- But a slow round can also mean the startup took time to build something that is then priced. We test which reading fits the data.
- Keep the two timelines in mind: we come back to them at the end.

⚠ The founder-side hook is a Claude proposal in `scaletta.md` §1 that the group has not approved. Keep or drop as a group.

### 3 · We ask whether the gap goes with exit, and whether hot markets change that · RESEARCH QUESTION · ⏱ 0:45

**Message:** the question has two parts: gap ↔ exit, and whether hype changes that link.
**Layout:** the research question in a large box at the centre; below it, three small icons with labels (gap · exit · market).
**On slide:**
- *Is the time between the first and the second VC round associated with the probability of exit, and does this association differ between hot and cold funding markets?*
- Gap: months between round 1 and round 2
- Exit: IPO or acquisition within five years
- Hot vs cold: the sector's share of VC dollars, relative to its own history
**Visual:** none (text slide with icons).
**Results:** none · **Inferences:** none
**Sources:** footer "PitchBook, US startups founded 2012–2019 (course extract)".
**Speech:**
- Read the question once, slowly.
- Stress "associated": we do not assign the gap at random, so we describe associations, not effects. We come back to this in the limits.
- Two parts: first the gap and exit; second, whether the link is different when capital is abundant.

---

## B · Literature and hypotheses

### 4 · Staging theory predicts opposite signs for the gap · LITERATURE · ⏱ 1:15

**Message:** theory does not agree on what a long gap means. That is why the question is open.
**Layout:** two columns facing each other. Left, "Slow = bad news" (green arrow down on exit). Right, "Fast = risky" (red arrow). A thin bar at the bottom: "Survivorship: who reaches round 2 is selected".
**On slide:**
- **Real option and learning:** investors refinance after good news, so a long gap is bad news
- **Staging as a leash:** short rounds for ventures that are hard to monitor, so a fast round can mark risk
- **Survivorship:** we see startups only when they raise again, so slow raisers that reach round 2 look safer
**Visual:** two-column diagram (to draw).
**Results:** none · **Inferences:** pointer to I-04 (home slide 18), only as a prediction here.
**Sources:**
- Staging gives the investor an option to abandon after new information (Bergemann and Hege, 2005; Dahiya and Ray, 2012).
- In learning models each period without good news lowers the investor's belief, so good projects are refinanced sooner (Bergemann and Hege, 2005).
- Rounds get shorter when agency and monitoring costs are higher (Gompers, 1995) and when the VC is far from the firm (Tian, 2011).
- Returns of private firms are observed only at financing events, so they are selected upward (Cochrane, 2005; Korteweg and Sorensen, 2010).
**Speech:**
- First view: VC is a real option. The investor waits for news; good news comes early, so a fast round is a good sign.
- Second view: the investor chooses round length. Short rounds are a leash for risky ventures. Then fast is not good, it is watched.
- Third, a selection point: we only see a startup's value when it raises again. Slow raisers who made it to round 2 have survived a longer test.
- So the sign of the gap is an empirical question.

⚠ The step "short rounds → riskier ventures" is our argument (I-04); the sources support only the first half. Say "we argue" aloud.

### 5 · In hot markets, a fast round may say less about the startup · LITERATURE · ⏱ 1:00

**Message:** when capital is abundant, rounds close fast for everyone, so speed may carry less information. That gives H2, and our opposite alternative.
**Layout:** split slide. Left half orange (hot market), right half light blue (cold market). In each half, one line on what a fast round and a slow round mean there.
**On slide:**
- VC supply moves in cycles: inflows raise prices, IPOs come in waves
- **H2 view:** in hot markets speed is cheap, so a slow round warns less
- **Our alternative (signal extraction):** in hot markets a slow round means investors chose not to fund, so it warns more
**Visual:** two-colour split (to draw).
**Results:** none · **Inferences:** none
**Sources:**
- Capital inflows into VC funds raise the prices of private deals (Gompers and Lerner, 2000).
- IPOs come in waves that follow market conditions (Pástor and Veronesi, 2005).
- Startups first funded in hot markets fail more often, but those that go public are valued higher (Nanda and Rhodes-Kropf, 2013).
- Early-stage VC deals fall sharply in recessions (Howell et al., 2020).
- Signal extraction is **our own argument**, not a literature result.
**Speech:**
- Funding markets are cyclical. In hot years money chases deals, and rounds close fast for everyone.
- If so, a fast round says less about the startup and a slow one should worry us less: that is H2.
- We also wrote down the opposite: in a hot market, if you still wait, investors chose not to fund you, so the wait says more.
- These two views predict opposite signs for the same coefficient.

⚠ Do not cite Nanda and Rhodes-Kropf (2017) or Townsend (2015) (decision D4, 16/11), although paper Table 1 still cites them. ⚠ Was the signal-extraction alternative written before or after the results? Say "stated before estimation" only if true (scaletta §2.3, Claude's additions).

### 6 · Four hypotheses, one key test · HYPOTHESES · ⏱ 1:00

**Message:** what we test, with the expected sign, and that H2 is the key one.
**Layout:** a 4-row table (slim version of paper Table 1): hypothesis · what it says · expected sign · competing view. The H2 row is highlighted with a frame and the label "key".
**On slide:**

| | Among two-round startups, a longer gap goes with… | Expected | Competing view |
|---|---|---|---|
| H1 | lower exit within 5 years | β1 < 0 | leash: ≥ 0 |
| H1b | higher failure within 5 years | > 0 | survivorship: < 0 |
| **H2 (key)** | a weaker exit penalty in hot markets | β3 > 0 | signal extraction: < 0 |
| H3 | a smaller valuation step from round 1 to round 2 | θ1 < 0 | progress is priced: > 0 |

**Visual:** the table above (no figure).
**Results:** none · **Inferences:** I-03 (progress priced, as a competing prediction; home slide 18).
**Sources:** footer "Hypotheses and sources: paper Table 1". Literature as on slides 4–5; H3: observed round-to-round returns are selected upward (Cochrane, 2005), so fast rounds should carry larger steps.
**Speech:**
- Four hypotheses, all about two-round startups: exit, failure, the hype interaction, the valuation step.
- H2 is the key one: does hype change the gap–exit link?
- For each one we also wrote the competing prediction, so the results can go either way without a story made up afterwards.
- On the slide we use Greek letters only as labels: β1 is the gap, β3 is gap × hype.

---

## C · Data and method

### 7 · From 57,751 startups to 9,263 with a full five-year window · DATA · ⏱ 0:50

**Message:** we keep every startup with a disclosed first round, then only those whose five-year window is fully observed.
**Layout:** horizontal funnel, three boxes from left to right, with the drop reason under each arrow. Under the last box, a bar split into two colours (two-round / one-round).
**On slide:**
- Course extract → at least one VC round, gap ≤ 10 years, no exit before round 1, disclosed round-1 amount → five-year window fully observed by 30 June 2022
- Undisclosed round-1 amounts dropped, not imputed
**Visual:** funnel 57,751 → 28,478 (15,518 two-round / 12,960 one-round) → 9,263 (4,483 / 4,780). To draw (paper Table 3).
**Results:** R-01, R-02, R-03, R-05, R-06 (R-04 only in speech, if asked).
**Sources:** footer "PitchBook course extract; sample steps: paper Table 3, `construction.pdf`; estimation sample: log L105–116".
**Speech:**
- We start from the course PitchBook extract of US startups founded 2012–2019.
- A VC round is a completed Seed, Early or Later Stage VC deal; same-day deals are merged.
- We drop startups with an undisclosed first-round amount, as suggested at the pitch, rather than guess it.
- To call a zero "no exit" we need the whole five-year window, so the estimation sample is 9,263 startups, about half with a second round.

⚠ R-01 (57,751) and R-04 (6,285 undisclosed) come from paper Table 3 and `construction.pdf`, not re-checked on the raw extract.

### 8 · We keep startups that never raised again, so we do not condition on round 2 · DESIGN · ⏱ 1:15

**Message:** the design compares two groups and measures the gap only where it exists. Everything else is dated at round 1.
**Layout:** paper Figure 1 (timing schematic) across the full width. Two labelled timelines: two-round startup (round 1 → gap → round 2 → five-year window) and one-round startup (round 1 → five-year window). A bracket under round 1: "controls, hype, fixed effects".
**On slide:**
- Two groups: two-round and one-round startups
- The gap enters only for two-round startups, as ln(1 + months)
- Controls and hype measured at round 1; round-2 variables left out
**Visual:** paper Figure 1 (a schematic; not in `figures.zip`, redraw it). Optional inset: gap histogram, Fig. 2 `d1_gap_histogram`.
**Results:** R-09 (mean gap 14.7 months, if the inset is used).
**Sources:** footer "Design: paper §3.2, Figure 1".
**Speech:**
- If we only kept startups with a second round, we would study survivors only. So we keep those that never raised again as a second group.
- The gap exists only for two-round startups. In the model it is the log of months, because the distribution has a long right tail.
- The outcome window starts at round 2 for two-round startups and at round 1 for the others.
- All controls are measured at round 1. Round-2 size or valuation could themselves be shaped by the gap, so they stay out.

### 9 · Hype is a sector's share of VC dollars, compared with its own history · VARIABLES · ⏱ 1:00

**Message:** hype measures whether a sector is hot relative to its own normal, not how big the sector is.
**Layout:** chart on the left (two thirds), a "how it is built" box on the right with three steps.
**On slide:**
- 1. Share of all US VC dollars going to the sector, in the year of round 1
- 2. Z-score within the sector (2012–2022)
- 3. Hot = +1 SD, cold = −1 SD
**Visual:** paper Figure 4, `d3_hype_by_sector` (hype by sector and year).
**Results:** R-14 (in speech only).
**Sources:** footer "Hype: sector share of VC dollars, z-scored within sector; PitchBook 2012–2022; paper Figure 4". Hot markets are measured through capital inflows in the literature too (Gompers and Lerner, 2000).
**Speech:**
- IT takes between 34% and 44% of VC dollars every year; Materials stays below 2.5%. A raw share would only tell us that IT is big.
- So we compare each sector with itself: +1 means one standard deviation above that sector's normal.
- With sector fixed effects in the model, H2 is identified by these ups and downs within each sector.
- Hot and cold in the results always mean +1 and −1 SD.

⚠ R-14 checked on `dataset.dta` (`sector_vc_share`, 2012–2022): IT 33.5–44.0%, Materials 0.5–2.4% (code run 17/11, not in log). Energy has one outlier year (2012: 13.8%), visible in the chart: be ready to explain it (very few deals recorded).

### 10 · A logit with interactions, read as changes in probability · METHOD · ⏱ 1:15

**Message:** one main model; we read its key terms as changes in the probability of exit, in hot vs cold markets.
**Layout:** a simplified equation at the top with three highlighted terms; below it, a 3-row "how to read" box.
**On slide:**
- Pr(exit within 5 years) = Λ( ρ1·two-round + **β1·ln gap** + β2·hype + **β3·ln gap × hype** + … + round-1 controls + fixed effects )
- **β1**: gap and exit at average hype · **β3**: how that slope changes per SD of hype
- Read as average marginal effects (AME, pp) in cold (−1) and hot (+1) markets, and their difference
- Controls: round-1 size, deal number, age, lead-investor type · fixed effects: year-quarter, sector, state · SEs clustered by sector × year of round 1 (41 clusters)
**Visual:** equation box + reading box (to draw). The full equation stays in the paper.
**Results:** R-47, R-48 (N and clusters in footer).
**Sources:**
- In a logit the interaction effect on the probability is not the interaction coefficient: it can differ in size and sign (Ai and Norton, 2003); best practice is to show it as marginal effects (Mize, 2019).
- Standard errors are allowed to be correlated among startups funded in the same sector and year (clustered SEs), the level at which hype is assigned (Abadie et al., 2023, our extension to hype).
- Logit, linear probability model and clustered SEs: course textbook (Hill, Griffiths and Lim, 2018).
- Footer: "Logit, N = 9,124 of 9,263 (cells that predict the outcome perfectly drop); 41 clusters; log L346, L351".
**Speech:**
- Our outcome is yes/no, so we use a logit.
- The coefficient that matters for H2 is β3, gap × hype. In a logit it lives in log-odds, so we translate into probabilities: how much does exit change with the gap in a cold market, in a hot market, and is the difference significant?
- We also run a linear probability model as a check: there the coefficient already is a probability.
- We do not interpret the two-round dummy ρ1: we will see why on the limits slide.

⚠ The course brain for 21072 does not exist yet (open point 7): cite the textbook without chapter numbers until checked.

---

## D · Results

### 11 · Startups that raise again exit more and fail far less · DESCRIPTIVES · ⏱ 0:50

**Message:** before any model, the two groups are very different. That is the scale for every number that follows.
**Layout:** one grouped bar chart: two pairs of bars (exit, failure), two-round dark blue vs one-round grey, values on the bars.
**On slide:**
- Raw five-year rates, no controls
- Both differences significant in t-tests (p < 0.001)
**Visual:** new chart from log L131–141 (exit 22.2% vs 15.6%; failure 12.4% vs 31.6%). To build; it does not exist among the figures.
**Results:** R-07, R-08 (R-11, R-12 in speech only).
**Sources:** footer "Estimation sample, N = 9,263; means and t-tests: log L131–196".
**Speech:**
- Two-round startups exit more and, above all, fail far less: about one in eight against almost one in three.
- They also raised larger first rounds and were younger at round 1.
- This is not a result about the gap; it is the backdrop. Keep 22% in mind: a 2-point change in exit is about a tenth of it.

### 12 · Across gap quintiles, exit is flat while failure falls · DESCRIPTIVES · ⏱ 1:00

**Message:** in the raw data, slow raisers do not exit more, they fail less and stay private more.
**Layout:** paper Figure 8 across the full width (stacked bars: exit / failure / still private, by gap quintile, plus a one-round bar for comparison). One line of text below.
**On slide:**
- Raw shares, no controls: exit, failure and still private are competing outcomes
**Visual:** paper Figure 8, `x1_outcomes_by_gap_quintile`.
**Results:** R-15.
**Sources:** footer "Two-round startups, estimation sample, gap quintiles (893–902 each); add-on log L1029–1053".
**Speech:**
- Five groups of two-round startups, from the fastest to the slowest second round.
- The exit share barely moves. Failure falls from the fastest to the slowest quintile; the share still private rises.
- So slow raisers are not exiting more; they are staying alive and private.
- These are raw shares; the models next check whether this holds once we control for round-1 differences.

⚠ The 14 startups with both outcomes are counted as exits (add-on log L997): say it only if asked.

### 13 · A longer gap is not significantly associated with exit, in hot or in cold markets · RESULTS H1, H2 · ⏱ 2:00

**Message:** H2, the key hypothesis, is not supported, and H1 has the right sign but is not significant. The data cannot distinguish a small exit penalty from none.
**Layout:** paper Figure 12 on the left (two thirds): predicted probability of exit by months between rounds, cold vs hot. On the right, a two-row verdict box.
**On slide:**
- **H2, gap × hype: not supported.** The sign is the opposite of H2 and not significant
- **H1, gap: right sign, not significant**
- In probabilities: hot − cold difference in the gap's AME not significant (p = 0.33)
**Visual:** paper Figure 12, `m2_exit_by_gap`. Backup: Fig. 11 `m1_exit_effect_by_hype` (AME by hype).
**Results:** R-16, R-17, R-18, R-19, R-20, R-21.
**Sources:** footer "Logit of exit within 5 years, N = 9,124; SEs clustered by sector × year of round 1 (41 clusters); log L358, L538–541, L657–703; AMEs on 4,444 two-round startups".
**Speech:**
- We start with H2, because it is the key one. If hype softened the gap penalty, the hot line would be flatter. It is not: if anything it is steeper, which is the opposite of H2, but it is not significant.
- In the cold market the predicted exit probability is flat at about 22% whatever the gap; in the hot market it goes from about 26% to 20%, and the bands overlap.
- The hot-minus-cold difference in marginal effects is about −1.9 points, with p = 0.33.
- H1: one log unit more gap, which is about 2.7 times as many months, goes with 8.5% lower odds of exit (odds ratio 0.915, p = 0.19). Right sign, not significant.
- The linear probability model tells the same story.
- So: not significant means we cannot tell a small penalty from none. It does not mean "no effect".

⚠ Paper Table 13 reports H1 from the model with interactions (β1 −0.071, p = 0.29); `scaletta.md` §5.1 uses the baseline model (−0.089, p = 0.188). The deck uses the baseline for H1 here. Choose one and use it on slides 13 and 18. ⚠ The Figure 12 grid is ln gap 1–4 (about 2 to 54 months): check the x-axis labels before quoting "months".

### 14 · A longer gap goes with less failure, not more · RESULTS H1b · ⏱ 1:30

**Message:** the strongest result: H1b is rejected with the opposite sign, in cold and hot markets alike.
**Layout:** paper Figure 16 on the left (predicted probability of failure by months between rounds, cold vs hot). On the right, the verdict and two numbers.
**On slide:**
- **H1b: rejected, opposite sign**
- Odds ratio 0.79 per log unit of gap (p = 0.005)
- About −1.9 pp over the interquartile range of the gap (about 8 to 19 months), against a mean failure rate of 12.4%
- Hype does not change it (p = 0.68)
**Visual:** paper Figure 16, `m6_failure_by_gap`. Backup: Fig. 17 `x2_fwl_outcomes_by_gap` (functional form, slide B2).
**Results:** R-26 (main), R-25, R-27, R-28, R-29.
**Sources:** footer "Logit of failure within 5 years, N = 9,235; SEs clustered by sector × year of round 1 (41 clusters); log L1305–1308, L1424–1467".
**Speech:**
- H1b said a long gap should go with more failure, because investors drop stalled ventures. We find the opposite.
- Each log unit of gap goes with about 21% lower odds of failure, significant at 1%.
- In probability: moving from a gap of 8 months to one of 19 months goes with about 2 points less failure, on a base of 12%, about 15% less in relative terms.
- The line has the same shape in hot and cold markets.
- Why this happens is on slide 18; what it does not mean is on slide 19.

⚠ Odds ratio 0.794 belongs to β1 = −0.231 (model with interactions, L1305); the baseline −0.241 gives 0.786 (open point 16). The slide uses the model with interactions, as in paper Table 13.

### 15 · Slower second rounds come with larger valuation steps · RESULTS H3 · ⏱ 1:30

**Message:** H3 is rejected with the opposite sign: a longer gap goes with a slightly larger total step, but a much smaller step per year.
**Layout:** paper Figure 19, two panels side by side: left, total step by gap quintile; right, step per year by gap quintile. Verdict in one line above.
**On slide:**
- **H3: rejected, opposite sign.** About +1% valuation step per 10% longer gap (elasticity 0.11, p < 0.001)
- Hype does not change it (p = 0.38)
- Slow raisers end with a larger total step but grow far more slowly per year
**Visual:** paper Figure 19, `x3_valuation_step_by_gap_quintile`. Backup: Fig. 18 `m9_valuation_by_gap`.
**Results:** R-33, R-34, R-37, R-49 (R-35 in backup).
**Inferences:** I-01 ✅ (a larger total step is about elapsed time, not value created by waiting) is said aloud here as one sentence; its home is slide 19.
**Sources:** footer "OLS of ln(post-money round 2 / post-money round 1), two-round startups with both valuations, N = 7,574; SEs clustered by sector × year of round 1 (73 clusters); log L2899, L3046; Figure 19: add-on log L1521–1580 (N = 7,514)".
**Speech:**
- H3 expected fast rounds to come with larger steps, as good news is priced. We find the opposite.
- A 10% longer gap goes with about a 1% larger step from round 1 to round 2.
- The right panel matters more: per year, the fastest quintile grows about five times faster than the slowest.
- So slow raisers end up with a bit more in total because more time has passed, not because waiting creates value.
- Valuations are post-money and disclosed for about half of the two-round startups: limits in backup B3.

### 16 · What startups bring to round 1 matters more than the gap · RESULTS CONTROLS · ⏱ 1:00

**Message:** round-1 characteristics are associated with exit far more strongly than the gap.
**Layout:** coefficient plot (odds ratios with 95% intervals) of the exit model, gap at the top in grey, round-1 controls below in dark blue. A vertical line at 1.
**On slide:**
- Larger first round, older startup at round 1 and the lead investor's type go with higher odds of exit
- The gap does not
**Visual:** paper Figure 14, `m4_exit_coefficients`, trimmed to gap + size + age + three lead types (Venture Capital, Corporate VC, Angel group). If the trim is not possible, a new odds-ratio plot.
**Results:** R-22, R-23, R-24 (R-30 for failure, in speech only).
**Sources:** footer "Logit of exit within 5 years, baseline model, N = 9,124; 41 clusters; log L358–379". Better-networked VCs perform better (Hochberg et al., 2007); CVC-backed firms are more innovative (Chemmanur et al., 2014); VCs see selection as more important than value-add (Gompers et al., 2020).
**Speech:**
- One log unit more first-round money goes with about 1.6 times the odds of exit. One more year of age at round 1, about +10%.
- A VC, a corporate VC or an angel group as lead goes with higher odds of exit, compared with the reference lead type.
- In failure, size and age go the same way; lead type does not matter.
- These are not effects of the investor: they mix who selects whom and what investors add.

⚠ The reference category of the lead-investor type is not visible in the log (open, register note on R-24): check before saying "compared with…". ⚠ Odds ratios differ slightly between the baseline and the interaction model (Angel group +95% vs +94%): use one model consistently.

### 17 · The pattern holds across windows, estimators and hype measures, in sign · ROBUSTNESS · ⏱ 1:15

**Message:** the main results do not depend on the window, the estimator or the hype measure. The one change makes H2 look worse, not better.
**Layout:** left, paper Figure 20 (β1 and β3 across 4-, 5-, 6-year windows, exit) stacked over Figure 21 (failure). Right, a checklist with ✓.
**On slide:**
- ✓ 4, 5 and 6-year windows: exit gap never significant, failure gap always significant
- ✓ Probit and linear probability model: same conclusions
- ✓ Finer hype measures, robust SEs, early exits removed, team and lead-age controls: gap × hype stays negative and not significant at 5%; the gap coefficients barely move
- ! Hype from past years only: gap × hype becomes significant, **opposite** to H2 (p = 0.04)
**Visual:** Fig. 20 `m7_windows_exit` + Fig. 21 `m8_windows_failure`.
**Results:** R-38, R-39, R-40, R-41, R-43, R-44 (R-42, R-45, R-46 in backup B2).
**Sources:** footer "Logit, H2 specification; log L1666–2176 (windows), L2584 (past-only hype, N = 6,593, 27 clusters), L2758 (probit); team and extra checks: add-on log". Young lead investors and grandstanding (Gompers, 1996) motivate the lead-age control.
**Speech:**
- The five-year window is a choice, so we try four and six. Exit stays insignificant, failure stays significant.
- Other estimators give the same answer.
- The most interesting check: if hype is measured only with past years, so nothing after round 1 is used, gap × hype becomes significant, and negative. That is our signal-extraction alternative, not H2.
- So we say "stable in sign", not "stable".

⚠ Do not use exit at any time (β1 −0.458, R-42) as evidence for H1: it mixes the gap with follow-up time. Backup only.

---

## E · Discussion, limits, conclusion

### 18 · A slow second round is not a distress signal · DISCUSSION · ⏱ 1:30

**Message:** taken together, the four verdicts fit selection and accumulated progress better than the good-news reading.
**Layout:** top, the four-row verdict table (slim paper Table 13): hypothesis · expected · found · verdict, coloured by verdict. Bottom, two boxes side by side: "Why less failure?" and "Why a larger step?".
**On slide:**

| | Expected | Found | Verdict |
|---|---|---|---|
| H1 gap → exit | − | − | Right sign, not significant |
| H1b gap → failure | + | − | Rejected, opposite sign |
| H2 gap × hype → exit | + | − | Not supported |
| H3 gap → valuation step | − | + | Rejected, opposite sign |

- Fast raisers may be the riskier ones, kept on a short leash (I-04)
- Slow raisers passed a longer test, and round 2 prices what they achieved meanwhile (I-03)

**Visual:** the table + two boxes. No new numbers (all numbers have their home on slides 13–15).
**Results:** pointers to R-17, R-26, R-33 (no numbers repeated).
**Inferences:** I-03 ✅, I-04 ✅.
**Sources:**
- Rounds are shorter when agency or monitoring costs are higher (Gompers, 1995; Tian, 2011): the first step of I-04; the step to "riskier" is ours.
- In learning models funding slows as the investor's belief falls (Bergemann and Hege, 2005).
- Observed valuations are a selected sample (Cochrane, 2005; Korteweg and Sorensen, 2010).
- Milestones govern the release of funds within a round, not the timing of the next round (Kaplan and Strömberg, 2003): the progress-priced reading (I-03) is our argument.
**Speech:**
- Put the four verdicts side by side: no hype moderation, no exit penalty we can detect, less failure, a larger step.
- One reading: short rounds are a leash. Investors keep risky ventures close, so fast raisers fail more.
- Another reading: slow raisers have survived a longer test, and round 2 prices what they built in the meantime.
- On hype: if anything a slow round says more in hot markets, as our alternative predicted.
- These readings are not exclusive, and our data cannot separate them.

⚠ Choose the H1 estimate (baseline or interaction model), as on slide 13.

### 19 · These are associations among startups that survived to round 2 · LIMITS TO CAUSALITY · ⏱ 1:30

**Message:** what we can and cannot claim, in three reasons, plus what a causal design would need.
**Layout:** three columns with an icon each (dice crossed out · clock looking forward · filter), one line under each. A bottom bar "What we can claim" with one sentence.
**On slide:**
- **The gap is not random:** unobserved quality, and investors choose round length
- **The group indicator looks ahead:** a startup acquired 8 months after round 1 is one-round *because* it exited, so ρ1 is not interpreted
- **Survivorship:** gap results describe startups that reached round 2. The gap measures what a startup survived and achieved, not how it is doing (I-02)
- *What we can claim:* conditional associations, useful to an investor at round 2; not advice to a founder on whether to wait
**Visual:** three-column diagram (to draw).
**Results:** pointer to R-15 (raw shares, slide 12) and R-46 (early exits removed: gap and gap × hype unchanged).
**Inferences:** I-02 ✅, I-01 ✅.
**Sources:**
- Sorting of better ventures to better investors explains about twice as much of IPO rates as investor influence (Sørensen, 2007).
- Investors set round length weighing agency and monitoring costs (Gompers, 1995; Tian, 2011).
- Valuations observed only at refinancing are a selected sample (Cochrane, 2005).
- Next steps: a survival model from round 1 with round 2 as a time-varying event, as in duration models of the time between rounds (Li, 2008); a funding-threshold discontinuity, as for angel groups (Kerr, Lerner and Schoar, 2014).
**Speech:**
- Three reasons why these are associations.
- First, better startups may both raise faster and do better, and the investor chooses the round length. Controls help only for what we observe.
- Second, whether a startup has a second round is known only after round 1. Some startups have one round because they already exited. So we never interpret the group dummy.
- Third, our gap results are about startups that made it to round 2. That is why we read the gap as what a startup survived and achieved.
- And the larger total step reflects elapsed time, not value created by waiting.
- A causal answer would need a survival model from round 1, or variation in the gap unrelated to quality.

### 20 · What founders and investors can take from this · CONCLUSION · ⏱ 1:00

**Message:** the answer to the research question, in one sentence per part.
**Layout:** the research question repeated small at the top; below it, the answer in large type; three takeaways in a row underneath. The two timelines from slide 2 come back in the corner.
**On slide:**
- **Answer:** in this sample, among startups that reach round 2, a longer gap is not significantly associated with exit, and hot markets do not change that. It goes with less failure and a larger total step.
- For investors at round 2: a slow round is not in itself a bad sign
- Round-1 information (size, age, lead type) says more than the gap
- Open: exit-market conditions at the time of exit; growth per year rather than total step
**Visual:** none (text + small timeline callback).
**Results:** none (no new numbers). **Inferences:** none new.
**Sources:** footer "Group 21, PitchBook 2012–2019".
**Speech:**
- Back to our two startups: startups like B, which waited 24 months, do not exit significantly less often on average, and fail less often.
- Part one of the question: no significant association with exit. Part two: hype does not soften it; if anything, a slow round says more in hot markets.
- What helps more is what we already know at round 1.
- Close on the answer, then "thank you, questions".

**Closing decided 17/11 (Lele, open point 23, option A):** the last sentence is the answer to the research question, not the founder implication. Never "founders should wait".

### 21 · References · REFERENCES · ⏱ 0:10

**Message:** full sources, for whoever reads the deck afterwards.
**Layout:** two columns, small type, author–year format as in the paper's reference list.
**On slide:**
- Data: PitchBook course extract (US startups founded 2012–2019), 21072 Data Analysis, Bocconi 2026/27
- Method: Hill, Griffiths and Lim (2018), *Principles of Econometrics*; Ai and Norton (2003); Mize (2019); Cameron, Gelbach and Miller (2008); Abadie, Athey, Imbens and Wooldridge (2023)
- Literature: Bergemann and Hege (2005); Chemmanur, Loutskina and Tian (2014); Cochrane (2005); Dahiya and Ray (2012); Gompers (1995, 1996); Gompers and Lerner (2000); Gompers, Gornall, Kaplan and Strebulaev (2020); Gornall and Strebulaev (2020); Ewens, Gorbenko and Korteweg (2022); Hochberg, Ljungqvist and Lu (2007); Howell, Lerner, Nanda and Townsend (2020); Kaplan and Strömberg (2003); Kerr, Lerner and Schoar (2014); Korteweg and Sorensen (2010); Li (2008); Nanda and Rhodes-Kropf (2013); Pástor and Veronesi (2005); Sørensen (2007); Tian (2011)
**Visual:** none.
**Results / Inferences:** none.
**Sources:** full entries generated from `fonti/fonti.bib`.
**Speech:** not presented; leave it up during questions, or skip.

⚠ The list must match exactly what the slides cite. Recheck after every change. Not cited, by decision: Nanda and Rhodes-Kropf (2017), Townsend (2015), Yu (2020).

---

## Backup slides (for questions; not timed)

### B1 · Full regression tables · BACKUP

**Message:** every coefficient, for questions.
**Layout:** three compact tables: exit (paper Table 6), failure (Table 8), valuation (Table 9). Columns: coefficient, SE, p; rows only gap, gap × hype, hype, two-round, controls; fixed effects as "yes".
**Visual:** `4. risultati/RQ1_tables.doc`, trimmed.
**Results:** R-16, R-17, R-25, R-26, R-31, R-33, R-34, R-35, R-36, R-48.
**Sources:** footer "Logs L346–550 (exit), L1139–1330 (failure), L2885–3050 (valuation)".
**Speech (if asked):** ρ1 is reported but not interpreted (slide 19). Valuation table label: "ln gap (θ1)", not "R × ln gap".

### B2 · Robustness in detail · BACKUP

**Message:** each check and what it changes.
**Layout:** one table (paper Tables 10–12 condensed) + the FWL figure.
**On slide:** window lengths; probit; LPM; exit at any time (N = 27,944, mixes gap with follow-up time); past-only hype; finer hype levels; robust SEs; early one-round exits removed; VIF; team and lead-age controls.
**Visual:** paper Fig. 17 `x2_fwl_outcomes_by_gap` (exit and failure against ln gap, net of controls: the relationship is close to linear).
**Results:** R-32, R-42, R-45, R-46.
**Sources:** footer "Logs L1666–2758; add-on log `not_in_log_checks.txt`".
**Speech (if asked):** the young-lead result (lower exit, opposite to grandstanding, Gompers 1996) is off our question: mention only if asked.

⚠ Paper v4 and the add-on log differ on clusters (190 / 570 vs 191 / 575) and some p-values (open point 21): the log wins.

### B3 · Limits of measurement and inference · BACKUP

**Message:** what could make our standard errors or our valuation measure less reliable.
**Layout:** four rows, problem · why it matters · what would fix it.
**On slide:**
- Few clusters (41): p-values can be too small; a wild cluster bootstrap would help
- Exit and failure are modelled separately, although they compete
- Valuations are post-money and disclosed for about half of the two-round startups
- The sample is the course cohort; hype is computed from the cohort's own deals
**Visual:** none.
**Results:** R-47, R-49.
**Sources:** with few clusters, cluster-robust tests reject too often; the wild cluster bootstrap brings the size back near 5% (Cameron, Gelbach and Miller, 2008). Post-money overstates fair value by 48% on average for 135 US unicorns (Gornall and Strebulaev, 2020). Post-money ignores contract terms other than the equity share (Ewens, Gorbenko and Korteweg, 2022).
**Speech (if asked):** we chose not to run the bootstrap (decision 17/11, open point 15); it stays a stated limit.

---

## Open points for the group (from this draft)

1. **Slide 2 hook:** keep the two-startup story? (Claude proposal, not approved.)
2. **H1 estimate on slides 13 and 18:** baseline (−0.089, p = 0.188) or model with interactions (−0.071, p = 0.29, as in paper Table 13)?
3. **Signal-extraction alternative (slide 5):** was it written before the results? If not, do not say it was.
4. **Lead-investor reference category (slide 16):** check in the do-file before saying "compared with…".
5. **Figure → file mapping:** check visually; align figure colours with the deck palette.
6. **New visuals to build:** slide 2 timelines, 4 two-column diagram, 5 hot/cold split, 7 funnel, 8 Figure 1 redrawn, 10 equation box, 11 bar chart, 16 trimmed odds-ratio plot, 19 three-column diagram.
7. **Speakers:** who presents which part (proposal: one member per part A–E).
