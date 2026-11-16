"""Cache su file dei risultati API, un file JSON per fonte.

Permette di riavviare il processo senza rifare le chiamate alle API gia'
interrogate con successo per una data fonte: se il processo muore a meta'
lavoro, il run successivo trova la cache e salta direttamente alla fase di
punteggio/decisione per le fonti gia' interrogate.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger("loop1.cache")


class SourceCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, fonte_id: str) -> Path:
        safe_id = "".join(c for c in fonte_id if c.isalnum() or c in "-_")
        return self.cache_dir / f"{safe_id}.json"

    def load(self, fonte_id: str) -> dict:
        p = self._path(fonte_id)
        if not p.exists():
            return {"api_results": {}}
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("cache corrotta per %s (%s), la ignoro", fonte_id, exc)
            return {"api_results": {}}

    def save(self, fonte_id: str, data: dict) -> None:
        p = self._path(fonte_id)
        tmp = p.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(p)  # scrittura atomica

    def has_api_result(self, fonte_id: str, api_name: str) -> bool:
        data = self.load(fonte_id)
        return api_name in data.get("api_results", {})

    def get_api_result(self, fonte_id: str, api_name: str):
        data = self.load(fonte_id)
        return data.get("api_results", {}).get(api_name)

    def set_api_result(self, fonte_id: str, api_name: str, query: str,
                        candidates: list[dict], error: str | None = None) -> None:
        data = self.load(fonte_id)
        data.setdefault("api_results", {})[api_name] = {
            "query": query,
            "candidates": candidates,
            "error": error,
        }
        self.save(fonte_id, data)
