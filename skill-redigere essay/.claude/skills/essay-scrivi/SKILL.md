---
name: essay-scrivi
description: Fase 6 — stesura. Invoca l'agente section-writer sulle sezioni ancora senza DRAFT, una alla volta e in ordine di scaletta, e dopo ciascuna lancia tools/stesura/verifica.py. Usala dopo /essay-scaletta (e /essay-glossario se fatto). /essay-scrivi <id> per una sezione sola, /essay-scrivi per tutte.
---

# /essay-scrivi [<id>]

**Sequenziale, mai parallelo**: ogni writer legge il DRAFT della sezione precedente per la
continuita', e se quella non c'e' si ferma. Il parallelismo qui produce sezioni che si ripetono e
non si agganciano.

1. Precondizioni: `build/sezioni.json` aggiornato (rilancia `tools/scaletta/leggi_scaletta.py` se la
   scaletta e' cambiata) e senza problemi bloccanti.
2. **Sezione pilota**: se nessuna sezione e' ancora scritta, scrivi prima solo la prima sezione
   foglia con argomento vero (non l'introduzione), e mostrala all'autore: e' la calibrazione della
   voce. Quello che passa qui diventa il registro di tutto l'essay. Prosegui sulle altre solo dopo
   il suo ok (nella tesi il pilota ha trovato la frase-cerniera in tre cappelli su tre).
3. Per ogni sezione senza DRAFT, nell'ordine di scaletta (saltando le `escludi`):
   - lancia un subagent `section-writer` con il prompt «Scrivi la sezione <id>. Radice del
     progetto: <radice>.»;
   - quando torna, lancia tu `python3 "<radice>/tools/stesura/verifica.py" <id>`: se ci sono HIGH,
     rilancia il writer sulla stessa sezione passandogli l'output. Non correggere tu la prosa;
   - annota cosa il writer ha dichiarato: buchi, cortezza, eccedenza.
4. Le sezioni-cappello (con figli) hanno spesso poco materiale: va bene un paragrafo breve, o
   nessun testo se il contenuto e' vuoto (il titolo basta).
5. Alla fine: `python3 "<radice>/tools/stato.py"` e un riepilogo per l'autore con tutti i
   `[[GAP:]]` e `[[CIT-NEEDED:]]` dichiarati, sezione per sezione.

Prossima fase: `/essay-controlla`.
