> Nota per l'essay: libreria copiata dalla tesi. Dove cita capitoli, budget o il Cap. 5
> della tesi, leggi «l'essay» e i vincoli di `progetto.json`. Il filtro accademico vale identico.

# Pattern anti-slop per il `prose-auditor` — libreria curata

Estratta da tre skill installate in `~/.claude/skills/`:

- **`unslop`** (v2.3.0, `~/.claude/skills/unslop/`) — `references/taboo-phrases.md`,
  `references/edit-library.md`, `references/core-contract.md`.
- **`no-ai-slop`** (`~/.claude/skills/no-ai-slop/SKILL.md`).
- **`stop-slop`** (`~/.claude/skills/stop-slop/SKILL.md`,
  `references/{phrases,structures,examples}.md`).

Ogni voce sotto è marcata **ATTIVA** (usala così com'è), **RIFORMULATA** (la regola
sorgente esiste ma va applicata con un vincolo più stretto in una tesi), o
**DISATTIVATA** (la regola sorgente esiste ma è sbagliata qui, con il motivo).

Il `prose-auditor` (§4.4 del prompt orchestratore) gira **una volta sola**, dopo
l'ultimo capitolo, sul documento intero, **non** dentro `/tesi-audit`. Il suo mandato
resta quello del §4.4: grammatica inglese accademica con attenzione agli errori tipici
di un madrelingua italiano, periodi oltre le 45 parole, catene di genitivi — **più**
questi pattern.

---

## 1. Coppie antitetiche (binary contrasts) — ATTIVA

Fonte: `stop-slop/references/structures.md`, `no-ai-slop` "Binary contrasts",
`unslop/edit-library.md`.

| Pattern | Perché è un tell |
|---|---|
| "Not because X. Because Y." / "Not X, it's Y." | Rovesciamento telegrafato |
| "[X] isn't the problem. [Y] is." | Reframe formulaico |
| "The question isn't X. It's Y." | Diversivo retorico |
| "not just X but also Y" | Hedge additivo senza contenuto nuovo |

**In una tesi**: questi pattern comprimono un confronto argomentativo in una figura
retorica invece di argomentarlo. Finding: riscrivere come due affermazioni dirette,
la seconda giustificata da una fonte o da un passaggio del ragionamento, non da
opposizione stilistica alla prima.

