#!/usr/bin/env python3
"""assemble.py — dal template Word dell'autore al documento finale.

Parte SEMPRE da un template (`template_docx` in progetto.json, di default
`input/template.docx`): stili, margini, font, frontespizio, intestazioni, piè di
pagina sono dell'autore e non si ricostruiscono. Se il template manca, lo script
si rifiuta (exit 3): l'orchestratore deve chiederlo alla persona, non inventarne uno.

Cosa fa, nell'ordine:
  1. controlla le precondizioni (template, lock file di Word, sezioni senza DRAFT,
     buchi [[GAP:]]/[[CIT-NEEDED:]] ancora aperti, chiavi assenti dal .bib);
  2. risolve i token [[CIT-N:k]] -> «Autore (Anno)» e [[CIT-P:k]] -> «(Autore, Anno)»
     in APA 7, deterministicamente, da `fonti/fonti.bib` (tools/bib.py);
  3. copia il template in `out/`, sostituisce `{{TITOLO}}` e `{{AUTORE}}` se ci sono,
     inserisce titoli (Heading 1-3) e prosa (stile corpo) al posto di `{{CORPO}}`,
     o in coda al documento se il segnaposto non c'e';
  4. aggiunge la reference list (solo le chiavi citate, alfabetica), con il corsivo;
  5. se il template ha un indice (campo TOC), chiede a Word di aggiornarlo all'apertura.

Numeri nei titoli: se lo stile Heading 1 del template ha la numerazione automatica,
il numero NON si scrive nel testo del titolo (diventerebbe «1. 1 Titolo»). Se non
ce l'ha e l'id della sezione e' numerico, lo script lo antepone.

Il LEDGER non entra mai nel Word. Nessuna formattazione diretta oltre al corsivo
della bibliografia.

Uso:
    python3 tools/word/assemble.py --dry-run     # solo precondizioni
    python3 tools/word/assemble.py
    python3 tools/word/assemble.py --bozza       # assembla anche con buchi aperti (lasciati in evidenza)
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402
from bib import Bibliografia  # noqa: E402

try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("ERRORE: manca python-docx. Usa un python3 che lo abbia (pip install python-docx).")


def template_path(cfg) -> Path:
    return comune.ROOT / cfg["template_docx"]


def da_assemblare(sez):
    return [k for k, v in sez.items() if not v["escludi"]]


def precondizioni(cfg, sez, bib, bozza):
    motivi, avvisi = [], []
    t = template_path(cfg)
    if not t.exists():
        return ["TEMPLATE MANCANTE"], []
    if comune.lock_files(t.parent) or comune.lock_files(comune.OUT):
        motivi.append("c'e' un file ~$… : Word ha aperto il template o l'output. Chiudi Word.")
    for sid in da_assemblare(sez):
        s, d = sez[sid], comune.draft_di(sid)
        if s["foglia"] and not d:
            motivi.append(f"{sid}: sezione foglia senza DRAFT")
        for m in comune.TOKEN_CIT.finditer(d):
            if m.group(2) not in bib.voci:
                motivi.append(f"{sid}: {m.group(0)} — chiave assente da fonti/fonti.bib")
            elif bib.mancanti(m.group(2)):
                avvisi.append(f"{m.group(2)}: voce .bib incompleta ({', '.join(bib.mancanti(m.group(2)))})")
        buchi = comune.TOKEN_BUCO.findall(d)
        if buchi and not bozza:
            motivi.append(f"{sid}: {len(buchi)} buchi aperti ([[GAP:]]/[[CIT-NEEDED:]]) — vanno chiusi "
                          "con l'autore, oppure usa --bozza")
    return motivi, sorted(set(avvisi))


def risolvi(testo, bib):
    citate = set()

    def sub(m):
        citate.add(m.group(2))
        return bib.narrativa(m.group(2)) if m.group(1) == "N" else bib.parentetica(m.group(2))
    return comune.TOKEN_CIT.sub(sub, testo), citate


def heading_numerati(doc) -> bool:
    try:
        st = doc.styles["Heading 1"]
    except KeyError:
        return False
    return st.element.find(".//" + qn("w:numPr")) is not None


def para_con_corsivo(par, testo):
    """`*…*` diventa un run corsivo; tutto il resto resta testo dello stile."""
    for i, pezzo in enumerate(re.split(r"\*([^*]+)\*", testo)):
        if pezzo:
            r = par.add_run(pezzo)
            if i % 2:
                r.italic = True


def trova_par(doc, segnaposto):
    for p in doc.paragraphs:
        if segnaposto in p.text:
            return p
    return None


def sostituisci_testo(doc, segnaposto, valore):
    p = trova_par(doc, segnaposto)
    if p is None:
        return False
    testo = p.text.replace(segnaposto, valore)
    for r in p.runs[1:]:
        r._r.getparent().remove(r._r)
    if p.runs:
        p.runs[0].text = testo
    else:
        p.add_run(testo)
    return True


class Inseritore:
    """Inserisce paragrafi prima di un'ancora (il segnaposto {{CORPO}}) o in coda."""

    def __init__(self, doc, ancora):
        self.doc, self.ancora = doc, ancora

    def add(self, testo, stile, corsivo=False):
        if self.ancora is not None:
            p = self.ancora.insert_paragraph_before("", style=stile)
        else:
            p = self.doc.add_paragraph("", style=stile)
        if corsivo:
            para_con_corsivo(p, testo)
        else:
            p.add_run(testo)
        return p


