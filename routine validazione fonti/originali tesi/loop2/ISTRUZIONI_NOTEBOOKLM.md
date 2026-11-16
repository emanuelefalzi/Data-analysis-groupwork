# Istruzioni per il SECONDO LETTORE (NotebookLM)

Fornisci una lettura indipendente delle stesse coppie già verificate dal lettore
locale. Dove i due concordano il dato è solido; dove divergono decide la persona.

BASE = /Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/
NON fare `cd` in quella cartella: percorsi assoluti da un'altra cwd.

## Cosa leggere prima
`FONTI/pipeline/prompt/B - notebooklm ESEGUIBILE.md` — testo della query, regole
anti-contaminazione, contratto di output. Prevale su tutto.

Notebook: `7060cbf5-c222-410f-a2be-c532433e962c` ("fonti tesi def", 48 sorgenti).

## Procedimento obbligatorio per ogni coppia
1. `notebook_get` per l'elenco delle sorgenti coi loro `id`. I titoli coincidono
   coi nomi dei PDF in `FONTI/fonti def/`, quindi abbini ogni `id_fonte` alla sorgente
   dal cognome dell'autore e dall'anno.
2. `notebook_query` passando **`source_ids` con il SOLO id della sorgente in
   esame**. Senza, NotebookLM pesca dalle altre 47 fonti e il confronto perde
   ogni significato.
3. Query esattamente come nel prompt B, sostituendo `{citazione}` e `{claim}`
   presi dal task in `FONTI/pipeline/loop2/task/<nodo>__<id_fonte>.json`.
4. Converti tu la risposta sostantiva in `esito_nlm` coi criteri del prompt B.
   NotebookLM non deve produrre i quattro valori.
5. Se la citazione restituita non proviene dalla fonte in esame:
   `fonte_citata_corretta: false` ed esito `non verificabile`.
6. Se la fonte non è presente fra le sorgenti del notebook: scrivi comunque il
   JSON con `esito_nlm: "non verificabile"`, `fonte_citata_corretta: false` e
   nota «fonte non presente nel notebook».

## Output
Un JSON per coppia in `BASE/FONTI/estrazioni/estratti_nlm/<nodo>__<id_fonte>.json` (percorso ASSOLUTO: la cartella sta sotto `FONTI/`, NON dentro `FONTI/pipeline/loop2/`), con esattamente
queste 7 chiavi: `nodo`, `id_fonte`, `esito_nlm`, `risposta_sintetica`,
`citazione_verbatim_nlm`, `fonte_citata_corretta`, `note`.

Uno script incrocia la tua `citazione_verbatim_nlm` col testo locale in
`FONTI/pipeline/testi estratti/<id>.txt` e declassa l'esito a `non verificabile` se non si
ritrova.

**Cosa mettere in `citazione_verbatim_nlm`, con precisione.** Il campo contiene **SOLO il
passaggio citato, UNO SOLO, e le parole esatte** che NotebookLM restituisce fra virgolette.
Non riscriverle, non correggerle, non tradurle — ma nemmeno impacchettarle. In particolare:

- **NIENTE involucro narrativo.** `Dalla sezione "Introduction" (p. 731, [7, 8]): "Packaged
  software applications…"` fa fallire il match e provoca un declassamento **spurio**. Va
  scritto solo `Packaged software applications…`.
- **NIENTE passaggi multipli** concatenati con `\n\n`, nemmeno se insieme spiegano meglio il
  punto: il contratto chiede un solo passaggio contiguo. Scegli il passaggio su cui si fonda
  davvero il tuo giudizio.
- Sezione e pagina, se te le serve annotare, vanno in `note`, non qui.

Errore osservato il 2026-09-07 su tutte e tre le coppie del nodo 4.1.3: i verdetti erano
corretti, il campo conteneva l'involucro, e lo scrittore li ha declassati tutti e tre a
`non verificabile` per un problema di formato.

NON aprire l'Excel.

## Report
Massimo 10 righe: per ogni coppia l'esito e se la citazione veniva dalla fonte
giusta. Segnala se `source_ids` non ha funzionato.
