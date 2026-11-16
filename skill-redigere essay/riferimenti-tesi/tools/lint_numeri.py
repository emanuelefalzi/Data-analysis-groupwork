#!/usr/bin/env python3
"""lint_numeri.py — ogni cifra, percentuale, data, importo e nome proprio del
DRAFT deve comparire *verbatim* nella whitelist (§4.7). La whitelist e'
l'unione di tutti i `source_desc` in perimetro + `Fonti` + `Estratti`.

Due livelli, non uno:
- se il candidato non compare da NESSUNA parte nella whitelist -> finding
  `high` (bloccante): e' un dato/nome inventato.
- se compare nella whitelist ma non nel `source_desc` del nodo o di un suo
  antenato -> solo un avviso: e' legittimo (es. termini ripresi nel Cap. 6
  per deduzione dai Cap. 1-4), ma va riletto.

Uso:
    /usr/bin/python3 tools/lint_numeri.py 4.2.1 "testo del paragrafo..."
    /usr/bin/python3 tools/lint_numeri.py 4.2.1 --file draft.txt
    /usr/bin/python3 tools/lint_numeri.py --help

Exit code: 0 nessun rilievo, 2 almeno un finding `high` (bloccante),
1 errore d'uso o di lettura.

Nota sull'estrazione dei "nomi propri": e' un'euristica su maiuscole di
inizio-parola fuori inizio-frase, non un NER vero — non ci sono librerie di
NLP fra i prerequisiti dichiarati (§9). Falsi negativi/positivi sono
possibili e vanno letti come tali, non come verdetto definitivo.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
BUILD_DIR = ingest.BUILD_DIR
NODES_DIR = ingest.NODES_DIR

# --------------------------------------------------------------------------
# estrazione candidati
# --------------------------------------------------------------------------

NUM_RE = re.compile(r"\b\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?\b|\b\d+(?:[.,]\d+)?\b")
PERCENT_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s?%")
MONEY_RE = re.compile(r"[$€£]\s?\d+(?:[.,]\d+)*|\b\d+(?:[.,]\d+)*\s?(?:USD|EUR|GBP|dollars?|euros?)\b", re.I)
DATE_ISO_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December")
DATE_TEXT_RE = re.compile(rf"\b(?:{MONTHS})\s+\d{{1,2}},?\s+\d{{4}}\b|\b\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}\b")

# Vocabolario strutturale del documento: non sono mai dati fabbricati, e la
# convenzione AG-04 autorizza esplicitamente "Chapter N" nel primo e nell'ultimo
# capoverso di ogni capitolo. Vanno esclusi dai "nomi propri".
STRUCTURAL_WORDS = {
    "chapter", "chapters", "section", "sections", "table", "tables",
    "figure", "figures", "appendix", "part", "thesis",
}

SENTENCE_STOP_STARTERS = {
    "the", "this", "these", "those", "it", "in", "on", "as", "when", "if",
    "however", "moreover", "therefore", "thus", "since", "while", "although",
    "given", "because", "a", "an", "such", "for", "with", "over", "under",
    "each", "both", "one", "two", "three", "four", "five", "many", "most",
    "some", "unlike", "beyond", "within", "across", "despite", "before",
    "after", "during", "once", "here", "there", "what", "which", "who",
}



# I token `[[...]]` non sono prosa: `[[CIT-N:akerlof1970]]` diventera' una
# citazione autore-data in assemblaggio, `[[GAP: ...]]` e `[[CIT-NEEDED: ...]]`
# spariscono del tutto. Contarli o analizzarli produce falsi rilievi: il testo
# dentro un token e' una nota all'autore, non un'affermazione della tesi.
# Un `[[CIT-N:x]]` lascia al suo posto un segnaposto di due parole, che e' la
# lunghezza media di una citazione parentetica APA resa in prosa.
TOKEN_RE = re.compile(r"\[\[([A-Z-]+)(?::[^\]]*)?\]\]")


def strip_tokens(testo):
    """Toglie i token `[[...]]` dal testo prima di analizzarlo.

    Qui i token spariscono del tutto, segnaposto compresi: questo lint cerca
    numeri e nomi propri fabbricati, e qualunque segnaposto capitalizzato
    ("Author Year") verrebbe scambiato per un nome proprio inventato. La
    lunghezza non conta in questo lint, quindi non serve rimpiazzare nulla.
    """
    out = TOKEN_RE.sub("", testo or "")
    return re.sub(r"\s{2,}", " ", out).strip()

def extract_numbers_dates_money(text):
    out = set()
    for rx in (DATE_ISO_RE, DATE_TEXT_RE, MONEY_RE, PERCENT_RE, NUM_RE):
        for m in rx.finditer(text or ""):
            out.add(m.group(0))
    return out


def extract_proper_nouns(text):
    """Sequenze di 1+ parole capitalizzate, escluse quelle a inizio frase
    quando la prima parola e' un termine funzionale comune (euristica, non
    NER: §9 non elenca librerie NLP fra i prerequisiti)."""
    text = text or ""
    out = set()
    # spezza in "frasi" grezze sulla punteggiatura forte
    for sent in re.split(r"(?<=[.!?])\s+", text):
        words = sent.split()
        i = 0
        while i < len(words):
            w = re.sub(r"^[^\w]+|[^\w]+$", "", words[i])
            if w and w[0:1].isupper() and w[1:].islower() or (w.isupper() and len(w) > 1):
                is_sentence_start = (i == 0)
                # estende alla sequenza di capitalizzate consecutive
                j = i
                seq = [w]
                while j + 1 < len(words):
                    w2 = re.sub(r"^[^\w]+|[^\w]+$", "", words[j + 1])
                    if w2 and (w2[0:1].isupper() and w2[1:].islower() or (w2.isupper() and len(w2) > 1)):
                        seq.append(w2)
                        j += 1
                    else:
                        break
                candidate = " ".join(seq)
                # Una parola capitalizzata a inizio frase non e' di per se' un
                # nome proprio: in inglese ogni frase comincia in maiuscolo.
                # Vale solo se apre una sequenza di piu' capitalizzate
                # ("Generative AI") o se la stessa parola compare capitalizzata
                # anche a meta' frase altrove nel testo. La vecchia regola
                # scartava solo i 40 termini di SENTENCE_STOP_STARTERS e
                # marcava HIGH parole comuni come "Transposed" o "Chapter",
                # bloccando il nodo su un falso positivo.
                if is_sentence_start:
                    # La prima parola di una frase e' maiuscola per posizione,
                    # non perche' sia un nome proprio: si scarta sempre, e si
                    # valuta solo cio' che la segue ("With AI" -> "AI").
                    seq = seq[1:]
                    if not seq:
                        i = j + 1
                        continue
                    candidate = " ".join(seq)
                if candidate.lower() in STRUCTURAL_WORDS:
                    i = j + 1
                    continue
                if len(candidate) > 1:
                    out.add(candidate)
                i = j + 1
            else:
                i += 1
    return out


def extract_candidates(text):
    return extract_numbers_dates_money(text) | extract_proper_nouns(text)


# --------------------------------------------------------------------------
# whitelist
# --------------------------------------------------------------------------

def load_whitelist_corpus(excel_path=EXCEL_PATH):
    """Ritorna (corpus_globale: str, source_desc_by_id: dict, parent_by_id: dict).
    Il corpus globale e' la concatenazione di tutti i source_desc in
    perimetro piu' i campi testuali di Fonti ed Estratti."""
    nodes_json_path = BUILD_DIR + "nodes.json"
    if os.path.exists(nodes_json_path):
        with open(nodes_json_path, encoding="utf-8") as f:
            nodes = json.load(f)["nodes"]
    else:
        loaded = ingest.load_workbook_rows(excel_path)
        nodes, _ = ingest.build_nodes(loaded)

    source_desc_by_id = {nid: n["source_desc"] for nid, n in nodes.items()}
    parent_by_id = {nid: n["parent"] for nid, n in nodes.items()}

    parts = [n["source_desc"] for n in nodes.values() if n["perimetro"] and n["source_desc"]]

    # Anche `FONTI/tesi.bib`, e non e' un di piu': dopo che
    # `bibliography-builder` ha risolto i token, il testo porta i nomi degli
    # autori, e quelli di una fonte ammessa per override dell'autore non stanno
    # nell'Excel congelato. Senza questo, un cognome legittimo esce come
    # finding `high` -- «dato fabbricato» -- su una fonte che l'autore ha
    # deciso di usare. E' successo con Holmstrom, e prima con Tabassi.
    bib = BASE + "FONTI/tesi.bib"
    if os.path.exists(bib):
        parts.append(open(bib, encoding="utf-8").read())
    # e la reference list gia' resa: il bib scrive i diacritici in notazione
    # LaTeX (`Holmstr\"om`), il testo li porta veri (`Holmstrom` con la
    # dieresi). Confrontare col solo bib fa fallire proprio i nomi accentati.
    biblio = BASE + "build/bibliography.md"
    if os.path.exists(biblio):
        parts.append(open(biblio, encoding="utf-8").read())

    loaded = ingest.load_workbook_rows(excel_path)
    for r in loaded["fonti"]:
        for col in ("Citazione", "Autori", "Titolo", "Sede / editore", "Cosa dice davvero", "Note"):
            v = ingest.clean(r.get(col))
            if v:
                parts.append(v)
    for r in loaded["estratti"]:
        for col in ("Citazione", "Claim da verificare", "Cosa dice davvero",
                     "Citazione verbatim", "Sezione", "Note", "Risoluzione (decisione autore)"):
            v = ingest.clean(r.get(col))
            if v:
                parts.append(v)

    corpus = "\n".join(parts)
    return corpus, source_desc_by_id, parent_by_id


