"""Ronde Z36: de verhalenmachine (opdracht_Z35.md stap 7, 8, 9; OPDRACHT_architect_Z36.md stap 2).
Gebruikt door vraag.py (bedenk, pareto, volgende, gewicht, afstand, dekking, ideeenrapport) en r_Z36.py.
Alles deterministisch via een seed. Uitvoer gaat alleen naar verhaal_profiel (ideeënbank, status voorlopig); Rogier kiest wat canon wordt.

Assen (7): positie, genre, schaal, volk, vorm, afloop, hoofdpersoon (leeftijdsband|geslacht).  afstand(a,b) = aantal assen dat verschilt.
Harde grenzen zijn filters, nooit scores (filter()).  Doelen: nieuwheid, verbondenheid, seriewaarde, lezersvraag, kosten (min), genrematch."""
import random,math,json,re,hashlib,collections,datetime
ASSEN=['positie','genre','schaal','volk','vorm','afloop','hoofdpersoon']
G=['romance','erotiek','horror','suspense','actie','intrige','komedie','tragiek']
POSITIES=['beslisser','betaler','vervalser','ontdekker','profiteur','toeschouwer','liefde tussen posities']
GENRES={'intrige':.55,'horror':.50,'thriller':.65,'mysterie':.55,'romance':.70,'komedie':.40,'actie':.55,'tragedie':.45,'survival':.40}
SCHALEN={'huis':.8,'dorp':.9,'stad':1.0,'rijk':1.2,'wereld':1.4}
VORMEN={'brieven':25,'ballade':15,'aftellen':30,'rechtszaak':30,'dagboek':25,'jij-vorm':25,'register als verteller':20,'kroniek':40,'realtime':30,'documenten':25,
 'wij-vorm':35,'kasboek':20,'kamerspel':25,'rondes':35,'toespraak':15,'lijst die krimpt':30,'twee stemmen':60,'lichaam als verteller':40,'getuigenverslag':25,'zelfportret':25,'nog niet gekozen':50}
AFLOPEN=['werkt','faalt','komt uit','blijft verborgen','keert om']
BANDEN={'18-25':22,'26-40':32,'41-60':50,'61+':67}
GESLACHT=['v','m','wisselend','groep']
HOOFDPERSONEN=[f'{b}|{g}' for b in BANDEN for g in GESLACHT]
# genre -> basisvector (romance, erotiek, horror, suspense, actie, intrige, komedie, tragiek); erotiek komt uit de heat-keuze
BASIS={'intrige':(0,0,0,2,0,5,0,1),'horror':(0,0,5,3,1,0,0,2),'thriller':(0,0,1,5,2,2,0,1),'mysterie':(0,0,1,4,0,3,1,1),'romance':(5,0,0,1,0,0,1,1),
 'komedie':(1,0,0,0,1,1,5,0),'actie':(0,0,0,3,5,1,0,1),'tragedie':(1,0,0,1,0,1,0,5),'survival':(0,0,2,3,3,0,0,2)}
