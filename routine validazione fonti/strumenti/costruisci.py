#!/usr/bin/env python3
"""Step 1: build the table of (x.y section x source) pairs from scaletta.md.

Reads every **Sources** block of scaletta.md. Each bullet that starts with one or
more `bibkey`s followed by ':' becomes one row per key; the text after ':' is
the "tesi" (what the scaletta attributes to the source). The txt of each key is
taken from the `file` field of fonti/fonti.bib.

Writes:
  lavoro/task/<id_fonte>.json   one task per source, listing all its rows
  tabella.csv                   the table, with extraction columns still empty
                                (verifica.py rewrites it with the results)

Keys without a txt (e.g. the @comment block of fonti.bib) get esito
'fonte assente'; bullets marked "pointer" get 'solo rimando'. Neither gets a
task: nobody reads them.

Standard library only. Usage (from anywhere):
    python3 "routine validazione fonti/strumenti/costruisci.py"
"""
import csv, hashlib, json, os, re

QUI = os.path.dirname(os.path.abspath(__file__))
ROUTINE = os.path.dirname(QUI)
REPO = os.path.dirname(ROUTINE)
SCALETTA = os.path.join(REPO, "scaletta.md")
BIB = os.path.join(REPO, "fonti", "fonti.bib")
TASK = os.path.join(ROUTINE, "lavoro", "task")
TABELLA = os.path.join(ROUTINE, "tabella.csv")

COLONNE = [
    # identification (costruisci.py)
    "riga", "sezione", "id_fonte", "autore_anno", "co_citate", "tesi",
    # verification (reader, checked by verifica.py)
    "esito", "estrazione", "citazione", "posizione", "citazione_trovata",
    # for writing the paper and the deck (reader)
    "frase_paper", "frase_slide", "forza", "tipo_studio", "dati_metodo", "numero_chiave",
    "limiti_vs_noi",
    # housekeeping
    "note", "file_txt"]


def autore_anno(autori, anno):
    """APA-style in-text citation from a bib author field: Smith (2001), Smith & Lee (2001),
    Smith et al. (2001)."""
    cognomi = [a.split(",")[0].strip() for a in re.split(r"\s+and\s+", autori) if a.strip()]
    if not cognomi:
        return ""
    if len(cognomi) == 1:
        testa = cognomi[0]
    elif len(cognomi) == 2:
        testa = f"{cognomi[0]} & {cognomi[1]}"
    else:
        testa = f"{cognomi[0]} et al."
    return f"{testa} ({anno})"

KEY = r"`([a-z][a-z]*\d{4}[a-z]?)`"
SEZ = re.compile(r"^#{2,3} (\d+(?:\.\d+)?) ")
BULLET = re.compile(r"^- (?:⚠ )?" + KEY)


def firma(testo):
    return hashlib.sha1(testo.encode("utf-8")).hexdigest()[:10]


def leggi_bib():
    """bibkey -> {'file': absolute txt path, 'autore_anno': 'Smith et al. (2001)'}."""
    out, chiave = {}, None
    for l in open(BIB, encoding="utf-8"):
        m = re.match(r"^@\w+\{([^,]+),", l)
        if m:
            chiave = m.group(1).strip()
            out[chiave] = {}
            continue
        m = re.match(r"^\s*(file|author|year)\s*=\s*\{(.+)\},?\s*$", l)
        if m and chiave:
            out[chiave][m.group(1)] = m.group(2).strip()
    for k, v in out.items():
        v["file"] = os.path.join(REPO, v["file"]) if v.get("file") else ""
        v["autore_anno"] = autore_anno(v.get("author", ""), v.get("year", ""))
    return out


def coppie():
    sez, dentro, righe = None, False, []
    for l in open(SCALETTA, encoding="utf-8"):
        l = l.rstrip("\n")
        m = SEZ.match(l)
        if m:
            sez = m.group(1)
        if re.match(r"^#+ Sources\b", l):
            dentro = True
            continue
        if l.startswith("#"):
            dentro = False
        if not dentro or not sez:
            continue
        if not BULLET.match(l):
            continue
        corpo = l[2:].lstrip("⚠ ").strip()
        testa, due_punti, coda = corpo.partition(": ")
        if not due_punti:                      # e.g. "`ai2003`, `mize2019` (pointer only, ...)."
            testa, coda = corpo, re.sub(KEY + r",? ?", "", corpo).strip()
        chiavi = re.findall(KEY, testa)
        tesi = coda.strip()
        for k in chiavi:
            righe.append({"sezione": sez, "id_fonte": k,
                          "co_citate": " ".join(c for c in chiavi if c != k), "tesi": tesi})
    return righe


def main():
    bib = leggi_bib()
    righe, visti = [], {}
    for r in coppie():
        base = f"{r['sezione']}__{r['id_fonte']}"
        visti[base] = visti.get(base, 0) + 1
        r["riga"] = base if visti[base] == 1 else f"{base}__{visti[base]}"
        b = bib.get(r["id_fonte"], {})
        txt = b.get("file", "")
        r["autore_anno"] = b.get("autore_anno", "")
        r["file_txt"] = os.path.relpath(txt, REPO) if txt and os.path.exists(txt) else ""
        if not r["file_txt"]:
            r["esito"] = "fonte assente"
        elif re.search(r"\bpointer", r["tesi"], re.I):
            r["esito"] = "solo rimando"          # no claim to check
        else:
            r["esito"] = ""
        righe.append(r)

    # one task per source
    os.makedirs(TASK, exist_ok=True)
    for f in os.listdir(TASK):
        if f.endswith(".json"):
            os.remove(os.path.join(TASK, f))
    per_fonte = {}
    for r in righe:
        if not r["esito"]:
            per_fonte.setdefault(r["id_fonte"], []).append(r)
    for k, rr in per_fonte.items():
        task = {"id_fonte": k, "autore_anno": rr[0]["autore_anno"], "file_txt": rr[0]["file_txt"],
                "righe": [{"riga": r["riga"], "firma": firma(r["tesi"]), "sezione": r["sezione"],
                           "tesi": r["tesi"], "co_citate": r["co_citate"]} for r in rr]}
        with open(os.path.join(TASK, k + ".json"), "w", encoding="utf-8") as fh:
            json.dump(task, fh, ensure_ascii=False, indent=1)

    with open(TABELLA, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLONNE, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)

    assenti = sorted({r["id_fonte"] for r in righe if not r["file_txt"]})
    da_leggere = sum(len(v) for v in per_fonte.values())
    print(f"{len(righe)} rows, {da_leggere} to read from {len(per_fonte)} sources "
          f"-> tabella.csv, lavoro/task/")
    if assenti:
        print(f"No txt, marked 'fonte assente': {', '.join(assenti)}")


if __name__ == "__main__":
    main()
