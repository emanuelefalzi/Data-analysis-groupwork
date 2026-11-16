# Mini-loop Glossario — redazione da zero

**Scopo:** produrre un glossario dei termini vincolanti della tesi, in forma direttamente consumabile dall'orchestratore di stesura.

**Perché serve:** questa tesi costruisce una scala di concetti vicini che NON sono sinonimi — *familiarity* → *domain expertise* (individuale) → *organizational domain capability*. Se un agente scrive "expertise" dove serve "capability", non è un refuso: è l'argomento che salta. Con più sessioni che scrivono capitoli diversi, la deriva terminologica è il rischio numero uno.

**Da zero:** non riusare l'estrazione di `glossario_matrici.json`, che era una prima passata generica. Quella resta come materiale di confronto a valle.

---

## FASE 1 — Candidatura dei termini (deterministica, uno script)

Input: foglio `iTOC`, colonne A (indice), B (titolo), C (descrizione).

Per ogni n-gramma di 1-4 parole nelle descrizioni inglesi, calcolare:
- frequenza assoluta e numero di nodi distinti in cui compare
- se compare in un **titolo** di nodo (segnale forte: è un concetto strutturale)
- se compare in nodi di capitoli diversi (segnale di trasversalità)

Escludere stopword e n-grammi puramente grammaticali. Produrre `glossario/candidati.json` con i termini ordinati per rilevanza.

Aggiungere d'ufficio i termini della tabella glossario del capitolo 3, che sono già dichiarati vincolanti dall'autore.

**Nessun giudizio in questa fase:** è conteggio, e serve a non dimenticare termini che un lettore umano darebbe per scontati.

## FASE 2 — Redazione delle voci (subagent Sonnet in parallelo)

Un subagent per **gruppo di termini imparentati**, non per singolo termine: le distinzioni si scrivono solo vedendo insieme i concetti che rischiano di essere confusi. Esempio di gruppo: `domain knowledge` / `domain expertise` / `domain capability` / `familiarity`.

Ogni subagent riceve i termini del gruppo, e per ciascuno **tutti i passaggi della tesi in cui compare** (nodo + frase). Deve produrre, per ogni termine:

```json
{
  "termine": "domain capability",
  "forma_canonica": "domain capability",
  "definizione": "…",
  "nodo_definizione": "3.2.3",
  "nodi_uso": ["3.2.3", "3.2.4", "4.2.2"],
  "varianti_vietate": [
    {"forma": "domain expertise", "perche": "è il livello individuale, non organizzativo"}
  ],
  "usabile_prima_del_nodo_definizione": false,
  "stato": "definito | usato ma non definito"
}
```

Regole per il subagent:

1. **La definizione si ricava dal testo della tesi, non da un dizionario.** Deve essere la definizione operativa interna a questo lavoro.
2. Se il termine è usato ma mai definito, `stato: "usato ma non definito"` e `definizione` vuota. **È un'informazione preziosa, non un fallimento**: segnala un buco da colmare prima della stesura. Nella prima passata ne erano emersi due, `prediction` e `pattern matching`.
3. **`varianti_vietate` è il campo che vale.** Se non ci sono varianti pericolose la lista è vuota; ma per i termini della scala concettuale deve elencare i vicini con la ragione della distinzione.
4. Non inventare distinzioni che la tesi non fa. Se al capitolo 3 l'autore usa `domain knowledge` e `domain competence` come sinonimi, va registrato così, non irrigidito.

## FASE 3 — Consolidamento (un solo processo)

- Unire i gruppi, risolvere i conflitti (lo stesso termine descritto due volte).
- Rendere **simmetriche** le varianti vietate: se A vieta B, B deve vietare A con la ragione speculare.
- Verificare che ogni `nodo_definizione` preceda tutti i `nodi_uso`. Dove non accade, segnalarlo: significa che il termine è usato prima di essere definito, ed è un problema di struttura da correggere nel Word.
- Scrivere `glossario/glossario.json` e il foglio `Glossario` nell'Excel.

## FASE 4 — Il linter (è questo che lo rende AI-friendly)

Il glossario non serve a essere letto: serve a essere **applicato**. Produrre `glossario/lint.py` con una funzione:

```python
lint(testo: str, nodo: str) -> list[Violazione]
```

che dato un paragrafo generato e il nodo a cui appartiene, restituisce:

- **variante vietata usata** → quale, quale forma canonica usare al suo posto, la ragione
- **termine tecnico usato prima del suo nodo di definizione** → quale, dove è definito
- **termine con `stato: "usato ma non definito"`** → avviso che va definito prima dell'uso

L'orchestratore chiama `lint()` su ogni paragrafo prima di considerarlo chiuso. Una violazione blocca, non avvisa soltanto.

## STRUTTURA DEL FOGLIO `Glossario`

| col | contenuto |
|---|---|
| A | Termine (forma canonica) |
| B | Definizione operativa |
| C | Nodo di definizione |
| D | Nodi d'uso |
| E | Varianti vietate |
| F | Perché sono vietate |
| G | Stato (`definito` / `usato ma non definito`) |
| H | Note |

Stessa grafica degli altri fogli: Arial, intestazione bianca su `1F3864`, wrap, freeze `B2`, griglia nascosta.

## ORDINE E COSTO

Fase 1 è uno script, minuti. Fase 2 sono 5-7 subagent in parallelo. Fase 3 e 4 un processo solo.
Va fatto **prima della stesura ma dopo il loop 2**: la verifica delle fonti può cambiare come un concetto viene definito, e riscrivere il glossario dopo costerebbe più che aspettare.
