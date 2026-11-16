"""Client HTTP condiviso: polite pool, rate limiting per host, backoff
esponenziale su 429/5xx, timeout su tutte le richieste.
"""
from __future__ import annotations

import logging
import random
import time
from urllib.parse import urlparse

import requests

log = logging.getLogger("loop1.http")

DEFAULT_TIMEOUT = 20  # secondi, applicato a ogni richiesta HTTP
MAX_RETRIES = 5
BACKOFF_BASE = 1.5  # secondi
BACKOFF_CAP = 60.0  # secondi
MIN_INTERVAL_PER_HOST = 1.0  # secondi fra due richieste allo stesso host


class PoliteSession:
    """Wrapper su requests.Session che rispetta un intervallo minimo per
    host e fa backoff esponenziale sui codici 429/500/502/503/504.
    """

    def __init__(self, contact_email: str, user_agent_app: str = "essay-recupero",
                 min_interval: float = MIN_INTERVAL_PER_HOST,
                 max_retries: int = MAX_RETRIES,
                 timeout: int = DEFAULT_TIMEOUT):
        self.session = requests.Session()
        self.contact_email = contact_email
        self.user_agent = f"{user_agent_app}/1.0 (mailto:{contact_email})"
        self.session.headers.update({"User-Agent": self.user_agent})
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.timeout = timeout
        self._last_request_at: dict[str, float] = {}

    def _throttle(self, host: str) -> None:
        last = self._last_request_at.get(host)
        if last is not None:
            elapsed = time.monotonic() - last
            wait = self.min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
        self._last_request_at[host] = time.monotonic()

    def get(self, url: str, params: dict | None = None,
            headers: dict | None = None) -> requests.Response:
        host = urlparse(url).netloc
        attempt = 0
        while True:
            self._throttle(host)
            try:
                resp = self.session.get(url, params=params, headers=headers,
                                         timeout=self.timeout)
            except requests.RequestException as exc:
                attempt += 1
                if attempt > self.max_retries:
                    raise
                sleep_for = min(BACKOFF_CAP, BACKOFF_BASE ** attempt) + random.uniform(0, 0.5)
                log.warning("errore di rete su %s (tentativo %d/%d): %s - riprovo fra %.1fs",
                            url, attempt, self.max_retries, exc, sleep_for)
                time.sleep(sleep_for)
                continue

            if resp.status_code == 200:
                return resp
            if resp.status_code in (429, 500, 502, 503, 504):
                attempt += 1
                if attempt > self.max_retries:
                    resp.raise_for_status()
                retry_after = resp.headers.get("Retry-After")
                if retry_after is not None:
                    try:
                        sleep_for = float(retry_after)
                    except ValueError:
                        sleep_for = min(BACKOFF_CAP, BACKOFF_BASE ** attempt)
                else:
                    sleep_for = min(BACKOFF_CAP, BACKOFF_BASE ** attempt) + random.uniform(0, 0.5)
                log.warning("HTTP %d su %s (tentativo %d/%d) - riprovo fra %.1fs",
                            resp.status_code, url, attempt, self.max_retries, sleep_for)
                time.sleep(sleep_for)
                continue
            # altri codici (404, 400, ...): non ha senso ritentare
            return resp
