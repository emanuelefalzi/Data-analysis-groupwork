#!/usr/bin/env python3
"""comune.py — percorsi, configurazione e funzioni condivise.

La radice del progetto e' la cartella che contiene `progetto.json` (ricavata dalla
posizione di questo file). I percorsi in progetto.json sono relativi alla radice:
`../scaletta.md` punta alla scaletta nella radice della repo.

Gli script non fanno mai `cd`: si lanciano con percorsi assoluti da qualunque cartella.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGETTO = ROOT / "progetto.json"
BUILD = ROOT / "build"
SEZIONI = ROOT / "sezioni"
REPORTS = ROOT / "reports"
OUT = ROOT / "out"
LATEX = ROOT / "latex"


def cfg() -> dict:
    return json.loads(PROGETTO.read_text(encoding="utf-8"))


def p(key: str) -> Path:
    """Percorso di una voce di progetto.json, risolto rispetto alla radice."""
    c = cfg()
    val = c[key] if key in c else c["latex"][key]
    return (ROOT / val).resolve()


def leggi_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def scrivi_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def die(msg: str, code: int = 2):
    print(f"ERRORE: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------- bib

def chiavi_bib() -> dict[str, dict]:
    """Chiave -> {author, year, title}. Parser minimo, basta per i controlli."""
    path = p("bib")
    if not path.exists():
        die(f"bib non trovato: {path}")
    txt = path.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", txt, re.S):
        if m.group(1).lower() == "comment":
            continue
        corpo = m.group(3)
        campi = {k.lower(): v.strip() for k, v in re.findall(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*\n", corpo, re.S)}
        out[m.group(2)] = campi
    return out


# ----------------------------------------------------------------- validazione

def validazione() -> list[dict]:
    """Righe di `routine validazione fonti/tabella.csv` (una per sezione × fonte)."""
    path = p("validazione_fonti")
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------- testo

TOKEN_RE = re.compile(r"\[\[(CIT-N|CIT-P|CIT-NEEDED|GAP|FIG|TAB|SEC)\s*:\s*([^\]]*?)\s*\]\]")


def draft_di(sid: str) -> str | None:
    f = SEZIONI / f"{sid}.md"
    if not f.exists():
        return None
    txt = f.read_text(encoding="utf-8")
    m = re.search(r"^## DRAFT\s*\n(.*?)(?=^## LEDGER|\Z)", txt, re.S | re.M)
    return m.group(1).strip() if m else None


def ledger_di(sid: str) -> list[str]:
    f = SEZIONI / f"{sid}.md"
    if not f.exists():
        return []
    txt = f.read_text(encoding="utf-8")
    m = re.search(r"^## LEDGER\s*\n(.*)", txt, re.S | re.M)
    if not m:
        return []
    return [r for r in m.group(1).splitlines() if r.strip().startswith("- ¶")]


def paragrafi(testo: str) -> list[str]:
    return [x.strip() for x in re.split(r"\n\s*\n", testo) if x.strip()]


def conta_parole(testo: str) -> int:
    """Parole come nel PDF: una citazione narrativa vale 2, parentetica 3, GAP/CIT-NEEDED 0,
    un rimando a figura/tabella/sezione 2."""
    pesi = {"CIT-N": 2, "CIT-P": 3, "CIT-NEEDED": 0, "GAP": 0, "FIG": 2, "TAB": 2, "SEC": 2}
    n = 0

    def sub(m):
        nonlocal n
        n += pesi[m.group(1)]
        return " "

    resto = TOKEN_RE.sub(sub, testo)
    return n + len(re.findall(r"[A-Za-z0-9][\w'’.\-%]*", resto))


NUM_RE = re.compile(r"(?<![\w.])[−\-–]?\d[\d,]*(?:\.\d+)?%?")


def numeri(testo: str) -> set[str]:
    """Numeri normalizzati (segno meno unificato, niente virgole delle migliaia, niente %)."""
    out = set()
    for m in NUM_RE.findall(TOKEN_RE.sub(" ", testo)):
        x = m.replace("−", "-").replace("–", "-").replace(",", "").rstrip("%")
        if x.lstrip("-") in {"", "."}:
            continue
        out.add(x)
    return out
