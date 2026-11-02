# Ronde Z50: personen na 801, een verhaal voor elke fantasie, en de catalogus zonder sjablonen (opdracht van Rogier, 2 november 2026: "kan je dat gewoon maken").
# Bronnen (door schrijvers gemaakt, hier getoetst en ingelezen): z50/catalogus.yaml (144 herschreven catalogusrijen), z50/paden_A/B/C.yaml (verhaalpaden
# en personen voor fase 9-10, 11-13, 14-16). Daarnaast krijgen de 18 paden van Z49 een persoon.
# 1. catalogus: elke rij krijgt een opvolger <code>-Z50 met dezelfde inhoud in eigen vorm; verwijzingen in niet-Kern-rijen en verhaalpaden wijzen naar de opvolger.
# 2. personen: canonrijen PER-Z50-* (categorie Personage, ideeënbank, voorstel), gekoppeld aan huis/volk/voorouders en aan andere verhaallijnen.
# 3. paden: rijen in verhaal_profiel; drager = de persoon (zoals in de oudere paden), de DRAGER-rij staat in kern_codes.
# Toetsen vooraf: codes bestaan, leeftijd >= 18, 3 van 7 assen verschillend per tijdperk; daarna toets.py (premisse_vorm, harde lijnen, sjabloon).
import sqlite3, os, sys, collections, subprocess, hashlib, itertools, yaml, re
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z50'; RN = 78; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
T = {9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 12: '12 Het Vertrek (na 801)',
     13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)', 15: '15 Het Zwevende Gat (na 801)', 16: '16 Tijd van het Schrift (na 801)'}
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z50.py')).rowcount
def bestaat(x): return c.execute('select 1 from canon where code=?', (x,)).fetchone() is not None
def lev(x):
    seen = set()
    while x and x not in seen:
        seen.add(x); r = c.execute('select status,vervangen_door from canon where code=?', (x,)).fetchone()
        if not r: return x
        st, vd = r
        if st in LEVEND or not vd: return x
        if vd.startswith('personage_profiel:'): return x
        x = vd.split(';')[0].strip()
    return x
def is_kern(code):
    r = c.execute('select draagkracht,draagkracht_handmatig from canon where code=?', (code,)).fetchone()
    return bool(r) and 'Kern' in ((r[0] or '') + (r[1] or ''))
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-7000:]); sys.exit(f'toets faalt na {stap}')

# ---------- 1. catalogus zonder sjablonen ----------
def stap_catalogus():
    if not os.path.exists('z50/catalogus.yaml'): print('geen z50/catalogus.yaml'); return
    nieuw_van = {}
    for x in yaml.safe_load(open('z50/catalogus.yaml')):
        oud = x['code']; nc = oud + '-Z50'; nieuw_van[oud] = nc
        r = c.execute("select categorie,onderwerp,status,tijdperk,verwijst_naar,hangt_samen_met,draagkracht_handmatig,ideeenbank,epistemiek from canon where code=? and status in ('vastgesteld','voorlopig')", (oud,)).fetchone()
        if not r or bestaat(nc): continue
        tekst = ' '.join(x['nieuw'].split())
        c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,draagkracht_handmatig,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (nc, r[0], r[1], tekst, tekst, 'Ronde Z50: zelfde inhoud, eigen vorm (catalogus zonder sjablonen)', r[2], RN, r[4], r[5], r[3], r[6], r[7] or 0, r[8] or 'feit (herschreven in Z50, inhoud gelijk)'))
        c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=?", (nc, oud))
        S['catalogus_herschreven'] += 1; wijz(nc, 'toegevoegd', 'canon', None, r[2]); wijz(oud, 'vervangen', 'status', r[2], 'voorlopig, vervangen (door ' + nc + ')')
    # verwijzingen bijwerken (niet in Kern-rijen; die lossen op via lev())
    for code, vn, hs in c.execute("select code,verwijst_naar,hangt_samen_met from canon where status in ('vastgesteld','voorlopig') and (verwijst_naar is not null or hangt_samen_met is not null)").fetchall():
        if is_kern(code): continue
        for kol, oud in (('verwijst_naar', vn), ('hangt_samen_met', hs)):
            if not oud: continue
            lijst = [y.strip() for y in oud.split(';')]; nw = ';'.join(dict.fromkeys(nieuw_van.get(y, y) for y in lijst if y))
            if nw != oud: c.execute(f'update canon set {kol}=? where code=?', (nw, code)); wijz(code, 'gewijzigd', kol, oud, nw); S['link_bijgewerkt'] += 1
    for vid, code, k, p in c.execute("select id,code,kern_codes,premisse_codes from verhaal_profiel").fetchall():
        for kol, oud in (('kern_codes', k), ('premisse_codes', p)):
            if not oud: continue
            nw = ';'.join(nieuw_van.get(y, y) for y in oud.split(';'))
            if nw != oud: c.execute(f'update verhaal_profiel set {kol}=? where id=?', (nw, vid)); wijz(code, 'gewijzigd', 'verhaal_profiel.' + kol, oud, nw); S['pad_link_bijgewerkt'] += 1
    toets('catalogus')

