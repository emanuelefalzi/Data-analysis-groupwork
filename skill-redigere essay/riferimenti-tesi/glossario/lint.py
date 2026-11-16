#!/usr/bin/env python3
"""Linter terminologico della tesi.

L'orchestratore di stesura chiama `lint(testo, nodo)` su ogni paragrafo
generato PRIMA di considerarlo chiuso. Una violazione BLOCCA, non avvisa.

Uso da riga di comando:
    python3 lint.py 4.2.1 "testo del paragrafo..."
    python3 lint.py 4.2.1 --file paragrafo.txt
    python3 lint.py --autotest        # controlla il glossario su se stesso
"""
from __future__ import annotations
import json, os, re, sys
from dataclasses import dataclass, asdict

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
GLOSSARIO = BASE + "FONTI/pipeline/glossario/glossario.json"

GRAVITA = {"blocca": 2, "avvisa": 1}


@dataclass
class Violazione:
    gravita: str          # "blocca" | "avvisa"
    tipo: str             # "variante_vietata" | "uso_prima_definizione" | "termine_non_definito"
    termine: str          # cosa e' stato trovato nel testo
    usa_invece: str       # forma canonica da usare, se applicabile
    perche: str
    nodo_definizione: str

    def __str__(self):
        freccia = f"  ->  usa «{self.usa_invece}»" if self.usa_invece else ""
        return f"[{self.gravita.upper()}] «{self.termine}»{freccia}\n    {self.perche}"


def _chiave_nodo(n):
    try:
        return tuple(int(p) for p in str(n).split("."))
    except Exception:
        return (99,)


def _prima_di(nodo_uso, nodo_def) -> bool:
    """Il nodo in cui sto scrivendo precede il nodo di definizione?"""
    if not nodo_def:
        return False
    return _chiave_nodo(nodo_uso) < _chiave_nodo(nodo_def)


def _anticipazione_ammessa(nodo_uso, nodo_def, can=None, voci=None) -> bool:
    """Il blocco introduttivo (0.x) e il nodo padre possono anticipare un
    termine: e' prassi normale annunciare un concetto e definirlo dopo.
    In piu' (patch AG-07): il glossario stesso puo' dichiarare l'anticipazione
    legittima, o su tutti i nodi (usabile_prima_del_nodo_definizione) o su un
    elenco esplicito di nodi/discendenti (anticipazioni_legittime)."""
    nu, nd = str(nodo_uso), str(nodo_def or "")
    if nu.startswith("0"):
        return True
    if nd.startswith(nu + ".") or nu == nd.split(".")[0]:
        return True
    v = next((x for x in (voci or [])
              if (x.get("forma_canonica") or "").lower() == (can or "").lower()), None)
    if v:
        if v.get("usabile_prima_del_nodo_definizione"):
            return True
        for a in v.get("anticipazioni_legittime", []) or []:
            a = str(a)
            if nu == a or nu.startswith(a + "."):
                return True
    return False


def _compila(voci):
    """Costruisce le regex una volta sola. Confine di parola, case-insensitive."""
    reg = []
    for v in voci:
        can = (v.get("forma_canonica") or "").strip()
        if not can:
            continue
        for var in v.get("varianti_vietate", []):
            forma = (var.get("forma") or "").strip()
            if not forma or forma.lower() == can.lower():
                continue
            # Due classi, due trattamenti diversi.
            # forma_errata      = forma che nella tesi non compare mai: usarla e' un errore -> BLOCCA
            # vicino_confondibile = termine legittimo con significato distinto: il linter non
            #                       puo' sapere quale dei due intendevi, quindi RICORDA la
            #                       distinzione invece di bloccare.
            classe = var.get("classe", "vicino_confondibile")
            tipo = "variante" if classe == "forma_errata" else "vicino"
            reg.append((tipo, re.compile(rf"\b{re.escape(forma)}\b", re.I),
                        forma, can, var.get("perche", ""), v.get("nodo_definizione", "")))
        reg.append(("canonico", re.compile(rf"\b{re.escape(can)}\b", re.I),
                    can, can, "", v.get("nodo_definizione", "")))
        if v.get("stato") != "definito":
            reg.append(("non_definito", re.compile(rf"\b{re.escape(can)}\b", re.I),
                        can, can, "", v.get("nodo_definizione", "")))
    return reg


