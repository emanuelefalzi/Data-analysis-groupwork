# Claim audit 5.3, 5.4, 5.5, 5.6

### CLM-5.4-01
- **Severità**: high
- **Sede**: 5.4, ¶2 — "H2 is rejected, opposite sign: the coefficient is stable in sign, not significance."
- **Categoria**: verdetto con parole diverse dal paper
- **Cosa non torna**: la formula dei verdetti per H2 e' «not supported» (scaletta L546: "H2 not supported"; 5.1 ¶2 e 5.4 ¶5 scrivono «H2 is not supported»). «rejected, opposite sign» e' il verdetto di H1b e H3. Il Contenuto di 5.4 (punto 3) dice solo «It does not support H2 either». Con il past-only hype β3 = −0.050 (p = 0.039) la riga resta «not supported»; il segno opposto e' gia' detto in 5.1 e non cambia il verdetto. Contraddice anche 5.4 ¶5 nella stessa sezione.
- **Verificato nel materiale**: sì, qui: "It does not support H2 either." (Contenuto 5.4 p.3); scaletta: "H1 *right sign, not significant*; H2 *not supported*."
- **Chi lo risolve**: fix-applier (sostituzione locale: «H2 is not supported either»; tenere «stable in sign, not significance»)

### CLM-5.6-01
- **Severità**: high
- **Sede**: 5.6, ¶3 — "In our setting, the valuation step uses post-money valuations, ignores contract terms other than the equity share and is observed for about half of two-round startups."
- **Categoria**: letteratura non attribuita
- **Cosa non torna**: «ignora i termini contrattuali diversi dalla quota di capitale» e' l'argomento riconoscibile di ewens2022 (post-money valuation e' una cattiva misura del valore perche' ignora i termini oltre l'equity share), fonte segnata «solo rimando» per questa sezione. Nel draft e' scritto come nostro ("In our setting... ignores"), senza CIT. Nel LEDGER ¶3 manca FONTE[ewens2022]; il Contenuto lo dà non attribuito, ma la tesi della fonte e' quella. Serve escalation al gruppo (citare ewens2022 con la sua tesi, o dire che e' una nostra osservazione).
- **Verificato nel materiale**: sì, qui: "On valuation, it only says post-money valuation is a poor metric of firm value because it ignores terms other than the equity share" (contesto ewens2022 dalla routine).
- **Chi lo risolve**: gruppo (escalation)

