#!/usr/bin/env python3
"""Ronde Z33: wereldtests, gestuurd door de tabel `regel` (canon-motor principe 6).
Elke regel: sql_test = een SELECT die (code, detail) teruggeeft voor elke overtreding, of 'py:<naam>' voor een controle in dit script.
niveau 'fout' laat de ronde falen (exit 1) als een bevinding NIEUW is (niet in toets_uitzondering); niveau 'signaal' wordt alleen gemeld.
Zonder tabel `regel` (oude db) draaien de ingebouwde Z31-controles.
Gebruik: python3 toets.py [db] [--rapport pad.md] [--json pad.json] [--alles]"""
import sqlite3,re,sys,os,difflib,collections
A=[x for i,x in enumerate(sys.argv[1:],1) if not x.startswith('--') and sys.argv[i-1] not in('--rapport','--json')]
DB=A[0] if A else os.environ.get('DB',os.path.join(os.path.dirname(os.path.abspath(__file__)),'canon.db'))
RAP=sys.argv[sys.argv.index('--rapport')+1] if '--rapport' in sys.argv else None
c=sqlite3.connect(DB);q=lambda s,*a:c.execute(s,a).fetchall()
LEVEND="status in('vastgesteld','voorlopig')"
LEVEND_P="(status in('vastgesteld','voorlopig') or vervangen_door='personage_profiel:'||code)"  # Z37 (D2): levend of opgenomen in personage_profiel
norm=lambda v:re.sub(r'[\s.]','',(v or '').replace('−','-').replace('ca.',''))
# ---------- py-controles (elk geeft lijst (code, detail)) ----------
def py_harde_grens():
  LBL=re.compile(r"(?:Veiligheids)?[Ll]abel: [^.]*\.")
  MIN=re.compile(r"\b(kind|kinderen|kindje|meisje|meisjes|minderjarig\w*|tiener\w*|puber\w*|(?:1[0-7]|[1-9]) jaar oud|\((?:1[0-7]|[1-9])\))",re.I)
  DIER=re.compile(r"\b(dier|dieren|hond|honden|geit|geiten|paard|paarden|beest|beesten)\b",re.I)
  SEX=re.compile(r"\b(seks|seksueel|seksuele|erotisch\w*|erotiek|geslachtsdaad|neuk\w*|gemeenschap|naakt|klaarkom\w*|orgasme\w*|penetr\w*|kink|kinks|bedpartner|minnaar|minnares|verkracht\w*)\b",re.I)
  NEG=re.compile(r"(geen|niet|nooit|zonder|niet-seksueel|non-seksueel)\W+(\w+\W+){0,6}?(seks|seksuele|erot|rol|minderjarig|dier|kind)",re.I)
  out=[]
  for code,ft in q(f"select code,feit_schoon from canon where {LEVEND_P}"):
    for z in re.split(r'(?<=[.;!?])\s+',LBL.sub('',ft or '')):
      if SEX.search(z) and (MIN.search(z) or DIER.search(z)) and not NEG.search(z): out.append((code,z.strip()))
  # ook de nieuwe Model-tabellen met vrije tekst
  for t,cols in (('boog','voorstel'),('personage','eigen_fout||\' \'||coalesce(voorstel,\'\')')):
    if t in TABS:
      for code,ft in q(f"select code,{cols} from {t}"):
        for z in re.split(r'(?<=[.;!?])\s+',ft or ''):
          if SEX.search(z) and (MIN.search(z) or DIER.search(z)) and not NEG.search(z): out.append((code,z.strip()))
  return out
def py_anker():
  out=[]
  for sl,w,bron,pat,ber in q('select sleutel,waarde,bron_code,patroon,bereik from anker where patroon is not null'):
    for code,ft in q(f"select code,feit_schoon from canon where {LEVEND_P}"+(" and code glob ?" if ber else ""),*([ber] if ber else [])):
      for p in pat.split(' || '):
        for m in re.finditer(p,ft or ''):
          v=next(g for g in m.groups() if g)
          if norm(v)!=norm(w): out.append((code,f'{sl}: rij zegt {v}, anker {w} ({bron})'))
  return out
