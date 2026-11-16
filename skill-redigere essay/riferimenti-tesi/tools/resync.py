#!/usr/bin/env python3
"""resync.py — rilegge l'Excel, confronta gli sha per colonna con
`build/nodes.json`, riporta *cosa* e' cambiato e riporta a `vuoto` i soli
nodi toccati (§3, §10). Non e' un canale di modifica strutturale: **fallisce
con un errore esplicito se l'insieme delle chiavi `Indice` e' cambiato** (un
nodo aggiunto o rimosso) e impone un `/tesi-ingest` pulito.

Uso:
    /usr/bin/python3 tools/resync.py               # applica: aggiorna nodes.json
    /usr/bin/python3 tools/resync.py --dry-run      # solo report, non scrive
    /usr/bin/python3 tools/resync.py --help

Non scrive mai sull'Excel. Non tocca `nodes/<id>.md`: quello lo fa il
node-writer/fix-applier, non questo script (§3: il materiale immutabile
vive in `nodes.json`, la prosa in `nodes/<id>.md`, sono due file diversi
con due proprietari diversi).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
BUILD_DIR = ingest.BUILD_DIR

COLONNE_SHA = ("desc", "fonti", "ruolo", "trappole", "note")

# campi che, per un nodo toccato, vanno rinfrescati col valore nuovo:
# tutto cio' che deriva direttamente dall'Excel, mai target_words/regime
# (quelli sono calcolati da /tesi-gap, non da questo script; expansion_ratio
# e' ritirato dalla specifica, non esiste piu' come campo — §3).
CAMPI_DA_RINFRESCARE = (
    "title", "source_desc", "fonti", "ruolo", "trappole", "note",
    "risoluzioni", "fonti_ammesse", "fonti_vietate", "fonti_vietate_dettaglio",
    "source_words", "sha", "perimetro", "is_leaf", "level", "chapter", "parent",
)


def load_existing_nodes_json(build_dir=BUILD_DIR):
    path = build_dir + "nodes.json"
    if not os.path.exists(path):
        raise SystemExit(
            f"{path} non esiste: /tesi-resync non e' un sostituto di /tesi-ingest. "
            "Esegui prima l'ingest."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f), path


def diff_nodes(old_nodes, new_nodes):
    """Ritorna (chiavi_cambiate: bool, aggiunti, rimossi, cambiati: {id: [colonne]})."""
    old_keys = set(old_nodes.keys())
    new_keys = set(new_nodes.keys())
    aggiunti = sorted(new_keys - old_keys)
    rimossi = sorted(old_keys - new_keys)
    chiavi_cambiate = bool(aggiunti or rimossi)

    cambiati = {}
    for nid in sorted(old_keys & new_keys):
        old_sha = old_nodes[nid].get("sha", {})
        new_sha = new_nodes[nid].get("sha", {})
        colonne = [c for c in COLONNE_SHA if old_sha.get(c) != new_sha.get(c)]
        if colonne:
            cambiati[nid] = colonne
    return chiavi_cambiate, aggiunti, rimossi, cambiati


def apply_resync(old_data, new_nodes, cambiati):
    """Aggiorna in place old_data['nodes'] per i soli nodi cambiati:
    rinfresca i campi derivati dall'Excel e riporta `stato` a 'vuoto'.
    I nodi non toccati restano bit-per-bit come sono (compreso il loro
    `stato`, che qui puo' essere gia' avanzato oltre 'vuoto' da un'altra
    fase della pipeline non coperta da questo script)."""
    for nid in cambiati:
        old_node = old_data["nodes"][nid]
        new_node = new_nodes[nid]
        for campo in CAMPI_DA_RINFRESCARE:
            old_node[campo] = new_node[campo]
        old_node["stato"] = "vuoto"
        # target_words/regime sono di /tesi-gap: se il materiale e' cambiato
        # non sono piu' affidabili, azzerali per evitare che un lint li legga
        # come ancora validi. expansion_ratio e' ritirato (§3): non lo
        # riscriviamo piu', nemmeno per un nodo generato prima di questa
        # correzione che lo portasse ancora come campo morto.
        old_node["target_words"] = 0
        old_node["regime"] = None
        old_node.pop("expansion_ratio", None)
    return old_data


def run(excel_path=EXCEL_PATH, dry_run=False):
    old_data, path = load_existing_nodes_json()
    old_nodes = old_data["nodes"]

    loaded = ingest.load_workbook_rows(excel_path)
    new_nodes, off_record_stats = ingest.build_nodes(loaded)

    chiavi_cambiate, aggiunti, rimossi, cambiati = diff_nodes(old_nodes, new_nodes)

    print(f"nodi in build/nodes.json: {len(old_nodes)}  ·  nodi nell'Excel ora: {len(new_nodes)}")
    print(f"blocchi [OFF-RECORD] rimossi in questa rilettura: {off_record_stats['totale']}")

    if chiavi_cambiate:
        print("\nERRORE: l'insieme delle chiavi Indice e' cambiato.")
        if aggiunti:
            print("  aggiunti: " + ", ".join(aggiunti))
        if rimossi:
            print("  rimossi: " + ", ".join(rimossi))
        print(
            "\n/tesi-resync non sa riconoscere righe aggiunte o rimosse: serve un "
            "/tesi-ingest pulito (§3, §10). Non ho toccato build/nodes.json."
        )
        sys.exit(2)

    if not cambiati:
        print("\nNessuna colonna cambiata sui nodi esistenti: nulla da fare.")
        sys.exit(0)

    print(f"\n{len(cambiati)} nodi con almeno una colonna cambiata:")
    for nid, colonne in cambiati.items():
        print(f"  {nid}: {', '.join(colonne)}")

    if dry_run:
        print("\n--dry-run: build/nodes.json non modificato.")
        return

    new_data = apply_resync(old_data, new_nodes, cambiati)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"\nriportati a 'vuoto': {len(cambiati)} nodi. Scritto: {path}")
    print(
        "Nota: nodes/<id>.md NON e' stato toccato — se quei nodi avevano gia' un DRAFT, "
        "resta li' finche' qualcuno non lo riscrive; 'stato' in nodes.json dice solo che "
        "va rivisto."
    )


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Rilegge l'Excel, confronta gli sha per colonna con build/nodes.json, "
                     "riporta a 'vuoto' i soli nodi toccati. Fallisce se le chiavi Indice "
                     "sono cambiate (serve un /tesi-ingest pulito).")
    ap.add_argument("--excel", default=EXCEL_PATH, help="percorso dell'Excel (assoluto)")
    ap.add_argument("--dry-run", action="store_true",
                     help="solo report: non scrive build/nodes.json")
    args = ap.parse_args(argv)
    try:
        run(excel_path=args.excel, dry_run=args.dry_run)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
