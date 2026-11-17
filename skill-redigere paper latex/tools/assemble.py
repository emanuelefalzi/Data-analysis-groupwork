#!/usr/bin/env python3
"""assemble.py — dai DRAFT al sorgente LaTeX in latex/gen/.

    python3 tools/assemble.py            # rifiuta se restano buchi o mancano pezzi
    python3 tools/assemble.py --bozza    # assembla comunque: buchi in rosso, sezioni mancanti segnate
    python3 tools/assemble.py --dry-run  # dice solo cosa manca

Scrive (tutto derivato, non si corregge a mano):
- latex/gen/abstract.tex, latex/gen/corpo.tex, latex/gen/appendice.tex
- latex/gen/fonti.bib (copia di ../fonti/fonti.bib), latex/figures/*.png (copie)
`latex/main.tex` e `latex/preambolo.tex` sono del gruppo: titolo, autori, stile.

Conversioni:
- [[CIT-N:k]] → \\textcite{k}; [[CIT-P:k]] → \\parencite{k} (biblatex-apa, author–year);
- [[FIG:x]] → Figure~\\ref{fig:x}; [[TAB:x]] → Table~\\ref{tab:x}; [[SEC:5.1]] → Section~\\ref{sec:5.1};
- caratteri: & % _ # $ escapati; β ρ θ χ² × − ≈ ≤ ≥ in math;
- ogni float `corpo` entra subito dopo il paragrafo che lo richiama per primo nella sua sezione.
Fra corpo e references c'e' `\\FloatBarrier` + `\\label{corpo-fine}`: compila.py conta le pagine da li'.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, LATEX, ROOT, TOKEN_RE, cfg, die, draft_di, leggi_json, p, paragrafi  # noqa: E402

GEN = LATEX / "gen"
UNICODE = [("β", r"$\beta$"), ("ρ", r"$\rho$"), ("θ", r"$\theta$"), ("χ²", r"$\chi^2$"),
           ("χ", r"$\chi$"), ("×", r"$\times$"), ("−", r"$-$"), ("≈", r"$\approx$"),
           ("≤", r"$\leq$"), ("≥", r"$\geq$"), ("→", r"$\rightarrow$"), ("±", r"$\pm$"),
           ("²", r"$^2$"), ("₁", r"$_1$"), ("₂", r"$_2$"), ("₃", r"$_3$")]


def tex_testo(s: str) -> str:
    """Testo semplice → LaTeX. `codice` → \\texttt{codice}."""
    if "`" in s:
        parti = s.split("`")
        return "".join(tex_testo(x) if i % 2 == 0 else r"\texttt{" + tex_testo(x) + "}"
                       for i, x in enumerate(parti))
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"), ("$", r"\$")]:
        s = s.replace(a, b)
    for a, b in UNICODE:
        s = s.replace(a, b)
    s = re.sub(r"\$([^$]*)\$\$([^$]*)\$", r"$\1\2$", s)    # $\beta$$_1$ → $\beta_1$
    s = s.replace("“", "``").replace("”", "''").replace("‘", "`").replace("’", "'")
    return s


def converti(paragrafo: str, bozza: bool, buchi: list[str]) -> str:
    pezzi, last = [], 0
    for m in TOKEN_RE.finditer(paragrafo):
        pezzi.append(tex_testo(paragrafo[last:m.start()]))
        tipo, arg = m.group(1), m.group(2)
        if tipo == "CIT-N":
            pezzi.append(rf"\citeN{{{arg.replace(' ', '')}}}")
        elif tipo == "CIT-P":
            pezzi.append(rf"\citeP{{{arg.replace(' ', '')}}}")
        elif tipo == "FIG":
            pezzi.append(rf"Figure~\ref{{fig:{arg}}}")
        elif tipo == "TAB":
            pezzi.append(rf"Table~\ref{{tab:{arg}}}")
        elif tipo == "SEC":
            pezzi.append(rf"Section~\ref{{sec:{arg}}}")
        else:
            buchi.append(m.group(0))
            pezzi.append(rf"\buco{{{tipo}: {tex_testo(arg)}}}" if bozza else "")
        last = m.end()
    pezzi.append(tex_testo(paragrafo[last:]))
    return "".join(pezzi)


def appendice(bozza: bool, buchi: list[str]) -> str:
    """Appendix A: file markdown gia' scritto (progetto.json → appendice_testo), incluso cosi' com'e'.
    «# A Titolo» → \\section, «## A.1 Titolo» → \\subsection, paragrafi → prosa."""
    path = p("appendice_testo")
    if not path.exists():
        return r"\buco{Appendix A non trovata: " + tex_testo(str(path.name)) + "}\n"
    testo = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    out = []
    for blocco in paragrafi(testo):
        m = re.match(r"^(#{1,3})\s+([A-Z](?:\.\d+)?)\s+(.+)$", blocco)
        if m:
            cmd = r"\section" if len(m.group(1)) == 1 else r"\subsection"
            out.append(rf"{cmd}{{{tex_testo(m.group(3))}}}\label{{sec:{m.group(2)}}}" + "\n")
        else:
            out.append(converti(blocco, bozza, buchi) + "\n")
    return "\n".join(out)


