# Ronde Z36: Rogiers besluiten (stap 0), opruimen (1c), sjabloonbesluiten (1a), verhalenmachine (stap 2). Idempotent en additief.
# Niets verwijderd; Kern alleen via BESLUIT-Z36-*; roman niet aangeraakt. toets.py na elke stap (exit 0 vereist).
# Gebruik: DB=kopie.db python3 r_Z36.py
import sqlite3,shutil,os,re,json,sys,collections,subprocess
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z36')]
import afgeleid,migreer
import data as D
DT='2026-11-01';RD='Z36';RN=65;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z36.db'): shutil.copy('canon.db','canon_backup_Z36.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
REDEN='Ronde Z36, stap 0: besluit van '+D.R
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z36.py')).rowcount
def toets(stap):
  afgeleid.bouw(c);c.commit()
  r=subprocess.run([sys.executable,'toets.py',DB,'--json',f'/tmp/toets_{RD}.json'],capture_output=True,text=True)
  print(f'[{stap}] toets exit {r.returncode}: '+' | '.join(l for l in r.stdout.splitlines()[1:4]))
  if r.returncode: print(r.stdout[-4000:]);sys.exit(f'toets faalt na {stap}')
def bestaat(code): return c.execute('select 1 from canon where code=?',(code,)).fetchone() is not None
def nieuw(code,cat,ond,feit,verw,reden=REDEN,status='vastgesteld',kern=False,tijdperk=None,jaar=None):
  if bestaat(code): return 0
  c.execute("insert into canon(code,categorie,onderwerp,feit,reden,status,ronde,verwijst_naar,hangt_samen_met,draagkracht_handmatig,tijdperk,jaar) values(?,?,?,?,?,?,?,?,?,?,?,?)",
            (code,cat,ond,feit,reden,status,RN,verw,verw,'Kern' if kern else None,tijdperk,jaar))
  S['canon_nieuw']+=1;wijz(code,'toegevoegd','canon',None,status);return 1
def vervang(oud,door):
  r=c.execute("select status from canon where code=? and status in('vastgesteld','voorlopig')",(oud,)).fetchone()
  if r and c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=?",(door,oud)).rowcount:
    S['canon_vervangen']+=1;wijz(oud,'vervangen','status',r[0],'voorlopig, vervangen (door '+door+')')
def zet(tabel,sleutel,waarde,veld,nieuwe,code=None):
  oud=c.execute(f'select {veld} from {tabel} where {sleutel}=?',(waarde,)).fetchone()
  if oud is None or oud[0]==nieuwe: return
  c.execute(f'update {tabel} set {veld}=? where {sleutel}=?',(nieuwe,waarde));S[tabel+'_gewijzigd']+=1;wijz(code or waarde,'gewijzigd',f'{tabel}.{veld}',oud[0],nieuwe)
def sluit_wrij(code,hoe):
  zet('wrijving','code',code,'status','opgelost')
  b=c.execute('select beschrijving from wrijving where code=?',(code,)).fetchone()
  if b and 'Opgelost in Z36' not in (b[0] or ''): zet('wrijving','code',code,'beschrijving',(b[0] or '')+' Opgelost in Z36: '+hoe)
def keuze(code,aanb,status,citaat=None):
  if not c.execute('select 1 from keuze where code=?',(code,)).fetchone(): return
  zet('keuze','code',code,'aanbeveling',aanb); zet('keuze','code',code,'status',status)
  if citaat: zet('keuze','code',code,'citaat',citaat)
