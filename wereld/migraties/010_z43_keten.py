"""Migratie 010 (ronde Z43: de geschiedenis verklaart zichzelf). Idempotent, additief.
Na review 1 van Z42: oorzaken, macht, wetten en huizen moeten getypeerde velden zijn, geen tekst in sim_gebeurtenis.detail.
Tabellen (elk gebruikt door een view en een toetsregel in dezelfde ronde):
  sim_fase   één rij per fase van een gekozen run: oorzaak (welke toestand de drempel passeerde), actor en zijn macht,
             mechanisme, handhaver, de vijf assen, het gedeelde mechanisme waarmee de fase rijmt, waarvan ze erft,
             en het gevolg na 60 jaar.                                   -> v_sim_keten, regels R-sim_oorzaak, R-sim_rijm
  sim_wet    één rij per wet per run: wetgever en zijn macht, rechtsgebied, handhaver, aanleiding, van/tot,
             en hoe ze verviel.                                          -> v_sim_wetboek, regel R-sim_wetgever
  sim_huis   één rij per huis per periode van gezag: bloed (ouderhuis), aanspraak, gezag van/tot.
                                                                          -> v_sim_stamboom, regel R-sim_huis"""
VERSIE = 10; NAAM = 'z43_keten'

def migreer(c):
    c.executescript("""
create table if not exists sim_fase(id integer primary key,run_id text,module text,van integer,tot integer,crisis text,oplossing text,naam text,
  beslisser text,macht_sleutel text,actor_macht real,mechanisme text,handhaver text,betaler text,vervalst text,ontdekt text,schaal text,
  oorzaak text,druk real,tweede_druk text,erft_van text,gedeeld_mechanisme text,rijmt_met text,assen_anders integer,gevolg text,blijvend text,
  epistemiek text,unique(run_id,van));
create table if not exists sim_wet(id integer primary key,run_id text,module text,wet text,tekst text,wetgever text,macht_sleutel text,
  wetgever_macht real,rechtsgebied text,handhaver text,aanleiding text,van integer,tot integer,vervalt_door text,canon_code text,
  epistemiek text,unique(run_id,wet,van));
create table if not exists sim_huis(id integer primary key,run_id text,module text,huis text,ouder text,ontstaan integer,aanspraak text,
  gezag_van integer,gezag_tot integer,gevallen integer,canon_code text,epistemiek text,unique(run_id,huis,gezag_van));
drop view if exists v_sim_keten;
create view v_sim_keten as select run_id,van,tot,crisis,naam,beslisser,round(actor_macht,2) as macht,mechanisme,erft_van,rijmt_met,assen_anders,gevolg
  from sim_fase order by run_id,van;
drop view if exists v_sim_wetboek;
create view v_sim_wetboek as select run_id,wet,tekst,wetgever,round(wetgever_macht,2) as macht,rechtsgebied,handhaver,van,tot,
  coalesce(tot,5000)-van as jaren,vervalt_door from sim_wet order by run_id,van;
drop view if exists v_sim_stamboom;
create view v_sim_stamboom as select run_id,huis,ouder,ontstaan,aanspraak,gezag_van,gezag_tot,gevallen from sim_huis order by run_id,ontstaan,gezag_van;
""")
