# Prompt: portare nel do-file i numeri che oggi non sono nel log

Da incollare in una nuova chat di Claude Code aperta sul repo `emanuelefalzi/Data-analysis-groupwork`. Scritto il 17/11/2026 su decisione di Lele (open point 17). L'esito si registra in `registers/changelog.md`.

---

Ciao. Lavori nel repo del Gruppo 21 (21072 Data Analysis, Bocconi). Prima di qualsiasi altra cosa leggi e segui `CLAUDE.md` e `RULES.md`: lavoro su `main`, `git pull --rebase` prima di iniziare e prima di ogni push, subagenti solo Sonnet, linguaggio da associazione e mai causale, nessun numero inventato.

## Obiettivo
Alcuni numeri del paper v4 (`5. paper e documentazione di percorso/paper_group21.pdf`) sono stati calcolati fuori dal do-file, in Python o a mano, quindi **non compaiono nel log Stata** `4. risultati/regression_analysis.txt`, che per le regole è la fonte primaria di ogni numero. Il gruppo ha deciso di aggiungere queste analisi al do-file principale `3. stata/rq1_two_group_analysis_v2.do`, così che dopo un nuovo run ogni numero sia nel log con un numero di riga.

**Non aggiungere** il wild cluster bootstrap (`boottest`): Lele ha deciso il 17/11 di non farlo.

## Vincoli sul codice
1. **Aggiungi solo in fondo**, in una nuova sezione `* 8. ADDITIONS FOR TRACEABILITY (17/11/2026)` messa subito prima di `log close`. Non modificare né spostare le righe esistenti. Il motivo: `registers/results register.md` cita il log per numero di riga (per esempio L1463, L2584). Se l'output delle sezioni 1–7 resta identico, quelle righe non si muovono. Se per un motivo tecnico devi toccare codice esistente, fermati e chiedi.
2. Usa le stesse convenzioni del file: i global `$X` (controlli al round 1) e `$FE` (effetti fissi year-quarter, settore, stato), il campione `if full_window == 1` per i modelli di exit e failure, e `vce(cluster sector_year_id)`, cioè errori correlati tra startup finanziate nello stesso settore e anno del round 1. Le eccezioni sono indicate qui sotto.
3. Ogni blocco deve **stampare nel log** i numeri che il paper riporta: una tabella con `tabstat`/`table`/`estimates table`, non solo un grafico. Dove il paper ha una tabella o una figura, aggiungi anche l'export: `esttab ... using "RQ1_tables.rtf", append $TAB` per le tabelle e `graph export figures/d9_....png, replace width(2000)` per le figure, con lo stesso stile `$LOOK`.
4. Commenti in inglese, brevi, nello stile del file. Niente parole causali ("effect of the gap" va evitato nei nuovi commenti).

## Cosa aggiungere (con i numeri del paper da confrontare)

**A. Tabella 12: controlli su team ed età del lead investor.** Porta dentro il contenuto di `3. stata/rq1_addon_extra_controls.do`: merge con `pitchbook_course.dta` (da `0. dati iniziali/pitchbook_course.dta.zip`, da scompattare nella cartella di lavoro di Stata), poi le variabili `ln_founders`, `MBA`, `Has_Core_AI_Term`, `young_lead` (lead con meno di 6 anni al round 1) e `lead_age_miss`. Stima i quattro logit (exit e failure, ognuno sullo stesso campione con dati sui founder, senza e con i controlli extra) ed esporta la Tabella 12 con `esttab`. Usa `preserve`/`restore` o variabili con nomi nuovi, così i blocchi successivi non cambiano. Numeri del paper (§5.4, Tabella 12): exit β1 = −0.100 in entrambe le colonne e β3 = −0.035; failure β1 da −0.231 a −0.229; young lead −0.334 su exit (odds ratio 0.72); AI −0.607 su failure; 41 cluster.

**B. Figura 8: exit / failure / still private entro 5 anni, per quintile del gap.** Campione `full_window == 1`. Startup a due round per quintile di `gap_months` (usa `gap_q`, già creata nel do-file, circa 895 per quintile) e startup a un round come confronto. Le 14 startup con data di exit e di failure entrambe nella finestra si contano come exit. Stampa le quote e fai il grafico a barre impilate. Numeri del paper: exit tra 21% e 24% nei quintili; failure dal 14% (più veloci) al 9% (più lenti); still private dal 64% al 69%; startup a un round 16% / 32% / 53%.

**C. Figura 17: binned scatter Frisch–Waugh–Lovell.** Startup a due round in `full_window == 1` (N = 4,483). Con `regress` residualizza su `$X $FE` sia `exit_5y` e `failure_5y` sia il gap (`log_gap`), poi riaggiungi la media campionaria. Fai 20 bin di uguale numerosità del gap residualizzato, con medie per bin e retta OLS su tutte le osservazioni. Stampa le due pendenze (`regress` dei residui). Paper: pendenza failure −0.030, exit −0.011. Attenzione: −0.030 coincide con il β3 del modello di failure (log L1308), quindi il run deve dire quale sia il numero giusto per la pendenza.

