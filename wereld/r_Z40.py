# Ronde Z40: besluiten na Z39, herstel ideeënbank, rem (schriftverbod), registerbereik, fase-overgang, module ziekte (Pest van 340).
# Gebouwd door de architect (de bouwer had geen credits meer); niet onafhankelijk getoetst: laat een tweede LLM Z40 keuren.
# Idempotent en additief; niets verwijderd; roman niet aangeraakt; toets.py na elke stap. Gebruik: DB=kopie.db python3 r_Z39.py [stappen]
import sqlite3,shutil,os,re,json,sys,collections,subprocess,random,math
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z39'),os.path.join(W,'z40')]
import afgeleid,migreer,sim,montecarlo as mc,tech,ziekte
import importlib.util as _iu
def _laad(naam,pad):
  s=_iu.spec_from_file_location(naam,pad);m=_iu.module_from_spec(s);s.loader.exec_module(m);return m
D=_laad('d39',os.path.join(W,'z39','data.py'))  # alleen D.R (naam van Rogier) wordt gebruikt
DT='2026-11-01';RD='Z40';RN=69;DB=os.environ.get('DB','canon.db')
STAPPEN=sys.argv[1:] or ['a','rem','overgang','ziekte','ideeen','proef','keuze']
if DB=='canon.db' and not os.path.exists('canon_backup_Z40.db'): shutil.copy('canon.db','canon_backup_Z40.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
REDEN='Ronde Z40: besluit van '+D.R+' (bevestigd in het gesprek met de architect, 2026-11-01)'
WREDEN='Ronde Z40: uit simulatie (verkenning, geen canon; BESLUIT-Z40-2)'
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z40.py')).rowcount
def toets(stap):
  afgeleid.bouw(c);c.commit()
  r=subprocess.run([sys.executable,'toets.py',DB,'--json',f'/tmp/toets_{RD}.json'],capture_output=True,text=True)
  print(f'[{stap}] toets exit {r.returncode}: '+' | '.join(l for l in r.stdout.splitlines()[1:4]))
  if r.returncode: print(r.stdout[-6000:]);sys.exit(f'toets faalt na {stap}')
def bestaat(code): return c.execute('select 1 from canon where code=?',(code,)).fetchone() is not None
def lev(x):
  for _ in range(6):
    r=c.execute('select status,vervangen_door from canon where code=?',(x,)).fetchone()
    if not r: return None
    if r[0] in('vastgesteld','voorlopig') or not r[1] or r[1].startswith('personage_profiel:'): return x
    x=r[1]
  return x
def nieuw(code,cat,ond,feit,verw,reden=REDEN,status='vastgesteld',kern=False,tijdperk=None,jaar=None,ideeenbank=0):
  if bestaat(code): return 0
  verw=';'.join(dict.fromkeys(y for y in (lev(x) for x in verw.split(';') if x) if y)) if verw else verw
  c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,draagkracht_handmatig,tijdperk,jaar,ideeenbank) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (code,cat,ond,feit,feit,reden,status,RN,verw or None,verw or None,'Kern' if kern else None,tijdperk,jaar,ideeenbank))
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
  if b and 'Opgelost in Z40' not in (b[0] or ''): zet('wrijving','code',code,'beschrijving',(b[0] or '')+' Opgelost in Z40: '+hoe)
def wrij_nieuw(code,titel,besch,verw):
  if c.execute('select 1 from wrijving where code=?',(code,)).fetchone(): return
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(titel,verw.replace(';',', '),besch,'canon','open',code,verw))
  S['wrijving_nieuw']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
def keuze(code,status,aanb_extra=None):
  r=c.execute('select aanbeveling from keuze where code=?',(code,)).fetchone()
  if not r: return
  if aanb_extra and aanb_extra not in (r[0] or ''): zet('keuze','code',code,'aanbeveling',(r[0] or '')+' '+aanb_extra)
  zet('keuze','code',code,'status',status)
def keuze_nieuw(code,soort,ond,aanb,raakt,citaat):
  if c.execute('select 1 from keuze where code=?',(code,)).fetchone(): return
  c.execute('insert into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',(code,soort,ond,aanb,raakt,'open','r_Z40.py',citaat))
  S['keuze_nieuw']+=1;wijz(code,'toegevoegd','keuze',None,'open')
def regel_nieuw(code,dom,oms,sq,bron,niveau):
  if c.execute('select 1 from regel where code=?',(code,)).fetchone(): return
  c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",(code,dom,oms,sq,bron,D.R,'actief',niveau))
  S['regel_nieuw']+=1;wijz(code,'toegevoegd','regel',None,niveau)
def opvolger(oud,nc,feit,extra_verw,reden):
  """Gewone opvolger: nieuwe levende rij met dezelfde status; de oude wijst ernaar."""
  r=c.execute('select categorie,onderwerp,verwijst_naar,status,tijdperk,jaar from canon where code=?',(oud,)).fetchone()
  if not r: return
  nieuw(nc,r[0],r[1],feit,(r[2] or '')+';'+extra_verw,reden=reden,status=r[3] if r[3] in('vastgesteld','voorlopig') else 'voorlopig',tijdperk=r[4],jaar=r[5]);vervang(oud,nc)