ACCENTI = {"\u0301": "'", "\u0300": "`", "\u0308": '"', "\u0302": "^", "\u0303": "~",
           "\u0327": "c", "\u030c": "v", "\u0304": "=", "\u0306": "u", "\u030a": "r"}
SPECIALI = {"ø": r"{\o}", "Ø": r"{\O}", "ß": r"{\ss}", "æ": r"{\ae}", "Æ": r"{\AE}",
            "ł": r"{\l}", "Ł": r"{\L}", "–": "--", "—": "---", "’": "'", "‘": "`",
            "“": "``", "”": "''", "ı": r"{\i}"}


def bib_ascii(testo: str) -> str:
    """UTF-8 → comandi LaTeX (Strömberg → Str{\\"o}mberg), per bibtex."""
    import unicodedata
    out = []
    for ch in testo:
        if ord(ch) < 128:
            out.append(ch)
        elif ch in SPECIALI:
            out.append(SPECIALI[ch])
        else:
            d = unicodedata.normalize("NFD", ch)
            if len(d) == 2 and d[1] in ACCENTI:
                out.append("{\\" + ACCENTI[d[1]] + ("{" + d[0] + "}" if ACCENTI[d[1]].isalpha() else d[0]) + "}")
            else:
                out.append("?")
    return "".join(out)


def bib_tex() -> str:
    """biblatex-apa + biber se installati (APA 7), altrimenti natbib + bibtex (apalike):
    cosi' il PDF esce su qualunque distribuzione LaTeX. Il testo usa sempre \\citeN / \\citeP."""
    kpse = shutil.which("kpsewhich")
    apa = False
    if kpse and shutil.which("biber"):
        r = subprocess.run([kpse, "apa.bbx"], capture_output=True, text=True)
        apa = bool(r.stdout.strip())
    if __import__("os").environ.get("PAPER_BIB") == "bibtex":   # forza il ripiego (test)
        apa = False
    if apa:
        return "\n".join(["% backend: biber", r"\usepackage[style=apa,backend=biber]{biblatex}",
                          r"\addbibresource{gen/fonti.bib}", r"\newcommand{\citeN}{\textcite}",
                          r"\newcommand{\citeP}{\parencite}",
                          r"\newcommand{\stampabib}{\printbibliography[title=References]}", ""])
    return "\n".join(["% backend: bibtex", r"\usepackage[round,sort]{natbib}",
                      r"\newcommand{\citeN}{\citet}", r"\newcommand{\citeP}{\citep}",
                      r"\newcommand{\stampabib}{\renewcommand{\refname}{References}\bibliographystyle{apalike}\bibliography{gen/fonti}}", ""])


