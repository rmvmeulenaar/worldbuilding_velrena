"""Ronde Z30: afgeleide architectuur (draagkracht, veiligheid, verwijzingen, historie, views).
Deterministisch en herhaalbaar: bron blijft de kolom `feit`; alles hier wordt eruit afgeleid.
Raakt NOOIT draagkracht_handmatig, anker, naam_markering, toets_uitzondering, wijziging of schema_versie aan.
Gebruik: python3 afgeleid.py [db]   (draait ook vanuit r_Z30.py)"""
import sqlite3,re,sys
KERN_RE=re.compile(r"^(ORIGIN-|GEH-zegel|REGEL-|GES-officiele|KAL-|EROS-GRENZEN|BESLUIT-\d+(-Z1)?$|BESLUIT-Z12-|BESLUIT-Z11-tijdlijn|BESLUIT-V5-|BESLUIT-Z16-|BESLUIT-Z30-|GEH-zegel-Z30|ROMAN-Z16-roman$|PER-liora-profiel$|PER-liora-Z6$|PER-aeron-profiel$|FASE-OVERZICHT-|TOESTAND-Z1[67]-PER-v4-(ysa-maren|thalen-orr)-)")
KERN_CAT={'Oorsprong','Tijdlijn','Demografie','Tijdperk','Magie','Geheimen'}
NIET_KERN=re.compile(r"^(ZINT-|MAGIE-GESCH-|GEB-)")
IDEE_PREF={'KINKFUNC','KINK','ACTIE','HORROR','COMEDY','SAW','NERD','ROMANCE','ROM','HELD','THRL','HAAK','VERLEID','DEGEN','OORLOG'}
IDEE_CAT={'Kinks en situaties','Horror','Comedy','Actie','Held','Romantiek','Oorlog','Haak'}
KLEUR_PREF={'ZINT'}
LBL=re.compile(r" ?(?<![\w(])(?:Veiligheids)?[Ll]abel: .*?\.(?= |$)")
TAG=re.compile(r" ?\[(?:Ronde )?[ZBGVDKr]\d+[a-z]?(?:[ :,][^\]]*)?\]")
VERV=re.compile(r"(?:[Vv]ervangen door|dubbel van) ([A-Z][A-Za-z0-9À-ÿ-]*[A-Za-z0-9])")
REGELS="""1. Status 'vervallen' of 'voorlopig, vervangen' -> Kleur (archief, buiten beeld in v_actief).
2. Status 'vastgesteld' EN (code past op KERN_RE of categorie in KERN_CAT) EN niet NIET_KERN -> Kern.
3. Code-prefix in IDEE_PREF of categorie in IDEE_CAT -> Kleur + ideeenbank=1.
4. Code-prefix ZINT (zintuigvoorbeelden) -> Kleur.
5. Al het andere (ook voorlopig: niet zeker = Structuur) -> Structuur.
6. Z34: rij in sjabloon_lid met markering 'ideeenbank' -> Kleur + ideeenbank=1 (niet als Kern, niet als draagkracht_handmatig gezet is).
7. Z40: rij met epistemiek 'simulatie ...' -> Kleur + ideeenbank=1, tenzij draagkracht_handmatig gezet is (dat gebeurt alleen bij een BESLUIT van Rogier). Simulatie wordt nooit vanzelf levende canon (BESLUIT-Z39-5, BESLUIT-Z40-2).
0. Voorrang (Z31): staat er iets in draagkracht_handmatig, dan wint dat altijd; dit script schrijft die kolom nooit. Uitzondering: een rij met status vervallen of 'voorlopig, vervangen' wordt nooit Kern (dan Kleur; toets.py meldt het)."""
def pref(code): return re.split(r'[-_]',code or '')[0]
def klasse(code,cat,st):
  idee=int(pref(code) in IDEE_PREF or cat in IDEE_CAT)
  if st in('vervallen','voorlopig, vervangen'): return 'Kleur',idee
  if st=='vastgesteld' and (KERN_RE.match(code) or cat in KERN_CAT) and not NIET_KERN.match(code): return 'Kern',0
  if idee or pref(code) in KLEUR_PREF: return 'Kleur',idee
  return 'Structuur',0
def kolom(c,t,k,typ):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {typ}')
def schema(c):
  for k,t in [('draagkracht','text'),('ideeenbank','integer'),('veilig_18plus','integer'),('veilig_variant','text'),('vervangen_door','text'),('feit_schoon','text')]: kolom(c,'canon',k,t)
  c.executescript("""
create table if not exists veiligheid_varianten(id integer primary key,tekst text unique,aantal integer,afwijking text,strippen integer);
create table if not exists verwijzing(van_tabel text,van_code text,naar_code text,bestaat integer);
create table if not exists historie(id integer primary key,code text,veld text,notitie text,origineel text);
create table if not exists handleiding(id integer primary key,code text unique,onderwerp text,tekst text);
create index if not exists ix_canon_code on canon(code);
create index if not exists ix_canon_cat on canon(categorie);
create index if not exists ix_canon_status on canon(status);
create index if not exists ix_canon_dk on canon(draagkracht);
create index if not exists ix_verw_van on verwijzing(van_code);
create index if not exists ix_verw_naar on verwijzing(naar_code);
create index if not exists ix_hist_code on historie(code);
drop view if exists v_kern; drop view if exists v_actief; drop view if exists v_ideeenbank; drop view if exists v_open; drop view if exists v_dode_links;
create view v_actief as select id,code,categorie,onderwerp,feit_schoon as feit,draagkracht,status,jaar,tijdperk,verwijst_naar from canon where status in('vastgesteld','voorlopig') and coalesce(ideeenbank,0)=0;
create view v_kern as select * from v_actief where draagkracht='Kern';
create view v_ideeenbank as select id,code,categorie,onderwerp,feit_schoon as feit,status from canon where ideeenbank=1 and status in('vastgesteld','voorlopig');
create view v_open as select 'wrijving' as soort,code,titel as wat,status,beschrijving as toelichting from wrijving where status like 'open%' union all select 'open_vraag',code,vraag,status,waarom_belangrijk from open_vraag where status like 'open%';
create view v_dode_links as select * from verwijzing where bestaat=0;
""")
def afwijking(t):
  w=[]
  if 'zonder instemming' in t: w.append("strenger: 'geen seksuele inhoud zonder instemming' (sluit gelabelde dwang tussen volwassenen uit)")
  if 'mogen hard' in t: w.append("extra: 'geweld/horror mogen hard'")
  if 'dwang tussen volwassenen' in t: w.append("de officiële zin over gelabelde dwang")
  if "geen minderjarigen" in t and "thema" not in t: w.append("mist 'donkere thema's gelabeld'")
  if 'Jongenshof' in t: w.append("noemt Jongenshof (inhoudelijk, niet-seksueel)")
  if 'geen minderjarigen' not in t: w.append("geen harde-lijnenlabel maar een themalabel")
  return '; '.join(w) or 'standaardformulering'
