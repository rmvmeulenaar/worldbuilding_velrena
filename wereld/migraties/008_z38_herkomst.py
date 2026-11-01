"""Migratie 008 (ronde Z38: herkomst in lagen, premisses met de hand, rijkdom mens per regio). Idempotent, additief.
Kolommen:
  canon.context          C1-keten die GEEN bron is (verwezen rij met bron, maar zonder gedeelde waarde): context, geen herkomst
  canon.herkomst_laag    hard (besluit, roman, notitie Rogier) | bijbel (wereldbijbel) | context (alleen C1-keten) | onbekend
  canon.bron_handmatig   bron die Rogier zelf aanwees (BESLUIT-Z38-1); gaat voor op elke afleiding
  verhaal_profiel.vervangen_door   samengevoegd profiel wijst naar het profiel dat blijft (B2: zelfde drager, zelfde obstakel)
  ideeen_verwerking.fase_bron, uitslag_z38, reden_z38, assen_z38   B3: waar de fase vandaan komt, nieuwe meting naast de oude
  competentievraag.volk  vraag die alleen voor één volk geldt (NULL = alle volken)
  competentie_antwoord.regio   regio van het antwoord (C: mens in 801 per regio)
View v_rijkdom: vragen per volk (algemeen + eigen vragen)."""
VERSIE=8;NAAM='z38_herkomst'
def _kol(c,t,k,ty='text'):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {ty}')
def migreer(c):
  for k in ('context','herkomst_laag','bron_handmatig'): _kol(c,'canon',k)
  _kol(c,'verhaal_profiel','vervangen_door')
  for k,ty in (('fase_bron','text'),('uitslag_z38','text'),('reden_z38','text'),('assen_z38','integer')): _kol(c,'ideeen_verwerking',k,ty)
  _kol(c,'competentievraag','volk');_kol(c,'competentie_antwoord','regio')
  if c.execute("select 1 from sqlite_master where name='rijkdom_lid'").fetchone():
    c.executescript("""
drop view if exists v_rijkdom;
create view v_rijkdom as
 select v.volk,v.fase_nr,d.code as domein,d.naam,
  (select count(distinct l.code) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code) as dekking,
  (select count(distinct l.laag) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code) as diepte,
  (select count(distinct l.code) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code
     and exists(select 1 from relatie r where r.naar_code=l.code or (r.van_code=l.code and (r.naar_code like 'PER%' or r.naar_code like 'ERF-%' or r.naar_code like 'VERHAAL%' or r.naar_code like 'HOOFDPERS%')))) as verbonden,
  (select count(*) from competentievraag q where q.domein_code=d.code and (q.volk is null or q.volk=v.volk)) as vragen,
  (select count(distinct a.vraag_code) from competentie_antwoord a join competentievraag q on q.code=a.vraag_code where q.domein_code=d.code and a.volk=v.volk and a.fase_nr=v.fase_nr) as beantwoord
 from (select distinct volk,fase_nr from rijkdom_lid) v cross join domein d;
""")
