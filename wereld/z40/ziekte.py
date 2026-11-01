"""Z40: module ziekte (opdracht_Z35.md stap 11c; BESLUIT-Z40-8). Valideringstest: de Pest van 340 (GEB-pest-340, GEB-r10-pest-oorsprong, GEB-r10-pest-qesh).
Model: stochastisch SEIR per regio, alleen mannen (aanname: de koorts zit in de mannenvertrekken, GEB-pest-340), maandstappen 330-350.
Oorsprong: de fokstallen van Hal-Neth (Saelith), met verwante lijnen en overvolle stallen. De kans dat daar een koorts ontstaat, groeit met de drukte;
het jaar volgt uit het model, niet uit de canon. Verspreiding: langs de rotatiekringen (mannen reizen sinds de rotatie, GEB-r10-rotatie) en de
karavaanroute naar Qesh. Qesh kan de karavaanroutes sluiten zodra het nieuws er is (GEB-r10-pest-qesh: 'Isolatie').
Geen personen, geen seksuele gebeurtenissen: alleen tellingen. Elke run is reproduceerbaar via seed."""
import random,zlib,math,statistics,collections
REG=('halneth','saelith','ambergaard','zoutkust','groenmuil','hoogvrouwe','stille','qesh')
# mannen per regio in fase 6 vóór de Pest (aanname; relatieve grootte uit REG-overzicht; stallen van Hal-Neth apart)
MANNEN={'halneth':150,'saelith':1200,'ambergaard':900,'zoutkust':600,'groenmuil':400,'hoogvrouwe':300,'stille':150,'qesh':500}
# koppeling: maandelijks contact via rotatiekringen (aanname: 0.04/reistijd) en karavaan naar Qesh (aanname)
BUUR={('halneth','saelith'):1e-4,  # afgesloten stallen (GEB-r10-pest-oorsprong): zelden contact naar buiten (aanname op de canonzin)
      ('saelith','ambergaard'):0.04,('saelith','zoutkust'):0.04,('saelith','groenmuil'):0.02,('zoutkust','groenmuil'):0.04,
      ('zoutkust','stille'):0.04,('ambergaard','hoogvrouwe'):0.04,('saelith','stille'):0.02,('saelith','qesh'):0.02}
P={ # parameter: (waarde, bron, aanname)
 'beta_stal':(10.0,'GEB-r10-pest-oorsprong (overvolle stallen)',1),       # per maand, R0 ~5 in de stallen
 'beta':(3.6,'aanname: R0 ~1,8 onder mannen buiten de stallen',1),
 'sigma':(2.0,'aanname: incubatie ~2 weken',1),
 'gamma':(2.0,'aanname: ziekteduur ~2 weken',1),
 'cfr':(0.35,'geijkt op GEB-pest-340 (een derde van de mannen); gevoeligheid: 0.3-0.5 in scorekaart',1),
 'vatbaar_verwant':(1.5,'GEB-r10-pest-oorsprong (verwante lijnen)',1),
 'ontstaan':(0.004,'aanname: kans per maand per drukte-eenheid dat in Hal-Neth een koorts ontstaat',1),
 'drukte_sinds':(320,'aanname: de stallen raken vol vanaf 320 (fokkerij, GEB-r10-pest-oorsprong)',1),
 'nieuws':(2,'aanname: maanden voor het nieuws Qesh bereikt (karavaan, koeriers)',1),
 'gerucht':(20,'aanname: aantal doden voordat er een gerucht naar Qesh gaat',1),
 'sluiten':(0.4,'GEB-r10-pest-qesh: Qesh sluit de karavaanroutes; kans per maand na het nieuws (aanname)',1),
}
def w(a,b): return BUUR.get((a,b)) or BUUR.get((b,a)) or 0
def binom(r,n,p):
  if n<=0 or p<=0: return 0
  if p>=1: return n
  if n<40: return sum(1 for _ in range(n) if r.random()<p)
  m=n*p;sd=math.sqrt(n*p*(1-p));return max(0,min(n,int(round(r.gauss(m,sd)))))
