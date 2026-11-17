#!/usr/bin/env python3
"""verifica.py — controlli deterministici sul DRAFT di una sezione.

    python3 tools/verifica.py <id>       # una sezione
    python3 tools/verifica.py --tutte    # tutte quelle con DRAFT, piu' i controlli globali

HIGH (bloccano):
- token sconosciuti o malformati; chiavi CIT fuori da `fonti_ammesse` o assenti dal .bib;
  FIG/TAB che non sono floats `corpo`; SEC verso id inesistenti;
- numeri che non stanno nel materiale della sezione (contenuto, numeri dal log, fonti, celle
  dei suoi floats);
- linguaggio causale su gap o hype; «no effect»; prima persona singolare;
- 8 parole consecutive copiate da un verbatim di fonte;
- LEDGER con un numero di righe diverso dai paragrafi;
- (globale) un float `corpo` mai richiamato; un float richiamato in due sezioni come «casa».
MEDIUM (si leggono e si decide frase per frase):
- connettivo inferenziale subito dopo una citazione (thus, therefore, accordingly, hence,
  «, which», «;»); frasi-cerniera d'annuncio; trattini lunghi; elenchi; parole fuori target;
  verdetti delle ipotesi con parole diverse da quelle del paper; caratteri LaTeX grezzi.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comune import (BUILD, TOKEN_RE, cfg, chiavi_bib, conta_parole, die, draft_di,  # noqa: E402
                    leggi_json, ledger_di, numeri, paragrafi)

CAUSALE = re.compile(
    r"\b(effects?|impacts?|causes?|caused|causal(?:ly)?|leads? to|led to|drives?|driven by|"
    r"reduces?|reduced|increases?|increased|raises?|lowers?|results? in)\b", re.I)
CONSENTITI = re.compile(
    r"(marginal effects?|fixed effects?|interaction effects?|main effects?|random effects?|"
    r"causal (?:claim|design|reading|interpretation|identification|effect of)|not causal|"
    r"limits? to (?:a )?causal|average marginal)", re.I)
TEMA = re.compile(r"\b(gap|time between rounds|hype|heat|slow|fast|longer|shorter)\b", re.I)
ANNUNCIO = re.compile(
    r"\b(the (?:following|next|remaining) sections?|this (?:section|paper) (?:first|then|proceeds|is organi[sz]ed)|"
    r"in what follows|the paper proceeds as follows|is structured as follows|we (?:first|then) (?:describe|present|discuss))\b", re.I)
CONNETTIVO = re.compile(r"^\s*(thus|therefore|accordingly|hence|consequently|as a result|this means|it follows)\b", re.I)
VERDETTI_OK = ["right sign, not significant", "rejected, opposite sign", "not supported"]
VERDETTI_KO = re.compile(r"\b(H1b?|H2|H3)\b[^.]{0,80}\b(confirmed|is supported|holds|validated|proved)\b", re.I)


def frasi(testo: str) -> list[str]:
    t = re.sub(r"\s+", " ", testo)
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", t) if x.strip()]


def materiale(s: dict, inv: dict) -> str:
    pezzi = [s["contenuto"], s["numeri_log"], s.get("trappole", ""), s.get("note_editoriali", "")]
    for f in s["fonti"]:
        pezzi.append(f["tesi"])
    for fid in s["floats"]:
        f = inv.get(fid, {})
        pezzi += f.get("celle", []) + [f.get("didascalia", "")]
    return "\n".join(pezzi)


def ngrammi(testo: str, n: int = 8) -> set[tuple]:
    w = re.findall(r"[a-z0-9]+", testo.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def verifica_sezione(s: dict, tutte: dict, inv: dict, bib: dict) -> list[tuple[str, str]]:
    sid = s["id"]
    d = draft_di(sid)
    if d is None:
        return [("HIGH", "nessun DRAFT")]
    r: list[tuple[str, str]] = []
    c = cfg()
    # token
    for m in re.finditer(r"\[\[([^\]]*)\]\]", d):
        if not TOKEN_RE.fullmatch(m.group(0)):
            r.append(("HIGH", f"token malformato: {m.group(0)}"))
    for m in TOKEN_RE.finditer(d):
        tipo, arg = m.group(1), m.group(2)
        if tipo in ("CIT-N", "CIT-P"):
            for k in [x.strip() for x in arg.split(",")]:
                if k not in bib:
                    r.append(("HIGH", f"chiave {k} non in fonti.bib"))
                elif k not in s["fonti_ammesse"]:
                    r.append(("HIGH", f"chiave {k} non ammessa in {sid} (ammesse: {', '.join(s['fonti_ammesse']) or 'nessuna'})"))
        elif tipo in ("FIG", "TAB"):
            f = inv.get(arg)
            if not f or f["dove"] != "corpo":
                r.append(("HIGH", f"{tipo}:{arg} non e' un float del corpo"))
            elif (tipo == "FIG") != (f["tipo"] == "figura"):
                r.append(("HIGH", f"{tipo}:{arg} ha il tipo sbagliato ({f['tipo']})"))
        elif tipo == "SEC" and arg not in tutte:
            r.append(("HIGH", f"SEC:{arg} non esiste"))
        elif tipo in ("GAP", "CIT-NEEDED"):
            r.append(("INFO", f"buco dichiarato: {m.group(0)}"))
    # numeri
    ammessi = numeri(materiale(s, inv))
    ammessi |= {x.lstrip("-") for x in ammessi} | {"1", "2", "3", "4", "5", "6", "7"}
    for n in sorted(numeri(d) - ammessi):
        if n.lstrip("-") not in ammessi:
            r.append(("HIGH", f"numero non nel materiale: {n}"))
    # frase per frase
    fr = frasi(d)
    for i, f in enumerate(fr):
        pulita = CONSENTITI.sub(" ", TOKEN_RE.sub(" ", f))
        if CAUSALE.search(pulita) and TEMA.search(pulita):
            r.append(("HIGH", f"linguaggio causale su gap/hype: «{f[:140]}»"))
        if re.search(r"\bno (?:effect|impact)\b", f, re.I):
            r.append(("HIGH", f"«no effect»: usare la formula del paper (not significant): «{f[:120]}»"))
        if re.search(r"(?<![A-Za-z])I(?![A-Za-z.])", TOKEN_RE.sub(" ", f)) and not re.search(r"\bH?I{2,}\b", f):
            r.append(("HIGH", f"prima persona singolare: «{f[:120]}»"))
        if ANNUNCIO.search(f):
            r.append(("MEDIUM", f"frase-cerniera d'annuncio: «{f[:120]}»"))
        if VERDETTI_KO.search(f):
            r.append(("MEDIUM", f"verdetto con parole diverse dal paper ({' / '.join(VERDETTI_OK)}): «{f[:120]}»"))
        if i > 0 and re.search(r"\[\[CIT-[NP]", fr[i - 1]) and CONNETTIVO.search(f):
            r.append(("MEDIUM", f"connettivo dopo una citazione (porta l'attribuzione): «{f[:120]}»"))
        if re.search(r"\[\[CIT-[NP]:[^\]]+\]\]\s*(?:;|, which)", f):
            r.append(("MEDIUM", f"«;» o «, which» dopo una citazione: «{f[:120]}»"))
    if "—" in d:
        r.append(("MEDIUM", "trattino lungo (—) usato come pausa"))
    if re.search(r"^\s*(?:[-*•]|\d+\.)\s", d, re.M):
        r.append(("MEDIUM", "elenco nel DRAFT: il corpo e' prosa continua"))
    if re.search(r"(?<!\\)[&_#$]|\\[a-zA-Z]+", d):
        r.append(("MEDIUM", "caratteri o comandi LaTeX nel DRAFT: si scrive testo semplice, l'assemblaggio converte"))
    # antiplagio sui verbatim
    gram_d = ngrammi(TOKEN_RE.sub(" ", d))
    for f in s["fonti"]:
        if f["citazione_verbatim"] and gram_d & ngrammi(f["citazione_verbatim"]):
            r.append(("HIGH", f"8 parole consecutive copiate dal verbatim di {f['chiave']}"))
    # parole
    if s["parole"]:
        n, t, tol = conta_parole(d), s["parole"], c["tolleranza_parole"]
        if n > t * (1 + tol):
            r.append(("MEDIUM", f"parole {n} > obiettivo {t} +{int(tol*100)}%: comprimere senza togliere affermazioni, o dichiarare"))
        elif n < t * (1 - tol):
            r.append(("INFO", f"parole {n} < obiettivo {t}: corta (va bene se il materiale finisce, dichiararlo)"))
    # ledger
    np_, nl = len(paragrafi(d)), len(ledger_di(sid))
    if np_ != nl:
        r.append(("HIGH", f"LEDGER con {nl} righe per {np_} paragrafi"))
    # floats della sezione richiamati
    for fid in s["floats"]:
        if not re.search(rf"\[\[(FIG|TAB):{re.escape(fid)}\]\]", d):
            gruppo = inv.get(fid, {}).get("gruppo") or []
            if not any(re.search(rf"\[\[FIG:{re.escape(g)}\]\]", d) for g in gruppo):
                r.append(("HIGH", f"float {fid} della sezione mai richiamato nel testo"))
    return r


def main():
    if len(sys.argv) != 2:
        die("uso: verifica.py <id> | --tutte")
    sezioni = leggi_json(BUILD / "sezioni.json")
    if sezioni is None:
        die("manca build/sezioni.json: lancia tools/leggi_scaletta.py")
    inv = {f["id"]: f for f in (leggi_json(BUILD / "floats.json") or [])}
    if not inv:
        die("manca build/floats.json: lancia tools/floats.py")
    tutte = {s["id"]: s for s in sezioni}
    bib = chiavi_bib()
    if sys.argv[1] == "--tutte":
        bersagli = [s for s in sezioni if draft_di(s["id"]) is not None]
    else:
        if sys.argv[1] not in tutte:
            die(f"sezione {sys.argv[1]} sconosciuta")
        bersagli = [tutte[sys.argv[1]]]
    n_high = 0
    for s in bersagli:
        rilievi = verifica_sezione(s, tutte, inv, bib)
        n_high += sum(1 for g, _ in rilievi if g == "HIGH")
        print(f"== {s['id']} {s['titolo']}: "
              + (", ".join(f"{sum(1 for g, _ in rilievi if g == x)} {x}" for x in ("HIGH", "MEDIUM", "INFO"))))
        for g, msg in rilievi:
            print(f"  [{g}] {msg}")
    if sys.argv[1] == "--tutte":
        print("== globale")
        for fid, f in inv.items():
            if f["dove"] != "corpo":
                continue
            home = [s["id"] for s in sezioni if fid in s["floats"]]
            scritte = [s for s in sezioni if s["id"] in home and draft_di(s["id"])]
            if scritte and not any(re.search(rf"\[\[(FIG|TAB):{re.escape(x)}\]\]", draft_di(s["id"]))
                                   for s in scritte for x in [fid] + (f.get("gruppo") or [])):
                print(f"  [HIGH] float {fid} mai richiamato nella sua sezione ({', '.join(home)})")
                n_high += 1
    sys.exit(1 if n_high else 0)


if __name__ == "__main__":
    main()
