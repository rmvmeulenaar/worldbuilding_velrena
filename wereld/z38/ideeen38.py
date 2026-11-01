# Z38 B3 (A8): fase invullen voor de ideeën zonder fase, assen uit de tekst halen, opnieuw meten.
# HEURISTISCH, niet met de hand gelezen: jaartallen in de tekst, trefwoorden, de tijdperken van rijen waarnaar het idee verwijst, het profiel.
# Waar niets wijst, blijft de fase leeg met fase_bron 'geen signaal'. De oude fase-kolom wordt alleen gevuld waar hij leeg was; fase_bron zegt waarom.
import re,collections,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','z36'))
import machine as M, ideeen as I
MIN_VERGELEKEN=4;MIN_AFSTAND=3
GRENS=((-601,0),(-151,1),(-41,2),(0,3),(130,4),(340,5),(720,6),(800,7))   # FASE-rijen: 0 tot -600, 1 -600..-150, 2 -150..-40, 3 -40..0, 4 0..130, 5 130..340, 6 340..720, 7 720..801
def fase_jaar(j):
  for g,f in GRENS:
    if j<=g: return f
  return 801
JAAR=re.compile(r'\b(?:jaar|in|sinds|rond|vanaf|tot|ca\.)\s+(-?\d{1,4})\b(?![.,]\d)')
TREF=[(0,r'\b(Makers|de Wieg|Wiegkast|het schip|landing|Muiterij|Reckoner|Ysa Maren)\b','voortijd (Makers, schip, Wieg)'),
      (3,r'\b(Offer der Dochters|Honderd Dochters|Zeven Kronen|Brandvelden)\b','Brand (Offer, Zeven Kronen)'),
      (2,r'\b(vonkkoning\w*|Vonkkoning\w*|eerste vonk)\b','Vonk (vonkkoningen)'),
      (4,r'\b(Deelwet|noodwet van jaar|stichting van het Jongenshof)\b','Noodtoestand (Deelwet)'),
      (6,r'\b(Zaadbeurs|Pest van|Hal-Neth|vervalsersgilde)\b','Markt (Zaadbeurs, Pest)'),
      (801,r'\b(Liora|Teo|Oogstmaan|Morvane-ir|Selvine|Ithrael|lekt|lekkende Zegel|Bloednacht|in 801)\b','801 (personen of toestand van nu)')]
