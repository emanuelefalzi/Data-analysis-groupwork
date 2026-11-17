********************************************************************************
* rq1_addon_not_in_log_checks.do  (add-on; does not change any existing file)
*
* WHAT IT CONTAINS
*   The analyses of paper v4 (paper_group21.pdf, 15/11/2026) that were computed
*   outside Stata (Python or by hand), so that each of their numbers is in a
*   Stata log with a line number:
*     A. Table 12: team and lead-investor-age controls (H2 logits).
*        This block absorbs rq1_addon_extra_controls.do (that file is kept as is).
*     B. Figure 8: exit / failure / still private within 5 years, by gap quintile.
*     C. Figure 17: Frisch-Waugh-Lovell binned scatter of exit and failure on ln gap.
*     D. Figure 19: valuation step, total and per year, by gap quintile.
*     E. The further checks of Section 5.4 on the H2 exit model (exit_h2):
*        E1 sector x quarter hype, E2 industry-group hype (year and quarter),
*        E3 sector share of all exits in the window, E4 robust SEs,
*        E5 without one-round startups with an outcome within 13 months,
*        E6 VIFs with the gap uncentred and centred.
*     F. N of the average marginal effects (4,444 vs 4,483 two-round startups).
*   No wild cluster bootstrap (boottest): not done, Lele's decision of 17/11/2026.
*
* DEPENDS ON (all in the Stata working directory)
*   group_21_dataset.dta   = 2. dataset/dataset.dta, renamed (see RULES.md)
*   pitchbook_course.dta   from 0. dati iniziali/pitchbook_course.dta.zip (blocks A, E2, E3)
*   Deal.csv               from 0. dati iniziali/Deal.csv.zip (block E2)
*   esttab (estout) installed: ssc install estout
*
* HOW TO RUN
*   Stata 17, same working directory as rq1_two_group_analysis_v2.do:
*     do rq1_addon_not_in_log_checks.do
*   Run the whole file in one go (blocks use tempfiles made by earlier blocks).
*
* OUTPUT
*   not_in_log_checks.log            (repo: 4. risultati/not_in_log_checks.txt)
*   RQ1_tables_not_in_log_checks.rtf (repo: 4. risultati/RQ1_tables_not_in_log_checks.rtf)
*   figures/x1_outcomes_by_gap_quintile.png        (paper Figure 8)
*   figures/x2_fwl_outcomes_by_gap.png             (paper Figure 17)
*   figures/x3_valuation_step_by_gap_quintile.png  (paper Figure 19)
*
* Section 1 below is copied unchanged from rq1_two_group_analysis_v2.do, so
* samples and specifications match regression_analysis.txt. Only the log name
* differs. These models describe associations, not causal effects.
********************************************************************************

* --- copied from rq1_two_group_analysis_v2.do lines 1-12 (log name changed, version added)
clear all
version 17
set more off
capture log close

log using not_in_log_checks.log, replace text
use "group_21_dataset.dta", clear
capture mkdir figures
capture which esttab
capture which coefplot

set scheme s1color
global LOOK "graphregion(color(white)) plotregion(color(white)) ylabel(, angle(0) glcolor(gs15)) legend(region(lcolor(white)))"

********************************************************************************
* 1. PREPARE THE VARIABLES (copied from rq1_two_group_analysis_v2.do lines 14-58)
********************************************************************************

* --- main file lines 18-20
* Lead investor type as a categorical for i. (base = "No lead identified").
label define lead_lbl 0 "No lead identified"
encode lead_type, generate(lead_cat) label(lead_lbl)

* --- main file lines 22-23
* Two startups have a negative age at round 1 (data errors).
replace startup_age_at_round1 = . if startup_age_at_round1 < 0

* --- main file lines 25-26
* Valuation step in logs (long right tail).
generate log_delta_v = ln(delta_v)

