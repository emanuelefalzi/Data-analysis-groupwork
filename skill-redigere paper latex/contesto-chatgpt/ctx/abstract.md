# Contesto — abstract

Parole obiettivo: 150 (±15%).
Ruolo: domanda, disegno, tre risultati in direzione, una frase sui limiti. Nessun numero oltre a N e ai tassi gia' nel testo. Nessuna citazione.

## Materiale: i DRAFT gia' scritti

**1 Introduction**
Venture capital (VC) arrives in stages, and at each stage investors decide whether to refinance the startup. The time between the first and the second VC round (the gap) is one of the few signals of progress that founders, investors and other outsiders can observe. Whether a short gap signals strength or a long gap signals distress is the question we ask.

The answer may depend on the market. In hot markets capital is abundant, rounds close fast and screening may be looser, so a fast round may say less about the startup. This motivates a two-part question: is the gap associated with the probability of exit, and does hype, the sector's share of VC dollars, change that association?

To answer it we use PitchBook data on 28,478 US startups. We keep every startup with a disclosed first VC round and split it into those that raised a second round and those that did not, so that we never condition on reaching round 2. The gap enters the model only for the first group. The main outcome is exit within five years, and hype is the sector's VC share in the year of round 1, z-scored within the sector.

Three results stand out. First, startups that raise a second round exit more and fail less, an association we report and do not read as an effect of refinancing. Second, among two-round startups a longer gap is not significantly associated with exit, and hype does not change this. Third, a longer gap goes with less failure and with a larger step in valuation between the two rounds.

The paper connects three literatures with one design. Staging studies relate the number and length of rounds to outcomes: round duration falls as expected agency costs rise, and ventures that go public get more rounds ([[CIT-P:gompers1995]]). More and shorter rounds go with a VC located far from the firm, and more rounds go with better IPO outcomes only for distant firms ([[CIT-P:tian2011]]). Round durations also respond to uncertainty, as a real-options view predicts ([[CIT-P:li2008]]). Hot-market studies find that inflows into VC funds go with higher prices of private deals ([[CIT-P:gompers2000]]), and that startups first funded in hot markets go bankrupt more often while those that go public are valued higher and patent more ([[CIT-P:nanda2013]]). Selection studies note that private-firm returns are observed only at financing events and are therefore selected upward ([[CIT-P:cochrane2005, korteweg2010]]). In our setting, startups with a long gap that are refinanced may look safer once refinanced. The contribution is to link staging, hot-market cycles and selection in a single design that keeps the one-round startups in the sample.

**2 Theory, literature and hypotheses**
We state each hypothesis in the direction in which staging is good news, and next to it we give the competing prediction that the opposite reading of the gap would produce. [[TAB:T1]] lists the hypotheses with their competing predictions.

**2.1 What the time between rounds measures**
Staging gives investors an abandonment option [[CIT-P:cornelli2003]]. VC-controlled ventures are more likely to have cash-flow and control rights contingent on observable milestones [[CIT-P:kaplan2003]]. Staging models predict screening through discontinuing ventures with poor early results [[CIT-P:dahiya2012]]. In our setting, investors can abandon after new information. On this reading, the gap between the first and the second VC round represents the time needed to produce investable news.

Under Bayesian learning, each period without success lowers investors' belief that a project is good [[CIT-P:bergemann2005]]. In software and services, the VC round is an experiment that buys information [[CIT-P:kerrnanda2014, ewens2018]]. In our setting, fast positive signals go with faster refinancing of good projects: a short gap reads as good news.

The leash view treats round length as a governance choice: rounds are shorter when agency or monitoring costs are higher. Greater investor distance was associated with more rounds and shorter intervals between them [[CIT-P:tian2011]]. In our setting, we argue that a short gap may mark a venture that is harder to monitor and riskier, giving the competing prediction.

Evidence links outcomes to the number and size of rounds, rarely to time. Patent applications were associated with larger first-round funding but not second-round funding in US biotechnology [[CIT-P:hoenen2014]]. We read the fading patent signal as reflecting information already known to investors by round 2. We know of no study relating the gap to exit while retaining one-round startups.

H1 states that, among two-round startups, a longer gap is associated with a smaller probability of exit within five years. For β1, the coefficient of R × ln(1 + months), this predicts β1 < 0. The competing leash view predicts β1 ≥ 0.