def profiel_opvolger(oud,nc,feit,reden):
  """Opvolger die meteen in personage_profiel staat (zoals D2 in Z37): de nieuwe rij is 'voorlopig, vervangen' door personage_profiel:nc."""
  r=c.execute('select categorie,onderwerp,verwijst_naar,tijdperk,jaar,vervangen_door,status from canon where code=?',(oud,)).fetchone()
  if not r or bestaat(nc): return
  c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,jaar,vervangen_door) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (nc,r[0],r[1],feit,feit,reden,'voorlopig, vervangen',RN,r[2],r[2],r[3],r[4],'personage_profiel:'+nc))
  S['canon_nieuw']+=1;wijz(nc,'toegevoegd','canon',None,'voorlopig, vervangen (personage_profiel:'+nc+')')
  if r[6] in('vastgesteld','voorlopig'): vervang(oud,nc)
  else: c.execute('update canon set vervangen_door=? where code=?',(nc,oud));wijz(oud,'vervangen','vervangen_door',r[5],nc)
def voeg_in(feit,zin):
  m=re.search(r'\s((?:Veiligheids)?[Ll]abel: )',feit)
  return feit[:m.start()]+' '+zin+feit[m.start():] if m else feit.rstrip()+' '+zin
def epi(code,e):
  c.execute("update canon set epistemiek=? where code=? and coalesce(epistemiek,'')=''",(e,code))
