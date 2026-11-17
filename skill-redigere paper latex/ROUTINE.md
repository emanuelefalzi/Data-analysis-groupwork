# Routine «redigere paper» — da un prompt al PDF

Si lancia dalla **radice della repo**, su qualunque computer, con un solo prompt:
**«lancia redigere paper»**. Il Claude che la riceve segue questo file dall'inizio alla fine
**senza chiedere conferme** (RULES.md: «do what was asked without asking again»). Si ferma
solo per ciò che solo un umano può fare (una password di amministratore). Tutto il resto lo
fa, lo verifica, lo corregge e lo rilancia da solo.

`<R>` = percorso assoluto di `skill-redigere paper latex/`. `py` = l'interprete Python 3
(`python3` su Mac/Linux, `py -3` o `python` su Windows). Gli script usano solo la libreria
standard: nessun `pip install`.

Prima di partire leggi `<R>/CLAUDE.md` (regole) e, se serve il perché, `<R>/PROCESSO.md`.

---

## 0. Repo aggiornata

`git pull --rebase` (RULES.md, Git). Se il pull porta un conflitto su un file binario, fermati
e chiedi (RULES.md): è l'unico caso in cui la routine si interrompe per una domanda.

## 1. Requisiti (una volta per computer)

1. `py --version` (≥ 3.9).
2. `pdflatex --version`. Se manca, installa LaTeX secondo il sistema:
   - **Linux (Debian/Ubuntu)**: `sudo apt-get install -y texlive-latex-recommended
     texlive-latex-extra texlive-fonts-recommended texlive-pictures texlive-bibtex-extra biber lmodern`
     (senza `sudo` se sei root).
   - **macOS**: se c'è Homebrew, `brew install --cask mactex-no-gui` (completo, ~5 GB) oppure
     `brew install --cask basictex` e poi `sudo tlmgr update --self && sudo tlmgr install
     collection-latexextra collection-fontsrecommended biblatex biblatex-apa biber lm`.
     `sudo` chiede la password del Mac: **non puoi darla tu**. Scrivi all'utente il comando esatto
     da incollare nel Terminale, aspetta che dica «fatto», poi riprendi da qui.
   - **Windows**: `winget install MiKTeX.MiKTeX` (MiKTeX installa da solo i pacchetti mancanti
     alla prima compilazione; se chiede conferma, rispondi sì nelle impostazioni di MiKTeX:
     «Always install missing packages»). Riapri il terminale perché `pdflatex` entri nel PATH.
   - Dopo l'installazione: `pdflatex --version` di nuovo. Se in PATH su Mac manca, aggiungi
     `/Library/TeX/texbin`.
3. `biber --version`: se manca va bene lo stesso. `tools/assemble.py` controlla se ci sono
   biber e `biblatex-apa`; se no usa natbib + bibtex (stile apalike, author–year). Il PDF esce
   comunque.
4. **Se LaTeX non si riesce a installare** (nessun permesso, nessuna rete): fai tutto il resto
   (stesura e controlli), esegui `assemble.py` e consegna la cartella `<R>/latex/` da caricare su
   Overleaf (Menu → Compiler pdfLaTeX; contiene già `gen/` e `figures/`). Dillo chiaramente.

## 2. Preparazione (deterministica)

```
py "<R>/tools/tabelle_testo.py"
py "<R>/tools/leggi_scaletta.py"
py "<R>/tools/floats.py"
py "<R>/tools/piano.py"
```

- `tabelle_testo.py` costruisce e controlla le 7 tabelle testuali (`4. risultati/tables testuali/`,
  vedi il suo README) e scrive `tracciabilita.md`. **Deve uscire senza errori.** Se una riga del
  log citata non contiene più il numero (do-file rilanciato), cerca il numero nel log nuovo e
  aggiorna il riferimento nel `.md`; se il numero è cambiato, il numero nuovo vince (RULES.md),
  aggiorna la cella e segnalalo nel report finale. Mai togliere una fonte per far passare il controllo.

- `leggi_scaletta.py` → `build/sezioni.json`. Segnala fonti non in `fonti.bib` e sezioni corte:
  annotali per il report finale, non fermarti.
- `floats.py` → deve dire **35 floats nel corpo (21 figure, 14 tabelle)** e nessun «⚠ … da
  scrivere» o «assente». Se un file manca (es. `figures.zip` cambiato), correggi il piano solo se
  è un nome di file cambiato; se un float non esiste più, segnalalo nel report e vai avanti.
