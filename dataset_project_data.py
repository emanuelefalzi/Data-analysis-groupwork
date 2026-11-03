from pathlib import Path

import numpy as np
import pandas as pd


# SETTINGS


DATA, OUT = Path("data"), Path("output")
OUT.mkdir(exist_ok=True)

# Deal types that count as a VC round. Angel, grant, debt and accelerator deals are left out on purpose, so "round 1" is the first institutional equity round, not the first money the company ever received.
VC_ROUND_TYPES = ["Seed Round", "Early Stage VC", "Later Stage VC"]

# Deal types that are not fundraising. They are excluded when we count how many financing deals the company had done by round 1 (round1_number), because an acquisition or a bankruptcy is not a funding event.
NOT_FINANCING = ["IPO", "Merger/Acquisition", "Reverse Merger", "Merger of Equals", "Buyout/LBO",
                 "Out of Business", "Bankruptcy: Liquidation"]

# Last date we treat as observed. Exits, failures and windows are measured up to this date. Note: the deal file actually runs to 15 Dec 2022, so this cut-off is conservative (see the review PDF).
DATA_END = pd.Timestamp("2022-06-30")

# Length of the outcome window after round 2, in years (the reasons for 3 are in the construction PDF).
WINDOW_YEARS = 3

# Gaps longer than 10 years between round 1 and round 2 are treated as data errors and dropped.
MAX_GAP_DAYS = 3653

# Average month length, used to turn day counts into months.
DAYS_PER_MONTH = 30.44

# First year used for the sector hype measures. The course startups are founded from 2012 on, so earlier years have almost no deals and would give noisy sector shares.
FIRST_HYPE_YEAR = 2012


def zscore(x):
    """Standardise a series: (x - mean) / SD. A value of +1 means one standard deviation above the mean."""
    return (x - x.mean()) / x.std()



# 1. LOAD THE RAW FILES
#############################################################################################################
# Startups: keep the ID, founding year, sector, state and the three outcome dates, and give them short names.
startups = pd.read_stata(DATA / "pitchbook_course.dta",
                         columns=["CompanyID", "YearFounded", "PrimaryIndustrySector", "HQState_Province",
                                  "IPODate", "AcquiredDate", "FailedDate"])
startups = startups.rename(columns={"CompanyID": "company_id", "YearFounded": "year_founded",
                                    "PrimaryIndustrySector": "sector", "HQState_Province": "state"})
# Stata stores missing text as "", so turn empty sector and state into proper missing values.
startups[["sector", "state"]] = startups[["sector", "state"]].replace("", np.nan)

# Deals: keep only the deals of course startups, with a valid date, that were actually completed (announced or failed deals never brought money in).
deals = pd.read_csv(DATA / "Deal.csv", low_memory=False,
                    usecols=["DealID", "CompanyID", "DealDate", "DealType", "DealStatus", "DealSize",
                             "PremoneyValuation", "PostValuation"]).rename(columns={"CompanyID": "company_id"})
deals = deals[deals["company_id"].isin(startups["company_id"])]
deals["DealDate"] = pd.to_datetime(deals["DealDate"], format="%m/%d/%Y", errors="coerce")
deals = deals[deals["DealDate"].notna() & (deals["DealStatus"] == "Completed")]

# Investor files, used only for the lead investor of round 1 (Step 4).
deal_investors = pd.read_csv(DATA / "DealInvestorRelation.csv", usecols=["DealID", "InvestorID", "IsLeadInvestor"],
                             low_memory=False)
investors = pd.read_csv(DATA / "Investor.csv", usecols=["InvestorID", "PrimaryInvestorType", "YearFounded"],
                        low_memory=False).rename(columns={"YearFounded": "investor_year_founded"})

# 2. ROUNDS 1, 2 AND 3, AND THE GAP (the treatment)
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