N=lambda r:f"simulatie ({r['run_id']}, seed {r['seed']})"
import statistics
E_BES='feit (besluit van Rogier, bevestigd in het gesprek met de architect op 2026-11-01)'
BZ40=[
('BESLUIT-Z40-1','Werkwijze','WRIJ-Z29-1 blijft open (romanwerk)',"Na Z39 blijft de kruipgang in h27 (WRIJ-Z29-1) open: dat lost Rogier op in de roman.",'BESLUIT-Z39-1;WRIJ-Z29-1'),
('BESLUIT-Z40-2','Werkwijze','Simulatie wordt nooit vanzelf canon',"Een rij met epistemiek 'simulatie' staat altijd in de ideeënbank (Kleur), tenzij een BESLUIT van Rogier haar via draagkracht_handmatig in de canon zet. afgeleid.py dwingt dit af (regel 7) en toets.py faalt erop (R-simulatie_in_canon). Herstelt de fout uit Z39, waar IDEE-Z39-1..10 door afgeleid.py van ideeenbank=1 naar 0 gingen.",'BESLUIT-Z39-5'),
('BESLUIT-Z40-3','Werkwijze','Kernbescherming in de simulatie blijft',"Canonpersonages leven in de simulatie tot hun canonjaar (SIM-kern). Alleen achtergrondfiguren en nieuwe kinderen kunnen eerder sterven.",'SIM-kern;REGEL-harde-grenzen'),
('BESLUIT-Z40-4','Geschiedenis','Het register bereikt de regio\'s langs de routes',"Het register ontstaat in Saelith en bereikt de andere regio's met reistijd (SIM-registerbereik). Zolang een regio niet bereikt is, stapelt daar het inteeltrisico op; zo kan de nevenramp in Groenmuil ontstaan (GEB-r10-neven-ramp).",'GEB-r10-eerste-register;GEB-r10-neven-ramp;KAART-seizoenen'),
('BESLUIT-Z40-5','Verhaal','Drie intrigevoorstellen worden een boog',"IDEE-Z39-4 (de koningsdochter in het register), IDEE-Z39-6 (Fenna en Ruben, de rustmaanden) en IDEE-Z39-7 (Orvath en Runa, de slikgangen) worden bogen in fase 4: VERHAAL-fase4-d-Z40, -e-Z40 en -f-Z40. IDEE-Z39-2 (Gunnar) is reserve. De andere blijven inspiratie in de ideeënbank.",'IDEE-Z39-4;IDEE-Z39-6;IDEE-Z39-7;IDEE-Z39-2'),
('BESLUIT-Z40-6','Geschiedenis','De rem op rooster en Orde is het schriftverbod',"Een rijksbreed rooster vraagt veel schrijvende handen, en schrijven is sinds het verbod (YSA-Z21-8, BESLUIT-Z17-9) een geheime kunst van de Zusters. Het rooster komt pas als genoeg vrouwen het geleerd hebben (SIM-schrijfsters). Ysa's verbod wordt zo de rem op de hele Noodtoestand.",'YSA-Z21-8;BESLUIT-Z17-9;GEB-r10-rotatie;GEB-r10-orde-naam'),
('BESLUIT-Z40-7','Werkwijze','Steekproef van 183 rijen per ronde',"De steekproef telt 183 rijen per ronde (Clopper-Pearson: bij 0 fouten is de 95%-bovengrens dan onder 2%). De architect leest daarna onafhankelijk mee.",'BESLUIT-Z33-1'),
('BESLUIT-Z40-8','Werkwijze','Eerst ziekte, dan economie; en een fase-overgang',"Validatie van de canon buiten fase 4: eerst de module ziekte met de Pest van 340 als test, daarna economie. Een volgende fase begint voortaan met de eindtoestand van de vorige (fase-overgang).",'GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh'),
]
BOGEN=[ # code, IDEE, onderwerp, feit, verwijst, boogvelden
('VERHAAL-fase4-d-Z40','IDEE-Z39-4','De koningsdochter in het register',
 "Isolde Edrunsdochter is negentien en weet dat Saske heeft gelogen over wie haar vader is. Om Saske voor te zijn klaagt ze Orvath de Moeras aan, die zijn beurten laat lopen voor een geroofde eilander. Saske slaat terug door Isoldes eigen blad open te leggen, en zo staat de dochter van de laatste koning ineens in het register waar ze zich voor verborg. Vorm: drie zittingen voor de Raad, aanklacht en verweer, en Isolde spreekt Saske aan in de jij-vorm.",
 'PER-f4-dochter-edrun;PER-f4-saske;PER-orvath;PER-f4-edrun;GEB-r10-laatste-koning;IDEE-Z39-4',
 dict(hoofdpersoon='Isolde Edrunsdochter',leeftijd_hoofdpersoon='19',geslacht_hoofdpersoon='v',romance='nee',erotische_sleutelscene='nee',terugkerend_motief='afkomst/verborgen blad',noodoplossing='werkt (met prijs)',wie_betaalt='Isolde (haar eigen blad) en Orvath',toon='koud, juridisch',vorm='drie zittingen: aanklacht, verweer, uitspraak',afloop='de dochter van de laatste koning staat in het register',verteller='Isolde, jij-vorm tegen Saske',tempo='drie zittingen in één week',beslisser_as='Isolde',betaler_as='Isolde en Orvath',vervalst_as='Saskes leugen over een vader',ontdekt_as='ja',schaal='stad',herkenbaar='je eigen geheim prijsgeven om een ander voor te zijn',zintuig='natte inkt op een blad dat iedereen mag lezen',haak='Wie haar vader is, staat nu zwart op wit, en het klopt niet.')),
('VERHAAL-fase4-e-Z40','IDEE-Z39-6','Rustmaanden voor een man zonder kinderen',
 "Fenna Rekenaarster schrijft rustmaanden in het rooster die niemand verdiend heeft. Ze merkt dat Ruben Gedeelde, beurt na beurt, nooit een kind verwekt. Laat ze dat staan, dan beschermt ze een onvruchtbare man die liever bij één geliefde blijft; meldt ze het, dan valt haar eigen gesjoemel mee om. Ze kiest voor Ruben en betaalt met de eerste vraag die Moeder Iris over het rooster stelt. Vorm: het rooster zelf, maand na maand, met doorhalingen.",
 'PER-f4-zuster-ondrea-leerling;PER-f4-gedeelde-man-ruben;PER-f4-orde-moeder-iris;GEB-r10-rotatie;GEB-r10-uitputting;IDEE-Z39-6',
 dict(hoofdpersoon='Fenna Rekenaarster',leeftijd_hoofdpersoon=None,geslacht_hoofdpersoon='v',romance='nee (Ruben houdt van een ander)',erotische_sleutelscene='nee',terugkerend_motief='rooster/rustmaanden',noodoplossing='faalt langzaam',wie_betaalt='Fenna',toon='teder en zakelijk',vorm='het rooster: kolommen en doorhalingen',afloop='Moeder Iris stelt de eerste vraag',verteller='het rooster (kolommen, kantlijn van Fenna)',tempo='twaalf maanden, één bladzijde per maand',beslisser_as='Fenna',betaler_as='Fenna',vervalst_as='rustmaanden die niemand verdiende',ontdekt_as='bijna',schaal='dorp',herkenbaar='een kleine regel breken om iemand te sparen',zintuig='potloodkrassen en een uitgeveegde naam',haak='Ruben verwekt nooit een kind, en zij weet waarom hij blijft.')),
('VERHAAL-fase4-f-Z40','IDEE-Z39-7','Slikgangen onder de mist',
 "Orvath de Moeras deelt met Runa van de Mist een bed en een geheim: de Oevrin hebben één op twee en geen Zegel. Runa wil haar eilanden buiten de rotatie houden en ziet in de slikgangen een schuilplaats voor mannen. Orvath weet dat de Orde zijn volk gaat leegroven zodra iemand die gangen ziet. Hun weigering en hun liefde kunnen niet allebei geheim blijven. Vorm: twee stemmen, om en om, boven water en onder water.",
 'PER-orvath;PER-f4-eiland-moeder-runa;GEB-r10-eilanden-weigering;UIT-VOLK-saelmor;IDEE-Z39-7',
 dict(hoofdpersoon='Orvath de Moeras',leeftijd_hoofdpersoon=None,geslacht_hoofdpersoon='m',romance='ja',erotische_sleutelscene='aangeduid (volwassen en kiezend)',terugkerend_motief='verborgen volk/slikgangen',noodoplossing='open',wie_betaalt='de Oevrin, als het uitkomt',toon='broeierig, dreigend',vorm='twee stemmen om en om, boven en onder water',afloop='open: de weigering of de liefde',verteller='Orvath en Runa, afwisselend',tempo='één zomer, van springtij tot springtij',beslisser_as='Runa',betaler_as='de Oevrin',vervalst_as='niets (verzwegen)',ontdekt_as='nee',schaal='wereld',herkenbaar='een liefde die een volk kan verraden',zintuig='slik tot de knieën, zout op de huid',haak='De Oevrin hebben één man op twee en geen Zegel.')),
]
def stap_a():
  for code,cat,ond,feit,verw in BZ40: nieuw(code,cat,ond,feit,verw);epi(code,E_BES)
  regel_nieuw('R-simulatie_in_canon','simulatie',"Een levende canonrij met epistemiek 'simulatie' staat in de ideeënbank, tenzij een BESLUIT haar via draagkracht_handmatig in de canon zet (BESLUIT-Z40-2).",'py:simulatie_in_canon','BESLUIT-Z40-2','fout')
  for code,idee,ond,feit,verw,bv in BOGEN:
    if nieuw(code,'Verhaal',ond,feit,verw,reden=REDEN+' (BESLUIT-Z40-5)',status='voorlopig',tijdperk='4 Noodtoestand'):
      c.execute("update canon set draagkracht_handmatig='Structuur' where code=?",(code,))
    epi(code,'simulatie (Z39-F4-0203, seed 390203); boog gemaakt door BESLUIT-Z40-5')
    vervang(idee,code)
    if not c.execute('select 1 from boog where code=?',(code,)).fetchone():
      kol=['code','fase','boek','bron','status','synopsis_code']+list(bv)
      c.execute(f"insert into boog({','.join(kol)}) values({','.join('?'*len(kol))})",[code,'4 Noodtoestand','fasebogen',code+'; '+idee,'voorlopig (BESLUIT-Z40-5)',code]+list(bv.values()))
      S['boog_nieuw']+=1;wijz(code,'toegevoegd','boog',None,'voorlopig')
  keuze('KEUZE-WRIJ-Z29-1','open','[Z40: blijft open, romanwerk (BESLUIT-Z40-1).]')
  for k,b in (('KEUZE-Z39-kernbescherming','BESLUIT-Z40-3'),('KEUZE-Z39-nevenramp','BESLUIT-Z40-4'),('KEUZE-Z39-premisses','BESLUIT-Z40-5'),('KEUZE-Z39-tijdlijn','BESLUIT-Z40-6'),('KEUZE-Z39-steekproef','BESLUIT-Z40-7'),('KEUZE-Z39-validatie','BESLUIT-Z40-8')):
    keuze(k,'besloten',f'[Z40: {b}]')
  # scorekaart Z39: de niet-ingevulde regel herstellen (getal uit z39/tech_rapport.json)
  sk='scorekaart_Z39.md'
  if os.path.exists(sk):
    t=open(sk,encoding='utf-8').read();v=json.load(open('z39/tech_rapport.json'))['makerskennis_vergeten_in_alle_regios_%']
    if "{T['makerskennis_vergeten_in_alle_regios_%']}" in t:
      open(sk,'w',encoding='utf-8').write(t.replace("{T['makerskennis_vergeten_in_alle_regios_%']}",str(v)));S['scorekaart_Z39_hersteld']+=1
  c.commit()