POS_MOD={'betaler':{'tragiek':1},'vervalser':{'intrige':1},'ontdekker':{'suspense':1},'profiteur':{'komedie':1},'toeschouwer':{'horror':1},'liefde tussen posities':{'romance':2},'beslisser':{'intrige':1}}
AF_MOD={'faalt':{'tragiek':1},'komt uit':{'suspense':1},'keert om':{'suspense':1},'blijft verborgen':{'intrige':1},'werkt':{}}
LANCERING={'verbondenheid':.30,'seriewaarde':.25,'nieuwheid':.20,'lezersvraag':.15,'kosten':.10}
HOOFDLIJN=re.compile(r'Liora|Stille Modus|Thalen|derde weg|instemmingssleutel|sleutel',re.I)  # Z36 (fout: gaf 0,00 in fase 4 en 6); niet meer gebruikt
# Z37 (D1.1): seriewaarde = raakt het profiel een rij van de hoofdlijn, direct (1,0) of via een relatie (0,6)? Anders 0.
# Hoofdlijn: BESLUIT-Z36-1, ORIGIN-10-Z36, BESLUIT-Z32-9, BOOG-boek1 (via zijn bronrijen), de derde weg, Thalen/Ysara, de Stille Modus, Hesta's cellen.
HOOFDLIJN_CODES={'BESLUIT-Z36-1':'Stille Modus','ORIGIN-10-Z36':'Stille Modus (Zegel jaar 0)','BESLUIT-Z32-9':'hoofdlijn boek 1','BESLUIT-Z36-4':'derde weg',
 'HAAK-Z1-derdeweg-1':'derde weg','HAAK-Z1-derdeweg-2':'derde weg','HAAK-Z1-derdeweg-3':'derde weg','HAAK-Z1-derdeweg-4':'derde weg',
 'PER-liora-profiel-Z32':'BOOG-boek1','BESLUIT-Z32-11':'BOOG-boek1','PER-ysara':'Thalen/Ysara','PER-v4-thalen-orr-Z32':'Thalen/Ysara','BESLUIT-Z15-7-Z37':'Thalen/Ysara',
 'BESLUIT-Z12-wortelstem':'Thalen/Ysara','ORIGIN-WAAROM-8':'Stille Modus','BESLUIT-Z37-1':'Stille Modus (twee lagen)','BESLUIT-Z37-2':'Stille Modus (h32)',
 'BESLUIT-Z37-3':"Hesta's cellen",'PER-v4-hesta-kael':"Hesta's cellen",'ZAAD-stille-modus':'Stille Modus','ZAAD-hesta-vonkcellen':"Hesta's cellen",'ZAAD-Z36-h32-protocol':'Stille Modus (h32)'}
def hoofdlijn(c):
  """Levende hoofdlijnrijen (vervangen rijen volgen hun opvolger) + de buren via één relatie."""
  H={}
  for k,v in HOOFDLIJN_CODES.items():
    x=k
    for _ in range(5):
      r=c.execute('select status,vervangen_door from canon where code=?',(x,)).fetchone()
      if not r or r[0] in('vastgesteld','voorlopig') or not r[1]: break
      x=r[1]
    H[x]=v
  buur={}
  for a,b in c.execute('select van_code,naar_code from relatie'):
    if a in H and b not in H: buur.setdefault(b,(a,H[a]))
    if b in H and a not in H: buur.setdefault(a,(b,H[b]))
  return H,buur
# riten voor erotische profielen van mensen, per fase (alleen bestaande RIT-codes worden gebruikt; gecontroleerd in wereldregel())
RITEN_MENS={0:[],1:['RIT-zwijgende-rit'],2:['RIT-strijdontvangst','RIT-gunstnacht'],3:['RIT-ontzegging-binding','RIT-maanzalving'],4:['RIT-maanzalving','RIT-zwijgende-rit'],
 5:['RIT-ontvangst','RIT-wijding','RIT-gunstnacht'],6:['RIT-veiling','RIT-zaadcontract','RIT-rolwisseling'],7:['RIT-rolwisseling','RIT-boeterite'],8:['RIT-wijding','RIT-rolwisseling']}
# volken die pas later bestaan (bron in de tuple); personage_profiel kent hun volksgeschiedenis vanaf fase 0, dus hier begrensd
VOLK_VANAF={'myrrhen':(6,'PER-myrr-ondal: eerste Myrrhen, fase 6, jaar 470'),'grauwen':(4,'PER-f4-grauwe-heske: stammoeder, jaar 45')}
SLUG={'karrûk':'karruk','sael-mor':'saelmor'}

def fasen(c): return c.execute('select fase,volgorde from fase_rijm order by volgorde').fetchall()
def fase_naam(c,x):
  x=str(x).strip()
  for f,v in fasen(c):
    if x==f or x==f.split(' ')[0] or x.lower()==f.split(' ',1)[1].lower(): return f,v
  raise SystemExit(f'onbekende fase {x}; kies uit '+', '.join(f for f,_ in fasen(c)))
def gewichten(c,naam='lancering serie'):
  r=c.execute("select gewichten from gewichtset where naam=? order by datum desc,id desc limit 1",(naam,)).fetchone()
  return json.loads(r[0]) if r else dict(LANCERING)
