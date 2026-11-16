# Prompt A — Lettore di una fonte contro un claim (ESEGUIBILE)

Questo file è il prompt operativo. Unisce il contratto di input/output allo strato metodologico, che sta in `pipeline/prompt/A - lettore fonti.md` e **va letto per intero prima di iniziare**. Se quel file e questo divergono sul formato di output, vince sempre questo file: la sua sezione «CONTRATTO DI OUTPUT» descrive un formato precedente (`non decidibile`, `attribuzione_incerta`, `motivo_rifiuto`) superato dal contratto qui sotto — ignorala.

Un'esecuzione = **una coppia (nodo × fonte)**. Un subagent Sonnet per coppia, in parallelo. Nessun subagent scrive nell'Excel.

---

## INPUT che ricevi

- `nodo` — indice del paragrafo della tesi (es. `3.1.1`)
- `id_fonte` — chiave della fonte (es. `akerlof1970`)
- `citazione` — forma inline, es. `(Akerlof, 1970)`
- `ruolo` — `mattone stretto` oppure `sfondo`
- `peer_reviewed` — `sì` / `no` / `n.d.`
- `claim` — l'affermazione che la tesi attribuisce alla fonte in QUEL nodo, in inglese. Se inizia con `ATTRIBUZIONE INCERTA:`, vedi regola 7.
- `percorso_testo` — il file di testo della fonte, estratto con `pdftotext`: testo semplice, **non markdown**, senza intestazioni gerarchiche. Per la maggior parte delle fonti e' stata usata la modalita' a flusso di lettura, non `-layout`, perche' su documenti a due colonne `-layout` affianca le colonne riga per riga e spezza le frasi. Le uniche "sezioni" riconoscibili sono quelle scritte come testo nel corpo (numerazione romana/araba, titoli in maiuscolo) o le intestazioni di pagina/rivista che pdftotext ripete a ogni pagina.
- `caratteri_testo` — lunghezza del file in caratteri. Determina la strategia di lettura, vedi sotto: la maggior parte delle fonti sta fra 25.000 e 300.000 caratteri, ma almeno una ne supera il milione.

## COMPITO

Stabilire se **quel documento**, così come ti è fornito, sostiene **quel claim**, così come è formulato.

Non stabilire se il claim è vero in assoluto. Non giudicare se la fonte è buona in generale. Non migliorare il claim.

## METODO

Leggi e applica `pipeline/prompt/A - lettore fonti.md`. In sintesi, nell'ordine: mappa il documento prima di cercare; cerca per concetto e non per parola; non fermarti alla prima corrispondenza; controlla sempre la sezione limiti/discussione. Poi applica i tre test — implicazione bidirezionale, confronto di portata, dimostra/menziona/assume.

## LETTURA IN BASE ALLA DIMENSIONE

Guarda `caratteri_testo` prima di aprire il file: leggerlo tutto non è sempre possibile né necessario.

- **Fino a ~60.000 caratteri:** leggi il file per intero.
- **Da ~60.000 a ~300.000:** leggi per intero abstract, introduzione e conclusioni/discussione; per il resto cerca il concetto del claim — sinonimi e perifrasi inclusi, non solo la parola — e leggi per intero solo i blocchi dove trovi un possibile riscontro.
- **Oltre ~300.000 caratteri** (es. `anitecassinform2025`, oltre 1.000.000 di caratteri): leggerlo per intero è materialmente impossibile nel contesto disponibile, non provarci. Genera prima 4-6 varianti terminologiche del concetto del claim (sinonimi, perifrasi, termini tecnici del campo), cercale nel testo, e leggi per intero solo l'intorno di ogni corrispondenza (qualche paragrafo prima e dopo). Se dopo questa ricerca sistematica non emerge nulla di pertinente, l'esito è `non verificabile` per impossibilità materiale di ispezionare l'intero documento — non `non usabile`: non avendo controllato tutto, non puoi escludere che il sostegno esista altrove. In `note` elenca i termini cercati.

## OUTPUT — contratto rigido

Restituisci **esclusivamente** un oggetto JSON con esattamente queste sette chiavi, senza testo prima o dopo:

```json
{
  "nodo": "3.1.1",
  "id_fonte": "akerlof1970",
  "esito": "usabile | da riformulare | non usabile | non verificabile",
  "cosa_dice_davvero": "…",
  "citazione_verbatim": "…",
  "sezione": "…",
  "note": "…"
}
```

**`esito`** — uno solo di questi quattro valori, scritti esattamente così, minuscoli:

| valore | significato | conseguenza in stesura |
|---|---|---|
| `usabile` | la fonte regge il claim come formulato | scrivi la frase come previsto |
| `da riformulare` | la fonte dice qualcosa di adiacente ma non esattamente quello | adatta la frase a `cosa_dice_davvero` |
| `non usabile` | la fonte non sostiene il claim, o lo contraddice | non citarla lì: serve una decisione umana |
| `non verificabile` | non hai una base decisionale sufficiente (vedi regole di rifiuto) | serve una decisione umana |