def py_leeftijd():
  out=[];geb={sl[:-len('_geboren')]:int(norm(w)) for sl,w in q("select sleutel,waarde from anker where sleutel like '%_geboren'")}
  per=collections.defaultdict(list)
  for code,ft in q(f"select code,feit_schoon from canon where {LEVEND} and code like 'TOESTAND-%'"):
    m=re.search(r'Jaar (-?\d+)[^,]*, leeftijd (\d+)',ft or '')
    if m: per[re.sub(r'^TOESTAND-Z\d+-(PER-v4-)?|-\d+$','',code)].append((code,int(m.group(1))-int(m.group(2))))
  for p,l in per.items():
    bj=[x for _,x in l]
    if max(bj)-min(bj)>1: out.append((p,f'geboortejaar volgens TOESTAND-rijen loopt uiteen: {sorted(set(bj))}'))
    for k,g in geb.items():
      nm_=q("select waarde from anker where sleutel=?",k+'_naam'); slug=nm_[0][0].lower().replace(' ','-') if nm_ else k
      if p.endswith(slug):
        for code,x in l:
          if abs(x-g)>1: out.append((code,f'geboren {x} volgens jaar-leeftijd, anker {g}'))
  # Z33: PER-rijen 'jaar J (geboren ca. G)' + 'N jaar' / '(N)' tegen geboorte-anker van dezelfde persoon
  for k,g in geb.items():
    nm_=q("select waarde,bron_code from anker where sleutel=?",k+'_naam')
    if not nm_: continue
    for code,gb in q("select code,geboren from personage_profiel where naam like ? and geboren is not null",nm_[0][0]+'%'):  # Z37: leest personage_profiel
      if abs(gb-g)>1: out.append((code,f'{nm_[0][0]}: geboren {gb}, anker {g}'))
  return out
NADOOD0=re.compile(r"\b(stem|Wortel|Rekenaar|Reckoner|Sterrensteen|kluis|herinner\w*|graf|as|lied\w*|liederen|naam|namen|godin|dood|stierf|sterft|gestorven|legende|beeld|tempel|dagboek|log\w*|plaat|brief|geest|echo|vereerd|aanbeden|annalen|Wieg|kern|stempatroon|bekennen|Orrim|Dochter\w*|sporen|Voortijd|Fase 0|-1240)\b",re.I)
NADOOD=re.compile(r"\b(stem|Wortel|Rekenaar|Reckoner|Sterrensteen|kluis|herinner\w*|graf|as|lied\w*|liederen|naam|namen|godin|dood|stierf|sterft|gestorven|legende|beeld|tempel|dagboek|log\w*|plaat|brief|geest|echo|vereerd|aanbeden|annalen|Wieg|kern|stempatroon|bekennen|Orrim|Dochter\w*|sporen|Voortijd|Fase 0|-1240|patroon|vernoemd|vernoem\w*|erfnaam|nagedachtenis|relikwie\w*|herdenk\w*|verhalen|verteld|overlevering|kronie\w*|register\w*|archief|portret|ooit|vroeger|grootmoeder|overgrootmoeder|voorouder\w*|stichtster|stichter|eerste)\b",re.I)
def py_na_dood():
  out=[];gezien=set()
  dood=[(sl[:-len('_sterfjaar')],int(norm(w))) for sl,w in q("select sleutel,waarde from anker where sleutel like '%_sterfjaar'")]
  lijst=[]
  for k,sj in dood:
    n=q("select waarde from anker where sleutel=?",k+'_naam')
    if n: lijst.append((n[0][0],sj,NADOOD0))
  if 'relatie' in TABS:  # Z33: sterfjaren uit PER-rijen (relatie sterft_in), alleen volledige namen
    for van,naar in q("select van_code,naar_code from relatie where soort='sterft_in' and van_code like 'PER%'"):
      f=q('select naam from personage_profiel where code=?',van)  # Z37: naam uit personage_profiel
      nm=re.match(r'([^.(]+)',f[0][0] or '') if f and f[0][0] else None
      if nm and len(nm.group(1).split())>=2: lijst.append((nm.group(1).strip(),int(naar.split(':')[1]),NADOOD))
  for naam,sj,ND in {(a,b):(a,b,x) for a,b,x in reversed(lijst)}.values():
    for code,jaar,ft in q(f"select code,jaar,feit_schoon from canon where {LEVEND_P} and feit_schoon like ?",f'%{naam}%'):
      m=re.match(r'Jaar (-?\d+)',ft or '');j=jaar if jaar is not None else (int(m.group(1)) if m else None)
      if j is not None and j>sj and not ND.search(ft) and (code,naam) not in gezien: gezien.add((code,naam));out.append((code,f'{naam} (sterft {sj}) genoemd in jaar {j}'))
  return out
