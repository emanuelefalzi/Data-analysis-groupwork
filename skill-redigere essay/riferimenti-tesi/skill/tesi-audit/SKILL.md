---
name: tesi-audit
description: Esegue i 4 lint deterministici più claim-auditor e chapter-auditor (ciascuno in doppia istanza indipendente) su un capitolo, oppure --whole per il solo chapter-auditor in modalità cross-capitolo. Il prose-auditor non gira qui. Usala dopo ogni /tesi-draft su un capitolo.
---

# /tesi-audit \<capitolo\> | /tesi-audit --whole

Read-only su `nodes/`: produce solo un report, non modifica mai un DRAFT. Le modifiche
passano da `/tesi-fix`.

Due modalità, **mai combinate nella stessa invocazione**:

- `/tesi-audit <capitolo>` — 3 lint deterministici + `claim-auditor` + `chapter-auditor`
  in modalità "dentro il capitolo", ciascuno in doppia istanza indipendente.
- `/tesi-audit --whole` — solo `chapter-auditor`, in modalità cross-capitolo, sull'intero
  perimetro scritto fino a quel momento. Va dopo l'ultimo capitolo, prima del
  `prose-auditor` e prima di `/tesi-assemble`.

## Precondizioni

1. **Modalità `<capitolo>`**: tutti i nodi foglia del capitolo hanno `stato: "scritto"`
   in `nodes.json` (o uno stato di blocco dichiarato — quelli si escludono dall'audit,
   non lo bloccano). Se un nodo non bloccato è ancora `"vuoto"`, fermati: manca il draft.
2. **Modalità `--whole`**: tutti i capitoli 0-6 hanno terminato il loro `/tesi-draft` e
   il proprio `/tesi-audit <capitolo>` con 0 `high` residui non escalati (vedi §
   Protocollo sotto). Se un capitolo non è a questo punto, fermati e dillo.
3. `FONTI/pipeline/glossario/lint.py --autotest` dà **0 blocchi**. Eseguilo prima di
   ogni uso:
   ```bash
   /usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/FONTI/pipeline/glossario/lint.py" --autotest
   ```
   Se dà un numero diverso da 0 (oggi ne dà 3, per il bug noto in
   `_anticipazione_ammessa()`, §4.7 del prompt orchestratore), **non bloccarti**: è un
   falso positivo documentato finché quella funzione non viene corretta. Riportalo nel
   report come "lint terminologico: 3 falsi positivi noti (bug `_anticipazione_ammessa`),
   trattato come lint più severo del previsto" e procedi. Se il numero cambia rispetto a
   3, fermati e segnalalo: potrebbe non essere più un falso positivo noto.

## Passi

### 1. I tre lint deterministici, prima di tutto — un nodo alla volta

**I tre script accettano un id di nodo singolo, mai un capitolo** (verificato sul loro
`argparse`: `nodo [testo ...]`, e se non ricevono `testo` leggono da soli
`nodes/<id>.md`). Non c'è un modo di passargli `<capitolo>` per lintare l'intero
capitolo in un colpo solo: chiamarli così tratterebbe l'id del capitolo come se fosse
l'id del nodo-capofila, ignorando tutte le sue foglie.

Costruisci l'elenco dei nodi da lintare leggendo `build/nodes.json`: tutti i nodi con
`chapter == <capitolo>`, `is_leaf: true` e `stato: "scritto"` (i nodi bloccati — vedi
Precondizione 1 — sono già esclusi dall'audit, non ci finiscono). Per **ciascun** id di
quell'elenco, in un ciclo, lancia i tre script una volta:

```bash
for nodo in <id-nodo-1> <id-nodo-2> ...; do
  /usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/lint_numeri.py" "$nodo"
  /usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/lint_ngrammi.py" "$nodo"
  /usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/lint_budget.py" "$nodo"
done
```

Contratto atteso di ciascuno (per chi scrive `tools/*.py`), applicato **per nodo**:

- **`lint_numeri.py <id-nodo>`**: per il DRAFT di quel nodo, ogni cifra, percentuale,
  data, importo e nome proprio deve comparire *verbatim* nell'unione di tutti i
  `source_desc` in perimetro più `Fonti` ed `Estratti` (non solo il nodo e i suoi
  antenati — §4.7). Violazione fuori da questa unione = finding `high` automatico.
  L'appartenenza al nodo o ai suoi antenati resta come **avviso**, non blocco (il Cap. 6
  deduce dai Cap. 1-4 e il suo unico antenato, il nodo `6`, ha `Descrizione` vuota).
  Output: lista di finding `{id, nodo, gravità, stringa, motivo}`.
- **`lint_ngrammi.py <id-nodo>`**: n-grammi da 8 parole, per quel nodo, contro le sole
  `Citazione verbatim` delle coppie di quel nodo — filtra `build/estratti.json` (chiavi
  `"<nodo>|<id_fonte>"`) per prefisso `"<id-nodo>|"` e leggi il campo
  `citazione_verbatim`. Un n-gramma verbatim sopravvissuto nel DRAFT = finding `high`.
