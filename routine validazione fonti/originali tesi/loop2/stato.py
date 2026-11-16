#!/usr/bin/env python3
"""Loop 2 - avanzamento. Sola lettura, non tocca nulla."""
import os, collections, openpyxl
BASE="/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/"
ws=openpyxl.load_workbook(BASE+"iTOC master.xlsx", data_only=True)["Estratti"]
tot=ver=0; esiti=collections.Counter(); manca=[]; div=[]
for r in range(2,ws.max_row+1):
    if not ws.cell(r,1).value: continue
    tot+=1
    e=ws.cell(r,8).value; n=ws.cell(r,12).value
    if e: ver+=1; esiti[e]+=1
    else: manca.append((ws.cell(r,1).value, ws.cell(r,2).value, ws.cell(r,4).value))
    if e and n and e!=n: div.append((ws.cell(r,1).value, ws.cell(r,2).value, e, n))
print(f"Coppie totali: {tot} | verificate: {ver} ({ver*100//max(tot,1)}%)")
for k,v in esiti.most_common(): print(f"  {k:<20} {v}")
if div:
    print(f"\nDivergenze fra i due lettori: {len(div)}")
    for n,f,a,b in div: print(f"  {n:<8} {f:<22} A={a} | NLM={b}")
ms=[m for m in manca if m[2]=="mattone stretto"]
print(f"\nDa verificare: {len(manca)} (di cui mattoni stretti: {len(ms)})")
for d,lab in ((BASE+"FONTI/estrazioni/estratti/","estratti/"),(BASE+"FONTI/estrazioni/estratti_nlm/","estratti_nlm/"),(BASE+"FONTI/pipeline/loop2/task/","task/")):
    n=len([x for x in os.listdir(d) if x.endswith(".json")]) if os.path.isdir(d) else 0
    print(f"  {lab:<16} {n} file")