def run(seed,sluit=True,jaren=(330,350)):
  st=lambda *k:random.Random(zlib.crc32(repr((seed,)+k).encode()))
  S={k:MANNEN[k] for k in REG};E=dict.fromkeys(REG,0);I=dict.fromkeys(REG,0);R=dict.fromkeys(REG,0);D=dict.fromkeys(REG,0)
  ev=[];index=None;dicht=None;nieuws=None;eerst={}
  for j in range(jaren[0],jaren[1]+1):
    for m in range(12):
      r=st(j,m);t=j+m/12
      if index is None:
        drukte=max(0,(t-P['drukte_sinds'][0])/10)
        if r.random()<P['ontstaan'][0]*drukte*P['vatbaar_verwant'][0]:
          index=(j,m);E['halneth']+=1;S['halneth']-=1;eerst['halneth']=j;ev.append((j,m,'index','halneth',None,1,'GEB-r10-pest-oorsprong'))
      for k in REG:
        N=MANNEN[k];b=P['beta_stal'][0] if k=='halneth' else P['beta'][0];v=P['vatbaar_verwant'][0] if k=='halneth' else 1.0
        druk=I[k]/N
        for o in REG:
          ww=w(k,o)
          if ww and not (dicht and 'qesh' in (k,o)): druk+=ww*I[o]/MANNEN[o]
        p_inf=1-math.exp(-b*v*druk)  # beta is per maand
        nE=binom(r,S[k],min(1,p_inf))
        nI=binom(r,E[k],1-math.exp(-P['sigma'][0]))
        nU=binom(r,I[k],1-math.exp(-P['gamma'][0]))
        nD=binom(r,nU,P['cfr'][0])
        S[k]-=nE;E[k]+=nE-nI;I[k]+=nI-nU;R[k]+=nU-nD;D[k]+=nD
        if nI and k not in eerst: eerst[k]=j;ev.append((j,m,'besmetting_regio',k,None,nI,'GEB-pest-340'))
        if nD: ev.append((j,m,'sterfte',k,None,nD,'GEB-pest-340'))
      if sluit and index and dicht is None:
        if nieuws is None and any(I[k] for k in REG if k!='qesh') and sum(D.values())>=P['gerucht'][0]: nieuws=(j,m)
        if nieuws and (j-nieuws[0])*12+(m-nieuws[1])>=P['nieuws'][0] and r.random()<P['sluiten'][0]:
          dicht=(j,m);ev.append((j,m,'route_dicht','qesh','saelith',0,'GEB-r10-pest-qesh'))
  return {'S':S,'E':E,'I':I,'R':R,'D':D,'ev':ev,'index':index,'dicht':dicht,'eerst':eerst}
def invariant(x):
  f=[]
  for k in REG:
    tot=x['S'][k]+x['E'][k]+x['I'][k]+x['R'][k]+x['D'][k]
    if tot!=MANNEN[k]: f.append(f'{k}: telling klopt niet ({tot} != {MANNEN[k]})')
    if min(x['S'][k],x['E'][k],x['I'][k],x['R'][k],x['D'][k])<0: f.append(f'{k}: negatief')
  if x['index'] is None and sum(x['D'].values()): f.append('sterfte zonder indexgeval')
  for (j,m,typ,k,o,n,cc) in x['ev']:
    if x['index'] and (j,m)<x['index']: f.append('gebeurtenis vóór het indexgeval');break
  return f
