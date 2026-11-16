# Loop 4 — fonti nuove: da `neo aggiunte/` a `Fonti` e `Estratti`

Scritto il 2026-09-06. **Non ancora eseguito.**

Riempie l'anagrafica delle sette fonti arrivate il 06-09 e verifica le coppie
nodo × fonte che ne nascono, con il protocollo a due lettori del loop 2: lettore
locale (subagent Sonnet, legge il PDF) + NotebookLM (secondo lettore indipendente).

`BASE = /Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/`
**Mai `cd` in `BASE`**: rompe gli import di Python. Percorsi assoluti da un'altra cwd.

---

## Cosa è cambiato prima di questo loop

Le sette fonti sono in `FONTI/fonti def/neo aggiunte/`, già rinominate in APA 7.
La riorganizzazione delle cartelle del 06-09 aveva rotto i percorsi di `prepara.py`,
`scrivi.py`, `stato.py` e `glossario/lint.py`: **corretti** (`pipeline/` e
`estrazioni/` ora stanno sotto `FONTI/`). Backup in `iTOC master backup/*_pre-fix-percorsi`.

| chiave | versione posseduta | corrisponde al record citato? |
|---|---|---|
| `miles1995` | copia Manchester Research Explorer | da controllare: può essere l'accepted manuscript |
| `nidumoluknotts1998` | JSTOR, MIS Quarterly 22(2), 105-137 | **sì**, versione pubblicata |
| `bockle2004` | IEEE Software 21(3) | **sì**, versione pubblicata |
| `boehm2004` | ISESE 2004 | **sì**, versione pubblicata |
| `hui2024` | draft autori, 12 ott. 2024 | **no** — il record è Organization Science 35(6) |
| `cui2026` | working paper MIT, feb. 2025 | **no** — il record è Management Science 2026 |
| `demirci2025` | CESifo WP 11276, ago. 2024 | **no** — il record è Management Science 71(10) |

Le ultime tre righe sono la ragione per cui la versione va scritta nella colonna `Note`
di `Fonti`: il metodo verifica il claim contro **il PDF che possiedi**, e i numeri di un
working paper possono non essere quelli dell'articolo pubblicato.

---

## FASE 0 — precondizioni. L'orchestratore si ferma se una manca

1. **Excel chiuso.** Oggi esiste `~$iTOC master 2.xlsx`: c'è un file aperto. Un
   salvataggio dell'utente con il file aperto da prima ha già cancellato un foglio intero.
2. **Quale file è canonico.** In `BASE` ci sono `iTOC master.xlsx` e `iTOC master 2.xlsx`,
   stessa dimensione e stessa ora. Tutti gli script scrivono su `iTOC master.xlsx`.
   Se il lavoro vero è nell'altro, gli script scrivono nel posto sbagliato.
3. **Backup** `iTOC master backup/iTOC master.<timestamp>.pre-loop4.xlsx`.
4. **Tre decisioni dell'autore** (§ Decisioni aperte, in fondo). Senza, la FASE 2 non
   sa quali coppie creare.

---

## FASE 1 — anagrafica in `Fonti` (script, nessun agente)

**Sei righe nuove** (55-60): `hui2024`, `cui2026`, `demirci2025`, `nidumoluknotts1998`,
`bockle2004`, `boehm2004` — quest'ultima solo se adottata.
**Una riga da aggiornare**: `miles1995`, oggi `Stato acquisizione = non_trovata`.

I campi bibliografici sono già tutti in `referti/DA SCARICARE.md`: chiave, citazione,
autori, anno, titolo, sede, DOI, URL, nodi candidati. Non si ricercano di nuovo.
`Peer-reviewed` si riferisce alla **sede del record**, non alla versione posseduta;
la versione va in `Note`.

Poi, nell'ordine:

- spostare i sette PDF da `neo aggiunte/` a `FONTI/fonti def/` — la convenzione è una
  cartella unica, un PDF per riga di `Fonti`, nessuna area di staging;
