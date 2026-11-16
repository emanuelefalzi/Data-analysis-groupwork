#!/usr/bin/env python3
"""Loop 2, fase 1 — prepara un task per ogni fonte da leggere.

Nella tesi il task era una coppia (nodo x fonte) con un claim gia' scritto da
verificare. Qui le affermazioni non esistono ancora: il task e' una fonte con le
DOMANDE del brief (`input/brief.md`, sezione «Domande per le fonti»), e il lettore
estrae cio' che la fonte risponde a ciascuna. E' la modalita' «estrazione per
domande» gia' usata sul group project Cosmico.

NON lancia i lettori: lo fa l'orchestratore (skill `essay-estrai`).
NON scrive in fonti.csv.

Uso:
    python3 tools/fonti/prepara.py               # tutte le fonti con testo e senza scheda
    python3 tools/fonti/prepara.py --solo akerlof1970
    python3 tools/fonti/prepara.py --rifai       # anche quelle gia' lette
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402
from lib.csvio import FontiCSV  # noqa: E402


def citazione_breve(r: dict) -> str:
    a = (r.get("autori") or r["id"]).split(";")[0].split(",")[0].strip()
    piu = ";" in (r.get("autori") or "") or " and " in (r.get("autori") or "")
    return f"({a}{' et al.' if piu else ''}, {r.get('anno') or 'n.d.'})"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", action="append")
    ap.add_argument("--rifai", action="store_true")
    a = ap.parse_args(argv)

    domande = comune.domande_dal_brief()
    if not domande:
        print("ERRORE: nessuna domanda trovata in input/brief.md.\n"
              "Serve una sezione il cui titolo contiene «Domande», con un elenco puntato: "
              "una domanda per riga. Senza domande il lettore non sa cosa estrarre.")
        return 2

    c = FontiCSV(comune.FONTI_CSV); c.open()
    comune.TASK.mkdir(parents=True, exist_ok=True)
    comune.SCHEDE.mkdir(parents=True, exist_ok=True)

    fatti, saltati = [], []
    for fid in c.all_ids():
        if a.solo and fid not in a.solo:
            continue
        r = c.get(fid)
        if r.get("stato") == "abbandonata":
            continue
        testo = comune.TESTI / f"{fid}.txt"
        if not testo.exists():
            saltati.append(f"{fid}: manca {comune.rel(testo)}")
            continue
        if (comune.SCHEDE / f"{fid}.json").exists() and not a.rifai:
            continue
        task = {
            "id_fonte": fid,
            "citazione": citazione_breve(r),
            "titolo": r.get("titolo", ""),
            "tipo": r.get("tipo", ""),
            "peer_reviewed": r.get("peer") or "n.d.",
            "contesto": r.get("contesto", ""),
            "domande": domande,
            "lingua_output": comune.config()["lingua"],
            "percorso_testo": str(testo),
            "caratteri_testo": testo.stat().st_size,
            "percorso_output": str(comune.SCHEDE / f"{fid}.json"),
        }
        (comune.TASK / f"{fid}.json").write_text(json.dumps(task, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
        fatti.append(task)

    for s in saltati:
        print(f"  salto {s}")
    if not fatti:
        print("Nessuna fonte da preparare.")
        return 0
    tot = sum(t["caratteri_testo"] for t in fatti)
    print(f"Preparati {len(fatti)} task in {comune.rel(comune.TASK)} · {len(domande)} domande ciascuno")
    print(f"  caratteri da leggere: {tot:,} (media {tot // len(fatti):,})")
    grandi = [t["id_fonte"] for t in fatti if t["caratteri_testo"] > 300_000]
    if grandi:
        print(f"  oltre 300.000 caratteri (lettura per ricerca, non integrale): {', '.join(grandi)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
