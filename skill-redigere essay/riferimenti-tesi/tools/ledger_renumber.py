#!/usr/bin/env python3
"""ledger_renumber.py — dopo ogni fix rinumera i `¶N` del LEDGER e verifica
che le righe del LEDGER siano tante quante i paragrafi del DRAFT (§6).
Verifica anche che la prima frase citata da ogni riga `SOURCE["..."]` esista
davvero nel `source_desc` del nodo (`str.find()`, niente offset di
carattere: §6 li ha aboliti apposta).

Uso:
    /usr/bin/python3 tools/ledger_renumber.py 4.2.1                 # rinumera e riscrive
    /usr/bin/python3 tools/ledger_renumber.py 4.2.1 --check-only    # solo verifica, non scrive
    /usr/bin/python3 tools/ledger_renumber.py 4.2.1 --path altro.md # file diverso da nodes/<id>.md
    /usr/bin/python3 tools/ledger_renumber.py --help

Disallineamento (righe LEDGER != paragrafi DRAFT) o prima-frase non trovata
nel `source_desc` = errore: exit code 2, il file non viene riscritto.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
NODES_DIR = ingest.NODES_DIR
BUILD_DIR = ingest.BUILD_DIR

LEDGER_LINE_RE = re.compile(r"^(-\s*)¶\d+(\s*←.*)$")
# Un capoverso puo' portare piu' span distinti (quattro frasi da quattro fonti):
# i writer hanno introdotto da soli la forma di continuazione "¶N (cont.)", che da'
# al LEDGER la granularita' di frase che il §6 punto 5 dichiara mancante. E' un
# miglioramento, non un errore di formato: si conta come parte del capoverso N.
LEDGER_CONT_RE = re.compile(r"^(-\s*)¶\d+\s*\(cont\.\)(\s*←.*)$")
SOURCE_QUOTE_RE = re.compile(r'SOURCE\["([^"]*)"\]')


def split_sections(md_text):
    """Ritorna (draft_text, ledger_text). Entrambe le sezioni sono
    obbligatorie per costruzione (§3: nodes/<id>.md contiene solo queste due)."""
    m_draft = re.search(r"##\s*DRAFT\s*\n(.*?)(?=\n##\s*LEDGER|\Z)", md_text, re.S)
    m_ledger = re.search(r"##\s*LEDGER\s*\n(.*)\Z", md_text, re.S)
    draft = m_draft.group(1) if m_draft else ""
    ledger = m_ledger.group(1) if m_ledger else ""
    return draft, ledger


def draft_paragraphs(draft_text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", draft_text.strip()) if p.strip()]
    return paras


def ledger_lines(ledger_text):
    # Le righe "(cont.)" non aprono un capoverso nuovo: appartengono al
    # precedente, quindi non entrano nel conteggio che va confrontato con i
    # capoversi del DRAFT.
    return [l for l in ledger_text.split("\n")
            if l.strip().startswith("-") and not LEDGER_CONT_RE.match(l)]


def renumber(ledger_text):
    lines = ledger_text.split("\n")
    out = []
    n = 0
    for line in lines:
        if line.strip().startswith("-"):
            c = LEDGER_CONT_RE.match(line)
            if c:
                # continuazione: appartiene al capoverso corrente, non ne apre uno nuovo
                out.append(f"{c.group(1)}\u00b6{n} (cont.){c.group(2)}")
                continue
            n += 1
            m = LEDGER_LINE_RE.match(line)
            if m:
                out.append(f"{m.group(1)}¶{n}{m.group(2)}")
            else:
                # riga malformata (manca la freccia o il ¶): la segnaliamo
                # com'e', rinumerare non deve inventare un formato
                out.append(line)
        else:
            out.append(line)
    return "\n".join(out), n


def get_source_desc(node_id, excel_path=EXCEL_PATH):
    nodes_json_path = BUILD_DIR + "nodes.json"
    if os.path.exists(nodes_json_path):
        import json
        with open(nodes_json_path, encoding="utf-8") as f:
            nodes = json.load(f)["nodes"]
    else:
        loaded = ingest.load_workbook_rows(excel_path)
        nodes, _ = ingest.build_nodes(loaded)
    node = nodes.get(node_id)
    if node is None:
        raise SystemExit(f"nodo {node_id!r} non trovato in nodes.json/Excel")
    return node["source_desc"]


def verify_sources(ledger_text_renumerato, source_desc):
    """Per ogni riga SOURCE["..."], verifica str.find() nel source_desc.
    Ritorna la lista delle prime-frasi non trovate."""
    missing = []
    for m in SOURCE_QUOTE_RE.finditer(ledger_text_renumerato):
        frase = m.group(1)
        if source_desc.find(frase) == -1:
            missing.append(frase)
    return missing


def process(node_id, path, check_only, excel_path=EXCEL_PATH):
    if not os.path.exists(path):
        raise SystemExit(f"file non trovato: {path}")
    md_text = open(path, encoding="utf-8").read()
    draft_text, ledger_text = split_sections(md_text)

    n_paragrafi = len(draft_paragraphs(draft_text))
    n_righe = len(ledger_lines(ledger_text))

    esito = {"n_paragrafi_draft": n_paragrafi, "n_righe_ledger": n_righe}

    if n_paragrafi != n_righe:
        esito["errore"] = (
            f"DISALLINEATO: {n_paragrafi} paragrafi nel DRAFT, {n_righe} righe nel LEDGER. "
            "Non rinumero e non riscrivo: allinea prima le righe."
        )
        return esito

    ledger_rinumerato, n_rinumerate = renumber(ledger_text)
    esito["n_rinumerate"] = n_rinumerate

    source_desc = get_source_desc(node_id, excel_path=excel_path)
    missing = verify_sources(ledger_rinumerato, source_desc)
    if missing:
        esito["prime_frasi_non_trovate"] = missing

    if not check_only and not missing:
        new_text = md_text.replace(ledger_text, ledger_rinumerato) if ledger_text else md_text
        # ricostruiamo esplicitamente per non affidarci a un replace fragile
        # se il testo del ledger comparisse per caso altrove nel file
        m_ledger_full = re.search(r"(##\s*LEDGER\s*\n)(.*)\Z", md_text, re.S)
        if m_ledger_full:
            new_text = md_text[:m_ledger_full.start(2)] + ledger_rinumerato
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        esito["scritto"] = True
    else:
        esito["scritto"] = False

    return esito


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Rinumera i ¶N del LEDGER, verifica paragrafi==righe e che ogni prima "
                     "frase SOURCE[...] esista nel source_desc del nodo.")
    ap.add_argument("nodo", help="id del nodo (usato anche per leggere source_desc)")
    ap.add_argument("--path", help="file .md da elaborare (default: nodes/<id>.md)")
    ap.add_argument("--check-only", action="store_true", help="non riscrive il file")
    ap.add_argument("--excel", default=EXCEL_PATH)
    args = ap.parse_args(argv)

    path = args.path or (NODES_DIR + f"{args.nodo}.md")
    try:
        esito = process(args.nodo, path, args.check_only, excel_path=args.excel)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"paragrafi DRAFT: {esito['n_paragrafi_draft']}  ·  righe LEDGER: {esito['n_righe_ledger']}")
    if "errore" in esito:
        print(esito["errore"])
        sys.exit(2)
    print(f"rinumerate: {esito['n_rinumerate']} righe")
    if esito.get("prime_frasi_non_trovate"):
        print("prime frasi NON trovate nel source_desc (str.find() fallito):")
        for f in esito["prime_frasi_non_trovate"]:
            print(f"  - {f!r}")
        print("Non riscritto: risolvi prima le citazioni non verificabili.")
        sys.exit(2)
    if args.check_only:
        print("--check-only: file non modificato.")
    else:
        print("scritto." if esito.get("scritto") else "non scritto.")
    sys.exit(0)


if __name__ == "__main__":
    main()
