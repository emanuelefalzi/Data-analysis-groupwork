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

* Lead investor type as a categorical for i. (base = "No lead identified").
label define lead_lbl 0 "No lead identified"
encode lead_type, generate(lead_cat) label(lead_lbl)

* Two startups have a negative age at round 1 (data errors).
replace startup_age_at_round1 = . if startup_age_at_round1 < 0

* Valuation step in logs (long right tail).
generate log_delta_v = ln(delta_v)

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

* Common options for the Word tables: all variables, fixed effects as Yes rows.
global TAB `"label b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) nobaselevels interaction(" x ") indicate("Year-quarter FE = *.round1_yq" "Sector FE = *.sector_id" "State FE = *.state_id") addnotes("Standard errors clustered by sector x year of round 1 in parentheses.")"'

********************************************************************************
* 2. DESCRIPTIVE STATISTICS
********************************************************************************

* Main sample: startups whose 5-year window is fully observed.
count if full_window == 1
tabulate two_rounds if full_window == 1

* Table 1 (Word): means and SDs by group.
estpost tabstat exit_5y failure_5y gap_months log_round1_size round1_number ///
    startup_age_at_round1 heat if full_window == 1, ///
    by(two_rounds) statistics(mean sd) columns(statistics)
esttab using "RQ1_tables.rtf", replace cells("mean(fmt(3)) sd(fmt(3))") ///
    unstack noobs nonumber label title("Table 1. Descriptive statistics by group")

* Do the groups differ? (difference in means)
ttest exit_5y if full_window == 1, by(two_rounds)
ttest failure_5y if full_window == 1, by(two_rounds)

* D1. Distribution of the gap between rounds.
histogram gap_months if full_window == 1, width(3) frequency ///
    color(navy%70) lcolor(white) ///
    xtitle("Months between rounds 1 and 2") ytitle("Startups") $LOOK
graph export figures/d1_gap_histogram.png, replace width(2000)

* D2. Startups per round-1 year, by group.
graph bar (count) exit, over(two_rounds) over(round1_year, label(angle(45))) ///
    asyvars stack bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Startups") legend(rows(1)) $LOOK
graph export figures/d2_startups_by_year.png, replace width(2000)

* D3. Hype over time in each sector (the variation H2 uses).
preserve
collapse (mean) heat, by(sector round1_year)
twoway connected heat round1_year, by(sector, note("") graphregion(color(white))) ///
    lcolor(navy) mcolor(navy) msize(small) yline(0, lcolor(gs10) lpattern(dash)) ///
    ytitle("Hype (z-score)") xtitle("Year of round 1") ylabel(, angle(0) glcolor(gs15))
graph export figures/d3_hype_by_sector.png, replace width(2000)
restore

* D4. Exit and failure rates by sector.
graph hbar (mean) exit_5y failure_5y if full_window == 1, ///
    over(sector, sort(1) descending label(labsize(small))) ///
    bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Share of startups") legend(order(1 "Exit within 5 years" 2 "Failure within 5 years") rows(1)) $LOOK
graph export figures/d4_outcomes_by_sector.png, replace width(2000)

* D5. Exit rate by group in cold, middle and hot markets.
graph bar (mean) exit_5y if full_window == 1, over(two_rounds) over(heat_t) ///
    asyvars bar(1, color(navy)) bar(2, color(cranberry)) blabel(bar, format(%4.2f)) ///
    ytitle("Share exiting within 5 years") legend(rows(1)) $LOOK
graph export figures/d5_exit_by_group_hype.png, replace width(2000)

* D6. Raw exit rate by gap quintile, cold vs hot markets (two-round startups, no controls).
graph bar (mean) exit_5y if full_window == 1 & two_rounds == 1 & heat_t != 2, ///
    over(heat_t) over(gap_q) asyvars bar(1, color(navy)) bar(2, color(cranberry)) ///
    ytitle("Share exiting within 5 years") b1title("Quintile of months between rounds") ///
    legend(order(1 "Cold market" 2 "Hot market") rows(1)) $LOOK
graph export figures/d6_exit_by_gap_quintile.png, replace width(2000)

* D7. Size of round 1 by group.
twoway (kdensity log_round1_size if full_window == 1 & two_rounds == 0, lcolor(navy) lwidth(medthick)) ///
       (kdensity log_round1_size if full_window == 1 & two_rounds == 1, lcolor(cranberry) lwidth(medthick)), ///
    xtitle("ln(1 + round-1 amount, USD M)") ytitle("Density") ///
    legend(order(1 "One round" 2 "Two or more rounds") rows(1)) $LOOK
graph export figures/d7_round1_size.png, replace width(2000)

* D8. Exit rate by lead investor type (types with at least 100 startups).
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

* M1. Effect of the gap along hype. H2 holds if the line is not flat.
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plotopts(lcolor(navy) lwidth(medthick)) ciopts(color(navy%20) lwidth(none)) ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    ytitle("Effect of ln(gap) on Pr(exit)") xtitle("Market hype at round 1 (SD)") $LOOK
graph export figures/m1_exit_effect_by_hype.png, replace width(2000)

* M2. Predicted exit by months between rounds, cold vs hot market (ticks in months).
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Pr(exit within 5 years)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m2_exit_by_gap.png, replace width(2000)

* M3. Predicted exit for one round vs two rounds along hype.
margins two_rounds, at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xtitle("Market hype at round 1 (SD)") ytitle("Pr(exit within 5 years)") ///
    legend(order(3 "One round" 4 "Two or more rounds") rows(1)) $LOOK
graph export figures/m3_exit_by_group.png, replace width(2000)

* M4. All coefficients of the main model (fixed effects not shown), with 95% CIs.
coefplot exit_h2, drop(_cons *.round1_yq *.sector_id *.state_id) xline(0, lcolor(gs8) lpattern(dash)) ///
    mcolor(navy) ciopts(lcolor(navy)) label ///
    xtitle("Logit coefficient") ylabel(, labsize(small)) $LOOK
graph export figures/m4_exit_coefficients.png, replace width(2000)

* Same model as a linear probability model: beta3 in probability units.
regress exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store exit_lpm

* Table 2 (Word): exit models, all variables.
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

* M5. Effect of the gap on failure along hype.
margins if two_rounds == 1, dydx(log_gap_r2) at(heat = (-2(0.25)2))
marginsplot, recast(line) recastci(rarea) title("") ///
    plotopts(lcolor(cranberry) lwidth(medthick)) ciopts(color(cranberry%20) lwidth(none)) ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    ytitle("Effect of ln(gap) on Pr(failure)") xtitle("Market hype at round 1 (SD)") $LOOK
graph export figures/m5_failure_effect_by_hype.png, replace width(2000)

* M6. Predicted failure by months between rounds, cold vs hot market.
margins if two_rounds == 1, at(log_gap_r2 = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Pr(failure within 5 years)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m6_failure_by_gap.png, replace width(2000)

* Table 3 (Word): failure models, all variables.
esttab fail_h1 fail_h2 using "RQ1_tables.rtf", append $TAB ///
    mtitles("Logit H1" "Logit H2") stats(N r2_p, labels("Observations" "Pseudo R2")) ///
    title("Table 3. Time between rounds, hype and failure within 5 years")

********************************************************************************
* 5. SENSITIVITY: 4- AND 6-YEAR WINDOWS
********************************************************************************

* If beta3 changes a lot between 4, 5 and 6 years, 5 years is not a safe cut.
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

* M7. Gap and gap x hype coefficients for 4, 5 and 6 years.
coefplot (exit_4y, label("4 years") mcolor(navy%50) ciopts(lcolor(navy%50))) ///
         (exit_h2, label("5 years") mcolor(navy) ciopts(lcolor(navy))) ///
         (exit_6y, label("6 years") mcolor(cranberry) ciopts(lcolor(cranberry))), ///
    keep(log_gap_r2 c.log_gap_r2#c.heat) xline(0, lcolor(gs8) lpattern(dash)) ///
    coeflabels(log_gap_r2 = "Gap (beta1)" c.log_gap_r2#c.heat = "Gap x hype (beta3)") ///
    xtitle("Logit coefficient, exit") legend(rows(1)) $LOOK
graph export figures/m7_windows_exit.png, replace width(2000)

* M8. The same for failure.
coefplot (fail_4y, label("4 years") mcolor(navy%50) ciopts(lcolor(navy%50))) ///
         (fail_h2, label("5 years") mcolor(navy) ciopts(lcolor(navy))) ///
         (fail_6y, label("6 years") mcolor(cranberry) ciopts(lcolor(cranberry))), ///
    keep(log_gap_r2 c.log_gap_r2#c.heat) xline(0, lcolor(gs8) lpattern(dash)) ///
    coeflabels(log_gap_r2 = "Gap (beta1)" c.log_gap_r2#c.heat = "Gap x hype (beta3)") ///
    xtitle("Logit coefficient, failure") legend(rows(1)) $LOOK
graph export figures/m8_windows_failure.png, replace width(2000)

* Table 4 (Word): window sensitivity, all variables.
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

* (b) Hype measured with past years only (no look-ahead).
logit exit_5y i.two_rounds##c.heat_past c.log_gap_r2##c.heat_past $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store rob_past

* (c) Probit instead of logit.
probit exit_5y i.two_rounds##c.heat c.log_gap_r2##c.heat $X $FE ///
    if full_window == 1, vce(cluster sector_year_id)
estimates store rob_probit

* Table 5 (Word): robustness, all variables.
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

* M9. Predicted valuation step by months between rounds, cold vs hot market.
margins, at(log_gap = (1(0.25)4) heat = (-1 1))
marginsplot, recast(line) recastci(rarea) title("") ///
    plot1opts(lcolor(navy) lwidth(medthick)) ci1opts(color(navy%20) lwidth(none)) ///
    plot2opts(lcolor(cranberry) lwidth(medthick)) ci2opts(color(cranberry%20) lwidth(none)) ///
    xlabel(1.39 "3" 1.95 "6" 2.56 "12" 3.22 "24" 3.61 "36" 3.89 "48") ///
    xtitle("Months between rounds 1 and 2") ytitle("Predicted ln(valuation step)") ///
    legend(order(3 "Cold market (-1 SD)" 4 "Hot market (+1 SD)") rows(1)) $LOOK
graph export figures/m9_valuation_by_gap.png, replace width(2000)

* Table 6 (Word): valuation step, all variables.
esttab val_h1 val_h2 using "RQ1_tables.rtf", append $TAB ///
    mtitles("OLS H3" "OLS H3 x hype") stats(N r2, labels("Observations" "R2")) ///
    title("Table 6. Time between rounds and the valuation step (two-round startups)")

* These models describe associations. They do not establish causality.

log close

