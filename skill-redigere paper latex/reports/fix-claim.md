# fix-claim (fix-applier)

## Applicati
- CLM-5.4-01 (5.4 ¶2): "H2 is rejected, opposite sign" -> "It does not support H2 either".
- CLM-5.2-01 (5.2 ¶2): AME at average hype now "-2.4 percentage points per unit of ln(1 + months) (p = 0.003)", N = 4,469 added (log L1488/L1451). Not verifiable in the material and left unchanged: the IQR sentence (-1.9 pp, mean failure 12.4%, about 15%); the group must confirm it or have it removed.
- CLM-5.2-02 (5.2 ¶3): "ranging from -2.1 to -2.8" -> AME -2.1 pp (p = 0.115) cold, -2.8 pp (p = 0.001) hot.

## Saltati (solo i tre richiesti applicati; gli altri non toccati)
Marked fix-applier but not requested, or needing material not in ctx / non-local rewrite: CLM-5.1-03, 5.2-05, 5-01, 2.3-01, 2.3-02, 2.4-02, 2.5-05, 2.5-06, 2.5-07, 2.2-02, 1-01, 1-02, 2.1-04, 2.1-05, 2.2-03, 5.4-03, 5.4-04, 5.5-03, 5.3-01.
Mixed gruppo/fix-applier: CLM-5.2-01 IQR part (above). Gruppo / paper-writer findings not touched.

## verifica.py
5.2 and 5.4: 0 HIGH (1 MEDIUM word-count each, pre-existing).

## Secondo giro (fix-applier)
Applicati: CLM-1-01 (1 ¶5 "the same logic ... than they are" -> "may look safer once refinanced"); CLM-1-02 ("raise" -> "go with higher prices"); CLM-2.1-04 (software and services); CLM-2.1-05 ("more likely to have"); CLM-2.2-02 ("may weaken"); CLM-2.3-01 ("abundant capital" moved out of the cited sentence); CLM-2.3-02 ("experimental" removed); CLM-2.4-02 ("In a study of MIT start-up offers"); CLM-2.5-05 ("after cuts in travel time, went with"); CLM-2.5-06 ("In software and services"); CLM-2.5-07 ("possible industry differences"); CLM-5.1-03 (partial: "estimation sample (full outcome window)"; N = 9,263 and 41 clusters not added, verifica.py flags them as numbers outside the section's material); CLM-5.3-01 (partial: exp(coefficient) - 1 identity added; no p-values in material); CLM-5.4-03 (N = 15,495 / 15,294, raw VC share as hype); CLM-5.4-04 ("association ... about 5% more negative"); CLM-5.5-03 ("may poorly proxy ... would bias").
Saltati: CLM-2.2-03 (finding says no action needed); CLM-5.2-05 (units of round-1 size and age not in the material); CLM-5-01 (sample of the 22.2/15.6/12.4/31.6 rates not in the material, "from 3.3").
verifica.py: 0 HIGH on 1, 2.1, 2.2, 2.3, 2.4, 2.5, 5.1, 5.3, 5.4, 5.5 (MEDIUM word counts pre-existing).
