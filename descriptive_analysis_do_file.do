
clear all
set more off
capture log close
log using core_descriptives.log, replace text
use "C:\Users\owend\Desktop\1st_sem\Stata_data_analysis\dataset_final.dta", clear


* 0. PREPARATION
*****************************************************************************************************
* lead investor type as a numeric factor, as in the main model
encode lead_type, gen(lead_cat)
* two startups have a negative age at round 1 (round dated before founding): data errors, set to missing as in the do-file
replace startup_age_at_round1 = . if startup_age_at_round1 < 0
* estimation sample = the startups the main logit actually uses; the logit is run quietly only to mark them (no output is shown)
quietly logit exit_3y c.log_gap##c.heat log_round1_size round1_number startup_age_at_round1 i.lead_cat i.round2_yq i.sector_id i.state_id if full_3y_window == 1, vce(cluster sector_year_id)
gen byte est = e(sample)
label variable est "Estimation sample of the main logit"
* gap in quintiles (1 = fastest) and heat in terciles (1 = coldest), both cut on the estimation sample
xtile gap_q = gap_months if est, nq(5)
xtile heat_t = heat if est, nq(3)
label define gap_q 1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest"
label values gap_q gap_q
label define heat_t 1 "Cold" 2 "Middle" 3 "Hot"
label values heat_t heat_t
* exit, failure and 3rd round in percent, so that means read as rates
gen exit_pct = 100 * exit_3y
gen fail_pct = 100 * failure_3y
gen r3_pct = 100 * round3_within_3y


* 1. SAMPLE
*****************************************************************************************************
* all startups with two VC rounds and a valid gap, those with the full 3-year window, and those in the logit
count
count if full_3y_window == 1
count if est
* startups lost between the window sample and the logit (missing covariates or fixed-effect cells with no exit)
count if full_3y_window == 1 & !est
* do the dropped startups differ? compare the outcome, the gap and heat for kept (est = 1) and dropped (est = 0) startups
tabstat exit_pct gap_months heat if full_3y_window == 1, by(est) statistics(n mean sd) format(%9.2f) nototal


* 2. SUMMARY STATISTICS OF THE MAIN VARIABLES (Table 1)
*****************************************************************************************************
* outcome, treatment, moderator and round-1 controls on the estimation sample
tabstat exit_3y gap_months log_gap heat log_round1_size round1_number startup_age_at_round1 if est, statistics(n mean sd p25 p50 p75 min max) columns(statistics) format(%9.3f)
* other outcomes in the same sample (robustness outcomes)
tabstat exit_3y failure_3y round3_within_3y if est, statistics(n mean sd) columns(statistics) format(%9.3f)
* lead investor type of round 1 (base category of i.lead_cat = Venture Capital)
tabulate lead_type if est, sort


* 3. EXIT RATE BY FUNDRAISING SPEED
*****************************************************************************************************
* gap range and exit rate in each gap quintile: the raw version of beta1
tabstat gap_months exit_pct if est, by(gap_q) statistics(n mean min max) format(%9.2f)


* 4. SECTOR HEAT
*****************************************************************************************************
* how much heat varies: number of sector-years (the clusters) and heat by sector
egen sy_tag = tag(sector_year_id) if est
count if sy_tag == 1
tabstat heat if sy_tag == 1, by(sector) statistics(n mean sd min max) format(%9.2f)
* exit rate and gap by heat tercile: are hot sector-years different in speed or in exits?
tabstat heat gap_months exit_pct if est, by(heat_t) statistics(n mean sd) format(%9.2f)
* exit rate (%) by gap quintile and heat tercile: the raw version of the interaction beta3
tabulate gap_q heat_t if est, summarize(exit_pct) means freq


* 5. TIME AND SECTOR
*****************************************************************************************************
* startups, exit rate and mean heat by year of round 2 (the time fixed effects absorb this level)
tabulate round2_year if est, summarize(exit_pct) means freq
tabstat heat gap_months if est, by(round2_year) statistics(mean) format(%9.2f)
* exit rate by sector (the sector fixed effects absorb this level)
tabulate sector if est, summarize(exit_pct) means freq


* 6. CORRELATIONS
*****************************************************************************************************
* main variables: a high correlation between the regressors would show up here before the VIFs
pwcorr exit_3y log_gap heat log_round1_size round1_number startup_age_at_round1 if est, star(0.05)
* the hype measures with each other: how close the robustness versions are to the main heat
pwcorr heat heat_past heat_quarter entry_z_l1 hype_index_l sector_vc_share if est, star(0.05) obs


* 7. FIGURES
*****************************************************************************************************
* (a) distribution of the gap in the estimation sample, in 3-month bins
histogram gap_months if est, width(3) start(0) percent fcolor(gs13) lcolor(black) lwidth(vthin) ///
    xtitle("Months between the 1st and 2nd VC round") ytitle("Percent of startups") ///
    ylabel(, angle(0) nogrid) graphregion(color(white)) plotregion(color(white))
