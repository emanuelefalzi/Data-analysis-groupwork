#!/usr/bin/env python3
"""Glossario, fase 3 — consolidamento (un solo processo, deterministico).

Unisce `glossario/out/<gruppo>.json` (scritti dai redattori) in
`glossario/glossario.json`:
  - lo stesso termine descritto da due gruppi -> conflitto segnalato, vince il primo;
  - varianti vietate rese SIMMETRICHE: se A segnala B come vicino confondibile,
    anche B segnala A (stessa ragione, letta dall'altro lato);
  - controlla che la sezione di definizione preceda tutti gli usi: dove non accade
    il termine e' usato prima di essere definito, ed e' un problema di struttura
    della scaletta, non del linter.

Uso:
    python3 tools/glossario/consolida.py
    python3 tools/glossario/lint.py --autotest      # subito dopo: atteso 0 blocchi
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402


def main() -> int:
    cartella = comune.ROOT / "glossario" / "out"
    files = sorted(cartella.glob("*.json"))
    if not files:
        print("Nessun file in glossario/out/.")
        return 1
    ordine = {sid: i for i, sid in enumerate(comune.sezioni())}
    voci, origine, conflitti, problemi = {}, {}, [], []
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for v in d["voci"]:
            k = v["forma_canonica"].lower()
            if k in voci:
                conflitti.append(f"«{v['forma_canonica']}» in {origine[k]} e {f.name}: tengo {origine[k]}")
                continue
            voci[k], origine[k] = v, f.name

    for k, v in voci.items():
        for var in v.get("varianti_vietate", []):
            altro = voci.get(var["forma"].lower())
            if altro and var.get("classe", "vicino_confondibile") == "vicino_confondibile":
                if not any(x["forma"].lower() == k for x in altro.get("varianti_vietate", [])):
                    altro.setdefault("varianti_vietate", []).append(
                        {"forma": v["forma_canonica"], "classe": "vicino_confondibile",
                         "perche": f"(speculare) {var.get('perche', '')}"})
        nd = v.get("sezione_definizione")
        if v.get("stato") == "definito" and nd:
            if nd not in ordine:
                problemi.append(f"«{v['forma_canonica']}»: sezione_definizione «{nd}» non esiste in scaletta")
                continue
            prima = [u for u in v.get("sezioni_uso", []) if u in ordine and ordine[u] < ordine[nd]]
            if prima and not v.get("usabile_prima_della_definizione"):
                problemi.append(f"«{v['forma_canonica']}» usato in {prima} prima della definizione in {nd}")

    dest = comune.GLOSSARIO
    dest.write_text(json.dumps({"voci": list(voci.values())}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Scritto {comune.rel(dest)}: {len(voci)} voci "
          f"({sum(1 for v in voci.values() if v.get('stato') != 'definito')} usate ma non definite)")
    for c in conflitti:
        print(f"  CONFLITTO {c}")
    for p in problemi:
        print(f"  STRUTTURA {p}")
    return 2 if problemi else 0


if __name__ == "__main__":
    raise SystemExit(main())
