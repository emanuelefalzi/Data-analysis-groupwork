#!/usr/bin/env python3
"""lint_budget.py — parole scritte contro la CAPACITA' del nodo, non contro
un pavimento: il pavimento non esiste piu' (§4.1, §4.7).

`target_words` non e' ricalcolato qui da zero: importa le stesse funzioni di
`gap.py` (la derivazione a cinque passi di §4.1 vive in un solo posto), cosi'
i due script non possono divergere silenziosamente.

Regola (§4.1): **target_words ±15%, nessun pavimento, in nessun caso.** Un
nodo sotto la banda si dichiara corto e va all'autore, non si allunga con
materiale non presente nella Descrizione: qui e' solo un finding, la
decisione resta a chi legge il report.

Uso:
    /usr/bin/python3 tools/lint_budget.py 4.2.1 "testo del paragrafo..."
    /usr/bin/python3 tools/lint_budget.py 4.2.1 --file draft.txt
    /usr/bin/python3 tools/lint_budget.py --help

Exit code: 0 dentro banda, 2 fuori banda (finding, non bloccante di per se':
la gravita' la legge chi chiama lo script), 1 errore d'uso.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gap  # noqa: E402
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
NODES_DIR = ingest.NODES_DIR

BANDA = 0.15



# I token `[[...]]` non sono prosa: `[[CIT-N:akerlof1970]]` diventera' una
# citazione autore-data in assemblaggio, `[[GAP: ...]]` e `[[CIT-NEEDED: ...]]`
# spariscono del tutto. Contarli o analizzarli produce falsi rilievi: il testo
# dentro un token e' una nota all'autore, non un'affermazione della tesi.
# Un `[[CIT-N:x]]` lascia al suo posto un segnaposto di due parole, che e' la
# lunghezza media di una citazione parentetica APA resa in prosa.
TOKEN_RE = re.compile(r"\[\[([A-Z-]+)(?::[^\]]*)?\]\]")


def strip_tokens(testo):
    """Toglie i token `[[...]]` dal testo prima di contarlo.

    Qui conta la lunghezza, non il contenuto: `[[CIT-N:akerlof1970]]` lascia un
    segnaposto di due parole, che e' quanto occupa una citazione autore-data
    resa in prosa; `[[GAP: ...]]` e `[[CIT-NEEDED: ...]]` spariscono, perche' in
    assemblaggio non lasciano niente.
    """
    def sub(m):
        return "Autore Anno" if m.group(1) in ("CIT-N", "CIT-P") else ""
    out = TOKEN_RE.sub(sub, testo or "")
    return re.sub(r"\s{2,}", " ", out).strip()

def target_words_for_node(node_id, excel_path=EXCEL_PATH, force_excel=False):
    """Ricava target_words per un nodo rigirando la sola derivazione del suo
    capitolo (gap.py), senza scrivere ne' leggere reports/gap.md."""
    nodes, _ = gap.load_nodes(excel_path=excel_path, force_excel=force_excel)
    node = nodes.get(node_id)
    if node is None:
        raise SystemExit(f"nodo {node_id!r} non trovato")
    if node["source_words"] == 0:
        return 0, "⚠ RICHIESTA AUTORE — Descrizione vuota, il nodo non va scritto"
    chapter = node["chapter"]
    budget_pp_map = gap.load_budget_pp(excel_path)
    cm = gap.chapter_metrics(nodes, chapter, budget_pp_map)
    if cm["k_c"] is None:
        raise SystemExit(f"capitolo {chapter}: budget_pp o materiale mancante, target non derivabile")
    targets, _ = gap.derive_targets_for_chapter(nodes, chapter, cm["k_c"])
    v = targets.get(node_id)
    if v is None:
        raise SystemExit(f"nodo {node_id!r}: derivazione non disponibile (bug o nodo senza testo)")
    nota = v["nota"]
    # I due estremi di k_c non sono simmetrici e non vanno trattati uguale.
    # SOTTO il pavimento il budget non basta per il materiale: quali
    # affermazioni cadono e' una decisione dell'autore, e li' si blocca.
    # SOPRA il tetto avanza capienza: nessun nodo e' in difficolta', i target
    # sono gia' clippati e scrivibili, e riempire l'avanzo vorrebbe dire
    # aggiungere affermazioni che nel materiale non ci sono -- cioe' violare la
    # regola sovrana per far quadrare un numero. Il capitolo esce piu' corto del
    # budget: e' un fatto da riportare, non un blocco.
    # (Il messaggio simmetrico aveva gia' fatto credere al writer di `6.3` che
    # `6.4` fosse bloccato, quando non lo era.)
    if cm["k_c"] < gap.CLIP_LOW:
        nota = (nota + " · " if nota else "") + f"capitolo {chapter} BLOCCATO IN COMPRESSIONE (k_c={cm['k_c']}): non scrivere finche' l'autore non decide quali affermazioni cadono"
    elif cm["k_c"] > gap.CLIP_HIGH:
        nota = (nota + " · " if nota else "") + f"capitolo {chapter} ha capienza in avanzo (k_c={cm['k_c']}): rendi tutto il materiale e dichiara lo scarto sotto banda, non allungare"
    return v["target_words"], nota


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


