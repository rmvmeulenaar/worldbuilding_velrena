# Ronde Z3: bijschrijven, dunne categorieën, wrijvingen en open vragen (idempotent)
import sqlite3,shutil,os
from r_Z3_data import R,CAT,REG
from r_Z3_besluit import W,V
RONDE=32;TAG='Z3';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
if not os.path.exists('canon_backup_Z3.db'): shutil.copy('canon.db','canon_backup_Z3.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT'):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
F=lambda z,h,v,s,hk:f'{z} Herkenbaar: {h} Vreemd: {v} Scène: {s}. Haak: {hk}'+GR
for old,(t,z,h,v,s,hk,refs,tech) in R.items():
  cat=c.execute("select categorie from canon where code=?",(old,)).fetchone()[0]
  new=old.replace('Z2','Z3')+'-b'
  add(new,cat,f'Zintuiglijk: {t}',F(z,h,v,s,hk),f'bijgeschreven tot Z1-niveau, vervangt {old}',refs+';'+old,tech)
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z3: vervangen door {new}]',old))
for cat,(k,rows) in CAT.items():
  for i,(t,z,h,v,s,hk,refs,tech) in enumerate(rows,1):
    add(f'ZINT-Z3-{k}-{i}',cat,f'Zintuiglijk: {t}',F(z,h,v,s,hk),f'zintuiglijke vulling {cat}',refs,tech)
for reg,(rc,rows,naam,mo) in REG.items():
  for i,(t,z,h,v,s,hk,refs,tech) in enumerate(rows,1):
    add(f'ZINT-Z3-{reg}-{i}','Zintuigen',t,F(z,h,v,s,hk),f'verdieping regio {naam}',f'{rc};ZINT-MOTIEF-{reg}',tech)
# wrijvingen
w=0
for code,opl in W.items():
  r=c.execute("select status,verwijst_naar,titel from wrijving where code=?",(code,)).fetchone()
  if not r: continue
  if r[0]!='opgelost':
    c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=?",(' | Oplossing Z3 (ingenieur): '+opl,code));w+=1
  add(f'BESLUIT-Z3-{code}','Besluit',f'Wrijving opgelost: {r[2]}',opl,f'oplossing {code}; levert verhaalmotor',(r[1] or '')+';'+code,'geen','BESL')
v=0
for code,a in V.items():
  r=c.execute("select status from open_vraag where code=?",(code,)).fetchone()
  if r and r[0]=='open':
    c.execute("update open_vraag set status='beantwoord (voorlopig)', antwoord=? where code=?",('Z3 (ingenieur): '+a,code));v+=1
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z3] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z3'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z3: haken, zintuigen, verbindingen',txt,'voorlopig','Ronde Z3: meting','ZINT-DEKKING-Z2',RONDE,'ZINT-DEKKING-Z3','REG-overzicht;ZINT-DEKKING-Z2','geen','META'))
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde Z3: vervangen door ZINT-DEKKING-Z3]' where code='ZINT-DEKKING-Z2' and status not like '%vervangen%'")
c.execute("delete from logboek where wat like 'Ronde Z3:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z3: {len(R)} rijen bijgeschreven, vulling Religie/Economie/Rituelen/Extreme rituelen/Dagelijks leven/Tijdperk (12) en Stille/Hoogvrouwe/Kharvos-B1 (10), {len(W)} wrijvingen opgelost, {len(V)} open vragen beantwoord, ZINT-DEKKING-Z3.'))
c.commit()
print('nieuw',n,'wrij',w,'vragen',v)
print('open wrij',c.execute("select count(*) from wrijving where status!='opgelost'").fetchone(),'open vragen',c.execute("select count(*) from open_vraag where status='open'").fetchone(),'canon',c.execute('select count(*) from canon').fetchone())
print(txt)
