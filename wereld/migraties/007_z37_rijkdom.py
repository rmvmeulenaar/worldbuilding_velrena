"""Migratie 007 (ronde Z37: machine herstellen, personage_profiel als bron, rijkdom). Idempotent, additief.
Nieuw:
  domein(code, naam, toelichting)                         17 levensdomeinen (opdracht_Z35 stap 10)
  competentievraag(code, domein_code, vraag)              3-5 vragen per domein; {volk} wordt per volk ingevuld
  competentie_antwoord(vraag_code, volk, fase_nr, antwoord_code)   welke canonrij de vraag beantwoordt (bron van '% beantwoord')
  rijkdom_lid(code, volk, fase_nr, domein_code, laag)     afgeleid (afgeleid_motor.rijkdom): welke rij telt in welke cel
  motief_detail(code, detail, patroon, codes, aantal, status)  een detail telt pas als motief bij >= 2 verhalen
  beroep(code, naam, afgeleid_van, zwarte_tweeling, wereldregel_code, verbinding)   stap 11c, beroepen-module (rijen staan in canon, ideeënbank)
  gave(code, naam, element, prijs, ja_regel, bron)        gaven-stelsel (rijen in canon, ideeënbank)
Kolommen: verhaal_profiel.premisse, premisse_codes, seriewaarde_reden; ideeen_verwerking.vergeleken, afstand_z37, uitslag_z37, reden_z37.
View v_rijkdom (volk x fase x domein: dekking, diepte, verbondenheid, % beantwoord). Triggers: nooit verwijderen; t_canon_vd_i/u staan vervangen_door='personage_profiel:'||code toe (D2)."""
VERSIE=7;NAAM='z37_rijkdom'
def _kol(c,t,k,ty='text'):
  if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {ty}')
def migreer(c):
  c.executescript("""
create table if not exists domein(id integer primary key,code text unique,naam text,toelichting text);
create table if not exists competentievraag(id integer primary key,code text unique,domein_code text,vraag text);
create table if not exists competentie_antwoord(id integer primary key,vraag_code text,volk text,fase_nr integer,antwoord_code text,unique(vraag_code,volk,fase_nr,antwoord_code));
create table if not exists rijkdom_lid(id integer primary key,code text,volk text,fase_nr integer,domein_code text,laag text,unique(code,volk,fase_nr,domein_code));
create table if not exists motief_detail(id integer primary key,code text unique,detail text,patroon text,codes text,aantal integer,status text);
create table if not exists beroep(id integer primary key,code text unique,naam text,afgeleid_van text,zwarte_tweeling text,wereldregel_code text,verbinding text);
create table if not exists gave(id integer primary key,code text unique,naam text,element text,prijs text,ja_regel text,bron text);
""")
  for t in ('domein','competentievraag','competentie_antwoord','motief_detail','beroep','gave'):
    c.execute(f"create trigger if not exists t_{t}_geen_delete before delete on {t} begin select raise(abort,'{t}: nooit verwijderen'); end")
  # D2: een rij mag naar zijn eigen personage_profiel-regel wijzen (vervangen_door='personage_profiel:'||code)
  for t,w in (('t_canon_vd_i','insert'),('t_canon_vd_u','update of vervangen_door')):
    sq=(c.execute("select sql from sqlite_master where name=?",(t,)).fetchone() or [''])[0] or ''
    if sq and 'personage_profiel:' not in sq:  # alleen een bestaande trigger vervangen (importeer laadt voorwaartse verwijzingen)
      c.execute(f'drop trigger if exists {t}')
      c.execute(f"create trigger {t} before {w} on canon when new.vervangen_door is not null and new.vervangen_door!='personage_profiel:'||new.code and not exists(select 1 from canon where code=new.vervangen_door) begin select raise(abort,'vervangen_door bestaat niet'); end")
  for k in ('premisse','premisse_codes','seriewaarde_reden'): _kol(c,'verhaal_profiel',k)
  for k,ty in (('vergeleken','integer'),('afstand_z37','integer'),('uitslag_z37','text'),('reden_z37','text')): _kol(c,'ideeen_verwerking',k,ty)
  c.executescript("""
drop view if exists v_rijkdom;
create view v_rijkdom as
 select v.volk,v.fase_nr,d.code as domein,d.naam,
  (select count(distinct l.code) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code) as dekking,
  (select count(distinct l.laag) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code) as diepte,
  (select count(distinct l.code) from rijkdom_lid l where l.volk=v.volk and l.fase_nr=v.fase_nr and l.domein_code=d.code
     and exists(select 1 from relatie r where r.naar_code=l.code or (r.van_code=l.code and (r.naar_code like 'PER%' or r.naar_code like 'ERF-%' or r.naar_code like 'VERHAAL%' or r.naar_code like 'HOOFDPERS%')))) as verbonden,
  (select count(*) from competentievraag q where q.domein_code=d.code) as vragen,
  (select count(distinct a.vraag_code) from competentie_antwoord a join competentievraag q on q.code=a.vraag_code where q.domein_code=d.code and a.volk=v.volk and a.fase_nr=v.fase_nr) as beantwoord
 from (select distinct volk,fase_nr from rijkdom_lid) v cross join domein d;
""")
