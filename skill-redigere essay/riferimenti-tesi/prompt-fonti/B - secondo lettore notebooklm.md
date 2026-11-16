# Prompt B — Il Secondo Lettore: metodologia della query a NotebookLM

## 0. Perché esiste questo passaggio, e cosa lo farebbe fallire

Lo scopo non è ottenere "un'altra opinione" generica sulla fonte: è ottenere una seconda lettura **indipendente** della stessa identica domanda che il Prompt A ha posto al lettore singolo-documento. Il valore diagnostico del confronto dipende interamente da questo: se le due letture concordano su una domanda diversa, la loro concordanza non prova niente; se divergono su una domanda diversa, la divergenza non segnala un problema reale, segnala solo che si è chiesto due cose diverse. Il vincolo "stessa domanda sostanziale" non è una preferenza di stile: è la condizione senza la quale l'intero secondo-lettore diventa rumore invece che segnale. Ogni scelta di formulazione descritta sotto è subordinata a questo vincolo.

Il rischio specifico di NotebookLM rispetto al Prompt A è che NotebookLM lavora su un corpus (il notebook con più fonti caricate), non su un documento isolato: può rispondere pescando contenuto da una fonte diversa da quella che si intende verificare, specialmente quando più fonti del corpus condividono terminologia o argomento (nel corpus ci sono, con ogni probabilità, più fonti sulla stessa area — es. più lavori su asymmetric information, più lavori su absorptive capacity). Una risposta che sembra confermare il claim ma è in realtà costruita su un'altra fonte del notebook è peggio di nessuna risposta: sembra una seconda lettura indipendente ma non lo è.

## 1. Come formulare la domanda perché sia la stessa domanda sostanziale del Prompt A

Il Prompt A verifica: "questo documento, così com'è, implica il claim, con la stessa portata (popolazione/contesto/condizioni) e allo stesso livello di forza (dimostra, non solo menziona o assume)?". La query a NotebookLM deve tradurre esattamente questi tre elementi (implicazione, portata, livello di forza), non semplificarli in una domanda più vaga tipo "cosa dice questa fonte su X?", che è una domanda diversa (esplorativa, non verificativa) e produrrebbe una risposta non comparabile.

Costruire la query attorno a tre componenti fisse, riprese identiche dal materiale già usato per il Prompt A:

