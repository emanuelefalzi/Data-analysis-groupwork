#!/usr/bin/env python3
"""piano.py — legge input/piano.md (pagine per sezione, piano dei floats) e stima il budget.

    python3 tools/piano.py            # stampa il budget di pagine e i problemi

Il piano e' una proposta finche' il gruppo non lo approva: lo script non decide nulla,
dice solo se i numeri tornano con il limite di `pagine_corpo_max`.
"""
from __future__ import annotations

import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from comune import cfg, p, die  # noqa: E402


def _tabella(testo: str, titolo: str) -> list[dict]:
    m = re.search(rf"^## {re.escape(titolo)}\s*\n(.*?)(?=^## |\Z)", testo, re.S | re.M)
    if not m:
        die(f"piano.md: manca la sezione '## {titolo}'")
    righe = [r.strip() for r in m.group(1).splitlines() if r.strip().startswith("|")]
    if len(righe) < 3:
        return []
    cols = [c.strip() for c in righe[0].strip("|").split("|")]
    out = []
    for r in righe[2:]:
        celle = [c.strip() for c in r.strip("|").split("|")]
        celle += [""] * (len(cols) - len(celle))
        out.append(dict(zip(cols, celle)))
    return out


def leggi_piano() -> dict:
    path = p("piano")
    if not path.exists():
        die(f"piano non trovato: {path}")
    testo = path.read_text(encoding="utf-8")
    sezioni = {}
    for r in _tabella(testo, "Sezioni"):
        try:
            sezioni[r["id"]] = {"pagine": float(r["pagine"]), "note": r.get("note", "")}
        except ValueError:
            die(f"piano.md: pagine non numeriche per la sezione {r['id']}")
    floats = []
    for r in _tabella(testo, "Floats"):
        r["altezza"] = float(r["altezza"] or 0)
        floats.append(r)
    return {"sezioni": sezioni, "floats": floats}


def spazio_floats(floats: list[dict], sid: str) -> float:
    """Spazio dei floats `corpo` di una sezione; una coppia affiancata conta come una riga."""
    tot, coppie = 0.0, {}
    for f in floats:
        if f["dove"] != "corpo" or f["sezione"] != sid:
            continue
        if f.get("affianca"):
            coppie.setdefault(f["affianca"], []).append(f["altezza"])
        else:
            tot += f["altezza"]
    for alt in coppie.values():
        tot += max(alt)          # le figure affiancate stanno in una riga sola
    return tot


def budget(piano: dict) -> dict:
    c = cfg()
    wpp = c["parole_per_pagina"]
    out = {}
    for sid, s in piano["sezioni"].items():
        fl = spazio_floats(piano["floats"], sid)
        parole = max(0, round((s["pagine"] - fl) * wpp / 10) * 10)
        out[sid] = {"pagine": s["pagine"], "floats": round(fl, 2), "parole": parole}
    return out


def main():
    piano = leggi_piano()
    b = budget(piano)
    c = cfg()
    tot = sum(x["pagine"] for x in b.values())
    fl = sum(x["floats"] for x in b.values())
    par = sum(x["parole"] for x in b.values())
    print(f"{'id':<9}{'pagine':>7}{'floats':>8}{'parole':>8}")
    for sid, x in b.items():
        flag = "  ⚠ floats > pagine" if x["floats"] > x["pagine"] else ""
        print(f"{sid:<9}{x['pagine']:>7.2f}{x['floats']:>8.2f}{x['parole']:>8}{flag}")
    print(f"\nTotale corpo: {tot:.2f} pagine (max {c['pagine_corpo_max']}), floats {fl:.2f}, "
          f"prosa {par} parole a {c['parole_per_pagina']}/pagina")
    if tot > c["pagine_corpo_max"]:
        print(f"⚠ Il piano supera il limite di {tot - c['pagine_corpo_max']:.2f} pagine.")
    sez_senza = sorted({f["sezione"] for f in piano["floats"] if f["dove"] == "corpo"} - set(b))
    if sez_senza:
        print(f"⚠ Floats assegnati a sezioni assenti dal piano: {', '.join(sez_senza)}")


if __name__ == "__main__":
    main()
