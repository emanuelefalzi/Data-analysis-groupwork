---
name: essay-scaletta
description: Fase 4 — costruzione della scaletta CON l'autore, passo per passo, a partire dal brief e dai documenti intermedi; poi la legge e la controlla con tools/scaletta/leggi_scaletta.py. La scaletta e' il contratto del testo. Usala quando l'autore vuole impostare, rivedere o allungare la struttura dell'essay.
---

# /essay-scaletta

**La scaletta e' dell'autore.** Tu proponi, lui decide. Nella tesi la scaletta (129 nodi con
`Descrizione` argomentata) l'ha scritta l'autore in dialogo con Claude, e la regola sovrana dice
che il testo non contiene nulla che non stia li': se la scrivi tu da solo, la regola sovrana
protegge le tue idee, non le sue.

## Come si lavora

1. Leggi `input/brief.md`, `intermedi/matrice.md`, le `intermedi/sintesi-*.md`, `intermedi/punti.md`.
2. **Proposta di impianto** (solo titoli, 4-8 sezioni, con `ruolo` di una riga e parole): mostrala
   in chat e chiedi cosa cambiare. Ragiona sull'argomento: dove sta la tesi, cosa deve essere
   dimostrato prima di cosa, dove le fonti sono forti e dove l'essay poggia sul ragionamento
   dell'autore. Distribuisci le parole su `parole_totali`.
3. **Sezione per sezione**, con l'autore: proponi i `punti` pertinenti (id da `punti.md`, con il loro
   `cosa_dice` e la `forza`), le `trappole` che vedi (punti di seconda mano, fonte non peer-reviewed
   su un claim forte, tensioni fra punti), l'`aggancio`. **Il contenuto lo scrive l'autore**: puoi
   chiedergli le sue idee e metterle in forma, ma ogni frase del contenuto deve essere sua o
   approvata da lui, e non ci metti affermazioni di letteratura che non stanno in un punto.
4. Scrivi `scaletta/scaletta.md` con la sintassi del file d'esempio (leggila: e' rigida apposta).
5. `python3 "<radice>/tools/scaletta/leggi_scaletta.py"` → `build/sezioni.json` + `reports/scaletta.md`.
   Mostra all'autore: problemi bloccanti, sezioni con poco materiale per le parole (usciranno corte:
   **non esiste un pavimento di parole**, il writer non riempie), punti validati non usati.
6. Itera finche' non ci sono problemi bloccanti e l'autore dice che va.

## Cose che valgono sempre

- Un punto citato nella scaletta deve essere validato (sta in `build/estratti.json`). Una fonte
  senza punti validati non si cita: se l'autore la vuole, si torna a `/essay-estrai`.
- Le fonti ammesse di una sezione sono SOLO quelle dei suoi punti.
- Se il materiale e' molto piu' delle parole, la sezione andra' compressa: **tagliare affermazioni
  e' una decisione dell'autore**, non del writer. Chiedi ora cosa sacrificare, oppure alza le parole.
- Introduzione e conclusione hanno anche loro un contenuto: «riprendere la tesi» non e' materiale.

Prossima fase: `/essay-glossario` (facoltativo) o `/essay-scrivi`.
