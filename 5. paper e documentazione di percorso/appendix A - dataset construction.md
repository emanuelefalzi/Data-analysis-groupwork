<!--
Appendix A of the final paper (paper_group21_v5). Written 17/11/2026 by Claude for Lele from
`2. dataset/construction.pdf` (14/11/2026) and `1. python/dataset.py`. Where construction.pdf is
superseded (RULES.md, "Known inconsistencies") this text follows RULES.md: main outcome exit_5y,
script name dataset.py, "full sample" = 28,478 and "estimation sample" = 9,263 (glossary.md).
The paper pipeline (`skill-redigere paper latex/`) includes this file as it is, after the
references and outside the 20-page limit. Edit it here; tokens [[SEC:x]] become section links.
-->

# A Dataset construction

This appendix describes how `dataset.dta` (28,478 startups, 57 variables) is built from the raw PitchBook files, so that every number in [[SEC:3.1]] and [[SEC:3.2]] can be reproduced. The script is `1. python/dataset.py`; it writes `output/rq1_two_group_dataset_v2.dta` and a `.csv` copy. The same file is called `dataset.dta` in the repository and `group_21_dataset.dta` in the Stata do-files.

## A.1 Inputs and settings

Four files from the course PitchBook extract are used. The startup file, `pitchbook_course.dta`, has one row per startup and gives the identifier, founding year, primary industry sector, headquarters state and the dates of IPO, acquisition and failure. The deal file, `Deal.csv`, gives for each deal the company, date, type, status, amount and pre- and post-money valuations. `DealInvestorRelation.csv` links deals to investors and flags the lead investor, and `Investor.csv` gives each investor's primary type and founding year.

Four settings are fixed in the script. The observation period ends on 30 June 2022. The main outcome window is five years, with four and six years as sensitivity checks. A gap between rounds of more than ten years (3,653 days) is treated as a data error. One month is 30.44 days.

## A.2 From deals to rounds

Only deals of course startups that are completed and carry a valid date are kept: 52,277 of the 57,751 startups have at least one. A VC deal is a deal of type Seed Round, Early Stage VC or Later Stage VC; angel, grant, debt and accelerator deals are not VC rounds. PitchBook often records one round as several deals on the same day, for example one per tranche or per investor group, so all VC deals of a company on the same date are merged into one round. Amounts are summed, and for valuations the highest reported value is kept, since the deals of one round share the same valuation and some of them leave it blank. Round k is then the k-th distinct date with a VC deal.

Every startup with a first VC round stays in the data, whether or not it raised a second one: 34,822 startups. A second round dated after 30 June 2022 lies outside the observed period and counts as no second round (828 startups). The group indicator `two_rounds` (R) equals 1 if a second round exists by that date. For two-round startups the gap is the number of months between rounds 1 and 2, and `log_gap_r2` is R × ln(1 + months), so it is zero for one-round startups. One startup with a gap above ten years is dropped. Because rounds are merged by date, a gap of zero days cannot occur.

## A.3 Outcomes and outcome windows

An exit is an IPO or an acquisition, whichever comes first; failure uses the failure date of the startup file. An exit or failure dated before round 1 is a data error, and these 58 startups are dropped, leaving 34,763. An exit or failure between round 1 and round 2 is not an error, since a startup can be acquired or close without raising again.

The outcome window opens at round 2 for two-round startups and at round 1 for one-round startups, which have no second round. `exit_5y` and `failure_5y` equal 1 if the event falls inside the five-year window; `exit_4y`, `exit_6y` and the corresponding failure variables do the same for four and six years. `exit_5y` is the main outcome. The variable `exit`, an exit at any time with no window, is used only as a robustness check. For a two-round startup an event between round 1 and round 2 falls outside its window and counts as zero (26 startups whose first recorded event comes before round 2, probably a dating error). `full_window` equals 1 when the whole five-year window ends by 30 June 2022: 9,263 startups, the estimation sample (12,184 for the four-year window, 6,769 for the six-year one). These are flags, not filters: no startup is dropped from the file for an incomplete window.

## A.4 Controls and the lead investor

All controls are measured at round 1. `log_round1_size` is ln(1 + round-1 amount in $M). The 6,285 startups whose round-1 amount is undisclosed are dropped rather than imputed, since imputing a value would assume that the amount is missing at random; this step gives the full sample of 28,478 startups, 15,518 with two rounds and 12,960 with one. `startup_age_at_round1` is the year of round 1 minus the founding year; the two negative ages are set to missing in Stata before estimation. `round1_number` counts the completed financing deals of any type dated up to and including round 1, excluding exit deals. A blank headquarters state becomes its own "Unknown" category, so these startups stay in the state fixed effects.

The lead investor of round 1 is the investor flagged as lead on a round-1 deal; when a round has several leads, the first one in file order is kept. Its primary type gives `lead_type`. Rounds with no lead flagged get their own category, "No lead identified", which is the base category in the models, and types with fewer than 50 startups are pooled into "Other". This gives the 16 categories of `lead_cat`. Round-2 variables, such as the round-2 amount and the valuation step, are built in the same way but are missing for one-round startups and enter only the robustness checks and the H3 model, because they are mediators of the gap. The valuation step is the post-money valuation at round 2 over the post-money valuation at round 1.

## A.5 Market hype and the timing keys

Hype is built from the deal file. For each sector s and year t, the sector's share of all VC dollars is share(s,t) = VC$(s,t) / Σ VC$(s′,t), and `heat` is this share z-scored within the sector over 2012 to 2022, so that a value of +1 means one standard deviation more money than is normal for that sector. Hype is attached to each startup by its sector and the year of its first round, because one-round startups have no second round. The quarterly version (`heat_quarter`) and the version standardised on past years only (`heat_past`) are built in the same way and are used only as robustness checks.

Because one-round startups have no round 2, all timing keys refer to round 1: `round1_yq` (year-quarter of round 1) gives the time fixed effects, and `sector_year_id` numbers the sector × year cells of round 1, the level at which hype varies and at which standard errors are clustered.

## A.6 Output

The 57 variables are written to the `.dta` file (Stata 14 or later, with labels) and to a `.csv` copy, one row per startup sorted by company identifier. Interaction terms are not stored: Stata builds them in the models.
