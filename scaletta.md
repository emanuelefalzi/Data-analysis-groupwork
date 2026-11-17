# Scaletta — paper (final version) and deck

**Group 21 · 21072 Data Analysis · Bocconi 2026/27 · v1, 16/11/2026 (Lele + Claude)**

Base: `paper_group21.pdf` v4 (15/11/2026). Sources: the keys of `fonti/fonti.bib` (53 entries, built from `fonti/txt`). Numbers: `regression_analysis.txt` with line number where checked (`log L…`); otherwise "paper Table/Fig. x, to verify".

> **Status: reference document (v1).** This file is the single source of truth for content, sources and numbers. It serves two uses: the paper v5 and the slide outline (`slide outline.md`), which is derived from it. Anyone in the group may edit it, but **every change must be logged in `registers/changelog.md`** (who, date, what, how, why; see `RULES.md`). Open items are in `registers/open points.md`.
>
> Decisions applied in v1 are listed below (D1–D4). Points still marked as Claude's proposals are not approved. The section titles are the ones in paper v4, plus a new Section 6 *Limitations to causality*, so the old Section 6 becomes Section 7. Everything under **Claude's additions** is a proposal. The group accepts or rejects it.

## How to read this file

Each subsection (x.y) has five blocks:

1. **Content**: the 4–5 main points. Each point has a bold label, 4–10 keywords and a 30–40-word description.
2. **Sources**: `fonti.bib` keys, each with what the source says in a few words. These summaries are **taken from paper v4 and not yet checked against the txt**. The skill checks them (`/essay-estrai`) before drafting.
3. **Guardrails**: what does **not** go in this subsection because it has its home elsewhere (→ x.y).
4. **Editorial notes**: tables and figures, numbers to check, wording.
5. **Claude's additions**: suggestions, with a confidence level.

Rules that hold throughout (from `RULES.md`):
- **Associations only.** Never "effect", "impact", "causes", "leads to" for the gap or for hype. Write "is associated with" or "goes with".
- Hypothesis verdicts use the exact wording of Table 13: *right sign, not significant* · *rejected, opposite sign* · *not supported*.
- Every number says what it is (logit coefficient / odds ratio / AME in pp / OLS), its p-value and sample, and that SEs are clustered by sector × year of round 1.

## Section map

| # | Title | Change from v4 |
|---|---|---|
| 1 | Introduction | unchanged (roadmap paragraph to be rewritten, see 1) |
| 2 | Theory, literature and hypotheses (2.1–2.5) | unchanged |
| 3 | Data, variables and descriptive statistics (3.1–3.3) | unchanged |
| 4 | Econometric models (4.1–4.3) | unchanged |
| 5 | Results (opening, 5.1–5.6) | **5.6 narrowed** to limits of measurement and inference. Its causal limits move to 6 |
| **6** | **Limitations to causality (6.1–6.4)** | **new**, subsections proposed by Claude |
| 7 | Conclusions and discussion | was 6. Causal extensions move to 6.4 |
| — | References | generated from `fonti.bib` |
| — | Glossary | `glossary.md` (16/11) |

**Structural decisions** (decided by Lele on 16/11/2026 unless marked open):
- **D1. Decided: split.** 5.6 keeps the limits of measurement and inference; Section 6 holds the limits to a causal reading.
- **D2. Decided:** the title is "Limitations to causality".
- **D3. Open** (open point 13). The home of the valuation-measurement caveats (post-money overstatement, disclosure for about half the sample). They appear three times in v4 (2.4, 5.3, 5.6). Proposal: home in 5.6, one-line pointer in 5.3, mechanism only in 2.4.
- **D4. Decided: rewrite.** `nanda2017` and `townsend2015` are not cited. The sentences that rested on them (2.3 points 2–3, 2.5 point 2, 6.4 point 2) now rest on sources in `fonti.bib` or are stated as our own argument.
- **Sources (16/11).** All 53 "da riformulare" proposals of the source validation are applied. The 11 "non usabile" verdicts were confirmed by a second reader (Sonnet), and each tesi was replaced with a narrower one that the txt supports. `yu2020` is removed.

---

## 1 Introduction

**Role:** set up the problem, the question, the design and the three headline findings, with directions only.

### Content
1. **Staging makes the gap visible**: *staged VC, refinancing decision, observable progress, time between rounds, founders, investors*
   VC arrives in stages, and investors decide at each stage whether to refinance. The time between round 1 and round 2 is one of the few progress signals outsiders can see. The question is whether it signals strength or distress.
2. **The market can change what speed means**: *hot markets, abundant capital, fast closing, weaker screening, cold markets*
   In hot markets capital is abundant, rounds close fast and screening may be looser, so a fast round may say less about the startup. This motivates a two-part question: gap and exit, and whether hype changes that link.
3. **Design in one paragraph**: *PitchBook, 28,478 startups, two groups, no conditioning on round 2, exit within five years, sector hype*
   We keep every startup with a disclosed first VC round, split into those that raised a second round and those that did not. The gap enters only for the first group; hype is the sector's VC share, z-scored.
4. **Three headline findings, directions only**: *two-round startups exit more, gap and exit flat, no hype moderation, less failure, larger step*
   Startups that raise again exit more and fail less. Among them, a longer gap is not significantly associated with exit, and hype does not change this. A longer gap goes with less failure and a larger valuation step.
5. **Three literatures we add to**: *staging duration, hot-market cycles, selection in VC returns, contribution, design gap*
   Staging studies relate the number and length of rounds to outcomes. Hot-market studies show the cycle changes which ventures are funded. Selection studies predict that slow raisers look safer once refinanced. We connect the three with one design.

### Sources
- `gompers1995`: round duration falls as expected agency costs rise; ventures that go public get more rounds.
- `tian2011`: more and shorter rounds when the VC is far; more rounds go with better IPO outcomes only for distant firms.
- `gompers2000`: inflows into VC funds raise the prices of private deals.
- `nanda2013`: hot-market startups go bankrupt more often; those that IPO are valued higher and patent more.
- `li2008`: VC round durations respond to uncertainty, as a real-options view predicts.
- `cochrane2005`, `korteweg2010`: private-firm returns are observed only at financing events, so they are selected upward.

### Guardrails
- No coefficients, p-values or odds ratios. They belong to 5.1–5.3. Directions only.
- Do not define the hype z-score or the outcome window formally. That is 3.2.
- Do not give the hypotheses' mechanisms. That is 2.1–2.4. One sentence of motivation each at most.
- Do not discuss survivorship as a limitation. That is 6.3.

### Editorial notes
- v4 ends with "The paper proceeds as follows. Section 2…". The skill bans announcement sentences ("niente frasi-cerniera di annuncio dell'ordine", `skill-redigere essay/CLAUDE.md`), and the section numbers change anyway. Drop it, or rewrite it as a statement of what each part shows.
- v4 says "Three results stand out". Keep the count at three, so it matches the conclusion.
- The abstract claims findings are "stable across … alternative hype measures". The past-only hype β3 is significant (log L2584), so "stable in sign" is the accurate wording.

### Claude's additions
- [Likely] Open with a concrete founder-side hook (two startups, same round 1, one refinances at 6 months and one at 24) before the literature. This works for the paper and for slide 1 of the deck.
- [Certain] The question is phrased as an association ("is associated with"). Keep it that way. Do not write "does the gap affect".

---

## 2 Theory, literature and hypotheses

**Opening paragraph (no x.y):** one sentence on why hypotheses are stated in the staging-as-good-news direction with explicit competing predictions, plus a pointer to Table 1. Nothing else.

### 2.1 What the time between rounds measures

**Role:** give the two readings of the gap and state H1.

#### Content
1. **Staging as a real option**: *abandonment option, milestones, contingent rights, screening, cut-off of poor ventures*
   VC is staged so investors can abandon after new information. Contracts tie rights to milestones, and staging screens out ventures with poor early results. On this reading the gap is the time a venture needs to produce investable news.
2. **Learning and experimentation**: *Bayesian learning, belief decline, positive signals, experimentation, faster refinancing*
   In learning models each period without good news lowers the investor's belief, so good projects are refinanced sooner. Experimentation accounts agree: early rounds buy information, and fast positive signals bring fast refinancing. A short gap reads as good news.
3. **Staging as a leash**: *agency costs, monitoring, distance, shorter rounds, our step to risk*
   A second strand treats round length as the investor's governance choice. Rounds get shorter when agency or monitoring costs are higher. We argue that a short gap may then mark a venture that is hard to monitor and riskier, not a good one: the competing prediction (I-04).
4. **Evidence and the gap we fill**: *number and size of rounds, patents' signalling, information priced by round 2, untested link*
   Evidence links outcomes to the number and size of rounds, rarely to time. Patent signals fade by round 2 because investors already know more. No study we know relates gap to exit while keeping firms that never raised again.
5. **H1 stated**: *β1 < 0, longer gap, lower exit probability, two-round startups, competing β1 ≥ 0*
   H1: among startups that raise a second round, a longer gap is associated with a lower probability of exit within five years. The leash view predicts zero or positive. β1 is the coefficient of R × ln gap.

