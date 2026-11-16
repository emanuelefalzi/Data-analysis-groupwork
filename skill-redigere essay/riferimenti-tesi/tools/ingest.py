#!/usr/bin/env python3
"""ingest.py — legge `iTOC master.xlsx` (foglio DOSSIER, non iTOC+Estratti a mano)
e produce `build/nodes.json`, `build/estratti.json`, `build/metrics.json` e uno
`nodes/<id>.md` per nodo (solo `## DRAFT` e `## LEDGER`, vuote).

Va lanciato con /usr/bin/python3 (ha openpyxl 3.1.5). Percorsi assoluti, mai `cd`
nella cartella della tesi.

Uso:
    /usr/bin/python3 tools/ingest.py              # scrive build/, nodes/
    /usr/bin/python3 tools/ingest.py --dry-run     # sola lettura, solo report
    /usr/bin/python3 tools/ingest.py --help

Riferimento: PROMPT-orchestratore-tesi.md §2 (albero), §3 (modello dati), §10
(FASE 0 / GATE 0). Stile ripreso da FONTI/pipeline/dossier.py.

Idempotente: rilanciarlo senza modifiche all'Excel riproduce lo stesso
`nodes.json` (a parte `generated_at`); non sovrascrive un `nodes/<id>.md` che
contiene già un DRAFT o un LEDGER non vuoti, per non perdere lavoro del
node-writer se qualcuno lo rilancia per sbaglio dopo l'inizio della stesura.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
EXCEL_PATH = BASE + "iTOC master.xlsx"
BUILD_DIR = BASE + "build/"
NODES_DIR = BASE + "nodes/"
REPORTS_DIR = BASE + "reports/"

WORDS_PER_PAGE = 350
WORDS_PER_PAGE_BAND = (310, 380)

# Il Cap. 7 era sospeso e §3 lo teneva fuori. Con la decisione dell'autore del
# 2026-09-08 -- budget su otto capitoli, `0->2 1->5 2->5 3->4 4->5 5->13 6->2
# 7->3` -- e' rientrato, e la costante era rimasta indietro.
# Non e' cosmetica: `lint_numeri` costruisce la whitelist dei numeri e dei nomi
# propri ammessi dalla UNIONE dei soli `source_desc` in perimetro. Con il Cap. 7
# fuori, le sue 504 parole di materiale non entravano nella whitelist, e ogni
# cifra o nome che vive solo li' sarebbe uscito come finding `high` -- cioe'
# "dato inventato" -- su materiale scritto dall'autore.
PERIMETRO_CAPITOLI = {"0", "1", "2", "3", "4", "5", "6", "7"}

OFF_RECORD_RE = re.compile(r"\[OFF-RECORD\][^\n]*")
AUDIT_RE = re.compile(r"\[AUDIT[^\]]*\][^\n]*")

# separatore usato da DOSSIER colonne H/I: " ; " (dossier.py, ' ; '.join(...))
DOSSIER_LIST_SEP = " ; "
DOSSIER_ENTRY_RE = re.compile(r"^\s*(?P<key>.+?)\s*\[(?P<label>[^\[\]]*)\]\s*$")


# --------------------------------------------------------------------------
# lettura Excel
# --------------------------------------------------------------------------

def find_lock_files(base=BASE):
    """File `~$*` di Word/Excel aperti. Se ce n'e' uno, ci si ferma (§1)."""
    out = []
    try:
        for name in os.listdir(base):
            if name.startswith("~$"):
                out.append(os.path.join(base, name))
    except FileNotFoundError:
        pass
    return out


def rows(ws):
    """Stesso helper di dossier.py: righe come dict header->valore."""
    rr = [list(r) for r in ws.iter_rows(values_only=True)]
    if not rr:
        return []
    hdr = [str(h) if h is not None else "" for h in rr[0]]
    return [dict(zip(hdr, r)) for r in rr[1:]]


def load_workbook_rows(excel_path=EXCEL_PATH):
    import openpyxl  # import qui: cosi' --help funziona anche senza openpyxl importato a livello di modulo in errore

    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    needed = {"iTOC", "DOSSIER", "Fonti", "Estratti"}
    missing = needed - set(wb.sheetnames)
    if missing:
        raise SystemExit(f"Fogli mancanti nell'Excel: {sorted(missing)}")
    return {
        "itoc": rows(wb["iTOC"]),
        "dossier": rows(wb["DOSSIER"]),
        "fonti": rows(wb["Fonti"]),
        "estratti": rows(wb["Estratti"]),
    }


# --------------------------------------------------------------------------
# utility di normalizzazione
# --------------------------------------------------------------------------

def clean(x):
    if x is None or str(x) == "None":
        return ""
    return str(x).strip()


def word_count(s):
    s = clean(s)
    return len(s.split()) if s else 0


def sha256_text(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()


def strip_off_record(text):
    """Rimuove ogni blocco `[OFF-RECORD]...` fino a fine riga. Ritorna
    (testo_pulito, n_blocchi_rimossi)."""
    text = text or ""
    n = len(OFF_RECORD_RE.findall(text))
    cleaned = OFF_RECORD_RE.sub("", text)
    # righe rimaste vuote dopo la rimozione: le ripuliamo, senza toccare il resto
    cleaned = "\n".join(line for line in cleaned.split("\n") if line.strip() != "")
    return cleaned.strip(), n


def extract_audit(text):
    """Estrae ogni blocco `[AUDIT ...]...` (fino a fine riga) da `text`, gia'
    privato di [OFF-RECORD]. Ritorna (testo_senza_audit, audit_aperto,
    n_blocchi): `audit_aperto` sono i blocchi estratti verbatim, uniti da
    '\\n\\n' se piu' di uno. E' una diagnosi con opzioni aperte (§3), mai
    materiale di stesura: va in un campo separato da `note`, non scartata."""
    text = text or ""
    blocks = AUDIT_RE.findall(text)
    cleaned = AUDIT_RE.sub("", text)
    cleaned = "\n".join(line for line in cleaned.split("\n") if line.strip() != "")
    return cleaned.strip(), "\n\n".join(blocks), len(blocks)


def parse_dossier_list(cell_value):
    """Parsa 'key1 [label1] ; key2 [label2]' -> [(key, label), ...].
    Usato sia per la colonna H (ammesse) sia per la I (vietate)."""
    val = clean(cell_value)
    if not val:
        return []
    out = []
    for part in val.split(DOSSIER_LIST_SEP):
        part = part.strip()
        if not part:
            continue
        m = DOSSIER_ENTRY_RE.match(part)
        if m:
            out.append((m.group("key").strip(), m.group("label").strip()))
        else:
            # formato inatteso: teniamo la stringa intera come chiave, label vuota
            out.append((part, ""))
    return out


def budget_pp_by_chapter(itoc_rows):
    """Budget pp per capitolo (valorizzato solo sulle righe di capitolo,
    iTOC colonna I). Riusato da gap.py: e' un solo giro sul foglio."""
    out = {}
    for r in itoc_rows:
        idx = clean(r.get("Indice"))
        if idx and "." not in idx and r.get("Budget pp") not in (None, ""):
            try:
                out[idx] = float(r.get("Budget pp"))
            except (TypeError, ValueError):
                pass
    return out