**2.2 Failure and survivorship**
Staging models predict abandonment when early returns disappoint [[CIT-P:bergemann2005, dahiya2012]]. In our setting, refinancing after good news implies cutting off stalled ventures: a long gap between the first and the second VC round should go with more failure, extending the real-option and screening arguments in [[SEC:2.1]].

VCs became less likely to terminate investments over successive rounds despite declining expected returns; politics may contribute [[CIT-P:guler2007]]. The model predicts that optimal contracts for innovation tolerate early failure [[CIT-P:manso2011]]. In our setting, continued funding under political and institutional pressures and tolerance for failure may weaken the predicted association between a long gap, abandonment and failure.

VC returns are observed only at financing events and are subject to selection [[CIT-P:cochrane2005]]. Estimates of VC risk and return were corrected for selection in observed valuations [[CIT-P:korteweg2010]]. In our setting, values and outcomes observed at financing events concern firms that remain alive and are worth more, selecting returns upward. A two-round startup has survived its gap. Conditioning on refinancing therefore predicts that two-round startups with a long gap look safer.

VC-backed and comparable non-VC firms differed in the timing of failure and acquisition [[CIT-P:puri2012]]. In our setting, the clock's starting point matters for measuring failure, motivating an explicit outcome window; for two-round startups, ours starts at round 2 ([[SEC:3.2]]).

H1b states that a longer gap is associated with a higher probability of failure within five years among two-round startups, predicting a positive gap coefficient in the failure model. Survivorship and tolerance for failure give the competing prediction of a negative gap coefficient.

**2.3 Hot and cold markets**
Fund inflows were associated with higher private-deal valuations [[CIT-P:gompers2000]]. VC investment responded to industry Q [[CIT-P:gompers2008]]. IPO waves reflect changing market conditions [[CIT-P:pastor2005]]. Theory predicts that greater VC competition weakens investors' bargaining power and raises valuations [[CIT-P:inderst2004]]. In our setting, we view hype as a capital-supply condition, that is, as abundant capital.

Hot-market cohorts had more bankruptcies, but their IPO firms had higher valuations and more patents [[CIT-P:nanda2013]]. Investors in hot markets funded riskier ventures with less concern about follow-on financing risk [[CIT-P:nanda2013]]. These cohort differences are discussed in [[SEC:1]].

Early-stage VC deals fell sharply during recessions [[CIT-P:howell2020]]. In our setting, we argue that follow-on funding in cold markets depends partly on capital supply, not only on venture quality.

The gap between the first and the second VC round mixes market and venture components. If rounds close quickly for everyone in hot markets, a long gap is less informative about the venture. Our key hypothesis, H2, predicts a weaker negative association between the gap and exit within five years in hot markets: β3 > 0.

We propose signal extraction as a competing argument: in cold markets, most ventures wait, so a long gap says little about venture quality. We argue that, with easy money in hot markets, a long gap indicates investors chose not to fund quickly and is more informative about the venture. We cautiously predict β3 < 0 under this alternative.

**2.4 Valuation steps**
Refinancing is more likely after value has risen. Observed returns between rounds are selected upward [[CIT-P:cochrane2005, korteweg2010]]. In our setting, if fast rounds follow good news, they should carry larger valuation steps. H3 predicts that, among two-round startups, a longer gap is associated with a smaller valuation step (θ1 < 0), defined as ln(post-money valuation at round 2 / post-money valuation at round 1).

We argue that rounds are priced on accumulated venture achievements. A longer gap allows more time for progress, potentially going with a larger total valuation step even with slower monthly value growth (θ1 > 0). Milestones govern disbursement of committed capital and some contractual rights within a round [[CIT-P:kaplan2003]]. In our setting, the accumulated-progress counter-prediction is our argument, not a literature prediction about the timing of the next round.

Later investors hold senior preferred shares, so post-money valuations overstate fair value. Reported post-money valuations averaged 48% above fair value for 135 US unicorns [[CIT-P:gornall2020]]. Post-money valuation poorly measures firm value because contractual provisions beyond equity ownership are omitted [[CIT-P:ewens2022]]. In a study of MIT start-up offers, entrepreneurs accepted lower valuations from more reputable VCs [[CIT-P:hsu2004]]. In our setting, measured valuation steps therefore mix value with contractual terms and bargaining power. Measurement limitations are discussed in [[SEC:5.6]].

