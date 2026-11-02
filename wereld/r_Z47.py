# Ronde Z47: de fantasie-matrix in de database, goed gemodelleerd (reactie op de vraag van Rogier, 2 november 2026: "hoe heb je dit gemodelleerd").
# Z46 zocht afhankelijkheden met zoekwoorden; dat gaf fouten (valparing zonder Skerra, tederheid die onmogelijk werd). Nu:
# - tijd/fantasie_afh.yaml: per fantasie de ECHTE afhankelijkheden (wat moet bestaan) en het verleden, door lezen van elke rij ingedeeld;
# - dit script zet die als links in verwijst_naar: naar de LOT-Z44-rij van het wezen of instituut (of GEB-Z45-losbandige-jaren voor het stalsysteem,
#   LOT-Z44-ishvar voor 'alleen gewone mensen') en naar de FASE-rij van het verleden. Geen tekst verandert; alleen links (gelogd in wijziging);
# - afgeleid_motor.fantasie_tijd() rekent daaruit fantasie_kern, fantasie_status en v_fantasie_matrix bij elke bouw;
# - nieuwe signaalregel R-fantasie_zonder_toekomst: een erotische fantasie zonder afhankelijkheid.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z47.py && python3 velmara.py tekst && python3 velmara.py toets && python3 tijd/fantasie.py
import sqlite3, os, sys, collections, subprocess, yaml
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z47'; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter()
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z47.py')).rowcount
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')
A = yaml.safe_load(open('tijd/fantasie_afh.yaml'))
for x in A:
    r = c.execute("select verwijst_naar,hangt_samen_met from canon where code=? and status in ('vastgesteld','voorlopig')", (x['code'],)).fetchone()
    if not r: print('niet levend of onbekend:', x['code']); continue
    if str(x.get('erotisch', 'ja')).lower() in ('nee', 'false'): S['niet_erotisch'] += 1; continue
    nieuw_ = [a for a in (x.get('hangt_af_van') or []) + ([x['verleden']] if x.get('verleden') else [])]
    for a in nieuw_:
        if not c.execute('select 1 from canon where code=?', (a,)).fetchone(): sys.exit(f"{x['code']}: anker {a} bestaat niet")
    for kol, oud in (('verwijst_naar', r[0]), ('hangt_samen_met', r[1])):
        lijst = [y for y in (oud or '').split(';') if y]
        erbij = [a for a in nieuw_ if a not in lijst]
        if not erbij: continue
        nw = ';'.join(lijst + erbij)
        c.execute(f'update canon set {kol}=? where code=?', (nw, x['code'])); wijz(x['code'], 'gewijzigd', kol, oud, nw); S[f'links_{kol}'] += len(erbij)
if not c.execute("select 1 from regel where code='R-fantasie_zonder_toekomst'").fetchone():
    c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
              ('R-fantasie_zonder_toekomst', 'tijd', 'Een erotische fantasie (VOOR-, KINK-, RIT-) zonder link naar een LOT-Z44-rij of GEB-Z45-losbandige-jaren: haar toekomst na 801 is onbekend.',
               "select code,'fantasie zonder toekomst: '||coalesce(naam,'') from fantasie_kern where afh is null",
               'Z47 (afgeleid_motor.fantasie_tijd)', 'architect Z47 (signaal)', 'actief', 'signaal'))
    S['regel_nieuw'] += 1; wijz('R-fantasie_zonder_toekomst', 'toegevoegd', 'regel', None, 'actief (signaal)')
toets('fantasie-links'); c.commit()
print(dict(S)); print(c.execute('select * from v_fantasie_matrix').fetchall())
