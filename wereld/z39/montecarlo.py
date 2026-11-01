"""Z39 11b.5-6: Monte Carlo (N runs) + storyteller (Pareto, stap 8; gewichtset, stap 9b). Elke run is reproduceerbaar: seed = basis + i."""
import sys,os,json,collections,statistics
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import sim
BASIS=390000
CANON={'GEB-deelwet-40':(40,40),'GEB-r10-eerste-register':(22,22),'GEB-r10-jongenshof':(50,50),'GEB-r10-rotatie':(78,78),'GEB-r10-orde-naam':(90,90),
       'GEB-r10-eilanden-weigering':(100,130),'GEB-r10-mannenroof':(18,35),'GEB-r10-neven-ramp':(33,38),'GEB-r10-deelwet-weerstand':(41,60),'GEB-r10-uitputting':(60,80)}
OBJ=('intrige','ommekeer','verbinding','rijm','doelmatch')
def typen(c): return sim.laad_typen(c)
def een(c,T,P,i,bescherm=True,fase=sim.FASE,alwetend=False,basis=BASIS):
  w=sim.Wereld(basis+i,P,T,None,bescherm,fase,alwetend).run();f=sim.invarianten(w);h=sim.canon_hits(w)
  return w,f,h
def draai(c,N=1000,bescherm=True,fase_nr=4,fase=sim.FASE,alwetend=False,basis=BASIS,prefix='Z39-F4'):
  T=typen(c);P=sim.seed_personen(c,fase_nr);R=[]
  for i in range(N):
    w,f,h=een(c,T,P,i,bescherm,fase,alwetend,basis)
    eerst={}
    for e in w.ev:
      if e[7] in CANON and e[7] not in eerst: eerst[e[7]]=e[0]
    R.append({'run_id':f'{prefix}-{i:04d}','seed':basis+i,'uitkomst':uitkomst(w),'geldig':0 if f else 1,'reden':'; '.join(f) or None,'scores':sim.score(w,h),'hits':h,'eerst':eerst,'stem':w.stem})
  return R
def uitkomst(w):
  """Vergelijkbare uitkomst van een run (voor de informatieproef): instituten met jaar, wie chanteert/verraadt wie, wie sterft wanneer."""
  inst=tuple(sorted(w.wetjaar.items()))
  rel=frozenset((e[2],e[3],e[4]) for e in w.ev if e[2] in('chantage','verraad','verbintenis','eed','ruzie'))
  dood=frozenset((p['code'],p['dood']) for p in w.P.values() if p['dood'] is not None and not p.get('fig'))
  return {'inst':inst,'rel':rel,'dood':dood,'chantage':sum(e[2]=='chantage' for e in w.ev),'verraad':sum(e[2]=='verraad' for e in w.ev)}
def pareto(R):
  G=[r for r in R if r['geldig']];rang={};rest=list(range(len(G)));k=0
  def dom(a,b): return all(a[o]>=b[o] for o in OBJ) and any(a[o]>b[o] for o in OBJ)
  while rest:
    k+=1;front=[i for i in rest if not any(dom(G[j]['scores'],G[i]['scores']) for j in rest if j!=i)]
    for i in front: rang[G[i]['run_id']]=k
    rest=[i for i in rest if i not in front]
  mx={o:max(r['scores'][o] for r in G) or 1 for o in OBJ+('gebeurtenissen',)};mn={o:min(r['scores'][o] for r in G) for o in OBJ+('gebeurtenissen',)}
  nm=lambda r,o:(r['scores'][o]-mn[o])/((mx[o]-mn[o]) or 1)
  for r in R:
    r['pareto_rang']=rang.get(r['run_id'])
    r['gewogen']=round(0.30*nm(r,'verbinding')+0.25*nm(r,'rijm')+0.20*nm(r,'ommekeer')+0.15*nm(r,'intrige')+0.10*(1-nm(r,'gebeurtenissen')),4) if r['geldig'] else None
  top=sorted([r for r in R if r['geldig']],key=lambda r:(r['pareto_rang'],-r['gewogen']))[:5]
  return top
def validatie(R):
  G=[r for r in R if r['geldig']];n=len(G);out={}
  for k,(a,b) in CANON.items():
    jr=[r['eerst'][k] for r in G if k in r['eerst']]
    out[k]={'ontstaat':round(100*len(jr)/n,1),'binnen_10j':round(100*sum(a-10<=x<=b+10 for x in jr)/n,1),'mediaan':statistics.median(jr) if jr else None,'canon':f'{a}' if a==b else f'{a}-{b}'}
  st=collections.Counter(tuple(r['stem']) for r in G);out['raad 7-5 (jaar -3)']={'ontstaat':round(100*st[(7,5)]/n,1),'verdeling':{f'{a}-{b}':v for (a,b),v in sorted(st.items(),reverse=True)}}
  return out
