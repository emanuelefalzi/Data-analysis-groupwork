from pathlib import Path

import numpy as np
import pandas as pd


DATA, OUT = Path("data"), Path("output")
OUT.mkdir(exist_ok=True)

# Deal types that count as a VC round. Angel, grant, debt and accelerator deals are left out on purpose, so "round 1" is the first institutional equity round, not the first money the company ever received.
VC_ROUND_TYPES = ["Seed Round", "Early Stage VC", "Later Stage VC"]

# Deal types that are not fundraising. They are excluded when we count how many financing deals the company had done by round 1 (round1_number), because an acquisition or a bankruptcy is not a funding event.
NOT_FINANCING = ["IPO", "Merger/Acquisition", "Reverse Merger", "Merger of Equals", "Buyout/LBO",
                 "Out of Business", "Bankruptcy: Liquidation"]

# Last date we treat as observed. Exits, failures and windows are measured up to this date. Note: the deal file actually runs to 15 Dec 2022, so this cut-off is conservative.
DATA_END = pd.Timestamp("2022-06-30")

# Length of the outcome window after round 1, in years. One-round startups have no round 2, so the clock starts at round 1 for both groups. 5 years from round 1 roughly equals 3 years after round 2 for the median two-round startup (median gap 16 months).
WINDOW_YEARS = 5
# Alternative windows for the sensitivity check asked at the pitch: if the results move a lot between 4, 5 and 6 years, 5 years is not a safe threshold.
CHECK_WINDOWS = [4, 6]

# Gaps longer than 10 years between round 1 and round 2 are treated as data errors and dropped.
MAX_GAP_DAYS = 3653

# Average month length, used to turn day counts into months.
DAYS_PER_MONTH = 30.44

# First year used for the sector hype measures. The course startups are founded from 2012 on, so earlier years have almost no deals and would give noisy sector shares.
FIRST_HYPE_YEAR = 2012


def zscore(x):
    """Standardise a series: (x - mean) / SD. A value of +1 means one standard deviation above the mean."""
    return (x - x.mean()) / x.std()


#############################################################################################################
# Startups: keep the ID, founding year, sector, state and the three outcome dates, and give them short names.
startups = pd.read_stata(DATA / "pitchbook_course.dta",
                         columns=["CompanyID", "YearFounded", "PrimaryIndustrySector", "HQState_Province",
                                  "IPODate", "AcquiredDate", "FailedDate"])
startups = startups.rename(columns={"CompanyID": "company_id", "YearFounded": "year_founded",
                                    "PrimaryIndustrySector": "sector", "HQState_Province": "state"})
#turn empty sector and state into proper missing values.
startups[["sector", "state"]] = startups[["sector", "state"]].replace("", np.nan)

# Deals: keep only the deals of course startups, with a valid date, that were actually completed (announced or failed deals never brought money in).
deals = pd.read_csv(DATA / "Deal.csv", low_memory=False,
                    usecols=["DealID", "CompanyID", "DealDate", "DealType", "DealStatus", "DealSize",
                             "PremoneyValuation", "PostValuation"]).rename(columns={"CompanyID": "company_id"})
deals = deals[deals["company_id"].isin(startups["company_id"])]
deals["DealDate"] = pd.to_datetime(deals["DealDate"], format="%m/%d/%Y", errors="coerce")
deals = deals[deals["DealDate"].notna() & (deals["DealStatus"] == "Completed")]

# Investor files, used only for the lead investor of round 1.
deal_investors = pd.read_csv(DATA / "DealInvestorRelation.csv", usecols=["DealID", "InvestorID", "IsLeadInvestor"],
                             low_memory=False)
investors = pd.read_csv(DATA / "Investor.csv", usecols=["InvestorID", "PrimaryInvestorType", "YearFounded"],
                        low_memory=False).rename(columns={"YearFounded": "investor_year_founded"})

