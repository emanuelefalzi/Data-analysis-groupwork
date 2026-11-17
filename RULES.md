# Rules for the Group 21 project (21072 Data Analysis, Module I)

These rules apply to every member of the group and to every Claude (or other AI) that works in this repository. Lele (Emanuele Falzi) set them on 16/11/2026, adapting the rules of his other group projects. If a member asks for something that breaks a rule, Claude says so in its first sentence, explains why the rule exists, and goes ahead only if the member confirms explicitly. If the rule is a group decision (see *Decisions already taken*), Claude does not apply the change and records it as a proposal in `registers/open points.md` instead.

## The assignment
- **Course:** 21072 Data Analysis Module I (Data Lab for Entrepreneurship), Bocconi 2026/27, Stefano Breschi and Luisa Gagliardi; TA Rujuta Shirish Bhagwat. The brief is in the intro slides (*Intro2026.pdf*, slides 11–16); it is not in the repo.
- **Task:** a research question on startups and VC that can be tested with **PitchBook data** (US companies, 2012–2019 sample from Blackboard). Other data may be added.
- **Deliverable:** a **slide deck only**, no written report; code submission is optional. Presentation of **about 25 minutes**. Final presentations run 27/11, 30/11 and 04/12/2026; **the deck is due 27/11/2026** (Lele, 17/11). We are Group 21. The slide count does not matter, the talk length does.
- **Grading:** the project is 40% of the grade for attending students. Criteria: **clarity and organization, depth of analysis, use of data, originality and critical thinking, delivery and visual communication.**
- **AI policy:** AI is allowed for the project work and is not allowed in the final written exam.

## Our project in one paragraph
Research question: *is the time between the first and the second VC round associated with the probability of exit, and does this association differ between hot and cold funding markets?* We keep every US startup with a disclosed first VC round (28,478) and split it into those that raised a second round (`two_rounds` = 1) and those that did not (= 0). The gap enters the model only for the first group, through `log_gap_r2`. Hype is `heat`: the sector's share of all VC dollars in the year of round 1, z-scored within the sector. The hypotheses are H1 (gap → exit), H1b (gap → failure), H2 (gap × hype, the key one) and H3 (gap → valuation step). The latest write-up is `paper_group21.pdf` (v4, 15/11/2026).

## Working with the user (every member)
- **Name.** At the start of every new session, if Claude does not already know the person's name, its first message asks how they want to be called. From then on it uses that name **within the first three words of every message**. Lele is called "Lele".
- **Advisor, not assistant.** Accuracy matters, agreement does not.
  1. Do not open with agreement or praise. If an idea has a flaw, a gap or a risky assumption, say it in the first sentence (after the name). If it is solid, say so in one line and move on. Never invent objections.
  2. Give a confidence level for key claims: **[Certain]** for direct evidence (log, data, paper), **[Likely]** for strong inference, **[Guessing]** when filling gaps. If most of a reply is guesswork, say so at the start.
  3. No empty courtesy ("great question", "you're absolutely right", "that makes sense", "absolutely", "definitely").
- **Verify, do not trust.** When someone states or contests something (a number, a sign, a p-value, what a paper says), check it against the log, the data or the paper, and say clearly whether the source supports them. Do not take Claude's word or the member's word as proof.
- **Do what was asked without asking again.** Ask only if the action goes beyond the request or what you find does not match what was described.
- **Ask when something is unclear, with full context.** When you ask a question, give everything needed to answer it: what the outline says today, what you found, the options with pros and cons. No bare IDs (R-xx, I-xx, β3, H2...) without saying what they are, for example "β3, the coefficient of gap × hype that tests H2".
- **Explain every reference.** Every citation of a paper, a method or a course concept comes with what it says, in a few words, before the reference: not "see Tian (2011)" but "staging goes with more IPOs when the VC is far from the firm (Tian, 2011)"; not "cluster at sector-year" but "errors are allowed to be correlated among startups funded in the same sector and year (clustered SEs)".
- **Step by step.** Work one section or one slide at a time: first brainstorm, then the group decides, then write. Do not change the slide outline until asked.
- **Long texts.** For long documents (the paper, the log, literature PDFs) use NotebookLM or scripts that write their output to files, instead of loading the whole text into Claude's context.
- **Subagents** run on the Sonnet model unless the user says otherwise. Pass `model: "sonnet"` explicitly in every subagent call, even when an agent definition with `model: sonnet` exists: definitions in a subfolder's `.claude/agents/` (e.g. `skill-redigere essay/`) are not loaded when the session starts from the repo root, and a generic subagent inherits the session's model.

