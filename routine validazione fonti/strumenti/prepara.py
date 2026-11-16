#!/usr/bin/env python3
"""Fase 1: prepara un task JSON per ogni coppia (sezione x fonte) di coppie.csv.

Equivalente di loop2/prepara.py della tesi, ma legge un CSV invece dell'Excel.
NON lancia i subagent: quello lo fa l'orchestratore (Claude in chat).

Uso:
    python3 prepara.py               # tutte le coppie che non hanno ancora un esito del lettore A
    python3 prepara.py --solo 2.1    # solo quella sezione
    python3 prepara.py --rifai       # rigenera anche quelle gia' lette
"""
import argparse, csv, json, os

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
COPPIE = os.path.join(RADICE, "coppie.csv")
TESTI = os.path.join(RADICE, "lavoro", "testi")
TASK = os.path.join(RADICE, "lavoro", "task")
OUT_A = os.path.join(RADICE, "lavoro", "estratti")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo")
    ap.add_argument("--rifai", action="store_true")
    a = ap.parse_args()
    os.makedirs(TASK, exist_ok=True)

    n = saltate = 0
    with open(COPPIE, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            sez, fid = (r.get("sezione") or "").strip(), (r.get("id_fonte") or "").strip()
            if not sez or not fid:
                continue
            if a.solo and sez != a.solo:
                continue
            nome = f"{sez}__{fid}.json"
            if not a.rifai and os.path.exists(os.path.join(OUT_A, nome)):
                continue
            testo = os.path.join(TESTI, fid + ".txt")
            if not os.path.exists(testo):
                print(f"  salto {sez} x {fid}: manca il testo, lancia prima salva_pagine.py")
                saltate += 1
                continue
            meta_p = os.path.join(TESTI, fid + ".meta.json")
            meta = json.load(open(meta_p, encoding="utf-8")) if os.path.exists(meta_p) else {}
            task = {
                "sezione": sez,
                "id_fonte": fid,
                "url": r.get("url", "").strip(),
                "citazione": r.get("citazione", "").strip(),
                "tipo_fonte": r.get("tipo_fonte", "").strip(),
                "ruolo": r.get("ruolo", "").strip(),
                "claim": r.get("claim", "").strip(),
                "percorso_testo": testo,
                "caratteri_testo": os.path.getsize(testo),
                "data_accesso": meta.get("data_accesso", ""),
            }
            with open(os.path.join(TASK, nome), "w", encoding="utf-8") as out:
                json.dump(task, out, ensure_ascii=False, indent=1)
            n += 1
    print(f"Preparati {n} task in lavoro/task/ ({saltate} saltati per testo mancante)")


if __name__ == "__main__":
    main()
