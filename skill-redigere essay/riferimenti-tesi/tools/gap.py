#!/usr/bin/env python3
"""gap.py — il gap report di PROMPT-orchestratore-tesi.md §7: per capitolo,
struttura in pagine, capacita' in parole, materiale, `fit_ratio`, `regime`
(compressione/resa/espansione, §3); per nodo, `target_words` derivato (§4.1,
cinque passi); l'elenco dei nodi senza materiale, dei nodi bloccati da un
rilievo `[AUDIT ...]` bloccante e ancora aperto (§3), e le domande del GATE 1.

Uso:
    /usr/bin/python3 tools/gap.py                 # legge build/nodes.json se
                                                    # esiste, altrimenti cade
                                                    # sull'Excel (sola lettura)
    /usr/bin/python3 tools/gap.py --dry-run        # forza lettura diretta
                                                    # dall'Excel, non scrive
                                                    # reports/gap.md
    /usr/bin/python3 tools/gap.py --chapter 5      # solo un capitolo
    /usr/bin/python3 tools/gap.py --help

Non scrive mai sull'Excel. Con --dry-run non scrive nemmeno `reports/gap.md`:
solo stdout, per poter verificare le colonne senza toccare la pipeline.

Le funzioni di questo modulo sono importate da `lint_budget.py`, cosi' la
derivazione di `target_words` vive in un solo posto.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

BASE = ingest.BASE
EXCEL_PATH = ingest.EXCEL_PATH
BUILD_DIR = ingest.BUILD_DIR
REPORTS_DIR = ingest.REPORTS_DIR
WORDS_PER_PAGE = ingest.WORDS_PER_PAGE
PERIMETRO_CAPITOLI = ingest.PERIMETRO_CAPITOLI  # {'0'..'6'}: il Cap. 7 resta fuori

# --------------------------------------------------------------------------
# costanti calibrate — struttura in pagine dei titoli
# --------------------------------------------------------------------------
# Non c'e' un renderer da riga di comando (§9): il conteggio esatto delle
# righe fisiche di un titolo dipenderebbe dai glifi reali di Arial grassetto
# nello specchio del template, che qui non possiamo misurare a ogni giro.
# Queste due costanti sono calibrate UNA VOLTA sulla misura nota e dichiarata
# in PROMPT-orchestratore-tesi.md §3 (2026-09-07): 100 titoli in perimetro,
# 115 righe fisiche (15 vanno a capo), 4,94 pagine. Verificato che con questa
# soglia si riproduce ESATTAMENTE 15 titoli a capo su 100 e 115 righe totali
# in aggregato sui dati reali di iTOC (scarto di ±1 riga su 2 capitoli su 7,
# che si compensano nel totale — inevitabile con un conteggio a caratteri
# invece che sui glifi veri). Se il template cambia, ricalibrare: rifare la
# procedura di §10 e aggiornare queste due costanti.
TITLE_CHARS_PER_LINE = 80
TITLE_PP_PER_LINE = 4.94 / 115  # ≈ 0.043 pagine per riga fisica di titolo

# "code non riempite" da pageBreakBefore su Heading1: §3 le stima a 0-1
# pagina per capitolo, attesa ~3,5 pagine sui 7 capitoli in perimetro.
# Dichiarata, non dedotta dalla capacita' (§3: "le capacita' ... non
# deducono le code ... ogni ratio riportato e' ottimistico"): qui la
# riportiamo solo come nota, non la sottraiamo da C_c.
TAIL_PP_PER_CHAPTER = 3.5 / 7

STRUTTURA_SOGLIA = 0.45  # struttura_pp(c) > 0.45 * budget_pp(c) => capienza rotta

# Il clip superiore e' 1,49 e non 1,50 perche' 1,50 e' il confine che
# `classifica_fit` assegna a `BLOCCATO IN ESPANSIONE`, e `clip` restituisce il
# bound: un capitolo con k_c >= 1,50 schiacciava OGNI suo nodo non vincolato
# esattamente sul confine, e il classificatore li dichiarava tutti in stato di
# errore -- cioe' `target_words = 0`, "non si scrive". Succedeva sul Cap. 6
# (k_c = 1,536): il nodo `6.4` chiedeva 237 parole contro 158 di materiale e
# risultava bloccato, pur non avendo nulla che non andasse. Il clip e il
# classificatore devono stare dalla stessa parte del proprio confine.
CLIP_LOW, CLIP_HIGH = 0.55, 1.49

# [DECISIONE AUTORE 2026-09-08] "1 riga:" nel campo Ruolo e' una specifica di
# lunghezza, non l'enunciato del ruolo, e vale 130 parole: circa nove righe di
# questo template (13,84 parole per riga). Il numero e' stato scelto perche' e'
# l'unico che rende coerenti le due decisioni dello stesso giorno: toglie al
# Cap. 5 le ~2.350 parole che il budget di 13 pagine gia' richiedeva, e porta
# la tesi a ~33,5 pagine contro 36 di budget, lasciando margine alle citazioni
# APA e alle tabelle che ancora non esistono.
# Fuori dal Cap. 5 il tetto quasi non morde: e' una decisione sul capitolo del
# caso, non sulla tesi intera.
TETTO_1RIGA = 130
CLIP_HIGH_CAPPELLO = 1.20

FIT_CLASSI = [
    (0.0, 0.55, "BLOCCATO IN COMPRESSIONE"),
    (0.55, 0.85, "compressione"),
    (0.85, 1.20, "resa diretta"),
    (1.20, 1.50, "espansione"),
    (1.50, math.inf, "BLOCCATO IN ESPANSIONE"),
]

# §3: 'regime' prende UNO di tre valori — compressione, resa, espansione — mai
# un quarto: i due estremi della classe (i BLOCCATO...) non sono regimi, sono
# stati (il nodo va a RICHIESTA AUTORE con target_words=0), quindi non compaiono
# qui e chi legge REGIME_DA_CLASSE.get(classe) con default None lo riconosce.
REGIME_DA_CLASSE = {
    "compressione": "compressione",
    "resa diretta": "resa",
    "espansione": "espansione",
}


def classifica_fit(fit_ratio):
    for lo, hi, nome in FIT_CLASSI:
        if lo <= fit_ratio < hi:
            return nome
    return "BLOCCATO IN ESPANSIONE"  # fit_ratio >= ultima soglia (math.inf non e' mai raggiunta sopra)


def regime_da_fit(fit_ratio):
    """§3/§7: regime a tre valori, derivato dalla stessa classifica_fit gia'
    corretta (5 classi). None per i due estremi: sono stati, non regimi."""
    return REGIME_DA_CLASSE.get(classifica_fit(fit_ratio))


# --------------------------------------------------------------------------
# foglio AUDIT 2026-09-07 — lookup per il blocco dei nodi con audit_aperto (§3)
# --------------------------------------------------------------------------

AUDIT_SHEET_NAME = "AUDIT 2026-09-07"
AUDIT_ID_RE = re.compile(r"\b[A-Z]{2,3}-\d{2}\b")


def load_audit_sheet(excel_path=EXCEL_PATH):
    """Legge, sola lettura, il foglio `AUDIT 2026-09-07`, indicizzato per
    `ID` (es. 'CL-06', 'ST-04'). Serve solo al lookup del §3: quali rilievi
    sono 'bloccante' e ancora 'aperto'. Non e' fra i fogli richiesti da
    `ingest.load_workbook_rows` (che carica solo iTOC/DOSSIER/Fonti/Estratti):
    lo leggiamo qui perche' la regola vive solo in gap.py (§3, correzione 2)."""
    import openpyxl

    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    if AUDIT_SHEET_NAME not in wb.sheetnames:
        return {}
    rr = [list(r) for r in wb[AUDIT_SHEET_NAME].iter_rows(values_only=True)]
    if not rr:
        return {}
    hdr = [str(h) if h is not None else "" for h in rr[0]]
    out = {}
    for r in rr[1:]:
        d = dict(zip(hdr, r))
        aid = ingest.clean(d.get("ID"))
        if aid:
            out[aid] = {
                "priorita": ingest.clean(d.get("Priorità")),
                "stato_lavorazione": ingest.clean(d.get("Stato lavorazione")),
            }
    return out