# Put rounds 1, 2 and 3 side by side. The inner join with round 2 keeps only startups with at least two VC rounds (no second round means no gap). Round 3 is a left join, so it is missing when there is none.
df = (round_k(1, {"DealDate": "round1_date", "size": "round1_size", "post": "round1_post"})
      .join(round_k(2, {"DealDate": "round2_date", "size": "round2_size", "pre": "round2_pre", "post": "round2_post"}), how="inner")
      .join(round_k(3, {"DealDate": "round3_date", "pre": "round3_pre"}), how="left")
      .join(startups.set_index("company_id"), how="left"))

# The gap is the time between the two rounds, t2 - t1. Gaps of 0 days or over 10 years are data errors.
df["gap_days"] = (df["round2_date"] - df["round1_date"]).dt.days
df = df[(df["gap_days"] > 0) & (df["gap_days"] <= MAX_GAP_DAYS)].copy()
df["gap_months"] = df["gap_days"] / DAYS_PER_MONTH
# The main regressor is log_gap = ln(1 + gap in months). The log pulls in the long right tail (a few startups wait many years), so a handful of very slow raisers do not drive the estimates. Adding 1 keeps very short gaps (under a month) defined and close to zero.
df["log_gap"] = np.log1p(df["gap_months"])


# 3. OUTCOMES
################################################################################################################
# An exit is an IPO or an acquisition, whichever comes first. Failure uses the failure date in the course file.
df["exit_date"] = df[["IPODate", "AcquiredDate"]].min(axis=1)
df["failure_date"] = df["FailedDate"]
# A company cannot exit or fail before it raises its second round, so such dates are errors: drop them.
df = df[~((df["exit_date"] < df["round2_date"]) | (df["failure_date"] < df["round2_date"]))].copy()

# Each outcome = 1 if the event happens within 3 years of round 2, 0 otherwise. All startups start the clock at their own round 2, so they are compared over the same length of time.
win_end = df["round2_date"] + pd.DateOffset(years=WINDOW_YEARS)
within = lambda d: ((d >= df["round2_date"]) & (d <= win_end)).astype(int)
df["exit_3y"] = within(df["exit_date"])          # main outcome of the logit
df["failure_3y"] = within(df["failure_date"])     # robustness: failure as the outcome
df["round3_within_3y"] = within(df["round3_date"])  # robustness: raising a 3rd round as the outcome
# A 0 in exit_3y only means "did not exit" if we can see the whole 3 years. For a startup whose round 2 was in 2021 a 0 mostly means "not yet". So the logit uses only startups whose window ends by DATA_END.
df["full_3y_window"] = (win_end <= DATA_END).astype(int)

# Variables for the survival models, which do not need a fixed window. The clock starts at round 2 and stops at the first of exit, failure or DATA_END. If it stops at DATA_END the startup is censored.
end = pd.concat([df["exit_date"], df["failure_date"], pd.Series(DATA_END, index=df.index)], axis=1).min(axis=1)
df["months_to_outcome"] = (end - df["round2_date"]).dt.days / DAYS_PER_MONTH
# Which event stopped the clock. If exit and failure fall on the same day (6 startups) we count it as an exit.
df["outcome_is_exit"] = (df["exit_date"] == end).astype(int)
df["outcome_is_failure"] = ((df["failure_date"] == end) & (df["outcome_is_exit"] == 0)).astype(int)
# For startups whose round 2 comes after DATA_END the clock would end before it starts (negative time), so the survival variables are set to missing for them (825 startups).
df.loc[df["round2_date"] > DATA_END, ["months_to_outcome", "outcome_is_exit", "outcome_is_failure"]] = np.nan


# 4. CONTROLS AT ROUND 1, ROUND-2 VARIABLES AND FIXED-EFFECT KEYS
######################################################################################################
# The controls are all measured at round 1, before the gap is over. Anything decided at round 2 (its size, its valuation) could itself be a result of how fast the startup raised, so it would absorb part of the relationship we want to measure. Those variables are kept only for robustness checks.

# Size of round 1 in logs ($M; ln(1 + x) so that very small rounds stay defined).
df["log_round1_size"] = np.log1p(df["round1_size"])
df["round1_year"] = df["round1_date"].dt.year
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
# Lead investor age at round 1 in years (control for "grandstanding": young VC firms may push their startups to raise quickly to build a track record). Negative ages are founding-year errors and set to missing.
df["lead_investor_age"] = (df["round1_year"] - lead["investor_year_founded"].reindex(df.index)).where(lambda a: a >= 0)