Prices were positively associated with capital inflows [[CIT-P:gompers2000]]. In our setting, hype could be associated with the valuation step directly and could moderate its association with the gap. We therefore include hype and gap × hype in the H3 model, with θ3 capturing the latter association.

**2.5 Controls: what they absorb and what the literature expects**
VCs surveyed ranked teams first in selection and considered deal selection more important than value-add [[CIT-P:gompers2020]]. Sorting of better ventures to better investors mattered more than investor influence for differences in IPO rates [[CIT-P:sorensen2007]]. In our setting, variables correlated with quality can appear predictive, so we use only controls fixed at round 1. [[TAB:T2]] summarises their mechanisms and expected signs.

We argue that a larger first VC round buys runway and reflects investor conviction and syndicate quality. In software and services, cheaper experimentation went with smaller initial cheques across more ventures [[CIT-P:ewens2018]]. In our setting, small first rounds can represent experimental bets. We expect larger first rounds to be associated with more exit within five years, less failure and a smaller valuation step.

Young firms exhibit an up-or-out pattern: survivors grow rapidly, but young firms frequently leave the market [[CIT-P:haltiwanger2013]]. In our setting, older firms at round 1 have survived and established a track record. Earlier deals capture experimentation already financed by angels or others, including seed financing. For age and earlier deals, we expect less failure and a smaller valuation step.

Lead-investor types differ in selection and influence. VC backing went with professionalisation [[CIT-P:hellmann2002]]. Better-networked VCs see more exits. VCs with greater IPO-capitalisation shares were associated with more successful exits and faster IPOs [[CIT-P:nahata2008]]. Closer VC monitoring, after cuts in travel time, went with higher innovation and IPO rates [[CIT-P:bernstein2016]]. CVCs back innovative firms and acquire them. Ventures funded by angel groups are more likely to survive, and some accelerators speed up development. Young VCs took firms public earlier, consistent with grandstanding [[CIT-P:gompers1996]]. In our setting, lead-investor coefficients mix selection and influence.

We include HQ state fixed effects to absorb VC's geographic concentration, sector fixed effects to absorb possible industry differences in success rates and maturation speed, and year-quarter fixed effects to absorb exit-market windows. Standard errors allow correlation among startups funded in the same sector and year, with clustering by sector × year of round 1, the level at which hype is assigned.

**3.1 Sample construction**
We used the course PitchBook extract: a startup file covering 57,751 US startups founded in 2012–2019, a deal file, and deal-investor and investor files identifying each round's lead investor.

A VC round is a completed, dated Seed, Early Stage or Later Stage VC deal, excluding angel, grant, debt and accelerator deals. We merged same-day VC deals of each company into one round, summing their amounts.

[[TAB:T3]] reports sample construction. We retained startups with at least one VC round, a gap between the first and the second VC round of at most ten years, and no exit or failure before round 1. Dropping undisclosed round-1 amounts yielded the full sample of 28,478 startups: 15,518 two-round startups and 12,960 one-round startups.

A zero denotes no exit only when the entire outcome window is observed. Requiring the five-year window to end by 30 June 2022 gives the estimation sample of 9,263 startups: 4,483 two-round startups and 4,780 one-round startups.

We treated round 2 after 30 June 2022 as no round 2. Dropping rather than imputing undisclosed round-1 amounts avoids assuming they are missing at random. We retained missing states as "Unknown".

**3.2 Variables**
We define R as 1 if a second VC round closed by 30 June 2022 and 0 otherwise. The gap between the first and the second VC round is measured in months. Its right-skewed distribution motivates R × ln(1 + months), keeping one-round startups in the sample at zero.

An exit is the first IPO or acquisition; failure uses PitchBook's failure date. The outcome window opens at round 2 for two-round startups and at round 1 for one-round startups. We use five years for the main outcome window, with four- and six-year windows for robustness.

[[TAB:F1]] shows this timing schematically. Two-round startups enter their outcome window only after surviving the gap, while round-1 controls, hype and fixed effects are dated at round 1. This timing informs our reading of the failure result.

Hype is the sector's share of all VC dollars in the year of round 1, z-scored within each of seven sectors over 2012–2022. Raw shares measure sector size, whereas the z-score measures a sector's position relative to its own norm: +1 denotes one standard deviation above that norm.

