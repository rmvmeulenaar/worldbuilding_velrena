"""Migratie 009 (ronde Z39: personagenetwerk en wereldsimulatie, opdracht_Z35.md stap 11). Idempotent, additief.
Tabellen (elk gebruikt door z39/sim.py, z39/tech.py, z39/intrige.py of de steekproef):
  verblijf(per_code, plek_code, van_jaar, tot_jaar)        wie waar wanneer (11a.2)
  kennis(per_code, weet_code, sinds_jaar, bron)              wie wat weet sinds wanneer (11a.3)
  per_relatie(van_code, soort, naar_code, van_jaar, tot_jaar) bron voor de nieuwe relatiesoorten in relatie (11a.4)
  sim_figuur                                                 achtergrondfiguren, pas gemaakt als een run ze nodig heeft (11a.1)
  sim_regel                                                  wereldregels als simulatieregels, met bron (11b.2)
  gebeurtenis_type                                           toegestane gebeurtenistypen van de personenmotor; geen type met harde-lijnrisico (11b.4)
  tech_gebeurtenistype                                       eigen gebeurtenistypen + invariant van de module technologie/beroepen (11c)
  sim_run, sim_gebeurtenis                                   Monte Carlo-runs (alle 1.000 + per module), en de gebeurtenissen van de top-5 (11b.5-7)
  steekproef                                                 acceptance sampling van nieuwe rijen (11d.2)
Kolommen: relatie.van_jaar, relatie.tot_jaar; epistemiek op alle nieuwe tabellen en canon; sim_gebeurtenis.oorzaak.
Views: v_personage_laag, v_sim_fase, v_sim_wie_weet, v_sim_waar, v_sim_validatie (koude lezer, 11d.3)."""
VERSIE=9;NAAM='z39_simulatie'
def _kol(c,t,k,ty='text'):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {ty}')
def migreer(c):
  c.executescript("""
create table if not exists verblijf(id integer primary key,per_code text,plek_code text,van_jaar integer,tot_jaar integer,bron text,status text,unique(per_code,plek_code,van_jaar,bron));
create table if not exists kennis(id integer primary key,per_code text,weet_code text,sinds_jaar integer,bron text,status text,unique(per_code,weet_code,bron));
create table if not exists per_relatie(id integer primary key,van_code text,soort text,naar_code text,van_jaar integer,tot_jaar integer,bron text,status text,unique(van_code,soort,naar_code,van_jaar,bron));
create table if not exists sim_figuur(id integer primary key,code text unique,naam text,laag text,volk text,geslacht text,plek_code text,functie text,geboren integer,ouder_code text,run_id text,bron text,status text);
create table if not exists sim_regel(id integer primary key,code text unique,module text,omschrijving text,parameter text,waarde text,bron_code text,aanname integer,actief_van integer,actief_tot integer,status text);
create table if not exists gebeurtenis_type(id integer primary key,code text unique,module text,omschrijving text,min_leeftijd integer,minderjarige_rol text,instemming_nodig integer,harde_lijn_risico integer,bron_code text);
create table if not exists tech_gebeurtenistype(id integer primary key,code text unique,module text,omschrijving text,invariant text,bron_code text);
create table if not exists sim_run(id integer primary key,run_id text unique,module text,fase_nr integer,seed integer,geldig integer,reden text,n_gebeurtenis integer,scores text,pareto_rang integer,gewogen real,gekozen integer,bron text);
create table if not exists sim_gebeurtenis(id integer primary key,run_id text,module text,jaar integer,seizoen text,type_code text,actor text,doel text,plek_code text,detail text,canon_code text,status text,unique(run_id,jaar,seizoen,type_code,actor,doel));
create table if not exists steekproef(id integer primary key,ronde text,tabel text,code text,past integer,geen_sjabloon integer,verbinding integer,oordeel text,toelichting text,unique(ronde,tabel,code));
""")
  if c.execute("select 1 from sqlite_master where name='relatie'").fetchone(): _kol(c,'relatie','van_jaar','integer');_kol(c,'relatie','tot_jaar','integer')
  # Aanscherping Z39 criterium 2: epistemiek op elke nieuwe rij en gebeurtenis: 'feit (...)', 'aanname (reden)' of 'simulatie (run-id, seed)'
  for t in ('verblijf','kennis','per_relatie','sim_figuur','sim_regel','gebeurtenis_type','tech_gebeurtenistype','sim_run','sim_gebeurtenis','steekproef','canon'): _kol(c,t,'epistemiek')
  _kol(c,'sim_gebeurtenis','oorzaak')
  c.executescript("""
drop view if exists v_personage_laag;
create view v_personage_laag as
 select p.code,p.naam,p.volk,p.fase_nr,
  case when exists(select 1 from personage h where h.per_code=p.code or h.code=p.code) then 'hoofd'
       when coalesce(p.wil,'')!='' or coalesce(p.geheim,'')!='' or coalesce(p.relaties,'')!='' then 'bij' else 'achtergrond' end as laag,
  p.regio as plek,p.rol as functie,'personage_profiel' as bron from personage_profiel p
 union all select f.code,f.naam,f.volk,4,'achtergrond',f.plek_code,f.functie,'sim_figuur' from sim_figuur f;
drop view if exists v_sim_fase;
create view v_sim_fase as select module,fase_nr,count(*) as runs,sum(geldig) as geldig,count(*)-sum(geldig) as weggegooid,sum(gekozen) as gekozen from sim_run group by 1,2;
drop view if exists v_sim_wie_weet;
create view v_sim_wie_weet as select k.per_code,coalesce(p.naam,f.naam) as naam,k.weet_code,k.sinds_jaar,k.bron from kennis k left join personage_profiel p on p.code=k.per_code left join sim_figuur f on f.code=k.per_code;
drop view if exists v_sim_waar;
create view v_sim_waar as select v.per_code,coalesce(p.naam,f.naam) as naam,v.plek_code,v.van_jaar,v.tot_jaar from verblijf v left join personage_profiel p on p.code=v.per_code left join sim_figuur f on f.code=v.per_code;
drop view if exists v_sim_top;
create view v_sim_top as select run_id,module,fase_nr,seed,pareto_rang,gewogen,scores from sim_run where gekozen=1;
drop view if exists v_sim_validatie;
create view v_sim_validatie as select module,canon_code,count(distinct run_id) as runs,min(jaar) as vroegst,max(jaar) as laatst,group_concat(distinct type_code) as typen from sim_gebeurtenis where canon_code is not null group by 1,2;
""")
