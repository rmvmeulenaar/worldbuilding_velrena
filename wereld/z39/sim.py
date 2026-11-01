"""Z39 11b: personenmotor voor fase 4 Noodtoestand (jaar 0-130), seizoensstappen, reproduceerbaar via seed.
Harde lijnen zitten IN de motor: laad_typen() weigert elk type met harde_lijn_risico; doe() weigert minderjarigen buiten
geboorte/opvoeding/erfenis en weigert verbintenis zonder instemming van twee volwassenen. Er bestaat geen seksueel gebeurtenistype:
geboorte volgt uit een verbintenis of een aanvaarde rotatiebeurt (beide met instemming van twee volwassenen).
Regionale bevolking is een telling (geen agenten); benoemde personages komen uit personage_profiel (fase_nr=4).
Achtergrondfiguren worden pas gemaakt als een run ze nodig heeft (kind, geroofde man)."""
import random,math,json,collections,re,zlib
FASE=(0,130);SZ=('lente','zomer','herfst','winter')
REG={'saelith':'REG-saelith','ambergaard':'REG-ambergaard','zoutkust':'REG-zoutkust','groenmuil':'REG-groenmuil','stille':'REG-stille','hoogvrouwe':'REG-hoogvrouwe'}
# reistijd in seizoenen (aanname op REG-overzicht en KAART-seizoenen); winter: Amberpas dicht; lente: delta (saelith) onbegaanbaar
BUUR={('saelith','ambergaard'):1,('saelith','zoutkust'):1,('saelith','groenmuil'):2,('zoutkust','groenmuil'):1,('zoutkust','stille'):1,('ambergaard','hoogvrouwe'):1,('saelith','stille'):2}
def reis(a,b):
  if a==b: return 0
  return BUUR.get((a,b)) or BUUR.get((b,a))
def dicht(a,b,sz):
  if sz=='winter' and 'ambergaard' in (a,b) and 'hoogvrouwe' in (a,b): return True
  if sz=='lente' and 'saelith' in (a,b): return True
  return False
MANNEN={'PER-halvar','PER-orvath','PER-f4-edrun','PER-f4-veerman-dries','PER-f4-gedeelde-man-ruben','PER-f4-clan-rover-gunnar','PER-f4-vathren-kerl','PER-f4-kluwer-zzak','PER-nood-grauwen-V5'}
ZUSTERS_W=('Zusters','Orde','Stille Zusters')
def wilsoort(w):
  w=(w or '').lower()
  for k,pat in (('vrijheid',r'laten kiezen|vrij van|niet meer geroofd|erkend'),('liefde',r'liefhebben|kiezen|houden|leven met|man,'),('register',r'controle|rooster|werk goed'),
                ('bescherming',r'beschermen|veilig'),('waarheid',r'weten|waarheid|waarschuwen'),('macht',r'kerk'),('handel',r'ruilen'),('overleven',r'overleven|voeden|bevolken|bestaan|rustig|plek|van hem')):
    if re.search(pat,w): return k
  return 'overleven'
