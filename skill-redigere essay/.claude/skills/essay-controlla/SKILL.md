---
name: essay-controlla
description: Fase 7 — controlli e correzioni. Lint deterministici su tutto l'essay, claim-auditor (una o due istanze), fix-applier sulle correzioni locali, prose-auditor sul documento intero, ed escalation all'autore di cio' che solo lui puo' decidere. Usala dopo /essay-scrivi e dopo ogni riscrittura importante.
---

# /essay-controlla

1. **Lint**: `python3 "<radice>/tools/stesura/verifica.py" --tutte` (con l'antiplagio a 8 parole
   contro tutti i testi delle fonti). Gli HIGH tornano al `section-writer` prima di andare avanti.
2. **claim-auditor**: se `doppio_auditor` e' false, una istanza su tutte le sezioni (report
   `reports/claim-tutte-A.md`). Se e' true, **due istanze in parallelo, in contesto pulito, che
   non si vedono** (`-A`, `-B`): i finding su cui concordano passano; sui discordi arbitri tu, e
   scrivi `reports/arbitraggio-claim.md` con la ragione di ogni scelta. Nel dubbio rileggi il
   materiale, non il LEDGER. (Nella tesi un'istanza ha segnalato sei frasi di cerniera legittime:
   respinte in arbitraggio. L'altra ha trovato connettivi che la prima non vedeva.)
3. **Instradamento** di ogni finding:
   - sostituzione locale (verbo, connettivo, token, termine) → `fix-applier` con quel report;
   - riscrittura di paragrafo → `section-writer` sulla sezione, con i finding;
   - **«letteratura non attribuita»**, claim da ritirare, materiale mancante, ogni «Chi lo risolve:
     autore» → `reports/escalation.md`. Non lo risolvi tu.
4. Rilancia `verifica.py --tutte`; se ci sono state riscritture, un nuovo giro di claim-auditor
   solo su quelle sezioni.
5. **prose-auditor**, una volta, sul documento intero → `fix-applier` con il suo report.
6. **Escalation all'autore**: presenta `reports/escalation.md` piu' tutti i `[[GAP:]]` e
   `[[CIT-NEEDED:]]` ancora aperti. Ogni voce si chiude solo con una decisione sua: fonte trovata
   (si torna a /essay-fonti e /essay-estrai per quella fonte), claim ritirato, o dichiarato come
   ragionamento proprio. Applichi la decisione, poi ricontrolli quella sezione.

Prossima fase: `/essay-word`, quando non restano buchi aperti (o l'autore vuole una bozza).
