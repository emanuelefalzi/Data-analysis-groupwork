"""Punteggio deterministico dei candidati e decisione (accettato / ambigua /
non_trovata). Nessun LLM: solo confronto testuale + regole.

--- Costanti di soglia (documentate qui, uniche nel codice) -----------------

FILTRO AUTORE: rigido, non e' un punteggio. Il cognome del primo autore del
candidato deve combaciare esattamente (dopo normalizzazione: minuscolo,
senza accenti, senza punteggiatura) con il cognome del primo autore atteso.
Nessun candidato che fallisce questo filtro entra nel punteggio.

FILTRO ANNO: coincidenza esatta = punteggio pieno; scarto di 1 anno (tipico
preprint pubblicato l'anno dopo, o viceversa) = punteggio ridotto ma il
candidato resta in gara; scarto >= 2 anni = candidato scartato del tutto,
troppo rischioso considerarlo lo stesso lavoro.

PESI del punteggio composito (sommano a 1.0):
  - W_SIM  = 0.65  similarita' testuale (titolo+abstract vs contesto d'uso
             + claim da verificare): e' il segnale piu' informativo perche'
             distingue fra piu' paper dello stesso autore/anno.
  - W_YEAR = 0.25  coincidenza dell'anno (pieno/penalizzato come sopra).
  - W_CITE = 0.10  conteggio citazioni, scalato logaritmicamente e saturato:
             indizio debole apposta, non deve mai da solo far vincere un
             candidato con similarita' bassa.

SOGLIE DI DECISIONE:
  - ACCEPT_MIN_SCORE = 0.32: punteggio minimo del primo candidato per poter
    essere accettato automaticamente. Valore calibrato empiricamente
    lanciando query reali su Crossref/OpenAlex/Semantic Scholar/arXiv per
    8 fonti vere della tesi: quando l'abstract manca (il caso piu' comune
    su Crossref) la similarita' testuale titolo-vs-contesto scende spesso
    sotto 0.10, e un candidato genuino con anno esatto e zero citazioni
    nella cache produce un punteggio "di base" di W_YEAR = 0.25 (nessun
    contributo da similarita' o citazioni). 0.32 sta appena sopra questo
    pavimento: un candidato viene accettato solo se porta *qualcosa* in
    piu' del solo anno giusto (un minimo di sovrapposizione testuale
    genuina, sim >= ~0.11, oppure una citation count consistente), ma non
    viene scartato solo perche' Crossref non fornisce l'abstract. Il
    filtro autore+anno a monte gia' elimina la maggior parte dei falsi
    positivi, quindi questa soglia serve a scartare i casi in cui il
    cognome combacia per puro caso (autori omonimi) senza nessun altro
    segnale a supporto.
  - ACCEPT_MARGIN_MIN = 0.12: distacco minimo fra il primo e il secondo
    candidato (dopo aver unito i duplicati inter-API) per considerare la
    scelta non ambigua. Se il distacco e' inferiore, due paper sono troppo
    simili per scegliere in automatico -> stato "ambigua".
  - SOURCE_AGREEMENT_BONUS = 0.05: se lo stesso lavoro (stesso DOI o titolo
    quasi identico) e' stato trovato da piu' di un'API, e' un segnale di
    affidabilita' aggiuntivo; bonus piccolo e cappato per non distorcere il
    punteggio principale.
  - CITATION_SATURATION = 500: citazioni oltre questa soglia contano come
    "tante" (punteggio 1.0 sulla componente citazioni); valore arbitrario
    ma ragionevole per paper accademici citati nella tesi.

Con un solo candidato sopravvissuto al filtro rigido: se il suo punteggio
e' >= ACCEPT_MIN_SCORE viene accettato; altrimenti va in "ambigua" (non
"non_trovata", perche' un candidato c'e' - semplicemente non abbastanza
sicuro da accettare senza controllo umano). "non_trovata" e' riservato al
caso di zero candidati superstiti dopo il filtro autore.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import textutil

W_SIM = 0.65
W_YEAR = 0.25
W_CITE = 0.10

YEAR_EXACT_SCORE = 1.0
YEAR_OFF_BY_ONE_SCORE = 0.55
YEAR_MISSING_SCORE = 0.30
YEAR_DISCARD_DIFF = 2  # >= questa differenza (in anni) -> candidato scartato

ACCEPT_MIN_SCORE = 0.32
ACCEPT_MARGIN_MIN = 0.12
SOURCE_AGREEMENT_BONUS = 0.05
CITATION_SATURATION = 500

TITLE_DEDUP_SIMILARITY = 0.90  # soglia difflib per considerare due titoli "lo stesso lavoro"


@dataclass
class ScoredCandidate:
    candidate: dict
    year_score: float
    sim_score: float
    cite_score: float
    composite: float
    source_apis: list = field(default_factory=list)


def _year_score(source_year: int | None, cand_year) -> float | None:
    """None = candidato da scartare (differenza troppo grande)."""
    if not cand_year:
        return YEAR_MISSING_SCORE
    try:
        cand_year = int(cand_year)
    except (TypeError, ValueError):
        return YEAR_MISSING_SCORE
    if source_year is None:
        return YEAR_MISSING_SCORE
    diff = abs(source_year - cand_year)
    if diff == 0:
        return YEAR_EXACT_SCORE
    if diff == 1:
        return YEAR_OFF_BY_ONE_SCORE
    return None  # scarto


def _citation_score(count) -> float:
    if not count or count <= 0:
        return 0.0
    return max(0.0, min(1.0, math.log1p(count) / math.log1p(CITATION_SATURATION)))


def _dedup_merge(candidates: list[dict]) -> list[dict]:
    """Unisce candidati che rappresentano molto probabilmente lo stesso
    lavoro (stesso DOI, o titolo quasi identico + stesso anno) trovati da
    piu' API diverse. Il merge preferisce, per ciascun campo, il primo
    valore non nullo incontrato (ordine di scoperta = ordine di query delle
    API); tiene traccia di tutte le source_api che hanno contribuito.
    """
    merged: list[dict] = []
    for cand in candidates:
        target = None
        cand_doi = cand.get("doi")
        cand_title_norm = textutil.normalize_title(cand.get("title") or "")
        for m in merged:
            if cand_doi and m.get("doi") and cand_doi == m["doi"]:
                target = m
                break
            m_title_norm = textutil.normalize_title(m.get("title") or "")
            if cand_title_norm and m_title_norm:
                import difflib
                ratio = difflib.SequenceMatcher(None, cand_title_norm, m_title_norm).ratio()
                same_year = (cand.get("year") and m.get("year") and cand["year"] == m["year"])
                if ratio >= TITLE_DEDUP_SIMILARITY and (same_year or not cand.get("year") or not m.get("year")):
                    target = m
                    break
        if target is None:
            merged_entry = dict(cand)
            merged_entry["_source_apis"] = [cand["source_api"]]
            merged.append(merged_entry)
        else:
            for k, v in cand.items():
                if k == "source_api":
                    continue
                if not target.get(k) and v:
                    target[k] = v
            target["_source_apis"].append(cand["source_api"])
    return merged


def score_candidates(source_surname_norm: str, source_year: int | None,
                      query_text: str, raw_candidates: list[dict]) -> list[ScoredCandidate]:
    """Applica filtro autore (rigido) + filtro anno, poi calcola il
    punteggio composito. Restituisce solo i candidati sopravvissuti,
    ordinati per punteggio decrescente.
    """
    # 1. filtro autore, rigido
    author_ok = [
        c for c in raw_candidates
        if c.get("authors") and textutil.author_surname_matches(source_surname_norm, c["authors"][0])
    ]

    # 2. dedup fra API (solo sui candidati che hanno gia' passato il filtro autore)
    deduped = _dedup_merge(author_ok)

    # 3. filtro anno + punteggio
    survivors = []
    year_scores = []
    for c in deduped:
        ys = _year_score(source_year, c.get("year"))
        if ys is None:
            continue
        survivors.append(c)
        year_scores.append(ys)

    if not survivors:
        return []

    titles_and_abstracts = [
        f"{c.get('title') or ''} {c.get('abstract') or ''}".strip() for c in survivors
    ]
    sim_scores = textutil.text_similarity(query_text, titles_and_abstracts)

    scored = []
    for c, ys, sim in zip(survivors, year_scores, sim_scores):
        cite = _citation_score(c.get("citation_count"))
        composite = W_SIM * sim + W_YEAR * ys + W_CITE * cite
        if len(c.get("_source_apis", [])) > 1:
            composite = min(1.0, composite + SOURCE_AGREEMENT_BONUS)
        scored.append(ScoredCandidate(
            candidate=c, year_score=ys, sim_score=sim, cite_score=cite,
            composite=composite, source_apis=c.get("_source_apis", [c.get("source_api")]),
        ))
    scored.sort(key=lambda s: s.composite, reverse=True)
    return scored


def decide(scored: list[ScoredCandidate]) -> tuple[str, ScoredCandidate | None, str]:
    """Ritorna (stato, candidato_scelto_o_None, motivazione).
    stato in {"trovata_da_confermare_download", "ambigua", "non_trovata"}.
    Nota: qui "trovata_da_confermare_download" e' un esito interno che dice
    solo "identita' risolta" - la fase 3 decidera' poi se diventa
    scaricata/paywall/trovata a seconda della disponibilita' del PDF.
    """
    if not scored:
        return "non_trovata", None, "nessun candidato ha superato il filtro (rigido) sul cognome del primo autore"

    if len(scored) == 1:
        top = scored[0]
        if top.composite >= ACCEPT_MIN_SCORE:
            return "identificata", top, (
                f"unico candidato dopo i filtri, punteggio {top.composite:.3f} >= "
                f"soglia {ACCEPT_MIN_SCORE}")
        return "ambigua", None, (
            f"unico candidato ma punteggio {top.composite:.3f} sotto la soglia "
            f"{ACCEPT_MIN_SCORE}: non abbastanza sicuro per accettare in automatico")

    top, second = scored[0], scored[1]
    margin = top.composite - second.composite
    if top.composite >= ACCEPT_MIN_SCORE and margin >= ACCEPT_MARGIN_MIN:
        return "identificata", top, (
            f"primo candidato punteggio {top.composite:.3f}, secondo {second.composite:.3f}, "
            f"margine {margin:.3f} >= soglia {ACCEPT_MARGIN_MIN}")
    return "ambigua", None, (
        f"primo candidato punteggio {top.composite:.3f}, secondo {second.composite:.3f}, "
        f"margine {margin:.3f} insufficiente (soglie: min={ACCEPT_MIN_SCORE}, "
        f"margine={ACCEPT_MARGIN_MIN})")
