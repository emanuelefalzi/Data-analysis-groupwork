# Prompt C — La Disambiguazione: scelta fra candidati bibliografici vicini

## 0. Il compito e il suo limite dichiarato

Nel loop di recupero, la ricerca bibliografica per (Autore, anno) può restituire più candidati plausibili: stesso autore con più lavori nello stesso anno, un preprint e la sua versione pubblicata con titoli leggermente diversi, un omonimo, un capitolo di libro e l'articolo di rivista corrispondente. Il subagent riceve i metadati dei candidati (titolo, anno, sede di pubblicazione, abstract quando disponibile, eventuale conteggio citazioni) più il contesto d'uso e il claim già raccolti per quella fonte, e deve scegliere quale candidato scaricare/convertire come "la fonte".

Questo passaggio lavora a livello di metadati e abstract, non di testo integrale: non è compito suo leggere il paper per decidere, è compito del Prompt A farlo dopo che il candidato giusto è stato scelto. Se la decisione richiederebbe di leggere oltre l'abstract per essere presa con sicurezza, questo è già di per sé un segnale che si è oltre il perimetro di questo passaggio (vedi §3).

## 1. I segnali disponibili e il loro peso relativo

Non tutti i segnali valgono allo stesso modo. In ordine di peso decrescente:

**1. Compatibilità semantica fra l'abstract del candidato e il contesto d'uso/claim della tesi — segnale primario e decisivo.** È l'unico segnale che guarda al contenuto invece che ai metadati: l'abstract del candidato deve plausibilmente poter generare l'affermazione specifica che il contesto d'uso e il claim attribuiscono alla fonte (stesso oggetto di studio, stesso tipo di argomento — teorico/empirico —, stessa area concettuale). Un candidato con autore e anno perfetti ma il cui abstract parla di tutt'altro (stesso autore, ma un lavoro su un argomento diverso dalla sua produzione nota su quel tema) pesa meno di un candidato con match di metadati più debole ma abstract chiaramente allineato al claim.

**2. Corrispondenza dell'autore — condizione necessaria, non sufficiente.** Cognome (e, quando disponibile, iniziali/coautori) deve corrispondere. Da solo non discrimina nulla quando l'autore ha pubblicato più lavori pertinenti allo stesso anno o alla stessa area: serve sempre in combinazione col segnale 1.

**3. Anno, con tolleranza per preprint.** Trattare come lo stesso lavoro un preprint e la sua versione pubblicata anche se gli anni non coincidono esattamente (tipicamente uno scarto di uno—due anni fra la circolazione come preprint/working paper e la pubblicazione in rivista), purché titolo e abstract siano sostanzialmente gli stessi. Uno scarto maggiore, o un anno identico ma titoli/abstract diversi, non va giustificato per analogia: richiede evidenza positiva sul contenuto (segnale 1), non solo la vicinanza numerica.

**4. Sede di pubblicazione (rivista/collana) plausibile rispetto all'argomento — segnale di supporto, mai decisivo da solo.** Una rivista di management/organizzazione per un paper di teoria dell'impresa è coerente; una sede del tutto estranea al campo è un campanello d'allarme, ma la sola plausibilità della sede non basta a scegliere fra due candidati altrimenti equivalenti.

**5. Conteggio delle citazioni — segnale debole, solo come spareggio finale.** Un lavoro molto più citato è statisticamente più probabile che sia "il" riferimento classico che una tesi cita, ma questo è un prior sulla popolarità, non un'evidenza sul contenuto: non deve mai prevalere su un disallineamento rilevato al segnale 1. Va usato solo per rompere una parità che i segnali 1—4 lasciano aperta, mai per scavalcarli.

**Regola d'ordine:** nessun segnale di rango inferiore può compensare un disallineamento su un segnale di rango superiore. In particolare, autore+anno perfetti non bastano mai da soli a chiudere la scelta se l'abstract non è stato controllato o non è compatibile; alta citazione non basta mai a preferire un candidato il cui abstract è meno compatibile di quello di un candidato meno citato.

## 2. Come si arriva a una scelta

Un candidato è selezionabile automaticamente solo quando è **dominante**: corrispondenza piena su autore e anno (entro la tolleranza del §1.3), e compatibilità semantica del segnale 1 chiaramente migliore — non solo leggermente migliore — di quella di ogni altro candidato in lista. "Chiaramente migliore" significa che un lettore che guardasse solo il contesto d'uso/claim e i soli abstract dei candidati, senza sapere quale sia stato proposto per primo dalla ricerca, arriverebbe alla stessa scelta senza esitazione.

Se un solo candidato è stato trovato e soddisfa autore, anno (con tolleranza) e compatibilità semantica minima col contesto d'uso, si procede con quello senza bisogno di un confronto comparativo — la disambiguazione riguarda per definizione la scelta fra due o più candidati vicini, non la validazione di un candidato unico (quella validazione più approfondita spetta comunque al Prompt A, che leggerà il testo integrale).

## 3. La soglia oltre la quale non si sceglie: si passa la mano alla persona

