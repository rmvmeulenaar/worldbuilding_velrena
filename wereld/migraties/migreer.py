#!/usr/bin/env python3
"""Past genummerde migraties (NNN_naam.py) in volgorde toe en noteert ze in schema_versie. Idempotent.
Gebruik: python3 migraties/migreer.py [db]"""
import sqlite3,sys,os,glob,importlib.util,datetime
D=os.path.dirname(os.path.abspath(__file__))
def draai(c):
  c.execute('create table if not exists schema_versie(versie integer primary key,naam text,toegepast text)')
  gedaan=[]
  for p in sorted(glob.glob(os.path.join(D,'[0-9][0-9][0-9]_*.py'))):
    s=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    m.migreer(c)  # altijd idempotent, dus ook bij een nieuwe/geïmporteerde db veilig
    if not c.execute('select 1 from schema_versie where versie=?',(m.VERSIE,)).fetchone():
      c.execute('insert into schema_versie values(?,?,?)',(m.VERSIE,m.NAAM,str(datetime.date.today())));gedaan.append(m.NAAM)
  c.commit();return gedaan
if __name__=='__main__':
  c=sqlite3.connect(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(D),'canon.db'))
  print('toegepast:',draai(c) or 'niets nieuw',c.execute('select * from schema_versie').fetchall())
