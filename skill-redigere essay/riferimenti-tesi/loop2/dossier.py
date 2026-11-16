import openpyxl, re, sys
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

P='/Users/emanuelefalzi/Desktop/scuola/bachelor/tesi 4 - scrittura/iTOC master.xlsx'
wb=openpyxl.load_workbook(P)          # formule preservate
wbv=openpyxl.load_workbook(P, data_only=True)

def rows(name, book):
    ws=book[name]
    rr=[list(r) for r in ws.iter_rows(values_only=True)]
    hdr=[str(h) for h in rr[0]]
    return [dict(zip(hdr,r)) for r in rr[1:]]

itoc=rows('iTOC', wb)
fonti=rows('Fonti', wbv)
estr=rows('Estratti', wbv)

FONTI={r['ID']:r for r in fonti if r['ID']}
CIT2ID={ (r['Citazione'] or '').strip('() '):i for i,r in FONTI.items() }

SEV={'usabile':0,'da riformulare':1,'non usabile':2}
ARB_VERDICT={'usabile':'usabile','da riformulare':'da riformulare',
             'riformulata':'da riformulare','non usabile':'non usabile'}
ARB_EXCL={'superata':'ESCLUSA (superata)','rimossa dal nodo':'ESCLUSA (rimossa dal nodo)'}

def effettivo(r, registrata_in_itoc=None):
    """Esito effettivo di una coppia. `registrata_in_itoc` dice se la colonna
    `Fonti + ruolo` del nodo elenca ancora quella fonte come voce di ruolo."""
    R=(str(r.get('Esito arbitrato') or '')).strip()
    H=(str(r.get('Esito') or '')).strip()
    L=(str(r.get('Esito NotebookLM') or '')).strip()

    # 1) R porta un verdetto esplicito: vince su tutto
    if R in ARB_VERDICT: return ARB_VERDICT[R], 'arbitrato (R)'
    # 2) R dice che la coppia e' uscita dal nodo
    if R in ARB_EXCL:    return ARB_EXCL[R], 'arbitrato (R)'
    # 3) DA DECIDERE: nessuno cita finche' l'autore non sceglie
    if R.upper()=='DA DECIDERE': return 'DA DECIDERE', 'arbitrato (R)'
    # 4) 'chiusa nel nodo': il problema e' stato risolto RISCRIVENDO il nodo.
    #    La fonte resta se e solo se l'iTOC la elenca ancora. Il vincolo d'uso
    #    e' in colonna S e va letto: non si cita a braccio.
    if R=='chiusa nel nodo':
        if registrata_in_itoc:
            return 'da riformulare (vincolo in S)', "R='chiusa nel nodo' + iTOC la registra"
        return 'ESCLUSA (chiusa nel nodo, fuori dall\'iTOC)', 'arbitrato (R)'
    # 5) 'nessun arbitrato': la divergenza NON e' un conflitto fra lettori.
    #    Il 'non usabile' di NotebookLM e' l'artefatto noto della citazione
    #    congiunta. Vale il lettore locale; il claim va scomposto in stesura.
    if R=='nessun arbitrato':
        if H in SEV: return H, "R='nessun arbitrato' \u2192 vale il lettore A; claim da scomporre"
        return 'senza esito', "R='nessun arbitrato'"
    # 6) nessun arbitrato registrato: vale il verdetto piu' severo fra H e L
    cand=[x for x in (H,L) if x in SEV]
    if not cand: return 'senza esito','\u2014'
    worst=max(cand, key=lambda x:SEV[x])
    src='lettori (peggiore fra H e L)' if len(cand)==2 else 'solo lettore A'
    return worst, src

# coppie per nodo
by_node={}
for r in estr:
    n=str(r['Nodo'] or '').strip()
    if not n or n=='None': continue
    by_node.setdefault(n,[]).append(r)

def clean(x, lim=None):
    s='' if x is None or str(x)=='None' else str(x).strip()
    return s[:lim] if lim else s

# fonti citate in iTOC col D
def itoc_ids(fr):
    out=[]
    for line in str(fr or '').split('\n'):
        m=re.match(r'\s*\(([^)]+)\)', line)
        if m:
            c=m.group(1).strip()
            out.append((CIT2ID.get(c) or 'FANTASMA:'+c, c, line.strip()))
    return out

# ---- costruzione righe DOSSIER ----
HDR=['Indice','Cap.','Liv.','Titolo nodo','Stato','Budget pp','Parole Descrizione',
     'Fonti AMMESSE (chiavi)','Fonti VIETATE (chiavi + motivo)','N. coppie',
     '⚠ COERENZA','Descrizione (letterale)','Ruolo argomentativo','Trappole / rischi',
     'Note autore','Fonti + ruolo (da iTOC)','DOSSIER FONTI (Estratti, per coppia)']