# ================= STAP 0: Rogiers besluiten =================
for code,cat,ond,feit,verw,kern in D.BESLUIT: nieuw(code,cat,ond,feit,verw,kern=bool(kern))
# ORIGIN-10 krijgt een opvolger met het motief
nieuw('ORIGIN-10-Z36','Oorsprong','Het Zegel bevestigt de Stille Modus (jaar 0), met het motief',D.ORIGIN10,'ORIGIN-10;BESLUIT-Z36-1;ORIGIN-WAAROM-8;BESLUIT-Z30-1;BESLUIT-Z30-2;BESLUIT-Z32-13',jaar=0)
vervang('ORIGIN-10','ORIGIN-10-Z36')
# Z36-2: ERF-voortijd vastgesteld
zet('canon','code','ERF-voortijd','status','vastgesteld')
# Z36-3: genre-overzichten hernummeren
NAMEN={1:('Vonk',2),2:('Brand',3),3:('Noodtoestand',4),4:('Ontvangst',5),5:('Markt',6),6:('Barsten',7),7:('Heden',801)}
for oud,(naam,nr) in NAMEN.items():
  oc=f'FASE-OVERZICHT-Z10-{oud}';r=c.execute('select feit,verwijst_naar,status from canon where code=?',(oc,)).fetchone()
  lijst=re.sub(r'^Genres in fase \d+ [^:]+: ','',r[0]);lijst=re.sub(r' ?Haak: elke fase heeft zijn eigen soort held, gruwel en liefde\.','',lijst)
  nc=f'FASE-OVERZICHT-Z36-{nr}'
  nieuw(nc,'Tijdperk',f'{naam}: genres (fase {nr})',f'{naam} (fase {nr}) heeft volgens de ideeënbank deze genres: {lijst} Telling volgens de ankers (BESLUIT-Z36-3).',r[1],status=r[2],kern=(r[2]=='vastgesteld'))
  vervang(oc,nc)
# Z36-4: derde weg in fase_rijm
zet('fase_rijm','fase','801 Heden','blijvende_verandering','Het Zegel kan niet meer ja zeggen namens een lichaam; wie het nog probeert, doet het zonder de dekking van het Zegel en op eigen naam (BESLUIT-Z36-4).','RIJM-801 Heden')
# Z36-5/6: patroonbreuken A en B
for code,oud,feit,verw in D.VALS:
  r=c.execute('select categorie,onderwerp from canon where code=?',(oud,)).fetchone()
  nieuw(code,r[0],r[1]+' (na de patroonbreuk)',feit,verw,status='vastgesteld');vervang(oud,code)
zet('fase_rijm','fase','6 Markt','ontdekt',"ja: Joris' lichaam getuigt en de leugen 'de Pest was een straf' sneuvelt binnen een seizoen in het openbaar (BESLUIT-Z36-5, VALS-markt-Z36)",'RIJM-6 Markt')
zet('fase_rijm','fase','5 Ontvangst','ontdekt','ja: het lek van Iresse (300) komt aan en het geloof overleeft toch (BESLUIT-Z36-6, VALS-ontvangst-Z36)','RIJM-5 Ontvangst')
zet('fase_rijm','fase','5 Ontvangst','ontdekt_as','ja','RIJM-5 Ontvangst')
zet('fase_rijm','fase','5 Ontvangst','blijvende_verandering','Een noodwet is een geloof geworden dat zijn eigen ontmaskering overleeft: men weet hoe het licht ontstond en ontvangt toch.','RIJM-5 Ontvangst')
# Z36-8: hoofdverhalen
KOP={'1':'De zoutstem (fase 1, ca. -355 tot -250)','2':'Ysel aan de rivierpoort (fase 2, ca. -150 tot -45)','3':'De kroniek van Anath (fase 3, ca. -40 tot 0)','4':'Een winter van vergaderingen (fase 4, jaar 14 tot ca. 60)','5':'Negen Ontvangsten (fase 5, ca. 260 tot 300)','6':'De melkos van Ambergaard (fase 6, ca. 338 tot 400, met naschok tot 720)','7':'Het kasboek van Annike (fase 7, ca. 722 tot 801)'}
for f,v in D.VERHAAL.items():
  oud=f'VERHAAL-fase{f}-Z35';nc=f'VERHAAL-fase{f}-Z36'
  r=c.execute('select feit,verwijst_naar,tijdperk from canon where code=?',(oud,)).fetchone()
  if v is None: feit=r[0].rstrip()+D.HAVRA;verw=r[1]+';PER-f6-havra-Z32' if bestaat('PER-f6-havra-Z32') else r[1]
  else: feit,verw=v
  verw=';'.join(x for x in verw.split(';') if bestaat(x))
  nieuw(nc,'Verhaal',KOP[f],feit,verw,reden=REDEN+' (VOORSTEL-Z35-verhaal-'+f+')',tijdperk=r[2]);vervang(oud,nc)
  for (bc,) in c.execute('select code from boog where synopsis_code=?',(oud,)).fetchall(): zet('boog','code',bc,'synopsis_code',nc)
