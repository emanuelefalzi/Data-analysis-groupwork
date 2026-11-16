#!/usr/bin/env python3
"""verifica_tutto.py — i quattro lint su tutti i nodi, stampando solo cio' che fallisce.

Serve a non far leggere all'orchestratore ottanta rapporti per sapere se la
tesi e' a posto. Un giro, una schermata, e il dettaglio sta nei LEDGER.
"""
import glob, os, re, subprocess, sys

B = "/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
sys.path.insert(0, B + "tools")
sys.path.insert(0, B + "FONTI/pipeline/glossario")
from lint_citazioni import draft_of
import lint as glint

def ordine(n):
    try: return (0, [int(x) for x in n.split(".")], "")
    except ValueError: return (1, [], n)

nodi = sorted((os.path.basename(p)[:-3] for p in glob.glob(B + "nodes/*.md")), key=ordine)
falliti, blocchi, dash, tok = {}, [], 0, []
scritti = 0

for nid in nodi:
    t = draft_of(f"{B}nodes/{nid}.md")
    if not t.strip():
        continue
    scritti += 1
    for tool in ("lint_budget", "lint_numeri", "lint_citazioni"):
        r = subprocess.run(["/usr/bin/python3", f"{B}tools/{tool}.py", nid],
                           capture_output=True, text=True)
        if r.returncode != 0:
            falliti.setdefault(tool, []).append(nid)
    if any("BLOCCA" in str(v) for v in glint.lint(t, nid)):
        blocchi.append(nid)
    dash += len(re.findall(r"[—–]", t))
    if re.search(r"\[\[", t):
        tok.append(nid)

print(f"nodi con testo: {scritti}")
for tool in ("lint_budget", "lint_numeri", "lint_citazioni"):
    v = falliti.get(tool, [])
    print(f"  {tool:16s} {len(v):3d} falliti" + (f"  {' '.join(v)}" if v and len(v) <= 15 else ""))
print(f"  glossario        {len(blocchi):3d} blocchi" + (f"  {' '.join(blocchi)}" if blocchi else ""))
print(f"  trattini lunghi  {dash:3d}")
print(f"  token [[...]]    {len(tok):3d}" + (f"  {' '.join(tok)}" if tok else ""))