def nodi_bloccati_da_audit(nodes, audit_by_id):
    """§3: estrae dal campo `audit_aperto` di ogni nodo gli id dei rilievi
    (`CL-06`, `ST-04`, ...) e li cerca in `audit_by_id`. Se almeno uno ha
    Priorita='bloccante' e Stato lavorazione='aperto', il nodo e' bloccato:
    non si scrive, va a RICHIESTA AUTORE. Ritorna {id_nodo: [id_rilievo, ...]}
    con i soli id effettivamente bloccanti (non tutti gli id citati)."""
    out = {}
    for nid, n in nodes.items():
        aa = n.get("audit_aperto") or ""
        if not aa:
            continue
        ids_citati = AUDIT_ID_RE.findall(aa)
        bloccanti = [
            rid for rid in ids_citati
            if rid in audit_by_id
            and audit_by_id[rid]["priorita"].strip().lower() == "bloccante"
            and audit_by_id[rid]["stato_lavorazione"].strip().lower() == "aperto"
        ]
        if bloccanti:
            out[nid] = bloccanti
    return out


def is_1riga(ruolo):
    return bool(ruolo) and ruolo.strip().lower().startswith("1 riga")


def is_deve_dimostrare(ruolo):
    return "deve dimostrare" in (ruolo or "").lower()