REGELS=[ # code, omschrijving, parameter, waarde, bron, aanname, van, tot
 ('SIM-verhouding','Van de verwekte zonen wordt ongeveer één op honderd geboren (X-filter, Zegel).','p_zoon','0.01','GAVE-VERHOUDINGEN-Z38',0,0,None),
 ('SIM-gave','Een geboren zoon krijgt de gave met kans 1 op 20 bij een gaven-vader, 1 op 2000 bij een gewone vader.','p_gave','0.05;0.0005','GAVE-VERHOUDINGEN-Z38',0,0,None),
 ('SIM-levensduur','Sterftekans per jaar volgt een Gompertz-curve rond de levensduur van het volk (mens 70: aanname; aelthir 900).','levensduur','mens=70;aelthir=900','ANKER:levensduur',1,None,None),
 ('SIM-deelwet','Als mannen schaars worden, kan de Registratrix de Deelwet afkondigen: één man voor vele vrouwen (vrouwen per man per jaar 1 -> 8).','last','1->8','GEB-deelwet-40',0,None,None),
 ('SIM-weigeren','Een vrouw mag een beurt weigeren (rang kost het); een man in een verbintenis die een beurt weigert, krijgt ruzie met het register. Geen beurt zonder instemming van beide volwassenen (harde lijn).','instemming','2 volwassenen','WET-wie-weigert;REGEL-harde-grenzen',0,None,None),
 ('SIM-uitputting','Last boven 3 geboorten per man per jaar verhoogt de sterftekans van mannen.','extra_sterfte','0.04 per last-eenheid boven 3','GEB-r10-uitputting',1,None,None),
 ('SIM-rotatie','Na uitputtingsdoden kan een rekenaarster een rooster invoeren: last gespreid, extra sterfte gehalveerd.','rotatie','last/2','GEB-r10-rotatie',0,None,None),
 ('SIM-roof','Een clan met minder mannen per vrouw dan een buurregio kan mannen roven; dat zet een vete.','roof','clanleidster levend','GEB-r10-mannenroof',0,None,None),
 ('SIM-register','Na genoeg vetes publiceren de Zusters een register; wie het register leest, weet wie wiens kind is.','register','vetes>=3','GEB-r10-eerste-register;FASE-noodtoestand',0,None,None),
 ('SIM-registertoegang','Alleen Zusters (later Orde) lezen het register; zij leren de geheimen van wie geregistreerd is.','toegang','Zusters','ERF-noodtoestand',0,None,None),
 ('SIM-inteelt','In een regio zonder register en met weinig mannen stapelt verwantschapsrisico op; boven de drempel volgt een inteeltramp.','risico','drempel 1.0','GEB-r10-neven-ramp',1,None,None),
 ('SIM-jongenshof','Zonen worden vanaf de stichting van het Jongenshof daar opgevoed (strikt niet-seksueel).','jongenshof','na register','GEB-r10-jongenshof;RIT-hofproef',0,None,None),
 ('SIM-orde','Met register en rooster kan een Moeder de Zusters tot Orde maken.','orde','register+rotatie','GEB-r10-orde-naam',0,None,None),
 ('SIM-eilanden','De Nevel-eilanden weigeren de rotatie zolang hun eilandmoeder leeft.','weigering','Runa levend','GEB-r10-eilanden-weigering',0,None,None),
 ('SIM-reistijd','Reizen kost 1-2 seizoenen tussen buurregio\'s; winter sluit de Amberpas, lente maakt de delta onbegaanbaar.','reistijd','seizoenen','KAART-seizoenen;REG-overzicht',1,None,None),
 ('SIM-raad','Raad der Moeders (jaar -3): 12 stemmen; Zusters stemmen meestal voor, eilandvrouwen meestal tegen.','raad','5 Zusters p=.85; 4 eiland p=.35; 3 Lisk p=.5','GEB-r10-raad-der-moeders;BESLUIT-Z3-WRIJ-055',1,-3,-3),
 ('SIM-varenne','Varenne-krediet en de Zaadbeurs bestaan pas vanaf 455; niet actief in fase 4.','krediet','uit','GEB-zaadbeurs-455',0,455,None),
 ('SIM-kern','De motor overschrijft geen Kern: canonpersonages zijn in hun canonjaar in leven (anker-invariant), canonjaren worden niet verschoven.','kern','invariant','REGEL-harde-grenzen;BESLUIT-Z30-4',0,None,None),
]
TYPEN=[ # code, omschrijving, min_leeftijd, minderjarige_rol, instemming, risico, bron
 ('geboorte','Een kind wordt geboren (uit een verbintenis of aanvaarde beurt).',0,'kind',0,0,'SIM-verhouding'),
 ('opvoeding','Een kind gaat naar een opvoedplek (Jongenshof, moederhuis); strikt niet-seksueel.',0,'kind',0,0,'SIM-jongenshof'),
 ('erfenis','Een kind of volwassene erft bij een dood.',0,'erfgenaam',0,0,'FASE-noodtoestand'),
 ('verbintenis','Twee volwassenen kiezen elkaar (huwelijk, geliefden); beide stemmen in.',18,None,1,0,'SIM-weigeren'),
 ('beurt_geweigerd','Een volwassene weigert een rotatiebeurt.',18,None,0,0,'SIM-weigeren'),
 ('schuld','Iemand raakt schuldig aan een ander (gunst, geld, zwijgen).',18,None,0,0,'FASE-noodtoestand'),
 ('chantage','Iemand gebruikt een geheim van een ander dat hij kent en kan bereiken.',18,None,0,0,'SIM-registertoegang'),
 ('verraad','Iemand verraadt een ander (geheim aan register, aanklacht).',18,None,0,0,'FASE-noodtoestand'),
 ('geheim_lekt','Een geheim gaat over naar iemand in dezelfde regio.',18,None,0,0,'SIM-registertoegang'),
 ('registerinzage','Een Zuster leest het register en leert geheimen.',18,None,0,0,'SIM-registertoegang'),
 ('vervalsing','Een registerhoudster vervalst een blad.',18,None,0,0,'VALS-noodtoestand'),
 ('ruzie','Twee volwassenen krijgen ruzie; rivaliteit.',18,None,0,0,'FASE-noodtoestand'),
 ('eed','Iemand zweert trouw aan een leidster.',18,None,0,0,'FASE-noodtoestand'),
 ('migratie','Iemand verhuist naar een buurregio (reistijd).',18,None,0,0,'SIM-reistijd'),
 ('roof','Een clan rooft een volwassen man uit een buurregio.',18,None,0,0,'SIM-roof'),
 ('dood','Iemand sterft.',0,'kind',0,0,'SIM-levensduur'),
 ('wet','Een regel van de wereld verandert (Deelwet, register, rooster, Orde, Jongenshof, weigering).',18,None,0,0,'FASE-noodtoestand'),
 ('raadstemming','Raad der Moeders stemt over de Zegel (jaar -3).',18,None,0,0,'SIM-raad'),
]
# Z40 parameters (aannames, BESLUIT-Z40-6 en -3): rem = schriftverbod (YSA-Z21-8, BESLUIT-Z17-9); bereik = registerbereik per regio
SCHRIJF_START=3        # Zusters die in jaar 0 nog kunnen schrijven (aanname)
SCHRIJF_OPLEIDING=20   # jaren per leerling per schrijfster (aanname: geheime kunst; één leerling per halve loopbaan)
SCHRIJF_MAX=300        # bovengrens: zoveel schrijfsters kan de Zusterschap verbergen en voeden (aanname)
SCHRIJF_ROOSTER=40     # schrijfsters nodig voor een rijksbreed rooster (aanname: ~10 per kernregio)
REGISTER_SPREID=0.25   # kans per lente dat het register een buurregio bereikt, gedeeld door reistijd (aanname)
def eindtoestand(w):
  """Z40: de toestand aan het eind van een run, als begin voor de volgende fase."""
  return {'wet':sorted(w.wet),'wetjaar':w.wetjaar,'W':w.W,'M':{k:{str(by):n for by,n in v.items() if n>0} for k,v in w.M.items()},
          'meisjes':{k:{str(by):n for by,n in v.items() if n>0} for k,v in w.meisjes.items()},'reg_bereik':w.reg_bereik,'schrijvers':w.schrijvers,
          'jongenshof':w.jongenshof,'vete':w.vete,'risico':dict(w.risico),'van_run_seed':w.seed,'jaar':w.fase[1]}