### CLM-5.5-01
- **Severità**: medium
- **Sede**: 5.5, ¶5 — "[[GAP: Specify the proposed links concerning CVC as acquirer, VC networks, angel groups and accelerators.]]" e "[[GAP: Establish whether these candidate explanations can coexist and whether the data can distinguish them.]]"
- **Categoria**: fatto non nel materiale (placeholder aperti)
- **Cosa non torna**: due GAP irrisolti nel testo. Il secondo copre una frase che le Note editoriali dicono di tenere («the four explanations are not mutually exclusive and cannot be separated»: ponte verso la Sezione 6) e la Trappola «the data cannot separate them (say so once)»: nel draft non e' detta da nessuna parte. Il primo (CVC come acquirer, reti VC, angel, acceleratori) non ha materiale.
- **Verificato nel materiale**: no, cercato e non trovato (nel Contenuto di 5.5 c'e' solo il confronto con Table 14 e il rimando a Hochberg).
- **Chi lo risolve**: paper-writer (frase sulla non-separabilita'); gruppo (collegamenti CVC/reti/angel/acceleratori)

### CLM-5.5-02
- **Severità**: medium
- **Sede**: 5.5, ¶4 — "The negative logit interaction coefficient β3 fits the signal-extraction alternative in [[SEC:2.3]]: a long gap is more informative in hot markets."
- **Categoria**: numero senza identita' / claim allargato
- **Cosa non torna**: il β3 principale (−0.056, p = 0.344, 5.1) non e' significativo. Il testo lo usa per sostenere un meccanismo senza dire che non e' significativo; il lettore capisce un β3 negativo accertato. Mancano p-value e campione. Il Contenuto (punto 4) ha la stessa omissione, ma il guardrail «mechanisms are consistent with, fits» non copre un coefficiente non significativo.
- **Verificato nel materiale**: sì, qui: "β3 = −0.056 (p = 0.344)" (5.1 draft, sezioni/5.1.md).
- **Chi lo risolve**: paper-writer

### CLM-5.4-02
- **Severità**: medium
- **Sede**: 5.4, ¶5 — "In the five-year models, β3 is −0.0020 (p = 0.670; 9,124 startups) for exit and −0.0031 (p = 0.542; 9,235 startups) for failure."
- **Categoria**: trappola non verificata (unita' di β3 con raw share)
- **Cosa non torna**: la Trappola dice che β3 con la quota grezza e' per punto percentuale di quota, non per SD, e che si confrontano segni e p-value, non grandezze. Il draft non dichiara l'unita' ne' che la quota non e' centrata (media 27,4%, minimo 0,4%): il lettore puo' confrontare −0.0020 con β3 = −0.056 di 5.1. Il caveat sulla quota zero appare solo in ¶6 per i test congiunti.
- **Verificato nel materiale**: sì, qui: "β3 is per percentage point of share, not per SD: compare signs and p-values, not sizes."
- **Chi lo risolve**: paper-writer (una clausola)

### CLM-5.4-03
- **Severità**: low
- **Sede**: 5.4, ¶7 — "squared-term logit coefficients are −0.227 for exit and −0.210 for failure (both p < 0.001)."
- **Categoria**: numero senza identita'
- **Cosa non torna**: manca il campione (15,495 per exit, 15,294 per failure, solo startup con due round, senza finestra, raw share come hype nel modello). Il «without an outcome window» e' detto, il resto no.
- **Verificato nel materiale**: sì, qui: "N 15,495 L10327 ... N 15,294 L10378".
- **Chi lo risolve**: fix-applier

### CLM-5.4-04
- **Severità**: low
- **Sede**: 5.4, ¶2 — "The gap penalty on exit is about 5% larger in odds per standard deviation of past-only hype."
- **Categoria**: linguaggio causale (lieve) / numero senza identita'
- **Cosa non torna**: «penalty on exit» presuppone un effetto negativo del gap sull'exit, mentre β1 sull'exit non e' significativo; la glossa «5% larger in odds» e' ambigua (β3 = −0.0498 → odds ratio 0.951 per SD, cioe' l'associazione tra gap e odds di exit e' piu' negativa del 4,9%). Il termine viene dal Contenuto, ma il glossario preferisce «is associated with».
- **Verificato nel materiale**: sì, qui: "the gap penalty on exit is about 5% larger in odds per SD of past hype." (Contenuto 5.4 p.3); β3 −0.0498 L2605.
- **Chi lo risolve**: fix-applier

### CLM-5.5-03
- **Severità**: low
- **Sede**: 5.5, ¶4 — "hype at round 1 poorly proxies exit-market conditions years later, biasing β3 towards zero."
- **Categoria**: fatto non nel materiale
- **Cosa non torna**: e' un'ipotesi nostra senza risultato sotto (nessun numero, nessuna I-xx citata). Il draft la introduce con «We also consider» ma poi la afferma come fatto («poorly proxies ... biasing»). Il Contenuto la dà allo stesso modo, quindi e' soprattutto un dubbio di registro: andrebbe «may poorly proxy... which would bias».
- **Verificato nel materiale**: sì, qui: "hype at round 1 is a poor proxy for exit-market conditions years later, biasing β3 towards zero." (Contenuto 5.5 p.4)
- **Chi lo risolve**: fix-applier

### CLM-5.5-04
- **Severità**: low
- **Sede**: 5.5, ¶2 — "Shorter rounds were associated with higher agency costs or greater investor distance, consistent with costlier monitoring [[CIT-P:gompers1995, tian2011]]. In our setting, we interpret this short leash as consistent with greater risk among short-gap startups."
- **Categoria**: claim allargato
- **Cosa non torna**: le fonti riguardano la durata del finanziamento di un round (shorter rounds); la nostra variabile e' il tempo tra round 1 e round 2. «short leash» e «short-gap startups» sovrappongono le due cose senza dirlo. Gompers 1995 non testa la difficolta' di monitoraggio (dal contesto: solo proxy di agency cost a livello di industria). L'attribuzione e' separata bene dalla nostra lettura (nessuna cucitura), quindi solo low.
- **Verificato nel materiale**: sì, qui: "shorter rounds where agency costs are higher (Gompers) or the VC is far, so monitoring is costlier (Tian)."
- **Chi lo risolve**: paper-writer

### CLM-5.3-01
- **Severità**: low
- **Sede**: 5.3, ¶3 — "Larger first rounds have an OLS coefficient of −0.139. Older startups and more earlier deals are associated with steps 6.1% and 4.2% smaller, respectively ... Accelerator-led first rounds go with steps 33% larger."
- **Categoria**: numero senza identita'
- **Cosa non torna**: −0.139 senza p-value (in Table 9 e' ***); 6,1%, 4,2%, 33% sono trasformazioni exp(coef)−1 (−0.063 → −6,1%; −0.043 → −4,2%; 0.288 → +33,4%) e senza coefficiente ne' p. Le trasformazioni tornano con le celle di T9 ma il testo non lo dice. Il 33% compare nel Contenuto solo nel sottotitolo.
- **Verificato nel materiale**: sì, qui: celle T9 "-0.063***", "-0.043**", "0.288**"; "size −0.139, age −6.1%, earlier deals −4.2%, accelerator +33%".
- **Chi lo risolve**: fix-applier

## Chiusura
- 5.3: nessuna criticita' sui numeri principali (θ1 0.109, θ3 −0.016 p 0.381, N 7,574 e 7,514, 1.18, 1.89→0.36, rapporto 5.2) tutti trovati nel materiale/log. Verdetto H3 «rejected, opposite sign» corretto.
- 5.4: tutti i numeri di ¶1–¶8 verificati su Contenuto/log (149/190/570 cluster, p 0.090, 9,124/9,235, −0.9 pp p 0.650 N 4,444, χ², 9,262, 0.94, 0.08, 0.31); unica differenza di sostanza: il verdetto H2 in ¶2. Guardrail del punto 6: quota grezza descritta correttamente (percentuale dei dollari VC nell'anno del round 1), non si scrive che l'associazione di failure «scompare», test congiunti dichiarati a quota zero; mancano solo l'unita' di β3 per punto percentuale (CLM-5.4-02). Sul tempo di esposizione senza finestra il draft e' conforme: «partly reflect time at risk», nessun uso di BF1–BF2 come risultato per H1 o come U rovesciata per le finestre. «Hot − cold» a ±1 SD della quota dichiarato.
- 5.5: nessun numero nuovo (conforme alla Trappola); «consistent with survivorship» al posto di «not the effect of waiting» (conforme).
- 5.6: nessun linguaggio causale; wild bootstrap segnalato come assente dal do-file.

Conteggio: high 2, medium 3, low 5 (totale 10).
Trappole verificate: 5.3 2/2; 5.4 8/8 (4 punti 1–5 piu' 4 del punto 6; la trappola del punto 6 su β3 per pp e' CLM-5.4-02); 5.5 4/4 (la non separabilita' dei meccanismi e' CLM-5.5-01); 5.6 2/2.
