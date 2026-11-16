#!/usr/bin/env python3
"""Fase 0: congela le pagine web in testo locale.

Un sito cambia: se il lettore A e NotebookLM leggono la pagina in due momenti
diversi, la divergenza non significa piu' nulla. Per questo ogni fonte viene
scaricata UNA volta, salvata in lavoro/testi/<id_fonte>.txt, e da li' in poi
tutti leggono e verificano contro quel file (la data di accesso finisce in
<id_fonte>.meta.json, serve anche per la citazione APA).

Solo libreria standard. Uso:
    python3 salva_pagine.py              # scarica le fonti che non hanno ancora un testo
    python3 salva_pagine.py --rifai      # riscarica tutto (cambia la data di accesso!)
    python3 salva_pagine.py --solo acme_chi_siamo

Se una pagina esce quasi vuota (sito fatto in JavaScript), lo script lo dice:
in quel caso il testo va preso col browser (get_page_text) e salvato a mano
nello stesso file, annotando in meta.json "estrazione": "browser".
"""
import argparse, csv, hashlib, json, os, re, sys, urllib.request
from datetime import date
from html.parser import HTMLParser

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
COPPIE = os.path.join(RADICE, "coppie.csv")
TESTI = os.path.join(RADICE, "lavoro", "testi")
MINIMO = 1500   # sotto questa soglia il testo e' sospetto (pagina JS, cookie wall)

SALTA = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "iframe"}
BLOCCHI = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr",
           "section", "article", "blockquote", "dd", "dt", "td", "th"}


class Testo(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parti, self.profondita = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SALTA:
            self.profondita += 1
        elif tag in BLOCCHI:
            self.parti.append("\n")

    def handle_endtag(self, tag):
        if tag in SALTA and self.profondita:
            self.profondita -= 1
        elif tag in BLOCCHI:
            self.parti.append("\n")

    def handle_data(self, data):
        if not self.profondita:
            self.parti.append(data)

    def testo(self):
        t = "".join(self.parti)
        t = re.sub(r"[ \t\xa0]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n\n", t)
        return t.strip()


def fonti():
    with open(COPPIE, encoding="utf-8-sig") as fh:
        visti = {}
        for r in csv.DictReader(fh):
            fid, url = (r.get("id_fonte") or "").strip(), (r.get("url") or "").strip()
            if fid and url:
                visti.setdefault(fid, url)
    return visti


def scarica(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Accept-Language": "it,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        grezzo = r.read()
        cs = r.headers.get_content_charset() or "utf-8"
    html = grezzo.decode(cs, errors="replace")
    p = Testo(); p.feed(html)
    return p.testo(), hashlib.sha256(grezzo).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rifai", action="store_true")
    ap.add_argument("--solo")
    a = ap.parse_args()
    os.makedirs(TESTI, exist_ok=True)

    for fid, url in fonti().items():
        if a.solo and fid != a.solo:
            continue
        out = os.path.join(TESTI, fid + ".txt")
        if os.path.exists(out) and not a.rifai:
            print(f"  gia' salvata   {fid}")
            continue
        try:
            testo, sha = scarica(url)
        except Exception as ex:
            print(f"  ERRORE         {fid}: {ex}  -> prendila col browser e salvala in {out}")
            continue
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(testo)
        meta = {"id_fonte": fid, "url": url, "data_accesso": date.today().isoformat(),
                "caratteri": len(testo), "sha256_html": sha, "estrazione": "salva_pagine.py"}
        with open(os.path.join(TESTI, fid + ".meta.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)
        avviso = "  <-- SOSPETTA: quasi vuota, rifalla col browser" if len(testo) < MINIMO else ""
        print(f"  salvata        {fid}: {len(testo):,} caratteri{avviso}")


if __name__ == "__main__":
    main()
