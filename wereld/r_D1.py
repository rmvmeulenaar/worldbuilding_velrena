# Ronde D1+D2+BESTUUR+CROSSLINKS (idempotent)
import sqlite3,shutil,os,re,json
RONDE=28;TAG='D1'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
if not os.path.exists('canon_backup_D1.db'): shutil.copy('canon.db','canon_backup_D1.db')
c=sqlite3.connect('canon.db');n=0;cnt={}
for f in ('d1/volk.py','d1/regio.py','d1/alg.py'): exec(open(f,encoding='utf-8').read())
CODES=lambda:{r[0] for r in c.execute('select code from canon')}
def ok(refs):
  cs=CODES(); return ';'.join(dict.fromkeys(r for r in refs.split(';') if r and r in cs))
def add(code,cat,ond,feit,reden,refs,soort='overig',**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  refs=ok(refs)
  if 'LUST' in str(kw.get('functie')) or '18+' in feit: feit=feit+GR
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1;cnt[soort]=cnt.get(soort,0)+1
# 0. EXTRA: handmatig labelen
HAND={'VERHAAL-fase6':'bio+metaal','TECH-GESCH-1':'bio','TECH-GESCH-2':'geen','TECH-GESCH-3':'bio','TECH-GESCH-5':'zegelsteen','TECH-GESCH-7':'bio','TECH-GESCH-9':'bio+gave',
'TECHNO-REGEL':'mengvorm','TECHNO-MIX':'mengvorm','TECHNO-TIJDLIJN':'mengvorm','TECHNO-SCHAAL':'mengvorm','TECHNO-VOLK-ves-lethi':'mengvorm','TECHNO-REGEL-V4':'mengvorm','TECHNO-MIX-V4':'mengvorm',
'VOOR-V4-aelthir-2':'bio','VOOR-V4-aelthir-3':'bio','VOOR-V4-karrûk-1':'geen','VOOR-V4-karrûk-3':'bio','VOOR-V4-karrûk-4':'zegelsteen','VOOR-V4-dhurn-1':'metaal','VOOR-V4-dhurn-2':'zegelsteen','VOOR-V4-dhurn-3':'zegelsteen',
'VOOR-V4-sael-mor-1':'bio','VOOR-V4-sael-mor-2':'geen','VOOR-V4-sael-mor-3':'bio','VOOR-V4-sael-mor-4':'geen','VOOR-V4-grauwen-1':'geen','VOOR-V4-grauwen-2':'geen','VOOR-V4-grauwen-3':'bio','VOOR-V4-grauwen-4':'bio',
'VOOR-V4-ishvar-1':'geen','VOOR-V4-ishvar-2':'geen','VOOR-V4-ishvar-3':'geen','VOOR-V4-ishvar-4':'metaal','VOOR-V4-vathren-1':'zegelsteen','VOOR-V4-vathren-2':'bio+zegelsteen','VOOR-V4-vathren-3':'zegelsteen','VOOR-V4-vathren-4':'zegelsteen',
'VOOR-V4-kluwer-2':'bio','VOOR-V4-kluwer-3':'bio','VOOR-V4-myrrhen-4':'bio','VOOR-V4-oevrin-1':'bio','VOOR-V4-oevrin-2':'bio','VOOR-V4-oevrin-3':'bio','VOOR-V4-oevrin-4':'geen',
'VOOR-V4-tharn-1':'geen','VOOR-V4-tharn-2':'geen','VOOR-V4-tharn-3':'geen','VOOR-V4-tharn-4':'geen','VOOR-V4-orrim-2':'zegelsteen','VOOR-V4-orrim-4':'geen','VOOR-V4-skerra-1':'bio','VOOR-V4-skerra-3':'geen','VOOR-V4-skerra-4':'bio',
'VOOR-V4-ves-lethi-1':'zegelsteen','VOOR-V4-ves-lethi-2':'bio','VOOR-V4-ves-lethi-3':'bio','VOOR-V4-ves-lethi-4':'bio','VOOR-V4-top-2':'geen','VOOR-V4-mid-3':'geen','VOOR-V4-mid-5':'gave','VOOR-V4-laag-4':'geen','VOOR-V4-laag-6':'gave','VOOR-V4-rebel-6':'geen','VOOR-V4-rebel-7':'gave'}
for k,t in HAND.items(): c.execute("update canon set techniek=? where code=?",(t,k))
# gewone personages niet op gave: alleen als ze zelf een gave dragen of gebruiken
pg=0
for code,feit,ond in c.execute("select code,feit,onderwerp from canon where categorie='Personage' and techniek='gave'").fetchall():
  t=(ond+' '+re.sub(r'Label: alle.*','',feit)).lower()
  if re.search(r'gaven-loze|gewone man|gewone mannen',t) and not re.search(r'is (een )?gaven-man',t) or not re.search(r'gaven-man|vonk|zaadkracht|gave (van|om|als)|zijn gave|haar gave|geladen|strijdontvangst|ontvangster|hoedster|zegel',t):
    c.execute("update canon set techniek='geen' where code=?",(code,));pg+=1
for k in ['KINK-ontlading-na-magie','RIT-stormontlading','HAND-stormontlading','RIT-volk-karruk']: c.execute("update canon set techniek='gave' where code=? and techniek='geen'",(k,))
# 1. Gaten techniek
for code,cat,o,f,fu,t,r in GAP: add(code,cat,o,f,'gat gave-techniek (17)',r,'gat',functie=fu,techniek=t)
VC=lambda v:'VOLK-aelthir-V5;VOLK-aelthir' if v=='aelthir' else f'VOLK-{v}'
for v,(nm,fn) in ZEG.items(): add(f'ZEG-D1-{v}','Voorwerp',nm,f'Zegelsteen-techniek van de {v}: {fn}. Prijs: zegelglas wordt gekocht van de Dhurn of gestolen uit de Orde; elk stuk is ooit een Orrim of een splinter van de Wieg geweest. Verlies: als het Zegel barst, dooft het. Haak (intrige): de Orde laat alle {nm.lower()}en registreren.','gat zegelsteen-techniek (17)',f'{VC(v)};TECHNO-zegelsteen;VOLK-orrim','gat',functie='INTR',techniek='zegelsteen')
for fa,(nm,fn) in MET.items(): add(f'MET-D1-{FASECODE[fa][5:]}','Techniek',nm,f'Vergeten metaal in fase {fa}: {fn}. Niemand weet dat het van het zaaischip Ysa komt; men gebruikt het als relikwie, niet als gewone techniek. Prijs: wie het aanraakt, raakt de Kluisraad. Haak (onthulling): het ding werkt nog.','gat metaal per fase (17)',f'{FASECODE[fa]};TECHNO-metaal;ORIGIN-1','gat',functie='THRL',techniek='metaal',jaar=FASEJAAR[fa],tijdperk=fa)
# 2. D1/D2 per volk
CAT={'eten':'Cultuur','drank':'Cultuur','geld':'Economie','ziekte':'Gezondheid','dood':'Religie','muziek':'Cultuur','spel':'Cultuur','humor':'Cultuur','taal':'Cultuur','feest':'Religie'}
SOORT={'eten':'D1 eten','drank':'D1 eten','geld':'D1 geld','ziekte':'D1 ziekte','dood':'D2 dood','muziek':'D2 muziek','spel':'D2 spel','humor':'D2 humor','taal':'D2 taal','feest':'D2 kalender/feest'}
for v,lst in V.items():
  vk=v.replace('û','u')
  for (o,titel,txt,fu,t) in lst:
    add(f'D1-{vk}-{o}',CAT[o],f'{titel} ({v})',txt,f'{SOORT[o]} per volk',f'{VC(v)};TECHNO-{t.split("+")[0]};DAG-TOP-{vk}-dag;WET-volk-{vk}',SOORT[o],functie=fu,techniek=t)
# 3. per regio
RC={'plant':'Planten en dieren','dier':'Planten en dieren','eten':'Cultuur','handel':'Economie','weer':'Land'}
RS={'plant':'D1 planten','dier':'D1 dieren','eten':'D1 eten','handel':'D1 geld','weer':'D2 weer'}
for rg,lst in R.items():
  for i,(s,nm,txt,fu,t) in enumerate(lst,1):
    if s=='dier': txt+=' (Dieren hier alleen als voedsel, werkdier, gevaar of symbool; nooit in een seksuele rol.)'
    add(f'D1-REG-{rg}-{i}',RC[s],f'{nm} ({rg})',txt,f'{RS[s]} per regio',f'REG-{rg};WET-reg-{rg};TECHNO-{t.split("+")[0]}',RS[s],functie=fu,techniek=t)
# 4. algemeen
SA={'Economie':'D1 geld','Gezondheid':'D1 ziekte'}
for code,cat,o,f,fu,t,r in A: add(code,cat,o,f,'D1/D2 algemeen',r,SA.get(cat,'D2 cultuur/hemel'),functie=fu,techniek=t)
# 5. Bestuur
for k,o,f,fu,t,r in B: add(f'BEST-{k}','Bestuur',o,f,'bestuur',r,'bestuur',functie=fu,techniek=t)
for v,f in VOLKBEST.items():
  vk=v.replace('û','u')
  add(f'BEST-volk-{vk}','Bestuur',f'Bestuur van de {v}',f+' Verhaalhaak (intrige): wie dit bestuur wil overnemen, moet de eigenaardigheid van het volk breken.','bestuur per volk',f'{VC(v)};WET-volk-{vk};BEST-raad-moeders','bestuur',functie='INTR',techniek='geen')
  add(f'BEST-orde-{vk}','Bestuur',f'De Orde en de {v}',f'Verhouding van de {v} tot Orde en Raad der Moeders: de Orde erkent hun bestuur alleen zolang ze leveren wat zij nodig heeft (zie functie in {VC(v).split(";")[0]}). Prijs: een Orde-gezante per volk die hun registers bijhoudt. Haak (intrige): de gezante bij de {v} is overgelopen.','bestuur volk-Orde',f'{VC(v)};BEST-orde-hoofd;BEST-volk-{vk}','bestuur',functie='INTR',techniek='geen')
for rg,f in REGBEST.items(): add(f'BEST-reg-{rg}','Bestuur',f'Bestuur van {rg}',f+' Haak (intrige): wie de belasting hier int, bepaalt de trouw van de regio.',f'bestuur per regio',f'REG-{rg};WET-reg-{rg};BEST-belasting','bestuur',functie='INTR',techniek='geen')
c.commit()
# 6. CROSSLINKS
nl=0
def link(a,b):
  global nl
  if a==b: return
  r=c.execute("select verwijst_naar from canon where code=?",(a,)).fetchone()
  if not r or not c.execute("select 1 from canon where code=?",(b,)).fetchone(): return
  rs=[x for x in (r[0] or '').split(';') if x]
  if b in rs: return
  rs.append(b); c.execute("update canon set verwijst_naar=? where code=?",(';'.join(rs),a)); nl+=1
VN={'aelthir':'aelthir','karrûk':'karrûk','karruk':'karrûk','dhurn':'dhurn','sael-mor':'sael-mor','grauwen':'grauwen','grauwe':'grauwen','ishvar':'ishvar','vathren':'vathren','kluwer':'kluwer','myrrhen':'myrrhen','oevrin':'oevrin','tharn':'tharn','orrim':'orrim','skerra':'skerra','ves-lethi':'ves-lethi'}
STAD={'saelith':'STAD-saelith','orvane':'STAD-orvane','lisk':'STAD-lisk','hallowyn':'STAD-hallowyn','kaldrun':'STAD-kaldrun','ijsgraf':'STAD-ijsgraf','brakhaven':'STAD-brakhaven','isla mirre':'STAD-isla-mirre','tuaro':'STAD-tuaro','qesh':'STAD-qesh','hoornburg':'STAD-kharvos-hoornburg','zoutklooster':'STAD-stille-zoutklooster'}
FASE=[('voortijd',None),('overvloed','FASE-overvloed'),('vonk','FASE-vonk'),('brand','FASE-brand'),('noodtoestand','FASE-noodtoestand'),('ontvangst','FASE-ontvangst'),('markt','FASE-markt'),('barsten','FASE-barsten')]
TC={'Voorwerp','Techniek','Dagelijks leven','Rebellen','Lichaam en vervorming','Rituelen','Extreme rituelen','Economie','Gezondheid','Cultuur','Bestuur','Planten en dieren'}
rows=c.execute("select code,categorie,feit,tijdperk,techniek,status from canon where status not like '%vervallen%'").fetchall()
for code,cat,feit,tp,te,st in rows:
  if code.startswith(('STAD-','FASE-','VOLK-','TECHNO-gave','TECHNO-metaal','TECHNO-bio','TECHNO-zegelsteen')) and code.count('-')<=1: continue
  f=(feit or '').lower()
  m=re.search(r'volk: ([a-zûè\-]+)',f)
  if m and m.group(1) in VN:
    v=VN[m.group(1)]; link(code,'VOLK-aelthir-V5' if v=='aelthir' else f'VOLK-{v}')
  for nm,sc in STAD.items():
    if re.search(r'\b'+nm+r'\b',f) and sc!=code: link(code,sc)
  if tp:
    for k,fc in FASE:
      if fc and k in tp.lower(): link(code,fc);break
  if te and te not in('geen','mengvorm') and cat in TC:
    for t in te.split('+'): link(code,f'TECHNO-{t}')
  if te=='metaal' and cat in TC: link(code,'ORIGIN-1')
# nieuwe rijen onderling: zelfde volk/regio aan elkaar
for v in V:
  vk=v.replace('û','u'); ks=[f'D1-{vk}-{o}' for o in CAT]
  pairs=[('eten','drank'),('drank','feest'),('ziekte','dood'),('muziek','feest'),('geld','eten'),('humor','spel'),('taal','humor')]
  for a,b in pairs: link(f'D1-{vk}-{a}',f'D1-{vk}-{b}')
  link(f'D1-{vk}-geld',f'BEST-volk-{vk}')
  link(f'BEST-volk-{vk}',f'D1-{vk}-geld')
  link(f'D1-{vk}-ziekte','GENEES-heelsters')
  link(f'D1-{vk}-feest','KAL-feestkalender')
  link(f'D1-{vk}-taal','SCHELD-algemeen')
  link(f'D1-{vk}-dood','DOOD-orde-asgang')
for rg in R:
  for i in range(1,len(R[rg])+1): link(f'D1-REG-{rg}-{i}',f'BEST-reg-{rg}')
  link(f'BEST-reg-{rg}',f'D1-REG-{rg}-8')
# dekking: rijen zonder enige geldige verbinding
import crosslinks_lib
rows_,codes,out,inn,broken=crosslinks_lib.graaf(c)
los=[k for k in codes if not out[k] and not inn[k]]
info={r[0]:r for r in c.execute("select code,categorie,tijdperk from canon")}
HUB={'Personage':'PER-liora','Geschiedenis':'TIJD-V4-fasejaren','Verhaal':'LIJN-overzicht','Bestuur':'BEST-raad-moeders'}
for k in los:
  _,cat,tp=info[k]; target=None
  if tp:
    for kk,fc in FASE:
      if fc and kk in tp.lower(): target=fc
  link(k,target or HUB.get(cat,'MACHT-evenwicht'))
rows_,codes,out,inn,broken2=crosslinks_lib.graaf(c)
los2=[k for k in codes if not out[k] and not inn[k]]
# 7. wrijvingen, vragen, logboek
def wrij(code,t,d,b,ty):
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone(): c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,ty,'open',code,d))
def vraag(code,v,w):
  if not c.execute("select 1 from open_vraag where code=?",(code,)).fetchone(): c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,?,?,?)",(v,w,'open',code,''))
