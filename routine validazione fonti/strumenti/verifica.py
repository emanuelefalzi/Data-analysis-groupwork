#!/usr/bin/env python3
"""Step 3: check the readers' JSON and write tabella.csv + referto.md.

For every row of every lavoro/estratti/<id_fonte>.json it checks mechanically
what the reader was only asked to do:
  - the row exists in the task and its `firma` matches (the tesi has not
    changed in scaletta.md since the task was built);
  - esito is one of the four allowed values;
  - 'usabile' / 'da riformulare' have a citazione;
  - the citazione (>= 25 characters) is in the source txt, as ONE contiguous
    passage (comparison on letters and digits only, so line breaks,
    hyphenation, ligatures and the publishers' "Downloaded from..." lines do
    not matter);
  - 'non verificabile' says what was read and searched (>= 150 characters).
A row that fails is a SCARTO: its columns stay empty in tabella.csv and the
reader of that source has to redo it. Never fix a reader's JSON by hand.

Usage (from anywhere):
    python3 "routine validazione fonti/strumenti/verifica.py"
"""
import csv, json, os, re, unicodedata

QUI = os.path.dirname(os.path.abspath(__file__))
ROUTINE = os.path.dirname(QUI)
REPO = os.path.dirname(ROUTINE)
TASK = os.path.join(ROUTINE, "lavoro", "task")
ESTRATTI = os.path.join(ROUTINE, "lavoro", "estratti")
TABELLA = os.path.join(ROUTINE, "tabella.csv")
REFERTO = os.path.join(ROUTINE, "referto.md")

ESITI = ["usabile", "da riformulare", "non usabile", "non verificabile"]
CAMPI = ["riga", "firma", "estrazione", "citazione", "posizione", "esito", "note"]

# publisher stamps that pdftotext puts in the middle of the text
TIMBRI = [
    re.compile(r"This content downloaded from.*?about\.jstor\.org/terms", re.S),
    re.compile(r"[\d, -]*Downloaded from.*$", re.M),
    re.compile(r"^.*Your use of the JSTOR archive.*$", re.M),
]


def alnum(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"[^a-z0-9]", "", s.lower())


_cache = {}


def testo(path):
    if path not in _cache:
        t = open(os.path.join(REPO, path), encoding="utf-8", errors="replace").read()
        for r in TIMBRI:
            t = r.sub(" ", t)
        _cache[path] = alnum(t)
    return _cache[path]


def controlla(r, task_riga, file_txt):
    err = []
    if task_riga is None:
        return ["row not in the task (scaletta changed? rerun costruisci.py and re-read)"]
    if r.get("firma") != task_riga["firma"]:
        err.append("firma does not match: the tesi changed since the reading, re-read")
    if r.get("esito") not in ESITI:
        err.append(f"esito not allowed: {r.get('esito')!r}")
    q = (r.get("citazione") or "").strip()
    if r.get("esito") in ("usabile", "da riformulare") and not q:
        err.append(f"'{r.get('esito')}' without citazione")
    if q:
        if len(alnum(q)) < 25:
            err.append("citazione too short to check (< 25 letters/digits)")
        elif alnum(q) not in testo(file_txt):
            err.append("citazione not found in the txt as one contiguous passage")
    est = (r.get("estrazione") or "").strip()
    if not est:
        err.append("estrazione empty")
    if r.get("esito") == "non verificabile" and len(est) < 150:
        err.append("'non verificabile' must say what was read and searched (>= 150 characters)")
    return err


