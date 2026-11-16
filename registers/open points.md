# Open points

Things we could not establish, inconsistencies to fix and proposals to change a group decision. Close an item by writing the outcome and the date; do not delete it.

| # | Open point | Context | Who / status |
|---|---|---|---|
| 1 | Exact submission date of the deck | Intro slides say "around the end of November"; presentations 27/11, 30/11, 04/12. Which day is Group 21? | open |
| 2 | Number of slides | 25 minutes, no slide limit in the brief | open |
| 3 | One file, three names | `dataset.dta` (repo) = `output/rq1_two_group_dataset_v2.dta` (written by `dataset.py`) = `group_21_dataset.dta` (opened by the do-files). Align them? | open |
| 4 | `construction.pdf` names `exit` as the main outcome | Paper v4 and do-file use `exit_5y`; the group chose `exit_5y` (16/11). Update `construction.pdf`? | open |
| 5 | Paper §5.4 checks are not in the Stata log | Their numbers cannot be traced to `regression_analysis.txt` (paper §5.6). Add them to the do-file, or mark them on the slides? | open |
| 6 | Accelerator control in the early notes | `main_important_stuff_ig.docx` cites `Accelerator_pre_r1` and Yu (2020); not in the v2 dataset | open |
| 7 | No course brain for 21072 | `Emanuele-Notes/backup-brain-I_sem_2026` has no 21072 folder; methods are cited from Hill, Griffiths and Lim (2018) for now | open |
| 8 | Raw PitchBook files not in the repo | `dataset.py` reads `data/pitchbook_course.dta`, `Deal.csv`, `DealInvestorRelation.csv`, `Investor.csv`. The group agreed they may be uploaded; files above 100 MB need zip or Git LFS. **16/11: uploaded zipped in `0. dati iniziali/`** (all zips < 50 MB); `dataset.py` still reads `data/`, so unzip there | done |
