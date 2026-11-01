"""Migratie 006 (ronde Z36, de verhalenmachine). Idempotent, additief.
Model (nieuw):
  verhaal_as(as_naam, waarde, toelichting, prior)      de toegestane waarden per as (stap 7); prior = aanname lezersvraag per genre (stap 8)
  verhaal_profiel                                         ideeënbank van de machine: elk profiel op 7 assen + genrevector + scores + filteruitslag (stap 7-9)
  boog_as(boog_code, positie..hoofdpersoon, genrevector)  de assen en genrevector van elke bestaande boog (stap 7.2 / 9a.1)
  doel(code, omschrijving, gewicht, bron_gewicht, richting)                 (stap 8.1)
  doelprofiel(code, naam, doel_*, min_*)                                    (stap 9a.2)
  lezersdata(boog_code, hoofdstuk, bron, datum, reads, afmaakpercentage, reacties)  (stap 8.5)
  gewichtset(naam, datum, methode, status, gewichten, bron)                 (stap 9b)
  ideeen_verwerking(code, ..., uitslag)                                     rapport ideeënbank door de machine (Z36 extra 1)
keuze: kolom citaat (werkregel 2).
Views: v_verhaal_as (bogen + profielen op de assen), v_positie_dekking (fase x positie), v_ideeen_rapport.
Triggers: nooit verwijderen."""
VERSIE=6;NAAM='z36_machine'
G=['romance','erotiek','horror','suspense','actie','intrige','komedie','tragiek']
def migreer(c):
  gv=','.join(f'g_{g} integer check(g_{g} between 0 and 5)' for g in G)
  c.executescript(f"""
create table if not exists verhaal_as(id integer primary key,as_naam text,waarde text,toelichting text,prior real,unique(as_naam,waarde));
create table if not exists boog_as(id integer primary key,boog_code text unique,positie text,genre text,schaal text,volk text,vorm text,afloop text,hoofdpersoon text,{gv},bron text,status text);
create table if not exists verhaal_profiel(id integer primary key,code text unique,run text,fase text,positie text,genre text,schaal text,volk text,vorm text,afloop text,hoofdpersoon text,leeftijd integer,geslacht text,partner text,instemming text,dwang_label integer default 0,{gv},
  erf_code text,zaadje_code text,wereldregel_code text,kern_codes text,herkomst text,doelprofiel text,
  nieuwheid real,verbondenheid real,seriewaarde real,lezersvraag real,kosten real,genrematch real,marginale_winst real,gevoeligheid text,
  uitslag text,reden text,status text default 'voorlopig',ideeenbank integer default 1);
create table if not exists doel(id integer primary key,code text unique,omschrijving text,gewicht real,bron_gewicht text,richting text check(richting in('max','min')));
create table if not exists doelprofiel(id integer primary key,code text unique,naam text unique,{','.join(f'doel_{g} integer' for g in G)},{','.join(f'min_{g} integer' for g in G)},bron text,status text);
create table if not exists lezersdata(id integer primary key,boog_code text,hoofdstuk text,bron text,datum text,reads integer,afmaakpercentage real,reacties integer);
create table if not exists gewichtset(id integer primary key,naam text,datum text,methode text,status text,gewichten text,bron text,unique(naam,datum,methode));
create table if not exists ideeen_verwerking(id integer primary key,code text unique,fase text,positie text,genre text,afstand_min integer,dichtste text,verbinding text,uitslag text,reden text,profiel_code text);
create index if not exists ix_vp_fase on verhaal_profiel(fase);
""")
  for t in ('verhaal_as','boog_as','verhaal_profiel','doel','doelprofiel','lezersdata','gewichtset','ideeen_verwerking'):
    c.execute(f"create trigger if not exists t_{t}_geen_delete before delete on {t} begin select raise(abort,'{t}: nooit verwijderen'); end")
  if 'drager' not in [r[1] for r in c.execute('pragma table_info(verhaal_profiel)')]: c.execute('alter table verhaal_profiel add column drager text')
  if 'citaat' not in [r[1] for r in c.execute('pragma table_info(keuze)')]: c.execute('alter table keuze add column citaat text')
  c.executescript("""
drop view if exists v_verhaal_as;
create view v_verhaal_as as
 select 'boog' as soort,b.fase,a.boog_code as code,a.positie,a.genre,a.schaal,a.volk,a.vorm,a.afloop,a.hoofdpersoon,a.status from boog_as a join boog b on b.code=a.boog_code
 union all
 select 'profiel',fase,code,positie,genre,schaal,volk,vorm,afloop,hoofdpersoon,uitslag from verhaal_profiel where uitslag in('ent-klaar','voorgesteld');
drop view if exists v_positie_dekking;
create view v_positie_dekking as
 select r.fase,p.waarde as positie,
  (select count(*) from v_verhaal_as v where v.fase=r.fase and v.positie=p.waarde and v.soort='boog') as in_canon,
  (select count(*) from v_verhaal_as v where v.fase=r.fase and v.positie=p.waarde and v.soort='profiel') as in_ideeenbank
 from fase_rijm r join verhaal_as p on p.as_naam='positie' order by r.volgorde,p.id;
drop view if exists v_ideeen_rapport;
create view v_ideeen_rapport as
 select coalesce(fase,'(geen fase)') as fase,coalesce(positie,'-') as positie,count(*) as instroom,
  sum(uitslag='uitval: afstand') as uitval_afstand,sum(uitval_verbinding) as uitval_verbinding,sum(uitslag='ent-klaar') as ent_klaar,sum(uitslag='uitval: geen fase') as geen_fase,sum(uitslag like 'uitval: filter%') as uitval_filter
 from (select *,uitslag='uitval: verbinding' as uitval_verbinding from ideeen_verwerking) group by 1,2;
""")
