# CLAUDE.md

You are working in the repository of **Group 21, 21072 Data Analysis (Data Lab for Entrepreneurship), Bocconi 2026/27**. Several group members use this repo, each with their own Claude.

**Before anything else, read and follow `RULES.md`.** It is binding for every session and every member:
- how to address the user (ask their name in the first message of the session if you don't know it, then use it within the first three words of every message);
- advisor mode, with [Certain] / [Likely] / [Guessing] confidence levels;
- Git on `main` only, with `git pull --rebase` before starting and before pushing;
- which file is the source for which number;
- associations, never causal language;
- the decisions already taken, which change only with group agreement.

@RULES.md

## Commit authors (decided by Lele, 17/11/2026)
Every commit is authored by the member you work for, never by Claude.
- Before the first commit of the session, check `git config user.name` and `git config user.email`. If they say `Claude` or `noreply@anthropic.com` (the default in Claude Code on the web), set them to the member's GitHub identity, for this repo only:
  - Lele: `git config user.name "emanuelefalzi"` and `git config user.email "47462473+emanuelefalzi@users.noreply.github.com"`.
  - Any other member: ask for their GitHub username and noreply email, then set them the same way.
- No AI attribution in commit messages: no `Co-Authored-By: Claude …`, no `Claude-Session: …`, no "Generated with Claude Code". In the message, name only the member, e.g. `(Lele)`, never `(Claude for Lele)`.
- Push to `main` only. Never create `claude/…` branches; if the environment starts you on one, switch to `main` before committing.

Also look at:
- `README.md`: what is in the repo and how to run the pipeline.
- `registers/`: results (R-xx), inferences (I-xx) and open points. Check them before proposing anything and update them when slides change.

Current task: **build the slide outline** (`slide outline.md`) from `5. paper e documentazione di percorso/paper_group21.pdf` v4, one section at a time: brainstorm, then the group decides, then write.

## Routine validazione fonti
When a member says «lancia routine validazione fonti» (or «valida le fonti», «run the source validation»), read `routine validazione fonti/CLAUDE.md` and run it from start to end without asking again. It checks every source cited in `scaletta.md` against its txt in `fonti/txt/` and writes `routine validazione fonti/tabella.csv` and `referto.md`.

## Routine redigere paper
When a member says «lancia redigere paper» (or «scrivi il paper», «run the paper pipeline»), read `skill-redigere paper latex/ROUTINE.md` and run it from start to end without asking again, on any computer (it installs what is missing or says exactly what to install). It turns `scaletta.md` into the final LaTeX paper (body ≤ 20 pages with all 21 figures and 14 tables of paper v4, then References and Appendix A) and writes `5. paper e documentazione di percorso/paper_group21_v5.pdf`.
