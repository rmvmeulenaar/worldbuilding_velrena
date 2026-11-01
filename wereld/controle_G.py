import sqlite3,subprocess,sys,os
n=sys.argv[1]
subprocess.run(['python3','genereer.py'],check=True)
if os.path.exists('/tmp/rt.db'): os.remove('/tmp/rt.db')
subprocess.run(['python3','importeer.py','WERELD_VELMARA.md','/tmp/rt.db'],check=True,capture_output=True)
a=sqlite3.connect('canon.db');b=sqlite3.connect('/tmp/rt.db')
for t in ('canon','wrijving','open_vraag','logboek'):
  x=a.execute(f'select count(*) from {t}').fetchone()[0];y=b.execute(f'select count(*) from {t}').fetchone()[0]
  print(f'roundtrip {t}: {x} vs {y}','OK' if x==y else 'FOUT')
fa={r for r in a.execute('select code,feit from canon')};fb={r for r in b.execute('select code,feit from canon')}
print('roundtrip feiten gelijk:',fa==fb)
W=open('WERELD_VELMARA.md').read()
codes=[r[0] for r in a.execute('select code from canon where ronde=?',(18+int(n),))]
mis=[c for c in codes if c not in W]
print(f'grep G{n}: {len(codes)-len(mis)}/{len(codes)} codes in WERELD_VELMARA.md; ontbrekend {mis}')
