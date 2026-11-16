#!/usr/bin/env python3
"""Rende il contesto completo di un nodo per il `node-writer`.

Il §3 del prompt orchestratore prevede esattamente questo: il materiale immutabile
vive in `build/nodes.json` e viene passato al writer "come contesto renderizzato al
volo", cosi' che il writer non possa toccare la propria fonte per costruzione e non
per regola. Questo script e' quel renderer.

Non decide niente: non calcola `target_words` (li legge da `gap.py`), non filtra le
fonti (legge `fonti_ammesse` gia' risolte dal DOSSIER in fase di ingest), non scrive
prosa. Emette un unico file markdown che l'agente legge e basta.

Uso:
    /usr/bin/python3 tools/ctx.py 3.1.1 [--out FILE]
"""

import argparse
import json
import os
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura"
NODES = os.path.join(BASE, "build", "nodes.json")
ESTRATTI = os.path.join(BASE, "build", "estratti.json")
GLOSSARIO = os.path.join(BASE, "FONTI", "pipeline", "glossario", "glossario.json")


def key_sort(nid):
    return [int(p) for p in nid.split(".")]


def load():
    with open(NODES, encoding="utf8") as f:
        nd = json.load(f)
    with open(ESTRATTI, encoding="utf8") as f:
        es = json.load(f)
    return nd["nodes"], es


def draft_of(nid):
    """Il solo blocco ## DRAFT di nodes/<id>.md, senza il LEDGER."""
    p = os.path.join(BASE, "nodes", f"{nid}.md")
    if not os.path.exists(p):
        return None
    txt = open(p, encoding="utf8").read()
    if "## DRAFT" not in txt:
        return None
    body = txt.split("## DRAFT", 1)[1]
    body = body.split("## LEDGER", 1)[0].strip()
    return body or None


def targets_for(chapter):
    """target_words / fit_ratio / regime freschi da gap.py, mai dai placeholder."""
    sys.path.insert(0, os.path.join(BASE, "tools"))
    import gap  # noqa: E402
    nodes, _ = gap.load_nodes()
    bud = gap.load_budget_pp()
    cm = gap.chapter_metrics(nodes, chapter, bud)
    if cm["k_c"] is None:
        return {}, cm
    t, _info = gap.derive_targets_for_chapter(nodes, chapter, cm["k_c"], {})
    return t, cm