# --------------------------------------------------------------------------
# caricamento nodi
# --------------------------------------------------------------------------

def load_nodes(excel_path=EXCEL_PATH, force_excel=False):
    """Ritorna (nodes_dict, sorgente_label). Preferisce build/nodes.json se
    esiste ed e' leggibile; altrimenti (o con force_excel) ricalcola al volo
    dall'Excel con ingest.build_nodes — sola lettura, non scrive niente."""
    nodes_json_path = BUILD_DIR + "nodes.json"
    if not force_excel and os.path.exists(nodes_json_path):
        with open(nodes_json_path, encoding="utf-8") as f:
            data = json.load(f)
        return data["nodes"], "build/nodes.json"
    loaded = ingest.load_workbook_rows(excel_path)
    nodes, _ = ingest.build_nodes(loaded)
    return nodes, "Excel (fallback, build/nodes.json assente o --dry-run)"


def load_budget_pp(excel_path=EXCEL_PATH):
    loaded = ingest.load_workbook_rows(excel_path)
    return ingest.budget_pp_by_chapter(loaded["itoc"])


# --------------------------------------------------------------------------
# struttura e capacita' per capitolo
# --------------------------------------------------------------------------

def chapter_struttura_pp(nodes, chapter):
    """Righe fisiche stimate dei titoli del capitolo (numerazione inclusa) e
    pagine equivalenti, con le costanti calibrate sopra."""
    righe = 0
    n_titoli = 0
    for n in nodes.values():
        if n["chapter"] != chapter:
            continue
        n_titoli += 1
        prefix_len = len(n["id"]) + 1  # 'N.N.N ' incluso lo spazio
        L = prefix_len + len(n["title"] or "")
        righe += max(1, math.ceil(L / TITLE_CHARS_PER_LINE))
    pp = righe * TITLE_PP_PER_LINE
    return n_titoli, righe, pp


def chapter_metrics(nodes, chapter, budget_pp_map):
    n_titoli, righe, struttura_pp = chapter_struttura_pp(nodes, chapter)
    budget_pp = budget_pp_map.get(chapter)
    chapter_nodes = [n for n in nodes.values() if n["chapter"] == chapter]
    n_foglie = sum(1 for n in chapter_nodes if n["is_leaf"])
    M_c = sum(n["source_words"] for n in chapter_nodes if n["source_words"] > 0)
    C_c = None
    k_c = None
    if budget_pp is not None:
        C_c = (budget_pp - struttura_pp) * WORDS_PER_PAGE
        k_c = (C_c / M_c) if M_c > 0 else None
    capienza_rotta = (budget_pp is not None) and (struttura_pp > STRUTTURA_SOGLIA * budget_pp)
    return {
        "capitolo": chapter,
        "n_nodi": len(chapter_nodes),
        "n_foglie": n_foglie,
        "righe_titoli": righe,
        "struttura_pp": round(struttura_pp, 3),
        "tail_pp_stimata": round(TAIL_PP_PER_CHAPTER, 3),
        "budget_pp": budget_pp,
        "capacita_parole_C_c": round(C_c, 1) if C_c is not None else None,
        "materiale_parole_M_c": M_c,
        "k_c": round(k_c, 4) if k_c is not None else None,
        "capienza_strutturale_rotta": capienza_rotta,
    }


