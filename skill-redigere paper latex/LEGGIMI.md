# Redigere paper LaTeX — come si usa

Trasforma `scaletta.md` nel paper finale in LaTeX: corpo ≤ 20 pagine con tutte le 21 figure e
le 14 tabelle del paper v4, poi References e Appendix A (dataset). Regole per Claude in
`CLAUDE.md`, il perché di ogni pezzo in `PROCESSO.md`, i passi esatti in `ROUTINE.md`.

## Un prompt solo

Da qualunque computer, apri Claude Code nella **radice della repo** e scrivi:

> lancia redigere paper

Claude aggiorna la repo, installa LaTeX se manca (su Mac può chiederti di incollare un comando
con `sudo` nel Terminale), scrive le sezioni una alla volta con un agente Sonnet, le controlla,
corregge, compila e mette il PDF in
`5. paper e documentazione di percorso/paper_group21_v5.pdf`, poi fa commit su `main`.

## Cosa serve sul computer

- **Python 3** (nessun pacchetto in più).
- **LaTeX con `pdflatex`**: TeX Live (Linux), MacTeX o BasicTeX (Mac), MiKTeX (Windows). biber e
  biblatex-apa sono facoltativi: senza, la bibliografia esce con natbib (author–year).
- Se LaTeX non si può installare, la cartella `latex/` si carica su Overleaf così com'è.

## Cosa è già deciso (17/11/2026)

- Pagine per sezione e posizione dei floats: `input/piano.md` (Claude, su mandato di Lele).
- Tabelle e figura «di testo» (T1–T4, T7, T13, T14, Figura 1): `latex/testo/`, ricostruite dalla
  scaletta aggiornata e dal log.
- Appendix A: `5. paper e documentazione di percorso/appendix A - dataset construction.md`.
- Titolo e sottotitolo: `progetto.json` (`titolo`, `sottotitolo`).

Le skill `/paper-*` funzionano solo se Claude Code parte da questa cartella; dalla radice vale
il prompt sopra.