NU=(801,r'\b(gunstbrie\w+|Ontvangster\w*|stalhuis\w*|Moeders?|Orde|gaven-m\w+|wachtrij|Zusters?)\b','801 (hedendaags stelsel: Orde, gunstbrief, stalhuis; geldt van fase 5 tot nu, als heden gelezen)')
MENS=r'\b(Ambergaard|Saelith|Zoutkust|Brakhaven|Hallowyn|Merk|Orvane|Lisk|Isla Mirre|moederhuis|stalhuis|Orde|Moeder)\b'
HP=[('18-25',r'\b(1[89]|2[0-5])\b ?(jaar|jarig)|jonge vrouw|jongeman'),('61+',r'\boude\b|grijze|bejaard'),('41-60',r'middelbare|vijftig'),('26-40',r'dertig')]
def verwerk(c):
  FN={r[1]:r[0] for r in c.execute("select fase,volgorde from fase_rijm")};FN[801]=FN.get(8,'801 Heden');F2N={v:k for k,v in FN.items()}
  def fnaam(f): return '801 Heden' if f==801 else FN.get(f)
  volken=sorted({r[0] for r in c.execute('select volk from personage_profiel where volk is not null')})
  bogen=collections.defaultdict(list)
  for r in c.execute('select g.fase,'+','.join('a.'+k for k in M.ASSEN)+',a.boog_code from boog_as a join boog g on g.code=a.boog_code'): bogen[r[0]].append(dict(zip(M.ASSEN+['code'],r[1:])))
  tp={r[0]:(r[1],r[2]) for r in c.execute('select code,tijdperk,jaar from canon')}
  ppf={r[0]:r[1] for r in c.execute('select code,fase_nr from personage_profiel')}
  n=collections.Counter()
  for code,ft,verw in c.execute("select code,feit_schoon,verwijst_naar from canon where ideeenbank=1 and status in('vastgesteld','voorlopig') order by id").fetchall():
    r=c.execute('select fase,uitslag,verbinding,profiel_code,fase_bron from ideeen_verwerking where code=?',(code,)).fetchone()
    if not r: continue
    fase,oud,links,prof,fb=r;t=ft or ''
    if fase and not (fb or '').startswith('Z38'): fb='Z36: tijdperk of jaar van de rij'
    elif not fase or (fb or '').startswith('Z38'):
      fase=None;fb=None
      js=[int(x) for x in JAAR.findall(t) if -1300<=int(x)<=801]
      if js: f=fase_jaar(js[0]);fb=f'Z38 jaartal in de tekst ({js[0]})'
      else:
        f=next(((ff,lab) for ff,p,lab in TREF if re.search(p,t)),None)
        if f: f,fb=f[0],'Z38 trefwoord: '+f[1]
        else:
          fs=collections.Counter()
          for x in (verw or '').split(';'):
            if x in ppf and ppf[x] is not None: fs[ppf[x]]+=1;continue
            a=tp.get(x)
            if a and (a[0] or a[1] is not None):
              g=I.fase_van(a[0],a[1]);g=801 if g=='801 Heden' else g
              if g is not None: fs[g]+=1
          if fs: f=fs.most_common(1)[0][0];fb='Z38 tijdperk van verwezen rijen ('+', '.join(f'{fnaam(k)}:{v}' for k,v in fs.most_common(3))+')'
          elif prof and c.execute('select fase from verhaal_profiel where code=?',(prof,)).fetchone(): fase=c.execute('select fase from verhaal_profiel where code=?',(prof,)).fetchone()[0];f=None;fb='Z38 fase van het profiel'
          elif re.search(NU[1],t): f,fb=801,'Z38 trefwoord: '+NU[2]
          else: f=None;fb='Z38 geen signaal'
      if f is not None: fase=fnaam(f)
    pre=re.match(r'[A-Z]+',code).group(0)
    p={'positie':I.zoek(I.POS,t),'genre':I.GENRE.get(pre),'volk':next((v for v in volken if v!='mens' and re.search(v.replace('û','[uû]'),t,re.I)),None) or ('mens' if re.search(MENS,t) else None),
       'schaal':I.zoek(I.SCH,t),'afloop':I.zoek(I.AF,t),'vorm':next((v for v in M.VORMEN if v!='nog niet gekozen' and re.search(r'\b'+re.escape(v)+r'\b',t,re.I)),None),'hoofdpersoon':I.zoek(HP,t)}
    bek={k:v for k,v in p.items() if v};vg=len(bek)
    if oud.startswith('uitval: filter'): u,rd,dm=oud,'filter harde lijn gaat vóór alles',None
    elif not fase: u,rd,dm='uitval: geen fase',fb,None
    else:
      bs=bogen.get(fase,[])
      if not bs: u,rd,dm=('ent-klaar' if links else 'uitval: verbinding'),'geen boog in deze fase om mee te vergelijken',None
      elif vg<MIN_VERGELEKEN: u,rd,dm='onbekend: te weinig assen',f'{vg} bekende assen ({",".join(bek) or "-"}); minimaal {MIN_VERGELEKEN}',None
      else:
        def as_(b,k): return (b.get(k) or '').split('|')[0] if k=='hoofdpersoon' else b.get(k)
        ds=[(sum(1 for k,v in bek.items() if as_(b,k) and v!=as_(b,k)),sum(1 for k in bek if as_(b,k)),b['code']) for b in bs]
        ds=[d for d in ds if d[1]>=MIN_VERGELEKEN] or ds
        dm,nv,dicht=min(ds)
        if nv<MIN_VERGELEKEN: u,rd,dm='onbekend: te weinig assen',f'{vg} assen bekend, maar maar {nv} ook bij de bogen bekend',None
        elif dm<MIN_AFSTAND: u,rd='uitval: afstand',f'afstand {dm} op {nv} vergeleken assen tot {dicht}'
        elif not links: u,rd='uitval: verbinding',f'afstand {dm} op {nv} assen tot {dicht}, maar geen ERF-rij of zaadje geraakt'
        else: u,rd='ent-klaar',f'afstand {dm} op {nv} vergeleken assen tot {dicht}; verbonden met {links.split(";")[0]}'
    vf=c.execute('select fase,fase_bron,uitslag_z38,reden_z38,assen_z38 from ideeen_verwerking where code=?',(code,)).fetchone()
    nw=(fase,fb,u,rd+' (Z38, heuristisch)',vg)
    if tuple(vf)!=nw: c.execute('update ideeen_verwerking set fase=?,fase_bron=?,uitslag_z38=?,reden_z38=?,assen_z38=? where code=?',nw+(code,));n['bijgewerkt']+=1
    n[u]+=1;n['bron: '+fb.split(' (')[0].split(':')[0]]+=1
  return n
def rapport(c):
  rows=c.execute("""select coalesce(fase,'(geen fase)'),coalesce(positie,'-'),count(*),sum(uitslag_z37='ent-klaar'),sum(uitslag_z38='ent-klaar'),sum(uitslag_z38='uitval: afstand'),sum(uitslag_z38 like 'onbekend%'),sum(uitslag_z38='uitval: verbinding'),sum(uitslag_z38='uitval: geen fase')
    from ideeen_verwerking group by 1,2 order by 1,2""").fetchall()
  s=['| fase | positie | instroom | ent-klaar Z37 | ent-klaar Z38 | uitval afstand Z38 | onbekend (<4 assen) Z38 | uitval verbinding Z38 | geen fase Z38 |','|---|---|---|---|---|---|---|---|---|']
  tot=[0]*7
  for r in rows:
    s.append('| '+' | '.join(str(x if x is not None else 0) for x in r)+' |');tot=[a+(b or 0) for a,b in zip(tot,r[2:])]
  s.append('| **totaal** | | '+' | '.join(str(x) for x in tot)+' |')
  return '\n'.join(s)