**D. Figura 19: step di valutazione totale e per anno, per quintile del gap.** Startup a due round con entrambe le post-money e gap ≥ 1 mese (paper: N = 7,514; nota che questo campione **non** è ristretto a `full_window`, come il modello H3). Quintili del gap calcolati in questo campione. A sinistra la media di `log_delta_v` con IC 95%; a destra la mediana di `log_delta_v / (gap_months/12)` con il range interquartile. Stampa anche il gap mediano per quintile. Paper: totale piatto a circa 1.06–1.08 nei primi quattro quintili e 1.18 nel più lento; mediana per anno da 1.89 (quintile più veloce, gap mediano 7 mesi) a 0.36 (più lento, 35 mesi).

**E. I check ulteriori della §5.4**, sempre sulla specificazione H2, cioè il modello `exit_h2`:
- E1. Hype a livello settore × trimestre: `heat_quarter` al posto di `heat`, cluster `sector_quarter_id` (paper: 149 cluster).
- E2. Hype a livello industry-group PitchBook × anno (42 gruppi, 191 cluster) e industry-group × trimestre (575 cluster). **Queste variabili non sono nel dataset.** Vanno costruite come `heat` (quota dei dollari VC del gruppo nell'anno o trimestre, z-score dentro il gruppo) da `pitchbook_course.dta` e `Deal.csv`. Il codice originale era in Python e non è nel repo. Se non riesci a ricostruirle in modo verificabile, **non inventare**: scrivilo e lascialo come open point.
- E3. Controllo per la quota del settore su tutte le exit durante la finestra della startup (paper: β3 = −0.035, p = 0.62). Non c'è nel dataset; stessa regola di E2.
- E4. Errori robusti invece che clusterizzati: `vce(robust)` (paper: p di β3 0.36 contro 0.35).
- E5. Togli le 367 startup a un round che hanno avuto exit o failure entro 13 mesi dal round 1 (usa `months_to_outcome`; verifica che il conteggio sia 367) (paper: β1 −0.065, β3 −0.056).
- E6. VIF: `regress` (LPM) della specificazione H2 poi `estat vif`, prima con il gap non centrato e poi con il gap centrato (paper: controlli sotto 2; R, gap e interazioni tra 10 e 19, sotto 2.5 dopo la centratura).
- Per E1–E6: β3 è il coefficiente di `c.log_gap_r2#c.heat` (gap × hype, che testa H2), β1 è quello di `log_gap_r2`. Raccogli tutto con un `estimates table ..., keep(log_gap_r2 c.log_gap_r2#c.heat) b se p stats(N)`.

**F. N degli AME.** Gli effetti marginali medi del modello di exit usano N = 4,444 startup a due round (log L659), non 4,483. Aggiungi un `count if e(sample) & two_rounds == 1` dopo `exit_h2` e, se c'è una differenza, un breve controllo di quali osservazioni escono (probabilmente categorie che predicono perfettamente l'outcome). Serve per la nota della Tabella 7.

## Dopo aver scritto il codice
1. **Stata non è disponibile nel container cloud.** Controlla con cura la sintassi riga per riga e verifica che ogni variabile usata esista in `2. dataset/dataset.dta` (puoi leggerlo con pandas). Il file va lanciato da un membro del gruppo con Stata 17, rinominando il dataset in `group_21_dataset.dta` (vedi le incongruenze note in RULES.md). Scrivi nel messaggio finale istruzioni passo passo per chi lancia il file.
2. Fai commit e push del solo do-file, con una riga in `registers/changelog.md` nello stesso commit (formato in RULES.md, sezione *Changes to `scaletta.md`*). Messaggio di commit, per esempio: `do-file: section 8, traceability additions (Claude for Lele)`.
3. Prepara una tabella "numero del paper → riga del log attesa" da completare dopo il run. **Non** modificare `regression_analysis.txt`, `RQ1_tables.doc`, `results register.md` o `scaletta.md` finché non c'è il nuovo log.

## Dopo il run (quando qualcuno carica il nuovo log)
- Sostituisci `4. risultati/regression_analysis.txt` con il nuovo log, rinominato. Prima controlla con un diff che le righe delle sezioni 1–7 siano identiche alla versione precedente. Se si sono spostate, fermati e avvisa Lele: le righe citate nel registro vanno rifatte.
- `RQ1_tables.doc` è un file binario: avvisa il gruppo prima di sovrascriverlo.
- Aggiorna `registers/results register.md` (le righe oggi marcate "not in log": R-15, R-32, R-37, R-45, R-46 e le altre segnalate nella sezione note) con i numeri di riga nuovi. Dove il log non coincide con il paper, **vince il log**: scrivi la differenza in `registers/open points.md` e non correggere in silenzio la scaletta.
- Chiudi gli open point 5, 9, 14 e 17 scrivendo l'esito e la data, oppure lasciali aperti per quello che non è stato possibile (per esempio E2 ed E3).
- Ogni modifica va in `registers/changelog.md`.