def py_naam():
  out=[];nm=collections.defaultdict(set)
  for code,naam in q("select code,naam from personage_profiel where code like 'PER-%' and naam is not null and archetype=0"):  # Z37: leest personage_profiel
    nm[naam.strip()].add(code)
  for naam,code in q("select waarde,bron_code from anker where sleutel like 'boek0_naam_%'"): nm[naam].add(code)
  TITEL={'Koning','Koningin','Moeder','Hoge','Zuster','Kapitein','Vrouwe','Veldvrouwe','Krijgsheer','Hoedster','Raadsvrouw','Registratrix','Hofmeesteres','Oude','Oudste','Heer','Vader','Meester','Broeder','Prinses','Prins','Generaal','Werkster'}
  voor=lambda n:([x for x in n.split() if x not in TITEL] or [n])[0]
  gem={(a,b) for a,b in q('select naam_a,naam_b from naam_markering')};gem|={(b,a) for a,b in gem}
  namen=sorted(nm)
  for i,a in enumerate(namen):
    for b in namen[i+1:]:
      va,vb=voor(a),voor(b)
      if len(va)<4 or len(vb)<4 or nm[a]&nm[b]: continue
      if (va==vb or (va[:3]==vb[:3] and difflib.SequenceMatcher(None,va,vb).ratio()>=0.72)) and (a,b) not in gem and (va,vb) not in gem: out.append((';'.join(sorted(nm[a]|nm[b])),f'{a} ~ {b}'))
  return out
def py_fase_nummer():
  F={int(sl.split('_')[1]):w for sl,w in q("select sleutel,waarde from anker where sleutel glob 'fase_[0-9]_naam'")}
  if not F: return []
  out=[];inv={v.lower():k for k,v in F.items()}
  for code,ft in q(f"select code,feit_schoon from canon where {LEVEND_P}"):
    for m in re.finditer(r'\b[Ff]ase:? ([0-7]) ([A-Z][a-zë]+)',ft or ''):
      n,naam=int(m.group(1)),m.group(2)
      if naam.lower() in inv and inv[naam.lower()]!=n: out.append((code,f'fase {n} {naam}: anker zegt {naam} = fase {inv[naam.lower()]} ({F[n]} = fase {n})'))
  return out
def _profiel(r): return (r['geslacht_hoofdpersoon'],'21-35' if (r['leeftijd_hoofdpersoon'] or 0) in range(21,36) else ('?' if r['leeftijd_hoofdpersoon'] is None else 'anders'),r['romance'],r['erotische_sleutelscene'],(r['terugkerend_motief'] or '').split('/')[0])
def _bogen():
  cols=[x[1] for x in c.execute('pragma table_info(boog)')];return [dict(zip(cols,x)) for x in q('select * from boog order by id')]
def py_mal_aangrenzend():
  b=_bogen();out=[]
  for x,y in zip(b,b[1:]):
    if 'onbekend' in _profiel(x) or None in _profiel(x): continue
    if _profiel(x)==_profiel(y): out.append((y['code'],f"zelfde profiel als vorige boog {x['code']}: {_profiel(y)}"))
  return out
MOTIEF_MAX=4
def py_motief_max():
  b=_bogen();tel=collections.defaultdict(list)
  for r in b:
    m=(r['terugkerend_motief'] or '').split('/')[0].strip()
    if m and m not in('geen','onbekend'): tel[m].append(r['code'])
  return [(f'MOTIEF:{m}',f'motief "{m}" in {len(l)} bogen (max {MOTIEF_MAX}): '+', '.join(l)) for m,l in tel.items() if len(l)>MOTIEF_MAX]
# ---------- Z34: geen sjablonen (HANDL-Z34-1, BESLUIT-Z34-1). Drempels in z34/herhaling.py (FAM_MIN, JACC, CAT_DREMPEL). ----------
NIEUW_VANAF=63  # ronde-nummer van Z34; rijen vanaf hier mogen geen sjabloon vormen
def _herh():
  sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'z34'));import herhaling;return herhaling
