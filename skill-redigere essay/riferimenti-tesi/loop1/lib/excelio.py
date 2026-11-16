"""Lettura/scrittura del foglio 'Fonti' dell'Excel di controllo.

Regole rispettate:
 - il codice scrive SOLO nelle colonne L, M, N, O, P, Q, R, S, T e appende
   in W; non tocca mai A-K, U, V.
 - l'abbinamento riga<->fonte si fa sempre cercando l'ID in colonna A, mai
   per numero di riga.
 - backup obbligatorio del file prima di qualsiasi scrittura.
 - una sola passata, un solo writer: il workbook viene aperto una volta e
   tenuto aperto per tutta la durata del run; in modalita' --commit si fa
   pero' un salvataggio incrementale dopo ogni fonte scritta con successo,
   cosi' un crash a meta' run non perde il lavoro gia' fatto (i.e. le righe
   gia' aggiornate restano salvate anche se il processo muore sulla fonte
   successiva).
"""
from __future__ import annotations

import datetime as dt
import logging
import shutil
from pathlib import Path

import openpyxl

log = logging.getLogger("loop1.excelio")

SHEET_NAME = "Fonti"

# lettera colonna -> intestazione attesa (per un controllo di sanita' alla
# apertura: se l'Excel reale ha intestazioni diverse, meglio fermarsi subito
# con un errore chiaro piuttosto che scrivere nelle celle sbagliate).
EXPECTED_HEADERS = {
    "A": "ID",
    "B": "Citazione",
    "C": "Autori",
    "D": "Anno",
    "E": "Ruolo",
    "F": "Priorit",  # "Priorità" - confronto per prefisso, accenti a parte
    "G": "Nodi",
    "H": "N. usi",
    "I": "Query",
    "J": "Contesto",
    "K": "Claim",
    "L": "Stato acquisizione",
    "M": "Titolo",
    "N": "Tipo",
    "O": "Sede",
    "P": "DOI",
    "Q": "URL",
    "R": "Open access",
    "S": "PDF locale",
    "T": "Peer",
    "U": "Stato verifica",
    "V": "Cosa dice",
    "W": "Note",
}

# colonne che questo script e' autorizzato a scrivere (oltre a W, che si
# appende soltanto)
WRITABLE_COLUMNS = ["L", "M", "N", "O", "P", "Q", "R", "S", "T"]
APPEND_COLUMN = "W"
ID_COLUMN = "A"

ALLOWED_STATO_ACQUISIZIONE = {"da_cercare", "trovata", "scaricata", "non_trovata", "paywall", "ambigua"}
ALLOWED_SI_NO = {"sì", "no"}
ALLOWED_PEER = {"sì", "no", "n.d."}


class ExcelSheet:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.wb = None
        self.ws = None
        self._id_row_map: dict[str, int] = {}

    def backup(self) -> Path:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.path.with_name(f"{self.path.stem}.backup_{ts}{self.path.suffix}")
        shutil.copy2(self.path, backup_path)
        log.info("backup creato: %s", backup_path)
        return backup_path

    def open(self) -> None:
        self.wb = openpyxl.load_workbook(self.path)
        if SHEET_NAME not in self.wb.sheetnames:
            raise ValueError(f"foglio '{SHEET_NAME}' non trovato nel workbook (fogli presenti: {self.wb.sheetnames})")
        self.ws = self.wb[SHEET_NAME]
        self._check_headers()
        self._build_id_row_map()

    def _check_headers(self) -> None:
        problems = []
        for col, expected_prefix in EXPECTED_HEADERS.items():
            cell = self.ws[f"{col}1"]
            actual = (cell.value or "").strip()
            if not actual.lower().startswith(expected_prefix.lower()[:4]):
                problems.append(f"colonna {col}: attesa intestazione tipo '{expected_prefix}...', trovata '{actual}'")
        if problems:
            raise ValueError(
                "le intestazioni del foglio 'Fonti' non corrispondono a quelle attese "
                "(A-W come da specifica). Controlla di puntare al file giusto.\n" +
                "\n".join(problems)
            )

    def _build_id_row_map(self) -> None:
        self._id_row_map.clear()
        row = 2
        max_row = self.ws.max_row
        while row <= max_row:
            val = self.ws[f"{ID_COLUMN}{row}"].value
            if val is not None and str(val).strip():
                self._id_row_map[str(val).strip()] = row
            row += 1
        log.info("indicizzate %d fonti per ID nel foglio '%s'", len(self._id_row_map), SHEET_NAME)

    def all_ids(self) -> list[str]:
        return list(self._id_row_map.keys())

    def get_row_dict(self, fonte_id: str) -> dict | None:
        row = self._id_row_map.get(fonte_id)
        if row is None:
            return None
        out = {}
        for col in EXPECTED_HEADERS:
            out[col] = self.ws[f"{col}{row}"].value
        out["_row"] = row
        return out

    def get_stato_acquisizione(self, fonte_id: str) -> str | None:
        row = self._id_row_map.get(fonte_id)
        if row is None:
            return None
        val = self.ws[f"L{row}"].value
        return (val or "").strip() if val else ""

    def write_fields(self, fonte_id: str, values: dict) -> None:
        """values: {colonna: valore} solo per colonne in WRITABLE_COLUMNS."""
        row = self._id_row_map.get(fonte_id)
        if row is None:
            raise KeyError(f"ID '{fonte_id}' non trovato in colonna {ID_COLUMN} del foglio '{SHEET_NAME}'")
        for col, val in values.items():
            if col not in WRITABLE_COLUMNS:
                raise ValueError(f"colonna '{col}' non e' scrivibile da questo script (solo {WRITABLE_COLUMNS})")
            if col == "L" and val not in ALLOWED_STATO_ACQUISIZIONE:
                raise ValueError(f"valore '{val}' non ammesso per stato acquisizione (L)")
            if col == "R" and val not in ("", None) and val not in ALLOWED_SI_NO:
                raise ValueError(f"valore '{val}' non ammesso per open access (R)")
            if col == "T" and val not in ("", None) and val not in ALLOWED_PEER:
                raise ValueError(f"valore '{val}' non ammesso per peer-reviewed (T)")
            self.ws[f"{col}{row}"] = val

    def append_note(self, fonte_id: str, note_line: str) -> None:
        row = self._id_row_map.get(fonte_id)
        if row is None:
            raise KeyError(f"ID '{fonte_id}' non trovato in colonna {ID_COLUMN} del foglio '{SHEET_NAME}'")
        cell = self.ws[f"{APPEND_COLUMN}{row}"]
        existing = (cell.value or "").strip()
        cell.value = f"{existing}\n{note_line}".strip() if existing else note_line

    def save(self) -> None:
        self.wb.save(self.path)
