#!/usr/bin/env python3
"""Legge `scaletta/scaletta.md` e produce `build/sezioni.json` + `reports/scaletta.md`.

E' l'equivalente di `ingest.py` + `gap.py` della tesi, dove la scaletta era un
Excel di 129 nodi. Qui e' un markdown scritto dall'autore (con Claude, passo per
passo). La scaletta e' il CONTRATTO del testo: la regola sovrana dice che la prosa
di una sezione non contiene nulla che non stia nel suo `contenuto` o nei `punti`
che elenca. Per questo la sintassi e' rigida quanto basta a essere letta da uno
script.

Sintassi (vedi `scaletta/scaletta.md` per l'esempio completo):

    # Titolo dell'essay                      <- opzionale
    ## 1 Introduzione                        <- livello 1: "## <id> <titolo>"
    parole: 250
    ruolo: deve dimostrare che ...           <- cosa la sezione deve ottenere
    punti: akerlof1970#2, spence1973#1       <- materiale dalle fonti validate
    aggancio: verso 2, dal problema alla ... <- transizione richiesta al writer
    trappole: non dire che ...               <- rischi da evitare, checklist dell'auditor
    Testo libero dell'autore: idee, argomenti, esempi, in qualunque forma.
    Tutto quello che non e' un campo e' `contenuto`, cioe' materiale.
    ### 1.1 Sottosezione                     <- livello 2;  #### = livello 3

L'id e' il primo token del titolo (`1`, `2.3`, `intro`). I commenti <!-- --> sono
ignorati. Un campo puo' essere preceduto da "- ".

Controlli (finding nel report, exit 2 se c'e' un HIGH):
  - id duplicati o titolo senza id;
  - punti che non esistono in build/estratti.json (= non validati);
  - punti da fonti senza voce nel .bib (citabili solo dopo averla aggiunta);
  - sezioni senza materiale (ne' contenuto ne' punti): il writer non potra' scriverle;
  - rapporto materiale/parole: se il materiale e' molto meno del target la sezione
    uscira' corta, perche' il writer non riempie (non esiste un pavimento di parole);
  - somma delle parole contro `parole_totali` di progetto.json.

Uso:
    python3 tools/scaletta/leggi_scaletta.py
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

CAMPI = {"parole", "ruolo", "punti", "aggancio", "trappole", "escludi"}
TITOLO = re.compile(r"^(#{1,4})\s+(.*\S)\s*$")
CAMPO = re.compile(r"^\s*(?:[-*]\s+)?(\w+)\s*:\s*(.*)$")
# sotto questa frazione di materiale rispetto al target la sezione esce corta:
# e' il limite inferiore del regime di espansione della tesi (fit_ratio 1,50)
RAPPORTO_MIN = 0.66


def leggi(testo: str) -> tuple[str, list[dict], list[str]]:
    testo = re.sub(r"<!--.*?-->", "", testo, flags=re.S)
    titolo_doc, sezioni, problemi = "", [], []
    corrente = None
    pila: list[tuple[int, str]] = []
    for riga in testo.splitlines():
        m = TITOLO.match(riga)
        if m:
            liv = len(m.group(1)) - 1
            if liv == 0:
                titolo_doc = m.group(2)
                corrente = None
                continue
            tok, _, resto = m.group(2).partition(" ")
            sid = tok.rstrip(".")
            if not resto.strip():
                problemi.append(f"[HIGH] titolo «{m.group(2)}» senza id: scrivi «{'#' * (liv + 1)} <id> <titolo>»")
                corrente = None
                continue
            while pila and pila[-1][0] >= liv:
                pila.pop()
            corrente = {"id": sid, "livello": liv, "titolo": resto.strip(),
                        "parent": pila[-1][1] if pila else None, "ordine": len(sezioni),
                        "parole_target": 0, "ruolo": "", "punti": [], "aggancio": "",
                        "trappole": "", "escludi": False, "_contenuto": []}
            pila.append((liv, sid))
            sezioni.append(corrente)
            continue
        if corrente is None:
            continue
        c = CAMPO.match(riga)
        if c and c.group(1).lower() in CAMPI:
            k, v = c.group(1).lower(), c.group(2).strip()
            if k == "parole":
                n = re.sub(r"\D", "", v)
                corrente["parole_target"] = int(n) if n else 0
            elif k == "punti":
                corrente["punti"] += [p.strip() for p in re.split(r"[,;\s]+", v) if p.strip()]
            elif k == "escludi":
                corrente["escludi"] = v.lower() in ("si", "sì", "yes", "true", "1")
            else:
                corrente[k] = (corrente[k] + " " + v).strip()
        else:
            corrente["_contenuto"].append(riga)
    for s in sezioni:
        s["contenuto"] = "\n".join(s.pop("_contenuto")).strip()
    return titolo_doc, sezioni, problemi


def main() -> int:
    if not comune.SCALETTA.exists():
        print(f"ERRORE: manca {comune.rel(comune.SCALETTA)}.")
        return 1
    cfg = comune.config()
    titolo_doc, sezioni, problemi = leggi(comune.SCALETTA.read_text(encoding="utf-8"))
    avvisi = []

    try:
        est = comune.estratti()
        punti, fonti = est["punti"], est["fonti"]
    except SystemExit:
        punti, fonti = {}, {}
        avvisi.append("build/estratti.json non esiste ancora: i `punti` non sono verificabili. "
                      "Va bene solo se l'essay non usa fonti.")

    visti = set()
    for s in sezioni:
        if s["id"] in visti:
            problemi.append(f"[HIGH] id «{s['id']}» duplicato")
        visti.add(s["id"])
        ok_punti = []
        for p in s["punti"]:
            if punti and p not in punti:
                problemi.append(f"[HIGH] {s['id']}: punto «{p}» non validato (non e' in build/estratti.json)")
            else:
                ok_punti.append(p)
        s["punti"] = ok_punti
        s["fonti_ammesse"] = sorted({p.split("#")[0] for p in ok_punti})
        for f in s["fonti_ammesse"]:
            if fonti.get(f, {}).get("nel_bib") is False:
                avvisi.append(f"{s['id']}: la fonte {f} non ha voce in fonti/fonti.bib")
        mat = comune.conta_parole(s["contenuto"]) + sum(
            comune.conta_parole(punti[p]["cosa_dice"]) for p in ok_punti if p in punti)
        s["parole_materiale"] = mat
        foglia = not any(x["parent"] == s["id"] for x in sezioni)
        s["foglia"] = foglia
        if s["escludi"]:
            continue
        if foglia and mat == 0:
            problemi.append(f"[HIGH] {s['id']} «{s['titolo']}»: nessun materiale (ne' testo ne' punti). "
                            "Il writer non puo' scriverla: aggiungi contenuto o punti.")
        if s["parole_target"] and mat and mat / s["parole_target"] < RAPPORTO_MIN:
            avvisi.append(f"{s['id']}: {mat} parole di materiale per {s['parole_target']} di target "
                          f"({mat / s['parole_target']:.2f}): uscira' corta, il writer non riempie. "
                          "Aggiungi materiale o abbassa il target.")
        if not s["ruolo"]:
            avvisi.append(f"{s['id']}: manca `ruolo:` (cosa deve dimostrare la sezione)")

    tot = sum(s["parole_target"] for s in sezioni if not s["escludi"])
    if cfg["parole_totali"] and tot and abs(tot - cfg["parole_totali"]) / cfg["parole_totali"] > cfg["tolleranza_parole"]:
        avvisi.append(f"somma dei target {tot} contro parole_totali {cfg['parole_totali']} di progetto.json")
    usati = {p for s in sezioni for p in s["punti"]}
    inutilizzati = sorted(set(punti) - usati)

    comune.BUILD.mkdir(parents=True, exist_ok=True)
    comune.SEZIONI_JSON.write_text(json.dumps(
        {"generato": dt.datetime.now().isoformat(timespec="seconds"), "titolo": titolo_doc,
         "sezioni": sezioni}, ensure_ascii=False, indent=1), encoding="utf-8")

    r = [f"# Scaletta — controllo del {dt.date.today().isoformat()}", "",
         f"Titolo: {titolo_doc or '(nessuno)'} · sezioni: {len(sezioni)} · target totale: {tot} parole"
         + (f" (progetto: {cfg['parole_totali']})" if cfg["parole_totali"] else ""), "",
         "| id | titolo | target | materiale | punti | fonti |", "|---|---|---|---|---|---|"]
    for s in sezioni:
        r.append(f"| {'  ' * (s['livello'] - 1)}{s['id']} | {s['titolo']}{' (esclusa)' if s['escludi'] else ''} "
                 f"| {s['parole_target'] or '—'} | {s['parole_materiale']} | {len(s['punti'])} "
                 f"| {', '.join(s['fonti_ammesse'])} |")
    r += [""]
    if problemi:
        r += ["## Problemi bloccanti", ""] + [f"- {p}" for p in problemi] + [""]
    if avvisi:
        r += ["## Avvisi", ""] + [f"- {x}" for x in avvisi] + [""]
    if inutilizzati:
        r += [f"## Punti validati non usati in nessuna sezione ({len(inutilizzati)})", "",
              ", ".join(inutilizzati), "", "Non e' un errore: e' materiale disponibile che la scaletta "
              "non usa. Guardali prima di chiudere la scaletta.", ""]
    comune.REPORTS.mkdir(parents=True, exist_ok=True)
    (comune.REPORTS / "scaletta.md").write_text("\n".join(r), encoding="utf-8")
    print("\n".join(r))
    print(f"Scritti {comune.rel(comune.SEZIONI_JSON)} e reports/scaletta.md")
    return 2 if problemi else 0


if __name__ == "__main__":
    raise SystemExit(main())
