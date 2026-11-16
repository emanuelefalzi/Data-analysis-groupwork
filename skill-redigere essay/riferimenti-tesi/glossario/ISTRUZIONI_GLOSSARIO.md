# Istruzioni per il REDATTORE del glossario

BASE = /Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/
NON fare `cd` in quella cartella: rompe gli import di Python. Percorsi assoluti da un'altra cwd.

## Perché esiste questo glossario

Una tesi di laurea in economia/management verrà scritta da più agenti, capitolo per capitolo. La tesi costruisce **scale di concetti vicini che NON sono sinonimi**: per esempio *familiarity* → *domain expertise* (individuale) → *organizational domain capability*. Se un agente scrive "expertise" dove serve "capability", non è un refuso: è l'argomento che salta.

Il glossario non serve a essere letto. Serve a essere **applicato da un linter** che blocca un paragrafo quando usa una variante vietata. Scrivi ogni voce pensando a quello.

## Il tuo input

`glossario/gruppi/<nome_gruppo>.json` contiene, per ogni termine del tuo gruppo:
- `termine`, `n_occorrenze`, `nodi` (gli indici dei paragrafi in cui compare)
- `occorrenze`: fino a 25 passaggi **verbatim** della tesi, con il nodo di provenienza

Il campo `tabella_glossario_cap3` contiene la tabella dei termini fissi che l'autore ha già dichiarato nel capitolo 3: quei significati sono **vincolanti**, non contraddirli.

Puoi anche consultare il foglio `iTOC` di `iTOC master.xlsx` (colonna A indice, B titolo, C descrizione) se ti serve più contesto di un nodo.

## Regole di redazione

1. **La definizione si ricava dal testo della tesi, non da un dizionario.** Deve essere la definizione operativa interna a QUESTO lavoro. Se un manuale definirebbe il termine diversamente, vince la tesi.
2. **Se il termine è usato ma mai definito**, metti `stato: "usato ma non definito"` e lascia `definizione` vuota. È un'informazione preziosa, non un fallimento: segnala un buco da colmare prima della stesura.
3. **`varianti_vietate` è il campo che vale.** Per i termini della scala concettuale elenca i vicini pericolosi con la ragione della distinzione. Se non ci sono varianti confondibili, lista vuota: non inventarne per riempire.
4. **Non irrigidire distinzioni che la tesi non fa.** Se l'autore usa due termini come sinonimi, registralo così, con `sinonimi_accettati`.
5. `nodo_definizione` è il nodo in cui il termine viene introdotto o definito per la prima volta. Serve al linter per bloccare l'uso tecnico prima di quel punto.

## Output

Un JSON in `BASE/glossario/out/<nome_gruppo>.json` (percorso ASSOLUTO, la cartella `glossario/` sta nella radice della tesi):

```json
{
  "gruppo": "1_scala_dominio",
  "voci": [
    {
      "termine": "domain capability",
      "forma_canonica": "domain capability",
      "definizione": "…",
      "nodo_definizione": "3.2.3",
      "nodi_uso": ["3.2.3", "3.2.4"],
      "varianti_vietate": [
        {"forma": "domain expertise", "perche": "è il livello individuale, non organizzativo"}
      ],
      "sinonimi_accettati": [],
      "usabile_prima_del_nodo_definizione": false,
      "stato": "definito",
      "citazione_ancora": "…"
    }
  ],
  "note_gruppo": "…"
}
```

- `stato`: `definito` oppure `usato ma non definito`
- `citazione_ancora`: un passaggio **verbatim** della tesi, copiato da `occorrenze`, che giustifica la definizione. Obbligatorio quando `stato` è `definito`. Deve essere un solo passaggio contiguo.
- `note_gruppo`: quello che hai notato e che serve a chi scriverà — derive terminologiche, incoerenze fra nodi, termini che l'autore usa in due sensi diversi.

## Report
Massimo 8 righe: quanti termini definiti e quanti non definiti, le distinzioni più pericolose che hai trovato, e le eventuali incoerenze nell'uso dell'autore. Non incollare il JSON.
