---
name: essay-fonti
description: Fase 1, loop 1 — recupero delle fonti. Identifica le fonti di input/fonti.csv via API bibliografiche (Crossref, OpenAlex, arXiv, Unpaywall), scarica i PDF open access, congela i testi in due rese con pdftotext e prepara fonti/fonti.bib. Usala quando l'autore aggiunge fonti o chiede di "cercare/scaricare le fonti".
---

# /essay-fonti

Tutti i comandi con percorsi assoluti, da qualunque cartella (mai `cd` nella radice).

1. **Dry-run del recupero**: `python3 "<radice>/tools/fonti/recupera.py"`. Interroga davvero le
   API ma non scrive e non scarica. Mostra all'autore cosa farebbe: identificate, ambigue, non
   trovate. Per le ambigue il report sta in `fonti/recupero/report.md` e i candidati in
   `fonti/recupero/da_disambiguare.json`: si sceglie con l'autore, poi si corregge la `query` nel CSV.
2. **Commit**: `python3 "<radice>/tools/fonti/recupera.py" --commit`. Fa il backup del CSV, scrive
   solo le colonne di acquisizione, salva dopo ogni fonte, scarica i PDF open access in
   `fonti/pdf/`. Non usa alcun LLM per scegliere il candidato: e' punteggio deterministico.
3. **Paywall**: le fonti `paywall` hanno l'URL nel CSV. Non le scarichi tu e non passi dal login
   d'ateneo: le elenchi all'autore, che le scarica e le mette in `fonti/pdf/<id>.pdf` (poi
   `stato` = `gia_presente`).
4. **Testi**: `python3 "<radice>/tools/fonti/estrai_testi.py"`. Due rese per PDF (default e `-raw`):
   il validatore cerca le citazioni in entrambe. Se segnala PDF quasi vuoti, sono scansioni: serve
   OCR, dillo. Pagine web, interviste, appunti: l'autore (o tu, su sua richiesta) mette il testo
   direttamente in `fonti/testi/<id>.txt`.
5. **Bibliografia**: `python3 "<radice>/tools/fonti/genera_bib.py"` (dry-run), poi `--commit`. Le
   voci sono una prima stesura: segnala all'autore quelle incomplete. Mai completarle a memoria
   o dal web senza dirlo. `python3 "<radice>/tools/bib.py"` mostra come verra' resa ogni voce.

Chiudi con: quante fonti hanno testo, quante mancano e perche'. Prossima fase: `/essay-estrai`.
