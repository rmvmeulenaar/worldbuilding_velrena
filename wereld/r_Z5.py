# Ronde Z5: diepte en details (idempotent); data in z5/*.txt
import sqlite3,shutil,os
RONDE=34;TAG='Z5';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
if not os.path.exists('canon_backup_Z5.db'): shutil.copy('canon.db','canon_backup_Z5.db')
c=sqlite3.connect('canon.db');n=0;nv=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT',status='voorlopig'):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+GR,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
def vervang(old,new):
  global nv
  nv+=c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z5: vervangen door {new}]',old)).rowcount
def L(f): return [l.rstrip('\n').split('|') for l in open('z5/'+f,encoding='utf-8') if l.strip()]
# 1 bijschrijven
for f in ['bij.txt','bij2.txt','bij3.txt']:
  for old,g,k,v,li,h,vr,sc,hk in L(f):
    r=c.execute("select categorie,onderwerp,feit,verwijst_naar,techniek,functie from canon where code=?",(old,)).fetchone()
    if not r: continue
    kern=r[2].split(' Label:')[0]
    if old.startswith('ZINT-Z3'): kern=''
    new=old+'-Z5b'
    blok=f'Geur: {g}. Geluid: {k}. Gevoel: {v}. Licht: {li}. Herkenbaar: {h}. Vreemd: {vr}. Scène: {sc}. Haak: {hk}.'
    add(new,r[0],r[1],(kern+' Verdiept (Z5): '+blok).strip() if kern else blok,f'bijgeschreven tot Z1-niveau, vervangt {old}',(r[3] or '')+';'+old,r[4] or 'geen',r[5] or 'ZINT')
    vervang(old,new)
# 2 verdieping
CATS=[('n_verhaal.txt','verhaal'),('n_gesch.txt','geschiedenis'),('n_seks.txt','seksualiteit'),('n_cult.txt','cultuur'),('n_gez.txt','gezondheid'),('n_lich.txt','lichaam'),('n_voor.txt','voorwerp'),('n_rel.txt','religie')]
for f,slug in CATS:
  for i,(t,g,k,v,li,vr,hk) in enumerate(L(f),1):
    r=c.execute("select categorie,onderwerp,techniek from canon where code=?",(t,)).fetchone()
    if not r: print('ontbreekt',t);continue
    add(f'ZINT-Z5-{slug}-{i}',r[0],f'Verdieping: {r[1]}',f'Verdieping van {t} ({r[1]}). Geur: {g}. Geluid: {k}. Gevoel: {v}. Licht: {li}. Vreemd: {vr}. Haak: {hk}.','zintuiglijke verdieping van een bestaande rij',t,r[2] or 'geen')
# 3 goedkeuring (Rogier akkoord met suggesties, via parent)
add('BESLUIT-Z5-makers','Besluit','Besluit Rogier: Makers in fase 0 per volk','Elk volk krijgt in fase 0 een Maker-voorganger, maar met twee soorten band. Aangepaste volken (Aelthir, Skerra, Orrim, Tharn, Dhurn, Sael-mor, Ishvar en andere mensenvolken) stammen echt af van Makers of hun bemanning. Gegroeide volken (Kluwers, Myrrhen, Oevrin, Ves-Lethi) hebben een Maker als schepper of bevrijder, niet als bloedvoorouder (Dr. Imke Zaal, Archivaris Pell Dunn, Fien Brakker, Proefpersoon Leth). Alternatief was: Makers alleen bij mensenvolken (te weinig oorzaak voor de anderen) of overal als voorouder (biologisch onlogisch). Waarom: alles komt uit één oorzaak, maar functie eerst: wie gegroeid is, heeft een maker en geen moeder. Gevolg voor de verhalen: elk volk kan in de kluis een eigen dossier vinden; voor mensenvolken is het familie, voor de anderen een schepper die hen vrijliet of misbruikte. Haak: de Kluwers ontdekken dat hun schepper in de eerste raat ligt en tegen bevel in handelde.','besluit Rogier (akkoord met suggestie Z5, via parent)','BESLUIT-Z4-fasen;PERS-Z4-kluwer-0-2;PERS-Z4-myrrhen-0-2;PERS-Z4-oevrin-0-2;PERS-Z4-veslethi-0-2;PERS-Z4-aelthir-0-1','geen','BESL','vastgesteld')
add('BESLUIT-Z5-buitenstaanders','Besluit','Besluit Rogier: personen die niet bij hun volk horen','Tamsin Dijkvrouw (PERS-Z4-tharn-1-2) is een mens die bij de Tharn werkt als dijkvrouw en tolk; Tobin de Smokkelaar (PERS-Z4-oevrin-7-1) is een mens die door de Oevrin is aangenomen. Ze blijven in de lijst van hun gastvolk, gelabeld als "aangenomen", met reden: wie het volk verandert, hoort bij de keten, ook als het bloed anders is. Alternatief was: verplaatsen naar een mensenvolk (verlies van de brugfunctie) of vervangen door een Tharn/Oevrin (verlies van bestaande lijnen). Gevolg voor de verhalen: buitenstaanders zijn de natuurlijke vertellers voor de lezer en de bron van wantrouwen binnen het volk; ze kunnen verraden of verbinden. Haak: een Tharn-reus vraagt Tamsin het dijklied te zingen, en zij kan het niet, omdat ze het lichaam niet heeft om het te voelen.','besluit Rogier (akkoord met suggestie Z5, via parent)','PERS-Z4-tharn-1-2;PERS-Z4-oevrin-7-1;PER-tamsin;PER-tobin;VOLK-tharn;VOLK-oevrin','geen','BESL','vastgesteld')
add('LIJST-Z5-goedkeuring','Besluit','TER GOEDKEURING (Z5): twee keuzes uit Z4','(a) Makers als voorouders van elk volk in fase 0. Alternatieven: alleen mensenvolken; overal bloedvoorouder; tweeledig (voorouder bij aangepaste volken, schepper bij gegroeide volken). Suggestie: tweeledig, omdat het biologisch klopt en toch alles uit één oorzaak laat komen; effect: elk volk een eigen kluisdossier, met familie of met een schepper. (b) Personen die niet bij hun volk horen (Tamsin bij de Tharn, Tobin bij de Oevrin). Alternatieven: verplaatsen; vervangen; houden als aangenomen. Suggestie: houden als aangenomen, omdat ze bruggen zijn; effect: vertellersrol voor de lezer en bron van wantrouwen. Status: beide goedgekeurd door Rogier, zie BESLUIT-Z5-makers en BESLUIT-Z5-buitenstaanders. Haak: elke keuze laat een spoor van twijfel achter.','lijst ter goedkeuring','BESLUIT-Z5-makers;BESLUIT-Z5-buitenstaanders','geen','BESL','vastgesteld')
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z5] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z5'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z5',txt,'voorlopig','Ronde Z5: meting','ZINT-DEKKING-Z4',RONDE,'ZINT-DEKKING-Z5','REG-overzicht;ZINT-DEKKING-Z4','geen','META'))
vervang('ZINT-DEKKING-Z4','ZINT-DEKKING-Z5')
c.execute("delete from logboek where wat like 'Ronde Z5:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z5: korte rijen bijgeschreven, verdiepingsrijen in 8 categorieën, besluiten Makers en buitenstaanders (Rogier akkoord).'))
c.commit()
print('nieuw',n,'vervangen',nv,'canon',c.execute('select count(*) from canon').fetchone()[0]);print(txt)
