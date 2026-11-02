# Ronde Z51: besluit van Rogier op keuzelijst Z50 ("ja is goed", 2 november 2026) en de lijn naar het begin.
# 1. BESLUIT-Z51-1 (Kern). 2. De vier sjabloonrijen waar de Kern op leunt, krijgen hun opvolger uit z50/catalogus.yaml; de Kern-profielen van Liora
# en Aeron krijgen een opvolger waarin ALLEEN die codes naar de opvolgers wijzen (inhoud ongewijzigd); de ankers van Liora wijzen naar het nieuwe profiel.
# 3. Legende = zeldzaam, verdwenen een tijdperk later (afgeleid_motor.fantasie_tijd). 4. Lijn naar het begin: afgeleide tabel lijn_begin en regel
# R-lijn_naar_begin (signaal). Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z51.py && python3 velmara.py tekst && python3 velmara.py toets
import sqlite3, os, sys, collections, subprocess, yaml, re
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z51'; RN = 79; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter()
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z51.py')).rowcount
def bestaat(x): return c.execute('select 1 from canon where code=?', (x,)).fetchone() is not None
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

BES = ('Besluit van Rogier (2 november 2026, "ja is goed") op keuzelijst Z50. (1) De vier fantasieën VOOR-teder, VOOR-overgave, VOOR-onderdanige-man en '
       'VOOR-vrouwenliefde krijgen hun herschreven opvolger; de profielen van Liora en Aeron wijzen naar die opvolgers, en verder verandert er niets aan hen. '
       '(2) Sef van Brakhaven is een vrouw, zoals in haar personage. (3) Legende betekent zeldzaam: wat in een tijdperk legende wordt, is pas een tijdperk later weg. '
       '(4) De Grauwen en de Vathren verdwijnen; dat verlies is het verhaal. (5) In fase 16 mogen verhalen op echte plekken en in echte jaren spelen, met motieven, '
       'zonder echte personen en zonder levende godsdiensten als product van Velmara. Daarnaast vroeg Rogier dat in alle fasen het lijntje naar het begin terug te halen is: '
       'zie de afgeleide tabel lijn_begin en de regel R-lijn_naar_begin.')
def stap_besluit():
    if bestaat('BESLUIT-Z51-1'): return
    v = 'BESLUIT-Z12-2;ORIGIN-1'
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,draagkracht_handmatig,tijdperk,ideeenbank,epistemiek,besloten_door,besloten_op) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              ('BESLUIT-Z51-1', 'Besluit', 'Keuzelijst Z50: herschrijven, Sef, legende, verdwijnen, fase 16', BES, BES, 'Ronde Z51: besluit van Rogier', 'vastgesteld', RN, v, v, 'Kern', None, 0,
               'feit (besluit van Rogier, 2026-11-02)', 'Rogier', DT))
    S['besluit'] += 1; wijz('BESLUIT-Z51-1', 'toegevoegd', 'canon', None, 'vastgesteld')