def node_level(idx):
    return idx.count(".") + 1


def node_chapter(idx):
    return idx.split(".")[0]


def node_parent(idx):
    parts = idx.split(".")
    if len(parts) <= 1:
        return None
    return ".".join(parts[:-1])


# --------------------------------------------------------------------------
# costruzione nodes.json / estratti.json
# --------------------------------------------------------------------------

def index_by(rows_list, key):
    out = {}
    for r in rows_list:
        k = clean(r.get(key))
        if k:
            out[k] = r
    return out


def group_estratti_by_node(estratti_rows):
    by_node = {}
    for r in estratti_rows:
        n = clean(r.get("Nodo"))
        if not n:
            continue
        by_node.setdefault(n, []).append(r)
    return by_node



def applica_override_fonti(nodes):
    """Applica `decisions/override-fonti.json`: le fonti che l'autore ammette
    nonostante il gate del DOSSIER le vieti.

    Serve perche' l'Excel e' congelato e una modifica diretta a
    `build/nodes.json` verrebbe persa al primo rigenero, in silenzio. Ogni voce
    del file cita la decisione dell'autore che la giustifica.
    """
    path = BASE + "decisions/override-fonti.json"
    if not os.path.exists(path):
        return 0
    dati = json.load(open(path, encoding="utf-8"))
    n = 0
    for v in dati.get("ammetti", []):
        nid, fonte = v["nodo"], v["fonte"]
        nodo = nodes.get(nid)
        if not nodo:
            continue
        nodo["fonti_vietate"] = [f for f in nodo.get("fonti_vietate", []) if f != fonte]
        if fonte not in {f["fonte"] for f in nodo.get("fonti_ammesse", [])}:
            nodo.setdefault("fonti_ammesse", []).append(
                {"fonte": fonte, "ruolo": "override autore", "regime": "usabile",
                 "override": v.get("decisione", "")})
            n += 1
    return n

