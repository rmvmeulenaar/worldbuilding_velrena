"""Migratie 011 (ronde Z44: de technologieboom). Idempotent, additief.
Tabellen (elk gebruikt door een view en een toetsregel in dezelfde ronde):
  tech_knoop       de boom zelf: per knoop familie, domein, vereisten, materiaalvoorwaarde, noodzaak, uitvinder, gevolg,
                   wat ze breekt, prijs, afstoting en canonbron; ook wat Velmara niet doet (status onmogelijk/onnodig) met reden.
                                                                   -> v_tech_boom, regel R-tech_boom
  sim_uitvinding   per gekozen run: welke knoop wanneer, door wie met hoeveel macht, uit welke nood, met welke vereisten
                   (en wanneer die er kwamen), en het gevolg na 60 jaar.   -> v_sim_uitvinding, regel R-sim_uitvinding"""
VERSIE = 11; NAAM = 'z44_boom'

def migreer(c):
    c.executescript("""
create table if not exists tech_knoop(id integer primary key,code text unique,naam text,familie text,domein text,status text,vereist text,
  materiaal text,noodzaak text,uitvinder text,gevolg text,breekt text,prijs text,afstoting integer,reden text,bron text,epistemiek text);
create table if not exists sim_uitvinding(id integer primary key,run_id text,module text,knoop text,jaar integer,uitvinder text,uitvinder_macht real,
  noodzaak text,materiaal text,vereist_met text,breekt text,prijs text,gevolg text,epistemiek text,unique(run_id,knoop));
drop view if exists v_tech_boom;
create view v_tech_boom as select code,naam,familie,domein,status,vereist,materiaal,noodzaak,uitvinder,breekt,prijs,afstoting,reden,bron
  from tech_knoop order by status,familie,code;
drop view if exists v_sim_uitvinding;
create view v_sim_uitvinding as select u.run_id,u.jaar,u.knoop,k.naam,k.familie,u.uitvinder,round(u.uitvinder_macht,2) as macht,u.noodzaak,u.vereist_met,u.breekt,u.gevolg
  from sim_uitvinding u left join tech_knoop k on k.code=u.knoop order by u.run_id,u.jaar;
""")