- `pdftotext -layout` → `FONTI/pipeline/testi estratti/<chiave>.txt` per tutte e sette;
- `tesi.bib`: da 54 a 60 voci;
- controllo d'invariante: **righe in `Fonti` = PDF in `fonti def/` = voci in `tesi.bib`**,
  meno le righe ancora `non_trovata`.

Restano `non_trovata`: **`ghemawat1991`** (non trovato: Internet Archive, prestito
digitale) e **`rumelt1984`** (document delivery inviato). Le loro righe in `Estratti`
(59 e 66) restano senza esito, ed è corretto così.

---

## FASE 2 — coppie in `Estratti` (orchestratore Opus, non un agente esecutore)

Il campo `Claim da verificare` è **quello che la tesi attribuisce alla fonte**: si scrive
leggendo `Descrizione` e `Fonti + ruolo` del nodo in `iTOC`, non si fa scrivere al
lettore. Se lo scrive il lettore, sta verificando sé stesso.

### 2a — coppie certe

| Nodo × fonte | Stato |
|---|---|
| `1.1.1 × miles1995` | **riga 12, già esistente**, sbloccata dall'arrivo del PDF |
| `1.2.3 × hui2024` | nuova — fonte portante |
| `1.2.3 × cui2026` | nuova — ancoraggio al software |
| `1.2.3 × demirci2025` | nuova — contro-evidenza, in nota |
| `1.2.3 × peng2023` | **nuova, costo zero**: PDF già in casa e già verificato, ma sulla coppia `1 × peng2023`. Qui il claim è diverso — Tabella 1, *Programming experience (years)*, coefficiente 8,23 (SE 4,36, p = 0,0629) — e va verificato come tale, con la significatività marginale dichiarata |
| `6.3 × reeddefillippi1990` | **nuova.** `STATO E PROSSIMI PASSI.md` la dà per creata: **non esiste**. In `Estratti` il `6.3` ha solo `prencipetell2001`, `non usabile`. Va creata davvero |

### 2b — le cinque risoluzioni e gli otto casi di citazione congiunta

`STATO.md` le teneva in sospeso *«finché le fonti nuove non sono arrivate, così le righe
si aggiornano insieme»*. Sono arrivate: **questo è il loop in cui si scrivono.**

Cinque arbitrati, da riscrivere in `Cosa dice davvero` e `Note` con esito `da riformulare`:
`2.2.2 × shrestha2019`, `6.1 × kirmanirao2000`, `4.3.2 × zuckerman1999`,
`3.2.2 × kahnemanklein2009`, `1.2.3 × siddiqzhang2026`.

Otto casi che si chiudono con la sola regola della cucitura (scomposizione dei claim con
citazione congiunta, regola 8 di `CONTESTO` §5): `1.1.2`, `1.3.1`, `3.1.1`, `4.1`,
`4.1.2`, `4.1.4`, `4.2.2`, `4.3.1`.

Le altre 30 righe con flag `⚠ divergenza` **non** si arbitrano: 16 sono `non verificabile`
da NotebookLM (vale il lettore locale), 14 sono scarti di un gradino (vale il più severo).

### 2c — coppie che dipendono da una decisione

`nidumoluknotts1998`, `bockle2004`, `boehm2004` hanno nodi *candidati*, non assegnati.
Nessuna riga in `Estratti` finché l'autore non dice a quale nodo vanno. Una riga senza
nodo non è una verifica, è un segnaposto.

---

## FASE 3 — lettore locale (subagent Sonnet)

```
python3 "BASE/FONTI/pipeline/loop2/prepara.py"
```

Genera un task JSON per ogni coppia senza esito, in `FONTI/pipeline/loop2/task/`.
Poi **un subagent Sonnet per coppia, memoria fresca**, che legge:

1. `FONTI/pipeline/loop2/ISTRUZIONI_LETTORE.md`
2. `FONTI/pipeline/prompt/A - lettore ESEGUIBILE.md` — prevale su tutto

