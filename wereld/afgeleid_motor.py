"""Ronde Z33 (canon-motor): afgeleide lagen. Deterministisch; aangeroepen aan het eind van afgeleid.bouw().
- canon.bron / bron_soort / besloten_door / besloten_op  (herkomst, afgeleid uit code/reden/feit; 'onbekend' als niet eenduidig, nooit verzonnen)
- relatie(van_code, soort, naar_code, bron)               (getypeerde relaties: leunt_op, vervangt, sterft_in, geboren_in, woont_in, partner_van, ouder_van/kind_van, broer_zus_van)
- anker_kopie(sleutel, code, waarde_in_rij, afwijkt, draagkracht, risico)  (levende kopieën van ankerwaarden)
Raakt Model-tabellen (regel, boog, personage, zaadje, anker, ...) nooit aan."""
import re,collections
LEV=('vastgesteld','voorlopig')
DATUM=re.compile(r'20\d\d-\d\d-\d\d')
BES=re.compile(r'\b((?:BESLUIT|ORIGIN)-[A-Za-z0-9-]*[A-Za-z0-9])')
HFD=re.compile(r'\(h(\d{1,2})\)|\bh(\d{1,2})\b')
def kolom(c,t,k,typ):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {typ}')
def schema(c):
  for k in ('bron','bron_soort','besloten_door','besloten_op','bron_spoor'): kolom(c,'canon',k,'text')
  c.executescript("""
create table if not exists relatie(van_code text,soort text,naar_code text,bron text,van_jaar integer,tot_jaar integer);
create index if not exists ix_rel_van on relatie(van_code);
create index if not exists ix_rel_naar on relatie(naar_code);
create index if not exists ix_rel_soort on relatie(soort);
create table if not exists anker_kopie(sleutel text,code text,waarde_in_rij text,afwijkt integer,draagkracht text,risico integer);
""")
ROGIER_NOTITIE=re.compile(r"Rogier:\s|Rogier volgt suggestie|[Gg]ekozen door Rogier|[Kk]euze van Rogier|Rogier (?:koos|kiest|besliste|beslist|bevestigt|bevestigde|vraagt|vroeg|wil)\b|op verzoek van Rogier|[Vv]olgens Rogier")
PRIMAIR=('besluit','roman','notitie van Rogier','wereldbijbel','auteur')
def herkomst(c):
  """Z37 (BESLUIT-Z37-C): een bron is een besluit, een romanhoofdstuk, een notitie van Rogier, of een rij waarnaar X ZELF verwijst en die zelf een bron heeft.
  Een rij die naar X verwijst is nooit de bron van X. Rondes 1-22 (oorspronkelijke wereldbijbel): 'auteur (Rogier), ronde N' als de historie die ronde noemt.
  'volgt uit/past bij de besluiten van Rogier' en '(wens Rogier)' (een opdracht om iets te maken, niet de inhoud) tellen niet; 'volgt uit...' is een zin van de agent, geen notitie van Rogier, en telt niet. Geen bron = onbekend; nooit verzonnen."""
  codes={r[0] for r in c.execute('select code from canon')}
  import os
  W=os.path.dirname(os.path.abspath(__file__))
  def opdracht(ronde_naam):
    for n in (f'OPDRACHT_ronde_{ronde_naam}.md',f'OPDRACHT_ronde{ronde_naam}.md'):
      if os.path.exists(os.path.join(W,n)): return n
    return None
  hist=collections.defaultdict(list)
  if c.execute("select 1 from sqlite_master where name='historie'").fetchone():
    for code,no in c.execute('select code,notitie from historie'): hist[code].append(no or '')
  RONDE=re.compile(r'\b[Rr]onde\s+([A-Z]?\d+b?)\b')
  heeft_bh='bron_handmatig' in [r[1] for r in c.execute('pragma table_info(canon)')]
  rijen=c.execute('select id,code,status,reden,feit_schoon,ronde,verwijst_naar,'+('bron_handmatig' if heeft_bh else 'null')+',onderwerp from canon').fetchall()
  res={};TEKST={}
  for i,code,st,reden,feit,ronde,vn,bh,ond in rijen:
    reden=reden or '';feit=feit or '';bron=soort=None;TEKST[code]=(feit,ond or '')
    if bh: bron,soort=bh,('besluit (handmatig aangewezen door Rogier, BESLUIT-Z39-3)' if bh.startswith('BESLUIT') else 'wereldbijbel (handmatig aangewezen door Rogier, '+('BESLUIT-Z38-1' if 'ronde onbekend' in bh else 'BESLUIT-Z39-3')+')')
    if not bron and (code or '').startswith(('BESLUIT-','ORIGIN-')): bron,soort=code,'besluit (eigen rij)'
    if not bron:
      m=[x for x in BES.findall(reden) if x in codes and x!=code]
      if m: bron,soort=m[0],'besluit (in reden)'
    if not bron:
      m=[x for x in BES.findall(feit) if x in codes and x!=code]
      if m: bron,soort=m[0],'besluit (in feit)'
    if not bron:
      m=[x.strip() for x in re.split(r'[;,]',vn or '') if BES.fullmatch(x.strip() or '-') and x.strip() in codes and x.strip()!=code]
      if m: bron,soort=m[0],'besluit (in verwijst_naar)'
    if not bron and re.search(r'Uit de roman \(h\d+\)|roman \(h\d+\)',feit):
      h=re.search(r'\(h(\d+)\)',feit).group(1);bron,soort=f'ROMAN-Z16-h{int(h):02d}','roman (hoofdstuk)'
      if bron not in codes: bron=f'roman h{h}'
    if not bron:
      t=reden+' '+' '.join(hist.get(code,[]))
      m=ROGIER_NOTITIE.search(t)
      if m:
        rn=RONDE.search(t[max(0,m.start()-80):m.end()]) or RONDE.search(t)
        bron,soort=f"notitie van Rogier (ronde {rn.group(1) if rn else ronde})",'notitie van Rogier (in reden/historie: "'+m.group(0).strip()+'")'
    if not bron and ronde is not None and 1<=ronde<=22:
      t=reden+' '+' '.join(hist.get(code,[]))
      naam=str(ronde) if ronde<=18 else 'G'+str(ronde-18)
      rn=next((m for m in RONDE.finditer(t) if m.group(1)==naam),None)
      if rn: bron,soort=f'auteur (Rogier), ronde {rn.group(1)}','wereldbijbel (ronde 1-22; historie noemt ronde '+rn.group(1)+')'
    res[code]=[i,st,reden,feit,ronde,vn,bron,soort,0]
  # tweede gang (regel C1, Z38 B1): X verwijst zelf naar Y en Y heeft een bron. Dat is pas een BRON als Y de bewering zelf bevat:
  # een gedeelde waarde die letterlijk in beide rijen staat (getal van 2+ cijfers buiten de 10 meest voorkomende, of 2+ eigennamen die niet de naam/het onderwerp van Y zijn
  # en niet tot de 120 meest voorkomende woorden met hoofdletter horen). Anders is Y context (kolom context), geen bron.
  CODE_RE=re.compile(r'\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9ûë]+)+\b')
  NUM_RE=re.compile(r'(?<![\w.+])-?\d{2,4}(?![\w+])');NAAM_RE=re.compile(r'\b[A-ZÀ-Ý][a-zà-ÿû]{3,}(?:-[A-Za-zà-ÿû]+)?\b')
  df=collections.Counter();dn=collections.Counter()
  for code,(f,o) in TEKST.items():
    t=CODE_RE.sub(' ',f);df.update(set(NAAM_RE.findall(t)));dn.update(set(NUM_RE.findall(t)))
  ALGN={x for x,_ in dn.most_common(10)}|{'-1240','-600','-150','-40','130','340','720','801'}  # o.a. 801, 100 en de fasegrenzen: te algemeen om een bewering aan te wijzen
  ALG={w for w,_ in df.most_common(120)}|{'Naam','Volk','Regio','Huis','Rol','Fase','Wil','Durft','Verbergt','Haak','Kern','Label','Zintuig','Geur','Geluid','Gevoel','Licht'}
  def waarden(code):
    f,o=TEKST.get(code,('',''));t=CODE_RE.sub(' ',f)
    return {x for x in NUM_RE.findall(t) if x not in ALGN},set(NAAM_RE.findall(t))-ALG
  WD={}
  def gedeeld(x,y):
    for k in (x,y):
      if k not in WD: WD[k]=waarden(k)
    (nx,mx),(ny,my)=WD[x],WD[y]
    eigen=set(re.findall(r'[A-Za-zà-ÿû]{4,}',(y+' '+TEKST.get(y,('',''))[1]).replace('-',' ')))
    eigen={e.lower() for e in eigen}
    n=nx&ny;m={w for w in mx&my if w.lower() not in eigen and not any(w.lower().startswith(e[:5]) for e in eigen if len(e)>=5)}
    return (sorted(n)[:3],sorted(m)[:3]) if (n or len(m)>=2) else None
  laag={}
  for code,r in res.items():
    if r[6]: laag[code]='hard' if r[7].startswith(('besluit','roman','notitie')) else 'bijbel'
  ctx={}
  for diepte in range(1,6):
    nieuw=0
    for code,r in res.items():
      if r[6]: continue
      for y in [x.strip() for x in re.split(r'[;,]',r[5] or '') if x.strip()]:
        ry=res.get(y)
        if ry and ry[6] and y!=code and ry[8]<diepte:
          g=gedeeld(code,y)
          if g:
            r[6],r[7],r[8]=y,f'canonrij met gedeelde waarde (X verwijst zelf naar {y} en beide noemen {", ".join(g[0]+g[1])}; diepte {diepte}; bron daar: {ry[7].split(" (")[0]})',diepte
            laag[code]=laag.get(y,'bijbel');nieuw+=1;break
          ctx.setdefault(code,y)
    if not nieuw: break
  for code,(i,st,reden,feit,ronde,vn,bron,soort,dp) in res.items():
    if not bron and code in ctx: bron,soort='onbekend',f'onbekend; context: {ctx[code]} (C1-keten zonder gedeelde waarde, Z38 B1)'
    if not bron: bron,soort='onbekend',f'onbekend (gegenereerd in ronde {ronde}; geen besluit, hoofdstuk, notitie van Rogier of verwezen rij met bron)'
    if heeft_bh: c.execute('update canon set context=?,herkomst_laag=? where id=?',(ctx.get(code) if bron=='onbekend' else None,laag.get(code) or ('context' if code in ctx else 'onbekend'),i))
    prim=soort.startswith(PRIMAIR)
    if prim and (soort.startswith(('notitie','wereldbijbel')) or st=='vastgesteld'): door='Rogier'
    elif st=='vastgesteld': door='Rogier (status vastgesteld; geen besluit genoemd)'
    elif st=='voorlopig': door=f'voorstel agent (ronde {ronde}), niet besloten'
    else: door='onbekend'
    d=sorted(DATUM.findall(reden+' '+(feit or '')))
    mo=re.match(r'\s*[Rr]onde\s+([A-Z]?\d+b?)\b',reden);sp=opdracht(mo.group(1)) if mo else None
    c.execute('update canon set bron=?,bron_soort=?,besloten_door=?,besloten_op=?,bron_spoor=? where id=?',(bron,soort,door,d[-1] if d else 'onbekend',(sp+(' (besluit van Rogier, vastgelegd in die ronde)' if door=='Rogier' else ' (agent-gegenereerd in die ronde; geen besluit)')) if sp else None,i))
