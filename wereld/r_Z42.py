# Ronde Z42: het materiaal van de Makers (BESLUIT-Z42-1, besluit van Rogier op 2026-11-02).
# Een vreemd schip op een gewone wereld: siliciumtechniek, gewone schimmel die de legering eet, geen erts bij de landing,
# ijzer later uit de bergen, magie als Makerstechniek. De roman verandert niet.
# Idempotent en additief: niets verwijderd; oude rijen worden 'voorlopig, vervangen' met opvolger; Kern alleen via de BESLUIT-rij.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z42.py && python3 velmara.py tekst && python3 velmara.py toets
import sqlite3, os, re, sys, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z42'; RN = 71; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
REDEN = 'Ronde Z42: besluit van Rogier (2026-11-02) op voorstel van de architect (architect/besluitvoorstel_Z42_materiaal.md)'
LEVEND = ('vastgesteld', 'voorlopig')
LABEL = (" Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; "
         "nooit seks met wie echt niet kan instemmen; donkere thema's gelabeld.")

def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z42.py')).rowcount

def lev(x):
    seen = set()
    while x and x not in seen:
        seen.add(x)
        r = c.execute('select status,vervangen_door from canon where code=?', (x,)).fetchone()
        if not r: return x
        st, vd = r
        if st in LEVEND or not vd: return x
        if vd.startswith('personage_profiel:'):
            y = vd.split(':', 1)[1]
            return y if c.execute('select 1 from canon where code=?', (y,)).fetchone() else x
        x = vd.split(';')[0].strip()
    return x

def bestaat(code): return c.execute('select 1 from canon where code=?', (code,)).fetchone() is not None

def nieuw(code, cat, ond, feit, verw, status='vastgesteld', kern=False, tijdperk=None, epistemiek=None, ideeenbank=0):
    if bestaat(code): return 0
    verw = ';'.join(dict.fromkeys(lev(x) for x in verw.split(';') if x))
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,draagkracht_handmatig,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (code, cat, ond, feit, feit, REDEN, status, RN, verw, verw, 'Kern' if kern else None, tijdperk, ideeenbank, epistemiek))
    S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, status); return 1

def vervang(oud, door):
    r = c.execute("select status from canon where code=? and status in ('vastgesteld','voorlopig')", (oud,)).fetchone()
    if r and c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=?", (door, oud)).rowcount:
        S['canon_vervangen'] += 1; wijz(oud, 'vervangen', 'status', r[0], 'voorlopig, vervangen (door ' + door + ')')

def opvolger(oud, nc, feit, extra_verw='BESLUIT-Z42-1', kern=False, epistemiek='feit (canon, herschreven na BESLUIT-Z42-1)'):
    r = c.execute('select categorie,onderwerp,verwijst_naar,status,tijdperk from canon where code=?', (oud,)).fetchone()
    if not r: return
    nieuw(nc, r[0], r[1], feit, (r[2] or '') + ';' + extra_verw, status=r[3] if r[3] in LEVEND else 'voorlopig', kern=kern, tijdperk=r[4], epistemiek=epistemiek)
    vervang(oud, nc)

def feit_van(code): return c.execute('select feit from canon where code=?', (code,)).fetchone()[0]

def vervang_tekst(code, nc, paren, kern=False):
    f = feit_van(code)
    for a, b in paren:
        if a not in f: sys.exit(f'{code}: tekst niet gevonden: {a[:60]}')
        f = f.replace(a, b, 1)
    opvolger(code, nc, f, kern=kern)

def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:4]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