* --- main file lines 28-43
* Short labels, used in the tables and graphs.
label define rounds_lbl 0 "One round" 1 "Two or more rounds"
label values two_rounds rounds_lbl
label variable two_rounds "Two or more rounds (R)"
label variable log_gap_r2 "R x ln(1 + months between rounds)"
label variable log_gap "ln(1 + months between rounds)"
label variable heat "Hype at round 1"
label variable heat_past "Hype at round 1, past years only"
label variable log_round1_size "ln(1 + round-1 amount, USD M)"
label variable round1_number "Deal number of round 1"
label variable startup_age_at_round1 "Startup age at round 1 (years)"
label variable lead_cat "Lead investor type"
label variable exit_5y "Exit within 5 years"
label variable failure_5y "Failure within 5 years"
label variable gap_months "Months between rounds 1 and 2"
label variable log_delta_v "ln(post-money r2 / post-money r1)"

* --- main file lines 45-51
* Hype terciles (cold, middle, hot) and gap quintiles, for the descriptive graphs.
xtile heat_t = heat if full_window == 1, nq(3)
label define heat_lbl 1 "Cold" 2 "Middle" 3 "Hot"
label values heat_t heat_lbl
xtile gap_q = gap_months if full_window == 1 & two_rounds == 1, nq(5)
label define gap_lbl 1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest"
label values gap_q gap_lbl

* --- main file lines 53-55
* Controls at round 1 and fixed effects, used in every model.
global X  "log_round1_size round1_number startup_age_at_round1 i.lead_cat"
global FE "i.round1_yq i.sector_id i.state_id"

* --- main file lines 57-58
* Common options for the Word tables: all variables, fixed effects as Yes rows.
global TAB `"label b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) nobaselevels interaction(" x ") indicate("Year-quarter FE = *.round1_yq" "Sector FE = *.sector_id" "State FE = *.state_id") addnotes("Standard errors clustered by sector x year of round 1 in parentheses.")"'

* --- new in this file: same options, note for the table of checks (clusters vary).
global TABE `"label b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) nobaselevels interaction(" x ") indicate("Year-quarter FE = *.round1_yq" "Sector FE = *.sector_id" "State FE = *.state_id") addnotes("Standard errors clustered at the level in the Clusters row; column E4 uses robust standard errors.")"'

* Original row order, restored after every merge or sort.
generate long _order = _n

********************************************************************************
* A. TABLE 12: TEAM AND LEAD-INVESTOR-AGE CONTROLS
*    Content of rq1_addon_extra_controls.do (lines 13-44), with new variable
*    names only, so the later blocks are not changed. Paper: exit beta1 = -0.100
*    in both columns, beta3 = -0.035; failure beta1 -0.231 -> -0.229;
*    young lead -0.334 on exit (OR 0.72); AI term -0.607 on failure; 41 clusters.
********************************************************************************

* Course-file variables (all fixed before round 1). Industry group and exit
* dates are also kept here, for blocks E2 and E3.
preserve
use CompanyID PrimaryIndustrySector PrimaryIndustryGroup NFounders MBA Has_Core_AI_Term ///
    IPODate AcquiredDate using "pitchbook_course.dta", clear
rename CompanyID company_id
rename PrimaryIndustryGroup igroup
tempfile course
save `course'
restore

merge m:1 company_id using `course', keep(master match) ///
    keepusing(igroup NFounders MBA Has_Core_AI_Term IPODate AcquiredDate) generate(_merge_course)
sort _order
tabulate _merge_course

* Team variables (addon lines 22).
generate ln_founders = ln(NFounders)

* Lead investor age (addon lines 25-27): young = lead firm under 6 years at round 1.
generate byte has_lead      = lead_type != "No lead identified"
generate byte young_lead    = has_lead & lead_investor_age < 6 & !missing(lead_investor_age)
generate byte lead_age_miss = has_lead & missing(lead_investor_age)

label variable ln_founders      "ln(number of founders)"
label variable MBA              "MBA founder"
label variable Has_Core_AI_Term "AI term in description"
label variable young_lead       "Young lead investor (< 6 years)"
label variable lead_age_miss    "Lead identified, age missing"

