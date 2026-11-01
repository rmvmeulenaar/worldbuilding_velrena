"""Z39 11d.3: tien vragen over de gesimuleerde fase 4, alleen uit de views beantwoord; daarna vergeleken met een directe telling in de tabellen."""
import sqlite3,sys,os
c=sqlite3.connect(os.environ.get('DB','canon.db'));q=lambda s,*a:c.execute(s,a).fetchall()
V=[
('Hoeveel runs zijn er in fase 4 gedraaid (module personen), en hoeveel weggegooid?',
 lambda:q("select runs,weggegooid from v_sim_fase where module='personen' and fase_nr=4")[0],
 lambda:q("select count(*),sum(1-geldig) from sim_run where module='personen' and fase_nr=4")[0]),
('Hoeveel runs zonder Kernbescherming werden weggegooid?',
 lambda:q("select weggegooid from v_sim_fase where module='personen_zonder_kernbescherming'")[0][0],
 lambda:q("select sum(1-geldig) from sim_run where module='personen_zonder_kernbescherming'")[0][0]),
('Welke run staat bovenaan de storyteller (fase 4)?',
 lambda:q("select run_id from v_sim_top where module='personen' and fase_nr=4 order by pareto_rang,gewogen desc limit 1")[0][0],
 lambda:q("select run_id from sim_run where module='personen' and fase_nr=4 and gekozen=1 order by pareto_rang,gewogen desc limit 1")[0][0]),
('Wie weet in jaar 40 het geheim van Saske Registerhoofd?',
 lambda:sorted(x for (x,) in q("select naam from v_sim_wie_weet where weet_code='PER-f4-saske#geheim' and sinds_jaar<=40")),
 lambda:sorted(x for (x,) in q("select coalesce(p.naam,f.naam) from kennis k left join personage_profiel p on p.code=k.per_code left join sim_figuur f on f.code=k.per_code where weet_code='PER-f4-saske#geheim' and sinds_jaar<=40"))),
('Waar is Ylva Kustroofster in jaar 30?',
 lambda:q("select plek_code from v_sim_waar where per_code='PER-f4-ylva' and van_jaar<=30 and (tot_jaar is null or tot_jaar>=30) order by van_jaar desc limit 1"),
 lambda:q("select plek_code from verblijf where per_code='PER-f4-ylva' and van_jaar<=30 and (tot_jaar is null or tot_jaar>=30) order by van_jaar desc limit 1")),
('In hoeveel van de bewaarde runs ontstaat de Deelwet, en wanneer het vroegst?',
 lambda:q("select runs,vroegst from v_sim_validatie where canon_code='GEB-deelwet-40' and module='personen'")[0],
 lambda:q("select count(distinct run_id),min(jaar) from sim_gebeurtenis where canon_code='GEB-deelwet-40' and module='personen'")[0]),
('Hoeveel achtergrondfiguren heeft de simulatie gemaakt?',
 lambda:q("select count(*) from v_personage_laag where bron='sim_figuur'")[0][0],
 lambda:q("select count(*) from sim_figuur")[0][0]),
('Hoeveel fase-4-personages zijn hoofdpersonage (laag hoofd)?',
 lambda:q("select count(*) from v_personage_laag where fase_nr=4 and laag='hoofd' and bron='personage_profiel'")[0][0],
 lambda:q("select count(*) from personage_profiel p where fase_nr=4 and exists(select 1 from personage h where h.per_code=p.code or h.code=p.code)")[0][0]),
('In welk jaar verschijnt het eerste register het vroegst in de bewaarde runs?',
 lambda:q("select vroegst from v_sim_validatie where canon_code='GEB-r10-eerste-register' and module='personen'")[0][0],
 lambda:q("select min(jaar) from sim_gebeurtenis where canon_code='GEB-r10-eerste-register' and module='personen'")[0][0]),
('Hoeveel technologie-runs zijn geldig?',
 lambda:q("select geldig from v_sim_fase where module='technologie'")[0][0],
 lambda:q("select sum(geldig) from sim_run where module='technologie'")[0][0]),
]
goed=0
for v,a,b in V:
  x,y=a(),b();ok=x==y;goed+=ok
  print(f"{'GOED' if ok else 'FOUT'} | {v} | view: {x} | tabel: {y}")
print(f'{goed}/10')
