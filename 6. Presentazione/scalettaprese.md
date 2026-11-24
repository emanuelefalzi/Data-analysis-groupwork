---
title: "Scaletta del deck v9, Group 21"
date: 2026-11-23
bibliography: ../fonti/fonti.bib
---

# Scaletta del deck v9

Cos'è: la scaletta di `6. Presentazione/group21_deck_v9.pptx` (44 slide), slide per slide, nello stesso ordine e con gli stessi contenuti del deck. Non riscrive e non aggiunge niente: testi, numeri e fonti sono quelli delle slide (il deck non ha note del relatore). Data: 23/11/2026.

Come si legge:
- le citazioni `[@chiave]` rimandano a `fonti/fonti.bib` (si risolvono con pandoc, `--citeproc`);
- "log Lxxx" = riga di `3. stata/regression_analysis.log` (log del 23/11; rinumerate dal log del 20/11 il 24/11); "add-on Lxxx" = riga di `4. risultati/not_in_log_checks.txt`. Le righe sono quelle citate nel deck, controllate a campione sul log attuale;
- le figure nel pptx sono immagini senza nome di file: il nome (d1, m2, n3...) è quello scritto nella fonte a piè di slide.

Sezioni del deck (barra in alto): 1 Question › 2 Data › 3 Descriptives › 4 Hypotheses › 5 Robustness › 6 Causality.

---

## Slide 1: Fundraising speed as a quality signal, tested against the VC cycle

- Sottotitolo: "Is a slow second VC round a bad sign? Evidence from 28,478 US startups, 2012–2019". Group 21 · 21072 Data Analysis · Data Lab for Entrepreneurship, Bocconi 2026/27.
- Research question: is the time between the first and the second VC round associated with the probability of exit, and does this association differ between hot and cold funding markets?
- Quattro blocchi: Gap (months, round 1 → 2) · Exit / failure (within 5 years) · Valuation step (post-money r2 / r1) · Market hype (hot vs cold sector); etichette H1 · H1b, H2, H3.
- Piè di slide: PitchBook course extract · logit with round-1 controls and fixed effects · associations, not causal effects.

Fonti: dati PitchBook (course extract).

## Slide 2: Four testable hypotheses: speed should go with exit, and hot markets should blur the signal

- H1 · Gap → exit: a longer gap goes with a lower probability of exit within 5 years; predicted β1 < 0. Competing: a slow round can reflect patient building (β1 ≥ 0).
- H1b · Gap → failure: a longer gap goes with a higher probability of failure within 5 years; predicted β1 > 0. Competing: slow raisers are survivors (β1 < 0).
- H2 · Gap × hype: in hot markets the negative gap–exit link is weaker; predicted β3 > 0. "The key hypothesis."
- H3 · Gap → value: a longer gap goes with a smaller valuation step from round 1 to 2; predicted θ1 < 0. OLS, two-round startups with both valuations.
- Nota: β1, β3 stimati solo tra le two-round startups; θ1 con OLS sulle two-round startups con entrambe le valutazioni.

Fonti: paper v4 §2 (`5. paper e documentazione di percorso/paper_group21.pdf`); `scaletta.md` 2.1–2.4.

## Slide 3: From 57,751 course startups to 9,263 with five fully observed years

- Funnel del campione: course extract (US, founded 2012–19) 57,751 → ≥ 1 completed deal, valid date 52,277 → ≥ 1 VC round 34,822 → gap ≤ 10 years (−1) 34,821 → no exit/failure before round 1 (−58) 34,763 → round-1 amount disclosed (−6,285) 28,478 → 5-year window fully observed 9,263.
- Regole che danno forma al campione: un round = tutti i deal VC (Seed, Early, Later Stage) di un'impresa nello stesso giorno; angel, grant, debt non sono round. Importi round-1 non dichiarati eliminati, non imputati. Round 2 dopo il 30 Jun 2022 = nessun round 2 (828). Estimation sample: 4,483 two-round + 4,780 one-round.
- Deal: completati, data valida; fine dati 30 June 2022.

Fonti: dataset construction note v4, Table 2; log L142–155.

## Slide 4: Every startup stays in: two-round startups carry the gap, one-round startups get a zero

- Schema temporale: R = 1 · two-round startup (15,518): t1, t2, gap, finestra di outcome di 5 anni; R = 0 · one-round startup (12,960): t1, finestra di 5 anni.
- Il gap esiste solo se c'è il round 2: il disegno non confronta mai una startup veloce e una lenta che non hanno raccolto di nuovo.
- Formule: Ri = 1[t2 esiste, t2 ≤ 30 Jun 2022]; gapi = (t2 − t1) / 30.44; log_gap_r2i = Ri · ln(1 + gapi).
- One-round startups hanno log_gap_r2 = 0: β1 è stimato solo tra le two-round. Gap medio 14.7 mesi (SD 9.1); ln(1 + gap) perché asimmetrico a destra: un'unità ≈ gap 2.7 volte più lungo. Round uniti per data, quindi nessun gap di 0 giorni; un gap > 10 anni eliminato.

Fonti: dataset construction note v4, Step 2; N totale 28,478; statistiche del gap sull'estimation sample, log L157.

## Slide 5: Exit and failure are counted in the same five-year window, which must be fully observed

- Formule: w0,i = t2 se Ri = 1, t1 se Ri = 0; Exiti = 1[w0 ≤ min(IPO, acquisition) ≤ w0 + 5y]; Faili = 1[w0 ≤ failure date ≤ w0 + 5y]; full_windowi = 1[w0 + 5y ≤ 30 Jun 2022]; ΔVi = post-money2 / post-money1 (H3, R = 1).
- Exit e failure sono outcome in competizione, stimati in logit separati.
- Uno 0 vuol dire "non è uscita" solo se tutti i 5 anni sono osservati: 9,263 startup (12,184 con 4 anni, 6,769 con 6).
- Grafico "Who enters the estimation sample" (asse 2012–2017–2022, fine dati 30 Jun 2022): finestra che parte nel 2013 dentro; nel 2016 dentro; dopo Jun 2017 fuori; nel 2019 fuori.
- Outcome principale exit_5y; exit at any time (senza finestra) solo robustness (sezione 5).

Fonti: dataset construction note v4, Step 3.

## Slide 6: Hype compares a sector's share of VC dollars with its own history; controls are fixed at round 1

