"""Migratie 002 (ronde Z31): robuust tegen kettingschade.
- canon.draagkracht_handmatig (override; afgeleid.py raakt hem nooit aan, heeft voorrang)
- anker: bron van waarheid voor sleutelgetallen/jaren/namen (+ patroon voor de afwijkingstoets)
- naam_markering: bewuste echo/erfnaam of open naambotsing
- toets_uitzondering: bekende, geregistreerde bevindingen (met wrijving) die toets.py niet laten falen
- wijziging: machineleesbaar logboek (licht event sourcing)
- schema_versie: welke migraties zijn toegepast"""
VERSIE=2;NAAM='z31_robuust'
def kolom(c,t,k,typ):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {typ}')
def migreer(c):
  kolom(c,'canon','draagkracht_handmatig','text')
  c.executescript("""
create table if not exists anker(id integer primary key,sleutel text unique,waarde text,bron_code text,toelichting text,patroon text,bereik text);
create table if not exists naam_markering(id integer primary key,naam_a text,naam_b text,codes text,soort text,status text,wrijving text,toelichting text,unique(naam_a,naam_b));
create table if not exists toets_uitzondering(id integer primary key,toets text,code text,detail text,reden text,wrijving text,unique(toets,code,detail));
create table if not exists wijziging(id integer primary key,ronde text,code text,soort text,veld text,oud text,nieuw text,datum text,bron text,unique(ronde,code,soort,veld,nieuw));
create index if not exists ix_wijz_code on wijziging(code);
""")