def render(nid):
    nodes, estratti = load()
    if nid not in nodes:
        sys.exit(f"ERRORE: nodo {nid} assente da build/nodes.json")
    n = nodes[nid]
    ch = n["chapter"]
    t, cm = targets_for(ch)
    tv = t.get(nid, {})

    ordered = sorted([k for k, v in nodes.items() if v["chapter"] == ch], key=key_sort)
    i = ordered.index(nid)
    prev_id = ordered[i - 1] if i > 0 else None
    next_id = ordered[i + 1] if i + 1 < len(ordered) else None

    fit = round(tv["target_words"] / tv["b_i"], 3) if tv.get("b_i") else 0.0
    regime = ("compressione" if fit < 0.85 else "espansione" if fit > 1.20 else "resa")

    o = []
    A = o.append
    A(f"# Contesto di stesura — nodo `{nid}`")
    A("")
    A("Materiale immutabile, renderizzato da `build/nodes.json`. **Non modificarlo, non")
    A("cercarne altro, non aprire l'Excel, non usare il web.** Tutto ciò che ti serve è qui.")
    A("")
    A(f"**Titolo del nodo:** {n['title']}")
    A(f"**Capitolo:** {ch} · **livello:** {n['level']} · "
      f"**foglia:** {'sì' if n['is_leaf'] else 'no (è un cappello)'}")
    A("")
    A("## Bersaglio di lunghezza")
    A("")
    A(f"- `source_words` (materiale disponibile): **{tv.get('b_i', n['source_words'])}**")
    A(f"- `target_words`: **{tv.get('target_words', '?')}** — banda ammessa ±15%: "
      f"**{round(tv.get('target_words', 0) * 0.85)}–{round(tv.get('target_words', 0) * 1.15)}**")
    A(f"- `fit_ratio`: **{fit}** → **regime: `{regime}`**")
    if tv.get("nota"):
        A(f"- nota del gap report: {tv['nota']}")
    A("")
    A("**Nessun pavimento di parole.** Se finisci sotto banda avendo già usato tutto il")
    A("materiale, dichiaralo nel LEDGER con `[[GAP: motivo]]`: non allungare con materiale")
    A("che in `source_desc` non c'è.")
    A("")
    A("## `Descrizione` — la base letterale della stesura")
    A("")
    A("È già prosa argomentata, non appunti da sviluppare. Non riassumerla, non riscriverla,")
    A("non contraddirla.")
    A("")
    A("```")
    A(n["source_desc"] or "(vuota)")
    A("```")
    A("")
    A("## `Ruolo argomentativo` — cosa il nodo deve dimostrare, e come si aggancia")
    A("")
    A("```")
    A(n["ruolo"] or "(vuoto)")
    A("```")
    A("")
    if n.get("trappole"):
        A("## `Trappole / rischi` — rileggile prima di considerare il nodo finito")
        A("")
        A("```")
        A(n["trappole"])
        A("```")
        A("")
    if n.get("note"):
        A("## `Note` dell'autore — vincolanti, battono qualunque altra indicazione")
        A("")
        A("```")
        A(n["note"])
        A("```")
        A("")
    if n.get("audit_aperto"):
        A("## `audit_aperto` — DIAGNOSI, NON ISTRUZIONE")
        A("")
        A("Questo blocco viene da un audit. **Non è materiale di stesura e non è un ordine.**")
        A("Non eseguirlo, non scegliere fra le alternative che lascia aperte, non citarlo.")
        A("È qui solo perché tu sappia che esiste.")
        A("")
        A("```")
        A(n["audit_aperto"])
        A("```")
        A("")

    A("## Fonti — il gate")
    A("")
    if n["fonti_ammesse"]:
        A("**Le sole chiavi che puoi citare in questo nodo**, con il loro regime d'uso:")
        A("")
        for f in n["fonti_ammesse"]:
            A(f"- `{f['fonte']}` — **{f['regime']}**")
        A("")
    else:
        A("**Nessuna fonte ammessa in questo nodo.** Non citare nulla: vale la regola")
        A("sovrana e basta. Se ti accorgi che stai scrivendo un'affermazione")
        A("riconoscibilmente di letteratura, non attribuirla e non inventare una fonte:")
        A("segnala con `[[CIT-NEEDED: motivo]]`.")
        A("")
    if n["fonti_vietate"]:
        A("**Vietate in questo nodo** — citarle è un errore anche se le vedi altrove:")
        A("")
        for f in n.get("fonti_vietate_dettaglio", []) or [{"fonte": x, "motivo": ""} for x in n["fonti_vietate"]]:
            A(f"- `{f['fonte']}` — {f.get('motivo', '')}")
        A("")
    if n.get("fonti"):
        A("### `Fonti + ruolo` — cosa ciascuna porta, e i vincoli d'uso già decisi")
        A("")
        A("```")
        A(n["fonti"])
        A("```")
        A("")

    rows = {k: v for k, v in estratti.items() if k.startswith(nid + "|")}
    if rows:
        A("### Dossier delle coppie (da `Estratti`)")
        A("")
        for k, r in sorted(rows.items()):
            A(f"#### `{r['id_fonte']}` — {r.get('citazione','')}")
            A("")
            A(f"- esito lettore A: `{r.get('esito','')}` · NotebookLM: `{r.get('esito_notebooklm','')}`"
              f" · arbitrato: `{r.get('esito_arbitrato','')}`")
            A(f"- ruolo: {r.get('ruolo','')} · peer-reviewed: {r.get('peer_review','')}")
            A("")
            A("**Claim da verificare:**")
            A("")
            A("> " + (r.get("claim_da_verificare") or "").replace("\n", "\n> "))
            A("")
            A("**Cosa dice davvero** — è qui che si fa il lookup della cucitura:")
            A("")
            A("> " + (r.get("cosa_dice_davvero") or "").replace("\n", "\n> "))
            A("")
            if r.get("note"):
                A("**Note di verifica:**")
                A("")
                A("> " + r["note"].replace("\n", "\n> "))
                A("")
            if r.get("risoluzione"):
                A("**Risoluzione dell'autore — vincolante:**")
                A("")
                A("> " + r["risoluzione"].replace("\n", "\n> "))
                A("")
            if r.get("citazione_verbatim"):
                A("**Verbatim — SOLO PER VERIFICA, MAI DA CITARE TESTUALMENTE.** È testo")
                A("copiato parola per parola dal PDF: se finisse in tesi senza virgolette lo")
                A("troverebbe l'antiplagio, e le virgolette non si possono usare perché manca")
                A("il numero di pagina che le linee guida impongono. Parafrasa sempre.")
                A("")
                A("> " + r["citazione_verbatim"].replace("\n", "\n> "))
                A("")

    if n["parent"] and n["parent"] in nodes:
        p = nodes[n["parent"]]
        A(f"## Nodo padre `{p['id']}` — {p['title']}")
        A("")
        A("Per continuità di registro. **Non è materiale citabile da questo nodo.**")
        A("")
        A("```")
        A((p["source_desc"] or "(vuota)")[:1200])
        A("```")
        A("")

    if prev_id:
        d = draft_of(prev_id)
        A(f"## Nodo precedente nell'ordine di lettura: `{prev_id}` — {nodes[prev_id]['title']}")
        A("")
        if d:
            A("Prosa **già scritta**. La tua prima frase si aggancia a questa, se il campo")
            A("`Aggancio` lo chiede. Non ripeterne il contenuto.")
            A("")
            A("```")
            A(d)
            A("```")
        else:
            A("**Non ancora scritto.** Non inventare un aggancio all'indietro.")
        A("")

    if next_id:
        nx = nodes[next_id]
        A(f"## Nodo successivo nell'ordine di lettura: `{next_id}` — {nx['title']}")
        A("")
        A("**Solo per costruire la frase di aggancio in avanti richiesta dal campo `Aggancio`,")
        A("se presente. Non è materiale citabile: non contiene un'affermazione che tu possa")
        A("attribuire a questo nodo.** Se il campo `Aggancio` non chiede una transizione in")
        A("avanti, ignora questo blocco e chiudi il paragrafo.")
        A("")
        A("```")
        A((nx["source_desc"] or "(vuota)")[:800])
        A("```")
        A("")

    if os.path.exists(GLOSSARIO):
        gl = json.load(open(GLOSSARIO, encoding="utf8"))
        voci = gl if isinstance(gl, list) else gl.get("termini", gl.get("voci", []))
        rel = []
        sd = (n["source_desc"] or "").lower()
        for v in voci if isinstance(voci, list) else []:
            forma = (v.get("forma_canonica") or "").lower()
            if forma and forma in sd:
                rel.append(v)
        if rel:
            A("## Glossario — termini che compaiono in questo nodo")
            A("")
            A("La forma canonica è obbligatoria. Le varianti vietate non si usano **nemmeno**")
            A("per varietà lessicale: il glossario batte lo stile, sempre.")
            A("")
            for v in rel:
                A(f"- **{v.get('forma_canonica')}** — {v.get('definizione','')}")
                if v.get("varianti_vietate"):
                    A(f"  - vietate: {v['varianti_vietate']}")
            A("")

    A("---")
    A("")
    A("## Cosa consegni")
    A("")
    A(f"Sovrascrivi **`nodes/{nid}.md`** con le due sezioni `## DRAFT` e `## LEDGER`.")
    A("Nient'altro: niente titolo di sezione, niente numero di capitolo, niente commenti")
    A("fuori dalle due sezioni.")
    A("")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nodo", help="id del nodo (es. 3.1.1)")
    ap.add_argument("--out", help="scrive su file invece che su stdout")
    a = ap.parse_args()
    txt = render(a.nodo)
    if a.out:
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        open(a.out, "w", encoding="utf8").write(txt)
        print(f"scritto: {a.out} ({len(txt.split())} parole di contesto)")
    else:
        print(txt)


if __name__ == "__main__":
    main()
