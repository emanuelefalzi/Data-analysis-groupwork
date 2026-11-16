#!/usr/bin/env python3
"""Lint sulla forma dei token di citazione (§4.7, §8).

Il token e' sdoppiato per un motivo grammaticale, non decorativo:

    [[CIT-N:akerlof1970]]  ->  Akerlof (1970) shows that ...   (narrativa)
    [[CIT-P:akerlof1970]]  ->  ... (Akerlof, 1970).            (parentetica)

La forma narrativa mette il nome dell'autore nella frase e puo' fare da
soggetto; la parentetica no. Scrivere "[[CIT-P:coff1999]] ties X to Y" produce
"(Coff, 1999) ties X to Y", che non e' inglese: serviva la narrativa.

E' un errore che nasce facilmente perche' chi scrive vede un token e non la
citazione che ne uscira', e che si scopre solo in assemblaggio, quando ormai
sta in 129 nodi. Qui costa una regex.

Uso:
    /usr/bin/python3 tools/lint_citazioni.py 3.2.3
    /usr/bin/python3 tools/lint_citazioni.py --capitolo 3
    /usr/bin/python3 tools/lint_citazioni.py --tutti
"""

import argparse
import glob
import json
import os
import re
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura"
NODES_DIR = os.path.join(BASE, "nodes")
NODES_JSON = os.path.join(BASE, "build", "nodes.json")

CIT_P = re.compile(r"\[\[CIT-P:([a-z0-9]+)\]\]")
CIT_N = re.compile(r"\[\[CIT-N:([a-z0-9]+)\]\]")
CIT_ANY = re.compile(r"\[\[CIT-[NP]:([a-z0-9]+)\]\]")

# Un token parentetico seguito da una parola minuscola che non sia una
# congiunzione o una preposizione sta quasi certamente facendo da soggetto.
NON_VERBI = {
    "and", "or", "but", "for", "nor", "so", "yet",
    "in", "on", "at", "by", "to", "of", "with", "from", "as", "than", "into",
    "the", "a", "an", "this", "that", "these", "those", "it", "its",
    "while", "whereas", "although", "though", "because", "since", "when",
    "where", "which", "who", "whose", "if", "unless", "however", "moreover",
}

# La forma narrativa mette il nome dell'autore DENTRO la frase, come
# costituente grammaticale: o e' soggetto ("Akerlof (1970) shows that ..."),
# oppure e' retto da una costruzione che governa un nome ("Building on Akerlof
# (1970), ...", "according to ...", "as shown by ..."). Se invece il token
# arriva in coda a una clausola gia' completa, la posizione e' quella della
# parentetica e il token narrativo produce una frase sgrammaticata:
# "... rather than verification itself Kirmani and Rao (2000)."
GOVERNA_NARRATIVA = re.compile(
    r"(?:building on|drawing on|following|according to|as shown by|as argued by|"
    r"as observed by|in the reading of|in the account of|for)\s*$",
    re.I,
)
NARRATIVA_TOKEN = re.compile(r"\[\[CIT-N:[a-z0-9]+\]\]")


def draft_of(path):
    """Il solo blocco `## DRAFT`, vuoto se il nodo non e' ancora scritto.

    La prima versione usava `##\\s*DRAFT\\s*\\n(.*?)(?:\\n##\\s*LEDGER|\\Z)`, che
    su uno scheletro vuoto restituiva la stringa `## LEDGER` invece del vuoto:
    `\\s*` mangiava anche la riga bianca, e il confine `\\n## LEDGER` non aveva
    piu' il suo `\\n`. Un nodo mai scritto risultava quindi scritto, e tutti i
    controlli che distinguono i due casi partivano su settanta nodi vuoti.
    """
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"##\s*DRAFT\b[ \t]*\n(.*?)(?=\n?##\s*LEDGER|\Z)", txt, re.S)
    testo = m.group(1).strip() if m else ""
    return "" if testo.startswith("## LEDGER") else testo


