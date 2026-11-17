#!/usr/bin/env python3
"""ctx.py — rende il contesto di UNA sezione per il writer (e per il claim-auditor).

    python3 tools/ctx.py <id>          # scrive build/ctx/<id>.md e ne stampa il percorso

Il contesto e' tutto e solo il materiale della sezione: convenzioni, ruolo, parole obiettivo,
contenuto della scaletta, numeri dal log, fonti citabili con la formulazione validata, floats
della sezione (con le celle delle tabelle, per sapere cosa NON ripetere), trappole, note
editoriali, la sezione precedente gia' scritta e la successiva (solo per l'aggancio).
`abstract` e' speciale: il materiale sono i DRAFT gia' scritti di tutte le sezioni.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, cfg, die, draft_di, leggi_json, p  # noqa: E402


def sezioni_ordinate() -> list[dict]:
    s = leggi_json(BUILD / "sezioni.json")
    if s is None:
        die("manca build/sezioni.json: lancia prima tools/leggi_scaletta.py")
    return s


def scrivibili(sezioni: list[dict]) -> list[dict]:
    """Le sezioni che hanno prosa: tutte tranne i cappelli senza apertura."""
    return [s for s in sezioni if s["contenuto"]]


def blocco_fonti(s: dict) -> str:
    if not s["fonti"]:
        return "_Nessuna fonte citabile in questa sezione: niente token CIT-N/CIT-P._\n"
    out = []
    for f in s["fonti"]:
        co = f" (citata insieme a {', '.join(f['co_citate'])})" if f["co_citate"] else ""
        rim = (" — **solo rimando**: la fonte e' gia' presentata altrove; qui la citi con la "
               "stessa tesi, in poche parole." if f["solo_rimando"] else "")
        out.append(
            f"### `{f['chiave']}`{co}{rim}\n"
            f"- **Tesi (vincolante, l'unica cosa che puoi attribuirle)**: {f['tesi']}\n"
            + (f"- *Contesto dal lettore della routine (NON materiale: nulla che stia solo qui va "
               f"nel testo)*: {f['estrazione_lettore']}\n" if f["estrazione_lettore"] else "")
            + (f"- *Limiti rispetto al nostro setting*: {f['limiti_vs_noi']}\n" if f["limiti_vs_noi"] else "")
            + (f"- *Verbatim (solo per vedere dove finisce la fonte, MAI da copiare)*: "
               f"\"{f['citazione_verbatim']}\"\n" if f["citazione_verbatim"] else ""))
    return "\n".join(out)


def glossario() -> str:
    g = p("glossario")
    return g.read_text(encoding="utf-8") if g.exists() else "_glossario non trovato_"


def blocco_floats(s: dict) -> str:
    inv = {f["id"]: f for f in (leggi_json(BUILD / "floats.json") or [])}
    if not s["floats"]:
        return "_Nessun float in questa sezione._\n"
    out = []
    for fid in s["floats"]:
        f = inv.get(fid)
        if not f:
            out.append(f"- `{fid}`: ⚠ non in build/floats.json (lancia tools/floats.py)")
            continue
        tok = "[[FIG:%s]]" % fid if f["tipo"] == "figura" else "[[TAB:%s]]" % fid
        riga = f"- `{tok}` {f['tipo']}: *{f['didascalia']}*"
        if f.get("celle"):
            riga += ("\n  Celle della tabella (gia' visibili al lettore: nel testo ne citi al "
                     "massimo le due o tre che reggono il messaggio): " + ", ".join(f["celle"][:80]))
        out.append(riga)
    return "\n".join(out) + "\n"


def rendi(sid: str) -> str:
    c = cfg()
    tutte = sezioni_ordinate()
    ordine = scrivibili(tutte)
    if sid == "abstract":
        corpo = "\n\n".join(f"**{s['id']} {s['titolo']}**\n{draft_di(s['id']) or '(DRAFT mancante)'}"
                            for s in ordine if not s.get("appendice"))
        return (f"# Contesto — abstract\n\nParole obiettivo: 150 (±{int(c['tolleranza_parole']*100)}%).\n"
                "Ruolo: domanda, disegno, tre risultati in direzione, una frase sui limiti. "
                "Nessun numero oltre a N e ai tassi gia' nel testo. Nessuna citazione.\n\n"
                "## Materiale: i DRAFT gia' scritti\n\n" + corpo + "\n")
    s = next((x for x in tutte if x["id"] == sid), None)
    if s is None:
        die(f"sezione {sid} non in build/sezioni.json")
    idx = [x["id"] for x in ordine].index(sid) if s in ordine else -1
    prec = ordine[idx - 1] if idx > 0 else None
    succ = ordine[idx + 1] if 0 <= idx < len(ordine) - 1 else None
    tol = int(c["tolleranza_parole"] * 100)
    conv = "\n".join(f"- {x}" for x in c["convenzioni"])
    parti = [
        f"# Contesto — {sid} {s['titolo']}\n",
        f"Parole obiettivo: **{s['parole']}** (±{tol}%; nessun pavimento). "
        f"Pagine di piano: {s['pagine']}.\n",
        f"**Ruolo**: {s['ruolo'] or '(non dichiarato)'}\n",
        "## Convenzioni\n" + conv + "\n",
        "## Glossario del gruppo (termini vincolanti: usa la colonna Use, mai Do not use)\n" + glossario() + "\n",
        "## Contenuto (l'unico materiale tuo, insieme ai numeri e alle fonti qui sotto)\n"
        + s["contenuto"] + "\n",
        "## Numeri dal log Stata (citabili cosi' come sono)\n"
        + (s["numeri_log"] or "_nessuno_") + "\n",
        "## Fonti citabili\n" + blocco_fonti(s),
        "## Fonti NON citabili qui (non nominarle)\n"
        + ("\n".join(f"- {x}" for x in s["fonti_scartate"]) or "_nessuna_") + "\n",
        "## Floats di questa sezione (vanno richiamati nel testo almeno una volta)\n" + blocco_floats(s),
        "## Trappole (guardrails della scaletta)\n" + (s["trappole"] or "_nessuna_") + "\n",
        "## Note editoriali (istruzioni, non materiale da affermare)\n"
        + (s["note_editoriali"] or "_nessuna_") + "\n",
        "## Sezione precedente (gia' scritta, per la continuita')\n"
        + (f"**{prec['id']} {prec['titolo']}**\n\n{draft_di(prec['id']) or '⚠ DRAFT MANCANTE: non scrivere.'}"
           if prec else "_e' la prima_") + "\n",
        "## Sezione successiva (solo per l'aggancio, mai materiale)\n"
        + (f"**{succ['id']} {succ['titolo']}** — ruolo: {succ['ruolo']}" if succ else "_e' l'ultima_") + "\n",
    ]
    return "\n".join(parti)


def main():
    if len(sys.argv) != 2:
        die("uso: ctx.py <id>")
    sid = sys.argv[1]
    out = BUILD / "ctx" / f"{sid}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendi(sid), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