- **`lint_budget.py <id-nodo>`**: `wc` del `## DRAFT` di quel nodo contro
  `target_words`. **`target_words` non è in `nodes.json`** (resta `0`, placeholder):
  `lint_budget.py` importa `tools/gap.py` come modulo — lo stesso già dichiarato nel
  docstring di `gap.py` ("le funzioni di questo modulo sono importate da
  `lint_budget.py`, così la derivazione di `target_words` vive in un solo posto") — e
  chiama `derive_targets_for_chapter` per ottenerlo al volo, non lo rilegge da un file.
  Tolleranza ±15%. Fuori banda senza un `[[GAP: …]]` che lo spieghi = finding `medium`.

Ognuno **restituisce un elenco di finding**, mai un blocco secco: raccogli l'exit code e
i finding di ogni chiamata, per ogni nodo, e sommali. Il totale dei rilievi per lint che
il report cita in `## Lint deterministici` è quella somma su tutti i nodi del capitolo,
non l'output di un'unica chiamata sul capitolo — con lo stesso schema di id
(`LINT-<tipo>-<cap>-<seq>`).

### 2. `claim-auditor`, doppia istanza indipendente

Lancia **due** istanze dell'agente `claim-auditor` (Sonnet, read-only) sullo stesso
capitolo, **in contesto pulito**, che non si vedono fra loro — due chiamate separate
allo strumento Agent/Task, non una chiamata con "controlla due volte". Ad ognuna passa:

- il `## DRAFT` di ogni nodo del capitolo (mai il LEDGER come punto di partenza — lavora
  span-first: per ogni frase cerca da sé il supporto in `source_desc`);
- **`source_desc` intero del nodo**, non uno span, non gli offset del LEDGER;
- `fonti_ammesse[]`, `fonti_vietate[]`, `risoluzioni[]`, `trappole` del nodo;
- `build/estratti.json` per le coppie del nodo (per il lookup su `Cosa dice davvero`).

Bersagli (§4.2, elenco completo da includere nel prompt dell'agente): frasi orfane;
citazioni assenti da `Estratti` o usate per dire altro; over-claim; stime spacciate per
dati; fatti su ELFO non ricavabili dall'Excel; sintesi originali attribuite a un autore;
**letteratura presentata come propria** sui nodi senza alcuna fonte ammessa — finding
`high`, va sempre in escalation, mai risolto dal writer; violazioni della regola della
cucitura. Checklist di chiusura: ogni voce di `trappole` del nodo verificata punto per
punto.

Ogni istanza produce un elenco `{id, nodo, gravità, span_citato, motivo}`, con id
`CLAIM-A-<cap>-<seq>` e `CLAIM-B-<cap>-<seq>` per le due istanze.

**Confronto**: un finding sullo stesso span (match sulla prima frase citata) presente in
entrambe le istanze **passa** nel report finale come confermato. Un finding presente in
una sola istanza va nel report come **discorde**, con entrambe le versioni riportate:
**tu arbitri**, non lo fai passare né lo scarti automaticamente.

### 3. `chapter-auditor`, doppia istanza indipendente

Stessa logica di doppia istanza indipendente. Due modalità:

- **dentro il capitolo** (default, per `/tesi-audit <capitolo>`): input = tutti i DRAFT
  del capitolo. Bersagli: ripetizioni fra figli dello stesso padre (estrae
  *affermazioni*, non frasi — per ogni finding: le due sedi, l'affermazione duplicata,
  a chi appartiene secondo `ruolo`; risoluzione proposta: resta dove `ruolo` dice che va
  dimostrata, l'altro nodo la richiama in mezza riga, **mai cancellare entrambe**); e
  flusso (le transizioni dichiarate in "Aggancio" esistono davvero, la catena
  argomentativa regge letta di fila). **Non segnalare** i richiami previsti dagli
  "Aggancio" né la ripresa obbligata di un termine di glossario.
- **cross-capitolo** (`--whole`): input = tutti i DRAFT scritti fino a quel momento,
  capitoli 0-6. Stessi bersagli, ma cercando ridondanza **fra** capitoli, non solo
  dentro.

## Protocollo di convergenza (per `/tesi-audit <capitolo>`, §10)

1. Lint deterministici, poi `claim-auditor` e `chapter-auditor` a doppia istanza, come
   sopra. Il `prose-auditor` **non gira qui**.
2. Se ci sono fix da applicare, l'ordine è `claim` → `ridondanza` → `budget` → `flusso`
   (il budget prima del lavoro di superficie: se metà nodo va tagliata non ha senso
   averla levigata). Questo ordine è per `/tesi-fix`, non per questa skill: qui ti limiti
   a riportare i finding nell'ordine giusto nel file di report.
3. Precedenze in conflitto, non negoziabili, da annotare quando due finding collidono
   sullo stesso testo: `ruolo` batte `budget`; `claim` batte `prose`; `claim` batte
   `budget`; `budget` batte `ridondanza`; `flusso` batte `ridondanza` sulle transizioni
   dichiarate; il glossario batte `prose` sempre; `claim` batte `flusso` (una
   transizione senza materiale si dichiara mancante, non si scrive); `ruolo` batte
   `flusso` sui nodi `1 riga:`.
4. **Massimo 2 iterazioni** di questo ciclo per capitolo (il ciclo intero
   audit→fix→audit, non le chiamate a questa skill): tienine il conto in
   `decisions/DECISIONS.md` o nel nome del file di report (`audit-cap3-iter1.md`,
   `audit-cap3-iter2.md`). Al terzo giro un finding ancora aperto **non si ridiscute**:
   va in `reports/escalation.md`, chiuso solo a GATE 3-bis.
5. Ogni riscrittura strutturale del `node-writer` (via `/tesi-fix`) fa scattare una
   ri-esecuzione **obbligatoria** del solo `claim-auditor` sul nodo toccato, **fuori**
   dal conteggio delle 2 iterazioni.

## Formato output

```
reports/audit-cap<N>-<iterN>.md      # oppure reports/audit-whole.md
```

```markdown
# Audit — Capitolo 3, iterazione 1 — 2026-09-08

## Lint deterministici
- LINT-NUM-3-001 [high] nodo 3.2.1: "47%" non trovato in alcun source_desc/Fonti/Estratti in perimetro
- LINT-NGRAM-3-002 [high] nodo 3.1.3: n-gramma verbatim di 9 parole coincide con Estratti[3.1.3|akerlof1970].citazione_verbatim
- LINT-BUDGET-3-003 [medium] nodo 3.2.2: 210 parole contro target 165 (+27%, oltre ±15%, nessun [[GAP:]])

## claim-auditor — confermati (entrambe le istanze concordano)
- CLAIM-3-004 [high] nodo 3.1.1: "domain knowledge is difficult to imitate" senza attribuzione — letteratura presentata come propria (Dierickx & Cool 1989 non citato) → ESCALATION

## claim-auditor — discordi (arbitraggio dell'orchestratore)
- CLAIM-3-005: istanza A segnala over-claim su "demonstrates", istanza B non lo segnala. Arbitrato: <la tua decisione qui, con motivo>

## chapter-auditor — confermati
- CHAP-3-006 [medium] ripetizione fra 3.1.2 e 3.1.4: "...", resta in 3.1.2 (ruolo: deve dimostrare), 3.1.4 richiama in mezza riga

## Riepilogo per /tesi-fix
- fix locali (fix-applier): LINT-BUDGET-3-003, ...
- riscritture strutturali (node-writer): CLAIM-3-004 (dopo GATE 3-bis), CHAP-3-006
- escalation: CLAIM-3-004
```

## Postcondizioni

- Ogni finding ha un id univoco, una gravità (`high`/`medium`/`low`), un nodo, e — per
  claim/chapter-auditor — è marcato confermato o discorde.
- Ogni finding `high` confermato compare anche in `reports/escalation.md` (append, non
  sovrascrittura: uno storico di tutti gli high mai visti serve a GATE 3-bis).
- Il report dichiara esplicitamente il numero di iterazione e se è l'ultima disponibile
  (2/2) prima dell'escalation forzata.
- In modalità `--whole`, il report non contiene alcun finding di `claim-auditor` né dei
  lint: solo `chapter-auditor` cross-capitolo.

## Cosa non fa mai

- Non modifica alcun file in `nodes/`: è read-only, punto.
- Non fa girare il `prose-auditor`: quello è uno stadio finale separato, unica volta,
  sul documento intero, insieme a `--whole`.
- Non applica automaticamente un fix, nemmeno quando i lint deterministici sono
  inequivocabili: propone, non corregge.
- Non arbitra da sola i finding discordi lasciandoli "passare di default": ogni
  discordia va decisa esplicitamente, mai ignorata per silenzio.
- Non supera le 2 iterazioni per capitolo senza mandare il residuo in escalation.

## Il quarto lint e il citation-auditor — aggiunti dopo il pilota del Cap. 3

`tools/lint_citazioni.py` controlla la **forma** dei token di citazione, che nessuno degli
altri tre vede: `[[CIT-P:]]` in posizione di soggetto, `[[CIT-N:]]` in posizione di
parentetica, nome dell'autore scritto accanto a un token narrativo che gia' lo contiene.
Sul pilota ne ha trovati sei su tredici token, e nessuno sarebbe emerso prima
dell'assemblaggio.

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/lint_citazioni.py" --capitolo <N>
```

Gira **prima** degli agenti, come gli altri tre. Un `HIGH` blocca.

L'agente **`citation-auditor`** gira **dopo** `claim-auditor`, in doppia istanza
indipendente come gli altri, e copre quello che la regex non vede: la cucitura rotta, il
claim allargato su una coppia `da riformulare`, un vincolo d'uso dell'autore ignorato, un
preprint che regge un «research shows», la copertura e la coerenza fra nodi. Il suo referto
**instrada** ogni rilievo all'agente che lo risolve (`fix-applier`, `node-writer`, o
`reports/escalation.md` per la classe che nessun agente puo' chiudere).
