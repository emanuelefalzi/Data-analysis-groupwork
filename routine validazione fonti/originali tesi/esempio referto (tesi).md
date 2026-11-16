# Referto loop 2 — 2026-09-03

**69 coppie verificate su 72.** Le tre mancanti (`ghemawat1991`, `miles1995`, `rumelt1984`) non hanno il PDF.

Esiti del lettore locale: **26 usabile · 35 da riformulare · 8 non usabile**

Ogni coppia è stata letta due volte in modo indipendente: dal lettore locale sul PDF e da NotebookLM. Sotto, l'ordine è per gravità, non per capitolo.

---


## 🔴 CONVERGENZA NEGATIVA — entrambi i lettori dicono che la fonte non regge  (7)

### **[mattone stretto]** `1.1.1` × (Ethiraj et al., 2005)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: Contradicts the claim: the source does frame a software services firm as generating value through projects delivered to specific clients, and does identify two salient capability classes, client-specific capabilities and project management capabilities (the latter reflecting technical capabilities in software design, development, and exec
- Nota: Claim composto: la parte su 'firm generates value through software projects and services delivered to specific clients' e sulla salienza di capacità tecniche/di project management è sostenuta dal testo; la clausola che decide il verdetto è 'developed through repeated interactions with the client' ri

### **[mattone stretto]** `1.2.1` × (Agrawal, Gans & Goldfarb, 2018)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: The source builds a distinction between prediction and judgment, not between execution and judgment; the word 'execution' never occurs in the paper, and there is no category defined as 'the application of codifiable procedures and knowledge'. Judgment is defined narrowly as the process by which a decision-maker determines the payoffs of a
- Nota: Il documento non usa mai il termine 'execution' e non definisce una componente 'application of codifiable procedures and knowledge': la dicotomia reale della fonte e' prediction/judgment, non execution/judgment (cercato 'execution', 'codifiable', 'codify': assente/estraneo al punto). La definizione 