# ---------- 1. het besluit ----------
BESLUIT = ("Een vreemd schip op een gewone wereld. Besluit van Rogier (2 november 2026). De materiaaltechniek van de Makers is silicium: "
    "de romp is een legering van aluminium en silicium met siliciumcomposiet, kernen en rekenwerk draaien op siliciumkristal, en het hart van het schip "
    "is een grijs kristal dat breekt als glas. Silicium zit overal in zand en steen, maar zuiver silicium vraagt een vlamboogoven van rond de 2000 graden, "
    "en daarvoor is geen energie meer: de kernen raken op en er is geen brandstof. Gewone schimmel van deze wereld eet de legering; voor de kolonisten, "
    "die uit de steriele ruimte kwamen, heet ze Velmara-schimmel. Rond de landingsplek in de delta zit geen erts; gewoon ijzer komt later uit de bergen. "
    "Makersmateriaal overleeft alleen waar de schimmel niet komt: droog, koud, verzegeld, in zout of in de Leegte. Alle magie is Makerstechniek, die na 801 "
    "langzaam uitdooft. De romantekst verandert niet: hoofdstuk 2 (\"Metabolises alloy\", \"No easy metal near the surface\") en hoofdstuk 33 "
    "(\"a heart of grey stone\") blijven letterlijk waar.")

def stap_besluit():
    nieuw('BESLUIT-Z42-1', 'Techniek', 'Het materiaal van de Makers: silicium op een gewone wereld', BESLUIT,
          'ORIGIN-WAAROM-2;ORIGIN-4;YSA-Z17-6;TECHNO-REGEL-V4;TECHNO-metaal;TECHNO-zegelsteen;GEB-Z17-sterrensteen-inslag',
          kern=True, tijdperk='0 Voortijd', epistemiek='feit (besluit van Rogier, 2026-11-02)')
    toets('besluit')

# ---------- 2. de rijen die tegenspraken ----------
def stap_herschrijf():
    vervang_tekst('ORIGIN-WAAROM-2', 'ORIGIN-WAAROM-2-Z42', [
        ('(1) energietekort, de kernen raken op en Velmara heeft geen metaal of brandstof;',
         '(1) energietekort: de kernen raken op, er is geen brandstof, en rond de landingsplek in de delta zit geen makkelijk metaal; '
         'zuiver silicium, het materiaal van het schip, is zonder die energie niet uit zand te maken;'),
        ('(3) een roestschimmel van Velmara vreet scheepsmetaal aan.',
         '(3) gewone schimmel van deze wereld vreet de aluminium-siliciumlegering van het schip aan; voor de kolonisten heet ze Velmara-schimmel (BESLUIT-Z42-1).'),
    ], kern=True)
    vervang_tekst('YSA-Z17-6', 'YSA-Z17-6-Z42', [
        ("Dat is Ysa's klok.",
         "Dat is Ysa's klok. Het is gewone schimmel van deze wereld, die de kolonisten nooit eerder zagen: de ruimte was steriel, deze grond niet (BESLUIT-Z42-1)."),
    ])
    vervang_tekst('TECHNO-metaal', 'TECHNO-metaal-Z42', [
        ('Resten van vóór het Zegel en van buiten Velmara: metalen schepen, energiekernen en rekenmachines in de Orde-kluizen. Oorsprong buiten Velmara voorlopig en open (kolonieschip-hint).',
         'Resten van het zaaischip en zijn kluizen, uit de tijd van de Makers: siliciumkristal, aluminium-siliciumlegering, energiekernen en rekenwerk in de Orde-kluizen (BESLUIT-Z42-1).'),
        ('Onbekend metaal dat niet roest, glasvezel, kernen die warm blijven, schermen die oplichten.',
         'Kristal dat blijft, en een legering die de schimmel van deze wereld opeet, behalve in droge, koude, verzegelde kluizen, in zout en in de Leegte; glasvezel, kernen die warm blijven, schermen die oplichten.'),
        ('Energiekernen die eeuwen branden; niemand kan ze bijvullen.',
         'Energiekernen die eeuwen branden; niemand kan ze bijvullen, en nieuw kristal maken vraagt een hitte die niemand meer kan opwekken.'),
    ])
    vervang_tekst('TECHNO-REGEL-V4', 'TECHNO-REGEL-V4-Z42', [
        ('zegelsteen is de gevallen scheepskern (Wieg); metaal en machine zijn hoog ontwikkelde, vergeten techniek van het zaaischip Ysa die deels nog draait (kluizen, kernen, Wiegkast, Sterrensteen).',
         'zegelsteen is het gevallen siliciumhart van het schip (de Sterrensteen, de Wieg); het siliciumwerk van het zaaischip Ysa is hoog ontwikkelde, vergeten techniek die deels nog draait (kluizen, kernen, Wiegkast). '
         'Gewoon ijzer bestaat, maar niet bij de landing: het komt pas uit de bergen (BESLUIT-Z42-1).'),
    ])
    vervang_tekst('TECHNO-zegelsteen', 'TECHNO-zegelsteen-Z42', [
        ('Oorsprong: Afgeleid van de Sterrensteen van het Zegel:',
         'Oorsprong: Afgeleid van de Sterrensteen, het gevallen siliciumhart van het zaaischip (BESLUIT-Z42-1):'),
    ])
    opvolger('TECHNO-metaal-schip', 'TECHNO-metaal-schip-Z42',
             'De Kluisschepen: drie Leegteschepen van siliciumlegering. In de Leegte groeit geen schimmel, dus één vliegt nog, zonder dat iemand de koers kiest.')
    opvolger('TECHNO-metaal-bouw', 'TECHNO-metaal-bouw-Z42',
             'Torens van naadloos kristal en legering onder de Orde-kathedraal, droog en verzegeld. Waar de afdichting lekt, bloeit de schimmel in de naden.')
    # het besluit wijst naar de levende opvolgers, niet naar de vervangen rijen
    v = c.execute("select verwijst_naar from canon where code='BESLUIT-Z42-1'").fetchone()[0]
    nv = ';'.join(dict.fromkeys(lev(x) for x in v.split(';') if x))
    if nv != v:
        c.execute("update canon set verwijst_naar=?,hangt_samen_met=? where code='BESLUIT-Z42-1'", (nv, nv)); wijz('BESLUIT-Z42-1', 'gewijzigd', 'verwijst_naar', v, nv)
    toets('herschrijf')

