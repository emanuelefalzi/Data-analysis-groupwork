"""Download del PDF ad accesso aperto, con verifica che sia davvero un PDF
(magic bytes %PDF) e non una pagina di errore HTML.
"""
from __future__ import annotations

import logging
from pathlib import Path

from .httpclient import PoliteSession

log = logging.getLogger("loop1.download")

MAX_PDF_BYTES = 100 * 1024 * 1024  # 100 MB, salvaguardia contro download anomali


def download_pdf(session: PoliteSession, url: str, dest_path: Path) -> tuple[bool, str]:
    """Scarica url in dest_path. Ritorna (successo, messaggio).
    Se il contenuto scaricato non inizia con %PDF, il file viene cancellato
    e si ritorna successo=False.
    """
    dest_path = Path(dest_path)
    try:
        resp = session.get(url)
    except Exception as exc:  # errori di rete gia' ritentati dentro PoliteSession
        return False, f"errore di rete durante il download: {exc}"

    if resp.status_code != 200:
        return False, f"HTTP {resp.status_code} durante il download"

    content = resp.content
    if len(content) > MAX_PDF_BYTES:
        return False, f"file troppo grande ({len(content)} byte), scarico interrotto per sicurezza"

    if not content[:5].startswith(b"%PDF"):
        return False, "il contenuto scaricato non e' un PDF valido (magic bytes assenti, probabile pagina di errore/HTML)"

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(content)

    # doppio controllo post-scrittura
    with open(dest_path, "rb") as f:
        head = f.read(5)
    if not head.startswith(b"%PDF"):
        dest_path.unlink(missing_ok=True)
        return False, "verifica post-scrittura fallita, file cancellato"

    return True, f"scaricato in {dest_path}"