REL=[('partner_van',r'(?:geliefde|minnaar|minnares|partner|echtgeno\w+|vrouw|man) van'),('ouder_van',r'(?:moeder|vader) van'),('kind_van',r'(?:dochter|zoon) van'),('broer_zus_van',r'(?:halfzus|halfbroer|zus|zuster|broer) van')]
def relaties(c):
  c.execute('delete from relatie')
  ins=lambda a,s,b,br,vj=None,tj=None:c.execute('insert into relatie(van_code,soort,naar_code,bron'+(',van_jaar,tot_jaar' if RJ else '')+') values(?,?,?,?'+(',?,?' if RJ else '')+')',(a,s,b,br)+((vj,tj) if RJ else ()))
  RJ='van_jaar' in [r[1] for r in c.execute('pragma table_info(relatie)')]
  for van,naar in c.execute('select distinct v.van_code,v.naar_code from verwijzing v where v.bestaat=1').fetchall(): ins(van,'leunt_op',naar,'verwijzing')
  for code,vd in c.execute("select code,vervangen_door from canon where vervangen_door is not null").fetchall(): ins(vd,'vervangt',code,'vervangen_door')
  # personages: naamindex (volledige naam en unieke voornaam)
  per=c.execute(f"select code,feit_schoon from canon where (status in{LEV} or vervangen_door='personage_profiel:'||code) and code like 'PER%' and feit_schoon like 'Naam: %'").fetchall()  # Z37: ook rijen in personage_profiel
  vol={};voor=collections.defaultdict(set)
  for code,f in per:
    n=re.match(r'Naam: ([^.]+)\.',f).group(1).strip();vol.setdefault(n,code);voor[n.split()[0]].add(code)
  def zoek(t):
    t=t.strip(' .;,')
    if t in vol: return vol[t]
    w=t.split()[0] if t else ''
    return next(iter(voor[w])) if len(voor.get(w,()))==1 else None
  for code,f in per:
    m=re.search(r'Relaties: ([^.]*)',f)
    if m:
      for deel in re.split(r';|, ',m.group(1)):
        for soort,pat in REL:
          mm=re.match(r'\s*'+pat+r' (.+)',deel.strip(),re.I)
          if mm:
            doel=zoek(mm.group(1))
            if doel and doel!=code: ins(code,soort,doel,code+' (Relaties)')
            break
    m=re.search(r'Regio: ([a-z-]+)',f)
    if m and c.execute('select 1 from canon where code=?',('REG-'+m.group(1),)).fetchone(): ins(code,'woont_in','REG-'+m.group(1),code+' (Regio)')
    m=re.search(r'geboren ca\. (-?\d{1,4})\)',f)
    if m: ins(code,'geboren_in','JAAR:'+m.group(1),code)
    m=re.search(r'(?:[Ss]terft|stierf)(?: als mens)? in (-?\d{1,4})\b',f)
    if m: ins(code,'sterft_in','JAAR:'+m.group(1),code)
  for sl,w,bron in c.execute("select sleutel,waarde,bron_code from anker where sleutel like '%_sterfjaar'").fetchall():
    n=c.execute('select bron_code from anker where sleutel=?',(sl[:-10]+'_naam',)).fetchone()
    if n: ins(n[0],'sterft_in','JAAR:'+w,'anker '+sl)
