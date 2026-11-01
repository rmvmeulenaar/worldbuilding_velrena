# Ronde V5: drie beslissingen, Hesk-namen, Ileth, kolom techniek (idempotent)
import sqlite3,shutil,os,re,json
RONDE=27;TAG='V5'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
if not os.path.exists('canon_backup_V5.db'): shutil.copy('canon.db','canon_backup_V5.db')
c=sqlite3.connect('canon.db');n=0
if 'techniek' not in [r[1] for r in c.execute('pragma table_info(canon)')]: c.execute('alter table canon add column techniek text')
def add(code,cat,ond,feit,reden,refs,**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1
def vervang(old,new,feit,ond=None):
  r=c.execute("select categorie,onderwerp,verwijst_naar,jaar,tijdperk,functie from canon where code=?",(old,)).fetchone()
  if not r: return
  add(new,r[0],ond or r[1],feit,f'vervangt {old}',';'.join(x for x in [old,r[2] or ''] if x),jaar=r[3],tijdperk=r[4],functie=r[5])
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status='voorlopig'",(f' [Ronde {TAG}: vervangen door {new}]',old))
F=lambda code: c.execute("select feit from canon where code=?",(code,)).fetchone()[0]
# 1a Ysa
add('BESLUIT-V5-ysa','Geschiedenis','Besluit: Ysa Maren beval de Muiterij (blijft)','Besluit (als ingenieur, voorlopig): de draai blijft. Ysa Maren beval de Rekenaar te rantsoeneren en wiste zijn geheugen. Tragisch motief: haar simulaties toonden dat de scheepskernen binnen twee generaties zouden opraken en dat de Rekenaar dan zelf de helft zou "afschakelen" om de machines te laten draaien; ze offerde een derde nu om de machines te stoppen en de rest te redden, en kon de stemming alleen winnen met bewijs dat machines muiten. Ze geloofde het, en ze had half gelijk. Kwaliteit voor de verhalen: de godin wordt geen schurk maar een spiegel van de Orde (iemand die lichamen opoffert voor het voortbestaan); elke Orde-figuur die zegt "het is voor ieders bestwil" echoot haar; de onthulling breekt het geloof niet goedkoop maar dwingt elk personage te kiezen of het doel de prijs waard was.'+GR,'beslissing VRAAG-069','ORIGIN-WAAROM-11;PER-v4-ysa-maren;ORIGIN-3',jaar=-1240,tijdperk='0 Voortijd')
add('ORIGIN-onthulplan-ysa','Verhaal','Onthulplan: de schuld van Ysa','Boek 1: liederen noemen de Muiterij "de koude gekte"; een Stille Zuster bezit een plaat met een vrouwenstem in de dode taal. Boek 2: Thalen (in de Sterrensteen) zegt "zij koos ons voor ons", nog onbegrijpelijk. Boek 3: de logboekplaat (TECH-ITEM-V4-metaal-7) wordt vertaald: het bevel, met haar naam. Boek 4: haar eigen dagboek in een Aelthir-geurarchief geeft het motief (de simulaties): de lezer moet haar tegelijk haten en begrijpen. Finale: Liora staat voor dezelfde keuze als Ysa.'+GR,'onthulplan','BESLUIT-V5-ysa;ORIGIN-onthulplan')
# 1b Aelthir
add('BESLUIT-V5-aelthir','Geschiedenis','Besluit: Aelthir zijn aangepaste kolonisten','Besluit (voorlopig): de Aelthir zijn het eerste experiment van de Makers (ca. -1230): kolonisten die vrijwillig hun lichaam lieten herschrijven om lang te leven en het geheugen van de kolonie te dragen, omdat schrift over machines verboden werd (ORIGIN-7). Prijs: bijna geen kinderen, doorschijnende huid, gevoel dat wegvalt. Levensduur: ca. 900 jaar (niet 400); de oude 400 was wat mensen dachten, omdat Aelthir zich na 400 jaar terugtrekken in de mist. Inheems blijven: Oevrin, Tharn, Kluwers en Orrim (hun rijen noemen ze al "ouder dan de mensen" en de Orrim-lichamen in het Zegel vragen om een volk dat hier al was). Kwaliteit: de Aelthir worden het levende bewijs van de Makers en verklaren waarom zij het geheim van het Zegel konden verkopen; de inheemse volken krijgen een eigen grief (zij werden gebruikt door gasten).'+GR,'beslissing VRAAG-070 en WRIJ-114','VOLK-aelthir;ORIGIN-7;VOLK-oevrin;VOLK-tharn;VOLK-kluwer;VOLK-orrim',jaar=-1230,tijdperk='0 Voortijd')
f=F('VOLK-aelthir').replace('Ouder dan de mensen: een volk dat al bestond toen de Sterrensteen viel; de steen kortte hun leven niet maar hun vruchtbaarheid','Aangepaste kolonisten: het eerste experiment van de Makers van het zaaischip Ysa (ca. -1230), herschreven om het geheugen van de kolonie te dragen; ze bestonden al toen de Sterrensteen viel, en de steen kortte hun vruchtbaarheid nog verder (BESLUIT-V5-aelthir)').replace('Ze leven 400 jaar','Ze leven ca. 900 jaar (na 400 jaar trekken ze zich terug in de mist, daarom dachten mensen dat ze 400 werden)').replace('na 300 jaar verliezen ze gevoel','na 600 jaar verliezen ze gevoel')
vervang('VOLK-aelthir','VOLK-aelthir-V5',f)
vervang('PER-aelthir-schurk-ileth','PER-aelthir-schurk-ileth-V5',F('PER-aelthir-schurk-ileth').replace('Fase: 4 Noodtoestand.','Fase: 4 Noodtoestand (geboren ca. -60, in 801 ca. 860 jaar oud, binnen de Aelthir-levensduur van ca. 900 jaar).'))
for vo in ['VOLK-oevrin','VOLK-tharn','VOLK-kluwer','VOLK-orrim']:
  r=c.execute("select verwijst_naar from canon where code=?",(vo,)).fetchone()
  if r and 'BESLUIT-V5-aelthir' not in (r[0] or ''): c.execute("update canon set verwijst_naar=? where code=?",(';'.join(x for x in [r[0] or '','BESLUIT-V5-aelthir'] if x),vo))
# 1c Thalen
add('BESLUIT-V5-thalen','Geschiedenis','Besluit: Thalen wil het Zegel herstellen','Besluit (voorlopig): Thalen Orr wil het Zegel HERSTELLEN: de gebroken instemmingssleutel (Stemklok) terugbrengen, zodat de kracht weer vraagt of iemand wil. De prijs: het Zegel wordt gedragen door de Dochters en Orrim-lichamen; herstellen betekent hen eruit halen, en dat is opofferen (ze sterven) of verlossen (ze worden vrij, maar het Zegel moet nieuwe dragers krijgen die wél instemmen). BREKEN is het plan van de rebellen (REBEL-rijen): alle vonkcellen komen vrij, zaadkracht en orde storten in, de verhouding 1 op 100 valt weg maar ook alle gaven, met hongersnood en oorlog. Kwaliteit: geen goed-tegen-kwaad-finale maar twee kanten met elk een echte prijs; Thalen is een bondgenoot met een eigen agenda (hij wil ook Ysa\'s schuld uitwissen), en de keuze komt bij de lezersfiguren te liggen.'+GR,'beslissing VRAAG-071','ORIGIN-WAAROM-12;PER-v4-thalen-orr;ORIGIN-10',functie='THRL')
HAKEN=[('INTR','Wie draagt het nieuwe Zegel?','Thalen heeft vrijwillige dragers nodig; de Orde biedt veroordeelden aan als "vrijwilligers", de Stille Zusters ontdekken het.'),
('ROM','De Dochter in de steen','Een Stille Zuster wordt verliefd op de stem van een Dochter in het Zegel; verlossen betekent dat ze haar eindelijk kan aanraken, of dat ze sterft.'),
('THRL','De klok van de barst','De Sterrensteen barst verder; herstellen kan alleen vóór de laatste barst, breken gebeurt dan vanzelf. Beide kampen racen.'),
('INTR','De rebellen kopen Orrim','Rebellen bieden de Orrim hun voorouders terug als ze helpen breken; de Orrim moeten kiezen tussen hun doden en de wereld.'),
('THRL','Thalens ware agenda','Herstellen wist ook het logboek met Ysa\'s bevel; wie dat ontdekt, weet dat Thalen haar wil beschermen.'),
('LUST','De eerste vraag','Bij een proef met de herstelde sleutel vraagt de kracht voor het eerst in 800 jaar instemming; twee volwassen geliefden ervaren wat seks met kracht kan zijn als beiden echt ja zeggen, en de Orde ziet haar macht verdampen.')]
for i,(fu,o,t) in enumerate(HAKEN,1): add(f'HAAK-V5-zegel-{i}','Verhaal',f'Haak herstellen/breken: {o}',t+GR,'verhaalhaak zegelconflict','BESLUIT-V5-thalen',functie=fu)
# Hesk
vervang('PER-nood-grauwen','PER-nood-grauwen-V5',F('PER-nood-grauwen').replace('Hesk de Eerste Grauwe','Grem de Eerste Grauwe'),'Grem de Eerste Grauwe')
vervang('PER-skerra-schurk-hesk','PER-skerra-schurk-skell',F('PER-skerra-schurk-hesk').replace('Hesk Klifmeester','Skell Klifmeester'),'Skell Klifmeester')
# vragen/wrijvingen sluiten
for q,a in {'VRAAG-069':'Ja, blijft; tragisch motief en onthulplan in BESLUIT-V5-ysa en ORIGIN-onthulplan-ysa.','VRAAG-070':'Aangepaste kolonisten (eerste experiment); Oevrin, Tharn, Kluwers en Orrim zijn inheems. Zie BESLUIT-V5-aelthir.','VRAAG-071':'Herstellen; breken is het rebellenplan. Zie BESLUIT-V5-thalen en HAAK-V5-zegel-1..6.'}.items():
  c.execute("update open_vraag set status='beantwoord (voorlopig)', antwoord=? where code=? and status='open'",(a+' [Ronde V5]',q))
for w,a in {'WRIJ-114':'Aelthir zijn aangepaste kolonisten van de Makers (BESLUIT-V5-aelthir).','WRIJ-108':'Aelthir leven ca. 900 jaar; Ileth geboren ca. -60, ca. 860 in 801 (PER-aelthir-schurk-ileth-V5).','WRIJ-086':'Met ca. 900 jaar levensduur is Vaelorn (600) geen uitzondering.','WRIJ-113':'Alleen de kweekster blijft Hesk; de Grauwe heet nu Grem, de Skerra Skell Klifmeester.'}.items():
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and status='open'",(f' [Opgelost V5: {a}]',w))
c.execute("update wrijving set beschrijving=beschrijving||' [V5: motief vastgelegd in BESLUIT-V5-ysa; blijft bewuste verhaalbron.]' where code=(select code from wrijving where titel='Godin Ysa als moordenares') and beschrijving not like '%V5:%'")
# 2 techniek
P={'gave':r'\bgaven?\b|gaven-|\bvonk|geladen|zaadkracht|eedmes|echoring|schutsteen|handlinnen',
'metaal':r'metaal|metalen|machine|\bkluis|kluizen|kernen\b|scheepskern|energiekern|wiegkast|rekenaar|lichtlans|vuurbuis|kaartplaat|stemschijf|landers?\b|zaaischip',
'bio':r'\bvlees|\bbloed\b|schimmel|\bbot(ten)?\b|chitine|weefsel|kweek|\bstallen?\b|leegteworm|wormen|zwam|spore|\bhars\b|levend schip|melk',
'zegelsteen':r'zegelglas|sterrensteen|zegelsteen|orrim-steen|kristal|gloedsieraad|\bwieg\b|stemklok'}
TECHCAT={'Techniek','Voorwerp','Dagelijks leven','Rituelen','Extreme rituelen','Rituele handelingen','Ritueel systeem','Economie','Gezondheid','Mode en kleding','Lichaam en vervorming','Magie','Rebellen'}
cnt={};onduidelijk=[]
for id_,code,cat,ond,feit in c.execute("select id,code,categorie,onderwerp,feit from canon").fetchall():
  t=None;m=re.match(r'(?:TECHNO|TECH-ITEM(?:-V4)?|OORSPRONG)-(gave|metaal|bio|zegelsteen)',code or '')
  if m: t=m.group(1)
  else:
    m=re.search(r'Techniek: (gave|metaal|bio|zegelsteen)',feit or '')
    if m: t=m.group(1)
  if not t:
    txt=((ond or '')+' '+re.sub(r'Label: alle.*','',feit or '')).lower()
    s={k:len(re.findall(p,txt)) for k,p in P.items()}
    drempel=1 if cat in TECHCAT else 2
    hit=sorted([k for k in s if s[k]>=drempel],key=lambda k:-s[k])
    if not hit: t='geen'
    elif len(hit)==1: t=hit[0]
    else:
      t='+'.join(sorted(hit[:2]))
      if len(hit)>2: onduidelijk.append((code,'3+ technieken: '+','.join(hit)))
    if t=='geen' and cat in ('Techniek','Voorwerp'): onduidelijk.append((code,'techcategorie zonder trefwoord'))
  c.execute("update canon set techniek=? where id=?",(t,id_)); cnt[t]=cnt.get(t,0)+1
json.dump({'telling':cnt,'onduidelijk':onduidelijk},open('v5/techniek_rapport.json','w'),ensure_ascii=False,indent=1)
if not c.execute("select 1 from logboek where wat like 'Ronde V5:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",('Ronde V5: drie beslissingen (Ysa beval de Muiterij blijft met tragisch motief; Aelthir aangepaste kolonisten, ca. 900 jaar, Oevrin/Tharn/Kluwers/Orrim inheems; Thalen wil herstellen, rebellen willen breken, 6 haken), Hesk-namen (Grem, Skell), WRIJ-086/108/113/114 opgelost, VRAAG-069/070/071 beantwoord, kolom techniek toegevoegd en alle rijen gelabeld, bijbel 17_techniek-overzicht.md.',))
c.commit();print('nieuw:',n);print(cnt);print('onduidelijk:',len(onduidelijk))
c.execute("update canon set feit=replace(feit,'Hesk Klifmeester','Skell Klifmeester'), reden=reden||' [Ronde V5: naam Hesk Klifmeester -> Skell Klifmeester]' where status='voorlopig' and feit like '%Hesk Klifmeester%'")
c.execute("update canon set feit=replace(feit,'Hesk de Eerste Grauwe','Grem de Eerste Grauwe'), reden=reden||' [Ronde V5: naam -> Grem]' where status='voorlopig' and feit like '%Hesk de Eerste Grauwe%'")
c.commit()