VERBODEN_TYPEN=('dwang','ontvoering_seksueel','kind_seksueel')  # bestaan niet; laad_typen weigert alles met risico>0
class Motorfout(Exception): pass
def binom(rnd,n,p):
  if n<=0 or p<=0: return 0
  if p>=1: return n
  if n<30:
    return sum(1 for _ in range(n) if rnd.random()<p)
  m=n*p;sd=math.sqrt(n*p*(1-p));return max(0,min(n,int(round(rnd.gauss(m,sd)))))
def laad_typen(c):
  T={}
  for code,minl,mr,inst,risico in c.execute('select code,min_leeftijd,minderjarige_rol,instemming_nodig,harde_lijn_risico from gebeurtenis_type where module=?',('personen',)):
    if risico: raise Motorfout(f'type {code} kan een harde lijn raken en wordt niet geladen')
    if code in VERBODEN_TYPEN: raise Motorfout(code)
    T[code]=(minl,mr,inst)
  return T
SYL={'saelith':['Ae','Lis','Ond','Sae','Ith','Mer','Vel','Ny'],'ambergaard':['Brecht','Aal','Hil','Gerd','Wob','Tje','Lies','Joost'],'zoutkust':['Ylv','Gun','Ragn','Sol','Tor','Ke','Bryn','Asa'],
     'groenmuil':['Hesk','Rav','Mos','Krul','Tak','Wor','Gro','Ul'],'stille':['Mist','Ru','Nev','Sil','Va','Oor','Ves','Lu'],'hoogvrouwe':['Bul','Dijk','Hoor','Stee','Grun','Ma','Kel','Ot']}