### **[mattone stretto]** `3.2.4` × (Dierickx & Cool, 1989)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: Dierickx & Cool argue that the imitability of a firm's asset stocks depends on five characteristics of the accumulation process: time compression diseconomies, asset mass efficiencies, interconnectedness of asset stocks, asset erosion, and causal ambiguity. Interconnectedness refers to the fact that accumulating one asset stock may depend
- Nota: Claim in citazione congiunta con Reed & DeFillippi (1990), senza indicazione di quale fonte sostenga quale clausola. Dierickx & Cool coprono solo il tema generale dell'imitabilita' delle risorse/asset stock (tramite time compression diseconomies, asset mass efficiencies, interconnectedness, asset er

### **[mattone stretto]** `4.2.1` × (Connelly et al., 2011)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: Connelly et al. (2011) is a general review and synthesis of signaling theory in the management literature. It never discusses commitment as manifesting itself in specific, persistent investments, and none of the concrete examples in the claim (a dedicated team, roadmap, data model, certifications, governance, P&L) appear anywhere in the t
- Nota: ATTRIBUZIONE INCERTA: il contenuto sostanziale del claim (commitment manifesto in investimenti specifici e persistenti - team dedicato, roadmap, data model, certificazioni, governance, P&L - con la rinuncia all'ampiezza come evidenza e non definizione di commitment) non compare in Connelly et al. 20

### **[mattone stretto]** `6.2` × (Harkonen et al., 2015)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: This is a literature review that surveys and categorises prior academic work on the concept of 'productisation' (transforming offerings, whether products, services, software, or technologies, into standardised, repeatable, comprehensible product-like deliverables). It reports definitions, characteristics, benefits, and a research agenda d
- Nota: Cercati nel testo (con esito negativo): fixed cost, upfront, standardis/standardiz, codif, architecture, niche, volume, amortiz, market size, economies of scale, resource, barrier, risk, investment. Nessuno di questi concetti compare associato a un argomento economico sui costi fissi di transizione 

### **[mattone stretto]** `6.3` × (Prencipe & Tell, 2001)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper studies inter-project learning in project-based firms via six case studies, distinguishing experience accumulation, knowledge articulation and knowledge codification (following Zollo and Winter). In its literature-review section it reports, citing Cowan and Foray (1997), that if knowledge can be codified and commodified, transfe
- Nota: ATTRIBUZIONE INCERTA: la verifica preliminare sospettava che solo la parte sull'AI fosse un'estensione della tesi; ho controllato anche l'argomento generale richiesto ("limit case" di competenza perfettamente codificabile, esempio regulatory compliance, trasparenza e verificabilita' ex ante) e non t

### **[mattone stretto]** `6.4` × (Liu & Ma, 2024)
- Lettore locale: **non usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: Contradicts the claim: the paper models an expert who optimally chooses a coarse (binary) diagnostic signal over a precise one, even when information acquisition is costless, but it frames this choice as efficiency-restoring and profit-maximizing, not as a symptom of a market that fails to reward unobservable excellence. With the binary s
- Nota: Caso limite (d)/(e) applicato: non è semplice silenzio ma contraddizione di valenza. Il comportamento superficiale (diagnosi grossolana ottimale) e' effettivamente presente nel paper, ma la spiegazione causale del claim ('il mercato non premia economicamente l'eccellenza non osservabile' -> 'special


## 🟠 UN LETTORE DICE «NON USABILE» — da guardare  (13)

### **[mattone stretto]** `1.1.2` × (Ethiraj et al., 2005)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper distinguishes two capability classes in software services firms: client-specific capabilities and a second, more fungible class it calls 'the software development and project management capability,' which comprises three components: (i) software design and building capabilities, including designing an appropriate system or archi
- Nota: ATTRIBUZIONE INCERTA: il claim attribuisce alla fonte l'elenco 'development, integration, cloud, architecture and project management'; ho verificato con grep che la stringa 'cloud' non compare mai nell'intero testo (105.055 caratteri), e nessun elenco a cinque voci di questo tipo compare nel documen

### `1.2.3` × (Siddiq & Zhang, 2026)
- Lettore locale: **usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper presents what it frames as the first empirical test of AI-driven labor commoditization, using contract-level data from Upwork, a large online freelance labor market spanning many job categories (writing, software development, design, accounting, customer service, administrative support), not software production specifically. It 
- Nota: Fonte non peer-reviewed (working paper, giugno 2026); la regola 2 sul tetto a 'da riformulare' non scatta qui perche' il claim e' gia' formulato in modo cauto ('preliminary', 'without proving'), coerente con lo status di working paper. La porzione teorica del meccanismo (Fukui et al.) non e' valutat

### **[mattone stretto]** `1.3.1` × (Coff, 1999)
- Lettore locale: **usabile** · NotebookLM: **non usabile**
- Cosa dice davvero: Coff's bargaining-power model lists replacement cost / availability of substitutes as one of four determinants of a stakeholder's power to appropriate rent. The text states explicitly that suppliers of differentiated or specialized inputs have more bargaining power, and that if an input is irreplaceable the supplier would have significant
- Nota: Citazione congiunta con Teece 1986 e Bowman & Ambrosini 2000 per quattro condizioni; Coff 1999 sostiene solo la clausola 'difficulty of substitution' (terzo determinante del suo modello di bargaining power: disponibilita' di sostituti/costo di sostituzione), applicata esplicitamente ai supplier che 

### **[mattone stretto]** `2.2.2` × (Shrestha, Ben-Menahem & von Krogh, 2019)
- Lettore locale: **non usabile** · NotebookLM: **da riformulare**
- Cosa dice davvero: Shrestha et al. (2019) propose a framework of three organizational structures for combining human and AI-based decision making (full delegation, hybrid sequential, and aggregated), built around five ex-ante contingency factors: specificity of the decision search space, interpretability, alternative-set size, speed, and replicability. The 
- Nota: Claim citato congiuntamente con NIST (2023); il paragrafo non assegna le clausole. Delle quattro clausole del claim (continuous monitoring; management of anomalies and drift; human intervention; possibility of correcting or suspending unexpected behaviours), le prime due e l'ultima sono del tutto as

### **[mattone stretto]** `3.1.1` × (Nelson, 1970)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper develops and names the search/experience goods taxonomy: search goods are those whose quality the consumer can determine by inspecting them prior to purchase, while experience goods are those the consumer can only evaluate by purchasing and using them ('We will call this information process " experience."'). The article never us
- Nota: ATTRIBUZIONE INCERTA: la fonte compare in un elenco di riferimenti congiunto con Akerlof (1970) e von Nordenflycht (2010) dopo un paragrafo su adverse selection e hidden action, senza indicare quale concetto di Nelson sia invocato in quel punto. Il testo di Nelson 1970 non menziona mai 'adverse sele

### **[mattone stretto]** `3.2.2` × (Kahneman & Klein, 2009)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The source argues that genuinely skilled intuition/expertise requires two preconditions: an environment that offers stable, objectively identifiable ('valid') cues, and an adequate opportunity to learn those cues through prolonged practice and rapid, unambiguous feedback. It links genuine recognition-based skill to a learned repertoire of
- Nota: ATTRIBUZIONE INCERTA: il claim elenca quattro indicatori specifici come se fossero enunciati dalla fonte, ma questa lista non compare nel testo; sembra un'operazionalizzazione originale dello studente. La fonte offre ingredienti reali riusabili: il concetto di repertorio di pattern riconoscibili (Ch

### **[mattone stretto]** `4.1` × (Jaakkola, 2011)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: Jaakkola's qualitative study of productization practices in Finnish PSFs describes how managers make abstract services tangible and evaluable before purchase: they package services as 'service products' or 'service packages' 'to create a resemblance to physical, tangible products that can be assessed and evaluated by the customer', and ad
- Nota: Citazione congiunta con Harkonen et al. 2015, clausole non assegnate. Jaakkola copre solo la prima meta' del claim (rendere alcuni attributi valutabili/verificabili prima dell'acquisto), in termini pratici di 'tangibilizzazione', non nel lessico search/credence attribute; la seconda clausola ('witho

### **[mattone stretto]** `4.1.2` × (Voss & Hsuan, 2009)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper models a service architecture as nodes classified as either standard or unique (heterogeneous), occurring at any of four levels of decomposition from industry down to individual service component. Its hypothetical cruise example shows that different modules of the same system carry different concentrations of unique nodes (modul
- Nota: Claim citato congiuntamente con Ulrich 1995 e Baldwin & Clark 2000, senza assegnazione delle clausole. Questa fonte puo' sostenere solo la quota generale del claim (la localizzazione dell'eterogeneita'/adattabilita' in un'architettura modulare non e' fissa: puo' essere a livello aggregato o a livell

### **[mattone stretto]** `4.1.4` × (Nelson, 1970)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: Nelson (1970) develops a theory distinguishing 'search goods' - whose quality attributes the consumer can evaluate by inspection prior to purchase - from 'experience goods' - whose quality can only be ascertained by actually purchasing and consuming the good (e.g., a television's performance or expected repair needs cannot be determined b
- Nota: Citazione congiunta con Darby & Karni (1973) per il 'credence-good conceptual framework'. Il termine 'credence' non compare mai nel testo di Nelson (1970) e nemmeno il concetto (verificato con ricerca sull'intero file): Nelson tratta solo la dicotomia search/experience, non una terza categoria di be

### **[mattone stretto]** `4.2.2` × (Zollo & Winter, 2002)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper frames the three learning mechanisms (experience accumulation, knowledge articulation, knowledge codification) as positions on a continuum in the investment of financial, temporal and cognitive resources: higher investment produces the more deliberate, articulated/codified forms of learning, which yield a crisper, more explicit 
- Nota: ATTRIBUZIONE INCERTA: il claim e' dichiarato dalla tesi stessa come meta' 'internamente' di un argomento a due livelli costruito insieme a Spence (1973); la fonte qui valutata fornisce un ingrediente reale e riusabile (l'investimento di risorse come cio' che distingue l'apprendimento deliberato, art

### **[mattone stretto]** `4.3.1` × (Dierickx & Cool, 1989)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: Dierickx and Cool argue that assets freely tradeable in factor markets cannot ground a sustainable competitive advantage, precisely because rivals can acquire equivalent assets on the open market; sustainability instead requires assets to be nontradeable, nonimitable and nonsubstitutable. They illustrate this with 'generic labor', which i
- Nota: Claim congiunto con Rumelt 1984 (non disponibile in cartella), a cui appartiene propriamente il termine 'isolating mechanisms': Dierickx & Cool non lo usano mai, e propongono un proprio framework (asset non-tradeable/non-imitable/non-substitutable) funzionalmente analogo ma non identico, gia' segnal

### **[mattone stretto]** `4.3.2` × (Zuckerman, 1999)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The paper's core mechanism is that critics (securities analysts) specialize by product category, and because of this division of labor a critical review confers a specific kind of legitimacy: it signals membership in an accepted category, i.e. the seller's 'market identity'. This identity, attributed by specialist critics, is explicitly d
- Nota: Il nucleo della distinzione identity/offering è presente ed è argomentato (non solo menzionato): è la proposizione centrale del paper, sostenuta anche dalla frase su 'firm’s position in the network of analyst coverage establishes its market identity... firm’s self-definition' (poco più avanti nel te

### **[mattone stretto]** `6.1` × (Kirmani & Rao, 2000)
- Lettore locale: **da riformulare** · NotebookLM: **non usabile**
- Cosa dice davvero: The source's general signaling framework holds that a quality signal is credible only if it entails a real, forfeitable economic bond that a low-quality firm would lose by falsely claiming high quality: the credible commitment a firm offers can be of two types, loss of potential revenue (revenues at risk) or increases in costs (costs at r
- Nota: ATTRIBUZIONE INCERTA: applicando i tre test alla claim generale citata da sola in testa al nodo ("quality signals must entail a real risk to revenue in order to be credible"), il nucleo -- serve un bond economico reale e perdibile perche' il segnale sia credibile -- e' sostenuto dalla fonte, ma il t


## 🟡 DIVERGENZA FORTE fra i due lettori  (16)

### `1` × (Cho, Kim & Kim, 2026)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: This position paper (arXiv preprint, not peer-reviewed) argues that AI adoption does not automatically translate into productivity gains because human and organizational factors (workforce composition, individual baseline capability, learning curves, incentives for fair use, and goal flexibility) moderate the relationship between AI capab
- Nota: Tetto per regola 2 applicato: peer_reviewed = no (preprint arXiv, position paper), e il claim ('studies... show') e formulato come risultato di ricerca acquisito, quindi esito massimo da riformulare anche se il contenuto fosse pienamente allineato. Nota 2 dell'incarico: il claim era stato scritto pe

### **[mattone stretto]** `1` × (Fukui et al., 2026)
- Lettore locale: **usabile** · NotebookLM: **non verificabile**
- Cosa dice davvero: The paper develops a formal search-and-matching model of 'commoditization of labor', in which firms standardize a fraction of the tasks in a job; standardized tasks are performed equally well by any worker, so output on those tasks depends only on firm technology, not on worker know-how. As standardization rises, aggregate job output beco
- Nota: La fonte formalizza davvero, con un modello, il meccanismo per cui il cambiamento tecnico che standardizza i compiti riduce il peso del know-how/qualita del lavoratore (capitale umano) sull'output, rendendo i lavoratori piu intercambiabili. Il testo non menziona mai AI, digital markets o 'AI-exposed

### **[mattone stretto]** `1.1.5` × (Davenport, 1998)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Davenport's central thesis is exactly the tension the claim describes as 'misalignment': ES vendors build generic, one-size-fits-all systems, and adopting one 'pusbes a company toward generic processes even when customized processes may be a source of competitive advantage' -- he shows companies (an industrial-parts distributor, Compaq) r
- Nota: Claim con citazione congiunta (Soh 2000, Brehm 2001, Strong & Volkoff 2010): valuto solo la quota sostenibile da davenport1998. Sostenuti bene: 'strategically distinctive processes' (driver esplicito e centrale, citazione riportata) e 'misalignments between system and organization' (e' il tema porta

### **[mattone stretto]** `1.1.5` × (Soh et al., 2000)
- Lettore locale: **usabile** · NotebookLM: **non verificabile**
- Cosa dice davvero: The source's entire framework centers on ERP 'misfits,' defined as gaps between the functionality offered by the package and that required by the adopting organization, i.e. misalignment between system and organization. It shows these misfits (and the resulting customization/workaround decisions) arising specifically from public-sector-sp
- Nota: Claim citato congiuntamente con Davenport 1998, Brehm et al. 2001, Strong & Volkoff 2010, clausole non assegnate: ho valutato solo la quota sostenibile da questa fonte, senza declassarla per le clausole di competenza altrui. Soh et al. 2000 copre chiaramente 'misalignments between system and organiz

### **[mattone stretto]** `1.1.5` × (Strong & Volkoff, 2010)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Strong and Volkoff's grounded-theory case study is centered on 'misfits' between an organization and its enterprise system, i.e. exactly the concept the claim calls 'misalignments between system and organization', and it identifies six misfit domains (functionality, data, usability, role, control, culture). The paper explicitly states tha
- Nota: Claim citato congiuntamente con Davenport 1998, Soh et al. 2000, Brehm et al. 2001 per cinque possibili driver della domanda di customization, senza assegnare le clausole alle singole fonti. Ho valutato solo la quota che questa fonte può sostenere: 'misalignments between system and organization' e' 

### **[mattone stretto]** `1.2.2` × (Jarrahi, 2018)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Jarrahi argues AI outperforms humans on tasks tied to 'complexity': quantitative, computationally intensive work with computable criteria (e.g. predictive analytics, data-driven pattern detection), and that this advantage grows with more data. Humans retain the comparative edge on tasks tied to 'uncertainty' (novel situations with no prec
- Nota: Claim citato congiuntamente con Raisch & Krakowski 2021; il lessico specifico del claim ('standardized, codified and verified', 'trade-off assessment and consideration of the consequences of error') non compare mai in Jarrahi 2018 e sembra provenire dal framework di R&K. Jarrahi sostiene solo la ver

### **[mattone stretto]** `1.2.2` × (Raisch & Krakowski, 2021)
- Lettore locale: **usabile** · NotebookLM: **non verificabile**
- Cosa dice davvero: Raisch and Krakowski argue that a task's nature determines whether AI is used for automation or augmentation: relatively routine, well-structured tasks can be automated because their rules can be explicitly formulated and codified, whereas more complex managerial tasks resist rule-based automation and require augmentation instead. For the
- Nota: Citazione congiunta con Jarrahi (2018): ho valutato solo la quota sostenibile da Raisch & Krakowski, senza declassare per clausole eventualmente coperte solo dall'altra fonte. Il meccanismo (compiti di routine/codificabili -> automazione; compiti complessi che richiedono giudizio, bilanciamento fra 

### **[mattone stretto]** `1.2.3` × (Fukui et al., 2026)
- Lettore locale: **usabile** · NotebookLM: **non verificabile**
- Cosa dice davvero: The paper formalizes a model with two firm-level parameters: technology quality z (which the text itself labels "the productivity of firm z") and the degree of task standardization s. Proposition 4 shows these have opposite effects: increasing z raises the firm's wage, output per worker and vacancy-filling rate, while increasing s lowers 
- Nota: La citazione verbatim scelta ancora la clausola più specifica di questo claim rispetto al nodo 1 (dove la stessa fonte è già usabile per il meccanismo generale): la distinzione formale fra aumento di produttività (z, che il testo chiama esplicitamente 'the productivity of firm z') e aumento di stand

### **[mattone stretto]** `3.1.1` × (von Nordenflycht, 2010)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: The source discusses 'opaque quality' — the difficulty nonexperts (clients) have in evaluating the quality of an expert's output even after it is produced and delivered — as one of two core managerial challenges arising from knowledge intensity in professional service firms and knowledge-intensive firms generally. In a footnote the author
- Nota: Citazione congiunta con Akerlof 1970 e Nelson 1970, clausole non assegnate. Questa fonte copre bene la quota generale 'applying information-asymmetry concepts to the context of knowledge-intensive services': dedica un'intera sottosezione (Opaque quality) a un problema di asimmetria informativa appli

### **[mattone stretto]** `3.1.3` × (Aarikka-Stenroos & Jaakkola, 2012)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: This paper's central empirical finding is that value in knowledge intensive business services is co-created through a dyadic joint problem solving process, in which customers actively adopt roles such as co-diagnoser, co-designer, co-producer and co-implementor alongside supplier roles (value option advisor, value process organizer, value
- Nota: Citazione congiunta con Darby & Karni (1973); non e' indicato quale fonte sostenga quale clausola, quindi valuto solo la quota attribuibile a questa fonte. Clausola 'co-produced by supplier and client': ben sostenuta (livello dimostra) dal passaggio citato, che descrive esattamente questo tramite i 

### **[mattone stretto]** `3.2.3` × (Prencipe & Tell, 2001)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: The paper argues that knowledge articulation and codification are the cognitive processes through which tacit, individual knowledge is turned into explicit representations (agreed-upon representations, codebooks, manuals, procedures, project documents, databases) that can be transferred and diffused across the individual, project and orga
- Nota: Citazione congiunta con Coff, 1999, senza assegnazione delle clausole. Prencipe & Tell copre bene 'articulated', 'retained in routines' e la persistenza di un residuo tacito necessario all'applicazione ("the production of codified knowledge implies the production of new forms of tacit knowledge"), m

### **[mattone stretto]** `4.1` × (Harkonen et al., 2015)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Harkonen et al. (2015) is a literature review defining productisation as a process yielding an offering that is 'standardised, repeatable and comprehendible' (Finding 1), with repeatability explicitly named as a recognised characteristic across the product, service, software and technology categories (Table 8: 'Standardisation/systemisati
- Nota: Claim cited jointly with Jaakkola (2011); questo giudizio riguarda solo la quota sostenibile da Harkonen et al. (2015). La fonte copre: repeatability come termine esplicito (Finding 1, Table 8), e l'idea generale che la produttizzazione riduce l'ambiguita' sull'offerta e migliora la comprensione/com

### **[mattone stretto]** `4.1.1` × (Baldwin & Clark, 2000)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: The source, in the chapter section "A Complete Set of Design Rules," defines what a complete set of design rules for a modular technical system must specify: architecture (which modules will be part of the system and their roles), interfaces (detailed descriptions of how modules interact, fit together, connect and communicate), and integr
- Nota: Citazione congiunta con Jaakkola (2011): valuto solo la quota sostenibile da Baldwin & Clark. La clausola centrale del claim ("productization codifies... the part of the problem that recurs across clients... into a stable offering") non trova alcun riscontro qui: il testo non contiene mai le parole 

### **[mattone stretto]** `4.1.2` × (Baldwin & Clark, 2000)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: The source defines modularization as partitioning design parameters into visible information (design rules and interfaces) and hidden information (parameters left to module designers' discretion). It states that visible design parameters/design rules must be established before module tasks begin and, once fixed, are relatively costly and 
- Nota: peer_reviewed=no e claim formulato come risultato acquisito: per regola 2 il tetto e' 'da riformulare', anche se nel merito il riscontro e' fortissimo (Baldwin & Clark e' di fatto la fonte primaria dell'intera cornice concettuale usata dal claim: confine invariante/variabile = design rules/visible i

### **[mattone stretto]** `4.1.4` × (Darby & Karni, 1973)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Darby and Karni define credence qualities as properties whose value cannot be judged even after use, because measurable output is jointly produced by cooperating inputs of uncertain quality: 'The central problem in fraud is the existence of credence qualities due to the joint production of directly estimable output by cooperating factors 
- Nota: ATTRIBUZIONE INCERTA: la conversione specifica "produttizzazione -> attributi search" (perimetro, artefatti, demo, success criteria) non compare nel testo di Darby & Karni: la fonte fornisce solo l'ingrediente della cornice 'credence quality' (di cui e' l'origine, non Nelson) e, in modo affine ma no

### `4.3.3` × (Ennen & Richter, 2010)
- Lettore locale: **da riformulare** · NotebookLM: **non verificabile**
- Cosa dice davvero: Ennen & Richter (2010) is a peer-reviewed synoptic review of 108 empirical studies (1988-2008) on complementarities in organizations. It defines complementarity, in its abstract, as "the beneficial interplay of the elements of a system where the presence of one element increases the value of others," i.e. value arising from interaction ra
- Nota: ATTRIBUZIONE INCERTA: il claim applica il principio generale di complementarita (interazione, non somma) a costrutti specifici della tesi ("productization", "domain depth") che non compaiono in nessun punto del testo di Ennen & Richter 2010 (verificato con grep sull'intero file). La fonte e' una ras


## ⚪ Divergenza lieve  (14)

### **[mattone stretto]** `0.2.2` × (Brynjolfsson, Rock & Syverson, 2021)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `1` × (Agrawal, Gans & Goldfarb, 2018)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### `1` × (Peng et al., 2023)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### **[mattone stretto]** `1.1.1` × (Hobday, 2000)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### `1.1.4` × (Anitec-Assinform, 2025)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### **[mattone stretto]** `1.2.2` × (Shrestha, Ben-Menahem & von Krogh, 2019)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### `2.2.2` × (NIST, 2023)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### **[mattone stretto]** `3.1.2` × (Glückler & Armbrüster, 2003)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `3.1.2` × (Kirmani & Rao, 2000)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**

### **[mattone stretto]** `3.1.3` × (Darby & Karni, 1973)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `3.2.3` × (Coff, 1999)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `4.1.2` × (Ulrich, 1995)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `4.2.2` × (Spence, 1973)
- Lettore locale: **usabile** · NotebookLM: **da riformulare**

### **[mattone stretto]** `4.2.3` × (Zuckerman, 1999)
- Lettore locale: **da riformulare** · NotebookLM: **usabile**


## ✅ I due lettori concordano  (19)

### `1` × (Siddiq & Zhang, 2026)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### `1.1.1` × (Brady & Davies, 2004)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `1.1.1` × (den Hertog, 2000)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `1.1.1` × (Prencipe & Tell, 2001)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `1.1.2` × (Prencipe & Tell, 2001)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### `1.1.4` × (Assintel, 2025)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### `1.1.5` × (Brehm et al., 2001)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `1.3` × (Teece, 1986)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### `1.3.1` × (Bowman & Ambrosini, 2000)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `1.3.1` × (Teece, 1986)
- Lettore locale: **da riformulare** · NotebookLM: **da riformulare**

### **[mattone stretto]** `3.1.1` × (Akerlof, 1970)
- Lettore locale: **da riformulare** · NotebookLM: **da riformulare**

### **[mattone stretto]** `3.1.4` × (Teece, 1986)
- Lettore locale: **da riformulare** · NotebookLM: **da riformulare**

### **[mattone stretto]** `3.2.1` × (Cohen & Levinthal, 1990)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `3.2.1` × (Zollo & Winter, 2002)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `3.2.4` × (Reed & DeFillippi, 1990)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `4.1.1` × (Jaakkola, 2011)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `4.2.3` × (Hsu, Hannan & Koçak, 2009)
- Lettore locale: **usabile** · NotebookLM: **usabile**

### **[mattone stretto]** `4.2.4` × (Cohen & Levinthal, 1990)
- Lettore locale: **da riformulare** · NotebookLM: **da riformulare**

### **[mattone stretto]** `4.3.3` × (Milgrom & Roberts, 1995)
- Lettore locale: **da riformulare** · NotebookLM: **da riformulare**