local extra ln_founders MBA Has_Core_AI_Term young_lead lead_age_miss

* Same sample for both columns: startups with founder data (addon line 33).
generate byte team_ok = !missing(ln_founders, MBA)
count if full_window == 1
count if full_window == 1 & team_ok
count if full_window == 1 & team_ok & missing(Has_Core_AI_Term)

* Four logits (addon lines 35-42): exit and failure, without and with the extra controls.
foreach y in exit_5y failure_5y {
    logit `y' i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
        if full_window == 1 & team_ok, vce(cluster sector_year_id)
    estimates store `y'_same
    logit `y' i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE `extra' ///
        if full_window == 1 & team_ok, vce(cluster sector_year_id)
    estimates store `y'_extra
}

* Table 12 in the log (addon lines 43-44, plus clusters).
estimates table exit_5y_same exit_5y_extra failure_5y_same failure_5y_extra, ///
    keep(log_gap_r2 c.log_gap_r2#c.heat `extra') b(%9.3f) se(%9.3f) p(%9.3f) stats(N N_clust)

* Odds ratio of the young-lead coefficient in the exit model with extra controls.
estimates restore exit_5y_extra
display "Young lead, exit (+ extra): coefficient = " %6.3f _b[young_lead] ", odds ratio = " %5.3f exp(_b[young_lead])

* Table 12 (Word): first table of this file, so replace.
esttab exit_5y_same exit_5y_extra failure_5y_same failure_5y_extra ///
    using "RQ1_tables_not_in_log_checks.rtf", replace $TAB ///
    mtitles("Exit: same sample" "Exit: + extra" "Failure: same sample" "Failure: + extra") ///
    stats(N N_clust r2_p, labels("Observations" "Clusters (sector x year)" "Pseudo R2")) ///
    title("Table 12. Adding team and lead-investor-age controls (logit, H2 specification)")

********************************************************************************
* B. FIGURE 8: EXIT / FAILURE / STILL PRIVATE WITHIN 5 YEARS, BY GAP QUINTILE
*    5-year sample. Two-round startups by gap_q (main file line 49), one-round
*    startups for comparison. Startups with both an exit and a failure in the
*    window count as exits. Paper: exit 21%-24% across quintiles; failure 14%
*    (fastest) to 9% (slowest); still private 64% to 69%; one round 16/32/53%.
********************************************************************************

* Startups with both outcomes in the window (paper: 14).
count if full_window == 1 & exit_5y == 1 & failure_5y == 1

generate byte out_exit = exit_5y == 1 if full_window == 1
generate byte out_fail = failure_5y == 1 & exit_5y == 0 if full_window == 1
generate byte out_priv = 1 - out_exit - out_fail if full_window == 1
label variable out_exit "Exit"
label variable out_fail "Failure"
label variable out_priv "Still private"

generate byte grp8 = gap_q if full_window == 1 & two_rounds == 1
replace grp8 = 6 if full_window == 1 & two_rounds == 0
label define grp8_lbl 1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest" 6 "One round"
label values grp8 grp8_lbl

* Shares by group (the numbers of Figure 8).
tabstat out_exit out_fail out_priv, by(grp8) statistics(n mean) format(%5.3f)

* X1. Stacked bars.
graph bar (mean) out_exit out_fail out_priv, over(grp8) stack ///
    bar(1, color(navy)) bar(2, color(cranberry)) bar(3, color(gs12)) ///
    blabel(bar, position(center) format(%4.2f)) ///
    ytitle("Share of startups, 5-year window") b1title("Quintile of months between rounds, and one-round startups") ///
    legend(order(1 "Exit" 2 "Failure" 3 "Still private") rows(1)) $LOOK
graph export figures/x1_outcomes_by_gap_quintile.png, replace width(2000)

********************************************************************************
* C. FIGURE 17: BINNED SCATTER, FRISCH-WAUGH-LOVELL
*    Two-round startups in the 5-year sample with all controls. Outcomes and
*    ln gap are residualised on $X $FE by OLS, sample mean added back; 20
*    equal-sized bins of the residualised gap; OLS lines on all observations.
*    Paper: N = 4,483; slope failure -0.030, exit -0.011. Note: one two-round
*    startup has a negative age set to missing in section 1, so N here can be
*    4,482. The paper's -0.030 equals beta3 of the failure model (main log
*    L1308): the slopes printed here are the numbers to use.
********************************************************************************

