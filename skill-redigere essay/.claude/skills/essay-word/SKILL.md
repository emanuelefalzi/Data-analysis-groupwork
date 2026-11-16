---
name: essay-word
description: Fase 8 — assemblaggio del Word finale dal template dell'autore - citazioni APA risolte dal .bib, titoli e prosa negli stili del template, reference list generata - e controllo finale del .docx. Se il template manca, si ferma e lo chiede. Usala dopo /essay-controlla.
---

# /essay-word

1. **Template**: se `template_docx` di `progetto.json` non esiste, **fermati e chiedilo all'autore**.
   Non generarne uno, non usarne uno trovato altrove: stili, margini, font e frontespizio sono suoi.
   Spiegagli che puo' mettere nel template `{{TITOLO}}`, `{{AUTORE}}` e un paragrafo `{{CORPO}}`
   dove vuole il testo (senza `{{CORPO}}` il testo va in coda).
2. **Chiudi Word.** Se esiste un file `~$…` accanto al template o in `out/`, fermati e dillo: non
   cancellarlo tu.
3. `python3 "<radice>/tools/word/assemble.py" --dry-run`. Se rifiuta, il suo elenco di motivi e'
   esattamente cio' che manca: sezioni senza DRAFT, buchi aperti, chiavi assenti dal .bib.
   Con buchi aperti l'autore puo' volere comunque una bozza: `--bozza` (i token restano nel testo,
   ben visibili).
4. `python3 "<radice>/tools/word/assemble.py"` → `out/essay.docx` (o `output_docx`).
5. `python3 "<radice>/tools/word/controlla_docx.py"`: nessun token residuo, un titolo per sezione
   nell'ordine giusto, nessun numero doppio nei titoli, stili previsti, parole totali.
6. Consegna all'autore il percorso del file e cosa controllare a mano aprendolo: aggiornare
   l'indice se c'e' (Word lo chiede all'apertura), voci bibliografiche incomplete segnalate, resa
   del frontespizio.