#### Sources
- `gompers1995`: staging as monitoring; duration falls with intangibility, R&D and market-to-book.
- `neher1999`: staging solves an agency problem between founder and investor.
- `cornelli2003`: staging gives the VC the option to abandon; convertibles deter window dressing of interim results.
- `kaplan2003`: VC contracts make cash-flow and control rights depend on observable milestones.
- `dahiya2012`: staging as a screen that cuts ventures with poor early results.
- `bergemann2005`: each period without success lowers the investor's belief that the project is good (theory).
- `kerrnanda2014`, `ewens2018`: VC rounds as experiments; cheaper start-up costs led VCs to fund more startups with smaller first cheques.
- `li2008`: duration model (Weibull AFT, right-censored) of the time between rounds, in a real-options framework.
- `wang2004`: staging gives the VC an option to quit, worth more the riskier the project (introductory remark, not a model result).
- `tian2011`: more and shorter rounds when the VC is distant.
- `hoenen2014`: patent *applications* raise round-1 funding but not round-2 funding (US biotech, 2001–2011).

#### Guardrails
- Failure and survivorship go in 2.2. Hype goes in 2.3.
- Do not use the leash view here to explain our results. That is 5.5 ("Staging intensity as a measure of risk"). Here it is only a prediction.
- No results: 5.1 has them.

#### Editorial notes
- Keep the order theory → competing theory → evidence → gap → hypothesis. Table 1, row H1, summarises it. Do not repeat the table in prose.
- H1 has to name the sample (two-round startups) and the window (five years) in the statement itself.

#### Claude's additions
- [Likely] The leash view predicts the failure result better than the exit result, and 5.5 depends on that. Flag it in one clause here ("a prediction we return to in 5.5"), not more.

### 2.2 Failure and survivorship

**Role:** state H1b and its survivorship counter-prediction.

#### Content
1. **Abandonment predicts more failure**: *option to abandon, stalled ventures, cut off, long gap, failure*
   If refinancing follows good news, investors cut off stalled ventures. A long gap should then go with more failure. This follows directly from the real-option and screening models of 2.1, applied to the bad tail.
2. **Investors do not always abandon**: *escalation, institutional pressure, tolerance for failure, innovation contracts*
   Investors keep funding under-performing ventures for political and institutional reasons. Contracts that tolerate early failure can be optimal for innovation. Both weaken the link between a long gap and abandonment, and so between a long gap and failure.
3. **Survivorship at refinancing**: *observed only at financing events, selection, value increase, positive selection on survival*
   Private-firm values and outcomes are seen only at financing events, and firms are refinanced only if alive and worth more. Returns at refinancing are therefore selected upward. This predicts that conditioning on refinancing makes slow raisers look safer.
4. **Life-cycle timing of failure**: *VC-backed vs non-VC firms, timing of failure, timing of acquisition, clock*
   VC-backed firms differ from comparable firms in when they fail and when they are acquired. When the clock starts therefore matters for how failure is measured, which motivates our explicit outcome window.
5. **H1b stated**: *H1b, failure within five years, gap coefficient > 0, competing negative sign, survivorship*
   H1b: a longer gap is associated with a higher probability of failure within five years among two-round startups. The competing prediction, from survivorship and tolerance for failure, is a negative coefficient on the gap in the failure model.

#### Sources
- `bergemann2005`, `dahiya2012`: abandonment of ventures whose early returns fall short (theory).
- `guler2007`: VCs become less likely to terminate as rounds accumulate, despite falling expected returns; politics may contribute.
- `manso2011`: contracts that tolerate early failure are optimal to motivate innovation.
- `cochrane2005`: VC returns are observed only at financing events, with selection bias.
- `korteweg2010`: corrects VC risk and return for the selection of observed valuations.
- `puri2012`: VC-backed and non-VC firms differ in the timing of failure and acquisition.

#### Guardrails
- **Survivorship has three homes. Keep them separate.** Here it is a *theoretical prediction*. In 5.5 ("Learning before refinancing") it is an *interpretation* of the failure result. In 6.3 it is a *limit to the causal reading*. Do not repeat the mechanism in full in each.
- Do not describe the window construction (Figure 1). That is 3.2. One sentence here, "our window starts at round 2", is enough.

#### Editorial notes
- v4 puts our design sentence ("a startup with a long gap has by construction survived that gap") in 2.2. Keep it as the bridge, and use it again only as a pointer in 6.3.

#### Claude's additions
- [Likely] Add one sentence saying that exit and failure are competing outcomes, so H1 and H1b are not independent tests. The paper says this only in 3.3 and 5.6, but readers need it when the hypotheses are set up.

### 2.3 Hot and cold markets

**Role:** build the key hypothesis H2 and its opposite-sign alternative.

#### Content
1. **VC supply moves in cycles**: *fund inflows, deal prices, public-market signals, IPO waves, bargaining power*
   Fund inflows raise private-deal prices. Investment follows public-market signals for an industry. IPOs come in waves. When capital is abundant, competition lowers investors' bargaining power and raises valuations. Hype is therefore a supply condition.
2. **Hot markets fund different ventures**: *hot-market cohorts, more failure, more innovation, experimental projects, financing risk*
   Startups first funded in hot markets go bankrupt more often, but those that go public are valued higher and patent more. In hot markets investors fund riskier startups and worry less about follow-on funding.
3. **Cold markets ration early-stage money**: *recessions, early-stage VC falls, capital supply, our argument on follow-on, not venture quality*
   Early-stage VC deals fall sharply in recessions. We argue that follow-on funding then depends partly on capital supply, not only on the venture. This last step is our reading, not a literature result.
4. **H2 (key): speed is cheap in hot markets**: *market component, venture component, gap less informative, β3 > 0*
   The gap mixes a market component with a venture component. If rounds close fast for everyone in hot markets, a slow round warns less there. H2: the negative gap–exit association is weaker in hot markets (β3 > 0).
5. **Our alternative: signal extraction**: *cold market waits, hot market easy money, gap more informative, β3 < 0, caution*
   Our own argument: in cold markets most ventures wait, so a long gap says little. In hot markets a long gap means investors chose not to fund quickly, so it says more about the venture (β3 < 0).

#### Sources
- `gompers2000`: fund inflows raise private-equity deal valuations.
- `gompers2008`: VC investment responds to industry Q; experienced VCs expand most, with no significant drop in success.
- `pastor2005`: IPO waves follow market conditions.
- `inderst2004`: more VC competition shifts bargaining to entrepreneurs and raises valuations (theory).
- `nanda2013`: pointer to Section 1 (same tesi); in hot markets investors fund riskier startups, worrying less about follow-on.
- `janeway2021`: review of VC booms and start-up financing.
- `howell2020`: early-stage VC deals fall sharply in recessions.
- D4 (16/11, Lele): `nanda2017` and `townsend2015` are not cited. Points 2 and 3 were rewritten so that they rest only on `nanda2013` and `howell2020` plus our own argument.

#### Guardrails
- Point 5 is **our argument, not a literature result**. Every sentence must say so ("we argue"). Do not attribute it to Howell or to any source.
- Do not explain the β3 result here. That is 5.5 ("Why hype does not soften the penalty"). Here the alternative is only stated as a prediction, with the same mechanism. 5.5 points back to it.
- The measurement of hype goes in 3.2.

#### Editorial notes
- v4 gives the signal-extraction mechanism twice in full (2.3 and 5.5). Choose one home. Proposal: the full mechanism here, then 5.5 opens with "the estimate fits the signal-extraction alternative of 2.3" and adds only the timing argument.
- H2 is "the key hypothesis". The deck needs it on the hypotheses slide and again on the main results slide.

#### Claude's additions
- [Likely] Writing the alternative before the results protects us from the "post hoc story" objection. Keep the sentence saying it was stated before estimation, **only if that is true**. Group to confirm: was it in the pitch or added after the results? If after, say so.

### 2.4 Valuation steps

**Role:** state H3 and its accumulated-progress counter-prediction (our argument, I-03).

#### Content
1. **Fast rounds should come with larger steps**: *refinancing after value increases, upward selection, good news, step-up*
   Refinancing is more likely after value has risen, so observed round-to-round returns are selected upward. If fast rounds follow good news, they should carry larger valuation steps from round 1 to round 2.
2. **H3 stated**: *θ1 < 0, longer gap, smaller valuation step, two-round startups*
   H3: among two-round startups, a longer gap is associated with a smaller log valuation step, measured as the post-money valuation at round 2 over the post-money valuation at round 1 (θ1 < 0), as the good-news reading predicts.
3. **Progress takes time and is priced (our argument)**: *total progress, longer gap, larger total step, θ1 > 0, not from the literature*
   We argue that rounds are priced on what the venture has achieved. A longer gap leaves more time to achieve it, so the total step can rise with the gap even if value grows more slowly per month (θ1 > 0). This is our reading (I-03): the literature ties milestones to the release of funds within a round, not to the timing of the next one.
4. **Prices also reflect terms and bargaining**: *senior preferred, post-money overstates, terms ignored, reputation discount, bargaining power*
   Post-money valuations overstate fair value because later investors hold senior shares, and they ignore contract terms other than the equity share. Entrepreneurs accept lower prices from reputable VCs. Measured steps mix value with contract and bargaining terms.
5. **Hype enters the valuation model too**: *capital inflows, prices rise, moderation, θ3*
   Prices rise with capital inflows, so hype could move the step directly and change its slope in the gap. This is why the H3 model also includes hype and its interaction with the gap.

#### Sources
- `cochrane2005`, `korteweg2010`: observed round-to-round returns are selected upward.
- `kaplan2003`: within a round, release of committed funds and some rights are contingent on milestones.
- `gornall2020`: post-money overstates fair value by 48% on average for 135 US unicorns.
- `ewens2022`: post-money valuation is a poor measure of firm value because it ignores contract terms other than the equity share.
- `hsu2004`: entrepreneurs accept lower valuations from more reputable VCs.
- `heughebaert2012`: university and government VCs value firms lower than independent VCs (Belgium).
- `gompers2000`: prices rise with fund inflows.

