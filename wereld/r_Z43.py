# Ronde Z43: mytheplan M0-M5. Alle aardse mythen krijgen een oorsprong in Velmara, als VOORSTEL in de ideeënbank.
# Bron: mythen/clusters.yaml (61 clusters, 300 voorbeelden), mythen/mythen.db (8.838 Wikidata-entiteiten, CC0), mythen/koppeling.md
# (de data kiest de canonrijen), mythen/oorsprong.yaml (59 oorsprongen met vervormingsketen). Niets wordt canon zonder besluit van Rogier.
# Idempotent en additief. Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 mythen/koppel.py && python3 mythen/toets_mythen.py
#   && python3 r_Z43.py && python3 velmara.py tekst && python3 velmara.py toets
import sqlite3, os, sys, collections, subprocess, yaml
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z43'; RN = 72; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); m = sqlite3.connect(os.path.join(W, 'mythen', 'mythen.db'))
S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
REDEN = 'Ronde Z43: mytheplan (architectuur/MYTHEPLAN.md), opdracht van Rogier 2026-11-02; voorstel van de architect, de koppeling gekozen door mythen/koppel.py'
EPI = 'voorstel (mytheplan M3, Z43)'
TIJD = {0: '0 Voortijd', 1: '1 Overvloed', 2: '2 Vonk', 3: '3 Brand', 4: '4 Noodtoestand', 5: '5 Ontvangst', 6: '6 Markt', 7: '7 Barsten', 8: '801 (nu)', 9: None}

def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z43.py')).rowcount

def lev(x):
    seen = set()
    while x and x not in seen:
        seen.add(x); r = c.execute('select status,vervangen_door from canon where code=?', (x,)).fetchone()
        if not r: return x
        st, vd = r
        if st in LEVEND or not vd: return x
        if vd.startswith('personage_profiel:'):
            y = vd.split(':', 1)[1]; return y if c.execute('select 1 from canon where code=?', (y,)).fetchone() else x
        x = vd.split(';')[0].strip()
    return x

def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:4]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

cl = {x['id']: x for x in yaml.safe_load(open('mythen/clusters.yaml'))}
oo = yaml.safe_load(open('mythen/oorsprong.yaml'))
for o in oo:
    code = 'MYTHE-Z43-' + o['cluster']; k = cl[o['cluster']]
    verw = ';'.join(dict.fromkeys(lev(x) for x in o['canon']))
    cu = m.execute('select culturen from cluster where id=?', (o['cluster'],)).fetchone()[0]
    sc = m.execute('select max(score) from koppel_score where cluster=?', (o['cluster'],)).fetchone()[0] or 0
    m.execute('insert or replace into oorsprong(cluster,laag,canon_codes,voorstel,score,status,regels,verlies,boek) values(?,?,?,?,?,?,?,?,?)',
              (o['cluster'], TIJD[o['laag']] or 'doorlopend', verw, code, sc, 'voorstel', ','.join(o['regels']), o['verlies'], o['boek']))
    for i, t in enumerate(o['keten'], 1):
        m.execute('insert or replace into vervorming(cluster,stap,eeuw,tekst,regel) values(?,?,?,?,?)',
                  (o['cluster'], i, ['Velmara', 'Midden-aarde en het zwevende gat', 'de aarde'][i - 1], t, ','.join(o['regels'])))
    if c.execute('select 1 from canon where code=?', (code,)).fetchone(): continue
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (code, 'Mythe', k['naam'], o['rij'], o['rij'], REDEN, 'voorlopig', RN, verw, verw, TIJD[o['laag']], 1, EPI))
             # herkenning, verlies en boek staan in mythen/oorsprong.yaml en mythen.db (context overleeft de roundtrip niet)
    S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
m.commit(); toets('mythen')
c.commit(); print(dict(S))