[[TAB:T4]] reports the variable definitions. The valuation step is ln(post-money at round 2 / post-money at round 1). Round-1 controls comprise log round-1 amount, number of deals so far, age at round 1 and lead-investor type (16 categories). We include year-quarter, sector and state fixed effects.

**3.3 Descriptive statistics**
In the estimation sample, two-round startups differ sharply from one-round startups ([[TAB:T5]]). Their exit-within-five-years shares are 22.2% and 15.6%, respectively; failure shares are 12.4% and 31.6%. Both differences are significant in t-tests. Two-round startups also raised larger first VC rounds and were younger at round 1.

The gap between the first and the second VC round has a median of about 13 months and a mean of 14.7 months among two-round startups. Its long right tail, shown in [[FIG:F2]], motivates the log specification and the use of the interquartile range for magnitudes.

[[FIG:F3]] shows the cohort truncation: the one-round share jumps after 2019 because recent cohorts had insufficient time to raise another VC round. Restricting the comparison to fully observed outcome windows removes this mechanical pattern from the group comparison.

Hype varies over time within every sector ([[FIG:F4]]). IT is cold in 2015–2019, healthcare peaks in 2020, and Energy has an outlier in 2012, when very few deals were recorded. Within-sector variation identifies H2 once sector fixed effects remove permanent differences between sectors.

[[FIG:F5]] presents exit and failure within five years by sector, while [[FIG:F6]] presents exit within five years by group and market hype. [[FIG:F7]] breaks down exit within five years by gap quintile and market hype. We use these raw patterns descriptively; the H1 and H2 tests are in [[SEC:5.1]] and [[SEC:5.2]].

Across gap quintiles, the exit share barely moves, the failure share falls and the share still private rises ([[FIG:F8]]). A long gap is followed more by staying private than by exit. These are raw shares of competing outcomes, without controls.

[[FIG:F9]] shows the distribution of the round-1 amount by group, complementing the comparison of first VC rounds in [[TAB:T5]]. [[FIG:F10]] reports exit within five years by lead-investor type.

**4.1 Main specification**
We estimate a logit of exit within five years for both groups. It includes R (indicating two-round startups), R × ln(1 + months), hype, round-1 controls and three sets of fixed effects, first without, then with, R × hype and R × ln(1 + months) × hype.

β1 and β3 use variation only among two-round startups because R multiplies the logged gap. One-round startups help estimate controls and fixed effects; ρ1 and ρ2 compare groups. We report ρ1 without interpretation ([[SEC:6.2]]).

In logit and probit, the interaction coefficient differs from the probability-scale interaction [[CIT-P:ai2003]]. In our setting, the logit coefficient measures a log-odds slope change; the probability-scale interaction can differ in size and sign and needs its own standard error. Marginal effects are recommended for estimating and presenting nonlinear interactions [[CIT-P:mize2019]]. In our setting, we report average marginal effects (AMEs) in percentage points. These describe the logged gap association at hype −1, 0 and +1 standard deviations.

H2 has three readings that should agree: β3, the log-odds slope change; the hot-minus-cold AME difference (delta method); and the linear probability model (LPM), where the interaction coefficient and probability-scale interaction coincide.

The logit uses 9,124 of the 9,263 startups in the estimation sample because Stata drops perfectly predicting cells; the LPM retains 9,262. Standard errors allow correlation among startups funded in the same sector and year, clustering by sector × year of round 1 across 41 clusters. With few clusters, p-values can be too small; checks appear in [[SEC:5.4]] and limitations in [[SEC:5.6]].

**4.2 Other outcomes**
For H1b, we estimate the same logit equation for failure within five years, using the exit model's estimation sample, controls, fixed effects and clustering.

For H3, we regress the log valuation step on the logged gap, hype and their interaction using OLS, with the same round-1 controls and fixed effects. Only two-round startups enter.

The step is observed at round 2, so no outcome window is needed. The valuation sample comprises 7,574 of 15,518 two-round startups with both post-money valuations, with 73 sector × year of round 1 clusters.

Both the step and the gap are logged, making θ1 an elasticity. Age and earlier deals enter in levels, so their coefficients are semi-elasticities. Magnitudes are reported in [[SEC:5.3]].

**4.3 Robustness tests**
We re-estimate the main equation as a linear probability model, with β3 in probability units, and a probit. Agreement would indicate that logit nonlinearity does not drive the interaction result.

