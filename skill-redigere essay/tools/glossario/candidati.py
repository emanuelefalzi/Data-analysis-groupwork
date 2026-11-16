#!/usr/bin/env python3
"""Glossario, fase 1 — candidatura dei termini (deterministica, nessun giudizio).

Conta gli n-grammi di 1-4 parole nel materiale dell'essay: `contenuto` delle
sezioni della scaletta + `cosa_dice` dei punti che la scaletta usa. Per ognuno:
frequenza, numero di sezioni distinte, se compare in un titolo (segnale forte:
concetto strutturale). Serve a non dimenticare termini che un lettore umano
darebbe per scontati. Il giudizio (quali termini sono vincolanti, quali vicini
sono pericolosi) lo fa dopo l'agente `redattore-glossario`, per gruppi.

Perche' esiste (lezione della tesi): un argomento accademico costruisce scale di
concetti vicini che NON sono sinonimi (familiarity → expertise → capability). Se
chi scrive mette «expertise» dove serve «capability» non e' un refuso: e'
l'argomento che salta. Con piu' sezioni scritte separatamente, la deriva
terminologica e' il rischio numero uno.

Uso:
    python3 tools/glossario/candidati.py [--top 60]
    python3 tools/glossario/candidati.py --gruppo scala_dominio "domain knowledge" "domain expertise"
        -> scrive glossario/gruppi/scala_dominio.json con tutte le occorrenze verbatim,
           input del redattore per quel gruppo
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

STOP = set("""a an the and or but if of to in on at by for with from as is are was were be been
being this that these those it its into than then there their they them which who whom whose
what when where why how not no can could may might must should would will shall do does did
has have had more most less least very also such only both each other any all some one two
between within without over under about through across per via e o il lo la i gli le un una di
da in con su per tra fra che non piu come del della dei delle nel nella al alla ed si se ma anche
""".split())


def materiale() -> list[tuple[str, str, bool]]:
    """[(id_sezione, testo, e_titolo)]"""
    sez = comune.sezioni()
    try:
        punti = comune.estratti()["punti"]
    except SystemExit:
        punti = {}
    out = []
    for s in sez.values():
        out.append((s["id"], s["titolo"], True))
        out.append((s["id"], s["contenuto"], False))
        for p in s["punti"]:
            if p in punti:
                out.append((s["id"], punti[p]["cosa_dice"], False))
    return out


def ngrammi(testo: str, n: int):
    tok = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]*", testo.lower())
    for i in range(len(tok) - n + 1):
        g = tok[i:i + n]
        if g[0] in STOP or g[-1] in STOP or any(len(x) < 3 for x in (g[0], g[-1])):
            continue
        yield " ".join(g)


def candidati(top: int):
    freq, sezioni, titoli = collections.Counter(), collections.defaultdict(set), set()
    for sid, t, tit in materiale():
        for n in (1, 2, 3, 4):
            for g in ngrammi(t, n):
                freq[g] += 1
                sezioni[g].add(sid)
                if tit:
                    titoli.add(g)
    righe = []
    for g, f in freq.items():
        nwords = len(g.split())
        if f < 2 and g not in titoli:
            continue
        punteggio = f * (1 + 0.5 * (nwords - 1)) + 3 * (g in titoli) + len(sezioni[g])
        righe.append({"termine": g, "frequenza": f, "sezioni": sorted(sezioni[g]),
                      "in_titolo": g in titoli, "punteggio": round(punteggio, 1)})
    righe.sort(key=lambda r: -r["punteggio"])
    return righe[:top]


def gruppo(nome: str, termini: list[str]) -> Path:
    mat = materiale()
    voci = []
    for t in termini:
        occ = []
        rx = re.compile(rf"\b{re.escape(t)}\b", re.I)
        for sid, testo, _ in mat:
            for frase in re.split(r"(?<=[.!?])\s+", testo):
                if rx.search(frase):
                    occ.append({"sezione": sid, "passaggio": frase.strip()})
        voci.append({"termine": t, "n_occorrenze": len(occ),
                     "sezioni": sorted({o["sezione"] for o in occ}), "occorrenze": occ[:25]})
    dest = comune.ROOT / "glossario" / "gruppi" / f"{nome}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"gruppo": nome, "termini": voci,
                                "ordine_sezioni": list(comune.sezioni())},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=60)
    ap.add_argument("--gruppo", help="nome del gruppo da preparare per il redattore")
    ap.add_argument("termini", nargs="*")
    a = ap.parse_args(argv)
    if a.gruppo:
        if not a.termini:
            sys.exit("--gruppo vuole l'elenco dei termini")
        print(f"Scritto {comune.rel(gruppo(a.gruppo, a.termini))}")
        return 0
    c = candidati(a.top)
    dest = comune.ROOT / "glossario" / "candidati.json"
    dest.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in c:
        print(f"{r['punteggio']:>6}  {r['termine']:<40} x{r['frequenza']:<3} "
              f"{'T ' if r['in_titolo'] else '  '}{','.join(r['sezioni'])}")
    print(f"\nScritto {comune.rel(dest)}. Ora raggruppa i termini imparentati (quelli che rischiano "
          "di essere confusi) e prepara un file per gruppo con --gruppo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
