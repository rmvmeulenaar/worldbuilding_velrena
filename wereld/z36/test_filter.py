# Filtertest met opzettelijk foute profielen, op een tijdelijke kopie (niets in canon.db). Elke regel moet WEIGERT tonen.
import sqlite3,shutil,sys,os,random,json,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import machine as M
shutil.copy('canon.db','/tmp/filtertest.db');c=sqlite3.connect('/tmp/filtertest.db')
w=M.Wereld(c,'6');rng=random.Random(5)
basis=M.maak(w,rng,'vervalser');basis.update(genre='horror',schaal='rijk',vorm='documenten',afloop='werkt',volk='mens',hoofdpersoon='26-40|v',leeftijd=32)
for g,x in M.genrevector(basis).items(): basis['g_'+g]=x
SLECHT=[('hoofdpersoon 16',dict(leeftijd=16,hoofdpersoon='18-25|v')),('dier als partner bij erotiek',dict(g_erotiek=4,partner='dier',wereldregel_code='RIT-veiling')),
 ('minderjarige partner',dict(g_erotiek=3,partner='minderjarige',wereldregel_code='RIT-veiling')),('kan niet instemmen',dict(g_erotiek=3,instemming='niet mogelijk',wereldregel_code='RIT-veiling')),
 ('dwang zonder label',dict(instemming='dwang',dwang_label=0)),('erotiek zonder wereldregel',dict(g_erotiek=4,wereldregel_code=None)),
 ('volk bestaat niet in fase 4 (myrrhen)',None),('kopie van een boog (afstand < 3)',None),('onbekende vorm',dict(vorm='sonnet'))]
ok=True
for naam,d in SLECHT:
  p=dict(basis);ww=w
  if naam.startswith('volk'): ww=M.Wereld(c,'4');p['fase']=ww.fase;p['volk']='myrrhen'
  elif naam.startswith('kopie'):
    b=dict(w.bogen[0]);p.update({k:b[k] for k in M.ASSEN});p['hoofdpersoon']='26-40|m' if b['hoofdpersoon']!='26-40|m' else '26-40|v'
  else: p.update(d)
  r=M.filter(ww,p)
  try: M.bewaar(c,ww,p,'TEST','filtertest');opgeslagen=True
  except ValueError: opgeslagen=False
  print(f"{'WEIGERT' if r and not opgeslagen else 'LAAT DOOR'} | {naam} | {r}");ok&=bool(r) and not opgeslagen
# doorkomer: zelfde basis zonder fout moet wel door de filters
print('controle goed profiel:',M.filter(w,basis) or 'door alle filters')
# directe insert om de toetsregel zelf te testen (buiten de machine om)
c.execute("insert into verhaal_profiel(code,run,fase,positie,genre,schaal,volk,vorm,afloop,hoofdpersoon,leeftijd,partner,instemming,g_erotiek,uitslag) values('VP-TEST-slecht','TEST','6 Markt','betaler','romance','huis','mens','brieven','faalt','18-25|v',16,'dier','ja',3,'voorgesteld')");c.commit()
r=subprocess.run([sys.executable,'toets.py','/tmp/filtertest.db'],capture_output=True,text=True)
print('toets.py op een db met een slecht profiel dat buiten de machine om is ingevoegd: exit',r.returncode);print('\n'.join(l for l in r.stdout.splitlines() if 'VP-TEST' in l or 'Nieuwe fouten' in l))
print('UITSLAG:', 'alle foute profielen geweigerd' if ok and r.returncode==1 else 'FOUT: iets kwam door')
