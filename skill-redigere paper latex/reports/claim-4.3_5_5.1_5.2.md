# Claim audit — 4.3, 5, 5.1, 5.2

Sezioni 4.3 e 5: nessun rilievo sulle frasi (ogni frase ha il suo span nel CONTENUTO; nessun numero fuori materiale). Rilievi solo su 5, 5.1, 5.2.

### CLM-5.1-01
- **Severità**: medium
- **Sede**: 5.1, ¶6 — "moving across the gap interquartile range corresponds to less than one percentage point in exit probability"
- **Categoria**: claim allargato
- **Cosa non torna**: la frase non dice a quale hype vale. Con gli AME del log (cold −0.25 pp, medio −1.16 pp, hot −2.11 pp per unita' di ln gap) e IQR di ln gap = 0.78 (3.02−2.24), "meno di un punto" regge a hype medio (≈ −0.9) e a cold (≈ −0.2), ma non a hot (≈ −1.6 pp). Il paragrafo precedente riporta proprio −2.1 pp in hot.
- **Verificato nel materiale**: sì, qui: "Moving across the gap IQR changes exit by less than one point." (CONTENUTO punto 5, senza condizione sull'hype; il calcolo su L701–705 la smentisce in hot)
- **Chi lo risolve**: paper-writer (specificare "at average hype" o riformulare)

### CLM-5.1-02
- **Severità**: low
- **Sede**: 5.1, ¶6 — "age at round 1 is associated with 10% higher exit odds"
- **Categoria**: numero senza identita'
- **Cosa non torna**: manca l'unita' (per anno? per unita' di log?) e la riga del log; il materiale dice solo "age +10%". Stesso per "Round-1 size has an odds ratio of 1.64" (per quale unita').
- **Verificato nel materiale**: no, cercato e non trovato (unita' non specificata)
- **Chi lo risolve**: paper-writer / gruppo (leggere unita' in Table 6/log)

### CLM-5.1-03
- **Severità**: low
- **Sede**: 5.1, ¶1 — "[[TAB:T6]] reports logit estimates for exit within five years among one-round and two-round startups."
- **Categoria**: numero senza identita'
- **Cosa non torna**: β1 = −0.089 (p = 0.188) e β1/β3 con interazioni non dichiarano il campione (estimation sample, N = 9,263) ne' i 41 cluster; il glossario li richiede per i numeri.
- **Verificato nel materiale**: no, il materiale di 5.1 non riporta N dei modelli principali
- **Chi lo risolve**: fix-applier

### CLM-5.2-01
- **Severità**: medium
- **Sede**: 5.2, ¶2 — "the AME is −2.4 per unit of ln(1 + months). Across the gap interquartile range, the association amounts to −1.9 percentage points against mean failure of 12.4%, about 15% smaller"
- **Categoria**: numero non nel materiale (non verificato nel log) / numero senza identita'
- **Cosa non torna**: −2.4, −1.9, 12.4% e 15% stanno solo nelle parole del CONTENUTO punto 2; la sezione "Numeri dal log" dice «AMEs for failure: from the grid at L1449 onwards. Values at hype −1/0/+1 still to read in the log». Nessun p-value ne' N (9,235 o altro) per l'AME. Il ledger non ha LOG per ¶2.
- **Verificato nel materiale**: no, cercato e non trovato nel blocco log
- **Chi lo risolve**: gruppo (leggere L1449+ e fornire p e N), poi fix-applier

### CLM-5.2-02
- **Severità**: medium
- **Sede**: 5.2, ¶3 — "[[FIG:F15]] shows AMEs ranging from −2.1 to −2.8 percentage points across cold and hot markets"
- **Categoria**: numero non nel materiale (non verificato nel log)
- **Cosa non torna**: l'intervallo −2.1/−2.8 compare solo nelle keyword del CONTENUTO punto 3, senza dire quale estremo e' cold e quale hot, ne' p-value; il log per gli AME failure e' dichiarato "still to read". "providing no evidence of moderation" e' accettabile (piu' debole di "does not moderate"), ma l'attribuzione degli AME alla Figura 15 non e' verificabile.
- **Verificato nel materiale**: no, cercato e non trovato (solo "AME −2.1 to −2.8 pp, cold and hot markets")
- **Chi lo risolve**: gruppo / fix-applier

### CLM-5.2-03
- **Severità**: medium
- **Sede**: 5.2, ¶4 — "Lead-investor type does not predict failure: its association concerns the upside rather than the downside."
- **Categoria**: fatto non nel materiale / interpretazione senza ID (e fuori dalla trappola "do not explain why", che rimanda alla 5.5)
- **Cosa non torna**: il CONTENUTO dice "so the lead type relates to the chance of a good outcome, not of a bad one", e' una lettura nostra (inferenza), non un risultato; nel DRAFT e' enunciata come fatto nella sezione Results, senza "we read this as" e senza inferenza approvata. Manca anche il riferimento numerico (assenza di significativita' dei lead type nel log).
- **Verificato nel materiale**: no, nessun numero a supporto dei lead type sul failure; solo la frase interpretativa
- **Chi lo risolve**: paper-writer (marcare come lettura o spostare in 5.5) / gruppo

### CLM-5.2-04
- **Severità**: low
- **Sede**: 5.2, ¶5 — "[[FIG:F17]] checks functional form using Frisch–Waugh–Lovell binned residuals ... For 4,482 two-round startups"
- **Categoria**: letteratura non attribuita (metodo non citato dal corso) / incoerenza numerica nota
- **Cosa non torna**: FWL e' un metodo standard non attribuito; la nota editoriale chiede di citarlo dal corso (Hill et al. 2018) e la lezione e' [Guessing], da chiedere a Lele. N = 4,482 (log L1087) contro 4,483 del paper v4 e di altre sezioni: open point 21c. Il testo usa 4,482, coerente col log.
- **Verificato nel materiale**: sì per i numeri, qui: "slope failure −0.0304 (SE 0.0092, p 0.002) L1140 ... N = 4,482 L1087"; no per l'attribuzione del metodo
- **Chi lo risolve**: gruppo (escalation)

### CLM-5.2-05
- **Severità**: low
- **Sede**: 5.2, ¶4 — "Larger first rounds and older startups are associated with 37% and 8% lower failure odds"
- **Categoria**: numero senza identita'
- **Cosa non torna**: manca l'unita' del regressore (log round-1 amount, anni di eta') e il p-value; come in CLM-5.1-02. Il materiale riporta solo "round-1 size −37% odds, age −8% odds".
- **Verificato nel materiale**: no (unita' non specificata)
- **Chi lo risolve**: fix-applier dopo lettura della Table 8

### CLM-5-01
- **Severità**: low
- **Sede**: 5, ¶4 — "22.2% of two-round and 15.6% of one-round startups exit, and 12.4% and 31.6% fail."
- **Categoria**: numero senza identita'
- **Cosa non torna**: i tassi sono nel materiale ("from 3.3") ma il campione su cui sono calcolati (estimation sample 9,263? full sample?) non e' detto; la trappola ammette la ripetizione come scala senza discussione, ma l'identita' del numero resta richiesta. Il confronto "two points about a tenth" (2/22.2 ≈ 9%) regge.
- **Verificato nel materiale**: sì per i valori, qui: "22.2% of two-round and 15.6% of one-round startups exit, and 12.4% and 31.6% fail"; no per il campione
- **Chi lo risolve**: fix-applier

## Conteggio
- high: 0 · medium: 4 · low: 5
- Trappole verificate: 4.3 (2 su 2: nessun risultato, team/lead-age elencati), 5 (1 su 1), 5.1 (4 su 4: ρ1 non interpretato con rimando 6.2; verdetti H1 "right sign, not significant" / H2 "not supported"; controlli vs letteratura non trattati; past-only hype assente), 5.2 (3 su 3: nessuna spiegazione del perche' in 5.2 salvo CLM-5.2-03; "goes with lower failure" rispettato; ρ1 non interpretato con rimando 6.2).