#### Guardrails
- Point 4 is a mechanism, so it stays short. The **limitation** (post-money and disclosure for about half the sample) has its home in 5.6 (D3).
- No numbers on the step. They are in 5.3.

#### Editorial notes
- `gornall2020` figure checked by the source validation: 48% on average for 135 US unicorns. Use this, not "about half".

#### Claude's additions
- [Likely] Add a sentence that the step is measured in total, not per month. This sets up Figure 19 in 5.3, the result that decides between points 1 and 3.

### 2.5 Controls: what they absorb and what the literature expects

**Role:** justify each round-1 control and each fixed effect, with its expected sign (Table 2).

#### Content
1. **Common causes and selection**: *team, deal selection, sorting, investor influence, quality, round-1 timing*
   VCs select mainly on the team, and sorting of better ventures to better investors explains more of outcomes than investor influence. Anything correlated with quality looks predictive, so we control only for variables fixed at round 1.
2. **Round-1 size**: *runway (our argument), investor conviction, syndicate quality, smaller experimental cheques*
   We argue that a larger first round buys runway and reflects investor conviction and syndicate quality. Cheaper experimentation means small first rounds are often experimental bets. Expected: more exit, less failure, a smaller step.
3. **Age and earlier deals at round 1**: *up-or-out, young firms, track record, angel and seed financing, experimentation already funded*
   Young firms grow fast but exit the market often. Older firms at round 1 have survived and have a track record. Earlier deals capture how much experimentation angels or others already financed. Expected: less failure, a smaller step.
4. **Lead-investor type**: *professionalisation, networks, reputation, monitoring, CVC as acquirer, angel groups, accelerators, grandstanding*
   Investor types select and add differently. VCs professionalise. Networked and reputable VCs see more exits. CVCs back innovative firms and buy them. Angel-funded ventures are more likely to survive. Some accelerators speed up development. Coefficients mix selection and influence.
5. **Fixed effects and clustering**: *HQ state, sector, year-quarter, geography, industry exit rates, exit windows, sector × year clusters*
   State FE absorb the geographic concentration of VC. Sector FE absorb industry differences in success rates and in how fast firms mature. Year-quarter FE absorb exit-market windows. SEs are clustered by sector × year of round 1, the level at which hype is assigned.

#### Sources
- `gompers2020`: VCs rank the team as the top selection factor and see selection as more important than value-add (survey).
- `sorensen2007`: sorting is almost twice as important as influence for IPO rates (CA and MA, 1982–95).
- `hochberg2007`: better-networked VCs perform better; their ventures survive to later rounds.
- `ewens2018`: cheaper experimentation means smaller first cheques to more ventures.
- `haltiwanger2013`: young firms show an up-or-out pattern.
- `hellmann2015`, `hellmann2021`: angels and VCs as sequential investors: friends and foes (theory; dynamic substitutes in BC data).
- `hellmann2002`: VC backing goes with professionalisation of start-ups.
- `nahata2008`: VCs with a higher IPO-capitalisation share go with more successful exits and faster IPOs.
- `bernstein2016`: closer VC monitoring raises innovation and IPO rates.
- `chemmanur2014`: CVC-backed firms are more innovative.
- `ma2020`: firms whose internal innovation has declined set up CVC to access startup technology.
- `kerrlerner2014`: angel funding goes with higher survival and growth just above the threshold (RD); exit is not significant.
- `hallen2020`: some accelerators speed up venture development. (`yu2020` removed 16/11, Lele; `gonzalezuribe2018` removed: it only reports this idea from others.)
- `gompers1996`: young VCs take firms public earlier, consistent with grandstanding (IPOs only).
- `sorenson2001`: VC investment is local and falls with distance.
- `chen2010`: VC firms and VC-backed companies are heavily concentrated in three metro areas.
- `gompers2009`: success rates differ across industries, so industry controls are needed.
- `lerner2020`: firms in different industries mature at very different speeds.
- `lerner1994`, `pastor2005`: IPOs cluster when market valuations are high (Lerner: biotech; Pástor & Veronesi: theory of IPO waves).
- `abadie2023`: cluster at the level of treatment assignment, when sampling is not clustered. Applying this to `heat` is our extension (hype is not an assigned treatment); say so.
- D4 (16/11, Lele): `nanda2017` not cited; point 2 now states runway as our argument.

#### Guardrails
- Expected signs only, no estimates. Estimates are in 5.1–5.3, and the comparison with the literature is in 5.5 (Table 14).
- Do not argue that round-1 controls make the estimates causal. 6.1 says the opposite.
- **Do not mention an `Accelerator_pre_r1` control.** It is not in the v2 dataset (RULES, known inconsistencies). Accelerators enter only as a lead-investor category.
- The few-clusters problem is in 5.6, not here.

#### Editorial notes
- 19 references in one subsection is a lot for a 25-minute deck. In the paper, keep them in Table 2. In the deck, one "controls" line is enough.
- Why controls are "fixed at round 1" (they cannot be outcomes of the gap) is a design decision. Keep it in one sentence here and point to it from 6.1.

#### Claude's additions
- [Likely] Say explicitly that round-2 variables (size, valuation) are left out on purpose because they are mediators. This is a group decision (RULES), and examiners often ask about it.

---

## 3 Data, variables and descriptive statistics

### 3.1 Sample construction

**Role:** take the reader from 57,751 startups to the 9,263-startup estimation sample, with every drop justified.

#### Content
1. **The PitchBook course extract**: *57,751 US startups, founded 2012–2019, deal file, investor files, lead investor*
   The data are the course PitchBook extract: a startup file of 57,751 US startups founded 2012–2019, a deal file, and deal-investor and investor files used to identify each round's lead investor.
2. **What counts as a VC round**: *completed and dated deals, Seed, Early Stage VC, Later Stage VC, same-day merge*
   A VC round is a completed, dated Seed, Early Stage or Later Stage VC deal. Angel, grant, debt and accelerator deals are not. Same-day VC deals of one company are merged into one round, with amounts summed.
3. **From the extract to the full sample**: *at least one VC round, gap ≤ 10 years, no pre-round-1 exit, disclosed amount, 28,478*
   Successive filters keep startups with a VC round, a gap of ten years or less, and no exit or failure dated before round 1. Dropping undisclosed round-1 amounts leaves 28,478 startups: 15,518 with two rounds and 12,960 with one.
4. **Full outcome window: estimation sample**: *5-year window, fully observed by 30 June 2022, 9,263, 4,483 / 4,780*
   A zero means "no exit" only if the whole window is observed. Keeping startups whose five-year window ends by 30 June 2022 gives 9,263 startups: 4,483 with two rounds and 4,780 with one.
5. **Handling rules**: *round 2 after cut-off, no imputation, missing at random, Unknown state*
   A round 2 after 30 June 2022 counts as no round 2. Undisclosed round-1 amounts are dropped, not imputed, which avoids assuming they are missing at random. A missing state is kept as "Unknown".

#### Sources
- None from `fonti.bib` (descriptive). Source of the counts: `construction.pdf` table (lines 122–130 of its text) and paper Table 3.

#### Guardrails
- Variable definitions go in 3.2. Do not define `log_gap_r2` or `heat` here.
- Do not discuss what dropping undisclosed amounts does to external validity. That is 5.6.
- Group sizes appear here once. Elsewhere, only "the estimation sample".

#### Editorial notes
- ⚠ **Terminology clash.** `construction.pdf` calls the 28,478 startups the "estimation sample". The paper calls the 9,263 that. Fix it in the glossary: *full sample* = 28,478, *estimation sample* = 9,263 (`full_window == 1`). Add it to open points.
- Table 3 is the table of this subsection. In the deck it becomes a funnel chart.
- The drop of undisclosed amounts was pitch feedback (13/11). One clause is enough.

#### Claude's additions
- [Likely] Give the share of undisclosed round-1 amounts (6,285 of 34,763, about 18%) and whether they differ in exit rates. That check is not in the log. If the group wants it, it is new code, not a number to write now.

### 3.2 Variables

**Role:** define group, gap, outcomes, window, hype and controls precisely enough to reproduce (Table 4, Figure 1).

#### Content
1. **Groups and the gap**: *R = two_rounds, months between rounds, log transform, multiplied by R, one-round startups at zero*
   R is 1 if a second VC round closed by 30 June 2022. The gap, in months, is right-skewed, so it enters as R × ln(1 + months). One-round startups stay in the sample with a value of zero.
2. **Outcomes and the outcome window**: *exit = IPO or acquisition, failure, window start, round 2 vs round 1, 4/5/6 years*
   An exit is an IPO or an acquisition, whichever comes first. Failure uses PitchBook's failure date. The window opens at round 2 for two-round startups and at round 1 for one-round startups. Five years is the main window.
3. **Figure 1: timing**: *schematic, survival through the gap, controls dated at round 1, hype at round 1*
   Figure 1 shows the timing. A two-round startup enters its outcome window only after surviving the gap, while controls, hype and fixed effects are all dated at round 1. This timing drives the reading of the failure result.
4. **Market hype**: *sector share of VC dollars, year of round 1, z-score within sector, 2012–2022, seven sectors*
   Hype is the sector's share of all VC dollars in the year of round 1, z-scored within the sector over 2012–2022. Raw shares measure sector size. The z-score measures moments: +1 is one SD above that sector's norm.