# --------------------------------------------------------------------------
# derivazione target_words — §4.1, cinque passi
# --------------------------------------------------------------------------

def clip(t, lo, hi):
    return max(lo, min(hi, t))


# Un residuo POSITIVO di capitolo significa che il budget in pagine e' piu'
# capiente del materiale. Spalmarlo senza tetto sui nodi non vincolati produce
# target che chiedono di scrivere piu' di quanto la `Descrizione` contenga --
# e la regola sovrana vieta di aggiungere affermazioni che nel materiale non
# ci sono. Succedeva davvero: nel Cap. 6 il nodo `6.4` riceveva 355 parole di
# target contro 158 di materiale (fit 2,25), cioe' lo stato che questo stesso
# modulo classifica `BLOCCATO IN ESPANSIONE`, prodotto dalla redistribuzione
# invece che dai dati.
#
# Il tetto e' il limite superiore della classe `espansione`: oltre 1,50 non c'e'
# un regime piu' ampio, c'e' uno stato di errore. Si riempie a livelli (chi e'
# gia' al tetto esce dal giro e il resto si ridistribuisce fra gli altri) e cio'
# che nessuno puo' assorbire **resta non allocato**: il capitolo esce piu' corto
# del budget, il che e' un fatto da riportare, non da correggere gonfiando.
# Il tetto e' lo stesso CLIP_HIGH: un solo numero, un solo posto.


def _redistribuisci(result, residuo):
    """Distribuisce `residuo` sui nodi non vincolati senza superare il tetto.

    Ritorna la quota che nessun nodo poteva assorbire (0.0 se e' entrata tutta).
    Un residuo negativo non ha tetto: comprimere e' sempre possibile, ed e'
    il caso del Cap. 5.
    """
    if residuo < 0:
        base = sum(v["b_i"] for v in result.values() if not v["vincolato"])
        if base:
            for v in result.values():
                if not v["vincolato"]:
                    v["t_i"] += residuo * (v["b_i"] / base)
        return 0.0

    resto = residuo
    for _ in range(50):  # in pratica bastano pochi giri: uno per ogni livello
        aperti = [v for v in result.values()
                  if not v["vincolato"] and v["t_i"] < CLIP_HIGH * v["b_i"] - 1e-9]
        base = sum(v["b_i"] for v in aperti)
        if resto <= 1e-6 or not base:
            break
        dato = 0.0
        for v in aperti:
            quota = resto * (v["b_i"] / base)
            spazio = CLIP_HIGH * v["b_i"] - v["t_i"]
            preso = min(quota, spazio)
            v["t_i"] += preso
            dato += preso
        if dato <= 1e-9:
            break
        resto -= dato
    return max(resto, 0.0)


