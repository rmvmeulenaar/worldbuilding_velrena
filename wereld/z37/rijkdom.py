# Z37 D3: rijkdom_lid (afgeleid, heuristisch), gaten per fase, motief_detail-telling.
# Indeling van een rij in volk x fase x domein gaat met code-prefix en trefwoorden, NIET met de hand gelezen (behalve de RIJK-Z37-rijen, die hun cel in de code dragen).
import re,collections
LEV="status in('vastgesteld','voorlopig')"
PREFIX=[(r'^D1-[a-z\-û]+-eten','eten'),(r'^D1-[a-z\-û]+-drank','drinken'),(r'^D1-[a-z\-û]+-muziek','muziek'),(r'^D1-[a-z\-û]+-(humor)','humor'),(r'^D1-[a-z\-û]+-(spel|feest)','feest'),
 (r'^D1-[a-z\-û]+-dood','rouw'),(r'^D1-[a-z\-û]+-ziekte','zorg'),(r'^D1-[a-z\-û]+-taal','taal'),(r'^D1-[a-z\-û]+-geld','handel'),(r'^TAAL-','taal'),(r'^WET-','recht'),(r'^BEST-','recht'),
 (r'^GELOOF-','geloof'),(r'^KLEED-','kleding'),(r'^UIT-VOLK','kleding'),(r'^ESTH-','wonen'),(r'^DAG-','werk'),(r'^VOOR-V4-','handel'),(r'^ECO-','handel'),(r'^TECHNO-','werk')]
WOORD={'eten':r'\beet\b|\beten\b|maaltijd|vlees|brood|vis\b|vruchten','drinken':r'\bdrank|drinken|\bmelk\b|water\b|bier\b','muziek':r'\blied|zing|trom|harp|muziek|ritme',
 'taal':r'\bnaam\b|namen|woord|vloek|taal','recht':r'\bstraf|misdaad|recht\b|vonnis|ruzie','handel':r'betal|munt|zilver|\bkoop|verkoop|handel|ruil','dieren':r'paard|\bvee\b|hond|haai|bloem|boom|plant|wier',
 'kinderen':r'opvoed|\bkind\b|kinderen|leerling|volwassen word','rouw':r'\bdode\b|begraaf|brandstapel|rouw|sterft','feest':r'feest|vier\w*|spel\b|vreugde','werk':r'\bwerk|beroep|ambacht|vissen|zeil',
 'humor':r'lach|grap|humor','kleding':r'\bdraagt\b|tuniek|schort|leer\b|kleding|tatoeage','wonen':r'\btent|hal\b|hallen|slaapt|slapen|woont','zorg':r'ziek|koorts|genees|verzorg|heelster',
 'reizen':r'reis|reizen|varen|vlucht|gast\b','geloof':r'bidden|gebed|geloof|god\b|godin|ritueel'}
def _slug(v): return re.sub(r'[^a-z]','',(v or '').lower().replace('û','u'))
def bouw(c):
  if not c.execute("select 1 from sqlite_master where name='domein'").fetchone(): return 0
  c.execute('delete from rijkdom_lid')
  volken={}
  for v,f in c.execute('select distinct volk,fase_nr from personage_profiel where volk is not null and fase_nr is not null'): volken.setdefault(v,set()).add(f)
  sl={_slug(v):v for v in volken};sl.update({'saelmor':'sael-mor','karruk':'karrûk'})
  FN={r[0].split(' ',1)[1].lower():r[1] for r in c.execute('select fase,volgorde from fase_rijm')}
  def fase(tp,jaar,t):
    if tp:
      if tp.startswith('801'): return 801
      m=re.match(r'(\d)\b',tp)
      if m: return int(m.group(1))
    if re.search(r'\b(in|Heden \()801\b|\b801\)',t or ''): return 801
    if jaar is not None:
      for g,f in ((-500,0),(-220,1),(-42,2),(0,3),(130,4),(330,5),(720,6),(800,7)):
        if jaar<=g: return f
      return 801
    return None
  n=0
  for code,tp,jaar,ft,verw in c.execute(f"select code,tijdperk,jaar,feit_schoon,verwijst_naar from canon where {LEV} and coalesce(ideeenbank,0)=0").fetchall():
    t=ft or ''
    m=re.match(r'^RIJK-Z37-([a-z]+)-([a-z]+)$',code);m38=re.match(r'^RIJK-Z38-mens-[a-z]+-([a-z]+)(?:-\d+)?$',code)
    if m: volk=sl.get(m.group(1));dom=m.group(2);f=801
    elif m38: volk='mens';dom=m38.group(1);f=801  # Z38 C: mens x domein in 801, regio in de code
    else:
      volk=None
      for s in re.findall(r'(?:VOLK|SEKS-VOLK|D1|DAG|GELOOF|WET|BEST|TAAL|KLEED|ESTH|UIT-VOLK|TECHNO-VOLK|VOOR-V4)-([a-zû\-]+?)(?:-|$)',code+'-'):
        if _slug(s) in sl: volk=sl[_slug(s)];break
      if not volk: continue
      dom=next((d for p,d in PREFIX if re.match(p,code)),None)
      if not dom:
        sc={d:len(re.findall(p,t,re.I)) for d,p in WOORD.items()};best=max(sc,key=sc.get)
        if not sc[best]: continue
        dom=best
      f=fase(tp,jaar,t)
    laag='twee lagen' if re.search(r'Officieel|Feitelijk|geheim',t) else ('verandering' if re.search(r'\b(in|sinds) 801\b|nieuw in|sinds de',t,re.I) else None)
    fasen=[f] if f is not None else sorted(volken.get(volk,set()))
    for fn in fasen:
      n+=c.execute('insert or ignore into rijkdom_lid(code,volk,fase_nr,domein_code,laag) values(?,?,?,?,?)',(code,volk,fn,dom,laag or ('fase-eigen' if f is not None else 'tijdloos'))).rowcount
  return n
