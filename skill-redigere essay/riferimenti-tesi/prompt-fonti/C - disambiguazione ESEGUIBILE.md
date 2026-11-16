# Prompt C — Disambiguazione di un riferimento (ESEGUIBILE)

Si usa nel loop di recupero, quando la ricerca bibliografica restituisce due o tre candidati vicini per lo stesso `(Autore, anno)` e lo scoring deterministico non ha un vincitore netto.

Strato metodologico completo in `pipeline/prompt/C - disambiguazione candidati.md`. Se quel file e questo divergono sul formato di output, vince sempre questo file: la sua sezione «CONTRATTO DI OUTPUT» descrive un formato precedente (`scelta_doi`/`confidenza`/`escalation`/`candidati_per_la_persona`) superato dal contratto qui sotto (`decisione`/`doi_scelto`/`motivazione`/`candidati_presentati`) — ignorala.

---

## INPUT

- `id_fonte`, `citazione`, `autori_raw`, `anno`
- `contesto_uso` — le frasi inglesi verbatim della scaletta in cui la fonte compare
- `claim` — l'affermazione che la tesi le attribuisce
- `candidati` — 2 o 3 record con titolo, autori, anno, sede, DOI, abstract, punteggio

## PESO DEI SEGNALI, in ordine decrescente

1. **Compatibilità semantica fra abstract del candidato e `contesto_uso` + `claim`** — decisivo. È l'unico segnale che distingue davvero due paper dello stesso autore e anno.
2. **Cognome del primo autore** — necessario ma non sufficiente: filtro, non punteggio.
3. **Anno**, con tolleranza ±1 per lo scarto fra preprint e pubblicazione.
4. **Sede di pubblicazione** — supporto: coerenza con il campo disciplinare del nodo.
5. **Conteggio citazioni** — solo spareggio fra candidati altrimenti pari. Mai decisivo da solo.

## SOGLIA DI ESCALATION — quando NON scegli

Passa la mano alla persona, senza scegliere, se anche solo una di queste condizioni si verifica:

- nessun candidato domina: due sono semanticamente compatibili in modo comparabile
- ambiguità autore + anno identici fra candidati che trattano temi diversi
- l'abstract manca su uno o più candidati competitivi
- l'unico discriminante rimasto è la sede o il conteggio citazioni
- la decisione richiederebbe di leggere il full text
- sospetto che il riferimento di partenza sia errato o inesistente

**Meglio dieci domande allo studente che una fonte sbagliata scritta nell'Excel.** Una fonte sbagliata accettata in automatico si propaga silenziosamente fino alla bibliografia.

## OUTPUT — contratto rigido

```json
{
  "id_fonte": "agrawal2018",
  "decisione": "scelto | escalation | nessun candidato valido",
  "doi_scelto": "10.3386/w24243",
  "motivazione": "…",
  "candidati_presentati": [
    {"doi": "…", "titolo": "…", "anno": 2018, "sede": "…", "perche_si": "…", "perche_no": "…"}
  ]
}
```

- `decisione: "scelto"` → `doi_scelto` valorizzato, `motivazione` spiega quale elemento del `contesto_uso` ha deciso.
- `decisione: "escalation"` → `doi_scelto` vuoto, e `candidati_presentati` contiene i candidati **con i pro e i contro di ciascuno**, non un rifiuto vuoto: la persona deve poter decidere in trenta secondi guardando quel campo.
- `decisione: "nessun candidato valido"` → tutti scartati dal filtro autore, oppure sospetto che il riferimento non esista. In `motivazione` scrivi dove hai cercato.

## REGOLE MECCANICHE

1. **Nessun dato bibliografico inventato.** Titolo, DOI, sede e anno devono provenire dai `candidati` che ti sono stati passati. Non aggiungere candidati da conoscenza pregressa: se pensi che il paper giusto non sia in lista, è `escalation` con la motivazione.
2. **La motivazione deve citare l'elemento del `contesto_uso` che ha deciso.** "Sembra più pertinente" non è una motivazione: "il nodo 1.1.1 parla di commesse temporanee e uniche, che è il tema del candidato 1 e non del candidato 2" lo è.
3. **Se il candidato migliore è un preprint e ne esiste la versione pubblicata fra i candidati, scegli quella pubblicata.**
4. **Attenzione alle traduzioni e alle riedizioni.** Un candidato con lo stesso titolo ma lingua o anno diversi dall'originale è quasi sempre l'edizione sbagliata. È già successo con NIST 2023, dove il primo candidato era la traduzione giapponese del 2024.
5. **Un riferimento che nessuna banca dati trova non va "sistemato" scegliendo il più somigliante.** Va marcato `nessun candidato valido`. Nella bibliografia di questa tesi due riferimenti sono risultati inesistenti: sono stati trovati perché nessuno ha forzato una scelta.
