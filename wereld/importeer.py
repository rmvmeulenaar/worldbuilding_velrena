#!/usr/bin/env python3
"""Gebruik: python3 importeer.py WERELD_VELMARA.md nieuw.db  -> leest REC-blokken in een nieuwe SQLite-database."""
import sys,re,sqlite3,os
src,dst=sys.argv[1],sys.argv[2]
if os.path.exists(dst): sys.exit(dst+' bestaat al; kies een nieuwe naam.')
c=sqlite3.connect(dst)
c.executescript("""create table canon(id integer primary key,categorie text,onderwerp text,feit text,status text,reden text,hangt_samen_met text,ronde integer,code text unique,verwijst_naar text,jaar integer,tijdperk text,intensiteit integer,weet text,functie text,afstoting integer,aantrekking_bron text,aantrekking integer,techniek text,draagkracht text,ideeenbank integer,veilig_18plus integer,veilig_variant text,vervangen_door text,feit_schoon text,draagkracht_handmatig text);
create table anker(id integer primary key,sleutel text unique,waarde text,bron_code text,toelichting text,patroon text,bereik text);
create table naam_markering(id integer primary key,naam_a text,naam_b text,codes text,soort text,status text,wrijving text,toelichting text,unique(naam_a,naam_b));
create table toets_uitzondering(id integer primary key,toets text,code text,detail text,reden text,wrijving text,unique(toets,code,detail));
create table wijziging(id integer primary key,ronde text,code text,soort text,veld text,oud text,nieuw text,datum text,bron text,unique(ronde,code,soort,veld,nieuw));
create table schema_versie(versie integer primary key,naam text,toegepast text);
create table handleiding(id integer primary key,code text unique,onderwerp text,tekst text);
create table wrijving(id integer primary key,titel text,delen_die_botsen text,beschrijving text,type text,status text,code text unique,verwijst_naar text);
create table open_vraag(id integer primary key,vraag text,waarom_belangrijk text,status text,antwoord text,code text unique,verwijst_naar text);
create table logboek(id integer primary key,datum text,wat text);
create table regel(id integer primary key,code text unique,domein text,omschrijving text,sql_test text,bron text,goedgekeurd_door text,status text,niveau text);
create table boog(id integer primary key,code text unique,fase text,boek text,hoofdpersoon text,leeftijd_hoofdpersoon integer,geslacht_hoofdpersoon text,romance text,erotische_sleutelscene text,terugkerend_motief text,noodoplossing text,wie_betaalt text,toon text,vorm text,afloop text,bron text,status text,voorstel text,voorstel_status text,verteller text,tempo text);
create table personage(id integer primary key,code text unique,naam text,per_code text,fase text,rol text,eigen_fout text,soort_fout text,wie_betaalt text,zelfbedrog text,daarna_doet text,bron text,status text,voorstel text,voorstel_status text);
create table zaadje(id integer primary key,code text unique,wat text,geplant_in text,oogst_in text,status text,bron text);
create table sjabloon_familie(id integer primary key,sig text unique,grootte integer,prefixen text,markering text,voorstel text,voorbeeld text);
create table sjabloon_lid(id integer primary key,sig text,code text,markering text,unique(sig,code));""")
# Z35: nieuwe Model-tabellen en boog-kolommen komen uit migratie 005; hier alleen de kolommen die de export draagt
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'migraties'))
import importlib.util as _iu
for _p in sorted(sum((__import__('glob').glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'migraties',_g)) for _g in ('00[56789]_*.py','01[0-9]_*.py')),[])):
  _s=_iu.spec_from_file_location('m5',_p);_m=_iu.module_from_spec(_s);_s.loader.exec_module(_m);_m.migreer(c)
Z36T=('verhaal_as','boog_as','verhaal_profiel','doel','doelprofiel','lezersdata','gewichtset','ideeen_verwerking','domein','competentievraag','competentie_antwoord','motief_detail','beroep','gave','sim_regel','gebeurtenis_type','tech_gebeurtenistype','sim_run','sim_gebeurtenis','sim_figuur','verblijf','kennis','per_relatie','steekproef','sim_fase','sim_wet','sim_huis')
INV={'wat':'feit','waarom':'reden'};n={}
for t,body in re.findall(r'<!-- REC (\w+) -->\n(.*?)<!-- /REC -->',open(src).read(),re.S):
  d={}
  for k,v in re.findall(r'^- \*\*(\w+):\*\* ?(.*)$',body,re.M): d[INV.get(k,k) if t=='canon' else k]=v if v!='' else None
  if t=='canon':
    for k in ('ronde','jaar','intensiteit','afstoting','aantrekking','ideeenbank','veilig_18plus'):
      if d.get(k) is not None: d[k]=int(d[k])
  if t=='logboek': d['id']=int(d['id'])
  if t=='schema_versie': d['versie']=int(d['versie'])
  if t=='wijziging' and d.get('veld') is None: d['veld']=''
  if t=='boog' and d.get('leeftijd_hoofdpersoon') is not None: d['leeftijd_hoofdpersoon']=int(d['leeftijd_hoofdpersoon'])
  if t=='sjabloon_familie' and d.get('grootte') is not None: d['grootte']=int(d['grootte'])
  for _k in {'personage_toestand':('jaar','leeftijd','aanname'),'levensduur':('jaren',),'fase_rijm':('volgorde',),'kernscene':('volgorde',),'keuze':('impact',)}.get(t,()):
    if d.get(_k) is not None: d[_k]=int(d[_k])
  if t in Z36T:
    for _k,_ty in [(r[1],r[2].upper()) for r in c.execute(f'pragma table_info({t})')]:
      if d.get(_k) is not None and _ty in('INTEGER','REAL'): d[_k]=(int if _ty=='INTEGER' else float)(d[_k])
  c.execute(f"insert into {t}({','.join(d)}) values({','.join('?'*len(d))})",list(d.values()));n[t]=n.get(t,0)+1
c.commit();print('geïmporteerd:',n)