# ---------- 2. personen ----------
def zin_persoon(p):
    zij = 'Ze' if p.get('geslacht', 'v') == 'v' else 'Hij'
    a = f"{p['naam']} ({p['volk']}, {p['regio']}) is geboren rond Zegeljaar {p['geboren']} en is {p['rol']}."
    b = f"{zij} wil {p['wil'].rstrip('.')}."
    g = f"Wat niemand weet: {p['geheim'].rstrip('.')}."
    k = f"Het kost {p['prijs'].rstrip('.')[0].lower() + p['prijs'].rstrip('.')[1:]}."
    v = 'Afkomst en lijnen: ' + ', '.join(p.get('afstamming') or []) + '.'
    orde = [[a, b, g, k, v], [a, g, b, k, v], [a, b, k, g, v], [a, k, b, g, v]][int(hashlib.sha1(p['code'].encode()).hexdigest(), 16) % 4]
    return ' '.join(orde).replace('Wat niemand weet: ', 'Wat niemand weet, is dat ').replace('Afkomst en lijnen: ', 'Uit de lijn van ')
def voeg_persoon(p, f):
    if bestaat(p['code']): return
    refs = [lev(x) for x in (p.get('afstamming') or []) + (p.get('verbonden_met') or []) if bestaat(x)]
    v = ';'.join(dict.fromkeys(refs + ['FASE-z44-' + {9: 'ja', 10: 'volken', 11: 'helden', 12: 'vertrek', 13: 'mensen', 14: 'smelt', 15: 'gat', 16: 'schrift'}[f]]))
    t = zin_persoon(p)
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (p['code'], 'Personage', p['naam'], t, t, 'Ronde Z50: persoon na 801, hoofdpersoon van een verhaalpad', 'voorlopig', RN, v, v, T[f], 1, 'voorstel (Z50, persoon na 801)'))
    S['persoon_nieuw'] += 1; wijz(p['code'], 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')

# ---------- 3. paden ----------
ASSEN = lambda r: [r['positie'], r['genre'], r['schaal'], r['volk'], r['vorm'], r['afloop'], r['hoofdpersoon']]
def bestaande_paden(fase):
    cols = [x[1] for x in c.execute('pragma table_info(verhaal_profiel)')]
    return [dict(zip(cols, r)) for r in c.execute("select * from verhaal_profiel where fase=? and coalesce(vervangen_door,'')=''", (fase,))]
G = ['g_romance', 'g_erotiek', 'g_horror', 'g_suspense', 'g_actie', 'g_intrige', 'g_komedie', 'g_tragiek']
def voeg_pad(p, bron):
    f = int(p['fase']); fase = T[f]
    hp = f"{p['hp']['band']}|{p['hp']['geslacht']}"
    r = dict(positie=p['positie'], genre=p['genre'], schaal=p['schaal'], volk=p['volk'], vorm=p['vorm'], afloop=p['afloop'], hoofdpersoon=hp)
    for b in bestaande_paden(fase):
        if sum(1 for x, y in zip(ASSEN(r), ASSEN(b)) if x != y) < 3: S['pad_te_dichtbij'] += 1; print('te dichtbij:', p['persoon'], b['code']); return
    if int(p['hp']['leeftijd']) < 18: sys.exit('leeftijd < 18')
    kern = [lev(x) for x in (p.get('fantasieen') or []) + ([p['drager']] if p.get('drager') else []) + (p.get('kern') or [])]
    for x in kern + [p['persoon']]:
        if not bestaat(x): sys.exit(f"{p['persoon']}: {x} bestaat niet")
    code = 'VP-' + str(f) + '-' + hashlib.sha1((p['persoon'] + p['premisse']).encode()).hexdigest()[:8]
    if c.execute('select 1 from verhaal_profiel where code=?', (code,)).fetchone(): return
    dwang = 1 if 'donker thema' in p['premisse'] else 0
    cols = ['code', 'run', 'fase', 'positie', 'genre', 'schaal', 'volk', 'vorm', 'afloop', 'hoofdpersoon', 'leeftijd', 'geslacht', 'partner', 'instemming', 'dwang_label'] + G + \
           ['wereldregel_code', 'kern_codes', 'herkomst', 'status', 'ideeenbank', 'drager', 'premisse', 'premisse_codes', 'reden']
    v = [code, 'Z50', fase, p['positie'], p['genre'], p['schaal'], p['volk'], p['vorm'], p['afloop'], hp, int(p['hp']['leeftijd']), p['hp']['geslacht'], 'volwassene', 'ja', dwang] + \
        [int(x) for x in p['gewichten']] + ['BESLUIT-Z12-2', ';'.join(dict.fromkeys(kern + [p['persoon']])), bron, 'voorlopig', 1, p['persoon'], ' '.join(p['premisse'].split()),
                                            ';'.join(dict.fromkeys(kern)), 'Ronde Z50: verhaalpad met persoon, maakt fantasieën na 801 mogelijk']
    c.execute(f"insert into verhaal_profiel({','.join(cols)}) values({','.join('?' * len(cols))})", v); S['pad_nieuw'] += 1
    wijz(code, 'toegevoegd', 'verhaal_profiel', None, 'voorlopig')
def stap_paden():
    for k in 'ABC':
        pad = f'z50/paden_{k}.yaml'
        if not os.path.exists(pad): print('ontbreekt', pad); continue
        d = yaml.safe_load(open(pad))
        tf = {}
        for x in d['paden']: tf.setdefault(x['persoon'], int(x['fase']))
        for p in d['personen']:
            p = dict(p); p.setdefault('geslacht', next((x['hp']['geslacht'] for x in d['paden'] if x['persoon'] == p['code']), 'v'))
            voeg_persoon(p, int(p.get('tijdperk') or tf.get(p['code'], 9)))
        for x in d['paden']: voeg_pad(x, f'schrijver {k} (Z50)')
    toets('paden')

# ---------- 4. de 18 paden van Z49 krijgen een persoon (drager = persoon, DRAGER-rij in kern_codes) ----------
Z49P = {
 'DRAGER-Z48-gave-9': dict(code='PER-Z50-merel-glas', naam='Merel van de Oude Weg', volk='mens', regio='Ambergaard', geboren=812, geslacht='v', rol='lampenmaakster die het gaveglas van haar moeder erft',
     wil='weten van wie de warmte in het glas komt', geheim='ze heeft het glas ooit zelf laten bijvullen', prijs='haar huwelijk, als ze kiest', afstamming=['VOLK-ishvar', 'GEB-Z45-losbandige-jaren'], verbonden_met=['VERHAAL-Z44-tijdperk-9']),
 'DRAGER-Z48-ontvangst-9': dict(code='PER-Z50-khaled-hoedster', naam='Iskan van Qesh', volk='ishvar', regio='Saelith', geboren=771, geslacht='m', rol='hoedster van de eerste Vrije Ontvangst',
     wil='een feest leiden zonder iemand te beschamen', geheim='hij heeft zelf nooit gekozen', prijs='zijn rust: iedereen wil nu met hem praten', afstamming=['VOLK-ishvar', 'HUI-qesh-Z6'], verbonden_met=['COMEDY-Z46-9-comedy']),
 'DRAGER-Z48-stal-9': dict(code='PER-Z50-tobin-spel', naam='Tobin Kademan', volk='mens', regio='Ambergaard', geboren=773, geslacht='m', rol='vrijgekomen stalman die in een Huis van Spel werkt',
     wil='zelf beslissen wat er van zijn verleden wordt gespeeld', geheim='hij kent de klant die het woord niet hoorde', prijs='de naam van het huis', afstamming=['GEB-Z45-losbandige-jaren', 'DAG-dag-man'], verbonden_met=['VERHAAL-Z45-losbandig', 'EROS-Z45-haak-1']),
 'DRAGER-Z48-vleugel-10': dict(code='PER-Z50-ilse-klif', naam='Ilse Klifdochter', volk='skerra', regio='Hoogvrouwe', geboren=1580, geslacht='v', rol='Skerra-dochter zonder vleugels met de zweefhuid van haar grootmoeder',
     wil='één keer vallen zoals haar voorouders', geheim='de huid is gescheurd en ze heeft hem zelf genaaid', prijs='één van hen landt niet veilig', afstamming=['VOLK-skerra', 'LOT-Z44-skerra'], verbonden_met=['HELD-Z46-10-held']),
 'DRAGER-Z48-vorm-10': dict(code='PER-Z50-wisselbloed', naam='Sanne Maanvoet', volk='ves-lethi', regio='Kharvos-grens', geboren=1600, geslacht='v', rol='vrouw met wisselbloed in een grensdorp',
     wil='niet meer verstoppen wat ze bij volle maan wordt', geheim='haar grootvader was een Ves-Lethi-spion', prijs='het vertrouwen van het dorp, eerst', afstamming=['VOLK-ves-lethi-Z6', 'LOT-Z44-ves-lethi'], verbonden_met=['HORROR-Z46-10-horror']),
 'DRAGER-Z48-korf-10': dict(code='PER-Z50-kluwer-was', naam='Zoem-van-de-Zevende', volk='kluwer', regio='Brakhaven', geboren=1700, geslacht='v', rol='Kluwer-werkster zonder korf die wasnachten verkoopt',
     wil='genoeg verdienen voor een eigen familie', geheim='de was raakt op en ze rekt hem met gewone bijenwas', prijs='haar klanten', afstamming=['VOLK-kluwer', 'LOT-Z44-kluwers'], verbonden_met=['INTR-Z46-10-intrige']),
 'DRAGER-Z48-geheugen-10': dict(code='PER-Z50-houtsnijder', naam='Oren Houtsnijder', volk='mens', regio='Groenmuil', geboren=1720, geslacht='m', rol='houtsnijder die met een Aelthir in een feeënring ligt',
     wil='haar herinneren als ze weg is', geheim='hij heeft als kind iets in de kluizen gezien', prijs='een herinnering die hij niet terugkrijgt', afstamming=['FEE-Z37-myrrhen-ringen', 'VOLK-aelthir-V5'], verbonden_met=['THRILL-Z46-11-thriller']),
 'DRAGER-Z48-zoem-10': dict(code='PER-Z50-grom-smid', naam='Grom Kwartdhurn', volk='dhurn', regio='Hoogvrouwe', geboren=1650, geslacht='m', rol='smid met een kwart Dhurn-bloed',
     wil='verkopen wat hij niet kan', geheim='hij weet de toon niet', prijs='zijn goede naam, bijna', afstamming=['VOLK-dhurn', 'GEB-Z42-eerste-ijzer'], verbonden_met=['COMEDY-Z46-11-comedy']),
 'DRAGER-Z48-maat-10': dict(code='PER-Z50-hal-reus', naam='Hal Langbot', volk='tharn', regio='Kaldrun', geboren=1690, geslacht='m', rol='jongeman met reuzenbloed aan een rijk hof',
     wil='begeerd worden zonder bekeken te worden', geheim='zijn botten groeien nog', prijs='zijn lichaam', afstamming=['VOLK-tharn', 'HUI-kaldra-Z6'], verbonden_met=['LOT-Z44-tharn']),
 'DRAGER-Z48-steen-10': dict(code='PER-Z50-ennika', naam='Ennika Badhuis', volk='mens', regio='Saelith', geboren=1640, geslacht='v', rol='hoedster van een badhuis met beeldnachten',
     wil='de laatste Orrim-stof redden', geheim='ze heeft de Orrim nooit gevraagd, tot nu', prijs='haar badhuis', afstamming=['VOLK-orrim', 'LOT-Z44-orrim'], verbonden_met=['OORLOG-Z46-10-oorlog']),
 'DRAGER-Z48-storm-10': dict(code='PER-Z50-karruk-vechtster', naam='Varna Roetvuist', volk='karrûk', regio='Amberpas', geboren=1620, geslacht='v', rol='Karrûk-vechtster die het jaarlijkse gevecht wint',
     wil='het gevecht houden zonder de Storm', geheim='ze heeft haar kampioen laten winnen in een eerder jaar', prijs='haar titel', afstamming=['VOLK-karrûk-Z6-Z38', 'LOT-Z44-karruk-storm'], verbonden_met=['HELD-Z46-9-held']),
 'DRAGER-Z48-gave-11': dict(code='PER-Z50-heelster-nevel', naam='Moira van de Nevel', volk='myrrhen', regio='Nevel-eilanden', geboren=3100, geslacht='v', rol='heelster die sporennachten bijhoudt in een dagboek',
     wil='voelen wat haar grootmoeder voelde', geheim='ze heeft haar geliefde al eens vergeten', prijs='haar herinneringen', afstamming=['VOLK-myrrhen-Z6', 'DRAGER-Z48-gave-11'], verbonden_met=['HORROR-Z46-11-horror']),
 'DRAGER-Z48-zee-11': dict(code='PER-Z50-kapitein-havenbloed', naam='Kapitein Brina Zoutkeel', volk='sael-mor', regio='Zoutkust', geboren=3150, geslacht='v', rol='kapiteinsvrouw met havenbloed',
     wil='een man van het land meenemen in de springtijnacht', geheim='ze kan zelf niet meer lang onder water', prijs='haar bemanning loopt gevaar', afstamming=['VOLK-sael-mor', 'LOT-Z44-sael-mor'], verbonden_met=['VERHAAL-Z44-tijdperk-11']),
 'DRAGER-Z48-ontvangst-13': dict(code='PER-Z50-aru-vuur', naam='Aru van het Plat', volk='mens', regio='het droge plat', geboren=6400, geslacht='v', rol='jonge vrouw die voor het eerst bij het vuur staat',
     wil='zelf vragen in plaats van gevraagd worden', geheim='ze kent de oude betekenis van het vuur van haar grootmoeder', prijs='de veiligheid van alleen kijken', afstamming=['DRAGER-Z48-ontvangst-13', 'VOLK-ishvar'], verbonden_met=['EROS-Z45-haak-8']),
 'DRAGER-Z48-stal-13': dict(code='PER-Z50-zuinige-boer', naam='Bort Nooitgenoeg', volk='ishvar', regio='het droge plat', geboren=6300, geslacht='m', rol='zuinigste boer van het dorp',
     wil='het oogstfeest gratis', geheim='hij heeft nooit iemand durven vragen', prijs='zijn zuinigheid', afstamming=['DRAGER-Z48-stal-13', 'VOLK-ishvar'], verbonden_met=['VERHAAL-Z44-tijdperk-13']),
 'DRAGER-Z48-vleugel-13': dict(code='PER-Z50-springster', naam='Lena Diepwater', volk='skerra', regio='de kliffen van het plat', geboren=6500, geslacht='v', rol='vrouw die voor het dorp terechtstaat na het klifspringfeest',
     wil='de waarheid over de sprong', geheim='zij liet echt los, zoals het oude spel vraagt', prijs='haar plek in het dorp', afstamming=['DRAGER-Z48-vleugel-13', 'LOT-Z44-skerra'], verbonden_met=['FASE-z44-mensen']),
 'DRAGER-Z48-vorm-13': dict(code='PER-Z50-weduwe-portret', naam='Ila Schilderes', volk='mens', regio='het droge plat', geboren=6550, geslacht='v', rol='weduwe die zichzelf schildert na elke sporenspiegel',
     wil='haar oude man nog één keer zien', geheim='ze weet al welk gezicht ze kust', prijs='haar nieuwe liefde, misschien', afstamming=['DRAGER-Z48-vorm-13', 'VOLK-myrrhen-Z6'], verbonden_met=['DRAGER-Z48-gave-11']),
 'DRAGER-Z48-zang-14': dict(code='PER-Z50-zangpoel', naam='Ysel Getijde', volk='mens', regio='de nieuwe kust', geboren=9000, geslacht='v', rol='vrouw die in de zangpoel staat met een Oevrin-man',
     wil='de poel houden zolang het water haar laat', geheim='ze zingt in akkoorden die geen mens kan', prijs='de poel en hem', afstamming=['VOLK-oevrin', 'DRAGER-Z48-zang-14'], verbonden_met=['VERHAAL-Z44-tijdperk-14', 'EROS-Z45-haak-9']),
}
FZ = {'9': 9, '10': 10, '11': 11, '13': 13, '14': 14}
def stap_z49():
    for vid, code, fase, drager, kern in c.execute("select id,code,fase,drager,kern_codes from verhaal_profiel where run='Z49'").fetchall():
        p = Z49P.get(drager)
        if not p: continue
        f = int(fase.split(' ')[0]); voeg_persoon(p, f)
        nk = ';'.join(dict.fromkeys((kern or '').split(';') + [p['code']]))
        c.execute('update verhaal_profiel set drager=?,kern_codes=? where id=?', (p['code'], nk, vid))
        wijz(code, 'gewijzigd', 'verhaal_profiel.drager', drager, p['code']); S['z49_persoon'] += 1
    toets('z49-personen')

for s in (sys.argv[1:] or ['catalogus', 'z49', 'paden']): globals()['stap_' + s]()
c.commit(); print(dict(S))
