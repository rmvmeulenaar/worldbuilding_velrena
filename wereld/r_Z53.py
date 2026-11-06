# Ronde Z53: gewone taal. Rogier (6 november 2026): "het hoeft niet expliciet te zijn... maar die hoofse taal vind ik geen goed taalgebruik."
# Maat: architectuur/TOON_VLEES_EN_BLOED.md, sectie Taal. Bron: z53/herschreven_A/B/C.yaml (door schrijvers, uit z53/werk_*.json).
# Per herschreven premisse komt er een opvolger in verhaal_profiel (code + '-Z53', verder dezelfde rij); de oude krijgt status 'vervangen',
# vervangen_door en uitslag 'herschreven'. Plus regel R-premisse_hoofs (signaal). Toetsen vooraf: code leeft, lengte <= 600, "donker thema" blijft
# staan bij dwang, namen (woorden met hoofdletter) uit de oude premisse blijven staan. Daarna toets.py.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z53.py && python3 velmara.py tekst && python3 velmara.py toets && python3 velmara.py kaart
import sqlite3, os, sys, collections, subprocess, yaml, re
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-06'; RD = 'Z53'; RN = 81; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter()
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z53.py')).rowcount
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-7000:]); sys.exit(f'toets faalt na {stap}')
NAAM = re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿû'-]{2,}")
GEWOON = {'De', 'Het', 'Een', 'Ze', 'Hij', 'Zij', 'In', 'Op', 'Als', 'Wat', 'Wie', 'Dat', 'Die', 'Daar', 'Dan', 'Maar', 'En', 'Om', 'Na', 'Bij', 'Voor', 'Tot', 'Zo', 'Elke', 'Elk',
          'Twee', 'Drie', 'Vier', 'Niemand', 'Haar', 'Zijn', 'Hun', 'Aan', 'Uit', 'Met', 'Door', 'Toen', 'Nu', 'Ook', 'Er', 'Waar', 'Omdat', 'Terwijl', 'Pas', 'Sinds', 'Zonder'}
def stap_herschrijf():
    cols = [x[1] for x in c.execute('pragma table_info(verhaal_profiel)') if x[1] != 'id']
    for k in 'ABC':
        pad = f'z53/herschreven_{k}.yaml'
        if not os.path.exists(pad): sys.exit('ontbreekt ' + pad)
        for item in yaml.safe_load(open(pad)) or []:
            oud = item['code']; nw = ' '.join(str(item['premisse']).split()); nc = oud + '-Z53'
            if c.execute('select 1 from verhaal_profiel where code=?', (nc,)).fetchone(): continue
            r = c.execute(f"select {','.join(cols)} from verhaal_profiel where code=? and coalesce(vervangen_door,'')='' and status='voorlopig'", (oud,)).fetchone()
            if not r: sys.exit(f'{oud}: bestaat niet of is al vervangen')
            row = dict(zip(cols, r))
            if nw == ' '.join((row['premisse'] or '').split()): S['gelijk'] += 1; continue
            if len(nw) > 600: sys.exit(f'{oud}: premisse langer dan 600 tekens')
            if (row['dwang_label'] or 'donker thema' in row['premisse']) and 'donker thema' not in nw: sys.exit(f'{oud}: label donker thema verdwenen')
            weg = {n for n in NAAM.findall(row['premisse']) if n not in GEWOON} - set(NAAM.findall(nw))
            weg = {n for n in weg if n.lower() not in nw.lower()}
            if weg: S['naam_weg'] += 1; print(f'let op {oud}: woorden met hoofdletter weg: {sorted(weg)}')
            row.update(code=nc, premisse=nw, reden=(row['reden'] or '') + ' | Z53: zelfde pad in gewone taal (TOON_VLEES_EN_BLOED.md, Taal)')
            c.execute(f"insert into verhaal_profiel({','.join(cols)}) values({','.join('?' * len(cols))})", [row[x] for x in cols])
            c.execute("update verhaal_profiel set status='vervangen',vervangen_door=?,uitslag=case when uitslag in ('voorgesteld','ent-klaar') then 'herschreven' else uitslag end where code=?", (nc, oud))
            S['herschreven'] += 1; wijz(nc, 'toegevoegd', 'verhaal_profiel', None, 'voorlopig'); wijz(oud, 'vervangen', 'verhaal_profiel.status', 'voorlopig', 'vervangen (door ' + nc + ')')
    toets('herschrijf')
HOOFS = ["% een nacht met %", "% de nacht met %", "% zich geeft%", "% zich aan hem geeft%", "% bemin%", "% proeft hem%", "% proeft haar%", "% neemt haar op%", "% het bed deelt%",
         "% het bed delen%", "%huid onthoudt%", "%lichaam onthoudt%", "%lichaam vertelt%", "%huid vertelt%", "% zijn gunst %", "% haar gunst %"]
def stap_regel():
    if c.execute("select 1 from regel where code='R-premisse_hoofs'").fetchone(): return
    w = ' or '.join(f"lower(premisse) like '{p}'" for p in HOOFS)
    c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
              ('R-premisse_hoofs', 'taal', 'Een levende premisse met hoofse of lyrische omschrijving van seks ("een nacht met", "zich geven", "beminnen", "de huid onthoudt"); zeg het gewoon (TOON_VLEES_EN_BLOED.md, Taal).',
               f"select code,'hoofse taal in premisse' from verhaal_profiel where coalesce(vervangen_door,'')='' and status='voorlopig' and ({w})",
               'Z53 (Rogier, 6 november 2026)', 'Rogier (opdracht Z53, signaal)', 'actief', 'signaal'))
    S['regel'] += 1; wijz('R-premisse_hoofs', 'toegevoegd', 'regel', None, 'actief (signaal)')
    toets('regel')
for s in (sys.argv[1:] or ['herschrijf', 'regel']): globals()['stap_' + s]()
c.commit(); print(dict(S))
print('signaal hoofs:', c.execute(c.execute("select sql_test from regel where code='R-premisse_hoofs'").fetchone()[0]).fetchall())
