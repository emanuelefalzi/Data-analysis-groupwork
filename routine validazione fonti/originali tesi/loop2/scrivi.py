#!/usr/bin/env python3
"""Loop 2 - Fase 3: scrittore unico.

Raccoglie i JSON prodotti dai subagent in estratti/ (e estratti_nlm/),
li VALIDA contro il contratto, e li riversa nel foglio Estratti in
un'unica passata. E' l'unico processo che apre l'Excel in scrittura.

La validazione non e' formale: applica meccanicamente le regole che ai
subagent sono state solo chieste. In particolare verifica che la
citazione verbatim esista davvero nel testo sorgente. Un 'usabile' la
cui citazione non si ritrova viene RIFIUTATO, non scritto.

Uso:
    python3 scrivi.py              # dry-run: valida e mostra, non scrive
    python3 scrivi.py --commit     # scrive davvero
"""
import argparse, json, os, re, shutil, sys
from datetime import datetime

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
XLSX = BASE + "iTOC master.xlsx"
MD   = BASE + "FONTI/pipeline/testi estratti/"
# Seconda resa dello STESSO PDF, con `pdftotext -raw`. Serve solo alla verifica.
# I PDF accademici a due colonne vengono resi in modo diverso dalle due modalita':
# quella di default a volte interfoglia le colonne riga per riga, e allora una frase
# del corpo non esiste come stringa contigua; -raw ricostruisce l'ordine di lettura
# ma su altri documenti sbaglia dove la modalita' di default va bene. Nessuna delle
# due domina: sono complementari. Una citazione autentica si ritrova in ALMENO UNA
# delle due, una citazione inventata in nessuna.
MD_RAW = BASE + "FONTI/pipeline/testi estratti raw/"
TASK = BASE + "FONTI/pipeline/loop2/task/"
IN_A = BASE + "FONTI/estrazioni/estratti/"
IN_B = BASE + "FONTI/estrazioni/estratti_nlm/"

ESITI = {"usabile", "da riformulare", "non usabile", "non verificabile"}
CHIAVI_A = {"nodo", "id_fonte", "esito", "cosa_dice_davvero",
            "citazione_verbatim", "sezione", "note"}
CHIAVI_B = {"nodo", "id_fonte", "esito_nlm", "risposta_sintetica",
            "citazione_verbatim_nlm", "fonte_citata_corretta", "note"}

# V2 - front matter: citazioni tecnicamente presenti ma prive di contenuto
# argomentativo. Ringraziamenti, copyright, recapiti, intestazioni editoriali.
FRONT_MATTER = re.compile(
    r"\b(we (?:thank|are grateful|acknowledge)|all rights reserved|"
    r"correspondence (?:to|should)|the views expressed|"
    r"©|copyright|working paper (?:no|series)|"
    r"any (?:errors|opinions) (?:are|expressed)|"
    r"provided (?:valuable |generous )?funding|"
    r"electronic copy available at|this paper was prepared for)\b", re.I)

# colonne del foglio Estratti
C_ESITO, C_DICE, C_QUOTE, C_SEZ, C_NLM, C_NOTE = 8, 9, 10, 11, 12, 14


def norm(s):
    """Normalizza per il confronto: spazi collassati, virgolette uniformate."""
    s = (s or "")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def _cerca(quote, percorso):
    """Cerca la citazione in UNA resa del PDF. Ritorna (trovata, motivo|None)."""
    if not os.path.exists(percorso):
        return False, None
    testo = norm(open(percorso, encoding="utf-8", errors="replace").read())
    q = norm(quote)
    if q in testo:
        return True, "match esatto"
    # tolleranza: la sillabazione a fine riga puo' spezzare le parole
    if q.replace("- ", "") in testo.replace("- ", ""):
        return True, "match dopo rimozione sillabazione"
    return False, None


def quote_presente(quote, fid):
    """La citazione verbatim si ritrova nel PDF sorgente?

    Controlla entrambe le rese del documento (default e -raw): sono lo stesso
    PDF letto con due ordini di lettura diversi, e su documenti a due colonne
    una frase contigua puo' esistere in una sola delle due. Trovarla in una
    basta; non trovarla in nessuna delle due e' il caso che conta davvero.
    Ritorna (trovata, motivo).
    """
    q = norm(quote)
    if len(q) < 25:
        return False, "citazione troppo breve per essere verificabile (<25 car.)"

    principale = MD + fid + ".txt"
    alternativa = MD_RAW + fid + ".txt"
    if not os.path.exists(principale) and not os.path.exists(alternativa):
        return False, "testo sorgente assente"

    ok, motivo = _cerca(quote, principale)
    if ok:
        return True, motivo
    ok, motivo = _cerca(quote, alternativa)
    if ok:
        return True, motivo + " nella resa -raw"
    return False, "non ritrovata in nessuna delle due rese del PDF"


