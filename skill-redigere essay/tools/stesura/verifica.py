#!/usr/bin/env python3
"""Tutti i controlli deterministici su una sezione scritta, in un colpo solo.

Nella tesi erano sei script separati (lint_numeri, lint_budget, lint_ngrammi,
lint_citazioni, ledger_renumber, glossario/lint). Qui sono funzioni di un unico
file, perche' su un essay si lanciano sempre insieme dopo ogni sezione.

  token     i soli token ammessi sono [[CIT-N:k]] [[CIT-P:k]] [[CIT-NEEDED: …]] [[GAP: …]];
            k deve essere fra le fonti ammesse della sezione e stare nel .bib     -> HIGH
  ngrammi   8 parole consecutive copiate da una citazione verbatim dei punti
            della sezione (o, con --tutte, da qualunque testo di fonte)          -> HIGH
  numeri    ogni cifra/percentuale/anno del DRAFT deve stare nel materiale
            (scaletta + punti + brief); fuori dalla sezione ma altrove = avviso   -> HIGH
  parole    parole contate come nel Word contro il target ±tolleranza; nessun
            pavimento: una sezione corta si segnala, non si allunga              -> MEDIUM
  ledger    tante righe quanti paragrafi; CONTENUTO["…"] ritrovabile nella
            scaletta; PUNTO[…] fra i punti della sezione                          -> HIGH
  glossario forme vietate e uso prima della definizione (se esiste il glossario)  -> HIGH
  stile     prima persona, metadiscorso, frasi-cerniera di annuncio, em dash,
            connettivo inferenziale subito dopo una citazione                    -> MEDIUM

L'ultimo controllo e' la lezione piu' costosa della tesi: chiudere il periodo
citato non chiude l'attribuzione. «… [CIT]. Governance thus becomes …» fa
leggere la conseguenza come se venisse dalla fonte. Lo script lo sospetta, il
giudizio resta al claim-auditor.

Uso:
    python3 tools/stesura/verifica.py 2.1
    python3 tools/stesura/verifica.py --tutte          # tutte le sezioni scritte + ngrammi sul corpus intero
    python3 tools/stesura/verifica.py 2.1 --rinumera   # rinumera i ¶ del LEDGER prima di controllare
Exit: 0 pulito, 2 almeno un HIGH.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

N_GRAMMI = 8
TOK = re.compile(r"[a-z0-9']+")
TUTTI_TOKEN = re.compile(r"\[\[[^\]]*\]\]")
NUM = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*\s?%?")
# il connettivo puo' stare in apertura («Thus, …») o dopo il soggetto («Governance thus
# becomes …», il caso trovato nella tesi): si cerca nelle prime sei parole della frase
CONNETTIVI = re.compile(r"^\W*(?:[\w'-]+\s+){0,5}?(thus|therefore|accordingly|hence|so|consequently|"
                        r"this means|quindi|pertanto|di conseguenza|dunque|ne segue)\b", re.I)
PRIMA_PERSONA = re.compile(r"\b(I|we|our|us|my|noi|nostro|nostra|nostri|nostre)\b")
METADISCORSO = re.compile(r"\b(this (essay|paper|section|chapter|thesis)|questo (saggio|elaborato|capitolo|paragrafo))\b", re.I)
CERNIERA = re.compile(r"\b(the following (section|sections|paragraphs?|pages?)|"
                      r"(will|shall) (now )?(be )?(discuss|examin|analy[sz]|address|turn)|"
                      r"turning now to|nel(la)? (prossim|seguent)[ei] (paragraf|sezion))", re.I)


class Esito:
    def __init__(self, sid):
        self.sid, self.f = sid, []

    def add(self, sev, cosa, dettaglio):
        self.f.append((sev, cosa, dettaglio))

    def alti(self):
        return [x for x in self.f if x[0] == "HIGH"]


def frasi(testo):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\[“\"(])", testo) if x.strip()]


def ngrammi(testo):
    t = TOK.findall(testo.lower())
    return {tuple(t[i:i + N_GRAMMI]) for i in range(len(t) - N_GRAMMI + 1)}


# ---------------------------------------------------------------------------

def c_token(e, s, draft, bib):
    for m in TUTTI_TOKEN.finditer(draft):
        t = m.group(0)
        mc = comune.TOKEN_CIT.fullmatch(t)
        if mc:
            k = mc.group(2)
            if k not in s["fonti_ammesse"]:
                e.add("HIGH", "token", f"{t}: «{k}» non e' fra le fonti ammesse della sezione "
                      f"({', '.join(s['fonti_ammesse']) or 'nessuna'})")
            if bib is not None and k not in bib:
                e.add("HIGH", "token", f"{t}: «{k}» non ha voce in fonti/fonti.bib")
        elif comune.TOKEN_BUCO.fullmatch(t):
            e.add("INFO", "buco dichiarato", t)
        else:
            e.add("HIGH", "token", f"{t}: forma non ammessa (solo CIT-N, CIT-P, CIT-NEEDED, GAP)")
    if "⚠" in draft or "RICHIESTA AUTORE" in draft:
        e.add("HIGH", "token", "segni di stato (⚠ / RICHIESTA AUTORE) dentro il DRAFT: usa [[GAP: motivo]]")


def c_ngrammi(e, s, draft, punti, corpus=None):
    mine = ngrammi(comune.TOKEN_CIT.sub(" ", draft))
    fonti = [(p, punti[p]["citazione_verbatim"]) for p in s["punti"] if p in punti]
    if corpus:
        fonti += corpus
    for et, src in fonti:
        comuni = mine & ngrammi(src)
        for ng in sorted(comuni)[:3]:
            e.add("HIGH", "ngrammi", f"copiato da {et}: «{' '.join(ng)}»")


def c_numeri(e, s, draft, punti, sez):
    proprio = comune.norm(s["contenuto"] + " " + " ".join(
        punti[p]["cosa_dice"] + " " + punti[p]["citazione_verbatim"] for p in s["punti"] if p in punti))
    altrove = comune.norm(" ".join(x["contenuto"] for x in sez.values()) + " "
                          + " ".join(p["cosa_dice"] for p in punti.values())
                          + (comune.BRIEF.read_text(encoding="utf-8") if comune.BRIEF.exists() else ""))
    pulito = TUTTI_TOKEN.sub(" ", draft)
    for n in {x.strip() for x in NUM.findall(pulito)}:
        nn = n.replace(" ", "").lower()
        if len(nn.strip("%")) < 2 and "%" not in nn:
            continue
        if nn in proprio.replace(" %", "%"):
            continue
        if nn in altrove.replace(" %", "%"):
            e.add("WARN", "numeri", f"«{n}» non e' nel materiale di questa sezione (sta altrove)")
        else:
            e.add("HIGH", "numeri", f"«{n}» non compare in nessun materiale: inventato o calcolato?")


def c_parole(e, s, draft, cfg):
    n = comune.parole_come_nel_word(draft)
    t = s["parole_target"]
    if not t:
        e.add("INFO", "parole", f"{n} parole (nessun target)")
        return
    tol = cfg["tolleranza_parole"]
    lo, hi = int(t * (1 - tol)), int(t * (1 + tol))
    if n > hi:
        e.add("MEDIUM", "parole", f"{n} parole, sopra la banda {lo}-{hi}")
    elif n < lo:
        e.add("MEDIUM", "parole", f"{n} parole, sotto la banda {lo}-{hi}: se il materiale non basta "
              "va bene corta, ma va dichiarato (materiale: %d)" % s["parole_materiale"])
    else:
        e.add("INFO", "parole", f"{n} parole, dentro la banda {lo}-{hi}")


def c_ledger(e, s, draft, ledger):
    pars = comune.paragrafi(draft)
    righe = [r for r in ledger.splitlines() if re.match(r"\s*-\s*¶\d+", r)]
    if len(righe) != len(pars):
        e.add("HIGH", "ledger", f"{len(righe)} righe di LEDGER per {len(pars)} paragrafi di DRAFT "
              "(usa --rinumera dopo aver sistemato le righe)")
    cont = comune.norm(s["contenuto"])
    for m in re.finditer(r'CONTENUTO\["(.+?)"\]', ledger):
        frase = comune.norm(m.group(1)).rstrip(".…")
        if frase and frase not in cont:
            e.add("HIGH", "ledger", f'CONTENUTO["{m.group(1)[:60]}…"] non si ritrova nel contenuto della sezione')
    for m in re.finditer(r"PUNTO\[([^\]]+)\]", ledger):
        if m.group(1) not in s["punti"]:
            e.add("HIGH", "ledger", f"PUNTO[{m.group(1)}] non e' fra i punti della sezione")


def rinumera(sid):
    p = comune.file_sezione(sid)
    txt = p.read_text(encoding="utf-8")
    i = txt.find("## LEDGER")
    if i < 0:
        return
    n = iter(range(1, 1000))
    nuovo = re.sub(r"¶\d+", lambda _: f"¶{next(n)}", txt[i:])
    p.write_text(txt[:i] + nuovo, encoding="utf-8")


def c_glossario(e, s, draft):
    if not comune.GLOSSARIO.exists():
        return
    sys.path.insert(0, str(comune.ROOT / "tools" / "glossario"))
    import lint as glint  # noqa: E402
    for v in glint.lint(comune.TOKEN_CIT.sub(" ", draft), s["id"]):
        e.add("HIGH" if v.gravita == "blocca" else "WARN", "glossario", str(v).replace("\n", " "))


def c_stile(e, s, draft, primo_o_ultimo):
    pulito = TUTTI_TOKEN.sub(lambda m: " CIT " if "CIT-N" in m.group(0) or "CIT-P" in m.group(0) else " ", draft)
    for m in PRIMA_PERSONA.finditer(pulito):
        e.add("MEDIUM", "stile", f"prima persona «{m.group(0)}»")
        break
    if not primo_o_ultimo:
        for m in METADISCORSO.finditer(pulito):
            e.add("MEDIUM", "stile", f"metadiscorso «{m.group(0)}» fuori da introduzione/conclusione: "
                  "afferma la cosa, non annunciarla (e non sostituirlo col passivo impersonale)")
    for m in CERNIERA.finditer(pulito):
        e.add("MEDIUM", "stile", f"frase-cerniera di annuncio «{m.group(0)}»: l'ordine lo dicono i titoli")
    if "—" in draft or " – " in draft or "--" in draft:
        e.add("MEDIUM", "stile", "trattino lungo usato come pausa: usa la punteggiatura naturale")
    fr = frasi(draft)
    for a, b in zip(fr, fr[1:]):
        if comune.TOKEN_CIT.search(a) and CONNETTIVI.search(b) and not comune.TOKEN_CIT.search(b):
            e.add("MEDIUM", "connettivo", f"dopo una citazione: «{b[:80]}…» — il connettivo porta "
                  "l'attribuzione nella frase dopo. Togli la citazione e rileggi: se la frase resta "
                  "sospesa, la formula di derivazione va all'inizio («Applied to …,»)")
    for m in re.finditer(r"\[\[CIT-[NP]:[^\]]+\]\]\s*[;,]\s*(which|the same|and thus|so)\b", draft):
        e.add("MEDIUM", "connettivo", f"«{m.group(0)}»: punto e virgola/relativa subito dopo la citazione")


# ---------------------------------------------------------------------------

def verifica(sid, sez, punti, cfg, bib, corpus=None):
    s = sez[sid]
    e = Esito(sid)
    draft, ledger = comune.draft_di(sid), comune.ledger_di(sid)
    if not draft:
        e.add("INFO", "assente", "nessun DRAFT")
        return e
    ids = [k for k, v in sez.items() if not v["escludi"]]
    primo_o_ultimo = sid in (ids[0], ids[-1]) or sez[sid]["parent"] in (ids[0], ids[-1])
    c_token(e, s, draft, bib)
    c_ngrammi(e, s, draft, punti, corpus)
    c_numeri(e, s, draft, punti, sez)
    c_parole(e, s, draft, cfg)
    c_ledger(e, s, draft, ledger)
    c_glossario(e, s, draft)
    c_stile(e, s, draft, primo_o_ultimo)
    return e


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sezione", nargs="?")
    ap.add_argument("--tutte", action="store_true")
    ap.add_argument("--rinumera", action="store_true")
    ap.add_argument("--json", action="store_true", help="output macchina")
    a = ap.parse_args(argv)
    cfg = comune.config()
    sez = comune.sezioni()
    try:
        punti = comune.estratti()["punti"]
    except SystemExit:
        punti = {}
    from bib import leggi_bib
    bib = set(leggi_bib(comune.BIB)) if comune.BIB.exists() else None

    if a.tutte:
        target = [k for k, v in sez.items() if not v["escludi"] and comune.draft_di(k)]
        corpus = [(f.name, f.read_text(encoding="utf-8", errors="replace"))
                  for f in sorted(comune.TESTI.glob("*.txt"))]
    elif a.sezione:
        if a.sezione not in sez:
            sys.exit(f"sezione «{a.sezione}» non in scaletta")
        target, corpus = [a.sezione], None
    else:
        ap.print_help()
        return 1

    tot_alti, risultati = 0, {}
    for sid in target:
        if a.rinumera:
            rinumera(sid)
        e = verifica(sid, sez, punti, cfg, bib, corpus)
        risultati[sid] = e.f
        tot_alti += len(e.alti())
        if not a.json:
            print(f"== {sid} {sez[sid]['titolo']}")
            for sev, cosa, det in sorted(e.f, key=lambda x: ["HIGH", "MEDIUM", "WARN", "INFO"].index(x[0])):
                print(f"  [{sev}] {cosa}: {det}")
    if a.json:
        print(json.dumps(risultati, ensure_ascii=False, indent=1))
    else:
        print(f"\n{tot_alti} finding HIGH." if tot_alti else "\nNessun HIGH.")
    return 2 if tot_alti else 0


if __name__ == "__main__":
    raise SystemExit(main())