VIER = ['VOOR-teder', 'VOOR-overgave', 'VOOR-onderdanige-man', 'VOOR-vrouwenliefde']
def stap_herschrijf():
    nieuw = {x['code']: ' '.join(x['nieuw'].split()) for x in yaml.safe_load(open('z50/catalogus.yaml')) if x['code'] in VIER}
    for oud in VIER:
        nc = oud + '-Z50'
        r = c.execute("select categorie,onderwerp,status,tijdperk,verwijst_naar,hangt_samen_met,draagkracht_handmatig,ideeenbank,epistemiek from canon where code=? and status in ('vastgesteld','voorlopig')", (oud,)).fetchone()
        if not r or bestaat(nc): continue
        c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,draagkracht_handmatig,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (nc, r[0], r[1], nieuw[oud], nieuw[oud], 'Ronde Z51: zelfde inhoud, eigen vorm (BESLUIT-Z51-1)', r[2], RN, r[4], r[5], r[3], r[6], r[7] or 0, r[8] or 'feit (herschreven in Z50, inhoud gelijk)'))
        c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=?", (nc, oud))
        S['herschreven'] += 1; wijz(nc, 'toegevoegd', 'canon', None, r[2]); wijz(oud, 'vervangen', 'status', r[2], 'voorlopig, vervangen (door ' + nc + ')')
    # Kern-profielen: alleen de codes naar de opvolgers
    for oud in ['PER-aeron-profiel', 'PER-liora-profiel-Z32']:
        nc = oud + '-Z51'
        r = c.execute("select categorie,onderwerp,feit,status,tijdperk,verwijst_naar,hangt_samen_met,draagkracht_handmatig,ideeenbank,epistemiek,reden from canon where code=? and status in ('vastgesteld','voorlopig')", (oud,)).fetchone()
        if not r or bestaat(nc): continue
        f, vn, hs = r[2], r[5] or '', r[6] or ''
        for x in VIER:
            f = re.sub(r'\b' + re.escape(x) + r'\b(?!-Z50)', x + '-Z50', f); vn = re.sub(r'\b' + re.escape(x) + r'\b(?!-Z50)', x + '-Z50', vn); hs = re.sub(r'\b' + re.escape(x) + r'\b(?!-Z50)', x + '-Z50', hs)
        vn = ';'.join(dict.fromkeys([y for y in vn.split(';') if y] + ['BESLUIT-Z51-1']))
        c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,draagkracht_handmatig,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (nc, r[0], r[1], f, f, (r[10] or '') + ' | Z51: codes van de vier fantasieën wijzen naar hun opvolgers (BESLUIT-Z51-1)', r[3], RN, vn, hs, r[4], 'Kern', r[8] or 0, r[9] or 'feit (canon; Z51: alleen codes bijgewerkt, BESLUIT-Z51-1)'))
        for t, d in c.execute('select toets,detail from toets_uitzondering where code=?', (oud,)).fetchall():  # dezelfde bekende uitzonderingen, nu onder de nieuwe code
            cols = [x[1] for x in c.execute('pragma table_info(toets_uitzondering)') if x[1] != 'id']
            row = dict(zip(cols, c.execute(f"select {','.join(cols)} from toets_uitzondering where code=? and toets=? and detail=?", (oud, t, d)).fetchone()))
            row['code'] = nc
            c.execute(f"insert or ignore into toets_uitzondering({','.join(cols)}) values({','.join('?' * len(cols))})", [row[k] for k in cols]); S['uitzondering_overgezet'] += 1
        c.execute("update canon set status='voorlopig, vervangen',vervangen_door=?,draagkracht_handmatig=null where code=?", (nc, oud))
        if r[7]: wijz(oud, 'gewijzigd', 'draagkracht_handmatig', r[7], 'leeg (Kern zit nu in ' + nc + ')')
        S['kern_profiel'] += 1; wijz(nc, 'toegevoegd', 'canon', None, r[3]); wijz(oud, 'vervangen', 'status', r[3], 'voorlopig, vervangen (door ' + nc + ', BESLUIT-Z51-1)')
        for (sl,) in c.execute('select sleutel from anker where bron_code=?', (oud,)).fetchall():
            c.execute('update anker set bron_code=? where sleutel=?', (nc, sl)); wijz('ANKER-' + sl, 'gewijzigd', 'anker.bron_code', oud, nc); S['anker'] += 1
    toets('herschrijf')

def stap_lijn():
    if not c.execute("select 1 from regel where code='R-lijn_naar_begin'").fetchone():
        c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
                  ('R-lijn_naar_begin', 'tijd', 'Een verhaal, persoon of verhaalpad zonder keten van links naar de Voortijd (BESLUIT-Z51-1: in alle fasen het lijntje terug naar het begin).',
                   "select code,'geen lijn naar het begin ('||soort||', fase '||coalesce(fase,'?')||')' from lijn_begin where stappen is null",
                   'Z51 (afgeleid_motor.lijn_naar_begin)', 'Rogier, BESLUIT-Z51-1 (signaal)', 'actief', 'signaal'))
        S['regel'] += 1; wijz('R-lijn_naar_begin', 'toegevoegd', 'regel', None, 'actief (signaal)')
    toets('lijn')
for s in (sys.argv[1:] or ['besluit', 'herschrijf', 'lijn']): globals()['stap_' + s]()
c.commit(); print(dict(S))
print(c.execute('select sum(stappen is not null),count(*),round(avg(stappen),1),max(stappen) from lijn_begin').fetchone())
