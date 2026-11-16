---
name: essay-intermedi
description: Fase 3 — documenti intermedi. Rielabora i punti validati in forma leggibile per l'autore - schede per fonte, matrice domanda x fonte, elenco dei punti con id, e una sintesi argomentata per domanda scritta da un agente e verificata da script. Usala dopo /essay-estrai, prima di costruire la scaletta.
---

# /essay-intermedi

1. `python3 "<radice>/tools/fonti/intermedi.py"` → `intermedi/schede/<id>.md`, `intermedi/matrice.md`,
   `intermedi/punti.md`. Sono derivati: non si correggono a mano.
2. **Sintesi per domanda, in parallelo**: un subagent `sintesi-domande` per domanda del brief.
   Prompt: «Scrivi `intermedi/sintesi-<Dn>.md` per la domanda <Dn> secondo il tuo contratto».
3. `python3 "<radice>/tools/fonti/verifica_sintesi.py"`: ogni paragrafo deve essere ancorato a punti
   validati o dichiararsi `Lacuna:`/`Tensione:`/`Nota:`. Rilancia l'agente sulle sintesi con HIGH.
4. Presenta all'autore, in breve: per ogni domanda, le posizioni trovate, le lacune e le tensioni,
   e quali punti sembrano portanti. Indica i file da leggere (`matrice.md` per il colpo d'occhio,
   le sintesi per il ragionamento, le schede per il dettaglio).

Prossima fase: `/essay-scaletta`, con l'autore.