Four- and six-year exit and failure models use fully observed outcome windows. Large movements in β1 or β3 would call the five-year choice into question.

Dropping the outcome window, we estimate exit at any time: 28,478 startups enter, and 27,944 are used, with 77 sector × year of round 1 clusters. Stata drops categories that perfectly predict the outcome. This check mixes the gap with remaining follow-up time.

Past-only hype uses a z-score based only on the sector's past years. This smaller-sample check restricts information to that available at round 1, avoiding look-ahead from future years of the same sector.

Further checks use finer hype and robust rather than clustered standard errors, exclude early one-round exits and failures, examine variance inflation factors, and add team and lead-investor-age controls in the subsample with founder data. Results are reported in [[SEC:5.4]].

**5 Results**
Every logit coefficient is a change in log-odds. We also report the odds ratio, exp(β), and the average marginal effect (AME) in percentage points. The linear probability model coefficient is already in probability units and checks the AME.

The gap enters as ln(1 + months), so one unit multiplies 1 + months by 2.7. A 10% longer gap goes with a log-odds difference of about β/10. Magnitudes use the interquartile range of ln gap, 2.24 to 3.02, which is 8 to 19 months.

In the interacted model the gap slope is β1 + β3 · hype. β1 is the slope at average hype, and β3 is its change per standard deviation of hype. ρ1 is the group difference at a zero-month gap, outside the data.

Unconditional five-year rates give the scale: 22.2% of two-round and 15.6% of one-round startups exit, and 12.4% and 31.6% fail. A two-point change in exit is about a tenth of the two-round rate.

**5.1 Exit (H1 and H2)**
[[TAB:T6]] reports logit estimates for exit within five years among one-round and two-round startups of the estimation sample (full outcome window). Standard errors are clustered by sector × year of round 1, allowing errors to be correlated among startups funded in the same sector and year. For the gap between the first and the second VC round, the baseline logit coefficient β1 is −0.089 (p = 0.188; odds ratio 0.915): a 2.7-fold longer gap goes with 8.5% smaller exit odds. The coefficient interval includes zero. H1 is right sign, not significant: we cannot distinguish a small negative association from none.

With hype interactions, the logit coefficients are β1 = −0.071 (p = 0.294) and β3 = −0.056 (p = 0.344). The gap slope is steeper as hype rises, opposite to H2, but the interaction coefficient is not significant. H2 is not supported.

[[TAB:T7]] reports average marginal effects (AMEs) for 4,444 two-round startups. Per unit of ln(1 + months), the AME is −0.3 percentage points in cold markets (p = 0.883) and −2.1 percentage points in hot markets (p = 0.068). Cold and hot denote hype at −1 and +1 standard deviation. The hot-minus-cold difference is −1.9 percentage points (p = 0.327), as shown in [[FIG:F11]]. The linear probability model agrees, with OLS coefficients β1 = −0.0121 (p = 0.271) and β3 = −0.0083 (p = 0.385).

In [[FIG:F12]], predicted exit within five years stays near 22% in cold markets. In hot markets, a gap of about 2 months corresponds to about 26%, compared with about 20% at 4½ years. The bands overlap throughout.

[[FIG:F13]] presents predicted exit probabilities for one-round and two-round startups by hype. The coefficient ρ1 of the two-round group indicator is reported in [[TAB:T6]]; we do not interpret it as an effect, for the reasons discussed in [[SEC:6.2]].

[[FIG:F14]] displays the main exit-model coefficients. Round-1 size has an odds ratio of 1.64, while age at round 1 is associated with 10% higher exit odds. Relative to no identified lead, angel-group, CVC and VC leads are associated with 94%, 55% and 39% higher exit odds, respectively. These associations are larger than the gap association: moving across the gap interquartile range corresponds to less than one percentage point in exit probability.

**5.2 Failure (H1b)**
[[TAB:T8]] reports failure logit estimates for 9,235 startups. Standard errors are clustered by sector × year of round 1, allowing errors to be correlated among startups funded in the same sector and year. The gap logit coefficient β1 is −0.241 (p = 0.001) at baseline and −0.231 (p = 0.005) with interactions. The latter corresponds to an odds ratio of 0.794: a 2.7-fold longer gap goes with 21% smaller failure odds. H1b is rejected, opposite sign.