quietly regress exit_5y log_gap $X $FE if full_window == 1 & two_rounds == 1
generate byte s_fwl = e(sample)
count if s_fwl

foreach v in exit_5y failure_5y log_gap {
    quietly regress `v' $X $FE if s_fwl
    predict double fwl_`v' if s_fwl, residuals
    quietly summarize `v' if s_fwl
    replace fwl_`v' = fwl_`v' + r(mean) if s_fwl
}
label variable fwl_log_gap "ln gap, net of controls and FE"

* Slopes of the residualised outcomes on the residualised gap.
regress fwl_exit_5y fwl_log_gap if s_fwl, vce(cluster sector_year_id)
estimates store fwl_exit
regress fwl_failure_5y fwl_log_gap if s_fwl, vce(cluster sector_year_id)
estimates store fwl_fail

* FWL check: same slope as ln gap in the OLS with all controls.
regress exit_5y log_gap $X $FE if s_fwl, vce(cluster sector_year_id)
estimates store fwl_exit_full
regress failure_5y log_gap $X $FE if s_fwl, vce(cluster sector_year_id)
estimates store fwl_fail_full

estimates table fwl_exit fwl_exit_full fwl_fail fwl_fail_full, ///
    keep(fwl_log_gap log_gap) b(%9.4f) se(%9.4f) p(%9.3f) stats(N)

* 20 bins of the residualised gap and the mean of each variable per bin.
xtile fwl_bin = fwl_log_gap if s_fwl, nq(20)
foreach v in exit_5y failure_5y log_gap {
    egen double fwlb_`v' = mean(fwl_`v') if s_fwl, by(fwl_bin)
}
egen byte fwl_tag = tag(fwl_bin) if s_fwl
sort _order

tabstat fwl_log_gap fwl_exit_5y fwl_failure_5y if s_fwl, by(fwl_bin) statistics(n mean) format(%6.3f)

* X2. Bin means and OLS lines on all observations.
twoway (scatter fwlb_exit_5y fwlb_log_gap if fwl_tag == 1 & s_fwl, mcolor(navy)) ///
       (lfit fwl_exit_5y fwl_log_gap if s_fwl, lcolor(navy) lwidth(medthick)) ///
       (scatter fwlb_failure_5y fwlb_log_gap if fwl_tag == 1 & s_fwl, mcolor(cranberry) msymbol(D)) ///
       (lfit fwl_failure_5y fwl_log_gap if s_fwl, lcolor(cranberry) lwidth(medthick)), ///
    xtitle("ln(1 + months between rounds), net of controls and FE") ///
    ytitle("Share within 5 years, net of controls and FE") ///
    legend(order(1 "Exit" 3 "Failure") rows(1)) $LOOK
graph export figures/x2_fwl_outcomes_by_gap.png, replace width(2000)

********************************************************************************
* D. FIGURE 19: VALUATION STEP, TOTAL AND PER YEAR, BY GAP QUINTILE
*    Two-round startups with both post-money valuations and a gap of at least
*    one month. Not restricted to full_window (like the H3 model). Quintiles
*    computed in this sample. Paper: N = 7,514; total step about 1.06-1.08 in
*    Q1-Q4 and 1.18 in Q5; median per year 1.89 (Q1, median gap 7 months) to
*    0.36 (Q5, 35 months).
********************************************************************************

