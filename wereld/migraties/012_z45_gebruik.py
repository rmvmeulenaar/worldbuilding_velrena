"""Migratie 012 (ronde Z45: gebruik, gewone uitvindingen, kennis en verspreiding). Idempotent, additief.
Kolommen (gebruikt door de regels R-tech_gebruik, R-sim_effect en R-sim_convergentie in dezelfde ronde, en door de view v_tech_gebruik):
  tech_knoop:      gebruik, voor_wie, aards (waar het in onze wereld op lijkt), tijdperk, soort (magisch, magisch-arm, gewoon),
                   vervalt_bij (wanneer magische techniek verloren gaat), opvolger (wat haar plaats inneemt)
  sim_uitvinding:  probleem, druk_voor, druk_na (de druk van dat probleem bij de uitvinding en 100 jaar later), macht_voor, macht_na,
                   kennis (de kennisvoorraad bij de uitvinding), verspreid_jaar (gebruik boven 90%), verloren, verloren_door"""
VERSIE = 12; NAAM = 'z45_gebruik'

def _kol(c, t, k, ty='text'):
    if k not in [r[1] for r in c.execute(f'pragma table_info({t})')]: c.execute(f'alter table {t} add column {k} {ty}')

def migreer(c):
    if not c.execute("select 1 from sqlite_master where name='tech_knoop'").fetchone(): return
    for k in ('gebruik', 'voor_wie', 'aards', 'tijdperk', 'soort', 'vervalt_bij', 'opvolger'): _kol(c, 'tech_knoop', k)
    for k, ty in (('probleem', 'text'), ('druk_voor', 'real'), ('druk_na', 'real'), ('macht_voor', 'real'), ('macht_na', 'real'),
                  ('kennis', 'real'), ('verspreid_jaar', 'integer'), ('verloren', 'integer'), ('verloren_door', 'text')):
        _kol(c, 'sim_uitvinding', k, ty)
    c.executescript("""
drop view if exists v_tech_gebruik;
create view v_tech_gebruik as select code,naam,soort,tijdperk,gebruik,voor_wie,aards,vereist,opvolger,vervalt_bij from tech_knoop
  where status='mogelijk' order by case soort when 'magisch' then 1 when 'magisch-arm' then 2 else 3 end,tijdperk,code;
""")