5. **Valuation step and controls**: *ln(post-money r2 / post-money r1), round-1 size, deal number, age, lead type, FE*
   The valuation step is ln(post-money at round 2 / post-money at round 1). Controls, all at round 1: log amount, number of deals so far, age, lead-investor type (16 categories). Fixed effects: year-quarter, sector, state.

#### Sources
- None required (definitions). The hype definition is our own. If the group wants to cite why a relative share is used, `gompers2000` and `nanda2013` measure hot markets through capital inflows.

#### Guardrails
- Do not report means or distributions. That is 3.3.
- Do not write the model equation. That is 4.1.
- Robustness variants (`heat_past`, finer hype) get one line in Table 4 at most. They are introduced in 4.3.

#### Editorial notes
- **Naming.** The variable is `heat`, the concept is "hype", and the text also says "hot/cold". Fix one canonical term in the glossary: *hype* in prose, `heat` only in code tables. "Hot"/"cold" = ±1 SD of hype, or terciles in the figures. The two uses must not be mixed.
- The IT example (about 40% of VC dollars every year, Materials about 1.5%) is a strong explanation for the z-score and works well as a deck visual. Check the numbers against code before keeping them (not in log).

#### Claude's additions
- [Likely] State the main outcome explicitly as `exit_5y` and mention that `exit` (any time) is robustness only. `construction.pdf` says otherwise and is superseded (RULES). A reader of both documents will notice.

### 3.3 Descriptive statistics

**Role:** show the raw patterns that motivate the models, without claiming them as tests.

#### Content
1. **Two groups differ sharply**: *exit 22.2% vs 15.6%, failure 12.4% vs 31.6%, t-tests, larger first rounds, younger*
   In the estimation sample, two-round startups exit more often and fail far less often than one-round startups. Both differences are significant in t-tests. They also raised larger first rounds and were younger at round 1.
2. **The gap distribution**: *median about 13 months, mean 14.7, right tail, log specification*
   The median two-round startup raised round 2 about 13 months after round 1 (mean 14.7, long right tail; Figure 2). The skew justifies the log specification and the interquartile range used later for magnitudes.
3. **Why the window is needed**: *cohort truncation, recent cohorts, one-round share after 2019, mechanical effect*
   For recent cohorts the share of one-round startups jumps, simply because there was no time to raise again (Figure 3). Restricting to fully observed windows removes this mechanical effect from the group comparison.
4. **Hype varies within sectors**: *Figure 4, within-sector variation, IT cold 2015–2019, healthcare peak 2020, Energy outlier*
   Hype varies over time within every sector (Figure 4). This within-sector variation is what identifies H2 once sector fixed effects remove permanent differences between sectors. Energy has one outlier year, 2012, when very few deals were recorded.
5. **Raw outcome patterns by gap**: *gap quintiles, exit flat, failure falls, still private rises, competing outcomes*
   Across gap quintiles the exit share barely moves, failure falls and the share still private rises (Figure 8). A slow round is followed more by staying private than by exit. Raw shares, no controls.

#### Sources
- None (descriptive). Source: log L120–200 (tabstat, t-tests) for Table 5. Figures 2–7 and 9–10 come from the do-file (`figures/d1…d8`). ⚠ **Figure 8 (exit / failure / still private) is not exported by the do-file**, so it is "not in log".

#### Guardrails
- Figures 7 and 8 are **descriptive**. Do not call them evidence for or against H1/H2. The tests are in 5.1–5.2.
- Do not interpret falling failure as survivorship here. That interpretation is 5.5, the limit is 6.3. One clause is allowed: "consistent with the models of Section 5".
- The lead-type exit rates (Figure 10) are only a motivation for the control. Do not compare them with literature here (that is 5.5).

#### Editorial notes
- **Ten figures in one subsection** (Figs 2–10). Proposal: keep 2, 3, 4 and 8 in the text. Move 5, 6, 7, 9 and 10 to an appendix. Figure 8 is the most informative and should get a deck slide.
- Check the Table 5 values against log L120–200 (still to do line by line).

#### Claude's additions
- [Likely] Figure 8 (exit / failure / still private) is the single best bridge to 6.3: slow raisers are not exiting more, they stay private more. Keep it in the main text.

---

## 4 Econometric models

### 4.1 Main specification

**Role:** write the main logit, say what each coefficient identifies, and why marginal effects are needed.

#### Content
1. **The equation**: *logit, exit within five years, R, R × ln gap, hype, interactions, controls, three FE*
   The main model is a logit of exit within five years on both groups, with R, R × ln gap, hype, their interactions, round-1 controls and three sets of fixed effects. It runs first without, then with, hype interactions.
2. **What identifies what**: *β1 within two-round startups, one-round startups, controls, fixed effects, ρ1, ρ2, group comparison*
   Because ln gap is multiplied by R, β1 and β3 come only from variation among two-round startups. One-round startups help estimate the controls and fixed effects. ρ1 and ρ2 compare the two groups.
3. **Interactions in a nonlinear model**: *log-odds, interaction effect on probability, different size and sign, own SE, AMEs*
   In a logit the interaction coefficient is on the log-odds scale. Its effect on the probability can differ in size and sign and needs its own standard error. We also report AMEs of ln gap at hype −1, 0, +1.
4. **Three readings of H2**: *β3, hot-minus-cold AME, delta method, LPM as check*
   H2 is read three ways that should agree: β3 as the change in the log-odds slope, the hot-minus-cold difference in AMEs (delta method), and the linear probability model, where the two coincide.
5. **Samples and clusters**: *9,124 of 9,263, perfect prediction drops, LPM 9,262, 41 clusters, few clusters*
   The logit uses 9,124 startups because Stata drops cells that predict the outcome perfectly. The LPM keeps 9,262. SEs are clustered by sector × year of round 1, giving 41 clusters. With few clusters, p-values can be too small.

#### Sources
- `ai2003`: in logit and probit the interaction effect is not the interaction coefficient.
- `mize2019`: best practice is to estimate and show nonlinear interactions with marginal effects.
- `cameron2008`: with few clusters (5–30) cluster-robust tests over-reject; the wild cluster bootstrap-t brings size near 5% (linear models).
- `abadie2023`: as in 2.5.
- Course: Hill, Griffiths and Lim (2018) for logit, LPM, interactions and clustered SEs. Not in `fonti.bib`, and the course-brain folder for 21072 does not exist yet (open point 7).

#### Guardrails
- How to read the coefficients (odds ratios, IQR, conditional main effects) is in the opening of Section 5. Here say only *what* is estimated.
- Do not state that the few-clusters problem is solved. The checks are in 5.4, the limit in 5.6.
- Do not interpret ρ1. Say only that 6.2 explains why.

#### Editorial notes
- Check N = 9,124 (log L346, L521), LPM N = 9,262 (log L971) and the 41 clusters in the log header.
- The equation stays in the paper. In the deck it becomes a simplified version with three highlighted terms (β1, β3, ρ1).

#### Claude's additions
- [Likely] Add one line saying that the model is a linear index in ln(1 + months), and that Figure 17 (5.2) checks the functional form. Otherwise a reader asks why log and not quadratic.

### 4.2 Other outcomes

**Role:** define the failure model (H1b) and the valuation OLS (H3).

#### Content
1. **Failure model**: *same logit, failure within five years, same controls, same FE, H1b*
   For H1b, the same logit equation is estimated with failure within five years as the outcome, on the same estimation sample, with the same controls, fixed effects and clustering as the exit model.
2. **Valuation model**: *OLS, log valuation step, ln gap, hype, interaction, two-round only*
   For H3, an OLS model regresses the log valuation step on ln gap, hype and their interaction, with the same round-1 controls and fixed effects. Only two-round startups enter, because the step needs a round 2.
3. **Valuation sample**: *7,574 of 15,518, both post-moneys, no window needed, 73 clusters*
   The valuation model needs no outcome window, because the step is observed at round 2. It therefore uses all two-round startups with both post-money valuations: 7,574 of 15,518, with 73 sector × year clusters.
4. **Elasticity reading**: *log–log, elasticity, θ1, semi-elasticity, age and earlier deals in levels*
   Both the step and the gap are in logs, so θ1 is an elasticity. Age and earlier deals enter in levels and read as semi-elasticities. This sets up the magnitudes reported in 5.3.

#### Sources
- None new (methods as in 4.1).

#### Guardrails
- Results go in 5.2–5.3.
- The disclosure-selection caveat goes in 5.6 (D3).

#### Editorial notes
- Check 7,574 / 73 clusters (log L2885 onwards).
- 4.2 can be short (about 150 words). Points 3 and 4 can merge if space is tight.

#### Claude's additions
- [Guessing] Name the two outcome samples consistently in the glossary: "estimation sample" (exit/failure, 9,263) vs "valuation sample" (7,574).

### 4.3 Robustness tests

**Role:** list the checks and what each would reveal, **before** any result.

#### Content
1. **Estimator**: *linear probability model, probit, β3 in probability units, estimator choice*
   The main equation is re-estimated as a linear probability model, where β3 reads directly in probability units, and as a probit. Agreement across estimators shows that the logit's nonlinearity is not driving the interaction result.
2. **Window length**: *4, 5 and 6 years, fully observed windows, stability of β1 and β3*
   Exit and failure models are re-run with four- and six-year windows, each on startups whose window of that length is fully observed. Large movement in β1 or β3 would make the five-year choice unsafe.
