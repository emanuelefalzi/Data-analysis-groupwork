# Appendix A — contratto (scheletro)

> **Stato: SCHELETRO, nessun contenuto ancora.** Il contenuto di ogni A.x si scrive con
> `/paper-appendice`: Claude lo ricava da `2. dataset/construction.pdf` e da
> `1. python/dataset.py`, nello stesso formato della scaletta (Role / Content / Guardrails),
> e il gruppo lo approva prima che si scriva la prosa. Fuori dal conteggio delle 20 pagine.
>
> Punti noti su cui `construction.pdf` è **superato** (RULES.md, *Known inconsistencies*):
> outcome principale = `exit_5y` (non `exit`); lo script si chiama `dataset.py`; il file ha tre
> nomi (`dataset.dta`, `output/rq1_two_group_dataset_v2.dta`, `group_21_dataset.dta`);
> «estimation sample» = 9,263 (`full_window == 1`), non 28,478; nessun `Accelerator_pre_r1`.

## A Dataset construction

**Role:** let a reader rebuild `dataset.dta` (28,478 startups × 57 variables) from the raw PitchBook files.
**Words:** 0

### A.1 Raw files and how they are linked

**Role:** what each raw file contains and the keys that join them.
**Words:** 0

#### Content

#### Guardrails
- Sample counts already given in 3.1 are not repeated here: pointer only.

### A.2 From deals to rounds

**Role:** which deals count as VC rounds, how same-day deals are merged, how the lead investor is found.
**Words:** 0

#### Content

#### Guardrails

### A.3 Variables built

**Role:** how each variable of the models is computed, with its name in the dataset.
**Words:** 0

#### Content

#### Guardrails
- Definitions already in 3.2 are not rewritten: here only the construction steps.