UIT=['a','e','in','ke','rik','ra','old','wen','je','mar']
class Wereld:
  def __init__(s,seed,P,T,regels,bescherm=True,fase=FASE,alwetend=False,rem=False,bereik=False,begin=None):
    s.TB={t[0]:t[6] for t in TYPEN};s.fase=fase;s.alwetend=alwetend;s.bescherm=bescherm;s.r=random.Random(seed);s.seed=seed;s.T=T;s.ev=[];s.fig=0;s.P={};s.kennis=[];s.rel=[];s.verbl=collections.defaultdict(list)
    s.wet=set();s.wetjaar={};s.vete=0;s.risico=collections.Counter();s.uitput=collections.deque(maxlen=8);s.jongenshof=False
    rnd=s.r
    for p in P:
      d=dict(p);d['leeft']=True;d['dood']=None;d['onderweg']=0;d['partner']=None;d['schuld']=set();d['actief']=d['geboren']<=fase[0]
      s.P[d['code']]=d
    # regio's: vrouwen (volwassen), mannen per geboortejaar (bestaande mannen van vóór de Zegel)
    s.W={k:(rnd.randint(2500,3500) if k!='stille' else rnd.randint(600,900)) for k in REG};s.M={}
    for k in REG: s.M[k]=collections.Counter({-a:int(s.W[k]*0.55*math.exp(-a/38)/14) for a in range(16,70)})
    s.meisjes=collections.defaultdict(collections.Counter);s.geregistreerd=set()
    # Z40 (opt-in; standaard uit, zodat Z39-runs bit voor bit reproduceerbaar blijven)
    s.rem=rem;s.bereik=bereik;s.reg_bereik={};s.schrijvers=SCHRIJF_START if rem else None;s.opleiding=SCHRIJF_OPLEIDING
    if begin: s.laad_begin(begin)
  def laad_begin(s,b):
    """Z40 fase-overgang: neem de eindtoestand van een vorige fase over (instituten, bevolking, registerbereik, schrijvers)."""
    s.wet=set(b['wet']);s.wetjaar=dict(b['wetjaar']);s.W=dict(b['W'])
    s.M={k:collections.Counter({int(by):n for by,n in v.items()}) for k,v in b['M'].items()}
    s.meisjes=collections.defaultdict(collections.Counter,{k:collections.Counter({int(by):n for by,n in v.items()}) for k,v in b['meisjes'].items()})
    s.reg_bereik=dict(b.get('reg_bereik',{}));s.jongenshof=b.get('jongenshof',False);s.vete=b.get('vete',0)
    s.risico=collections.Counter(b.get('risico',{}))
    if s.rem and b.get('schrijvers') is not None: s.schrijvers=b['schrijvers']
  def leeftijd(s,p,j): return j-p['geboren']
  def doe(s,j,sz,typ,actor,doel=None,plek=None,detail='',canon=None,oorzaak=None):
    if typ not in s.T: raise Motorfout('onbekend type '+typ)
    minl,mr,inst=s.T[typ]
    for x in (actor,doel):
      if x in s.P:
        p=s.P[x];lt=s.leeftijd(p,j)
        if lt<18 and not mr: raise Motorfout(f'{typ} met minderjarige {x}')
        if not p['leeft'] and typ not in('erfenis','dood'): raise Motorfout(f'{typ} door dode {x}')
    if inst:
      for x in (actor,doel):
        if x not in s.P or s.leeftijd(s.P[x],j)<18 or not s.P[x].get('_ja'): raise Motorfout(f'{typ} zonder instemming van twee volwassenen')
    s.ev.append((j,sz,typ,actor,doel,plek,detail,canon,oorzaak or s.TB.get(typ)))
  def figuur(s,j,regio,functie,geslacht,ouder=None,geboren=None):
    s.fig+=1;rnd=s.stroom('naam',s.fig);naam=rnd.choice(SYL[regio])+rnd.choice(UIT)
    code=f'SIMF-{s.seed}-{s.fig}'
    s.P[code]={'code':code,'naam':naam,'geslacht':geslacht,'volk':'mens','plek':regio,'geboren':j if geboren is None else geboren,'wil':'overleven','groep':None,'leeft':True,'dood':None,'onderweg':0,'partner':None,'schuld':set(),'actief':True,'fig':True,'functie':functie,'ouder':ouder,'canonjaar':None,'geheim':None}
    s.verbl[code].append([regio,j,None]);return code
  def zet_plek(s,code,regio,j):
    v=s.verbl[code]
    if v and v[-1][2] is None: v[-1][2]=j
    v.append([regio,j,None]);s.P[code]['plek']=regio
  def weet(s,wie,wat,j,bron):
    if not any(k[0]==wie and k[1]==wat for k in s.kennis): s.kennis.append((wie,wat,j,bron))
  def relatie(s,a,soort,b,j):
    if not any(x[0]==a and x[1]==soort and x[2]==b for x in s.rel): s.rel.append([a,soort,b,j,None])
  def levend(s,j,regio=None,volw=True):
    return [p for p in s.P.values() if p['leeft'] and p['actief'] and not p['onderweg'] and (regio is None or p['plek']==regio) and (not volw or j-p['geboren']>=18)]
  def mannen(s,k): return sum(s.M[k].values())
  # ---------- één run ----------
  def run(s):
    rnd=s.r
    # Raad der Moeders, jaar -3 (validatie stemming 7-5)
    ja=sum(rnd.random()<0.85 for _ in range(5))+sum(rnd.random()<0.35 for _ in range(4))+sum(rnd.random()<0.5 for _ in range(3))
    s.stem=(ja,12-ja);s.doe(-3,'herfst','raadstemming','RAAD',None,'saelith',f'{ja} tegen {12-ja}','GEB-r10-raad-der-moeders')
    for p in s.P.values():
      if p['actief']: s.verbl[p['code']].append([p['plek'],max(s.fase[0],p['geboren']),None])
      if p.get('geheim') and p['actief']: s.weet(p['code'],p['code']+'#geheim',max(0,p['geboren']+18),'eigen geheim')
    for kode,wie,wat,j in SEED_KENNIS:
      if kode in s.P and wie in s.P: s.weet(wie,wat,j,'canon (personage_profiel, Relaties)')
    if s.alwetend:  # proef 11a/criterium 3: iedereen weet alles vanaf het begin
      for p in s.P.values():
        for q in s.P.values():
          if q.get('geheim') and p['code']!=q['code']: s.weet(p['code'],q['code']+'#geheim',max(s.fase[0],q['geboren']+18,p['geboren']),'alwetend (proef)')
    for j in range(s.fase[0],s.fase[1]+1):
      for sz in SZ: s.stap(j,sz)
    s.slot=s.fase[1]
    return s
  def stroom(s,*k): return random.Random(zlib.crc32(repr((s.seed,)+k).encode()))
  def stap(s,j,sz):
    s.r=s.stroom('wereld',j,sz);rnd=s.r
    for p in s.P.values():  # canonpersonages met geboren>0 worden in hun jaar geboren (seed, niet gegenereerd)
      if not p['actief'] and p['geboren']==j and sz=='lente':
        p['actief']=True;s.verbl[p['code']].append([p['plek'],j,None]);s.doe(j,sz,'geboorte',p['code'],None,p['plek'],'canonpersonage geboren','personage_profiel:'+p['code'])
        if p.get('geheim'): s.weet(p['code'],p['code']+'#geheim',j+18,'eigen geheim')
      if p['onderweg']:
        p['onderweg']-=1
        if not p['onderweg']: s.zet_plek(p['code'],p['doelplek'],j)
    if sz=='lente': s.bevolking(j)
    s.instituten(j,sz)
    for p in list(s.levend(j)):
      s.r=s.stroom('handel',p['code'],j,sz);s.handel(p,j,sz)
    s.r=s.stroom('na',j,sz)
    if sz=='winter': s.sterfte(j)
  def bevolking(s,j):
    s.r=s.stroom('bevolking',j);rnd=s.r;last_tot=0;doden_last=0
    for k in REG:
      M=s.mannen(k);W=s.W[k]
      if M<=0: continue
      cap=8 if ('deelwet' in s.wet and not (k=='stille' and 'eilanden' in s.wet) and not (k=='ambergaard' and s.wetjaar.get('weerstand_tot',0)>j)) else 1
      if 'rotatie' in s.wet: cap=cap
      geb=int(min(W*0.07,M*cap*0.9)*rnd.uniform(0.85,1.15))
      zonen=binom(rnd,geb,0.01)
      s.M[k][j]+=zonen;s.meisjes[k][j]+=geb-zonen
      last=geb/max(M,1);last_tot+=last
      if last>3:
        extra=0.04*(last-3)*(0.5 if 'rotatie' in s.wet else 1)
        for by in list(s.M[k]):
          if j-by>=16:
            d=binom(rnd,s.M[k][by],extra)
            s.M[k][by]-=d;doden_last+=d
      if (k not in s.reg_bereik if s.bereik else 'register' not in s.wet) and M/max(W,1)<0.08: s.risico[k]+=rnd.uniform(0.05,0.15)*(2 if k=='groenmuil' else 1)
      # meisjes worden vrouwen na 16 jaar, vrouwen sterven ~2%/jaar
      s.W[k]=int(W*0.965)+s.meisjes[k].pop(j-16,0)
      for by in list(s.M[k]):
        a=j-by;q=0.003*math.exp(a/14) if a>0 else 0.01
        d=binom(rnd,s.M[k][by],min(q,1))
        s.M[k][by]=max(0,s.M[k][by]-d)
    s.uitput.append(doden_last)
    if s.rem:  # Z40 rem: schrijven is een geheime kunst van de Zusters; elke schrijfster leidt gemiddeld één leerling op per SCHRIJF_OPLEIDING jaar
      s.schrijvers=min(SCHRIJF_MAX,s.schrijvers+binom(rnd,s.schrijvers,1/s.opleiding))
    if s.bereik and 'register' in s.wet:  # Z40: het register bereikt een regio langs de routes, met reistijd
      for k in REG:
        if k in s.reg_bereik: continue
        bron=[r for r in s.reg_bereik if reis(r,k)]
        nodig=2*(len(s.reg_bereik)+1)
        if bron and (not s.rem or s.schrijvers>=nodig) and rnd.random()<REGISTER_SPREID/min(reis(r,k) for r in bron):
          s.reg_bereik[k]=j;s.doe(j,'lente','wet','REGISTER',None,k,f'het register bereikt {k}','GEB-r10-eerste-register')
          for p in s.levend(j,k,volw=False): s.geregistreerd.add(p['code'])
    if doden_last>0 and 'deelwet' in s.wet: s.doe(j,'lente','dood','MANNEN',None,None,f'{doden_last} mannen sterven aan uitputting','GEB-r10-uitputting' if doden_last>=20 else None)
  def zusters(s,j,naam_pat=None):
    return [p for p in s.levend(j) if (p.get('groep') or '').startswith(ZUSTERS_W) and (naam_pat is None or re.search(naam_pat,p['code']))]
  def instituten(s,j,sz):
    s.r=s.stroom('instituten',j,sz);rnd=s.r
    tot_M=sum(s.mannen(k) for k in REG);tot_W=sum(s.W.values())
    if 'deelwet' not in s.wet and tot_M/tot_W<0.12 and s.zusters(j) and rnd.random()<0.06:
      z=rnd.choice(s.zusters(j));s.wet.add('deelwet');s.wetjaar['deelwet']=j;s.doe(j,sz,'wet',z['code'],None,'saelith','Deelwet afgekondigd','GEB-deelwet-40')
      boer=[p for p in s.levend(j,'ambergaard') if wilsoort(p['wil'])=='liefde']
      if boer:
        s.wetjaar['weerstand_tot']=j+rnd.randint(10,25);s.doe(j,sz,'wet',boer[0]['code'],None,'ambergaard',f'Ambergaard weigert te delen tot {s.wetjaar["weerstand_tot"]}','GEB-r10-deelwet-weerstand')
      runa=s.P.get('PER-f4-eiland-moeder-runa')
    if 'deelwet' in s.wet and 'eilanden' not in s.wet:
      runa=s.P.get('PER-f4-eiland-moeder-runa')
      if runa and runa['leeft'] and runa['actief'] and j-runa['geboren']>=25 and rnd.random()<0.1:
        s.wet.add('eilanden');s.wetjaar['eilanden']=j;s.doe(j,sz,'wet',runa['code'],None,'stille','De eilanden houden hun eigen mannen','GEB-r10-eilanden-weigering')
    if 'deelwet' in s.wet and 'rotatie' not in s.wet and sum(s.uitput)>=30 and (not s.rem or s.schrijvers>=SCHRIJF_ROOSTER):
      rek=[p for p in s.zusters(j) if wilsoort(p['wil'])=='register']
      if rek and rnd.random()<0.15:
        z=rnd.choice(rek);s.wet.add('rotatie');s.wetjaar['rotatie']=j;s.doe(j,sz,'wet',z['code'],None,'saelith','rooster: mannen reizen in vaste kring','GEB-r10-rotatie')
    if 'register' not in s.wet and s.vete>=3 and s.zusters(j) and rnd.random()<0.2:
      z=rnd.choice(s.zusters(j));s.wet.add('register');s.wetjaar['register']=j;s.doe(j,sz,'wet',z['code'],None,'saelith','eerste register: wie is wiens kind','GEB-r10-eerste-register')
      if s.bereik: s.reg_bereik['saelith']=j
      for p in s.levend(j,volw=False):
        if p['plek'] in (('saelith',) if s.bereik else ('saelith','ambergaard','zoutkust')): s.geregistreerd.add(p['code'])
    if 'register' in s.wet and not s.jongenshof and s.zusters(j) and rnd.random()<0.012:
      z=s.zusters(j,'jongenshof|ithra') or s.zusters(j);z=rnd.choice(z);s.jongenshof=True;s.wetjaar['jongenshof']=j
      s.doe(j,sz,'wet',z['code'],None,'saelith','Jongenshof gesticht','GEB-r10-jongenshof')
    if 'register' in s.wet and 'rotatie' in s.wet and 'orde' not in s.wet:
      iris=s.P.get('PER-f4-orde-moeder-iris');kand=[p for p in s.zusters(j) if wilsoort(p['wil'])=='macht'] or ([iris] if iris and iris['leeft'] and iris['actief'] and j-iris['geboren']>=30 else [])
      if kand and rnd.random()<0.08:
        s.wet.add('orde');s.wetjaar['orde']=j;s.doe(j,sz,'wet',kand[0]['code'],None,'saelith','de Zusters heten voortaan de Orde','GEB-r10-orde-naam')
        for p in s.P.values():
          if p.get('groep')=='Zusters': p['groep']='Orde'
    for k,v in list(s.risico.items()):
      if v>=1.0 and 'ramp_'+k not in s.wet:
        s.wet.add('ramp_'+k);s.doe(j,sz,'wet','DORP',None,k,'inteeltramp in een dorp zonder register','GEB-r10-neven-ramp' if k=='groenmuil' else None);s.vete+=1
  def handel(s,p,j,sz):
    rnd=s.r;ws=wilsoort(p['wil']);code=p['code'];hier=p['plek']
    anderen=[q for q in s.levend(j,hier) if q['code']!=code]
    x=rnd.random()
    # verbintenis: twee volwassenen die het allebei willen
    if ws=='liefde' and not p['partner'] and anderen and x<0.08:
      q=rnd.choice(anderen)
      if not q['partner'] and (p['geslacht']!=q['geslacht'] or rnd.random()<0.5):
        p['_ja']=rnd.random()<0.8;q['_ja']=rnd.random()<(0.7 if wilsoort(q['wil']) in('liefde','overleven') else 0.3)
        if p['_ja'] and q['_ja']:
          s.doe(j,sz,'verbintenis',code,q['code'],hier,'kiezen elkaar');p['partner']=q['code'];q['partner']=code;s.relatie(code,'verbonden_met',q['code'],j)
        p['_ja']=q['_ja']=False
    # geboorte binnen een verbintenis met een man (figuur op aanvraag)
    if p['partner'] and p['geslacht']=='v' and 18<=j-p['geboren']<=42 and sz=='zomer':
      q=s.P.get(p['partner'])
      if q and q['leeft'] and q['geslacht']=='m' and rnd.random()<0.12:
        zoon=rnd.random()<0.01;kind=s.figuur(j,hier,'kind van '+p['naam'],'m' if zoon else 'v',ouder=code)
        s.doe(j,sz,'geboorte',kind,code,hier,('zoon' if zoon else 'dochter')+' van '+p['naam']+' en '+q['naam'])
        if zoon and s.jongenshof: s.doe(j,sz,'opvoeding',kind,None,'saelith','naar het Jongenshof','GEB-r10-jongenshof')
    # rotatiebeurt: man in verbintenis weigert
    if p['geslacht']=='m' and p['partner'] and 'deelwet' in s.wet and x<0.1:
      s.doe(j,sz,'beurt_geweigerd',code,None,hier,'weigert de beurt om bij zijn geliefde te blijven','GEB-deelwet-40',oorzaak='gebeurtenis:verbintenis')
      z=[q for q in anderen if (q.get('groep') or '').startswith(ZUSTERS_W)]
      if z: s.doe(j,sz,'ruzie',z[0]['code'],code,hier,'het register eist zijn beurt',oorzaak='gebeurtenis:beurt_geweigerd');s.relatie(z[0]['code'],'rivaal_van',code,j)
      buur=[q for q in anderen if q['geslacht']=='v' and not q['partner']]
      if buur and rnd.random()<0.3:
        b=rnd.choice(buur);s.doe(j,sz,'verraad',b['code'],code,hier,'klaagt hem aan bij het register',None,oorzaak='gebeurtenis:beurt_geweigerd');s.relatie(code,'verraden_door',b['code'],j);s.weet(b['code'],code+'#weigering',j,'gezien')
    # Zusters: registerinzage, vervalsing
    if (p.get('groep') or '').startswith(ZUSTERS_W) and 'register' in s.wet:
      if x<0.15:
        for q in s.levend(j):
          if q['code'] in s.geregistreerd and q.get('geheim') and rnd.random()<0.3 and q['code']!=code:
            s.weet(code,q['code']+'#geheim',j,'register');s.doe(j,sz,'registerinzage',code,q['code'],hier,'leest het blad van '+q['naam'],oorzaak='gebeurtenis:wet')
            break
      if ws=='register' and x>0.97:
        s.doe(j,sz,'vervalsing',code,None,hier,'vervalst een blad','VALS-noodtoestand');s.weet(code,code+'#vervalsing',j,'eigen daad')
    # chantage: ik weet een geheim van iemand binnen bereik
    for (wie,wat,sj,br) in [k for k in s.kennis if k[0]==code and k[1].endswith('#geheim') and k[2]<=j]:
      doel=wat.split('#')[0];q=s.P.get(doel)
      if q and q['leeft'] and q['actief'] and not q['onderweg'] and doel!=code and (reis(hier,q['plek']) or 0)<=1 and reis(hier,q['plek']) is not None and j-q['geboren']>=18 and code not in q['schuld'] and rnd.random()<0.02 and wilsoort(q['wil'])!=ws:
        s.doe(j,sz,'chantage',code,doel,hier,'gebruikt wat ze weet over '+q['naam'],oorzaak='kennis:'+wat);s.relatie(doel,'schuldig_aan',code,j);q['schuld'].add(code)
        if rnd.random()<0.25:
          s.doe(j,sz,'verraad',doel,code,q['plek'],'keert zich tegen wie dreigt',oorzaak='gebeurtenis:chantage');s.relatie(code,'verraden_door',doel,j)
        break
    # geheim lekt
    if anderen and x<0.03:
      mijn=[k for k in s.kennis if k[0]==code and k[2]<=j]
      if mijn:
        k=rnd.choice(mijn);q=rnd.choice(anderen)
        if k[1].split('#')[0]!=q['code']: s.weet(q['code'],k[1],j,'van '+code);s.doe(j,sz,'geheim_lekt',code,q['code'],hier,'vertelt verder',oorzaak='kennis:'+k[1])
    # eed aan een leidster (clan of Zusters)
    if p.get('groep') and x>0.985:
      leid=[q for q in anderen if q.get('groep')==p['groep'] and q['code']!=code and j-q['geboren']>j-p['geboren']]
      if leid: s.doe(j,sz,'eed',code,leid[0]['code'],hier,'zweert trouw');s.relatie(code,'eed_aan',leid[0]['code'],j)
    # roof (clans): volwassen man uit een buurregio
    if ws in('overleven',) and (p.get('groep') or '').endswith('clan') and sz=='zomer' and 'register' not in s.wet:
      for k in REG:
        r_=reis(hier,k)
        if r_==1 and s.mannen(hier)/max(s.W[hier],1)<0.5 and s.mannen(k)/max(s.W[k],1)>s.mannen(hier)/max(s.W[hier],1) and rnd.random()<0.3:
          for by in sorted(s.M[k],reverse=True):
            if s.M[k][by]>0 and j-by>=18:
              n=min(s.M[k][by],rnd.randint(2,12));s.M[k][by]-=n;s.M[hier][by]+=n;break
          slachtoffer=s.figuur(j-0,k,'geroofde man','m',geboren=j-rnd.randint(20,40))
          s.doe(j,sz,'roof',code,slachtoffer,k,f'rooft mannen uit {k}','GEB-r10-mannenroof');s.zet_plek(slachtoffer,hier,j);s.vete+=1
          break
    # migratie
    if x>0.993:
      opties=[k for k in REG if reis(hier,k)==1 and not dicht(hier,k,sz)]
      if opties:
        k=rnd.choice(opties);p['onderweg']=reis(hier,k);p['doelplek']=k;s.zet_plek(code,'onderweg',j);s.doe(j,sz,'migratie',code,None,hier,'vertrekt naar '+k)
    # wil_hetzelfde_als en rivaliteit
    if anderen and x<0.02:
      q=rnd.choice(anderen)
      if wilsoort(q['wil'])==ws: s.relatie(code,'wil_hetzelfde_als',q['code'],j)
      if q['partner'] and q['partner']==p.get('partner'): s.relatie(code,'rivaal_van',q['code'],j)
  def sterfte(s,j):
    s.r=s.stroom('sterfte',j);rnd=s.r
    for p in list(s.P.values()):
      if not p['leeft'] or not p['actief']: continue
      a=j-p['geboren'];L=900 if p['volk']=='aelthir' else 70
      if s.bescherm and p.get('canonjaar') is not None and j<p['canonjaar']: continue  # SIM-kern: canonpersonage leeft in zijn canonjaar
      q=0.002+0.0006*math.exp((a-L+25)/7.5)*(70/L) if a>=0 else 0
      if p['geslacht']=='m' and 'deelwet' in s.wet and not p.get('fig') and 'rotatie' not in s.wet: q+=0.01
      if rnd.random()<q:
        p['leeft']=False;p['dood']=j;s.doe(j,'winter','dood',p['code'],None,p['plek'],f'sterft op {a}')
        v=s.verbl[p['code']]
        if v and v[-1][2] is None: v[-1][2]=j
        kind=[q2 for q2 in s.P.values() if q2.get('ouder')==p['code'] and q2['leeft']]
        if kind: s.doe(j,'winter','erfenis',kind[0]['code'],p['code'],p['plek'],'erft van '+p['naam'])
        if p['partner'] and p['partner'] in s.P: s.P[p['partner']]['partner']=None