def build_nodes(loaded):
    """Costruisce la lista di record nodo (schema §3) + le statistiche dei
    filtri [OFF-RECORD] e [AUDIT ...] (quest'ultimo estratto in `audit_aperto`,
    mai lasciato in `note`). Non scrive niente su disco."""
    itoc_rows = loaded["itoc"]
    dossier_by_idx = index_by(loaded["dossier"], "Indice")
    estratti_by_node = group_estratti_by_node(loaded["estratti"])

    all_idx = {clean(r.get("Indice")) for r in itoc_rows if clean(r.get("Indice"))}

    off_record_itoc_removed = 0
    off_record_dossier_removed = 0
    audit_blocchi_perimetro = 0
    audit_blocchi_totale = 0

    nodes = {}
    for r in itoc_rows:
        idx = clean(r.get("Indice"))
        if not idx:
            continue  # riga TOTALE o vuota

        title = clean(r.get("Titolo nodo"))
        source_desc = clean(r.get("Descrizione"))
        fonti_ruolo = clean(r.get("Fonti + ruolo"))
        ruolo = clean(r.get("Ruolo argomentativo"))
        trappole = clean(r.get("Trappole / rischi"))
        note_raw = clean(r.get("Note"))

        note_clean, n_removed_itoc = strip_off_record(note_raw)
        off_record_itoc_removed += n_removed_itoc

        # Note ha tre classi (§3): [DECISIONE AUTORE] resta in `note` (vincolante),
        # [OFF-RECORD] e' gia' fuori sopra, [AUDIT ...] e' una diagnosi con opzioni
        # aperte, non un'istruzione: va in un campo suo, mai in `note`.
        note_clean, audit_aperto, n_audit = extract_audit(note_clean)

        # DOSSIER!O ("Note autore") dovrebbe essere la stessa colonna copiata
        # verbatim da dossier.py: la filtriamo comunque, e' un passo esplicito
        # e indipendente richiesto dalla specifica.
        drow = dossier_by_idx.get(idx, {})
        note_autore_raw = clean(drow.get("Note autore"))
        _, n_removed_dossier = strip_off_record(note_autore_raw)
        off_record_dossier_removed += n_removed_dossier

        # fonti ammesse / vietate dal DOSSIER (colonne H, I) — mai da Estratti!Esito (§7)
        ammesse_raw = parse_dossier_list(drow.get("Fonti AMMESSE (chiavi)"))
        vietate_raw = parse_dossier_list(drow.get("Fonti VIETATE (chiavi + motivo)"))
        fonti_ammesse = [{"fonte": k, "regime": lbl} for k, lbl in ammesse_raw]
        fonti_vietate = [k for k, _ in vietate_raw]
        fonti_vietate_dettaglio = [{"fonte": k, "motivo": lbl} for k, lbl in vietate_raw]

        # risoluzioni[]: Estratti!S per le coppie del nodo, solo dove valorizzata
        risoluzioni = []
        for p in estratti_by_node.get(idx, []):
            sres = clean(p.get("Risoluzione (decisione autore)"))
            if sres:
                risoluzioni.append({"fonte": clean(p.get("ID fonte")), "risoluzione": sres})

        idx_level = node_level(idx)
        idx_chapter = node_chapter(idx)
        idx_parent = node_parent(idx)
        is_leaf = not any(other != idx and other.startswith(idx + ".") for other in all_idx)

        audit_blocchi_totale += n_audit
        if idx_chapter in PERIMETRO_CAPITOLI:
            audit_blocchi_perimetro += n_audit

        node = {
            "id": idx,
            "level": idx_level,
            "chapter": idx_chapter,
            "parent": idx_parent,
            "perimetro": idx_chapter in PERIMETRO_CAPITOLI,
            "is_leaf": is_leaf,
            "title": title,
            "source_desc": source_desc,
            "fonti": fonti_ruolo,
            "ruolo": ruolo,
            "trappole": trappole,
            "note": note_clean,
            "audit_aperto": audit_aperto,  # diagnosi con opzioni aperte (§3): mai materiale
            "risoluzioni": risoluzioni,
            "fonti_ammesse": fonti_ammesse,
            "fonti_vietate": fonti_vietate,
            "fonti_vietate_dettaglio": fonti_vietate_dettaglio,
            # regime e' assegnato per capitolo da /tesi-gap (§3), non qui:
            # placeholder finche' gap.py non gira.
            "regime": None,
            "sha": {
                "desc": sha256_text(source_desc),
                "fonti": sha256_text(fonti_ruolo),
                "ruolo": sha256_text(ruolo),
                "trappole": sha256_text(trappole),
                "note": sha256_text(note_raw),  # sha sul grezzo: un edit a un blocco
                                                 # OFF-RECORD deve comunque far scattare resync
            },
            # stato iniziale sempre 'vuoto', qualunque cosa dica iTOC!Stato (§3)
            "stato": "vuoto",
            "target_words": 0,
            "source_words": word_count(source_desc),
        }
        nodes[idx] = node

    off_record_stats = {
        "itoc_f_rimossi": off_record_itoc_removed,
        "dossier_o_rimossi": off_record_dossier_removed,
        "totale": off_record_itoc_removed + off_record_dossier_removed,
        # blocchi [AUDIT ...] estratti in audit_aperto (§3): stessa forma delle
        # righe sopra, ma non fanno parte del totale [OFF-RECORD] — restano qui
        # solo per non aggiungere un terzo valore di ritorno che romperebbe
        # gap.py/resync.py/lint_numeri.py/ledger_renumber.py, che fanno tutti
        # `nodes, _ = ingest.build_nodes(...)` o leggono solo `off_record_stats`.
        "audit_perimetro": audit_blocchi_perimetro,
        "audit_totale": audit_blocchi_totale,
    }
    n_ovr = applica_override_fonti(nodes)
    off_record_stats["override_fonti"] = n_ovr
    return nodes, off_record_stats