# 2. ROUNDS 1, 2, THE TWO GROUPS AND THE GAP
########################################################################################################
# PitchBook sometimes records one round as several deals on the same day (for example one per tranche or per investor group). We merge them: a VC round is all VC deals of a company on the same date. The amounts are added up; for valuations we take the highest reported value, since the deals of one round share the same valuation and some of them simply leave it blank.
vc = deals[deals["DealType"].isin(VC_ROUND_TYPES)].copy()
rounds = (vc.groupby(["company_id", "DealDate"], as_index=False)
          .agg(size=("DealSize", "sum"), pre=("PremoneyValuation", "max"), post=("PostValuation", "max")))
# A summed size of 0 means no amount was disclosed, not a round of $0.
rounds["size"] = rounds["size"].replace(0, np.nan)
# Number the rounds of each company in date order: k = 1 is the first VC round, k = 2 the second, ...
rounds = rounds.sort_values(["company_id", "DealDate"])
rounds["k"] = rounds.groupby("company_id").cumcount() + 1


def round_k(k, cols):
    """Return round number k of every company (one row per company), with the columns renamed as in cols."""
    r = rounds[rounds["k"] == k].set_index("company_id")
    return r[list(cols)].rename(columns=cols)


# Put rounds 1, 2 and 3 side by side, every startup with a 1st VC round stays in, whether or not it ever raised a 2nd one.
df = (round_k(1, {"DealDate": "round1_date", "size": "round1_size", "post": "round1_post"})
      .join(round_k(2, {"DealDate": "round2_date", "size": "round2_size", "pre": "round2_pre", "post": "round2_post"}), how="left")
      .join(round_k(3, {"DealDate": "round3_date", "pre": "round3_pre"}), how="left")
      .join(startups.set_index("company_id"), how="left"))

# A round 2 dated after DATA_END is outside the observed period, so it is treated as no round 2.
df.loc[df["round2_date"] > DATA_END, ["round2_date", "round2_size", "round2_pre", "round2_post", "round3_date", "round3_pre"]] = np.nan

# The gap is the time between the two rounds, t2 - t1, defined only for startups with a round 2. Gaps over 10 years are data errors and those startups are dropped (rounds are merged by date, so a gap of 0 days cannot occur).
df["gap_days"] = (df["round2_date"] - df["round1_date"]).dt.days
df = df[~(df["gap_days"] > MAX_GAP_DAYS)].copy()
df["gap_months"] = df["gap_days"] / DAYS_PER_MONTH

# Group variable: two_rounds = 1 if the startup has a 2nd VC round, 0 if it has only one round.
df["two_rounds"] = df["round2_date"].notna().astype(int)

# log_gap = ln(1 + gap in months), only for two-round startups (missing otherwise).
df["log_gap"] = np.log1p(df["gap_months"])
# log_gap_r2 = two_rounds x log_gap, set to 0 for one-round startups. This is the variable that enters the regression next to two_rounds, so the one-round startups stay in the sample and the gap slope is estimated among two-round startups only.
df["log_gap_r2"] = df["log_gap"].fillna(0)


# 3. OUTCOMES
################################################################################################################
# An exit is an IPO or an acquisition, whichever comes first. Failure uses the failure date in the course file.
df["exit_date"] = df[["IPODate", "AcquiredDate"]].min(axis=1)
df["failure_date"] = df["FailedDate"]
# A company cannot exit or fail before its first VC round, so such dates are errors: drop them. Exits or failures before round 2 are legitimate (a startup can be acquired without a 2nd round).
df = df[~((df["exit_date"] < df["round1_date"]) | (df["failure_date"] < df["round1_date"]))].copy()