SEED_KENNIS=[('PER-f4-ylva','PER-f4-saske','PER-f4-ylva#geheim',0),('PER-f4-brecht','PER-f4-buurvrouw-aaltje','PER-f4-brecht#geheim',20),('PER-f4-saske','PER-f4-dochter-edrun','PER-f4-saske#geheim',50)]
def seed_personen(c,fase_nr=4):
  P=[];gezien=set()
  for code,naam,volk,regio,huis,rol,jaar,geb,wil,geheim in c.execute("select code,naam,volk,regio,huis,rol,jaar,geboren,wil,geheim from personage_profiel where fase_nr=? and code like 'PER-%' and naam is not null order by code",(fase_nr,)):
    if naam in gezien or not regio: continue
    gezien.add(naam)
    aann=geb is None
    if geb is None: geb=(jaar or 30)-35
    P.append({'code':code,'naam':naam,'volk':volk or 'mens','plek':regio if regio in REG else 'saelith','groep':huis,'wil':wil,'geslacht':'m' if code in MANNEN else 'v','geboren':geb,'canonjaar':jaar,'geheim':geheim,'aanname_geboren':aann})
  return P
# ---------- invarianten ----------
def invarianten(w):
  fout=[]
  dood={p['code']:p['dood'] for p in w.P.values() if p['dood'] is not None}
  for (j,sz,typ,a,d,plek,det,cc,oz) in w.ev:
    if a in dood and typ not in('dood','erfenis') and j>dood[a]: fout.append(f'{a} handelt na zijn dood ({typ} {j})');break
  for code,v in w.verbl.items():
    vs=sorted(v,key=lambda x:x[1])
    for x,y in zip(vs,vs[1:]):
      if x[2] is None or x[2]>y[1]: fout.append(f'{code} op twee plekken ({x[0]} en {y[0]} in {y[1]})');break
    if len(fout)>3: break
  bron={}
  for p in w.P.values(): bron[p['code']+'#geheim']=p['geboren']
  for (wie,wat,sj,br) in w.kennis:
    b=wat.split('#')[0]
    if b in w.P and sj<w.P[b]['geboren']: fout.append(f'{wie} weet {wat} in {sj}, vóór de bron bestaat');break
  for p in w.P.values():
    if p.get('canonjaar') is not None and p['dood'] is not None and p['dood']<p['canonjaar'] and p['canonjaar']<=w.fase[1]:
      fout.append(f'anker: {p["code"]} sterft in {p["dood"]}, vóór canonjaar {p["canonjaar"]}');break
  zonen=sum(sum(v for by,v in w.M[k].items() if by>=0) for k in REG)
  return fout
