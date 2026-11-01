# Opdrachten van de verhalenmachine (Z36), aangeroepen via vraag.py. Alleen --bewaar schrijft; al het andere leest.
import sys,json,random,math,collections,hashlib,datetime,os
import machine as M
def opt(a,naam,std=None):
  return a[a.index(naam)+1] if naam in a else std
def kop(w,W,dp):
  print(f"# {w.fase}: volken {', '.join(w.volken)}; bestaande bogen {len(w.bogen)}, eerdere profielen {len(w.profielen)}")
  print('gewichten: '+', '.join(f'{k} {v:.2f}' for k,v in W.items())+(f"; doelprofiel {dp['naam']} (min "+', '.join(f'{g}>={v}' for g,v in dp['min'].items() if v)+')' if dp else ''))
def bedenk(c,a):
  w=M.Wereld(c,a[1],opt(a,'--run'));n=int(a[2]) if len(a)>2 and a[2].isdigit() else 10
  dp=M.doelprofiel(c,opt(a,'--profiel'));W=M.gewichten(c)
  seed=int(hashlib.md5(f"{w.fase}|{n}|{dp and dp['naam']}|{opt(a,'--run')}".encode()).hexdigest(),16)%10**8
  cands,afval=M.pool(w,int(opt(a,'--pool',4000)),seed,dp)
  kop(w,W,dp);print(f"kandidaten na filters: {len(cands)}; afgevallen: {dict(afval)}")
  gek=M.farthest(w,cands,n,W,dp);M.gevoeligheid(gek,W,dp)
  print(f"\n## {len(gek)} profielen (farthest-point, eerst alle zeven posities, daarna marginale winst)\n")
  for i,p in enumerate(gek,1): print(f'{i}. '+M.regel(p,dp))
  if '--bewaar' in a:
    run=opt(a,'--run');assert run,'--bewaar vraagt --run'
    print('bewaard:',sum(M.bewaar(c,w,p,run,'machine bedenk',dp) for p in gek));c.commit()
  return gek
def pareto(c,a):
  w=M.Wereld(c,a[1],opt(a,'--run'));n=int(a[2]) if len(a)>2 and a[2].isdigit() else 10
  dp=M.doelprofiel(c,opt(a,'--profiel'));W=M.gewichten(c)
  seed=int(hashlib.md5(f"pareto|{w.fase}|{n}|{dp and dp['naam']}".encode()).hexdigest(),16)%10**8
  cands,afval=M.pool(w,int(opt(a,'--pool',3000)),seed,dp)
  kop(w,W,dp);fr=M.fronten(cands,dp)
  print(f"kandidaten na filters: {len(cands)}; afgevallen: {dict(afval)}; Pareto-fronten: {len(fr)} (eerste front {len(fr[0]) if fr else 0} profielen)")
  sel=M.greedy(w,fr[0] if len(fr[0])>=n else [p for f in fr[:3] for p in f],n,W,dp);M.gevoeligheid(sel,W,dp)
  print(f"\n## {len(sel)} uit het eerste front (greedy op marginale winst; niemand hierboven wordt op alle doelen tegelijk verslagen)\n")
  for i,p in enumerate(sel,1): print(f'{i}. '+M.regel(p,dp))
  return sel
def volgende(c,a):
  """Thompson sampling: welk genre/welke lege positie eerst. Prior per genre (aanname) + lezersdata."""
  rng=random.Random(int(opt(a,'--seed',1)));gaten=c.execute('select fase,positie from v_positie_dekking where in_canon=0 and in_ideeenbank=0').fetchall()
  w=M.Wereld(c,a[1] if len(a)>1 and not a[1].startswith('--') else '801')
  tr=collections.Counter()
  for _ in range(1000):
    s={g:rng.betavariate(w.prior.get(g,.5)*10+w.lezers[g][0],(1-w.prior.get(g,.5))*10+w.lezers[g][1]) for g in M.GENRES};tr[max(s,key=s.get)]+=1
  print('Thompson sampling (1000 trekkingen): '+', '.join(f'{g} {n/10:.1f}%' for g,n in tr.most_common()))
  print('lege posities (geen boog en geen profiel):',len(gaten));[print(' ',f,p) for f,p in gaten[:30]]
