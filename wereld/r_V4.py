# Ronde V4: oorsprong (Makers), tijdlijn, voorwerpen, dagelijks leven, rebellen (idempotent)
import sqlite3,shutil,os
RONDE=26;TAG='V4'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
if not os.path.exists('canon_backup_V4.db'): shutil.copy('canon.db','canon_backup_V4.db')
c=sqlite3.connect('canon.db');n=0;vv=[]
for f in ('v4/data.py','v4/data2.py','v4/data3.py'): exec(open(f,encoding='utf-8').read())
def add(code,cat,ond,feit,reden,refs,**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  refs=';'.join(r for r in refs.split(';') if r)
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1
def vervang(old,new,feit=None,**kw):
  r=c.execute("select categorie,onderwerp,feit,hangt_samen_met,verwijst_naar,jaar,tijdperk,functie from canon where code=?",(old,)).fetchone()
  if not r: return
  add(new,r[0],r[1],feit or r[2],f'vervangt {old}',';'.join(x for x in [old,r[4] or ''] if x),jaar=kw.get('jaar',r[5]),tijdperk=kw.get('tijdperk',r[6]),functie=r[7])
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status='voorlopig'",(f' [Ronde {TAG}: vervangen door {new}]',old)); vv.append(old)
# 1. Oorsprong
for code,nm,rol,txt in PERS: add('PER-v4-'+code,'Personage',nm,f'Naam: {nm}. Volk: mens (Maker, kolonist van het zaaischip Ysa). Fase: 0 Voortijd, jaar -1240. Rol: {rol}. {txt}'+GR,'Makers','ORIGIN-4',jaar=-1240,tijdperk='0 Voortijd')
for s,j,t,o,f,r in ORIGIN: add('ORIGIN-'+s,'Geschiedenis',f'Oorsprong {s}: {o}',f+GR,'oorsprongsketen (Makers + verborgen sf)',f'{"ORIGIN-"+str(int(s)-1) if s!="1" else ""};{r}',jaar=j,tijdperk=t)
for s,o,f,r in WAAROM: add('ORIGIN-WAAROM-'+s,'Geschiedenis',f'Waarom het lichaam {s}: {o}',f+GR,'mini-saga van de Makers',f'ORIGIN-4;{r}',jaar=-1238,tijdperk='0 Voortijd',functie=('ROM' if s=='6' else 'INTR' if s in '37' else 'THRL' if s in ('5','11','12') else None))
add('HAAK-v4-stemklok','Verhaal','Thriller-haak: de omweg van Hesta','Wie in 801 de omweg van Hesta Kael in de Wieg vindt, kan het Zegel weer laten vragen om toestemming, of het voorgoed doven. Ithrael, Morvane-ir en de Stille Pen jagen op hetzelfde logboek.'+GR,'verhaalhaak','ORIGIN-WAAROM-9;ORIGIN-WAAROM-5',functie='THRL')
add('ORIGIN-onthulplan','Verhaal','Onthulplan oorsprong',ONTHUL,'wat de lezer wanneer ontdekt','ORIGIN-1;ORIGIN-WAAROM-11;ORIGIN-WAAROM-12')
add('ORIGIN-keuze','Geschiedenis','Waarom deze oorsprong gekozen is','Gekozen: één zaaischip (Ysa) met Makers die bewust het lichaam kozen (besluit Rogier). Reden: verklaart in één keten de twee inslagplaatsen, de koude huizen, de Sprekende Kluis (Dhurn-handen), de Wiegkast en 1 op 100 als ontworpen getal, waarom zaad kracht draagt, waarom de godin Ysa heet en waarom toestemming de horror is. Geen A/B-variant nodig. Hint blijft voorlopig.','beslissing V4','ORIGIN-1;ORIGIN-WAAROM-8;ORIGIN-WAAROM-9')
add('GENRE-wet2-V4','Genre','Genre-wet 2: de Makers kozen het lichaam','Wet 2 (V4): "De Makers kozen het lichaam, en het lichaam is de prijs." Alle levende techniek is een bewuste ontwerpkeuze van de wetenschappers van het zaaischip; de hoog ontwikkelde machines zijn niet verboden door de natuur maar vergeten, en wat er nog op draait (kluizen, kernen, Wiegkast, Sterrensteen) wordt met lichamen betaald. Reden: past bij Rogiers besluit en houdt de V3-vondst "prijs" vast.','vervangt GENRE-wet2-V3','GENRE-zegelpunk;ORIGIN-4')
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde V4: vervangen door GENRE-wet2-V4]' where code='GENRE-wet2-V3' and status='voorlopig'")
vervang('TECHNO-REGEL','TECHNO-REGEL-V4','TECHNO-REGEL (V4): vier technologieën. Bio (vlees, bloed, schimmel, bot) en gave zijn het ontwerp van de Makers; zegelsteen is de gevallen scheepskern (Wieg); metaal en machine zijn hoog ontwikkelde, vergeten techniek van het zaaischip Ysa die deels nog draait (kluizen, kernen, Wiegkast, Sterrensteen). Geen regel "alleen lichamen": het lichaam is gekozen, niet gedwongen.')
vervang('TECHNO-MIX','TECHNO-MIX-V4',c.execute("select feit from canon where code='TECHNO-MIX'").fetchone()[0]+' (V4) Elke mengvorm is een terugkeer naar wat de Makers scheidden: vlees met machine wekt de oude Koudhand-ruzie, en zegelsteen met gave is de Wieg zelf in het klein.')
vervang('TECH-GESCH-12','TECH-GESCH-12-V4','Velmara: lichaam en materiaal, omdat de Makers dat kozen (ORIGIN-4). Daaronder: hoog ontwikkelde, vergeten machinetechniek van het zaaischip Ysa die nog draait. Buiten (andere zaaischepen en werelden): machinaal.')
vervang('TECH-GESCH-10','TECH-GESCH-10-V4','Biopunk-wapens: brandader, steenpijl; daarnaast machinale resten (vuurbuizen, lichtlans) in Orde-kluizen, van het zaaischip Ysa.')
add('TECH-GESCH-0','Techniek','Techniek in de Voortijd','Zaaischip Ysa: machines, kernen, landers, Rekenaar. Na de Muiterij en de stemming (ORIGIN-4) wordt alles biologisch ontworpen; machinekennis wordt verboden en vergeten (ORIGIN-7).','techniekgeschiedenis vanaf de oorsprong','ORIGIN-4;ORIGIN-7;TECH-GESCH-1',jaar=-1238,tijdperk='0 Voortijd')
for code in ['OORSPRONG-metaal-1','OORSPRONG-metaal-5','OORSPRONG-metaal-6','OORSPRONG-metaal-8','OORSPRONG-zegelsteen-1','OORSPRONG-zegelsteen-3','OORSPRONG-bio-8','TECHNO-metaal-genees','GEB-sterrensteen-inslag','PLEK-HEILIG-inslagkrater','MAGIE-GESCH-12','GOD-sterrensteen-heilig']:
  r=c.execute("select verwijst_naar from canon where code=?",(code,)).fetchone()
  if r and 'ORIGIN' not in (r[0] or ''): c.execute("update canon set verwijst_naar=? where code=?",(';'.join(x for x in [r[0] or '','ORIGIN-1'] if x),code))
