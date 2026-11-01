#!/usr/bin/env python3
"""Ronde Z31: roundtrip-controle. WERELD_VELMARA.md -> importeer.py -> migraties -> afgeleid.py -> vergelijk ALLE tabellen met canon.db (zonder id-kolom, als multiset). Exit 1 bij verschil."""
import sqlite3,subprocess,sys,os,collections,tempfile
sys.path.insert(0,'migraties');import afgeleid,migreer
DB=sys.argv[1] if len(sys.argv)>1 else 'canon.db'
d=tempfile.mkdtemp();nw=os.path.join(d,'rt.db')
subprocess.run([sys.executable,'importeer.py','WERELD_VELMARA.md',nw],check=True,capture_output=True)
n=sqlite3.connect(nw);migreer.draai(n);afgeleid.bouw(n);o=sqlite3.connect(DB)
tabs=[r[0] for r in o.execute("select name from sqlite_master where type='table'")]
fout=0
for t in tabs:
  if t=='schema_versie': cols=['versie','naam']
  else: cols=[r[1] for r in o.execute(f'pragma table_info({t})') if r[1]!='id']
  nc=[r[1] for r in n.execute(f'pragma table_info({t})')]
  mis=[k for k in cols if k not in nc]
  if mis: print(t,'KOLOMMEN KWIJT:',mis);fout+=1;continue
  A=collections.Counter(o.execute(f"select {','.join(cols)} from {t}"));B=collections.Counter(n.execute(f"select {','.join(cols)} from {t}"))
  dv=sum(((A-B)+(B-A)).values());fout+=bool(dv);print(f'{t}: {sum(A.values())} rijen, {len(cols)} kolommen, verschillen {dv}')
vo=[r[0] for r in o.execute("select name from sqlite_master where type='view'")];vn=[r[0] for r in n.execute("select name from sqlite_master where type='view'")]
print('views gelijk:',sorted(vo)==sorted(vn),sorted(vo))
sys.exit(1 if fout else 0)