We report average marginal effects (AMEs) in percentage points, for 4,469 two-round startups. At average hype, the AME is −2.4 percentage points per unit of ln(1 + months) (p = 0.003). Across the gap interquartile range, the association amounts to −1.9 percentage points against mean failure of 12.4%, about 15% smaller in relative terms.

The gap × hype logit coefficient β3 is −0.030 (p = 0.681), providing no evidence of moderation by hype. [[FIG:F15]] shows AMEs of −2.1 percentage points (p = 0.115) in cold markets and −2.8 percentage points (p = 0.001) in hot markets, defined as hype at −1 and +1 standard deviation. In [[FIG:F16]], predicted failure is about 15–18% at a gap of about 2 months and about 9% at about 4½ years in both markets.

Larger first rounds and older startups are associated with 37% and 8% lower failure odds, respectively, mirroring the exit associations with opposite signs. Lead-investor type does not predict failure: its association concerns the upside rather than the downside. The two-round group coefficient ρ1 is reported in [[TAB:T8]]; we do not interpret it, for the reasons discussed in [[SEC:6.2]].

[[FIG:F17]] checks functional form using Frisch–Waugh–Lovell binned residuals after partialling out controls and fixed effects. For 4,482 two-round startups, the failure OLS slope is −0.0304 (SE = 0.0092, p = 0.002). Failure declines steadily across the range of ln(1 + months), supporting the log form without dependence on a few extreme gaps. The exit bins are flat.

**5.3 Valuation step (H3)**
[[TAB:T9]] reports OLS estimates for the valuation sample of 7,574 two-round startups. Standard errors are clustered by sector × year of round 1, allowing errors to be correlated among startups funded in the same sector and year. The OLS coefficient θ1 on the gap between the first and the second VC round is 0.109 (p < 0.001). H3 is rejected, opposite sign. This elasticity associates a 10% longer gap with a valuation step about 1% larger, and a move from 8 to 19 months across the interquartile range with a step about 8.9% larger.

The gap × hype OLS coefficient θ3 is −0.016 (p = 0.381), providing no evidence of moderation by hype. In [[FIG:F18]], the predicted log step rises from about 0.9–1.0 at very short gaps to about 1.2 at four years in both cold and hot markets, defined as hype at −1 and +1 standard deviation.

Larger first rounds have an OLS coefficient of −0.139. Older startups and more earlier deals are associated with steps 6.1% and 4.2% smaller, respectively (percentage changes are exp(coefficient) − 1 of the coefficients in [[TAB:T9]]), consistent with part of the growth being priced at round 1. Accelerator-led first rounds go with steps 33% larger. We discuss the pricing interpretation in [[SEC:5.5]] and the post-money and disclosure caveats in [[SEC:5.6]].

For 7,514 startups, [[FIG:F19]] shows a mean total valuation step approximately flat across the first four gap quintiles and higher, at 1.18 log points, in the longest-gap quintile. The median step per year falls from 1.89 to 0.36 log points: startups with short gaps gain value about five times faster per year. We read the positive θ1 as total progress accumulated before round 2 rather than speed of value creation, consistent with the competing prediction in [[SEC:2.4]]. Speed of value creation favours startups with short gaps.

**5.4 Robustness**
[[TAB:T10]] reports logit coefficients across four-, five- and six-year outcome windows. Exit β1 and β3 are never significant; failure β1 is negative and significant throughout, while failure β3 remains close to zero. These conclusions do not depend on the five-year choice. Standard errors are clustered by sector × year of round 1, allowing errors to be correlated among startups funded in the same sector and year, except where alternative clustering or standard errors are specified. The tables report ρ1, the coefficient on the two-round indicator; we do not interpret it, for the reasons in [[SEC:6.2]].

[[TAB:T11]] reports the estimator and hype checks. Probit preserves the signs and significance, with interaction coefficient β3 = −0.028 (p = 0.390). For exit at any time, the logit coefficient β1 = −0.458 is not comparable with the windowed estimates: long-gap startups have less follow-up time after round 2, mixing the gap association with time at risk. With past-only hype, logit β3 = −0.050 (p = 0.039) in a smaller sample of 6,593 startups and 27 clusters. The gap association with exit odds is about 5% more negative per standard deviation of past-only hype. It does not support H2 either: the coefficient is stable in sign, not significance. We discuss its interpretation in [[SEC:5.5]].