def doelprofiel(c,naam):
  if not naam: return None
  r=c.execute(f"select code,naam,{','.join('doel_'+g for g in G)},{','.join('min_'+g for g in G)} from doelprofiel where naam=? or code=?",(naam,naam)).fetchone()
  if not r: raise SystemExit(f'onbekend doelprofiel {naam}; kies uit: '+', '.join(x[0] for x in c.execute('select naam from doelprofiel')))
  return {'code':r[0],'naam':r[1],'doel':dict(zip(G,r[2:10])),'min':dict(zip(G,r[10:18]))}
def afstand(a,b): return sum(1 for k in ASSEN if (a.get(k) or '')!=(b.get(k) or ''))
def genrevector(p):
  v=dict(zip(G,BASIS[p['genre']]));v['erotiek']=p.get('heat',0)
  if p.get('heat',0)>=3: v['romance']+=1
  for k,d in list(POS_MOD.get(p['positie'],{}).items())+list(AF_MOD.get(p['afloop'],{}).items()): v[k]+=d
  return {k:max(0,min(5,x)) for k,x in v.items()}
# ---------------- wereld: wat bestaat er per fase ----------------
class Wereld:
  def __init__(s,c,fase,run=None):
    s.c=c;s.fase,s.vg=fase_naam(c,fase);s.run=run
    s.naam=s.fase.split(' ',1)[1]
    s.fnr=s.vg if s.vg<8 else 801
    s.volken=sorted(({r[0] for r in c.execute('select volk from personage_profiel where volk is not null and fase_nr=?',(s.fnr,))}|{'mens'})-{v for v,f in VOLK_VANAF.items() if s.vg<f[0]})
    s.volken=sorted(set(s.volken))
    s.bogen=[dict(zip(['code']+ASSEN,r)) for r in c.execute('select a.boog_code,a.positie,a.genre,a.schaal,a.volk,a.vorm,a.afloop,a.hoofdpersoon from boog_as a join boog b on b.code=a.boog_code where b.fase=?',(s.fase,))]
    q='select code,positie,genre,schaal,volk,vorm,afloop,hoofdpersoon from verhaal_profiel where fase=? and uitslag in(\'ent-klaar\',\'voorgesteld\')'
    a=[s.fase];
    if run: q+=' and run<?';a.append(run)
    s.profielen=[dict(zip(['code']+ASSEN,r)) for r in c.execute(q,a)]
    r=c.execute('select erft_van,fase from fase_rijm where fase=?',(s.fase,)).fetchone()
    s.erf_eigen='ERF-'+s.naam.lower() if c.execute("select 1 from canon where code=? and status in('vastgesteld','voorlopig')",('ERF-'+s.naam.lower(),)).fetchone() else None
    s.erf_van=[x for x in re.split(r'[;,]\s*',r[0] or '') if x]
    pat=[s.fase,s.fase.split(' ')[0]+' ',s.naam]
    s.zaadjes=[z for z,o in c.execute("select code,oogst_in from zaadje where status like 'open%'") if o and (o.startswith(s.fase) or (s.vg==8 and '801' in o) or o.lower().startswith(s.naam.lower()))]
    s.kern=[r[0] for r in c.execute("select code from v_kern where code in('BESLUIT-Z30-4','REGEL-harde-grenzen','BESLUIT-Z36-4',?) or code in(select van_code from verwijzing where naar_code in(?,?)) order by code",('FASE-OVERZICHT-Z36-'+s.fase.split(' ')[0],'FASE-'+s.naam.lower(),'ERF-'+s.naam.lower()))]
    s.inkom=collections.Counter(r[0] for r in c.execute("select naar_code from relatie where soort='leunt_op'"))
    s.prior={w:p for w,p in c.execute("select waarde,prior from verhaal_as where as_naam='genre'")} or dict(GENRES)
    s.lezers=collections.defaultdict(lambda:[0.0,0.0])
    for genre,reads,af in c.execute('select a.genre,l.reads,l.afmaakpercentage from lezersdata l join boog_as a on a.boog_code=l.boog_code'):
      if reads: s.lezers[genre][0]+=reads*(af or 0)/100/100;s.lezers[genre][1]+=reads*(1-(af or 0)/100)/100
    s.codes={r[0] for r in c.execute("select code from canon where status in('vastgesteld','voorlopig')")}
    s.H,s.buur=hoofdlijn(c)
    s.dragers=c.execute("select code,volk,leeftijd_band,wil from personage_profiel where fase_nr=? and archetype=0 and coalesce(leeftijd_band,'?')!='onder 18'",(s.fnr,)).fetchall()
  def bestaand(s): return s.bogen+s.profielen
  def wereldregel(s,p):
    if p['volk']!='mens':
      sl=SLUG.get(p['volk'],p['volk'])
      opts=[x for x in sorted(s.codes) if x.startswith(f'SEKS-VOLK-{sl}-') and not x.endswith('-kern')]
    else: opts=[x for x in RITEN_MENS.get(s.vg,[]) if x in s.codes]
    if not opts: return None
    return opts[int(hashlib.md5((p['positie']+p['genre']+p['vorm']).encode()).hexdigest(),16)%len(opts)]
  def lezersvraag(s,genre):
    pr=s.prior.get(genre,.5);a=pr*10+s.lezers[genre][0];b=(1-pr)*10+s.lezers[genre][1];return a/(a+b)
