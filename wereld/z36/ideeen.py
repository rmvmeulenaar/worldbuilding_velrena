# Z36: de ideeënbank door de machine. Heuristisch: fase, positie, genre, volk, schaal en afloop worden uit code, tijdperk, jaar en trefwoorden gelezen, niet met de hand.
# Verbinding = de rij verwijst naar een ERF-rij, een zaadje, of een rij die een ERF-rij of zaadje zelf noemt.
# Afstand telt alleen assen die uit de rij te lezen zijn (onbekend telt als gelijk: streng). Ent-klaar = fase bekend, afstand >= 3 tot elke boog van die fase, en verbonden met levende canon buiten de ideeënbank.
import re,collections
import machine as M
GENRE={'HORROR':'horror','ROMANCE':'romance','ROM':'romance','ACTIE':'actie','OORLOG':'actie','INTR':'intrige','COMEDY':'komedie','THRL':'thriller','SAW':'horror','DEGEN':'tragedie','HELD':'actie',
 'EROS':'romance','KINK':'romance','KINKFUNC':'romance','VOOR':'romance','VERLEID':'romance','SEKS':'romance','BODY':'romance','KLEED':'romance','NERD':'komedie','ONTWAAK':'mysterie','HAAK':'mysterie','TOESTAND':'tragedie','SYS':'intrige','TECH':'mysterie','PLEK':'mysterie','ZINT':None,'LICH':'horror'}
POS=[('vervalser',r'vervals|vervalst|herschrijf|liegt|leugen'),('ontdekker',r'ontdek|ontmask|onthul|komt uit|leest|vindt'),('betaler',r'betaalt|prijs|offer|verliest|sterft'),('profiteur',r'verdien|winst|koopt|verkoopt|markt|rijk worden'),
 ('beslisser',r'beslist|kiest|besluit|beveelt|stemt'),('liefde tussen posities',r'liefde|minnaar|minnares|verliefd|bemint'),('toeschouwer',r'ziet|kijkt|getuige')]
SCH=[('wereld',r'wereld|overal|alle volken'),('rijk',r'rijk\b|oorlog|leger|grens'),('stad',r'Saelith|Ambergaard|Brakhaven|Qesh|stad|markt'),('dorp',r'dorp|clan|boerderij|mijn'),('huis',r'kamer|bed|huis|cel\b')]
AF=[('faalt',r'mislukt|faalt|sterft'),('komt uit',r'komt uit|onthul|ontmask'),('blijft verborgen',r'geheim|verborgen|niemand weet'),('keert om',r'keert|omslag|wending'),('werkt',r'lukt|wint|slaagt')]
def fase_van(tp,jaar):
  if tp:
    m=re.match(r'(\d+)',tp)
    if tp.startswith('801') : return '801 Heden'
    if m and int(m.group(1))<=7: return int(m.group(1))
  if jaar is None: return None
  for grens,f in ((-500,0),(-220,1),(-42,2),(0,3),(130,4),(330,5),(720,6),(800,7)):
    if jaar<=grens: return f
  return '801 Heden'
def zoek(pat,t):
  for w,p in pat:
    if re.search(p,t,re.I): return w
def verwerk(c,run,volken):
  FN={r[1]:r[0] for r in c.execute("select fase,volgorde from fase_rijm")}
  bogen=collections.defaultdict(list)
  for r in c.execute('select g.fase,'+','.join('a.'+k for k in M.ASSEN)+',a.boog_code from boog_as a join boog g on g.code=a.boog_code'): bogen[r[0]].append(dict(zip(M.ASSEN+['code'],r[1:])))
  erf={r[0]:r[1] for r in c.execute("select code,verwijst_naar from canon where code like 'ERF-%' and status in('vastgesteld','voorlopig')")}
  zt={r[0]:' '.join(x or '' for x in r[1:]) for r in c.execute('select code,wat,bron,geplant_in from zaadje')}
  X=set(erf)|set(zt)|{x for v in erf.values() for x in (v or '').split(';') if x}|set(re.findall(r'[A-Z][A-Z0-9]+-[\w-]+',' '.join(zt.values())))|{r[0] for r in c.execute("select naar_code from relatie where van_code like 'ERF-%'")}
  NAMEN={'voortijd':0,'overvloed':1,'vonk':2,'brand':3,'noodtoestand':4,'ontvangst':5,'markt':6,'barsten':7}
  hard={r[0] for r in c.execute("select code from toets_uitzondering where toets='harde_grens'")}
  n=0
  for code,tp,jaar,ft,verw in c.execute("select code,tijdperk,jaar,feit_schoon,verwijst_naar from canon where ideeenbank=1 and status in('vastgesteld','voorlopig') order by id").fetchall():
    t=ft or '';pre=re.match(r'[A-Z]+',code).group(0)
    f=fase_van(tp,jaar)
    if f is None:
      m=re.search(r'\bfase (\d)\b',t,re.I) or re.search(r'\b(Voortijd|Overvloed|Noodtoestand|Ontvangst|Barsten)\b',t)
      if m: f=int(m.group(1)) if m.group(1).isdigit() else NAMEN[m.group(1).lower()]
    fase=f if isinstance(f,str) else FN.get(f)
    p={'positie':zoek(POS,t),'genre':GENRE.get(pre),'volk':next((v for v in volken if v!='mens' and re.search(v.replace('û','[uû]'),t,re.I)),None),'schaal':zoek(SCH,t),'afloop':zoek(AF,t)}
    links=[x for x in (verw or '').split(';') if x in X]
    if code in hard: u,reden,dmin,dicht='uitval: filter harde lijn','bekende bevinding R-harde_grens (toets_uitzondering)',None,None
    elif not fase: u,reden,dmin,dicht='uitval: geen fase','geen tijdperk of jaar',None,None
    else:
      ds=[(sum(1 for k,v in p.items() if v and v!=b[k]),b['code']) for b in bogen.get(fase,[])]
      dmin,dicht=min(ds) if ds else (7,None)
      if dmin<3: u,reden='uitval: afstand',f'afstand {dmin} tot {dicht} op de {sum(1 for v in p.values() if v)} leesbare assen'
      elif not links: u,reden='uitval: verbinding','raakt geen ERF-rij en geen zaadje (ook niet via een rij die zij noemen)'
      else: u,reden='ent-klaar',f'afstand {dmin} tot {dicht}; verbonden met {links[0]}'
    n+=c.execute('insert or ignore into ideeen_verwerking(code,fase,positie,genre,afstand_min,dichtste,verbinding,uitslag,reden,profiel_code) values(?,?,?,?,?,?,?,?,?,?)',(code,fase,p['positie'],p['genre'],dmin,dicht,';'.join(links[:3]) or None,u,reden+f' (run {run}, heuristisch)',None)).rowcount
  return n