def build_estratti_index(loaded):
    """estratti.json: il foglio Estratti indicizzato (nodo, id_fonte)."""
    out = {}
    for r in loaded["estratti"]:
        nodo = clean(r.get("Nodo"))
        fonte = clean(r.get("ID fonte"))
        if not nodo or not fonte:
            continue
        key = f"{nodo}|{fonte}"
        out[key] = {
            "nodo": nodo,
            "id_fonte": fonte,
            "citazione": clean(r.get("Citazione")),
            "ruolo": clean(r.get("Ruolo")),
            "peer_review": clean(r.get("Peer-rev.")),
            "pdf": clean(r.get("PDF")),
            "claim_da_verificare": clean(r.get("Claim da verificare")),
            "esito": clean(r.get("Esito")),
            "cosa_dice_davvero": clean(r.get("Cosa dice davvero")),
            "citazione_verbatim": clean(r.get("Citazione verbatim")),
            "sezione": clean(r.get("Sezione")),
            "esito_notebooklm": clean(r.get("Esito NotebookLM")),
            "divergenza": clean(r.get("Divergenza")),
            "note": clean(r.get("Note")),
            "esito_arbitrato": clean(r.get("Esito arbitrato")),
            "risoluzione": clean(r.get("Risoluzione (decisione autore)")),
        }
    return out


def build_metrics(nodes, loaded):
    """Aggregati descrittivi (parole, budget, ratio) per capitolo. Non e' il
    gap report (quello e' /tesi-gap): sono i numeri grezzi da cui gap.py parte,
    cosi' non deve rileggere l'Excel ogni volta."""
    itoc_rows = loaded["itoc"]
    budget_by_chapter = {}
    for r in itoc_rows:
        idx = clean(r.get("Indice"))
        if idx and "." not in idx and r.get("Budget pp") not in (None, ""):
            budget_by_chapter[idx] = r.get("Budget pp")

    per_chapter = {}
    for idx, n in nodes.items():
        cap = n["chapter"]
        c = per_chapter.setdefault(cap, {
            "n_nodi": 0, "n_foglie": 0, "source_words": 0,
            "budget_pp": budget_by_chapter.get(cap),
        })
        c["n_nodi"] += 1
        if n["is_leaf"]:
            c["n_foglie"] += 1
        c["source_words"] += n["source_words"]

    totale_perimetro = sum(v["source_words"] for k, v in per_chapter.items()
                            if k in PERIMETRO_CAPITOLI)
    totale_tutto = sum(v["source_words"] for v in per_chapter.values())

    return {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "n_nodi_totale": len(nodes),
        "n_fonti": len(loaded["fonti"]),
        "n_coppie_estratti": len(loaded["estratti"]),
        "words_per_page": WORDS_PER_PAGE,
        "words_per_page_band": list(WORDS_PER_PAGE_BAND),
        "source_words_totale": totale_tutto,
        "source_words_perimetro": totale_perimetro,
        "per_capitolo": per_chapter,
    }


