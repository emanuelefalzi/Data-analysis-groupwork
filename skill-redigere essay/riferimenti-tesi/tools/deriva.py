#!/usr/bin/env python3
"""Quanto ha scritto ogni capitolo contro la sua capienza.

I lint controllano la banda del singolo nodo, ma la banda si deriva dalla
lunghezza del materiale e la prosa scritta corre sistematicamente piu' lunga:
attribuzioni, claim composti spezzati in periodi separati, transizioni. Il
singolo nodo sfora in su o in giu' e **al livello di capitolo si compensa** --
il Cap. 3, finito, e' uscito a 1.225 parole contro 1.220 di capienza.

Quello che va guardato e' quindi la deriva del capitolo, non la banda del nodo.
"""
import json, os, re, sys
B = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura"
sys.path.insert(0, os.path.join(B, "tools"))
import gap, lint_citazioni as L

nodes, _ = gap.load_nodes()
bud = gap.load_budget_pp()
d = json.load(open(os.path.join(B, "build", "nodes.json"), encoding="utf8"))["nodes"]

print(f"{'Cap':4}{'nodi':>6}{'scritti':>8}{'materiale':>11}{'scritto':>9}{'capienza':>10}{'uso':>7}")
tw = tc = 0
for c in ["0", "1", "2", "3", "4", "5", "6", "7"]:
    ks = [k for k in d if d[k]["chapter"] == c and d[k]["source_words"] > 0]
    w = 0
    for k in ks:
        t = L.draft_of(os.path.join(B, "nodes", f"{k}.md"))
        if t:
            w += len(re.sub(r"\[\[[^\]]*\]\]", "", t).split())
    m = gap.chapter_metrics(nodes, c, bud)
    cap = m["capacita_parole_C_c"] or 0
    # Il campo `stato` di nodes.json viene dall'Excel e ingest.py lo rigenera:
    # dopo ogni ingest torna "vuoto" su TUTTI i nodi, compresi quelli che hanno
    # un DRAFT su disco. Contarlo dava zero nodi scritti su una tesi scritta a
    # meta'. L'unica verita' su cosa e' scritto e' il file.
    scritti = sum(1 for k in ks
                  if L.draft_of(os.path.join(B, "nodes", f"{k}.md")).strip())
    pct = f"{100*w/cap:.0f}%" if cap else "-"
    print(f"{c:4}{len(ks):>6}{scritti:>8}{m['materiale_parole_M_c']:>11}{w:>9}{cap:>10.0f}{pct:>7}")
    tw += w; tc += cap
print(f"{'TOT':4}{'':6}{'':8}{'':11}{tw:>9}{tc:>10.0f}{100*tw/tc:>6.0f}%")
