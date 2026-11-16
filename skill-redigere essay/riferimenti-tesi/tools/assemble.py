#!/usr/bin/env python3
"""assemble.py — da `LF3236167.docx` a `out/LF3236167.docx`.

Inserisce **solo struttura e testo gia' risolto**. Non tocca stili, font,
margini, `sectPr`, header e footer; non inserisce tabelle (e' `table-inserter`)
e non risolve citazioni (e' `bibliography-builder`, che gira prima).

Il contratto completo sta in `.claude/skills/tesi-assemble/SKILL.md`, passo 2.

Perche' si parte dal template e non da un documento vuoto: il front matter, le
tre sezioni coi rispettivi `sectPr`, la numerazione romana dell'indice e quella
araba del corpo, i `footerReference`, sono gia' a norma nel template e
l'autore li ha sistemati a mano. Ricostruirli sarebbe rifare un lavoro fatto.

Uso:
    /usr/bin/python3 tools/assemble.py
    /usr/bin/python3 tools/assemble.py --dry-run   # controlla e non scrive
"""

import argparse
import json
import os
import re
import shutil
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
TEMPLATE = BASE + "LF3236167.docx"
OUT_DIR = BASE + "out/"
# Il nome e' quello del template, non "tesi.docx": e' il file che l'autore
# consegna all'ateneo, e il nome fa parte della consegna.
# [DECISIONE AUTORE 2026-09-08] «voglio che nella cartella out mi metti questo
# file di word lf3236167.docx»
OUT = OUT_DIR + "LF3236167.docx"
NODES_JSON = BASE + "build/nodes.json"
NODES_DIR = BASE + "nodes/"
BIBLIO = BASE + "build/bibliography.md"
STRUTTURA = BASE + "decisions/struttura.json"

# I tre heading segnaposto vivi nel template. Se non si rimuovono PRIMA di
# inserire il corpo ereditano la numerazione dello stile e il primo Heading 1
# vero -- il Capitolo 1 -- diventa `2.`.
SEGNAPOSTO = [("Heading1", "Rq"), ("Heading2", "Ff"), ("Heading3", "")]

TOKEN_RESIDUO = re.compile(r"\[\[CIT-[NP]:")
TOKEN_AMMESSO_MA_BLOCCANTE = re.compile(r"\[\[(?:GAP|CIT-NEEDED):")



def struttura():
    """Le decisioni dell'autore sulla struttura che l'Excel congelato non esprime.

    Senza questo file `assemble.py` si comporterebbe come se `7.4.8` dovesse
    ancora essere scritto, e rifiuterebbe l'assemblaggio per sempre.
    """
    if not os.path.exists(STRUTTURA):
        return {"escludi": set(), "conclusione": None}
    d = json.load(open(STRUTTURA, encoding="utf-8"))
    return {"escludi": {v["nodo"] for v in d.get("escludi_dal_documento", [])},
            "conclusione": d.get("conclusione_finale")}


def chiave(nid):
    return [int(x) for x in nid.split(".")]


def draft_of(path):
    """Il solo blocco `## DRAFT`. Il `## LEDGER` non entra mai nel .docx."""
    if not os.path.exists(path):
        return ""
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"##\s*DRAFT\b[ \t]*\n(.*?)(?=\n?##\s*LEDGER|\Z)", txt, re.S)
    testo = m.group(1).strip() if m else ""
    return "" if testo.startswith("## LEDGER") else testo


def carica_nodi():
    d = json.load(open(NODES_JSON, encoding="utf-8"))["nodes"]
    return {k: v for k, v in d.items() if v.get("perimetro")}