# ---------------- filters (harde grenzen: nooit een score) ----------------
def filter(w,p,extra=()):
  """Geeft None als het profiel door alle filters komt, anders de reden. extra: profielen die al gekozen zijn (zelfde run)."""
  if (p.get('leeftijd') or 0)<18: return 'harde lijn: hoofdpersoon jonger dan 18'
  if (p.get('g_erotiek') or 0)>0:
    if p.get('partner') in('dier','minderjarige') or 'dier' in (p.get('partner') or '') : return 'harde lijn: dier of minderjarige in een seksuele rol'
    if p.get('instemming')=='niet mogelijk': return 'harde lijn: seks met wie echt niet kan instemmen'
    if p.get('instemming')=='dwang' and not p.get('dwang_label'): return 'harde lijn: dwang zonder label donker thema'
    if not p.get('wereldregel_code'): return 'wereld: erotiek zonder bestaande wereldregel of rite (code)'
  if p.get('instemming')=='dwang' and not p.get('dwang_label'): return 'harde lijn: dwang zonder label donker thema'
  if p['volk'] not in w.volken: return f"Kern/wereld: volk {p['volk']} bestaat niet in {w.fase} (personage_profiel)"
  for k,vals in (('positie',POSITIES),('genre',GENRES),('schaal',SCHALEN),('vorm',VORMEN),('afloop',AFLOPEN),('hoofdpersoon',HOOFDPERSONEN)):
    if p[k] not in vals: return f'as {k}: waarde {p[k]} niet toegestaan (verhaal_as)'
  for b in w.bestaand()+list(extra):
    if afstand(p,b)<3: return f"R-verhaal_afstand: afstand {afstand(p,b)} tot {b['code']}"
  for b in w.bogen:
    if all(p[k]==b[k] for k in ('positie','afloop','schaal')): return f"rijm: zelfde positie, afloop en schaal als {b['code']} (kopie van de motor, geen rijm)"
  return None
def minimum_ok(p,dp):
  return dp is None or all((p['g_'+g] or 0)>=(dp['min'][g] or 0) for g in G)
# ---------------- doelen ----------------
def scores(w,p,dp=None,collectie=()):
  best=w.bestaand()+list(collectie)
  p['nieuwheid']=round(min((afstand(p,b) for b in best),default=7)/7,3)
  z=1 if p.get('zaadje_code') else 0;e=1 if p.get('erf_code') else 0
  cent=math.log1p(w.inkom[p.get('wereldregel_code') or '']+w.inkom[p.get('erf_code') or ''])/math.log(60)
  p['verbondenheid']=round((z+e+min(1,cent))/3,3)
  geraakt=[x for x in (p.get('erf_code'),p.get('zaadje_code'),p.get('wereldregel_code'),p.get('drager')) if x]
  d=[x for x in geraakt if x in w.H];b=[x for x in geraakt if x in w.buur]
  if d: p['seriewaarde']=1.0;p['seriewaarde_reden']=f'direct: {d[0]} ({w.H[d[0]]})'
  elif b: p['seriewaarde']=0.6;p['seriewaarde_reden']=f'via relatie: {b[0]} - {w.buur[b[0]][0]} ({w.buur[b[0]][1]})'
  else: p['seriewaarde']=0.0;p['seriewaarde_reden']='raakt geen hoofdlijnrij (ook niet via een relatie)'
  if 'premisse' not in p: p['premisse'],p['premisse_codes']=premisse(w.c,p)
  p['lezersvraag']=round(w.lezersvraag(p['genre']),3)
  p['kosten']=round(VORMEN[p['vorm']]*SCHALEN[p['schaal']]/84,3)
  if dp: p['genrematch']=round(1-sum(abs((p['g_'+g] or 0)-(dp['doel'][g] or 0)) for g in G)/40,3)
  return p
