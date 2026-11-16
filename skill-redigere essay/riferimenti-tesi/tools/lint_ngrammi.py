#!/usr/bin/env python3
"""lint_ngrammi.py — controllo antiplagio a n-grammi di 8 parole (§4.7).

Modalita' di default, **per nodo**: il DRAFT del nodo contro le sole
`Citazione verbatim` (Estratti colonna J) delle coppie di quel nodo. E' qui
che va intercettato il rischio, non in fondo alla consegna: `DOSSIER`
colonna Q consegna al writer 103 stringhe copiate parola per parola dai PDF,
con l'ordine esplicito di parafrasarle.

Modalita' `--whole`: il testo passato contro **tutti** i file di
`FONTI/pipeline/testi estratti/` — il controllo finale sul documento intero
(§10, FASE DI CONSEGNA, punto 6).

Uso:
    /usr/bin/python3 tools/lint_ngrammi.py 4.2.1 "testo del paragrafo..."
    /usr/bin/python3 tools/lint_ngrammi.py 4.2.1 --file draft.txt
    /usr/bin/python3 tools/lint_ngrammi.py --whole --file documento.txt
    /usr/bin/python3 tools/lint_ngrammi.py --help

Match case-insensitive, su token alfanumerici (la punteggiatura e gli spazi
non contano ai fini del match, come ci si aspetta da un controllo
antiplagio). Exit code: 0 nessun match, 2 almeno un n-gramma di 8 parole
copiato verbatim (finding `high`), 1 errore d'uso o di lettura.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
NODES_DIR = ingest.NODES_DIR
TESTI_ESTRATTI_DIR = BASE + "FONTI/pipeline/testi estratti/"

N = 8
TOKEN_RE = re.compile(r"[A-Za-z0-9']+")


def tokenize(text):
    return TOKEN_RE.findall((text or "").lower())


def ngrams(tokens, n=N):
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def load_verbatim_for_node(node_id, excel_path=EXCEL_PATH):
    loaded = ingest.load_workbook_rows(excel_path)
    out = []
    for r in loaded["estratti"]:
        if ingest.clean(r.get("Nodo")) == node_id:
            v = ingest.clean(r.get("Citazione verbatim"))
            if v:
                out.append((ingest.clean(r.get("ID fonte")), v))
    return out


def load_whole_corpus(dirpath=TESTI_ESTRATTI_DIR):
    files = sorted(glob.glob(os.path.join(dirpath, "*")))
    out = []
    for path in files:
        if os.path.isdir(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                out.append((os.path.basename(path), f.read()))
        except OSError:
            continue
    return out


def find_matches(testo, corpora):
    """corpora: lista di (etichetta, testo_sorgente). Ritorna lista di
    finding {n_gramma, fonte}."""
    testo_ngrams = ngrams(tokenize(testo))
    if not testo_ngrams:
        return []
    findings = []
    for etichetta, sorgente in corpora:
        src_ngrams = ngrams(tokenize(sorgente))
        common = testo_ngrams & src_ngrams
        for ng in sorted(common):
            findings.append({"n_gramma": " ".join(ng), "fonte": etichetta})
    findings.sort(key=lambda f: (f["fonte"], f["n_gramma"]))
    return findings


def read_text_for_node(nodo):
    path = NODES_DIR + f"{nodo}.md"
    if not os.path.exists(path):
        raise SystemExit(f"nodes/{nodo}.md non trovato: passa --file o --text, oppure il testo in riga")
    content = open(path, encoding="utf-8").read()
    m = re.search(r"##\s*DRAFT\b[ \t]*\n(.*?)(?=\n?##\s*LEDGER|\Z)", content, re.S)
    testo = m.group(1).strip() if m else ""
    if testo.startswith("## LEDGER"):
        testo = ""
    return testo


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Lint antiplagio a n-grammi di 8 parole, per nodo (contro Citazione "
                     "verbatim di Estratti) o --whole (contro FONTI/pipeline/testi estratti/).")
    ap.add_argument("nodo", nargs="?", help="id del nodo (obbligatorio se non --whole)")
    ap.add_argument("testo", nargs="*", help="testo da controllare (se assente, legge nodes/<id>.md)")
    ap.add_argument("--file", help="legge il testo da questo file")
    ap.add_argument("--text", help="testo da controllare, alternativa a --file/posizionale")
    ap.add_argument("--whole", action="store_true",
                     help="controlla contro tutti i file di FONTI/pipeline/testi estratti/ "
                          "invece che contro le sole Citazione verbatim del nodo")
    ap.add_argument("--excel", default=EXCEL_PATH)
    ap.add_argument("--testi-estratti-dir", default=TESTI_ESTRATTI_DIR)
    args = ap.parse_args(argv)

    try:
        if args.text:
            testo = args.text
        elif args.file:
            testo = open(args.file, encoding="utf-8").read()
        elif args.testo:
            testo = " ".join(args.testo)
        elif args.nodo:
            testo = read_text_for_node(args.nodo)
        else:
            raise SystemExit("serve un testo: nodo+testo, --file o --text")

        if args.whole:
            corpora = load_whole_corpus(args.testi_estratti_dir)
            if not corpora:
                raise SystemExit(f"nessun file trovato in {args.testi_estratti_dir!r}")
        else:
            if not args.nodo:
                raise SystemExit("modalita' per nodo: serve l'id del nodo (o usa --whole)")
            verbatims = load_verbatim_for_node(args.nodo, excel_path=args.excel)
            corpora = [(f"Estratti[{args.nodo}|{fid}]", v) for fid, v in verbatims]
            if not corpora:
                print(f"OK: nessuna 'Citazione verbatim' registrata per il nodo {args.nodo}, "
                      "niente da controllare.")
                sys.exit(0)

        findings = find_matches(testo, corpora)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)

    if not findings:
        print(f"OK: nessun n-gramma di {N} parole copiato verbatim.")
        sys.exit(0)
    for f in findings:
        print(f"[HIGH] copiato verbatim da {f['fonte']}: “{f['n_gramma']}”")
    print(f"\n{len(findings)} n-grammi copiati verbatim. Parafrasa prima di chiudere il nodo.")
    sys.exit(2)


if __name__ == "__main__":
    main()