def bouw(c):
  schema(c)
  if 'draagkracht_handmatig' not in [r[1] for r in c.execute('pragma table_info(canon)')]: c.execute('alter table canon add column draagkracht_handmatig text')
  _epi='epistemiek' in [r[1] for r in c.execute('pragma table_info(canon)')]
  rows=c.execute('select id,code,categorie,status,feit,reden,verwijst_naar,draagkracht_handmatig'+(',epistemiek' if _epi else ',null')+' from canon').fetchall()
  # Z34: sjabloonleden die als ideeenbank gemarkeerd zijn (tabel sjabloon_lid, met de hand/besluit; dit script schrijft die tabel nooit)
  IDEE_LID={r[0] for r in c.execute("select code from sjabloon_lid where markering='ideeenbank'")} if c.execute("select 1 from sqlite_master where name='sjabloon_lid'").fetchone() else set()
  codes=set(r[1] for r in rows)
  import collections;cnt=collections.Counter(m.group(0).strip() for r in rows for m in LBL.finditer(r[4] or ''))
  for t,n in cnt.most_common():
    s=int('geen minderjarigen' in t and 'Jongenshof' not in t)
    if c.execute('select 1 from veiligheid_varianten where tekst=?',(t,)).fetchone(): c.execute('update veiligheid_varianten set aantal=?,afwijking=?,strippen=? where tekst=?',(n,afwijking(t),s,t))
    else: c.execute('insert into veiligheid_varianten(tekst,aantal,afwijking,strippen) values(?,?,?,?)',(t,n,afwijking(t),s))
  V={t:(i,s) for i,t,s in c.execute('select id,tekst,strippen from veiligheid_varianten')}
  c.execute('delete from verwijzing');c.execute('delete from historie')
  for i,code,cat,st,f,r,v,hand,epi in rows:
    dk,idee=klasse(code,cat,st);f=f or ''
    if code in IDEE_LID and dk!='Kern' and not hand: dk,idee='Kleur',1
    if (epi or '').startswith(('simulatie','voorstel')) and not hand: dk,idee='Kleur',1  # Z40 regel 7; Z41: ook voorstellen van de architect
    if hand: dk='Kleur' if (hand=='Kern' and st in('vervallen','voorlopig, vervangen')) else hand
    ids=[];schoon=f
    for m in LBL.finditer(f):
      vid,s=V[m.group(0).strip()];ids.append(str(vid))
      if s: schoon=schoon.replace(m.group(0),'',1)
    for m in TAG.finditer(schoon): c.execute('insert into historie(code,veld,notitie,origineel) values(?,?,?,?)',(code,'feit',m.group(0).strip(),None))
    for m in TAG.finditer(r or ''): c.execute('insert into historie(code,veld,notitie,origineel) values(?,?,?,?)',(code,'reden',m.group(0).strip(),None))
    schoon=re.sub(r'  +',' ',TAG.sub('',schoon)).strip()
    if schoon!=f: c.execute('insert into historie(code,veld,notitie,origineel) values(?,?,?,?)',(code,'feit','origineel feit (volledig)',f))
    vd=VERV.findall((f)+' '+(r or ''))
    vd=next((x for x in vd if x in codes),None) if st=='voorlopig, vervangen' else None
    c.execute('update canon set draagkracht=?,ideeenbank=?,veilig_18plus=?,veilig_variant=?,feit_schoon=?,vervangen_door=coalesce(vervangen_door,?) where id=?',(dk,idee,int(bool(ids)),';'.join(ids) or None,schoon,vd,i))
  for tab in('canon','wrijving','open_vraag'):
    for code,v in c.execute(f'select code,verwijst_naar from {tab}').fetchall():
      for n in re.split(r'[;,]\s*',v or ''):
        n=n.strip()
        if n and n!='-': c.execute('insert into verwijzing values(?,?,?,?)',(tab,code,n,int(n in codes or bool(c.execute('select 1 from wrijving where code=? union select 1 from open_vraag where code=? union select 1 from handleiding where code=?',(n,n,n)).fetchone()))))
  import os as _o,sys as _s;_s.path.insert(0,_o.path.dirname(_o.path.abspath(__file__)));import afgeleid_motor;afgeleid_motor.bouw(c)
  c.commit()
if __name__=='__main__':
  c=sqlite3.connect(sys.argv[1] if len(sys.argv)>1 else 'canon.db');bouw(c)
  print(c.execute('select draagkracht,count(*) from canon group by 1').fetchall())
