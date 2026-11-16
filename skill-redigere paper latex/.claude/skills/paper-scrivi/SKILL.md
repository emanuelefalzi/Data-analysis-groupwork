---
name: paper-scrivi
description: Fase 3 - stesura. Lancia il subagent paper-writer (model sonnet) su una sezione alla volta, in ordine di scaletta, e dopo ciascuna tools/verifica.py. /paper-scrivi <id> per una sezione, /paper-scrivi per tutte quelle mancanti, /paper-scrivi abstract alla fine.
---

# /paper-scrivi [<id>]

**Sequenziale, mai parallelo**: ogni writer legge il DRAFT della sezione precedente.

1. Precondizioni: `build/sezioni.json` e `build/floats.json` aggiornati (rilancia
   `leggi_scaletta.py` e `floats.py` se scaletta o piano sono cambiati).
2. **Sezione pilota**: se nessuna sezione e' scritta, scrivi prima solo **5.1** (risultati su
   exit: numeri, tabella, figura, verdetti) e mostrala all'utente. E' la calibrazione del
   registro e dei rimandi ai floats: quello che passa li' vale per tutto il paper.
3. Per ogni sezione senza DRAFT, in ordine (le sezioni-cappello senza contenuto non si scrivono):
   - subagent `paper-writer` **con `model: "sonnet"` esplicito nella chiamata** (gli agenti di
     questa cartella non si caricano se la sessione parte dalla radice della repo; in quel caso
     usa un subagent generico e passagli il testo di `.claude/agents/paper-writer.md` come
     istruzioni) con il prompt «Scrivi la sezione <id>. Radice del progetto: <radice>.»;
   - poi lancia tu `python3 "<radice>/tools/verifica.py" <id>`: se ci sono HIGH, rilancia il
     writer sulla stessa sezione con l'output. **Non correggere tu la prosa**;
   - annota buchi, cortezza, eccedenza dichiarati.
4. **Abstract per ultimo** (`/paper-scrivi abstract`): il suo materiale sono i DRAFT gia' scritti.
5. Fine: `python3 "<radice>/tools/stato.py"` e un riepilogo con tutti i `[[GAP:]]` e
   `[[CIT-NEEDED:]]`, sezione per sezione, spiegati per esteso.

Prossima fase: `/paper-controlla`.