wrij('WRIJ-D1-1','Jaartelling 13 maanden vs. oudere kalenderrijen','KAL-jaartelling;SYS-levenscyclus-kalender','KAL-jaartelling voert 13 maanden in; oudere kalenderrijen noemen geen aantal. Voorstel: 13 maanden aanhouden.','continuïteit')
wrij('WRIJ-D1-2','Kleine Maan nieuw aan de hemel','HEMEL-tweede-maan;KAART-seizoenen','Eerdere rijen noemen één maan. Voorstel: de Kleine Maan is alleen zichtbaar bij heldere nachten, mensen noemen hem "de splinter".','continuïteit')
wrij('WRIJ-D1-3','Zaadas in brood (Orde-asgang) en Aelthir-verbod op vlees van sprekenden','DOOD-orde-asgang;D1-aelthir-eten','Aelthir weigeren tempelbrood; past, maar maakt hen verdacht bij de Orde. Bewust als verhaalbron.','bron')
vraag('VRAAG-D1-1','Is de bewegende ster (het zaaischip) bewoond, en door wie?','Bepaalt de interstellaire laag en de finale.')
vraag('VRAAG-D1-2','Wie zit er in de Kluisraad, en weet Ithrael van de kluisgeneeskunde?','Sleutel voor intrige in de Orde.')
vraag('VRAAG-D1-3','Mag de Mannenraad ooit echte macht krijgen?','Bepaalt de politieke boog van de mannen.')
if not c.execute("select 1 from logboek where wat like 'Ronde D1:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",(f'Ronde D1: dagelijks leven (eten, drank, geld, ziekte, dood, muziek, spel, humor, taal, feesten per volk; planten, dieren, eten, handel, weer per regio), hemel en kalender, bestuur, techniek-gaten gevuld, handlabels, {nl} nieuwe crosslinks, bijbel 18_crosslinks.md, export toont techniek.',))
c.commit()
best=c.execute("select count(*) from canon where code like 'BEST-%'").fetchone()[0]
json.dump({'nieuw':n,'per_soort':cnt,'crosslinks':nl,'personages_van_gave_naar_geen':pg,'los_voor':len(los),'los_na':len(los2),'kapotte_verwijzingen':broken2,'bestuur':best},open('d1/rapport.json','w'),ensure_ascii=False,indent=1)
print(open('d1/rapport.json').read())