# Each outcome = 1 if the event happens within 5 years of the window start, 0 otherwise. The window starts at round 2 for two-round startups (as in the pitch) and at round 1 for one-round startups, which have no round 2.
df["window_start"] = df["round2_date"].where(df["two_rounds"] == 1, df["round1_date"])
win_end = df["window_start"] + pd.DateOffset(years=WINDOW_YEARS)
within = lambda d: ((d >= df["window_start"]) & (d <= win_end)).astype(int)
df["exit_5y"] = within(df["exit_date"])          # main outcome of the logit
df["failure_5y"] = within(df["failure_date"])     # robustness: failure as the outcome
# exit: 1 if the startup ever exited (IPO or acquisition) after its 1st round, with no time window, so every startup is kept.
df["exit"] = df["exit_date"].notna().astype(int)
# A 0 in exit_5y only means "did not exit" if we can see the whole 5 years. So the logit uses only startups whose window ends by DATA_END (window start by 30 Jun 2017).
df["full_window"] = (win_end <= DATA_END).astype(int)
# The same three variables for the 4- and 6-year windows (exit_4y, failure_4y, full_window_4y, ...), built exactly like the 5-year ones.
for w in CHECK_WINDOWS:
    w_end = df["window_start"] + pd.DateOffset(years=w)
    df[f"exit_{w}y"] = ((df["exit_date"] >= df["window_start"]) & (df["exit_date"] <= w_end)).astype(int)
    df[f"failure_{w}y"] = ((df["failure_date"] >= df["window_start"]) & (df["failure_date"] <= w_end)).astype(int)
    df[f"full_window_{w}y"] = (w_end <= DATA_END).astype(int)

# Variables for the survival models, which do not need a fixed window. The clock starts at round 1 and stops at the first of exit, failure or DATA_END. If it stops at DATA_END the startup is censored.
end = pd.concat([df["exit_date"], df["failure_date"], pd.Series(DATA_END, index=df.index)], axis=1).min(axis=1)
df["months_to_outcome"] = (end - df["round1_date"]).dt.days / DAYS_PER_MONTH
# Which event stopped the clock. If exit and failure fall on the same day (6 startups) we count it as an exit.
df["outcome_is_exit"] = (df["exit_date"] == end).astype(int)
df["outcome_is_failure"] = ((df["failure_date"] == end) & (df["outcome_is_exit"] == 0)).astype(int)
# For startups whose round 1 comes after DATA_END the clock would be negative, so the survival variables are set to missing for them.
df.loc[df["round1_date"] > DATA_END, ["months_to_outcome", "outcome_is_exit", "outcome_is_failure"]] = np.nan


# 4. CONTROLS AT ROUND 1, ROUND-2 VARIABLES AND FIXED-EFFECT
######################################################################################################
# The controls are all measured at round 1. Anything decided at round 2 (its size, its valuation) could itself be a result of how fast the startup raised, so it would absorb part of the relationship we want to measure. Those variables are kept only for robustness checks.

# Size of round 1 in logs ($M; ln(1 + x) so that very small rounds stay defined).
df["log_round1_size"] = np.log1p(df["round1_size"])
df["round1_year"] = df["round1_date"].dt.year
# Undisclosed round-1 amounts are dropped.
n_no_size = int(df["log_round1_size"].isna().sum())
df = df[df["log_round1_size"].notna()].copy()
# Age of the startup at round 1, in years. Two startups have a negative age (round dated before founding); they are left as they are here and recoded to missing in the do-file.
df["startup_age_at_round1"] = df["round1_year"] - df["year_founded"]
# round1_number: how many financing deals (of any type, not only VC) the company had done up to and including round 1. A startup that had angel or grant money before its first VC round is further along than one whose first ever deal is VC. Companies with no earlier deals get 1.
fin = deals[~deals["DealType"].isin(NOT_FINANCING)].merge(df["round1_date"].reset_index(), on="company_id")
df["round1_number"] = fin[fin["DealDate"] <= fin["round1_date"]].groupby("company_id").size().reindex(df.index).fillna(1)