**`cosa_dice_davvero`** — in inglese, 2-5 frasi, cosa la fonte afferma effettivamente su quel punto. Non la tua interpretazione del claim: il contenuto della fonte. Se l'esito è `non verificabile`, spiega qui perché, indicando cosa hai effettivamente letto o cercato prima di rinunciare — non è un'opzione di default per evitare il lavoro quando il documento è ragionevolmente corto.

**`citazione_verbatim`** — una frase copiata **parola per parola** dal testo fornito, lunga almeno 25 caratteri (sotto questa soglia lo script scrittore la scarta comunque). Obbligatoria per `usabile`, `da riformulare` e per `non usabile` quando la fonte contraddice. Stringa vuota solo se l'esito è `non verificabile` o se la fonte semplicemente tace sul punto. Deve essere la frase specifica su cui si fonda `cosa_dice_davvero`, non una frase qualunque scelta solo perché facile da ritrovare (una riga dei ringraziamenti, il titolo, una frase generica dell'abstract): una citazione presente nel testo ma estranea al giudizio rende l'output vuoto anche se supera la validazione automatica. Lo script normalizza spazi, virgolette e trattini di fine riga prima del confronto — non serve preoccuparsi di questi dettagli tipografici, ma le parole devono essere quelle esatte, mai una parafrasi.

**`sezione`** — un riferimento di posizione nel testo continuo, non un'intestazione markdown: non esiste (vedi `percorso_testo` sopra). In ordine di preferenza: (1) il titolo di sezione se compare testualmente nel corpo, copiato esattamente com'è, refusi OCR compresi (es. `III. Examples and applications`, `4. Discussion`); (2) se manca ma il documento ripete un'intestazione di pagina/rivista a ogni pagina, riporta quella stringa così com'è (es. `492 QUARTERLY JOURNAL OF ECONOMICS`) — è comunque un ancoraggio migliore di niente; (3) stringa vuota se non esiste nessuna delle due. Non inventare mai un titolo che non compare testualmente, e non è mai un numero di pagina isolato.

**`note`** — in italiano. Qui vanno: il caso limite applicato se ce n'è uno, l'eventuale attribuzione incerta, la sotto-affermazione che ha determinato il verdetto su un claim composto, ogni avvertenza per chi scriverà.

## REGOLE MECCANICHE — la violazione invalida l'output

1. **Nessun `usabile` o `da riformulare` senza `citazione_verbatim` ritrovabile** nel testo con un match esatto (soglia minima 25 caratteri, vedi sopra). Prima di rispondere, ricerca la tua stessa citazione nel testo fornito e verifica che ci sia, carattere per carattere. **Deve essere UN SOLO passaggio contiguo del file.** Non concatenare due frasi prese da punti diversi del documento, nemmeno se insieme illustrano meglio il punto: il risultato e' una stringa che nel sorgente non esiste, e viene scartata. Se ti servirebbero due passaggi, scegli quello piu' portante per il giudizio e menziona l'altro a parole in `cosa_dice_davvero`. Attenzione anche ai salti di pagina e alle intestazioni ripetute: interrompono la contiguita' anche quando visivamente il testo sembra continuo.
2. **Se `peer_reviewed` è `no`, l'esito massimo è `da riformulare`** quando il claim è formulato come risultato acquisito. Un working paper, un report di settore o un articolo di rivista manageriale non sostengono una frase del tipo "la ricerca dimostra".
3. **Se disponi solo dell'abstract**, l'esito massimo è `da riformulare`. Mai `usabile`.
4. **Divieto di usare conoscenza pregressa del paper.** Molte di queste fonti sono celebri e il modello crede di ricordarle. Vale solo il testo fornito in questa chiamata. Se il ricordo contraddice il testo, vince il testo; se il testo non basta, l'esito è `non verificabile`.
5. **I numeri non si parafrasano.** Ogni valore numerico va riportato esattamente come appare: stessa cifra, stessa unità, stesso arrotondamento.
6. **Divieto di ammorbidire un giudizio negativo.** Non spostare l'esito verso l'alto perché la fonte "dovrebbe" funzionare, essendo già nell'Excel.
7. **Divieto di attribuire alla fonte una sintesi dello studente.** Test: la frase resterebbe vera e sensata anche se questa fonte non fosse mai esistita? Se sì, la tua `note` deve **iniziare esattamente con** `ATTRIBUZIONE INCERTA:` (stringa fissa, così resta cercabile nel foglio), e scegli fra `da riformulare` (la fonte fornisce comunque un ingrediente riusabile) e `non usabile` (non fornisce nulla). Se il `claim` che ricevi **inizia già** con `ATTRIBUZIONE INCERTA:`, un passaggio precedente ha già segnalato questo sospetto: il testo dopo i due punti è una nota di contesto, non il claim da valutare, e la frase fra virgolette al suo interno è la formulazione su cui applicare i test. Non limitarti a confermare il sospetto già scritto: applica comunque tu i tre test del metodo su quella frase, e motiva con parole tue la scelta fra `da riformulare` e `non usabile`. In questo caso l'esito non può mai essere `usabile`, e la `note` deve comunque iniziare con `ATTRIBUZIONE INCERTA:`.
11. **Non attribuire alla fonte la posizione di un'opera che la fonte stessa cita.** Se il passaggio dice «X et al. osservano che…», «secondo Y…», «Z sostiene che…», l'idea è di X, Y o Z dentro quella rassegna della letteratura, non della fonte che stai valutando — non usarla come `cosa_dice_davvero` a meno che la fonte non la faccia esplicitamente propria (endorsement chiaro, non semplice rassegna).
8. **Claim composto:** valuta ogni sotto-affermazione e assegna **il minimo** dei verdetti, mai il massimo. In `note` indica quale sotto-affermazione ha deciso. Se il claim dichiara la citazione congiunta con altre fonti e non assegna le clausole (formule tipo «cited jointly with X, Y; the paragraph does not indicate which source supports which clause»), valuta la quota che QUESTA fonte può sostenere e dichiara in `note` quali clausole restano scoperte: non declassare la fonte per clausole che spettano a un'altra.
9. **Contraddizione ≠ silenzio.** Se la fonte afferma l'opposto, l'esito è `non usabile`, la `citazione_verbatim` col passaggio che contraddice è obbligatoria (non è ammesso lasciarla vuota come nel caso di semplice silenzio), e `cosa_dice_davvero` deve iniziare con `Contradicts the claim:` seguito dalla spiegazione — mai una formulazione neutra che lascia solo intuire che la fonte tace.
10. **In caso di dubbio interpretativo fra due esiti adiacenti, scegli il più conservativo.** Fra `usabile` e `da riformulare` scegli il secondo; fra `da riformulare` e `non usabile` scegli il secondo. Il costo di un falso positivo stampato in tesi è più alto di quello di un falso negativo che un umano recupera.

