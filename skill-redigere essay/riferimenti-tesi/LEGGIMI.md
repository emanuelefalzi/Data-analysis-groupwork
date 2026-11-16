# riferimenti-tesi — i componenti originali, solo da leggere

Copie **non modificate** dei pezzi della pipeline con cui è stata scritta la tesi (cartella
`tesi 4 - scrittura`, settembre 2026). Servono quando una regola della versione generale non
basta e si vuole capire da dove viene. **Non vanno eseguiti**: hanno percorsi assoluti verso la
cartella della tesi, leggono `iTOC master.xlsx`, e alcuni scrivono su quell'Excel.

Il file della tesi `CLAUDE.md` è stato rinominato `CLAUDE-tesi.md` apposta: con il suo nome vero
Claude lo caricherebbe come istruzioni quando lavora in questa sottocartella. Per lo stesso motivo
agenti e skill stanno in `agenti/` e `skill/`, non sotto `.claude/`, così non si registrano.

## Cosa c'è e a cosa corrisponde

| Originale | Cos'era | Diventato |
|---|---|---|
| `PROMPT-orchestratore-tesi.md` | il design completo della pipeline di stesura (§0-§12) | `PROCESSO.md` |
| `CLAUDE-tesi.md` | regole sempre attive della tesi | `CLAUDE.md` |
| `CONTESTO-EXCEL-per-orchestratore.md` | le colonne dell'Excel iTOC | `scaletta/scaletta.md` (sintassi) |
| `loop1/` | recupero fonti sull'Excel (`recupera.py`, `lib/`) | `tools/fonti/recupera.py` + `lib/csvio.py` |
| `loop2/` | prepara/scrivi/stato del doppio lettore, `dossier.py` | `tools/fonti/prepara.py`, `valida.py` |
| `prompt-fonti/A - lettore …` | metodo e contratto del lettore (verifica di claim) | `prompt/metodo-lettura.md`, agente `lettore-fonti` |
| `prompt-fonti/B - notebooklm …` | secondo lettore | agente `secondo-lettore-nlm` |
| `prompt-fonti/C - disambiguazione …` | scelta fra candidati ambigui del loop 1 | (a mano, con l'autore: `/essay-fonti` passo 1) |
| `prompt-fonti/D - loop glossario.md` | il mini-loop glossario | `tools/glossario/`, agente `redattore-glossario` |
| `prompt-fonti/E - loop 4 …`, `REDTEAM.md`, `REVISIONE.md` | giri successivi di verifica e red team | non portati: troppo per un essay |
| `glossario/` | istruzioni del redattore e `lint.py` | `tools/glossario/lint.py` |
| `tools/ingest.py`, `gap.py`, `resync.py` | Excel → `nodes.json`, gap report, regimi | `tools/scaletta/leggi_scaletta.py` |
| `tools/ctx.py` | contesto renderizzato per il writer | `tools/stesura/ctx.py` |
| `tools/lint_*.py`, `ledger_renumber.py` | i lint deterministici | `tools/stesura/verifica.py` |
| `tools/assemble.py` | assemblaggio nel template d'ateneo | `tools/word/assemble.py` |
| `tools/comprimi.py`, `stima_pagine.py`, `conta_pagine.py` | compressione e stima pagine | non portati: su un essay basta il conteggio parole |
| `agenti/node-writer.md` | il writer di nodo | agente `section-writer` |
| `agenti/claim-auditor.md` | anti-invenzione | agente `claim-auditor` |
| `agenti/citation-auditor.md`, `chapter-auditor.md` | citazioni, ridondanza fra capitoli | assorbiti in `claim-auditor` e `verifica.py` |
| `agenti/bibliography-builder.md` | risoluzione citazioni | `tools/bib.py` (deterministico) |
| `agenti/final-check.md` | controllo del Word | `tools/word/controlla_docx.py` |
| `agenti/prose-auditor.md`, `fix-applier.md` | lingua, correzioni locali | stessi nomi |
| `agenti/front-back-matter.md`, `table-inserter.md` | abstract/introduzione, matrici del Cap. 5 | non portati: l'introduzione è una sezione della scaletta |
| `skill/tesi-*` | i comandi della tesi | `/essay-*` |
| `skill/tesi-slop/references/` | libreria anti-slop | `.claude/skills/essay-slop/` |
| `revisione-da-word/` | pipeline di revisione partendo dal Word finito (regola sovrana rovesciata) | non portata: per un lavoro di revisione, parti da qui |