# boog-velden die de nieuwe synopsen veranderen
for bc,veld,w in [('VERHAAL-fase2','beslisser_as','Ysel'),('VERHAAL-fase2','betaler_as','Ysel en haar netwerk'),('VERHAAL-fase1-Z32','vorm','ballade'),('VERHAAL-fase3','vorm','kroniek met kantlijn'),('VERHAAL-fase4','vorm','wij-vorm (twaalf stemmen)'),('VERHAAL-fase4','erotische_sleutelscene','geen (alleen gerucht)'),('VERHAAL-fase5','vorm','negen Ontvangsten in veertig jaar'),('VERHAAL-fase6-Z32','wie_betaalt','Moeder Havra'),('VERHAAL-fase7-Z32','vorm','kasboek'),('VERHAAL-fase1-Z32','romance','geen')]:
  zet('boog','code',bc,veld,w)
# voorstelrijen naar vervangen, keuzes besloten
VB={'kern-voortijd-erf':'BESLUIT-Z36-2','kern-faseoverzicht':'BESLUIT-Z36-3','kern-derde-weg':'BESLUIT-Z36-4','breuk-markt':'BESLUIT-Z36-5','breuk-ontvangst':'BESLUIT-Z36-6','breuk-noodtoestand':'BESLUIT-Z36-7'}
VB.update({f'verhaal-{i}':'BESLUIT-Z36-8' for i in range(1,8)})
for k,b in VB.items():
  if k=='breuk-noodtoestand':
    r=c.execute("select status from canon where code=?",('VOORSTEL-Z35-'+k,)).fetchone()
    if r and r[0]!='vervallen': zet('canon','code','VOORSTEL-Z35-'+k,'status','vervallen')
  else: vervang('VOORSTEL-Z35-'+k,b)
  keuze('KEUZE-VOORSTEL-Z35-'+k,f'Besloten door Rogier in {b}.','besloten')
for w,b in [('WRIJ-Z30-2','BESLUIT-Z36-1: de Stille Modus heeft een motief en een plaats in het boek (zaadje h32, wacht op de roman)'),('WRIJ-Z21-5','BESLUIT-Z36-1: de negen vonkcellen dragen de upload van de Stille Modus'),('WRIJ-Z22-2','BESLUIT-Z36-1 en WRIJ-Z36-3: het blauwe licht is Hesta die de deur opent'),('WRIJ-Z33-1','BESLUIT-Z36-3: FASE-OVERZICHT-Z36-* volgen de ankers'),('WRIJ-Z34-1','BESLUIT-Z36-9: eerst Liora\u2019s ja, dan Teo\u2019s uitstel'),('WRIJ-Z35-1','BESLUIT-Z36-8: Ysel beslist in het hoofdverhaal van fase 2, Tarn in boog 2-c')]:
  sluit_wrij(w,b);keuze('KEUZE-'+w,'Besloten: '+b+'.','besloten')
# nieuwe wrijvingen
for code,titel,verw,besch,typ in D.WRIJ:
  if not c.execute('select 1 from wrijving where code=?',(code,)).fetchone() and c.execute('insert or ignore into wrijving(code,titel,delen_die_botsen,beschrijving,type,status,verwijst_naar) values(?,?,?,?,?,?,?)',(code,titel,verw,besch,typ,'open',';'.join(x for x in verw.split(';') if bestaat(x)))).rowcount: S['wrijving_nieuw']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