# 2. Tijdlijn
FIX=[('OORSPRONG-gave-4',90,'4 Noodtoestand'),('OORSPRONG-gave-5',100,'4 Noodtoestand'),('OORSPRONG-metaal-5',90,'4 Noodtoestand'),('OORSPRONG-bio-3',33,'4 Noodtoestand'),('OORSPRONG-zegelsteen-4',205,'5 Ontvangst'),('OORSPRONG-zegelsteen-1',-480,'1 Overvloed'),('OORSPRONG-bio-6',338,'6 Markt'),('OORSPRONG-zegelsteen-2',-30,'3 Brand'),('MAGIE-GESCH-1',-478,'1 Overvloed')]
for code,j,t in FIX: vervang(code,code+'-V4',jaar=j,tijdperk=t)
add('TIJD-V4-fasejaren','Geschiedenis','Tijdlijn V4: fasejaren rechtgezet','Bron van waarheid: FASE-rijen (1: -600..-150, 2: -150..-40, 3: -40..0, 4: 0..130, 5: 130..340, 6: 340..720, 7: 720..801). Het Zegel valt op jaar 0 (GEB-zegel-gelegd), dus OORSPRONG-zegelsteen-3 blijft 0. De V2-rijen op jaar 60 zijn een middenjaar van fase 4 en kloppen. Rijen die jaar 0 kregen maar later gebeuren, kregen een eigen jaar (90, 100, 33, 205). Ook rechtgezet: Sterrensteen valt in -480 (niet -100), de Pest-stam in 338 (niet 500), de splinterhakkers in -30, de vroege Vonk in -478 (steenkoorts) en niet bij Orric (-150). Myrrhen-pest 470 = de tweede Pest (GEB-r10-tweede-pest), geen botsing. Nieuwe fase 0 Voortijd: ca. -1250 tot -600.','tijdlijncontrole','FASE-noodtoestand;GEB-zegel-gelegd;ORIGIN-1')
# 3. Voorwerpen
for k,lst in ITEMS.items():
  for i,(nm,s,f,m,p,r,h,z) in enumerate(lst,1):
    add(f'TECH-ITEM-V4-{k}-{i}','Techniek',nm,f'Voorwerp ({k}, {s}). Functie: {f}. Maker: {m}. Prijs: {p}. Risico: {r}. Verhaalhaak: {h}. Zintuig: {z}.'+(GR if s=='erotisch' else ''),'voorwerp per technologie',f'TECHNO-{k}',functie=('LUST' if s=='erotisch' else None))