out=[]
problemi=[]
for r in itoc:
    idx=clean(r['Indice'])
    if not idx: continue
    cap=idx.split('.')[0]; liv=idx.count('.')+1
    desc=clean(r['Descrizione'])
    pairs=by_node.get(idx,[])
    d_ids=itoc_ids(r['Fonti + ruolo'])
    d_keys={k for k,_,_ in d_ids}

    amm=[]; viet=[]; blocks=[]
    for p in sorted(pairs, key=lambda x:str(x['ID fonte'])):
        fid=clean(p['ID fonte']); ver,src=effettivo(p, fid in d_keys)
        fr=FONTI.get(fid,{})
        head=(f"▸ {fid} — {clean(p['Citazione'])}\n"
              f"   ESITO EFFETTIVO: {ver}   [{src}]\n"
              f"   ruolo: {clean(p['Ruolo']) or '—'} · peer-rev: {clean(p['Peer-rev.']) or '—'} · "
              f"acquisizione: {clean(fr.get('Stato acquisizione')) or '—'}")
        body=[head]
        body.append(f"   CLAIM DA VERIFICARE: {clean(p['Claim da verificare'])}")
        body.append(f"   COSA DICE DAVVERO: {clean(p['Cosa dice davvero'])}")
        if clean(p['Citazione verbatim']):
            body.append(f"   VERBATIM (solo verifica — NON citare nel testo) [{clean(p['Sezione']) or 's.n.'}]: "
                        f"{clean(p['Citazione verbatim'])}")
        if clean(p['Note']): body.append(f"   NOTE VERIFICA: {clean(p['Note'])}")
        if clean(p.get('Risoluzione (decisione autore)')):
            body.append(f"   RISOLUZIONE AUTORE: {clean(p['Risoluzione (decisione autore)'])}")
        blocks.append('\n'.join(body))
        if ver.startswith(('usabile','da riformulare')): amm.append(f'{fid} [{ver}]')
        else: viet.append(f'{fid} [{ver}]')

    # coerenza
    fl=[]
    for k,c,_ in d_ids:
        if k.startswith('FANTASMA:'):
            fl.append(f'iTOC cita "{c}" che NON esiste nel foglio Fonti')
        else:
            st=clean(FONTI.get(k,{}).get('Stato acquisizione'))
            if st=='abbandonata': fl.append(f'iTOC cita {k}, fonte ABBANDONATA (fuori da tesi.bib)')
            if (idx,k) not in {(idx,clean(p['ID fonte'])) for p in pairs}:
                fl.append(f'iTOC cita {k} ma non c\'è la riga ({idx},{k}) in Estratti')
    for p in pairs:
        fid=clean(p['ID fonte']); ver,_=effettivo(p, fid in d_keys)
        if fid not in d_keys and ver.startswith(('usabile','da riformulare')):
            fl.append(f'Estratti ha ({idx},{fid}) esito "{ver}" ma iTOC col.D non la registra')
    if desc and not pairs and liv>=3 and len(desc.split())>=60 and cap not in ('5','7','0'):
        fl.append('nodo foglia con ≥60 parole e ZERO coppie in Estratti')
    if fl: problemi.append((idx,fl))

    out.append([idx,cap,liv,clean(r['Titolo nodo']),clean(r['Stato']),r['Budget pp'],
                len(desc.split()),
                ' ; '.join(amm), ' ; '.join(viet), len(pairs),
                ' | '.join(fl),
                desc, clean(r['Ruolo argomentativo']), clean(r['Trappole / rischi']),
                clean(r['Note']), clean(r['Fonti + ruolo']),
                '\n\n'.join(blocks)])

# ---- scrittura ----
if 'DOSSIER' in wb.sheetnames: del wb['DOSSIER']
ws=wb.create_sheet('DOSSIER', 1)
ws.append(HDR)
for row in out: ws.append(row)

hf=Font(bold=True, color='FFFFFF'); hfill=PatternFill('solid', fgColor='1F3864')
for c in range(1,len(HDR)+1):
    cell=ws.cell(1,c); cell.font=hf; cell.fill=hfill
    cell.alignment=Alignment(vertical='center', wrap_text=True)
ws.freeze_panes='D2'
widths=[9,6,6,46,10,10,11,34,34,9,52,80,44,44,44,70,110]
for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
wrap=Alignment(vertical='top', wrap_text=True)
warn=PatternFill('solid', fgColor='FFF2CC'); bad=PatternFill('solid', fgColor='FCE4E4')
for ri in range(2, ws.max_row+1):
    ws.row_dimensions[ri].height=60
    for ci in range(1,len(HDR)+1): ws.cell(ri,ci).alignment=wrap
    if ws.cell(ri,11).value: ws.cell(ri,11).fill=bad
    if ws.cell(ri,9).value:  ws.cell(ri,9).fill=warn
ws.auto_filter.ref=f'A1:{get_column_letter(len(HDR))}{ws.max_row}'

wb.save(P)
print('DOSSIER scritto:', ws.max_row-1, 'righe ·', len(HDR), 'colonne')
print('\n=== NODI CON PROBLEMI DI COERENZA ===')
for idx,fl in problemi:
    print(' ', idx)
    for f in fl: print('    -',f)