def py_sjabloon_nieuw():
  h=_herh();R=q(f"select code,feit_schoon,coalesce(ronde,0) from canon where {LEVEND}")
  nw=[(a,b) for a,b,r in R if r>=NIEUW_VANAF];out=[]
  for sig,v in h.families(nw,3).items(): out+=[(x,f'nieuwe rijen delen sjabloon {sig[:60]} ({len(v)}x)') for x in v]
  nc={a for a,_ in nw}
  for a,b,j in h.near_dups([(a,b) for a,b,_ in R]):
    if a in nc or b in nc: out.append((a if a in nc else b,f'bijna-kopie (Jaccard {j}) van {b if a in nc else a}'))
  return out
def py_herhaling_categorie():
  h=_herh();R=q(f"select code,categorie,feit_schoon from canon where {LEVEND} and coalesce(ideeenbank,0)=0")
  F=h.families([(a,c_) for a,_,c_ in R]);inF={x for v in F.values() for x in v};tel=collections.Counter(b for _,b,_ in R);fam=collections.Counter(b for a,b,_ in R if a in inF)
  return [(f'CAT:{k}',f'{fam[k]}/{n} rijen ({fam[k]/n:.0%}) in een sjabloonfamilie (drempel {h.CAT_DREMPEL:.0%})') for k,n in tel.items() if n>=10 and fam[k]/n>h.CAT_DREMPEL]
def py_boog_uniek():
  out=[]
  if 'verteller' not in [r[1] for r in c.execute('pragma table_info(boog)')]: return out
  for kol in ('vorm','verteller','toon','afloop','tempo'):
    d=collections.defaultdict(list)
    for code,v in q(f'select code,{kol} from boog'):
      if v and v not in('onbekend','-'): d[v.strip().lower()].append(code)
    out+=[(l[1],f'{kol} gelijk aan {l[0]}: {v[:60]}') for v,l in d.items() if len(l)>1]
  return out
def py_personage_fout_uniek():
  d=collections.defaultdict(list)
  for code,s in q("select code,soort_fout from personage where soort_fout is not null and soort_fout!='-'"): d[s.split(' (')[0].strip().lower()].append(code)
  return [(l[1],f'soort_fout "{k}" ook bij {l[0]}') for k,l in d.items() if len(l)>1]
# ---------- Z35: rijmregel (fase_rijm, boog-assen). Assen: beslisser, betaler, vervalst, ontdekt, schaal. NULL telt niet als verschil. ----------
RIJM_ASSEN=('beslisser_as','betaler_as','vervalst_as','ontdekt_as','schaal')
_n=lambda v:re.sub(r'\s+',' ',(v or '').strip().lower())
def _verschil(a,b): return sum(1 for k in RIJM_ASSEN if a.get(k) and b.get(k) and _n(a[k])!=_n(b[k]))
def _rijm():
  if 'fase_rijm' not in TABS: return []
  cols=[x[1] for x in c.execute('pragma table_info(fase_rijm)')];return [dict(zip(cols,x)) for x in q('select * from fase_rijm order by volgorde')]
def py_rijm_assen():
  R=_rijm();return [(y['fase'],f"verschilt van {x['fase']} op {_verschil(x,y)} van 5 assen (min 3)") for x,y in zip(R,R[1:]) if _verschil(x,y)<3]
def py_rijm_erfenis():
  R=_rijm();out=[];vg={}
  for r in R:
    naam=(r['fase'].split(' ',1)+[''])[1].lower();vg['ERF-'+naam]=r['volgorde']
  lev={x for (x,) in q(f"select code from canon where {LEVEND} and code like 'ERF-%'")}
  for r in R:
    if r['volgorde']<1: continue
    ok=[e for e in re.split(r'[;,]\s*',r['erft_van'] or '') if e in lev and vg.get(e,99)<r['volgorde']]
    if not ok: out.append((r['fase'],f"erft_van '{r['erft_van'] or ''}': geen levende ERF-rij uit een eerdere fase"))
  return out
def py_rijm_spiraal():
  R=_rijm();out=[];eerder=[]
  for r in R:
    b=_n(r['blijvende_verandering'])
    if not b: out.append((r['fase'],'blijvende_verandering is leeg'));continue
    w=set(re.findall(r'\w+',b))
    for f,e in eerder:
      if b==e or len(w&set(re.findall(r'\w+',e)))/max(1,len(w|set(re.findall(r'\w+',e))))>=0.6: out.append((r['fase'],f'blijvende_verandering komt terug uit {f}'))
    eerder.append((r['fase'],b))
  return out