def local_corpus(node_id, source_desc_by_id, parent_by_id):
    """source_desc del nodo e di tutti i suoi antenati."""
    parts = []
    cur = node_id
    seen = set()
    while cur and cur not in seen:
        seen.add(cur)
        d = source_desc_by_id.get(cur)
        if d:
            parts.append(d)
        cur = parent_by_id.get(cur)
    return "\n".join(parts)


# --------------------------------------------------------------------------
# lint
# --------------------------------------------------------------------------

def lint_numeri(testo, nodo, excel_path=EXCEL_PATH):
    corpus, source_desc_by_id, parent_by_id = load_whitelist_corpus(excel_path)
    loc = local_corpus(nodo, source_desc_by_id, parent_by_id)
    candidati = extract_candidates(testo)

    findings = []
    for c in sorted(candidati):
        if c in corpus:
            if c not in loc:
                findings.append({
                    "gravita": "avviso", "termine": c,
                    "motivo": "compare nella whitelist (Fonti/Estratti/altro nodo) ma non nel "
                              "source_desc di questo nodo o di un suo antenato: verifica che sia "
                              "legittimo qui (es. ripresa per deduzione)."
                })
        else:
            # Una sequenza di piu' parole capitalizzate puo' essere l'accostamento
            # casuale di due termini entrambi legittimi ("SME ELFO"): l'euristica
            # di estrazione li incolla, ma non e' un nome fabbricato. Si scende a
            # livello di parola e si segnala solo cio' che manca davvero.
            parole = c.split()
            if len(parole) > 1:
                ignote = [w for w in parole if w not in corpus]
                if not ignote:
                    continue
                for w in ignote:
                    findings.append({
                        "gravita": "high", "termine": w,
                        "motivo": "non compare verbatim in nessun source_desc in perimetro, ne' in "
                                  "Fonti o Estratti: possibile dato/nome fabbricato "
                                  f"(trovato nella sequenza \"{c}\")."
                    })
                continue
            findings.append({
                "gravita": "high", "termine": c,
                "motivo": "non compare verbatim in nessun source_desc in perimetro, ne' in "
                          "Fonti o Estratti: possibile dato/nome fabbricato."
            })
    findings.sort(key=lambda f: (0 if f["gravita"] == "high" else 1, f["termine"].lower()))
    return findings


