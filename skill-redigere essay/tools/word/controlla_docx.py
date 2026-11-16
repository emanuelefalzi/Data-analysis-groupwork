#!/usr/bin/env python3
"""Ultimo controllo, deterministico e read-only, sul Word assemblato.

Riprende i controlli dell'agente `final-check` della tesi che non hanno bisogno
di un modello:
  1. nessun token residuo `[[…]]` e nessun residuo di `## LEDGER`/`¶` (HIGH);
  2. un titolo per ogni sezione della scaletta, nell'ordine giusto (HIGH);
  3. nessun numero scritto due volte nel titolo («1. 1 Titolo») (HIGH);
  4. nel corpo solo gli stili Heading 1-3, lo stile corpo e quelli gia' presenti
     nel template (MEDIUM);
  5. nessun segnaposto {{…}} rimasto (HIGH);
  6. parole totali del corpo contro parole_totali di progetto.json (INFO);
  7. trattini lunghi usati come pausa (MEDIUM).

Uso:
    python3 tools/word/controlla_docx.py [percorso.docx]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402
from docx import Document  # noqa: E402


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    cfg = comune.config()
    path = Path(argv[0]) if argv else comune.ROOT / cfg["output_docx"]
    if not path.exists():
        print(f"ERRORE: {comune.rel(path)} non esiste. Prima: tools/word/assemble.py")
        return 1
    doc = Document(str(path))
    tmpl = comune.ROOT / cfg["template_docx"]
    stili_template = {p.style.name for p in Document(str(tmpl)).paragraphs} if tmpl.exists() else set()
    ammessi = {"Heading 1", "Heading 2", "Heading 3", cfg["stile_corpo"]} | stili_template

    f = []
    pars = doc.paragraphs
    for i, p in enumerate(pars):
        t = p.text
        if "[[" in t:
            f.append(("HIGH", f"¶{i}: token residuo «{t[t.index('[['):][:60]}»"))
        if "## LEDGER" in t or re.search(r"¶\d+\s*←", t):
            f.append(("HIGH", f"¶{i}: residuo di LEDGER"))
        if re.search(r"\{\{[A-Z]+\}\}", t):
            f.append(("HIGH", f"¶{i}: segnaposto rimasto «{re.search(r'{{[A-Z]+}}', t).group(0)}»"))
        if p.style.name not in ammessi and t.strip():
            f.append(("MEDIUM", f"¶{i}: stile «{p.style.name}» non previsto"))
        if p.style.name.startswith("Heading") and re.match(r"^\d+(\.\d+)*\.?\s+\d", t):
            f.append(("HIGH", f"¶{i}: numero ripetuto nel titolo «{t[:50]}»"))
        if "—" in t or " – " in t:
            f.append(("MEDIUM", f"¶{i}: trattino lungo «…{t[max(0, t.find('—') - 30):t.find('—') + 30]}…»"))

    sez = [s for s in comune.sezioni().values() if not s["escludi"]]
    titoli = [p.text for p in pars if p.style.name.startswith("Heading")]
    j = 0
    for s in sez:
        while j < len(titoli) and not titoli[j].rstrip().endswith(s["titolo"].rstrip()):
            j += 1
        if j == len(titoli):
            f.append(("HIGH", f"titolo della sezione {s['id']} «{s['titolo']}» assente o fuori ordine"))
            j = 0
        else:
            j += 1

    corpo = [p.text for p in pars if p.style.name == cfg["stile_corpo"]]
    parole = sum(comune.conta_parole(t) for t in corpo)
    f.append(("INFO", f"parole nel corpo (bibliografia inclusa): {parole}"
              + (f" · obiettivo {cfg['parole_totali']}" if cfg["parole_totali"] else "")))

    for sev, msg in sorted(f, key=lambda x: ["HIGH", "MEDIUM", "INFO"].index(x[0])):
        print(f"[{sev}] {msg}")
    alti = sum(1 for x in f if x[0] == "HIGH")
    print(f"\n{alti} HIGH." if alti else "\nNessun HIGH: il documento e' pronto per la rilettura dell'autore.")
    return 2 if alti else 0


if __name__ == "__main__":
    raise SystemExit(main())
