#!/usr/bin/env python3
"""floats.py — prepara figure e tabelle per LaTeX, secondo input/piano.md.

    python3 tools/floats.py

1. Estrae `figures.zip` in `build/figures/` (solo i PNG).
2. Converte `RQ1_tables.doc` (RTF prodotto dal do-file) in HTML con LibreOffice headless e
   ne ricava le 6 tabelle. Ogni tabella diventa `build/tabelle/t<n>.tex` in forma compatta
   (booktabs): restano le righe chiave e le statistiche; i dummy del lead investor diventano
   una riga «Yes» e le righe di coefficienti omessi (0.000 con errore «.») spariscono.
   **Nessun numero viene ricalcolato o arrotondato**: le celle sono quelle del do-file.
3. Scrive `build/floats.json` (inventario: id, tipo, file, sezione, dove, didascalia, label)
   e segnala floats del piano senza file.

Le tabelle-testo (`tabella-testo`) non si generano qui: il loro .tex sta in
`latex/tabelle-testo/` ed e' scritto a partire dalla scaletta, approvato dal gruppo.
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, ROOT, p, scrivi_json  # noqa: E402
from piano import leggi_piano  # noqa: E402

FIG_DIR = BUILD / "figures"
TAB_DIR = BUILD / "tabelle"

# righe dei 16 tipi di lead investor (categoria di riferimento: nessun lead identificato)
LEAD_TYPES = {
    "Accelerator/Incubator", "Angel (individual)", "Angel Group", "Asset Manager",
    "Corporate Venture Capital", "Corporation", "Family Office", "Government",
    "Growth/Expansion", "Hedge Fund", "Impact Investing", "Not-For-Profit Venture Capital",
    "Other", "PE/Buyout", "Venture Capital",
}


def estrai_figure(zip_path: Path) -> list[str]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    nomi = []
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            nome = Path(info.filename).name
            if not nome.lower().endswith(".png") or "/" in nome or nome.startswith("."):
                continue
            with z.open(info) as src, (FIG_DIR / nome).open("wb") as dst:
                shutil.copyfileobj(src, dst)
            nomi.append(nome)
    return sorted(nomi)


def rtf_a_html(rtf: Path) -> str:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sys.exit("ERRORE: LibreOffice (soffice) non trovato: serve per leggere RQ1_tables.doc")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "tabelle.rtf"
        shutil.copy(rtf, src)
        subprocess.run([soffice, "--headless", "--convert-to", "html", "--outdir", tmp, str(src)],
                       check=True, capture_output=True, timeout=180)
        return (Path(tmp) / "tabelle.html").read_text(encoding="utf-8", errors="ignore")


def _testo(frammento: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", frammento))).strip()


def tabelle_da_html(h: str) -> list[dict]:
    out = []
    blocchi = list(re.finditer(r"<table.*?</table>", h, re.S))
    for i, m in enumerate(blocchi):
        prima = _testo(h[blocchi[i - 1].end() if i else 0:m.start()])
        mt = re.search(r"Table\s+(\d+)\.\s*(.+)$", prima)
        dopo_fine = blocchi[i + 1].start() if i + 1 < len(blocchi) else len(h)
        dopo = _testo(h[m.end():dopo_fine])
        nota = re.split(r"Table\s+\d+\.", dopo)[0].strip()
        righe = []
        for r in re.findall(r"<tr.*?</tr>", m.group(0), re.S):
            righe.append([_testo(c) for c in re.findall(r"<t[dh].*?</t[dh]>", r, re.S)])
        out.append({"n": int(mt.group(1)) if mt else i + 1,
                    "titolo": mt.group(2).strip() if mt else "", "nota": nota, "righe": righe})
    return out


def tex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_")]:
        s = s.replace(a, b)
    s = re.sub(r"(?<=\s)x(?=\s)", r"$\\times$", s)          # «R x ln(...)» → R × ln(...)
    s = s.replace("<", r"$<$").replace(">", r"$>$")
    return s


def cella(s: str, etichetta: str = "") -> str:
    s = s.strip()
    m = re.fullmatch(r"(-?\d[\d.]*)\s*(\*{1,3})", s)
    if m:
        return f"{m.group(1)}$^{{{m.group(2)}}}$"
    if etichetta == "Observations" and re.fullmatch(r"\d+\.000", s):   # 9124.000 → 9,124
        return f"{int(float(s)):,}"
    return tex_escape(s)


def compatta(t: dict) -> tuple[list[list[str]], list[str]]:
    """Righe tenute (etichetta + celle) e righe riassunte (Yes)."""
    righe = t["righe"]
    ncol = max(len(r) for r in righe)
    righe = [r + [""] * (ncol - len(r)) for r in righe]
    n_int = next((k for k, r in enumerate(righe) if r[0]), len(righe))
    intest = [r for r in righe[:n_int] if any(r[1:])]
    corpo = righe[n_int:]
    tenute, lead = [], False
    i = 0
    while i < len(corpo):
        r = corpo[i]
        lab = r[0]
        succ = corpo[i + 1] if i + 1 < len(corpo) else [""] * ncol
        ha_se = not succ[0] and any(x.startswith("(") for x in succ[1:])
        if not lab and not any(r[1:]):
            i += 1
            continue
        if lab == "main" and not any(r[1:]):
            i += 1
            continue
        if lab in LEAD_TYPES:
            lead = True
            i += 2 if ha_se else 1
            continue
        omesso = all(x in ("", "0.000") for x in r[1:]) and all(x in ("", "(.)") for x in succ[1:])
        if omesso and ha_se:
            i += 2
            continue
        tenute.append(r)
        if ha_se:
            tenute.append(succ)
            i += 2
        else:
            i += 1
    riassunte = ["Lead-investor type (15 dummies)"] if lead else []
    return intest, tenute, riassunte


def riga_intestazione(r: list[str]) -> str:
    """«One round, '', Two rounds, ''» → \\multicolumn{2}{c}{One round} & ..."""
    celle, k = [tex_escape(r[0])], 1
    while k < len(r):
        n = 1
        while k + n < len(r) and not r[k + n] and r[k]:
            n += 1
        x = tex_escape(r[k])
        celle.append(rf"\multicolumn{{{n}}}{{c}}{{{x}}}" if n > 1 else x)
        k += n
    return " & ".join(celle) + r" \\"


def tabella_tex(t: dict, fid: str, didascalia: str) -> str:
    intest, corpo, riassunte = compatta(t)
    ncol = max(len(r) for r in intest + corpo)
    # le righe FE/statistiche in coda: prima delle quali va la riga dei lead
    idx_fe = next((k for k, r in enumerate(corpo) if r[0].endswith("FE") or r[0] == "Observations"), len(corpo))
    righe_tex = []
    for k, r in enumerate(corpo):
        if k == idx_fe:
            righe_tex.append(r"\midrule")
            for lab in riassunte:
                righe_tex.append(" & ".join([tex_escape(lab)] + ["Yes"] * (ncol - 1)) + r" \\")
        righe_tex.append(" & ".join([tex_escape(r[0])] + [cella(x, r[0]) for x in r[1:]]) + r" \\")
    nota = t["nota"]
    if "clustered" in nota:                         # il do-file ripete la riga generica
        nota = nota.replace("Standard errors in parentheses ", "", 1)
    nota = tex_escape(nota) if nota else ""
    righe_int = [riga_intestazione(r) for r in intest]
    return "\n".join([
        "% Generato da tools/floats.py da RQ1_tables.doc (do-file). Non modificare a mano.",
        r"\begin{table}[tbp]",
        r"\centering\small",
        rf"\caption{{{tex_escape(didascalia)}}}",
        rf"\label{{tab:{fid}}}",
        r"\begin{tabular}{l" + "c" * (ncol - 1) + "}",
        r"\toprule",
        *righe_int,
        r"\midrule",
        *righe_tex,
        r"\bottomrule",
        r"\end{tabular}",
        (rf"\par\smallskip\parbox{{0.95\linewidth}}{{\footnotesize {nota}}}" if nota else ""),
        r"\end{table}",
    ]) + "\n"


def figura_tex(f: dict, coppia: dict | None) -> str:
    if coppia:
        a, b = coppia
        sub = []
        for x in (a, b):
            sub.append("\n".join([
                r"\begin{subfigure}[t]{0.49\linewidth}", r"\centering",
                rf"\includegraphics[width=\linewidth]{{{x['file']}}}",
                rf"\caption{{{tex_escape(x['didascalia'])}}}", rf"\label{{fig:{x['id']}}}",
                r"\end{subfigure}"]))
        return "\n".join([r"\begin{figure}[tbp]", r"\centering", (r"\hfill" + "\n").join(sub),
                          r"\end{figure}"]) + "\n"
    return "\n".join([
        r"\begin{figure}[tbp]", r"\centering",
        rf"\includegraphics[width=0.78\linewidth]{{{f['file']}}}",
        rf"\caption{{{tex_escape(f['didascalia'])}}}", rf"\label{{fig:{f['id']}}}",
        r"\end{figure}"]) + "\n"


def main():
    piano = leggi_piano()
    figure = estrai_figure(p("figure_zip"))
    print(f"{len(figure)} figure in build/figures/")
    tabelle = tabelle_da_html(rtf_a_html(p("tabelle_rtf")))
    print(f"{len(tabelle)} tabelle lette da RQ1_tables.doc: "
          + "; ".join(f"t{t['n']} {t['titolo']}" for t in tabelle))
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    scrivi_json(BUILD / "tabelle_rtf.json", tabelle)

    inventario, problemi, fatte = [], [], set()
    per_coppia = {}
    for f in piano["floats"]:
        if f["dove"] == "corpo" and f.get("affianca"):
            per_coppia.setdefault(f["affianca"], []).append(f)
    for f in piano["floats"]:
        voce = {k: f[k] for k in ("id", "tipo", "file", "dove", "sezione", "didascalia")}
        voce["label"] = ("fig:" if f["tipo"] == "figura" else "tab:") + f["id"]
        if f["tipo"] == "figura":
            if f["file"] not in figure:
                problemi.append(f"{f['id']}: {f['file']} non e' in figures.zip")
            voce["tex"] = None
            if f["dove"] == "corpo" and f["id"] not in fatte:
                coppia = per_coppia.get(f.get("affianca") or "", [])
                coppia = coppia if len(coppia) == 2 else None
                tex = figura_tex(f, coppia)
                gruppo = [x["id"] for x in coppia] if coppia else [f["id"]]
                out = TAB_DIR / f"fig-{'-'.join(gruppo)}.tex"
                out.write_text(tex, encoding="utf-8")
                fatte.update(gruppo)
                voce["tex"] = str(out.relative_to(ROOT))
                voce["gruppo"] = gruppo
        elif f["tipo"] == "tabella":
            n = int(f["file"].lstrip("t"))
            t = next((x for x in tabelle if x["n"] == n), None)
            if t is None:
                problemi.append(f"{f['id']}: tabella {n} assente da RQ1_tables.doc")
                continue
            out = TAB_DIR / f"{f['id']}.tex"
            out.write_text(tabella_tex(t, f["id"], f["didascalia"] or t["titolo"]), encoding="utf-8")
            voce["tex"] = str(out.relative_to(ROOT))
            voce["titolo_dofile"] = t["titolo"]
            voce["celle"] = sorted({x for r in t["righe"] for x in r[1:] if x})
        else:  # tabella-testo
            src = ROOT / f["file"]
            voce["tex"] = f["file"] if src.exists() else None
            if f["dove"] == "corpo" and not src.exists():
                problemi.append(f"{f['id']}: tabella di testo da scrivere ({f['file']})")
        inventario.append(voce)
    for f in figure:
        if not any(x["file"] == f for x in piano["floats"]):
            problemi.append(f"{f}: in figures.zip ma non nel piano")
    scrivi_json(BUILD / "floats.json", inventario)
    corpo = [x["id"] for x in inventario if x["dove"] == "corpo"]
    print(f"Floats nel corpo ({len(corpo)}): {', '.join(corpo)}")
    for x in problemi:
        print("  ⚠", x)


if __name__ == "__main__":
    main()
