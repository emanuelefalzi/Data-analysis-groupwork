#!/usr/bin/env python3
"""Linter terminologico — il glossario non serve a essere letto, serve a essere applicato.

Dato il testo di una sezione e il suo id, restituisce:
  - BLOCCA  forma_vietata          una forma che l'essay non usa mai (classe `forma_errata`)
  - BLOCCA  uso_prima_definizione  termine tecnico usato prima della sezione che lo definisce
  - AVVISA  termini_vicini         due termini legittimi ma distinti nello stesso paragrafo
  - AVVISA  termine_non_definito   l'essay lo usa ma non lo definisce da nessuna parte

Ripreso dal linter della tesi, con la patch che li' era arrivata dopo (AG-07): il
glossario stesso puo' dichiarare un'anticipazione legittima, su tutte le sezioni
(`usabile_prima_della_definizione`) o su un elenco (`anticipazioni_legittime`).
L'ordine delle sezioni viene dalla scaletta, non dal numero dell'id. La prima
sezione (introduzione) puo' sempre anticipare un termine.

Uso:
    python3 tools/glossario/lint.py 2.1 "testo del paragrafo..."
    python3 tools/glossario/lint.py 2.1 --file paragrafo.txt
    python3 tools/glossario/lint.py --autotest     # un glossario sano non blocca le proprie definizioni
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

GRAVITA = {"blocca": 2, "avvisa": 1}


@dataclass
class Violazione:
    gravita: str
    tipo: str
    termine: str
    usa_invece: str
    perche: str
    sezione_definizione: str

    def __str__(self):
        freccia = f"  ->  usa «{self.usa_invece}»" if self.usa_invece else ""
        return f"[{self.gravita.upper()}] «{self.termine}»{freccia}\n    {self.perche}"


def _ordine() -> dict:
    try:
        return {sid: i for i, sid in enumerate(comune.sezioni())}
    except SystemExit:
        return {}


def _prima_di(uso: str, defi: str, ordine: dict) -> bool:
    if not defi or uso not in ordine or defi not in ordine:
        return False
    return ordine[uso] < ordine[defi]


def _anticipazione_ammessa(uso: str, defi: str, voce: dict, ordine: dict) -> bool:
    if ordine and ordine.get(uso) == 0:
        return True                       # l'introduzione annuncia, poi si definisce
    if defi.startswith(uso + "."):
        return True                       # il cappello della sezione che contiene la definizione
    if voce.get("usabile_prima_della_definizione"):
        return True
    return any(uso == a or uso.startswith(str(a) + ".") for a in voce.get("anticipazioni_legittime", []) or [])


def _compila(voci):
    reg = []
    for v in voci:
        can = (v.get("forma_canonica") or "").strip()
        if not can:
            continue
        for var in v.get("varianti_vietate", []):
            forma = (var.get("forma") or "").strip()
            if not forma or forma.lower() == can.lower():
                continue
            # forma_errata: mai usata nell'essay, usarla e' un errore -> BLOCCA
            # vicino_confondibile: termine legittimo con significato distinto -> RICORDA
            tipo = "variante" if var.get("classe") == "forma_errata" else "vicino"
            reg.append((tipo, re.compile(rf"\b{re.escape(forma)}\b", re.I), forma, can, var.get("perche", ""), v))
        reg.append(("canonico", re.compile(rf"\b{re.escape(can)}\b", re.I), can, can, "", v))
    return reg


_CACHE: dict = {}


def carica(percorso=comune.GLOSSARIO):
    if percorso not in _CACHE:
        if not Path(percorso).exists():
            _CACHE[percorso] = ([], [])
        else:
            d = json.loads(Path(percorso).read_text(encoding="utf-8"))
            _CACHE[percorso] = (d["voci"], _compila(d["voci"]))
    return _CACHE[percorso]


def lint(testo: str, sezione: str, percorso=comune.GLOSSARIO) -> list[Violazione]:
    voci, reg = carica(percorso)
    ordine = _ordine()
    viste, out = set(), []
    for tipo, rx, forma, can, perche, voce in reg:
        if not rx.search(testo or ""):
            continue
        defi = voce.get("sezione_definizione", "") or ""
        if tipo == "variante":
            k = ("v", forma.lower())
            if k not in viste:
                viste.add(k)
                out.append(Violazione("blocca", "forma_vietata", forma, can,
                                      perche or f"forma che l'essay non usa: sostituiscila con «{can}»", defi))
        elif tipo == "vicino":
            if not re.search(rf"\b{re.escape(can)}\b", testo or "", re.I):
                continue
            k = ("c", tuple(sorted([forma.lower(), can.lower()])))
            if k not in viste:
                viste.add(k)
                out.append(Violazione("avvisa", "termini_vicini", f"{forma} + {can}", "",
                                      perche or "usati insieme: verifica di non averli scambiati", defi))
        else:
            if voce.get("stato") != "definito":
                k = ("n", can.lower())
                if k not in viste:
                    viste.add(k)
                    out.append(Violazione("avvisa", "termine_non_definito", can, "",
                                          "l'essay lo usa ma non lo definisce: va definito prima "
                                          "di usarlo in senso tecnico", ""))
            elif _prima_di(sezione, defi, ordine) and not _anticipazione_ammessa(sezione, defi, voce, ordine):
                k = ("p", can.lower())
                if k not in viste:
                    viste.add(k)
                    out.append(Violazione("blocca", "uso_prima_definizione", can, "",
                                          f"usato in {sezione} ma definito solo in {defi}: "
                                          "o lo definisci qui, o riformuli", defi))
    out.sort(key=lambda v: (-GRAVITA[v.gravita], v.tipo, v.termine.lower()))
    return out


def blocca(violazioni) -> bool:
    return any(v.gravita == "blocca" for v in violazioni)


def _autotest() -> int:
    voci, _ = carica()
    problemi = tot = 0
    for v in voci:
        anc, sez = v.get("citazione_ancora") or "", v.get("sezione_definizione") or ""
        if not anc or not sez:
            continue
        tot += 1
        for x in lint(anc, sez):
            if x.gravita == "blocca":
                print(f"  {v['forma_canonica']} @ {sez}: [{x.tipo}] {x.termine}")
                problemi += 1
    print(f"autotest: {problemi} blocchi su {tot} citazioni-ancora (atteso: 0)")
    return 2 if problemi else 0


if __name__ == "__main__":
    if "--autotest" in sys.argv:
        sys.exit(_autotest())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sez = sys.argv[1]
    testo = open(sys.argv[3], encoding="utf-8").read() if sys.argv[2] == "--file" else " ".join(sys.argv[2:])
    vs = lint(testo, sez)
    if not vs:
        print("OK: nessuna violazione terminologica.")
        sys.exit(0)
    for v in vs:
        print(v)
    print(f"\n{len(vs)} rilievi. ", end="")
    if blocca(vs):
        print("BLOCCATO: risolvi i rilievi BLOCCA prima di chiudere la sezione.")
        sys.exit(2)
    print("Solo avvisi: leggili.")
