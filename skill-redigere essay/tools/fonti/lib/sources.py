"""Client per le API bibliografiche gratuite: Crossref, OpenAlex,
Semantic Scholar, arXiv, Unpaywall.

Ogni funzione search_* restituisce una lista di "candidati" normalizzati:
    {
        "source_api": "crossref" | "openalex" | "semanticscholar" | "arxiv",
        "title": str | None,
        "authors": [str, ...],       # nomi completi cosi' come dati dall'API
        "year": int | None,
        "venue": str | None,
        "doi": str | None,           # senza prefisso https://doi.org/
        "url": str | None,           # landing page
        "abstract": str | None,
        "type": str | None,
        "citation_count": int | None,
        "is_oa": bool | None,
        "oa_pdf_url": str | None,
    }

Ogni valore proviene testualmente dal corpo della risposta API (nessun
valore inventato o "corretto" a mano). L'unica normalizzazione applicata e'
tecnica: strip del prefisso https://doi.org/ dal DOI e lowercase del DOI
stesso (il DOI e' case-insensitive per specifica).
"""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET

from .httpclient import PoliteSession

log = logging.getLogger("loop1.sources")

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_tags(text: str | None) -> str | None:
    """Crossref restituisce l'abstract con markup JATS (<jats:p>...</jats:p>).
    Qui si toglie solo il markup per l'uso interno nel confronto testuale;
    il campo salvato in Excel (titolo/sede/doi/...) non viene mai toccato,
    quindi questo non e' una "correzione" di un valore bibliografico, solo
    pulizia di uno strato di formattazione per il calcolo di similarita'.
    """
    if not text:
        return text
    return _TAG_RE.sub(" ", text).strip() or None


def _clean_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    d = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.lower().startswith(prefix):
            d = d[len(prefix):]
    return d.lower() or None


# ---------------------------------------------------------------------------
# Crossref
# ---------------------------------------------------------------------------

def search_crossref(session: PoliteSession, query: str, rows: int = 5) -> list[dict]:
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "mailto": session.contact_email,
    }
    resp = session.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    out = []
    for item in data.get("message", {}).get("items", []):
        title_list = item.get("title") or []
        title = title_list[0] if title_list else None
        authors = []
        for a in item.get("author", []) or []:
            given = a.get("given", "")
            family = a.get("family", "")
            full = f"{given} {family}".strip() or a.get("name")
            if full:
                authors.append(full)
        year = None
        for date_field in ("published-print", "published-online", "published", "issued"):
            dp = item.get(date_field)
            if dp and dp.get("date-parts") and dp["date-parts"][0]:
                y = dp["date-parts"][0][0]
                if y:
                    year = int(y)
                    break
        venue = None
        cont = item.get("container-title") or []
        if cont:
            venue = cont[0]
        out.append({
            "source_api": "crossref",
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "doi": _clean_doi(item.get("DOI")),
            "url": item.get("URL"),
            "abstract": _strip_tags(item.get("abstract")),
            "type": item.get("type"),
            "citation_count": item.get("is-referenced-by-count"),
            "is_oa": None,
            "oa_pdf_url": None,
        })
    return out


# ---------------------------------------------------------------------------
# OpenAlex
# ---------------------------------------------------------------------------

def _reconstruct_openalex_abstract(inv_index: dict | None) -> str | None:
    if not inv_index:
        return None
    positions: dict[int, str] = {}
    max_pos = -1
    for word, idxs in inv_index.items():
        for i in idxs:
            positions[i] = word
            max_pos = max(max_pos, i)
    if max_pos < 0:
        return None
    return " ".join(positions.get(i, "") for i in range(max_pos + 1)).strip() or None


