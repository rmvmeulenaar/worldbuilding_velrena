"""Migratie 004 (ronde Z34, 'geen sjablonen'). Idempotent.
Model: sjabloon_familie (één rij per gemeten sjabloonfamilie, met markering en voorstel), sjabloon_lid (welke rij in welke familie, markering).
afgeleid.py leest sjabloon_lid: markering 'ideeenbank' -> ideeenbank=1 en Kleur (nooit voor Kern of bij draagkracht_handmatig).
boog: extra assen verteller en tempo (mal-breker)."""
VERSIE=4;NAAM='z34_sjabloon'
def migreer(c):
  c.executescript("""
create table if not exists sjabloon_familie(id integer primary key,sig text unique,grootte integer,prefixen text,markering text,voorstel text,voorbeeld text);
create table if not exists sjabloon_lid(id integer primary key,sig text,code text,markering text,unique(sig,code));
create trigger if not exists t_sjabloon_familie_geen_delete before delete on sjabloon_familie begin select raise(abort,'sjabloon_familie: nooit verwijderen'); end;
create trigger if not exists t_sjabloon_lid_geen_delete before delete on sjabloon_lid begin select raise(abort,'sjabloon_lid: nooit verwijderen'); end;
drop view if exists v_sjabloon;
create view v_sjabloon as select f.sig,f.grootte,f.markering,f.voorstel,count(l.code) as leden from sjabloon_familie f left join sjabloon_lid l on l.sig=f.sig group by f.sig;
""")
  cols=[r[1] for r in c.execute('pragma table_info(boog)')]
  for k in ('verteller','tempo'):
    if k not in cols: c.execute(f'alter table boog add column {k} text')
