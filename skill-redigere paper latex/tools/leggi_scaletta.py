#!/usr/bin/env python3
"""leggi_scaletta.py — dalla scaletta della repo (scaletta.md) al contratto per sezione.

    python3 tools/leggi_scaletta.py        # scrive build/sezioni.json e stampa i problemi

Legge il formato di `scaletta.md` cosi' com'e' (Role / Content / Sources / Numbers (log) /
Guardrails / Editorial notes / Claude's additions) e lo incrocia con:
- `input/piano.md` (pagine → parole obiettivo, floats della sezione);
- `routine validazione fonti/tabella.csv` (contesto sulle fonti: limiti, verbatim).

Cosa diventa materiale citabile (regola sovrana):
- `contenuto` = blocco Content (+ paragrafo d'apertura per le sezioni-cappello);
- `numeri_log` = blocco Numbers (log);
- `fonti` = le righe «`chiave`: tesi» del blocco Sources con la chiave in `fonti.bib`. La tesi
  della scaletta e' vincolante (ristretta sul txt dal gruppo il 16/11); l'estrazione del lettore
  della routine di validazione arriva al writer solo come contesto.
- `Claude's additions` resta fuori, a meno che `includi_aggiunte_claude` sia true.
- `Editorial notes` e `Guardrails` sono istruzioni per il writer, non materiale da affermare.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, cfg, chiavi_bib, die, p, scrivi_json, validazione  # noqa: E402
from piano import budget, leggi_piano  # noqa: E402

BLOCCHI = {
    "content": "contenuto",
    "sources": "sources",
    "numbers (log)": "numeri_log",
    "guardrails": "trappole",
    "editorial notes": "note_editoriali",
    "claude's additions": "aggiunte_claude",
}
SEZ_RE = re.compile(r"^(##|###)\s+(\d+(?:\.\d+)?)\b\s*(.*)$")
BLK_RE = re.compile(r"^#{3,4}\s+(.+?)\s*$")


def _pulisci_titolo(sid: str, resto: str) -> tuple[str, str]:
    t = resto.strip()
    if t.lower().startswith("(opening"):
        # «### 5 (opening, no x.y): How to read the coefficients»
        return sid, t.split(":", 1)[1].strip() if ":" in t else ""
    t = re.sub(r"\s*\((?:[^)]*\b(?:NEW|new|narrowed|was \d+|decided)\b[^)]*)\)\s*", " ", t).strip()
    return sid, t


def parse_scaletta(testo: str) -> list[dict]:
    sezioni: list[dict] = []
    cur = None
    blocco = None
    for riga in testo.splitlines():
        m = SEZ_RE.match(riga)
        if m:
            livello = 1 if m.group(1) == "##" else 2
            sid, titolo = _pulisci_titolo(m.group(2), m.group(3))
            opening = m.group(3).strip().lower().startswith("(opening")
            if opening and cur and cur["id"] == sid:
                # l'apertura della sezione-cappello scritta come ### : stessa sezione
                cur["titolo_apertura"] = titolo
                blocco = None
                continue
            cur = {"id": sid, "livello": livello, "titolo": titolo, "ruolo": "",
                   **{v: "" for v in BLOCCHI.values()}, "apertura": ""}
            sezioni.append(cur)
            blocco = None
            continue
        if riga.startswith("## ") and not SEZ_RE.match(riga):
            cur, blocco = None, None          # «## Claude's additions: for the next steps» ecc.
            continue
        if cur is None:
            continue
        mb = BLK_RE.match(riga)
        if mb and mb.group(1).lower() in BLOCCHI:
            blocco = BLOCCHI[mb.group(1).lower()]
            continue
        if mb:                                   # un ### di sottosezione non numerata
            blocco = None
            continue
        mw = re.match(r"^\*\*Words:\*\*\s*(\d+)", riga)
        if mw:
            cur["parole_appendice"] = int(mw.group(1))
            continue
        mr = re.match(r"^\*\*Role:\*\*\s*(.*)", riga)
        if mr:
            cur["ruolo"] = (cur["ruolo"] + " " + mr.group(1)).strip()
            continue
        mo = re.match(r"^\*\*Opening[^*]*\*\*\s*(.*)", riga)
        if mo:
            cur["apertura"] = mo.group(1).strip()
            continue
        if riga.strip() == "---":
            continue
        if blocco:
            cur[blocco] += riga + "\n"
    for s in sezioni:
        for k in list(BLOCCHI.values()) + ["apertura"]:
            s[k] = s[k].strip()
    return sezioni


def sources(blocco: str) -> list[tuple[list[str], str]]:
    """Righe «- `chiave`, `chiave2`: tesi» del blocco Sources. Le righe che non iniziano con
    una chiave (note, «None…», «(… removed)», decisioni D4) non sono fonti."""
    out = []
    for riga in blocco.splitlines():
        m = re.match(r"^\s*-\s+((?:`[a-z][a-z0-9]+\d{4}[a-z]?`(?:\s*,\s*|\s+and\s+)?)+)\s*:\s*(.+)$", riga)
        if m:
            out.append((re.findall(r"`([^`]+)`", m.group(1)), m.group(2).strip()))
    return out


def main():
    c = cfg()
    path = p("scaletta")
    if not path.exists():
        die(f"scaletta non trovata: {path}")
    sezioni = parse_scaletta(path.read_text(encoding="utf-8"))
    piano = leggi_piano()
    bud = budget(piano)
    bib = chiavi_bib()
    val = validazione()
    problemi = []

    for s in sezioni:
        sid = s["id"]
        # le sezioni-cappello hanno figli: il loro contenuto e' l'apertura
        s["ha_figli"] = any(x["id"].startswith(sid + ".") for x in sezioni)
        if s["ha_figli"] and not s["contenuto"]:
            s["contenuto"] = s["apertura"]
        if not c.get("includi_aggiunte_claude"):
            s.pop("aggiunte_claude", None)
        b = bud.get(sid)
        if b is None and s["ha_figli"] and not s["contenuto"]:
            b = {"parole": 0, "pagine": 0}             # cappello senza apertura: solo titolo
        if b is None:
            problemi.append(f"[{sid}] assente da piano.md: nessun budget di parole")
        s["parole"] = b["parole"] if b else 0
        s["pagine"] = b["pagine"] if b else 0
        s["floats"] = [f["id"] for f in piano["floats"] if f["dove"] == "corpo" and f["sezione"] == sid]

        # fonti: la tesi della scaletta e' VINCOLANTE (dal 16/11 tutte le tesi sono state
        # ristrette sul txt: scaletta, «Structural decisions» → Sources). La riga della
        # routine di validazione, se c'e', da' solo contesto (limiti, verbatim).
        fonti, scartate = [], []
        for chiavi, tesi in sources(s.pop("sources")):
            for k in chiavi:
                if k not in bib:
                    scartate.append(f"{k} (non in fonti.bib)")
                    continue
                righe = [r for r in val if r["id_fonte"] == k and r["sezione"] == sid] or \
                        [r for r in val if r["id_fonte"] == k]
                r = righe[0] if righe else {}
                fonti.append({
                    "chiave": k, "tesi": tesi, "co_citate": [x for x in chiavi if x != k],
                    "solo_rimando": bool(re.search(r"\b(pointer|as in \d|same tesi)", tesi, re.I)),
                    "estrazione_lettore": r.get("estrazione", ""), "forza": r.get("forza", ""),
                    "limiti_vs_noi": r.get("limiti_vs_noi", ""),
                    "citazione_verbatim": r.get("citazione", ""),
                    "esito_routine_16_11": r.get("esito", "nessuna riga"),
                })
        s["fonti"] = fonti
        s["fonti_ammesse"] = sorted({f["chiave"] for f in fonti})
        s["fonti_scartate"] = scartate
        if scartate:
            problemi.append(f"[{sid}] fonti non citabili: {'; '.join(scartate)}")
        materiale = len((s["contenuto"] + " " + s["numeri_log"]).split()) + sum(
            len(f["tesi"].split()) for f in fonti)
        s["parole_materiale"] = materiale
        if s["parole"] and not s["ha_figli"] and materiale / s["parole"] < 0.66:
            problemi.append(f"[{sid}] materiale {materiale} parole per {s['parole']} obiettivo: "
                            "uscira' corta (nessun pavimento)")
        if not s["contenuto"] and not s["ha_figli"]:
            problemi.append(f"[{sid}] nessun contenuto: la sezione non si puo' scrivere")

    # l'abstract ha un contratto proprio (i DRAFT); l'appendice e' gia' scritta
    ids = {s["id"] for s in sezioni}
    for sid in piano["sezioni"]:
        if sid not in ids and sid != "abstract":
            problemi.append(f"[{sid}] in piano.md ma non in scaletta.md")

    scrivi_json(BUILD / "sezioni.json", sezioni)
    print(f"{len(sezioni)} sezioni → build/sezioni.json")
    tot = sum(s["parole"] for s in sezioni)
    print(f"Parole obiettivo (senza abstract): {tot}")
    for x in problemi:
        print("  ⚠", x)


if __name__ == "__main__":
    main()
