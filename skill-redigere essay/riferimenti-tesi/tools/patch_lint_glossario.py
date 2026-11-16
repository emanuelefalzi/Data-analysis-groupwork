#!/usr/bin/env python3
"""patch_lint_glossario.py — applica la patch a
`FONTI/pipeline/glossario/lint.py` descritta in PROMPT-orchestratore-tesi.md
§4.7. NON e' un lint: e' la patch stessa. Non modifica `lint.py` in questa
consegna — la applica solo quando l'autore lancia questo script.

Diagnosi (verificata leggendo il codice, non solo il prompt):

- La gravita' di `uso_prima_definizione` e' scritta a mano come stringa
  `"blocca"` in `_anticipazione_ammessa`... no: in realta' e' hardcoded
  dentro `lint()`, alla chiamata `Violazione("blocca", "uso_prima_definizione",
  ...)`. Il prompt orchestratore lo descrive come stato di fatto, non come
  bug da correggere qui: non esiste, ne' nel codice ne' in `glossario.json`,
  un campo che dovrebbe pilotare quella gravita'. **Questa patch non tocca
  quella riga**: resta "blocca", come confermato corretto dal prompt stesso
  ("il toggle che il resto del prompt suppone non esiste... trattalo come un
  lint piu' severo del previsto — non come rotto").
- Il bug vero e' in `_anticipazione_ammessa(nodo_uso, nodo_def)`: ignora del
  tutto `usabile_prima_del_nodo_definizione` e `anticipazioni_legittime`, due
  campi che `glossario.json` gia' porta su 48/48 voci (verificato). Effetto
  misurato: `python3 lint.py --autotest` blocca 3 citazioni-ancora legittime
  su 38 (verificato eseguendo l'autotest prima di questa patch) — tutte e
  tre risolte da questi due campi (verificato a mano, vedi sotto).

Patch (nella sola `_anticipazione_ammessa`, piu' il suo unico chiamante):
aggiunge due parametri opzionali (`can`, `voci`) e, se il termine anticipato
ha `usabile_prima_del_nodo_definizione: true`, o se il nodo d'uso e' nella
lista (o discendente di un nodo della lista) `anticipazioni_legittime`,
l'anticipazione e' ammessa. Verificato con una copia patchata di `lint.py`
in un file temporaneo: l'autotest passa da 3 blocchi a 0.

Uso:
    /usr/bin/python3 tools/patch_lint_glossario.py --dry-run   # mostra il diff, non scrive
    /usr/bin/python3 tools/patch_lint_glossario.py             # applica, con backup timestampato
    /usr/bin/python3 tools/patch_lint_glossario.py --help

Non tocca nessun altro file. Se il testo atteso non si trova piu' in
`lint.py` (perche' qualcuno l'ha gia' modificato), si ferma senza scrivere
niente ed esce con errore: non applica patch alla cieca.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import os
import sys

BASE = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
LINT_PY = BASE + "FONTI/pipeline/glossario/lint.py"

OLD_FUNC = '''def _anticipazione_ammessa(nodo_uso, nodo_def) -> bool:
    """Il blocco introduttivo (0.x) e il nodo padre possono anticipare un
    termine: e' prassi normale annunciare un concetto e definirlo dopo."""
    nu, nd = str(nodo_uso), str(nodo_def or "")
    if nu.startswith("0"):
        return True
    if nd.startswith(nu + ".") or nu == nd.split(".")[0]:
        return True
    return False'''

NEW_FUNC = '''def _anticipazione_ammessa(nodo_uso, nodo_def, can=None, voci=None) -> bool:
    """Il blocco introduttivo (0.x) e il nodo padre possono anticipare un
    termine: e' prassi normale annunciare un concetto e definirlo dopo.
    In piu' (patch AG-07): il glossario stesso puo' dichiarare l'anticipazione
    legittima, o su tutti i nodi (usabile_prima_del_nodo_definizione) o su un
    elenco esplicito di nodi/discendenti (anticipazioni_legittime)."""
    nu, nd = str(nodo_uso), str(nodo_def or "")
    if nu.startswith("0"):
        return True
    if nd.startswith(nu + ".") or nu == nd.split(".")[0]:
        return True
    v = next((x for x in (voci or [])
              if (x.get("forma_canonica") or "").lower() == (can or "").lower()), None)
    if v:
        if v.get("usabile_prima_del_nodo_definizione"):
            return True
        for a in v.get("anticipazioni_legittime", []) or []:
            a = str(a)
            if nu == a or nu.startswith(a + "."):
                return True
    return False'''

OLD_CALL = '''        elif tipo == "canonico":
            if _prima_di(nodo, nodo_def) and not _anticipazione_ammessa(nodo, nodo_def):'''

NEW_CALL = '''        elif tipo == "canonico":
            if _prima_di(nodo, nodo_def) and not _anticipazione_ammessa(nodo, nodo_def, can, voci):'''

REPLACEMENTS = [(OLD_FUNC, NEW_FUNC), (OLD_CALL, NEW_CALL)]


def build_patched_text(original_text):
    """Applica le sostituzioni in sequenza. Solleva ValueError col dettaglio
    se uno dei due blocchi attesi non si trova (lint.py e' cambiato)."""
    text = original_text
    for i, (old, new) in enumerate(REPLACEMENTS, 1):
        if old not in text:
            raise ValueError(
                f"blocco atteso #{i} non trovato in {LINT_PY}: lint.py e' cambiato "
                "rispetto alla diagnosi di questa patch. Non applico niente."
            )
        if text.count(old) > 1:
            raise ValueError(f"blocco atteso #{i} trovato piu' di una volta: ambiguo, non applico niente.")
        text = text.replace(old, new)
    return text


def make_diff(original_text, patched_text):
    return "".join(difflib.unified_diff(
        original_text.splitlines(keepends=True),
        patched_text.splitlines(keepends=True),
        fromfile="lint.py (originale)", tofile="lint.py (patchato)",
    ))


def run(dry_run, lint_path=LINT_PY):
    if not os.path.exists(lint_path):
        raise SystemExit(f"non trovato: {lint_path}")
    original = open(lint_path, encoding="utf-8").read()
    patched = build_patched_text(original)
    diff = make_diff(original, patched)

    if not diff:
        print("Nessuna differenza: lint.py sembra gia' patchato.")
        return

    print(diff)

    if dry_run:
        print("--dry-run: nessuna scrittura. Rilancia senza --dry-run per applicare.")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = lint_path + f".bak.{ts}"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original)
    with open(lint_path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"\nApplicata. Backup: {backup_path}")
    print("Verifica ora con:")
    print(f'  /usr/bin/python3 "{lint_path}" --autotest')
    print("Atteso: 0 blocchi su 38 citazioni-ancora (erano 3 prima della patch).")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Applica la patch AG-07 a FONTI/pipeline/glossario/lint.py: "
                     "_anticipazione_ammessa() legge finalmente "
                     "usabile_prima_del_nodo_definizione e anticipazioni_legittime.")
    ap.add_argument("--dry-run", action="store_true", help="mostra il diff, non scrive niente")
    ap.add_argument("--lint-path", default=LINT_PY, help="percorso di lint.py (default: quello del progetto)")
    args = ap.parse_args(argv)
    try:
        run(dry_run=args.dry_run, lint_path=args.lint_path)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
