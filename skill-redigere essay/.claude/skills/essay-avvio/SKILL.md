---
name: essay-avvio
description: Primo comando quando si apre la cartella per un nuovo essay (o la si riapre). Controlla progetto.json, brief, elenco fonti e template Word, chiede all'autore cio' che manca e dice da quale fase ripartire. Usala anche quando l'autore chiede "da dove parto", "come funziona", "a che punto siamo".
---

# /essay-avvio

1. Leggi `CLAUDE.md` e `PROCESSO.md` della radice, se non li hai gia' in contesto.
2. Lancia `python3 "<radice>/tools/stato.py"` e leggi l'output.
3. Per ogni riga non spuntata della fase 0, chiedi all'autore — una domanda per cosa che manca,
   tutte insieme, non a rate:
   - **`progetto.json`**: titolo, autore, lingua (`en`/`it`), parole totali, stile citazionale
     (solo `apa7` e' implementato in `tools/bib.py`), nomi fissi (es. il nome di un'azienda che
     non deve mai diventare «the company»), se vuole il doppio auditor e il secondo lettore
     NotebookLM, l'email per il polite pool delle API bibliografiche;
   - **`input/brief.md`**: consegna, tesi o domanda centrale, **domande per le fonti** (senza
     queste il loop di estrazione non parte), idee proprie, vincoli;
   - **`input/fonti.csv`**: le fonti, anche solo `id,autori,anno` (id stile `cognomeanno`,
     minuscolo, unico); i PDF che ha gia' vanno in `fonti/pdf/<id>.pdf` con `stato` = `gia_presente`;
   - **il template Word**: `input/template.docx`. **Se manca, chiedilo esplicitamente** e non
     proseguire oltre la fase 7 senza: `assemble.py` si rifiuta, e non se ne genera uno al posto
     suo. Spiega che puo' contenere i segnaposto `{{TITOLO}}`, `{{AUTORE}}`, `{{CORPO}}`.
4. Compila tu `progetto.json` con le risposte (e' configurazione, non testo dell'essay). Il brief
   e la scaletta li scrive l'autore: puoi proporre una bozza del brief dalle sue risposte, ma la
   fa sua lui.
5. Chiudi dicendo la fase da cui si riparte e la skill che la esegue.
