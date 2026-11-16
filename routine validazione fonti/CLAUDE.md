# Routine di validazione fonti — doppio lettore indipendente

Questa cartella contiene la routine con cui Lele ha verificato le fonti della tesi (loop 2:
108 coppie, lettore locale + NotebookLM + validatore meccanico), adattata a **fonti che sono
siti web**. Quando Lele dice «valida le fonti», «fai il giro sulle fonti», «loop fonti» o
simili, intende questa procedura. Va seguita così com'è.

## La regola sovrana

La domanda non è «il claim è vero?» ma **«questa pagina, così come l'abbiamo salvata, sostiene
questo claim, così come è formulato?»**. Nessun agente inventa, ammorbidisce o allarga. Un
`non usabile` dichiarato vale più di un `usabile` sbagliato: nel dubbio vince l'esito più
conservativo.

## Cosa c'è

| Percorso | Cos'è |
|---|---|
| `coppie.csv` | **L'input.** Una riga per ogni coppia (sezione del lavoro × pagina citata). Da compilare. |
| `prompt/A - lettore sito.md` | Prompt del lettore A (subagent Sonnet, uno per coppia) |
| `prompt/B - secondo lettore notebooklm sito.md` | Prompt del secondo lettore su NotebookLM |
| `strumenti/salva_pagine.py` | Fase 0: congela ogni URL in `lavoro/testi/<id>.txt` + data di accesso |
| `strumenti/prepara.py` | Fase 1: un task JSON per coppia in `lavoro/task/` |
| `strumenti/valida.py` | Fase 3: valida i due lettori, verifica i verbatim, scrive `esiti.csv` e `referto.md` |
| `originali tesi/` | I file **originali** della tesi, per riferimento. Non si eseguono: puntano all'Excel della tesi. `prompt/A - lettore fonti.md` è la metodologia completa e va letta dal lettore A. |

Usa `/usr/bin/python3` (gli script usano solo la libreria standard). Lancia gli script con
percorso assoluto.

## `coppie.csv` — colonne

`sezione, id_fonte, url, citazione, tipo_fonte, ruolo, claim`

- `id_fonte`: breve, senza spazi (`acme_chi_siamo`). Una pagina = un id: se due URL dello stesso
  sito sostengono cose diverse, sono due fonti.
- `tipo_fonte`: `sito dell'oggetto` (il sito dell'azienda di cui si parla), `istituzionale`,
  `stampa`, `accademico`, `altro`. Conta: il sito dell'oggetto prova solo cosa l'azienda dichiara.
- `ruolo`: `mattone stretto` se l'argomento crolla senza quella fonte, altrimenti `sfondo`.
- `claim`: la frase che il lavoro attribuisce alla pagina, il più possibile uguale a come è scritta.

Se Lele dà un documento (Word, PDF) invece del CSV, **il primo lavoro è costruire `coppie.csv`**
estraendo ogni citazione e la frase che regge, e farglielo approvare prima di partire.

## La procedura

1. **Fase 0 — congelare.** `salva_pagine.py`. Ogni pagina sotto ~1.500 caratteri è sospetta (sito in
   JavaScript, cookie wall): prendila col browser integrato (`get_page_text`), salvala nello stesso
   `.txt` e scrivi `"estrazione": "browser"` nel `.meta.json`. Da qui in poi **nessuno legge il sito
   dal vivo**: tutti leggono il testo congelato, altrimenti i due lettori leggono pagine diverse.
2. **Fase 1 — task.** `prepara.py`.
3. **Fase 2a — lettore A.** Un subagent **Sonnet** per coppia, in parallelo, contesto pulito. Gli si
   passa: il percorso del suo task, il prompt A, e la metodologia `originali tesi/prompt/A - lettore
   fonti.md` (ignorando la sua sezione «CONTRATTO DI OUTPUT»). Scrive solo il suo JSON.
4. **Fase 2b — NotebookLM**, solo dopo che A ha finito. Segui il prompt B: carica i `.txt` congelati
   come sorgenti (se `source_type="file"` non accetta il `.txt`, usa `source_type="text"` col
   contenuto del file e il titolo uguale all'`id_fonte`), mappa gli id, una query per coppia **con
   `source_ids` ristretto a quella sola fonte**. Può farlo un subagent per blocchi di coppie, che
   non deve leggere `lavoro/estratti/`.
5. **Fase 3 — validare.** `valida.py`. Gli output scartati vanno **rifatti** dal lettore
   corrispondente con l'errore in mano, non corretti a mano. Ripeti finché non ci sono scarti.
6. **Fase 4 — referto a Lele.** `referto.md` ordina per gravità: convergenza negativa →
   divergenze → entrambi non verificabile → da riformulare → positive. Le **divergenze** e i
   `non usabile` li decide il gruppo, non l'agente. Per i `da riformulare` proponi la frase
   ristretta (vince `cosa_dice_davvero`: il claim si restringe, mai si allarga).

## Regole che si rompono più spesso (imparate sulla tesi)

- **Verbatim concatenati.** Il lettore incolla due frasi da punti diversi: la stringa non esiste e
  `valida.py` la scarta. Un solo passaggio contiguo.
- **Involucro intorno al verbatim di NotebookLM** («Dalla sezione X: "…"»): fa fallire il match e
  declassa verdetti giusti. Solo le parole esatte.
- **`source_ids` dimenticato**: NotebookLM risponde da un'altra pagina e il confronto è nullo.
- **Conoscenza pregressa**: su aziende note il modello «ricorda» cose che la pagina non dice.
  Vale solo il testo congelato.
- **Il sito dell'azienda come prova di un fatto**: «X è leader» diventa «X si presenta come
  leader». Questo è il rischio tipico delle fonti web, e nella tesi non c'era.
- **Ciò che la pagina riporta di altri** (un cliente citato, uno studio ripreso) non è della pagina.
- **Citazioni dal boilerplate** (cookie, footer, P. IVA): presenti nel testo, prive di contenuto.

## Modelli e controllo

Subagent su **Sonnet**. La sicurezza viene dai **due lettori indipendenti** che non si vedono e
dal validatore meccanico, non da un modello più grande. L'orchestratore non scrive verdetti: lancia,
valida, arbitra le divergenze solo presentandole a Lele.

## Cosa non fare

- Non correggere a mano i JSON dei lettori per farli passare.
- Non riscaricare le pagine a metà giro (`--rifai` cambia la data di accesso e il testo).
- Non far leggere a NotebookLM gli esiti di A.
- Non modificare il lavoro di gruppo: il referto propone, decide il gruppo.
