# Proposte di riformulazione: righe «da riformulare»

Generato il 16/11/2026 dalla routine validazione fonti (`tabella.csv`, 53 righe `da riformulare`).
**Sono proposte, non decisioni**: `scaletta.md` non è stato modificato. Il gruppo decide quali adottare.

Regole seguite:
- Ogni proposta si limita alla colonna `estrazione` del lettore: la tesi si stringe, non si allarga mai.
- Le tesi sono in inglese e nello stile corto del blocco **Sources** di `scaletta.md`.
- ⧉ = stessa tesi condivisa da più fonti (stesso punto elenco). Si propone **una sola** formulazione che valga per tutte.
- Ogni verdetto è una lettura singola (un lettore Sonnet per fonte), controllata solo meccanicamente (la citazione esiste nel txt).

## 1 · Motivazione
| Riga | Tesi attuale | Proposta |
|---|---|---|
| 1 Tian (2011) | more and shorter rounds when the VC is far; more staging goes with better outcomes | more and shorter rounds when the VC is far; more rounds go with better IPO outcomes only for distant firms |
| 1 Nanda & Rhodes-Kropf (2013) | startups first funded in hot markets fail more often but are more innovative when they succeed | hot-market startups go bankrupt more often; those that IPO are valued higher and patent more |

## 2.1 · Lo staging come opzione
| Riga | Tesi attuale | Proposta |
|---|---|---|
| Cornelli & Yosha (2003) | staging with convertible securities keeps the option to stop | staging gives the VC the option to abandon; convertibles deter window dressing of interim results |
| Bergemann & Hege (2005) | each period without good news lowers the investor's belief | each period without success lowers the investor's belief that the project is good (theory) |
| Ewens et al. (2018) | entrepreneurship as experimentation; cheaper experimentation changes how VC funds early bets | VC rounds as experiments; cheaper start-up costs led VCs to fund more startups with smaller first cheques |
| Li (2008) | hazard models of round duration in a real-options framework | duration model (Weibull AFT, right-censored) of the time between rounds, in a real-options framework |
| Hoenen et al. (2014) | the signalling value of patents is strong at round 1 and largely gone by round 2 | patent *applications* raise round-1 funding but not round-2 funding (US biotech, 2001–2011) |

## 2.2 · Abbandono
| Riga | Tesi attuale | Proposta |
|---|---|---|
| Dahiya & Ray (2012) ⧉ con Bergemann & Hege | abandonment of stalled ventures | abandonment of ventures whose early returns fall short (theory) |
| Guler (2007) | VC firms keep funding under-performing ventures for political and institutional reasons | VCs become less likely to terminate as rounds accumulate, despite falling expected returns; politics may contribute |

## 2.3 · Mercati caldi
| Riga | Tesi attuale | Proposta |
|---|---|---|
| Gompers et al. (2008) | VC investment responds to public-market signals; experienced VCs expand most in hot markets without lower success | VC investment responds to industry Q; experienced VCs expand most, with no significant drop in success |
| Inderst & Mueller (2004) | abundant capital lowers investors' bargaining power and raises start-up values | more VC competition shifts bargaining to entrepreneurs and raises valuations (theory) |
| Nanda & Rhodes-Kropf (2013) | hot-market cohorts fail more but innovate more | come la riga 1 (oppure solo un rimando alla 1) |

## 2.4 · Valutazioni e clausole
| Riga | Tesi attuale | Proposta |
|---|---|---|
| Kaplan & Strömberg (2003) | rounds and contract rights are tied to milestones | within a round, release of committed funds and some rights are contingent on milestones |
| Gornall & Strebulaev (2020) | post-money valuations overstate fair value (by about half on average for unicorns, per v4) | post-money overstates fair value by 48% on average for 135 US unicorns |
| Heughebaert & Manigart (2012) | investor types with more bargaining power negotiate lower prices | university and government VCs value firms lower than independent VCs (Belgium) |

## 2.5 · Selezione, investitori, uscita, cluster
| Riga | Tesi attuale | Proposta |
|---|---|---|
| Gompers et al. (2020) | VCs select deals mainly on the team; selection matters more than value added | VCs rank the team as the top selection factor and see selection as more important than value-add (survey) |
| Sørensen (2007) | sorting explains about twice as much of the outcome difference as influence (per v4) | sorting is almost twice as important as influence for IPO rates (CA and MA, 1982–95) |
| Hellmann & Thiele (2015) ⧉ con Hellmann et al. (2021) | angels and VCs as substitutes or complements in early financing | angels and VCs as sequential investors: friends and foes (theory; dynamic substitutes in BC data) |
| Nahata (2008) | VC reputation goes with better investment performance | VCs with a higher IPO-capitalisation share go with more successful exits and faster IPOs |
| Ma (2020) | CVC invests to source external innovation | firms whose internal innovation has declined set up CVC to access startup technology |
| Kerr et al. (2014) | angel-group funding improves survival and growth (regression discontinuity) | angel funding goes with higher survival and growth just above the threshold (RD); exit is not significant |
| ⧉ Yu (2020), Hallen et al. (2020), Gonzalez-Uribe & Leatherbee (2018) | accelerators help ventures resolve uncertainty early | accelerator firms close earlier and more often, *suggesting* faster learning about quality (Yu); some accelerators speed up development (Hallen) |
| Gompers (1996) | young VC firms push for early exits to build reputation (grandstanding) | young VCs take firms public earlier, consistent with grandstanding (IPOs only) |
| ⧉ Lerner (1994), Pástor & Veronesi (2005) | IPO windows open and close with market conditions | IPOs cluster when market valuations are high (Lerner: biotech; Pástor & Veronesi: theory of IPO waves) |
| Abadie et al. (2023) | cluster at the level at which the regressor is assigned | cluster at the level of treatment assignment, when sampling is not clustered |

