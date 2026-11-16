---
name: tesi-slop
description: Non è un comando da invocare. È la libreria di pattern anti-slop che il prose-auditor legge come riferimento quando gira, una volta sola, sul documento intero. Non fa parte di /tesi-audit.
---

# tesi-slop — libreria di pattern, non una skill eseguibile

Questa directory non risponde a `/tesi-slop`. Non c'è un comando da lanciare, non
produce un report da sola, non gira in nessun punto della pipeline elencato al §10 del
prompt orchestratore tranne uno: è il materiale che il `prose-auditor` (§4.4) legge come
libreria di pattern quando esegue il proprio stadio finale, unica volta, sul documento
intero, insieme a `/tesi-audit --whole`.

Se un agente o una skill sta cercando "come riconoscere un pattern da testo generato",
il file da leggere è `references/pattern-anti-slop.md`.

## Perché esiste come estrazione e non come skill installata

Le tre skill sorgente — `unslop`, `no-ai-slop`, `stop-slop`, installate globalmente in
`~/.claude/skills/` — restano **fuori dal runtime** di questa pipeline (§9 del prompt
orchestratore). Sono scritte per prosa discorsiva in inglese o italiano generico
(marketing, blog, saggistica), non per una tesi accademica: **vietano in blocco cose
che in una tesi sono corrette**, in particolare l'hedging epistemico che protegge da un
over-claim — la stessa cosa che il resto di questa pipeline (regola della cucitura,
`claim-auditor`, la regola sovrana) esiste per proteggere. Installarle come stadio
avrebbe fatto vincere alla libreria sbagliata un conflitto che la pipeline aveva già
deciso nell'altro senso.

`references/pattern-anti-slop.md` è quindi un'estrazione **curata**, non una copia: ogni
regola delle tre skill sorgente è stata classificata come attiva, riformulata, o
disattivata **con il motivo scritto accanto**. Il `prose-auditor` non installa né invoca
`unslop`/`no-ai-slop`/`stop-slop`: legge solo questo file.

## Il filtro accademico, in breve (dettaglio nel file)

- **Avverbi**: non si vieta la classe. Si vieta solo l'avverbio di rinforzo che
  sostituisce un argomento (`clearly`, `obviously`, `undoubtedly`, `certainly`,
  `undeniably` senza supporto nella frase). Si protegge sempre l'avverbio che
  **limita** un claim (`largely`, `partly`, `typically`, `primarily`, `arguably`,
  `plausibly`, `potentially`): è hedging, e l'hedging non si tocca mai.
- **Passivo**: non si vieta la classe. La convenzione di tempi e persona di
  `CLAUDE.md`/`AG-04` vieta la prima persona ovunque: un divieto assoluto di passivo,
  applicato alla lettera, costringerebbe a inventare soggetti agentivi artificiali
  (esattamente la "falsa agentività" che le stesse librerie vietano altrove) o a violare
  il divieto di prima persona. Restano segnalati solo il passivo **evitabile** (un
  attore già nominabile nella frase che il passivo nasconde senza motivo) e il passivo
  che nasconde chi ha fatto un'affermazione quando l'attribuzione conta (fonte vs.
  autore della tesi).
- **`which`**: la regola sorgente più vicina è "non iniziare una frase con un
  pronome interrogativo/relativo (What, When, Where, Which, Who, Why, How)" — una
  regola di ritmo per prosa discorsiva. In una tesi, una proposizione relativa
  introdotta da `which` (specie non restrittiva, con virgola) è normale sintassi
  accademica e spesso l'unico modo di aggiungere una precisazione senza spezzare la
  frase in due o forzare un soggetto ripetuto. Resta attivo solo il caso stretto:
  frasi che **iniziano** con `Which` come domanda retorica — quello sì è un tell da
  testo generato, e non serve mai in una tesi che non pone domande retoriche al
  lettore.

## Divieti per questa directory

- Non installare `unslop`, `no-ai-slop` o `stop-slop` come skill del progetto: restano
  dove sono, in `~/.claude/skills/`, mai referenziate da `.claude/skills/` di questa
  cartella oltre a questa nota.
- Non far girare questa libreria come stadio a sé: la usa solo il `prose-auditor`,
  quando gira lui.
- Non applicare mai una regola di questo file contro l'hedging: se un pattern qui
  sembra colpire una frase che protegge da un over-claim, quella frase vince, non la
  regola.