# zaadjes
z=D.ZAADJE
if c.execute('insert or ignore into zaadje(code,wat,geplant_in,oogst_in,status,bron) values(?,?,?,?,?,?)',z).rowcount: S['zaadje_nieuw']+=1;wijz(z[0],'toegevoegd','zaadje',None,z[4])
zet('zaadje','code','ZAAD-stille-modus','status','gezaaid in voorstel (ZAAD-Z36-h32-protocol, wacht op roman)')
zet('zaadje','code','ZAAD-stille-modus','bron','BESLUIT-Z36-1; ORIGIN-10-Z36; ZAAD-Z36-h32-protocol')
zet('zaadje','code','ZAAD-hesta-vonkcellen','oogst_in','jaar 28: de upload van de Stille Modus (BESLUIT-Z36-1)')
zet('zaadje','code','ZAAD-hesta-vonkcellen','status','geoogst in canon (BESLUIT-Z36-1)')
zet('zaadje','code','ZAAD-blauw-licht','oogst_in','jaar 28 via dezelfde deur (BESLUIT-Z36-1, WRIJ-Z36-3)')
zet('zaadje','code','ZAAD-blauw-licht','status','geoogst in canon; tijdsvolgorde open in WRIJ-Z36-3')
# keuzepunt 'Moeder'
KM=('KEUZE-Z36-moeder','keuzepunt','Weet de Reckoner dat Ysa "Mother" heet?',
 'Ja, houden. Reden: de downlink naar Ysa\u2019s oortje is in h25 nog levend, en vanaf h21 heet ze Mother in het kamp; de Reckoner kan de titel dus gehoord hebben. Het zaadje in h32 hoeft niets uit te leggen.',
 'ZAAD-Z36-h32-protocol;ROMAN-Z16-roman',None,'Structuur','open','stille_modus_Z36.md deel 2 (Rogier)','ROMAN-Z16-h25: de verbinding naar Ysa\u2019s oortje staat nog open (downlink live); h21: het kamp noemt Ysa "Mother".')
if c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,impact,draagkracht,status,bron,citaat) values(?,?,?,?,?,?,?,?,?,?)',KM).rowcount: S['keuze_nieuw']+=1;wijz(KM[0],'toegevoegd','keuze',None,'open')
# regelverfijning: Kern die naar een vervangen rij met een levende Kern-opvolger wijst, leunt op die opvolger
NS="select r.van_code,'Kern leunt op Kleur: '||r.naar_code||' ('||b.status||')' from relatie r join canon a on a.code=r.van_code join canon b on b.code=r.naar_code where r.soort='leunt_op' and a.draagkracht='Kern' and a.status in('vastgesteld','voorlopig') and b.draagkracht='Kleur' and not exists(select 1 from canon s where s.code=b.vervangen_door and s.draagkracht='Kern' and s.status in('vastgesteld','voorlopig'))"
zet('regel','code','R-kern_leunt_op_kleur','sql_test',NS)
afgeleid.bouw(c)
for code,det in c.execute(NS+" and r.van_code like 'FASE-OVERZICHT-Z36-%'").fetchall():
  S['uitzondering']+=c.execute('insert or ignore into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',('kern_leunt_op_kleur',code,det,'overgedragen van de FASE-OVERZICHT-Z10-rij die deze rij vervangt (BESLUIT-Z36-3); een genrelijst wijst naar de ideeënbank','WRIJ-Z33-2')).rowcount
toets('stap 0')
# ================= STAP 1c: keuzelijst opruimen =================
alle=codes=None
C={r[0] for r in c.execute('select code from canon')}
dood=c.execute('select count(*) from v_dode_links').fetchone()[0]
F={tuple(x) for x in json.load(open(f'/tmp/toets_{RD}.json'))}
for w in ['WRIJ-Z30-4','WRIJ-Z33-3','WRIJ-Z33-6','WRIJ-Z33-9','WRIJ-Z33-10','WRIJ-Z33-11']:
  U=c.execute('select toets,code,detail from toets_uitzondering where wrijving=?',(w,)).fetchall()
  actief=sum(tuple(u) in F for u in U)
  extra=f'; v_dode_links telt nu {dood}' if w=='WRIJ-Z30-4' else ''
  if actief==0 and (w!='WRIJ-Z30-4' or dood==0):
    bewijs=f'toets.py Z36 stap 0: van de {len(U)} geregistreerde bevindingen komt er 0 nog voor{extra}'
    sluit_wrij(w,bewijs);keuze('KEUZE-'+w,'Sluiten, bewezen: '+bewijs+'.','besloten')