def ammesse_per_nodo(nid):
    if not os.path.exists(NODES_JSON):
        return None
    d = json.load(open(NODES_JSON, encoding="utf-8"))["nodes"]
    if nid not in d:
        return None
    return {f["fonte"] for f in d[nid].get("fonti_ammesse", [])}, \
           set(d[nid].get("fonti_vietate", []))


def lint_nodo(nid):
    path = os.path.join(NODES_DIR, f"{nid}.md")
    if not os.path.exists(path):
        return [("errore", f"nodes/{nid}.md non trovato")]
    testo = draft_of(path)
    out = []

    for m in CIT_P.finditer(testo):
        coda = testo[m.end():m.end() + 60].strip()
        parola = re.match(r"([A-Za-z']+)", coda)
        if parola and parola.group(1).lower() not in NON_VERBI and parola.group(1)[0].islower():
            out.append(("HIGH",
                        f"«[[CIT-P:{m.group(1)}]] {parola.group(1)} ...» — token parentetico "
                        f"usato come soggetto: renderebbe «({m.group(1).capitalize()}, anno) "
                        f"{parola.group(1)} ...», che non e' inglese. Qui serve [[CIT-N:]]."))

    # Il token narrativo rende NOME + ANNO insieme ("Akerlof (1970)"): scrivere
    # anche il nome accanto lo duplica. E' l'errore che nasce se si crede che il
    # token porti solo l'anno.
    for m in NARRATIVA_TOKEN.finditer(testo):
        prima_parole = re.findall(r"[A-Z][A-Za-z'\-]+", testo[max(0, m.start() - 60):m.start()])
        if prima_parole:
            chiave = m.group(0)
            cognomi = [w for w in prima_parole[-3:] if len(w) > 3]
            for c in cognomi:
                if c.lower()[:5] in chiave.lower():
                    out.append(("HIGH",
                                f"«{c} {m.group(0)}» — il nome dell'autore e' scritto "
                                f"accanto al token narrativo, che gia' lo contiene: "
                                f"renderebbe «{c} {c} (anno)». Togli il nome scritto a "
                                f"mano, oppure usa [[CIT-P:]] se volevi la parentetica."))
                    break

    for m in NARRATIVA_TOKEN.finditer(testo):
        prima = testo[:m.start()]
        # inizio di frase: il token e' in posizione di soggetto, corretto
        if re.search(r"(?:^|[.!?]\s+|\n\s*)$", prima):
            continue
        # retto da una costruzione narrativa: corretto
        ultima_clausola = re.split(r"[.!?;]\s+", prima)[-1]
        if GOVERNA_NARRATIVA.search(ultima_clausola.rstrip()):
            continue
        coda = testo[m.end():m.end() + 2]
        contesto = ultima_clausola.strip()[-55:]
        out.append(("MEDIO",
                    f"«...{contesto} {m.group(0)}{coda.strip()}» — token narrativo in "
                    f"posizione di parentetica: non e' ne' soggetto ne' retto da "
                    f"'building on'/'according to'/'as shown by'. Renderebbe una frase "
                    f"sgrammaticata. Qui serve [[CIT-P:]]."))

    # Una fonte che il DOSSIER ammette e che la colonna `Fonti + ruolo` dichiara
    # "mattone stretto" porta un mattone preciso dell'argomento: se il nodo non
    # la cita, quel mattone non c'e'. Non e' sempre un errore -- a volte la
    # Descrizione non ha una clausola che quella fonte regga -- ma va guardato,
    # perche' il caso tipico e' un writer che l'ha lasciata fuori per rientrare
    # nella banda di parole, e li' vale la precedenza `ruolo` batte `budget`.
    amm0 = ammesse_per_nodo(nid)
    # Dopo il passaggio di `bibliography-builder` i token non esistono piu' per
    # progetto: sono diventati «Akerlof (1970)» e «(Soh et al., 2000)». Da quel
    # momento questo controllo cerca una cosa che non c'e' e segnala come «fonte
    # non usata» ogni fonte citata in chiaro -- rumore su ~47 nodi, che rischia
    # di coprire un rilievo vero. Un nodo che non ha piu' NESSUN token ma ha
    # citazioni rese e' un nodo gia' risolto: la copertura andava verificata
    # prima, e infatti lo e' stata.
    risolto = not CIT_ANY.search(testo) and re.search(r"\(\d{4}\)|,\s\d{4}\)", testo)
    # solo sui nodi gia' scritti: uno scheletro vuoto non cita niente per
    # definizione, e segnalarlo sarebbe rumore su tutta la tesi non ancora fatta
    if amm0 is not None and testo.strip() and not risolto:
        ammesse0, _ = amm0
        usate = {m.group(1) for m in CIT_ANY.finditer(testo)}
        d = json.load(open(NODES_JSON, encoding="utf-8"))["nodes"].get(nid, {})
        fr = (d.get("fonti") or "")
        for k in sorted(ammesse0 - usate):
            stretto = "mattone stretto" in fr.lower()
            out.append(("MEDIO",
                        f"«{k}» e' ammessa in questo nodo ma non compare nel DRAFT"
                        + (" ed e' dichiarata mattone stretto in `Fonti + ruolo`" if stretto else "")
                        + ". Verifica che sia una scelta e non una fonte lasciata fuori "
                          "per rientrare in banda: su una coppia portante vale "
                          "`ruolo` batte `budget`."))

    amm = ammesse_per_nodo(nid)
    if amm is not None:
        ammesse, vietate = amm
        for m in CIT_ANY.finditer(testo):
            k = m.group(1)
            if k in vietate:
                out.append(("HIGH", f"«{k}» e' fra le fonti VIETATE di questo nodo: "
                                    f"citarla e' un errore anche se compare altrove."))
            elif k not in ammesse:
                out.append(("HIGH", f"«{k}» non e' fra le fonti ammesse di questo nodo "
                                    f"(gate del DOSSIER, col. H). Nessuna fonte nuova, mai."))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("nodo", nargs="?", help="id del nodo (es. 3.2.3)")
    g.add_argument("--capitolo", help="tutti i nodi di un capitolo")
    g.add_argument("--tutti", action="store_true", help="tutti i nodi scritti")
    a = ap.parse_args(argv)

    if a.nodo:
        nodi = [a.nodo]
    else:
        pat = f"{a.capitolo}*.md" if a.capitolo else "*.md"
        # `nodes/` non contiene piu' solo nodi numerati: `conclusione-finale.md`
        # e' la chiusura della tesi, che l'autore ha voluto senza intestazione e
        # quindi senza un id dell'iTOC. Ordinarla come un numero fa esplodere il
        # lint, quindi i nomi non numerici vanno in fondo invece che in errore.
        def ordine(nid):
            try:
                return (0, [int(x) for x in nid.split(".")], "")
            except ValueError:
                return (1, [], nid)

        nodi = sorted(
            (os.path.basename(p)[:-3] for p in glob.glob(os.path.join(NODES_DIR, pat))),
            key=ordine,
        )
        if a.capitolo:
            nodi = [n for n in nodi if n == a.capitolo or n.startswith(a.capitolo + ".")]

    tot = 0
    for nid in nodi:
        ril = lint_nodo(nid)
        ril = [r for r in ril if r[0] != "errore"]
        for sev, msg in ril:
            print(f"[{sev}] {nid}: {msg}")
        tot += sum(1 for s, _ in ril if s == "HIGH")
    if tot:
        print(f"\n{tot} rilievi HIGH.")
        print("BLOCCATO: la forma del token decide la resa in assemblaggio, non e' cosmetica.")
        sys.exit(2)
    print("OK: nessun rilievo sulla forma delle citazioni.")


if __name__ == "__main__":
    main()