# Lead investor of round 1. First find all investors in the round-1 deals, then keep the one flagged as lead. If a round has several leads, the first one in the file is used.
r1 = vc.merge(df["round1_date"].reset_index(), left_on=["company_id", "DealDate"], right_on=["company_id", "round1_date"])
r1 = r1[["company_id", "DealID"]].merge(deal_investors, on="DealID").merge(investors, on="InvestorID", how="left")
lead = r1[r1["IsLeadInvestor"] == "Yes"].drop_duplicates("company_id").set_index("company_id")
# Lead type (VC, corporate VC, angel, ...). Rounds with no lead flagged get their own category, so they are not dropped. Types with fewer than 50 startups are pooled into "Other" to avoid near-empty dummies in i.lead_cat.
df["lead_type"] = lead["PrimaryInvestorType"].reindex(df.index).fillna("No lead identified")
small = df["lead_type"].value_counts().loc[lambda s: s < 50].index
df.loc[df["lead_type"].isin(small), "lead_type"] = "Other"
# Lead investor age at round 1 in years (control for grandstanding: young VC firms may push their startups to raise quickly to build a track record). Negative ages are founding-year errors and set to missing.
df["lead_investor_age"] = (df["round1_year"] - lead["investor_year_founded"].reindex(df.index)).where(lambda a: a >= 0)

# Round-2 variables. These are mediators (decided at the same time as the gap ends), so they are used only as robustness controls and in the valuation analysis, never in the main model. They are missing for startups without a round 2.
df["log_round2_size"] = np.log1p(df["round2_size"])
# Valuation step-up = pre-money value at round 2 / post-money value at round 1. Above 1 means the company was worth more at round 2 than right after round 1 (an up-round). Missing when either valuation is not reported.
df["valuation_step_up"] = (df["round2_pre"] / df["round1_post"]).where(lambda v: v > 0)
df["log_valuation_step_up"] = np.log(df["valuation_step_up"])
# Valuation change for H3: delta_v = post-money at round 2 / post-money at round 1 (above 1 means the company is worth more after round 2). Missing when either valuation is not reported.
df["delta_v"] = (df["round2_post"] / df["round1_post"]).where(lambda v: v > 0)
df["up_round"] = (df["valuation_step_up"] > 1).astype(float).where(df["valuation_step_up"].notna())


# 4b. ROUND 3: FROM ROUND 2 TO ROUND 3, AND FROM ROUND 1 TO ROUND 3
########################################################################################################
# Round 3 happens after round 2, so these variables can be outcomes or descriptives, never controls. All of them are missing for startups without a third VC round.
df["has_round3"] = df["round3_date"].notna().astype(int)

# Gaps in months, with logs built the same way as log_gap so the three gaps are on the same scale.
df["gap_23_months"] = (df["round3_date"] - df["round2_date"]).dt.days / DAYS_PER_MONTH
df["log_gap_23"] = np.log1p(df["gap_23_months"])
df["gap_13_months"] = (df["round3_date"] - df["round1_date"]).dt.days / DAYS_PER_MONTH
df["log_gap_13"] = np.log1p(df["gap_13_months"])

# Step-ups to round 3: pre-money at round 3 divided by the post-money at round 2 (2 to 3) or at round 1 (1 to 3).
df["valuation_step_up_23"] = (df["round3_pre"] / df["round2_post"]).where(lambda v: v > 0)
df["log_valuation_step_up_23"] = np.log(df["valuation_step_up_23"])
df["valuation_step_up_13"] = (df["round3_pre"] / df["round1_post"]).where(lambda v: v > 0)
df["log_valuation_step_up_13"] = np.log(df["valuation_step_up_13"])

