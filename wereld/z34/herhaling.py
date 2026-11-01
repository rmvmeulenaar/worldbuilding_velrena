"""Ronde Z34: herhalingsmeting (geen schatting). Gedeeld door meet-script en toets.py.
Sjabloon-signatuur van een rij (feit_schoon):
  - 'L:' + reeks labels als de rij >=2 labels 'Woord(en):' heeft (bijv. Geur:|Geluid:|Haak:) -> label-skelet
  - anders 'O:' + de eerste 4 woorden met getallen vervangen door # -> openingsskelet
Familie = signatuur die in >= FAM_MIN levende rijen voorkomt.
Near-duplicate = Jaccard op woord-3-grepen >= JACC (kandidaten via MinHash-LSH, daarna exact nagerekend)."""
import re,collections,zlib,numpy as np
FAM_MIN=5;JACC=0.5;CAT_DREMPEL=0.35
LAB=re.compile(r"(?:^|(?<=[.;:!?)]) )([A-ZÀ-Ý][\wÀ-ÿ'()/-]*(?: [\wÀ-ÿ'()/-]+){0,3}):(?= )")
def woorden(t): return re.findall(r"[\wÀ-ÿ'-]+",(t or '').lower())
def signatuur(t):
  t=t or '';l=[m.group(1) for m in LAB.finditer(t)]
  l=[re.sub(r'\d+','#',x) for x in l]
  if len(l)>=2: return 'L:'+'|'.join(l[:8])
  w=re.sub(r'\d+','#',' '.join(t.split()[:4]));return 'O:'+w
def families(rows,fam_min=FAM_MIN):
  """rows: [(code,tekst)] -> {sig:[codes]} alleen sig met >=fam_min."""
  d=collections.defaultdict(list)
  for code,t in rows: d[signatuur(t)].append(code)
  return {s:v for s,v in d.items() if len(v)>=fam_min}
def shingles(t,k=3):
  w=woorden(t);return {' '.join(w[i:i+k]) for i in range(max(0,len(w)-k+1))}
def near_dups(rows,jacc=JACC,perm=64,bands=16):
  S=[shingles(t) for _,t in rows];idx=[i for i,s in enumerate(S) if len(s)>=5]
  rng=np.random.default_rng(34);P=(1<<61)-1;a=rng.integers(1,P,perm,dtype=np.uint64);b=rng.integers(0,P,perm,dtype=np.uint64)
  M={}
  for i in idx:
    h=np.array([zlib.crc32(x.encode()) for x in S[i]],dtype=np.uint64)
    M[i]=((h[:,None]*a+b)%np.uint64(4294967311)).min(0)
  r=perm//bands;kand=set()
  for bd in range(bands):
    bk=collections.defaultdict(list)
    for i in idx: bk[M[i][bd*r:(bd+1)*r].tobytes()].append(i)
    for v in bk.values():
      if 1<len(v)<400:
        for x in range(len(v)):
          for y in range(x+1,len(v)): kand.add((v[x],v[y]))
  out=[]
  for i,j in kand:
    A,B=S[i],S[j];jj=len(A&B)/len(A|B)
    if jj>=jacc: out.append((rows[i][0],rows[j][0],round(jj,3)))
  return out
def zinnen(t): return [z.strip() for z in re.split(r'(?<=[.!?])\s+',t or '') if len(z.split())>=5]