# ================= REM: schriftverbod + registerbereik, Monte Carlo fase 4 =================
ZREG=[('SIM-schrijfsters','personen',"Schrijven is een geheime kunst van de Zusters (schriftverbod, YSA-Z21-8). In jaar 0 kunnen 3 Zusters schrijven; elke schrijfster leidt gemiddeld één leerling op per 20 jaar (maximaal 300). Een rijksbreed rooster vraagt 40 schrijfsters.",'start;opleiding;max;rooster','3;20;300;40','YSA-Z21-8;BESLUIT-Z17-9;BESLUIT-Z40-6',1),
      ('SIM-registerbereik','personen',"Het register ontstaat in Saelith en bereikt een buurregio met kans 0,25 per lente, gedeeld door de reistijd, als er twee schrijfsters per bereikte regio zijn. Tot een regio bereikt is, stapelt daar het inteeltrisico op.",'spreiding;schrijfsters_per_regio','0.25/reistijd;2','GEB-r10-eerste-register;BESLUIT-Z40-4',1)]
def zaai(regels):
  for code,mod,oms,par,waarde,bron,aann in regels:
    S['sim_regel']+=c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
      (code,mod,oms,par,waarde,bron,aann,None,None,'voorlopig',f'aanname (parameter gekozen in Z40; bron {bron})' if aann else f'feit (regel uit canon {bron})')).rowcount
def run_rem(basis,n,prefix,opleiding=sim.SCHRIJF_OPLEIDING,fase_nr=4,fase=sim.FASE,begin=None):
  T=mc.typen(c);P=sim.seed_personen(c,fase_nr);R=[]
  for i in range(n):
    w=sim.Wereld(basis+i,P,T,None,True,fase,False,rem=True,bereik=True,begin=begin);w.opleiding=opleiding;w.run()
    f=sim.invarianten(w);h=sim.canon_hits(w);eerst={}
    for e in w.ev:
      if e[7] in mc.CANON and e[7] not in eerst: eerst[e[7]]=e[0]
    sc=sim.score(w,h);sc.update({'opleiding':opleiding,'schrijvers_eind':w.schrijvers,'register_bereik':w.reg_bereik,'herhaald_ingesteld':sum(1 for e in w.ev if e[2]=='wet' and e[7] in('GEB-deelwet-40','GEB-r10-eerste-register'))})
    R.append({'run_id':f'{prefix}-{i:04d}','seed':basis+i,'uitkomst':mc.uitkomst(w),'geldig':0 if f else 1,'reden':'; '.join(f) or None,'scores':sc,'hits':h,'eerst':eerst,'stem':w.stem,'_w':w})
  return R