In [[TAB:T12]], adding the number of founders, an MBA founder, an AI term and a young lead investor, aged less than six years, leaves β1 and β3 essentially unchanged. The exit and failure samples contain 7,591 and 7,685 startups, respectively, with 41 clusters. Omitted team quality of this kind does not explain the null results. A young lead is associated with lower exit odds (odds ratio 0.716, p = 0.009). [[CIT-N:gompers1996]] predicts earlier IPOs for firms backed by young VCs. In our setting, the young-lead association concerns exit within five years.

[[FIG:F20]] and [[FIG:F21]] show the exit and failure coefficient patterns across outcome windows. Further checks address hype measurement and inference. With sector × quarter, industry group × year and industry group × quarter hype, the logit interaction coefficients β3 are −0.036 (p = 0.405), −0.070 (p = 0.280) and −0.078 (p = 0.090), respectively, using 149, 190 and 570 clusters. None is significant at 5%. The all-quarter base gives β3 = −0.057 (p = 0.368); adding sector exit share gives −0.031 (p = 0.656). Heteroskedasticity-robust standard errors barely change the p-value, from 0.344 with clustered standard errors to 0.358; the inference limitation is discussed in [[SEC:5.6]]. Removing 367 early one-round exits leaves β1 and β3 essentially unchanged, at −0.065 and −0.056 (p = 0.339 for β3). Uncentred VIFs of 10.1–18.7 for the group indicator, gap and interactions contrast with 1.01–1.52 for round-1 controls; after centring, all VIFs are at most 2.44.

[[TAB:BT1]] and [[TAB:BT2]] in Appendix B replace z-scored hype with the raw VC share, the sector's percentage of all VC dollars in the year of round 1. Logit β3 is close to zero and not significant for exit or failure in all three windows and without a window. In the five-year models, β3 is −0.0020 (p = 0.670; 9,124 startups) for exit and −0.0031 (p = 0.542; 9,235 startups) for failure. At shares of 14.3% and 40.4%, the mean minus and plus one standard deviation, the hot − cold difference in the average marginal effect of ln(1 + months) on exit is −0.9 percentage points (p = 0.650; 4,444 two-round startups). Using the share minus its sector mean retains only within-sector movement and gives logit β3 = −0.010 (p = 0.596; 9,124 startups). H2 is not supported.

[[TAB:BT3]] and [[TAB:BT4]] in Appendix B add a squared gap, measured in ln(1 + months) or months, with raw VC share as hype. No squared term is significant at 5% inside the four-, five- or six-year windows. Only the squared logarithmic term in the six-year window is significant at 10% (exit p = 0.070; failure p = 0.065). In five-year models, the linear and squared terms are not jointly significant: for exit, χ²(2) = 0.32 (p = 0.851) in logarithms and 1.85 (p = 0.396) in months; for failure, χ²(2) = 2.42 (p = 0.299) and 0.95 (p = 0.622), respectively. These tests are evaluated at a raw share of zero.

Only without an outcome window is logarithmic curvature significant: squared-term logit coefficients are −0.227 for exit (N = 15,495) and −0.210 for failure (N = 15,294), both p < 0.001, among two-round startups with the raw VC share as hype. [[FIG:BF1]] and [[FIG:BF2]] in Appendix B show predicted probabilities falling at long gaps for both outcomes among two-round startups. These patterns partly reflect time at risk: a longer gap leaves less time after round 2 for either exit or failure.

In [[FIG:BF3]] in Appendix B, based on 9,262 observations, the correlation between the two-round indicator and its interaction with ln(1 + months) is 0.94, consistent with the high uncentred VIFs. Hype correlates at most 0.08 in absolute value with the group indicator, gap and round-1 controls, and 0.31 with the raw VC share.

**5.5 Discussion of the results**
We read the four verdicts in [[TAB:T13]] together: among two-round startups, a longer gap between the first and the second VC round is associated with less failure, a larger valuation step and, at most, a slightly smaller probability of exit within five years. A long gap is not a distress signal here.

Shorter rounds were associated with higher agency costs or greater investor distance, consistent with costlier monitoring [[CIT-P:gompers1995, tian2011]]. In our setting, we interpret this short leash as consistent with greater risk among short-gap startups. Our argument is that risk fattens both tails, fitting higher failure alongside a weak exit association.

