# Claim audit: 6.2, 6.3, 6.4, 7, abstract

Sezioni: 6.2, 6.3, 6.4, 7, abstract. Nessun rilievo high. 6.2 pulita.
Per l'abstract il materiale sono i DRAFT di 1, 3.1, 3.2, 5.1, 5.2, 5.3, 6.2, 6.3, 7.

## Controlli richiesti sull'abstract
- Verdetti con le parole del paper: H1 "right sign, not significant" (5.1 ¶1), H2 "not supported" (5.1 ¶2), H1b "rejected, opposite sign" (5.2 ¶1), H3 "rejected, opposite sign" (5.3 ¶1). Tutti corrispondono.
- H3 e' davvero "rejected, opposite sign" nel DRAFT di 5.3: si', "H3 is rejected, opposite sign" (¶1, θ1 = 0.109, p < 0.001).
- "valuation growth per year is slower": sostenuto solo da 5.3 ¶3 ("The median step per year falls from 1.89 to 0.36 log points: startups with short gaps gain value about five times faster per year", Figure 19, 7,514 startups) e da 6.1. E' un descrittivo grezzo per quintili. Vedi CLM-abstract-01.
- N 28,478 e 9,263: in 3.1 ¶3 e ¶4. Lunghezza 157 parole, nel range 150 ±15%.