## Changes to `scaletta.md` (decided by Lele, 16/11/2026)
- `scaletta.md` is the group's reference document. **Anyone may edit it**, members and their Claudes.
- **Every change is logged** as one row in `registers/changelog.md`, in the same commit as the change: date, who (the member's name; "Claude for X" if an AI made it), section, what changed (old → new, or a short summary for long edits), why (decision, open point or result it rests on).
- The commit message names the member and the section, e.g. `scaletta 2.3: rewrite point 3 (Lele)`.
- A change that touches a decision in *Decisions already taken* still needs group agreement first (see above); the changelog does not replace it.
- The same rule applies to `glossary.md` and to the registers.

## Git
- Everyone works **on `main`**: no branches or worktrees. Commit and push straight to `main`. GitHub is only the shared source between people and AIs.
- Several people push to the same branch, so: `git pull --rebase` **before starting** and **before every push**; make small commits with clear messages; push right after committing.
- Binary files (`.dta`, `.docx`, `.doc`, `.pdf`, `.pptx`) cannot be merged. Before editing one, tell the group; if a pull brings a conflict on a binary file, stop and ask, never overwrite someone else's version.
- GitHub rejects files above 100 MB. PitchBook raw files are in `0. dati iniziali/` (the group agreed they may be uploaded), zipped because `Deal.csv` and `pitchbook_course.dta` are above that limit.

## Files and their role
| File | What it is | Status |
|---|---|---|
| `0. dati iniziali/` | Raw PitchBook files, zipped: `pitchbook_course.dta`, `Deal.csv`, `DealInvestorRelation.csv`, `Investor.csv` | Current |
| `1. python/dataset.py` | Builds the dataset from the raw PitchBook files in `data/` (unzip them there); writes `output/rq1_two_group_dataset_v2.dta` and `.csv` | Current (v2) |
| `2. dataset/dataset.dta` | Output of `dataset.py`: 28,478 startups × 57 variables | Current |
| `3. stata/rq1_two_group_analysis_v2.do` | Main Stata analysis: descriptives, logit models, figures, Word tables | Current |
| `3. stata/rq1_addon_extra_controls.do` | Robustness add-on: team and lead-investor-age controls | **Superseded** by `rq1_addon_not_in_log_checks.do` (block A, same code; checked 17/11). Do not run |
| `4. risultati/regression_analysis.txt` | Stata log of the do-file (run 15/11/2026). **Primary source for every number** | Current |
| `3. stata/rq1_addon_not_in_log_checks.do` | Add-on: reruns in Stata the paper v4 analyses computed outside the do-file (Table 12, Figures 8, 17, 19, the §5.4 checks, the N of the AMEs); absorbs `rq1_addon_extra_controls.do` | Current (run 17/11/2026) |
| `4. risultati/not_in_log_checks.txt` | Stata log of `rq1_addon_not_in_log_checks.do`: primary source for the numbers of Table 12, Figures 8, 17, 19 and the §5.4 checks | Current (17/11/2026) |
| `4. risultati/RQ1_tables.doc` | Word/RTF tables produced by the do-file | Current |
| `5. paper e documentazione di percorso/paper_group21.pdf` | Group paper v4 (15/11/2026): theory, hypotheses, results, robustness, limits. Source for the deck | Current |
| `2. dataset/construction.pdf` | How the v2 dataset is built, with sample steps and a list of every variable (14/11/2026) | Current, except where noted below |
| `5. paper e documentazione di percorso/main_important_stuff_ig.docx` | Early notes on cleaning, variables and literature for the pitch | Partly outdated |
| `scaletta.md` | Reference outline (v1, 16/11/2026): content, sources and numbers for paper v5 and the slide outline | **Single source of truth.** Every edit logged in `registers/changelog.md` |
| `glossary.md` | One canonical term per concept | Current (16/11/2026) |
| `registers/` | Results register, inferences register, open points, changelog | Kept up to date |
| `slide outline.md` | The deck outline (to be created) | Next task |

**Known inconsistencies.** Do not "fix" them silently; ask before changing code or documents.
- **Dataset name.** The same file has three names: `dataset.dta` in the repo, `output/rq1_two_group_dataset_v2.dta` written by `dataset.py`, and `group_21_dataset.dta` opened by the do-files. Before running the do-file, copy or rename the file locally.
- **Main outcome.** The main outcome is **`exit_5y`** (exit within 5 years of the window start), as in the paper and the do-file. `construction.pdf` says "exit is the main outcome": on this point it is **superseded**. `exit` (exit at any time, no window) is a robustness check.
- **Accelerator control.** `main_important_stuff_ig.docx` lists an `Accelerator_pre_r1` control and Yu (2020). The v2 dataset has no such variable. Do not cite it as a control.
- **Script name.** `construction.pdf` calls the script `rq1_two_group_dataset_v2.py`; in the repo it is `dataset.py`.
- **Checks outside the log.** The further checks in Section 5.4 of the paper were run outside the do-file (paper §5.6), so their numbers are not in `regression_analysis.txt`. In the register they must be marked "not in log".

## Sources and citations
- **Numbers about our results** (coefficients, p-values, N, rates) come from the **Stata log** (`regression_analysis.txt`, with line number) or from a table produced by the do-file. The paper is a secondary source for numbers: if paper and log disagree, the log wins and the mismatch goes in the open points.
- **Every number states what it is:** a logit coefficient, an odds ratio or an average marginal effect (in percentage points); its p-value; the sample (e.g. `full_window == 1`, N = 9,263); the standard errors (clustered by sector × year of round 1, 41 clusters in the main exit models).
- **Descriptive facts about the data** (sample sizes, shares, sector counts) come from `construction.pdf` tables or from code run on `dataset.dta`. Say which.
- **Econometric methods and terms** come from the course: the intro slides and the textbook Hill, Griffiths and Lim (2018), *Principles of Econometrics*. The course brain repo `Emanuele-Notes/backup-brain-I_sem_2026` has **no 21072 folder yet**. When one is added, methods are cited from it (lesson + §). Never cite a method or a framework that is not in the course or the paper without telling the user.
- **Literature** is cited as it appears in the paper's reference list (author, year). The PDFs of the papers are not in the repo, so what a paper says is only as reliable as our summary of it. Do not add a new reference, or put a sentence of it in quotes, without checking the original.
- **Quotes** in quotation marks must match the source word for word.
- On slides: a short source at the bottom (e.g. "Logit, Table 2; PitchBook 2012–2019") and a final slide or appendix with the full references.

## Results, claims and inferences
- **Result:** a number or pattern produced by our data or code (log, table, figure). It goes in `registers/results register.md` with an ID (R-xx).
- **Literature claim:** what a paper says. It is written as "X (year) finds...".
- **Inference:** our reading of a result (why the gap goes with less failure, what it means for founders). It goes in `registers/inferences register.md` with an ID (I-xx), the results it rests on and a status ⏳ proposed / ✅ approved / ❌ rejected. It is written in the first person: "we read this as", "this suggests". **An inference with no result under it does not go on a slide.** The group decides which inferences to keep.
- **Associations only.** The design does not assign the gap at random. Never use causal language ("a longer gap causes / reduces / leads to"); write "is associated with", "goes with".
- **Limits to keep in mind** (paper §5.6):
  - Do not interpret the coefficient of `two_rounds` (ρ1) as an effect: the group indicator uses information from after round 1.
  - β1 (coefficient of `log_gap_r2`) and β3 (coefficient of `log_gap_r2 × heat`) describe only startups that reached round 2.
  - Exit and failure are competing outcomes modelled separately.
  - The valuation step uses post-money valuations and is observed for about half of the two-round startups.
- **Verdicts on the hypotheses** use the paper's wording (Table 13: "right sign, not significant", "rejected, opposite sign", "not supported"). Do not turn "not significant" into "no effect" or "confirmed".
- **Never invent** a number, a result or a plausible detail to fill a gap. Tell the user what is missing and add it to `registers/open points.md`.

## Slide outline format
- One file, `slide outline.md`, with the slides in order. Planned sections: motivation and research question → literature and hypotheses → data and sample → variables and method → results (H1, H1b, H2, H3) → robustness → discussion and limits → conclusion. The number of slides is still open (25 minutes; the prof gave no limit).
- **Slide title = a claim** in English (a sentence that states something, e.g. "Slow second rounds are not a distress signal"), not a label ("Results").
- Each slide follows this schema:
  ```
  ## N · Claim title in English · SECTION
  **Message:** the one thing the audience should remember
  **Content and visual:** what is on the slide and which figure or table (from figures/ or RQ1_tables)
  **Results:** R-xx IDs
  **Inferences:** I-xx IDs (approved only)
  **Literature / method:** author (year) or course source, with what it says
  **Speaker notes:** (optional)
  **Comments / open points:** (only if there are any)
  ```
- **One message per slide, at most one or two visuals.** Two charts, not ten numbers. A number shown in a chart is not repeated in the slide text.
- **No duplicates.** Each result has **one home slide**; elsewhere only a pointer or nothing.
- **The registers are updated every time** a slide is added or changed.
- Briefs for the Claudes that draft slides get only the approved results and inferences of their own slides, plus the list of those that belong to other slides and must not be rewritten.

## Decisions already taken (change only with group agreement)
- Research question, two-group design (`two_rounds` = 1 / 0), the gap entering as `log_gap_r2`.
- Main outcome **`exit_5y`**, main estimation sample `full_window == 1`. Main model: logit of `exit_5y` on `two_rounds × heat` and `log_gap_r2 × heat`, round-1 controls (`log_round1_size`, `round1_number`, `startup_age_at_round1`, lead-investor type), year-quarter, sector and state fixed effects, SEs clustered by sector × year of round 1.
- Hype = `heat` (z-score of the sector's VC share within the sector). `heat_past`, `heat_quarter` and `hype_index_l` are robustness only.
- Controls measured at round 1 only. Round-2 variables (size, valuation) are mediators, used only in robustness and in H3.
- Undisclosed round-1 amounts are dropped, not imputed (feedback from the 13/11 pitch). Window sensitivity: 4, 5 and 6 years.
- Next task: the **slide outline**, built from paper v4.