generate byte s_val = two_rounds == 1 & !missing(log_delta_v) & !missing(gap_months) & gap_months >= 1
count if s_val

xtile val_q = gap_months if s_val, nq(5)
label values val_q gap_lbl
generate double step_per_year = log_delta_v / (gap_months / 12) if s_val
label variable step_per_year "ln(V2/V1) per year of gap"

* Gap, total step and step per year by quintile.
tabstat gap_months if s_val, by(val_q) statistics(n p50) format(%6.2f)
tabstat log_delta_v if s_val, by(val_q) statistics(n mean sd) format(%6.3f)
tabstat step_per_year if s_val, by(val_q) statistics(n p25 p50 p75) format(%6.3f)

* 95% confidence intervals of the mean total step.
forvalues q = 1/5 {
    ci means log_delta_v if s_val & val_q == `q'
}

* X3. Left: mean total step with 95% CI. Right: median step per year with IQR.
preserve
keep if s_val
collapse (mean) m_tot = log_delta_v (sd) sd_tot = log_delta_v (count) n_tot = log_delta_v ///
    (p25) p25_yr = step_per_year (p50) p50_yr = step_per_year (p75) p75_yr = step_per_year ///
    (p50) gap_med = gap_months, by(val_q)
generate double lo_tot = m_tot - invttail(n_tot - 1, 0.025) * sd_tot / sqrt(n_tot)
generate double hi_tot = m_tot + invttail(n_tot - 1, 0.025) * sd_tot / sqrt(n_tot)
list val_q n_tot gap_med m_tot lo_tot hi_tot p25_yr p50_yr p75_yr, noobs separator(0)

twoway (bar m_tot val_q, barwidth(0.7) color(navy%70)) ///
       (rcap hi_tot lo_tot val_q, lcolor(black)), ///
    xlabel(1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest") xtitle("Quintile of months between rounds") ///
    ytitle("Mean ln(V2/V1)") title("Total step", size(medium)) $LOOK legend(off) ///
    name(x3_left, replace) nodraw
twoway (bar p50_yr val_q, barwidth(0.7) color(cranberry%70)) ///
       (rcap p75_yr p25_yr val_q, lcolor(black)), ///
    xlabel(1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest") xtitle("Quintile of months between rounds") ///
    ytitle("Median ln(V2/V1) per year of gap") title("Step per year", size(medium)) $LOOK legend(off) ///
    name(x3_right, replace) nodraw
graph combine x3_left x3_right, rows(1) graphregion(color(white)) xsize(10) ysize(4.5)
graph export figures/x3_valuation_step_by_gap_quintile.png, replace width(2000)
restore

********************************************************************************
* E. FURTHER CHECKS OF SECTION 5.4 ON THE H2 EXIT MODEL (exit_h2)
*    beta1 = coefficient of log_gap_r2; beta3 = coefficient of
*    c.log_gap_r2#c.hv (gap x hype, which tests H2). hv holds the hype measure
*    of each check, so every column has the same coefficient names.
********************************************************************************

generate double hv = heat
label variable hv "Hype (measure varies by column)"

* E0. exit_h2 with hv = heat: must match regression_analysis.txt L521-541
*     (N = 9,124, 41 clusters, beta1 = -0.071, beta3 = -0.056).
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store e0_main

* E1. Sector x quarter hype, clustered by sector x quarter (paper: 149 clusters).
replace hv = heat_quarter
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(cluster sector_quarter_id)
estimates store e1_sq

* ---------------------------------------------------------------------------
* E2. Hype by PitchBook industry group (paper: 42 groups; 191 clusters by
*     group x year, 575 by group x quarter). Not in the dataset: built here from
*     Deal.csv and pitchbook_course.dta with the rules of heat and heat_quarter
*     in 1. python/dataset.py (lines 61-64, 219-260). The paper's original
*     Python code is not in the repo. Check: the same code run by sector must
*     give back heat and heat_quarter exactly, or the do-file stops.
* ---------------------------------------------------------------------------

* Completed VC deals of the course startups (dataset.py lines 61-64, 74, 220-221).
preserve
import delimited using "Deal.csv", clear varnames(1) case(preserve) colrange(1:20) ///
    stringcols(1 5) asdouble encoding("utf-8") bindquote(strict)
keep CompanyID DealDate DealType DealStatus DealSize
confirm numeric variable DealSize
generate ddate = date(DealDate, "MDY")
format ddate %td
keep if !missing(ddate) & DealStatus == "Completed"
keep if inlist(DealType, "Seed Round", "Early Stage VC", "Later Stage VC")
rename CompanyID company_id
merge m:1 company_id using `course', keep(match) nogenerate keepusing(PrimaryIndustrySector igroup)
rename PrimaryIndustrySector sector
count
tempfile vcdeals
save `vcdeals'

foreach g in sector igroup {
    * Annual: share of all VC $ in the year (from 2012), z-score within the group (dataset.py lines 224-231).
    use `vcdeals', clear
    drop if `g' == ""
    generate year = year(ddate)
    keep if year >= 2012
    collapse (sum) usd = DealSize, by(`g' year)
    bysort year: egen double usd_all = total(usd)
    generate double share = usd / usd_all
    bysort `g': egen double m = mean(share)
    bysort `g': egen double s = sd(share)
    generate double hy_`g' = (share - m) / s
    rename year round1_year
    keep `g' round1_year hy_`g'
    tempfile hy_`g'
    save `hy_`g''

    * Quarterly: 2012q1-2022q2, empty quarters = 0, mean and SD over 2013q1-2019q4 (dataset.py lines 251-259).
    use `vcdeals', clear
    drop if `g' == ""
    generate q = qofd(ddate)
    keep if q >= tq(2012q1) & q <= tq(2022q2)
    collapse (sum) usd = DealSize, by(`g' q)
    fillin `g' q
    replace usd = 0 if _fillin == 1
    bysort q: egen double usd_all = total(usd)
    generate double share = usd / usd_all
    generate byte ref = q >= tq(2013q1) & q <= tq(2019q4)
    bysort `g': egen double m = mean(cond(ref, share, .))
    bysort `g': egen double s = sd(cond(ref, share, .))
    generate double hq_`g' = (share - m) / s
    * Variant: mean and SD over all quarters 2012q1-2022q2 (used for industry groups only).
    bysort `g': egen double m_all = mean(share)
    bysort `g': egen double s_all = sd(share)
    generate double hqa_`g' = (share - m_all) / s_all
    generate round1_yq = year(dofq(q)) * 10 + quarter(dofq(q))
    keep `g' round1_yq hq_`g' hqa_`g'
    tempfile hq_`g'
    save `hq_`g''
}
restore

