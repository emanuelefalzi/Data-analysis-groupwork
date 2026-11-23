clear all
set more off
capture log close

log using regression_analysis.log, replace text
use "group_21_dataset.dta", clear
capture mkdir figures
capture which esttab
capture which coefplot

set scheme s1color
global LOOK "graphregion(color(white)) plotregion(color(white)) ylabel(, angle(0) glcolor(gs15)) legend(region(lcolor(white)))"

********************************************************************************
* 1. PREPARE THE VARIABLES
********************************************************************************

* Lead investor type as a categorical (base = "No lead identified").
label define lead_lbl 0 "No lead identified"
encode lead_type, generate(lead_cat) label(lead_lbl)

* Two startups have a negative age at round 1 (data errors).
replace startup_age_at_round1 = . if startup_age_at_round1 < 0

* Valuation step in logs (long right tail).
generate log_delta_v = ln(delta_v)


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

* New variables (19-20 Nov): raw VC-share hype, gap in months, failure with no window.
* vc_share = sector % of all VC $ in the year of round 1 (no z-score, as the TA suggested).
generate vc_share = 100 * sector_vc_share
label variable vc_share "Hype: sector % of VC $ (raw share)"
* Same share minus the sector's own average (raw units, only the movement over time).
bysort sector_id round1_year: generate byte tag_sy = _n == 1 & !missing(vc_share)
bysort sector_id: egen vc_share_mean = mean(cond(tag_sy == 1, vc_share, .))
generate vc_share_dm = vc_share - vc_share_mean
label variable vc_share_dm "Hype: VC share minus sector mean (pp)"
drop tag_sy vc_share_mean
* Gap in months (0 for one-round startups, like log_gap_r2).
generate gap_r2 = two_rounds * gap_months
replace gap_r2 = 0 if two_rounds == 0
label variable gap_r2 "R x months between rounds"
* Failure with no window: failure before any exit by the end of the data.
generate failure_ever = outcome_is_failure
label variable failure_ever "Failure (no window)"
label variable exit "Exit (no window)"

* Hype terciles (cold, middle, hot) and gap quintiles, for the descriptive graphs.
xtile heat_t = heat if full_window == 1, nq(3)
label define heat_lbl 1 "Cold" 2 "Middle" 3 "Hot"
label values heat_t heat_lbl
xtile gap_q = gap_months if full_window == 1 & two_rounds == 1, nq(5)
label define gap_lbl 1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest"
label values gap_q gap_lbl

* Controls at round 1 and fixed effects, used in every model.
global X  "log_round1_size round1_number startup_age_at_round1 i.lead_cat"
global FE "i.round1_yq i.sector_id i.state_id"

