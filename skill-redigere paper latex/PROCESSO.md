# Il processo — da scaletta.md al PDF

Cosa fa la pipeline, in che ordine, e perché ogni pezzo esiste. Le regole nascono dalla tesi di
Lele (`../skill-redigere essay/PROCESSO.md`, sezione «Lezioni della tesi») e da `../RULES.md`.

## Cosa cambia rispetto a `skill-redigere essay`

| | Essay | Paper LaTeX |
|---|---|---|
| scaletta | `scaletta/scaletta.md` con sintassi propria | `../scaletta.md` della repo, letta così com'è |
| verifica delle fonti | `/essay-estrai` (lettori + `valida.py`) | già fatta: tesi della scaletta ristrette sul txt (16/11) |
| unità citabile | punto validato `fonte#n` | riga «`chiave`: tesi» del blocco Sources della sezione |
| numeri | dal materiale | dal materiale **e** dalle celle delle tabelle del do-file |
| lunghezza | parole per sezione | **pagine** per sezione, floats compresi; limite 20 sul corpo |
| floats | nessuno | figure (`figures.zip`) e tabelle (`RQ1_tables.doc`) convertite in LaTeX |
| uscita | Word dal template | LaTeX (biblatex-apa) compilato in PDF, conteggio pagine automatico |
| appendice | — | Appendix A sul dataset, contratto proprio da `construction.pdf` |

Non cambia: la regola sovrana, il claim che si restringe, la cucitura e il connettivo, il LEDGER,
nessun pavimento di parole, la sezione pilota, i derivati che non si toccano a mano.

## Lo schema

```
 ../scaletta.md ─┐
 input/piano.md ─┼─► leggi_scaletta.py ─► build/sezioni.json  (contenuto, numeri, fonti validate, parole, floats)
 tabella.csv ────┘                              │
 figures.zip, RQ1_tables.doc ─► floats.py ─► build/figures, build/tabelle/*.tex, build/floats.json
 construction.pdf ─► Appendix A già scritta (5. paper e documentazione di percorso/)
                                                │
 per sezione, in ordine: ctx.py ─► paper-writer ─► verifica.py      (pilota: 5.1)
                                                │
 verifica.py --tutte ─► paper-claim-auditor ─► fix / riscrittura / escalation ─► prose-auditor
                                                │
 assemble.py ─► latex/gen/*.tex ─► compila.py (pdflatex + biber|bibtex) ─► paper_group21_v5.pdf, pagine del corpo ≤ 20
```

## Fase 0–1 — avvio (`/paper-avvio`)

`leggi_scaletta.py` legge i blocchi della scaletta: **Content** e **Numbers (log)** diventano
materiale; **Guardrails** diventano trappole; **Editorial notes** istruzioni; **Claude's
additions** restano fuori (non sono approvate). Le chiavi del blocco **Sources** diventano citabili
solo se la routine di validazione le ha giudicate citabili *per quella sezione*.

**Perché la tesi della scaletta e non l'esito della routine.** La routine di validazione
(16/11) ha letto ogni fonte contro la tesi di allora; il gruppo ha poi ristretto tutte le tesi
«da riformulare» e «non usabile» sul txt, con un secondo lettore per le seconde. `tabella.csv`
non è stata aggiornata dopo: i suoi esiti sono superati, la sua estrazione resta come contesto.

`piano.py` traduce le pagine in parole: (pagine − spazio dei floats) × `parole_per_pagina`.
**Perché le pagine e non le parole.** Il vincolo del corso è sulle pagine, e figure e tabelle
«contano» e occupano posto: un budget in sole parole sforerebbe sempre. Dopo la prima
compilazione `compila.py` misura le parole per pagina vere e si ricalibra.

## Fase 2 — floats (`/paper-floats`)

`floats.py` legge gli RTF del do-file in Python puro (`rtf_tabelle.py`) e converte le 7 tabelle
in booktabs compatte (i dummy del lead investor diventano una riga «Yes», salvo quelli nominati
dalla colonna `tieni`; i coefficienti omessi spariscono) **senza toccare una cella**. Le figure
vanno a coppie nello stesso float, ognuna con il suo numero, come nel paper v4. Le 7 tabelle e la
figura «di testo» del paper v4 stanno in `latex/testo/`, ricostruite dalla scaletta e dal log.

**Perché compatte e a coppie.** 35 floats in 20 pagine: su un PDF di prova con testo finto
della lunghezza obiettivo i floats prendono circa 11,6 pagine e la prosa sta in circa 4.800
parole. Le tabelle del do-file hanno 75–200 righe; quelle che servono sono 10–20.

## Fase 3 — stesura (`/paper-scrivi`)

Una sezione alla volta, in ordine, con `ctx.py` → `paper-writer` → `verifica.py`. **Pilota: 5.1**,
perché è la sezione che mette insieme tutto ciò che può andare storto (numeri con identità,
verdetti, rimandi ai floats, niente causalità): quello che passa lì è il registro di tutto.
L'abstract si scrive per ultimo, dai DRAFT.

`verifica.py` (deterministico): token e chiavi ammesse; numeri nel materiale; linguaggio causale
su gap e hype; «no effect»; verdetti; connettivo dopo citazione; frasi-cerniera; antiplagio a 8
parole sui verbatim; parole contro obiettivo; LEDGER allineato; ogni float richiamato.

## Fase 4 — controlli (`/paper-controlla`)

`paper-claim-auditor` span-first, frase per frase contro il materiale. Correzioni locali al
`fix-applier`, riscritture al writer, decisioni di merito al gruppo (`reports/escalation.md`).
Un `prose-auditor` sul documento intero alla fine.

## Fase 5 — LaTeX (`/paper-latex`)

`assemble.py` converte i token (biblatex-apa: `\textcite`, `\parencite`), piazza ogni float dopo
il paragrafo che lo richiama per primo, scrive `latex/gen/`. `compila.py` compila e legge dalla
`.aux` la pagina della label `corpo-fine` (messa dopo un `\FloatBarrier`, così nessun float del
corpo scivola nelle references): quello è il numero di pagine del corpo, e deve essere ≤ 20.
`flafter` e `placeins` tengono ogni float dopo il suo richiamo e dentro la sua sezione.

**Se sfora**: si propongono al gruppo, in ordine di costo, affiancare figure, escludere un float,
ridurre le pagine di una sezione nel piano. Mai tagli silenziosi di affermazioni.
