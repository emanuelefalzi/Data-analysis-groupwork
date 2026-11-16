# Redigere paper LaTeX — come si usa

Trasforma `scaletta.md` nel paper finale in LaTeX: corpo ≤ 20 pagine con figure e tabelle,
poi References e Appendix A (dataset). Regole per Claude in `CLAUDE.md`, perché di ogni pezzo in
`PROCESSO.md`.

**Stato (16/11/2026): prima versione della skill.** Script e skill funzionano su una prova; non
è stata ancora scritta nessuna sezione. `input/piano.md` e `input/appendice-A.md` sono proposte.

## Prima di partire, il gruppo decide

1. **La scaletta** (`../scaletta.md`, oggi draft v0) e le riformulazioni proposte dalla routine
   di validazione (`../routine validazione fonti/proposte riformulazione.md`).
2. **Il piano** (`input/piano.md`): pagine per sezione e quali figure/tabelle entrano nel corpo.
   Il paper v4 ha 34 pagine, 21 figure e 14 tabelle: in 20 pagine ne entrano circa 14.
3. **Titolo e autori** in `latex/main.tex`.

## Poi, in ordine

Apri Claude Code **in questa cartella** (così gli agenti e le skill si caricano) e:

| Comando | Cosa fa | Il gruppo cosa fa |
|---|---|---|
| `/paper-avvio` | controlla requisiti, legge scaletta e piano, elenca fonti non citabili e sezioni corte | decide i buchi |
| `/paper-floats` | figure e tabelle in LaTeX; scrive le tabelle di testo | approva tabelle di testo e didascalie |
| `/paper-appendice` | contratto di Appendix A da `construction.pdf` | approva il contratto |
| `/paper-scrivi` | una sezione alla volta, controllata (pilota 5.1) | **approva il pilota** |
| `/paper-controlla` | auditor, correzioni, escalation | decide le escalation |
| `/paper-latex` | assembla, compila, conta le pagine | rilegge il PDF |

`/paper-stato` in qualunque momento. `/paper-latex --bozza` dà un PDF di lavoro con i buchi in rosso.

## Requisiti

`python3`, LibreOffice (`soffice`), `pdftotext`, e LaTeX con biber:

```bash
apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra biber latexmk lmodern
```

Su Mac: MacTeX (ha già tutto) e LibreOffice. La cartella `latex/` dopo `/paper-latex` si può
caricare su Overleaf così com'è.
