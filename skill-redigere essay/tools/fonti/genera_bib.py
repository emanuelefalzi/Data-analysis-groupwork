#!/usr/bin/env python3
"""Genera le voci mancanti di `fonti/fonti.bib` a partire da `input/fonti.csv`.

La bibliografia finale si genera SEMPRE da `fonti.bib`, mai a mano (regola della
tesi). Questo script fa solo la prima stesura delle voci: titolo, sede e DOI
arrivano dalle API del loop 1, gli autori dal CSV. Le voci gia' presenti nel
.bib non vengono mai toccate: se ne correggi una a mano, resta corretta.

Quello che le API non danno (volume, numero, pagine, editore, nomi completi
degli autori) NON viene inventato: la voce esce incompleta e lo script lo dice.
`tools/word/cita.py` rende comunque la voce con i campi che ci sono.

Formato atteso per `autori` nel CSV: «Cognome, N.; Cognome, N.» oppure
«Cognome N. and Cognome N.»; con un solo cognome va bene uguale.

Uso:
    python3 tools/fonti/genera_bib.py           # dry-run: mostra cosa aggiungerebbe
    python3 tools/fonti/genera_bib.py --commit
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402
from lib.csvio import FontiCSV  # noqa: E402
from bib import leggi_bib  # noqa: E402


def autori_bib(s: str) -> str:
    parti = [p.strip() for p in re.split(r";| and | & ", s or "") if p.strip()]
    return " and ".join(parti)


def tipo_bib(tipo: str) -> str:
    t = (tipo or "").lower()
    if "book-chapter" in t or "chapter" in t:
        return "incollection"
    if t in ("book", "monograph") or "book" in t:
        return "book"
    if "proceedings" in t:
        return "inproceedings"
    if any(k in t for k in ("posted-content", "preprint", "report", "working")):
        return "techreport"
    if "web" in t or "sito" in t:
        return "online"
    return "article"


def voce(r: dict) -> tuple[str, list[str]]:
    tipo = tipo_bib(r.get("tipo"))
    campi = {
        "author": autori_bib(r.get("autori")),
        "year": r.get("anno"),
        "title": r.get("titolo"),
        ("journal" if tipo == "article" else "booktitle" if tipo in ("incollection", "inproceedings")
         else "institution" if tipo == "techreport" else "publisher"): r.get("sede"),
        "doi": r.get("doi"),
        "url": "" if r.get("doi") else r.get("url"),
    }
    mancano = [k for k in ("author", "year", "title") if not campi.get(k)]
    if tipo == "article":
        mancano += ["volume/number/pages (le API non li danno: completali a mano se servono)"]
    righe = [f"@{tipo}{{{r['id']},"]
    for k, v in campi.items():
        if v:
            righe.append(f"  {k} = {{{v}}},")
    righe.append("}")
    return "\n".join(righe), mancano


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args(argv)

    c = FontiCSV(comune.FONTI_CSV); c.open()
    gia = set(leggi_bib(comune.BIB).keys()) if comune.BIB.exists() else set()
    nuove = []
    for fid in c.all_ids():
        r = c.get(fid)
        if fid in gia or r.get("stato") in ("abbandonata", "non_trovata", "ambigua", "da_cercare"):
            continue
        testo, mancano = voce(r)
        nuove.append(testo)
        print(f"+ {fid}" + (f"   incompleta: {', '.join(mancano)}" if mancano else ""))
    if not nuove:
        print("Nessuna voce da aggiungere.")
        return 0
    if not a.commit:
        print(f"\n[dry-run] aggiungerei {len(nuove)} voci a {comune.rel(comune.BIB)}. Usa --commit.")
        return 0
    comune.BIB.parent.mkdir(parents=True, exist_ok=True)
    with open(comune.BIB, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n\n".join(nuove) + "\n")
    print(f"\nAggiunte {len(nuove)} voci a {comune.rel(comune.BIB)}. Rileggile: e' una prima stesura.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
