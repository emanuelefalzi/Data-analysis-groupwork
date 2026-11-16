#!/usr/bin/env python3
"""Documenti intermedi — la rielaborazione delle fonti in forma leggibile.

Da `build/estratti.json` (solo punti validati) produce, in `intermedi/`:
  - `schede/<id_fonte>.md`  una scheda per fonte: sintesi, punti per domanda, limiti
  - `matrice.md`            domanda x fonte: chi risponde a cosa, con quale forza
  - `punti.md`              tutti i punti per domanda, con il loro id: e' l'elenco
                            da cui si sceglie il materiale della scaletta

Sono documenti DERIVATI: si rigenerano a ogni giro, non vanno corretti a mano
(una correzione va fatta nella scheda JSON del lettore e poi si rivalida).
La sintesi argomentata per domanda (`intermedi/sintesi-D<n>.md`) invece la scrive
l'agente `sintesi-domande` e si verifica con `verifica_sintesi.py`.

Le `citazione_verbatim` compaiono nelle schede, marcate, solo perche' la persona
possa controllare: nel testo finale non entrano mai (antiplagio).

Uso:
    python3 tools/fonti/intermedi.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

SIGLA = {"dimostra": "D", "menziona": "m", "assume": "a"}


def main() -> int:
    e = comune.estratti()
    domande, fonti, punti = e["domande"], e["fonti"], e["punti"]
    out = comune.INTERMEDI
    (out / "schede").mkdir(parents=True, exist_ok=True)

    for fid, f in fonti.items():
        ps = [p for p in punti.values() if p["id_fonte"] == fid]
        r = [f"# {fid}", "", f"**{f['citazione']}** — {f['titolo']}", "",
             f"Tipo: {f['tipo_documento']} · peer-reviewed: {f['peer_reviewed']}"
             + (" · ⚠ assente da fonti.bib" if f.get("nel_bib") is False else ""), "",
             "## Sintesi", "", f["sintesi"], ""]
        for q in domande + [{"id": "altro", "testo": "altro materiale pertinente"}]:
            qp = [p for p in ps if p["domanda"] == q["id"]]
            if not qp:
                continue
            r += [f"## {q['id']} — {q['testo']}", ""]
            for p in qp:
                conf = {True: " · confermato NLM", False: " · NLM non concorde", None: ""}[p.get("confermato_nlm")]
                r += [f"**`{p['id']}`** ({p['forza']}{conf}) — {p['cosa_dice']}", "",
                      f"> verbatim, solo per controllo, mai da copiare: «{p['citazione_verbatim']}»"
                      + (f" — {p['sezione']}" if p["sezione"] else ""), ""]
                if p["seconda_mano"]:
                    r += [f"⚠ di seconda mano: l'idea e' di {p['seconda_mano']}", ""]
                if p["note"]:
                    r += [f"_Note:_ {p['note']}", ""]
        if f["domande_senza_risposta"]:
            r += ["## Domande a cui la fonte non risponde", ""]
            r += [f"- {x['domanda']}: {x['cosa_ho_cercato']}" for x in f["domande_senza_risposta"]] + [""]
        if f["limiti"]:
            r += ["## Limiti", "", f["limiti"], ""]
        (out / "schede" / f"{fid}.md").write_text("\n".join(r), encoding="utf-8")

    # matrice domanda x fonte
    ids = sorted(fonti)
    r = ["# Matrice domanda × fonte", "",
         "D = dimostra · m = menziona · a = assume · numero = quanti punti. "
         "Vuoto = la fonte non risponde (dichiarato nella scheda).", "",
         "| fonte | " + " | ".join(q["id"] for q in domande) + " | altro |",
         "|---|" + "---|" * (len(domande) + 1)]
    for fid in ids:
        celle = []
        for qid in [q["id"] for q in domande] + ["altro"]:
            qp = [p for p in punti.values() if p["id_fonte"] == fid and p["domanda"] == qid]
            celle.append(f"{len(qp)}{''.join(sorted({SIGLA[p['forza']] for p in qp}))}" if qp else "")
        r.append(f"| {fid} | " + " | ".join(celle) + " |")
    r += ["", "## Domande", ""] + [f"- **{q['id']}** {q['testo']}" for q in domande]
    scoperte = [q["id"] for q in domande if not any(p["domanda"] == q["id"] for p in punti.values())]
    if scoperte:
        r += ["", f"⚠ Domande senza alcun punto: {', '.join(scoperte)} — o servono altre fonti, "
              "o quella parte dell'essay sara' ragionamento dell'autore senza citazioni."]
    (out / "matrice.md").write_text("\n".join(r) + "\n", encoding="utf-8")

    # elenco dei punti, per scegliere il materiale della scaletta
    r = ["# Punti validati, per domanda", "",
         "Ogni id (`fonte#n`) si puo' mettere nel campo `punti:` di una sezione della scaletta.", ""]
    for q in domande + [{"id": "altro", "testo": "altro"}]:
        qp = [p for p in punti.values() if p["domanda"] == q["id"]]
        if not qp:
            continue
        r += [f"## {q['id']} — {q['testo']}", ""]
        r += [f"- `{p['id']}` [{p['forza']}] {p['cosa_dice']}" for p in qp] + [""]
    (out / "punti.md").write_text("\n".join(r), encoding="utf-8")

    print(f"Scritte {len(fonti)} schede in {comune.rel(out / 'schede')}, "
          f"{comune.rel(out / 'matrice.md')}, {comune.rel(out / 'punti.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
