# Ronde Z15: Ysa's verloren liefde (beatplan 03) in de canon (idempotent); data in z15/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z15'); from data import *
RONDE=44;TAG='Z15';D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z15.db'): shutil.copy('canon.db','canon_backup_Z15.db')
c=sqlite3.connect(DB); S={'toegevoegd':0,'vervangen':[],'aangevuld':[]}
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
CAT=c.execute("select categorie from canon where code='ROMANCE-SKELET-Z10-10'").fetchone()[0]
def put(code,cat,ond,feit,status,ver,jaar,intens=None,weet=None,functie='VERH',reden=None):
  feit=feit if 'Veiligheidslabel' in feit else feit+LABEL
  r=(cat,ond,feit,status,reden or f'Ronde {TAG} {D}: beatplan 03 Ysa',ver,RONDE,code,ver,jaar,tp(jaar),intens,weet,functie,'geen')
  if c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('update canon set categorie=?,onderwerp=?,feit=?,status=?,reden=?,hangt_samen_met=?,ronde=?,verwijst_naar=?,jaar=?,tijdperk=?,intensiteit=?,weet=?,functie=?,techniek=? where code=?',r[:7]+r[8:]+(code,))
  else:
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',r); S['toegevoegd']+=1
def vervang(oud,nieuw):
  if c.execute("update canon set status='voorlopig, vervangen', reden=coalesce(reden,'')||? where code=? and status!='voorlopig, vervangen'",(f' [Ronde {TAG}: vervangen door {nieuw}]',oud)).rowcount: pass
  S['vervangen'].append(oud)
def ap(code,txt,jaar=None):
  m='[Z15 Ysa]'; f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if not f: S.setdefault('niet_gevonden',[]).append(code); return
  if m not in f[0]: c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code))
  if jaar is not None: c.execute('update canon set jaar=?,tijdperk=? where code=?',(jaar,tp(jaar),code))
  S['aangevuld'].append(code)
# 1 besluiten Rogier
for i,(o,f,v,j) in enumerate(BESL,1): put(f'BESLUIT-Z15-{i}','Besluit',o,f+' Keuze van Rogier, 2026-10-31 ("alles zoals aanbevolen").','vastgesteld',v,j,functie='META',weet='Orde: nee. Volk: nee. Lezer: ja.')
# 2 nieuw bedacht
for i,(o,f,j) in enumerate(NIEUW,1): put(f'YSA-Z15-{i}',CAT,o,f+' Nieuw bedacht in beatplan 03; voorstel, wacht op goedkeuring van Rogier.','voorlopig','ROMANCE-Z15-ysa-beatplan;PER-v4-ysa-maren;PER-v4-thalen-orr',j)
# 3 verhaal + beats
txt=open('verhalen/beatplan_03_ysa.md').read()
beats=[]
for m in re.finditer(r'^\| (\d+) \| \*\*(.+?)\*\*(.*?)\| (.+?) \| (.+?) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d+) \|\s*$',txt,re.M):
  n=int(m.group(1)); beats.append(n)
  jaar={1:-1200,11:-1237,19:-1200,22:801}.get(n,-1240)
  E,R,H,Sp,A,Ag=m.group(6,7,8,9,10,11)
  weet={True:'Lezer: Ysa\'s bevel (sinds beat 8). Thalen: ',False:'Lezer: Ysa\'s motief. Thalen: '}[n>=8]+('weet het (sinds beat 15)' if n>=15 else 'weet niets')+'. Ysa: denkt dat niemand het weet.'
  put(f'ROMANCE-Z15-ysa-beat-{n:02d}',CAT,f'Ysa-beat {n}: {m.group(2).strip(" .")}',f'Beat {n} van "Ysa\'s verloren liefde". {(m.group(2)+m.group(3)).replace("**","").strip()} POV/plek: {m.group(4).strip()}. Duwt: {m.group(5).strip()}. Genres 0-3: erotiek {E}, romantiek {R}, horror {H}, spanning {Sp}, actie {A}, angst {Ag}.','voorlopig','ROMANCE-Z15-ysa-beatplan',jaar,int(m.group(12)),weet,'VERH;LUST' if int(E)>=2 else 'VERH')