# Fixed effects and clusters. Non-raisers have no round 2, so time is now measured at round 1: round1_yq is the year-quarter of round 1 written as yyyyq (e.g. 20153 = 2015 Q3), used as time fixed effects. round2_year is kept for description only.
df["round2_year"] = df["round2_date"].dt.year
q = df["round1_date"].dt.to_period("Q")
df["round1_yq"] = q.dt.year * 10 + q.dt.quarter
df = df.reset_index()
# Numeric codes for sector and state (alphabetical order, starting at 1), so Stata can use i.sector_id and i.state_id. A missing state is coded "Unknown" so those startups stay in the regression; a missing sector stays missing.
df["state"] = df["state"].fillna("Unknown")
df["sector_id"] = (df["sector"].astype("category").cat.codes + 1).replace(0, np.nan)
df["state_id"] = (df["state"].astype("category").cat.codes + 1).replace(0, np.nan)
# Cluster IDs. Annual heat takes one value per sector and year of round 1, so startups in the same sector-year share the same shock and their errors are correlated: we cluster at that level. The sector x quarter ID is for the models that use quarterly heat.
df["sector_year_id"] = df.groupby(["sector", "round1_year"]).ngroup() + 1
df["sector_quarter_id"] = df.groupby(["sector", "round1_yq"]).ngroup() + 1
df.loc[df["sector"].isna(), ["sector_year_id", "sector_quarter_id"]] = np.nan


# 5. SECTOR HYPE
########################################################################################################
# Hype is measured on the money side: how much of all VC money goes to a sector, compared with what is normal for that sector. All measures are computed from the VC deals of the course startups and attached to each startup through the year (or quarter) of its round 1, because non-raisers have no round 2.
vc = vc.merge(startups[["company_id", "sector"]], on="company_id", how="left")
vc = vc[vc["sector"].notna()]

# (a) Sector share of VC money in a year: share(s,t) = VC $ in sector s in year t / VC $ in all sectors in year t. Using a share rather than dollars takes out the market-wide boom (2021 was large for every sector), so what is left is whether investors were tilting towards this sector in particular.
y = vc[vc["DealDate"].dt.year >= FIRST_HYPE_YEAR].assign(year=lambda d: d["DealDate"].dt.year)
hype = y.groupby(["sector", "year"], as_index=False)["DealSize"].sum()
hype["sector_vc_share"] = hype["DealSize"] / hype.groupby("year")["DealSize"].transform("sum")
hype = hype.sort_values(["sector", "year"])
g = hype.groupby("sector")["sector_vc_share"]

# (b) heat, the main moderator: the share z-scored within its own sector over 2012-2022. IT always gets a large share and Energy a small one; that is a permanent difference, not hype. Comparing each sector with its own mean and SD means heat = +1 reads as "one SD above what is normal for this sector".
hype["heat"] = g.transform(zscore)

# (c) heat_past: the same z-score, but the mean and SD use only the sector's earlier years (from 2012 up to t-1). heat uses all years, including later ones, which the investors at round 2 could not have known. heat_past avoids this. It needs at least two earlier years, so it starts in 2014.
hype["heat_past"] = ((hype["sector_vc_share"] - g.transform(lambda s: s.shift(1).expanding(2).mean()))
                     / g.transform(lambda s: s.shift(1).expanding(2).std()))

# (d) Entry side of hype: number of course startups founded in the sector each year, z-scored within the sector and lagged one year. The lag is there because founding comes well before funding: the companies founded this year are not yet raising, so last year's foundings are the ones competing for money now. Course startups are founded 2012-2019 only, so this measure is missing for later years.
founded = startups.groupby(["sector", "year_founded"]).size().rename("n").reset_index()
hype = hype.merge(founded.rename(columns={"year_founded": "year"}), on=["sector", "year"], how="left")
hype["entry_z"] = hype.groupby("sector")["n"].transform(zscore)
hype["entry_z_l1"] = hype.groupby("sector")["entry_z"].shift(1)

# (e) hype_index_l: average of the money side and the entry side, (heat + entry_z_l1) / 2, as suggested by the TA.
hype["hype_index_l"] = (hype["heat"] + hype["entry_z_l1"]) / 2

df = df.merge(hype[["sector", "year", "sector_vc_share", "heat", "heat_past", "entry_z_l1", "hype_index_l"]]
              .rename(columns={"year": "round1_year"}), on=["sector", "round1_year"], how="left")