3. **No window**: *exit at any time, all 28,478, follow-up time*
   Exit at any time is estimated on all startups without a window. This tests what happens when the window is dropped, at the cost of mixing the gap with remaining follow-up time.
4. **Hype without look-ahead**: *past-only z-score, look-ahead, information at round 1, smaller sample*
   Hype is recomputed using only the sector's past years, so the measure uses only information available at round 1. This removes the concern that the z-score uses future years of the same sector.
5. **Further checks and extra controls**: *finer hype, robust SEs, early exits removed, VIF, team and lead-age controls*
   Further checks: hype at finer levels, robust instead of clustered SEs, removing early one-round exits and failures, variance inflation factors, and team and lead-investor-age controls on the subsample with founder data.

#### Sources
- `gompers1996`: young lead investors and grandstanding (motivates the young-lead control).
- `cameron2008`: SEs that ignore within-cluster correlation can greatly understate the true SEs.

#### Guardrails
- **No results here.** Every number is in 5.4. This subsection says only *why* each check exists.
- Team and lead-age controls are mentioned in v4 only in 5.4. Proposal: list them here too, so 4.3 is complete.

#### Editorial notes
- Flag here, in one clause, which checks are **outside the do-file**: point 5 (finer hype, robust SEs, early exits, VIF; Table 12 run in Python). RULES requires them to be marked "not in log".

#### Claude's additions
- [Likely] Number the checks (i)–(vi) and reuse the numbering in 5.4, so the reader can match design to result without the text repeating itself.

---

## 5 Results

### 5 (opening, no x.y): How to read the coefficients

**Role:** the reading key for all of Section 5, given once.

#### Content
1. **Three readings of a logit coefficient**: *log-odds, odds ratio, exp(β) − 1, AME in pp, LPM*
   Every logit coefficient is a change in log-odds. We report the odds ratio, exp(β), the average marginal effect in percentage points, and the LPM coefficient, which is already in probability units and checks the AME.
2. **Log-level magnitudes**: *ln(1 + months), 2.7-fold, 10% longer gap ≈ β/10, IQR 2.24–3.02 (8–19 months)*
   One unit of ln gap multiplies 1 + months by 2.7. A 10% longer gap changes log-odds by about β/10. Magnitudes use the interquartile range of ln gap, 2.24 to 3.02, which is 8 to 19 months.
3. **Conditional main effects**: *slope = β1 + β3 · hype, β1 at average hype, β3 per SD, ρ1 at zero gap*
   In the interacted model the gap slope is β1 + β3 · hype. β1 is the slope at average hype, and β3 its change per SD of hype. ρ1 is the group gap at a zero-month gap, outside the data.
4. **Scale with raw rates**: *raw five-year rates, exit 22.2% vs 15.6%, failure 12.4% vs 31.6%, scale*
   Unconditional five-year rates scale every effect: 22.2% of two-round and 15.6% of one-round startups exit, and 12.4% and 31.6% fail. A two-point change in exit is about a tenth of the two-round rate.

#### Sources
- `ai2003`, `mize2019` (pointer only, already explained in 4.1).

#### Guardrails
- Raw rates come from 3.3. Repeat them only as a scale, without discussion.

#### Editorial notes
- This block is didactic. In the paper keep it about 250 words. In the deck, one "how to read" box on the first results slide.

#### Claude's additions
- [Likely] Add a 3-row "reading" table (scale, what 1 unit means, example) instead of prose. It saves words and helps the oral delivery.

### 5.1 Exit (H1 and H2)

**Role:** report H1 and H2 on exit, in coefficients and in probabilities.

#### Content
1. **H1: right sign, not significant**: *β1 = −0.089, p = 0.188, odds ratio 0.915, interval includes zero*
   In the baseline logit the gap coefficient is −0.089 (p = 0.188): a 2.7-fold longer gap goes with 8.5% lower odds of exit. The sign matches H1, but the data cannot tell a small penalty from none.
2. **H2: opposite sign, not significant**: *β1 = −0.071, β3 = −0.056, p = 0.344, slope steeper in hot markets*
   With hype interactions, β1 = −0.071 (p = 0.294) and β3 = −0.056 (p = 0.344). The gap slope gets steeper, not flatter, as hype rises, which is the opposite of H2. β3 is not significant.
3. **The same in probabilities**: *AME cold −0.3 pp, hot −2.1 pp (p = 0.07), hot − cold −1.9 pp (p = 0.33), LPM*
   AMEs per unit of ln gap: about zero in cold markets, −2.1 pp in hot ones (p = 0.07). The hot-minus-cold difference, −1.9 pp, is not significant (p = 0.33). The LPM gives the same reading.
4. **Predicted probabilities**: *Figure 12, cold flat about 22%, hot 26% → 20%, overlapping bands*
   Predicted exit is flat at about 22% in cold markets. In hot markets it falls from about 26% at three months to about 20% at four years, but the bands overlap everywhere (Figures 11–12).
5. **Controls are larger than the gap**: *round-1 size OR 1.64, age +10%, angel group +94%, CVC +56%, VC +39%*
   Round-1 size and age at round 1 go with much higher exit odds, and angel-group, CVC and VC leads with higher odds than no identified lead. Moving across the gap IQR changes exit by less than one point.

#### Numbers (log)
- H1 β1 −0.0889, p 0.188: **log L358**. H2 β1 −0.0714, p 0.294: **L538**. β3 −0.0557, p 0.344: **L541**.
- AMEs −0.0025 (p 0.883) / −0.0116 (p 0.293) / −0.0211 (p 0.068): **L672–676** (N = 4,444 two-round startups). Hot − cold −0.0186, χ²(1) = 0.96, p = 0.327: **L693–703**.
- LPM β1 −0.0121 (p 0.271), β3 −0.0083 (p 0.385): **L989, L992**.

#### Sources
- None new. Results are ours; literature comparisons go in 5.5.

#### Guardrails
- **ρ1 (the coefficient of R) is reported, not interpreted.** v4's Figure 13 paragraph ("should not be read as the effect of raising a second round") points to 6.2, which holds the reason.
- The controls versus the literature (Table 14) is in 5.5. Here, only their size relative to the gap.
- Verdict wording, exactly: H1 *right sign, not significant*; H2 *not supported*.
- Do not mention past-only hype here. It is in 5.4.

#### Editorial notes
- ⚠ The AMEs use **N = 4,444** two-round startups (log L659), not 4,483. Mention it in the Table 7 note.
- Figures 11, 12, 13 and 14 make four figures. Proposal: keep 11 or 12 in the text (the deck needs only one: Figure 12 is more intuitive), and move 13 and 14 to the appendix.
- The deck's main results slide: Figure 12 plus one sentence. The coefficient table goes in a backup slide.

#### Claude's additions
- [Likely] Lead with the null on H2, since H2 is "the key hypothesis". In the deck, open the results on H2, not H1.
- [Certain] "Not significant" ≠ "no effect". Keep "the data cannot distinguish a small penalty from none" as the model sentence.

### 5.2 Failure (H1b)

**Role:** report the failure result, the largest and most stable gap association.

#### Content
1. **H1b rejected, opposite sign**: *β1 = −0.241 (p = 0.001), β1 = −0.231 (p = 0.005), odds ratio 0.794, 21% lower odds, opposite sign*
   The gap coefficient in the failure logit is negative and significant: −0.241 in the baseline, −0.231 with interactions. A 2.7-fold longer gap goes with 21% lower failure odds, the opposite of H1b.
2. **Magnitude in probability**: *AME −2.4 pp per unit, −1.9 pp over IQR, mean 12.4%, about −15% relative*
   One unit of ln gap goes with 2.4 points less failure at average hype. Over the gap's interquartile range that is −1.9 points against a mean of 12.4%, a relative fall of about 15%.
3. **Hype does not change it**: *β3 = −0.030, p = 0.681, AME −2.1 to −2.8 pp, cold and hot markets*
   Hype does not moderate the failure slope (β3 = −0.030, p = 0.681). Predicted failure falls from about 15–17% at three months to about 9% at four years in both cold and hot markets (Figures 15–16).
4. **Controls mirror exit, lead type does not**: *round-1 size −37% odds, age −8% odds, lead type not predictive, upside vs downside*
   Larger first rounds and older startups fail less, mirroring the exit model with opposite signs. Lead-investor type does not predict failure, so the lead type relates to the chance of a good outcome, not of a bad one.
5. **Functional form check**: *Frisch–Waugh–Lovell, binned residuals, linear in ln gap, slope −0.030*
   After partialling out controls and fixed effects, failure falls steadily across the whole range of ln gap (Figure 17). The log form fits, and no few extreme gaps drive the result. For exit the bins are flat.

#### Numbers (log)
- β1 −0.2409, p 0.001: **L1151**. β1 −0.2309, p 0.005: **L1305**. β3 −0.0301, p 0.681: **L1308**. N = 9,235 (**L1139, L1288**).
- AMEs for failure: from the grid at **L1424** onwards. Values at hype −1/0/+1 still to read in the log.

#### Sources
- None new (literature in 5.5).

#### Guardrails
- **Do not explain why** failure falls (leash, survivorship, learning). That is 5.5. Here only "opposite to H1b".
- Do not say "a longer gap reduces failure". Say "goes with lower failure".
- ρ1 for failure (−0.716): report only, with a pointer to 6.2.