for v,lst in VOLKITEMS.items():
  for i,(nm,s,f,p,r,h,z) in enumerate(lst,1):
    add(f'VOOR-V4-{v}-{i}','Voorwerp',nm,f'Voorwerp van {v} ({s}). Functie: {f}. Maker: {v}. Prijs: {p}. Risico: {r}. Verhaalhaak: {h}. Zintuig: {z}.'+(GR if s=='erotisch' else ''),'voorwerp per volk',f'VOLK-{v}',functie=('LUST' if s=='erotisch' else None))
for kl,lst in KLASSE.items():
  for i,(nm,s,f,t,p,r,h,z) in enumerate(lst,1):
    add(f'VOOR-V4-{kl}-{i}','Voorwerp',nm,f'Voorwerp van klasse {kl} ({s}). Functie: {f}. Techniek: {t}. Prijs: {p}. Risico: {r}. Verhaalhaak: {h}. Zintuig: {z}.'+(GR if s=='erotisch' else ''),'voorwerp per klasse','DAG-KLASSE-'+kl,functie=('LUST' if s=='erotisch' else None))
# 4. Dagelijks leven
KL={'top':'Heersers en hoven: dag in rituelen, eten met proefsters, intimiteit als politiek.','mid':'Middenklasse en ambachten: gilden, gunstbrieven als loon, angst om te dalen.','laag':'Lagere klassen: mijnen, stallen, havens, rand; lichaam als arbeid.','sub':'Subculturen: wie buiten de klassen leeft om lust, kunst, geloof of vrijheid.','rebel':'Anarchisten en rebellen: wie het systeem wil breken.'}
for k,t in KL.items(): add('DAG-KLASSE-'+k,'Dagelijks leven',f'Klasse: {k}',t+GR,'klassenoverzicht','DAG-werk')
for code,nm,r,d,i in TOP:
  add(f'DAG-TOP-{code}-dag','Dagelijks leven',f'{nm}: dag en rituelen',d+GR,'dagelijks leven heersers',f'DAG-KLASSE-top;{r}')
  add(f'DAG-TOP-{code}-geheim','Dagelijks leven',f'{nm}: intimiteit, rivaliteit, geheim',i+GR,'dagelijks leven heersers',f'DAG-TOP-{code}-dag;{r}')
for code,nm,t in MID: add('DAG-MID-'+code,'Dagelijks leven',nm,t+GR,'middenklasse','DAG-KLASSE-mid')
for code,nm,t in LAAG: add('DAG-LAAG-'+code,'Dagelijks leven',nm,t+GR,'lagere klassen','DAG-KLASSE-laag')
for code,nm,t in SUB: add('DAG-SUB-'+code,'Dagelijks leven',nm,t+GR,'subcultuur','DAG-KLASSE-sub')
for code,nm,t in REBEL: add('REBEL-'+code,'Rebellen',nm,t+GR,'rebellengroep','DAG-KLASSE-rebel',functie='INTR')
# 5. Wrijvingen en vragen
for q,a in ANTW.items():
  c.execute("update open_vraag set status='beantwoord (voorlopig)', antwoord=? where code=? and status='open'",(a+' [Ronde V4]',q))
