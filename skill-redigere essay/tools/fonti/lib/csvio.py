"""Lettura/scrittura di `input/fonti.csv`, l'elenco delle fonti.

Sostituisce `excelio.py` della tesi, che lavorava sul foglio `Fonti` dell'Excel.
Le regole sono le stesse:
 - lo script scrive SOLO nelle colonne di acquisizione (stato ... peer) e
   appende in `note`; non tocca mai id, autori, anno, query, contesto;
 - l'abbinamento riga<->fonte si fa sempre per `id`, mai per numero di riga;
 - backup obbligatorio prima di qualsiasi scrittura;
 - salvataggio dopo ogni fonte, cosi' un crash a meta' run non perde nulla.
"""
from __future__ import annotations

import csv
import datetime as dt
import logging
import shutil
from pathlib import Path

log = logging.getLogger("fonti.csvio")

COLONNE = [
    "id", "autori", "anno", "query", "contesto",          # le scrive l'autore
    "stato", "titolo", "tipo", "sede", "doi", "url",       # le scrive recupera.py
    "open_access", "pdf_locale", "peer",
    "note",                                                # si appende soltanto
]
SCRIVIBILI = ["stato", "titolo", "tipo", "sede", "doi", "url",
              "open_access", "pdf_locale", "peer"]

STATI = {"da_cercare", "trovata", "scaricata", "non_trovata", "paywall",
         "ambigua", "gia_presente", "abbandonata"}
SI_NO = {"sì", "no"}
PEER = {"sì", "no", "n.d."}


class FontiCSV:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.righe: list[dict] = []
        self._idx: dict[str, int] = {}

    def backup(self) -> Path:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = self.path.with_name(f"{self.path.stem}.backup_{ts}{self.path.suffix}")
        shutil.copy2(self.path, dest)
        log.info("backup creato: %s", dest)
        return dest

    def open(self) -> None:
        with open(self.path, newline="", encoding="utf-8-sig") as f:
            r = csv.DictReader(f)
            mancanti = [c for c in ("id", "autori", "anno") if c not in (r.fieldnames or [])]
            if mancanti:
                raise ValueError(f"{self.path.name}: mancano le colonne {mancanti}. "
                                 f"Intestazione attesa: {','.join(COLONNE)}")
            for riga in r:
                if not (riga.get("id") or "").strip():
                    continue
                self.righe.append({c: (riga.get(c) or "").strip() for c in COLONNE})
        self._idx = {r["id"]: i for i, r in enumerate(self.righe)}
        log.info("indicizzate %d fonti in %s", len(self.righe), self.path.name)

    def all_ids(self) -> list[str]:
        return [r["id"] for r in self.righe]

    def get(self, fonte_id: str) -> dict | None:
        i = self._idx.get(fonte_id)
        return None if i is None else self.righe[i]

    def stato(self, fonte_id: str) -> str:
        r = self.get(fonte_id)
        return (r or {}).get("stato") or "da_cercare"

    def write_fields(self, fonte_id: str, values: dict) -> None:
        r = self.get(fonte_id)
        if r is None:
            raise KeyError(f"id '{fonte_id}' non trovato in {self.path.name}")
        for col, val in values.items():
            if col not in SCRIVIBILI:
                raise ValueError(f"colonna '{col}' non scrivibile da questo script ({SCRIVIBILI})")
            if col == "stato" and val not in STATI:
                raise ValueError(f"stato '{val}' non ammesso")
            if col == "open_access" and val and val not in SI_NO:
                raise ValueError(f"open_access '{val}' non ammesso")
            if col == "peer" and val and val not in PEER:
                raise ValueError(f"peer '{val}' non ammesso")
            r[col] = val or ""

    def append_note(self, fonte_id: str, riga: str) -> None:
        r = self.get(fonte_id)
        r["note"] = f"{r['note']} | {riga}".strip(" |") if r["note"] else riga

    def save(self) -> None:
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLONNE)
            w.writeheader()
            w.writerows(self.righe)