- Se uno script fallisce con un errore di codice: leggi il traceback, correggi lo script in
  `<R>/tools/`, rilancia. È parte della routine (Lele, 17/11: «se non va lo correggi e lo rilanci»).

## 3. Stesura (sequenziale, una sezione alla volta)

L'ordine è quello di `build/sezioni.json` (salta le sezioni con `contenuto` vuoto: sono solo
titoli). Per **ogni** sezione:

1. `py "<R>/tools/ctx.py" <id>`.
2. Subagent **con `model: "sonnet"` esplicito**. Gli agenti di `<R>/.claude/agents/` non sono
   caricati quando la sessione parte dalla radice: usa un subagent generico e passagli come
   istruzioni il testo intero di `<R>/.claude/agents/paper-writer.md`, più il prompt
   «Scrivi la sezione <id>. Radice del progetto: <R>.».
3. `py "<R>/tools/verifica.py" <id>`. Con HIGH: rilancia il writer sulla stessa sezione con
   l'output della verifica (massimo 3 giri). Se dopo 3 giri resta un HIGH, annotalo e vai avanti.
   **Non correggere tu la prosa.**

**Pilota: 5.1 per prima.** Dopo la 5.1, leggi tu DRAFT e verifica e controlla registro, numeri
con identità (coefficiente / odds ratio / AME, p-value, campione), verdetti con le parole del
paper, richiami a tabelle e figure. Se qualcosa non va come regola generale, aggiungi una riga
alle istruzioni che passi ai writer successivi (non a `paper-writer.md`) e riscrivi la 5.1.
Poi le altre in ordine dalla 1. **L'abstract per ultimo** (`ctx.py abstract`).

## 4. Controlli

1. `py "<R>/tools/verifica.py" --tutte`.
2. Claim-auditor: subagent `model: "sonnet"` con le istruzioni di
   `<R>/.claude/agents/paper-claim-auditor.md`, a gruppi di 3–4 sezioni contigue.
3. Ogni finding: sostituzione locale → subagent sonnet con
   `skill-redigere essay/.claude/agents/fix-applier.md`; riscrittura → paper-writer; decisione di
   merito (taglio, fonte, numero non tracciabile, letteratura non attribuita) →
   `<R>/reports/escalation.md`, **non bloccante**: si chiude nel report finale per il gruppo.
4. Un prose-auditor sul documento intero (subagent sonnet con
   `skill-redigere essay/.claude/agents/prose-auditor.md` e
   `skill-redigere essay/.claude/skills/essay-slop/references/pattern-anti-slop.md`).
5. `verifica.py --tutte` di nuovo dopo le correzioni.

## 5. LaTeX e limite di pagine

```
py "<R>/tools/assemble.py"          # se rifiuta per buchi aperti: py ... --bozza
py "<R>/tools/compila.py"
```

- Il PDF va in `5. paper e documentazione di percorso/paper_group21_v5.pdf`.
- **Corpo > 20 pagine**: i floats restano tutti (decisione di Lele). Abbassa la colonna `pagine`
  di `input/piano.md` per le sezioni con più prosa (le parole obiettivo si ricalcolano da sole:
  pagine − floats, per `parole_per_pagina`), rilancia `leggi_scaletta.py` e chiedi ai writer di **comprimere** quelle sezioni senza
  togliere affermazioni; poi di nuovo 4.1 e 5. Massimo 2 giri; se sfora ancora, consegna e di'
  di quante pagine e quali affermazioni andrebbero tagliate (decide il gruppo).
- Riferimenti non risolti, overfull grossi, errori di compilazione: correggi la causa
  (tabella di testo, didascalia, token) e ricompila.
- Guarda il PDF (2–3 pagine con floats, rese come immagini): float lontani dal richiamo o
  pagine mezze vuote si segnalano nel report.

## 6. Consegna

1. `py "<R>/tools/stato.py"`.
2. Commit **su `main`** (RULES.md): `git pull --rebase`, poi commit dei DRAFT (`<R>/sezioni/`),
   dei report, del PDF e di eventuali correzioni agli script; messaggio
   «paper v5: draft from scaletta (Claude for <nome>)»; `git push`.
3. Report all'utente (italiano, con contesto completo, niente ID nudi): pagine del corpo,
   sezioni corte o compresse, buchi `[[GAP]]` rimasti e perché, escalation, fonti non citabili,
   cosa è stato corretto negli script durante il giro.