def lint_budget(node_id, testo, excel_path=EXCEL_PATH, force_excel=False):
    target, nota = target_words_for_node(node_id, excel_path=excel_path, force_excel=force_excel)
    # `split()` spezza sugli spazi, quindi due parole unite da un trattino lungo
    # senza spazi -- «and—as», «argues—consistent» -- valgono UNA parola sola. Non
    # e' teoria: un writer se n'e' accorto, ha visto il conteggio scendere da 18 a
    # 16, ha concluso di essere rientrato in banda e ha tolto la dichiarazione di
    # fuori banda. Il testo non era cambiato, era cambiata la misura.
    # Il trattino lungo CON spazi non ha questo problema ed e' punteggiatura
    # legittima: non si tocca qui (semmai lo guarda il prose-auditor, perche'
    # abusarne e' un marcatore di testo generato).
    scritte = len(re.sub(r"(\w)[—–]+(\w)", r"\1 \2", testo or "").split())
    if target == 0:
        return {
            "target_words": 0, "parole_scritte": scritte, "esito": "n/a",
            "nota": nota,
        }
    lo, hi = target * (1 - BANDA), target * (1 + BANDA)
    dentro = lo <= scritte <= hi
    return {
        "target_words": target, "banda": (round(lo), round(hi)),
        "parole_scritte": scritte, "esito": "OK" if dentro else "FUORI BANDA",
        "nota": nota,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Lint budget: parole del DRAFT contro target_words ±15% (§4.1), "
                     "nessun pavimento. Riusa la derivazione di gap.py.")
    ap.add_argument("nodo", help="id del nodo (es. 4.2.1)")
    ap.add_argument("testo", nargs="*", help="testo da contare (se assente, legge nodes/<id>.md)")
    ap.add_argument("--file", help="legge il testo da questo file invece che da nodes/<id>.md")
    ap.add_argument("--text", help="testo da contare, alternativa a --file/posizionale")
    ap.add_argument("--excel", default=EXCEL_PATH)
    ap.add_argument("--from-excel", action="store_true",
                     help="ignora build/nodes.json, ricalcola dall'Excel (sola lettura)")
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

        r = lint_budget(args.nodo, testo, excel_path=args.excel, force_excel=args.from_excel)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"target_words: {r['target_words']}" + (f"  banda ±15%: {r['banda']}" if "banda" in r else ""))
    print(f"parole scritte: {r['parole_scritte']}")
    print(f"esito: {r['esito']}")
    if r["nota"]:
        print(f"nota: {r['nota']}")
    if r["esito"] == "FUORI BANDA":
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