### CLM-abstract-01
- **Severità**: medium
- **Sede**: abstract, ¶1 — "although valuation growth per year is slower"
- **Categoria**: claim allargato / incoerenza fra sezioni
- **Cosa non torna**: la frase sta in 5.3 ¶3 solo come mediana grezza per quintili di gap (Figure 19), senza modello, controlli o p-value. L'abstract la mette accanto a un risultato OLS con p < 0.001 come se avesse lo stesso statuto. Inoltre 7 ¶5 dice che "comparing growth per year rather than total valuation steps" e' ancora un'estensione aperta: abstract e conclusioni si contraddicono.
- **Verificato nel materiale**: si', qui (5.3 ¶3): "The median step per year falls from 1.89 to 0.36 log points: startups with short gaps gain value about five times faster per year."
- **Chi lo risolve**: gruppo (o la frase scende a "in raw medians" nell'abstract, oppure 7 ¶5 non chiama aperto il confronto)

### CLM-abstract-02
- **Severità**: low
- **Sede**: abstract, ¶1 — "(rejected, opposite sign) ... (rejected, opposite sign)"
- **Categoria**: verdetto
- **Cosa non torna**: le parole sono quelle del paper (5.2 ¶1, 5.3 ¶1). Pero' l'abstract non dice qual era l'ipotesi (H1b, H3). Un lettore legge "rejected" come giudizio sul risultato osservato ("less failure ... rejected"). Il sign opposto e' rispetto all'ipotesi, non detto.
- **Verificato nel materiale**: si', qui (5.2): "H1b is rejected, opposite sign." e (5.3): "H3 is rejected, opposite sign."
- **Chi lo risolve**: paper-writer

### CLM-abstract-03
- **Severità**: low
- **Sede**: abstract, ¶1 — "Hype moderation is not supported."
- **Categoria**: claim allargato
- **Cosa non torna**: in 7 ¶2 il gruppo qualifica che con hype solo-passato β3 e' negativo e significativo. L'abstract non lo dice. Il verdetto di H2 resta quello di 5.1 ("not supported"), quindi non e' falso, ma e' la parte piu' fragile.
- **Verificato nel materiale**: si', qui (7 ¶2): "with past-only hype, β3 remains negative but becomes significant."
- **Chi lo risolve**: gruppo (decide se l'abstract porta la qualifica)

### CLM-abstract-04
- **Severità**: low
- **Sede**: abstract, ¶1 — "Does the interval between a startup's first and second venture capital (VC) rounds predict exit"
- **Categoria**: linguaggio (predict)
- **Cosa non torna**: "predict" non e' causale ma il resto del paper usa "is associated with"; 1 usa "is the gap associated with the probability of exit".
- **Verificato nel materiale**: si', qui (1 ¶2): "is the gap associated with the probability of exit".
- **Chi lo risolve**: fix-applier

### CLM-6.3-01
- **Severità**: medium
- **Sede**: 6.3, ¶5 — "the gap measures what a startup has already survived and achieved, rather than its current condition."
- **Categoria**: over-claim (inferenza scritta come fatto)
- **Cosa non torna**: il materiale e' "We read the gap as a measure of ... (I-02)": e' una lettura nostra. Il DRAFT toglie "we read" e afferma "measures". Il materiale cita anche "less failure"; il DRAFT lo perde e ne tiene solo due delle tre prove.
- **Verificato nel materiale**: si', qui: "We read the gap as a measure of how much a startup has already survived and achieved before round 2, not of how it is doing: less failure, a larger total step and a flat exit link."
- **Chi lo risolve**: fix-applier (sostituzione locale)

### CLM-7-01
- **Severità**: low
- **Sede**: 7, ¶3 — "the gap adds little information about exit beyond round-1 characteristics, including round size and lead-investor type"
- **Categoria**: claim allargato
- **Cosa non torna**: il materiale ha un hedge ("seems to carry little information ... such as size and lead type"); il DRAFT lo toglie e lo trasforma in un fatto. L'informazione incrementale non e' un risultato del log (H1 e' "not significant", non "no information").
- **Verificato nel materiale**: si', qui: "the pace of refinancing seems to carry little information about exit beyond what is visible at round 1, such as size and lead type."
- **Chi lo risolve**: fix-applier

### CLM-7-02
- **Severità**: low
- **Sede**: 7, ¶4 — "Relevant perspectives in the staging literature provide points of comparison [[CIT-P:cochrane2005, korteweg2010, kaplan2003]]."
- **Categoria**: cucitura / citazione vaga
- **Cosa non torna**: la tesi vincolante e' solo "pointers to the views the results fit". La frase non dice quali viste sono (selection account, good-news) e le etichetta "staging literature", mentre cochrane2005 e korteweg2010 riguardano la selezione delle valutazioni osservate. Il lettore non sa a quale fonte attribuire "selection account". La frase dopo ("In our setting, the findings fit the selection account...") e' corretta come nostra applicazione.
- **Verificato nel materiale**: si', qui (tesi): "pointers to the views the results fit."
- **Chi lo risolve**: paper-writer

### CLM-6.4-01
- **Severità**: low
- **Sede**: 6.4, ¶2 — "[[CIT-N:howell2020]] finds that VC activity contracts during recessions ... In our setting, causal identification of the gap would require variation unrelated to venture quality, such as investor-capital shocks delaying rounds."
- **Categoria**: cucitura
- **Cosa non torna**: la citazione e' resa correttamente ("possible mechanism" non allarga "one likely mechanism"). Ma Howell parla di calo dell'attivita' di deal in recessione, non di ritardo dei round: il collegamento a "shocks delaying rounds" e' nostro e non e' marcato come tale oltre "In our setting". Prova togliendo la citazione: la frase dopo regge da sola, quindi non e' un'attribuzione impropria. Solo da tenere d'occhio.
- **Verificato nel materiale**: si', qui (tesi): "VC activity falls in recessions, mostly early-stage; capital-supply frictions are one likely mechanism."
- **Chi lo risolve**: gruppo (nessuna azione se accetta il collegamento)

## Conteggio
- high: 0
- medium: 2 (CLM-abstract-01, CLM-6.3-01)
- low: 5 (CLM-abstract-02, -03, -04, CLM-7-01, -02) + 1 (CLM-6.4-01) = 6

Totale 8 rilievi (high 0, medium 2, low 6).

## Trappole verificate: 9 su 9
- 6.2: numeri early-exit solo in 5.4, qui solo rimando (ok); valori di ρ1 non ripetuti (ok).
- 6.3: meccanismo non rispiegato (ok); Figure 8 richiamata verso 3.3, non riprodotta (ok).
- 6.4: nessuna promessa di eseguire i disegni (ok); il survival model sta qui e non in 7 (ok).
- 7: nessun numero oltre N = 9,263 (ok); implicazione per founder descrittiva, mai "should wait" (ok); disegni causali non ripetuti, solo rimando a 6.4 (ok).