# Round-2 variables. These are mediators (decided at the same time as the gap ends), so they are used only as robustness controls and in the valuation analysis, never in the main model.
df["log_round2_size"] = np.log1p(df["round2_size"])
# Valuation step-up = pre-money value at round 2 / post-money value at round 1. Above 1 means the company was worth more at round 2 than right after round 1 (an up-round). Missing when either valuation is not reported.
df["valuation_step_up"] = (df["round2_pre"] / df["round1_post"]).where(lambda v: v > 0)
df["log_valuation_step_up"] = np.log(df["valuation_step_up"])
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

# Fixed effects and clusters. round2_yq is the year-quarter of round 2 written as yyyyq (e.g. 20163 = 2016 Q3), used as time fixed effects.
df["round2_year"] = df["round2_date"].dt.year
q = df["round2_date"].dt.to_period("Q")
df["round2_yq"] = q.dt.year * 10 + q.dt.quarter
df = df.reset_index()
# Numeric codes for sector and state (alphabetical order, starting at 1), so Stata can use i.sector_id and i.state_id. A missing sector or state stays missing.
df["sector_id"] = (df["sector"].astype("category").cat.codes + 1).replace(0, np.nan)
df["state_id"] = (df["state"].astype("category").cat.codes + 1).replace(0, np.nan)
# Cluster IDs. Annual heat takes one value per sector and year, so startups in the same sector-year share the same shock and their errors are correlated: we cluster at that level. The sector x quarter ID is for the models that use quarterly heat.
df["sector_year_id"] = df.groupby(["sector", "round2_year"]).ngroup() + 1
df["sector_quarter_id"] = df.groupby(["sector", "round2_yq"]).ngroup() + 1
df.loc[df["sector"].isna(), ["sector_year_id", "sector_quarter_id"]] = np.nan


# 5. SECTOR HYPE (the moderator)
########################################################################################################
# Hype is measured on the money side: how much of all VC money goes to a sector, compared with what is normal for that sector. All measures are computed from the VC deals of the course startups and attached to each startup through the year (or quarter) of its round 2.
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

# (c) heat_past: the same z-score, but the mean and SD use only the sector's earlier years (from 2012 up to t-1). heat uses all years, including later ones, which the investors at round 2 could not have known. heat_past avoids this look-ahead. It needs at least two earlier years, so it starts in 2014.
hype["heat_past"] = ((hype["sector_vc_share"] - g.transform(lambda s: s.shift(1).expanding(2).mean()))
                     / g.transform(lambda s: s.shift(1).expanding(2).std()))

# (d) Entry side of hype: number of course startups founded in the sector each year, z-scored within the sector and lagged one year. The lag is there because founding comes well before funding: the companies founded this year are not yet raising, so last year's foundings are the ones competing for money now. Course startups are founded 2012-2019 only, so this measure is missing for later years.
founded = startups.groupby(["sector", "year_founded"]).size().rename("n").reset_index()
hype = hype.merge(founded.rename(columns={"year_founded": "year"}), on=["sector", "year"], how="left")
hype["entry_z"] = hype.groupby("sector")["n"].transform(zscore)
hype["entry_z_l1"] = hype.groupby("sector")["entry_z"].shift(1)

# (e) hype_index_l: average of the money side and the entry side, (heat + entry_z_l1) / 2, as suggested by the TA.
hype["hype_index_l"] = (hype["heat"] + hype["entry_z_l1"]) / 2

# Attach the annual measures to each startup by sector and year of round 2.
df = df.merge(hype[["sector", "year", "sector_vc_share", "heat", "heat_past", "entry_z_l1", "hype_index_l"]]
              .rename(columns={"year": "round2_year"}), on=["sector", "round2_year"], how="left")

