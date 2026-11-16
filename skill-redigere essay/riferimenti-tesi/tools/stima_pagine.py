#!/usr/bin/env python3
"""stima_pagine.py — impagina il documento a mano, riga per riga.

**Non e' una misura, e' una stima**: quella vera la da' solo Word, e per pilotarlo
da script macOS chiede un permesso di Automazione che questo terminale non ha
(errore -1743). Il numero esatto si ottiene aprendo `out/LF3236167.docx` e
guardando la barra di stato.

Perche' allora questa e non `parole / 350`: quella costante e' una media sul
testo corrente, e sbaglia proprio dove il documento e' anomalo. Il Cap. 7 sono
23 affermazioni di 12-30 parole ciascuna: ognuna occupa una riga e mezza ma
**consuma un paragrafo intero**, cioe' due righe. Le quattro tabelle e i 128
titoli non sono prosa affatto. Qui ogni elemento e' contato per le righe che
occupa davvero.

Uso:
    /usr/bin/python3 tools/stima_pagine.py
    /usr/bin/python3 tools/stima_pagine.py --righe-per-pagina 28
"""

import argparse
import math
import sys

from docx import Document
from docx.oxml.ns import qn

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
DOC = BASE + "out/LF3236167.docx"

EMU_PER_MM = 36000
# Times New Roman 12pt: larghezza media di un carattere in prosa inglese,
# spazi inclusi. Misurata sulle metriche del font, non stimata a occhio.
MM_PER_CARATTERE = 2.05


def righe(testo, per_riga):
    if not testo.strip():
        return 1
    return max(1, math.ceil(len(testo) / per_riga))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--righe-per-pagina", type=int, default=28,
                    help="il template a norma ne tiene 27-29 (guide.pdf §10.3)")
    ap.add_argument("--doc", default=DOC)
    a = ap.parse_args()

    d = Document(a.doc)
    s = d.sections[-1]
    larghezza_mm = (s.page_width - s.left_margin - s.right_margin) / EMU_PER_MM
    per_riga = int(larghezza_mm / MM_PER_CARATTERE)

    corpo = d.element.body
    n_righe = 0
    n_par = n_titoli = n_tab = 0
    salti = 0

    for el in corpo.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            st = el.find(qn("w:pPr") + "/" + qn("w:pStyle"))
            stile = st.get(qn("w:val")) if st is not None else "Normal"
            testo = "".join(t.text or "" for t in el.iter(qn("w:t")))
            if stile == "Heading1":
                # `pageBreakBefore` nello stile: il resto della pagina si perde
                salti += 1
                n_righe += 3          # il titolo piu' lo spazio sopra e sotto
                n_titoli += 1
            elif stile in ("Heading2", "Heading3"):
                n_righe += righe(testo, per_riga) + 1
                n_titoli += 1
            else:
                n_righe += righe(testo, per_riga)
                n_par += 1
        elif tag == "tbl":
            n_tab += 1
            # una riga di tabella occupa piu' di una riga di testo: le celle
            # vanno a capo. Due righe di testo per riga di tabella, piu' la
            # didascalia e lo spazio attorno.
            n_righe += len(el.findall(qn("w:tr"))) * 2 + 2

    # ogni Heading 1 spreca in media meta' pagina di coda
    pagine_corpo = n_righe / a.righe_per_pagina
    coda = salti * 0.5
    stima = pagine_corpo + coda

    print(f"larghezza del testo: {larghezza_mm:.0f} mm  ->  ~{per_riga} caratteri per riga")
    print(f"righe per pagina:    {a.righe_per_pagina}")
    print()
    print(f"paragrafi di prosa:  {n_par}")
    print(f"titoli:              {n_titoli}  (di cui {salti} Heading 1, con salto pagina)")
    print(f"tabelle:             {n_tab}")
    print(f"righe totali:        {n_righe}")
    print()
    print(f"pagine di testo:     {pagine_corpo:.1f}")
    print(f"code di pagina:      {coda:.1f}  ({salti} capitoli x mezza pagina)")
    print(f"STIMA:               {stima:.0f} pagine")
    print()
    print("Non comprende l'indice, che Word genera all'apertura: da 128 titoli")
    print("vengono circa 3 pagine in piu'. Ne' i ringraziamenti del front matter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