merge m:1 sector round1_year using `hy_sector', keep(master match) nogenerate
merge m:1 sector round1_yq   using `hq_sector', keep(master match) nogenerate keepusing(hq_sector)
merge m:1 igroup round1_year using `hy_igroup', keep(master match) nogenerate
merge m:1 igroup round1_yq   using `hq_igroup', keep(master match) nogenerate
sort _order

* Check: the rebuild by sector equals heat and heat_quarter in the dataset.
generate double chk_heat  = abs(hy_sector - heat)
generate double chk_heatq = abs(hq_sector - heat_quarter)
summarize chk_heat chk_heatq
count if missing(hy_sector) != missing(heat)
assert r(N) == 0
count if missing(hq_sector) != missing(heat_quarter)
assert r(N) == 0
assert chk_heat < 1e-6 if !missing(chk_heat)
assert chk_heatq < 1e-6 if !missing(chk_heatq)
display "Check passed: the hype code reproduces heat and heat_quarter exactly."

label variable hy_igroup  "Hype, industry group x year"
label variable hq_igroup  "Hype, industry group x quarter (2013-19 base)"
label variable hqa_igroup "Hype, industry group x quarter (all-quarter base)"

* Cluster IDs: industry group x year and industry group x quarter of round 1.
egen ig_year_id    = group(igroup round1_year)
egen ig_quarter_id = group(igroup round1_yq)

