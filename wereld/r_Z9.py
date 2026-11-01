# Ronde Z9: actie, oorlog/agressie, horror (idempotent); data in z9/*.py
import sqlite3,shutil,os,sys
sys.path.insert(0,'z9');from actie import A;from oorlog import O;from horror import H,S
RONDE=38;TAG='Z9';D='2026-10-31'
GR=" Veiligheidslabel: geweld, oorlog en horror mogen hard zijn; alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen."
if not os.path.exists('canon_backup_Z9.db'): shutil.copy('canon.db','canon_backup_Z9.db')
c=sqlite3.connect('canon.db');n=0
BEST={r[0] for r in c.execute('select code from canon')}
AL={'PER-jorrit-Z7':'PER-Z7-jorrit','VOORW-Z7-registerkraai':'VOORW-Z7-registerkraai-oud','EROS-STOP-Z7-zoutkust':'EROS-STOP-Z7-mensen-zoutkust','BESLUIT-Z7-liora-kracht':'BESLUIT-Z7-LIORA-KRACHT'}
def R(refs,extra):
  k=[AL.get(x,x) for x in refs.split(';')];k=[x for x in k if x in BEST]+[extra]; return ';'.join(dict.fromkeys(k))
def add(code,cat,ond,feit,reden,refs,tech,functie,afst=None):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("update canon set verwijst_naar=?,hangt_samen_met=? where code=? and ronde=?",(refs,refs,code,RONDE)); return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie,afstoting) values(?,?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+GR,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie,afst));n+=1
for i,(o,l,w,wp,wd,k,h,z,r,t) in enumerate(A,1):
  add(f'ACTIE-Z9-{i}','Actie',f'Actie: {o}',f'Locatie: {l}. Wie (volwassen): {w}. Wapen/gave: {wp}. Zintuig: {z}. Wending: {wd}. Wat het kost: {k}. Haak: {h}. Techniek: {t}.','actiescènes (wens Rogier)',R(r,'FUNC-MIL'),t,'MIL')
for i,(o,f,w,z,k,h,r,t) in enumerate(O,1):
  add(f'OORLOG-Z9-{i}','Oorlog',f'Oorlog (fase {f}): {o}',f'{w}. Zintuig: {z}. Prijs: {k}. Haak: {h}. Techniek: {t}.','oorlog en agressie als keten door fasen 0-7 (wens Rogier)',R(r,f'LIJN-fase-{f}' if 1<=f<=5 else 'FUNC-MIL'),t,'MIL')
for i,(o,dr,op,z,a,v,h,s,r,t) in enumerate(H,1):
  add(f'HORROR-Z9-{i}','Horror',f'Horror: {o}',f'Dreiging: {dr}. Opbouw: {op}. Zintuig dat de gruwel draagt: {z}. Afstoting: {a}/10. Wat de personages verliezen: {v}. Haak: {h}. Zo schrijf je het: {s}. Techniek: {t}.','horror uit de wereldoorzaak (wens Rogier)',R(r,'GEB-sterrensteen-val'),t,'HORROR',int(a))
for i,(o,hp,dr,op,cl,e,r) in enumerate(S,1):
  add(f'HORROR-SKELET-Z9-{i}','Verhaal',f'Horrorskelet: {o}',f'Hoofdpersoon (volwassen): {hp}. Dreiging: {dr}. Opbouw: {op}. Climax: {cl}. Einde en prijs: {e}. Haak: het einde opent een volgend verhaal.','horrorverhaalskelet',R(r,f'HORROR-Z9-{i}'),'geen','VERH')
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z9] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z9'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z9',txt,'voorlopig','Ronde Z9: meting','ZINT-DEKKING-Z8',RONDE,'ZINT-DEKKING-Z9','REG-overzicht;ZINT-DEKKING-Z8','geen','META'))
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde Z9: vervangen door ZINT-DEKKING-Z9]' where code='ZINT-DEKKING-Z8' and status not like '%vervangen%'")
c.execute("delete from logboek where wat like 'Ronde Z9:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z9: {len(A)} actie, {len(O)} oorlog/agressie, {len(H)} horror + {len(S)} horrorskeletten; alles voorlopig, binnen de vaste lijnen.'))
c.commit()
print('nieuw',n,'canon',c.execute('select count(*) from canon').fetchone()[0]);print(txt)
