# Brief — Agente di controllo bibliografico

**Da lanciare:** subagent Sonnet, memoria fresca (nessun contesto di questa sessione).
**Quando:** deciso dall'utente. NON lanciare senza suo via esplicito.

---

## Contesto minimo da dare all'agente

Tesi di laurea triennale in economia/management, in inglese, ~32 pagine, stile citazionale **APA 7**.

File coinvolti, tutti in `/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/`:

- `tesi.bib` — 50 voci BibTeX, generate dal foglio `Fonti`. Le chiavi corrispondono alla colonna A (ID).
- `iTOC master.xlsx`, foglio `Fonti` — 51 righe. Colonne rilevanti: A ID, B Citazione, C Autori, D Anno, M Titolo, N Tipo, O Sede/editore, P DOI, S PDF locale, T Peer-reviewed, W Note.
- `fonti def/` — 47 PDF, nominati in formato APA 7 (`Autore, I. (Anno). Titolo.pdf`).

## Compito

Verificare che `tesi.bib`, il foglio `Fonti` e i PDF in cartella siano **corretti fra loro e coerenti**, e correggere il `.bib`.

### 1. Coerenza incrociata (fra le tre fonti di verità)

Per ogni voce del `.bib`, controllare che coincidano con il foglio `Fonti` e con il PDF vero:

- autori, anno, titolo, sede di pubblicazione
- il DOI risolve e punta a quel documento (verificare via `https://api.crossref.org/works/{doi}`)
- il PDF in `fonti def/` corrisponde davvero a quella voce (leggere la prima pagina con `pdftotext`)
- il nome del file segue il formato APA e riporta lo **stesso anno** della citazione

Segnalare ogni discrepanza. **Attenzione specifica agli anni:** Crossref restituisce spesso la data di pubblicazione *online*, diversa dall'anno di fascicolo. Ne sono già stati corretti tre a mano (Connelly 2010→2011, Ethiraj 2004→2005, Ennen & Richter 2009→2010). Cercarne altri.

### 2. Completare le voci malformate (priorità alta)

Otto voci sono state costruite senza Crossref e hanno i campi impastati. Vanno riscritte con i campi BibTeX corretti:

`davenport1998`, `ghemawat1991`, `miles1995`, `rumelt1984`, `anitecassinform2025`, `assintel2025`, `chokimkim2026`, `peng2023`

Problemi noti da correggere:
- `rumelt1984`: autore `{Rumelt}` senza iniziale; il `booktitle` contiene prosa italiana ("in R. B. Lamb (a cura di), ..., pp. 556-570") invece dei campi separati `editor`, `booktitle`, `publisher`, `pages`. È un `@incollection`.
- `anitecassinform2025` e `assintel2025`: `howpublished` contiene prosa con edizione e note. Sono `@techreport`: usare `institution`, `type`, `year`, `url`.
- `davenport1998`: `@article`, Harvard Business Review 76(4), 121-131, senza DOI.
- `ghemawat1991`: `@book`, Free Press, New York. ISBN reperibile.
- `peng2023` e `chokimkim2026`: preprint arXiv. Usare `@misc` con `eprint`, `archivePrefix`, `primaryClass`, `url`.

I dati necessari sono nella colonna `W Note` del foglio `Fonti`, dove ogni fonte ha la sua storia di recupero.

### 3. Completare le colonne del foglio Fonti

- `T Peer-reviewed` — 41/51 compilate. Completare secondo questa regola: `sì` per articoli di riviste con revisione paritaria e atti di conferenza referati; `no` per preprint, working paper, report di settore, articoli di rivista manageriale non referata (HBR, California Management Review), libri commerciali; `n.d.` solo se davvero indeterminabile.
- `R Open access` — 42/51. Meno importante, completare dove è banale.
- `N Tipo` e `O Sede/editore` — completare i pochi vuoti.

### 4. Verifica finale

- Nessuna chiave duplicata, parentesi bilanciate, il file si parsa.
- Se `pandoc` è disponibile, provare a generare una bibliografia APA da `tesi.bib` e riportare gli eventuali errori: `pandoc --citeproc --csl apa.csl`. Se manca il CSL, segnalarlo senza bloccarsi.
- Ogni chiave del `.bib` deve esistere come ID nel foglio `Fonti`, e viceversa (eccetto `fukui2026`, vedi sotto).

## Cose da NON fare

- **Non inventare nessun dato bibliografico.** Titoli, DOI, ISBN, numeri di pagina devono venire da una risposta API verificabile o dal PDF stesso. Un campo che non si riesce a reperire resta vuoto e viene segnalato. È la regola centrale di tutto questo lavoro: la bibliografia era stata costruita con l'AI e conteneva riferimenti inventati.
- **Non aggiungere `fukui2026` al `.bib`.** È un riferimento risultato inesistente, verificato su Crossref, OpenAlex, arXiv, ricerca web e su un notebook di 282 fonti. Va rimosso dalla tesi, non recuperato.
- Non toccare il foglio `iTOC`, né le colonne A-K, U, V del foglio `Fonti`.
- Fare un backup timestamped dell'Excel prima di scriverci.
- Non fare `cd` nella cartella della tesi: rompe gli import di Python. Lavorare da un'altra cwd con percorsi assoluti.
- Se l'Excel dà `PermissionError`, significa che l'utente lo ha aperto: fermarsi e dirlo, non ritentare in loop.

## Output atteso

1. `tesi.bib` corretto e completo.
2. Foglio `Fonti` con le colonne completate.
3. `pipeline/loop1/report_controllo_bib.md` — elenco di tutte le discrepanze trovate, cosa è stato corretto e cosa richiede una decisione umana.

Report in chat: max 25 righe, con l'elenco delle discrepanze per gravità e le eventuali domande aperte.