def per_relaties(c):
  """Z39 (11a.4): voorlopige relaties uit de simulatie (rivaal_van, schuldig_aan, eed_aan, verraden_door, meester_van, wil_hetzelfde_als) met van_jaar/tot_jaar."""
  if not c.execute("select 1 from sqlite_master where name='per_relatie'").fetchone(): return
  for a,s_,b,vj,tj,br in c.execute('select van_code,soort,naar_code,van_jaar,tot_jaar,bron from per_relatie').fetchall():
    c.execute('insert into relatie(van_code,soort,naar_code,bron,van_jaar,tot_jaar) values(?,?,?,?,?,?)',(a,s_,b,br,vj,tj))
def anker_kopie(c):
  c.execute('delete from anker_kopie')
  norm=lambda v:re.sub(r'[\s.]','',(v or '').replace('−','-').replace('ca.',''))
  inkom=collections.Counter(r[0] for r in c.execute("select naar_code from relatie where soort='leunt_op'"))
  rows=c.execute(f"select code,feit_schoon,draagkracht,status from canon where status in{LEV} or vervangen_door='personage_profiel:'||code").fetchall()  # Z37: ook personage_profiel
  for sl,w,bron,pat,ber in c.execute('select sleutel,waarde,bron_code,patroon,bereik from anker where patroon is not null').fetchall():
    for code,ft,dk,st in rows:
      if code==bron or (ber and not re.fullmatch(ber.replace('*','.*'),code)): continue
      for p in pat.split(' || '):
        m=re.search(p,ft or '')
        if m:
          v=next(g for g in m.groups() if g);af=int(norm(v)!=norm(w))
          r=3*{'Kern':3,'Structuur':2,'Kleur':1}.get(dk,1)+2*(st=='vastgesteld')+10*af+(bron not in (ft or ''))*2+min(5,inkom[code])
          c.execute('insert into anker_kopie values(?,?,?,?,?,?)',(sl,code,v,af,dk,r));break