def py_rijm_binnen_fase():
  if 'beslisser_as' not in [x[1] for x in c.execute('pragma table_info(boog)')]: return []
  b=_bogen();out=[];d=collections.defaultdict(list)
  for r in b: d[r['fase']].append(r)
  for f,l in d.items():
    for i,x in enumerate(l):
      for y in l[i+1:]:
        if _verschil(x,y)<2: out.append((y['code'],f"verschilt van {x['code']} op {_verschil(x,y)} rijm-assen (min 2)"))
  return out
VA=['positie','genre','schaal','volk','vorm','afloop','hoofdpersoon']
def _vp():
  if 'verhaal_profiel' not in TABS: return [],[]
  b=[dict(zip(['code','fase']+VA,r)) for r in q("select a.boog_code,g.fase,"+','.join('a.'+k for k in VA)+" from boog_as a join boog g on g.code=a.boog_code")]
  p=[dict(zip(['code','fase']+VA,r)) for r in q("select code,fase,"+','.join(VA)+" from verhaal_profiel where uitslag in('ent-klaar','voorgesteld') order by id")]
  return b,p
def py_verhaal_afstand():
  b,p=_vp();out=[]
  for i,x in enumerate(p):
    for y in [z for z in b if z['fase']==x['fase']]+[z for z in p[:i] if z['fase']==x['fase']]:
      d=sum(1 for k in VA if x[k]!=y[k])
      if d<3: out.append((x['code'],f"afstand {d} tot {y['code']} (min 3)"))
  return out
def py_profiel_harde_lijn():
  if 'verhaal_profiel' not in TABS: return []
  out=[]
  for code,lft,partner,inst,dl,ero,wr in q("select code,leeftijd,partner,instemming,dwang_label,g_erotiek,wereldregel_code from verhaal_profiel"):
    if (lft or 0)<18: out.append((code,'hoofdpersoon jonger dan 18 of zonder leeftijd'))
    if (ero or 0)>0 and partner and ('dier' in partner or 'minderjarig' in partner): out.append((code,'dier of minderjarige in een seksuele rol'))
    if (ero or 0)>0 and inst=='niet mogelijk': out.append((code,'seks met wie niet kan instemmen'))
    if inst=='dwang' and not dl: out.append((code,'dwang zonder label donker thema'))
    if (ero or 0)>0 and not wr: out.append((code,'erotiek zonder wereldregel'))
  return out
def py_positie_dekking():
  if 'verhaal_profiel' not in TABS: return []
  rs=q("select fase,positie,in_canon+in_ideeenbank from v_positie_dekking");d=collections.defaultdict(dict)
  for f,p,n in rs: d[f][p]=n
  out=[]
  for f,m in d.items():
    leeg=[p for p,n in m.items() if not n]
    if leeg: out.append((f,'lege posities: '+', '.join(leeg)+('; terwijl '+', '.join(p for p,n in m.items() if n>=3)+' al 3 keer of vaker' if any(n>=3 for n in m.values()) else '')))
  return out
def py_premisse_vorm():
  """Z38 B2 (BESLUIT-Z38-12): een premisse is met de hand geschreven, geen invulzin. Fout bij (a) >50% van de woord-3-grepen gedeeld
  met een andere premisse, (b) een fasenaam of ERF-label letterlijk als obstakel, (c) de invulmarkers van de oude sjabloonzinnen."""
  if 'vervangen_door' not in [r[1] for r in q('pragma table_info(verhaal_profiel)')]: return []
  P=[(c_,p_) for c_,p_ in q("select code,premisse from verhaal_profiel where premisse is not null and premisse not like 'geen premisse%' and coalesce(vervangen_door,'')=''")]
  out=[];G={}
  for c_,p_ in P:
    w=re.findall(r"[a-zà-ÿû']+",re.sub(r'\[[^\]]*\]','',p_).lower());G[c_]={tuple(w[i:i+3]) for i in range(len(w)-2)}
  for a,_ in P:
    for b,_ in P:
      if a<b and G[a] and G[b]:
        k=len(G[a]&G[b])
        if k/len(G[a])>0.5 or k/len(G[b])>0.5: out.append((a,f'deelt {k} woord-3-grepen met {b}'))
  FASEN=[r[0].split(' ',1)[1] for r in q('select fase from fase_rijm') if ' ' in r[0]]
  LBL=[x.strip().lower() for (f,) in q("select feit_schoon from canon where code like 'ERF-%' and status in('vastgesteld','voorlopig')") for x in re.split(r'[;:,]',re.sub(r'\([^)]*\)','',f or '')) if len(x.strip())>=15]
  for c_,p_ in P:
    t=p_.lower()
    for l in LBL:
      if l.rstrip('.') in t: out.append((c_,f'ERF-label letterlijk: "{l[:50]}"'))
    for f in FASEN:
      if re.search(r'\b\d+ '+f+r'\b|\b'+f+r'\b[^.;]{0,40}(staat in de weg|houdt [^.]{0,30}tegen)',p_): out.append((c_,f'fasenaam als obstakel: {f}'))
    if re.search(r'staat in de weg|In de weg:|houdt dat tegen|zet door, tegen de prijs|\(wat nu verborgen blijft\)',p_): out.append((c_,'invulmarker van het oude sjabloon'))
  return out
