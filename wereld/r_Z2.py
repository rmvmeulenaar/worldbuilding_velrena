# Ronde Z2: zintuiglijke verdieping dunne categorieën + Ambergaard/Saelith + REG-kharvos opschonen (idempotent)
import sqlite3,shutil,os
from r_Z2_data import CAT,REG
RONDE=31;TAG='Z2';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
if not os.path.exists('canon_backup_Z2.db'): shutil.copy('canon.db','canon_backup_Z2.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT'):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
for cat,(k,rows) in CAT.items():
  for i,(t,z,h,v,s,hk,refs,tech) in enumerate(rows,1):
    add(f'ZINT-Z2-{k}-{i}',cat,f'Zintuiglijk: {t}',f'{z} Herkenbaar: {h} Vreemd: {v} Scène: {s}. Haak: {hk}'+GR,f'zintuiglijke verdieping {cat}',refs,tech)
for reg,(rc,rows,mo,mf) in REG.items():
  for i,(soort,t,z,h,v,s,hk,refs,tech) in enumerate(rows,1):
    add(f'{soort}-Z2-{reg}-{i}','Land' if soort=='STAD' else 'Zintuigen',t,f'{z} Herkenbaar: {h} Vreemd: {v} Scène: {s}. Haak: {hk}'+GR,f'verdieping regio {reg}',f'{rc};{refs};ZINT-MOTIEF-{reg}',tech)
  add(f'ZINT-MOTIEF-Z2-{reg}','Zintuigen',mo,mf+' Gebruik: herhaal het motief bij elke scène in deze regio, zonder het te benoemen. Haak: het tegenmotief markeert waar het Zegel zich laat zien.','verdiept motief',f'{rc};ZINT-MOTIEF-{reg}')
# 3 verwijzingen
om=0
for id_,v in c.execute("select id,verwijst_naar from canon where verwijst_naar like '%REG-kharvos%'").fetchall():
  parts=(v or '').split(';');new=[('REG-kharvos-B1' if p.strip()=='REG-kharvos' else p) for p in parts]
  if new!=parts:
    c.execute("update canon set verwijst_naar=? where id=?",(';'.join(dict.fromkeys(new)),id_));om+=1
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z2] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z2'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z2: haken, zintuigen, verbindingen',txt,'voorlopig','Ronde Z2: meting (herberekend bij elke run)','ZINT-DEKKING',RONDE,'ZINT-DEKKING-Z2','REG-overzicht;ZINT-DEKKING','geen','META'))
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde Z2: vervangen door ZINT-DEKKING-Z2]' where code='ZINT-DEKKING' and status not like '%vervangen%'")
c.execute("delete from logboek where wat like 'Ronde Z2:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z2: zintuiglijke verdieping (12 per categorie: Bestuur, Magie, Kinks, Wetten, Voorkeuren, Ritueel, Besluit, Planten en dieren), 10 regiorijen + verdiept motief voor Ambergaard en Saelith, ZINT-DEKKING-Z2; verwijst_naar REG-kharvos -> REG-kharvos-B1 in alle rijen die het noemden.'))
c.commit();print('nieuw',n,'omgezet',om);print(txt)