**Non toccare**: un contrasto teorico legittimo fra due posizioni della letteratura
(es. "Ghemawat and Del Sol (1998) attribute the effect to X, whereas Peteraf (1993)
attributes it to Y") non è questo pattern. La differenza è se il contrasto porta
un'attribuzione verificabile o solo un effetto retorico.

## 2. Frasi-ponte vuote (throat-clearing) — ATTIVA

Fonte: `stop-slop/references/phrases.md` "Throat-Clearing Openers", `no-ai-slop`.

Esempi da cercare: "It is worth noting that…", "It should be emphasized that…", "The
following section explores…", "Building on the above, it becomes clear that…",
"Turning now to…", "It is important to note that…".

**In una tesi**: queste aperture non affermano niente di verificabile e occupano
budget di parole in un regime dove il Cap. 5 eccede già di 3.743 parole (§3 del prompt
orchestratore). Finding: cancellare l'apertura, far iniziare la frase con
l'affermazione stessa.

**Non toccare**: il metadiscorso esplicitamente ammesso da `CLAUDE.md`
("`This thesis…` solo nel Cap. 0 e nell'abstract, `This chapter…` solo nel primo e
nell'ultimo paragrafo di un capitolo") non è slop in quei punti: è la convenzione
decisa da GATE 2 (`AG-04`). Segnalalo solo se compare **fuori** da quei punti.

## 3. Chiuse pseudo-profonde (fake-profound kickers) — ATTIVA

Fonte: `no-ai-slop` "Fake-profound kickers", `stop-slop/references/structures.md`
"Dramatic Fragmentation", `unslop/edit-library.md`.

Esempi: un ultimo periodo di paragrafo che trasforma l'argomento appena fatto in
un'aforisma o in una metafora ("This is what differentiation really means in an age of
generative AI."), frammenti drammatici ("Speed. Quality. Cost. Pick two."), chiusure
"In conclusion, / Ultimately, / Overall," seguite da un riassunto di ciò che il
paragrafo ha appena detto.

**In una tesi**: una tesi non ha bisogno di un mic-drop a fine paragrafo. Finding:
cancellare la frase, o sostituirla con l'ultima affermazione verificabile che il
paragrafo aveva già fatto.

## 4. Avverbi di rinforzo usati al posto di un argomento — RIFORMULATA

Fonte sorgente: `stop-slop/references/phrases.md` "Adverbs — Kill all adverbs. No
-ly words." e `no-ai-slop` "Often-empty adverbs".

**Le librerie sorgente vietano la classe intera.** È la regola sbagliata qui, e va
disattivata come divieto generale: **il filtro accademico è obbligatorio** (istruzione
esplicita del prompt che ha commissionato questa libreria). Un avverbio che **limita**
un'affermazione — `largely`, `partly`, `typically`, `primarily`, `broadly`,
`arguably`, `plausibly`, `potentially`, `relatively`, `somewhat` — è **hedging**: è
lo strumento con cui una tesi evita di affermare più di quanto la fonte sostenga.
**Non si tocca mai**, per istruzione esplicita del §11 del prompt orchestratore
("Non rimuovere l'hedging che protegge da un over-claim") e della regola sovrana.

**Resta attivo, riformulato**, solo il sottoinsieme di avverbi che **sostituiscono**
un argomento invece di limitarlo — quelli che affermano certezza senza fornirla:
`clearly`, `obviously`, `undoubtedly`, `certainly`, `undeniably`, `evidently` (quando
non introduce una vera evidenza), `naturally` (nel senso di "ovviamente"). Se uno di
questi compare e la frase non porta una fonte o un passaggio dimostrativo a supporto,
è un finding: non perché è un avverbio, ma perché **afferma la certezza al posto di
argomentarla** — è la classe "over-claim" che il `claim-auditor` cerca anche a livello
di frase intera (§4.2), qui applicata al singolo avverbio.

Avverbi puramente di intensità colloquiale (`really`, `just`, `literally`,
`honestly`, `simply`, `actually`, `truly`) restano un finding **solo** se non portano
alcuna funzione tecnica nella frase — raro in prosa accademica, quindi questa
sotto-regola avrà pochissime occorrenze attese, e non va applicata in automatico a
`actually`, che in questa tesi ha anche un significato tecnico specifico legato al
registro accademico-italiano (falso amico elencato al §4.4: attenzione a
`actually`/`eventually` come calchi, non solo come riempitivo).

## 5. Passivo — RIFORMULATA (in gran parte disattivata)

Fonte sorgente: `stop-slop` "Use active voice… No passive constructions" (regola 3 e
Quick Checks), `stop-slop/references/structures.md` "Passive Voice", `no-ai-slop`
"Use active voice", `unslop/edit-library.md` Pattern 12.

**Le librerie sorgente vietano il passivo in blocco.** Anche questa è la regola
sbagliata qui, per un motivo strutturale, non stilistico: `CLAUDE.md` e il rilievo
`AG-04` (GATE 2, chiuso) impongono **mai la prima persona, né singolare né plurale**,
in tutta la tesi. Un divieto assoluto di passivo, applicato alla lettera, ha solo due
uscite: (a) inventare un soggetto agentivo per ogni frase — che è esattamente la
**falsa agentività** ("the data tells us", "the market rewards") che le stesse
librerie vietano come pattern separato (voce 7 sotto), applicata qui a costrutti come
meccanismi teorici, fonti, o "questa tesi" fuori dai punti ammessi da `CLAUDE.md`; oppure
(b) violare il divieto di prima persona per nominare un soggetto umano che non esiste
nel testo (l'autore, "we", il lettore). Nessuna delle due è accettabile: **il divieto
di passivo in blocco è disattivato per questa tesi.**

**Resta attivo, ristretto**, solo il passivo **evitabile senza le due uscite sopra**:
quando la frase ha già, nel proprio contenuto, un attore non-umano legittimo che il
passivo nasconde senza motivo — una fonte, un meccanismo, ELFO come attore di mercato.
Esempio: "It has been shown that switching costs increase with customisation" quando
`Estratti` attribuisce chiaramente l'affermazione a una fonte con chiave ammessa →
finding, riscrivere come `[[CIT-N:chiave]]` narrativa ("Author (Year) shows that…").
Questo caso non è "elimina il passivo": è "l'attribuzione mancante nasconde la fonte",
e si sovrappone al mandato del `claim-auditor`, non è un pattern di stile puro.

**Non toccare mai**: il passivo usato per descrivere un processo, un metodo, o un
risultato quando nominare l'attore non aggiungerebbe informazione verificabile
("the survey was administered to 42 respondents") — è la forma standard della prosa
accademica in questo registro, non un tell da testo generato.

## 6. `which` — RIFORMULATA (quasi interamente disattivata)

Fonte sorgente: `stop-slop/references/structures.md` "Sentence Starters to Avoid —
Sentences starting with What, When, Where, Which, Who, Why, How → Restructure."

**La regola sorgente vieta ogni frase che inizia con un pronome Wh-, `which` incluso.**
Applicata a una tesi, colpirebbe anche le proposizioni relative — che in inglese
accademico sono lo strumento normale per aggiungere una precisazione o una condizione
senza spezzare il periodo o ripetere il soggetto. **Disattivata come divieto sulle
proposizioni relative.** Non è mai un finding che una frase contenga `..., which
implies that…` o `a mechanism which operates only under conditions X`.

**Resta attivo solo il caso stretto** della regola sorgente: una frase che **inizia**
il periodo con `Which` come domanda retorica rivolta al lettore ("Which of these
explanations holds? "). Questo sì è un tell da prosa generata rivolta a un pubblico
generalista, e non ha mai una ragione d'essere in una tesi, che non pone domande al
lettore.

## 7. Falsa agentività (false agency) — ATTIVA, con un'aggiunta specifica di questa tesi

Fonte: `stop-slop/references/structures.md` "False Agency", `no-ai-slop`
"Use active voice… inanimate things do human verbs".

Pattern: un soggetto inanimato che compie un verbo umano — "the data tells us", "the
market rewards efficiency", "the mechanism decides", "the framework reveals".

**In una tesi**: si sovrappone parzialmente alla voce 5 (passivo), ma è un pattern
distinto — qui il soggetto è presente ma sbagliato, non assente. Finding: nominare
l'attore reale (una fonte con `[[CIT-N/P:...]]`, ELFO, un meccanismo definito, mai "the
company" — vietato esplicitamente da `CLAUDE.md`) o riformulare come proprietà del
meccanismo invece che azione.

**Aggiunta specifica**: attenzione a "the framework/model/thesis shows/demonstrates
that…" quando il soggetto grammaticale è il documento stesso, fuori dai punti in cui
`CLAUDE.md` ammette il metadiscorso (`This thesis…` solo Cap. 0 e abstract). È lo
stesso pattern applicato al caso più frequente atteso in questa tesi.

## 8. Puffery da importanza (importance puffery) — ATTIVA

Fonte: `no-ai-slop` "Importance puffery", `stop-slop/references/phrases.md`
"Vague Declaratives".

Esempi: "marks a pivotal shift", "plays a vital role", "underscores its significance",
"represents a significant departure", "The implications are significant", "The reasons
are structural" senza dire quali.

**In una tesi**: dichiarare importanza senza mostrarla è esattamente il contrario del
lavoro che una tesi deve fare — ed è distinguibile dall'over-claim (voce 4) perché qui
il problema non è la certezza ingiustificata su un fatto, ma la vaghezza su
*cosa* si sta affermando. Finding: sostituire con il dato specifico, o cancellare se il
dato specifico è già nella frase precedente.

## 9. Attribuzione debole (weasel attribution) — ATTIVA, con lookup obbligato

Fonte: `unslop/references/taboo-phrases.md` (tabella "Which experts? Name them or
cut."), `no-ai-slop` "Weasel attribution".

Esempi: "experts agree", "research suggests" (senza chiave), "studies show", "it is
widely believed".

**In una tesi**: questo pattern **coincide** con un mandato già assegnato al
`claim-auditor` (§4.2, "citazioni assenti da `Estratti`") e al gate delle fonti (§7).
Il `prose-auditor` lo segnala come pattern di superficie, ma la sua correzione non è
mai "riformulare la frase per suonare meno vaga": è "trovare la chiave in
`fonti_ammesse[]` del nodo o dichiarare `[[CIT-NEEDED: motivo]]`". Non risolverlo da
solo: è un finding che va verso `claim-auditor`/`node-writer`, non verso
`fix-applier`.

## 10. Sinonimia forzata (synonym cycling) — ATTIVA

Fonte: `no-ai-slop` "Synonym cycling".

Pattern: ruotare fra sinonimi dello stesso concetto per varietà stilistica invece di
ripetere il termine esatto.

**In una tesi, questo pattern è più grave che nella prosa generica**: il glossario
(`FONTI/pipeline/glossario/glossario.json`, 48 termini) impone una forma canonica per
concetto, con `varianti_vietate` esplicite. Il lint terminologico (§4.7) blocca già le
varianti vietate note; il `prose-auditor` segnala il caso più ampio — sinonimia non
ancora catalogata nel glossario, ma che rischia di introdurre ambiguità terminologica —
e **il glossario batte sempre `prose`** in caso di conflitto (§10 punto 4 del prompt
orchestratore): se seguire questo pattern romperebbe una forma già fissata dal
glossario, vince il glossario.

## 11. Colon reveals — ATTIVA

Fonte: `no-ai-slop` "Colon reveals".

Pattern: "The detail that makes it work: a separate mechanism absorbs the cost." —
un'affermazione, due punti, una rivelazione a effetto.

**In una tesi**: riscrivere come frase piana. I due punti restano legittimi per liste,
etichette, o citazioni dirette (rare, §8 vieta comunque le citazioni testuali), non per
effetto drammatico.

## 12. Ritmo robotico e liste puntate — RIFORMULATA

Fonte: `stop-slop` "Vary rhythm… Two items beat three", `no-ai-slop` "Robotic rhythm",
"Formatting slop — bullet lists where two sentences of prose would read better".

**In una tesi, questa regola cambia di segno su un punto preciso**: §4.1 del prompt
orchestratore vieta esplicitamente le liste puntate nel corpo ("Prosa continua, niente
liste puntate"). Non è quindi una preferenza stilistica del `prose-auditor`: è già un
vincolo strutturale a monte, verificato più severamente lì. Il `prose-auditor` verifica
solo il resto della regola sorgente — evitare tre frasi consecutive della stessa
lunghezza/forma sintattica, evitare che ogni paragrafo finisca con lo stesso tipo di
chiusura — che restano pattern di superficie legittimi.

## 13. Em dash usati come pausa — ATTIVA (coincide con la skill `long-dash`)

Fonte: `stop-slop` "No em dashes" (regola 6 e Quick Checks), `no-ai-slop` "Em dashes".
Menzionato esplicitamente anche al §4.4 del prompt orchestratore come bersaglio diretto
del `prose-auditor`.

**In una tesi**: l'em dash o l'en dash usato come pausa drammatica va sostituito con la
punteggiatura naturale (virgola, punto, due punti, parentesi) — esattamente il lavoro
già fatto dalla skill di progetto `long-dash` (`~/.claude/skills/long-dash/`, non parte
di questa libreria ma disponibile separatamente). Il `prose-auditor` segnala le
occorrenze; non serve reinstallare `long-dash` come stadio, basta applicare la stessa
sostituzione nodo per nodo tramite `fix-applier` (sostituzione locale, non riscrittura
strutturale — non cambia cosa la frase afferma).

## 14. Riassunti-recap e "In conclusion" — ATTIVA, con un'eccezione dichiarata

Fonte: `no-ai-slop` "Summary-recap endings".

**In una tesi**: un paragrafo di chiusura capitolo che riassume punto per punto quanto
già detto è slop nella prosa generica ma può coincidere con una funzione richiesta
altrove nel prompt — verificare prima se quel paragrafo è il punto in cui `ruolo` del
nodo richiede esplicitamente un "Aggancio" al capitolo successivo (52 nodi su 129, §3).
Se sì, non è un recap superfluo: è la transizione richiesta, e va lasciata. Il finding
scatta solo quando il paragrafo ripete affermazioni già fatte **senza** introdurre
l'aggancio al nodo/capitolo successivo.

---

## Pattern delle librerie sorgente lasciati fuori per intero

Non hanno equivalente in una tesi accademica, quindi non sono nemmeno "disattivati con
motivo": semplicemente non si applicano, e includerli avrebbe solo allungato questo
file senza dare al `prose-auditor` niente da cercare:

- Gergo di marketing/business ("lean into", "deep dive", "circle back", "game-changer",
  "paradigm shift") — non compare in prosa accademica su un caso B2B software, e se
  comparisse sarebbe già un problema di registro più grave di questo, da segnalare
  come tale.
- Preset di voce personale (`unslop --preset crisp/warm/expert/story`,
  `no-ai-slop` "Preserve the writer's real voice") — questa tesi non ha una voce
  personale da preservare: `CLAUDE.md` vieta esplicitamente la prima persona, quindi
  non esiste una "voce dell'autore" nel senso in cui queste librerie lo intendono.
- Regole di formattazione per pubblicazione web (emoji nei titoli, grassetto sparso a
  metà frase) — il template Word ammette solo `Heading 1/2/3` e `Normal`, quindi questi
  pattern sono già impossibili per costruzione, non serve un lint per escluderli.
- "Put the reader in the room", "You beats People" (`stop-slop` regola 5) — una tesi
  non si rivolge al lettore in seconda persona.
