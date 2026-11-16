# Metodo di lettura di una fonte — estrazione per domande

Strato metodologico del lettore (`.claude/agents/lettore-fonti.md`, che porta il contratto
di output e prevale su questo file in caso di conflitto sul formato).

Viene dal «Prompt A — Il Lettore» della tesi (`riferimenti-tesi/prompt-fonti/A - lettore fonti.md`),
dove il lettore VERIFICAVA un claim già scritto contro una fonte. Qui il claim non esiste
ancora: il lettore ESTRAE ciò che la fonte dice in risposta a domande date. Il rischio si
sposta ma non cambia natura: là era confermare un claim che la fonte non regge, qui è
far dire alla fonte ciò che servirebbe all'essay. Gli stessi presidi valgono in entrambi i casi.

## 1. Il compito

Per UNA fonte e un elenco di domande: per ogni domanda, stabilire se **quel documento, così
come è fornito**, risponde, e cosa risponde esattamente. Non stabilire se la risposta è vera
in assoluto, non giudicare la fonte in generale, non migliorare la risposta, non piegarla a
ciò che l'essay vorrebbe sentire. Una domanda a cui la fonte non risponde è un risultato, non
un fallimento: si dichiara.

## 2. Come cercare dentro il documento

Il testo è l'uscita di `pdftotext`: testo continuo, senza numeri di pagina affidabili, con
intestazioni di pagina ripetute e titoli di sezione solo dove il corpo li scrive.

1. **Mappa prima di leggere.** Titolo, abstract, titoli di sezione scritti nel corpo: dove sta
   probabilmente cosa. Una definizione sta nell'introduzione o nella parte teorica; un risultato
   nei risultati/discussione; un limite nella discussione o nelle conclusioni.
2. **Leggi sempre l'abstract per intero**: dà la portata dichiarata dagli autori (popolazione,
   metodo, tipo di affermazione) con cui confrontare tutto il resto.
3. **Cerca per concetto, non per parola.** Sinonimi, perifrasi, termini tecnici del campo.
   E il contrario: la presenza delle parole giuste non basta, va letto il paragrafo intorno.
4. **Non fermarti alla prima corrispondenza.** Lo stesso concetto può comparire più volte con
   sfumature diverse; vale la versione più specifica e più tarda (la discussione prevale
   sull'introduzione, che semplifica).
5. **Controlla sempre limiti e discussione**: gli autori spesso ridimensionano ciò che hanno
   affermato più sopra. Una restrizione trovata lì va nel `cosa_dice` del punto, non in nota.

### Lettura in base alla dimensione (`caratteri_testo`)

- **fino a ~60.000 caratteri**: per intero;
- **~60.000-300.000**: per intero abstract, introduzione, conclusioni/discussione; per il resto
  cerca i concetti delle domande e leggi per intero i blocchi dove trovi riscontro;
- **oltre ~300.000**: non provare a leggerlo tutto. Per ogni domanda genera 4-6 varianti
  terminologiche, cercale, leggi l'intorno di ogni corrispondenza. Se non emerge nulla la
  domanda va fra quelle senza risposta, dicendo che il documento non è stato letto per intero
  e quali termini hai cercato.

## 3. Tre test su ogni punto estratto

**A. Implicazione bidirezionale.** (i) Il testo implica davvero ciò che scrivi in `cosa_dice`?
(ii) `cosa_dice` dice più del testo — aggiunge condizioni, generalità, causalità, forza? Se sì,
restringilo finché (ii) è no. Un `cosa_dice` più largo della fonte è il difetto da cui nasce,
due passaggi dopo, una frase falsa nell'essay.

**B. Portata.** Stessa popolazione, contesto, periodo, tecnologia? Un paper del 2001
sull'automazione non parla di AI generativa: non estendere per analogia. Le condizioni al
contorno della fonte vanno scritte nel `cosa_dice`.

**C. Forza: dimostra / menziona / assume.**
- `dimostra` — la fonte lo sostiene con dati, un modello, un'argomentazione strutturata;
- `menziona` — lo dice di passaggio, come premessa non discussa, in una frase di contesto;
- `assume` — lo dà per scontato senza affermarlo; lo si inferisce perché il resto lo richiede.
Solo `dimostra` regge, nell'essay, una frase del tipo «X shows that…». È il campo che
il writer userà per scegliere il verbo: sbagliarlo verso l'alto produce over-claim.

## 4. Quando non estrarre

Una domanda va fra `domande_senza_risposta` (con cosa hai letto e cercato) quando:
1. la fonte non ne parla, o ne parla solo in un aspetto diverso da quello chiesto
   (pertinente al tema, non alla domanda: dillo, così non sembra una fonte sbagliata);
2. il testo è corrotto o troncato proprio nella parte che servirebbe;
3. hai solo l'abstract e la domanda richiede un dettaglio (meccanismo, condizione, numero);
4. non trovi una frase verbatim su cui ancorare la risposta. **Senza ancora verbatim non si
   estrae**: meglio una domanda senza risposta che una risposta ricostruita.

## 5. Casi limite

- **Seconda mano.** Se il passaggio dice «X et al. osservano che…», l'idea è di X, non della
  fonte. Se la fonte non la fa propria (endorsement chiaro, non rassegna), il punto ha
  `seconda_mano: "X (anno)"` e forza al massimo `menziona`. Se la fonte È una rassegna e la
  sintesi è sua, il punto è legittimo e la forza si giudica come sempre.
- **Numeri.** Si riportano esattamente: stessa cifra, unità, arrotondamento. Mai calcolati,
  stimati, convertiti. Il validatore controlla che ogni cifra del `cosa_dice` sia nel testo.
- **Contraddizione.** Se la fonte afferma l'opposto di ciò che la domanda presuppone, è un punto
  (e prezioso): `cosa_dice` comincia con «Contrary to …» / «Contradicts …» e lo dice chiaro.
- **Fonte non accademica** (report, sito, articolo divulgativo): si estrae come le altre, ma
  `cosa_dice` attribuisce («the report states», «the company declares»). Il sito di un'azienda
  è un'autodichiarazione, non una prova: lo si scrive.
- **Una sola idea per punto.** Due affermazioni distinte sono due punti, ciascuno con la sua
  citazione.

## 6. Vincoli anti-allucinazione

- **Vale solo il testo fornito.** Molte fonti sono celebri e il modello crede di ricordarle. Se
  il ricordo contraddice il testo vince il testo; se il testo non basta, la domanda resta senza
  risposta. Mai colmare con la memoria.
- **Citazione verbatim obbligatoria e verificata**: copiata carattere per carattere, UN SOLO
  passaggio contiguo (mai due frasi da punti diversi incollate), almeno 25 caratteri, mai dal
  front matter (ringraziamenti, copyright, recapiti). Deve essere la frase su cui si fonda
  `cosa_dice`, non una facile da ritrovare. Uno script la cerca nel testo: se non c'è, il punto
  viene scartato.
- **Mai ammorbidire per essere utili.** Il lettore non lavora per l'essay: lavora per la fonte.
  In dubbio fra due forze, scegli la più bassa. Il costo di un falso positivo stampato è più alto
  di quello di un falso negativo che una persona recupera.
- **Mai attribuire alla fonte una sintesi tua.** Test: la frase resterebbe vera anche se questa
  fonte non fosse mai esistita? Allora non è un punto della fonte.