## 4 · Metodo
| Riga | Tesi attuale | Proposta |
|---|---|---|
| 4.1 Cameron et al. (2008) | with few clusters, cluster-robust p-values are too small; the wild cluster bootstrap fixes this | with few clusters (5–30) cluster-robust tests over-reject; wild cluster bootstrap-t brings size near 5% (linear models) |
| 4.1 Abadie et al. (2023) | cluster at the level of treatment assignment | come la riga 2.5 |
| 4.3 Cameron et al. (2008) | the reason robust vs clustered SEs is a relevant check | SEs that ignore within-cluster correlation can greatly understate the true SEs |
| 5.4 Cameron et al. (2008) | why robust vs clustered SEs matters | come la riga 4.3 |

## 5.3–5.6 · Risultati e discussione
| Riga | Tesi attuale | Proposta |
|---|---|---|
| 5.3 Kaplan & Strömberg (2003) | the milestone view of 2.4 | milestones govern release of funds within a round, not the timing of the next round |
| 5.4 Gompers (1996) | grandstanding, the prediction our young-lead coefficient contradicts | grandstanding predicts young VCs bring firms to IPO earlier *(il "contradicts" va detto come risultato nostro)* |
| ⧉ 5.5 Gompers (1995), Tian (2011) | short rounds for riskier or harder-to-monitor ventures | shorter rounds where agency costs are higher (Gompers) or the VC is far, so monitoring is costlier (Tian) |
| 5.5 Korteweg & Sorensen (2010) | selection at refinancing | valuations are observed only at refinancing or exit, so observed valuations are a selected sample |
| ⧉ 5.5 Gompers & Lerner (2000), Nanda & Rhodes-Kropf (2013) | the hot-market reading behind H2 | in hot markets capital chases deals, so prices rise (G&L) and investors fund riskier startups, worrying less about follow-on (N&RK) |
| 5.5 Gompers et al. (2008) | hot-market investment by experienced VCs is not less successful; exit depends on public markets | experienced VCs' hot-market deals show no significant drop in success *(togliere "exit depends on public markets")* |
| 5.5 Lerner (1994) | IPO timing follows market conditions | biotech IPOs cluster at peaks in equity valuations (1978–92) |
| 5.5 Gompers et al. (2020) ⧉ con Sørensen (2007) | selection vs influence | VCs see selection as more important than value-add (survey); Sørensen estimates sorting ≈ 2× influence |
| 5.5 Hoenen et al. (2014) | information at round 2 is largely priced (Table 14, H1 row) | information asymmetries fall after round 1, so the patent signal stops mattering at round 2 |
| 5.5 Guler (2007) | tolerance for failure (Table 14, H1b row) | VCs are reluctant to terminate as rounds accumulate |
| 5.6 Gornall & Strebulaev (2020) | post-money overstates fair value | post-money overstates fair value for US unicorns (48% on average) |

### 5.5 «control-sign comparisons»
Nessuna delle cinque fonti la sostiene così com'è scritta. Si propone di sostituirla con un elenco, una riga per fonte, con la parte effettivamente confrontabile:
- Hochberg et al. (2007): first rounds led by corporate VCs are less likely to survive to the next round.
- Haltiwanger et al. (2013): the size–growth relationship vanishes once firm age is controlled for.
- Chemmanur et al. (2014), Kerr et al. (2014) e Yu (2020): da togliere su questo punto (risultano `non usabile` / `non verificabile`), perché non riportano segni dei controlli utilizzabili.

## 6 · Conclusione e limiti
| Riga | Tesi attuale | Proposta |
|---|---|---|
| 6.1 Gompers et al. (2020) | VCs select mainly on the team | VCs rank the team as the top selection factor, somewhat ahead of business factors |
| ⧉ 6.1 Gompers (1995), Tian (2011) | round length chosen by the investor according to risk and monitoring costs | VCs set round length weighing agency and monitoring costs *(togliere "risk")* |
| 6.3 Korteweg & Sorensen (2010) | outcomes observed only at refinancing are selected | valuations observed only at refinancing or exit are a selected sample |
| 6.4 Li (2008) | hazard models of round duration (a model of point 1) | Weibull duration model of time between rounds, with right-censoring |
| 6.4 Howell et al. (2020) | VC follows the economy down (supply-side variation) | VC activity falls in recessions, mostly early-stage; capital-supply frictions are one likely mechanism |

## Scelte per il gruppo (non solo riformulazioni)
1. **Abadie et al. (2023), righe 2.5 e 4.1:** applicare la loro regola a `heat` è un'estensione nostra, perché `heat` non è un trattamento assegnato. Si può dire esplicitamente o citare Abadie solo per la logica generale.
2. **Gonzalez-Uribe & Leatherbee (2018):** l'idea che gli acceleratori risolvano prima l'incertezza è di Yu e di Smith & Hannigan, loro la riportano soltanto. Conviene togliere la loro citazione da questo punto.
3. **5.4 Gompers (1996):** che il nostro coefficiente sui lead giovani «contraddica» il grandstanding va scritto come risultato nostro (R-xx), non come tesi della fonte.