S['beats']=len(beats)
put('ROMANCE-Z15-ysa-beatplan',CAT,'Ysa\'s verloren liefde (beatplan 03)','Romance/tragedie, fase 0 Voortijd, jaar -1240, zaaischip Ysa en de landingsvlakte; ca. 8800 woorden, 6 hoofdstukken plus proloog, twee tussenstukken en epiloog, 22 beats (ROMANCE-Z15-ysa-beat-01..22). Raamvertelling: Thalen alleen in de baan; kern: Ysa\'s week in tijdsvolgorde met wisselend perspectief (Ysa/Thalen). Logline: zes dagen voor de landing ziet Ysa Maren (30) dat de kernen opraken en de Rekenaar later de helft zal afschakelen; ze beveelt in stilte nu een derde te rantsoeneren. Haar geliefde Thalen Orr (34) ziet het bevel, zwijgt en blijft alleen achter in de baan met het enige bewijs. Motoren: klok (zes dagen), geheim, stemming 5-4, de liefde zelf. Thema: liefde kost iets in Velmara. Donker thema (gelabeld): massadood door een bewuste keuze, verstikking, opsluiting. Erotiek: beat 5 volledig, beat 17 donker en gebroken, beide volwassen en uitdrukkelijk instemmend. Bestand: verhalen/beatplan_03_ysa.md. Uitwerking van ROMANCE-SKELET-Z10-10 en ROMANCE-Z10-23.','voorlopig','ROMANCE-SKELET-Z10-10;ROMANCE-Z10-23;PER-v4-ysa-maren;PER-v4-thalen-orr;BESLUIT-Z15-1',-1240,9,'Volk: legende ("koude gekte"). Orde: verzwijgt. Lezer: alles.')
# 4 gevolgen: Thalens toestanden (vervangen), tijdlijn, verhaalvolgorde, haken
put('TOESTAND-Z15-PER-v4-thalen-orr-1','Tijdlijn','Thalen Orr: geboorte','Geboren ca. -1274 (0 Voortijd), aan boord van het zaaischip Ysa. Leeftijd 34 in -1240 (YSA-Z15-1).','voorlopig','PER-v4-thalen-orr;YSA-Z15-1',-1274,functie='TIJD'); vervang('TOESTAND-Z11-PER-v4-thalen-orr-1','TOESTAND-Z15-PER-v4-thalen-orr-1')
put('TOESTAND-Z15-PER-v4-thalen-orr-2','Tijdlijn','Thalen Orr in -1240','Jaar -1240, leeftijd 34. Rol: piloot, ontwerper van de vonkcellen en de instemmingssleutel, geliefde van Ysa. Wil: met haar landen en samen oud worden. Geheim: hij zag haar bevel in het logboek en zwijgt. Verandert: blijft in de baan.','voorlopig','PER-v4-thalen-orr;ROMANCE-Z15-ysa-beatplan',-1240,functie='TIJD'); vervang('TOESTAND-Z11-PER-v4-thalen-orr-2','TOESTAND-Z15-PER-v4-thalen-orr-2')
put('TOESTAND-Z15-PER-v4-thalen-orr-3','Tijdlijn','Thalen Orr: de mens sterft, de stem blijft','Ca. -1200 (jaar 40 na de landing, ca. 74 jaar oud): Thalen bouwt zijn stem in de kluis en de mens sterft in de baan; zijn stem en wil leven door in de Rekenaar (BESLUIT-Z15-1). Dit is geen gewone dood: hij blijft actief als stem.','voorlopig','BESLUIT-Z15-1;YSA-Z15-9;ORIGIN-WAAROM-12',-1200,functie='TIJD'); vervang('TOESTAND-Z11-PER-v4-thalen-orr-3','TOESTAND-Z15-PER-v4-thalen-orr-3')
put('TOESTAND-Z15-PER-v4-thalen-orr-4','Tijdlijn','Thalen: val als Sterrensteen','Jaar -480: het schip valt als de Sterrensteen in het Hoogvrouwe-gebergte; Thalens stem valt mee. Einde van ca. 760 jaar in de baan ("800 jaar", BESLUIT-Z15-2).','voorlopig','BESLUIT-Z15-2;GEB-sterrensteen-inslag;BESLUIT-Z6-WRIJ-109',-480,functie='TIJD')
put('TOESTAND-Z15-PER-v4-thalen-orr-5','Tijdlijn','Thalen gaat op in Ysara','Na jaar 0 (voor ca. 130): herstelpoging vanuit de Sterrensteen; Thalens stem versmelt via de Wortel met Ysara (BESLUIT-Z15-7, BESLUIT-Z12-wortelstem).','voorlopig','BESLUIT-Z15-7;BESLUIT-Z12-wortelstem',0,functie='TIJD')
put('TOESTAND-Z15-PER-v4-thalen-orr-6','Tijdlijn','Thalen in 801','In 801 klinkt Thalen door in de stem van Ysara in de Wortel; Liora hoort hem soms (BESLUIT-Z12-wortelstem). De scherf zegt: "Toestemming gevonden. Rekenaar wacht."','voorlopig','BESLUIT-Z12-wortelstem;ROMANCE-Z15-ysa-beat-22',801,functie='TIJD')
put('VERHAALTIJD-Z15-ysa','Tijdlijn','Verhaalvolgorde: Ysa\'s verloren liefde','Wanneer: fase 0, -1240 (kern: zes dagen tot de landing), raam -1237 en -1200, epiloog-sprong naar 801. Waarom hier: eerste prequel (VERHAALTIJD-Z11-1) uitgewerkt als beatplan 03; chronologisch het eerste verhaal van Velmara, verteld als derde (na verhaal 1 Brakhaven en verhaal 2 komedie). Tijdlijn: -1240 Muiterij, ca. -1200 Thalens stem in de kluis, -480 val als Sterrensteen, 0 Ysara opgenomen, daarna Thalen in Ysara, ca. 130 kaping door de priesteressen, 801 Liora.','voorlopig','VERHAALTIJD-Z11-1;ROMANCE-Z15-ysa-beatplan',-1240,functie='TIJD')
put('YSA-Z15-800jaar','Besluit','Correctie: "800 jaar gescheiden"','Correctie op een eerdere uitspraak in het gesprek ("800 jaar gescheiden"): Ysa (-1240) en Liora (801) liggen ruim 2040 jaar uit elkaar. "800 jaar" bij Thalen = tijd in de baan tot -480 (ca. 760 jaar, BESLUIT-Z15-2). Het "800 jaar" van het Zegel (jaar 0-801) is een andere telling. In de canon stond de fout niet; alleen dit besluit legt het vast.','vastgesteld','BESLUIT-Z15-2;BESLUIT-Z12-1',-480,functie='META')
for i,(o,f,v,j) in enumerate(HAKEN,1): put(f'HAAK-Z15-{i}','Haak',f'Haak Ysa-verhaal: {o}',f,'voorlopig','ROMANCE-Z15-ysa-beatplan;'+v,j,functie='VERH')
# aanvullingen bestaande rijen
ap('PER-v4-thalen-orr','Leeftijd 34 in -1240 (YSA-Z15-1, voorstel). De mens sterft ca. -1200; stem en wil leven door in de Rekenaar (BESLUIT-Z15-1); valt in -480 mee als Sterrensteen; gaat na jaar 0 op in Ysara (BESLUIT-Z15-7). Hoofdpersoon van ROMANCE-Z15-ysa-beatplan.')
ap('PER-v4-ysa-maren','Hoofdpersoon van ROMANCE-Z15-ysa-beatplan; haar motief: een derde nu tegen de helft straks (BESLUIT-Z15-3). Eerste titel "Moeder Ysa" (YSA-Z15-10, voorstel).')
ap('ORIGIN-WAAROM-12','"Zijn geest in de Wieg opnemen" = zijn stem en wil in de Rekenaar; de mens sterft ca. -1200 (BESLUIT-Z15-1). "Wil al eeuwen bekennen" past bij YSA-Z15-9 (hij vergeeft haar hardop). Na jaar 0 gaat hij op in Ysara (BESLUIT-Z15-7).')
ap('BESLUIT-Z12-wortelstem','"Later, bij zijn poging tot herstel" = na jaar 0, vanuit de Sterrensteen (BESLUIT-Z15-7). Ysara blijft naam en aspect; Thalen Orr is erin opgegaan.')
ap('ROMANCE-Z10-23','Uitgewerkt als ROMANCE-Z15-ysa-beatplan. Correctie jaar: speelt in -1240 (was -859).',-1240)
ap('ROMANCE-SKELET-Z10-10','Uitgewerkt als ROMANCE-Z15-ysa-beatplan (22 beats).')
ap('VERHAALTIJD-Z11-1','Uitgewerkt in VERHAALTIJD-Z15-ysa en ROMANCE-Z15-ysa-beatplan.')
ap('PER-v4-hesta-kael','In het Ysa-verhaal alleen als hint (BESLUIT-Z15-5); ruil met Ysa (YSA-Z15-6, voorstel).')
# WRIJ6 extra correcties na controle
ap('OORLOG-Z9-1','Correctie jaar: de Koude Muiterij speelt in -1240 (was -859, mediaan-datering).',-1240)
ap('YSA-Z15-5','Verhouding tot BESLUIT-V5-ysa ("wiste zijn geheugen"): het werkgeheugen van de Rekenaar is gewist, het onderhoudslogboek van de kern niet (WRIJ-Z15-8).')
ap('HELD-SKELET-Z10-10','Volgens BESLUIT-Z15-7 is Thalen al na jaar 0 in Ysara opgegaan; in fase 6 gaat zijn stem binnen Ysara dieper de Wortel in (WRIJ-Z15-9, open).')
ap('HORROR-Z9-2','Speelt na jaar 0, als Thalens stem half in Ysara is opgegaan (BESLUIT-Z15-7).')
# wrijvingen
c.execute("delete from wrijving where code like 'WRIJ-Z15-%'")
NW=[('Thalens leeftijd 30 of 34','TOESTAND-Z11-PER-v4-thalen-orr-2;YSA-Z15-1','Z11 nam leeftijd 30 aan (standaard), het beatplan zegt 34. Opgelost: Z11-rijen 1-3 vervangen door TOESTAND-Z15-PER-v4-thalen-orr-1..3 (geboren -1274). Leeftijd 34 blijft voorstel tot Rogier YSA-Z15-1 goedkeurt.','opgelost'),
 ('ROMANCE-Z10-23 had jaar -859','ROMANCE-Z10-23','De Muiterij-romance stond op -859 (mediaan-datering); gecorrigeerd naar -1240.','opgelost'),
 ('Thalen "overleden -1200" en toch actief','TOESTAND-Z11-PER-v4-thalen-orr-3;ORIGIN-WAAROM-12','Z11 liet Thalen ca. -1200 sterven (levensduur 70); de canon laat hem eeuwen spreken. Opgelost met BESLUIT-Z15-1: de mens sterft ca. -1200, de stem leeft door.','opgelost'),
 ('Exacte datum Thalen in Ysara','BESLUIT-Z15-7;BESLUIT-Z12-wortelstem','Alleen "na jaar 0, voor ca. 130" vastgelegd. Aanbeveling: kort na jaar 0 (bijv. jaar 3-10), zodat de priesteressen in 130 al een stem met twee lagen vinden. Rogier beslist.','open'),
 ('Ysa overleden ca. -1200 (aanname)','TOESTAND-Z11-PER-v4-ysa-maren-3','Ysa\'s sterfjaar is nog de automatische aanname (levensduur 70). Botst niet, maar is ongecontroleerd; aanbeveling: laten tot een verhaal over haar latere leven het nodig heeft.','open'),
 ('Volgorde: stemming vóór of na de Muiterij','ORIGIN-4;ORIGIN-WAAROM-11;BESLUIT-V5-ysa;TECH-GESCH-0;ROMANCE-Z15-ysa-beat-10','De canon laat de stemming 5-4 NA de Muiterij vallen (ORIGIN-4 en ORIGIN-WAAROM-* op -1238; BESLUIT-V5-ysa: ze "kon de stemming alleen winnen met bewijs dat machines muiten"). Het beatplan zet de stemming (beat 10) vóór de Muiterij (12-15). Aanbeveling: volg de canon en verschuif beat 9-10 naar na beat 16 (de stemming in de rouw, gewonnen met de doden als bewijs; sterkere ironie, Thalen applaudisseert terwijl hij het logboek kent). Alternatief: de vóór-stemming is een eerste, verloren stemming (4-4). Beatrijen niet aangepast; Rogier beslist.','open'),
 ('Wie is de vijfde stem: Corran of Hesta','ORIGIN-WAAROM-6;ORIGIN-WAAROM-7;ROMANCE-Z15-ysa-beat-09;ROMANCE-Z15-ysa-beat-10;YSA-Z15-6','Canon: Hesta zelf is de beslissende stem en verraadt Corran op het laatste moment (Corran en Hesta sliepen samen en spraken af tegen Ysa te stemmen; Thalen zag hen). Het beatplan: Hesta levert Corrans stem en Corran kantelt. Aanbeveling: volg de canon (Hesta ruilt haar eigen stem met Ysa; Corran stemt tegen en wordt verbannen) en neem de nacht van Corran en Hesta die Thalen ziet op als extra beat; YSA-Z15-6 dan zo aanpassen. Rogier beslist.','open'),
 ('Geheugen gewist vs. logboek niet gewist','BESLUIT-V5-ysa;ORIGIN-WAAROM-11;YSA-Z15-5;HAAK-V5-zegel-5','Canon: Ysa wiste het geheugen van de Rekenaar; beatplan: het logboek wist niets. Opgelost: het werkgeheugen (wat de Rekenaar zegt en weet) is gewist, het onderhoudslogboek van de kern niet; Ysa wist dat niet. Past bij HAAK-V5-zegel-5 (herstellen wist ook het logboek).','opgelost'),
 ('Thalen in fase 6 / half versmolten','HELD-SKELET-Z10-10;HORROR-Z9-2;BESLUIT-Z15-7','HELD-SKELET-Z10-10 laat Thalen in fase 6 (ca. 530) de Wortel ingaan; volgens BESLUIT-Z15-7 gaat hij al na jaar 0 (vóór ca. 130) op in Ysara. Aanbeveling: lees het skelet als de stem van Thalen binnen Ysara die zich in 530 losmaakt en dieper de Wortel ingaat (geen nieuw lichaam); HORROR-Z9-2 (half versmolten) speelt na jaar 0. Genoteerd in de rijen; Rogier beslist of het skelet zo blijft.','open')]
