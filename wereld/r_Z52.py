# Ronde Z52: vlees en bloed. Meer seks, horror en intrige met de toon van Verhoeven (opdracht van Rogier, 6 november 2026).
# Ontwerp en criteria: architectuur/TOON_VLEES_EN_BLOED.md. Bronnen: z52/paden_A.yaml (fase 0-4), _B (5 t/m 801), _C (9-16), door schrijvers gemaakt,
# hier getoetst en ingelezen: personen (nieuw: PER-Z52-*, ideeënbank) en verhaalpaden (verhaal_profiel, run Z52). Toetsen vooraf: codes bestaan en leven,
# leeftijd >= 18, minstens 3 van 7 assen verschillend per tijdperk, minstens 4 toon-criteria en twee van erotiek/horror/intrige >= 4; daarna toets.py.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z52.py && python3 velmara.py tekst && python3 velmara.py toets && python3 velmara.py kaart
import sqlite3, os, sys, collections, subprocess, hashlib, yaml, re
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-06'; RD = 'Z52'; RN = 80; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
FASE_LABEL = {r[0]: r[0] for r in c.execute('select distinct fase from verhaal_profiel')}
NR = {f.split(' ')[0]: f for f in FASE_LABEL}
FASEROW = dict(c.execute("select cast(fase as text),code from tijdas").fetchall())
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z52.py')).rowcount
def levend(x):  # ook personages die naar personage_profiel zijn omgezet (BESLUIT Z37 D2) tellen als bestaand
    return c.execute("select 1 from canon where code=? and (status in ('vastgesteld','voorlopig') or vervangen_door like 'personage_profiel:%')", (x,)).fetchone() is not None
def bestaat(x): return c.execute('select 1 from canon where code=?', (x,)).fetchone() is not None
def lev(x):
    seen = set()
    while x and x not in seen:
        seen.add(x); r = c.execute('select status,vervangen_door from canon where code=?', (x,)).fetchone()
        if not r: return x
        st, vd = r
        if st in LEVEND or not vd or vd.startswith('personage_profiel:'): return x
        x = vd.split(';')[0].strip()
    return x
def fase_str(x):
    x = str(x).strip()
    return FASE_LABEL.get(x) or NR.get(x.split(' ')[0]) or sys.exit(f'onbekende fase {x}')
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-7000:]); sys.exit(f'toets faalt na {stap}')
def zin_persoon(p):
    zij = 'Ze' if p.get('geslacht', 'v') == 'v' else 'Hij'
    a = f"{p['naam']} ({p['volk']}, {p['regio']}) is geboren rond jaar {p['geboren']} en is {p['rol']}."
    b = f"{zij} wil {str(p['wil']).rstrip('.')}."
    g = f"Wat niemand weet, is dat {str(p['geheim']).rstrip('.')}."
    pr = str(p['prijs']).rstrip('.'); k = f"Het kost {pr[0].lower() + pr[1:]}."
    v = 'Uit de lijn van ' + ', '.join(p.get('afstamming') or []) + '.'
    orde = [[a, b, g, k, v], [a, g, b, k, v], [a, b, k, g, v], [a, k, b, g, v]][int(hashlib.sha1(p['code'].encode()).hexdigest(), 16) % 4]
    return ' '.join(orde)