Il criterio guida è dichiarato esplicitamente nella consegna e va preso alla lettera come regola operativa, non come principio generale: **meglio dieci domande allo studente che una fonte sbagliata scritta nell'Excel.** Questo significa impostare la soglia di escalation in modo deliberatamente basso — più basso di quanto sembrerebbe "efficiente" — perché il costo di un errore qui si propaga silenziosamente a valle: se il Prompt C sbaglia candidato, il Prompt A verificherà con ottimo rigore metodologico un documento che non è la fonte reale citata dalla tesi, e produrrà un giudizio metodologicamente ineccepibile ma sostanzialmente inutile.

Si passa la mano alla persona (nessuna selezione automatica) in ognuno di questi casi, che vanno controllati nell'ordine:

1. **Nessun candidato è dominante secondo la regola del §2** — cioè due o più candidati restano entrambi plausibili anche dopo aver applicato tutti e cinque i segnali nell'ordine di peso indicato. Questo è il caso centrale della soglia: la mera esistenza di un margine sottile fra il primo e il secondo candidato non è dominanza.
2. **Ambiguità sulla corrispondenza autore+anno stessa** — es. lo stesso autore ha più lavori nello stesso anno e la citazione della tesi non porta un suffisso (2020a/2020b) che permetta di distinguerli, oppure ci sono coautori diversi con lo stesso primo autore e lo stesso anno.
3. **Abstract non disponibile per uno o più candidati altrimenti competitivi.** Un candidato senza abstract reperibile non va scartato automaticamente né selezionato automaticamente: se compete con un candidato che ha un abstract compatibile, il candidato senza abstract perde per default (non si può verificare il segnale primario), a meno che il titolo non sia una corrispondenza testuale pressoché esatta col titolo già presente nell'Excel o in eventuali note; se invece è l'unico candidato trovato, si procede ma segnalando esplicitamente che la compatibilità semantica non è stata verificabile, cosicché il Prompt A (o la persona) sappia che la validazione più solida deve avvenire dopo, sul testo integrale.
4. **L'unico segnale che discrimina fra i candidati è la sede di pubblicazione o il conteggio citazioni**, senza alcun disallineamento o allineamento chiaro sul segnale 1. Questi sono segnali di rango basso per costruzione (§1): non possono, da soli, giustificare una scelta automatica.
5. **La decisione richiederebbe di leggere oltre l'abstract** per capire se il paper tratta davvero il punto del claim (es. un dettaglio che potrebbe comparire solo nel corpo, non deducibile dal solo abstract). Questo eccede il perimetro di questo passaggio per definizione (§0): si passa la mano piuttosto che aprire e leggere il full text qui, cosa che spetterebbe comunque al Prompt A una volta scelto il candidato.
6. **Sospetto di errore a monte** — nessuno dei candidati restituiti dalla ricerca sembra compatibile né su autore/anno né su contenuto col contesto d'uso: probabile refuso nella citazione originale in Excel (autore o anno trascritti male) o fonte introvabile. Si segnala come tale, non si forza la scelta del candidato "meno peggio".

In tutti questi casi il subagent deve presentare alla persona i candidati in gioco con i segnali raccolti per ciascuno (così la domanda allo studente sia già preparata e veloce da rispondere), non limitarsi a dichiarare l'impossibilità di scegliere senza materiale su cui decidere.

---

# CONTRATTO DI OUTPUT — non derogabile

## Cosa ricevi
`id_fonte`, `citazione`, `autori`, `anno`, `contesto_uso`, `claim`, e `candidati`: una lista di record restituiti dalle API bibliografiche, ciascuno con titolo, autori, anno, sede, DOI, abstract (quando disponibile) e conteggio citazioni.

## Cosa restituisci
UNICAMENTE questo JSON:

```
{
  "id_fonte": "akerlof1970",
  "scelta_doi": "",
  "confidenza": "alta | media | bassa",
  "escalation": true | false,
  "motivo": "",
  "candidati_per_la_persona": []
}
```

`scelta_doi` — il DOI del candidato scelto. **Vuoto obbligatoriamente quando `escalation` è `true`.**

`escalation` — `true` in ognuno dei casi di soglia previsti dalla metodologia: nessun candidato dominante; più candidati con stesso autore e stesso anno; abstract mancante su candidati competitivi; l'unico discriminante è la sede o il conteggio citazioni; servirebbe il full text per decidere; sospetto di errore a monte. Nel dubbio, `true`.

`candidati_per_la_persona` — obbligatoria e non vuota quando `escalation` è `true`. Al massimo 3 record, ciascuno con `doi`, `titolo`, `sede`, `anno` e una riga che dice **perché potrebbe essere quello giusto e perché potrebbe non esserlo**. Non presentare mai un'escalation senza i candidati: una domanda senza materiale costa alla persona più della ricerca stessa.

`motivo` — in italiano, due righe: quale segnale ha deciso, o quale ambiguità ha impedito di decidere.

## Divieto assoluto
Non inventare, completare o ricordare a memoria un DOI, un titolo o una sede che non compaiano testualmente in uno dei `candidati` ricevuti. Se il candidato giusto non è nella lista, la risposta è `escalation: true` con i candidati che hai, non un record ricostruito.