#### Editorial notes
- ⚠ Figure 17 (FWL binned scatter) is **not exported by the do-file**, so it is "not in log".
- Figure 17 (FWL) is "the course's way" of checking functional form. If it is a course concept, cite it from the course (Hill et al. 2018 / lessons). [Guessing] which lesson. Ask Lele.
- Deck: this is the strongest result and deserves its own slide (Figure 16 or 17).

#### Claude's additions
- [Likely] The phrase "the largest and most stable gap effect" uses *effect*. Change it to "association" (RULES).

### 5.3 Valuation step (H3)

**Role:** report H3 and show that the result concerns total progress, not speed of value creation.

#### Content
1. **H3 rejected, opposite sign**: *θ1 = 0.109 (p < 0.001), elasticity, +1.1% per 10% gap, +8.9% over IQR*
   θ1 = 0.109 is an elasticity: a 10% longer gap goes with a step about 1.1% larger, and moving from 8 to 19 months with a step about 8.9% larger. This is the opposite of H3.
2. **No moderation by hype**: *θ3 = −0.016, p = 0.381, Figure 18, cold and hot markets*
   Hype does not change the gap–step slope (θ3 = −0.016, p = 0.381). The predicted log step rises from about 0.9–1.0 for very short gaps to about 1.2 at four years in both markets (Figure 18).
3. **Controls priced at round 1**: *size −0.139, age −6.1%, earlier deals −4.2%, accelerator +33%*
   Larger first rounds, older startups and more earlier deals all go with smaller steps, as expected when part of the growth is priced at round 1. Accelerator-led first rounds are followed by much larger steps.
4. **Total vs per-year step**: *Figure 19, total flat then 1.18, per-year median 1.89 → 0.36, five times faster*
   The total step is flat across the first four gap quintiles and higher for the slowest. Per year, the median step falls from 1.89 to 0.36 log points. Fast raisers gain value about five times faster per year.
5. **The accumulated-progress reading**: *total progress, speed of value creation, competing prediction of 2.4, our argument*
   We read the positive θ1 as a statement about total progress accumulated before round 2, not about how fast value is created. It matches the competing prediction of 2.4. Speed of value creation favours fast raisers.

#### Numbers (log)
- θ1 0.1088, p < 0.001, N = 7,574: **L2899** (baseline) / 0.1086 **L3043**. θ3 −0.0163, p 0.381: **L3046**.
- ⚠ Figure 19 (and its 1.89 / 0.36 medians) is **not produced by the do-file**: no export for it in `rq1_two_group_analysis_v2.do`. Mark it "not in log".

#### Sources
- `kaplan2003`: milestones govern release of funds within a round, not the timing of the next round.

#### Guardrails
- The post-money and disclosure caveats: one-line pointer to 5.6 (D3). Do not repeat `gornall2020` and `ewens2022` here.
- The "progress that is priced" explanation is in 5.5. Point 5 here states only the reading of Figure 19.

#### Editorial notes
- Table 9 row label "R × ln gap (β1)" is misleading for an R = 1-only model (its note says so). Rename it to "ln gap (θ1)" in the final table.
- The deck can show Figure 19 (two panels) as a single slide. It is the most intuitive visual in the paper.

#### Claude's additions
- [Likely] Point 4 is the strongest answer to "slow raisers do better?": no. They end with more in total but grow more slowly. Keep that sentence for the conclusion and the deck.

### 5.4 Robustness

**Role:** show that the conclusions do not depend on the window, estimator, hype measure or omitted team quality.

#### Content
1. **Window length**: *4/5/6-year windows, exit β1 never significant, failure β1 always significant, Figures 20–21*
   With four-, five- and six-year windows, exit β1 and β3 are never significant. Failure β1 is negative and significant in all three windows, and β3 is close to zero. The five-year choice drives none of the results (Figures 20–21).
2. **Estimator and no window**: *probit, β3 −0.028 (p = 0.390), exit ever, β1 −0.458, follow-up time*
   The probit gives the same signs and significance. Exit at any time gives a large negative gap coefficient, but it is not comparable: long-gap startups have less follow-up time left, so the estimate mixes gap with time.
3. **Past-only hype**: *β3 = −0.050 (p = 0.039), opposite to H2, 6,593 startups, 27 clusters*
   With hype computed from past years only, β3 becomes significant but stays negative: the gap penalty on exit is about 5% larger in odds per SD of past hype. It does not support H2 either. Smaller sample.
4. **Team and lead-age controls**: *founders, MBA, AI term, young lead < 6 years, β1 and β3 unchanged*
   Adding founders, an MBA founder, an AI term and a young lead investor leaves the gap coefficients unchanged, so omitted team quality of this kind does not explain the null. A young lead goes with lower exit odds.
5. **Further checks (not in log)**: *finer hype, exit-market share, robust SEs, early exits removed, VIF < 2*
   Finer hype measures give β3 between −0.033 and −0.071, not significant. Robust SEs barely change p-values. Removing early one-round exits leaves β1 and β3 unchanged. VIFs are fine once the gap is centred.

#### Numbers (log)
- Windows: exit 4y β1 −0.0277 / β3 −0.0712 (**L1666, L1669**); exit 6y −0.0140 / −0.0650 (**L1864, L1867**); fail 4y −0.2851 / 0.0108 (**L2014, L2017**); fail 6y −0.1898 / 0.0234 (**L2173, L2176**).
- Exit ever β1 −0.4581 (**L2370**). Past-only hype β3 −0.0498, p 0.039 (**L2584**). Probit β3 −0.0284, p 0.390 (**L2758**).
- ⚠ **Table 12 (team and lead-age controls) is not in `regression_analysis.txt`**: it was run in Python (statsmodels). `rq1_addon_extra_controls.do` reruns it, but its log is not in the repo. Mark it "not in log" (RULES) and add it to open points.
- ⚠ Point 5: "paper §5.4, not in log" (open point 5).

#### Sources
- `gompers1996`: grandstanding predicts young VCs bring firms to IPO earlier. That our young-lead coefficient goes the other way is our result (R-xx), not the source's claim.
- `cameron2008`: as in 4.3.

#### Guardrails
- **"Robust SEs give the same p-value, so the few clusters do not matter" is not a substitute for the wild bootstrap.** That limitation is in 5.6. Here state only the check.
- The past-only hype result is evidence about H2's sign. Its *interpretation* (signal extraction) is in 5.5.
- Do not call the exit-ever coefficient a result for H1. It is a lesson on why the window is needed.

#### Editorial notes
- The abstract and conclusion say "stable across … hype measures". The past-only β3 becomes significant (same sign), so "stable in sign" is the honest wording.
- The deck needs at most one robustness slide: a coefficient plot across windows (Figures 20–21) plus a checklist of the rest.

#### Claude's additions
- [Likely] The "young lead goes with lower exit, opposite to grandstanding" finding is interesting but off the RQ. Keep it to one sentence in the paper, and leave it out of the deck.

### 5.5 Discussion of the results

**Role:** put the four verdicts together, discuss candidate mechanisms and compare with the literature (Tables 13–14).

#### Content
1. **Verdicts and the overall reading**: *Table 13, a slow second round is not a distress signal, less failure, larger step, flat exit*
   The four verdicts together: once a startup reaches round 2, a longer wait goes with lower failure, a larger valuation step and at most a slightly lower chance of exit. A slow second round is not a distress signal here.
2. **Staging intensity as a measure of risk (home of I-04)**: *leash, short rounds for hard-to-monitor ventures, our step to risk, both tails*
   Investors keep ventures with high agency or monitoring costs on short rounds. We argue that these ventures are also riskier, so fast raisers are on average riskier (I-04). That predicts their higher failure and a weak exit link, because risk fattens both tails.
3. **Learning before refinancing and priced progress (home of I-03)**: *longer test passed, survivors, priced progress (our argument), elasticity far below one*
   We argue that slow raisers have passed a longer test before round 2 and accumulated more progress, which round 2 prices. The elasticity far below one means they grow more slowly per month: more in total, less per unit of time.
4. **Why hype does not soften the penalty**: *signal extraction (see 2.3), past-only hype, exit-market timing, attenuation*
   The negative β3 fits the signal-extraction alternative of 2.3: in hot markets a slow round is more informative. A second reason is timing: hype at round 1 is a poor proxy for exit-market conditions years later, biasing β3 towards zero.
5. **What the controls add**: *round-1 size, CVC as acquirer, VC networks, angel groups, accelerators, selection vs influence*
   The strongest exit predictors are visible at round 1: size, age and lead type. We compare them with the literature (Table 14) rather than claim a match: the closest source finds that CVC-led first rounds are less likely to reach round 2 (Hochberg et al., 2007), a different outcome from our exit models. Following the selection literature, these coefficients mix the selection of better startups with what investors add.

#### Sources
- `gompers1995`, `tian2011`: shorter rounds where agency costs are higher (Gompers) or the VC is far, so monitoring is costlier (Tian).
- `bergemann2005`: uncertainty about the project resolves over time; funding slows as the investor's belief falls (theory).
- `cochrane2005`, `korteweg2010`: valuations are observed only at refinancing or exit, so observed valuations are a selected sample.
- `kaplan2003`: as in 5.3.
- `gompers1995`: VCs stage capital infusions to gather information (milestones appear only as a rival explanation he rejects).
- `gompers2000`, `nanda2013`: in hot markets capital chases deals, so prices rise (G&L) and investors fund riskier startups, worrying less about follow-on (N&RK).
- `howell2020`: early-stage VC deals fall sharply in recessions (no claim on follow-on funding).
- `gompers2008`: experienced VCs' hot-market deals show no significant drop in success.
- `lerner1994`: biotech IPOs cluster at peaks in equity valuations (1978–92).
- Control-sign comparisons, one source per line:
  - `hochberg2007`: first rounds led by corporate VCs are less likely to survive to the next round.
  - `haltiwanger2013`: the size–growth relationship vanishes once firm age is controlled for.
  - (`chemmanur2014`, `kerrlerner2014`, `yu2020` removed here: they report no control signs we can compare.)