def nut(p,W,dp=None):
  w=dict(W)
  if dp: w={k:v*.8 for k,v in w.items()};w['genrematch']=.2
  return sum(v*((1-p['kosten']) if k=='kosten' else p.get(k,0) or 0) for k,v in w.items())
DOELEN=['nieuwheid','verbondenheid','seriewaarde','lezersvraag','kosten']
def vec(p,dp): return [p['nieuwheid'],p['verbondenheid'],p['seriewaarde'],p['lezersvraag'],-p['kosten']]+([p['genrematch']] if dp else [])
def domineert(a,b): return all(x>=y for x,y in zip(a,b)) and any(x>y for x,y in zip(a,b))
# ---------------- kandidaten ----------------
def maak(w,rng,positie=None):
  band=rng.choice(list(BANDEN));p={'fase':w.fase,'positie':positie or rng.choice(POSITIES),'genre':rng.choice(list(GENRES)),'schaal':rng.choice(list(SCHALEN)),
   'volk':rng.choice(w.volken),'vorm':rng.choice([v for v in VORMEN if v!='nog niet gekozen']),'afloop':rng.choice(AFLOPEN),'hoofdpersoon':f'{band}|{rng.choice(GESLACHT)}',
   'leeftijd':BANDEN[band],'heat':rng.choice([0,0,1,2,3,4,5]),'partner':'volwassene','instemming':'ja','dwang_label':0}
  p['geslacht']=p['hoofdpersoon'].split('|')[1]
  for g,x in genrevector(p).items(): p['g_'+g]=x
  p['wereldregel_code']=w.wereldregel(p) if p['g_erotiek']>0 or p['volk']!='mens' else None
  if p['g_erotiek']>0 and not p['wereldregel_code']: p['g_erotiek']=0;p['heat']=0
  pos=POSITIES.index(p['positie'])
  p['erf_code']=(w.erf_van[pos%len(w.erf_van)] if w.erf_van and p['positie'] in('beslisser','betaler','profiteur') else w.erf_eigen) or (w.erf_van[0] if w.erf_van else None)
  p['zaadje_code']=w.zaadjes[(pos+AFLOPEN.index(p['afloop']))%len(w.zaadjes)] if w.zaadjes and p['afloop'] in('komt uit','keert om','faalt') else None
  p['kern_codes']=';'.join(w.kern[:6])
  p['drager']=kies_drager(w,p,band)
  return p
def kies_drager(w,p,band):
  """Z37: een drager met een Wil gaat voor (zonder Wil geen premisse); daarna dezelfde hash-keuze als in Z36."""
  dr=[d for d in w.dragers if d[1]==p['volk'] and (d[2] is None or d[2]==band)]
  met=[d for d in dr if d[3]] or dr
  return met[int(hashlib.md5(json.dumps([p[k] for k in ASSEN]).encode()).hexdigest(),16)%len(met)][0] if met else None