# (f) heat_quarter: the same idea as heat but with quarterly shares, for a timing closer to the round itself. Quarters with no deal in a sector count as a share of 0. The mean and SD come from a fixed base period, 2013Q1-2019Q4, which covers the round-2 dates of almost all the estimation sample (only 0.4% are in 2012).
vc["q"] = vc["DealDate"].dt.to_period("Q")
usd_q = (vc.pivot_table(index="q", columns="sector", values="DealSize", aggfunc="sum")
         .reindex(pd.period_range("2012Q1", DATA_END.to_period("Q"), freq="Q")).fillna(0))
share_q = usd_q.div(usd_q.sum(axis=1), axis=0)
ref = share_q.loc["2013Q1":"2019Q4"]
hq = ((share_q - ref.mean()) / ref.std()).stack().rename("heat_quarter").reset_index()
hq.columns = ["q", "sector", "heat_quarter"]
# Write the quarter as yyyyq so it matches round1_yq, then attach it by sector and quarter of round 1.
hq["round1_yq"] = hq["q"].dt.year * 10 + hq["q"].dt.quarter
df = df.merge(hq[["round1_yq", "sector", "heat_quarter"]], on=["round1_yq", "sector"], how="left")


# 5b. ADD-ON: EXTRA CONTROLS, TEAM AND LEAD-INVESTOR AGE
########################################################################################################
# All fixed before round 1, so they can be controls.
# Team: number of founders, an MBA founder and an AI term in the company description.
team = pd.read_stata(DATA / "pitchbook_course.dta", columns=["CompanyID", "NFounders", "MBA", "Has_Core_AI_Term"])
team = team.rename(columns={"CompanyID": "company_id"})
df = df.merge(team, on="company_id", how="left")
# Founders in logs (team size is right-skewed).
df["ln_founders"] = np.log(df["NFounders"])
# Young lead investor: the lead firm is less than 6 years old at round 1, the cut-off Gompers (1996) uses for grandstanding.
has_lead = df["lead_type"] != "No lead identified"
df["young_lead"] = (has_lead & (df["lead_investor_age"] < 6)).astype(int)
# A lead was identified but its founding year is missing: flagged so these startups are not counted as "old lead".
df["lead_age_miss"] = (has_lead & df["lead_investor_age"].isna()).astype(int)
# Sample flag for the extra-controls models: founder data available (both columns are compared on this same sample).
df["team_ok"] = (df["ln_founders"].notna() & df["MBA"].notna()).astype(int)


