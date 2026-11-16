#!/usr/bin/env python3
"""bib.py — lettura di `fonti/fonti.bib` e resa APA 7 (in-text e reference list).

Nella tesi questo lavoro lo faceva un agente (`bibliography-builder`). Qui e'
deterministico: risolvere `[[CIT-N:chiave]]` in «Autore (Anno)» non richiede
giudizio, e uno script non sbaglia l'ordine alfabetico ne' inventa un anno.

Regole APA 7 applicate:
  - narrativa:   Akerlof (1970) · Baldwin and Clark (2000) · Teece et al. (1997)
  - parentetica: (Akerlof, 1970) · (Baldwin & Clark, 2000) · (Teece et al., 1997)
  - stesso autore e anno su due chiavi diverse: 2000a, 2000b
  - reference list alfabetica per cognome del primo autore, solo le chiavi citate.
Un campo mancante nel .bib resta mancante: non si stima mai.

Uso diretto (controllo):
    python3 tools/bib.py                 # elenca le voci e i campi mancanti
    python3 tools/bib.py chiave1 chiave2 # mostra la resa di quelle voci
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comune  # noqa: E402


# ---------------------------------------------------------------------------
# parser BibTeX minimo (graffe annidate, virgolette, campi su piu' righe)
# ---------------------------------------------------------------------------

def _valore(s: str, i: int) -> tuple[str, int]:
    while s[i] in " \t\n":
        i += 1
    if s[i] == "{":
        prof, j = 0, i
        while j < len(s):
            if s[j] == "{":
                prof += 1
            elif s[j] == "}":
                prof -= 1
                if prof == 0:
                    return s[i + 1:j], j + 1
            j += 1
        raise ValueError("graffa non chiusa")
    if s[i] == '"':
        j = s.index('"', i + 1)
        return s[i + 1:j], j + 1
    m = re.match(r"[^,}\s]+", s[i:])
    return m.group(0), i + m.end()


def leggi_bib(path: Path = comune.BIB) -> dict:
    """{chiave: {"tipo": ..., campo: valore}}"""
    if not Path(path).exists():
        return {}
    s = Path(path).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", s):
        tipo, chiave = m.group(1).lower(), m.group(2)
        if tipo in ("comment", "string", "preamble"):
            continue
        i, campi = m.end(), {"tipo": tipo}
        while i < len(s):
            while i < len(s) and s[i] in " \t\n,":
                i += 1
            if i >= len(s) or s[i] == "}":
                break
            k = re.match(r"([\w-]+)\s*=", s[i:])
            if not k:
                break
            i += k.end()
            v, i = _valore(s, i)
            campi[k.group(1).lower()] = re.sub(r"\s+", " ", v.replace("{", "").replace("}", "")).strip()
        out[chiave] = campi
    return out


# ---------------------------------------------------------------------------
# autori
# ---------------------------------------------------------------------------

def autori(voce: dict) -> list[tuple[str, str]]:
    """[(cognome, nomi)] da `author` (o `editor`, o `institution` per i report)."""
    raw = voce.get("author") or voce.get("editor") or ""
    if not raw:
        ente = voce.get("institution") or voce.get("organization") or voce.get("publisher") or ""
        return [(ente, "")] if ente else []
    out = []
    for a in re.split(r"\s+and\s+", raw):
        a = a.strip()
        if "," in a:
            cognome, nomi = [x.strip() for x in a.split(",", 1)]
        else:
            parti = a.split()
            cognome, nomi = (parti[-1], " ".join(parti[:-1])) if len(parti) > 1 else (a, "")
        out.append((cognome, nomi))
    return out


def iniziali(nomi: str) -> str:
    pezzi = [p for p in re.split(r"[\s.]+", nomi) if p]
    return " ".join(("-".join(x[0] + "." for x in p.split("-"))) for p in pezzi)


def anno(voce: dict) -> str:
    return voce.get("year") or "n.d."


class Bibliografia:
    def __init__(self, path: Path = comune.BIB, lingua: str = "en"):
        self.voci = leggi_bib(path)
        self.e = "e" if lingua == "it" else "and"
        self._suffissi = self._calcola_suffissi()

    def _calcola_suffissi(self) -> dict:
        """2000a/2000b per chiavi diverse con stessi autori in-text e stesso anno."""
        gruppi: dict = {}
        for k, v in self.voci.items():
            gruppi.setdefault((self._nomi_intext(v, "&"), anno(v)), []).append(k)
        suff = {}
        for (_, _), ks in gruppi.items():
            if len(ks) > 1:
                for i, k in enumerate(sorted(ks, key=lambda k: self.voci[k].get("title", ""))):
                    suff[k] = "abcdefghij"[i]
        return suff

    def _nomi_intext(self, v: dict, congiunzione: str) -> str:
        a = autori(v)
        if not a:
            return v.get("title", "Anon.")
        if len(a) == 1:
            return a[0][0]
        if len(a) == 2:
            return f"{a[0][0]} {congiunzione} {a[1][0]}"
        return f"{a[0][0]} et al."

    def anno_k(self, k: str) -> str:
        return anno(self.voci[k]) + self._suffissi.get(k, "")

    def narrativa(self, k: str) -> str:
        return f"{self._nomi_intext(self.voci[k], self.e)} ({self.anno_k(k)})"

    def parentetica(self, k: str) -> str:
        return f"({self._nomi_intext(self.voci[k], '&')}, {self.anno_k(k)})"

    def mancanti(self, k: str) -> list[str]:
        v = self.voci[k]
        m = [c for c in ("author", "year", "title") if not v.get(c) and not (c == "author" and autori(v))]
        if v["tipo"] == "article" and not v.get("journal"):
            m.append("journal")
        return m

    def voce_lista(self, k: str) -> str:
        """Voce della reference list. Il corsivo e' marcato con *...*, che
        `assemble.py` trasforma in run corsivi nel Word."""
        v = self.voci[k]
        a = autori(v)
        nomi = [f"{c}, {iniziali(n)}".rstrip(", ") for c, n in a]
        if len(nomi) == 1:
            chi = nomi[0]
        elif 1 < len(nomi) <= 20:
            chi = ", ".join(nomi[:-1]) + ", & " + nomi[-1]
        else:
            chi = ", ".join(nomi[:19]) + ", ... " + nomi[-1]
        if chi and not chi.endswith("."):
            chi += "."
        titolo = (v.get("title") or "").rstrip(".")
        t = v["tipo"]
        pezzi = [f"{chi} ({self.anno_k(k)})."]
        if t == "article":
            pezzi.append(f"{titolo}.")
            rivista = v.get("journal", "")
            vol = v.get("volume", "")
            num = f"({v['number']})" if v.get("number") else ""
            pag = v.get("pages", "").replace("--", "–")
            dettaglio = f"*{rivista}*" if rivista else ""
            if vol:
                dettaglio += f", *{vol}*{num}"
            if pag:
                dettaglio += f", {pag}"
            if dettaglio:
                pezzi.append(dettaglio + ".")
        elif t == "book":
            pezzi.append(f"*{titolo}*.")
            if v.get("publisher"):
                pezzi.append(f"{v['publisher']}.")
        elif t in ("incollection", "inbook", "inproceedings"):
            pezzi.append(f"{titolo}.")
            dove = v.get("booktitle", "")
            if dove:
                ed = f"In {v['editor']} (Ed.), " if v.get("editor") else "In "
                pag = f" (pp. {v['pages'].replace('--', '–')})" if v.get("pages") else ""
                pezzi.append(f"{ed}*{dove}*{pag}.")
            if v.get("publisher"):
                pezzi.append(f"{v['publisher']}.")
        else:  # techreport, online, misc
            pezzi.append(f"*{titolo}*.")
            ente = v.get("institution") or v.get("organization") or v.get("publisher")
            if ente and (not a or a[0][0] != ente):
                pezzi.append(f"{ente}.")
        if v.get("doi"):
            doi = v["doi"]
            pezzi.append(doi if doi.startswith("http") else f"https://doi.org/{doi}")
        elif v.get("url"):
            pezzi.append(v["url"])
        return " ".join(p for p in pezzi if p.strip())

    def ordina(self, chiavi) -> list[str]:
        def k(x):
            a = autori(self.voci[x])
            return (comune.norm(a[0][0]) if a else comune.norm(self.voci[x].get("title", "")),
                    self.anno_k(x))
        return sorted(chiavi, key=k)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    b = Bibliografia(lingua=comune.config()["lingua"])
    if not b.voci:
        print(f"{comune.rel(comune.BIB)} assente o vuoto.")
        return 1
    chiavi = argv or b.ordina(b.voci)
    for k in chiavi:
        if k not in b.voci:
            print(f"{k}: NON nel .bib")
            continue
        m = b.mancanti(k)
        print(f"{k}\n  {b.narrativa(k)} · {b.parentetica(k)}\n  {b.voce_lista(k)}"
              + (f"\n  MANCA: {', '.join(m)}" if m else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