# ---- Z36 stap 1a: personage_profiel (ViewModel, afgeleid uit de PER-/PERS-/HOOFDPERS-rijen; nooit met de hand bewerken) ----
# Bron blijft de canonrij (feit). Deze tabel zet de labels in kolommen, zodat de generator (vraag.py bedenk) en het
# personagenetwerk ze kunnen lezen zonder tekst te ontleden. Leeg = NULL ('-', 'onbekend' worden NULL).
PP_KOL={'Naam':'naam','Volk':'volk','Regio':'regio','Huis':'huis','Rol':'rol','Fase':'fase_tekst','Wil':'wil','Durft':'durft','Verbergt':'verbergt',
 'Wat de omgeving weet':'omgeving','Seksuele voorkeur':'voorkeur','Lichaam/vervorming':'lichaam','Relaties':'relaties','Rol in de keten':'keten',
 'Geheim':'geheim','Einde':'einde','Kern':'kern','Verandert':'verandert','Zintuiglijk':'zintuiglijk','Haak':'haak'}
PP_LAB=re.compile(r"(?:^|(?<=[.;:!?)] ))([A-ZÀ-Ý][\wÀ-ÿ'()/-]*(?: [\wÀ-ÿ'()/-]+){0,3}):(?= )")
def _volk(v):
  v=(v or '').strip().lower()
  if not v or v in('-','onbekend'): return None
  if v.startswith('mens'): return 'mens'
  return {'kluwers':'kluwer','karruk':'karrûk','saelmor':'sael-mor','veslethi':'ves-lethi'}.get(v,v.split(' ')[0].strip('.,;'))