# 6. SAVE
########################################################################################################
# Variable labels for Stata.
labels = {
    "company_id": "PitchBook company ID",
    "sector": "Industry sector", "sector_id": "Sector code (i.sector_id)",
    "state": "US state of HQ", "state_id": "State code (i.state_id)",
    "year_founded": "Founding year",
    "round1_date": "Date of 1st VC round", "round2_date": "Date of 2nd VC round (missing if none)",
    "window_start": "Outcome window start: round 2, or round 1 if no round 2",
    "round1_year": "Year of 1st VC round", "round2_year": "Year of 2nd VC round",
    "round1_yq": "Year-quarter of 1st round (yyyyq, time FE)",
    "sector_year_id": "Sector x year of 1st round (main cluster)",
    "sector_quarter_id": "Sector x quarter of 1st round (cluster, quarterly heat)",
    "two_rounds": "Group: 1 = two or more VC rounds, 0 = one round",
    "gap_months": "Months between 1st and 2nd VC round",
    "log_gap": "ln(1 + gap in months), two-round startups only",
    "log_gap_r2": "two_rounds x log_gap (0 if one round): regressor",
    "exit_5y": "Exit (IPO/acq.) within 5y of round 2 (round 1 if no round 2)",
    "failure_5y": "Failure within 5y of round 2 (round 1 if no round 2)",
    "exit": "Exit (IPO or acquisition) ever, no window",
    "full_window": "Full 5-year window observed (estimation sample)",
    "exit_4y": "Exit (IPO/acq.) within 4y of round 2 (round 1 if no round 2)",
    "failure_4y": "Failure within 4y of round 2 (round 1 if no round 2)",
    "full_window_4y": "Full 4-year window observed",
    "exit_6y": "Exit (IPO/acq.) within 6y of round 2 (round 1 if no round 2)",
    "failure_6y": "Failure within 6y of round 2 (round 1 if no round 2)",
    "full_window_6y": "Full 6-year window observed",
    "months_to_outcome": "Months from 1st round to exit, failure or data end",
    "outcome_is_exit": "Survival clock ended by an exit",
    "outcome_is_failure": "Survival clock ended by a failure",
    "log_round1_size": "ln(1 + amount of 1st VC round, $M)",
    "round1_number": "Financing deal number of the 1st VC round",
    "startup_age_at_round1": "Startup age at 1st VC round (years)",
    "lead_type": "Lead investor type, 1st VC round",
    "lead_investor_age": "Lead investor age at 1st VC round (years)",
    "log_round2_size": "ln(1 + amount of 2nd VC round, $M)",
    "valuation_step_up": "Pre-money r2 / post-money r1",
    "delta_v": "Post-money r2 / post-money r1 (H3 outcome)",
    "log_valuation_step_up": "ln(valuation step-up)",
    "up_round": "Step-up > 1 (up-round)",
    "round3_date": "Date of 3rd VC round",
    "has_round3": "Startup raised a 3rd VC round",
    "gap_23_months": "Months between 2nd and 3rd VC round",
    "log_gap_23": "ln(1 + months between rounds 2 and 3)",
    "gap_13_months": "Months between 1st and 3rd VC round",
    "log_gap_13": "ln(1 + months between rounds 1 and 3)",
    "valuation_step_up_23": "Pre-money r3 / post-money r2",
    "log_valuation_step_up_23": "ln(step-up r2 to r3)",
    "valuation_step_up_13": "Pre-money r3 / post-money r1",
    "log_valuation_step_up_13": "ln(step-up r1 to r3)",
    "sector_vc_share": "Sector share of all VC $, year of 1st round",
    "heat": "Heat: z of sector VC share within sector, year of round 1 (main)",
    "heat_quarter": "Quarterly heat: z of quarter share (2013-19 base)",
    "heat_past": "Heat using only past years (no look-ahead)",
    "entry_z_l1": "Startups founded in sector, z, previous year",
    "hype_index_l": "Hype index: (heat + entry_z_l1) / 2",
}

labels.update({
    "NFounders": "Number of founders (course file)",
    "ln_founders": "ln(number of founders)",
    "MBA": "At least one founder has an MBA",
    "Has_Core_AI_Term": "Description contains a core AI term",
    "young_lead": "Lead investor younger than 6 years at round 1",
    "lead_age_miss": "Lead identified but its age is missing",
    "team_ok": "Founder data available (extra-controls sample)",
})

df = df[list(labels)].sort_values("company_id").reset_index(drop=True)
df.to_csv(OUT / "rq1_two_group_dataset_v4.csv", index=False)

st = df.copy()
for c in ["sector", "state", "lead_type"]:
    st[c] = st[c].fillna("").astype(str)
st.to_stata(OUT / "rq1_two_group_dataset_v4.dta", write_index=False, version=118, variable_labels=labels)
es = df[df["full_window"] == 1]
print(f"Dropped for an undisclosed round-1 amount: {n_no_size:,}")
print(f"Rows: {len(df):,} | estimation sample (full_window): {len(es):,} | variables: {df.shape[1]}")
print(f"In the estimation sample: two rounds: {es['two_rounds'].sum():,} | one round: {(1 - es['two_rounds']).sum():,} | exit rate {es['exit_5y'].mean():.3f} | failure rate {es['failure_5y'].mean():.3f}")