def score(w,canon_hits):
  T=collections.Counter(e[2] for e in w.ev)
  intrige=T['chantage']+T['verraad']+T['vervalsing']
  ommekeer=T['verraad']+T['geheim_lekt']//3+len([1 for e in w.ev if e[2]=='wet'])
  verbinding=len(canon_hits)
  rijm=sum(['register' in w.wet, any(e[2]=='dood' and e[3]=='MANNEN' for e in w.ev), T['vervalsing']>0, not any(e[2]=='verraad' and e[4] and e[4] in w.P and (w.P[e[4]].get('groep') or '').startswith(ZUSTERS_W) for e in w.ev)])
  g={'intrige':min(5,intrige/4),'suspense':min(5,(T['chantage']+T['geheim_lekt']/4)/2),'tragiek':min(5,T['dood']/10),'romance':min(5,T['verbintenis']),'horror':min(5,2*('ramp_groenmuil' in w.wet)+T['roof']/4)}
  doel={'intrige':5,'suspense':3,'tragiek':2,'romance':0,'horror':2}  # DP-intrige-horror-rand (benadering)
  doelmatch=round(1-sum(abs(g[k]-doel[k]) for k in doel)/25,3)
  return {'intrige':intrige,'ommekeer':ommekeer,'verbinding':verbinding,'rijm':rijm,'doelmatch':doelmatch,'gebeurtenissen':len(w.ev)}
def canon_hits(w): return sorted({e[7] for e in w.ev if e[7] and not e[7].startswith('personage_profiel:')})