graph export fig_gap_hist.png, replace width(2400)

* (b) exit rate by gap quintile for cold and hot sector-years (bottom and top heat tercile); solid circles = cold, dashed triangles = hot
preserve
keep if est & inlist(heat_t, 1, 3)
collapse (mean) exit_pct (count) n = exit_3y, by(gap_q heat_t)
twoway (connected exit_pct gap_q if heat_t == 1, lcolor(black) mcolor(black) msymbol(O) lpattern(solid)) ///
       (connected exit_pct gap_q if heat_t == 3, lcolor(gs7) mcolor(gs7) msymbol(T) lpattern(dash)), ///
       xlabel(1 "Q1 fastest" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 slowest") xtitle("Gap quintile") ytitle("Exit within 3 years (%)") ///
       ylabel(, angle(0) nogrid) legend(order(1 "Cold sector-years (bottom heat tercile)" 2 "Hot sector-years (top heat tercile)") rows(2) region(lcolor(none))) ///
       graphregion(color(white)) plotregion(color(white))
graph export fig_exit_gap_heat.png, replace width(2400)
restore

* (c) exit rate against log gap in 20 equal-sized bins (binned scatter): the shape of the raw gap-exit relationship
preserve
keep if est
xtile bin = log_gap, nq(20)
collapse (mean) exit_pct log_gap, by(bin)
twoway scatter exit_pct log_gap, mcolor(black) msymbol(O) msize(medsmall) ///
    xtitle("log gap = ln(1 + months between rounds 1 and 2)") ytitle("Exit within 3 years (%)") ///
    ylabel(, angle(0) nogrid) graphregion(color(white)) plotregion(color(white))
graph export fig_exit_loggap_bins.png, replace width(2400)
restore

* (d) gap by heat tercile (box plot, outside values hidden): do startups raise faster in hot sector-years?
graph box gap_months if est, over(heat_t) noout box(1, fcolor(gs13) lcolor(black)) medline(lcolor(black)) ///
    ytitle("Months between the 1st and 2nd VC round") ylabel(, angle(0) nogrid) graphregion(color(white)) plotregion(color(white))
graph export fig_gap_by_heat.png, replace width(2400)

* (e) heat over time in each sector (one value per sector-year, all startups): where the moderator's variation comes from
preserve
keep if !missing(heat, sector_id)
collapse (mean) heat, by(sector round2_year)
twoway line heat round2_year, lcolor(black) lwidth(medthin) yline(0, lcolor(gs10) lpattern(dash)) ///
    by(sector, note("") cols(4) graphregion(color(white))) subtitle(, size(small) fcolor(white) lcolor(none)) ///
    xlabel(2012(2)2022, labsize(small)) ylabel(, angle(0) nogrid labsize(small)) xtitle("Year of round 2") ytitle("Heat (z within sector)")
graph export fig_heat_by_sector.png, replace width(2400)
restore

* (f) exit rate by year of round 2 in the estimation sample (the year-quarter fixed effects absorb this pattern)
preserve
keep if est
collapse (mean) exit_pct, by(round2_year)
twoway bar exit_pct round2_year, barwidth(0.7) fcolor(gs12) lcolor(black) lwidth(vthin) ///
    xlabel(2012(1)2019) xtitle("Year of round 2") ytitle("Exit within 3 years (%)") ylabel(, angle(0) nogrid) ///
    graphregion(color(white)) plotregion(color(white))
graph export fig_exit_by_year.png, replace width(2400)
restore

* (g) exit rate by sector in the estimation sample (the sector fixed effects absorb this pattern)
graph hbar (mean) exit_pct if est, over(sector, sort(1) descending label(labsize(small))) bar(1, fcolor(gs12) lcolor(black) lwidth(vthin)) ///
    ytitle("Exit within 3 years (%)") ylabel(, nogrid) graphregion(color(white)) plotregion(color(white))
graph export fig_exit_by_sector.png, replace width(2400)

* (h) cumulative share exited since round 2 for fast and slow raisers (Kaplan-Meier, all startups with round 2 by DATA_END, no fixed window)
* failure is treated as censoring, so 1 - S(t) is the exit curve if failed startups could still have exited; read it as descriptive
preserve
keep if !missing(months_to_outcome) & months_to_outcome > 0
summarize gap_months, detail
gen byte slow = gap_months > r(p50)
stset months_to_outcome, failure(outcome_is_exit == 1)
sts graph, failure by(slow) tmax(84) plot1opts(lcolor(black) lpattern(solid)) plot2opts(lcolor(gs7) lpattern(dash)) ///
    xlabel(0(12)84) xtitle("Months since round 2") ytitle("Share exited") title("") ///
    legend(order(1 "Fast raisers (gap below median)" 2 "Slow raisers (gap above median)") rows(2) region(lcolor(none))) ///
    ylabel(, angle(0) nogrid) graphregion(color(white)) plotregion(color(white))
graph export fig_km_exit_fast_slow.png, replace width(2400)
restore

log close

