#!/usr/bin/env python3
"""floats.py — prepara figure e tabelle per LaTeX, secondo input/piano.md. Solo Python standard.

    python3 tools/floats.py

1. Estrae `figures.zip` in `build/figures/` (solo i PNG).
2. Legge le tabelle degli RTF del do-file (`tabelle_rtf` in progetto.json: alias → file) con
   `rtf_tabelle.py`, senza LibreOffice. Nel piano una tabella del do-file si indica come
   `<alias>:<numero>` (es. `main:2`, `checks:12`). Ogni tabella diventa `build/tabelle/<id>.tex`
   in forma compatta (booktabs): restano le righe chiave e le statistiche; i dummy del lead
   investor diventano una riga «Yes»; le righe di coefficienti omessi (0.000 con «(.)») spariscono.
   **Nessun numero viene ricalcolato o arrotondato**: le celle sono quelle del do-file.
3. `tabella-testo` e `figura-testo`: il .tex sta in `latex/testo/<id>.tex`, scritto dalla
   scaletta e dal log (non generato qui).
4. Scrive `build/floats.json` (inventario) e segnala i floats del piano senza file.
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import BUILD, ROOT, cfg, scrivi_json  # noqa: E402
from piano import leggi_piano  # noqa: E402
from rtf_tabelle import tabelle_rtf  # noqa: E402

FIG_DIR = BUILD / "figures"
TAB_DIR = BUILD / "tabelle"

# i 15 tipi di lead investor con un coefficiente (base: nessun lead identificato)
LEAD_TYPES = {
    "Accelerator/Incubator", "Angel (individual)", "Angel Group", "Asset Manager",
    "Corporate Venture Capital", "Corporation", "Family Office", "Government",
    "Growth/Expansion", "Hedge Fund", "Impact Investing", "Not-For-Profit Venture Capital",
    "Other", "PE/Buyout", "Venture Capital",
}
CONTEGGI = {"Observations", "Clusters", "Clusters (sector x year)"}


def estrai_figure(zip_path: Path) -> list[str]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    nomi = []
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            nome = Path(info.filename).name
            if not nome.lower().endswith(".png") or nome.startswith("."):
                continue
            with z.open(info) as src, (FIG_DIR / nome).open("wb") as dst:
                shutil.copyfileobj(src, dst)
            nomi.append(nome)
    return sorted(nomi)


def tex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_")]:
        s = s.replace(a, b)
    s = re.sub(r"(?<=\s)x(?=\s)", r"$\\times$", s)          # «R x ln(...)» → R × ln(...)
    return s.replace("<", r"$<$").replace(">", r"$>$")


def cella(s: str, etichetta: str = "") -> str:
    s = s.strip()
    m = re.fullmatch(r"(-?\d[\d.]*)\s*(\*{1,3})", s)
    if m:
        return f"{m.group(1)}$^{{{m.group(2)}}}$"
    if etichetta in CONTEGGI and re.fullmatch(r"\d+\.000", s):   # 9124.000 → 9,124
        return f"{int(float(s)):,}"
    return tex_escape(s)


def compatta(t: dict, tieni_lead: set[str]) -> tuple[list, list, bool]:
    righe = [r for r in t["righe"]]
    ncol = max(len(r) for r in righe)
    righe = [r + [""] * (ncol - len(r)) for r in righe]
    n_int = next((k for k, r in enumerate(righe) if r[0]), len(righe))
    intest = [r for r in righe[:n_int] if any(r[1:])]
    corpo, tenute, lead = righe[n_int:], [], False
    i = 0
    while i < len(corpo):
        r = corpo[i]
        succ = corpo[i + 1] if i + 1 < len(corpo) else [""] * ncol
        ha_se = not succ[0] and any(x.startswith("(") for x in succ[1:])
        passo = 2 if ha_se else 1
        if (not r[0] and not any(r[1:])) or (r[0] == "main" and not any(r[1:])):
            i += 1
            continue
        if r[0] in LEAD_TYPES and r[0] not in tieni_lead:
            lead = True
            i += passo
            continue
        if ha_se and all(x in ("", "0.000") for x in r[1:]) and all(x in ("", "(.)") for x in succ[1:]):
            i += 2
            continue
        if not r[0] and not ha_se and any(r[1:]):     # riga d'intestazione a meta' tabella
            tenute.append(["__intest__"] + r[1:])
            i += 1
            continue
        tenute.append(r)
        if ha_se:
            tenute.append(succ)
        i += passo
    return intest, tenute, lead


def riga_intestazione(r: list[str]) -> str:
    celle, k = [tex_escape(r[0])], 1
    while k < len(r):
        n = 1
        while k + n < len(r) and not r[k + n] and r[k]:
            n += 1
        x = tex_escape(r[k])
        celle.append(rf"\multicolumn{{{n}}}{{c}}{{{x}}}" if n > 1 else x)
        k += n
    return " & ".join(celle) + r" \\"


def tabella_tex(t: dict, fid: str, didascalia: str, tieni_lead: set[str]) -> str:
    intest, corpo, lead = compatta(t, tieni_lead)
    ncol = max(len(r) for r in intest + corpo)
    idx_fe = next((k for k, r in enumerate(corpo) if r[0].endswith("FE") or r[0] in CONTEGGI), len(corpo))
    righe_tex = []
    for k, r in enumerate(corpo):
        if k == idx_fe:
            righe_tex.append(r"\midrule")
            if lead:
                lab = "Lead-investor type dummies" + (" (others)" if tieni_lead else "")
                righe_tex.append(" & ".join([lab] + ["Yes"] * (ncol - 1)) + r" \\")
        if r[0] == "__intest__":
            righe_tex.append(r"\midrule")
            righe_tex.append(" & ".join([""] + [rf"\textit{{{tex_escape(x)}}}" for x in r[1:]]) + r" \\")
            continue
        righe_tex.append(" & ".join([tex_escape(r[0])] + [cella(x, r[0]) for x in r[1:]]) + r" \\")
    nota = t["nota"]
    if "clustered" in nota:
        nota = nota.replace("Standard errors in parentheses ", "", 1)
    nota = tex_escape(nota)
    largo = ncol > 5
    return "\n".join([
        "% Generato da tools/floats.py dagli RTF del do-file. Non modificare a mano.",
        r"\begin{table}[tbp]",
        r"\centering\scriptsize\renewcommand{\arraystretch}{0.92}",
        r"\setlength{\tabcolsep}{4pt}",
        rf"\caption{{{tex_escape(didascalia)}}}",
        rf"\label{{tab:{fid}}}",
        r"\resizebox{\ifdim\width>\linewidth\linewidth\else\width\fi}{!}{%",
        r"\begin{tabular}{l" + "c" * (ncol - 1) + "}",
        r"\toprule",
        *[riga_intestazione(r) for r in intest],
        r"\midrule",
        *righe_tex,
        r"\bottomrule",
        r"\end{tabular}}",
        (rf"\par\smallskip\parbox{{0.95\linewidth}}{{\scriptsize {nota}}}" if nota else ""),
        r"\end{table}",
    ]) + "\n"


def figura_tex(gruppo: list[dict]) -> str:
    """Una figura, o due/tre affiancate nello stesso float: ognuna in una minipage con la SUA
    didascalia, quindi ognuna conserva il suo numero (Figure 5, Figure 6), come nel paper."""
    if len(gruppo) > 1:
        w = 0.48 if len(gruppo) == 2 else 0.31
        pezzi = []
        for x in gruppo:
            pezzi.append("\n".join([
                rf"\begin{{minipage}}[t]{{{w}\linewidth}}", r"\centering",
                rf"\includegraphics[width=\linewidth,height=4.6cm,keepaspectratio]{{figures/{x['file']}}}",
                rf"\caption{{{tex_escape(x['didascalia'])}}}", rf"\label{{fig:{x['id']}}}",
                r"\end{minipage}"]))
        return "\n".join([r"\begin{figure}[tbp]", r"\centering", "\n\\hfill\n".join(pezzi),
                          r"\end{figure}"]) + "\n"
    f = gruppo[0]
    return "\n".join([
        r"\begin{figure}[tbp]", r"\centering",
        rf"\includegraphics[width={f.get("larghezza") or "0.6"}\linewidth,height=6cm,keepaspectratio]{{figures/{f['file']}}}",
        rf"\caption{{{tex_escape(f['didascalia'])}}}", rf"\label{{fig:{f['id']}}}",
        r"\end{figure}"]) + "\n"


def main():
    c = cfg()
    piano = leggi_piano()
    figure = estrai_figure((ROOT / c["figure_zip"]).resolve())
    print(f"{len(figure)} figure in build/figures/")
    rtf = {}
    for alias, path in c["tabelle_rtf"].items():
        rtf[alias] = tabelle_rtf((ROOT / path).resolve())
        print(f"{alias}: " + "; ".join(f"{t['n']} {t['titolo'][:50]}" for t in rtf[alias]))
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    inventario, problemi, fatte = [], [], set()
    gruppi = {}
    for f in piano["floats"]:
        if f["tipo"] == "figura" and f["dove"] == "corpo" and f.get("affianca"):
            gruppi.setdefault(f["affianca"], []).append(f)
    for f in piano["floats"]:
        voce = {k: f[k] for k in ("id", "tipo", "file", "dove", "sezione", "didascalia")}
        voce["label"] = ("fig:" if f["tipo"].startswith("figura") else "tab:") + f["id"]
        voce["tex"] = None
        if f["tipo"] == "figura":
            if f["file"] not in figure:
                problemi.append(f"{f['id']}: {f['file']} non e' in figures.zip")
            elif f["dove"] in ("corpo", "appendice") and f["id"] not in fatte:
                g = gruppi.get(f.get("affianca") or "", [f])
                ids = [x["id"] for x in g]
                out = TAB_DIR / f"fig-{'-'.join(ids)}.tex"
                out.write_text(figura_tex(g), encoding="utf-8")
                fatte.update(ids)
                for x in inventario:                       # figure gia' viste dello stesso gruppo
                    if x["id"] in ids:
                        x["gruppo"] = ids
                voce["tex"] = str(out.relative_to(ROOT))
            voce["gruppo"] = [x["id"] for x in gruppi.get(f.get("affianca") or "", [])] or None
        elif f["tipo"] == "tabella":
            alias, _, n = f["file"].partition(":")
            t = next((x for x in rtf.get(alias, []) if str(x["n"]) == n), None)
            if t is None:
                problemi.append(f"{f['id']}: tabella {f['file']} assente dagli RTF")
                inventario.append(voce)
                continue
            tieni = {x.strip() for x in (f.get("tieni") or "").split(";") if x.strip()}
            out = TAB_DIR / f"{f['id']}.tex"
            out.write_text(tabella_tex(t, f["id"], f["didascalia"] or t["titolo"], tieni), encoding="utf-8")
            voce["tex"] = str(out.relative_to(ROOT))
            voce["celle"] = sorted({x for r in t["righe"] for x in r[1:] if x})
        else:                                              # tabella-testo, figura-testo
            src = ROOT / f["file"]
            if src.exists():
                voce["tex"] = f["file"]
                voce["celle"] = sorted(set(re.findall(r"[−\-]?\d[\d,]*\.?\d*", src.read_text(encoding="utf-8"))))
            elif f["dove"] == "corpo":
                problemi.append(f"{f['id']}: {f['tipo']} da scrivere ({f['file']})")
        inventario.append(voce)
    for f in figure:
        if not any(x["file"] == f for x in piano["floats"]):
            problemi.append(f"{f}: in figures.zip ma non nel piano")
    scrivi_json(BUILD / "floats.json", inventario)
    corpo = [x["id"] for x in inventario if x["dove"] == "corpo"]
    nfig = sum(1 for x in inventario if x["dove"] == "corpo" and x["tipo"].startswith("figura"))
    print(f"Floats nel corpo: {len(corpo)} ({nfig} figure, {len(corpo) - nfig} tabelle)")
    app = [x for x in inventario if x["dove"] == "appendice"]
    afig = sum(1 for x in app if x["tipo"].startswith("figura"))
    print(f"Floats in appendice B: {len(app)} ({afig} figure, {len(app) - afig} tabelle)")
    for x in app:
        if not x.get("tex"):
            problemi.append(f"{x['id']}: float di appendice senza .tex")
    for x in problemi:
        print("  ⚠", x)


if __name__ == "__main__":
    main()
