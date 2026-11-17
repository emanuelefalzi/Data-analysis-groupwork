# Scaletta presentazione — deck skeleton

**Group 21 · 21072 Data Analysis · final presentation, about 25 minutes · v0, 17/11/2026 (Lele + Claude)**

Derived from `scaletta.md` (v1, 16/11/2026), which stays the single source of truth for content, sources and numbers. This file holds **only what goes on the slides**.

**Status: v0 skeleton.** For now each slide has only its section, a claim title and three keywords. Layout, sources, speaker notes, R-xx / I-xx IDs come in later passes, one section at a time.

Rules that apply to every slide (`RULES.md`): title = a claim in English, not a label; associations only, never "effect / causes / leads to"; hypothesis verdicts in the wording of paper Table 13; one message per slide, one or two visuals at most; each result has one home slide.

Timing: 20 main slides ≈ 75 seconds each, plus backup.

---

## A · Opening and motivation

### 1 · Is a slow second VC round a bad sign? · TITLE
- Group 21, Data Lab for Entrepreneurship
- research question in one line
- PitchBook, US startups 2012–2019

### 2 · Two startups raise the same first round: one raises again in 6 months, the other in 24 · MOTIVATION
- staged VC
- time between rounds as a visible signal
- strength or distress?

### 3 · We ask whether the gap goes with exit, and whether hot markets change that · RESEARCH QUESTION
- gap between round 1 and round 2
- exit within five years
- hot vs cold funding markets

## B · Literature and hypotheses

### 4 · Staging theory predicts opposite signs for the gap · LITERATURE
- real option and learning: slow = bad news
- staging as a leash: short rounds for risky ventures
- survivorship at refinancing

### 5 · In hot markets, a fast round may say less about the startup · LITERATURE
- VC supply moves in cycles
- hot-market cohorts fail more
- H2 vs signal extraction

### 6 · Four hypotheses, one key test · HYPOTHESES
- H1 / H1b: gap and exit / failure
- H2 (key): gap × hype
- H3: gap and valuation step

## C · Data and method

### 7 · From 57,751 startups to 9,263 with a full five-year window · DATA
- disclosed first round: 28,478
- full outcome window: 9,263
- 4,483 two-round vs 4,780 one-round

### 8 · We keep startups that never raised again, so we do not condition on round 2 · DESIGN
- two groups (`two_rounds`)
- gap only for two-round startups
- timing: controls and hype at round 1

### 9 · Hype is a sector's share of VC dollars, compared with its own history · VARIABLES
- sector share of VC dollars, year of round 1
- z-score within sector
- hot = +1 SD, cold = −1 SD

### 10 · A logit with interactions, read as changes in probability · METHOD
- logit of exit within five years
- round-1 controls, three fixed effects, clustered SEs
- average marginal effects, hot minus cold

## D · Results

### 11 · Startups that raise again exit more and fail far less · DESCRIPTIVES
- exit: two-round vs one-round
- failure: two-round vs one-round
- raw rates, no controls

### 12 · Across gap quintiles, exit is flat while failure falls · DESCRIPTIVES
- exit flat
- failure falls, still private rises
- competing outcomes

### 13 · A longer gap is not significantly associated with exit, in hot or in cold markets · RESULTS H1, H2
- H1: right sign, not significant
- H2: opposite sign, not significant
- predicted probabilities, hot vs cold

### 14 · A longer gap goes with less failure, not more · RESULTS H1b
- H1b: rejected, opposite sign
- lower odds of failure
- hype does not change it

### 15 · Slower second rounds come with larger valuation steps · RESULTS H3
- H3: rejected, opposite sign
- larger total step
- per-year step falls

### 16 · What startups bring to round 1 matters more than the gap · RESULTS CONTROLS
- round-1 size
- lead-investor type
- age at round 1

### 17 · The pattern holds across windows, estimators and hype measures, in sign · ROBUSTNESS
- 4, 5, 6-year windows
- probit, LPM, no window
- past-only hype: significant, opposite to H2

## E · Discussion, limits, conclusion

### 18 · A slow second round is not a distress signal · DISCUSSION
- verdicts (Table 13)
- survivors who passed a longer test
- progress takes time and is priced

### 19 · These are associations among startups that survived to round 2 · LIMITS TO CAUSALITY
- the gap is not assigned at random
- the group indicator looks ahead
- survivorship at refinancing

### 20 · What founders and investors can take from this · CONCLUSION
- a slow round is not a bad sign
- round-1 information matters more
- next step: survival model from round 1

### 21 · References · REFERENCES
- literature cited in the deck
- data: PitchBook course extract
- course: Hill, Griffiths and Lim (2018)

---

## Backup slides

### B1 · Full regression tables · BACKUP
- exit, failure, valuation models
- coefficients, odds ratios, AMEs
- N and clusters

### B2 · Robustness in detail · BACKUP
- window length figures
- team and lead-age controls
- further checks (robust SEs, early exits removed, VIF)

### B3 · Limits of measurement and inference · BACKUP
- few clusters (41)
- exit and failure modelled separately
- post-money valuations, disclosed for about half
