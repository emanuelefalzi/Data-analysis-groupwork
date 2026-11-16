#!/usr/bin/env python3
"""Loop 2, fase 3 — validatore unico delle schede fonte.

Raccoglie i JSON dei lettori (`fonti/schede/` del lettore A, `fonti/schede_nlm/`
del secondo lettore), li VALIDA contro il contratto e produce l'unico file da cui
il resto della pipeline legge le fonti: `build/estratti.json`.

La validazione non e' formale: applica meccanicamente le regole che ai lettori
sono state solo chieste. Il punto che conta: ogni `citazione_verbatim` deve
esistere davvero nel testo della fonte, in almeno una delle due rese
(`fonti/testi/`, `fonti/testi_raw/`). Un punto la cui citazione non si ritrova
viene SCARTATO: un'estrazione senza ancora testuale e' un'affermazione inventata
finche' non si prova il contrario.

Ogni punto valido riceve un id stabile `<id_fonte>#<n>` (es. `akerlof1970#3`):
e' quello che la scaletta cita per dire «questa sezione usa questo materiale».

Uso:
    python3 tools/fonti/valida.py           # valida, scrive build/estratti.json e reports/estrazione.md
    python3 tools/fonti/valida.py --solo akerlof1970   # mostra solo quella fonte
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402
from lib.csvio import FontiCSV  # noqa: E402

TIPI_DOC = {"empirico", "teorico", "rassegna", "report", "libro", "capitolo",
            "sito", "intervista", "altro"}
FORZE = {"dimostra", "menziona", "assume"}
CHIAVI_A = {"id_fonte", "tipo_documento", "sintesi", "punti",
            "domande_senza_risposta", "limiti", "note"}
CHIAVI_PUNTO = {"n", "domanda", "cosa_dice", "forza", "citazione_verbatim",
                "sezione", "seconda_mano", "note"}
CHIAVI_B = {"id_fonte", "punti_nlm", "note"}
CHIAVI_PUNTO_B = {"domanda", "cosa_dice", "citazione_verbatim", "fonte_citata_corretta"}
MAX_ALTRO = 3

# citazioni tecnicamente presenti ma prive di contenuto: ringraziamenti,
# copyright, recapiti, intestazioni editoriali (regola V2 della tesi)
FRONT_MATTER = re.compile(
    r"\b(we (?:thank|are grateful|acknowledge)|all rights reserved|"
    r"correspondence (?:to|should)|the views expressed|©|copyright|"
    r"working paper (?:no|series)|any (?:errors|opinions) (?:are|expressed)|"
    r"provided (?:valuable |generous )?funding|electronic copy available at|"
    r"this paper was prepared for)\b", re.I)
NUMERO = re.compile(r"\d+(?:[.,]\d+)*%?")

_cache: dict = {}


def testo_norm(fid: str, raw: bool) -> str:
    k = (fid, raw)
    if k not in _cache:
        p = (comune.TESTI_RAW if raw else comune.TESTI) / f"{fid}.txt"
        _cache[k] = comune.norm(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else ""
    return _cache[k]


def citazione_presente(quote: str, fid: str) -> tuple[bool, str]:
    q = comune.norm(quote)
    if len(q) < 25:
        return False, "citazione troppo breve per essere verificabile (<25 caratteri)"
    for raw in (False, True):
        t = testo_norm(fid, raw)
        if not t:
            continue
        resa = " nella resa -raw" if raw else ""
        if q in t:
            return True, "match esatto" + resa
        # la sillabazione a fine riga puo' spezzare le parole
        if q.replace("- ", "") in t.replace("- ", ""):
            return True, "match dopo rimozione sillabazione" + resa
    if not testo_norm(fid, False) and not testo_norm(fid, True):
        return False, "testo della fonte assente"
    return False, "non ritrovata in nessuna delle due rese del testo"


def valida_punto(p: dict, fid: str, ids_domande: set) -> list[str]:
    e = []
    if set(p) != CHIAVI_PUNTO:
        e.append(f"chiavi del punto: mancano {sorted(CHIAVI_PUNTO - set(p))}, "
                 f"estranee {sorted(set(p) - CHIAVI_PUNTO)}")
        return e
    if p["domanda"] not in ids_domande and p["domanda"] != "altro":
        e.append(f"domanda '{p['domanda']}' non esiste nel brief")
    if p["forza"] not in FORZE:
        e.append(f"forza '{p['forza']}' non ammessa ({sorted(FORZE)})")
    dice = (p.get("cosa_dice") or "").strip()
    if len(dice) < 40:
        e.append("cosa_dice vuoto o troppo scarno")
    quote = p.get("citazione_verbatim") or ""
    ok, perche = citazione_presente(quote, fid)
    if not ok:
        e.append(f"citazione_verbatim {perche}")
    if quote and FRONT_MATTER.search(quote):
        e.append("citazione presa dal front matter: non e' contenuto della fonte")
    if (p.get("seconda_mano") or "").strip() and p["forza"] == "dimostra":
        e.append("seconda_mano compilato ma forza 'dimostra': se la fonte riporta un "
                 "risultato altrui, al massimo lo 'menziona'")
    # i numeri non si parafrasano: ogni cifra di cosa_dice deve stare nella fonte
    t = testo_norm(fid, False) + " " + testo_norm(fid, True)
    for num in NUMERO.findall(dice):
        if len(num.strip("%")) < 2:
            continue
        if num.lower() not in t:
            e.append(f"il numero «{num}» di cosa_dice non compare nel testo della fonte")
    return e


def valida_a(d: dict, ids_domande: set) -> tuple[list[dict], list[str], list[str]]:
    """Ritorna (punti_validi, errori_bloccanti, scarti_di_punti)."""
    if set(d) != CHIAVI_A:
        return [], [f"chiavi: mancano {sorted(CHIAVI_A - set(d))}, estranee {sorted(set(d) - CHIAVI_A)}"], []
    fid = d["id_fonte"]
    err = []
    if d["tipo_documento"] not in TIPI_DOC:
        err.append(f"tipo_documento '{d['tipo_documento']}' non ammesso ({sorted(TIPI_DOC)})")
    if len((d.get("sintesi") or "").strip()) < 80:
        err.append("sintesi vuota o troppo scarna")
    nn = [p.get("n") for p in d["punti"]]
    if len(nn) != len(set(nn)) or not all(isinstance(x, int) for x in nn):
        err.append("i numeri 'n' dei punti devono essere interi e unici")
    # copertura: ogni domanda o ha almeno un punto o e' dichiarata senza risposta
    coperte = {p.get("domanda") for p in d["punti"]}
    vuote = {x.get("domanda") for x in d["domande_senza_risposta"]}
    for q in sorted(ids_domande - coperte - vuote):
        err.append(f"domanda {q} ne' coperta da un punto ne' dichiarata senza risposta")
    for x in d["domande_senza_risposta"]:
        if len((x.get("cosa_ho_cercato") or "").strip()) < 80:
            err.append(f"{x.get('domanda')}: 'cosa_ho_cercato' troppo scarno (va detto cosa si e' "
                       "letto e cercato: non e' una scappatoia)")
    if sum(1 for p in d["punti"] if p.get("domanda") == "altro") > MAX_ALTRO:
        err.append(f"piu' di {MAX_ALTRO} punti 'altro': l'estrazione deve seguire le domande")
    if err:
        return [], err, []
    validi, scarti = [], []
    for p in d["punti"]:
        e = valida_punto(p, fid, ids_domande)
        if e:
            scarti.append(f"punto {fid}#{p.get('n')}: " + "; ".join(e))
        else:
            validi.append(p)
    return validi, [], scarti


def valida_b(d: dict) -> tuple[list[dict], list[str]]:
    if not CHIAVI_B <= set(d):
        return [], [f"chiavi mancanti: {sorted(CHIAVI_B - set(d))}"]
    out, note = [], []
    for p in d["punti_nlm"]:
        if not CHIAVI_PUNTO_B <= set(p):
            note.append(f"punto NLM con chiavi mancanti: {sorted(CHIAVI_PUNTO_B - set(p))}")
            continue
        ok, perche = citazione_presente(p.get("citazione_verbatim") or "", d["id_fonte"])
        # senza riscontro nel testo locale non e' un secondo lettore indipendente:
        # e' un'affermazione non controllabile (il notebook puo' pescare da altre fonti)
        p["riscontrato"] = bool(ok and p.get("fonte_citata_corretta") is not False)
        p["motivo"] = perche if not ok else ("fonte sbagliata" if not p["riscontrato"] else perche)
        out.append(p)
    return out, note


def leggi(cartella: Path) -> dict:
    out = {}
    for f in sorted(cartella.glob("*.json")) if cartella.exists() else []:
        try:
            out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa: BLE001
            out[f.stem] = {"_illeggibile": str(ex)}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo")
    a = ap.parse_args(argv)

    domande = comune.domande_dal_brief()
    ids_domande = {q["id"] for q in domande}
    csvf = FontiCSV(comune.FONTI_CSV); csvf.open()

    A, B = leggi(comune.SCHEDE), leggi(comune.SCHEDE_NLM)
    fonti, punti, rifiutate, scarti, confronto = {}, {}, {}, [], {}

    for fid, d in A.items():
        if a.solo and fid != a.solo:
            continue
        if "_illeggibile" in d:
            rifiutate[fid] = [f"JSON illeggibile: {d['_illeggibile']}"]
            continue
        if d.get("id_fonte") != fid:
            rifiutate[fid] = [f"id_fonte '{d.get('id_fonte')}' diverso dal nome del file"]
            continue
        validi, err, sc = valida_a(d, ids_domande)
        if err:
            rifiutate[fid] = err
            continue
        scarti += sc
        r = csvf.get(fid) or {}
        fonti[fid] = {
            "citazione": r.get("autori", "") + (f" ({r.get('anno')})" if r.get("anno") else ""),
            "titolo": r.get("titolo", ""),
            "peer_reviewed": r.get("peer") or "n.d.",
            "tipo_documento": d["tipo_documento"],
            "sintesi": d["sintesi"],
            "limiti": d["limiti"],
            "note": d["note"],
            "domande_senza_risposta": d["domande_senza_risposta"],
            "nel_bib": None,
        }
        nlm_ok: set = set()
        if fid in B and "_illeggibile" not in B[fid]:
            pb, _ = valida_b(B[fid])
            nlm_ok = {p["domanda"] for p in pb if p["riscontrato"]}
            a_dom = {p["domanda"] for p in validi}
            confronto[fid] = {
                "concordi": sorted(a_dom & nlm_ok),
                "solo_A": sorted(a_dom - nlm_ok),
                "solo_NLM": sorted(nlm_ok - a_dom),   # il lettore A potrebbe aver mancato qualcosa
                "nlm_non_riscontrati": [f"{p['domanda']}: {p['motivo']}" for p in pb if not p["riscontrato"]],
            }
        for p in validi:
            pid = f"{fid}#{p['n']}"
            punti[pid] = dict(p, id=pid, id_fonte=fid,
                              peer_reviewed=fonti[fid]["peer_reviewed"],
                              confermato_nlm=(p["domanda"] in nlm_ok) if fid in B else None)

    try:
        from bib import leggi_bib
        nel_bib = set(leggi_bib(comune.BIB))
        for fid in fonti:
            fonti[fid]["nel_bib"] = fid in nel_bib
    except Exception:  # noqa: BLE001
        pass

    comune.BUILD.mkdir(parents=True, exist_ok=True)
    comune.REPORTS.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().isoformat(timespec="seconds")
    if not a.solo:
        comune.ESTRATTI_JSON.write_text(json.dumps(
            {"generato": ts, "domande": domande, "fonti": fonti, "punti": punti,
             "rifiutate": rifiutate, "scarti": scarti, "confronto_nlm": confronto},
            ensure_ascii=False, indent=1), encoding="utf-8")

    # --- report leggibile -------------------------------------------------
    righe = [f"# Estrazione fonti — validazione del {ts[:10]}", "",
             f"Schede lette: {len(A)} · valide: {len(fonti)} · rifiutate intere: {len(rifiutate)} · "
             f"punti validi: {len(punti)} · punti scartati: {len(scarti)}", ""]
    if rifiutate:
        righe += ["## Schede rifiutate (vanno rifatte dal lettore)", ""]
        for fid, err in rifiutate.items():
            righe.append(f"- **{fid}**: " + " · ".join(err))
        righe.append("")
    if scarti:
        righe += ["## Punti scartati", ""] + [f"- {s}" for s in scarti] + [""]
    righe += ["## Copertura per domanda", ""]
    for q in domande:
        chi = sorted({p["id_fonte"] for p in punti.values() if p["domanda"] == q["id"]})
        righe.append(f"- **{q['id']}** {q['testo']} — {len(chi)} fonti: {', '.join(chi) or '⚠ NESSUNA'}")
    righe.append("")
    if confronto:
        righe += ["## Confronto con il secondo lettore (NotebookLM)", ""]
        for fid, c in confronto.items():
            flag = " ⚠" if c["solo_NLM"] else ""
            righe.append(f"- **{fid}**{flag}: concordi {c['concordi']} · solo A {c['solo_A']} · "
                         f"solo NLM {c['solo_NLM']}"
                         + (f" · NLM non riscontrati: {c['nlm_non_riscontrati']}" if c["nlm_non_riscontrati"] else ""))
        righe += ["", "«solo NLM» = il secondo lettore ha trovato, con citazione riscontrata, una risposta "
                  "che il lettore A dichiara assente: si rilegge la fonte, decide la persona.", ""]
    senza_scheda = [i for i in csvf.all_ids() if csvf.stato(i) != "abbandonata"
                    and (comune.TESTI / f"{i}.txt").exists() and i not in A]
    if senza_scheda:
        righe += [f"## Fonti con testo ma senza scheda ({len(senza_scheda)})", "",
                  ", ".join(senza_scheda), ""]
    fuori_bib = [f for f, v in fonti.items() if v["nel_bib"] is False]
    if fuori_bib:
        righe += ["## Fonti senza voce in fonti/fonti.bib (non citabili nel Word finché manca)", "",
                  ", ".join(fuori_bib), ""]
    rep = comune.REPORTS / "estrazione.md"
    if not a.solo:
        rep.write_text("\n".join(righe), encoding="utf-8")
    print("\n".join(righe))
    if not a.solo:
        print(f"\nScritti {comune.rel(comune.ESTRATTI_JSON)} e {comune.rel(rep)}")
    return 2 if rifiutate else 0


if __name__ == "__main__":
    raise SystemExit(main())