1. **Il contesto d'uso** (le frasi verbatim della scaletta della tesi), riportato quasi integralmente nella query, per fissare l'ambito esatto in cui il punto viene impiegato — non un riassunto della propria comprensione del nodo, che introdurrebbe una parafrasi ulteriore e quindi un'altra fonte di scarto rispetto al Prompt A.
2. **Il claim da verificare**, riportato testualmente, non riformulato in forma di domanda generica ("è vero che...", mantenendo la stessa polarità e la stessa portata del claim originale, senza né restringerlo né allargarlo rispetto a come è scritto nell'Excel).
3. **Una richiesta esplicita di risposta verificativa, non esplorativa**: chiedere se il documento sostiene il claim così com'è, chiedere di segnalare esplicitamente se il documento dice qualcosa di più ristretto, più ampio o diverso rispetto al claim, e chiedere una citazione testuale (verbatim, non parafrasata) a sostegno della risposta. Questa è la stessa richiesta di evidenza verbatim imposta al Prompt A: se una delle due letture fornisce un ancoraggio testuale e l'altra no, il confronto è già compromesso.

Non aggiungere alla query elementi che il Prompt A non aveva a disposizione (es. conoscenza di altre fonti del notebook, sintesi comparative fra più fonti): la query a NotebookLM deve restare, nella sostanza, la stessa singola domanda posta a un singolo documento, anche se lo strumento tecnicamente interroga un corpus.

## 2. Come evitare la contaminazione fra fonti

La contaminazione è il rischio principale e va trattata su due livelli, non uno solo: non basta scrivere nella query "rispondi solo sulla base della fonte X", perché è un'istruzione che il modello può disattendere silenziosamente, soprattutto quando un'altra fonte del notebook tratta lo stesso argomento in modo più diretto o più citabile.

- **Livello tecnico (prioritario): restringere le fonti attive.** Prima di interrogare, selezionare/attivare nel notebook solo la fonte da verificare e disattivare (deselezionare) tutte le altre, quando lo strumento offre questa selezione per fonte — NotebookLM è pensato per lavorare sia su un singolo documento sia sull'intero corpus a seconda di quali fonti sono selezionate per la query. Questo è un vincolo strutturale, non solo un'istruzione testuale, e va preferito sempre che sia disponibile: riduce lo spazio in cui la contaminazione può avvenire invece di limitarsi a vietarla a parole.
- **Livello testuale (di rinforzo, mai sostitutivo): istruzione esplicita nella query** di rispondere usando solo il documento indicato, di dichiarare esplicitamente se l'informazione richiesta non è presente in quel documento (invece di completarla attingendo altrove), e di astenersi da qualunque integrazione proveniente da altre fonti del notebook anche se pertinenti all'argomento.
- **Verifica a valle (obbligatoria in ogni caso, anche con la selezione tecnica attiva): controllare la citazione riportata da NotebookLM.** NotebookLM allega alle risposte riferimenti puntuali alle fonti da cui ha tratto il contenuto (citazioni cliccabili che rimandano al passaggio esatto). Prima di accettare la risposta come seconda lettura valida, verificare che la citazione allegata rimandi effettivamente al documento che si sta verificando e non a un titolo diverso, anche se simile per argomento o per autore. Se la risposta cita, anche parzialmente, un'altra fonte del notebook, la risposta va scartata come non valida per questo confronto, non corretta o filtrata a mano: si segnala la contaminazione e, se possibile, si restringe ulteriormente la selezione delle fonti attive e si ripete la query.
- **Caso limite: fonti quasi-duplicate nello stesso notebook** (due paper vicini per argomento, o una working paper e la sua versione pubblicata). In questo caso la sola istruzione testuale è particolarmente inaffidabile: la restrizione tecnica delle fonti attive è l'unica misura su cui affidarsi con sufficiente certezza.

*(Verificato: la capacità di NotebookLM di ancorare le risposte a citazioni puntuali verificabili nelle fonti caricate, e di rispondere su una fonte singola o su più fonti del corpus a seconda della query, è documentata dal produttore e da guide indipendenti — non è un'assunzione di progetto. Fonti: https://iet.ucdavis.edu/aggie-ai/ai-tools/notebooklm , https://academictech.uchicago.edu/2026/04/06/google-notebooklm-an-ai-tool-for-research-and-studying/ . Il giudizio che la selezione tecnica delle fonti sia più affidabile della sola istruzione testuale, e la procedura di verifica a valle sulla citazione, sono scelte progettuali mie, non affermazioni verificate su una fonte esterna.)*

## 3. Come rendere la risposta confrontabile con quella del lettore A

Il confronto fra le due letture lo fa una persona, non un algoritmo: il compito di questo prompt è produrre una risposta che quella persona possa affiancare al giudizio del Prompt A senza dover indovinare cosa NotebookLM intendesse. Per questo:

- La risposta richiesta deve sempre contenere due componenti distinte e riconoscibili: (i) se il documento sostiene o no il claim così com'è, con eventuale indicazione di dove diverge (portata più stretta/più ampia, condizione aggiuntiva, livello di forza inferiore — le stesse dimensioni di scostamento usate nel Prompt A, cfr. §2 di quel documento); (ii) la citazione verbatim su cui la risposta si fonda, così da poter essere confrontata direttamente con la citazione verbatim prodotta dal Prompt A sullo stesso claim.
- Non chiedere a NotebookLM di restituire direttamente uno dei tre esiti (usabile / da riformulare / non usabile): quel vocabolario e quella scala di giudizio appartengono al framework del Prompt A e non vanno imposti a uno strumento diverso, che potrebbe applicarli in modo inconsistente senza il resto della metodologia (test di implicazione bidirezionale, confronto di portata, distinzione dimostra/menziona/assume) che dà a quei tre esiti il loro significato. Il compito di NotebookLM è produrre una lettura sostantiva comparabile nel contenuto; è la persona, nel confronto, a collocare quella lettura sulla stessa scala usata per il Prompt A.
- Se NotebookLM non trova nulla di pertinente nella fonte selezionata, la risposta corretta attesa è che lo dichiari esplicitamente invece di inventare un contenuto plausibile: una dichiarazione esplicita di assenza è essa stessa un dato comparabile (corrisponde a un possibile "non usabile" del Prompt A), mentre un'invenzione silenziosa non lo è e va trattata come risposta da scartare, non da usare.

## 4. Quando la seconda lettura non è utilizzabile

La query va ripetuta con fonti più ristrette, oppure il risultato va scartato e segnalato come "seconda lettura non disponibile per questa coppia nodo × fonte" (da trattare come dato mancante, mai forzato), quando: la fonte da verificare non è presente come sorgente isolabile nel notebook (es. è stata caricata insieme ad altre in un unico documento aggregato); la risposta cita più fonti contemporaneamente senza che sia possibile isolare quale parte viene dalla fonte di interesse; la risposta non fornisce alcuna citazione verificabile; oppure due tentativi successivi di restringere le fonti attive continuano a produrre citazioni incrociate. In nessuno di questi casi si adatta o si interpreta la risposta per renderla utilizzabile: un dato di confronto dubbio è più dannoso di un dato di confronto assente, perché inquina silenziosamente la lettura di dove "i due lettori concordano".

---

# CONTRATTO DI OUTPUT — non derogabile

## Cosa ricevi
`nodo`, `id_fonte`, `citazione`, `claim`, `contesto_uso`, e l'identificativo della fonte corrispondente dentro il notebook NotebookLM.

## Regola di isolamento
Prima di interrogare, restringi le fonti attive del notebook alla sola fonte in esame. La restrizione tecnica viene prima dell'istruzione testuale: se non è possibile restringere, dichiaralo e scarta la lettura invece di procedere su un notebook aperto a tutte le fonti.

## Cosa restituisci
UNICAMENTE questo JSON, senza testo attorno:

```
{
  "nodo": "3.1.1",
  "id_fonte": "akerlof1970",
  "lettura": "",
  "citazione_verbatim": "",
  "fonte_citata": "",
  "sufficiente": true | false,
  "note": ""
}
```

`lettura` — in inglese, cosa la fonte dice sul punto del claim. **Non deve contenere nessuno dei quattro esiti** (`usabile`, `da riformulare`, `non usabile`, `non decidibile`): quel vocabolario appartiene solo al primo lettore, e riusarlo qui contaminerebbe il confronto. Descrivi il contenuto, non il verdetto.

`fonte_citata` — a quale sorgente NotebookLM ha ancorato la risposta. Se è diversa dalla fonte in esame, `sufficiente` va a `false`: è contaminazione.

`sufficiente` — `false` quando la fonte non era isolabile, quando la citazione allegata non è verificabile, o quando NotebookLM ha risposto incrociando più sorgenti.

## Confronto con il primo lettore (passo successivo, separato)
Un passo distinto accosta questa `lettura` all'output del lettore A sulla stessa coppia (nodo × fonte) e produce un solo valore per la colonna `Secondo lettore`:

- `conferma` — le due letture dicono sostanzialmente la stessa cosa sul punto del claim
- `contraddice` — divergono nel merito: una sostiene ciò che l'altra nega, o attribuiscono alla fonte contenuti incompatibili
- `non confrontabile` — `sufficiente` era `false`, oppure il lettore A aveva risposto `non decidibile`

Solo `contraddice` accende la riga per la revisione umana. `conferma` su un esito `usabile` è il caso in cui il dato è solido e non richiede nulla.