def derive_targets_for_chapter(nodes, chapter, k_c, audit_bloccati=None):
    """Passi 1-5 di §4.1 sui nodi del capitolo con source_words > 0.
    Ritorna {id: {"target_words":..., "vincolato": bool, "nota": str,
    "conflitto_ruolo": bool}}. Se k_c e' None (nessun materiale o nessun
    budget), non deriva niente: i chiamanti devono controllare prima.

    `audit_bloccati` (§3, correzione 2): {id_nodo: [id_rilievo, ...]} dei nodi
    con un rilievo [AUDIT ...] bloccante e aperto. Quei nodi non ricevono un
    target derivato dalla scalatura: restano a target_words=0, come i nodi
    senza materiale, e il loro b_i non entra nella redistribuzione fra i nodi
    non vincolati (cosi' la somma resta coerente con C_c)."""
    audit_bloccati = audit_bloccati or {}
    result = {}
    chapter_nodes = [n for n in nodes.values() if n["chapter"] == chapter and n["source_words"] > 0]

    unvincolati_b = 0.0
    for n in chapter_nodes:
        b_i = n["source_words"]
        ruolo = n["ruolo"] or ""
        nota = ""
        conflitto = False
        if n["id"] in audit_bloccati:
            t_i = 0.0
            vincolato = True
            rilievi = ", ".join(audit_bloccati[n["id"]])
            nota = (f"⚠ RICHIESTA AUTORE — bloccato da audit_aperto ({rilievi}, "
                    "bloccante+aperto in AUDIT 2026-09-07): non si scrive")
        elif is_1riga(ruolo) and b_i <= 70:
            t_i = float(b_i)
            vincolato = True
            # NON scrivere qui "banda 40-70": era la regola vecchia, quella
            # che [DECISIONE AUTORE 2026-09-08] ha sostituito col tetto a 130.
            # Oggi per questi nodi il target E' il materiale (t_i = b_i) e la
            # banda e' il +-15% attorno ad esso, come per ogni altro nodo. La
            # nota stale e' stata usata da un agente per giustificare 70 parole
            # su 53 di materiale, cioe' un'espansione del 32% presentata come
            # dentro banda.
            nota = ("1 riga: con materiale <= 70 parole: target = materiale, "
                    "escluso dalla scalatura di capitolo e dalla redistribuzione "
                    "del residuo")
        elif is_1riga(ruolo) and b_i > 70:
            # tetto duro: il Ruolo vince sul budget, e non entra nella
            # redistribuzione del residuo di capitolo.
            t_i = float(min(b_i, TETTO_1RIGA))
            vincolato = True
            conflitto = b_i > TETTO_1RIGA
            if conflitto:
                nota = (f"1 riga: tetto {TETTO_1RIGA} parole applicato — "
                        f"{b_i - TETTO_1RIGA} parole di Descrizione non entrano in prosa")
            else:
                nota = f"1 riga: sotto il tetto di {TETTO_1RIGA}, target = materiale"
        elif is_deve_dimostrare(ruolo):
            t_i = clip(b_i * k_c, CLIP_LOW * b_i, CLIP_HIGH * b_i)
            vincolato = False
        elif not n["is_leaf"]:
            # cappello: introduce e basta, clip superiore piu' stretto
            t_i = clip(b_i * k_c, CLIP_LOW * b_i, CLIP_HIGH_CAPPELLO * b_i)
            vincolato = False
        else:
            t_i = clip(b_i * k_c, CLIP_LOW * b_i, CLIP_HIGH * b_i)
            vincolato = False
        if not vincolato:
            unvincolati_b += b_i
        result[n["id"]] = {
            "b_i": b_i, "t_i": t_i, "vincolato": vincolato,
            "conflitto_ruolo": conflitto, "nota": nota,
        }

    C_c = k_c * sum(n["source_words"] for n in chapter_nodes)
    somma_t = sum(v["t_i"] for v in result.values())
    residuo = C_c - somma_t
    residuo_pct = abs(residuo) / C_c if C_c else 0.0
    blocco_capitolo = False
    non_allocato = 0.0
    if abs(residuo) > 1e-6:
        if unvincolati_b > 0:
            non_allocato = _redistribuisci(result, residuo)
        elif residuo < 0 and residuo_pct > 0.05:
            # solo un residuo NEGATIVO che nessun nodo puo' assorbire e' un
            # blocco: significa che i target vincolati non ci stanno nel
            # budget. Un residuo positivo vuol dire soltanto che il capitolo
            # esce piu' corto del budget, e va riportato, non bloccato.
            blocco_capitolo = True

    for v in result.values():
        tw = round(v["t_i"])
        # su un nodo piccolo il round puo' riscavalcare il tetto: con 30 parole
        # di materiale, 1,49*30 = 44,7 arrotonda a 45 e il fit torna esattamente
        # 1,50, cioe' di nuovo lo stato di errore. Sopra il tetto si arrotonda
        # per difetto. (Capitava a `7.1.4`.)
        if not v["vincolato"] and v["b_i"]:
            tw = min(tw, math.floor(CLIP_HIGH * v["b_i"]))
        v["target_words"] = tw
    return result, {"residuo": round(residuo, 1), "residuo_pct": round(residuo_pct, 4),
                     "blocco_capitolo": blocco_capitolo,
                     "residuo_non_allocato": round(non_allocato, 1)}


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def build_report(nodes, budget_pp_map, only_chapter=None, audit_by_id=None):
    chapters = sorted(PERIMETRO_CAPITOLI, key=lambda c: int(c))
    if only_chapter is not None:
        chapters = [c for c in chapters if c == str(only_chapter)]

    audit_by_id = audit_by_id or {}
    audit_bloccati = nodi_bloccati_da_audit(nodes, audit_by_id)

    lines = []
    per_capitolo = {}
    nodi_report = {}
    nodi_senza_materiale = []
    nodi_audit_bloccati = {}
    conflitti_ruolo = []

    for c in chapters:
        cm = chapter_metrics(nodes, c, budget_pp_map)
        per_capitolo[c] = cm

        chapter_nodes = [n for n in nodes.values() if n["chapter"] == c]
        for n in chapter_nodes:
            if n["perimetro"] and n["source_words"] == 0:
                nodi_senza_materiale.append(n["id"])
            if n["perimetro"] and n["id"] in audit_bloccati:
                nodi_audit_bloccati[n["id"]] = audit_bloccati[n["id"]]

        if cm["k_c"] is None or cm["budget_pp"] is None:
            continue  # niente materiale o budget non trovato: nessun target derivabile

        targets, residuo_info = derive_targets_for_chapter(nodes, c, cm["k_c"], audit_bloccati)
        cm["residuo_parole"] = residuo_info["residuo"]
        cm["residuo_pct"] = residuo_info["residuo_pct"]
        cm["blocco_capitolo_residuo"] = residuo_info["blocco_capitolo"]
        # solo il lato compressione e' un blocco: vedi la nota in lint_budget.py
        cm["capitolo_bloccato_k"] = cm["k_c"] < CLIP_LOW
        cm["capienza_in_avanzo"] = cm["k_c"] > CLIP_HIGH

        for nid, v in targets.items():
            b_i = v["b_i"]
            if v["conflitto_ruolo"]:
                conflitti_ruolo.append(nid)
            if nid in audit_bloccati:
                # §3: bloccato da un [AUDIT ...] bloccante+aperto — non e' un
                # regime, e' lo stato RICHIESTA AUTORE, target_words=0.
                nodi_report[nid] = {
                    "capitolo": c,
                    "is_leaf": nodes[nid]["is_leaf"],
                    "source_words": b_i,
                    "target_words": 0,
                    "fit_ratio": 0.0,
                    "classe": "⚠ RICHIESTA AUTORE (audit bloccante aperto)",
                    "regime": None,
                    "conflitto_ruolo": v["conflitto_ruolo"],
                    "nota": v["nota"],
                }
                continue
            fit_ratio = v["target_words"] / b_i if b_i else 0.0
            if v["conflitto_ruolo"]:
                # Il tetto "1 riga:" e' una decisione dell'autore, non un
                # sintomo di budget insufficiente: non va classificato come
                # BLOCCATO IN COMPRESSIONE, che significherebbe "non si
                # scrive". Il nodo si scrive, ma il writer deve dichiarare
                # cosa lascia fuori: e' selezione, non compressione.
                classe = f"tetto 1 riga (-{b_i - v['target_words']} parole)"
            else:
                classe = classifica_fit(fit_ratio)
            nodi_report[nid] = {
                "capitolo": c,
                "is_leaf": nodes[nid]["is_leaf"],
                "source_words": b_i,
                "target_words": v["target_words"],
                "fit_ratio": round(fit_ratio, 3),
                "classe": classe,
                "regime": regime_da_fit(fit_ratio),
                "conflitto_ruolo": v["conflitto_ruolo"],
                "nota": v["nota"],
            }

    return {
        "per_capitolo": per_capitolo,
        "nodi": nodi_report,
        "nodi_senza_materiale": sorted(set(nodi_senza_materiale)),
        "nodi_audit_bloccati": dict(sorted(nodi_audit_bloccati.items())),
        "conflitti_ruolo": sorted(set(conflitti_ruolo)),
    }