def gaten(c,fase_nr,top=20):
  """Top-N gaten in een fase: cellen volk x domein met lage rijkdom, gewogen naar het aantal bogen, profielen en personages van dat volk in die fase."""
  fase=c.execute('select fase from fase_rijm where volgorde=?',(8 if fase_nr==801 else fase_nr,)).fetchone()
  fn=fase[0] if fase else None
  nodig=collections.defaultdict(list)
  for code,volk in c.execute('select a.boog_code,a.volk from boog_as a join boog b on b.code=a.boog_code where b.fase=?',(fn,)): nodig[volk].append(code)
  for code,volk in c.execute("select code,volk from verhaal_profiel where fase=? and uitslag in('ent-klaar','voorgesteld')",(fn,)): nodig[volk].append(code)
  pers=collections.Counter(r[0] for r in c.execute('select volk from personage_profiel where fase_nr=? and archetype=0',(fase_nr,)))
  rows=[]
  for volk,dom,naam,dek,diep,verb,vr,bea in c.execute('select volk,domein,naam,dekking,diepte,verbonden,vragen,beantwoord from v_rijkdom where fase_nr=?',(fase_nr,)):
    rijk=dek*max(1,diep)*(1+verb)
    vraag=len(nodig.get(volk,[]))*2+pers.get(volk,0)
    if not vraag: continue
    pct=(bea/vr) if vr else 0
    rows.append((vraag/(1+rijk)*(1.5-pct),volk,naam,dek,diep,verb,f'{bea}/{vr}',vraag,nodig.get(volk,[])[:6],pers.get(volk,0)))
  rows.sort(key=lambda r:-r[0]);return rows[:top]
VERHAAL=[(r'^(YSA|ROMAN|ROMANCE)-','roman Ysa (boek 0)'),(r'^(ZAAD-)?VERHAAL-fase(\d)','VERHAAL-fase{2}'),(r'^(BESLUIT|PER|VOORW)-Z7-','verhaal 1 (Z7)'),(r'^INTR-fase(\d)','VERHAAL-fase{1}'),(r'^RIJK-Z37-','rijkdom Z37 (geen verhaal)')]
def motief(c,MOTIEF):
  out=[]
  for code,det,pat in MOTIEF:
    hits=[r for r in c.execute(f"select code,feit_schoon from canon where {LEV}").fetchall() if re.search(pat,r[1] or '',re.I)]
    hits+=[(z,w) for z,w in c.execute('select code,wat from zaadje') if re.search(pat,w or '',re.I)]
    st=set()
    for cd,_ in hits:
      for p,lab in VERHAAL:
        m=re.match(p,cd)
        if m:
          if 'geen verhaal' not in lab: st.add(lab.format(*([None]+list(m.groups()))))
          break
    out.append((code,det,pat,';'.join(sorted(x for x,_ in hits)[:40]),len(st),'motief (in '+str(len(st))+' verhalen: '+', '.join(sorted(st))+')' if len(st)>=2 else ('detail (1 verhaal: '+', '.join(st)+')' if st else 'detail (geen verhaal)')))
  return out
