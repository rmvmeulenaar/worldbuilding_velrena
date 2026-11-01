"""Z39 11a.5: graafvragen over verblijf, kennis, per_relatie en wil. Gebruik: vraag.py intrige <complot|chantage|rivaliteit|erfwrok> [PLEK] [JAAR]"""
import sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import sim
def _wil(c):
  w={a:sim.wilsoort(b) for a,b in c.execute('select code,wil from personage_profiel')}
  w.update({a:'overleven' for (a,) in c.execute('select code from sim_figuur')});return w
def _naam(c):
  n={a:b for a,b in c.execute('select code,naam from personage_profiel')};n.update({a:b for a,b in c.execute('select code,naam from sim_figuur')});return n
def plek(c,per,jaar):
  r=c.execute("select plek_code from verblijf where per_code=? and van_jaar<=? and (tot_jaar is null or tot_jaar>=?) order by van_jaar desc limit 1",(per,jaar,jaar)).fetchone()
  return r[0] if r else None
def leeft(c,per,jaar): return plek(c,per,jaar) not in (None,)
def rel(c,soort,jaar):
  return [(a,b,vj) for a,b,vj in c.execute("select van_code,naar_code,van_jaar from per_relatie where soort=? and van_jaar<=? and (tot_jaar is null or tot_jaar>=?)",(soort,jaar,jaar))]
def complot(c,P,J):
  """personages die hetzelfde willen en dezelfde vijand hebben (vijand = rivaal_van of verraden_door)"""
  W=_wil(c);vijand=collections.defaultdict(set)
  for a,b,_ in rel(c,'rivaal_van',J)+rel(c,'verraden_door',J): vijand[a].add(b)
  out=[]
  ks=[k for k in vijand if not P or plek(c,k,J)==P]
  for i,a in enumerate(ks):
    for b in ks[i+1:]:
      gem=vijand[a]&vijand[b]
      if gem and W.get(a)==W.get(b): out.append((a,b,sorted(gem),W.get(a)))
  return out
def chantage(c,P,J):
  """iemand weet een geheim van een ander, binnen bereikbare reistijd (<=1 seizoen)"""
  out=[]
  for wie,wat,sj in c.execute("select per_code,weet_code,sinds_jaar from kennis where weet_code like '%#geheim' and sinds_jaar<=?",(J,)):
    doel=wat.split('#')[0];pa,pb=plek(c,wie,J),plek(c,doel,J)
    if not pa or not pb or pa=='onderweg' or pb=='onderweg' or wie==doel: continue
    a,b=pa.replace('REG-',''),pb.replace('REG-','');rt=sim.reis(a,b)
    if rt is not None and rt<=1 and (not P or P in (pa,pb)): out.append((wie,doel,pa,pb,sj))
  return out
def rivaliteit(c,P,J):
  """twee personages die hetzelfde willen, en een derde die het heeft (partner, eed of meesterschap van de derde)"""
  W=_wil(c);out=[]
  zelfde=rel(c,'wil_hetzelfde_als',J)
  bezit=collections.defaultdict(set)
  for s_ in ('verbonden_met','eed_aan','meester_van'):
    for a,b,_ in rel(c,s_,J): bezit[b].add(a)
  for a,b,_ in zelfde:
    for derde,hebbers in bezit.items():
      if derde not in(a,b) and W.get(derde)==W.get(a) and (not P or plek(c,a,J)==P): out.append((a,b,derde,W.get(a)));break
  return out
def erfwrok(c,P,J):
  """nazaat van iemand die verraden is, leeft tegelijk met een nazaat van de verrader"""
  kind=collections.defaultdict(list)
  for k,o in c.execute('select code,ouder_code from sim_figuur where ouder_code is not null'): kind[o].append(k)
  out=[]
  for a,b,vj in c.execute("select van_code,naar_code,van_jaar from per_relatie where soort='verraden_door'"):
    for ka in kind[a]:
      for kb in kind[b]:
        if plek(c,ka,J) and plek(c,kb,J) and (not P or plek(c,ka,J)==P): out.append((ka,kb,a,b,vj))
  return out
PAT={'complot':complot,'chantage':chantage,'rivaliteit':rivaliteit,'erfwrok':erfwrok}
def vraag(c,pat,P=None,J=130):
  N=_naam(c);rows=PAT[pat](c,P,int(J))
  return [tuple(N.get(x,x) if isinstance(x,str) else x for x in r)+tuple(x for x in r if isinstance(x,str) and x in N) for r in rows]
if __name__=='__main__':
  import sqlite3;c=sqlite3.connect(os.environ.get('DB','canon.db'))
  for r in vraag(c,*sys.argv[1:]): print(r)