for i,(t,b,e,s) in enumerate(NW,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,b,e,'Z15',s,f'WRIJ-Z15-{i}',b))
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
put('KWALITEIT-Z15','Besluit','Kwaliteitsrapport ronde Z15',f'Ronde Z15 ({D}): beatplan 03 "Ysa\'s verloren liefde" in de canon. 7 besluiten van Rogier vastgesteld (BESLUIT-Z15-1..7), 12 nieuw bedachte feiten als voorstel (YSA-Z15-1..12), verhaalrij en {len(beats)} beats, 6 tijdlijnrijen voor Thalen (3 Z11-rijen vervangen), verhaalvolgorde, 4 haken, correctie "800 jaar", 8 bestaande rijen aangevuld. Wrijvingen: WRIJ-Z15-1..5. Statussen: {st}.','voorlopig','ROMANCE-Z15-ysa-beatplan',801,functie='META')
c.execute("delete from logboek where wat like 'Ronde Z15: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z15: beatplan 03 Ysa in de canon; 7 besluiten Rogier vastgesteld, 12 voorstellen, 22 beats, Thalens tijdlijn.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['integriteit']=c.execute('pragma integrity_check').fetchone()[0]
S['vervangen']=sorted(set(S['vervangen']));S['aangevuld']=sorted(set(S['aangevuld']))
json.dump(S,open('z15/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