def code_van(p): return 'VP-'+p['fase'].split(' ')[0]+'-'+hashlib.md5(json.dumps([p[k] for k in ASSEN]+[p.get('g_erotiek')],ensure_ascii=False).encode()).hexdigest()[:8]
def pool(w,n,seed,dp=None):
  rng=random.Random(seed);out=[];afval=collections.Counter();gezien=set()
  for _ in range(n):
    p=maak(w,rng);k=tuple(p[a] for a in ASSEN)+(p['g_erotiek'],)
    if k in gezien: continue
    gezien.add(k);r=filter(w,p)
    if r: afval[r.split(':')[0]]+=1;continue
    if not minimum_ok(p,dp): afval['doelprofiel-minimum']+=1;continue
    out.append(scores(w,p,dp))
  return out,afval
# ---------------- selectie ----------------
def farthest(w,cands,n,W,dp=None,dekking=True):
  """Farthest-point sampling met de rijm- en afstandsfilters; gelijke afstand -> hoogste marginale winst. Eerst alle 7 posities."""
  gekozen=[]
  for _ in range(n):
    open_pos=[x for x in POSITIES if x not in {g['positie'] for g in gekozen}] if dekking else []
    best=None
    for p in cands:
      if p in gekozen or (open_pos and p['positie'] not in open_pos): continue
      if any(afstand(p,g)<3 for g in gekozen): continue
      d=min((afstand(p,b) for b in w.bestaand()+gekozen),default=7)
      sc=(d,nut(scores(w,dict(p),dp,gekozen),W,dp))
      if best is None or sc>best[0]: best=(sc,p)
    if not best: break
    p=best[1];scores(w,p,dp,gekozen);p['marginale_winst']=round(nut(p,W,dp),4);gekozen.append(p)
  return gekozen
def greedy(w,cands,n,W,dp=None):
  """Greedy op marginale winst: nieuwheid wordt steeds opnieuw gemeten tegen wat al gekozen is (afnemende meeropbrengst)."""
  gekozen=[]
  for _ in range(n):
    best=None
    for p in cands:
      if p in gekozen or any(afstand(p,g)<3 for g in gekozen): continue
      q=scores(w,dict(p),dp,gekozen);m=nut(q,W,dp)
      if best is None or m>best[0]: best=(m,p)
    if not best: break
    p=best[1];scores(w,p,dp,gekozen);p['marginale_winst']=round(best[0],4);gekozen.append(p)
  return gekozen
def fronten(cands,dp):
  rest=list(cands);out=[]
  while rest:
    f=[p for p in rest if not any(domineert(vec(q,dp),vec(p,dp)) for q in rest if q is not p)]
    out.append(f);rest=[p for p in rest if p not in f]
  return out
def gevoeligheid(lijst,W,dp=None,top=3):
  basis=sorted(lijst,key=lambda p:-nut(p,W,dp));t0=[id(p) for p in basis[:top]];wissel=collections.Counter();n=0
  for k in W:
    for f in (.9,1.1):
      w2=dict(W);w2[k]*=f;s=sum(w2.values());w2={a:b/s for a,b in w2.items()}
      t=[id(p) for p in sorted(lijst,key=lambda p:-nut(p,w2,dp))[:top]];n+=1
      for p in lijst:
        if (id(p) in t0)!=(id(p) in t): wissel[id(p)]+=1
  for p in lijst:
    if wissel[id(p)]: p['gevoeligheid']=f'close call (top-{top} wisselt bij {wissel[id(p)]} van {n} verschuivingen van ±10%)'
    elif id(p) in t0: p['gevoeligheid']=f'robuust (blijft in de top-{top} bij alle {n} verschuivingen van ±10%)'
    else: p['gevoeligheid']=f'robuust buiten de top-{top} ({n} verschuivingen)'
  return basis
K=['code','run','fase','positie','genre','schaal','volk','vorm','afloop','hoofdpersoon','leeftijd','geslacht','partner','instemming','dwang_label']+['g_'+g for g in G]+['erf_code','zaadje_code','wereldregel_code','kern_codes','herkomst','doelprofiel','nieuwheid','verbondenheid','seriewaarde','lezersvraag','kosten','genrematch','marginale_winst','gevoeligheid','uitslag','reden','drager','premisse','premisse_codes','seriewaarde_reden']
def bewaar(c,w,p,run,herkomst,dp=None,uitslag='voorgesteld',reden=None):
  """Schrijft een profiel in de ideeënbank. Filtert ALTIJD opnieuw: een profiel dat een harde grens schendt komt er nooit in."""
  r=filter(w,p) if uitslag in('voorgesteld','ent-klaar') else None
  if r: raise ValueError('filter weigert profiel: '+r)
  p=dict(p);p.setdefault('code',code_van(p))
  if p.get('premisse') is None: p['premisse'],p['premisse_codes']=premisse(c,p)
  p['run']=run;p['herkomst']=herkomst;p['doelprofiel']=dp['naam'] if dp else None;p['uitslag']=uitslag;p['reden']=reden
  return c.execute(f"insert or ignore into verhaal_profiel({','.join(K)}) values({','.join('?'*len(K))})",[p.get(k) for k in K]).rowcount