* Number of industry groups: full sample and 5-year sample.
quietly tabulate igroup
display "Industry groups, full sample: " r(r)
quietly tabulate igroup if full_window == 1
display "Industry groups, 5-year sample: " r(r)

* E2a. Industry group x year hype, clustered by group x year.
replace hv = hy_igroup
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(cluster ig_year_id)
estimates store e2_igy

* E2b. Industry group x quarter hype (same rule as heat_quarter), clustered by group x quarter.
replace hv = hq_igroup
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(cluster ig_quarter_id)
estimates store e2_igq

* E2c. As E2b, with the all-quarter base (the paper does not say which base it used).
replace hv = hqa_igroup
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(cluster ig_quarter_id)
estimates store e2_igqa

* ---------------------------------------------------------------------------
* E3. Control for the sector's share of all exits during the startup's own
*     5-year window (paper: beta3 = -0.035, p = 0.62). Not in the dataset, and
*     the paper does not define it fully. Our definition: exits (first of IPO
*     or acquisition date) of all companies in pitchbook_course.dta, counted
*     from window_start to window_start + 5 years, both ends included (the
*     exit_5y window); share = exits in the startup's sector / all exits.
* ---------------------------------------------------------------------------

* Window dates in days (window_start is a %tc datetime).
generate ws_d = dofc(window_start)
generate we_d = mdy(month(ws_d), day(ws_d), year(ws_d) + 5)
replace we_d = mdy(2, 28, year(ws_d) + 5) if missing(we_d) & !missing(ws_d)
format ws_d we_d %td

* Check of the window: the startup's own exit date in [ws_d, we_d] must give exit_5y.
generate own_exit_d = min(IPODate, AcquiredDate)
count if full_window == 1 & exit_5y != (!missing(own_exit_d) & own_exit_d >= ws_d & own_exit_d <= we_d)
assert r(N) == 0

* Daily running count of exits by sector and in total.
preserve
use CompanyID PrimaryIndustrySector IPODate AcquiredDate using "pitchbook_course.dta", clear
generate exit_d = min(IPODate, AcquiredDate)
keep if !missing(exit_d) & PrimaryIndustrySector != ""
rename PrimaryIndustrySector sector
summarize exit_d
assert exit_d >= mdy(1, 1, 1980) & exit_d <= mdy(12, 31, 2035)
generate n = 1
collapse (sum) n, by(sector exit_d)
rename exit_d e3_day
tempfile exits
save `exits'

keep sector
duplicates drop
tempfile sectors
save `sectors'

clear
set obs `=mdy(12, 31, 2035) - mdy(1, 1, 1980) + 1'
generate e3_day = mdy(1, 1, 1980) + _n - 1
cross using `sectors'
merge 1:1 sector e3_day using `exits', nogenerate
replace n = 0 if missing(n)
sort sector e3_day
by sector: generate double cum_s = sum(n)
bysort e3_day: egen double cum_all = total(cum_s)
keep sector e3_day cum_s cum_all
tempfile grid
save `grid'
restore

* Exits in the window = running count at we_d minus running count the day before ws_d.
generate e3_day = ws_d - 1
merge m:1 sector e3_day using `grid', keep(master match) nogenerate
rename (cum_s cum_all) (c0_s c0_all)
replace e3_day = we_d
merge m:1 sector e3_day using `grid', keep(master match) nogenerate
rename (cum_s cum_all) (c1_s c1_all)
sort _order
generate double exit_share = (c1_s - c0_s) / (c1_all - c0_all)
label variable exit_share "Sector share of all exits in the window"
summarize exit_share if full_window == 1

replace hv = heat
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv c.exit_share $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store e3_exitsh