def main():
    bozza = "--bozza" in sys.argv
    dry = "--dry-run" in sys.argv
    sezioni = leggi_json(BUILD / "sezioni.json")
    inv = {f["id"]: f for f in (leggi_json(BUILD / "floats.json") or [])}
    if sezioni is None or not inv:
        die("mancano build/sezioni.json o build/floats.json: lancia leggi_scaletta.py e floats.py")
    mancanti, buchi = [], []
    for s in sezioni:
        if s["contenuto"] and draft_di(s["id"]) is None:
            mancanti.append(s["id"])
    if draft_di("abstract") is None:
        mancanti.append("abstract")
    float_senza_tex = [f["id"] for f in inv.values() if f["dove"] == "corpo" and not f.get("tex")
                       and not any(f["id"] in (g.get("gruppo") or []) for g in inv.values() if g.get("tex"))]
    if dry or ((mancanti or float_senza_tex) and not bozza):
        print("Sezioni senza DRAFT:", ", ".join(mancanti) or "nessuna")
        print("Floats del corpo senza .tex:", ", ".join(float_senza_tex) or "nessuno")
        if not dry:
            die("assemblaggio rifiutato (usa --bozza per un PDF di lavoro)")
        return

    GEN.mkdir(parents=True, exist_ok=True)
    (LATEX / "figures").mkdir(exist_ok=True)
    for png in (BUILD / "figures").glob("*.png"):
        shutil.copy(png, LATEX / "figures" / png.name)
    shutil.copy(p("bib"), GEN / "fonti.bib")

    posti: set[str] = set()

    def float_tex(fid: str) -> str:
        f = inv[fid]
        if f.get("tex") is None:
            for g in inv.values():
                if fid in (g.get("gruppo") or []) and g.get("tex"):
                    f = g
                    break
        if f.get("tex") is None:
            return rf"\buco{{float {fid} senza sorgente}}" + "\n"
        chiave = "-".join(f.get("gruppo") or [f["id"]])
        if chiave in posti:
            return ""
        posti.add(chiave)
        return (ROOT / f["tex"]).read_text(encoding="utf-8")

    def blocco(s: dict) -> str:
        out = []
        comando = r"\section" if s["livello"] == 1 else r"\subsection"
        out.append(f"{comando}{{{tex_testo(s['titolo'])}}}\\label{{sec:{s['id']}}}\n")
        d = draft_di(s["id"])
        if d is None:
            if s["contenuto"]:
                out.append(rf"\buco{{Sezione {s['id']} non ancora scritta}}" + "\n")
            return "\n".join(out)
        home = set(s["floats"])
        for par in paragrafi(d):
            out.append(converti(par, bozza, buchi) + "\n")
            for m in re.finditer(r"\[\[(FIG|TAB):([^\]]+)\]\]", par):
                if m.group(2) in home:
                    out.append(float_tex(m.group(2)))
        for fid in s["floats"]:                      # floats mai richiamati: in coda (verifica.py li segnala)
            t = float_tex(fid)
            if t:
                out.append("% ⚠ float non richiamato nel testo\n" + t)
        return "\n".join(out)

    corpo = [blocco(s) for s in sezioni]
    app = appendice(bozza, buchi)
    bt = bib_tex()
    (GEN / "bib.tex").write_text(bt, encoding="utf-8")
    if "backend: bibtex" in bt:                      # bibtex e' a 8 bit: accenti in forma LaTeX
        (GEN / "fonti.bib").write_text(bib_ascii(p("bib").read_text(encoding="utf-8")), encoding="ascii")
    c = cfg()
    (GEN / "titolo.tex").write_text(
        rf"\title{{{tex_testo(c['titolo'])}}}" + "\n"
        + rf"\author{{{tex_testo(c.get('sottotitolo', c['autore']))}}}" + "\n" + r"\date{}" + "\n",
        encoding="utf-8")
    ab = draft_di("abstract")
    (GEN / "abstract.tex").write_text(
        (converti(ab, bozza, buchi) if ab else r"\buco{abstract non ancora scritto}") + "\n", encoding="utf-8")
    (GEN / "corpo.tex").write_text("% Generato da tools/assemble.py. Non modificare a mano.\n\n"
                                   + "\n".join(corpo), encoding="utf-8")
    (GEN / "appendice.tex").write_text("% Generato da tools/assemble.py. Non modificare a mano.\n\n"
                                       + app, encoding="utf-8")
    if buchi and not bozza:
        die(f"{len(buchi)} buchi aperti nel testo: {'; '.join(buchi[:5])} (usa --bozza)")
    print(f"latex/gen/ scritto: {len(corpo)} sezioni di corpo, appendice {'sì' if app else 'NO'}, "
          f"{len(posti)} floats piazzati, {len(buchi)} buchi" + (" (BOZZA)" if bozza else ""))


if __name__ == "__main__":
    main()