def gate1_domande(report):
    n_conflitti = len(report["conflitti_ruolo"])
    parole_conflitto = sum(
        report["nodi"][nid]["source_words"] - min(70, report["nodi"][nid]["source_words"])
        for nid in report["conflitti_ruolo"] if nid in report["nodi"]
    )
    domande = [
        "1. il budget di pagine per capitolo: l'allocazione attuale (Budget pp in iTOC) "
        "resta quella su cui misurare, o l'autore vuole approvare una riallocazione? "
        "Nessuno script la modifica da solo.",
        f"2. 'Ruolo' = '1 riga:' — e' una specifica di lunghezza o l'enunciato del ruolo? "
        f"{n_conflitti} nodi in conflitto (Ruolo '1 riga:' con Descrizione oltre 70 parole), "
        f"~{parole_conflitto} parole eccedenti il tetto di 70 (proxy, non il conteggio esatto "
        "di una eventuale versione precedente). Default finche' non risponde: NON troncare.",
        "3. dove vivono abstract, introduzione e reference list — nodi nuovi in iTOC creati "
        "dall'autore, o appendice tecnica esente dal divieto di §11? Senza risposta la "
        "pipeline non assembla.",
        "4. il taglio del Cap. 5 (o di ogni altro capitolo bloccato in compressione, vedi "
        "sotto): quali affermazioni sopravvivono, proposto per nodo e approvato dall'autore "
        "prima di /tesi-draft su quel capitolo.",
    ]
    if report["nodi_audit_bloccati"]:
        elenco = "; ".join(
            f"{nid} ({', '.join(rilievi)})"
            for nid, rilievi in report["nodi_audit_bloccati"].items()
        )
        domande.append(
            f"5. {len(report['nodi_audit_bloccati'])} nodi hanno un rilievo [AUDIT ...] "
            f"ancora 'bloccante' e 'aperto' nel foglio AUDIT 2026-09-07, quindi non si "
            f"scrivono finche' l'autore non decide (vedi sezione 'Nodi bloccati da "
            f"audit_aperto'): {elenco}."
        )
    return domande


