# Claim audit delle riscritture: 2.1, 2.2, 2.4, 2.5, 4.1, 5.1, 5.2, 5.4, 5.5, 5.6

Audit del 23/11/2026 su `sezioni/<id>.md` contro `build/ctx/<id>.md` (rigenerati con `tools/ctx.py`). Il LEDGER guardato solo dopo il giudizio frase per frase. Nessun numero ricontrollato nel log intero (non fa parte del materiale): i numeri sono confrontati con il blocco "Numeri dal log" e con il Contenuto.

## Parte 1. Stato dei vecchi rilievi (high/medium delle sezioni assegnate)

| Vecchio id | Sev. | Stato | Perche' |
|---|---|---|---|
| CLM-2.1-01 | high | RISOLTO | il nesso "segnali positivi veloci, rifinanziamento piu' rapido" e' ora un `[[GAP: ...]]` dichiarato; nessuna affermazione nostra al suo posto. Resta una decisione del gruppo (fonte o nostra ipotesi). |
| CLM-2.1-02 | high | RISOLTO | la frase "The leash view treats round length as a governance choice" non ha token, ma le tre frasi successive citano neher1999, gompers1995, tian2011 con le loro tesi; il periodo con il nostro passo ("we argue") e' separato. |
| CLM-2.1-03 | high | RISOLTO nella forma | l'interpretazione e' ora attribuita agli autori ("The authors interpret..."). Resta un nuovo medium sulla base documentale: vedi CLM-2.1-07. |
| CLM-2.2-01 | high | RISOLTO nella forma | "alive/worth more" tolto, la logica e' attribuita a cochrane2005/korteweg2010, la nostra applicazione e' separata. Resta un nuovo medium: vedi CLM-2.2-04. |
| CLM-2.2-02 | medium | RISOLTO | "may weaken". |
| CLM-2.4-01 | medium | RISOLTO | le azioni senior sono ora un `[[GAP]]` dichiarato. |
| CLM-2.5-01 | high | RISOLTO | hochberg2007 citato con la sua tesi ("more likely to reach later rounds"); "see more exits" tolto. |
| CLM-2.5-02 | high | RISOLTO | chemmanur2014 e ma2020 citati; "acquire them" e' un `[[GAP]]` dichiarato. |
| CLM-2.5-03 | high | RISOLTO | kerrlerner2014 citato, con "exit difference not significant". |
| CLM-2.5-04 | high | RISOLTO | hallen2020 citato, "some accelerators went with faster venture development". |
| CLM-4.1-01 | medium | **ANCORA APERTO** | "the corresponding probability-scale interaction can differ in size and sign and needs its own standard error" sta subito dopo la citazione di ai2003 (che regge solo "the interaction effect is not the interaction coefficient"); tolto "In our setting", ma l'idea resta scritta in voce neutra senza fonte. Prova "togli la citazione": la frase dopo resta idea di Ai & Norton. Chi: paper-writer (spostare la citazione a coprire il periodo) o gruppo (attribuire il "size and sign" ad ai2003 e' possibile solo dal contesto del lettore, non dalla tesi). |
| CLM-5.1-01 | medium | RISOLTO | "at average hype" aggiunto; −1.16 pp x 0.78 = 0.9 pp, "less than one point" regge. |
| CLM-5.2-01 | medium | RISOLTO | AME −2.4 pp con p = 0.003 e N = 4,469 (L1488, L1451); l'IQR −1.9 pp e il −15% tornano per aritmetica (0.0242 x 0.78 = 0.0189; 1.9/12.4 = 15%). |
| CLM-5.2-02 | medium | RISOLTO | −2.1 (p = 0.115) cold e −2.8 (p = 0.001) hot coincidono con L1484 e L1492. |
| CLM-5.2-03 | medium | RISOLTO nella forma | ora "We read this contrast ... as suggesting"; resta senza ID di inferenza (vedi CLM-5.2-07, low). |
| CLM-5.4-01 | high | RISOLTO | "It does not support H2 either" con "stable in sign, not significance". |
| CLM-5.4-02 | medium | RISOLTO | β3 "per percentage point of VC share, not per standard deviation", media 27.4%, confronto di segni e p-value. |
| CLM-5.5-01 | medium | **ANCORA APERTO (meta')** | il secondo GAP e' risolto ("The four explanations are not mutually exclusive, and our data cannot distinguish among them"). Il primo GAP "[[GAP: Specify the proposed links concerning CVC as acquirer, VC networks, angel groups and accelerators.]]" e' ancora nel testo: decisione del gruppo. |
| CLM-5.5-02 | medium | RISOLTO | "negative but not significant", "consistent with, but does not establish". |
| CLM-5.6-01 | high | RISOLTO | ewens2022 citato con la sua tesi ("omit contract terms beyond the equity share"). |

Vecchi low, stato in breve: RISOLTI 2.1-04, 2.1-05, 2.4-02, 2.5-05, 2.5-06, 2.5-07, 5.4-03, 5.4-04, 5.5-03. ANCORA APERTI 2.1-06 (H1 ripetuta rispetto alla riga di Tab. 1, decide il gruppo), 4.1-02 (ρ1, ρ2, β1, β3 mai definiti in 4.1), 5.1-02 (unita' di 1.64 e +10% mancanti), 5.1-03 (N = 9,263 e 41 cluster non dati in 5.1; solo "estimation sample (full outcome window)"), 5.2-04 (Frisch-Waugh-Lovell non attribuito al corso), 5.2-05 (unita' di −37% e −8% mancanti), 5.5-04 (round length vs gap: "short leash" e "short-gap startups" sovrappongono le due cose). 2.2-03 ("stalled"): nessuna azione necessaria, come da rilievo originale.

## Parte 2. Nuovi rilievi

### 2.1

### CLM-2.1-07
- **Severità**: medium
- **Sede**: 2.1, ¶4 — "The authors interpret this pattern as reflecting reduced information asymmetries after the initial investment."
- **Categoria**: claim allargato (attribuzione fuori dalla tesi)
- **Cosa non torna**: la tesi vincolante di hoenen2014 e' solo "patent applications raise round-1 funding but not round-2 funding". L'interpretazione degli autori compare soltanto nel "Contesto dal lettore" (marcato NON materiale: "nulla che stia solo qui va nel testo") e nel verbatim; il Contenuto la scrive senza dire di chi sia ("because investors already know more").
- **Verificato nel materiale**: parziale: Contesto lettore, "The authors read the pattern as a signal that diminishes once the investors' information asymmetries lessen"; non nella tesi.
- **Chi lo risolve**: gruppo (decidere se la tesi di hoenen2014 va estesa all'interpretazione degli autori)

### CLM-2.1-08
- **Severità**: low
- **Sede**: 2.1, ¶4 — "Evidence links outcomes to the number and size of rounds, rarely to time."
- **Categoria**: letteratura non attribuita (generalizzazione sulla letteratura senza token)
- **Cosa non torna**: affermazione sullo stato della letteratura senza citazione; il Contenuto la scrive uguale, ma la sola fonte della frase dopo (hoenen2014) riguarda importi, non numero di round.
- **Verificato nel materiale**: si', Contenuto 4: "Evidence links outcomes to the number and size of rounds, rarely to time." Nessuna fonte del blocco la regge per il "number of rounds" (tian2011 e' sul numero di round ma e' citata in ¶3 per altro).
- **Chi lo risolve**: gruppo

### CLM-2.1-09
- **Severità**: low
- **Sede**: 2.1, ¶5 — "For β1, the coefficient of R × ln(1 + months)"
- **Categoria**: fatto non nel materiale (simbolo non definito)
- **Cosa non torna**: R non e' definito in 2.1 (il glossario lo definisce come `two_rounds`); 4.1 lo definisce solo in prosa. Vedi anche 4.1-02 aperto.
- **Verificato nel materiale**: no, "R" senza definizione nel Contenuto di 2.1.
- **Chi lo risolve**: paper-writer

### 2.2

### CLM-2.2-04
- **Severità**: medium
- **Sede**: 2.2, ¶3 — "[[CIT-N:cochrane2005]] identifies upward selection in VC returns, which are observed at refinancing or exit events that are more likely after favourable returns."
- **Categoria**: claim allargato
- **Cosa non torna**: la tesi di cochrane2005 in 2.2 e' "VC returns are observed only at financing events, with selection bias", senza direzione. "Upward" e "more likely after favourable returns" stanno nella tesi di 2.4 (e nel contesto del lettore), non in quella di 2.2; qui il Contenuto 3 mette "selected upward" come nostra conseguenza. Il periodo citato porta quindi un'attribuzione piu' forte di quella consentita in questa sezione.
- **Verificato nel materiale**: no per 2.2: cercato "upward", "more likely", "favourable" in ctx 2.2: solo nel Contenuto (nostro) e nel testo della 2.1 precedente.
- **Chi lo risolve**: paper-writer (riscrittura: attribuire solo "observed only at financing events, with selection bias"; "upward" come nostra applicazione)

### 2.4

### CLM-2.4-03
- **Severità**: low
- **Sede**: 2.4, ¶3 — "In our setting, measured valuation steps therefore mix value with contractual terms and bargaining power."
- **Categoria**: cucitura e connettivo
- **Cosa non torna**: "therefore" subito dopo quattro citazioni (gornall2020 su 135 unicorni, ewens2022, hsu2004 su 51 start-up MIT); la conclusione generalizza al nostro campione, dove i limiti dicono che le valutazioni sono per lo piu' piccole; "bargaining power" non e' nella tesi di hsu2004 (reputazione) e heughebaert2012 non e' citata.
- **Verificato nel materiale**: si', Contenuto 4: "Measured steps mix value with contract and bargaining terms."
- **Chi lo risolve**: fix-applier (togliere "therefore")

### CLM-2.4-04
- **Severità**: low
- **Sede**: 2.4, ¶4 — "Prices were positively associated with capital inflows [[CIT-P:gompers2000]]."
- **Categoria**: duplicato
- **Cosa non torna**: lo stesso risultato e' gia' a casa in 2.3 ¶1 ("Fund inflows were associated with higher private-deal valuations"); qui basterebbe un rimando. Il Contenuto di 2.4 punto 5 lo richiede come premessa.
- **Verificato nel materiale**: si', Contenuto 5: "Prices rise with capital inflows"; tesi gompers2000 "prices rise with fund inflows".
- **Chi lo risolve**: gruppo

### 2.5

### CLM-2.5-08
- **Severità**: low
- **Sede**: 2.5, ¶5 — "clustering by sector × year of round 1, the level at which hype is assigned."
- **Categoria**: claim allargato
- **Cosa non torna**: "assigned" suggerisce un'assegnazione che nel disegno non c'e' (RULES: nothing is assigned); la tesi di abadie2023 (non citata qui, "applying this to heat is our extension... say so") chiede di dichiarare l'estensione. Il Contenuto ha la stessa formula.
- **Verificato nel materiale**: si', Contenuto 5: "the level at which hype is assigned"; abadie2023 note: "hype is not an assigned treatment".
- **Chi lo risolve**: paper-writer

### CLM-2.5-09
- **Severità**: low
- **Sede**: 2.5, ¶5 — "to absorb VC's geographic concentration ... and year-quarter fixed effects to absorb exit-market windows."
- **Categoria**: fatto non nel materiale (fatti sul mondo senza citazione)
- **Cosa non torna**: concentrazione geografica del VC e finestre di exit sono idee di letteratura (sorenson2001, chen2010, lerner1994) non citate; chen2010 e' segnata come "Contradicts the tesi" e lerner1994 come biotech only. E' motivazione di disegno e sta nel Contenuto, quindi low.
- **Verificato nel materiale**: si' per la formula, Contenuto 5; nessuna fonte usata.
- **Chi lo risolve**: gruppo

### 4.1

### CLM-4.1-03
- **Severità**: low
- **Sede**: 4.1, ¶5 — "With few clusters, p-values can be too small; checks appear in [[SEC:5.4]] and limitations in [[SEC:5.6]]."
- **Categoria**: letteratura non attribuita
- **Cosa non torna**: e' l'idea di cameron2008 senza citazione (fonte nel blocco, "solo rimando"); inoltre la tesi di cameron2008 e' per 5-30 cluster in modelli lineari, mentre qui i cluster sono 41. Il Contenuto ha la frase non attribuita.
- **Verificato nel materiale**: si', Contenuto 5: "With few clusters, p-values can be too small." cameron2008 limiti: "G between 5 and 30, while our main exit models have 41 clusters".
- **Chi lo risolve**: gruppo

### 5.1

### CLM-5.1-04
- **Severità**: medium
- **Sede**: 5.1, ¶3 — "for 4,444 two-round startups ... −0.3 percentage points ... (p = 0.883) ... −2.1 percentage points ... (p = 0.068) ... −1.9 percentage points (p = 0.327)"
- **Categoria**: float ripetuto
- **Cosa non torna**: il testo riporta quasi tutte le celle di T7 per la riga exit (N, AME cold, p cold, AME hot, p hot, differenza, p), piu' le due del LPM, mentre la regola e' due o tre celle. Il Contenuto elenca gli stessi numeri; i valori sono corretti (L701-705, L722-732, L1014, L1017).
- **Verificato nel materiale**: si', celle T7 "0.88", "0.07", "0.33", "4,444"; numeri dal log.
- **Chi lo risolve**: paper-writer (o gruppo, se si tiene per budget di pagine)

### CLM-5.1-05
- **Severità**: low
- **Sede**: 5.1, ¶6 — "These associations are larger than the gap association: at average hype, moving across the gap interquartile range corresponds to less than one percentage point in exit probability."
- **Categoria**: claim allargato
- **Cosa non torna**: confronta variazioni di odds in percentuale (94%, 55%, 39%, 1.64) con una variazione in punti percentuali (0.9 pp, AME con p = 0.293 al livello medio), che sono su scale diverse; il confronto e' del Contenuto ("Controls are larger than the gap") ma senza dire che l'AME medio non e' significativo.
- **Verificato nel materiale**: si', Contenuto 5; AME −0.0116 (p 0.293) in "Numeri dal log".
- **Chi lo risolve**: paper-writer

### CLM-5.1-06
- **Severità**: low
- **Sede**: 5.1, ¶5 — "The coefficient ρ1 of the two-round group indicator is reported in [[TAB:T6]]"
- **Categoria**: fatto non nel materiale
- **Cosa non torna**: il LEDGER dichiara "NESSUNA FONTE" per ¶5; nel materiale T6 ha titolo "Time between rounds, hype and exit" e solo celle numeriche, senza etichetta per ρ1.
- **Verificato nel materiale**: no, cercato e non trovato (ρ1 in T6).
- **Chi lo risolve**: gruppo (verificare nella tabella)

### 5.2

### CLM-5.2-06
- **Severità**: low
- **Sede**: 5.2, ¶2-¶3 e ¶5 — "for 4,469 two-round startups ... −2.1 ... −2.8 ... For 4,482 two-round startups"
- **Categoria**: duplicato / numero senza identita'
- **Cosa non torna**: gli AME per il failure (−2.4, −2.1, −2.8 con p) sono le stesse celle di T7, che ha casa in 5.1, ma 5.2 non richiama T7. Nelle sezioni 5.1-5.2 compaiono quattro N per le two-round (4,483 nel glossario, 4,482, 4,469, 4,444) senza spiegazione, come l'open point 21c.
- **Verificato nel materiale**: si', "same cells as Table 7" e "N = 4,482 (paper says 4,483: open point 21c)".
- **Chi lo risolve**: gruppo

### CLM-5.2-07
- **Severità**: low
- **Sede**: 5.2, ¶4 — "We read this contrast with the exit results as suggesting that lead type is more closely associated with upside outcomes than with failure."
- **Categoria**: fatto non nel materiale (inferenza senza ID)
- **Cosa non torna**: lettura nostra ora marcata come tale, ma senza ID di inferenza approvata e senza numero a supporto (nessuna cella di T8 per i lead type nel materiale).
- **Verificato nel materiale**: parziale, Contenuto 4: "so the lead type relates to the chance of a good outcome, not of a bad one".
- **Chi lo risolve**: gruppo

### 5.4

### CLM-5.4-05
- **Severità**: medium
- **Sede**: 5.4, ¶5, ¶6, ¶7 (tutti i numeri dei punti BT1-BT4, BF1-BF2)
- **Categoria**: trappola non verificata (violata)
- **Cosa non torna**: la Trappola del punto 6 dice "Cite in the text only the two or three numbers that carry the point"; ¶5 riporta circa dieci numeri (β3 con p e N per exit e failure, i due share, l'AME hot-cold, β3 sector-demeaned), ¶6 dodici (due p al 10%, quattro χ² con p) e ¶7 quattro. I valori sono tutti esatti rispetto a "Numeri dal log", ma l'appendice (BT1-BT4) e' fuori corpo proprio per non ripeterli.
- **Verificato nel materiale**: si', Trappola: "Cite in the text only the two or three numbers that carry the point."
- **Chi lo risolve**: paper-writer (con la decisione del gruppo se tagliare, perche' tagliare e' una decisione del gruppo)

### CLM-5.4-06
- **Severità**: low
- **Sede**: 5.4, ¶2 e ¶4 — "the logit coefficient β1 = −0.458"; "Heteroskedasticity-robust standard errors"; "367 early one-round exits"
- **Categoria**: numero senza identita'
- **Cosa non torna**: β1 = −0.458 senza p-value ne' N; "heteroskedasticity-robust" non e' nel materiale (il log dice "robust SEs", e il contesto di cameron2008 avverte che non c'e' un confronto robust vs clustered); "early" non e' definito.
- **Verificato nel materiale**: no, cercato e non trovato (p e N di L2391; definizione di "early").
- **Chi lo risolve**: fix-applier

### CLM-5.4-07
- **Severità**: low
- **Sede**: 5.4, ¶7 — "Only without an outcome window is logarithmic curvature significant"
- **Categoria**: claim allargato (livello di significativita' non detto)
- **Cosa non torna**: ¶6 dice che nella finestra a sei anni il termine quadratico logaritmico e' significativo al 10% (p = 0.070 e 0.065); "only without a window" vale solo al 5%.
- **Verificato nel materiale**: si', Contenuto 6: "at 10% only ln gap squared with the 6-year window".
- **Chi lo risolve**: fix-applier ("at the 5% level")

### 5.5

### CLM-5.5-05
- **Severità**: low
- **Sede**: 5.5, ¶5 — "The four explanations are not mutually exclusive, and our data cannot distinguish among them."
- **Categoria**: fatto non nel materiale (riferimento ambiguo)
- **Cosa non torna**: le "four explanations" non sono elencate in 5.5; la frase segue il periodo su selezione e influenza, e il lettore puo' riferirla a quello. Il Contenuto la ha nelle Note editoriali ("v4 already says...").
- **Verificato nel materiale**: si', Note editoriali: "the four explanations are not mutually exclusive and cannot be separated".
- **Chi lo risolve**: paper-writer

### 5.6

### CLM-5.6-02
- **Severità**: low
- **Sede**: 5.6, ¶1 — "The wild cluster bootstrap addresses inference with few clusters [[CIT-P:cameron2008]]. In our setting, the main exit models use 41 clusters ... and p-values may be too small. Robust standard errors yield almost identical p-values"
- **Categoria**: claim allargato / cucitura
- **Cosa non torna**: cameron2008 regge il bootstrap per pochi cluster in modelli lineari con G = 5-30; la frase successiva applica "few clusters / p-values may be too small" ai 41 cluster nostri, fuori da quel range, subito dopo la citazione. "Robust standard errors" non dice che sono non clusterizzati (il glossario vieta "robust SEs" per quelli clusterizzati).
- **Verificato nel materiale**: si', Contenuto 1: "Robust SEs give almost the same p-values, but a wild cluster bootstrap would be the safer test"; limiti: "G = 5 to 30; our models are logit with 41 clusters".
- **Chi lo risolve**: fix-applier

## Conteggio

- Nuovi rilievi: **high 0 · medium 4 · low 15** (totale 19). Medium: CLM-2.1-07, CLM-2.2-04, CLM-5.1-04, CLM-5.4-05.
- Vecchi high/medium delle sezioni assegnate: 20. RISOLTI 18, ANCORA APERTI 2 (CLM-4.1-01, CLM-5.5-01 per il solo primo GAP). I vecchi low aperti sono elencati in Parte 1.
- Trappole verificate: 32 su 33 (2.1: 3/3; 2.2: 2/2; 2.4: 2/2; 2.5: 4/4; 4.1: 3/3; 5.1: 4/4; 5.2: 3/3; 5.4: 5/6, violata la trappola "floats" del punto 6, CLM-5.4-05; 5.5: 4/4; 5.6: 2/2). Nessun Accelerator_pre_r1, nessun linguaggio causale su gap o hype, nessuna citazione verbatim, verdetti con le parole del paper (H1 "right sign, not significant", H1b "rejected, opposite sign", H2 "not supported", ρ1 mai interpretato).
- Tutti i numeri delle sezioni 5.1, 5.2, 5.4 coincidono con il blocco "Numeri dal log" (i valori derivati −1.9 pp, −15%, 0.9 pp tornano per aritmetica con IQR 0.78).
