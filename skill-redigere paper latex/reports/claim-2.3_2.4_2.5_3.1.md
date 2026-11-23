# Claim audit 2.3, 2.4, 2.5, 3.1

## 2.3 Hot and cold markets

### CLM-2.3-01
- **Severità**: medium
- **Sede**: 2.3, ¶1 — "Theory predicts that abundant capital and greater VC competition weaken investors' bargaining power and raise valuations [[CIT-P:inderst2004]]."
- **Categoria**: claim allargato / cucitura
- **Cosa non torna**: la tesi di inderst2004 riguarda solo la competizione fra VC (piu' VC rispetto agli imprenditori) che sposta il potere negoziale e alza le valutazioni. "Abundant capital" viene dal nostro CONTENUTO (punto 1), non dalla fonte, ma e' dentro la frase citata.
- **Verificato nel materiale**: sì, qui: "more VC competition shifts bargaining to entrepreneurs and raises valuations (theory)"; "abundant capital" non compare nelle fonti.
- **Chi lo risolve**: fix-applier (togliere "abundant capital and" dalla frase citata o spostarlo in "In our setting")

### CLM-2.3-02
- **Severità**: low
- **Sede**: 2.3, ¶2 — "Investors in hot markets funded riskier, experimental ventures with less concern about follow-on financing risk [[CIT-P:nanda2013]]."
- **Categoria**: claim allargato
- **Cosa non torna**: il contesto di nanda2013 documenta solo piu' bancarotte e, per le IPO, valutazioni e brevetti piu' alti. "Experimental" e "less concern about follow-on" reggono solo sulla tesi vincolante, non sul contesto. Nessun altro rilievo: rimando a SEC:1 corretto.
- **Verificato nel materiale**: parziale, tesi: "in hot markets investors fund riskier startups, worrying less about follow-on"; "experimental" solo nel CONTENUTO.
- **Chi lo risolve**: fix-applier

## 2.4 Valuation steps

### CLM-2.4-01
- **Severità**: medium
- **Sede**: 2.4, ¶3 — "Later investors hold senior preferred shares, so post-money valuations overstate fair value."
- **Categoria**: orfana / cucitura (meccanismo di letteratura senza attribuzione)
- **Cosa non torna**: la frase causale sta prima delle citazioni; il meccanismo (azioni senior) non e' in nessun contesto di gornall2020 (solo: media 48% sopra il fair value per 135 unicorni) ne' di ewens2022 (termini contrattuali oltre la quota). Compare solo nel CONTENUTO, ed e' un'idea riconoscibile della letteratura.
- **Verificato nel materiale**: no, cercato e non trovato nei contesti delle fonti.
- **Chi lo risolve**: paper-writer (attribuire o attenuare)

### CLM-2.4-02
- **Severità**: low
- **Sede**: 2.4, ¶3 — "Entrepreneurs accepted lower valuations from more reputable VCs [[CIT-P:hsu2004]]."
- **Categoria**: claim allargato
- **Cosa non torna**: evidenza su 51 start-up MIT E-Lab, solo primo round professionale, confronto fra offerte (sconto 10-14%). La frase e' generale, senza condizioni.
- **Verificato nel materiale**: sì, qui: "entrepreneurs are willing to accept a discount on the valuation of their start-up in order to access the capital of VCs with better reputations"
- **Chi lo risolve**: fix-applier

## 2.5 Controls

### CLM-2.5-01
- **Severità**: high
- **Sede**: 2.5, ¶4 — "Better-networked VCs see more exits."
- **Categoria**: letteratura non attribuita
- **Cosa non torna**: risultato di hochberg2007 (VC meglio connessi, portfolio con piu' probabilita' di sopravvivere a round successivi e di uscire; fonte presente nel materiale) scritto senza CIT-P, come fatto. Non e' nel LEDGER.
- **Verificato nel materiale**: sì, hochberg2007: "better-networked VCs perform better; their ventures survive to later rounds"
- **Chi lo risolve**: gruppo (escalation), poi paper-writer per il token CIT-P

### CLM-2.5-02
- **Severità**: high
- **Sede**: 2.5, ¶4 — "CVCs back innovative firms and acquire them."
- **Categoria**: letteratura non attribuita
- **Cosa non torna**: idea da chemmanur2014 (CVC-backed piu' innovative, brevetti) e ma2020 (parent con innovazione interna in calo), senza citazione. "Acquire them" non e' sostenuto: ma2020 parla di integrare le tecnologie, non di acquisizione delle startup.
- **Verificato nel materiale**: no per "acquire"; chemmanur2014: "CVC-backed firms are more innovative"
- **Chi lo risolve**: gruppo (escalation)

### CLM-2.5-03
- **Severità**: high
- **Sede**: 2.5, ¶4 — "Ventures funded by angel groups are more likely to survive"
- **Categoria**: letteratura non attribuita / claim allargato
- **Cosa non torna**: da kerrlerner2014 (regression discontinuity, 130 deal di due gruppi di angel, 2001-2006); senza citazione e senza condizioni. Per l'exit la fonte non trova significativita'.
- **Verificato nel materiale**: sì, kerrlerner2014: "angel funding goes with higher survival and growth just above the threshold (RD); exit is not significant"
- **Chi lo risolve**: gruppo (escalation)

### CLM-2.5-04
- **Severità**: high
- **Sede**: 2.5, ¶4 — "some accelerators speed up development"
- **Categoria**: letteratura non attribuita
- **Cosa non torna**: da hallen2020 (acceleratori USA early, campione piccolo), senza citazione.
- **Verificato nel materiale**: sì, hallen2020: "some accelerators speed up venture development"
- **Chi lo risolve**: gruppo (escalation)

### CLM-2.5-05
- **Severità**: low
- **Sede**: 2.5, ¶4 — "Closer VC monitoring raised innovation and IPO rates [[CIT-P:bernstein2016]]."
- **Categoria**: over-claim lieve
- **Cosa non torna**: la fonte e' un DiD su tagli del tempo di viaggio (IPO +1,0%, exit +1,4%), non su exit in generale; il verbo "raised" e' al passato ma senza il disegno.
- **Verificato nel materiale**: sì, "closer VC monitoring raises innovation and IPO rates"
- **Chi lo risolve**: fix-applier

### CLM-2.5-06
- **Severità**: low
- **Sede**: 2.5, ¶2 — "Cheaper experimentation went with smaller initial cheques across more ventures [[CIT-P:ewens2018]]."
- **Categoria**: claim allargato
- **Cosa non torna**: evidenza su un solo shock (AWS), settori software/servizi, 2002-2010; la frase suona generale.
- **Verificato nel materiale**: sì, "cheaper experimentation means smaller first cheques to more ventures"
- **Chi lo risolve**: fix-applier

### CLM-2.5-07
- **Severità**: low
- **Sede**: 2.5, ¶5 — "sector fixed effects to absorb industry differences in success rates and maturation speed"
- **Categoria**: fatto non nel materiale
- **Cosa non torna**: affermazione sul mondo senza citazione; gompers2009 non sostiene differenze permanenti (indicata come non supportata) e lerner2020 regge solo la velocita' di maturazione. Formulata come motivazione di disegno, quindi lieve.
- **Verificato nel materiale**: parziale (lerner2020 solo maturazione)
- **Chi lo risolve**: fix-applier

## 3.1 Sample construction

Nessun rilievo. Tutti i numeri (57,751; 28,478 = 15,518 + 12,960; 9,263 = 4,483 + 4,780; 30 June 2022; gap <= 10 anni) coincidono con CONTENUTO e con le celle di T3; T3 richiamata; nessuna definizione di log_gap_r2 o heat; nessuna discussione di validita' esterna.

## Conteggio

- high: 4
- medium: 2
- low: 5
- Trappole verificate: 12 su 12 (2.3: 3, 2.4: 2, 2.5: 4, 3.1: 3). Nessuna violata: niente Accelerator_pre_r1, nessuna stima in 2.5, β3 non spiegato in 2.3, nessun numero sullo step in 2.4.
- Linguaggio causale su gap/hype: nessuno. Citazioni verbatim: nessuna. Duplicati: gompers2000 e nanda2013 ripetuti come rimandi, ammessi.