def bewaar(R,module,fase_nr,gekozen=(),bron='r_Z40.py'):
  for r in R:
    sc={k:v for k,v in r['scores'].items()}
    S['sim_run']+=c.execute('insert or ignore into sim_run(run_id,module,fase_nr,seed,geldig,reden,n_gebeurtenis,scores,pareto_rang,gewogen,gekozen,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (r['run_id'],module,fase_nr,r['seed'],r['geldig'],r['reden'],sc.get('gebeurtenissen',0),json.dumps(sc,ensure_ascii=False,default=str),r.get('pareto_rang'),r.get('gewogen'),1 if r['run_id'] in gekozen else 0,bron,N(r))).rowcount
def ev_opslaan(r,w,module):
  for (j,sz,typ,a,d,plek,det,cc,oz) in w.ev:
    S['sim_gebeurtenis']+=c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (r['run_id'],module,j,sz,typ,a,d or '-',sim.REG.get(plek,plek) if plek else None,det or '-',cc,'voorlopig',N(r),oz)).rowcount
def stap_rem():
  zaai(ZREG);c.commit()
  if c.execute("select count(*) from sim_run where module='personen_z40'").fetchone()[0]>=1000: return
  R=run_rem(400000,1000,'Z40-F4R');top=mc.pareto(R);ids={r['run_id'] for r in top}
  bewaar(R,'personen_z40',4,ids)
  for r in top: ev_opslaan(r,r['_w'],'personen_z40')
  V=mc.validatie(R)
  ramp=round(100*sum('ramp_groenmuil' in r['_w'].wet for r in R if r['geldig'])/sum(r['geldig'] for r in R),1)
  gev={}
  for opl in (15,25,30):
    R2=run_rem(400000,200,f'Z40-F4R-O{opl}',opleiding=opl);bewaar(R2,'personen_z40_gevoeligheid',4)
    G=[r for r in R2 if r['geldig']]
    med=lambda k:statistics.median([r['eerst'][k] for r in G if k in r['eerst']]) if any(k in r['eerst'] for r in G) else None
    gev[opl]={'rotatie_mediaan':med('GEB-r10-rotatie'),'orde_mediaan':med('GEB-r10-orde-naam'),'nevenramp_%':round(100*sum('ramp_groenmuil' in r['_w'].wet for r in G)/len(G),1),'geldig':len(G)}
  json.dump({'validatie':V,'nevenramp_groenmuil_%':ramp,'gevoeligheid_opleiding':gev,'top':[(r['run_id'],r['seed'],r['pareto_rang'],r['gewogen']) for r in top],
             'weggegooid':collections.Counter((r['reden'] or '').split(':')[0] for r in R if not r['geldig'])},open('z40/mc_fase4_rem.json','w'),ensure_ascii=False,indent=1,default=str)
  json.dump({'eind':sim.eindtoestand(top[0]['_w']),'run':top[0]['run_id']},open('z40/eind_fase4.json','w'),ensure_ascii=False,indent=1,default=str)
  c.commit()
# ================= OVERGANG: fase 5 begint met de eindtoestand van fase 4 =================
def stap_overgang():
  if c.execute("select count(*) from sim_run where module='personen_z40_f5'").fetchone()[0]>=50: return
  fz=c.execute("select waarde,toelichting from anker where sleutel='fase_5_naam'").fetchone()
  a,b=map(int,re.search(r'\((\d+) tot (\d+)\)',fz[1]).groups())
  eind=json.load(open('z40/eind_fase4.json'))['eind']
  R=run_rem(406000,50,'Z40-F5O',fase_nr=5,fase=(a,b),begin=eind)
  if any(r['geldig'] for r in R): mc.pareto(R)
  bewaar(R,'personen_z40_f5',5)
  G=[r for r in R if r['geldig']]
  z39=c.execute("select count(*) from sim_gebeurtenis where module='personen' and run_id like 'Z39-F5%' and type_code='wet'").fetchone()[0]
  json.dump({'fase':(a,b),'begin_van':json.load(open('z40/eind_fase4.json'))['run'],'geldig':len(G),'weggegooid':collections.Counter((r['reden'] or '').split(':')[0] for r in R if not r['geldig']),
             'deelwet_of_register_opnieuw_ingesteld_runs':sum(1 for r in G if r['scores']['herhaald_ingesteld']),
             'instituten_bij_start':eind['wet'],'gem':{k:round(sum(r['scores'][k] for r in G)/max(1,len(G)),2) for k in ('intrige','ommekeer','verbinding','gebeurtenissen')}},
            open('z40/overgang_fase5.json','w'),ensure_ascii=False,indent=1,default=str)
  c.commit()