# (f) heat_quarter: the same idea as heat but with quarterly shares, for a timing closer to the round itself. Quarters with no deal in a sector count as a share of 0. The mean and SD come from a fixed base period, 2013Q1-2019Q4, which covers the round-2 dates of almost all the estimation sample (only 0.4% are in 2012).
vc["q"] = vc["DealDate"].dt.to_period("Q")
usd_q = (vc.pivot_table(index="q", columns="sector", values="DealSize", aggfunc="sum")
         .reindex(pd.period_range("2012Q1", DATA_END.to_period("Q"), freq="Q")).fillna(0))
share_q = usd_q.div(usd_q.sum(axis=1), axis=0)
ref = share_q.loc["2013Q1":"2019Q4"]
hq = ((share_q - ref.mean()) / ref.std()).stack().rename("heat_quarter").reset_index()
hq.columns = ["q", "sector", "heat_quarter"]
# Write the quarter as yyyyq so it matches round2_yq, then attach it by sector and quarter of round 2.
hq["round2_yq"] = hq["q"].dt.year * 10 + hq["q"].dt.quarter
df = df.merge(hq[["round2_yq", "sector", "heat_quarter"]], on=["round2_yq", "sector"], how="left")


# 6. SAVE
########################################################################################################
# Variable labels for Stata. The order of this dictionary is also the column order of the output files.
labels = {
    "company_id": "PitchBook company ID",
    "sector": "Industry sector", "sector_id": "Sector code (i.sector_id)",
    "state": "US state of HQ", "state_id": "State code (i.state_id)",
    "year_founded": "Founding year",
    "round1_date": "Date of 1st VC round", "round2_date": "Date of 2nd VC round",
    "round1_year": "Year of 1st VC round", "round2_year": "Year of 2nd VC round",
    "round2_yq": "Year-quarter of 2nd round (yyyyq, time FE)",
    "sector_year_id": "Sector x year of 2nd round (main cluster)",
    "sector_quarter_id": "Sector x quarter of 2nd round (cluster, quarterly heat)",
    "gap_months": "Months between 1st and 2nd VC round",
    "log_gap": "ln(1 + gap in months): fundraising speed",
    "exit_3y": "Exit (IPO or acquisition) within 3 years of 2nd round",
    "failure_3y": "Failure within 3 years of 2nd round",
    "round3_within_3y": "3rd VC round within 3 years of 2nd round",
    "full_3y_window": "Full 3-year window observed (estimation sample)",
    "months_to_outcome": "Months from 2nd round to exit, failure or data end",
    "outcome_is_exit": "Survival clock ended by an exit",
    "outcome_is_failure": "Survival clock ended by a failure",
    "log_round1_size": "ln(1 + amount of 1st VC round, $M)",
    "round1_number": "Financing deal number of the 1st VC round",
    "startup_age_at_round1": "Startup age at 1st VC round (years)",
    "lead_type": "Lead investor type, 1st VC round",
    "lead_investor_age": "Lead investor age at 1st VC round (years)",
    "log_round2_size": "ln(1 + amount of 2nd VC round, $M)",
    "valuation_step_up": "Pre-money r2 / post-money r1",
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
    "sector_vc_share": "Sector share of all VC $, year of 2nd round",
    "heat": "Heat: z of sector VC share within sector (main)",
    "heat_quarter": "Quarterly heat: z of quarter share (2013-19 base)",
    "heat_past": "Heat using only past years (no look-ahead)",
    "entry_z_l1": "Startups founded in sector, z, previous year",
    "hype_index_l": "Hype index: (heat + entry_z_l1) / 2",
}
# Keep only the 47 variables, one row per startup sorted by ID, and write the CSV.
df = df[list(labels)].sort_values("company_id").reset_index(drop=True)
df.to_csv(OUT / "rq1_core_dataset.csv", index=False)
# Stata cannot store missing text values, so text columns get "" instead of a missing value in the .dta.
st = df.copy()
for c in ["sector", "state", "lead_type"]:
    st[c] = st[c].fillna("").astype(str)
st.to_stata(OUT / "rq1_core_dataset.dta", write_index=False, version=118, variable_labels=labels)
print(f"Rows: {len(df):,} | estimation sample (full_3y_window): {df['full_3y_window'].sum():,} | variables: {df.shape[1]}")