for w,(cc,cit,aanb) in D.LEES.items():
  st=c.execute('select status from keuze where code=?',('KEUZE-'+w,)).fetchone()
  if not st or st[0]!='open': continue
  ft=c.execute('select feit from canon where code=?',(cc,)).fetchone() or c.execute('select beschrijving from wrijving where code=?',(cc,)).fetchone()
  bron=' '.join(x or '' for x in [ft[0] if ft else '']+[r[0] for r in c.execute('select detail from toets_uitzondering where code=?',(cc,))])
  if cit and cit not in bron: sys.exit(f'citaat niet gevonden in {cc}: {cit}')
  keuze('KEUZE-'+w,'Aanbeveling: '+aanb,'open',f'{cc}: "{cit}"' if cit else f'{cc}: "{(ft[0] if ft else "")[:200]}"')
# herkomst: citaat uit de rij zelf + concrete aanbeveling (heuristiek: kandidaten volgen uit verwijzingen, niet met de hand gelezen)
for code,ond,aanb,raakt in c.execute("select code,onderwerp,aanbeveling,raakt from keuze where soort='herkomst' and status='open'").fetchall():
  ft=(c.execute('select feit from canon where code=?',(raakt,)).fetchone() or [''])[0] or ''
  zin=re.split(r'(?<=[.!?])\s',ft.strip())[0][:220]
  m=re.match(r'kandidaat: ([A-Z][\w-]+) \(die rij heeft bron ([^)]+)\)',aanb or '')
  if m: nb=f'Aanbeveling: leg {m.group(1)} vast als bron van {raakt}. Reden: die rij heeft zelf een bron ({m.group(2)}) en {raakt} verwijst ernaar. Heuristisch gevonden, Rogier bevestigt.'
  else: nb=f'Aanbeveling: {raakt} blijft Structuur met bron "ideeënbank (geen besluit gevonden)". Reden: geen enkele rij met een bekende herkomst wijst naar deze rij; ik verzin geen bron.'
  if (aanb or '').startswith('Aanbeveling:'): continue
  keuze(code,nb,'open',f'{raakt}: "{zin}"')
toets('stap 1c')
# ================= STAP 1a: elke sjabloonfamilie een besluit (geen rijen vervangen: zie scorekaart, blokkade) =================
for sig,m,prf,vs in c.execute('select sig,markering,prefixen,voorstel from sjabloon_familie').fetchall():
  if sig in('L:Naam|Volk|Regio|Huis|Rol|Fase|Wil|Durft','L:Kern|Naam|Volk|Regio|Huis|Rol|Fase|Wil','L:Volk|Fase|Rol|Verandert|Zintuiglijk|Haak|Verdiept (Z#)|Geur') and 'Z36' not in (vs or ''):
    zet('sjabloon_familie','sig',sig,'voorstel',(vs or '')+' Z36: de velden staan nu in kolommen in personage_profiel (afgeleid, herbouwd door afgeleid_motor.py); de tekstrijen blijven levend omdat ankers, relaties en naamtoetsen ernaar wijzen. Vervangen pas als die drie op personage_profiel lezen.','SJAB-'+sig);continue
  if vs: continue
  if m in('ideeenbank','al ideeenbank'): t='Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.'
  else: t='Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.'
  zet('sjabloon_familie','sig',sig,'voorstel',t,'SJAB-'+sig)
