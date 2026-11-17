#!/usr/bin/env python3
"""tabelle_testo.py — costruisce e CONTROLLA le tabelle testuali del paper (quelle che il do-file
non produce: Tables 1, 2, 3, 4, 7, 13, 14 del paper v4).

    python3 tools/tabelle_testo.py           # scrive <id>.tex e tracciabilita.md, esce con 1 se un controllo fallisce

I sorgenti stanno in `4. risultati/tables testuali/<id>.md` (progetto.json → `tabelle_testo`).
Ogni cella del corpo della tabella dichiara la sua fonte fra graffe; le intestazioni no.

    | H1: longer gap, less exit {scaletta 2.1} | −0.071 (p = 0.29) {log L538} |

Fonti ammesse e cosa controlla lo script:
- `{log L538}`        riga di `4. risultati/regression_analysis.txt`: ogni numero della cella deve
                      esserci, arrotondato allo stesso numero di decimali (`< 0.001` vale 0.000);
- `{checks L123}`     stessa cosa su `4. risultati/not_in_log_checks.txt`;
- `{rtf main:2}`      tabella del do-file (alias in progetto.json → `tabelle_rtf`): ogni numero
                      della cella deve essere una cella di quella tabella;
- `{construction L127}` riga di `2. dataset/construction.txt` (testo di construction.pdf):
                      numeri e nomi `in_codice` devono esserci;
- `{scaletta 2.3}`    sezione di `scaletta.md`: deve esistere; i numeri della cella devono stare
                      nel testo della sezione; ogni `[cite: chiave]` deve stare nel suo blocco
                      Sources e in `fonti.bib`;
- `{glossary}`        `glossary.md`: i nomi `in_codice` devono esserci;
- `{rules}`           RULES.md: la cella deve essere una delle tre formule dei verdetti;
- `{paper T2}`        tabella del paper v4: fonte secondaria, non controllabile a macchina;
                      lo script la conta e la segnala nel report.
Una cella del corpo non vuota senza fonte e' un errore. Con piu' fonti, un numero basta che
stia in una.

Sintassi della cella: testo semplice (β1, ×, − in Unicode), `[cite: k1, k2]` → (Autore, anno),
`[citeN: k]` → Autore (anno), `$...$` matematica LaTeX. Una riga che inizia con `| ~ |` e' un
\\midrule. Testata del file: `label:`, `didascalia:`, `colonne:` (spec LaTeX delle colonne),
`nota:` (facoltativa, con le sue fonti fra graffe), `font:` (facoltativo, default footnotesize).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import ROOT, cfg, chiavi_bib, die, p  # noqa: E402
from leggi_scaletta import parse_scaletta, sources  # noqa: E402
from rtf_tabelle import tabelle_rtf  # noqa: E402

TAG = re.compile(r"\{(log|checks|construction|rtf|scaletta|glossary|rules|paper)\b\s*([^}]*)\}")
CITE = re.compile(r"\[(cite|citeN):\s*([^\]]+)\]")
NUM = re.compile(r"(?<![\w.])[−\-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])[−\-+]?\d+(?:\.\d+)?|(?<![\w\d])[−\-]?\.\d+")
# numeri che sono rimandi, non dati: «Table 6», «Tables 6 and 8», «column 2», «Section 3.1»
RIMANDO = re.compile(r"\b(?:Tables?|Figures?|columns?|Sections?)\s+\d+(?:\.\d+)?(?:\s*(?:,|and)\s*\d+(?:\.\d+)?)*")
VERDETTI = {"right sign, not significant", "rejected, opposite sign", "not supported"}


def numeri_cella(t: str) -> list[str]:
    t = RIMANDO.sub(" ", CITE.sub(" ", TAG.sub(" ", t))).replace("$", " ")
    return [m.group(0).replace("−", "-").lstrip("+") for m in NUM.finditer(t)]


def numeri_fonte(t: str) -> list[float]:
    out = []
    for m in re.finditer(r"-?\d[\d,]*\.?\d*|-?\.\d+", t):
        try:
            out.append(float(m.group(0).replace(",", "")))
        except ValueError:
            pass
    return out


def combacia(n: str, fonte: list[float], testo_fonte: str) -> bool:
    if n.replace(",", "") in testo_fonte.replace(",", ""):
        return True
    dec = len(n.split(".")[1]) if "." in n else 0
    x = float(n.replace(",", ""))
    return any(round(y, dec) == x for y in fonte)


class Contesto:
    def __init__(self):
        c = cfg()
        self.log = (ROOT / c["log_stata"][0]).resolve().read_text(errors="ignore").split("\n")
        self.checks = (ROOT / c["log_stata"][1]).resolve().read_text(errors="ignore").split("\n")
        self.constr = p("construction_txt").read_text(errors="ignore").split("\n")
        self.glossario = p("glossario").read_text(encoding="utf-8")
        testo = p("scaletta").read_text(encoding="utf-8")
        self.scaletta = {s["id"]: s for s in parse_scaletta(testo)}
        self.bib = chiavi_bib()
        self.rtf = {a: tabelle_rtf((ROOT / f).resolve()) for a, f in c["tabelle_rtf"].items()}


def riga_di(righe: list[str], rif: str) -> str | None:
    m = re.fullmatch(r"L(\d+)", rif.strip())
    if not m or not (1 <= int(m.group(1)) <= len(righe)):
        return None
    return righe[int(m.group(1)) - 1]


def controlla_cella(testo: str, ctx: Contesto) -> tuple[list[str], list[str]]:
    """Ritorna (errori, fonti dichiarate)."""
    tags = TAG.findall(testo)
    pulito = TAG.sub("", testo).strip()
    err, dich = [], [f"{t} {r}".strip() for t, r in tags]
    if not pulito:
        return [], dich
    if not tags:
        return [f"«{pulito}»: nessuna fonte"], dich
    nums = numeri_cella(testo)
    lessico, valori, sez_cit = "", [], []
    for tipo, rif in tags:
        rif = rif.strip()
        if tipo in ("log", "checks", "construction"):
            righe = {"log": ctx.log, "checks": ctx.checks, "construction": ctx.constr}[tipo]
            r = riga_di(righe, rif)
            if r is None:
                err.append(f"{{{tipo} {rif}}}: riga inesistente")
                continue
            lessico += " " + r
            valori += numeri_fonte(r)
            if "< 0.001" in pulito or "<0.001" in pulito:
                valori.append(0.001) if re.search(r"\b0\.000\b", r) else None
        elif tipo == "rtf":
            alias, _, n = rif.partition(":")
            t = next((x for x in ctx.rtf.get(alias, []) if str(x["n"]) == n), None)
            if t is None:
                err.append(f"{{rtf {rif}}}: tabella inesistente")
                continue
            celle = " ".join(c for r in t["righe"] for c in r[1:])
            lessico += " " + celle
            valori += numeri_fonte(celle)
        elif tipo == "scaletta":
            s = ctx.scaletta.get(rif)
            if s is None:
                err.append(f"{{scaletta {rif}}}: sezione inesistente")
                continue
            lessico += " " + " ".join(str(v) for v in s.values())
            valori += numeri_fonte(" ".join(str(v) for v in s.values()))
            sez_cit.append(s)
        elif tipo == "glossary":
            lessico += " " + ctx.glossario
            valori += numeri_fonte(ctx.glossario)
        elif tipo == "rules":
            if pulito.lower() not in VERDETTI:
                err.append(f"«{pulito}»: non e' una delle formule dei verdetti di RULES.md")
        elif tipo == "paper":
            lessico += " " + pulito                   # fonte secondaria: non controllabile
            valori += numeri_fonte(pulito.replace("−", "-"))
    for n in nums:
        if n.endswith("0.001") and "<" in pulito:
            if not any(abs(v - 0.001) < 1e-9 or v == 0 for v in valori) and not re.search(r"\b0\.000\b", lessico):
                err.append(f"«{n}» (p < 0.001) non trovato nelle fonti")
            continue
        if not combacia(n, valori, lessico):
            err.append(f"numero {n} non trovato in {', '.join(dich)}")
    for codice in re.findall(r"`([^`]+)`", pulito):
        if any(t in ("construction", "glossary", "scaletta") for t, _ in tags) and \
                codice.replace("\\", "") not in lessico.replace("\\", ""):
            err.append(f"`{codice}` non trovato in {', '.join(dich)}")
    for _, chiavi in CITE.findall(pulito):
        for k in [x.strip() for x in chiavi.split(",")]:
            if k not in ctx.bib:
                err.append(f"[cite: {k}] non in fonti.bib")
            elif not sez_cit:
                err.append(f"[cite: {k}] senza una {{scaletta x.y}} che la ammetta")
            elif not any(k in [c for ks, _ in sources(s.get("sources", "") or "") for c in ks] or
                         k in s.get("_sources_keys", []) for s in sez_cit):
                err.append(f"[cite: {k}] non nel blocco Sources di {', '.join('scaletta ' + s['id'] for s in sez_cit)}")
    return err, dich


def tex_cella(t: str) -> str:
    from assemble import tex_testo  # noqa: E402
    t = TAG.sub("", t).strip()
    pezzi, last = [], 0
    for m in re.finditer(r"\$[^$]*\$|" + CITE.pattern, t):
        pezzi.append(tex_testo(t[last:m.start()]))
        if m.group(0).startswith("$"):
            pezzi.append(m.group(0))
        else:
            cmd = r"\citeN" if m.group(1) == "citeN" else r"\citeP"
            pezzi.append(f"{cmd}{{{','.join(x.strip() for x in m.group(2).split(','))}}}")
        last = m.end()
    pezzi.append(tex_testo(t[last:]))
    s = "".join(pezzi)
    return re.sub(r"\$\\(beta|rho|theta)\$(\d)", r"$\\\1_{\2}$", s)


def leggi_md(path: Path) -> dict:
    testo = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    meta = dict(re.findall(r"^(label|didascalia|colonne|nota|font):\s*(.+)$", testo, re.M))
    righe = [r.strip() for r in testo.splitlines() if r.strip().startswith("|")]
    if len(righe) < 3:
        die(f"{path.name}: nessuna tabella markdown")
    celle = [[c.strip() for c in r.strip("|").split("|")] for r in righe]
    return {"meta": meta, "intest": celle[0], "corpo": celle[2:]}


def main():
    cartella = p("tabelle_testo")
    ctx = Contesto()
    # le chiavi del blocco Sources: parse_scaletta le tiene in "sources" (testo grezzo)
    report, errori_tot = ["# Tracciabilità delle tabelle testuali", "",
                          "Generato da `skill-redigere paper latex/tools/tabelle_testo.py`. "
                          "Una riga per cella: valore, fonte dichiarata, esito del controllo.", ""], 0
    for md in sorted(cartella.glob("T*.md"), key=lambda x: int(re.sub(r"\D", "", x.stem) or 0)):
        t = leggi_md(md)
        meta = t["meta"]
        lab = meta.get("label", md.stem)
        report += [f"## {lab} · {meta.get('didascalia', '')}", "", "| Cella | Fonte | Esito |", "|---|---|---|"]
        righe_tex, n_err, secondarie = [], 0, 0
        for r in t["corpo"]:
            if r and r[0] == "~":
                righe_tex.append(r"\midrule")
                continue
            for c in r:
                err, dich = controlla_cella(c, ctx)
                if not TAG.sub("", c).strip():
                    continue
                secondarie += any(d.startswith("paper") for d in dich)
                esito = "✗ " + "; ".join(err) if err else ("⚠ fonte secondaria" if any(d.startswith("paper") for d in dich) else "✓")
                n_err += len(err)
                report.append(f"| {TAG.sub('', c).strip().replace('|', '/')} | {'; '.join(dich) or '—'} | {esito} |")
            righe_tex.append(" & ".join(tex_cella(c) for c in r) + r" \\")
        nota = meta.get("nota", "")
        if nota:
            err, dich = controlla_cella(nota, ctx)
            n_err += len(err)
            report.append(f"| *(nota)* | {'; '.join(dich) or '—'} | {'✗ ' + '; '.join(err) if err else '✓'} |")
        errori_tot += n_err
        report.append("")
        tex = "\n".join([
            f"% Generato da tools/tabelle_testo.py da «{md.name}». Non modificare a mano:",
            "% si corregge il .md e si rilancia lo script. Fonti di ogni cella: tracciabilita.md.",
            r"\begin{table}[tbp]",
            "\\centering\\" + meta.get("font", "footnotesize"),
            rf"\caption{{{tex_cella(meta.get('didascalia', ''))}}}",
            rf"\label{{tab:{lab}}}",
            r"\begin{tabular}{" + meta.get("colonne", "l" * len(t["intest"])).replace(" ", "") + "}",
            r"\toprule",
            " & ".join(tex_cella(c) for c in t["intest"]) + r" \\",
            r"\midrule",
            *righe_tex,
            r"\bottomrule",
            r"\end{tabular}",
            (rf"\par\smallskip\parbox{{0.95\linewidth}}{{\scriptsize {tex_cella(nota)}}}" if nota else ""),
            r"\end{table}", ""])
        (cartella / f"{md.stem}.tex").write_text(tex, encoding="utf-8")
        print(f"{md.stem}: {'OK' if not n_err else f'{n_err} errori'}"
              + (f", {secondarie} celle con fonte secondaria (paper v4)" if secondarie else ""))
    (cartella / "tracciabilita.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Report: {cartella / 'tracciabilita.md'}")
    sys.exit(1 if errori_tot else 0)


if __name__ == "__main__":
    main()
