* =====================================================================
* rq1_addon_extra_controls.do  (add-on, does not change any existing file)
* Robustness: adds team and lead-investor-age controls to the H2 logits.
* Run after opening group_21_dataset.dta, with pitchbook_course.dta in
* the working directory. Same specification as exit_h2 / fail_h2.
* =====================================================================
version 17
set more off

capture confirm variable lead_cat
if _rc encode lead_type, gen(lead_cat)

* --- team variables from the course file (all fixed before round 1)
preserve
use CompanyID NFounders MBA Has_Core_AI_Term using "pitchbook_course.dta", clear
rename CompanyID company_id
tempfile team
save `team'
restore
capture drop _merge_team
merge m:1 company_id using `team', keep(master match) gen(_merge_team)
gen ln_founders = ln(NFounders)

* --- lead investor age (Gompers 1996: young VC firms grandstand)
gen byte has_lead      = lead_type != "No lead identified"
gen byte young_lead    = has_lead & lead_investor_age < 6 & !missing(lead_investor_age)
gen byte lead_age_miss = has_lead & missing(lead_investor_age)

local base log_round1_size round1_number startup_age_at_round1 i.lead_cat i.round1_yq i.sector_id i.state_id
local extra ln_founders MBA Has_Core_AI_Term young_lead lead_age_miss

* same sample for both columns: startups with founder data
gen byte team_ok = !missing(ln_founders, MBA)

foreach y in exit_5y failure_5y {
    logit `y' i.two_rounds##c.heat c.log_gap_r2##c.heat `base' ///
        if full_window == 1 & team_ok, vce(cluster sector_year_id)
    estimates store `y'_same
    logit `y' i.two_rounds##c.heat c.log_gap_r2##c.heat `base' `extra' ///
        if full_window == 1 & team_ok, vce(cluster sector_year_id)
    estimates store `y'_extra
}
estimates table exit_5y_same exit_5y_extra failure_5y_same failure_5y_extra, ///
    keep(log_gap_r2 c.log_gap_r2#c.heat `extra') b(%9.3f) se(%9.3f) p(%9.3f) stats(N)
