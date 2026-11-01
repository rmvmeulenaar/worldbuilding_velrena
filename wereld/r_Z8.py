# Ronde Z8: lichaamsvorming/bimbofication, verleiding, expliciete kinks (idempotent); data in z8/*.py
import sqlite3,shutil,os,sys
sys.path.insert(0,'z8');from body import B;from verleid import V,S;from kink import K
RONDE=37;TAG='Z8';D='2026-10-31'
GR=" Veiligheidslabel: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; dwang tussen volwassenen alleen als gelabeld donker thema."
DK=" Donker thema (gelabeld): dwang/overmacht tussen volwassenen, met prijs en gevolg."
if not os.path.exists('canon_backup_Z8.db'): shutil.copy('canon.db','canon_backup_Z8.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,tech,functie):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+GR,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
for i,(o,z,k,h,r,t,d) in enumerate(B,1):
  add(f'BODY-Z8-{i}','Lichaam en vervorming',f'Vorming: {o}',f'Zintuig: {z}. Wat het kost: {k}. Haak: {h}. Techniek: {t}.'+(DK if d else ''),'lichaamsvorming en bimbofication (wens Rogier)',r+';LICH-gaven-vervorming',t,'LUST')
for i,(o,w,z,k,h,r) in enumerate(V,1):
  add(f'VERLEID-Z8-{i}','Kinks en situaties',f'Verleiding: {o}',f'Wie (volwassen): {w}. Zintuig en taal: {z}. Wat het kost: {k}. Haak: {h}.'+(DK if 'donker' in o else ''),'verleidingslaag (wens Rogier)',r+';EROS-GRENZEN-Z7','geen','LUST')
for i,(o,hp,tg,doel,wend,eind) in enumerate(S,1):
  add(f'VERLEID-SKELET-Z8-{i}','Verhaal',f'Verleidingsskelet: {o}',f'Hoofdpersoon (volwassen): {hp}. Tegenspeler (volwassen): {tg}. Doel: {doel}. Wending: {wend}. Einde: {eind}. Haak: het einde opent een volgend verhaal.','verhaalskelet verleiding','EROS-GRENZEN-Z7;VERLEID-Z8-20','geen','VERH')
for i,(o,wat,wie,af,z,k,h,r,t,d) in enumerate(K,1):
  add(f'KINK-Z8-{i}','Kinks en situaties',f'Kink: {o}',f'Wat in Velmara: {wat}. Wie (volwassen): {wie}. Afspraak/stopwoord: {af}. Zintuig: {z}. Risico en prijs: {k}. Haak: {h}. Techniek: {t}.'+(DK if d else ''),'expliciete kinks (wens Rogier: fisting, latex, BDSM e.a.)',r+';EROS-GRENZEN-Z7',t,'LUST')
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z8] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z8'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z8',txt,'voorlopig','Ronde Z8: meting','ZINT-DEKKING-Z7',RONDE,'ZINT-DEKKING-Z8','REG-overzicht;ZINT-DEKKING-Z7','geen','META'))
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde Z8: vervangen door ZINT-DEKKING-Z8]' where code='ZINT-DEKKING-Z7' and status not like '%vervangen%'")
c.execute("delete from logboek where wat like 'Ronde Z8:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z8: 50 vormingsrijen (bimbofication), 30 verleidingsrijen + 10 skeletten, 60 kinkrijen; alles voorlopig, binnen de vaste lijnen.'))
c.commit()
print('nieuw',n,'canon',c.execute('select count(*) from canon').fetchone()[0]);print(txt)