Output in `FONTI/estrazioni/estratti/<nodo>__<chiave>.json`, 7 chiavi esatte.
Il vincolo duro è la `citazione_verbatim`: **un solo passaggio contiguo**, minimo 25
caratteri, ritrovabile con match esatto nel `.txt`, mai dal front matter. `scrivi.py`
rifiuta un `usabile` la cui citazione non si ritrova.

---

## FASE 4 — NotebookLM (secondo lettore)

**Precondizione che fa fallire tutto se saltata.** Il notebook
`7060cbf5-c222-410f-a2be-c532433e962c` ("fonti tesi def") ha **48 sorgenti** contro le 60
voci che `tesi.bib` avrà dopo la FASE 1. Le fonti nuove **non sono nel notebook**: se si
interroga così, ogni coppia nuova torna `non verificabile` e il secondo lettore non
esiste. Prima si caricano i sette PDF con `source_add`, poi si verifica con
`notebook_get` che ci siano.

Per ogni coppia, come da `ISTRUZIONI_NOTEBOOKLM.md` e `prompt/B - notebooklm ESEGUIBILE.md`:
`notebook_query` passando **`source_ids` con il solo id della sorgente in esame** — senza,
NotebookLM pesca dalle altre 59 e il confronto perde ogni significato.

Output in `FONTI/estrazioni/estratti_nlm/<nodo>__<chiave>.json`, 7 chiavi esatte.
NotebookLM non produce l'esito: la conversione dei quattro valori la fa il lettore, coi
criteri del prompt B. **Non aprire l'Excel.**

---

## FASE 5 — scrittore unico

```
python3 "BASE/FONTI/pipeline/loop2/scrivi.py"            # dry-run, valida e mostra
python3 "BASE/FONTI/pipeline/loop2/scrivi.py" --commit   # scrive
```

È l'**unico** processo che apre l'Excel in scrittura, e fa il backup da sé. Rileggere il
dry-run prima di committare: la validazione è meccanica e scarta il lavoro non conforme.

---

## FASE 6 — chiusura

```
python3 "BASE/FONTI/pipeline/loop2/stato.py"
```

Le divergenze nuove fra i due lettori vanno all'autore, una per una. Poi si aggiornano
**solo** i due file canonici — `referti/DA SCARICARE.md` e
`referti/STATO E PROSSIMI PASSI.md`. Non si crea un terzo file di stato.

---

## Decisioni aperte — servono prima della FASE 2

1. **`boehm2004` dentro o fuori.** `DA SCARICARE.md` diceva «prendila **solo se** Böckle
   non esce». Böckle è uscito. Il criterio scritto nello stesso file — *una fonte in più
   costa una riga, un PDF e almeno una coppia in doppia lettura; se non sblocca un nodo
   scoperto e non sostituisce una fonte bocciata, il costo supera il beneficio* — dice di
   lasciarla fuori. **Raccomandazione: fuori**, PDF tenuto ma non in bibliografia.
2. **A quali nodi vanno `nidumoluknotts1998` e `bockle2004`.** Candidati:
   Nidumolu → `4.1.2`, `4.3.1`, `2.3.2`; Böckle → `4.1.1`, `4.1.2`, `6.2`.
   Nota: il `2.3.2` non ha oggi nessuna fonte, e il `6.2` è già chiuso con `krueger2016`.
3. **Il testo del `6.3`**, in attesa di ok dall'05-09.

## Due cose viste preparando questo loop, che non riguardano le fonti nuove

- **`fukui2026` è `mattone stretto` del nodo `1.2.3`**, verificata `usabile` da entrambi i
  lettori, PDF in `fonti def/`. `DA SCARICARE.md` però descrive il `1.2.3` come poggiato
  su `siddiqzhang2026` e non nomina mai Fukui. Le due descrizioni non coincidono: da
  riconciliare prima di scrivere il nodo.
- **Il `6.2` cita `krueger2016` con quattro autori**; il record pubblicato ACM ne ha
  cinque (c'è anche Meinicke) e il foglio `Fonti` li ha corretti. Il nome del PDF e il
  campo `Fonti + ruolo` del nodo portano ancora la versione a quattro.