c.execute("update wrijving set beschrijving=beschrijving||' [Herzien V4: machines zijn vergeten techniek van de Makers; wet 2 is nu GENRE-wet2-V4. Blijft opgelost.]' where code='WRIJ-107' and beschrijving not like '%Herzien V4%'")
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Opgelost V4: 340 = eerste Pest, 470 = tweede Pest; Myrrhen ontstaan na de tweede. Zie TIJD-V4-fasejaren]' where code='WRIJ-053' and status='open'")
def wrij(t,d,b,ty):
  if c.execute("select 1 from wrijving where titel=?",(t,)).fetchone(): return
  m=max(int(r[0][5:]) for r in c.execute("select code from wrijving where code like 'WRIJ-%'"))
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,'open',?,?)",(t,d,b,ty,f'WRIJ-{m+1:03d}',d.replace('; ',';')))
def vraag(v,w,r):
  if c.execute("select 1 from open_vraag where vraag=?",(v,)).fetchone(): return
  m=max(int(x[0][6:]) for x in c.execute("select code from open_vraag where code like 'VRAAG-%'"))
  c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,f'VRAAG-{m+1:03d}',r))
wrij('Twee personages heten Hesk','PER-hesk-kweker; PER-nood-grauwen; PER-skerra-schurk-hesk','Drie Hesks (kweekster, Grauwe, Skerra) kunnen lezers verwarren; voorstel: één hernoemen.','naamgeving')
wrij('Aelthir bestonden al vóór de mensen?','VOLK-aelthir; ORIGIN-1','Als de mensen van het zaaischip komen, zijn de Aelthir dan inheems of eerder aangepaste kolonisten?','oorsprong')
wrij('Godin Ysa als moordenares','ORIGIN-WAAROM-11; GELOOF-officieel-vs-echt','De verborgen waarheid maakt de godin schuldig; dat raakt het hele geloof. Bewust gekozen als late draai.','bron van verhalen')
vraag('Moet de draai "Ysa beval de Muiterij" in de reeks, of is Ysa onschuldig?','Grootste draai van de oorsprong.','ORIGIN-WAAROM-11')
vraag('Zijn de Aelthir inheems op Velmara of aangepaste kolonisten?','Bepaalt hun Rekening en leeftijd.','VOLK-aelthir;ORIGIN-1')
vraag('Wil Thalen Orr het Zegel breken of herstellen?','Bepaalt de finale.','ORIGIN-WAAROM-12')
if not c.execute("select 1 from logboek where wat like 'Ronde V4:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",('Ronde V4: oorsprong gekozen (zaaischip Ysa, Makers kozen het lichaam; ORIGIN-1..10, ORIGIN-WAAROM-1..12, 4 Makers, onthulplan), genre-wet 2 = GENRE-wet2-V4, TECHNO-REGEL/MIX/TECH-GESCH bijgewerkt, tijdlijn rechtgezet (TIJD-V4-fasejaren), 160 voorwerpen, dagelijks leven per klasse, 14 subculturen, 9 rebellengroepen, vragen 022/025/061/063/066/067/068 voorlopig beantwoord.',))
add('GENRE-balans-V4','Genre','Genre-balans na V4','Sterker: intrige (rebellen, hoven), thriller (Makers-saga, omweg van Hesta), verborgen sf (zaaischip). Nog dun: humor, gewone vreugde, eten/muziek per volk (ronde D1/D2). Romance tussen volken blijft een kans.','balans','GENRE-zegelpunk')
c.commit()
codes={r[0] for r in c.execute('select code from canon')}
mis=sorted({x for (v,) in c.execute("select verwijst_naar from canon where ronde=?",(RONDE,)) for x in (v or '').split(';') if x and x not in codes})
print(f'V4: nieuw {n}, canon {len(codes)}, vervangen {len(vv)}; ontbrekende verwijzingen: {mis}')
