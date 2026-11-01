"""Z39 11c: module technologie + beroepen op hetzelfde patroon (actoren = regio's, regels met bron, kansen, runs, storyteller, eigen invariant).
Uitvindingen komen uit de canon van fase 4; elke verspreiding kost lichamen (genre-wet 2: GENRE-wet2-V4); kennis kan vergeten worden (de Makers).
Beroepen: een beroep ontstaat pas waar zijn wereldregel-techniek bestaat; zijn zwarte tweeling pas waar het beroep bestaat (tabel beroep, Z37)."""
import random,zlib,collections,statistics,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import sim
TECH={ # code: (oorsprong, vereist, kans per jaar na vereiste, wie betaalt (canon), canonrij, canonjaar)
 'register':('saelith',None,0.06,'vrouwen zonder kind en clans (FASE-noodtoestand)','GEB-r10-eerste-register',22),
 'bloedmerk':('saelith','register',0.10,'vervalsers en wie geen merk heeft (GEB-r10-bloedmerk)','GEB-r10-bloedmerk',28),
 'jongenshof':('saelith','register',0.04,'moeders die hun zoon afstaan, niet-seksueel (GEB-r10-jongenshof)','GEB-r10-jongenshof',50),
 'rooster':('saelith','register',0.02,'mannen, uitgeput (GEB-r10-uitputting)','GEB-r10-rotatie',78),
 'makerskennis':('saelith',None,None,'iedereen die het zaaischip nog kende (GENRE-wet2-V4)','GENRE-wet2-V4',None),
}
TYPEN=[('uitvinding','technologie','Een techniek ontstaat in haar oorsprongsregio.','geen verspreiding vóór uitvinding','GENRE-wet2-V4'),
 ('verspreiding','technologie','Een techniek bereikt een buurregio langs een route (reistijd).','alleen vanuit een regio die haar heeft','KAART-seizoenen'),
 ('prijs','technologie','Een verspreiding kost lichamen; wie betaalt komt uit de canon.','prijs > 0 bij elke verspreiding','GENRE-wet2-V4'),
 ('vergeten','technologie','Een techniek verdwijnt uit een regio.','vergeten techniek verspreidt niet meer vanuit die regio','GENRE-wet2-V4'),
 ('beroep','beroepen','Een beroep ontstaat in een regio waar zijn techniek bestaat.','geen beroep zonder techniek in de regio','ERF-noodtoestand'),
 ('zwarte_tweeling','beroepen','De zwarte tweeling van een beroep ontstaat waar het beroep al bestaat.','geen tweeling vóór het beroep','ERF-noodtoestand')]
BEROEP_TECH={'BEROEP-Z37-jongensverstopster':'jongenshof','BEROEP-Z37-naamgever':'register','BEROEP-Z37-nee-getuige':'register'}
def run(seed,beroepen,jaren=(0,130)):
  st=lambda *k:random.Random(zlib.crc32(repr((seed,)+k).encode()))
  heeft=collections.defaultdict(dict);ev=[];vergeten=collections.defaultdict(set)
  for k in sim.REG: heeft[k]['makerskennis']=jaren[0]
  for j in range(jaren[0],jaren[1]+1):
    r=st('j',j)
    for t,(o,req,p,wie,cc,cj) in TECH.items():
      if p and t not in heeft[o] and (req is None or req in heeft[o]) and r.random()<p:
        heeft[o][t]=j;ev.append((j,'uitvinding',t,o,None,0,cc))
    for k in list(sim.REG):
      for t,sinds in list(heeft[k].items()):
        if t=='makerskennis':
          if r.random()<0.03: del heeft[k][t];vergeten[k].add(t);ev.append((j,'vergeten',t,k,None,0,'GENRE-wet2-V4'))
          continue
        for b in sim.REG:
          rt=sim.reis(k,b)
          if rt and t not in heeft[b] and t not in vergeten[b] and j-sinds>=rt and r.random()<0.08/rt:
            heeft[b][t]=j;n=r.randint(1,12);ev.append((j,'verspreiding',t,b,k,0,None));ev.append((j,'prijs',t,b,TECH[t][3],n,None))
    for bc,(naam,tw) in beroepen.items():
      t=BEROEP_TECH.get(bc)
      if not t: continue
      for k in sim.REG:
        if t in heeft[k] and (bc,k) not in {(e[2],e[3]) for e in ev if e[1]=='beroep'} and r.random()<0.05: ev.append((j,'beroep',bc,k,naam,0,None))
        if (bc,k) in {(e[2],e[3]) for e in ev if e[1]=='beroep'} and (bc,k) not in {(e[2],e[3]) for e in ev if e[1]=='zwarte_tweeling'} and r.random()<0.03: ev.append((j,'zwarte_tweeling',bc,k,tw,0,None))
  return ev