def precondizioni(nodi):
    """Ritorna la lista dei motivi di rifiuto. Vuota = si puo' assemblare."""
    motivi = []

    if os.path.exists(BASE + "~$LF3236167.docx"):
        motivi.append("esiste un lock file ~$LF3236167.docx: Word ha il template aperto")

    esclusi = struttura()["escludi"]
    senza_draft = [n for n, v in sorted(nodi.items(), key=lambda kv: chiave(kv[0]))
                   if n not in esclusi
                   and v["source_words"] > 0 and not draft_of(f"{NODES_DIR}{n}.md")]
    if senza_draft:
        motivi.append("nodi con materiale ma senza DRAFT: " + ", ".join(senza_draft))

    residui, bloccanti = [], []
    for n in nodi:
        if n in esclusi:
            continue
        t = draft_of(f"{NODES_DIR}{n}.md")
        if TOKEN_RESIDUO.search(t):
            residui.append(n)
        if TOKEN_AMMESSO_MA_BLOCCANTE.search(t):
            bloccanti.append(n)
    if residui:
        motivi.append("token [[CIT-N:]]/[[CIT-P:]] non risolti in " + ", ".join(sorted(residui, key=chiave))
                      + " — non li risolve questo script: manca il passaggio di `bibliography-builder`")
    if bloccanti:
        motivi.append("token [[GAP:]]/[[CIT-NEEDED:]] ancora aperti in "
                      + ", ".join(sorted(bloccanti, key=chiave)) + " — vanno al GATE 3-bis")

    if not os.path.exists(BIBLIO):
        motivi.append("build/bibliography.md non esiste: lo produce `bibliography-builder`, non questo script")

    return motivi


# --------------------------------------------------------------------------
# costruzione del corpo
# --------------------------------------------------------------------------

def sopprimi_numerazione(par):
    """Toglie la numerazione automatica a livello di paragrafo.

    Serve sul nodo `0` e sui suoi discendenti: nell'Excel sono numerati `0.x`,
    ma in tesi quel capitolo non porta numero, e i rimandi ad esso vanno scritti
    in forma testuale (per questo i writer hanno l'istruzione di non usare `0.x`
    nei rimandi). E' l'unica formattazione diretta che questo script applica.
    """
    pPr = par._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl"); ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId"); numId.set(qn("w:val"), "0")
    numPr.append(ilvl); numPr.append(numId)
    pPr.append(numPr)


def rimuovi_segnaposto(doc):
    """Rimuove i tre heading segnaposto. Ritorna quanti ne ha tolti."""
    tolti = 0
    for par in list(doc.paragraphs):
        for stile, testo in SEGNAPOSTO:
            if par.style.style_id == stile and par.text.strip() == testo:
                par._p.getparent().remove(par._p)
                tolti += 1
                break
    return tolti


def svuota_cache_toc(doc):
    """Ricostruisce il campo TOC vuoto, invece di cancellarlo.

    Il campo, nel template, non sta nel primo paragrafo dell'`sdtContent`: il
    primo e' il titolo «Table of Contents», il **secondo** porta `begin` +
    `instrText` + `separate` insieme alla voce memorizzata, e il **terzo** porta
    `end`. Una prima versione di questa funzione teneva solo il primo paragrafo
    e cancellava gli altri: cosi' non svuotava la cache, **distruggeva il
    campo**, e il documento usciva con l'indice vuoto sotto il titolo. L'ha
    trovato `final-check`.

    Qui il titolo resta, il risultato memorizzato sparisce, e il campo viene
    riscritto pulito e marcato `dirty`, cosi' Word lo rigenera all'apertura.
    """
    def run(figlio):
        r = OxmlElement("w:r")
        r.append(figlio)
        return r

    rifatti = 0
    for sdt in doc.element.body.iter(qn("w:sdt")):
        content = sdt.find(qn("w:sdtContent"))
        if content is None:
            continue
        paragrafi = list(content.findall(qn("w:p")))
        if not paragrafi:
            continue
        # via tutto tranne il titolo
        for p in paragrafi[1:]:
            content.remove(p)

        campo = OxmlElement("w:p")
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        begin.set(qn("w:dirty"), "true")
        campo.append(run(begin))

        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = 'TOC \\o "1-3" \\h \\z \\u'
        campo.append(run(instr))

        sep = OxmlElement("w:fldChar")
        sep.set(qn("w:fldCharType"), "separate")
        campo.append(run(sep))

        # segnaposto: Word lo sostituisce con l'indice vero all'aggiornamento
        t = OxmlElement("w:t")
        t.text = "Aggiornare il campo per generare l'indice."
        campo.append(run(t))

        fine = OxmlElement("w:fldChar")
        fine.set(qn("w:fldCharType"), "end")
        campo.append(run(fine))

        content.append(campo)
        rifatti += 1
    return rifatti


