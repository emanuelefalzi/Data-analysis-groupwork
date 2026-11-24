# Tables testuali

Le 7 tabelle del paper che il do-file non produce: Tables 1, 2, 3, 4, 7, 13 e 14 del paper v4
(le altre 7 vengono da `../RQ1_tables.doc` e `../RQ1_tables_not_in_log_checks.rtf`).

| File | Tabella del paper | Fonti principali |
|---|---|---|
| `T1.md` | 1 · Hypotheses and competing predictions | scaletta 2.1–2.4 |
| `T2.md` | 2 · Round-1 controls and expected signs | scaletta 2.5; paper v4 Table 2 per i segni che la scaletta non dice |
| `T3.md` | 3 · Sample construction | `2. dataset/construction.txt` (Table 2), log righe 150–153 |
| `T4.md` | 4 · Variable definitions | `construction.txt` (Table 6), `glossary.md` |
| `T7.md` | 7 · Average marginal effects | log righe 688–732 (exit), 1451–1492 (failure) |
| `T13.md` | 13 · Summary of the hypotheses | log righe 567, 570, 1330, 2920; formule dei verdetti di RULES.md |
| `T14.md` | 14 · Estimates against the literature | log, tabelle del do-file 2, 3, 6, scaletta 5.5 |

## Come funziona la tracciabilità

**Si modifica solo il `.md`.** Ogni cella del corpo dichiara la sua fonte fra graffe:

    | H1: longer gap, less exit {scaletta 2.1} | −0.071 (p = 0.29) {log L546} | Right sign, not significant {rules} |

`skill-redigere paper latex/tools/tabelle_testo.py` legge i `.md`, controlla ogni cella e scrive
`<id>.tex` (usato dal paper) e `tracciabilita.md` (una riga per cella: valore, fonte, esito).
Se un controllo fallisce esce con errore e il paper non si compila.

| Fonte | Controllo |
|---|---|
| `{log L546}` | la riga 546 di `3. stata/regression_analysis.log` contiene ogni numero della cella, con lo stesso arrotondamento |
| `{checks L123}` | idem su `not_in_log_checks.txt` |
| `{rtf main:2}`, `{rtf checks:12}` | ogni numero è una cella di quella tabella del do-file |
| `{construction L127}` | la riga di `2. dataset/construction.txt` contiene numeri e nomi `in_codice` |
| `{scaletta 2.3}` | la sezione esiste, contiene i numeri; ogni `[cite: chiave]` sta nel suo blocco Sources e in `fonti.bib` |
| `{glossary}` | `glossary.md` contiene i nomi `in_codice` |
| `{rules}` | la cella è una delle tre formule dei verdetti |
| `{paper T2}` | fonte secondaria (tabella del paper v4): **non controllabile**, contata nel report |

Se il do-file viene rilanciato e le righe del log si spostano, lo script lo segnala: si cerca il
numero nel log nuovo e si aggiorna il riferimento nel `.md`.

`2. dataset/construction.txt` è il testo di `construction.pdf` (`pdftotext -layout`, 17/11/2026):
se il PDF cambia, va rigenerato.