def scores(x):
  tot=sum(MANNEN.values());dood=sum(x['D'].values());rest=[k for k in REG if k!='qesh']
  q=x['D']['qesh']/MANNEN['qesh'];o=sum(x['D'][k] for k in rest)/sum(MANNEN[k] for k in rest)
  piek=collections.Counter()
  for (j,m,typ,k,_,n,_) in x['ev']:
    if typ=='sterfte': piek[j]+=n
  return {'sterfte_mannen':round(dood/tot,3),'sterfte_qesh':round(q,3),'sterfte_rest':round(o,3),'index_jaar':x['index'][0] if x['index'] else None,
          'piekjaar':piek.most_common(1)[0][0] if piek else None,'qesh_dicht':x['dicht'][0] if x['dicht'] else None,'gebeurtenissen':len(x['ev'])}
def draai(N=1000,basis=402000,sluit=True,prefix='Z40-ZIEKTE'):
  out=[]
  for i in range(N):
    x=run(basis+i,sluit);f=invariant(x)
    out.append({'run_id':f'{prefix}-{i:04d}','seed':basis+i,'geldig':0 if f else 1,'reden':'; '.join(f[:3]) or None,'scores':scores(x),'ev':x['ev']})
  return out
def validatie(R,R0=None):
  G=[r for r in R if r['geldig']];n=len(G) or 1
  ont=[r for r in G if r['scores']['sterfte_mannen']>=0.10]  # de koorts ontsnapt uit Hal-Neth
  esc={'ontsnapt_uit_halneth_%':round(100*len(ont)/n,1)}
  if ont:
    esc.update({'bij_ontsnapping_sterfte_mediaan':statistics.median(r['scores']['sterfte_mannen'] for r in ont),
      'bij_ontsnapping_een_derde_%':round(100*sum(0.25<=r['scores']['sterfte_mannen']<=0.42 for r in ont)/len(ont),1),
      'bij_ontsnapping_piekjaar_mediaan':statistics.median(r['scores']['piekjaar'] for r in ont),
      'bij_ontsnapping_vertraging_index_tot_piek_mediaan':statistics.median(r['scores']['piekjaar']-r['scores']['index_jaar'] for r in ont),
      'bij_ontsnapping_qesh_lager_dan_half_%':round(100*sum(r['scores']['sterfte_qesh']<0.5*r['scores']['sterfte_rest'] for r in ont)/len(ont),1)});s=lambda k:[r['scores'][k] for r in G if r['scores'][k] is not None]
  ontstaan=[r for r in G if r['scores']['index_jaar'] is not None]
  v={'runs':len(R),'geldig':len(G),'pest_ontstaat_%':round(100*len(ontstaan)/n,1),
     'indexjaar_mediaan':statistics.median(s('index_jaar')) if ontstaan else None,'indexjaar_336_340_%':round(100*sum(336<=x<=340 for x in s('index_jaar'))/n,1),
     'piekjaar_mediaan':statistics.median(s('piekjaar')) if ontstaan else None,'piek_338_342_%':round(100*sum(338<=x<=342 for x in s('piekjaar'))/n,1),
     'sterfte_mannen_mediaan':statistics.median(s('sterfte_mannen')),'een_derde_(25-42%)_%':round(100*sum(0.25<=x<=0.42 for x in s('sterfte_mannen'))/n,1),
     'qesh_lager_dan_half_rest_%':round(100*sum(1 for r in ontstaan if r['scores']['sterfte_qesh']<0.5*r['scores']['sterfte_rest'])/max(1,len(ontstaan)),1),
     'qesh_dicht_mediaan':statistics.median([x for x in s('qesh_dicht')]) if s('qesh_dicht') else None}
  v.update(esc)
  if R0:
    G0=[r for r in R0 if r['geldig'] and r['scores']['sterfte_mannen']>=0.10]
    v['bij_ontsnapping_qesh_sterfte_zonder_sluiting_mediaan']=statistics.median([r['scores']['sterfte_qesh'] for r in G0]) if G0 else None
    v['bij_ontsnapping_qesh_sterfte_met_sluiting_mediaan']=statistics.median([r['scores']['sterfte_qesh'] for r in ont]) if ont else None
  return v
