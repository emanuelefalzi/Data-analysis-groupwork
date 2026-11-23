# Escalation al gruppo — paper v5 (23/11/2026)

Stato: tutte le 28 sezioni e l'abstract sono scritti. Le bozze di 6.2, 6.3, 6.4, 7, l'abstract e le riscritture di 2.1, 2.2, 2.4, 2.5, 4.1, 5.1, 5.2, 5.4, 5.5 e 5.6 vengono da ChatGPT (manuale), con correzioni locali di Claude. `verifica.py --tutte` non dà nessun HIGH.
PDF di bozza: `5. paper e documentazione di percorso/paper_group21_v5_bozza.pdf`, compilato con tectonic perché pdflatex non è installato. I GAP sono evidenziati.

## 1. Limite di pagine: il corpo è di 22 pagine, il massimo è 20
- Ho già tolto la prosa ridondante. In particolare la 5.4 è scesa da 863 a circa 610 parole: i numeri che sono già nelle tabelle T10–T12 e B1–B4 non si ripetono più nel testo.
- Il resto dell'eccesso dipende soprattutto da dove LaTeX piazza i floats. Le pagine 8–9 contengono solo le figure 2–10, e le pagine 12 e 14 sono mezze vuote.
- Opzioni (decide il gruppo, CLAUDE.md regola 7):
  - (a) Spostare in Appendix B alcune figure descrittive (per esempio Figures 2–6 o 9–10). Si cambia `dove` in `input/piano.md`.
  - (b) Rimpicciolire le figure dei pannelli descrittivi, mettendone due per riga.
  - (c) Comprimere ancora 2.5 (389 parole contro 170), 5.2, 5.3, 2.4 e 2.2. Si guadagna circa mezza pagina.
  - (d) Accettare 21–22 pagine.

## 2. GAP aperti (servono una fonte o una decisione)
- 2.1: una fonte sul legame fra segnali positivi rapidi e rifinanziamento più veloce.
- 2.4: una fonte che colleghi le azioni senior alla sovrastima del post-money.
- 2.5: le prove che i CVC acquisiscono le startup che finanziano.
- 5.5: i collegamenti specifici fra CVC come acquirente, reti VC, angel group, acceleratori ed exit.

## 3. Rilievi da decidere
- Abstract e 7 ¶5. La «growth per year» esiste solo come mediana grezza (Figure 19) e la sezione 7 la tratta come estensione aperta. Dall'abstract l'ho tolta: resta da decidere se 5.3 ¶3 la presenta come descrittiva.
- 2.1-06: H1 viene ripetuta nel testo e anche nella Tabella 1.
- Restano i rilievi low elencati in `claim-riscritture.md` e in `claim-6.2-6.3-6.4-7-abstract.md`. Sono rimasti aperti anche quelli di gruppo dei report precedenti: 3.3-02/03, 4.1-02, 5.2-04/05, 5-01.

## 4. Tecnico
- 3.2 cita lo schema TikZ F1 con `[[TAB:F1]]`, che rende «Table ??». Con `[[FIG:F1]]` invece `verifica.py` segnala «tipo sbagliato (figura-testo)». Va corretto il controllo dei tipi in `verifica.py`, oppure il token di assemble per `figura-testo`.
- `compila.py` richiede pdflatex. Su questo Mac c'è solo tectonic: o si installa MacTeX/BasicTeX, o si aggiunge a compila.py un fallback su tectonic.
