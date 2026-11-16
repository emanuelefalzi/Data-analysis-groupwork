#!/usr/bin/env python3
"""Loop 2 - Fase 1: prepara i task per i subagent.

Legge il foglio Estratti e produce un file JSON per ogni coppia (nodo x fonte)
ancora da verificare, con tutto quello che serve al subagent.
NON lancia i subagent: quello lo fa l'orchestratore.
NON scrive nell'Excel.

Uso:
    python3 prepara.py                 # tutte le coppie non verificate
    python3 prepara.py --solo 3.1.1    # solo quel nodo
    python3 prepara.py --mattoni       # solo i mattoni stretti
    python3 prepara.py --limite 3      # prime N (per il collaudo)
"""
import argparse, json, os, sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
XLSX = BASE + "iTOC master.xlsx"
MD   = BASE + "FONTI/pipeline/testi estratti/"
TASK = BASE + "FONTI/pipeline/loop2/task/"
OUT  = BASE + "FONTI/estrazioni/estratti/"

COL = dict(nodo=1, fonte=2, citazione=3, ruolo=4, peer=5, pdf=6, claim=7, esito=8)


def carica(solo=None, mattoni=False, limite=None, rifai=False):
    import openpyxl
    ws = openpyxl.load_workbook(XLSX, data_only=True)["Estratti"]
    task = []
    for r in range(2, ws.max_row + 1):
        g = lambda c: ws.cell(r, COL[c]).value
        if not g("nodo"):
            continue
        if not rifai and g("esito"):
            continue                       # gia' verificata
        if solo and str(g("nodo")) != solo:
            continue
        if mattoni and g("ruolo") != "mattone stretto":
            continue
        fid = g("fonte")
        testo = MD + fid + ".txt"
        if not os.path.exists(testo):
            print(f"  salto {g('nodo')} x {fid}: manca {os.path.basename(testo)}")
            continue
        task.append({
            "nodo": str(g("nodo")),
            "id_fonte": fid,
            "citazione": g("citazione"),
            "ruolo": g("ruolo"),
            "peer_reviewed": g("peer"),
            "claim": g("claim"),
            "percorso_testo": testo,
            "caratteri_testo": os.path.getsize(testo),
            "riga_excel": r,
        })
        if limite and len(task) >= limite:
            break
    return task


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo")
    ap.add_argument("--mattoni", action="store_true")
    ap.add_argument("--limite", type=int)
    ap.add_argument("--rifai", action="store_true",
                    help="rigenera anche le coppie gia' verificate")
    a = ap.parse_args()

    os.makedirs(TASK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    task = carica(a.solo, a.mattoni, a.limite, a.rifai)
    if not task:
        print("Nessuna coppia da preparare.")
        return

    for t in task:
        nome = f"{t['nodo']}__{t['id_fonte']}.json"
        with open(TASK + nome, "w", encoding="utf-8") as fh:
            json.dump(t, fh, ensure_ascii=False, indent=1)

    print(f"Preparati {len(task)} task in loop2/task/")
    ms = sum(1 for t in task if t["ruolo"] == "mattone stretto")
    print(f"  di cui mattoni stretti: {ms}")
    tot = sum(t["caratteri_testo"] for t in task)
    print(f"  caratteri di testo totali da leggere: {tot:,}")
    print(f"  media per fonte: {tot // len(task):,}")


if __name__ == "__main__":
    main()