# ---------- 3. het eerste ijzer (voorstel: jaar en plek open, vroegste fase volgens het besluit) ----------
def stap_ijzer():
    nieuw('GEB-Z42-eerste-ijzer', 'Geschiedenis', 'Het eerste ijzer',
          'In de bergen van Hoogvrouwe vinden Dhurn-mijnwerkers, nazaten van het volk van Corran, roodbruin gesteente dat in het vuur zacht wordt. '
          'Het is het eerste ijzer van deze wereld: zwaar, grof, en geen schimmel die het eet. Jaar open; de vroegste fase volgens BESLUIT-Z42-1 is de Overvloed. '
          'Voorstel uit Z42; wacht op een besluit van Rogier over jaar en plek.',
          'BESLUIT-Z42-1;VOLK-dhurn;REG-hoogvrouwe;FASE-overvloed', status='voorlopig', tijdperk='1 Overvloed',
          epistemiek='voorstel (architect Z42, geen besluit)', ideeenbank=1)
    toets('ijzer')

# ---------- 4. alle rijen met metaal indelen ----------
PAT = re.compile(r'\b(ijzer|ijzeren|zwaard|zwaarden|ketting|kettingen|kanonnen|kanonskogel|smid|smeden|smederij|staal|stalen|metaal|metalen)\b|kanon(?<!in kanon)|(?<!on)kruit', re.I)
MAKER = re.compile(r'Maker|schip|kluis|lander|Rekenaar|Reckoner|Wieg|kern|Sterrensteen|Leegteschip|zegelplaat|wrak|vóór 205|uit 205|Kluiswacht|Orde-kluis|machine|metaalpapier|metaal-oud', re.I)
KHARVOS = re.compile(r'Kharvos|Harrow|Hoornburg', re.I)
KRUIT = re.compile(r'kanon(?<!in kanon)|(?<!on)kruit|\bgeweer', re.I)
SCHIP_CODES = ('ORIGIN', 'YSA-', 'ROMAN-', 'TECHNO-metaal', 'TECH-ITEM', 'OORSPRONG-metaal', 'BESLUIT-Z30', 'BESLUIT-Z19', 'ROMANCE-Z15b', 'OORLOG-Z9-1')