def gewicht(c,a):
  W=M.gewichten(c)
  if a[1]=='swing':
    # vraag.py gewicht swing kosten:10,lezersvraag:40,nieuwheid:60,seriewaarde:80,verbondenheid:100   (punten 0-100 voor de swing van slechtste naar beste)
    pt={k:float(v) for k,v in (x.split(':') for x in a[2].split(','))};s=sum(pt.values());nw={k:round(v/s,3) for k,v in pt.items()}
    print('swing-gewichten:',nw)
    if '--bewaar' in a:
      c.execute('insert or ignore into gewichtset(naam,datum,methode,status,gewichten,bron) values(?,?,?,?,?,?)',(opt(a,'--naam','lancering serie'),str(datetime.date.today()),'swing','voorlopig',json.dumps(nw),'vraag.py gewicht swing '+a[2]));c.commit()
  elif a[1]=='paren':
    # bestand met regels "A>B" (A en B zijn profielcodes); Bradley-Terry op de doelvectoren (logistische regressie, gradient)
    paren=[l.strip().split('>') for l in open(a[2]) if '>' in l]
    vp={r[0]:r[1:] for r in c.execute('select code,nieuwheid,verbondenheid,seriewaarde,lezersvraag,kosten from verhaal_profiel')}
    ks=['nieuwheid','verbondenheid','seriewaarde','lezersvraag','kosten'];b=[0.0]*5
    for _ in range(400):
      g=[0.0]*5
      for x,y in paren:
        d=[(vp[x][i]-vp[y][i])*(-1 if ks[i]=='kosten' else 1) for i in range(5)];pr=1/(1+math.exp(-sum(bi*di for bi,di in zip(b,d))))
        for i in range(5): g[i]+=(1-pr)*d[i]
      b=[bi+.5*gi/len(paren)-.01*bi for bi,gi in zip(b,g)]
    pos=[max(0,x) for x in b];s=sum(pos) or 1;nw={k:round(v/s,3) for k,v in zip(ks,pos)}
    print(f'Bradley-Terry uit {len(paren)} keuzes: coëfficiënten',dict(zip(ks,[round(x,3) for x in b])),'-> gewichten',nw)
    u=lambda x:sum(bi*(vp[x][i]*(-1 if ks[i]=='kosten' else 1)) for i,bi in enumerate(b))
    tegen=[(x,y) for x,y in paren if u(x)<u(y)];dubbel={(x,y) for x,y in paren if [y,x] in paren}
    print(f'consistentie: {len(paren)-len(tegen)} van {len(paren)} keuzes passen bij de fit; {len(tegen)} spreken haar tegen (twijfelpunten); {len(dubbel)//2} paren werden beide kanten op gekozen')
    for x,y in tegen[:5]: print('  twijfel:',x,'>',y)
    if '--bewaar' in a:
      c.execute('insert or ignore into gewichtset(naam,datum,methode,status,gewichten,bron) values(?,?,?,?,?,?)',(opt(a,'--naam','lancering serie'),str(datetime.date.today()),'paren (Bradley-Terry)','voorlopig',json.dumps(nw),f'{len(paren)} keuzes uit {a[2]}'));c.commit()
    return nw
  elif a[1]=='toon':
    # vraag.py gewicht toon <fase>: 20 paren van het Pareto-front om te kiezen (A of B); schrijf de keuzes als 'A>B' in een bestand en geef dat aan 'paren'
    f,_=M.fase_naam(c,a[2]);ks=['code']+M.ASSEN+['g_'+g for g in M.G]+['nieuwheid','verbondenheid','seriewaarde','lezersvraag','kosten','erf_code','zaadje_code','wereldregel_code','drager','kern_codes']
    st=[dict(zip(ks,r)) for r in c.execute('select '+','.join(ks)+" from verhaal_profiel where fase=? and uitslag in('voorgesteld','ent-klaar')",(f,))]
    fr=M.fronten(st,None)[0] if st else [];rng=random.Random(11)
    print(f'{len(st)} bewaarde profielen in {f}, waarvan {len(fr)} op het Pareto-front; kies per paar A of B en schrijf "CODE_A>CODE_B" in een bestand')
    for i in range(min(20,len(fr)*(len(fr)-1)//2)):
      x,y=rng.sample(fr,2)
      print(f'paar {i+1}:\n  A '+M.regel(x).replace(chr(10),chr(10)+'  ')+'  B '+M.regel(y).replace(chr(10),chr(10)+'  '))
def afstand(c,a):
  def get(code):
    r=c.execute('select code,'+','.join(M.ASSEN)+' from verhaal_profiel where code=? union all select boog_code,'+','.join(M.ASSEN)+' from boog_as where boog_code=?',(code,code)).fetchone()
    return dict(zip(['code']+M.ASSEN,r))
  x,y=get(a[1]),get(a[2]);print(f"afstand {M.afstand(x,y)}: verschilt op "+', '.join(k for k in M.ASSEN if x[k]!=y[k]))
def dekking(c,a):
  rs=c.execute('select fase,positie,in_canon,in_ideeenbank from v_positie_dekking').fetchall();fs=list(dict.fromkeys(r[0] for r in rs))
  print('fase | '+' | '.join(p[:10] for p in M.POSITIES))
  for f in fs: print(f+' | '+' | '.join(f'{x}+{y}' for ff,p,x,y in rs if ff==f))
  print('(canon+ideeënbank; 0+0 is een gat)')
def ideeenrapport(c,a):
  t=c.execute("select count(*),sum(uitslag='uitval: afstand'),sum(uitslag='uitval: verbinding'),sum(uitslag='ent-klaar'),sum(uitslag='uitval: geen fase'),sum(uitslag like 'uitval: filter%') from ideeen_verwerking").fetchone()
  print(f'instroom {t[0]}; uitval afstand {t[1]}; uitval verbinding {t[2]}; uitval filter {t[5]}; geen fase {t[4]}; ent-klaar {t[3]}')
  for r in c.execute('select fase,sum(instroom),sum(uitval_afstand),sum(uitval_verbinding),sum(ent_klaar),sum(geen_fase) from v_ideeen_rapport group by 1'): print('  fase',r[0],': instroom',r[1],'| afstand',r[2],'| verbinding',r[3],'| ent-klaar',r[4])
  if '--positie' in a:
    print('  per fase en positie (instroom, uitval afstand, uitval verbinding, ent-klaar):')
    for r in c.execute("select fase,positie,instroom,uitval_afstand,uitval_verbinding,ent_klaar from v_ideeen_rapport where fase!='(geen fase)' order by 1,2"): print('   ',' | '.join(str(x) for x in r))
CMD={'bedenk':bedenk,'pareto':pareto,'volgende':volgende,'gewicht':gewicht,'afstand':afstand,'dekking':dekking,'ideeenrapport':ideeenrapport}
