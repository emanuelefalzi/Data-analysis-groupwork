# Istruzioni per il LETTORE del loop 2

Verifichi UNA coppia (nodo × fonte) di una tesi di laurea: stabilisci se la fonte
sostiene davvero l'affermazione che la tesi le attribuisce.

BASE = /Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/
NON fare `cd` in quella cartella: rompe gli import di Python. Usa percorsi
assoluti lavorando da un'altra cwd.

## Cosa leggere prima di iniziare
1. `FONTI/pipeline/prompt/A - lettore ESEGUIBILE.md` — prompt operativo e contratto di output.
   PREVALE SU TUTTO.
2. `FONTI/pipeline/prompt/A - lettore fonti.md` — metodologia. La sua sezione
   «CONTRATTO DI OUTPUT» è vecchia e va IGNORATA.

## Cosa fare
Leggi il task che ti viene indicato in `FONTI/pipeline/loop2/task/<nodo>__<id_fonte>.json`,
applica metodo e contratto, e scrivi il JSON di output in
`BASE/FONTI/estrazioni/estratti/<nodo>__<id_fonte>.json` (percorso ASSOLUTO: la cartella `estrazioni/estratti/` sta sotto `FONTI/`, NON dentro `FONTI/pipeline/loop2/`).

## Vincoli verificati da uno script — violarli fa scartare il tuo lavoro
- `citazione_verbatim` ritrovabile nel testo sorgente con match esatto, minimo
  25 caratteri
- UN SOLO passaggio contiguo: mai concatenare frasi prese da punti diversi
  del documento, nemmeno se insieme spiegano meglio il punto
- mai dal front matter (ringraziamenti, copyright, recapiti, "we thank",
  "all rights reserved")
- deve essere la frase su cui si fonda davvero `cosa_dice_davvero`, non una
  scelta comoda perché facile da ritrovare
- se l'esito è `non verificabile`, `cosa_dice_davvero` deve superare i 200
  caratteri e dichiarare cosa hai letto e cercato
- se il `claim` inizia con `ATTRIBUZIONE INCERTA:`, l'esito NON può essere
  `usabile` e le `note` devono contenere quella stringa
- esattamente le 7 chiavi previste, nessuna in più

## Citazioni congiunte
Molti claim dicono «cited jointly with X, Y; the paragraph does not indicate
which source supports which clause». In quel caso valuta la quota che QUESTA
fonte può sostenere e dichiara in `note` quali clausole restano scoperte: non
declassare la fonte per clausole che spettano a un'altra.

## Report
Massimo 6 righe: l'esito, la ragione in una frase, le difficoltà incontrate.
NON incollare il JSON.