def py_fee_afspraak():
  """Z38 A9 (BESLUIT-Z38-9, uitwerking BESLUIT-Z30-4): een feeënafspraak gaat nooit over seks. Fout als een levende FEE-rij of een rij die een
  feeënafspraak beschrijft een seksueel woord bevat dat niet ontkend wordt."""
  SEX=re.compile(r"\b(seks\w*|erotisch\w*|erotiek|geslachtsdaad|neuk\w*|naakt|klaarkom\w*|orgasme\w*|bedpartner|minnaar|minnares|ontvangst|ontvangen|zaad|zaadje|lust|wellust|verleid\w*|nacht met)\b",re.I)
  NEG=re.compile(r"(nooit|geen|niet|zonder)\W+(\w+\W+){0,5}?$",re.I)
  out=[]
  for code,f in q("select code,feit_schoon from canon where status in('vastgesteld','voorlopig') and code not like 'BESLUIT-%' and code not like 'REGEL-feeenafspraak%' and (code like 'FEE-%' or lower(feit_schoon) like '%feeënafspraak%' or lower(feit_schoon) like '%feeafspraak%' or lower(feit_schoon) like '%afspraak met een fee%' or lower(feit_schoon) like '%afspraak met de fee%')"):
    f=f or ''
    for zin in re.split(r'(?<=[.!?;])\s+',f):
      if not re.search(r'afspraak|belo\w+|ja bindt|gelofte',zin,re.I) and not code.startswith('FEE-'): continue
      for m in SEX.finditer(zin):
        if not NEG.search(zin[:m.start()]): out.append((code,f'seksueel woord in feeënafspraak: "{m.group(0)}"'));break
  return out
TABS={r[0] for r in q("select name from sqlite_master where type='table'")}
OUD=[('kern_vastgesteld',"select code,'Kern maar status '||status from canon where draagkracht='Kern' and status!='vastgesteld'",'fout'),
('handmatig_waarde',"select code,'ongeldige draagkracht_handmatig '||draagkracht_handmatig from canon where draagkracht_handmatig is not null and draagkracht_handmatig not in('Kern','Structuur','Kleur')",'fout'),
('handmatig_kern',"select code,'draagkracht_handmatig=Kern op een rij met status '||status||' (telt niet als Kern)' from canon where draagkracht_handmatig='Kern' and status!='vastgesteld'",'fout'),
('vervangen_door',"select code,case when vervangen_door is null then 'voorlopig, vervangen zonder vervangen_door' else 'vervangen_door '||vervangen_door||' bestaat niet' end from canon where status='voorlopig, vervangen' and (vervangen_door is null or vervangen_door not in(select code from canon))",'fout'),
('dode_link',"select van_code,van_tabel||': '||naar_code from verwijzing where bestaat=0",'fout'),
('harde_grens','py:harde_grens','fout'),('anker','py:anker','fout'),('leeftijd','py:leeftijd','fout'),('na_dood','py:na_dood','fout'),('naam','py:naam','fout')]
# ---------- Z39: simulatie ----------
def py_sim_harde_lijn():
  """Harde lijnen in de simulatie: geen type met harde-lijnrisico; verbintenis/romantiek alleen tussen volwassenen; minderjarigen alleen in geboorte/opvoeding/erfenis/dood."""
  if 'gebeurtenis_type' not in TABS: return []
  out=[(t,'gebeurtenistype met harde-lijnrisico') for (t,) in q("select code from gebeurtenis_type where coalesce(harde_lijn_risico,0)!=0")]
  geb={a:b for a,b in q("select code,geboren from personage_profiel where geboren is not null")}
  geb.update({a:b for a,b in q("select code,geboren from sim_figuur")})
  for rid,j,typ,a,d in q("select run_id,jaar,type_code,actor,doel from sim_gebeurtenis where module='personen'"):
    if typ in('geboorte','opvoeding','erfenis','dood','raadstemming','wet'): continue
    for x in (a,d):
      if x in geb and j-geb[x]<18: out.append((f'{rid}:{typ}:{x}',f'minderjarige ({j-geb[x]}) in {typ}'))
  return out
