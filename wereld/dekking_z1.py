import re
Z=re.compile(r'\b(geur|ruik|ruikt|stinkt|klinkt|geluid|zoem|ruis|smaak|smaakt|proef|zoet|zout|bitter|koud|kou|warm|heet|ijzig|lauw|licht|gloei|glans|schemer|aanraking|huid|glad|ruw|nat|klam|zacht)\w*',re.I)
H=re.compile(r'(haak|HAAK-|verhaalhaak)',re.I)
def meet(c):
  rows=c.execute("select code,categorie,feit,verwijst_naar,functie from canon where status in ('voorlopig','vastgesteld') and code!='ZINT-DEKKING'").fetchall()
  def hk(r): return bool(H.search(r[2] or '')) or (r[0] or '').startswith('HAAK') or bool(r[4] and any(x in r[4] for x in ['THRL','INTR','ROM','LUST']))
  def zi(r): return len(Z.findall(r[2] or ''))>=2
  def vb(r): return bool((r[3] or '').strip())
  N=len(rows);a=sum(map(hk,rows));b=sum(map(zi,rows));d=sum(map(vb,rows));alle=sum(1 for r in rows if hk(r) and zi(r) and vb(r))
  o=[f'Actieve rijen {N}. Met verhaalhaak {a} ({100*a//N}%), met zintuiglijk detail (2+ zintuigwoorden) {b} ({100*b//N}%), met verbinding {d} ({100*d//N}%), alle drie {alle} ({100*alle//N}%).']
  cat={}
  for r in rows:
    x=cat.setdefault(r[1],[0,0,0]);x[0]+=1;x[1]+=zi(r);x[2]+=hk(r)
  dun=sorted(((k,v) for k,v in cat.items() if v[0]>=15),key=lambda kv:kv[1][1]/kv[1][0])[:8]
  o.append('Dunst zintuiglijk per categorie: '+'; '.join(f'{k} {v[1]}/{v[0]}' for k,v in dun)+'.')
  reg=[]
  for rc in [x[0] for x in c.execute("select code from canon where code like 'REG-%' and code!='REG-overzicht' and status in ('voorlopig','vastgesteld')")]:
    rs=[r for r in rows if rc in (r[3] or '').split(';')]
    if rs: reg.append((rc,len(rs),sum(map(zi,rs)),sum(map(hk,rs))))
  reg.sort(key=lambda x:x[2]/x[1])
  o.append('Per regio (verwijzende rijen, zintuiglijk, haak): '+'; '.join(f'{a} {b}/{z}/{h}' for a,b,z,h in reg)+'.')
  o.append('Nog dun: de categorieën hierboven en regio\'s vooraan in de lijst; volgende stap is per regio 10-20 zintuiglijke bestaande rijen aanvullen en GEB-/PER-rijen een geur- en geluiddetail geven.')
  return ' '.join(o)