- `sorensen2007`, `gompers2020`: VCs see selection as more important than value-add (survey); Sørensen estimates sorting ≈ 2× influence.
- `hoenen2014`: information asymmetries fall after round 1, so the patent signal stops mattering at round 2 (Table 14, H1 row).
- `guler2007`: VCs are reluctant to terminate as rounds accumulate (Table 14, H1b row).

#### Guardrails
- **Explanations, not limits.** "The negative failure coefficient is in part survivorship … not the effect of waiting" (v4) is a causal limitation, so it moves to 6.3. Here: "consistent with survivorship".
- Do not repeat the signal-extraction mechanism in full. It is in 2.3 (see 2.3 notes).
- No new numbers. Every number cited here has its home in 5.1–5.4.
- Mechanisms are "consistent with", "fits". The data cannot separate them (say so once).

#### Editorial notes
- v4 already says that the four explanations are not mutually exclusive and cannot be separated. Keep this sentence. It is the bridge to Section 6.
- Table 14 is long. In the paper keep it. In the deck, a 4-row version (H1, H1b, H2, H3) with "prediction / estimate / reading".

#### Claude's additions
- [Likely] Explanations 2 and 3 make **opposite** assumptions about who the fast raisers are: risky (leash) vs good (learning). Say which result discriminates between them, if any. Figure 19 is now read in 6.1 point 6 (I-01, decided 17/11), not as evidence against the leash: per-year growth faster for fast raisers is also compatible with I-04 (riskier ventures, fatter tails).

### 5.6 Limitations (narrowed: measurement and inference)

**Role:** limits that weaken *precision and measurement*, not the causal reading (those are in 6). Group decision D1.

#### Content
1. **Few clusters**: *41 clusters, sector × year, p-values too small, wild cluster bootstrap*
   Inference in the main exit models rests on 41 clusters. Robust SEs give almost the same p-values, but a wild cluster bootstrap would be the safer test and is not in our do-file.
2. **Competing outcomes modelled separately**: *exit, failure, still private, multinomial, competing risks*
   Exit and failure are competing outcomes, with a third state, still private, absorbing the rest. Separate logits do not use the three states jointly. A multinomial or competing-risks model would.
3. **Valuation measurement**: *post-money, fair value, terms ignored, disclosure, selected sample*
   The step uses post-money valuations, which overstate fair value and ignore contract terms other than the equity share, and it is observed for about half of two-round startups. If disclosure follows good rounds, the sample is selected towards high steps.
4. **What the sample represents**: *course cohort, hype from cohort's own deals, ageing cohort, disclosed round 1 only*
   Hype is built from deals of the course cohort (founded 2012–2019), so annual shares partly reflect its ageing. Dropping undisclosed round-1 amounts keeps only startups that disclosed. Both limit how far results generalise.
5. **Traceability**: *checks outside the do-file, Python, Table 12, not in log*
   The further checks in 5.4 and the team-control table were run outside the Stata do-file, partly in Python, so their numbers are not in the log that produces every other number in the paper and cannot be traced.

#### Sources
- `cameron2008`: wild cluster bootstrap for few clusters.
- `gornall2020`: post-money overstates fair value for US unicorns (48% on average).
- `ewens2022`: as in 2.4.
- `cochrane2005`: selection in observed valuations.

#### Guardrails
- **Not here:** associations vs causation, look-ahead in R, conditioning on round 2, unobserved quality. All are in 6.
- Do not list fixes in detail. One clause each ("a wild bootstrap would…"). Design extensions go in 6.4 and 7.

#### Editorial notes
- **D1 decided (16/11): split kept.**
- **D2/D3** as in the section map.

#### Claude's additions
- [Likely] Point 1 can be closed rather than listed: running `boottest` (wild cluster bootstrap) in Stata on the H2 model is a small addition to the do-file. That is new code and needs a group decision (open point 15). **Rejected 17/11 (Lele): not done.** Point 1 stays as a stated limitation.

---

## 6 Limitations to causality (NEW, title decided D2)

**Role:** explain precisely why every estimate is an association, which coefficients each problem affects, and what design would be needed for a causal claim. All four subsections are **Claude's proposal**. The group decides.

**Opening (no x.y):** two sentences. The design compares startups and does not assign the gap; this section lists the three channels through which the comparison departs from a causal one (6.1–6.3), and what would close them (6.4).

### 6.1 The gap is not assigned at random

#### Content
1. **Unobserved quality drives both**: *omitted variable, venture quality, team, speed and outcome, selection on unobservables*
   Startups choose, and are chosen for, their refinancing pace. Unobserved quality, such as team or traction, can shorten the gap and change exit or failure at the same time, so β1 mixes any gap effect with quality.
2. **The investor chooses the gap**: *staging as a leash, round length set for monitoring costs, reverse logic, endogenous treatment*
   Round length is partly the investor's choice, set according to agency and monitoring costs (and, we argue, risk: I-04, 5.5). A short gap can then reflect what the investor expects rather than cause anything, so the gap is endogenous to the outcome's determinants.
3. **Round-1 controls help, but only so far**: *fixed at round 1, no bad controls, round-2 mediators excluded, observables only*
   Controls are fixed at round 1, so they cannot be outcomes of the gap, and round-2 variables are excluded as mediators. This avoids bad controls but adjusts only for observables.
4. **Extra controls do not move β1, which is not proof**: *team controls, β1 unchanged, coefficient stability, residual bias*
   Adding founder, MBA, AI and young-lead controls leaves β1 and β3 unchanged. That is reassuring about these observables but does not rule out other unobserved quality. Stability is not identification.
5. **Hype is not exogenous either**: *sector-year shares, cohort composition, demand shocks, common shocks*
   Hype is a sector-year share of VC dollars. It moves with sector demand and opportunity shocks that can also affect exits, so β3 describes how the gap–exit association varies with hype, not what hype does.
6. **A larger total step is not value created by waiting (I-01)**: *total vs per-year step, time accumulates, θ1 > 0, Figure 19*
   We read the positive θ1 as a statement about elapsed time, not about waiting as a strategy: the total step is slightly larger after a long gap, but the step per year falls sharply with the gap (Figure 19). Waiting longer is not shown to create value.

#### Sources
- `sorensen2007`: sorting of better ventures to better investors outweighs influence.
- `gompers2020`: VCs rank the team as the top selection factor, somewhat ahead of business factors.
- `gompers1995`, `tian2011`: VCs set round length weighing agency and monitoring costs.
- `wang2004`: staging responds to moral hazard and risk.

#### Guardrails
- Point 4 only **points** to the numbers in 5.4. Do not repeat them.
- Do not repeat the leash mechanism (2.1). One sentence explaining why it makes the gap endogenous.
- Never write "we cannot rule out that the gap causes…". Write "β1 is an association that can mix…".

#### Editorial notes
- Course link: "omitted variable bias" and "endogenous regressor" (Hill, Griffiths and Lim 2018). Cite them from the course once the 21072 brain exists (open point 7). [Guessing] on chapter numbers. Do not write them until checked.

#### Claude's additions
- [Likely] Sign the likely bias where possible. If higher quality means faster refinancing and more exit, omitted quality makes β1 *more negative* than any true gap effect, which makes our null on exit even less of a penalty. Propose it as an inference (I-xx) for the group.

### 6.2 The group indicator looks ahead

#### Content
1. **R uses post-round-1 information**: *two_rounds, defined after round 1, look-ahead, future information*
   Whether a startup raises a second round is known only after round 1. Splitting the sample on R uses information from the future relative to the controls and hype, which are dated at round 1.
2. **Early outcomes block round 2**: *early exit, early failure, cannot raise again, mechanical link*
   A startup that fails or is acquired soon after round 1 cannot raise round 2. Part of the R = 0 group is therefore defined by the outcome itself, which builds a mechanical link between R and outcomes.
3. **So ρ1 is not interpreted**: *ρ1, group difference, selection plus mechanics, not the effect of raising again*
   ρ1, the coefficient of R, mixes selection of better startups into round 2 with this mechanical link. It is reported but not read as the effect of raising a second round.
4. **β1 and β3 are much less affected**: *within two-round group, early exits removed, β1 unchanged, β3 unchanged*
   β1 and β3 are estimated within the two-round group, so the look-ahead affects them much less. Removing the one-round startups that exited or failed within 13 months leaves them unchanged (5.4).

#### Sources
- None in `fonti.bib` specific to look-ahead. If the group wants a citation: survival analysis with a time-varying covariate (course or a methods text). ⚠ Not in `fonti.bib`. Ask before adding.

#### Guardrails
- Report the numbers of the early-exit check only in 5.4. A pointer here.
- ρ1's values are in 5.1/5.2. Do not repeat them.

#### Editorial notes
- RULES lists this limit explicitly ("Do not interpret ρ1 as an effect"). The wording must match.

#### Claude's additions
- [Likely] One sentence with an example (a startup acquired 8 months after round 1 is in R = 0 *because* it exited) makes this concrete for the audience.

