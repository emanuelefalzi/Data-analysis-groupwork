"""Utilita' testuali: normalizzazione nomi, tokenizzazione, similarita' testuale.

Nessuna dipendenza pesante obbligatoria. Se scikit-learn e' installato viene
usato TfidfVectorizer + cosine_similarity (piu' preciso); altrimenti si
ricade su un TF-IDF scritto a mano con la sola stdlib (collections, math).
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

try:
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
    _HAS_SKLEARN = True
except Exception:  # pragma: no cover - dipende dall'ambiente
    _HAS_SKLEARN = False

# Stopword inglesi (il corpus di contesto/claim e' in inglese). Lista corta
# ma sufficiente per togliere il rumore piu' comune senza dipendenze esterne.
STOPWORDS = frozenset("""
a about above after again against all am an and any are aren't as at be
because been before being below between both but by can't cannot could
couldn't did didn't do does doesn't doing don't down during each few for
from further had hadn't has hasn't have haven't having he he'd he'll he's
her here here's hers herself him himself his how how's i i'd i'll i'm i've
if in into is isn't it it's its itself let's me more most mustn't my myself
no nor not of off on once only or other ought our ours ourselves out over
own same shan't she she'd she'll she's should shouldn't so some such than
that that's the their theirs them themselves then there there's these they
they'd they'll they're they've this those through to too under until up
very was wasn't we we'd we'll we're we've were weren't what what's when
when's where where's which while who who's whom why why's with won't would
wouldn't you you'd you'll you're you've your yours yourself yourselves
also within upon among across without between per via one two three thus
however moreover therefore et al 2018 2019 2020 2021 2022 2023 2024 2025
""".split())

_PARTICLES = {"van", "von", "de", "der", "den", "del", "di", "la", "le",
              "da", "dos", "das", "bin", "al", "st", "mac", "mc"}

_WORD_RE = re.compile(r"[a-z0-9]+")


def strip_accents(s: str) -> str:
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_name(s: str) -> str:
    """minuscolo, senza accenti, senza punteggiatura, spazi collassati."""
    if not s:
        return ""
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def first_author_surname(autori_raw: str) -> str:
    """Estrae il cognome del primo autore da una citazione tipo
    'Agrawal, Gans & Goldfarb' -> 'Agrawal', 'Baldwin & Clark' -> 'Baldwin',
    'Smith et al.' -> 'Smith'.
    """
    if not autori_raw:
        return ""
    s = autori_raw.strip()
    s = re.sub(r"\bet\s*al\.?\b", "", s, flags=re.I)
    parts = re.split(r",|&|\band\b", s, flags=re.I)
    first = parts[0].strip() if parts else s
    return normalize_name(first)


def extract_surname_from_full_name(full_name: str) -> str:
    """Euristica per estrarre il cognome da un nome completo 'Ajay Agrawal'
    -> 'agrawal'; gestisce particelle comuni ('van', 'de', ...).
    """
    if not full_name:
        return ""
    tokens = normalize_name(full_name).split()
    if not tokens:
        return ""
    if len(tokens) == 1:
        return tokens[0]
    # cerca una particella prima dell'ultimo blocco
    for i in range(len(tokens) - 1):
        if tokens[i] in _PARTICLES:
            return " ".join(tokens[i:])
    return tokens[-1]


def author_surname_matches(source_surname_norm: str, candidate_first_author: str) -> bool:
    """Confronto RIGIDO (normalizzato) fra cognome atteso e cognome del
    primo autore del candidato. Nessun match parziale/fuzzy: se non
    combaciano esattamente dopo normalizzazione, il candidato va scartato.
    """
    if not source_surname_norm or not candidate_first_author:
        return False
    cand_surname = extract_surname_from_full_name(candidate_first_author)
    return cand_surname == source_surname_norm


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    text = strip_accents(text).lower()
    tokens = _WORD_RE.findall(text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def _manual_tfidf_cosine(query: str, candidates: list[str]) -> list[float]:
    """TF-IDF + coseno scritto a mano (fallback senza scikit-learn)."""
    docs_tokens = [tokenize(query)] + [tokenize(c) for c in candidates]
    n_docs = len(docs_tokens)
    df: Counter = Counter()
    for toks in docs_tokens:
        for term in set(toks):
            df[term] += 1

    def vectorize(toks: list[str]) -> dict[str, float]:
        tf = Counter(toks)
        vec = {}
        for term, count in tf.items():
            idf = math.log((1 + n_docs) / (1 + df[term])) + 1.0
            vec[term] = count * idf
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {k: v / norm for k, v in vec.items()}

    query_vec = vectorize(docs_tokens[0])
    scores = []
    for toks in docs_tokens[1:]:
        cand_vec = vectorize(toks)
        # dot product sul vocabolario condiviso
        common = set(query_vec) & set(cand_vec)
        dot = sum(query_vec[t] * cand_vec[t] for t in common)
        scores.append(max(0.0, min(1.0, dot)))
    return scores


def _sklearn_tfidf_cosine(query: str, candidates: list[str]) -> list[float]:
    docs = [query] + candidates
    # tokenizer custom cosi' applichiamo le stesse stopword/normalizzazione
    vectorizer = TfidfVectorizer(tokenizer=tokenize, lowercase=False,
                                  preprocessor=lambda x: x, token_pattern=None)
    try:
        matrix = vectorizer.fit_transform(docs)
    except ValueError:
        # vocabolario vuoto (testi troppo corti / solo stopword)
        return [0.0] * len(candidates)
    sims = cosine_similarity(matrix[0:1], matrix[1:])[0]
    return [float(max(0.0, min(1.0, s))) for s in sims]


def text_similarity(query: str, candidates: list[str]) -> list[float]:
    """Similarita' testuale query vs ciascun candidato, in [0, 1].
    Usa scikit-learn se disponibile, altrimenti un TF-IDF stdlib equivalente.
    """
    if not candidates:
        return []
    if not query or not query.strip():
        return [0.0] * len(candidates)
    if _HAS_SKLEARN:
        try:
            return _sklearn_tfidf_cosine(query, candidates)
        except Exception:
            pass  # fallback silenzioso al metodo manuale
    return _manual_tfidf_cosine(query, candidates)


def normalize_title(title: str) -> str:
    if not title:
        return ""
    t = strip_accents(title).lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