toets('stap 1a')
# ================= STAP 2: de verhalenmachine =================
import machine as M, ideeen
AS=[('positie',x,None,None) for x in M.POSITIES]+[('genre',g,'prior lezersvraag (aanname, geen data)',p) for g,p in M.GENRES.items()]+[('schaal',s,f'kostenfactor {f}',None) for s,f in M.SCHALEN.items()]
AS+=[('vorm',v,f'ca. {k}k woorden (aanname)',None) for v,k in M.VORMEN.items()]+[('afloop',x,None,None) for x in M.AFLOPEN]+[('hoofdpersoon',h,'leeftijdsband|geslacht; altijd 18+',None) for h in M.HOOFDPERSONEN]
afgeleid.bouw(c)
AS+=[('volk',v,'uit personage_profiel'+(f'; bestaat vanaf fase {M.VOLK_VANAF[v][0]} ({M.VOLK_VANAF[v][1]})' if v in M.VOLK_VANAF else ''),None) for (v,) in c.execute('select distinct volk from personage_profiel where volk is not null order by 1')]
for r in AS: S['verhaal_as']+=c.execute('insert or ignore into verhaal_as(as_naam,waarde,toelichting,prior) values(?,?,?,?)',r).rowcount
for bc,(pos,gen,sch,vk,vorm,af,hp,gv) in D.BOOG_AS.items():
  if c.execute(f"insert or ignore into boog_as(boog_code,positie,genre,schaal,volk,vorm,afloop,hoofdpersoon,{','.join('g_'+g for g in M.G)},bron,status) values({','.join('?'*18)})",(bc,pos,gen,sch,vk,vorm,af,hp,*gv,'schatting architect Z36 uit synopsis en boogvelden','voorlopig')).rowcount: S['boog_as']+=1;wijz(bc,'toegevoegd','boog_as',None,'voorlopig')
for code,om,gw,bron,richting in D.DOEL: S['doel']+=c.execute('insert or ignore into doel(code,omschrijving,gewicht,bron_gewicht,richting) values(?,?,?,?,?)',(code,om,gw,bron,richting)).rowcount
for code,naam,doel,mn in D.DOELPROFIEL: S['doelprofiel']+=c.execute(f"insert or ignore into doelprofiel(code,naam,{','.join('doel_'+g for g in M.G)},{','.join('min_'+g for g in M.G)},bron,status) values({','.join('?'*20)})",(code,naam,*doel,*mn,'architect Z36 (startwaarden; Rogier stelt bij)','voorlopig')).rowcount
S['gewichtset']+=c.execute('insert or ignore into gewichtset(naam,datum,methode,status,gewichten,bron) values(?,?,?,?,?,?)',('lancering serie',DT,'startwaarde','voorlopig',json.dumps(M.LANCERING),'aanname (opdracht_Z35.md 9b.3); te vervangen door vraag.py gewicht swing of paren')).rowcount
REG=[('R-verhaal_afstand','verhaal','Elk voorgesteld of ent-klaar verhaalprofiel verschilt op minstens 3 van de 7 assen van elke boog en elk eerder profiel in dezelfde fase.','py:verhaal_afstand','opdracht_Z35.md 7.3; OPDRACHT_architect_Z36.md stap 2','architect (Z36), ter vaststelling door Rogier','actief','fout'),
('R-profiel_harde_lijn','veiligheid','Geen verhaalprofiel met een hoofdpersoon onder 18, een dier of minderjarige in een seksuele rol, seks met wie niet kan instemmen, ongelabelde dwang, of erotiek zonder wereldregel.','py:profiel_harde_lijn','BESLUIT-Z30-4; opdracht_Z35.md 9a.2','architect (Z36), ter vaststelling door Rogier','actief','fout'),
('R-positie_dekking','verhaal','Signaal: een fase waarin een van de zeven posities nergens voorkomt, niet in een boog en niet in de ideeënbank.','py:positie_dekking','opdracht_Z35.md 7.4','architect (Z36), ter vaststelling door Rogier','actief','signaal')]
for r in REG:
  if c.execute('insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)',r).rowcount: S['regel']+=1;wijz(r[0],'toegevoegd','regel',None,RD)
