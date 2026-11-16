---
name: paper-appendice
description: Prepara il CONTRATTO (non la prosa) di Appendix A sulla costruzione del dataset, da construction.pdf e dataset.py, nel formato della scaletta. Il gruppo lo approva, poi /paper-scrivi A.1... scrive la prosa. Fuori dal limite di 20 pagine.
---

# /paper-appendice

L'appendice e' l'unica parte del paper che non nasce da `scaletta.md`: il suo materiale e'
`2. dataset/construction.pdf` (fatti descrittivi sul dataset, ammessi da RULES.md) e
`1. python/dataset.py` (cosa fa davvero il codice).

1. Estrai il testo: `pdftotext "<repo>/2. dataset/construction.pdf" "<radice>/build/construction.txt"`.
   Leggilo con uno script o a pezzi, non tutto nel contesto se e' lungo.
2. Per ogni A.x di `input/appendice-A.md` scrivi il blocco `#### Content` con 3–5 punti nel
   formato della scaletta (etichetta in grassetto, parole chiave, 30–40 parole), e `**Words:**`.
   Ogni punto deve essere ritrovabile in `construction.txt` o nel codice: cita fra parentesi la
   riga o la funzione (es. «construction.pdf L122–130», «dataset.py `merge_same_day`»).
3. **Dove construction.pdf e' superato** (elenco in testa a `appendice-A.md` e in RULES.md,
   *Known inconsistencies*) vince RULES.md: scrivi la versione corretta e segnala la differenza
   nel `#### Guardrails`. Non correggere `construction.pdf`.
4. Niente numeri del campione gia' in 3.1: rimando con `[[SEC:3.1]]`.
5. Mostra il contratto al gruppo. Solo dopo l'approvazione: `/paper-scrivi A.1` ecc.