def py_epistemiek():
  """Aanscherping Z39 (2): elke rij in de simulatietabellen heeft epistemiek; simulatierijen noemen run-id en seed."""
  out=[]
  for t in ('verblijf','kennis','per_relatie','sim_figuur','sim_regel','gebeurtenis_type','tech_gebeurtenistype','sim_run','sim_gebeurtenis','steekproef'):
    if t not in TABS: continue
    for (i,e) in q(f"select id,epistemiek from {t}"):
      if not e: out.append((f'{t}:{i}','geen epistemiek'))
      elif e.startswith('simulatie') and not ('seed' in e and re.search(r'Z\d+-',e)): out.append((f'{t}:{i}','simulatie zonder run-id/seed'))
  out+=[(c_,'Z39-rij zonder epistemiek') for (c_,) in q("select code from canon where ronde>=68 and coalesce(epistemiek,'')=''")] if 'epistemiek' in [r[1] for r in c.execute('pragma table_info(canon)')] else []
  return out

def py_simulatie_in_canon():
  """Z40 (BESLUIT-Z40-2): een levende canonrij met epistemiek 'simulatie' staat in de ideeënbank, tenzij een BESLUIT haar via draagkracht_handmatig in de canon zette."""
  if 'epistemiek' not in [r[1] for r in c.execute('pragma table_info(canon)')]: return []
  return [(code,'simulatie-epistemiek maar ideeenbank=0 zonder besluit') for code,hand,idee in c.execute("select code,draagkracht_handmatig,coalesce(ideeenbank,0) from canon where status in('vastgesteld','voorlopig') and epistemiek like 'simulatie%'") if not idee and not hand]
PY={k[3:]:v for k,v in globals().items() if k.startswith('py_')}
REGELS=[(r[0][2:] if r[0].startswith('R-') else r[0],r[1],r[2]) for r in q("select code,sql_test,coalesce(niveau,'fout') from regel where status='actief' order by id")] if 'regel' in TABS else OUD
B=[];S=[];GEDRAAID=[]
for naam,test,niv in REGELS:
  try: res=PY[test[3:]]() if test.startswith('py:') else q(test)
  except Exception as e: res=[('-',f'REGEL KAPOT: {e}')];niv='fout'
  GEDRAAID.append((naam,niv,len(res)))
  for code,d in res: (B if niv=='fout' else S).append((naam,code or '-',(d or '')[:300]))
B=list(dict.fromkeys(B))
if '--json' in sys.argv:
  import json;json.dump(B,open(sys.argv[sys.argv.index('--json')+1],'w'),ensure_ascii=False,indent=0)
U={(t,code,d) for t,code,d in q('select toets,code,detail from toets_uitzondering')}
nieuw=[x for x in B if x not in U];bekend=[x for x in B if x in U]
tel=collections.Counter(t for t,_,_ in nieuw);telb=collections.Counter(t for t,_,_ in bekend);tels=collections.Counter(t for t,_,_ in S)
L=[f'# Toets {DB}',f'Regels gedraaid: {len(GEDRAAID)} (fout: {sum(1 for g in GEDRAAID if g[1]=="fout")}, signaal: {sum(1 for g in GEDRAAID if g[1]=="signaal")})',f'Nieuwe fouten: {len(nieuw)} {dict(tel)}',f'Bekend (geregistreerd met wrijving): {len(bekend)} {dict(telb)}',f'Signalen (laten de ronde niet falen): {len(S)} {dict(tels)}','']
L+=[f'- NIEUW [{t}] {code}: {d}' for t,code,d in nieuw]
if '--alles' in sys.argv: L+=[f'- bekend [{t}] {code}: {d}' for t,code,d in bekend]+[f'- signaal [{t}] {code}: {d}' for t,code,d in S]
print('\n'.join(L if len(L)<200 else L[:200]+[f'... ({len(L)-200} meer)']))
if RAP: open(RAP,'w').write('\n'.join(L)+'\n')
sys.exit(1 if nieuw else 0)
