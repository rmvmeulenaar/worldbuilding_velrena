"""Migratie 003 (ronde Z33, canon-motor als meetlat). Idempotent.
Model (bron, met de hand/besluit): regel, boog, personage, zaadje.
ViewModel (afgeleid_motor.py): canon.bron/bron_soort/besloten_door/besloten_op, relatie, anker_kopie.
Views: v_impact, v_anker, v_actief_anker, v_herkomst_gat, v_mal, v_personage_gat, v_zaadje_open.
Triggers (constraints): geen DELETE op canon/wrijving/open_vraag/regel/boog/personage/zaadje; geldige status en draagkracht; vervangen_door moet bestaan."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import afgeleid_motor
VERSIE=3;NAAM='z33_motor'
MODEL="""
create table if not exists regel(id integer primary key,code text unique,domein text,omschrijving text,sql_test text,bron text,goedgekeurd_door text,status text,niveau text);
create table if not exists boog(id integer primary key,code text unique,fase text,boek text,hoofdpersoon text,leeftijd_hoofdpersoon integer,geslacht_hoofdpersoon text,romance text,erotische_sleutelscene text,terugkerend_motief text,noodoplossing text,wie_betaalt text,toon text,vorm text,afloop text,bron text,status text,voorstel text,voorstel_status text);
create table if not exists personage(id integer primary key,code text unique,naam text,per_code text,fase text,rol text,eigen_fout text,soort_fout text,wie_betaalt text,zelfbedrog text,daarna_doet text,bron text,status text,voorstel text,voorstel_status text);
create table if not exists zaadje(id integer primary key,code text unique,wat text,geplant_in text,oogst_in text,status text,bron text);
"""
def migreer(c):
  c.executescript(MODEL)
  if 'niveau' not in [r[1] for r in c.execute('pragma table_info(regel)')]: c.execute('alter table regel add column niveau text')
  afgeleid_motor.schema(c)
  c.executescript("""
drop view if exists v_impact; drop view if exists v_anker; drop view if exists v_actief_anker; drop view if exists v_herkomst_gat; drop view if exists v_mal; drop view if exists v_personage_gat; drop view if exists v_zaadje_open;
create view v_impact as select naar_code as code,van_code as leunt,1 as niveau,soort as via from relatie where soort in('leunt_op','vervangt')
  union select r1.naar_code,r2.van_code,2,r1.soort||'>'||r2.soort from relatie r1 join relatie r2 on r2.naar_code=r1.van_code and r2.soort in('leunt_op','vervangt') where r1.soort in('leunt_op','vervangt') and r2.van_code<>r1.naar_code;
create view v_anker as select a.sleutel,a.waarde,a.bron_code,c.draagkracht as bron_draagkracht,c.status as bron_status,a.toelichting,(select count(*) from anker_kopie k where k.sleutel=a.sleutel) as levende_kopieen,(select count(*) from anker_kopie k where k.sleutel=a.sleutel and k.afwijkt=1) as afwijkend from anker a left join canon c on c.code=a.bron_code;
create view v_actief_anker as select v.*,(select group_concat(k.sleutel||'='||a.waarde||' (bron '||a.bron_code||')','; ') from anker_kopie k join anker a on a.sleutel=k.sleutel where k.code=v.code) as ankerwaarden from v_actief v;
create view v_herkomst_gat as select code,draagkracht,status,bron_soort from canon where status in('vastgesteld','voorlopig') and draagkracht in('Kern','Structuur') and (bron='onbekend' or bron is null);
create view v_mal as select code,fase,boek,hoofdpersoon,leeftijd_hoofdpersoon,geslacht_hoofdpersoon,romance,erotische_sleutelscene,terugkerend_motief,noodoplossing,toon,
  (case when geslacht_hoofdpersoon='v' then 1 else 0 end)+(case when leeftijd_hoofdpersoon between 21 and 35 then 1 else 0 end)+(case when romance='ja' then 1 else 0 end)+(case when erotische_sleutelscene='ja' then 1 else 0 end)+(case when terugkerend_motief like 'register%' then 1 else 0 end) as mal_score,voorstel from boog;
create view v_personage_gat as select code,naam,fase,status,voorstel from personage where status like 'profiel%';
create view v_zaadje_open as select * from zaadje where status like 'open%';
create trigger if not exists t_canon_geen_delete before delete on canon begin select raise(abort,'canon: nooit verwijderen; zet status op vervallen of voorlopig, vervangen'); end;
create trigger if not exists t_wrijving_geen_delete before delete on wrijving begin select raise(abort,'wrijving: nooit verwijderen'); end;
create trigger if not exists t_vraag_geen_delete before delete on open_vraag begin select raise(abort,'open_vraag: nooit verwijderen'); end;
create trigger if not exists t_regel_geen_delete before delete on regel begin select raise(abort,'regel: nooit verwijderen; zet status op vervallen'); end;
create trigger if not exists t_boog_geen_delete before delete on boog begin select raise(abort,'boog: nooit verwijderen'); end;
create trigger if not exists t_personage_geen_delete before delete on personage begin select raise(abort,'personage: nooit verwijderen'); end;
create trigger if not exists t_zaadje_geen_delete before delete on zaadje begin select raise(abort,'zaadje: nooit verwijderen'); end;
create trigger if not exists t_canon_status_i before insert on canon when new.status not in('vastgesteld','voorlopig','voorlopig, vervangen','vervallen') begin select raise(abort,'ongeldige status'); end;
create trigger if not exists t_canon_status_u before update of status on canon when new.status not in('vastgesteld','voorlopig','voorlopig, vervangen','vervallen') begin select raise(abort,'ongeldige status'); end;
create trigger if not exists t_canon_dk_i before insert on canon when (new.draagkracht is not null and new.draagkracht not in('Kern','Structuur','Kleur')) or (new.draagkracht_handmatig is not null and new.draagkracht_handmatig not in('Kern','Structuur','Kleur')) begin select raise(abort,'ongeldige draagkracht'); end;
create trigger if not exists t_canon_dk_u before update of draagkracht,draagkracht_handmatig on canon when (new.draagkracht is not null and new.draagkracht not in('Kern','Structuur','Kleur')) or (new.draagkracht_handmatig is not null and new.draagkracht_handmatig not in('Kern','Structuur','Kleur')) begin select raise(abort,'ongeldige draagkracht'); end;
create trigger if not exists t_canon_vd_i before insert on canon when new.vervangen_door is not null and not exists(select 1 from canon where code=new.vervangen_door) begin select raise(abort,'vervangen_door bestaat niet'); end;
create trigger if not exists t_canon_vd_u before update of vervangen_door on canon when new.vervangen_door is not null and not exists(select 1 from canon where code=new.vervangen_door) begin select raise(abort,'vervangen_door bestaat niet'); end;
create trigger if not exists t_regel_status before insert on regel when new.status not in('actief','signaal','voorstel','vervallen') begin select raise(abort,'regel: status actief/signaal/voorstel/vervallen'); end;
""")