H=[('HANDL-Z36-1','De verhalenmachine',"Een verhaal is een punt op zeven assen (verhaal_as): positie, genre, schaal, volk, vorm, afloop, hoofdpersoon. Afstand is het aantal assen dat verschilt; minder dan 3 is een kopie (R-verhaal_afstand). Bestaande bogen staan op de assen in boog_as, nieuwe ideeën in verhaal_profiel (ideeënbank, nooit Kern). Opdrachten: vraag.py bedenk, pareto, volgende, gewicht, afstand, dekking, ideeenrapport. Een run ziet alleen eerdere runs; zo voegt opnieuw draaien niets toe."),
   ('HANDL-Z36-2','Filters zijn geen scores',"De harde lijnen (BESLUIT-Z30-4), de wereldregels en de Kern sluiten een profiel uit voordat er iets gescoord wordt; machine.bewaar filtert opnieuw en weigert. Pas daarna wegen de doelen (tabel doel) met de gewichtset. Gewichten en priors zijn aannames tot Rogier ze met vraag.py gewicht swing of paren vastlegt of er lezersdata is.")]
for h in H:
  if c.execute('insert or ignore into handleiding(code,onderwerp,tekst) values(?,?,?)',h).rowcount: S['handleiding']+=1;wijz(h[0],'toegevoegd','handleiding',None,RD)
toets('stap 2 basis')
# run Z36-01: ideeënbank door de machine
volken=[r[0] for r in c.execute("select waarde from verhaal_as where as_naam='volk'")]
S['ideeen_verwerking']+=ideeen.verwerk(c,'Z36-01',volken)
toets('stap 2 run Z36-01')
# run Z36-02: lege posities vullen, 3 profielen per gat (gat = geen boog en geen profiel uit een eerdere run)
W=M.gewichten(c);RUN='Z36-02'
for fase,vg in M.fasen(c):
  w=M.Wereld(c,fase,RUN)
  bezet={b['positie'] for b in w.bestaand()}
  for i,pos in enumerate(M.POSITIES):
    if pos in bezet or c.execute('select 1 from verhaal_profiel where run=? and fase=? and positie=?',(RUN,fase,pos)).fetchone(): continue
    cands,_=M.pool(w,1500,hash((fase,pos))%10**6 if False else vg*100+i,None)
    cands=[p for p in cands if p['positie']==pos]
    eigen=[dict(zip(['code']+M.ASSEN,r)) for r in c.execute('select code,'+','.join(M.ASSEN)+' from verhaal_profiel where run=? and fase=?',(RUN,fase))]
    cands=[p for p in cands if all(M.afstand(p,e)>=3 for e in eigen)]
    for p in M.greedy(w,cands,3,W): S['profiel_'+RUN]+=M.bewaar(c,w,p,RUN,'positie vullen (dekking)')
c.commit();toets('stap 2 run Z36-02')
# run Z36-03: fase 4, twintig profielen (test van afstand en dekking)
w=M.Wereld(c,'4','Z36-03')
if not c.execute("select 1 from verhaal_profiel where run='Z36-03'").fetchone():
  cands,_=M.pool(w,4000,436,None)
  for p in M.farthest(w,cands,20,W): S['profiel_Z36-03']+=M.bewaar(c,w,p,'Z36-03','test fase 4 (20 profielen)')
c.commit();toets('stap 2 run Z36-03')
# run Z36-04: demo fase 6, erotische suspense (bewaard, zodat de ideeënbank hem kent)
dp=M.doelprofiel(c,'erotische suspense');w=M.Wereld(c,'6','Z36-04')
if not c.execute("select 1 from verhaal_profiel where run='Z36-04'").fetchone():
  cands,_=M.pool(w,4000,646,dp)
  gek=M.farthest(w,cands,10,W,dp);M.gevoeligheid(gek,W,dp)
  for p in gek: S['profiel_Z36-04']+=M.bewaar(c,w,p,'Z36-04','demo fase 6',dp)
c.commit();toets('stap 2 run Z36-04')
print('telling:',dict(S))
