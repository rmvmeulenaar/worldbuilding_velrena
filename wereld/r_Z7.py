# Ronde Z7: besluiten verhaal 1, stopwoorden, rauwe erotische laag (idempotent); data in z7/*.py
import sqlite3,shutil,os,sys
sys.path.insert(0,'z7');from data import BES,NIEUW,STOP;from rauw import R
RONDE=36;TAG='Z7';D='2026-10-31'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; dwang tussen volwassenen alleen als gelabeld donker thema."
if not os.path.exists('canon_backup_Z7.db'): shutil.copy('canon.db','canon_backup_Z7.db')
c=sqlite3.connect('canon.db');n=0;nv=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT',status='voorlopig',lab=True):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+(GR if lab else ''),status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
def vervang(old,new):
  global nv
  nv+=c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z7: vervangen door {new}]',old)).rowcount
for code,(ond,feit,alt,eff,refs,tech) in BES.items():
  add(code,'Besluit',ond,f'{feit}. Reden en alternatieven: {alt}. {eff}.','besluit uit verhaal 1 (goedgekeurd door Rogier)',refs+';verhaal_01_brakhaven',tech,'BESL','vastgesteld',lab=False)
for code,cat,ond,feit,refs in NIEUW:
  add(code,cat,ond,feit+'.','nieuw uit verhaal 1',refs,'geen','ZINT','vastgesteld',lab=False)
add('EROS-GRENZEN-Z7','Kinks en situaties','Vaste lijnen van de erotiek (Z7)','Vaste lijnen: alleen volwassenen (18+), ook in geschiedenis en ritueel; geen dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen (kinderen, dieren, gebonden Dochters en Orrim in het Zegel, ernstig zieken): die blijven horror zonder seks. Instemming hoeft niet in elke scène een beat te zijn: escapisme mag rauw. Dwang en overmacht tussen volwassenen zijn een gelabeld donker thema, geen standaard, en hebben altijd een prijs en een gevolg. Haak: zie EROS-RAUW-Z7-* en EROS-STOP-Z7-*.','grenzen herzien na wens Rogier','REGEL-seksuele-normen;EROS-GRENZEN-Z6','geen','LUST','vastgesteld',lab=False)
vervang('EROS-GRENZEN-Z6','EROS-GRENZEN-Z7')
for v,(woord,wanneer) in STOP.items():
  ref='REG-zoutkust;BESLUIT-Z7-JORRIT' if v=='mensen-zoutkust' else f'VOLK-{v};EROS-Z6-VOLK-{v}'
  add(f'EROS-STOP-Z7-{v}','Volken seksualiteit',f'Stopwoord bij {v}',f'Woord of teken: {woord}. Wanneer wel en niet: {wanneer}. Haak: wie het teken van een ander volk gebruikt, verraadt waar hij geleerd heeft.','stopwoord per volk',ref+';EROS-GRENZEN-Z7','geen','LUST')
for i,(ond,wie,zin,kost,intr,hk,donker) in enumerate(R,1):
  lb=' Donker thema (gelabeld): dwang/overmacht tussen volwassenen, met prijs en gevolg.' if donker else ''
  add(f'EROS-RAUW-Z7-{i}','Kinks en situaties',f'Rauw: {ond}',f'Wie (volwassen): {wie}. Zintuig: {zin}. Wat het kost: {kost}. Intrige: {intr}. Haak: {hk}.{lb}','rauwe erotische laag (wens Rogier: escapisme)','EROS-GRENZEN-Z7','geen','LUST')
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z7] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z7'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z7',txt,'voorlopig','Ronde Z7: meting','ZINT-DEKKING-Z6',RONDE,'ZINT-DEKKING-Z7','REG-overzicht;ZINT-DEKKING-Z6','geen','META'))
vervang('ZINT-DEKKING-Z6','ZINT-DEKKING-Z7')
c.execute("delete from logboek where wat like 'Ronde Z7:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z7: 4 besluiten uit verhaal 1, nieuwe personen/voorwerpen, stopwoorden per volk, rauwe erotische laag, grenzen herzien.'))
c.commit()
print('nieuw',n,'vervangen',nv,'canon',c.execute('select count(*) from canon').fetchone()[0]);print(txt)
