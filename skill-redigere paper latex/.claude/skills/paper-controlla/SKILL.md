---
name: paper-controlla
description: Fase 4 - controlli - verifica.py su tutto, paper-claim-auditor (sonnet) per sezione, correzioni o escalation al gruppo, poi un prose-auditor sul documento intero. Usala dopo /paper-scrivi.
---

# /paper-controlla

1. `python3 "<radice>/tools/verifica.py" --tutte`. Ogni HIGH torna al `paper-writer`.
2. `paper-claim-auditor` (subagent, `model: "sonnet"` esplicito) a gruppi di 3–4 sezioni
   contigue; se `doppio_auditor` e' true, due istanze indipendenti e arbitri tu i discordi.
3. Destino di ogni finding: sostituzione locale → subagent con le istruzioni di
   `../skill-redigere essay/.claude/agents/fix-applier.md`; riscrittura → `paper-writer`;
   merito (tagli, fonti, numeri non tracciabili, letteratura non attribuita) →
   `reports/escalation.md`, al gruppo, con contesto completo (RULES.md).
4. Un **prose-auditor** sul documento intero (istruzioni:
   `../skill-redigere essay/.claude/agents/prose-auditor.md`, pattern:
   `../skill-redigere essay/.claude/skills/essay-slop/references/pattern-anti-slop.md`): i tic
   di un testo scritto a pezzi si vedono solo di fila.
5. Rilancia `verifica.py --tutte` dopo ogni giro di correzioni.

Prossima fase: `/paper-latex`.