def inserisci_corpo(doc, nodi):
    """Aggiunge titoli e prosa. `add_paragraph` inserisce prima del sectPr
    finale, che e' esattamente dove va il corpo."""
    esclusi = struttura()["escludi"]
    n_titoli = n_par = 0
    for nid in sorted(nodi, key=chiave):
        if nid in esclusi:
            continue
        v = nodi[nid]
        livello = min(v["level"], 3)
        h = doc.add_paragraph(v["title"], style=f"Heading {livello}")
        # mai il numero nel testo: Word lo antepone da se' via numId="3"
        if nid == "0" or nid.startswith("0."):
            sopprimi_numerazione(h)
        n_titoli += 1
        for blocco in [b.strip() for b in draft_of(f"{NODES_DIR}{nid}.md").split("\n\n") if b.strip()]:
            doc.add_paragraph(blocco, style="Normal")
            n_par += 1
    return n_titoli, n_par



def inserisci_conclusione(doc):
    """La conclusione finale: in coda al corpo, senza intestazione.

    Non e' un nodo dell'`iTOC` e non porta un titolo: l'autore l'ha voluta come
    chiusura nuda dopo l'ultima sezione del Cap. 7, preceduta da una riga vuota.
    """
    c = struttura()["conclusione"]
    if not c:
        return 0
    path = BASE + c["file"]
    if not os.path.exists(path):
        return 0
    doc.add_paragraph("", style="Normal")          # la riga vuota chiesta dall'autore
    n = 0
    for blocco in [b.strip() for b in draft_of(path).split("\n\n") if b.strip()]:
        doc.add_paragraph(blocco, style="Normal")
        n += 1
    return n


def inserisci_bibliografia(doc):
    """Copia `build/bibliography.md`, gia' formattata da `bibliography-builder`.

    Non la rigenera da `FONTI/tesi.bib`: alfabetizzazione, autori multipli e
    filtraggio alle sole chiavi citate sono lavoro di quell'agente.
    """
    righe = [r.rstrip() for r in open(BIBLIO, encoding="utf-8").read().splitlines()]
    voci = 0
    for r in righe:
        if not r.strip():
            continue
        if r.startswith("#"):
            doc.add_paragraph(r.lstrip("# ").strip(), style="Heading 1")
        else:
            doc.add_paragraph(r.strip(), style="Normal")
            voci += 1
    return voci


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="controlla le precondizioni e non scrive nulla")
    a = ap.parse_args(argv)

    nodi = carica_nodi()
    motivi = precondizioni(nodi)
    if motivi:
        print("ASSEMBLE — RIFIUTATO")
        for m in motivi:
            print(f"Motivo: {m}")
        print("out/LF3236167.docx non toccato.")
        return 2

    if a.dry_run:
        print("ASSEMBLE — dry run: tutte le precondizioni passano, niente scritto.")
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(TEMPLATE, OUT)
    doc = Document(OUT)

    tolti = rimuovi_segnaposto(doc)
    n_titoli, n_par = inserisci_corpo(doc, nodi)
    n_concl = inserisci_conclusione(doc)
    voci = inserisci_bibliografia(doc)
    toc = svuota_cache_toc(doc)
    doc.save(OUT)

    # riapertura di controllo: se il file non si riapre, non e' un documento
    Document(OUT)
    h1 = sum(1 for p in Document(OUT).paragraphs if p.style.style_id == "Heading1")

    print("ASSEMBLE")
    print(f"out/LF3236167.docx generato da LF3236167.docx (copia)")
    print(f"Nodi inseriti: {n_titoli} in perimetro · paragrafi di prosa: {n_par}")
    print(f"Heading segnaposto rimossi: {tolti} (attesi 3)")
    print(f"Conclusione finale: {n_concl} paragrafi, senza intestazione")
    print(f"Reference list inserita da build/bibliography.md: {voci} voci")
    print(f"Cache TOC svuotata: {'si' if toc else 'no'}")
    print(f"Heading 1 nel documento: {h1}")
    print("Matrici: non inserite qui — invoca `table-inserter` con build/matrici.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