* Common options for the tables
global TAB `"label b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) nobaselevels interaction(" x ") indicate("Year-quarter FE = *.round1_yq" "Sector FE = *.sector_id" "State FE = *.state_id") addnotes("Standard errors clustered by sector x year of round 1 in parentheses.")"'

********************************************************************************
* 2. DESCRIPTIVE STATISTICS
********************************************************************************

* Main sample: startups whose 5-year window is fully observed.
count if full_window == 1
tabulate two_rounds if full_window == 1

* Table 1: means and SDs by group.
estpost tabstat exit_5y failure_5y gap_months log_round1_size round1_number ///
    startup_age_at_round1 heat if full_window == 1, ///
    by(two_rounds) statistics(mean sd) columns(statistics)
esttab using "RQ1_tables.rtf", replace cells("mean(fmt(3)) sd(fmt(3))") ///
    unstack noobs nonumber label title("Table 1. Descriptive statistics by group")

* Do the groups differ? (difference in means)
ttest exit_5y if full_window == 1, by(two_rounds)
ttest failure_5y if full_window == 1, by(two_rounds)

* Distribution of the gap between rounds.
histogram gap_months if full_window == 1, width(3) frequency ///
    color(navy%70) lcolor(white) ///
    xtitle("Months between rounds 1 and 2") ytitle("Startups") $LOOK
graph export figures/d1_gap_histogram.png, replace width(2000)

* Startups per round-1 year, by group.
graph bar (count) exit, over(two_rounds) over(round1_year, label(angle(45))) ///
    asyvars stack bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Startups") legend(rows(1)) $LOOK
graph export figures/d2_startups_by_year.png, replace width(2000)

* Hype over time in each sector.
preserve
collapse (mean) heat, by(sector round1_year)
twoway connected heat round1_year, by(sector, note("") graphregion(color(white))) ///
    lcolor(navy) mcolor(navy) msize(small) yline(0, lcolor(gs10) lpattern(dash)) ///
    ytitle("Hype (z-score)") xtitle("Year of round 1") ylabel(, angle(0) glcolor(gs15))
graph export figures/d3_hype_by_sector.png, replace width(2000)
restore

* Exit and failure rates by sector.
graph hbar (mean) exit_5y failure_5y if full_window == 1, ///
    over(sector, sort(1) descending label(labsize(small))) ///
    bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Share of startups") legend(order(1 "Exit within 5 years" 2 "Failure within 5 years") rows(1)) $LOOK
graph export figures/d4_outcomes_by_sector.png, replace width(2000)

* Exit rate by group in cold, middle and hot markets.
graph bar (mean) exit_5y if full_window == 1, over(two_rounds) over(heat_t) ///
    asyvars bar(1, color(navy)) bar(2, color(cranberry)) blabel(bar, format(%4.2f)) ///
    ytitle("Share exiting within 5 years") legend(rows(1)) $LOOK
graph export figures/d5_exit_by_group_hype.png, replace width(2000)

* Exit rate by gap quintile, cold vs hot markets (two-round startups, no controls).
graph bar (mean) exit_5y if full_window == 1 & two_rounds == 1 & heat_t != 2, ///
    over(heat_t) over(gap_q) asyvars bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Share exiting within 5 years") b1title("Quintile of months between rounds") ///
    legend(order(1 "Cold market" 2 "Hot market") rows(1)) $LOOK
graph export figures/d6_exit_by_gap_quintile.png, replace width(2000)

* Size of round 1 by group.
twoway (kdensity log_round1_size if full_window == 1 & two_rounds == 0, lcolor(navy) lwidth(medthick)) ///
       (kdensity log_round1_size if full_window == 1 & two_rounds == 1, lcolor(cranberry) lwidth(medthick)), ///
    xtitle("ln(1 + round-1 amount, USD M)") ytitle("Density") ///
    legend(order(1 "One round" 2 "Two or more rounds") rows(1)) $LOOK
graph export figures/d7_round1_size.png, replace width(2000)

* Exit rate by lead investor type (types with at least 100 startups).
bysort lead_cat: egen lead_n = total(full_window)
graph hbar (mean) exit_5y if full_window == 1 & lead_n >= 100, ///
    over(lead_cat, sort(1) descending label(labsize(small))) bar(1, color(navy)) ///
    ytitle("Share exiting within 5 years") $LOOK
graph export figures/d8_exit_by_lead_type.png, replace width(2000)

********************************************************************************
* 3. MAIN MODEL: LOGIT OF EXIT WITHIN 5 YEARS
********************************************************************************

* H1: gap, group and hype without interactions.
logit exit_5y i.two_rounds c.log_gap_r2 c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store exit_h1

* H2: add the interactions with hype. beta3 = c.log_gap_r2#c.heat.
logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store exit_h2

* Effect of the gap in a cold (-1 SD), normal and hot (+1 SD) market.
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-1 0 1))
* Hot minus cold: is the difference significant?
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-1 1)) contrast(atcontrast(r))

* Effect of the gap along hype. H2 holds if the line is not flat.
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plotopts(lcolor(navy) lwidth(medthick)) ciopts(color(navy%20) lwidth(none)) ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    ytitle("Effect of ln(gap) on Pr(exit)") xtitle("Market hype at round 1 (SD)") $LOOK
graph export figures/m1_exit_effect_by_hype.png, replace width(2000)

* Predicted exit by months between rounds, cold vs hot market.
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Pr(exit within 5 years)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m2_exit_by_gap.png, replace width(2000)

* Predicted exit for one round vs two rounds along hype.
margins two_rounds, at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xtitle("Market hype at round 1 (SD)") ytitle("Pr(exit within 5 years)") ///
    legend(order(3 "One round" 4 "Two or more rounds") rows(1)) $LOOK
graph export figures/m3_exit_by_group.png, replace width(2000)

* All coefficients of the main model (fixed effects not shown), with 95% Confidence Intervals.
coefplot exit_h2, drop(_cons *.round1_yq *.sector_id *.state_id) xline(0, lcolor(gs8) lpattern(dash)) ///
    mcolor(navy) ciopts(lcolor(navy)) label ///
    xtitle("Logit coefficient") ylabel(, labsize(small)) $LOOK
graph export figures/m4_exit_coefficients.png, replace width(2000)

* Same model as LPM.
regress exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store exit_lpm

* Table 2: exit models, all variables.
esttab exit_h1 exit_h2 exit_lpm using "RQ1_tables.rtf", append $TAB ///
    mtitles("Logit H1" "Logit H2" "LPM H2") stats(N r2_p r2, labels("Observations" "Pseudo R2" "R2")) ///
    title("Table 2. Time between rounds, hype and exit within 5 years")

********************************************************************************
* 4. FAILURE WITHIN 5 YEARS
********************************************************************************

logit failure_5y i.two_rounds c.log_gap_r2 c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store fail_h1

logit failure_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store fail_h2

* Effect of the gap on failure along hype.
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plotopts(lcolor(cranberry) lwidth(medthick)) ciopts(color(cranberry%20) lwidth(none)) ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    ytitle("Effect of ln(gap) on Pr(failure)") xtitle("Market hype at round 1 (SD)") $LOOK
graph export figures/m5_failure_effect_by_hype.png, replace width(2000)

* Predicted failure by months between rounds, cold vs hot market.
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Pr(failure within 5 years)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m6_failure_by_gap.png, replace width(2000)

* Table 3: failure models, all variables.
esttab fail_h1 fail_h2 using "RQ1_tables.rtf", append $TAB ///
    mtitles("Logit H1" "Logit H2") stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 3. Time between rounds, hype and failure within 5 years")

********************************************************************************
* 5. SENSITIVITY: 4- AND 6-YEAR WINDOWS
********************************************************************************

* If beta3 changes a lot between 4, 5 and 6 years, 5 years is not a safe cut. => result stays robust
logit exit_4y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window_4y == 1, vce(cluster sector_year_id)
estimates store exit_4y

logit exit_6y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window_6y == 1, vce(cluster sector_year_id)
estimates store exit_6y

logit failure_4y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window_4y == 1, vce(cluster sector_year_id)
estimates store fail_4y

logit failure_6y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window_6y == 1, vce(cluster sector_year_id)
estimates store fail_6y

* Gap and gap x hype coefficients for 4, 5 and 6 years.
coefplot (exit_4y, label("4 years") mcolor(navy%50) ciopts(lcolor(navy%50))) ///
         (exit_h2, label("5 years") mcolor(navy) ciopts(lcolor(navy))) ///
         (exit_6y, label("6 years") mcolor(cranberry) ciopts(lcolor(cranberry))), ///
    keep(log_gap_r2 c.log_gap_r2#c.heat) xline(0, lcolor(gs8) lpattern(dash)) ///
    coeflabels(log_gap_r2 = "Gap (beta1)" c.log_gap_r2#c.heat = "Gap x hype (beta3)") ///
    xtitle("Logit coefficient, exit") legend(rows(1)) $LOOK
graph export figures/m7_windows_exit.png, replace width(2000)

* The same for failure.
coefplot (fail_4y, label("4 years") mcolor(navy%50) ciopts(lcolor(navy%50))) ///
         (fail_h2, label("5 years") mcolor(navy) ciopts(lcolor(navy))) ///
         (fail_6y, label("6 years") mcolor(cranberry) ciopts(lcolor(cranberry))), ///
    keep(log_gap_r2 c.log_gap_r2#c.heat) xline(0, lcolor(gs8) lpattern(dash)) ///
    coeflabels(log_gap_r2 = "Gap (beta1)" c.log_gap_r2#c.heat = "Gap x hype (beta3)") ///
    xtitle("Logit coefficient, failure") legend(rows(1)) $LOOK
graph export figures/m8_windows_failure.png, replace width(2000)

* Table 4: window sensitivity, all variables.
esttab exit_4y exit_h2 exit_6y fail_4y fail_h2 fail_6y using "RQ1_tables.rtf", append $TAB ///
    mtitles("Exit 4y" "Exit 5y" "Exit 6y" "Failure 4y" "Failure 5y" "Failure 6y") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 4. Sensitivity to the outcome window (logit)")

********************************************************************************
* 6. ROBUSTNESS
********************************************************************************

* (a) Exit at any time, all startups (no window).
logit exit i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE, ///
    vce(cluster sector_year_id)
estimates store rob_ever

* (b) Hype measured with past years only.
logit exit_5y i.two_rounds##c.heat_past c.log_gap_r2##c.heat_past $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store rob_past

* (c) Probit instead of logit.
probit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store rob_probit

* Table 5: robustness, all variables.
esttab rob_ever rob_past rob_probit using "RQ1_tables.rtf", append $TAB ///
    mtitles("Exit ever" "Past hype" "Probit") stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 5. Robustness of the exit model")

********************************************************************************
* 7. VALUATION STEP (H3): TWO-ROUND STARTUPS ONLY
********************************************************************************

* delta_v = post-money round 2 / post-money round 1, in logs.
regress log_delta_v c.log_gap heat $X $FE if two_rounds == 1, ///
    vce(cluster sector_year_id)
estimates store val_h1

regress log_delta_v c.log_gap##c.heat $X $FE if two_rounds == 1, ///
    vce(cluster sector_year_id)
estimates store val_h2

* Predicted valuation step by months between rounds, cold vs hot market.
margins, at(log_gap = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Predicted ln(valuation step)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m9_valuation_by_gap.png, replace width(2000)

* Table 6: valuation step, all variables.
esttab val_h1 val_h2 using "RQ1_tables.rtf", append $TAB ///
    mtitles("OLS H3" "OLS H3 x hype") stats(N r2, labels("Observations" "R2")) ///
    title("Table 6. Time between rounds and the valuation step (two-round startups)")

********************************************************************************
* 8. Other numbers and statistics
********************************************************************************

* Interquartile range of ln gap among two-round startups (2.24 to 3.02 = 8 to 19 months).
summarize log_gap if full_window == 1 & two_rounds == 1, detail

* Odds ratios of the main exit and failure models (exp(b), used in the text).
estimates restore exit_h2
logit, or
estimates restore fail_h2
logit, or

* Average marginal effects of ln gap on FAILURE at cold, normal and hot hype (Table 7, row 2).
estimates restore fail_h2
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-1 0 1))
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-1 1)) contrast(atcontrast(r))

* LPM: exit change over the interquartile range of the gap (0.78 units of ln gap).
estimates restore exit_lpm
lincom 0.78 * log_gap_r2

********************************************************************************
* 9. FURTHER ROBUSTNESS: sector x quarter FEs, robust SEs instead of clustered SEs
********************************************************************************

* (d) Hype by sector x quarter instead of sector x year, clustered at that level.
logit exit_5y i.two_rounds##c.heat_quarter c.log_gap_r2##c.heat_quarter $X $FE ///
    if full_window == 1, vce(cluster sector_quarter_id)
estimates store rob_quarter

* (e) Robust instead of clustered standard errors: main model and past-only hype.
logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(robust)
estimates store rob_robust
logit exit_5y i.two_rounds##c.heat_past c.log_gap_r2##c.heat_past $X $FE ///
    if full_window == 1, vce(robust)
estimates store rob_past_robust

* (f) Same sample as the past-hype model, but with the main hype measure.
*     If beta3 is also about -0.05 here, the past-hype result comes from the sample.
logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1 & !missing(heat_past), vce(cluster sector_year_id)
estimates store rob_past_sample

* (g) Drop one-round startups that exited or failed within 13 months of round 1
*     (before they could plausibly have raised again): 367 startups.
generate byte early_out = two_rounds == 0 & (exit_5y == 1 | failure_5y == 1) & months_to_outcome <= 13
tabulate early_out if full_window == 1
logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1 & early_out == 0, vce(cluster sector_year_id)
estimates store rob_noearly

* (h) Variance inflation factors (LPM), with the gap uncentred and centred.
quietly regress exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE if full_window == 1
estat vif
summarize log_gap if full_window == 1 & two_rounds == 1, meanonly
generate log_gap_r2_c = two_rounds * (log_gap - r(mean))
replace log_gap_r2_c = 0 if two_rounds == 0
quietly regress exit_5y i.two_rounds##c.heat c.log_gap_r2_c##c.heat $X $FE if full_window == 1
estat vif

* Table 7: further robustness, all variables.
esttab rob_quarter rob_robust rob_past_robust rob_past_sample rob_noearly using "RQ1_tables.rtf", append $TAB ///
    mtitles("Sector x quarter hype" "Robust SE" "Past hype, robust SE" "Past-hype sample" "No early one-rounders") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 7. Further robustness of the exit model")

********************************************************************************
*******************************************************************************
* 10. EXTRA CONTROLS: TEAM AND LEAD-INVESTOR AGE 
********************************************************************************

* ln_founders, MBA, Has_Core_AI_Term (team), young_lead (lead firm < 6 years old, Gompers 1996)
* and lead_age_miss (lead identified, age missing). team_ok = 1 if founder data is available.
global XTRA "ln_founders MBA Has_Core_AI_Term young_lead lead_age_miss"

label variable ln_founders "ln(number of founders)"
label variable MBA "MBA founder"
label variable Has_Core_AI_Term "AI term in description"
label variable young_lead "Young lead investor (< 6 years)"
label variable lead_age_miss "Lead identified, age missing"

* How many startups have founder data?
tabulate team_ok if full_window == 1

* Exit: main model on the founder-data sample, then with the extra controls (same sample).
logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1 & team_ok == 1, vce(cluster sector_year_id)
estimates store exit_same

logit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $XTRA $FE ///
    if full_window == 1 & team_ok == 1, vce(cluster sector_year_id)
estimates store exit_extra

* Failure: the same two models.
logit failure_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1 & team_ok == 1, vce(cluster sector_year_id)
estimates store fail_same

logit failure_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $XTRA $FE ///
    if full_window == 1 & team_ok == 1, vce(cluster sector_year_id)
estimates store fail_extra

* Table 8: extra controls, all variables.
esttab exit_same exit_extra fail_same fail_extra using "RQ1_tables.rtf", append $TAB ///
    mtitles("Exit: same sample" "Exit: + extra" "Failure: same sample" "Failure: + extra") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 8. Adding team and lead-investor-age controls")

********************************************************************************
* 11. ADDITIONAL FIGURES
********************************************************************************

* Exit, failure and still private within 5 years, by gap quintile.
preserve
keep if full_window == 1
generate byte o_exit = exit_5y == 1
generate byte o_fail = failure_5y == 1 & exit_5y != 1
generate byte o_priv = 1 - o_exit - o_fail
generate byte grp = gap_q
replace grp = 6 if two_rounds == 0
label define grp_lbl 1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest" 6 "One round"
label values grp grp_lbl
tabstat o_exit o_fail o_priv, by(grp) statistics(n mean)
graph bar (mean) o_exit o_fail o_priv, over(grp) stack ///
    bar(1, color(navy)) bar(2, color(cranberry)) bar(3, color(gs11)) ///
    legend(order(1 "Exit" 2 "Failure" 3 "Still private") rows(1)) ///
    ytitle("Share within 5 years of window start") $LOOK
graph export figures/n3_outcomes_by_gap_quintile.png, replace width(2000)
restore

* Binned scatter of exit and failure on ln gap, net of controls and fixed effects, two-round startups, 20 bins.
preserve
keep if full_window == 1 & two_rounds == 1
quietly regress log_gap $X $FE
predict rx if e(sample), residuals
summarize log_gap if e(sample), meanonly
replace rx = rx + r(mean)
foreach y in exit_5y failure_5y {
    quietly regress `y' $X $FE
    predict r_`y' if e(sample), residuals
    summarize `y' if e(sample), meanonly
    replace r_`y' = r_`y' + r(mean)
    regress r_`y' rx
}
xtile bin = rx, nq(20)
collapse (mean) rx r_exit_5y r_failure_5y, by(bin)
twoway (scatter r_exit_5y rx, mcolor(navy)) (lfit r_exit_5y rx, lcolor(navy)), ///
    title("Exit within 5 years") ytitle("Share, net of controls and FE") ///
    xtitle("ln(1 + months), net of controls and FE") legend(off) name(n4a, replace) nodraw $LOOK
twoway (scatter r_failure_5y rx, mcolor(cranberry)) (lfit r_failure_5y rx, lcolor(cranberry)), ///
    title("Failure within 5 years") ytitle("Share, net of controls and FE") ///
    xtitle("ln(1 + months), net of controls and FE") legend(off) name(n4b, replace) nodraw $LOOK
graph combine n4a n4b, cols(2) graphregion(color(white))
graph export figures/n4_binscatter_exit_failure.png, replace width(2000)
restore

* Valuation step: total and per year, by gap quintile
preserve
keep if two_rounds == 1 & delta_v > 0 & !missing(delta_v) & gap_months >= 1
generate step_py = log_delta_v / (gap_months / 12)
xtile vq = gap_months, nq(5)
label values vq gap_lbl
tabstat gap_months log_delta_v step_py, by(vq) statistics(n mean p25 p50 p75)
graph bar (mean) log_delta_v, over(vq) bar(1, color(navy)) ///
    ytitle("Mean ln(V2 / V1)") title("Total step") name(n2a, replace) nodraw $LOOK
graph bar (median) step_py, over(vq) bar(1, color(cranberry)) ///
    ytitle("Median log points per year") title("Step per year") name(n2b, replace) nodraw $LOOK
graph combine n2a n2b, cols(2) graphregion(color(white))
graph export figures/n2_step_total_vs_per_year.png, replace width(2000)
restore


********************************************************************************
* 12. HYPE AS THE RAW VC SHARE (TA's suggestion)
********************************************************************************

* Main H2 models with vc_share instead of heat, for 4, 5, 6 years and no window.
* w = 0 means no window (all startups, outcome by the end of the data).
foreach w in 4 5 6 0 {
    if `w' == 5      local cnd "full_window == 1"
    else if `w' == 0 local cnd "!missing(two_rounds)"
    else             local cnd "full_window_`w'y == 1"
    local ex = cond(`w' == 0, "exit", "exit_`w'y")
    local fa = cond(`w' == 0, "failure_ever", "failure_`w'y")

    logit `ex' i.two_rounds##c.vc_share c.log_gap_r2##c.vc_share $X $FE ///
        if `cnd', vce(cluster sector_year_id)
    estimates store vcs_exit_`w'

    logit `fa' i.two_rounds##c.vc_share c.log_gap_r2##c.vc_share $X $FE ///
        if `cnd', vce(cluster sector_year_id)
    estimates store vcs_fail_`w'
}

* Hot minus cold effect of the gap (mean +/- 1 SD of vc_share), 5-year exit.
summarize vc_share if full_window == 1
local lo = r(mean) - r(sd)
local hi = r(mean) + r(sd)
estimates restore vcs_exit_5
margins if two_rounds == 1, dydx(log_gap_r2) at(vc_share = (`lo' `hi')) contrast(atcontrast(r))

* Check: VC share minus the sector mean (only the movement within each sector), 5 years.
logit exit_5y i.two_rounds##c.vc_share_dm c.log_gap_r2##c.vc_share_dm $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store vcs_exit_dm

* Table 9: hype as the raw VC share.
esttab exit_h2 vcs_exit_4 vcs_exit_5 vcs_exit_6 vcs_exit_0 vcs_exit_dm using "RQ1_tables.rtf", append $TAB ///
    mtitles("Exit 5y, z-score" "Exit 4y" "Exit 5y" "Exit 6y" "Exit, no window" "Exit 5y, share - mean") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 9. Exit with hype as the raw VC share")
esttab fail_h2 vcs_fail_4 vcs_fail_5 vcs_fail_6 vcs_fail_0 using "RQ1_tables.rtf", append $TAB ///
    mtitles("Failure 5y, z-score" "Failure 4y" "Failure 5y" "Failure 6y" "Failure, no window") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 10. Failure with hype as the raw VC share")

********************************************************************************
* 13. NON-LINEAR GAP: ln(gap) + ln(gap)^2 AND months + months^2
********************************************************************************
global LOG "i.two_rounds##c.vc_share c.log_gap_r2##c.vc_share c.log_gap_r2#c.log_gap_r2 $X $FE"
global MO  "i.two_rounds##c.vc_share c.gap_r2##c.vc_share c.gap_r2#c.gap_r2 $X $FE"

* (a) Exit
logit exit_4y $LOG if full_window_4y == 1, vce(cluster sector_year_id)
estimates store sq_exit_log_4
logit exit_5y $LOG if full_window == 1, vce(cluster sector_year_id)
estimates store sq_exit_log_5
logit exit_6y $LOG if full_window_6y == 1, vce(cluster sector_year_id)
estimates store sq_exit_log_6
logit exit $LOG, vce(cluster sector_year_id)
estimates store sq_exit_log_0

logit exit_4y $MO if full_window_4y == 1, vce(cluster sector_year_id)
estimates store sq_exit_mo_4
logit exit_5y $MO if full_window == 1, vce(cluster sector_year_id)
estimates store sq_exit_mo_5
logit exit_6y $MO if full_window_6y == 1, vce(cluster sector_year_id)
estimates store sq_exit_mo_6
logit exit $MO, vce(cluster sector_year_id)
estimates store sq_exit_mo_0

* (b) Failure
logit failure_4y $LOG if full_window_4y == 1, vce(cluster sector_year_id)
estimates store sq_fail_log_4
logit failure_5y $LOG if full_window == 1, vce(cluster sector_year_id)
estimates store sq_fail_log_5
logit failure_6y $LOG if full_window_6y == 1, vce(cluster sector_year_id)
estimates store sq_fail_log_6
logit failure_ever $LOG, vce(cluster sector_year_id)
estimates store sq_fail_log_0

logit failure_4y $MO if full_window_4y == 1, vce(cluster sector_year_id)
estimates store sq_fail_mo_4
logit failure_5y $MO if full_window == 1, vce(cluster sector_year_id)
estimates store sq_fail_mo_5
logit failure_6y $MO if full_window_6y == 1, vce(cluster sector_year_id)
estimates store sq_fail_mo_6
logit failure_ever $MO, vce(cluster sector_year_id)
estimates store sq_fail_mo_0

* Is the gap needed at all (linear + squared jointly)? Main 5-year models.
estimates restore sq_exit_log_5
testparm c.log_gap_r2 c.log_gap_r2#c.log_gap_r2
estimates restore sq_exit_mo_5
testparm c.gap_r2 c.gap_r2#c.gap_r2
estimates restore sq_fail_log_5
testparm c.log_gap_r2 c.log_gap_r2#c.log_gap_r2
estimates restore sq_fail_mo_5
testparm c.gap_r2 c.gap_r2#c.gap_r2

* Graphs: predicted probability for two-round startups along the gap.
* (a) ln(gap) + ln(gap)^2, no window (all startups, outcome by the end of the data) (axis ticks in months)
estimates restore sq_exit_log_0
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4))
marginsplot, recast(line) recastci(rarea) title("Exit (no window)") ///
    plotopts(lcolor(navy)) ciopts(color(navy%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds") ytitle("Predicted probability") name(g1, replace) nodraw $LOOK

estimates restore sq_fail_log_0
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4))
marginsplot, recast(line) recastci(rarea) title("Failure (no window)") ///
    plotopts(lcolor(cranberry)) ciopts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds") ytitle("Predicted probability") name(g2, replace) nodraw $LOOK

graph combine g1 g2, cols(2) graphregion(color(white))
graph export figures/q1_nonlinear_ln_gap.png, replace width(2400)

* (b) months + months^2, no window (all startups, outcome by the end of the data)
estimates restore sq_exit_mo_0
margins if two_rounds == 1, at(gap_r2 = (0(3)48))
marginsplot, recast(line) recastci(rarea) title("Exit (no window)") ///
    plotopts(lcolor(navy)) ciopts(color(navy%20) lwidth(none)) ///
    xtitle("Months between rounds") ytitle("Predicted probability") name(g3, replace) nodraw $LOOK

estimates restore sq_fail_mo_0
margins if two_rounds == 1, at(gap_r2 = (0(3)48))
marginsplot, recast(line) recastci(rarea) title("Failure (no window)") ///
    plotopts(lcolor(cranberry)) ciopts(color(cranberry%20) lwidth(none)) ///
    xtitle("Months between rounds") ytitle("Predicted probability") name(g4, replace) nodraw $LOOK

graph combine g3 g4, cols(2) graphregion(color(white))
graph export figures/q2_nonlinear_months.png, replace width(2400)

* Note: with no window, a longer gap leaves less time after round 2 to exit or fail,
* so part of the gap effect there is time at risk, not speed.

* Tables 11-12: non-linear gap.
esttab sq_exit_log_4 sq_exit_log_5 sq_exit_log_6 sq_exit_log_0 sq_exit_mo_4 sq_exit_mo_5 sq_exit_mo_6 sq_exit_mo_0 ///
    using "RQ1_tables.rtf", append $TAB ///
    mtitles("ln 4y" "ln 5y" "ln 6y" "ln no window" "months 4y" "months 5y" "months 6y" "months no window") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 11. Exit with a squared gap: ln(gap) + ln(gap)^2 and months + months^2")
esttab sq_fail_log_4 sq_fail_log_5 sq_fail_log_6 sq_fail_log_0 sq_fail_mo_4 sq_fail_mo_5 sq_fail_mo_6 sq_fail_mo_0 ///
    using "RQ1_tables.rtf", append $TAB ///
    mtitles("ln 4y" "ln 5y" "ln 6y" "ln no window" "months 4y" "months 5y" "months 6y" "months no window") ///
    stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 12. Failure with a squared gap: ln(gap) + ln(gap)^2 and months + months^2")


********************************************************************************
* 14. CORRELATION HEATMAP OF THE MAIN REGRESSORS AND CONTROLS
********************************************************************************
generate vc_lead = lead_type == "Venture Capital"
label variable vc_lead "VC lead"
capture which heatplot
if _rc != 0 {
    capture ssc install heatplot, replace
    capture ssc install palettes, replace
    capture ssc install colrspace, replace
}
correlate two_rounds log_gap_r2 gap_r2 heat vc_share log_round1_size round1_number ///
    startup_age_at_round1 vc_lead if full_window == 1
matrix C = r(C)
matrix rownames C = R R_x_ln_gap R_x_gap_months hype_z hype_vc_share ln_size_r1 deal_no_r1 age_r1 vc_lead
matrix colnames C = R R_x_ln_gap R_x_gap_months hype_z hype_vc_share ln_size_r1 deal_no_r1 age_r1 vc_lead
matrix list C, format(%5.2f)

heatplot C, values(format(%4.2f) size(vsmall)) color(hcl diverging, intensity(.8)) ///
    cuts(-1(0.1)1) lower nodiagonal aspectratio(1) legend(off) ///
    xlabel(, angle(45) labsize(small)) ylabel(, labsize(small)) graphregion(color(white))
graph export figures/c1_correlation_heatmap.png, replace width(2000)


********************************************************************************
* 15. LAGGED HYPE ROBUSTNESS: SECTOR HYPE IN YEAR t - 1
********************************************************************************

* Build 1-year lagged sector hype (t - 1) on a unique sector x year panel
* so L. never bleeds across sectors or bridges skipped calendar years.
preserve
keep if !missing(sector_id) & !missing(round1_year)
collapse (firstnm) heat vc_share vc_share_dm, by(sector_id round1_year)
xtset sector_id round1_year

generate heat_l1        = L.heat
generate vc_share_l1    = L.vc_share
generate vc_share_dm_l1 = L.vc_share_dm

keep sector_id round1_year heat_l1 vc_share_l1 vc_share_dm_l1
tempfile hype_lags
save `hype_lags', replace
restore

merge m:1 sector_id round1_year using `hype_lags', keep(master match) nogen

label variable heat_l1        "Hype at round 1, lagged 1 year (t-1)"
label variable vc_share_l1    "Hype: sector % of VC $, lagged 1 year (t-1)"
label variable vc_share_dm_l1 "Hype: VC share minus sector mean, lagged 1 year (t-1)"

* (a) Exit within 5 years with 1-year lagged z-score hype (H1, H2, and LPM)
logit exit_5y i.two_rounds c.log_gap_r2 c.heat_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_exit_h1

logit exit_5y i.two_rounds##c.heat_l1 c.log_gap_r2##c.heat_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_exit_h2

regress exit_5y i.two_rounds##c.heat_l1 c.log_gap_r2##c.heat_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_exit_lpm

* (b) Exit within 5 years with 1-year lagged raw VC share (and demeaned share)
logit exit_5y i.two_rounds##c.vc_share_l1 c.log_gap_r2##c.vc_share_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_vcs_exit

logit exit_5y i.two_rounds##c.vc_share_dm_l1 c.log_gap_r2##c.vc_share_dm_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_vcs_exit_dm

* (c) Failure within 5 years with 1-year lagged hype (z-score and raw VC share)
logit failure_5y i.two_rounds##c.heat_l1 c.log_gap_r2##c.heat_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_fail_h2

logit failure_5y i.two_rounds##c.vc_share_l1 c.log_gap_r2##c.vc_share_l1 $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store lag_vcs_fail

* Marginal effect of ln(gap) across cold (-1 SD), normal (0), and hot (+1 SD) lagged hype
estimates restore lag_exit_h2
margins if two_rounds == 1, dydx(log_gap_r2) at(heat_l1 = (-1 0 1))
margins if two_rounds == 1, dydx(log_gap_r2) at(heat_l1 = (-1 1)) contrast(atcontrast(r))

margins if two_rounds == 1, dydx(log_gap_r2) at(heat_l1 = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plotopts(lcolor(navy) lwidth(medthick)) ciopts(color(navy%20) lwidth(none)) ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    ytitle("Effect of ln(gap) on Pr(exit)") xtitle("Lagged market hype at t-1 (SD)") $LOOK
graph export figures/m10_exit_effect_by_hype_l1.png, replace width(2000)

* (d) Valuation step (H3, two-round startups only) with 1-year lagged hype
regress log_delta_v c.log_gap##c.heat_l1 $X $FE if two_rounds == 1, ///
    vce(cluster sector_year_id)
estimates store lag_val_h2

regress log_delta_v c.log_gap##c.vc_share_l1 $X $FE if two_rounds == 1, ///
    vce(cluster sector_year_id)
estimates store lag_val_vcs

* Table 13: 5-year exit and failure with 1-year lagged sector hype
esttab lag_exit_h1 lag_exit_h2 lag_exit_lpm lag_vcs_exit lag_vcs_exit_dm lag_fail_h2 lag_vcs_fail ///
    using "RQ1_tables.rtf", append $TAB ///
    mtitles("Exit H1 (t-1)" "Exit H2 (t-1)" "Exit LPM (t-1)" "Exit share (t-1)" ///
            "Exit dm share (t-1)" "Failure H2 (t-1)" "Failure share (t-1)") ///
    stats(N r2_p r2, labels("Observations" "Pseudo R2" "R2")) ///
    title("Table 13. Exit and failure within 5 years with 1-year lagged sector hype")

* Table 14: Valuation step with 1-year lagged sector hype
esttab lag_val_h2 lag_val_vcs using "RQ1_tables.rtf", append $TAB ///
    mtitles("OLS H3 z-score (t-1)" "OLS H3 share (t-1)") ///
    stats(N r2, labels("Observations" "R2")) ///
    title("Table 14. Valuation step with 1-year lagged sector hype (two-round startups)")

log close