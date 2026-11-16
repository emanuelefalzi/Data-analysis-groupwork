# Routine validazione fonti (source validation)

**Trigger.** When a member says «lancia routine validazione fonti», «valida le fonti», «run the
source validation» or similar, run this procedure as it is, from start to end, without asking
again. It needs nothing from the member. Repo-wide rules (`RULES.md`: name in the first three
words, advisor mode, Git on `main`) still apply.

## What it does

It checks every source cited in `scaletta.md` against the text of that source in `fonti/txt/`.
One row per pair **(x.y section of the scaletta × bib key)**:

| column | filled by | what it is |
|---|---|---|
| `riga` | `costruisci.py` | row id, `<sezione>__<id_fonte>` (`__2` if the same pair appears twice) |
| `sezione`, `id_fonte` | `costruisci.py` | the x.y and the `fonti.bib` key |
| `co_citate` | `costruisci.py` | other keys cited in the same bullet |
| `tesi` | `costruisci.py` | what the scaletta says the source says (text after the key in the **Sources** block) |
| `estrazione` | reader | what the txt really says on that point |
| `citazione` | reader | one contiguous passage, word for word |
| `posizione` | reader | section or page of the passage |
| `esito` | reader / scripts | `usabile` · `da riformulare` · `non usabile` · `non verificabile` · `fonte assente` (no txt) · `solo rimando` (bullet is a pointer, no claim) · `da leggere` · `SCARTO` |
| `citazione_trovata` | `verifica.py` | `sì` if the quote is in the txt |
| `note` | reader / `verifica.py` | caveats, or why the row was discarded |
| `file_txt` | `costruisci.py` | path of the txt used |

**The rule above all:** the question is not "is the tesi true?" but "does this txt, as it is,
support this tesi, as it is worded?". When in doubt, the more conservative esito wins.

## Files

| Path | What it is |
|---|---|
| `strumenti/costruisci.py` | Step 1: parses `scaletta.md` + `fonti/fonti.bib`, writes `lavoro/task/<id_fonte>.json` and an empty `tabella.csv` |
| `prompt/lettore.md` | The reader prompt (one Sonnet subagent per source) |
| `strumenti/verifica.py` | Step 3: checks every reader JSON, fills `tabella.csv`, writes `referto.md` |
| `tabella.csv` | **The table** (UTF-8 with BOM, opens in Excel). Output, never edited by hand |
| `referto.md` | The report, ordered by severity |
| `lavoro/` | Tasks and reader outputs (`estratti/`). Kept in Git so another member can resume |

Scripts use only the Python standard library. Run them from the repo root:
`python3 "routine validazione fonti/strumenti/<script>.py"`.

## Procedure

0. `git pull --rebase` (RULES).
1. **Build.** `costruisci.py`. It prints how many rows and sources there are to read. If
   `lavoro/estratti/` already has outputs from an earlier run, keep them: `verifica.py` accepts
   them only if the tesi has not changed (`firma`), so only changed or new rows need reading.
   To start from zero, delete `lavoro/estratti/` first.
2. **Read.** Run `verifica.py` once to see which sources have rows `da leggere` or `SCARTO`. For
   each of those sources, launch **one subagent on Sonnet** (`model: "sonnet"`), in parallel in
   batches of about 10, with this prompt:
   > Read and follow `routine validazione fonti/prompt/lettore.md`. Your task is
   > `routine validazione fonti/lavoro/task/<id_fonte>.json`. Write only your output JSON.

   If a source already has an output but some rows are SCARTO, give its reader the errors that
   `verifica.py` printed and ask it to rewrite the whole JSON for that source.
3. **Check.** `verifica.py`. Repeat step 2 for the SCARTO rows until there are none (at most
   3 rounds; after that, leave them as SCARTO and list them in the report to the member).
4. **Commit** on `main`: `tabella.csv`, `referto.md`, `lavoro/`. Message e.g.
   "Source validation: N rows read". Pull with rebase before pushing.
5. **Report to the member** in chat, short: counts per esito, then every `non usabile`,
   `non verificabile` and `fonte assente` row in one line each, then the `da riformulare` rows
   with a proposed narrower wording taken from `estrazione` (the tesi shrinks, never widens).

## What the orchestrator does not do

- It does not write verdicts or fix a reader's JSON to make it pass: wrong rows are redone by
  the reader.
- It does not edit `scaletta.md`, the paper or the slide outline. The report proposes, the
  group decides (RULES: decisions are the group's).
- It does not read the PDFs or the web: only the txt in `fonti/txt/` counts.
- One reader per source, no second reader: the group chose this to keep it simple (16/11/2026).
  The report says so, so nobody reads a single reading as a double check.

## Known limits

- The `tesi` is the short summary in the **Sources** block, not the sentences of the Content
  block. A source can be fine for its summary and still be stretched in the prose.
- `nanda2017` and `townsend2015` have no txt (`fonti/non scaricati.md`): their rows are
  `fonte assente` until the txt is added to `fonti/txt/` and to `fonti.bib` with a `file` field.
- The parser reads bullets that start with `` `key` `` (optionally after ⚠) inside a
  `#### Sources` / `### Sources` block. A different format in `scaletta.md` is skipped silently:
  check the row count that `costruisci.py` prints.
