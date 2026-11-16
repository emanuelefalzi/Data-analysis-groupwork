#!/usr/bin/env python3
"""Congela il testo di ogni fonte, in due rese, prima che qualcuno la legga.

Per ogni `fonti/pdf/<id>.pdf` produce:
  - `fonti/testi/<id>.txt`      pdftotext in modalita' a flusso di lettura (default)
  - `fonti/testi_raw/<id>.txt`  pdftotext -raw

Perche' due rese dello stesso PDF (lezione della tesi): sui PDF a due colonne la
modalita' di default a volte interfoglia le colonne riga per riga, e allora una
frase del corpo non esiste come stringa contigua; -raw ricostruisce l'ordine di
lettura ma su altri documenti sbaglia dove il default va bene. Nessuna domina.
Il lettore legge `testi/`; il validatore cerca la citazione in tutte e due:
una citazione autentica si ritrova in almeno una, una inventata in nessuna.

Non usa -layout: affianca le colonne e spezza le frasi.

Fonti non-PDF (pagine web salvate, appunti, trascrizioni): metti direttamente
`fonti/testi/<id>.txt` a mano. Lo script non lo sovrascrive.

Uso:
    python3 tools/fonti/estrai_testi.py            # solo le fonti senza testo
    python3 tools/fonti/estrai_testi.py --rifai    # rigenera tutto
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comune  # noqa: E402

SOGLIA_SCANSIONE = 2000   # sotto questi caratteri il PDF e' probabilmente un'immagine


def estrai(pdf: Path, dest: Path, raw: bool) -> int:
    cmd = ["pdftotext", "-enc", "UTF-8"] + (["-raw"] if raw else []) + [str(pdf), str(dest)]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest.stat().st_size if dest.exists() else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rifai", action="store_true", help="rigenera anche i testi gia' presenti")
    a = ap.parse_args(argv)

    if not shutil.which("pdftotext"):
        print("ERRORE: pdftotext non trovato. Installa poppler: brew install poppler")
        return 1
    comune.TESTI.mkdir(parents=True, exist_ok=True)
    comune.TESTI_RAW.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(comune.PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"Nessun PDF in {comune.rel(comune.PDF_DIR)}.")
    fatti, sospetti = 0, []
    for pdf in pdfs:
        fid = pdf.stem
        t, tr = comune.TESTI / f"{fid}.txt", comune.TESTI_RAW / f"{fid}.txt"
        if t.exists() and tr.exists() and not a.rifai:
            continue
        try:
            n = estrai(pdf, t, raw=False)
            estrai(pdf, tr, raw=True)
        except subprocess.CalledProcessError as e:
            print(f"  ERRORE su {pdf.name}: {e.stderr.decode(errors='replace')[:200]}")
            continue
        fatti += 1
        if n < SOGLIA_SCANSIONE:
            sospetti.append((fid, n))
        print(f"  {fid:<28} {n:>9,} caratteri")

    print(f"\nTesti estratti in questo giro: {fatti}")
    if sospetti:
        print("ATTENZIONE: testo quasi vuoto, probabilmente PDF scansionato (serve OCR):")
        for fid, n in sospetti:
            print(f"  {fid}: {n} caratteri")

    # quadro complessivo, per vedere subito cosa manca
    ids_csv = []
    if comune.FONTI_CSV.exists():
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lib.csvio import FontiCSV
        c = FontiCSV(comune.FONTI_CSV); c.open()
        ids_csv = [i for i in c.all_ids() if c.stato(i) not in ("abbandonata",)]
    senza = [i for i in ids_csv if not (comune.TESTI / f"{i}.txt").exists()]
    if senza:
        print(f"\nFonti in fonti.csv ancora senza testo ({len(senza)}): {', '.join(senza)}")
        print("  -> manca il PDF in fonti/pdf/<id>.pdf, oppure metti a mano fonti/testi/<id>.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
