#!/usr/bin/env python3
"""conta_pagine.py — quante pagine viene davvero il documento assemblato.

Perche' serve uno script e non una stima: `python-docx` non impagina, e tutte
le stime fatte finora (parole/350 + titoli + code di pagina) sono uscite lontane
dal vero. Se una decisione dell'autore dipende dal numero -- e dipende, la
soglia e' 50 pagine -- il numero va misurato, non calcolato.

Come: Word esporta un PDF, `pdfinfo` conta le pagine. LibreOffice non e'
installato su questa macchina, Word si'.

Cautele, perche' guidare Word da script puo' fare danni:
- **non** quitta Word se era gia' aperto quando lo script parte: l'autore
  potrebbe averci dentro del lavoro non salvato;
- apre il solo documento richiesto e lo chiude senza salvare;
- se Word non risponde entro il timeout, lo dice invece di restare appeso.

Uso:
    /usr/bin/python3 tools/conta_pagine.py                    # out/LF3236167.docx
    /usr/bin/python3 tools/conta_pagine.py <percorso.docx>
"""

import os
import subprocess
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
DEFAULT = BASE + "out/LF3236167.docx"


def word_gia_aperto():
    r = subprocess.run(["osascript", "-e",
                        'application "Microsoft Word" is running'],
                       capture_output=True, text=True)
    return r.stdout.strip() == "true"


def esporta_pdf(docx, pdf, timeout=600):
    """Apre il docx in Word, esporta un PDF, chiude il documento."""
    # `with timeout` e' obbligatorio: il default di AppleScript e' 120 secondi e
    # Word, su un documento di cinquanta pagine al primo avvio, ci mette di piu'.
    # Senza, si prende un -1712 «AppleEvent timed out» che sembra un errore del
    # documento e non lo e'.
    script = f'''
    with timeout of {timeout} seconds
        tell application "Microsoft Word"
            set d to open file name POSIX file "{docx}" as string with read only
            save as d file name POSIX file "{pdf}" as string file format format PDF
            close d saving no
        end tell
    end timeout
    '''
    r = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True, timeout=timeout + 60)
    if r.returncode != 0:
        raise RuntimeError("Word non ha esportato il PDF: " + r.stderr.strip()[:400])


def pagine(pdf):
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True)
    for riga in r.stdout.splitlines():
        if riga.startswith("Pages:"):
            return int(riga.split()[1])
    raise RuntimeError("pdfinfo non ha riportato il numero di pagine")


def main():
    docx = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    if not os.path.exists(docx):
        print(f"non trovato: {docx}")
        return 2
    pdf = os.path.splitext(docx)[0] + ".pdf"

    era_aperto = word_gia_aperto()
    esporta_pdf(docx, pdf)
    if not era_aperto:
        subprocess.run(["osascript", "-e", 'tell application "Microsoft Word" to quit'],
                       capture_output=True)

    n = pagine(pdf)
    print(f"{os.path.basename(docx)}: {n} pagine")
    print(f"PDF: {pdf}")
    if not era_aperto:
        print("(Word non era aperto prima: e' stato chiuso)")
    else:
        print("(Word era gia' aperto: lasciato aperto, chiuso il solo documento)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