def stap_indeling():
    rij = [r for r in c.execute("select code,tijdperk,draagkracht,feit from canon where status in ('vastgesteld','voorlopig') and ronde<?", (RN,)) if PAT.search(r[3] or '')]
    groep = collections.defaultdict(list)
    for code, tp, dk, feit in rij:
        f = feit or ''; tp = tp or ''
        if KRUIT.search(f) and not MAKER.search(f): g = 'wrijving: kruit en kanonnen'
        elif code.startswith(SCHIP_CODES) or MAKER.search(f): g = 'past: Makersmateriaal (overleeft alleen waar de schimmel niet komt)'
        elif KHARVOS.search(f): g = 'past: Kharvos (machines en ijzer van de Harrow)'
        elif tp.startswith('0'): g = 'wrijving: gewoon ijzer in de Voortijd'
        elif tp: g = 'past: gewoon ijzer na de ertsvondst'
        else: g = 'past: zonder fase (geldt vanaf de ertsvondst)'
        groep[g].append((code, tp, dk))
    # wrijvingen vastleggen (één per soort, met de rijen erbij), zodat Rogier ze ziet op de keuzelijst
    for g, rs in groep.items():
        if not g.startswith('wrijving'): continue
        wc = 'WRIJ-Z42-' + ('kruit' if 'kruit' in g else 'voortijd-ijzer')
        if c.execute('select 1 from wrijving where code=?', (wc,)).fetchone(): continue
        codes = ';'.join(r[0] for r in rs)
        besch = (f"{len(rs)} rij(en) botsen met BESLUIT-Z42-1: " + g.split(': ', 1)[1] + '. ' +
                 ('Kruit vraagt salpeter, zwavel en houtskool; dat kan zonder machinekracht, maar het is een grote stap in de techniek. Voorstel: kanonnen alleen in Kharvos, of vervangen door zegelglas-werptuigen.'
                  if 'kruit' in g else 'In de Voortijd is er geen erts; voorstel: het metaal is Makersmateriaal of wordt been, steen of zegelglas.'))
        c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",
                  ('Z42 materiaal: ' + g.split(': ', 1)[1], codes.replace(';', ', '), besch, 'canon', 'open', wc, 'BESLUIT-Z42-1;' + codes))
        S['wrijving_nieuw'] += 1; wijz(wc, 'toegevoegd', 'wrijving', None, 'open')
    with open('wijzigingen_Z42_indeling.md', 'w') as o:
        o.write('# Z42: indeling van alle rijen met metaal na BESLUIT-Z42-1\n\n')
        o.write(f'Gezocht op hele woorden: ijzer(en), zwaard(en), ketting(en), kanon(nen) (niet \"in kanon\" als zang), smid/smeden, staal/stalen, metaal/metalen, (bus)kruit. Levende rijen van vóór Z42: {len(rij)}.\n\n| Groep | Aantal |\n|---|---|\n')
        for g, rs in sorted(groep.items(), key=lambda kv: -len(kv[1])): o.write(f'| {g} | {len(rs)} |\n')
        for g, rs in sorted(groep.items()):
            o.write(f'\n## {g} ({len(rs)})\n\n' + '\n'.join(f'- `{cd}` ({tp or "zonder fase"}, {dk})' for cd, tp, dk in rs) + '\n')
    S['ingedeeld'] = len(rij)
    toets('indeling')

STAPPEN = sys.argv[1:] or ['besluit', 'herschrijf', 'ijzer', 'indeling']
for s in STAPPEN: globals()['stap_' + s]()
c.commit(); print(dict(S))
