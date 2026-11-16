#!/usr/bin/env python3
"""comprimi.py — il piano di taglio, quando il documento supera il limite di pagine.

Non taglia niente: **calcola dove tagliare e quanto**, e stampa un piano che
l'orchestratore esegue dispacciando un `node-writer` per nodo. La decisione di
quanto togliere e' aritmetica; quella di cosa togliere resta a chi scrive, e
ogni affermazione che cade va dichiarata nel `LEDGER`.

## Come sceglie i nodi

Ordina per **eccedenza sul proprio target**, non per lunghezza assoluta. Un nodo
lungo che sta nella sua banda ha gia' la lunghezza che il materiale merita:
comprimerlo significherebbe togliere contenuto. Un nodo che sfora del 50% ha
prosa larga, e li' si stringe senza perdere nulla.

## Cosa esclude, e perche'

- **Il Cap. 5**: il tetto di 130 parole ha gia' selezionato una volta, e otto
  dei suoi nodi hanno perso piu' della meta' del materiale. Comprimerlo ancora
  vorrebbe dire tagliare due volte lo stesso capitolo.
- **I Cap. 0, 6 e 7**: stanno sotto la propria capienza, non c'e' margine.
- **I nodi sotto le 60 parole**: sono frasi singole, e stringere una frase
  singola la rompe.

Uso:
    /usr/bin/python3 tools/comprimi.py --pagine-attuali 52 --limite 50
    /usr/bin/python3 tools/comprimi.py --parole 700     # taglio diretto
"""

import argparse
import json
import os
import re
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
sys.path.insert(0, BASE + "tools")
from lint_citazioni import draft_of          # noqa: E402
import gap                                    # noqa: E402

PAROLE_PER_PAGINA = 350
CAPITOLI_COMPRIMIBILI = ["1", "2", "3", "4"]
MINIMO_PAROLE = 60          # sotto questa soglia un nodo e' una frase sola
QUOTA_MASSIMA = 0.20        # a nessun nodo si chiede piu' del 20% delle sue parole


def parole(testo):
    return len(re.sub(r"(\w)[—–]+(\w)", r"\1 \2", testo).split())


def candidati():
    nodes = json.load(open(BASE + "build/nodes.json", encoding="utf-8"))["nodes"]
    bud = gap.load_budget_pp()
    out = []
    for c in CAPITOLI_COMPRIMIBILI:
        cm = gap.chapter_metrics(nodes, c, bud)
        if not cm or not cm.get("k_c"):
            continue
        targets, _ = gap.derive_targets_for_chapter(nodes, c, cm["k_c"])
        for nid, v in targets.items():
            p = f"{BASE}nodes/{nid}.md"
            if not os.path.exists(p):
                continue
            w = parole(draft_of(p))
            tw = v["target_words"]
            if w < MINIMO_PAROLE or not tw or w <= tw:
                continue
            out.append({"nodo": nid, "scritte": w, "target": tw,
                        "eccedenza": w - tw, "tetto": int(w * QUOTA_MASSIMA)})
    out.sort(key=lambda r: r["eccedenza"], reverse=True)
    return out


def piano(da_tagliare):
    """Distribuisce il taglio sui nodi piu' eccedenti, senza superare il tetto."""
    scelti, resto = [], da_tagliare
    for r in candidati():
        if resto <= 0:
            break
        quota = min(r["eccedenza"], r["tetto"], resto)
        if quota < 5:            # sotto le cinque parole non vale un giro d'agente
            continue
        scelti.append(dict(r, taglia=quota))
        resto -= quota
    return scelti, resto


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagine-attuali", type=float)
    ap.add_argument("--limite", type=float, default=50.0)
    ap.add_argument("--parole", type=int, help="taglio in parole, invece che in pagine")
    a = ap.parse_args()

    if a.parole:
        da_tagliare = a.parole
        motivo = f"{a.parole} parole richieste"
    elif a.pagine_attuali:
        # un margine di mezza pagina: rientrare esatti sulla soglia e' fragile
        da_tagliare = int((a.pagine_attuali - a.limite + 0.5) * PAROLE_PER_PAGINA)
        motivo = (f"{a.pagine_attuali} pagine contro un limite di {a.limite}, "
                  f"piu' mezza pagina di margine")
    else:
        ap.error("serve --pagine-attuali oppure --parole")

    if da_tagliare <= 0:
        print("Nessun taglio necessario.")
        return 0

    scelti, resto = piano(da_tagliare)
    print(f"PIANO DI COMPRESSIONE — {motivo}")
    print(f"da togliere: {da_tagliare} parole\n")
    print(f"{'nodo':10}{'scritte':>9}{'target':>8}{'eccede':>8}{'taglia':>8}   dopo")
    for r in scelti:
        print(f"{r['nodo']:10}{r['scritte']:>9}{r['target']:>8}"
              f"{r['eccedenza']:>8}{r['taglia']:>8}   {r['scritte'] - r['taglia']}")
    coperto = sum(r["taglia"] for r in scelti)
    print(f"\ncoperto: {coperto} parole su {da_tagliare} in {len(scelti)} nodi")
    if resto > 0:
        print(f"SCOPERTO: {resto} parole. I nodi comprimibili non bastano senza")
        print("toccare il Cap. 5 o togliere affermazioni: decisione dell'autore.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