We also argue that long-gap startups have passed a longer test before round 2 and accumulated more progress, priced at that round. The valuation-step elasticity far below one means a larger total step but slower growth per month. Observed valuations form a selected sample because observation occurs at refinancing or exit [[CIT-P:cochrane2005, korteweg2010]]. In our setting, the longer-test reading is consistent with survivorship.

The negative logit interaction coefficient β3 fits the signal-extraction alternative in [[SEC:2.3]]: a long gap is more informative in hot markets. The past-only hype check is reported in [[SEC:5.4]]. We also consider attenuation: hype at round 1 may poorly proxy exit-market conditions years later, which would bias β3 towards zero.

The strongest exit predictors are already visible at round 1: size, age and lead type. [[TAB:T14]] compares our estimates with the literature. Corporate-VC-led first rounds were less likely to reach the next round [[CIT-P:hochberg2007]]. In our setting, the outcome is exit within five years, so we do not claim a match. [[GAP: Specify the proposed links concerning CVC as acquirer, VC networks, angel groups and accelerators.]] Sorting outweighed investor influence in IPO outcomes, while surveyed VCs ranked selection above value-add [[CIT-P:sorensen2007, gompers2020]]. In our setting, we read these coefficients as mixing selection of better startups with what investors add. [[GAP: Establish whether these candidate explanations can coexist and whether the data can distinguish them.]]

**5.6 Limitations**
The wild cluster bootstrap addresses inference with few clusters [[CIT-P:cameron2008]]. In our setting, the main exit models use 41 clusters, defined by sector × year of round 1, and p-values may be too small. Robust standard errors yield almost identical p-values, but a wild cluster bootstrap would be safer and is absent from our do-file.

Exit and failure are competing outcomes, with still private accounting for the rest. Separate logits do not jointly model these three states, whereas a multinomial or competing-risks model would.

Post-money valuations overstate fair value for US unicorns [[CIT-P:gornall2020]]. In our setting, the valuation step uses post-money valuations, ignores contract terms other than the equity share and is observed for about half of two-round startups. Observed valuations are selected [[CIT-P:cochrane2005]]. In our setting, if disclosure follows good rounds, the valuation sample is selected towards high steps.

We construct hype from the course cohort's own deals. The cohort comprises startups founded in 2012–2019, so annual shares partly reflect its ageing. Dropping undisclosed round-1 amounts retains only startups that disclosed. Both features limit how far our results generalise.

**6 Limitations to causality**
Our design compares startups and does not assign the gap, so every estimate is an association. We set out three channels through which the comparison departs from a causal one ([[SEC:6.1]] to [[SEC:6.3]]) and what would close them ([[SEC:6.4]]).

**6.1 The gap is not assigned at random**
Startups choose, and are selected for, their refinancing pace. Unobserved team quality or traction, can be associated with both a shorter gap between the first and the second VC round and exit or failure. With selection on unobservables, β1 can mix the gap association with omitted venture quality.

VCs weigh agency and monitoring costs when choosing round length [[CIT-P:gompers1995, tian2011]]. In our setting, a short gap can reflect investor expectations and, we argue, risk ([[SEC:5.5]]), making the gap endogenous to outcome determinants.

Controls fixed at round 1 cannot be outcomes of the gap; round-2 mediators are excluded. Adding founder, MBA, AI and young-lead controls leaves β1 and β3 unchanged ([[SEC:5.4]]). Both adjustments address only observables: stability is not identification.

Hype, a sector-year share of VC dollars, is not exogenous either. Cohort composition and common sector demand and opportunity shocks can accompany variation in hype and exits. β3 describes how the association between the gap and exit varies with hype, without identifying what hype does.

We read the positive OLS coefficient θ1 in terms of elapsed time, not waiting as a strategy. Total valuation steps are slightly larger after long gaps, but steps per year fall sharply with the gap. Waiting longer is not shown to create value.

**6.2 The group indicator looks ahead**
(DRAFT mancante: usa la versione che hai scritto in questa chat)

**6.3 Conditioning on refinancing: survivorship**
(DRAFT mancante: usa la versione che hai scritto in questa chat)

**6.4 What a causal design would need**
(DRAFT mancante: usa la versione che hai scritto in questa chat)

**7 Conclusions and discussion**
(DRAFT mancante: usa la versione che hai scritto in questa chat)
