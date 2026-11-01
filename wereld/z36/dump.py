import sqlite3,sys,hashlib
def dump(p):
  c=sqlite3.connect(p);out={}
  for (t,) in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by 1"):
    cols=sorted(r[1] for r in c.execute(f'pragma table_info({t})') if r[1]!='id')
    rows=sorted(repr(r) for r in c.execute(f"select {','.join(cols)} from {t}"))
    if t=='wijziging' or t=='schema_versie': rows=sorted(x for x in rows)
    out[t]=(len(rows),hashlib.md5('\n'.join(rows).encode()).hexdigest())
  return out
a,b=dump(sys.argv[1]),dump(sys.argv[2])
diff=[t for t in set(a)|set(b) if a.get(t)!=b.get(t)]
print('tabellen',len(a),'verschillen:',diff or 0)
for t in diff: print(' ',t,a.get(t),b.get(t))