def write_node_md(node_id, path):
    """Crea nodes/<id>.md con sole '## DRAFT' e '## LEDGER' vuote. Non
    sovrascrive un file che contiene gia' del testo oltre lo scheletro, per
    idempotenza sicura (§3: nodes/<id>.md e' l'unico posto dove vive la
    prosa scritta dal node-writer)."""
    empty_template = "## DRAFT\n\n## LEDGER\n"
    if os.path.exists(path):
        existing = open(path, encoding="utf-8").read()
        if existing.strip() != empty_template.strip():
            return False  # gia' popolato: non lo tocchiamo
    with open(path, "w", encoding="utf-8") as f:
        f.write(empty_template)
    return True


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def run(excel_path=EXCEL_PATH, out_base=BASE, dry_run=False):
    lock_files = find_lock_files(os.path.dirname(excel_path) or ".")
    if lock_files:
        raise SystemExit(
            "Trovati file di lock (Word/Excel aperti), fermo tutto senza toccare "
            "niente:\n  " + "\n  ".join(lock_files)
        )
    if not os.path.exists(excel_path):
        raise SystemExit(f"Excel non trovato: {excel_path}")

    loaded = load_workbook_rows(excel_path)
    nodes, off_record_stats = build_nodes(loaded)
    estratti_idx = build_estratti_index(loaded)
    metrics = build_metrics(nodes, loaded)

    print(f"nodi letti da iTOC: {len(nodes)}")
    print(f"coppie lette da Estratti: {len(loaded['estratti'])}")
    print(f"fonti lette da Fonti: {len(loaded['fonti'])}")
    print(f"righe DOSSIER lette: {len(loaded['dossier'])}")
    print(
        "blocchi [OFF-RECORD] rimossi — iTOC!F: "
        f"{off_record_stats['itoc_f_rimossi']}  ·  DOSSIER!O: "
        f"{off_record_stats['dossier_o_rimossi']}  ·  totale: "
        f"{off_record_stats['totale']}"
    )
    if off_record_stats["totale"] == 0:
        raise SystemExit(
            "ERRORE: zero blocchi [OFF-RECORD] rimossi. Il filtro non ha "
            "agganciato niente: o e' rotto, o qualcosa nell'Excel e' cambiato. "
            "Fermo l'ingest (§3 del prompt orchestratore)."
        )
    print(
        "blocchi [AUDIT ...] estratti in audit_aperto — perimetro: "
        f"{off_record_stats['audit_perimetro']}  ·  totale (perimetro + fuori "
        f"perimetro): {off_record_stats['audit_totale']}"
    )

    n_ammesse = sum(1 for n in nodes.values() if n["fonti_ammesse"])
    n_senza_desc_perimetro = sum(
        1 for n in nodes.values() if n["perimetro"] and not n["source_desc"]
    )
    print(f"nodi con almeno una fonte ammessa: {n_ammesse}")
    print(f"nodi in perimetro con Descrizione vuota: {n_senza_desc_perimetro}")

    if dry_run:
        print("\n--dry-run: nessun file scritto (build/, nodes/ invariati).")
        return

    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(NODES_DIR, exist_ok=True)

    nodes_json = {
        "words_per_page": WORDS_PER_PAGE,
        "words_per_page_band": list(WORDS_PER_PAGE_BAND),
        "generated_at": metrics["generated_at"],
        "nodes": nodes,
    }
    with open(BUILD_DIR + "nodes.json", "w", encoding="utf-8") as f:
        json.dump(nodes_json, f, ensure_ascii=False, indent=2)

    with open(BUILD_DIR + "estratti.json", "w", encoding="utf-8") as f:
        json.dump(estratti_idx, f, ensure_ascii=False, indent=2)

    with open(BUILD_DIR + "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    n_written = 0
    n_skipped = 0
    for idx in nodes:
        path = NODES_DIR + f"{idx}.md"
        if write_node_md(idx, path):
            n_written += 1
        else:
            n_skipped += 1
    print(f"\nnodes/*.md scritti: {n_written}  ·  gia' popolati (non toccati): {n_skipped}")
    print(f"scritto: {BUILD_DIR}nodes.json, {BUILD_DIR}estratti.json, {BUILD_DIR}metrics.json")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Ingest di iTOC master.xlsx (foglio DOSSIER) -> build/nodes.json, "
                     "build/estratti.json, build/metrics.json, nodes/<id>.md.")
    ap.add_argument("--excel", default=EXCEL_PATH, help="percorso dell'Excel (assoluto)")
    ap.add_argument("--dry-run", action="store_true",
                     help="sola lettura: stampa il report, non scrive build/ ne' nodes/")
    args = ap.parse_args(argv)
    try:
        run(excel_path=args.excel, dry_run=args.dry_run)
    except SystemExit:
        raise
    except Exception as e:  # qualunque altro errore: exit code diverso da zero
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
