#!/usr/bin/env python3
"""comune.py — percorsi, configurazione e funzioni condivise da tutti gli script.

Nessun percorso assoluto scritto a mano: la radice del progetto e' la cartella che
contiene `progetto.json`, ricavata dalla posizione di questo file. Cosi' la cartella
si copia, si rinomina e si sposta senza toccare il codice.

Regola di casa ereditata dalla tesi: gli script non fanno mai `cd`. Si lanciano da
qualunque cartella con percorsi assoluti, per esempio:

    python3 "<radice>/tools/stato.py"
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PROGETTO = ROOT / "progetto.json"
BRIEF = ROOT / "input" / "brief.md"
FONTI_CSV = ROOT / "input" / "fonti.csv"

FONTI = ROOT / "fonti"
PDF_DIR = FONTI / "pdf"
TESTI = FONTI / "testi"            # pdftotext, modalita' a flusso di lettura
TESTI_RAW = FONTI / "testi_raw"    # pdftotext -raw: seconda resa, serve solo alla verifica
TASK = FONTI / "task"
SCHEDE = FONTI / "schede"          # output del lettore A (un JSON per fonte)
SCHEDE_NLM = FONTI / "schede_nlm"  # output del secondo lettore (NotebookLM)
BIB = FONTI / "fonti.bib"

INTERMEDI = ROOT / "intermedi"
SCALETTA = ROOT / "scaletta" / "scaletta.md"
GLOSSARIO = ROOT / "glossario" / "glossario.json"
SEZIONI = ROOT / "sezioni"
BUILD = ROOT / "build"
REPORTS = ROOT / "reports"
OUT = ROOT / "out"

ESTRATTI_JSON = BUILD / "estratti.json"
SEZIONI_JSON = BUILD / "sezioni.json"

DEFAULT_CONFIG = {
    "titolo": "",
    "autore": "",
    "lingua": "en",
    "stile_citazionale": "apa7",
    "parole_totali": 0,
    "tolleranza_parole": 0.15,
    "nomi_fissi": {},
    "doppio_auditor": False,
    "secondo_lettore_nlm": False,
    "notebook_nlm": "",
    "template_docx": "input/template.docx",
    "output_docx": "out/essay.docx",
    "stile_corpo": "Normal",
    "titolo_bibliografia": "References",
}


def config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if PROGETTO.exists():
        cfg.update(json.loads(PROGETTO.read_text(encoding="utf-8")))
    return cfg


def rel(p) -> str:
    """Percorso relativo alla radice, per i messaggi."""
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def lock_files(cartella: Path) -> list[Path]:
    """File `~$*` lasciati da Word/Excel aperti. Se ci sono, non si scrive:
    nella tesi un salvataggio con il file aperto ha cancellato un foglio intero."""
    return sorted(cartella.glob("~$*")) if cartella.exists() else []


# ---------------------------------------------------------------------------
# testo
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    """Normalizza per il confronto: virgolette, trattini, spazi, minuscole."""
    s = s or ""
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return re.sub(r"\s+", " ", s).strip().lower()


def conta_parole(testo: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", testo or ""))


TOKEN_CIT = re.compile(r"\[\[CIT-([NP]):([^\]\s]+)\]\]")
TOKEN_BUCO = re.compile(r"\[\[(GAP|CIT-NEEDED):([^\]]*)\]\]")


def parole_come_nel_word(testo: str) -> int:
    """Conta come conterebbe il documento finito: una citazione autore-data
    occupa circa due parole, un [[GAP:]] o [[CIT-NEEDED:]] non lascia nulla."""
    t = TOKEN_CIT.sub(" Autore Anno ", testo or "")
    t = TOKEN_BUCO.sub(" ", t)
    return conta_parole(t)


# ---------------------------------------------------------------------------
# file di sezione: sezioni/<id>.md con `## DRAFT` e `## LEDGER`
# ---------------------------------------------------------------------------

_DRAFT = re.compile(r"##\s*DRAFT\b[ \t]*\n(.*?)(?=\n?##\s*LEDGER\b|\Z)", re.S)
_LEDGER = re.compile(r"##\s*LEDGER\b[ \t]*\n(.*)\Z", re.S)


def file_sezione(sid: str) -> Path:
    return SEZIONI / f"{sid}.md"


def draft_di(sid_o_path) -> str:
    p = Path(sid_o_path) if str(sid_o_path).endswith(".md") else file_sezione(sid_o_path)
    if not p.exists():
        return ""
    m = _DRAFT.search(p.read_text(encoding="utf-8"))
    testo = m.group(1).strip() if m else ""
    return "" if testo.startswith("## LEDGER") else testo


def ledger_di(sid_o_path) -> str:
    p = Path(sid_o_path) if str(sid_o_path).endswith(".md") else file_sezione(sid_o_path)
    if not p.exists():
        return ""
    m = _LEDGER.search(p.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def paragrafi(testo: str) -> list[str]:
    return [b.strip() for b in re.split(r"\n\s*\n", testo or "") if b.strip()]


# ---------------------------------------------------------------------------
# dati costruiti dagli altri script
# ---------------------------------------------------------------------------

def carica_json(path: Path, cosa_lo_produce: str):
    if not path.exists():
        sys.exit(f"ERRORE: manca {rel(path)}. Lo produce {cosa_lo_produce}.")
    return json.loads(path.read_text(encoding="utf-8"))


def sezioni() -> dict:
    """{id: record} nell'ordine della scaletta."""
    d = carica_json(SEZIONI_JSON, "tools/scaletta/leggi_scaletta.py")
    return {s["id"]: s for s in sorted(d["sezioni"], key=lambda s: s["ordine"])}


def estratti() -> dict:
    return carica_json(ESTRATTI_JSON, "tools/fonti/valida.py")


def domande_dal_brief() -> list[dict]:
    """Le domande per le fonti: voci di elenco sotto un titolo che contiene
    «Domande». Ognuna diventa D1, D2, ... nell'ordine in cui compare, a meno che
    la riga non porti gia' un'etichetta esplicita `D3:`."""
    if not BRIEF.exists():
        return []
    righe = BRIEF.read_text(encoding="utf-8").splitlines()
    dentro, out = False, []
    for r in righe:
        if r.startswith("#"):
            dentro = "domand" in r.lower()
            continue
        if not dentro:
            continue
        m = re.match(r"\s*(?:[-*]|\d+[.)])\s+(.*\S)", r)
        if not m:
            continue
        testo = m.group(1)
        if testo.startswith("<!--"):
            continue
        e = re.match(r"(D\d+)\s*[:.)-]\s*(.*)", testo)
        if e:
            out.append({"id": e.group(1), "testo": e.group(2)})
        else:
            out.append({"id": f"D{len(out) + 1}", "testo": testo})
    return out