def blocca(findings):
    return any(f["gravita"] == "high" for f in findings)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def read_text_for_node(nodo):
    path = NODES_DIR + f"{nodo}.md"
    if not os.path.exists(path):
        raise SystemExit(f"nodes/{nodo}.md non trovato: passa --file o --text, oppure il testo in riga")
    content = open(path, encoding="utf-8").read()
    m = re.search(r"##\s*DRAFT\b[ \t]*\n(.*?)(?=\n?##\s*LEDGER|\Z)", content, re.S)
    testo = m.group(1).strip() if m else ""
    if testo.startswith("## LEDGER"):
        testo = ""
    return strip_tokens(testo)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Lint numeri/date/importi/nomi propri del DRAFT contro la whitelist "
                     "(union di source_desc in perimetro + Fonti + Estratti).")
    ap.add_argument("nodo", help="id del nodo (es. 4.2.1)")
    ap.add_argument("testo", nargs="*", help="testo da lintare (se assente, legge nodes/<id>.md)")
    ap.add_argument("--file", help="legge il testo da questo file invece che da nodes/<id>.md")
    ap.add_argument("--text", help="testo da lintare, alternativa a --file/posizionale")
    ap.add_argument("--excel", default=EXCEL_PATH)
    args = ap.parse_args(argv)

    try:
        if args.text:
            testo = args.text
        elif args.file:
            testo = open(args.file, encoding="utf-8").read()
        elif args.testo:
            testo = " ".join(args.testo)
        else:
            testo = read_text_for_node(args.nodo)

        findings = lint_numeri(testo, args.nodo, excel_path=args.excel)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)

    if not findings:
        print("OK: nessun rilievo.")
        sys.exit(0)
    for f in findings:
        print(f"[{f['gravita'].upper()}] «{f['termine']}»\n    {f['motivo']}")
    print(f"\n{len(findings)} rilievi.")
    if blocca(findings):
        print("BLOCCATO: risolvi i finding HIGH prima di chiudere il nodo.")
        sys.exit(2)
    print("Solo avvisi: puoi procedere, ma leggili.")
    sys.exit(0)


if __name__ == "__main__":
    main()
