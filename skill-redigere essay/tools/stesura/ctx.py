#!/usr/bin/env python3
"""Rende il contesto completo di una sezione per l'agente `section-writer`.

Il materiale immutabile (scaletta, punti validati, glossario) vive in `build/` e
viene passato al writer come un unico file markdown renderizzato al volo: il
writer non puo' toccare la propria fonte per costruzione, non per regola.

Cosa ci mette, e cosa no (lezioni della tesi):
  - la sezione intera: contenuto, ruolo, aggancio, trappole, target di parole;
  - SOLO i punti elencati nella scaletta per quella sezione, con `cosa_dice`;
    la citazione verbatim c'e', marcata come «non copiare»: serve a riconoscere
    dove finisce la fonte, mai a essere ripresa (antiplagio);
  - il padre (titolo e contenuto) per orientamento;
  - la sezione precedente GIA' SCRITTA (DRAFT), per la continuita': la scrittura
    e' sequenziale. Se manca, il writer si ferma;
  - la sezione successiva: solo titolo e contenuto, per costruire l'aggancio,
    mai come materiale;
  - le convenzioni di progetto.json (lingua, nomi fissi) e il glossario.
Non ci mette mai: le altre sezioni, le fonti intere, il brief (che ha gia'
prodotto la scaletta: il contratto e' la scaletta).

Uso:
    python3 tools/stesura/ctx.py 2.1            # scrive build/ctx/2.1.md e lo stampa
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 1
    sid = argv[0]
    sez = comune.sezioni()
    if sid not in sez:
        print(f"ERRORE: sezione «{sid}» non in build/sezioni.json (rilancia leggi_scaletta.py?)")
        return 1
    s = sez[sid]
    if s["escludi"]:
        print(f"ERRORE: la sezione «{sid}» e' marcata `escludi: sì` nella scaletta: non si scrive.")
        return 1
    cfg = comune.config()
    try:
        punti = comune.estratti()["punti"]
        fonti = comune.estratti()["fonti"]
    except SystemExit:
        punti, fonti = {}, {}
    ids = [k for k, v in sez.items() if not v["escludi"]]
    i = ids.index(sid)
    prec = ids[i - 1] if i > 0 else None
    succ = ids[i + 1] if i + 1 < len(ids) else None

    r = [f"# Contesto per la sezione {sid} — {s['titolo']}", "",
         "Materiale immutabile. Tutto cio' che scrivi deve stare qui dentro (regola sovrana).", "",
         "## Convenzioni di progetto", "",
         f"- lingua del testo: **{cfg['lingua']}** · stile citazionale: {cfg['stile_citazionale']}",
         f"- target: **{s['parole_target'] or 'non fissato'}** parole "
         f"(tolleranza ±{int(cfg['tolleranza_parole'] * 100)}%) · materiale: {s['parole_materiale']} parole"]
    for nome, regola in (cfg.get("nomi_fissi") or {}).items():
        r.append(f"- nome fisso: **{nome}** — {regola}")
    if cfg.get("convenzioni"):
        r += [f"- {c}" for c in cfg["convenzioni"]]
    r += ["", "## La sezione", "",
          f"- livello: {s['livello']} · padre: {s['parent'] or '—'} · foglia: {s['foglia']}",
          f"- **ruolo**: {s['ruolo'] or '(non dichiarato)'}",
          f"- **aggancio**: {s['aggancio'] or '(nessuno: non inventare una transizione)'}",
          f"- **trappole**: {s['trappole'] or '(nessuna)'}",
          f"- **fonti ammesse**: {', '.join(s['fonti_ammesse']) or 'nessuna — la sezione e ragionamento dell autore'}",
          "", "### Contenuto dell'autore (materiale)", "", s["contenuto"] or "(vuoto)", ""]
    if s["punti"]:
        r += ["### Punti dalle fonti (materiale)", ""]
        for pid in s["punti"]:
            p = punti.get(pid)
            if not p:
                r += [f"- `{pid}` ⚠ NON VALIDATO: non usarlo", ""]
                continue
            f = fonti.get(p["id_fonte"], {})
            r += [f"- **`{pid}`** — fonte `{p['id_fonte']}` ({f.get('citazione', '')}; peer: "
                  f"{p['peer_reviewed']}) · forza: **{p['forza']}**"
                  + (f" · ⚠ seconda mano: idea di {p['seconda_mano']}" if p["seconda_mano"] else ""),
                  f"  - cosa dice: {p['cosa_dice']}",
                  f"  - verbatim (NON COPIARE, serve solo a vedere dove finisce la fonte): «{p['citazione_verbatim']}»"]
            if p["note"]:
                r.append(f"  - note: {p['note']}")
            r.append("")
    if s["parent"] and s["parent"] in sez:
        pa = sez[s["parent"]]
        r += [f"## Padre: {pa['id']} {pa['titolo']} (solo orientamento)", "", pa["contenuto"] or "(vuoto)", ""]
    if prec:
        d = comune.draft_di(prec)
        r += [f"## Sezione precedente: {prec} {sez[prec]['titolo']} — DRAFT gia' scritto", "",
              d if d else "⚠ NON ANCORA SCRITTA: fermati, la scrittura e' sequenziale.", ""]
    if succ:
        r += [f"## Sezione successiva: {succ} {sez[succ]['titolo']} (SOLO per l'aggancio, mai materiale)", "",
              sez[succ]["contenuto"] or "(vuoto)", ""]
    if comune.GLOSSARIO.exists():
        g = json.loads(comune.GLOSSARIO.read_text(encoding="utf-8"))["voci"]
        r += ["## Glossario (termini vincolanti)", ""]
        for v in g:
            vv = "; ".join(f"«{x['forma']}» ({x.get('classe', 'vicino_confondibile')}: {x.get('perche', '')})"
                           for x in v.get("varianti_vietate", []))
            r.append(f"- **{v['forma_canonica']}**: {v.get('definizione') or '(usato ma non definito)'}"
                     + (f" — attenzione a: {vv}" if vv else ""))
        r.append("")
    out = comune.BUILD / "ctx" / f"{sid}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(r), encoding="utf-8")
    print("\n".join(r))
    print(f"\n[scritto {comune.rel(out)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
