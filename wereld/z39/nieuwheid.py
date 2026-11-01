"""Succescriterium Z39: per premisse max. aandeel gedeelde woord-3-grepen met elke bestaande rij (<20%), en of de set personages (PER-codes) samen met het belang al in een bestaande rij voorkomt."""
import re,sqlite3
def tg(s): w=re.findall(r'\w+',(s or '').lower());return {tuple(w[i:i+3]) for i in range(len(w)-2)}
def meet(c,P,uitsluit_prefix='IDEE-Z39-'):
  rows=[(a,b) for a,b in c.execute("select code,coalesce(feit,'')||' '||coalesce(verwijst_naar,'') from canon") if not a.startswith(uitsluit_prefix)]
  T=[(a,tg(b)) for a,b in rows];naam={a:(b or a).split()[0] for a,b in c.execute('select code,naam from personage_profiel')}
  out=[]
  for code,txt,refs,_,ax,sp in P:
    t=tg(txt);mx,waar=max(((len(t&u)/len(t)),a) for a,u in T if u)
    pers=[x for x in refs.split(';') if x.startswith('PER-')]
    samen=[a for a,b in rows if all((p in b) or (naam.get(p,'#') in b) for p in pers) and ax[2].split()[0] in b.lower()]
    alleen_pers=[a for a,b in rows if all((p in b) or (naam.get(p,'#') in b) for p in pers)]
    out.append({'code':code,'max_overlap':round(mx,3),'met':waar,'personen':pers,'belang':ax[2],'samen_met_belang':samen,'personen_samen':alleen_pers})
  return out
def afstand(P):
  A=[(x[0],(frozenset(p for p in x[2].split(';') if p.startswith('PER-')),)+tuple(x[4])) for x in P]
  m=99;paar=None
  for i in range(len(A)):
    for j in range(i+1,len(A)):
      d=sum(a!=b for a,b in zip(A[i][1],A[j][1]))
      if d<m: m,paar=d,(A[i][0],A[j][0])
  return m,paar
