---
name: tesi-status
description: Stampa lo stato per nodo, parole scritte contro capacità, e i finding aperti per severità. Usala in qualunque momento per sapere a che punto è la pipeline, non modifica nulla.
---

# /tesi-status

Sola lettura. Legge `build/nodes.json`, `nodes/*.md`, `reports/gap.md`,
`reports/escalation.md` e i report più recenti in `reports/`. Non invoca nessun agente,
non gira alcun lint, non tocca l'Excel. È la fotografia, non il motore.

**`target_words`/`fit_ratio` non sono in `nodes.json`** (restano `0`/`0.0`, placeholder
di `/tesi-ingest`, §"Cosa NON produce" di `/tesi-ingest`): questa skill li legge da
`reports/gap.md`, se esiste. Se `reports/gap.md` non esiste o è più vecchio dell'ultimo
`nodes.json`, rilancialo prima (`/usr/bin/python3 tools/gap.py`, senza `--chapter`,
per non produrre un report parziale) e dillo nel report di stato invece di mostrare
capacità a zero per finta.

## Precondizioni

- `build/nodes.json` esiste. Se non esiste, dillo e basta: "nessun ingest ancora
  eseguito, /tesi-status non ha nulla da riportare." Non inventare uno stato vuoto.

## Passi

```bash
/usr/bin/python3 -c "
import json
BASE = '/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/'
nodes = json.load(open(BASE + 'build/nodes.json'))['nodes']
# conta stato (per nodo), parole scritte (wc sul ## DRAFT di nodes/<id>.md)
# vedi 'Formato output' sotto per la tabella esatta da produrre
"
```

Per ogni nodo in perimetro (capitoli 0-6):

1. Leggi `stato` da `nodes.json` (`"vuoto"` o `"scritto"` — sono gli unici due valori
   che questa pipeline scrive lì: uno stato "bloccato" non esiste come valore di
   `stato`, va dedotto guardando se il nodo compare fra i "Nodi senza materiale" o in un
   capitolo `capitolo_bloccato_k` di `reports/gap.md`).
2. Se `nodes/<id>.md` esiste ed ha un `## DRAFT` non vuoto, conta le parole del solo
   DRAFT (non del LEDGER, non dei commenti `<!-- ... -->`).
3. Cerca la riga del nodo nella tabella "Per nodo foglia" di `reports/gap.md` per
   `target_words`/`fit_ratio`/`classe`; confronta con le parole scritte (scarto
   assoluto e percentuale).
4. Leggi `reports/escalation.md` e ogni `reports/audit-cap*.md` più recente per
   contare i finding **non** marcati `[FIXED ...]` né chiusi a GATE 3-bis, per
   gravità (`high`/`medium`/`low`), per nodo e per capitolo.

## Formato output

```markdown
# Stato tesi — 2026-09-08

## Per capitolo
| Cap | Nodi | Scritti | Bloccati | Parole scritte | Capacità (target) | % | Finding aperti (H/M/L) |
|---|---|---|---|---|---|---|---|
| 0 | 11 | 0 | 8 | 0 | 496 | 0% | 0/0/0 |
| 3 | 11 | 11 | 0 | 1180 | 1219 | 97% | 0/1/2 |
| 5 | 29 | 0 | 29* | 0 | 2693 | — | 0/0/0 |

\* Cap. 5 in attesa di approvazione del taglio (GATE, vedi decisions/DECISIONS.md):
nessun nodo è "bloccato" nel senso di /tesi-gap, ma /tesi-draft si rifiuta di scriverli
finché manca l'approvazione.

## Per nodo (solo quelli non "vuoto" o con finding aperti)
| Nodo | Stato | Parole | Target | Scarto | Finding aperti |
|---|---|---|---|---|---|
| 3.1.1 | scritto | 168 | 149 | +13% | — |
| 3.2.4 | scritto | 90 | 95 | -5% | CLAIM-3-004 [high, escalation] |
| 0.1 | vuoto (senza materiale, vedi reports/gap.md) | — | — | — | — |

## Finding aperti per severità (tutta la tesi)
- high: 1 (CLAIM-3-004, in reports/escalation.md dal 2026-09-08, non ancora chiuso a GATE 3-bis)
- medium: 3
- low: 0

## Riepilogo
Nodi scritti: 11/100 in perimetro. Parole: 1.180/8.770 capacità (13%).
Capitoli completi: 3. Capitoli in attesa di gate: 5 (taglio non approvato).
Gate aperti: GATE 3-bis (1 escalation pendente).
```

## Postcondizioni

- La tabella per capitolo copre **tutti** i capitoli 0-6 (mai solo quelli con attività
  recente): un capitolo a zero è informazione, non rumore da nascondere.
- Ogni finding `high` non ancora chiuso a GATE 3-bis compare esplicitamente, mai solo
  nel conteggio aggregato.
- Il Cap. 7 non compare in nessuna tabella: è fuori perimetro, non "a zero".

## Cosa non fa mai

- Non modifica `nodes.json`, `nodes/*.md`, né alcun report.
- Non gira lint né agenti: se un numero sembra sospetto (es. un nodo "scritto" con 0
  parole), lo segnala come anomalia nel report invece di andarlo a verificare
  eseguendo altro.
- Non decide se un gate è superato: riporta lo stato dei file (`decisions/DECISIONS.md`,
  `reports/escalation.md`), la decisione se procedere resta all'orchestratore e
  all'autore.