## AUTOCONTROLLO PRIMA DI RISPONDERE

Le regole 2, 3, 4 e 5 sono facili da violare senza lasciare traccia: nessuno script le controlla dopo di te. Prima di emettere il JSON, passa in rassegna:

1. La `citazione_verbatim` è nel testo fornito, parola per parola (regola 1).
2. Se `peer_reviewed` è `no` e il claim è formulato come risultato acquisito, l'esito non è `usabile` — e se hai applicato il tetto, lo dici in `note` (regola 2).
3. Se disponi solo dell'abstract, l'esito non è `usabile` — e se hai applicato il tetto, lo dici in `note` (regola 3).
4. `cosa_dice_davvero` riporta quello che il testo dice, non quello che ricordi del paper (regola 4).
5. Ogni numero che hai riportato compare nel testo con la stessa cifra e la stessa unità (regola 5).
6. La citazione scelta è quella su cui si fonda `cosa_dice_davvero`, non la più facile da ritrovare (titolo, ringraziamenti, affiliazioni, finanziamenti): se il giudizio resterebbe identico anche cancellandola, è la citazione sbagliata.
7. Ogni elemento sostanziale di `cosa_dice_davvero` (soggetti, oggetti, conseguenze specifiche) compare davvero nella fonte, non solo nel `claim`: parafrasare il claim spacciandolo per contenuto della fonte è la violazione più difficile da notare, perché sembra un output regolare.
8. Se il passaggio attribuisce l'idea a un'altra opera citata al suo interno, non l'hai scritta in `cosa_dice_davvero` come posizione della fonte in esame (regola 11).
9. Il verbo che useresti per descrivere cosa fa la fonte è "dimostra", non "menziona" o "cita di sfuggita": se è menziona, l'esito massimo è `da riformulare`.

## DOVE FINISCE IL TUO OUTPUT

Scrivi il JSON in `estrazioni/estratti/<nodo>__<id_fonte>.json` (es. `estrazioni/estratti/3.1.1__akerlof1970.json`).
**Non aprire l'Excel. Non scriverci.** Il riversamento nel foglio `Estratti` lo fa un unico processo scrittore, alla fine, leggendo questi file.

## MAPPATURA SUL FOGLIO `Estratti`

Per riferimento, lo scrittore finale mapperà così:

| chiave JSON | colonna |
|---|---|
| `esito` | H — Esito |
| `cosa_dice_davvero` | I — Cosa dice davvero |
| `citazione_verbatim` | J — Citazione verbatim |
| `sezione` | K — Sezione |
| `note` | N — Note |

Le colonne A-G sono già compilate e non si toccano. La colonna L (Esito NotebookLM) è del secondo lettore. La colonna M è una formula.