* ---------------------------------------------------------------------------
* E4. Robust instead of clustered standard errors (paper: p of beta3 0.36 vs 0.35).
* ---------------------------------------------------------------------------
logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1, vce(robust)
estimates store e4_robust

* ---------------------------------------------------------------------------
* E5. Without one-round startups that exited or failed within 13 months of
*     round 1 (paper: 367 startups; beta1 -0.065, beta3 -0.056).
* ---------------------------------------------------------------------------
generate byte early_out = two_rounds == 0 & months_to_outcome <= 13 & ///
    (outcome_is_exit == 1 | outcome_is_failure == 1)
count if full_window == 1 & early_out == 1

logit exit_5y i.two_rounds##c.hv c.log_gap_r2##c.hv $X $FE ///
    if full_window == 1 & early_out == 0, vce(cluster sector_year_id)
estimates store e5_noearly

* E1-E5 side by side: beta1, beta3, N and clusters.
estimates table e0_main e1_sq e2_igy e2_igq e2_igqa e3_exitsh e4_robust e5_noearly, ///
    keep(log_gap_r2 c.log_gap_r2#c.hv) b(%9.3f) se(%9.3f) p(%9.3f) stats(N N_clust)

esttab e0_main e1_sq e2_igy e2_igq e2_igqa e3_exitsh e4_robust e5_noearly ///
    using "RQ1_tables_not_in_log_checks.rtf", append $TABE ///
    mtitles("Main (heat)" "E1 sector x qtr" "E2 group x year" "E2 group x qtr" ///
            "E2 group x qtr, all-qtr base" "E3 + exit share" "E4 robust SE" "E5 no early exits") ///
    stats(N N_clust r2_p, labels("Observations" "Clusters" "Pseudo R2")) ///
    title("Further checks of the H2 exit model (paper Section 5.4)")

* ---------------------------------------------------------------------------
* E6. Variance inflation factors, H2 specification as an LPM (paper: controls
*     below 2; R, gap and interactions 10-19 uncentred, below 2.5 centred).
* ---------------------------------------------------------------------------
regress exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE if full_window == 1
estimates store e6_lpm
estat vif

* Centre ln gap at its mean among two-round startups in the same sample.
quietly summarize log_gap if e(sample) & two_rounds == 1
display "Mean ln gap used for centring: " %6.4f r(mean)
generate double log_gap_r2_c = cond(two_rounds == 1, log_gap - r(mean), 0) if !missing(log_gap_r2)
label variable log_gap_r2_c "R x ln gap, centred"

regress exit_5y i.two_rounds##c.heat c.log_gap_r2_c##c.heat $X $FE if full_window == 1
estimates store e6_lpm_c
estat vif

* Centring is a reparametrisation: beta1 and beta3 and their SEs do not change.
estimates table e6_lpm e6_lpm_c, ///
    keep(log_gap_r2 c.log_gap_r2#c.heat log_gap_r2_c c.log_gap_r2_c#c.heat) b(%9.4f) se(%9.4f)

********************************************************************************
* F. N OF THE AVERAGE MARGINAL EFFECTS
*    The AMEs of the exit model use N = 4,444 two-round startups (main log
*    L659), not 4,483. Same model as exit_h2 (main file lines 144-149).
********************************************************************************

logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store exit_h2
generate byte in_h2 = e(sample)

* Same AMEs as main log L657-670 (consistency check).
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-1 0 1))

count if full_window == 1 & two_rounds == 1
count if in_h2 == 1 & two_rounds == 1

* Two-round startups in the 5-year sample that the logit does not use, and why:
* a missing control, or a lead type or state that predicts no exit perfectly.
count if full_window == 1 & two_rounds == 1 & in_h2 == 0
count if full_window == 1 & two_rounds == 1 & in_h2 == 0 & missing(startup_age_at_round1)
tabulate lead_cat if full_window == 1 & two_rounds == 1 & in_h2 == 0
tabulate state if full_window == 1 & two_rounds == 1 & in_h2 == 0

* These models describe associations. They do not establish causality.

log close