def valida_a(d):
    """Ritorna (ok, errori[])."""
    e = []
    if set(d) != CHIAVI_A:
        mancanti = CHIAVI_A - set(d); extra = set(d) - CHIAVI_A
        if mancanti: e.append(f"chiavi mancanti: {sorted(mancanti)}")
        if extra:    e.append(f"chiavi estranee: {sorted(extra)}")
        if mancanti: return False, e
    if d.get("esito") not in ESITI:
        e.append(f"esito non ammesso: {d.get('esito')!r}")
        return False, e
    esito = d["esito"]
    quote = d.get("citazione_verbatim") or ""

    # REGOLA 1 - nessun 'usabile' senza citazione ritrovabile
    if esito in ("usabile", "da riformulare"):
        if not quote.strip():
            e.append(f"'{esito}' senza citazione verbatim")
        else:
            ok, perche = quote_presente(quote, d["id_fonte"])
            if not ok:
                e.append(f"citazione verbatim {perche}")
    # REGOLA 9 - se dichiara una citazione, va verificata SEMPRE, anche su
    # 'non usabile' (contraddizione) e 'non verificabile': una citazione
    # inventata a sostegno di un giudizio negativo e' comunque inventata.
    elif quote.strip():
        ok, perche = quote_presente(quote, d["id_fonte"])
        if not ok:
            e.append(f"citazione verbatim su '{esito}' {perche}")
    dice = (d.get("cosa_dice_davvero") or "").strip()
    if not dice:
        e.append("cosa_dice_davvero vuoto")

    # V2 - la citazione non puo' venire dal front matter
    if quote.strip() and FRONT_MATTER.search(quote):
        e.append("citazione presa dal front matter (ringraziamenti, copyright, "
                 "recapiti): non e' contenuto argomentativo della fonte")

    # V1 - claim gia' marcato ATTRIBUZIONE INCERTA a monte
    tf = TASK + f"{d['nodo']}__{d['id_fonte']}.json"
    if os.path.exists(tf):
        try:
            claim = (json.load(open(tf, encoding="utf-8")).get("claim") or "")
        except Exception:
            claim = ""
        if claim.strip().startswith("ATTRIBUZIONE INCERTA"):
            if esito == "usabile":
                e.append("claim marcato ATTRIBUZIONE INCERTA: 'usabile' non ammesso "
                         "(regola 7 del prompt)")
            if "ATTRIBUZIONE INCERTA" not in (d.get("note") or ""):
                e.append("claim marcato ATTRIBUZIONE INCERTA: le note devono "
                         "affrontarlo esplicitamente")

    # V4 - 'non verificabile' non puo' essere una scappatoia silenziosa
    if esito == "non verificabile" and len(dice) < 200:
        e.append("'non verificabile' con motivazione troppo scarna (<200 car.): "
                 "va dichiarato cosa e' stato letto e cercato")
    return (len(e) == 0), e


def valida_b(d):
    e = []
    mancanti = CHIAVI_B - set(d)
    if mancanti:
        return False, [f"chiavi mancanti: {sorted(mancanti)}"]
    if d.get("esito_nlm") not in ESITI:
        return False, [f"esito_nlm non ammesso: {d.get('esito_nlm')!r}"]
    if d.get("fonte_citata_corretta") is False and d["esito_nlm"] != "non verificabile":
        e.append("citazione da fonte sbagliata ma esito diverso da 'non verificabile'")
    # Incrocio della citazione di NotebookLM col testo locale. Non e' un
    # rifiuto: il notebook puo' ospitare un'edizione diversa dello stesso
    # lavoro. Ma se la citazione non si ritrova, l'esito viene declassato a
    # 'non verificabile', perche' senza riscontro non e' un secondo lettore
    # indipendente: e' un'affermazione non controllabile.
    q = (d.get("citazione_verbatim_nlm") or "").strip()
    if q and d["esito_nlm"] in ("usabile", "da riformulare"):
        ok, perche = quote_presente(q, d["id_fonte"])
        if not ok:
            d["esito_nlm"] = "non verificabile"
            d["note"] = (d.get("note") or "") + \
                f" [declassato dallo scrittore: citazione NotebookLM {perche}]"
    return (len(e) == 0), e


def leggi(cartella, valida):
    buoni, scarti = {}, []
    if not os.path.isdir(cartella):
        return buoni, scarti
    for fn in sorted(os.listdir(cartella)):
        if not fn.endswith(".json"):
            continue
        try:
            d = json.load(open(cartella + fn, encoding="utf-8"))
        except Exception as ex:
            scarti.append((fn, [f"JSON illeggibile: {ex}"])); continue
        ok, err = valida(d)
        if ok:
            buoni[(str(d["nodo"]), d["id_fonte"])] = d
        else:
            scarti.append((fn, err))
    return buoni, scarti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args()

    A, scartiA = leggi(IN_A, valida_a)
    B, scartiB = leggi(IN_B, valida_b)

    print(f"Lettore A : {len(A)} validi, {len(scartiA)} scartati")
    print(f"NotebookLM: {len(B)} validi, {len(scartiB)} scartati")
    for nome, err in scartiA + scartiB:
        print(f"  SCARTO {nome}")
        for x in err:
            print(f"         - {x}")
    if not A and not B:
        print("\nNiente da scrivere.")
        return

    import openpyxl
    if a.commit:
        shutil.copy2(XLSX, BASE + f"iTOC master.backup_{datetime.now():%Y%m%d_%H%M%S}.xlsx")
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["Estratti"]

    scritte = 0
    for r in range(2, ws.max_row + 1):
        k = (str(ws.cell(r, 1).value), ws.cell(r, 2).value)
        if k in A:
            d = A[k]
            if a.commit:
                ws.cell(r, C_ESITO).value = d["esito"]
                ws.cell(r, C_DICE).value  = d["cosa_dice_davvero"]
                ws.cell(r, C_QUOTE).value = d["citazione_verbatim"]
                ws.cell(r, C_SEZ).value   = d["sezione"]
                ws.cell(r, C_NOTE).value  = d["note"]
            else:
                print(f"  [dry] {k[0]:<8} {k[1]:<22} -> {d['esito']}")
            scritte += 1
        if k in B and a.commit:
            ws.cell(r, C_NLM).value = B[k]["esito_nlm"]

    if a.commit:
        wb.save(XLSX)
        print(f"\nScritte {scritte} righe nel foglio Estratti. Backup creato.")
    else:
        print(f"\n[dry-run] Scriverei {scritte} righe. Usa --commit per confermare.")


if __name__ == "__main__":
    main()
