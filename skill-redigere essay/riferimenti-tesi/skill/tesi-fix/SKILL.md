---
name: tesi-fix
description: Applica i finding di un report di /tesi-audit, un finding per volta, con lock per capitolo e un commit per fix che cita il finding-id. Usala subito dopo /tesi-audit, prima del prossimo giro di audit.
---

# /tesi-fix \<report-id\>

`<report-id>` identifica un file sotto `reports/` (es. `audit-cap3-iter1` per
`reports/audit-cap3-iter1.md`). Questa skill **non rilegge l'Excel** e non riscrive
`nodes.json` oltre allo `stato`: lavora solo su `nodes/*.md` e sui report.

Due percorsi distinti, mai confusi (§4.5 del prompt orchestratore):

1. **Sostituzione locale** (`fix-applier`, Sonnet, scrive) — grammatica, slop,
   terminologia. **Mai** il depotenziamento di un claim.
2. **Riscrittura strutturale** (di nuovo `node-writer`, con il finding come vincolo) —
   ogni finding di flusso o di ridondanza, e **ogni** depotenziamento di un claim
   (sposta cosa la tesi afferma, può spostare una clausola dentro o fuori dal periodo
   citato — la regola della cucitura lo impone).

## Precondizioni

1. `reports/<report-id>.md` esiste ed è stato prodotto da `/tesi-audit` (ha lo schema
   di finding-id descritto lì: `LINT-*`, `CLAIM-*`, `CHAP-*`).
2. **Lock per capitolo**: prima di iniziare, verifica che nessun'altra istanza di
   `/tesi-fix` stia lavorando sullo stesso capitolo. Meccanismo minimo: crea
   `reports/.lock-cap<N>` con il tuo pid/timestamp all'inizio, cancellalo alla fine; se
   esiste già all'avvio, fermati e segnalalo (non sovrascriverlo, non aspettare in
   loop). I report sono per capitolo, i file sono per nodo: il lock è sul capitolo,
   perché due fix nello stesso capitolo su nodi diversi possono comunque collidere
   sull'aggancio fra fratelli.

## Passi

### 1. Ordina i finding

Dentro il report, applica nell'ordine di precedenza di `/tesi-audit` §Protocollo:
`claim` → `ridondanza` (`CHAP-*` di tipo ripetizione) → `budget` (`LINT-BUDGET-*`) →
`flusso` (`CHAP-*` di tipo flusso). I `LINT-NUM-*` e `LINT-NGRAM-*` (entrambi `high`,
classe "dato fabbricato" o plagio) vanno trattati come `claim`: prima di tutto.

Salta ogni finding già marcato `ESCALATION` nel report: quelli si chiudono solo a
GATE 3-bis con l'autore, mai qui.

### 2. Per ogni finding, uno alla volta

Decidi il percorso:

- **`fix-applier`** se il finding è: violazione di glossario, refuso grammaticale,
  slop di prosa (pattern di `.claude/skills/tesi-slop/`), terminologia — cioè non tocca
  *cosa* la frase afferma, solo *come* lo dice. Input: solo il paragrafo (non l'intero
  DRAFT), il finding, la regola violata. **Non aggiorna il LEDGER**: dopo il fix, esegui
  lo script di rinumerazione:
  ```bash
  /usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/tools/ledger_renumber.py" <id-nodo>
  ```
  che rinumera i `¶N` e verifica che il conteggio righe LEDGER = conteggio paragrafi
  DRAFT. Se non torna, il fix ha fuso o diviso un paragrafo senza dirlo: fermati sul
  nodo, non proseguire con gli altri finding di quel nodo finché non è risolto.

- **`node-writer`** (di nuovo) se il finding è: flusso, ridondanza cross-nodo, o **un
  depotenziamento di claim di qualunque tipo**. Input: il record del nodo completo
  (come in `/tesi-draft`), più il finding come vincolo esplicito nel prompt ("il claim
  in ¶3 va ristretto a quanto Cosa dice davvero dice: <testo>"). Il `## DRAFT` del nodo
  viene riscritto, il `## LEDGER` viene rigenerato dall'agente stesso (qui sì, perché è
  una riscrittura, non una sostituzione locale).
  **Dopo questa riscrittura, rilancia `claim-auditor` (singola istanza, non doppia) sul
  solo nodo toccato**, fuori dal conteggio delle 2 iterazioni di `/tesi-audit`. Se il
  nuovo `claim-auditor` trova un `high`, quel finding torna aperto: non lo chiudere.

### 3. Il lint terminologico rigira dopo ogni fix

```bash
/usr/bin/python3 "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/FONTI/pipeline/glossario/lint.py" <id-nodo> --file <path-al-draft-del-nodo>
```

Non come stadio a parte: il `fix-applier` cercando varietà lessicale può rompere il
glossario dopo che il controllo era già passato. Se dà `BLOCCATO` (exit 2), il fix non
è chiuso: correggi la variante segnalata prima di passare al finding successivo. I 3
falsi positivi noti (bug `_anticipazione_ammessa`, vedi `/tesi-audit`) restano
attesi — non bloccarti su quelli specifici, ma su ogni altro sì.

### 4. Commit

**Un commit per fix**, non uno per finding-batch, messaggio:

```
fix(<id-nodo>): <finding-id> — <riassunto in 5-8 parole>
```

Anche una riscrittura strutturale è un commit isolato: serve a poter fare `revert` di un
singolo fix senza toccare gli altri. Nessun `git revert` automatico sui conflitti: quelli
si risolvono con la tabella di precedenza del passo 1, mai annullando un commit per
tentativi.

### 5. Aggiorna il report

Nel file `reports/<report-id>.md`, marca ogni finding chiuso con `[FIXED — commit
<hash>]` accanto al suo id. Non cancellare il finding dal report: la storia resta
leggibile.

## Formato output

Riepilogo a fine esecuzione:

```
FIX — audit-cap3-iter1 — 2026-09-08
Applicati: 4/6 (LINT-BUDGET-3-003 via fix-applier, CLAIM-3-004 via node-writer + re-audit
  OK, CHAP-3-006 via node-writer, LINT-NGRAM-3-002 via fix-applier)
Saltati (escalation): CLAIM-3-004bis (letteratura come propria, GATE 3-bis)
Bloccati (LEDGER disallineato dopo fix): nessuno
Commit: 4, da <hash> a <hash>
```

## Postcondizioni

- Ogni finding del report è in uno di tre stati: `FIXED` (con hash), `ESCALATION`
  (invariato, mai toccato da questa skill), o riportato come bloccato con motivo.
- Nessun `nodes/<id>.md` ha un LEDGER disallineato rispetto al proprio DRAFT dopo che
  questa skill dichiara di aver finito.
- Il lock `reports/.lock-cap<N>` non esiste più a fine esecuzione.
- Ogni nodo toccato da una riscrittura strutturale ha avuto un secondo passaggio di
  `claim-auditor` (singola istanza) dopo la riscrittura, e il suo esito è nel report.

## Cosa non fa mai

- Non applica il depotenziamento di un claim tramite `fix-applier`: sempre e solo via
  `node-writer`.
- Non chiude un finding marcato `ESCALATION`: quello si chiude solo a GATE 3-bis, con
  l'autore, fuori da questa skill.
- Non applica più di un finding all'interno di uno stesso commit.
- Non lavora su due capitoli in parallelo dietro lo stesso lock.
- Non rilancia i 3 lint deterministici da capo (quello lo fa il prossimo giro di
  `/tesi-audit`, non questa skill).