def main():
    with open(TABELLA, encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        colonne, righe = rd.fieldnames, list(rd)

    tasks = {}
    for f in os.listdir(TASK):
        if f.endswith(".json"):
            t = json.load(open(os.path.join(TASK, f), encoding="utf-8"))
            tasks[t["id_fonte"]] = t

    esiti, scarti, illeggibili = {}, {}, []
    if os.path.isdir(ESTRATTI):
        for f in sorted(os.listdir(ESTRATTI)):
            if not f.endswith(".json"):
                continue
            try:
                d = json.load(open(os.path.join(ESTRATTI, f), encoding="utf-8"))
            except Exception as ex:
                illeggibili.append(f"{f}: {ex}")
                continue
            t = tasks.get(d.get("id_fonte"))
            if t is None:
                illeggibili.append(f"{f}: id_fonte {d.get('id_fonte')!r} has no task")
                continue
            per_riga = {x["riga"]: x for x in t["righe"]}
            for r in d.get("righe", []):
                e = controlla(r, per_riga.get(r.get("riga")), t["file_txt"])
                (scarti if e else esiti)[r.get("riga")] = e or r

    for r in righe:
        # rows without a reader (fonte assente / solo rimando) keep their esito
        if r["esito"] in ("fonte assente", "solo rimando"):
            continue
        for c in ("estrazione", "citazione", "posizione", "esito", "citazione_trovata", "note"):
            r[c] = ""
        x = esiti.get(r["riga"])
        if x:
            for c in ("estrazione", "citazione", "posizione", "esito", "note"):
                r[c] = (x.get(c) or "").strip()
            r["citazione_trovata"] = "sì" if r["citazione"] else ""
        elif r["riga"] in scarti:
            r["esito"] = "SCARTO"
            r["note"] = "; ".join(scarti[r["riga"]])
        else:
            r["esito"] = "da leggere"

    with open(TABELLA, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=colonne)
        w.writeheader()
        w.writerows(righe)

    ordine = ["SCARTO", "da leggere", "non usabile", "non verificabile", "fonte assente",
              "da riformulare", "usabile", "solo rimando"]
    conta = {o: [r for r in righe if r["esito"] == o] for o in ordine}
    with open(REFERTO, "w", encoding="utf-8") as fh:
        fh.write("# Source validation report\n\n")
        fh.write("Generated by `strumenti/verifica.py` from `tabella.csv`. One reader per source, "
                 "no second reader: every verdict below is a single reading, checked only "
                 "mechanically (the quote exists in the txt).\n\n")
        fh.write("| esito | rows |\n|---|---|\n")
        for o in ordine:
            fh.write(f"| {o} | {len(conta[o])} |\n")
        fh.write("\n")
        for o in ordine:
            if not conta[o] or o in ("usabile", "solo rimando"):
                continue
            fh.write(f"## {o} ({len(conta[o])})\n\n")
            for r in conta[o]:
                fh.write(f"### {r['sezione']} · `{r['id_fonte']}`\n")
                fh.write(f"- **Tesi (scaletta):** {r['tesi']}\n")
                if r["estrazione"]:
                    fh.write(f"- **What the source says:** {r['estrazione']}\n")
                if r["citazione"]:
                    pos = f" ({r['posizione']})" if r["posizione"] else ""
                    fh.write(f"- **Quote{pos}:** \"{r['citazione']}\"\n")
                if r["note"]:
                    fh.write(f"- **Note:** {r['note']}\n")
                fh.write("\n")
        if conta["usabile"]:
            fh.write(f"## usabile ({len(conta['usabile'])})\n\n")
            for r in conta["usabile"]:
                fh.write(f"- {r['sezione']} · `{r['id_fonte']}`: {r['tesi']}\n")

    print("  ".join(f"{o}: {len(conta[o])}" for o in ordine))
    for x in illeggibili:
        print(f"  UNREADABLE {x}")
    per_fonte = {}
    for k, e in scarti.items():
        per_fonte.setdefault(k.split("__")[1], []).append((k, e))
    for f, lst in sorted(per_fonte.items()):
        print(f"  SCARTO in {f}:")
        for k, e in lst:
            print(f"     {k}: {'; '.join(e)}")
    print("-> tabella.csv, referto.md")


if __name__ == "__main__":
    main()