# ================= ZIEKTE: de Pest van 340 =================
ZTYPEN=[('index','ziekte','Het eerste geval ontstaat in de stallen van Hal-Neth.','geen sterfte vóór het indexgeval','GEB-r10-pest-oorsprong'),
        ('besmetting_regio','ziekte','De koorts bereikt een regio.','alleen via een route met een besmette regio','GEB-pest-340'),
        ('sterfte','ziekte','Mannen sterven aan de koorts (telling per regio en maand).','telling klopt per regio (S+E+I+R+D = mannen)','GEB-pest-340'),
        ('route_dicht','ziekte','Qesh sluit de karavaanroutes.','na het gerucht','GEB-r10-pest-qesh')]
def stap_ziekte():
  zaai([(f'ZIEKTE-{k}','ziekte',f'{k}: {v[1]}',k,str(v[0]),'GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh',v[2]) for k,v in ziekte.P.items()]+
       [('ZIEKTE-mannen','ziekte','Mannen per regio vóór de Pest (aanname; Hal-Neth apart).','mannen',json.dumps(ziekte.MANNEN),'FASE-markt;REG-overzicht',1),
        ('ZIEKTE-koppeling','ziekte','Contact per maand tussen regio\'s (rotatiekringen, karavaan; afgesloten stallen).','koppeling',json.dumps({f'{a}-{b}':v for (a,b),v in ziekte.BUUR.items()}),'GEB-r10-rotatie;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh',1),
        ('ZIEKTE-alleen-mannen','ziekte','Alleen mannen worden ziek (aanname op GEB-pest-340: de koorts zit in de mannenvertrekken).','vatbaar','mannen','GEB-pest-340',1)])
  for t in ZTYPEN:
    S['tech_gebeurtenistype']+=c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',('ziekte_'+t[0],t[1],t[2],t[3],t[4],'aanname (moduleontwerp Z40, bron '+t[4]+')')).rowcount
  c.commit()
  if c.execute("select count(*) from sim_run where module='ziekte'").fetchone()[0]>=1000: return
  R=ziekte.draai(1000,basis=402000);R0=ziekte.draai(200,basis=402000,sluit=False,prefix='Z40-ZIEKTE-OPEN')
  ont=[r for r in R if r['geldig'] and r['scores']['sterfte_mannen']>=0.10]
  kand=[r for r in ont if r['scores']['sterfte_qesh']<0.5*r['scores']['sterfte_rest']] or ont
  best=min(kand,key=lambda r:(abs(r['scores']['index_jaar']-338)+abs(r['scores']['piekjaar']-340),abs(r['scores']['sterfte_mannen']-1/3),r['seed'])) if kand else None
  bewaar(R,'ziekte',6,{best['run_id']} if best else set());bewaar(R0,'ziekte_zonder_sluiting',6)
  gev={}
  base=dict(ziekte.P)
  for cfr in (0.3,0.5):
    ziekte.P['cfr']=(cfr,)+base['cfr'][1:];R2=ziekte.draai(200,basis=407000,prefix=f'Z40-ZIEKTE-CFR{int(cfr*100)}');bewaar(R2,'ziekte_gevoeligheid',6)
    gev[f'cfr {cfr}']={k:ziekte.validatie(R2)[k] for k in ('ontsnapt_uit_halneth_%','bij_ontsnapping_sterfte_mediaan','bij_ontsnapping_een_derde_%')}
  ziekte.P.clear();ziekte.P.update(base)
  if best:
    for (j,m,typ,k,o,n,cc) in best['ev']:
      S['sim_gebeurtenis']+=c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (best['run_id'],'ziekte',j,f'maand {m+1}','ziekte_'+typ,k,o or '-',k,(f'{n} man' if n==1 else f'{n} mannen') if n else '-',cc,'voorlopig',N(best),'ZIEKTE-'+('ontstaan' if typ=='index' else 'beta'))).rowcount
  json.dump({'validatie':ziekte.validatie(R,R0),'gevoeligheid':gev,'gekozen':best['run_id'] if best else None,'gekozen_scores':best['scores'] if best else None},open('z40/ziekte.json','w'),ensure_ascii=False,indent=1,default=str)
  c.commit()
