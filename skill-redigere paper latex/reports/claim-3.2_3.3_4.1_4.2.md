# Claim audit — 3.2, 3.3, 4.1, 4.2

Esito: 0 high, 1 medium, 5 low. Nessuna frase orfana, nessun numero fuori materiale, nessuna letteratura non attribuita, nessun linguaggio causale su gap o hype, nessun verdetto con parole proprie.

### CLM-4.1-01
- **Severità**: medium
- **Sede**: 4.1, ¶3 — "In our setting, the logit coefficient measures a log-odds slope change; the probability-scale interaction can differ in size and sign and needs its own standard error."
- **Categoria**: cucitura e connettivo
- **Cosa non torna**: la frase segue subito la citazione ai2003. "Can differ in size and sign / needs its own SE" è l'idea di Ai & Norton (il testo la presenta come «in our setting», ma è un fatto generale sui modelli non lineari). Il CONTENUTO la ha come nostra, ma la tesi vincolante di ai2003 è solo «the interaction effect is not the interaction coefficient». Prova «togli la citazione»: la frase dopo porta da sola contenuto riconoscibile della letteratura, senza fonte.
- **Verificato nel materiale**: sì, qui: "Its effect on the probability can differ in size and sign and needs its own standard error." (CONTENUTO punto 3, senza attribuzione) vs tesi ai2003: "in logit and probit the interaction effect is not the interaction coefficient."
- **Chi lo risolve**: paper-writer (riscrittura: spostare la citazione a coprire il periodo, o togliere «In our setting» dal generale); eventualmente gruppo se si vuole attribuire ad ai2003 il «size and sign» (oggi solo nel contesto del lettore, non nella tesi)

### CLM-3.3-01
- **Severità**: low
- **Sede**: 3.3, ¶1 — "Their exit-within-five-years shares are 22.2% and 15.6%, respectively; failure shares are 12.4% and 31.6%."
- **Categoria**: float ripetuto
- **Cosa non torna**: quattro celle di T5 ripetute nel testo (limite: due o tre). I valori sono nel materiale e coerenti con T5 (0.222, 0.156, 0.124, 0.316).
- **Verificato nel materiale**: sì, qui: "In the estimation sample, two-round startups exit more often and fail far less often"; keywords "exit 22.2% vs 15.6%, failure 12.4% vs 31.6%"
- **Chi lo risolve**: paper-writer

### CLM-3.3-02
- **Severità**: low
- **Sede**: 3.3, ¶1 — "Both differences are significant in t-tests."
- **Categoria**: numero senza identità
- **Cosa non torna**: manca il p-value / livello; il materiale non ne dà (nessun numero dal log). Il testo non inventa, ma la convenzione chiede il p-value dove serve.
- **Verificato nel materiale**: no, cercato e non trovato (p-value dei t-test)
- **Chi lo risolve**: gruppo (decidere se aggiungere dal log, L157-237) o lasciare

### CLM-3.3-03
- **Severità**: low
- **Sede**: 3.3, ¶5 — "[[FIG:F6]] presents exit within five years by group and market hype. [[FIG:F7]] breaks down exit within five years by gap quintile and market hype."
- **Categoria**: trappola non verificata (glossario: hot/cold = ±1 SD in modelli, terzili nelle figure, dirlo)
- **Cosa non torna**: «market hype» nelle figure descrittive non dice se è terzili o ±1 SD; il materiale non lo specifica (solo il titolo F7 «cold and hot markets»), quindi non si può precisare senza inventare.
- **Verificato nel materiale**: no, cercato e non trovato (definizione dei gruppi di hype in F6/F7)
- **Chi lo risolve**: gruppo (verificare nel do-file e dichiarare)

### CLM-3.3-04
- **Severità**: low
- **Sede**: 3.3, ¶6 — "A long gap is followed more by staying private than by exit."
- **Categoria**: claim allargato (ambiguità)
- **Cosa non torna**: il materiale dice solo che la quota still private sale con il gap e l'exit è piatta; «followed more by staying private than by exit» può essere letto come confronto di livelli (private > exit), non supportato. Fedele alla frase del CONTENUTO («slow round»), quindi basso.
- **Verificato nel materiale**: sì, qui: "the exit share barely moves, failure falls and the share still private rises (Figure 8)"
- **Chi lo risolve**: paper-writer

### CLM-4.1-02
- **Severità**: low
- **Sede**: 4.1, ¶2 — "ρ1 and ρ2 compare groups."
- **Categoria**: fatto non nel materiale (simboli non definiti)
- **Cosa non torna**: ρ1, ρ2, β1, β3 compaiono senza definizione in 4.1 (nessuna equazione; il glossario definisce solo β1, β3, ρ1). ρ2 (presumibilmente R × hype) non è definito né nel materiale né nel glossario. Il testo è fedele al CONTENUTO.
- **Verificato nel materiale**: sì per ρ1 (glossario), no per ρ2: "ρ1 and ρ2 compare the two groups." (CONTENUTO, senza definizione)
- **Chi lo risolve**: gruppo (definire i simboli, es. nella 4.1 o in Tab. 4)

## Note senza rilievo
- 3.2 e 4.2: ogni frase regge su CONTENUTO/glossario. In 4.2 «73 sector × year of round 1 clusters»: il materiale dice «73 sector × year clusters» («of round 1» è aggiunta coerente col glossario); 7,574/15,518/73 non sono nel log del materiale e la nota editoriale dice di controllarli (L2906): resta da verificare nel log, non nel materiale.
- 4.1: 9,124, 9,262, 41 cluster tutti nel CONTENUTO; N 9,263 coerente con 3.1/glossario. Nessun affermato che i pochi cluster siano risolti. cameron2008 e abadie2023 non citate: ammesso.

## Conteggio
high 0, medium 1, low 5. Trappole verificate: 11 su 11 (3.2: 3/3; 3.3: 3/3; 4.1: 3/3; 4.2: 2/2).