### 6.3 Conditioning on refinancing: survivorship

#### Content
1. **β1 and β3 describe refinanced startups only**: *conditional on round 2, refinanced startups, scope, not all round-1 startups*
   The gap exists only for startups that reached round 2, so β1 and β3 describe how speed relates to outcomes among refinanced startups, not among all startups that raised a first round.
2. **The window starts after the gap**: *outcome window at round 2, survived the gap, positive selection, slow raisers survivors*
   For two-round startups the window opens at round 2, so a slow raiser has already survived a long gap. Slow raisers are positively selected on survival, which pushes the failure coefficient negative.
3. **What survivorship means for the failure result**: *real association, investor at round 2, not the effect of waiting, failure result*
   The negative failure coefficient is partly this survivorship. It is a real association, and it is exactly what an investor observing round 2 sees, but it is not the effect of waiting longer before raising again.
4. **Raw evidence that fits**: *still private rises, failure falls, exit flat, Figure 8*
   The raw three-way split in Figure 8 fits this reading: across gap quintiles, slow raisers fail less and stay private more, without exiting more. Survivorship predicts exactly this pattern; a pure distress story does not.
5. **What the gap measures (I-02)**: *survived and achieved, not how it is doing, state not lever, founder vs investor*
   We read the gap as a measure of how much a startup has already survived and achieved before round 2, not of how it is doing: less failure, a larger total step and a flat exit link. It describes a state an investor observes, not a lever a founder can pull.

#### Sources
- `cochrane2005`, `korteweg2010`: valuations observed only at refinancing or exit are a selected sample.
- `puri2012`: timing of failure over the life cycle.

#### Guardrails
- The mechanism (prediction) is in 2.2 and the interpretation in 5.5. Here only the **consequence for causal reading**. Do not explain the theory again.
- Figure 8 is shown in 3.3. Point to it here, do not reproduce it.

#### Editorial notes
- This subsection directly qualifies the strongest result of the paper (failure). It should be the clearest paragraph of Section 6.

#### Claude's additions
- [Likely] Distinguish *selection bias* (a threat to causal reading) from *a selected population* (a scope condition). Survivorship is the second for an investor at round 2 and the first for a founder asking "should I wait?". This difference matters for the conclusion's founder implication.

### 6.4 What a causal design would need

#### Content
1. **Survival model from round 1**: *hazard model, round 2 as time-varying covariate, all at risk from round 1, removes look-ahead*
   A survival model with round 2 as a time-varying covariate would treat all startups as at risk from round 1 and remove the look-ahead in R. It still estimates associations but fixes 6.2.
2. **Exogenous variation in the gap**: *supply shock, investor capital, natural experiment, quality-unrelated delay*
   A causal gap effect needs variation in the gap unrelated to venture quality, such as shocks to investors' capital that delay rounds for reasons outside the venture. We have no such shock in our data.
3. **Discontinuity designs**: *regression discontinuity, funding threshold, comparable startups, financing effect*
   Discontinuity designs compare startups just above and just below a funding threshold, which isolates the effect of financing itself. Nothing in our data provides such a threshold for the gap between rounds, so this route is closed here.
4. **What we can honestly claim**: *conditional associations, investor at round 2, founder choice, descriptive claim*
   Without these designs the paper offers conditional associations. They describe what an investor at round 2 can infer from the pace of refinancing, not what a founder gains by raising faster or slower.

#### Sources
- `kerrlerner2014`: regression-discontinuity evidence on angel-group funding (a model of point 3).
- `li2008`: Weibull duration model of time between rounds, with right-censoring (a model of point 1).
- `howell2020`: VC activity falls in recessions, mostly early-stage; capital-supply frictions are one likely mechanism.

#### Guardrails
- Section 7 must not list these extensions again in full. One sentence pointing back to 6.4.
- Do not suggest we will run these designs before the deadline unless the group decides it.

#### Editorial notes
- v4 places the survival model among the extensions in its conclusion. Move it here and keep in 7 only the non-causal extensions (exit-market timing, growth per year).

#### Claude's additions
- [Likely] Point 4 is the sentence that should survive into the deck's limits slide almost verbatim.

---

## 7 Conclusions and discussion (was 6)

**Role:** answer the question, give implications, and close with what is left open. No new numbers.

### Content
1. **The answer**: *no meaningful association with exit, no hype moderation, less failure, larger step*
   In 9,263 US startups with a fully observed five-year window, the gap has a small, negative, insignificant association with exit, and hype does not change it as expected. A longer gap goes with less failure and a larger step.
2. **Robustness in one line**: *windows, estimators, hype measures, stable in sign*
   The pattern holds across four- to six-year windows, logit, probit and linear probability models, and hype measured at several levels, at least in sign: with past-only hype, β3 becomes significant and stays negative.
3. **For founders and investors**: *slow round not a bad sign, round-1 information, round size, lead type*
   For founders, a slower second round is not in itself a bad sign. For investors, the pace of refinancing seems to carry little information about exit beyond what is visible at round 1, such as size and lead type.
4. **For the staging literature**: *accumulated progress and survival, not distress, selection view, our progress reading, hype makes slowness informative*
   The findings fit the selection account and our accumulated-progress reading (I-03, 5.5) better than the good-news reading; what the gap measures, and what it does not, is in 6.3 (I-02). Hype, if anything, makes a slow round more informative.
5. **What remains open**: *exit-market conditions, timing account of H2, growth per year, pointer to 6.4*
   Two extensions sharpen the descriptive picture: exit-market conditions measured at the time of exit, to test the timing account of H2, and growth per year rather than the total step. Causal extensions are in 6.4.

### Sources
- `cochrane2005`, `korteweg2010`, `kaplan2003`: pointers to the views the results fit.

### Guardrails
- No numbers beyond the sample size. Every estimate has its home in 5.x.
- The founder implication must respect 6.3: "is not in itself a bad sign" (descriptive), never "founders should wait".
- Do not repeat the causal designs (6.4).

### Editorial notes
- v4 says "the answer to both parts is no". Fine, but add "in this sample" and "in association".
- The deck's last slide = points 1, 3 and the 6.4 point-4 sentence.

### Claude's additions
- ~~End on the reframing (I-02).~~ Superseded 17/11 (Lele): I-02 has its home in 6.3. The closing line of the deck is still to choose (open point 21).

---

## Claude's additions: for the next steps

### A. Glossary: done, see `glossary.md` (16/11). Candidate list kept for history
Terms that drift in v4 or across documents, which the glossary must fix:
- **gap** / time between rounds / refinancing speed / months between rounds: one canonical term in prose ("gap"), defined once.
- **two-round / one-round startups** vs R = 1 / R = 0 vs "startups that raised again". Pick one.
- **hype** vs heat vs hot/cold market: *hype* in prose, `heat` in code; "hot" and "cold" = +1 / −1 SD, terciles only in the figures.
- **exit** (IPO or acquisition, first one) vs **exit_5y** vs exit ever.
- **failure** vs failure_5y. **Still private** as the third state.
- **outcome window** and its start (round 2 vs round 1).
- **full sample** (28,478) vs **estimation sample** (9,263) vs **valuation sample** (7,574). ⚠ `construction.pdf` uses "estimation sample" for 28,478.
- **valuation step** vs step-up vs ln(V2/V1).
- **staging**, real option, leash, signal extraction, survivorship, look-ahead.
- **odds ratio**, **AME (pp)**, LPM, clustered SEs, interaction effect.
- Forbidden variants (RULES): *effect / impact / causes / leads to / reduces* (about the gap or hype) → *is associated with / goes with*.

### B. Points added to `registers/open points.md` on 16/11 (items 9–12, 14)
1. Table 12 (team and lead-age controls) is not in the Stata log: Python run, and the add-on log is not in the repo.
2. "Estimation sample" means 28,478 in `construction.pdf` and 9,263 in the paper.
3. `nanda2017` and `townsend2015` are cited but not downloaded (D4).
4. Abstract/conclusion "stable across hype measures" vs the significant past-only β3.
5. AMEs use N = 4,444 two-round startups, not 4,483 (log L659).
6. Figures 8, 17 and 19 (and Figure 1, a schematic) are not exported by `rq1_two_group_analysis_v2.do`: their numbers cannot be traced to the log.

### C. Deck (kept in mind only)
- [Guessing] About 14–16 slides for 25 minutes: 1 hook/RQ, 1 literature + hypotheses (Table 1 slim), 1 design (Figure 1), 1 sample funnel, 1 hype measure (Figure 4), 1 raw picture (Figure 8), 1 model "how to read", 3 results (H2/H1 Figure 12, H1b Figure 16/17, H3 Figure 19), 1 robustness, 1 discussion (Table 14 slim), 1 limits to causality, 1 conclusion, plus backup.
- Every section above names its "deck" visual in the editorial notes, so the outline can be derived from this file.

### D. From this scaletta to the skill's `scaletta/scaletta.md`
The skill (`skill-redigere essay`) has its own syntax (`parole:`, `ruolo:`, `punti:`, `aggancio:`, `trappole:`). Once the group approves this draft, the mapping is: **Role → ruolo**, **Content → contenuto**, **Guardrails → trappole**, **Sources → punti** (after `/essay-estrai` has validated the points `fonte#n`). Word budgets (`parole:`) still need to be decided. v4 is about 9,000 words of prose plus tables. [Guessing] on the target length of the final paper: the brief asks only for a deck.