def aggiorna_toc(doc) -> bool:
    if "TOC \\" not in doc.element.body.xml and "TOC \\o" not in doc.element.body.xml:
        return False
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is None:
        u = OxmlElement("w:updateFields")
        u.set(qn("w:val"), "true")
        settings.append(u)
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--bozza", action="store_true")
    a = ap.parse_args(argv)

    cfg = comune.config()
    sez = comune.sezioni()
    bib = Bibliografia(lingua=cfg["lingua"])
    motivi, avvisi = precondizioni(cfg, sez, bib, a.bozza)
    if motivi == ["TEMPLATE MANCANTE"]:
        print(f"ASSEMBLE — RIFIUTATO\nManca il template Word: {cfg['template_docx']}\n"
              "Chiedilo all'autore e mettilo li' (o cambia `template_docx` in progetto.json). "
              "Non se ne genera uno: stili, margini e frontespizio sono suoi.")
        return 3
    for x in avvisi:
        print(f"Avviso: {x}")
    if motivi:
        print("ASSEMBLE — RIFIUTATO")
        for m in motivi:
            print(f"Motivo: {m}")
        return 2
    if a.dry_run:
        print("ASSEMBLE — dry run: le precondizioni passano, niente scritto.")
        return 0

    out = comune.ROOT / cfg["output_docx"]
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template_path(cfg), out)
    doc = Document(str(out))

    titolo = cfg.get("titolo") or comune.carica_json(comune.SEZIONI_JSON, "leggi_scaletta.py").get("titolo", "")
    sostituisci_testo(doc, "{{TITOLO}}", titolo)
    sostituisci_testo(doc, "{{AUTORE}}", cfg.get("autore", ""))
    ancora = trova_par(doc, "{{CORPO}}")
    ins = Inseritore(doc, ancora)
    numerati = heading_numerati(doc)

    citate, n_tit, n_par = set(), 0, 0
    for sid in da_assemblare(sez):
        s = sez[sid]
        testo_tit = s["titolo"]
        if not numerati and re.fullmatch(r"\d+(\.\d+)*", sid):
            testo_tit = f"{sid} {testo_tit}" if "." in sid else f"{sid}. {testo_tit}"
        ins.add(testo_tit, f"Heading {min(s['livello'], 3)}")
        n_tit += 1
        risolto, c = risolvi(comune.draft_di(sid), bib)
        citate |= c
        for blocco in comune.paragrafi(risolto):
            ins.add(blocco, cfg["stile_corpo"])
            n_par += 1

    if citate:
        ins.add(cfg["titolo_bibliografia"], "Heading 1")
        for k in bib.ordina(citate):
            ins.add(bib.voce_lista(k), cfg["stile_corpo"], corsivo=True)
    if ancora is not None:
        ancora._p.getparent().remove(ancora._p)
    toc = aggiorna_toc(doc)
    doc.save(str(out))
    Document(str(out))  # riapertura di controllo

    (comune.BUILD / "bibliografia.md").write_text(
        "\n".join(f"- {bib.voce_lista(k)}" for k in bib.ordina(citate)) + "\n", encoding="utf-8")
    print("ASSEMBLE")
    print(f"{comune.rel(out)} generato da {cfg['template_docx']}")
    print(f"Titoli: {n_tit} · paragrafi: {n_par} · voci bibliografiche: {len(citate)}")
    print(f"Numerazione automatica dei titoli nel template: {'si (numero non scritto)' if numerati else 'no (numero scritto)'}")
    print(f"Segnaposto {{{{CORPO}}}}: {'trovato' if ancora is not None else 'assente, corpo in coda'}")
    print(f"Indice da aggiornare all'apertura: {'si' if toc else 'nessun indice nel template'}")
    print("Ora: python3 tools/word/controlla_docx.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
