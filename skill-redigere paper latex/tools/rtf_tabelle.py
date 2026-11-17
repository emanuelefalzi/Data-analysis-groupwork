#!/usr/bin/env python3
"""rtf_tabelle.py — legge le tabelle di un RTF (esttab di Stata, anche risalvato da Word)
senza LibreOffice: solo Python standard, quindi gira su qualunque computer.

    python3 tools/rtf_tabelle.py <file.rtf>     # stampa titolo e righe di ogni tabella

Uso da codice: `tabelle_rtf(path) -> [{"n", "titolo", "nota", "righe": [[cella, ...], ...]}]`.
Le celle restano testo cosi' com'e' nell'RTF (nessun arrotondamento).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# gruppi che non contengono testo del documento
DESTINAZIONI = {
    "fonttbl", "colortbl", "stylesheet", "info", "pict", "header", "footer", "headerl",
    "headerr", "footerl", "footerr", "listtable", "listoverridetable", "rsidtbl", "generator",
    "xmlnstbl", "themedata", "colorschememapping", "latentstyles", "datastore", "mmathPr",
    "pgdsctbl", "revtbl", "filetbl", "operator", "author", "title", "company", "pnseclvl",
    "defchp", "defpap", "wgrffmtfilter", "fldinst", "object", "shp", "nonshppict", "bkmkstart",
    "bkmkend", "protusertbl", "lsdlockedexcept", "aftnsep", "ftnsep", "ftnsepc", "aftnsepc",
}
TOKEN = re.compile(r"\\([a-zA-Z]+)(-?\d+)? ?|\\'([0-9a-fA-F]{2})|\\(.)|([{}])|([^\\{}\r\n]+)|[\r\n]+")


def rtf_a_testo(rtf: str) -> str:
    """Testo con marcatori: TAB fra celle, '\\x1e' a fine riga di tabella, '\\n' a fine paragrafo."""
    out = []
    pila = []                 # per ogni gruppo: (salta, uc)
    salta, uc, da_saltare = False, 1, 0
    for m in TOKEN.finditer(rtf):
        parola, num, hexa, sym, graffa, testo = m.groups()
        if graffa == "{":
            pila.append((salta, uc))
            continue
        if graffa == "}":
            salta, uc = pila.pop() if pila else (False, 1)
            continue
        if salta:
            continue
        if parola:
            if parola in DESTINAZIONI:
                salta = True
            elif parola == "uc":
                uc = int(num or 1)
            elif parola == "u":
                n = int(num)
                out.append(chr(n + 65536 if n < 0 else n))
                da_saltare = uc
            elif parola == "cell":
                out.append("\t")
            elif parola == "row":
                out.append("\x1e\n")
            elif parola in ("par", "line"):
                out.append("\n")
            elif parola == "tab":
                out.append(" ")
            continue
        if sym is not None:
            if sym == "*":
                salta = True
            elif sym in "\\{}":
                out.append(sym)
            elif sym == "~":
                out.append(" ")
            elif sym == "-":
                pass
            continue
        if hexa:
            if da_saltare:
                da_saltare -= 1
                continue
            out.append(bytes([int(hexa, 16)]).decode("cp1252", errors="replace"))
            continue
        if testo:
            if da_saltare:
                k = min(da_saltare, len(testo))
                testo, da_saltare = testo[k:], da_saltare - k
            out.append(testo)
    return "".join(out)


def tabelle_rtf(path: Path) -> list[dict]:
    """Una tabella = righe consecutive. Il testo fra due tabelle si divide cosi': le righe da
    nota («Standard errors…», «* p < …») vanno alla tabella prima, il resto e' il titolo della
    tabella dopo («Table N. titolo», oppure l'ultima riga di testo se manca il numero)."""
    testo = rtf_a_testo(path.read_text(encoding="latin-1"))
    tabelle, cur, fra = [], None, []

    def apri():
        note = [t for t in fra if re.match(r"(Standard errors|\* p|\*\s*p\s*<|Note)", t)]
        titoli = [t for t in fra if t not in note]
        if tabelle:
            tabelle[-1]["nota"] = " ".join(note)
        tit = titoli[-1] if titoli else ""
        mt = re.match(r"Table\s+(\d+)\.\s*(.+)$", tit)
        return {"n": int(mt.group(1)) if mt else None, "titolo": mt.group(2).strip() if mt else tit,
                "nota": "", "righe": []}

    for riga in testo.split("\n"):
        if riga.endswith("\x1e"):
            celle = [re.sub(r"\s+", " ", c).strip() for c in riga[:-1].split("\t")]
            if celle and celle[-1] == "":
                celle = celle[:-1]
            if cur is None:
                cur = apri()
                tabelle.append(cur)
                fra = []
            cur["righe"].append(celle)
        else:
            t = re.sub(r"\s+", " ", riga).strip()
            if t:
                fra.append(t)
                cur = None
    if tabelle:
        tabelle[-1]["nota"] = " ".join(t for t in fra if re.match(r"(Standard errors|\* p)", t))
    for i, t in enumerate(tabelle):
        if t["n"] is None:
            t["n"] = f"senza-numero-{i + 1}"
    return tabelle


if __name__ == "__main__":
    for t in tabelle_rtf(Path(sys.argv[1])):
        print(f"Table {t['n']}. {t['titolo']}  [{len(t['righe'])} righe]  nota: {t['nota'][:90]}")
        for r in t["righe"][:6]:
            print("   ", r)