def invariant(ev):
  f=[];heeft=collections.defaultdict(set);ber=set()
  for k in sim.REG: heeft[k].add('makerskennis')
  for (j,typ,t,k,x,n,cc) in ev:
    if typ=='uitvinding': heeft[k].add(t)
    elif typ=='verspreiding':
      if t not in heeft[x]: f.append(f'{t} verspreid vanuit {x} dat haar niet heeft ({j})')
      heeft[k].add(t)
    elif typ=='prijs' and n<=0: f.append(f'verspreiding van {t} zonder prijs')
    elif typ=='vergeten': heeft[k].discard(t)
    elif typ=='beroep':
      if BEROEP_TECH[t] not in heeft[k]: f.append(f'{t} in {k} zonder {BEROEP_TECH[t]}')
      ber.add((t,k))
    elif typ=='zwarte_tweeling' and (t,k) not in ber: f.append(f'tweeling van {t} in {k} vóór het beroep')
  return f
def draai(c,N=1000,basis=391000):
  beroepen={b:(n,tw) for b,n,tw in c.execute('select code,naam,zwarte_tweeling from beroep')}
  R=[]
  for i in range(N):
    ev=run(basis+i,beroepen);f=invariant(ev)
    eerst={}
    for e in ev:
      if e[1]=='uitvinding': eerst.setdefault(e[2],e[0])
    R.append({'run_id':f'Z39-TECH-{i:04d}','seed':basis+i,'geldig':0 if f else 1,'reden':'; '.join(f[:3]) or None,'ev':ev,'eerst':eerst,
      'scores':{'verspreidingen':sum(e[1]=='verspreiding' for e in ev),'lichamen':sum(e[5] for e in ev if e[1]=='prijs'),'beroepen':sum(e[1]=='beroep' for e in ev),'tweelingen':sum(e[1]=='zwarte_tweeling' for e in ev),'vergeten':sum(e[1]=='vergeten' for e in ev)}})
  return R,beroepen
def rapport(R,beroepen):
  G=[r for r in R if r['geldig']];n=len(G) or 1;out={}
  for t,(o,req,p,wie,cc,cj) in TECH.items():
    if not p: continue
    jr=[r['eerst'][t] for r in G if t in r['eerst']]
    out[t]={'ontstaat_%':round(100*len(jr)/n,1),'mediaan':statistics.median(jr) if jr else None,'canon':cj,'binnen_10j_%':round(100*sum(abs(x-cj)<=10 for x in jr)/n,1)}
  out['makerskennis_vergeten_in_alle_regios_%']=round(100*sum(all(any(e[1]=='vergeten' and e[3]==k for e in r['ev']) for k in sim.REG) for r in G)/n,1)
  for b in beroepen:
    out['beroep '+b]=('%.1f%% runs; tweeling in %.1f%%'%(100*sum(any(e[1]=='beroep' and e[2]==b for e in r['ev']) for r in G)/n,100*sum(any(e[1]=='zwarte_tweeling' and e[2]==b for e in r['ev']) for r in G)/n)) if b in BEROEP_TECH else 'niet in fase 4: de techniek van zijn wereldregel bestaat nog niet'
  return out