_CACHE = {}


def carica(percorso=GLOSSARIO):
    if percorso not in _CACHE:
        d = json.load(open(percorso, encoding="utf-8"))
        _CACHE[percorso] = (d["voci"], _compila(d["voci"]))
    return _CACHE[percorso]


def lint(testo: str, nodo: str, percorso=GLOSSARIO) -> list[Violazione]:
    voci, reg = carica(percorso)
    viste = set()
    out = []
    for tipo, rx, forma, can, perche, nodo_def in reg:
        if not rx.search(testo or ""):
            continue
        if tipo == "variante":
            k = ("v", forma.lower(), can.lower())
            if k in viste:
                continue
            viste.add(k)
            out.append(Violazione("blocca", "forma_vietata", forma, can,
                                  perche or f"forma che la tesi non usa mai: sostituiscila con «{can}»",
                                  nodo_def))
        elif tipo == "vicino":
            # Avviso, non blocco: entrambi i termini sono legittimi, ma sono
            # diversi. Serve a ricordare la distinzione a chi scrive.
            if not re.search(rf"\b{re.escape(can)}\b", testo or "", re.I):
                continue      # se il termine vicino non compare, non c'e' rischio di confusione
            k = ("c", tuple(sorted([forma.lower(), can.lower()])))
            if k in viste:
                continue
            viste.add(k)
            out.append(Violazione("avvisa", "termini_vicini", f"{forma} + {can}", "",
                                  perche or "usati insieme nello stesso paragrafo: verifica di non averli scambiati",
                                  nodo_def))
        elif tipo == "canonico":
            if _prima_di(nodo, nodo_def) and not _anticipazione_ammessa(nodo, nodo_def, can, voci):
                k = ("p", can.lower())
                if k in viste:
                    continue
                viste.add(k)
                out.append(Violazione("blocca", "uso_prima_definizione", can, "",
                                      f"usato nel nodo {nodo} ma definito solo nel nodo "
                                      f"{nodo_def}: o lo definisci qui, o riformuli",
                                      nodo_def))
        elif tipo == "non_definito":
            k = ("n", can.lower())
            if k in viste:
                continue
            viste.add(k)
            out.append(Violazione("avvisa", "termine_non_definito", can, "",
                                  "la tesi lo usa ma non lo definisce da nessuna parte: "
                                  "va definito prima di usarlo in senso tecnico", ""))
    out.sort(key=lambda v: (-GRAVITA[v.gravita], v.tipo, v.termine.lower()))
    return out


def blocca(violazioni) -> bool:
    return any(v.gravita == "blocca" for v in violazioni)


def _autotest():
    """Passa ogni citazione-ancora del glossario nel linter, sul suo nodo di
    definizione. Un glossario sano non deve bloccare le proprie definizioni."""
    voci, _ = carica()
    problemi = 0
    for v in voci:
        anc = v.get("citazione_ancora") or ""
        nodo = v.get("nodo_definizione") or ""
        if not anc or not nodo:
            continue
        for x in lint(anc, nodo):
            if x.gravita == "blocca":
                print(f"  {v['forma_canonica']} @ {nodo}: [{x.tipo}] {x.termine}"
                      + (f" -> {x.usa_invece}" if x.usa_invece else ""))
                problemi += 1
    print(f"autotest: {problemi} blocchi su {sum(1 for v in voci if v.get('citazione_ancora') and v.get('nodo_definizione'))} citazioni-ancora")
    print("Un glossario sano non blocca le proprie definizioni: qui il numero atteso e' 0.")


if __name__ == "__main__":
    if "--autotest" in sys.argv:
        _autotest()
        sys.exit(0)
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    nodo = sys.argv[1]
    if sys.argv[2] == "--file":
        testo = open(sys.argv[3], encoding="utf-8").read()
    else:
        testo = " ".join(sys.argv[2:])
    vs = lint(testo, nodo)
    if not vs:
        print("OK: nessuna violazione.")
        sys.exit(0)
    for v in vs:
        print(v)
    print(f"\n{len(vs)} rilievi. ", end="")
    if blocca(vs):
        print("BLOCCATO: risolvi i rilievi marcati BLOCCA prima di chiudere il paragrafo.")
        sys.exit(2)
    print("Solo avvisi: puoi procedere, ma leggili.")
