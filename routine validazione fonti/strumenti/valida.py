#!/usr/bin/env python3
"""Fase 3: valida i JSON dei due lettori e scrive esiti.csv + referto.md.

Equivalente di loop2/scrivi.py della tesi, senza Excel. Applica meccanicamente
le regole che ai lettori sono state solo chieste:
  - la citazione verbatim deve esistere nel testo congelato (>= 25 caratteri);
  - niente citazioni da cookie banner, footer, copyright;
  - 'non verificabile' deve dichiarare cosa e' stato letto (>= 200 caratteri);
  - ATTRIBUZIONE INCERTA a monte vieta 'usabile';
  - la citazione di NotebookLM non ritrovata nel testo locale declassa a
    'non verificabile' (senza riscontro non e' un secondo lettore).
Un output che viola le regole e' SCARTATO, non scritto: va rifatto.

Uso:
    python3 valida.py
"""
import csv, json, os, re
from collections import defaultdict

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
TESTI = os.path.join(RADICE, "lavoro", "testi")
TASK = os.path.join(RADICE, "lavoro", "task")
IN_A = os.path.join(RADICE, "lavoro", "estratti")
IN_B = os.path.join(RADICE, "lavoro", "estratti_nlm")
ESITI_CSV = os.path.join(RADICE, "esiti.csv")
REFERTO = os.path.join(RADICE, "referto.md")

ESITI = ["usabile", "da riformulare", "non usabile", "non verificabile"]
RANGO = {e: i for i, e in enumerate(ESITI)}
CHIAVI_A = {"sezione", "id_fonte", "esito", "cosa_dice_davvero",
            "citazione_verbatim", "posizione", "note"}
CHIAVI_B = {"sezione", "id_fonte", "esito_nlm", "risposta_sintetica",
            "citazione_verbatim_nlm", "fonte_citata_corretta", "note"}

# Testo presente nella pagina ma privo di contenuto: cookie, footer, legale.
BOILERPLATE = re.compile(
    r"\b(cookie|privacy policy|all rights reserved|tutti i diritti riservati|"
    r"©|copyright|p\.? ?iva|partita iva|newsletter|iscriviti|subscribe|"
    r"accetta(?:re)? tutti|accept all|termini e condizioni|terms of use)\b", re.I)


def norm(s):
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def quote_presente(quote, fid):
    q = norm(quote)
    if len(q) < 25:
        return False, "troppo breve per essere verificabile (<25 car.)"
    p = os.path.join(TESTI, fid + ".txt")
    if not os.path.exists(p):
        return False, "testo sorgente assente"
    t = norm(open(p, encoding="utf-8", errors="replace").read())
    if q in t:
        return True, "match esatto"
    return False, "non ritrovata nel testo congelato della pagina"


def claim_del_task(d):
    tf = os.path.join(TASK, f"{d['sezione']}__{d['id_fonte']}.json")
    if os.path.exists(tf):
        try:
            return json.load(open(tf, encoding="utf-8"))
        except Exception:
            pass
    return {}


def valida_a(d):
    e = []
    if set(d) != CHIAVI_A:
        m, x = CHIAVI_A - set(d), set(d) - CHIAVI_A
        if m: e.append(f"chiavi mancanti: {sorted(m)}")
        if x: e.append(f"chiavi estranee: {sorted(x)}")
        if m: return False, e
    if d["esito"] not in ESITI:
        return False, [f"esito non ammesso: {d['esito']!r}"]
    esito, quote = d["esito"], (d.get("citazione_verbatim") or "").strip()
    if esito in ("usabile", "da riformulare") and not quote:
        e.append(f"'{esito}' senza citazione verbatim")
    if quote:
        ok, perche = quote_presente(quote, d["id_fonte"])
        if not ok:
            e.append(f"citazione verbatim {perche}")
        if BOILERPLATE.search(quote):
            e.append("citazione presa da cookie/footer/note legali: non e' contenuto")
    dice = (d.get("cosa_dice_davvero") or "").strip()
    if not dice:
        e.append("cosa_dice_davvero vuoto")
    if esito == "non verificabile" and len(dice) < 200:
        e.append("'non verificabile' senza dichiarare cosa e' stato letto e cercato (<200 car.)")
    task = claim_del_task(d)
    if (task.get("claim") or "").startswith("ATTRIBUZIONE INCERTA"):
        if esito == "usabile":
            e.append("claim marcato ATTRIBUZIONE INCERTA: 'usabile' non ammesso")
        if "ATTRIBUZIONE INCERTA" not in (d.get("note") or ""):
            e.append("claim marcato ATTRIBUZIONE INCERTA: le note devono affrontarlo")
    if task.get("tipo_fonte") == "sito dell'oggetto" and esito == "usabile" \
            and "AUTODICHIARAZIONE" not in (d.get("note") or ""):
        e.append("fonte autoreferenziale giudicata 'usabile' senza nota AUTODICHIARAZIONE")
    return not e, e