def format_report(report, sorgente):
    out = []
    out.append("# Gap report\n")
    out.append(f"(fonte dati nodi: {sorgente})\n")
    out.append("\n## Per capitolo\n")
    out.append("| Cap | Nodi | Foglie | Righe tit. | Strutt. pp | Budget pp | "
                "Capacita' C_c | Materiale M_c | k_c | Regime | Note |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c, cm in report["per_capitolo"].items():
        note = []
        if cm["capienza_strutturale_rotta"]:
            note.append(f"CAPIENZA STRUTTURALE ROTTA (>{int(STRUTTURA_SOGLIA*100)}% del budget)")
        if cm.get("capitolo_bloccato_k"):
            note.append(f"BLOCCATO IN COMPRESSIONE (k_c={cm['k_c']})")
        elif cm.get("capienza_in_avanzo"):
            note.append(f"capienza in avanzo (k_c={cm['k_c']}), non un blocco")
        if cm.get("blocco_capitolo_residuo"):
            note.append(f"residuo oltre ±5% di C_c ({cm.get('residuo_pct',0)*100:.1f}%)")
        regime = "-"
        if cm["k_c"] is not None:
            # §3/§7: tre valori (compressione/resa/espansione), riusando la
            # stessa classifica_fit a 5 classi del livello nodo; i due estremi
            # non sono un regime, sono lo stato BLOCCATO gia' segnalato sopra.
            regime = regime_da_fit(cm["k_c"]) or classifica_fit(cm["k_c"])
        out.append(
            f"| {c} | {cm['n_nodi']} | {cm['n_foglie']} | {cm['righe_titoli']} | "
            f"{cm['struttura_pp']} | {cm['budget_pp']} | {cm['capacita_parole_C_c']} | "
            f"{cm['materiale_parole_M_c']} | {cm['k_c']} | {regime} | "
            f"{'; '.join(note) or '-'} |"
        )
    out.append(
        f"\n(tail non dedotta dalla capacita', ~{TAIL_PP_PER_CHAPTER:.2f} pp/capitolo attesa "
        "dal pageBreakBefore di ogni Heading1 — §3: le capacita' qui sopra sono un limite "
        "superiore, ogni ratio e' ottimistico)\n"
    )

    out.append("\n## Per nodo foglia\n")
    out.append("| Nodo | source_words | target_words | fit_ratio | classe | conflitto ruolo |")
    out.append("|---|---|---|---|---|---|")
    for nid, v in sorted(report["nodi"].items(), key=lambda kv: tuple(
            int(p) for p in kv[0].split("."))):
        if not v["is_leaf"]:
            continue
        out.append(
            f"| {nid} | {v['source_words']} | {v['target_words']} | {v['fit_ratio']} | "
            f"{v['classe']} | {'SI' if v['conflitto_ruolo'] else ''} |"
        )

    out.append("\n## Nodi senza materiale (Descrizione vuota, in perimetro)\n")
    if report["nodi_senza_materiale"]:
        for nid in report["nodi_senza_materiale"]:
            out.append(f"- {nid}  → target_words=0, stato ⚠ RICHIESTA AUTORE, non passare al writer")
    else:
        out.append("(nessuno)")

    out.append("\n## Nodi bloccati da audit_aperto (rilievo bloccante e ancora aperto)\n")
    if report["nodi_audit_bloccati"]:
        for nid, rilievi in report["nodi_audit_bloccati"].items():
            out.append(
                f"- {nid}  ({', '.join(rilievi)})  → target_words=0, stato ⚠ RICHIESTA "
                "AUTORE, non passare al writer — vedi AUDIT 2026-09-07"
            )
    else:
        out.append("(nessuno)")

    out.append("\n## Conflitto Ruolo/materiale ('1 riga:' con Descrizione > 70 parole)\n")
    if report["conflitti_ruolo"]:
        for nid in report["conflitti_ruolo"]:
            out.append(f"- {nid}")
    else:
        out.append("(nessuno)")

    out.append("\n## Domande del GATE 1\n")
    for d in gate1_domande(report):
        out.append(d)

    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def run(dry_run=False, chapter=None, excel_path=EXCEL_PATH):
    force_excel = dry_run
    nodes, sorgente = load_nodes(excel_path=excel_path, force_excel=force_excel)
    budget_pp_map = load_budget_pp(excel_path)
    audit_by_id = load_audit_sheet(excel_path)
    report = build_report(nodes, budget_pp_map, only_chapter=chapter, audit_by_id=audit_by_id)
    text = format_report(report, sorgente)
    print(text)
    if not dry_run:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        with open(REPORTS_DIR + "gap.md", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nscritto: {REPORTS_DIR}gap.md")
    else:
        print("\n--dry-run: reports/gap.md non scritto.")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Gap report §7: struttura/capacita'/materiale per capitolo, "
                     "target_words e fit_ratio per nodo, nodi senza materiale, "
                     "domande GATE 1.")
    ap.add_argument("--excel", default=EXCEL_PATH, help="percorso dell'Excel (assoluto)")
    ap.add_argument("--dry-run", action="store_true",
                     help="legge direttamente dall'Excel (ignora build/nodes.json) "
                          "e non scrive reports/gap.md: solo stdout")
    ap.add_argument("--chapter", default=None, help="limita il report a un solo capitolo (es. 5)")
    args = ap.parse_args(argv)
    try:
        run(dry_run=args.dry_run, chapter=args.chapter, excel_path=args.excel)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