def personage_profiel(c):
  c.execute("""create table if not exists personage_profiel(id integer primary key,code text unique,familie text,naam text,volk text,regio text,huis text,rol text,
    fase text,fase_nr integer,jaar integer,geboren integer,leeftijd_band text,wil text,durft text,verbergt text,omgeving text,voorkeur text,lichaam text,relaties text,
    keten text,geheim text,einde text,kern text,verandert text,zintuiglijk text,haak text,archetype integer,bron text)""")
  c.execute('delete from personage_profiel')
  FN={r[0].split(' ',1)[1].lower():r[1] for r in c.execute("select fase,volgorde from fase_rijm")} if c.execute("select 1 from sqlite_master where name='fase_rijm'").fetchone() else {}
  # Z37 (D2): personage_profiel is de bron voor personages. Bronrijen: levende personagerijen, rijen die naar het profiel zijn omgezet
  # (vervangen_door='personage_profiel:'||code) en de archetype-rijen uit de ideeënbank.
  rows=c.execute(f"select code,feit_schoon from canon where categorie='Personage' and ((status in{LEV} and coalesce(ideeenbank,0)=0) or vervangen_door='personage_profiel:'||code or (status in{LEV} and feit_schoon like 'Archetype, geen vaste persoon%'))").fetchall()
  for code,f in rows:
    f=f or '';arch=int(f.startswith('Archetype, geen vaste persoon'))
    ms=list(PP_LAB.finditer(f))
    if len(ms)<2 and not arch: continue
    d={}
    for i,m in enumerate(ms):
      lab=m.group(1);end=ms[i+1].start() if i+1<len(ms) else len(f)
      v=f[m.end():end].strip().rstrip('.').strip()
      k=PP_KOL.get(lab)
      if k and k not in d: d[k]=None if v in('','-','onbekend','—') else v
    fam='archetype' if arch else 'L:'+'|'.join(m.group(1) for m in ms[:8])
    fn=fj=gb=None;ft=d.get('fase_tekst') or ''
    m=re.match(r'(801|[0-7])\b',ft) or re.match(r'(801)',ft)
    if m: fn=int(m.group(1))
    else:
      for naam,nr in FN.items():
        if naam in ft.lower(): fn=nr;break
    m=re.search(r'jaar (-?\d{1,4})',ft);fj=int(m.group(1)) if m else None
    m=re.search(r'geboren ca\. (-?\d{1,4})',ft);gb=int(m.group(1)) if m else None
    lb=None
    if fj is not None and gb is not None:
      a=fj-gb;lb='onder 18' if a<18 else '18-25' if a<=25 else '26-40' if a<=40 else '41-60' if a<=60 else '61+'
    if not d.get('naam') and arch: d['naam']=f.split('.')[1].strip()[:80] if '.' in f else None
    c.execute('insert into personage_profiel(code,familie,naam,volk,regio,huis,rol,fase,fase_nr,jaar,geboren,leeftijd_band,wil,durft,verbergt,omgeving,voorkeur,lichaam,relaties,keten,geheim,einde,kern,verandert,zintuiglijk,haak,archetype,bron) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (code,fam,d.get('naam'),_volk(d.get('volk')),d.get('regio'),d.get('huis'),d.get('rol'),d.get('fase_tekst'),fn,fj,gb,lb,d.get('wil'),d.get('durft'),d.get('verbergt'),d.get('omgeving'),d.get('voorkeur'),d.get('lichaam'),d.get('relaties'),d.get('keten'),d.get('geheim'),d.get('einde'),d.get('kern'),d.get('verandert'),d.get('zintuiglijk'),d.get('haak'),arch,code))
def persoon_identiteit(c):
  """Z41: één persoon = één knoop. Personagecodes met dezelfde codestam (PER-liora-Z6-Z32 / PER-liora-profiel-Z32) of dezelfde naam
  (zonder '(801)'-achtervoegsel) horen bij één persoon. Afgeleid: wordt bij elke bouw opnieuw gemaakt."""
  import re as _re
  c.execute('drop table if exists persoon_identiteit')
  c.execute('create table persoon_identiteit(code text primary key, persoon text, naam text, grond text)')
  if not c.execute("select 1 from sqlite_master where name='personage_profiel'").fetchone(): return
  def stam(code):
    s=code
    for _ in range(4): s=_re.sub(r'-(Z\d+[a-z]?|V\d+|B\d+|D\d+|G\d+|profiel|r\d+)$','',s)
    return s
  rows=c.execute("select code,naam from personage_profiel").fetchall()
  rows+=c.execute("select code,naam from personage where code not in (select code from personage_profiel)").fetchall()
  ouder={}
  def vind(x):
    while ouder.setdefault(x,x)!=x: x=ouder[x]
    return x
  def bind(a,b):
    a,b=vind(a),vind(b)
    if a!=b: ouder[max(a,b)]=min(a,b)
  grond=collections.defaultdict(set);ps=collections.defaultdict(list);pn=collections.defaultdict(list)
  for code,naam in rows:
    vind(code);ps[stam(code)].append(code)
    if naam and naam.strip(): pn[_re.sub(r'\s*\(\d+\)$','',naam.strip())].append(code)
  for d_,g_ in ((ps,'code'),(pn,'naam')):
    for k,cs in d_.items():
      for x in cs[1:]: bind(cs[0],x);grond[x].add(g_);grond[cs[0]].add(g_)
  groep=collections.defaultdict(list)
  for code,naam in rows: groep[vind(code)].append((code,naam))
  for w,leden in groep.items():
    naam=next((n for _,n in leden if n),None)
    persoon=sorted(leden,key=lambda t:(t[1] is None,len(t[0]),t[0]))[0][0]
    for code,_ in leden: c.execute('insert or ignore into persoon_identiteit values(?,?,?,?)',(code,persoon,naam,','.join(sorted(grond[code])) or 'eigen'))
  c.execute('drop view if exists v_persoon')
  c.execute("create view v_persoon as select persoon,max(naam) naam,count(*) codes,group_concat(code,';') leden from persoon_identiteit group by persoon")

def tijdas(c):
  """Z44: één onderliggende tijdas. Afgeleid uit de FASE-rijen ('X tot Y' aan het begin van het feit), de anker-rij TIJD-anker
  (jaren BP van 801) en alle tijdperk-labels in de canon. tijdas: fase, code, naam, van, tot (Zegeljaar), van_bp, tot_bp, voorstel.
  tijdperk_label: elk gebruikt tijdperk-label -> fase (NULL = onbekend; regel R-tijdperk_onbekend meldt dat als signaal)."""
  import re as _re
  for t in ('tijdas','tijdperk_label'): c.execute(f'drop table if exists {t}')
  c.execute('create table tijdas(fase integer primary key, code text, naam text, van integer, tot integer, van_bp integer, tot_bp integer, voorstel integer)')
  c.execute('create table tijdperk_label(label text primary key, fase integer)')
  num=lambda x:int(x.replace('.',''))
  rij=[]
  for code,tp,ond,feit,ib in c.execute("select code,tijdperk,onderwerp,feit,coalesce(ideeenbank,0) from canon where code like 'FASE-%' and code not like 'FASE-OVERZICHT%' and status in ('vastgesteld','voorlopig')"):
    m=_re.match(r'\s*(-?[\d.]+)\s+tot\s+(-?[\d.]+)',feit or '')
    if m: rij.append((num(m.group(1)),num(m.group(2)),code,tp,ond,ib))
  rij.sort()
  a=c.execute("select feit from canon where code='TIJD-anker' and status in ('vastgesteld','voorlopig')").fetchone()
  A=None
  if a:
    m=_re.search(r'(\d{1,3}(?:\.\d{3})+|\d{4,6}) jaar',a[0]); A=num(m.group(1)) if m else None
  bp=lambda j: None if A is None else A-(j-801)
  voor=[r for r in rij if r[1]<=801]; na=[r for r in rij if r[0]>=801]
  F=[(i,)+r for i,r in enumerate(voor)]+[(len(voor),801,802,'HEDEN','801 (nu)','Heden',0)]+[(len(voor)+1+i,)+r for i,r in enumerate(na)]
  namen={}
  for f,van,tot,code,tp,ond,ib in F:
    nm=(tp or ond or code)
    c.execute('insert into tijdas values(?,?,?,?,?,?,?,?)',(f,code,nm,van,tot,bp(van),bp(tot),ib))
    for x in {tp,ond}:
      if x: namen[_re.sub(r'^\d+\s+','',x).split(' (')[0].lower()]=f
  fasen={f for f,*_ in F}
  for (lab,) in c.execute("select distinct tijdperk from canon where tijdperk is not null and trim(tijdperk)<>''").fetchall():
    m=_re.match(r'\s*(\d+)',lab);f=None
    if m:
      k=int(m.group(1));f=len(voor) if k==801 else (k if k in fasen else None)
    if f is None and 'na 801' in lab: f=len(voor)+1 if len(voor)+1 in fasen else None
    if f is None:
      kern=_re.sub(r'^\d+\s+','',lab).split(' (')[0].split(';')[0].strip().lower()
      f=namen.get(kern) or next((v for n,v in namen.items() if n and (n in lab.lower())),None)
    c.execute('insert or replace into tijdperk_label values(?,?)',(lab,f))
  c.execute('drop view if exists v_tijdlijn')
  c.execute("""create view v_tijdlijn as select k.code,k.categorie,k.onderwerp,k.tijdperk,t.fase,t.naam fase_naam,t.van,t.tot,t.van_bp,t.tot_bp,coalesce(k.ideeenbank,0) ideeenbank
    from canon k join tijdperk_label l on l.label=k.tijdperk left join tijdas t on t.fase=l.fase where k.status in ('vastgesteld','voorlopig')""")

def fantasie_tijd(c):
  """Z47: per erotische fantasie (VOOR-, KINK-, RIT-) het verleden, de afhankelijkheden en de status per tijdperk na 801. Afgeleid uit de canon zelf:
  - afhankelijkheid = een link in verwijst_naar naar een LOT-Z44-rij (hoe iets verdwijnt) of naar GEB-Z45-losbandige-jaren (einde van het stalsysteem);
    LOT-Z44-ishvar betekent: alleen gewone mensen nodig.
  - verlies_fase = de fase van het tijdperk van die rij (tijdperk_label); verleden = de vroegste FASE-rij waarnaar de fantasie verwijst.
  - status per fase: echt (voor het verlies), zeldzaam (in het tijdperk van het verlies), daarna 'spel' (macht of instituut weg; rollenspel
    tussen volwassenen) of 'onmogelijk' (een lichaam of volk dat er niet meer is). Rijen met 'niet-seksueel' tellen niet mee."""
  import re as _re
  for t in ('fantasie_kern','fantasie_status'): c.execute(f'drop table if exists {t}')
  c.execute('create table fantasie_kern(code text primary key, naam text, afh text, soort text, verleden_fase integer, verlies_fase integer)')
  c.execute('create table fantasie_status(code text, fase integer, status text, primary key(code,fase))')
  LICHAAM={'skerra','ves-lethi','kluwers','aelthir','dhurn','tharn','orrim','sael-mor','oevrin','myrrhen','vathren','grauwen','reuzenstieren','leegtewormen'}
  BLIJFT={'ishvar','oevrin','myrrhen'}
  lab=dict(c.execute('select label,fase from tijdperk_label').fetchall()); fase_code=dict(c.execute('select code,fase from tijdas').fetchall())
  tp=dict(c.execute("select code,tijdperk from canon where status in ('vastgesteld','voorlopig')").fetchall())
  ORDE=['echt','zeldzaam','spel','onmogelijk']
  for code,ond,feit,verw in c.execute("""select code,onderwerp,feit,coalesce(verwijst_naar,'') from canon where status in ('vastgesteld','voorlopig')
      and (code like 'VOOR-%' or code like 'KINK-%' or code like 'RIT-%') and categorie in ('Voorkeuren','Kinks en situaties','Extreme rituelen','Rituelen')""").fetchall():
    if 'niet-seksueel' in (feit or ''): continue
    refs=[x.strip() for x in verw.split(';') if x.strip()]
    anker=[x for x in refs if x.startswith('LOT-Z44-') or x=='GEB-Z45-losbandige-jaren']
    vf=[fase_code[x] for x in refs if x.startswith('FASE-') and x in fase_code]
    m=_re.search(r'Oorsprong: ([A-Z][\w-]+)',feit or '')
    if not vf and m and lab.get(tp.get(m.group(1))) is not None: vf=[lab[tp[m.group(1)]]]
    if not anker:
      c.execute('insert into fantasie_kern values(?,?,?,?,?,?)',(code,ond,None,None,min(vf) if vf else None,None)); continue
    st={f:'echt' for f in range(9,17)}; soorten=set(); verlies=[]
    for a in anker:
      n='stalsysteem' if a.startswith('GEB-Z45') else a[8:]
      if n in BLIJFT and n!='oevrin': soorten.add('mens'); continue
      fv=lab.get(tp.get(a)); fv=14 if n=='oevrin' else (9 if n=='stalsysteem' else fv)
      if fv is None: continue
      verlies.append(fv); s='lichaam' if n in LICHAAM else 'macht'; soorten.add(s)
      for f in range(9,17):
        k='echt' if f<fv else ('zeldzaam' if f==fv else ('onmogelijk' if s=='lichaam' else 'spel'))
        if ORDE.index(k)>ORDE.index(st[f]): st[f]=k
    c.execute('insert into fantasie_kern values(?,?,?,?,?,?)',(code,ond,';'.join(anker),','.join(sorted(soorten)),min(vf) if vf else None,min(verlies) if verlies else None))
    for f,k in st.items(): c.execute('insert into fantasie_status values(?,?,?)',(code,f,k))
  c.execute('drop view if exists v_fantasie_matrix')
  c.execute("""create view v_fantasie_matrix as select s.fase,t.naam,sum(s.status='echt') echt,sum(s.status='zeldzaam') zeldzaam,sum(s.status='spel') spel,
    sum(s.status='onmogelijk') onmogelijk from fantasie_status s left join tijdas t on t.fase=s.fase group by s.fase""")

def bouw(c):
  schema(c);herkomst(c);personage_profiel(c);relaties(c);per_relaties(c);anker_kopie(c);persoon_identiteit(c);tijdas(c);fantasie_tijd(c)
  import os,sys,importlib.util as iu  # Z37: rijkdom_lid (afgeleid) als de tabel domein bestaat
  pad=os.path.join(os.path.dirname(os.path.abspath(__file__)),'z37','rijkdom.py')
  if os.path.exists(pad):
    sp=iu.spec_from_file_location('rijkdom37',pad);m=iu.module_from_spec(sp);sp.loader.exec_module(m);m.bouw(c)
  c.commit()