def voeg_persoon(p, fase):
    if bestaat(p['code']): return
    f = fase.split(' ')[0]
    fr = FASEROW.get(f if f != '801' else '8')
    refs = [lev(x) for x in (p.get('afstamming') or []) + (p.get('verbonden_met') or []) if bestaat(x)] + ([fr] if fr and bestaat(fr) else [])
    v = ';'.join(dict.fromkeys(refs)); t = zin_persoon(p)
    tp = {'0': '0 Voortijd', '1': '1 Overvloed', '2': '2 Vonk', '3': '3 Brand', '4': '4 Noodtoestand', '5': '5 Ontvangst', '6': '6 Markt', '7': '7 Barsten', '801': '801 (nu)'}.get(f, fase)
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (p['code'], 'Personage', p['naam'], t, t, 'Ronde Z52: persoon in een vlees-en-bloedpad', 'voorlopig', RN, v, v, tp, 1, 'voorstel (Z52, persoon)'))
    S['persoon_nieuw'] += 1; wijz(p['code'], 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
ASSEN = lambda r: [r['positie'], r['genre'], r['schaal'], r['volk'], r['vorm'], r['afloop'], r['hoofdpersoon']]
G = ['g_romance', 'g_erotiek', 'g_horror', 'g_suspense', 'g_actie', 'g_intrige', 'g_komedie', 'g_tragiek']
def wereldregel(volk, fase):
    if '(na 801)' in fase: return 'BESLUIT-Z12-2'
    r = c.execute("select code from canon where code like ? and status in ('vastgesteld','voorlopig') order by code limit 1", ('SEKS-VOLK-' + volk.replace('û', 'u').replace('-', '') + '%',)).fetchone()
    return r[0] if r else 'REGEL-harde-grenzen'
def voeg_pad(p, bron):
    fase = fase_str(p['fase']); hp = f"{p['hp']['band']}|{p['hp']['geslacht']}"
    r = dict(positie=p['positie'], genre=p['genre'], schaal=p['schaal'], volk=p['volk'], vorm=p['vorm'], afloop=p['afloop'], hoofdpersoon=hp)
    cols0 = [x[1] for x in c.execute('pragma table_info(verhaal_profiel)')]
    for b in [dict(zip(cols0, x)) for x in c.execute("select * from verhaal_profiel where fase=? and coalesce(vervangen_door,'')=''", (fase,))]:
        if sum(1 for x, y in zip(ASSEN(r), ASSEN(b)) if x != y) < 3: S['te_dichtbij'] += 1; print('te dichtbij:', p['persoon'], b['code']); return
    g = [int(x) for x in p['gewichten']]
    if int(p['hp']['leeftijd']) < 18: sys.exit('leeftijd < 18')
    if len(p.get('toon') or []) < 4 or sum(1 for i in (1, 2, 5) if g[i] >= 4) < 2: S['toon_te_zwak'] += 1; print('toon te zwak:', p['persoon']); return
    kern = [lev(x) for x in (p.get('fantasieen') or []) + ([p['drager']] if p.get('drager') else []) + (p.get('kern') or [])]
    pers = lev(p['persoon'])
    for x in kern + [pers]:
        if not levend(x): sys.exit(f"{p['persoon']}: {x} bestaat niet of leeft niet")
    code = 'VP-' + fase.split(' ')[0] + '-' + hashlib.sha1((pers + p['premisse']).encode()).hexdigest()[:8]
    if c.execute('select 1 from verhaal_profiel where code=?', (code,)).fetchone(): return
    dwang = 1 if 'donker thema' in p['premisse'] else 0
    cols = ['code', 'run', 'fase', 'positie', 'genre', 'schaal', 'volk', 'vorm', 'afloop', 'hoofdpersoon', 'leeftijd', 'geslacht', 'partner', 'instemming', 'dwang_label'] + G + \
           ['wereldregel_code', 'kern_codes', 'herkomst', 'status', 'ideeenbank', 'drager', 'premisse', 'premisse_codes', 'reden']
    v = [code, 'Z52', fase, p['positie'], p['genre'], p['schaal'], p['volk'], p['vorm'], p['afloop'], hp, int(p['hp']['leeftijd']), p['hp']['geslacht'], 'volwassene', 'ja', dwang] + g + \
        [wereldregel(p['volk'], fase), ';'.join(dict.fromkeys(kern + [pers])), bron, 'voorlopig', 1, pers, ' '.join(p['premisse'].split()), ';'.join(dict.fromkeys(kern)),
         'Ronde Z52: toon vlees en bloed (criteria ' + ','.join(str(x) for x in p['toon']) + '); architectuur/TOON_VLEES_EN_BLOED.md']
    c.execute(f"insert into verhaal_profiel({','.join(cols)}) values({','.join('?' * len(cols))})", v); S['pad_nieuw'] += 1
    wijz(code, 'toegevoegd', 'verhaal_profiel', None, 'voorlopig')
alle = []
for k in 'ABC':
    pad = f'z52/paden_{k}.yaml'
    if not os.path.exists(pad): print('ontbreekt', pad); continue
    alle.append((k, yaml.safe_load(open(pad))))
for k, d in alle:
    fase_van = {}
    for x in d['paden']: fase_van.setdefault(x['persoon'], fase_str(x['fase']))
    for p in d.get('personen') or []:
        p = dict(p); p.setdefault('geslacht', next((x['hp']['geslacht'] for x in d['paden'] if x['persoon'] == p['code']), 'v'))
        voeg_persoon(p, fase_van.get(p['code']) or fase_str(p.get('tijdperk', 9)))
for k, d in alle:
    for p in d.get('personen') or []:
        r = c.execute('select verwijst_naar from canon where code=?', (p['code'],)).fetchone()
        if not r: continue
        refs = [lev(x) for x in (p.get('afstamming') or []) + (p.get('verbonden_met') or []) if bestaat(x)]
        nw = ';'.join(dict.fromkeys([y for y in (r[0] or '').split(';') if y] + refs))
        if nw != r[0]: c.execute('update canon set verwijst_naar=?,hangt_samen_met=? where code=?', (nw, nw, p['code']))
for k, d in alle:
    for x in d['paden']: voeg_pad(x, f'schrijver {k} (Z52, vlees en bloed)')
toets('vlees en bloed'); c.commit(); print(dict(S))
