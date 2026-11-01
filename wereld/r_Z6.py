# Ronde Z6: wrijvingen, oude vragen, erotische laag (idempotent); data in z6/*.py
import sqlite3,shutil,os,sys
sys.path.insert(0,'z6');from wrij import W,V;from eros import VOLK,REG,SCENE,TAAL;from geil import G
RONDE=35;TAG='Z6';D='2026-10-31'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
if not os.path.exists('canon_backup_Z6.db'): shutil.copy('canon.db','canon_backup_Z6.db')
c=sqlite3.connect('canon.db');n=0;nv=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT',status='voorlopig'):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+GR,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
def vervang(old,new):
  global nv
  nv+=c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z6: vervangen door {new}]',old)).rowcount
# 1 wrijvingen
for wc,(tekst,olds,bij) in W.items():
  r=c.execute("select titel,verwijst_naar from wrijving where code=?",(wc,)).fetchone()
  if not r: continue
  nr=wc.split('-')[1];bc=f'BESLUIT-Z6-WRIJ-{nr}'
  add(bc,'Besluit',f'Besluit wrijving {wc}: {r[0]}',tekst+' Haak: zie verhaal hierboven.','ingenieursbesluit wrijving',f'{wc};{r[1]}','geen','BESL')
  for o in olds:
    x=c.execute("select categorie,onderwerp,feit,verwijst_naar,techniek,functie from canon where code=? and status not like '%vervangen%'",(o,)).fetchone()
    if not x: continue
    new=o+'-Z6';add(new,x[0],x[1],x[2].split(' Label:')[0]+' Bijgesteld: '+bij,f'bijgesteld na {bc}',(x[3] or '')+';'+bc,x[4] or 'geen',x[5] or 'ZINT');vervang(o,new)
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and status='open'",(f' [Opgelost in Z6: {bc}]',wc))
# 2 vragen
for vc,(alt,keuze,reden,eff) in V.items():
  bc=f'BESLUIT-Z6-{vc}'
  add(bc,'Besluit',f'Besluit {vc}',f'Alternatieven: {alt}. Keuze: {keuze}. Reden: {reden}. Effect op verhalen: {eff}. Haak: {eff}.','ingenieursbesluit oude open vraag',vc,'geen','BESL')
  c.execute("update open_vraag set status='beantwoord (voorlopig)', antwoord=? where code=? and status='voorstel gedaan'",(f'Z6 (ingenieur): {keuze}. Zie {bc}.',vc))
# 3 erotiek
add('EROS-GRENZEN-Z6','Kinks en situaties','Veiligheidslijnen van de erotiek','Alleen volwassenen (18+), ook in geschiedenis en rituelen. Alleen seks met instemming; wie niet kan instemmen (dragers, Orrim in het Zegel) komt nooit in een seksuele rol, alleen als horror zonder seks. Geen dieren in een seksuele rol. Dwang alleen als gelabeld donker thema tussen volwassenen. Instemming is spanning, geen hindernis. Haak: elke volksvorm van ja en nee staat in EROS-Z6-VOLK-*.','grenzen','REGEL-seksuele-normen','geen','LUST','vastgesteld')
for vc,(verl,zin,taal,op,tab,inst,hk) in VOLK.items():
  s=vc.replace('VOLK-','')
  add(f'EROS-Z6-VOLK-{s}','Volken seksualiteit',f'Erotiek bij {s}',f'Verleiding: {verl}. Zintuig: {zin}. Taal en tempo: {taal}. Wat opwindt: {op}. Taboe: {tab}. Instemming: {inst}. Diversiteit: alle seksualiteiten komen voor. Haak: {hk}.','erotische laag per volk',f'{vc};EROS-GRENZEN-Z6','geen','LUST')
for rc,(zin,stijl) in REG.items():
  s=rc.replace('REG-','')
  add(f'EROS-Z6-REG-{s}','Volken seksualiteit',f'Erotiek in {s}',f'Geur en gevoel: {zin}. Stijl: {stijl}. Instemming wordt gevraagd in de taal van de streek (zie EROS-TAAL-Z6). Haak: wie de streekregel breekt, verraadt waar hij vandaan komt.','erotische laag per regio',f'{rc};EROS-GRENZEN-Z6','geen','LUST')
for i,(soort,wie,zin,wat,kost) in enumerate(SCENE,1):
  add(f'EROS-SCENE-Z6-{i}','Kinks en situaties',f'Scènesjabloon: {soort}',f'Soort: {soort}. Wie (volwassen): {wie}. Zintuig dat draagt: {zin}. Wat verandert: {wat}. Wat het kost: {kost}. Instemming expliciet in de scène. Haak voor intrige: {kost}.','scènesjabloon','EROS-GRENZEN-Z6;LIJST-Z4-boek1','geen','LUST')
for i,(wie,woord,klank) in enumerate(TAAL,1):
  add(f'EROS-TAAL-Z6-{i}','Voorkeuren',f'Taal van lust: {wie}',f'Woorden: {woord}. Geluid: {klank}. Haak: wie het verkeerde woord kiest, verraadt zijn afkomst.','taal en geluid van lust','EROS-GRENZEN-Z6','geen','LUST')
for i,(ond,refs,hon,lich,hk) in enumerate(G,1):
  add(f'EROS-GEIL-Z6-{i}','Voorkeuren',f'Geilheid: {ond}',f'Wat hongerig maakt: {hon}. Lichaam: {lich}. Haak (intrige): {hk}.','geilheid als eigen laag (aanvulling Rogier)',refs+';EROS-GRENZEN-Z6','geen','LUST')
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z6] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z6'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z6',txt,'voorlopig','Ronde Z6: meting','ZINT-DEKKING-Z5',RONDE,'ZINT-DEKKING-Z6','REG-overzicht;ZINT-DEKKING-Z5','geen','META'))
vervang('ZINT-DEKKING-Z5','ZINT-DEKKING-Z6')
c.execute("delete from logboek where wat like 'Ronde Z6:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z6: alle open wrijvingen opgelost, 10 oude vragen beslist, erotische laag (volk, regio, scènes, taal, geilheid, grenzen).'))
c.commit()
print('nieuw',n,'vervangen',nv,'canon',c.execute('select count(*) from canon').fetchone()[0])
print('open wrij',c.execute("select count(*) from wrijving where status='open'").fetchone(),'open vragen',c.execute("select count(*) from open_vraag where status in ('open','voorstel gedaan')").fetchone());print(txt)