# ================= PROEF: steekproef van 183 =================
def stap_proef():
  if c.execute("select count(*) from steekproef where ronde='Z40'").fetchone()[0]: return
  per=set(x for (x,) in c.execute('select code from personage_profiel'))
  codes=set(x for (x,) in c.execute('select code from canon'))
  pool=[('canon',r) for r in c.execute("select code,feit,verwijst_naar,epistemiek from canon where ronde=?",(RN,))]
  pool+=[('sim_regel',r) for r in c.execute("select code,bron_code,aanname,epistemiek from sim_regel where code like 'SIM-schrijf%' or code like 'SIM-registerb%' or code like 'ZIEKTE-%'")]
  pool+=[('boog',r) for r in c.execute("select code,synopsis_code,fase from boog where code like '%-Z40'")]
  pool+=[('sim_gebeurtenis',r) for r in c.execute("select id,run_id,module,jaar,type_code,actor,doel,canon_code,epistemiek from sim_gebeurtenis where run_id like 'Z40-%'")]
  pool+=[('sim_run',r) for r in c.execute("select run_id,module,seed,geldig,reden,epistemiek from sim_run where run_id like 'Z40-%'")]
  # gelaagd: alle nieuwe canonrijen, bogen en regels altijd; de rest van de 183 willekeurig uit de simulatierijen
  vast=[x for x in pool if x[0] in('canon','boog','sim_regel')];rest=[x for x in pool if x[0] not in('canon','boog','sim_regel')]
  rnd=random.Random(40);sample=vast+rnd.sample(rest,max(0,min(183-len(vast),len(rest))))
  for t,row in sample:
    if t=='canon': code,feit,verw,ep=row;p=bool(feit);g=True;v=all(x in codes for x in (verw or '').split(';') if x) and bool(ep)
    elif t=='sim_regel': code,bron,aann,ep=row;p=bool(bron);g=True;v=all(x in codes for x in bron.split(';') if x);
    elif t=='boog': code,syn,fase=row;p=fase.startswith('4');g=True;v=syn in codes
    elif t=='sim_gebeurtenis':
      i,run,mod,j,typ,a,d,cc,ep=row;code=f'sim_gebeurtenis:{i}'
      p=(330<=j<=350) if mod=='ziekte' else (-3<=j<=340);g=True;v=(cc is None or cc in codes or (cc.startswith('personage_profiel:') and cc.split(':',1)[1] in per)) and 'seed' in (ep or '') and run in (ep or '')
      if mod!='ziekte': v=v and (a in per or a in ('RAAD','MANNEN','DORP','REGISTER') or a.startswith('SIMF') or a in codes)
    else: code,mod,seed,geldig,reden,ep=row;p=geldig in(0,1);g=True;v=str(seed) in (ep or '')
    ok=p and g and v
    S['steekproef']+=c.execute('insert or ignore into steekproef(ronde,tabel,code,past,geen_sjabloon,verbinding,oordeel,toelichting,epistemiek) values(?,?,?,?,?,?,?,?,?)',
      ('Z40',t,str(code),int(p),int(g),int(v),'goed' if ok else 'fout','automatisch oordeel (r_Z40.stap_proef); canonrijen, bogen en regels daarna gelezen door de architect','aanname (architect is in Z40 ook bouwer: niet onafhankelijk)')).rowcount
  c.commit()
# ================= KEUZE =================
def stap_keuze():
  rem=json.load(open('z40/mc_fase4_rem.json'));zk=json.load(open('z40/ziekte.json'));ov=json.load(open('z40/overgang_fase5.json'))
  V=rem['validatie'];zv=zk['validatie']
  K=[('KEUZE-Z40-rem','simulatie','De rem helpt, maar haalt jaar 78 niet',
      f"Met het schriftverbod als rem valt het rooster in mediaan jaar {V['GEB-r10-rotatie']['mediaan']} (zonder rem 51, canon 78) en de Orde in jaar {V['GEB-r10-orde-naam']['mediaan']} (canon 90). Gevoeligheid (leertijd per leerling): {json.dumps({k:v['rotatie_mediaan'] for k,v in rem['gevoeligheid_opleiding'].items()})}.",
      "Twee mogelijkheden: (a) de leertijd is langer dan 20 jaar (dan past jaar 78 bij ongeveer 30 jaar per leerling: één leerling per loopbaan); (b) er is nog een tweede rem (bijvoorbeeld het verzet van Ambergaard of de mannenroof). Aanbeveling: (a), één leerling per loopbaan, want dat past bij een geheime kunst. Rogier kiest.",'SIM-schrijfsters;GEB-r10-rotatie'),
     ('KEUZE-Z40-pest','simulatie','De Pest ontstaat alleen als de koorts uit Hal-Neth ontsnapt',
      f"Met afgesloten stallen ontsnapt de koorts in {zv['ontsnapt_uit_halneth_%']}% van de runs. Als ze ontsnapt, sterft {zv.get('bij_ontsnapping_sterfte_mediaan')} van de mannen (een derde in {zv.get('bij_ontsnapping_een_derde_%')}%), met {zv.get('bij_ontsnapping_vertraging_index_tot_piek_mediaan')} jaar tussen eerste koorts en piek (canon: 338 tot 340). Qesh blijft er grotendeels buiten in {zv.get('bij_ontsnapping_qesh_lager_dan_half_%')}% van die runs. Het jaar valt 2 tot 3 jaar vroeg (indexjaar mediaan {zv['indexjaar_mediaan']}).",
      "De canon klopt met het model als de stallen echt afgesloten waren en de koorts één keer naar buiten kwam. Dat is een verhaal: wie liet haar ontsnappen? (Saskia's rapport, VERHAAL-fase6). Aanbeveling: vastleggen als bevinding, en het moment van ontsnappen als zaadje voor fase 6.",'GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh'),
     ('KEUZE-Z40-qesh','simulatie','Qesh ontsnapt alleen als het vroeg sluit',
      f"Zonder sluiting sterft in Qesh {zv.get('bij_ontsnapping_qesh_sterfte_zonder_sluiting_mediaan')} van de mannen, met sluiting {zv.get('bij_ontsnapping_qesh_sterfte_met_sluiting_mediaan')}. Sluiten helpt alleen als Qesh dicht gaat vóór de koorts de karavaan bereikt.",
      "Aanbeveling: Qesh sloot op het eerste gerucht, niet op de doden. Dat past bij GEB-r10-qesh-afwijking (Qesh is anders) en geeft een vraag voor later: wie waarschuwde Qesh zo vroeg?",'GEB-r10-pest-qesh'),
     ('KEUZE-Z40-bogen','verhaal','Drie nieuwe bogen in fase 4 bevestigen',
      "VERHAAL-fase4-d-Z40 (Isolde, drie zittingen), -e-Z40 (Fenna, het rooster als verteller) en -f-Z40 (Orvath en Runa, twee stemmen boven en onder water) staan voorlopig, met vorm, verteller en tempo ingevuld door de architect.",
      "Bevestig de vormen of geef een andere. Leeftijd van Fenna en Orvath staat niet in de canon en is leeg gelaten.",'VERHAAL-fase4-d-Z40;VERHAAL-fase4-e-Z40;VERHAAL-fase4-f-Z40'),
     ('KEUZE-Z40-onafhankelijk','controle','Z40 is gebouwd door de architect zelf',
      "De bouwer had geen credits; de architect bouwde Z40 en keurde het zelf. Dat breekt de regel 'één bouwt, de ander toetst'.",
      "Laat de andere LLM Z40 keuren zodra die weer kan: dezelfde 8 metingen, een eigen steekproef van 183 en een eigen koude lezer.",'BESLUIT-Z40-7')]
  for code,soort,ond,citaat,aanb,raakt in K: keuze_nieuw(code,soort,ond,aanb,raakt,citaat)
  c.commit()

