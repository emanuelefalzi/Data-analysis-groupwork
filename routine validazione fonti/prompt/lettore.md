# Reader prompt: one source against its rows of the scaletta

You are the reader of **one** source. The orchestrator gives you the path of your task,
`routine validazione fonti/lavoro/task/<id_fonte>.json`. It holds:

- `id_fonte`: the bib key of the source;
- `file_txt`: the text of the source (a PDF turned into txt, relative to the repo root);
- `righe`: every place where `scaletta.md` cites this source. Each row has `riga` (its id),
  `firma` (copy it back unchanged), `sezione` (the x.y of the scaletta), `tesi` (what the
  scaletta says the source says) and `co_citate` (other keys cited in the same bullet, if any).

## The one question

For each row: **does this txt, as it is, support this tesi, as it is worded?** You are not
deciding whether the tesi is true, whether the paper is good, or how to improve the tesi. Only the
txt counts: do not use what you remember about the paper or its authors.

## How to read

1. Read the whole txt once before judging any row. If it is very long, read at least the
   abstract, the introduction, the conclusion and every section relevant to your rows.
2. Search by concept, not by word. The same words in the txt are not support; different words
   can be.
3. Do not stop at the first match. Introductions simplify: if the results, discussion or
   conclusion narrow the point, the narrower version wins.
4. For each row, three tests in order:
   - **Implication both ways.** Does the txt imply the tesi? Does the tesi say more than the txt
     (extra conditions, generality, causality, strength, a number)?
   - **Scope.** Same subject, sample, period and conditions?
   - **Shows, mentions or assumes.** Does the txt show the point (data, model, argument), only
     mention it in passing, or only assume it? Only "shows" supports a tesi worded as a finding.
5. If `co_citate` is not empty, the tesi is shared with other sources. Judge only what **this**
   source supports. If it supports only part of the tesi, say which part in `note`.

## Esito

| esito | meaning |
|---|---|
| `usabile` | the txt supports the tesi as worded |
| `da riformulare` | the txt says something close but narrower, weaker or different: the tesi must shrink to `estrazione` |
| `non usabile` | the txt does not support the tesi, or contradicts it |
| `non verificabile` | not enough in the txt to decide (e.g. the relevant part is missing or unreadable) |

Rules:
- **When in doubt between two adjacent esiti, choose the more conservative one.** A declared
  `non usabile` is worth more than a wrong `usabile`.
- **Compound tesi** (two claims joined by ";" or "and"): the esito is the worst of the parts, and
  `note` says which part decided it.
- **Numbers are not paraphrased.** If the tesi has a number ("about twice as much"), the txt must
  have the same number, unit and rounding. If not: at most `da riformulare`.
- **Causal wording.** If the tesi says "raises", "causes", "leads to" and the txt only shows an
  association, or the other way round: at most `da riformulare`.
- **What the source reports from others** ("as X (1998) shows") is X's, not this source's,
  unless the source makes it its own. Say so in `note`.
- **Contradiction is not silence.** If the txt says the opposite: `non usabile`, a quote is
  required, and `estrazione` starts with `Contradicts the tesi:`.
- **Never soften a negative verdict.**

## Output: one JSON, nothing else

Write `routine validazione fonti/lavoro/estratti/<id_fonte>.json`, with exactly one entry per row
of the task:

```json
{
  "id_fonte": "gompers1995",
  "righe": [
    {
      "riga": "2.1__gompers1995",
      "firma": "copied from the task",
      "estrazione": "2–4 sentences in English: what the txt really says on this point.",
      "citazione": "ONE contiguous passage, copied word for word from the txt",
      "posizione": "section title or page where the passage is, as written in the txt",
      "esito": "usabile | da riformulare | non usabile | non verificabile",
      "note": "edge cases, which part of a compound tesi decided, shared-tesi caveats"
    }
  ]
}
```

- **`citazione`**: ONE contiguous passage, at least 25 characters, copied word for word: the one
  the verdict rests on. Never join two passages with "…". Never take it from the title page,
  headers, footers or the "Downloaded from…" / JSTOR stamps. Required for `usabile`,
  `da riformulare` and `non usabile` when the txt contradicts the tesi. Line breaks and
  hyphenation do not matter: the check compares letters and digits only.
- **`estrazione`**: what the source says, not what the tesi says. For `non verificabile`, at least
  150 characters on what you read and what you looked for.
- Before writing, search your own quote in the txt (e.g. `grep -F` on a distinctive part of it)
  and make sure it is there.

`strumenti/verifica.py` checks every row: a quote not found, a missing quote, a wrong `firma` or
an esito outside the four values makes the row a SCARTO, and you will be asked to redo it.

## Report in chat

At most 5 lines: how many rows per esito, and anything hard (missing pages, a tesi that mixes two
sources). Do not paste the JSON.
