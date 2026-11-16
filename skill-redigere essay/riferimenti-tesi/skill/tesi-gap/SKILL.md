---
name: tesi-gap
description: Genera il gap report (capacità contro materiale, fit_ratio, regime per capitolo, nodi senza materiale, domande GATE 1) eseguendo tools/gap.py. Invocala subito dopo /tesi-ingest e prima di qualunque /tesi-draft. È GATE 1: dopo averlo prodotto, ti fermi.
---

# /tesi-gap

Esegue `tools/gap.py` (già scritto — non riscriverlo). Read-only su Excel e su
`nodes/`: legge `build/nodes.json` (o, con `--dry-run`, rilegge l'Excel direttamente) e
scrive **solo** `reports/gap.md`. Non tocca `nodes.json`: `target_words`, `fit_ratio` e
`regime` **non vengono mai persistiti** su `nodes.json` — vivono soltanto nell'output di
questo comando, ricalcolato ogni volta.

## Precondizioni

1. `build/nodes.json` esiste (altrimenti `tools/gap.py` cade sull'Excel come fallback,
   il che funziona ma è più lento e non è il caso normale: se manca, di' all'utente di
   lanciare prima `/tesi-ingest`).
2. `build/nodes.json` non più vecchio dell'ultima modifica nota all'Excel — se lo è,
   serve prima `/tesi-resync`.

## Passi

### Report completo (quello che conta per GATE 1)

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/gap.py"
```

Scrive `reports/gap.md` (sovrascritto, non un file per iterazione: la storia sta in git
se il file è già tracciato) e lo stampa anche su stdout. **Non passare `--chapter` in
questa invocazione**: `--chapter N` filtra anche il file scritto su disco, e
sovrascriverebbe il report completo con la sola vista di un capitolo — è un'opzione per
uso interno di `/tesi-draft` (vedi sotto), non per il gap report ufficiale.

### Uso interno da altre skill (non per GATE 1)

`/tesi-draft` e altre skill che hanno bisogno solo del `target_words` di un capitolo
**senza** toccare `reports/gap.md` usano:

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/gap.py" --chapter 5 --dry-run
```

`--dry-run` fa due cose insieme: non scrive `reports/gap.md` (sicuro da chiamare senza
sporcare il report ufficiale) **e** forza la lettura diretta dall'Excel invece di
`build/nodes.json` — quindi verifica prima che non ci siano lock file, stessa
precondizione di `/tesi-ingest`.

## Cosa calcola — verificato sul codice reale di `tools/gap.py`

### Per capitolo (`chapter_metrics`)

```
struttura_pp(c)  = righe fisiche stimate dei titoli × 0,043 pp/riga
                    (costante calibrata una volta sulla misura nota di §3: 115 righe
                    fisiche = 4,94 pagine sui 100 titoli in perimetro; ricalibrare le
                    due costanti in tools/gap.py se il template cambia)
C_c              = (budget_pp(c) − struttura_pp(c)) × 350        # None se budget_pp assente
M_c              = Σ source_words(i) per i in c, source_words > 0
k_c              = C_c / M_c                                      # None se M_c == 0
capienza_strutturale_rotta = struttura_pp(c) > 0,45 × budget_pp(c)
capitolo_bloccato_k        = k_c < 0,55 oppure k_c > 1,50
regime (di capitolo, per il report) = tre valori, non due — riusa la stessa
                              classificazione a 5 classi del livello nodo:
                              k_c < 0,55            → stato "BLOCCATO IN COMPRESSIONE"
                              0,55 ≤ k_c < 0,85      → "compressione"
                              0,85 ≤ k_c < 1,20      → "resa"
                              1,20 ≤ k_c < 1,50      → "espansione"
                              k_c ≥ 1,50             → stato "BLOCCATO IN ESPANSIONE"
```

`tail_pp_stimata` (le code non riempite da `pageBreakBefore`, ~0,5 pagine per
capitolo) è **dichiarata nel report, non sottratta da `C_c`**: ogni capacità riportata
è quindi un limite superiore, come da §3 del prompt orchestratore.

### Per nodo foglia con materiale (`derive_targets_for_chapter`, i cinque passi di §4.1)

- `Ruolo` = `1 riga:` e `source_words ≤ 70` → `target_words = source_words`, escluso
  dalla scalatura.
- `Ruolo` = `1 riga:` e `source_words > 70` → scalato come gli altri
  (`clip(b_i·k_c, 0,55·b_i, 1,50·b_i)`), ma marcato `conflitto_ruolo: true` — **non**
  bloccato: il default finché l'autore non risponde a GATE 1 è non troncare.
- `Ruolo` contiene `Deve dimostrare` o è un nodo foglia generico → `clip(b_i·k_c, 0,55·b_i, 1,50·b_i)`.
- Nodo non foglia con testo (un "cappello") → stesso calcolo ma tetto superiore più
  stretto, `clip(b_i·k_c, 0,55·b_i, 1,20·b_i)`.
- **Residuo**: la differenza fra `C_c` e la somma dei `target_words` si ridistribuisce
  sui nodi non vincolati, in proporzione a `source_words`. Se non c'è nessun nodo non
  vincolato su cui ridistribuire e il residuo supera il 5% di `C_c`,
  `blocco_capitolo_residuo: true`.

`fit_ratio(nodo) = target_words / source_words` (calcolato **dopo** il clip — quindi in
pratica quasi sempre dentro `[0,55 ; 1,50]` per costruzione: il segnale "bloccato" vero
è **a livello di capitolo**, `capitolo_bloccato_k`, quando l'intero capitolo ha
`k_c` fuori banda — vedi il Cap. 5 oggi, `k_c ≈ 0,42`. Non aspettarti molti nodi
individualmente marcati `BLOCCATO IN COMPRESSIONE/ESPANSIONE` nella tabella per nodo:
è il capitolo che lo è, e la tabella per nodo lo eredita solo indirettamente tramite
target ridotti.

`regime(nodo)` (per `/tesi-draft`) = tre valori, stessa soglia della classe a 5 fasce
(§7): `"compressione"` per `fit_ratio` 0,55-0,85, `"resa"` per 0,85-1,20, `"espansione"`
per 1,20-1,50. Ai due estremi non è un regime: è `None`, perché quel caso — a livello di
nodo — non dovrebbe presentarsi per costruzione (il clip del passo 3 tiene `fit_ratio`
dentro `[0,55 ; 1,50]`); se compare comunque, il writer non riceve un regime e il nodo va
trattato come bloccato, non come un quarto caso.

**Nodi senza materiale** (`source_words == 0`, in perimetro): esclusi dal calcolo,
elencati a parte in `nodi_senza_materiale`.

## Formato output — `reports/gap.md`, esatto (dal codice, non parafrasato)

```markdown
# Gap report

(fonte dati nodi: build/nodes.json)

## Per capitolo
| Cap | Nodi | Foglie | Righe tit. | Strutt. pp | Budget pp | Capacita' C_c | Materiale M_c | k_c | Regime | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 29 | 23 | 30 | 1.31 | 9 | 2693.2 | 6436 | 0.4185 | BLOCCATO IN COMPRESSIONE | BLOCCATO IN COMPRESSIONE (k_c=0.4185) |
...

(tail non dedotta dalla capacita', ~0.50 pp/capitolo attesa dal pageBreakBefore di ogni
Heading1 — §3: le capacita' qui sopra sono un limite superiore, ogni ratio e' ottimistico)

## Per nodo foglia
| Nodo | source_words | target_words | fit_ratio | classe | conflitto ruolo |
|---|---|---|---|---|---|
| 3.1.1 | 175 | 149 | 0.851 | resa diretta | |
| 5.2.1 | 175 | 73 | 0.417 | compressione | |

## Nodi senza materiale (Descrizione vuota, in perimetro)
- 0.1  → target_words=0, stato ⚠ RICHIESTA AUTORE, non passare al writer
...

## Conflitto Ruolo/materiale ('1 riga:' con Descrizione > 70 parole)
- 5.2.1
...

## Domande del GATE 1
1. il budget di pagine per capitolo: ...
2. 'Ruolo' = '1 riga:' — e' una specifica di lunghezza o l'enunciato del ruolo? ...
3. dove vivono abstract, introduzione e reference list — ...
4. il taglio del Cap. 5 (o di ogni altro capitolo bloccato in compressione, vedi sopra): ...
```

Le quattro domande sono generate dal codice stesso (`gate1_domande()`), non
riformularle a mano: riportale **testualmente** così come lo script le stampa,
compresi i numeri che calcola (nodi in conflitto, parole eccedenti).

## Cosa aggiungere tu, oltre all'output dello script (obbligatorio, §3 del prompt)

Lo script **non** enfatizza automaticamente il Cap. 5 rispetto agli altri numeri
aggregati. Aggiungi tu, in una riga subito dopo la tabella per capitolo:

> Il Cap. 5 da solo eccede il proprio budget più di quanto l'intera tesi ecceda il
> proprio: ogni cifra aggregata su tutto il perimetro, in questo report o altrove, va
> letta insieme al dato del Cap. 5, altrimenti dice il falso.

## Postcondizioni

- `reports/gap.md` esiste e contiene **entrambe** le tabelle (per capitolo e per nodo
  foglia), mai una sola.
- Le quattro domande del GATE 1 sono presenti, testuali, nell'ordine dello script.
- Dopo aver scritto il report, **ti fermi**: non esegui `/tesi-draft` nella stessa
  risposta, nemmeno sul capitolo pilota (Cap. 3). L'autore deve rispondere prima.
- Se hai usato `--chapter`, verifica di averlo fatto **solo** con `--dry-run`: se
  `reports/gap.md` oggi contiene un solo capitolo, qualcuno ha invocato lo script senza
  `--dry-run` con `--chapter` impostato — rilancialo senza `--chapter` per ripristinare
  il report completo prima di dichiarare GATE 1 superato.

## Cosa non fa mai

- Non scrive `target_words`/`fit_ratio`/`regime` su `nodes.json`: solo su
  `reports/gap.md`, e solo per l'invocazione corrente (si perde e si ricalcola al
  prossimo giro — non è un bug, è la scelta di tenere la formula in un solo posto).
- Non decide l'allocazione del budget, non modifica `Budget pp` sull'Excel.
- Non propone da sola l'elenco dei tagli del Cap. 5 nodo per nodo.
- Non lancia `/tesi-draft` né alcun agente.