- Moderatore M, market hype: shares,t = VC$s,t / Σ VC$t; heats,t = (shares,t − means) / SDs. Una quota, non dollari: si toglie il boom di mercato generale; z-score dentro il settore: heat = +1 è una SD sopra il normale per quel settore. Check: solo anni passati, trimestrale, quota grezza.
- Controlli X, misurati al round 1: ln(1 + round-1 amount, USD M) (dimensione e risorse all'ingresso); deal number del round 1 (deal di finanziamento fino a t1: maturità); età della startup al round 1 (year(t1) − anno di fondazione); tipo di lead investor (VC, CVC, angel, …; base: nessun lead). Effetti fissi: year-quarter di t1, settore, stato.
- Dimensione e valutazione del round 2 sono mediatori, mai controlli. La letteratura per ogni controllo è nella slide dell'equazione di ogni ipotesi.
- s = settore, t = anno del round 1; quote dai deal VC delle course startups, 2012–2022.

Fonti: dataset construction note v4, Steps 4–5.

## Slide 7: Two-round startups exit more and fail far less than one-round startups, before any control

- Tabella 1 (estimation sample, full_window = 1, N = 9,263), one round / two rounds / all (SD tra parentesi):
  - Exit within 5 years: .156 (.363) / .222 (.416) / .188
  - Failure within 5 years: .316 (.465) / .124 (.329) / .223
  - Months between rounds: — / 14.74 (9.08) / 14.74
  - ln(1 + round-1 amount): .786 (.751) / .973 (.768) / .877
  - Deal number of round 1: 1.345 (.748) / 1.307 (.663) / 1.327
  - Age at round 1 (years): 1.207 (1.142) / .872 (.891) / 1.045
  - Hype at round 1 (z): .145 (.880) / .203 (.953) / .173
  - N: 4,780 / 4,483 / 9,263
- Cosa dicono i numeri grezzi: exit 22.2% vs 15.6% (t = −8.19, p < 0.001); failure 12.4% vs 31.6% (t = 22.81, p < 0.001); le two-round startups raccolgono round 1 più grandi e sono più giovani, quindi i controlli contano; solo differenze grezze: R usa informazione successiva al round 1.

Fonti: log L157 (medie, SD); log L201, L220 (t-test a due campioni, varianze uguali).

## Slide 8: The typical second round comes after about a year; one-round startups pile up in later cohorts

- Sinistra, figura d1: mesi tra round 1 e round 2 (bin di 3 mesi), two-round startups dell'estimation sample.
- Destra, figura d2: startup per anno del round 1, per gruppo, full sample.
- Range interquartile del gap: circa 8–19 mesi (ln(1+gap) 2.24–3.02).

Fonti: figure d1, d2; IQR di ln(1+gap) log L3332.

## Slide 9: Hype moves within each sector over time; two-round startups exit more in cold and hot markets alike

- Sinistra, figura d3: heat medio (z-score dentro il settore) per settore e anno del round 1.
- Destra, figura d5: quota di exit entro 5 anni per gruppo e terzile di hype (cold / middle / hot), estimation sample, grezzo.

Fonti: figure d3, d5.

## Slide 10: Two-round startups raise larger first rounds, and exit rates differ by lead-investor type

- Sinistra, figura d7: densità di ln(1 + round-1 amount, USD M) per gruppo.
- Destra, figura d8: quota di exit entro 5 anni per tipo di lead investor (tipi con almeno 100 startup).
- Estimation sample, quote grezze, nessun controllo.

Fonti: figure d7, d8.

## Slide 11: Regressors are weakly correlated, except R with R × ln gap, which is mechanical and harmless once centred

- Figura c1: matrice di correlazione, estimation sample.
- Lettura: R e R × ln gap 0.94, per costruzione (termine del gap = 0 quando R = 0); hype quasi non correlato con il gap (0.03) e con i controlli; coppia di controlli più correlata: deal number ed età (0.31).
- Variance inflation (LPM del modello principale), non centrato / centrato: R 10.07 / 1.23; R × ln gap 10.38 / 1.13; R × ln gap × hype 17.86 / 1.10.

Fonti: correlazioni log L10633 (figura c1); VIF log L4662 (non centrati) e L4790 (gap centrato alla media delle two-round).

## Slide 12: H1: a slow second round should be bad news for exit, but theory also allows the opposite

- H1, enunciato: tra le two-round startups, un gap più lungo tra round 1 e round 2 è associato a una probabilità di exit entro cinque anni più bassa; predicted β1 < 0.
- (+) Lettura "segnale di allarme", β1 < 0:
  - lo staging è un'opzione di abbandonare le imprese i cui primi risultati deludono [@dahiya2012];
  - la convinzione dell'investitore scende in ogni periodo senza successo [@bergemann2005];
  - lo stage financing dà al VC l'opzione di abbandonare allo stadio intermedio [@cornelli2003].
- (−) Lettura opposta, β1 ≥ 0:
  - round più brevi dove il monitoraggio costa di più; un round veloce può segnalare un'impresa difficile da monitorare [@gompers1995; @tian2011];
  - i valori si vedono solo al rifinanziamento o all'exit: chi raccoglie di nuovo è selezionato [@cochrane2005; @korteweg2010];
  - i VC chiudono meno man mano che i round si accumulano [@guler2007].
- Il passaggio "round veloce = impresa più rischiosa" è un argomento nostro.

Fonti: [@dahiya2012; @bergemann2005; @cornelli2003; @gompers1995; @tian2011; @cochrane2005; @korteweg2010; @guler2007]; `scaletta.md` 2.1–2.2 (L103–108); fonti validate in `routine validazione fonti/tabella.csv` (usabile o con formulazione ristretta).

## Slide 13: H1 is a logit of exit on the group, the gap and hype, with round-1 controls and fixed effects

- Equazione: Pr(Exiti = 1) = Λ(α + ρ1Ri + β1 Ri ln(1+gapi) + β2 heats,t + γ′Xi,t1 + δyq + μs + πstate). Λ = CDF logistica · full_window = 1 · SE clusterizzati per settore × anno del round 1 (41 cluster) · H1 si testa con β1. Stessa equazione per H1b e H2.
- Tabella termine / perché è nel modello / supporto:
  - Ri: differenza di livello tra gruppi, non un effetto; scelta di disegno (`scaletta.md` 3.2).
  - Ri ln(1+gapi): pendenza del gap tra le two-round (β1); durata dei round, real options [@li2008].
  - heats,t: condizioni di mercato al round 1 (moderatore di H2); i flussi in entrata alzano le valutazioni [@gompers2000].
  - ln(1 + round-1 amount): risorse e convinzione all'ingresso; primi assegni piccoli = esperimenti [@ewens2018].
  - Deal number del round 1: finanziamento esterno precedente = più matura; finanziamento angel e sopravvivenza [@kerrlerner2014]*.
  - Età al round 1: le imprese giovani crescono in fretta ma chiudono spesso; up-or-out [@haltiwanger2013].
  - Tipo di lead investor: gli investitori selezionano e supportano in modo diverso; le imprese con CVC brevettano di più [@chemmanur2014].
  - Year-quarter FE δyq: le finestre di exit si aprono con i mercati; IPO biotech quando le valutazioni sono al picco [@lerner1994]*.
  - Sector FE μs · State FE π: differenze permanenti tra settori; il VC è locale; scelta di disegno · [@sorenson2001].
  - Cluster settore × anno: heat è comune dentro un settore-anno; clusterizzare al livello di assegnazione [@abadie2023]*.
- \* = formulazione ristretta (tabella.csv).

Fonti: [@li2008; @gompers2000; @ewens2018; @kerrlerner2014; @haltiwanger2013; @chemmanur2014; @lerner1994; @sorenson2001; @abadie2023]; logit con FE: Hill, Griffiths & Lim (2018) (non nel .bib, vedi in fondo); do-file sezione 3 (exit_h1).

## Slide 14: H1: right sign, not significant. A 2.7-fold longer gap goes with 7–9% lower exit odds

- Tabella 2, exit within 5 years, Logit (1) / Logit (2) / LPM (2):
  - Two or more rounds (R): 0.489** / 0.444** / 0.066**
  - R × ln(1 + months) β1: −0.089 (0.068) / −0.071 (0.068) / −0.012 (0.011)
  - ln(1 + round-1 amount): 0.496*** / 0.496*** / 0.083***
  - Deal number of round 1: 0.004 / 0.004 / 0.000
  - Age at round 1: 0.096*** / 0.096*** / 0.013***
  - Lead: Venture Capital: 0.328*** / 0.328*** / 0.054***
  - Lead: Corporate VC: 0.441** / 0.441** / 0.076*
  - Observations: 9,124 / 9,124 / 9,262; Pseudo R² / R²: 0.064 / 0.064 / 0.064
- SE clusterizzati · * p<0.10 ** p<0.05 *** p<0.01 · FE year-quarter, settore, stato · (2) aggiunge R × hype e gap × hype (riportati sotto H2). Logit N = 9,124: 139 oss. eliminate per predizione perfetta.
- Quanto è grande β1: odds ratio 0.931 (modello 2): gap 2.7 volte più lungo, odds di exit più basse del 7% (p = 0.294); LPM: da 8 a 19 mesi (IQR del gap) −0.94 pp, p = 0.271; AME di ln gap a hype medio −1.2 pp (p = 0.293).
- Verdetto: right sign, not significant.

Fonti: Tabella 2, `4. risultati/RQ1_tables.doc`; log L395, L575, L1026 (β1), L3399 (odds ratio), L3721–3726 (LPM sull'IQR), L711–713 (AME, exit_h2, N = 4,444).

## Slide 15: The raw picture agrees: exit is flat across gap quintiles

- Sinistra, figura n3: quote di exit entro 5 anni dall'inizio finestra per quintile di gap, estimation sample: 22.2 · 22.7 · 21.1 · 23.7 · 21.5%, contro 15.6% per le one-round.
- Destra, figura n4: two-round startups, outcome e ln gap al netto dei controlli round-1 e FE, 20 bin; pendenza dai micro-dati, SE OLS. Pendenza netta dell'exit su ln gap: −0.011 (p = 0.277). Pannello failure: vedi H1b.

Fonti: figura n3 (log L5728 ss.); figura n4 (log L5805).

## Slide 16: β1 stays small and insignificant across windows, models and controls

- Tabella check / N / β1 / p / log:
  - Main model (5 years): 9,124 / −0.071 / 0.294 / L575
  - 4-year window: 12,030 / −0.028 / 0.627 / L1703
  - 6-year window: 6,613 / −0.014 / 0.740 / L1901
  - Probit: 9,124 / −0.042 / 0.279 / L2792
  - LPM: 9,262 / −0.012 / 0.271 / L1026
  - + team & young-lead controls: 7,591 / −0.100 / 0.160 / L5219
  - Hype as raw VC share: 9,124 / −0.024 / 0.877 / L6330
- Grafico: righe di β1 per finestra (le righe di β3 sono di H2).
- Tutti i p-value sopra 0.15: nessuna specificazione rende il gap un predittore significativo dell'exit.
- β1 = coefficiente di R × ln(1+gap) nell'equazione dell'exit (coefficiente probit per il probit); modelli con quota grezza e gap al quadrato: termine lineare a vc_share = 0; gap al quadrato, check di disegno e outcome senza finestra: sezione 5.

Fonti: log L575, L1703, L1901, L2792, L1026, L5219, L6330.

## Slide 17: H1b: a slow second round should go with more failure, unless slow raisers are the survivors

- H1b, enunciato: tra le two-round startups, un gap più lungo è associato a una probabilità di failure entro cinque anni più alta; predicted β1 > 0.
- (+) Lettura failure, β1 > 0:
  - staging come opzione (H1): le imprese senza notizie vengono abbandonate, quindi un'attesa lunga dovrebbe finire più spesso in failure;
  - imprese con e senza VC differiscono nel momento in cui falliscono: il timing della failure è informativo [@puri2012].
- (−) Lettura opposta, β1 < 0:
  - i contratti ottimali tollerano il fallimento iniziale: la pazienza non è difficoltà [@manso2011];
  - le imprese di lead VC ben connessi sopravvivono più spesso fino ai round successivi [@hochberg2007];
  - argomento nostro: ogni two-round startup è sopravvissuta fino al round 2; chi raccoglie lentamente ha superato i suoi anni più deboli.
- Il passaggio della sopravvivenza è una nostra inferenza, non un risultato di una fonte. Fonti dello staging come opzione: vedi H1.

Fonti: [@puri2012; @manso2011; @hochberg2007]; `scaletta.md` 2.2 (L148–149); tabella.csv (usabile / formulazione ristretta).

## Slide 18: H1b uses the same logit with failure as the outcome; exit and failure are competing risks

- Equazione: Pr(Faili = 1) = Λ(α + ρ1Ri + β1 Ri ln(1+gapi) + β2 heats,t + γ′Xi,t1 + δyq + μs + πstate). Stesso campione, controlli, FE e cluster di H1 · H1b si testa con β1 di questa equazione.
- Cosa cambia per la failure: outcome = data di failure tra w0 e w0 + 5 anni; outcome in competizione: una startup che esce non può fallire dopo; due logit separati, quindi H1 e H1b non sono test indipendenti; le one-round falliscono 31.6% vs 12.4%: R è una differenza di livello, non un effetto.
- Controlli con una ragione specifica per la failure:
  - Età al round 1: le imprese giovani chiudono molto più spesso [@haltiwanger2013];
  - Tipo di lead investor: le imprese di lead VC ben connessi sopravvivono più a lungo [@hochberg2007];
  - Round-1 amount: autonomia finanziaria all'ingresso [@ewens2018];
  - Deal no., FE, cluster: come in H1.
- Logit N = 9,235: 28 oss. eliminate dove uno stato predice perfettamente la failure.

Fonti: [@haltiwanger2013; @hochberg2007; @ewens2018]; do-file sezione 4 (fail_h1); log L1158–1172.

## Slide 19: H1b rejected, opposite sign: a 2.7-fold longer gap goes with 21% lower failure odds

- Tabella 3, failure within 5 years, Logit (1) / Logit (2):
  - R × ln(1 + months) β1: −0.241*** (0.076) / −0.231*** (0.083)
  - 95% CI: [−0.39, −0.09] / [−0.39, −0.07]
  - p-value: 0.001 / 0.005
  - N / clusters: 9,235 / 41 in entrambi
- Odds ratio di β1 0.794: gap 2.7 volte più lungo, odds di failure più basse del 21% (p = 0.005).
- I coefficienti logit sono variazioni nelle log-odds di failure; la dimensione sulla scala delle probabilità è nella slide successiva.
- Grafico: failure predetta per mesi tra i round, cold vs hot.
- Verdetto: rejected, opposite sign.
- Pseudo R² 0.101; controlli round-1 e FE in entrambi; termini di interazione sotto H2.

Fonti: Tabella 3, `4. risultati/RQ1_tables.doc`; log L1188 (β1, modello 1), L1342 (β1, modello 2), L3547 (odds ratio).

## Slide 20: H1b in probabilities: a 2.7-fold longer gap goes with 2.4 points less failure

- Leggere il logit, scala / valore / lettura: log-odds β1 −0.231 (solo segno e significatività); odds ratio exp(β1) 0.794 (odds di failure × 0.79 per un'unità in più di ln(1+gap)); AME −2.42 pp (Pr(failure) 2.4 punti più bassa, in media sulle two-round).
- Un'unità di ln(1 + months) ≈ gap 2.7 volte più lungo (es. 7 → 21 mesi). Su un tasso base del 12.4% per le two-round, −2.4 punti è circa un quinto di failure in meno.
- AME per hype al round 1 (pp, 95% CI, p): cold (−1 SD) −2.05 [−4.6, 0.5] 0.115; average (0) −2.42 [−4.0, −0.8] 0.003; hot (+1 SD) −2.80 [−4.4, −1.2] 0.001; hot minus cold −0.75 [−3.5, 2.0] 0.600.
- Figura m5: effetto di ln gap su Pr(failure) lungo l'hype (−2…+2 SD), 95% CI: negativo a ogni livello, significativo da hype medio in su; nessuna differenza significativa tra cold e hot.

Fonti: AME dopo fail_h2, two-round startups, N = 4,469: log L3685–3687 (hype −1, 0, +1 SD), L3704–3713 (contrasto, χ²(1) = 0.28); figura m5, log L1461–1518; tasso base log L157.

## Slide 21: The negative gap–failure link survives every fixed window and the team controls

- Tabella check / N / β1 / p / log:
  - Main model (5 years): 9,235 / −0.231 / 0.005 / L1342
  - 4-year window: 12,156 / −0.285 / <0.001 / L2051
  - 6-year window: 6,757 / −0.190 / 0.026 / L2210
  - Founder sample, same model: 7,685 / −0.231 / 0.014 / L5398
  - + team & young-lead controls: 7,685 / −0.229 / 0.013 / L5570
  - Hype as raw VC share: 9,235 / −0.147 / 0.384 / L6481
- Controlli di team: team fondatori più grandi (−0.160, p = 0.001) e un termine AI (−0.607, p < 0.001) vanno con meno failure; β1 non si muove.
- Grafico: righe di β1 per finestra (le righe di β3 sono di H2).
- Modello con quota grezza: β1 è la pendenza a quota di settore 0%, fuori dai dati (media 27%): non confrontabile.
- Nessun probit o LPM per la failure nel log; gap al quadrato, check di disegno e outcome senza finestra: sezione 5.

Fonti: log L1342, L2051, L2210, L5398, L5570, L6481; controlli di team log L5596–5600.

## Slide 22: H2: when capital is abundant, raising speed should be a weaker signal of quality

- H2, enunciato: l'associazione negativa tra gap ed exit è più debole per le startup il cui round 1 è caduto in un mercato di settore hot; predicted β3 > 0.
- (+) Il capitale abbondante offusca il segnale, β3 > 0:
  - i flussi nei fondi alzano le valutazioni dei nuovi deal [@gompers2000];
  - più concorrenza tra investitori sposta il potere negoziale verso gli imprenditori [@inderst2004];
  - le startup dei mercati hot falliscono più spesso; quelle che vanno in IPO sono valutate di più [@nanda2013].
- (−) Lettura opposta, β3 < 0:
  - argomento nostro: nei mercati cold tutti aspettano, quindi un gap lungo dice poco; nei mercati hot un gap lungo vuol dire che gli investitori hanno scelto di non finanziare;
  - il VC early-stage cala molto nelle recessioni [@howell2020];
  - i VC esperti investono di più quando sale la Q del settore, senza calo significativo del successo [@gompers2008].
- Nessuna fonte testa se il gap è più o meno informativo a seconda del mercato: il ponte verso H2 e la lettura opposta sono argomenti nostri.

Fonti: [@gompers2000; @inderst2004; @nanda2013; @howell2020; @gompers2008]; `scaletta.md` 2.3 (L181–183); tabella.csv (usabile / formulazione ristretta).

## Slide 23: H2 adds two interactions; β3 measures how the gap slope changes with hype

- Equazione: Pr(Exiti = 1) = Λ(α + ρ1Ri + β1Ri ln(1+gapi) + β2 heats,t + ρ2Ri heats,t + β3 Ri ln(1+gapi) heats,t + γ′Xi,t1 + δyq + μs + πstate).
- Lettura dei coefficienti: β3 = variazione della pendenza del gap per +1 SD di hype (H2 prevede β3 > 0); β1 = pendenza del gap tra le two-round a hype medio (heat = 0); ρ2 = differenza di hype tra one- e two-round, non un effetto (R usa informazione successiva al round 1); β2 = pendenza dell'hype per le one-round.
- Si riporta l'AME del gap a hype = −1, 0, +1 SD e il contrasto hot-minus-cold, perché nei modelli non lineari il coefficiente di interazione non è l'effetto di interazione [@ai2003; @mize2019].
- Stesso campione, controlli, FE e cluster di H1; heat è z-score dentro il settore, quindi β3 usa la variazione nel tempo dentro ogni settore.

Fonti: [@ai2003; @mize2019]; do-file sezione 3 (exit_h2).

## Slide 24: H2 not supported: the gap–exit slope is, if anything, steeper in hot markets

- Gap × hype β3, Logit (2) / LPM (2): coefficiente −0.056 / −0.008; SE clusterizzati (0.059) / (0.009); p 0.344 / 0.385; odds ratio 0.946 / —.
- AME di ln gap su Pr(exit) per hype al round 1 (pp, p): cold (−1 SD) −0.25, 0.883; average (0) −1.16, 0.293; hot (+1 SD) −2.11, 0.068; hot minus cold −1.86, 0.327.
- Grafico: effetto di ln gap su Pr(exit) lungo l'hype, 95% CI.
- Verdetto: not supported.
- Logit N = 9,124, 41 cluster.

Fonti: Tabella 2, `4. risultati/RQ1_tables.doc`; log L578 (β3 logit), L3402 (odds ratio), L1029 (β3 LPM), L711–713 (AME, exit_h2, N = 4,444), L717–741 (contrasto).

## Slide 25: Predicted exit by gap barely differs between cold and hot markets, in the model and in the raw data

- Sinistra, figura m2: Pr(exit entro 5 anni) predetta per mesi tra i round, margins di exit_h2 per le two-round a heat = −1 e +1, 95% CI.
- Destra, figura d6: quota di exit grezza per quintile di gap, cold vs hot (terzile di hype basso vs alto), two-round startups, nessun controllo.

Fonti: figure m2, d6.

## Slide 26: β3 is negative in every hype measure; only past-only hype turns significant, against H2

- Tabella misura di hype / check, N, β3, p, log:
  - Main: sector × year (41 cl.): 9,124 / −0.056 / 0.344 / L578
  - 4-year window: 12,030 / −0.071 / 0.208 / L1706
  - 6-year window: 6,613 / −0.065 / 0.156 / L1904
  - Probit: 9,124 / −0.028 / 0.390 / L2795
  - Sector × quarter (149 cl.): 9,124 / −0.036 / 0.405 / L3804
  - Industry group × year (190 cl.): 9,123 / −0.070 / 0.280 / add-on L2368
  - Industry group × quarter (570 cl.): 9,124 / −0.057 / 0.368 / add-on L2740
  - Raw VC share (per pp): 9,124 / −0.002 / 0.670 / L6333
  - + team & young-lead controls: 7,591 / −0.035 / 0.602 / L5222
  - Past-only hype (27 cl.): 6,593 / −0.050** / 0.039 / L2621
  - Past-only hype, robust SEs: 6,593 / −0.050 / 0.176 / L4172
  - Main hype, past-hype sample: 6,593 / −0.062 / 0.303 / L4354
- L'unico check significativo: past-only hype, β3 = −0.050, p = 0.039, opposto a H2; campione più piccolo (6,593 startup, 27 cluster); stessa dimensione dell'hype principale su quel campione (−0.062, p = 0.303); p = 0.176 con SE robusti; con pochi cluster i test cluster-robust possono rifiutare troppo spesso [@cameron2008].

Fonti: [@cameron2008]; log L578, L1706, L1904, L2795, L3804, L6333, L5222, L2621, L4172, L4354; add-on (`not_in_log_checks.txt`) L2368, L2740, cluster L2353, L2539.

## Slide 27: H3: if speed is good news, faster second rounds should be priced at a bigger step-up

- H3, enunciato: tra le two-round startups, un gap più lungo va con uno step di valutazione più piccolo, ln(post-money2 / post-money1); predicted θ1 < 0.
- (+) Lettura "buona notizia", θ1 < 0:
  - parte del finanziamento impegnato dentro un round è condizionata a milestone [@kaplan2003];
  - le valutazioni si osservano solo al rifinanziamento o all'exit, quindi i valori osservati sono selezionati [@korteweg2010].
- (−) Lettura opposta, θ1 > 0:
  - argomento nostro (I-03, proposta, non ancora approvata dal gruppo): un gap più lungo lascia più tempo per costruire, quindi lo step totale può salire anche se il valore cresce più lentamente al mese;
  - Kaplan & Strömberg legano le milestone ai fondi dentro un round, non al timing del round successivo [@kaplan2003].
- Selezione al rifinanziamento: [@cochrane2005], vedi H1.

Fonti: [@kaplan2003; @korteweg2010; @cochrane2005]; `scaletta.md` 2.4 (L215–217); tabella.csv (usabile / formulazione ristretta).

## Slide 28: H3 is an OLS of the log step on the gap and hype, among two-round startups with both valuations

- Equazione: ln ΔVi = θ0 + θ1 ln(1+gapi) + θ2 heats,t + θ3 ln(1+gapi) heats,t + γ′Xi,t1 + δyq + μs + πstate + εi. ΔV = post-money2 / post-money1 · stessi controlli round-1 e FE di H1 · cluster per settore × anno · H3 si testa con θ1.
- Controlli con una ragione specifica per lo step:
  - Tipo di lead investor: i VC con reputazione ottengono valutazioni più basse del 10–14% [@hsu2004];
  - Year-quarter FE: i flussi nei fondi alzano le valutazioni dei deal [@gompers2000];
  - Round-1 amount: scala la post-money del round 1 (lettura nostra);
  - Deal no., età, FE: come in H1.
- Cosa misura lo step, e cosa no: la post-money sopravvaluta il fair value in media del 48% per 135 unicorni US [@gornall2020]; gli step mescolano valore e potere negoziale per tipo di VC [@heughebaert2012]; osservato per il 49% delle two-round: campione selezionato (lettura nostra).
- N = 7,574 delle 15,518 two-round startups (entrambe le post-money dichiarate), 73 cluster.

Fonti: [@hsu2004; @gompers2000; @gornall2020; @heughebaert2012]; do-file sezione 7 (val_h1, val_h2); log L3069–3073.

## Slide 29: H3 rejected, opposite sign: a 2.7-fold longer gap goes with an 11% larger step-up

- Tabella 6, ln(post-money2 / post-money1), OLS (2), coefficiente e p:
  - ln(1 + months) θ1: 0.109*** (0.020), <0.001
  - ln(1 + round-1 amount): −0.139***, <0.001
  - Deal number of round 1: −0.043***, <0.001
  - Age at round 1: −0.063***, <0.001
  - Lead: Venture Capital: 0.043**, 0.044
  - Lead: Accelerator: 0.290**, 0.014
  - N / clusters / R²: 7,574 / 73 / 0.085
- +11.5% = exp(0.109) − 1: gap 2.7 volte più lungo, step-up della post-money più grande dell'11.5%. val_h1 dà lo stesso θ1 (0.109, p < 0.001).
- Figura m9: ln step predetto per mesi tra i round, cold vs hot (margins di val_h2 a heat = −1 e +1).
- Verdetto: rejected, opposite sign.

Fonti: Tabella 6, `4. risultati/RQ1_tables.doc`; log L3080 (θ1, modello 2), L3085–3087 (controlli), L3069–3073 (N, R², cluster).

## Slide 30: Per year, fast raisers gain value faster; in total, slow raisers end slightly higher

- Sinistra, figura n2 e tabstat (two-round con ΔV > 0 e gap ≥ 1 mese, N = 7,514; non è il campione della regressione), quintile di gap / mesi / ln step medio / mediana per anno: Q1 fastest 6.4 / 1.06 / 1.89; Q3 16.6 / 1.08 / 0.74; Q5 slowest 38.1 / 1.18 / 0.36.
- Step totale da piatto a crescente, step per anno cinque volte più piccolo. Lettura nostra (I-03, proposta): θ1 > 0 riflette tempo per costruire, non crescita più rapida.
- Termini di hype (OLS 2), coef / p: hype al round 1 θ2 0.052 / 0.340; ln gap × hype θ3 −0.016 / 0.381. L'hype non cambia lo step né la sua relazione con il gap.

Fonti: figura n2, log L5865–5893; θ2, θ3 di val_h2, log L3081–3083.

## Slide 31: Design-wide checks: neither inference, sample composition nor market exit conditions move β1 or β3

- Tabella (exit entro 5 anni), N / β1 / p / β3 / p:
  - Main model, SE clusterizzati per settore × anno: 9,124 / −0.071 / 0.294 / −0.056 / 0.344
  - Robust (not clustered) SEs: 9,124 / −0.071 / 0.255 / −0.056 / 0.358
  - Drop 367 one-round startups out within 13 months: 8,759 / −0.065 / 0.331 / −0.056 / 0.339
  - + sector share of all exits in the window: 9,124 / −0.058 / 0.394 / −0.031 / 0.656
- Inferenza: 41 cluster sono pochi, i test cluster-robust possono rifiutare troppo spesso con pochi cluster [@cameron2008]; i SE robusti danno le stesse conclusioni.
- Composizione del campione: le one-round che escono o falliscono prima di poter raccogliere di nuovo possono essere classificate male; toglierle non cambia niente.
- Condizioni di exit del mercato: le exit si concentrano nel tempo; la quota del settore su tutte le exit nella finestra (coef 2.41, p = 0.203) lascia β1 e β3 invariati.
- Cali di N nei logit per predizione perfetta: 139 (exit), 28 (failure).

Fonti: [@cameron2008]; log L575/L578 (main), L3983/L3986 (SE robusti), L4541/L4544 (senza uscite precoci; 367 startup, L4465); add-on L3079–3084 (controllo exit-share, definizione nostra: open point 21).

## Slide 32: Non-linearity: adding the squared gap, in logs or in months, does not change any fixed-window result

- Modello: Pr(Yi = 1) = Λ(… + β1 Ri gi + βsq Ri gi² + …), gi = ln(1 + monthsi) oppure gi = monthsi; logit con R × gap + R × gap², hype come quota VC grezza, controlli round-1 e FE, SE clusterizzati per settore × anno.
- Perché: un round lento può contare solo oltre una soglia, o il log può nascondere curvatura. H0: nessuna curvatura (βsq = 0); test congiunto H0: β1 = βsq = 0 (il gap non conta affatto).
- Tabella outcome · forma del gap, βsq 4 anni / 5 anni / 6 anni / test congiunto 5 anni (p tra parentesi):
  - Exit · ln gap: −0.005 (0.922) / −0.034 (0.580) / −0.131 (0.070) / χ² 0.32 (0.851)
  - Exit · months: −0.0002 (0.431) / −0.0004 (0.185) / −0.0006 (0.250) / χ² 1.85 (0.396)
  - Failure · ln gap: −0.066 (0.284) / −0.059 (0.267) / −0.088 (0.065) / χ² 2.42 (0.299)
  - Failure · months: 0.0002 (0.663) / 0.0002 (0.583) / −0.0001 (0.933) / χ² 0.95 (0.622)
- N = 12,030 / 9,124 / 6,613 per l'exit e 12,156 / 9,235 / 6,757 per la failure (4 / 5 / 6 anni).
- Nessun termine al quadrato è significativo al 5% in nessuna finestra o forma. I test congiunti non rifiutano che i termini del gap siano zero: in questa specificazione (hype come quota grezza) anche il legame con la failure perde significatività, come nel check con quota grezza di H1b.

Fonti: do-file sezione 13; log L7588–7968 (exit, ln), L8328–8708 (exit, months), L9044–9359 (failure, ln), L9689–10004 (failure, months); test congiunti (testparm) L10295–10337.

## Slide 33: Without a fixed window the gap looks strongly protective and curved, but that is exposure time

- Figure q1 e q2: margins dei modelli senza finestra con il quadrato, ln gap + ln gap² (sinistra) e months + months² (destra).
- Coefficienti senza finestra, coef / p: Exit: R × ln gap −0.458 / <0.001; Failure: R × ln gap* −0.583 / <0.001; Exit: ln gap² −0.227 / <0.001; Failure: ln gap² −0.210 / <0.001; Exit: months² 0.00001 / 0.907; Failure: months² 0.0002 / 0.147.
- Un gap lungo lascia meno tempo nei dati per uscire o fallire: senza finestra il gap mescola la velocità con il tempo a rischio (nota del do-file).
- La curvatura compare solo in log e solo senza finestra: non c'è in nessun modello a finestra fissa (slide precedente). Per questo ogni ipotesi si testa su una finestra fissa di 5 anni. *Failure senza finestra: solo specificazione con quota grezza.
- Modelli senza finestra: ogni startup, outcome fino alla fine dei dati.

Fonti: log L2407 (exit, specificazione heat, N = 27,944, 77 cluster), L7140 (failure, specificazione quota grezza, N = 26,349); modelli al quadrato L8121–8126, L9509–9514 (ln), L8861–8866, L10154–10159 (months); do-file, nota della sezione 13.

## Slide 34: Robustness at a glance: the four verdicts hold, with two explained exceptions

- Tabella check × H1 β1 / H1b β1 / H2 β3 / H3 θ1 (✓ = stesso segno e stesso verdetto di significatività del modello principale; ✗ = il verdetto cambia; – = non stimato):
  - 4- and 6-year windows: ✓ / ✓ / ✓ / –
  - Probit / LPM: ✓ / – / ✓ / –
  - Team & young-lead controls: ✓ / ✓ / ✓ / –
  - Hype as raw VC share: ✓ / ✗ (n.s.) / ✓ / –
  - Squared gap, ln and months (section 5): ✓ / ✗ (n.s.) / – / –
  - Alternative hype measures (4): – / – / ✓ / –
  - Past-only hype: – / – / ✗ (p = 0.039) / –
  - Robust SEs · no early outs · exit share: ✓ / – / ✓ / –
  - Hype interaction in the valuation OLS: – / – / – / ✓
- Due eccezioni: H1b perde significatività solo nelle specificazioni con quota VC grezza, dove β1 è una pendenza a quota 0%, fuori dai dati; l'hype solo-passato perde il 29% del campione e si basa su 27 cluster.

Fonti: riassunto delle slide di robustness di ogni ipotesi e della sezione 5 (slide 16, 21, 26, 30–33); numeri e righe di log lì.

## Slide 35: H1 and H1b: one backdoor stays open, through quality we cannot observe

- DAG (versione snella): T = Gap; Y = Exit (H1) / failure (H1b); C = Unobserved quality (tratteggiato, non osservato); C = Round-1 controls & FE (ombreggiato, aggiustato); S = Reached round 2 (R = 1) (collider / selezione, condizionato); M = Round-2 size & valuation (mediatore). Etichetta della freccia T → Y: β1. Legenda: ombreggiato = aggiustato, tratteggiato = non osservato.
- Percorsi da T a Y: causale Gap → Exit / failure; causale Gap → Round-2 size & valuation → Exit / failure; bias aperto Gap ← Unobserved quality → Exit / failure. Altri 5 percorsi non causali sono bloccati da ciò che aggiustiamo.
- Quindi β1 è un'associazione: mescola il gap con la qualità che guida sia la velocità sia l'exit.

Fonti: DAG dal Causal Workbench del gruppo (artifact condiviso); aggiustato = nel modello (controlli round-1, FE) o condizionato (R = 1); percorsi per d-separazione; stesso DAG per exit e failure.

## Slide 36: H2: sector-specific shocks can move hype, speed and exits together

- DAG: T = Gap; Y = Exit within 5 years; Mod = Hype at round 1 (freccia ambra tratteggiata: l'hype cambia la pendenza T → Y, β3); C = Sector-year shock; C = Exit market (year-quarter FE); C = Unobserved quality. Etichetta: β1 + β3 · hype.
- Percorsi da T a Y: causale Gap → Exit within 5 years; bias aperto Gap ← Sector-year shock → Exit; bias aperto Gap ← Unobserved quality → Exit. Altri 5 percorsi non causali bloccati.
- β3 confronta pendenze tra livelli di hype: è distorto solo se lo shock cambia anche la pendenza, non solo il livello delle exit.
- I FE di settore assorbono le differenze permanenti e quelli year-quarter gli shock comuni nel tempo; uno shock a un settore in un anno non è assorbito.

Fonti: DAG dal Causal Workbench.

## Slide 37: H3: we see the valuation step only when it is disclosed, which selects on the outcome

- DAG: T = Gap; Y = Valuation step ln ΔV; C = Unobserved quality; C = Lead type & bargaining; C = Hype & fund inflows; M = Progress between rounds (lettura nostra I-03, proposta); S = Valuation disclosed. Etichetta: θ1.
- Percorsi da T a Y: causale Gap → ln ΔV; causale Gap → Progress between rounds → ln ΔV; bias aperto Gap ← Unobserved quality → ln ΔV; bias aperto Gap → Valuation disclosed ← ln ΔV. Altri 2 percorsi non causali bloccati.
- Valutazione dichiarata per 7,574 delle 15,518 two-round startups; condizionare sulla disclosure, figlia dell'outcome, può distorcere θ1 in entrambe le direzioni. La selezione sulla disclosure è la minaccia più grande per H3; la sua direzione è ignota.

Fonti: DAG dal Causal Workbench; N log L3069–3073 (vedi slide 28).

## Slide 38: Selection and confounding: what we did about them, and what is left

- Tabella minaccia / cosa abbiamo fatto / cosa resta / rischio:
  - La qualità non osservata guida sia velocità sia exit: controlli round-1 (dimensione, deal number, età, tipo di lead), FE year-quarter, settore e stato; i controlli di team e young-lead lasciano β1 invariato (−0.100 in entrambe le colonne, log L5028/L5219) / la qualità dopo il round 1 (traction, prodotto) non è in PitchBook; riportiamo solo associazioni / High.
  - Il gap esiste solo per chi ha raggiunto il round 2: le one-round restano nel campione con R = 1/0; togliendo 367 one-round uscite o fallite entro 13 mesi β1 resta −0.065 (L4541) / i risultati non dicono cosa farebbe un'attesa più lunga a una startup che non ha mai raccolto di nuovo / Medium.
  - Condizionare sul round 2 lega qualità e condizioni di mercato: controlli round-1 e FE nel modello (e hype, in H2) bloccano questi percorsi nel DAG / i percorsi attraverso la qualità non osservata restano aperti / Medium.
  - Shock specifici di settore muovono insieme hype ed exit: FE di settore e year-quarter; quattro misure di hype alternative e un controllo exit-share lasciano β3 tra −0.002 e −0.071, mai significativo tranne l'hype solo-passato / gli shock settore × anno non sono assorbiti / Medium.
- Limitazioni scritte nel Causal Workbench; stato: proposte, da concordare con il gruppo.

Fonti: log L5028, L5219, L4541; per gli altri numeri le righe sono nelle slide delle ipotesi e di robustness (26, 31).

## Slide 39: Timing, measurement and scope: smaller threats, each with a design answer

- Tabella minaccia / cosa abbiamo fatto / cosa resta / rischio:
  - Senza finestra fissa la velocità si mescola al tempo a rischio: tutte le ipotesi usano una finestra fissa di 5 anni dal round 2 (round 1 per le one-round), completamente osservata; finestre di 4 e 6 anni come check / basso per i modelli principali / Low.
  - Dimensione e valutazione del round 2 sono mediatori: mai controlli nei modelli principali; usati solo in H3 e nella robustness / nessuno per i modelli principali / Low.
  - Exit anticipate possono cambiare il gap: la finestra parte al round 2; exit prima del round 2 delle two-round contano 0 (26 startup) / l'anticipazione dentro la finestra non si può escludere con questi dati / Medium.
  - Le valutazioni sono dichiarate in modo selettivo e sopravvalutano il valore: H3 riportata come associazione tra chi dichiara; lo step per anno accanto allo step totale / direzione del bias di disclosure ignota / High.
  - Campione e contesto limitano la generalizzazione: importi non dichiarati eliminati invece che imputati (feedback del pitch); funnel del campione riportato / i risultati possono non valere per startup non US o per coorti più recenti / Medium.
- Limitazioni scritte nel Causal Workbench; stato: proposte, da concordare con il gruppo.

Fonti: sopravvalutazione della post-money, 135 unicorni US [@gornall2020].

## Slide 40: Fundraising speed is not the quality signal we expected

- H1 · Gap → exit: right sign, not significant. Un gap più lungo va con odds di exit leggermente più basse, mai in modo significativo (slide 14–16).
- H1b · Gap → failure: rejected, opposite sign. Un gap più lungo va con meno failure, in ogni finestra fissa (slide 19–21).
- H2 · Gap × hype: not supported. I mercati hot non indeboliscono il legame gap–exit; semmai è più ripido (slide 24–26).
- H3 · Gap → valuation: rejected, opposite sign. Chi raccoglie lentamente chiude con uno step più grande in totale, più piccolo per anno (slide 29–30).
- Cosa vuol dire: tra le startup che raccolgono di nuovo, un secondo round lento non è un segnale di difficoltà nei nostri dati. Sono associazioni: la qualità non osservata resta un percorso aperto (slide 35).
- Ogni risultato ha la sua slide; i numeri sono lì, non ripetuti qui.

Fonti: verdetti con la formulazione del paper v4, Table 13.

## Slide 41: Questions and discussion

- Q&A: descriviamo associazioni; il gap non è assegnato a caso e la qualità non osservata resta un percorso aperto (slide 35).
- Domande attese, risposta breve, slide:
  - Il gap non è solo qualità? Forse: è l'unico backdoor aperto; controlli e variabili di team non muovono β1 (35, 38).
  - Perché un gap lungo va con meno failure? La sopravvivenza è un argomento nostro: chi raccoglie lentamente ha superato i suoi anni più deboli (17–20).
  - Perché una finestra fissa di 5 anni? Senza, il gap mescola velocità e tempo a rischio (5, 33).
  - La misura di hype conta? β3 è negativo in ogni misura; solo l'hype solo-passato è significativo (26).
  - E le valutazioni non dichiarate? H3 vale solo per il 49% che dichiara; direzione del bias ignota (37, 39).
- Le letture segnate "our argument" sono proposte non ancora approvate dal gruppo.

Fonti: rimandi alle slide indicate.

## Slide 42: Thank you

- Group 21 · 21072 Data Analysis; titolo "Fundraising speed as a quality signal, tested against the VC cycle"; Data Lab for Entrepreneurship · Bocconi 2026/27.
- Research question ripetuta (come slide 1).
- Associations, not causal effects. PitchBook course extract, US startups, round 1 in 2012–2019.

Fonti: nessuna citazione.

## Slide 43: References

- Prima parte della bibliografia del deck: Abadie et al. (2023); Ai & Norton (2003); Bergemann & Hege (2005); Cameron et al. (2008); Chemmanur et al. (2014); Cochrane (2005); Cornelli & Yosha (2003); Dahiya & Ray (2012); Ewens et al. (2018); Gompers (1995); Gompers & Lerner (2000); Gompers et al. (2008); Gornall & Strebulaev (2020); Guler (2007); Haltiwanger et al. (2013); Heughebaert & Manigart (2012).
- Nota del deck: letteratura da `fonti/fonti.bib`, ognuna controllata con `routine validazione fonti/tabella.csv` (usabile o formulazione ristretta); lista generata e confrontata con le slide da script.

Fonti: [@abadie2023; @ai2003; @bergemann2005; @cameron2008; @chemmanur2014; @cochrane2005; @cornelli2003; @dahiya2012; @ewens2018; @gompers1995; @gompers2000; @gompers2008; @gornall2020; @guler2007; @haltiwanger2013; @heughebaert2012].

## Slide 44: References (continued)

- Seconda parte: Hill, Griffiths & Lim (2018), Principles of Econometrics, 5th ed., manuale del corso; Hochberg et al. (2007); Howell et al. (2020); Hsu (2004); Inderst & Mueller (2004); Kaplan & Strömberg (2003); Kerr, Lerner & Schoar (2014); Korteweg & Sorensen (2010); Lerner (1994); Li (2008); Manso (2011); Mize (2019); Nanda & Rhodes-Kropf (2013); Puri & Zarutskie (2012); Sorenson & Stuart (2001); Tian (2011).

Fonti: [@hochberg2007; @howell2020; @hsu2004; @inderst2004; @kaplan2003; @kerrlerner2014; @korteweg2010; @lerner1994; @li2008; @manso2011; @mize2019; @nanda2013; @puri2012; @sorenson2001; @tian2011]; Hill, Griffiths & Lim (2018) non nel .bib.

---

## Fonti non trovate nel .bib

- **Hill, Griffiths & Lim (2018), *Principles of Econometrics*, 5th ed., Wiley** (manuale del corso; slide 13 e 44): non c'è una voce in `fonti/fonti.bib`. Nessuna chiave inventata.
- **Causal Workbench** (artifact condiviso del gruppo; slide 35–39): non è letteratura, non va nel .bib.
- Documenti interni citati nei piè di slide, non bibliografici: dataset construction note v4, paper v4 (`paper_group21.pdf`), `scaletta.md`, `routine validazione fonti/tabella.csv`, do-file (sezioni 3, 4, 7, 13).

Tutte le altre 31 fonti del deck hanno una chiave in `fonti/fonti.bib`.
