#!/usr/bin/env python3
"""Controlla le sintesi per domanda scritte dall'agente `sintesi-domande`.

Le sintesi (`intermedi/sintesi-D<n>.md`) sono il primo testo argomentato del
progetto e la base su cui la persona costruisce la scaletta: per questo valgono
le stesse regole del testo finale. Ogni paragrafo deve portare almeno un
riferimento `[P:fonte#n]` a un punto validato; ogni riferimento deve esistere;
ogni numero deve comparire nei punti citati dal paragrafo. Un paragrafo senza
riferimenti e' ammesso solo se comincia con «Lacuna:», «Tensione:» o «Nota:»,
cioe' se dichiara un buco o un conflitto invece di affermare qualcosa.

Uso:
    python3 tools/fonti/verifica_sintesi.py            # tutte le sintesi
    python3 tools/fonti/verifica_sintesi.py D2
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

REF = re.compile(r"\[P:([^\]\s]+)\]")
NUM = re.compile(r"\d+(?:[.,]\d+)*%?")
DICHIARAZIONI = ("lacuna:", "tensione:", "nota:", "gap:", "tension:", "note:")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    punti = comune.estratti()["punti"]
    files = sorted(comune.INTERMEDI.glob("sintesi-*.md"))
    if argv:
        files = [f for f in files if f.stem.split("-", 1)[1] in argv]
    if not files:
        print("Nessuna sintesi in intermedi/.")
        return 0
    problemi = 0
    for f in files:
        corpo = re.sub(r"^#.*$", "", f.read_text(encoding="utf-8"), flags=re.M)
        for i, par in enumerate(comune.paragrafi(corpo), 1):
            refs = REF.findall(par)
            if not refs:
                if not par.lower().lstrip("*_ ").startswith(DICHIARAZIONI):
                    print(f"[HIGH] {f.name} ¶{i}: nessun [P:...] — «{par[:90]}…»")
                    problemi += 1
                continue
            mancanti = [r for r in refs if r not in punti]
            for r in mancanti:
                print(f"[HIGH] {f.name} ¶{i}: [P:{r}] non e' un punto validato")
                problemi += 1
            materiale = " ".join(comune.norm(punti[r]["cosa_dice"] + " " + punti[r]["citazione_verbatim"])
                                 for r in refs if r in punti)
            for n in NUM.findall(REF.sub("", par)):
                if len(n.strip("%")) >= 2 and n.lower() not in materiale:
                    print(f"[HIGH] {f.name} ¶{i}: numero «{n}» assente dai punti citati")
                    problemi += 1
    print(f"\n{problemi} problemi." if problemi else "OK: ogni paragrafo e' ancorato a punti validati.")
    return 2 if problemi else 0


if __name__ == "__main__":
    raise SystemExit(main())
