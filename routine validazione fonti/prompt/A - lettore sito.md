# Prompt A — Lettore di una pagina web contro un claim

Adattamento per siti web del prompt A della tesi (`originali tesi/prompt/A - lettore ESEGUIBILE.md`).
Metodologia completa in `originali tesi/prompt/A - lettore fonti.md`: leggila per intero prima
di iniziare, ma **ignora la sua sezione «CONTRATTO DI OUTPUT»**, superata da quella qui sotto.

Un'esecuzione = **una coppia (sezione × fonte)**. Un subagent Sonnet per coppia, in parallelo.
Nessun subagent scrive in `esiti.csv` o in `referto.md`: lo fa solo `strumenti/valida.py`.

## Input

Il task in `lavoro/task/<sezione>__<id_fonte>.json`:

- `sezione` — la parte del lavoro di gruppo che cita la fonte (es. `2.1`)
- `id_fonte`, `url`, `citazione` — la pagina e come viene citata
- `tipo_fonte` — `sito dell'oggetto` (il sito dell'azienda/ente di cui si parla), `istituzionale`,
  `stampa`, `accademico`, `altro`
- `ruolo` — `mattone stretto` (regge l'argomento) oppure `sfondo`
- `claim` — cosa il lavoro attribuisce alla pagina
- `percorso_testo` — il **testo congelato** della pagina (`lavoro/testi/<id_fonte>.txt`), salvato
  in data `data_accesso`. **Leggi quello, non il sito dal vivo**: la pagina può essere cambiata,
  e il confronto con NotebookLM regge solo se entrambi leggono la stessa versione.

## Compito

Stabilire se **quella pagina**, così come è stata salvata, sostiene **quel claim**, così come è
formulato. Non se il claim è vero, non se il sito è affidabile in generale, non migliorare il claim.

Metodo, in ordine: mappa la pagina prima di cercare; cerca per concetto, non per parola; non
fermarti alla prima corrispondenza. Poi i tre test: implicazione bidirezionale, confronto di
portata, dimostra/menziona/assume.

## Output — contratto rigido

Scrivi **solo** questo JSON, esattamente 7 chiavi, in `lavoro/estratti/<sezione>__<id_fonte>.json`:

```json
{
  "sezione": "2.1",
  "id_fonte": "acme_chi_siamo",
  "esito": "usabile | da riformulare | non usabile | non verificabile",
  "cosa_dice_davvero": "…",
  "citazione_verbatim": "…",
  "posizione": "…",
  "note": "…"
}
```

| esito | significato | conseguenza |
|---|---|---|
| `usabile` | la pagina regge il claim come formulato | la frase resta |
| `da riformulare` | la pagina dice qualcosa di adiacente | la frase si restringe a `cosa_dice_davvero` |
| `non usabile` | la pagina non lo sostiene o lo contraddice | decide il gruppo |
| `non verificabile` | non c'è base sufficiente | decide il gruppo |

- **`cosa_dice_davvero`** — 2-5 frasi, nella lingua del lavoro: cosa la pagina afferma davvero su
  quel punto. Se `non verificabile`, almeno 200 caratteri su cosa hai letto e cercato.
- **`citazione_verbatim`** — UN SOLO passaggio contiguo, copiato parola per parola dal testo
  congelato, almeno 25 caratteri, quello su cui si fonda il giudizio. Mai da cookie banner, menu,
  footer, note legali, newsletter.
- **`posizione`** — il titolo della sezione della pagina sotto cui sta il passaggio, copiato
  com'è; stringa vuota se non c'è.
- **`note`** — casi limite, attribuzione incerta, sotto-affermazione decisiva, avvertenze.

## Regole — la violazione invalida l'output

1. **Niente `usabile`/`da riformulare` senza citazione ritrovabile.** Prima di rispondere, cerca la
   tua citazione nel file e verifica che ci sia, carattere per carattere. Mai concatenare due punti.
2. **Fonte autoreferenziale (`tipo_fonte` = `sito dell'oggetto`).** Il sito di un'azienda prova
   cosa l'azienda **dichiara** di sé, non che sia vero. Un claim formulato come fatto («X è leader
   del mercato», «X riduce i costi del 30%») ha esito massimo `da riformulare`, verso la forma «X
   dichiara che…». `usabile` solo se il claim è già formulato come dichiarazione, e allora `note`
   deve iniziare con `AUTODICHIARAZIONE:`.
3. **Pagine non accademiche** (stampa, blog, report): un claim formulato come risultato acquisito
   («la ricerca dimostra») ha esito massimo `da riformulare`.
4. **Divieto di conoscenza pregressa.** Vale solo il testo congelato. Non aprire il sito dal vivo,
   non usare quello che ricordi dell'azienda.
5. **I numeri non si parafrasano**: stessa cifra, stessa unità, stesso arrotondamento, e se la
   pagina dice l'anno di riferimento del dato va riportato.
6. **Divieto di ammorbidire un giudizio negativo.**
7. **Attribuzione incerta.** Se la frase resterebbe vera anche se la pagina non esistesse, è una
   sintesi del gruppo: `note` inizia con `ATTRIBUZIONE INCERTA:` ed esito fra `da riformulare` e
   `non usabile`, mai `usabile`.
8. **Claim composto**: il minimo dei verdetti, e in `note` quale sotto-affermazione ha deciso.
9. **Contraddizione ≠ silenzio.** Se la pagina dice l'opposto: `non usabile`, citazione obbligatoria,
   `cosa_dice_davvero` inizia con `Contraddice il claim:`.
10. **Nel dubbio fra due esiti adiacenti, il più conservativo.**
11. **Non attribuire alla pagina ciò che riporta di altri** («secondo uno studio di…», una citazione
    di un cliente, un comunicato ripreso): è di quell'altro, salvo che la pagina lo faccia proprio.

## Autocontrollo prima di rispondere

La citazione è nel file? È quella su cui si fonda il giudizio? Ogni elemento di `cosa_dice_davvero`
sta nella pagina e non solo nel claim? I numeri sono identici? Se la fonte è il sito dell'oggetto,
hai distinto dichiarazione da fatto?

## Report in chat

Massimo 6 righe: esito, ragione in una frase, difficoltà. Non incollare il JSON.