def regel(p,dp=None,extra=''):
  g=' '.join(f"{x[:3]}{p['g_'+x]}" for x in G)
  s=(f"{p.get('code') or code_van(p)} | {p['positie']} | {p['genre']} | {p['schaal']} | {p['volk']} | {p['vorm']} | {p['afloop']} | {p['hoofdpersoon']}\n"
     f"    genre: {g}\n    doelen: nieuwheid {p['nieuwheid']:.2f}, verbondenheid {p['verbondenheid']:.2f}, seriewaarde {p['seriewaarde']:.2f}, lezersvraag {p['lezersvraag']:.2f}, kosten {p['kosten']:.2f}"
     +(f", genrematch {p['genrematch']:.2f}" if dp else '')+(f"; marginale winst {p['marginale_winst']:.3f}" if p.get('marginale_winst') is not None else '')+'\n'
     f"    raakt: {p.get('erf_code') or '-'}; zaadje {p.get('zaadje_code') or '-'}; wereldregel/rite {p.get('wereldregel_code') or '-'}; drager {p.get('drager') or '(nieuw personage nodig)'}\n"
     f"    mag niet breken (v_kern): {p.get('kern_codes') or '-'}\n")
  if p.get('seriewaarde_reden'): s+=f"    seriewaarde: {p['seriewaarde_reden']}\n"
  if p.get('premisse') or 'premisse' in p: s+=f"    premisse: {p.get('premisse') or '(geen: '+(p.get('premisse_codes') or 'drager ontbreekt')+')'}\n"
  if p.get('gevoeligheid'): s+=f"    gevoeligheid: {p['gevoeligheid']}\n"
  return s+extra

# ---------------- Z37 (D1.3): premisse van één zin, alleen uit geraakte rijen ----------------
def _zin(t,n=140):
  t=re.sub(r'\s+',' ',(t or '').strip()).rstrip('.')
  t=re.split(r'(?<=[.;])\s',t)[0].rstrip('.;')
  return t if len(t)<=n else t[:n].rsplit(' ',1)[0]+' …'
LIDW=re.compile(r'^(Een|De|Het|Dat|Die|Dit|Deze|Zijn|Haar|Hun|Alle|Elke|Geen|Wie|Wat|In|Op|Na|Voor|Als|Ze|Hij|Zij|Er|Niet|Nooit|Om|Met|Van)\b')
def _klein(t): return t[:1].lower()+t[1:] if t and LIDW.match(t) else t
def premisse(c,p):
  """Z38 B2 (BESLUIT-Z38-12): premissen worden met de hand geschreven uit de rijen die het profiel raakt; de machine vult geen zin meer in.
  Bestaat er een handgeschreven premisse voor dezelfde drager en dezelfde ERF-rij, dan wordt die getoond; anders geen premisse.
  (De oude invulzin staat in z36/machine_backup_Z38.py.)"""
  dr=p.get('drager');erf=p.get('erf_code')
  if not dr: return None,'geen premisse: geen drager (nieuw personage nodig)'
  try:
    r=c.execute("select premisse,premisse_codes from verhaal_profiel where drager=? and coalesce(erf_code,'')=coalesce(?,'') and premisse is not null and premisse not like 'geen premisse%' and coalesce(vervangen_door,'')='' limit 1",(dr,erf)).fetchone()
  except Exception: r=None
  if r: return r[0],r[1]
  return None,'geen premisse: met de hand te schrijven uit de geraakte rijen (BESLUIT-Z38-12)'