# ================= IDEEEN: nieuwe premisses uit de Z40-runs (ideeënbank, epistemiek simulatie) =================
IDEEEN=[
('IDEE-Z40-1','Zes maanden achter de muur','Z40-ZIEKTE-0271',402271,
 "In de zomer van 338 krijgt één man in de afgesloten stallen van Hal-Neth koorts. Zes maanden blijft ze binnen de muren; in de winter is ze in Saelith. Machteld vlucht uit Hal-Neth om te vertellen wat ze zag, en pas als de eerste mannen in Saelith sterven, begrijpt ze dat zij de koorts naar buiten droeg.",
 'GEB-r10-pest-oorsprong;GEB-pest-340;THRL-fase6-builen-Z32;PER-f6-machteld'),
('IDEE-Z40-2','Wie waarschuwde Qesh?','Z40-ZIEKTE-0271',402271,
 "Qesh sluit de karavaanroutes in de eerste maand van 339, voordat er buiten Hal-Neth één man is gestorven. Iemand bracht het gerucht. De karavaanvrouw die het deed, staat met haar eigen mannen buiten de poort die ze zelf liet sluiten, en Qesh wordt machtig door een daad die het nooit zal erkennen.",
 'GEB-r10-pest-qesh;GEB-pest-340;STAD-qesh'),
('IDEE-Z40-3','De laatste leerling','Z40-F4R-0931',400931,
 "Schrijven is een geheime kunst, en elke schrijfster leert in haar leven maar één leerling. Saske vervalst dertig jaar lang bladen in het register, en het rijksrooster komt pas als er genoeg handen zijn die schrijven. De laatste leerling die het rooster mogelijk maakt, is ook de eerste die kan lezen wat Saske veranderde.",
 'PER-f4-saske;GEB-r10-rotatie;VALS-noodtoestand;YSA-Z21-8;BESLUIT-Z40-6'),
('IDEE-Z40-4','Twee jaar te laat in Groenmuil','Z40-F4R-0931',400931,
 "Het register bereikt Groenmuil twee jaar na de ramp in het dorp van de neven. Er waren te weinig vrouwen die konden schrijven om er eerder een te sturen. De Zuster die eindelijk aankomt, schrijft de eerste misvormde kinderen in, en weet dat het verbod van de godin hen zo heeft gemaakt.",
 'GEB-r10-neven-ramp;GEB-r10-eerste-register;PER-f4-grauwe-heske;VOLK-grauwen;BESLUIT-Z40-4'),
('IDEE-Z40-5','Tine en de man die weigert','Z40-F4R-0931',400931,
 "Zuster Tine vervalst in Ambergaard bladen voor wie haar betaalt, en klaagt tegelijk Halvar de Gedeelde aan omdat hij zijn beurten weigert. Halvar weet welke bladen niet kloppen. Hij kan haar breken, maar dan breekt hij ook de vrouwen die haar betaalden om een kind te mogen krijgen van wie ze wilden.",
 'PER-f4-registerzuster-tine;PER-halvar;VALS-noodtoestand;GEB-deelwet-40'),
]
def stap_ideeen():
  for code,ond,run,seed,txt,verw in IDEEEN:
    nieuw(code,'Verhaal',ond,txt,verw,reden=WREDEN+' (premisse met de hand geschreven door de architect uit de gebeurtenissen van '+run+')',status='voorlopig',tijdperk='4 Noodtoestand' if 'F4R' in run else '6 Markt',ideeenbank=1)
    epi(code,f'simulatie ({run}, seed {seed}); premisse met de hand geschreven door de architect')
  c.commit()
if __name__=='__main__':
  for st in STAPPEN:
    fn=globals().get('stap_'+st)
    if fn: fn();toets(st)
  print(dict(S))