def search_openalex(session: PoliteSession, query: str, per_page: int = 5) -> list[dict]:
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": per_page,
        "mailto": session.contact_email,
    }
    resp = session.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    out = []
    for item in data.get("results", []):
        authors = []
        for a in item.get("authorships", []) or []:
            name = (a.get("author") or {}).get("display_name")
            if name:
                authors.append(name)
        best_oa = item.get("best_oa_location") or {}
        primary_loc = item.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        oa_pdf = best_oa.get("pdf_url") or primary_loc.get("pdf_url")
        out.append({
            "source_api": "openalex",
            "title": item.get("display_name") or item.get("title"),
            "authors": authors,
            "year": item.get("publication_year"),
            "venue": source.get("display_name"),
            "doi": _clean_doi(item.get("doi")),
            "url": item.get("id"),
            "abstract": _reconstruct_openalex_abstract(item.get("abstract_inverted_index")),
            "type": item.get("type"),
            "citation_count": item.get("cited_by_count"),
            "is_oa": (item.get("open_access") or {}).get("is_oa"),
            "oa_pdf_url": oa_pdf,
        })
    return out


# ---------------------------------------------------------------------------
# Semantic Scholar Graph API
# ---------------------------------------------------------------------------

def search_semanticscholar(session: PoliteSession, query: str, limit: int = 5) -> list[dict]:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors,venue,externalIds,abstract,citationCount,"
                   "openAccessPdf,publicationTypes",
    }
    resp = session.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    out = []
    for item in data.get("data", []) or []:
        ext = item.get("externalIds") or {}
        oa_pdf = item.get("openAccessPdf") or {}
        pub_types = item.get("publicationTypes") or []
        out.append({
            "source_api": "semanticscholar",
            "title": item.get("title"),
            "authors": [a.get("name") for a in (item.get("authors") or []) if a.get("name")],
            "year": item.get("year"),
            "venue": item.get("venue"),
            "doi": _clean_doi(ext.get("DOI")),
            "url": f"https://www.semanticscholar.org/paper/{item.get('paperId')}" if item.get("paperId") else None,
            "abstract": item.get("abstract"),
            "type": ", ".join(pub_types) if pub_types else None,
            "citation_count": item.get("citationCount"),
            "is_oa": bool(oa_pdf.get("url")) if oa_pdf else None,
            "oa_pdf_url": oa_pdf.get("url"),
        })
    return out


# ---------------------------------------------------------------------------
# arXiv
# ---------------------------------------------------------------------------

_ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(session: PoliteSession, query: str, max_results: int = 5) -> list[dict]:
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    resp = session.get(url, params=params)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    out = []
    for entry in root.findall("atom:entry", _ARXIV_NS):
        title_el = entry.find("atom:title", _ARXIV_NS)
        title = title_el.text.strip().replace("\n", " ") if title_el is not None and title_el.text else None
        summary_el = entry.find("atom:summary", _ARXIV_NS)
        abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None and summary_el.text else None
        published_el = entry.find("atom:published", _ARXIV_NS)
        year = None
        if published_el is not None and published_el.text:
            try:
                year = int(published_el.text[:4])
            except ValueError:
                year = None
        authors = []
        for a in entry.findall("atom:author", _ARXIV_NS):
            name_el = a.find("atom:name", _ARXIV_NS)
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())
        id_el = entry.find("atom:id", _ARXIV_NS)
        arxiv_url = id_el.text.strip() if id_el is not None and id_el.text else None
        pdf_url = None
        for link in entry.findall("atom:link", _ARXIV_NS):
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                pdf_url = link.get("href")
        out.append({
            "source_api": "arxiv",
            "title": title,
            "authors": authors,
            "year": year,
            "venue": "arXiv preprint",
            "doi": _clean_doi(entry.findtext("{http://arxiv.org/schemas/atom}doi")),
            "url": arxiv_url,
            "abstract": abstract,
            "type": "preprint",
            "citation_count": None,
            "is_oa": True,
            "oa_pdf_url": pdf_url,
        })
    return out


# ---------------------------------------------------------------------------
# Unpaywall (accesso aperto per DOI)
# ---------------------------------------------------------------------------

def get_unpaywall(session: PoliteSession, doi: str) -> dict | None:
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": session.contact_email}
    resp = session.get(url, params=params)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    data = resp.json()
    best = data.get("best_oa_location") or {}
    return {
        "is_oa": data.get("is_oa"),
        "pdf_url": best.get("url_for_pdf") or best.get("url"),
        "landing_url": best.get("url"),
        "host_type": best.get("host_type"),
    }