def valida_b(d):
    if CHIAVI_B - set(d):
        return False, [f"chiavi mancanti: {sorted(CHIAVI_B - set(d))}"]
    if d["esito_nlm"] not in ESITI:
        return False, [f"esito_nlm non ammesso: {d['esito_nlm']!r}"]
    if d.get("fonte_citata_corretta") is False and d["esito_nlm"] != "non verificabile":
        return False, ["citazione da fonte sbagliata ma esito diverso da 'non verificabile'"]
    q = (d.get("citazione_verbatim_nlm") or "").strip()
    if d["esito_nlm"] in ("usabile", "da riformulare"):
        ok, perche = quote_presente(q, d["id_fonte"]) if q else (False, "assente")
        if not ok:
            d["esito_nlm"] = "non verificabile"
            d["note"] = (d.get("note") or "") + f" [declassato: citazione NotebookLM {perche}]"
    return True, []


def leggi(cartella, valida):
    buoni, scarti = {}, []
    if not os.path.isdir(cartella):
        return buoni, scarti
    for fn in sorted(os.listdir(cartella)):
        if not fn.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(cartella, fn), encoding="utf-8"))
        except Exception as ex:
            scarti.append((fn, [f"JSON illeggibile: {ex}"])); continue
        ok, err = valida(d)
        if ok:
            buoni[(str(d["sezione"]), d["id_fonte"])] = d
        else:
            scarti.append((fn, err))
    return buoni, scarti


def classe(a, b):
    if a is None:
        return "manca lettore A"
    if b is None:
        return "manca NotebookLM"
    if a == b:
        if a == "usabile": return "convergenza positiva"
        if a == "da riformulare": return "convergenza: da riformulare"
        if a == "non usabile": return "convergenza negativa"
        return "entrambi non verificabile"
    return "divergenza (decide la persona)"


ORDINE = ["convergenza negativa", "divergenza (decide la persona)", "entrambi non verificabile",
          "convergenza: da riformulare", "manca NotebookLM", "manca lettore A", "convergenza positiva"]


def main():
    A, sa = leggi(IN_A, valida_a)
    B, sb = leggi(IN_B, valida_b)
    print(f"Lettore A : {len(A)} validi, {len(sa)} scartati")
    print(f"NotebookLM: {len(B)} validi, {len(sb)} scartati")
    for nome, err in sa + sb:
        print(f"  SCARTO {nome}")
        for x in err:
            print(f"         - {x}")

    righe, gruppi = [], defaultdict(list)
    for k in sorted(set(A) | set(B)):
        a, b = A.get(k, {}), B.get(k, {})
        c = classe(a.get("esito"), b.get("esito_nlm"))
        r = {"sezione": k[0], "id_fonte": k[1], "esito_A": a.get("esito", ""),
             "esito_NLM": b.get("esito_nlm", ""), "classe": c,
             "cosa_dice_davvero": a.get("cosa_dice_davvero", ""),
             "citazione_verbatim": a.get("citazione_verbatim", ""),
             "posizione": a.get("posizione", ""), "note_A": a.get("note", ""),
             "note_NLM": b.get("note", "")}
        righe.append(r); gruppi[c].append(r)

    with open(ESITI_CSV, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(righe[0]) if righe else ["sezione"])
        w.writeheader(); w.writerows(righe)

    with open(REFERTO, "w", encoding="utf-8") as fh:
        fh.write(f"# Referto validazione fonti\n\n{len(righe)} coppie · "
                 f"{len(sa) + len(sb)} output scartati da rifare\n\n")
        for c in ORDINE:
            if not gruppi[c]:
                continue
            fh.write(f"## {c} ({len(gruppi[c])})\n\n")
            for r in gruppi[c]:
                fh.write(f"### `{r['sezione']}` × `{r['id_fonte']}`\n"
                         f"- A: **{r['esito_A'] or '-'}** · NotebookLM: **{r['esito_NLM'] or '-'}**\n"
                         f"- Cosa dice davvero: {r['cosa_dice_davvero'][:400]}\n"
                         f"- Nota: {r['note_A'][:300]}\n\n")
    print(f"\nScritti {os.path.basename(ESITI_CSV)} e {os.path.basename(REFERTO)} ({len(righe)} coppie)")


if __name__ == "__main__":
    main()
