# Ronde Z41: de verhalengraaf laten kloppen.
# 1 draden:     verwijzingen in levende rijen volgen de opvolger van vervangen rijen (geen oude versies meer).
# 2 dood:       19 doodlopende verwijzingen naar vervallen gebeurtenissen: naar de levende opvolger, of naar een nieuwe
#               gebeurtenis in de ideeënbank (voorlopig) als er geen opvolger is.
# 3 haken:      35 zwevende haken krijgen concrete knopen (personage, plek, volk, gebeurtenis), gelezen uit hun eigen tekst.
# 4 identiteit: één persoon = één knoop (persoon_identiteit), voor personages die onder twee codes staan.
# Gebouwd door de architect op verzoek van Rogier (2026-11-01). Idempotent, additief: niets verwijderd, roman niet aangeraakt,
# Kern-rijen niet gewijzigd. Elke wijziging staat in tabel wijziging (ronde Z41). Gebruik: DB=kopie.db python3 r_Z41.py [stappen]
import sqlite3, shutil, os, re, sys, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-01'; RD = 'Z41'; RN = 70; DB = os.environ.get('DB', 'canon.db')
STAPPEN = sys.argv[1:] or ['draden', 'dood', 'haken', 'identiteit', 'tijd', 'personen801']
if DB == 'canon.db' and not os.path.exists('canon_backup_Z41.db'): shutil.copy('canon.db', 'canon_backup_Z41.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
REDEN = 'Ronde Z41: verhalengraaf laten kloppen (architect, op verzoek van Rogier, 2026-11-01)'

def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', None if oud is None else str(oud), str(nieuw), DT, 'r_Z41.py')).rowcount

def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:4]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

LEVEND = ('vastgesteld', 'voorlopig')
def lev(x):
    """Levende opvolger van x. Een rij die naar personage_profiel:X is verhuisd, wijst naar X (X is zelf een canonrij)."""
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

def zet_verw(code, nieuwe, waarom):
    oud = c.execute('select verwijst_naar from canon where code=?', (code,)).fetchone()[0]
    if (oud or '') == nieuwe: return
    c.execute('update canon set verwijst_naar=? where code=?', (nieuwe, code))
    S['verwijst_naar_gewijzigd'] += 1; wijz(code, 'gewijzigd', 'canon.verwijst_naar (' + waarom + ')', oud, nieuwe)

def is_kern(code):
    r = c.execute('select draagkracht,draagkracht_handmatig from canon where code=?', (code,)).fetchone()
    return r and 'Kern' in (r[0] or '', r[1] or '')

# ---------- 1 draden ----------
def stap_draden():
    for code, v in c.execute(f"select code,verwijst_naar from canon where status in {LEVEND} and verwijst_naar is not null").fetchall():
        if is_kern(code): S['kern_overgeslagen'] += 1; continue
        delen = [x.strip() for x in re.split(r'[;,]\s*', v) if x.strip()]
        nieuw = list(dict.fromkeys(lev(x) for x in delen))
        if nieuw != delen: zet_verw(code, ';'.join(nieuw), 'volgt opvolger')
    # verhaalprofielen: dezelfde regel voor de codevelden
    for veld in ('drager', 'erf_code', 'zaadje_code', 'wereldregel_code', 'premisse_codes'):
        for code, v in c.execute(f"select code,{veld} from verhaal_profiel where status='voorlopig' and {veld} is not null").fetchall():
            delen = [x.strip() for x in v.split(';') if x.strip()]
            nieuw = list(dict.fromkeys(lev(x) for x in delen))
            if nieuw != delen:
                c.execute(f'update verhaal_profiel set {veld}=? where code=?', (';'.join(nieuw), code))
                S['profiel_gewijzigd'] += 1; wijz(code, 'gewijzigd', 'verhaal_profiel.' + veld + ' (volgt opvolger)', v, ';'.join(nieuw))
    toets('draden')

# ---------- 2 dood ----------
OPVOLGER = {  # vervallen gebeurtenis -> levende gebeurtenis met hetzelfde voorval (gelezen: zelfde naam, wat en gevolg)
    'GEB-bloednacht-lisk': 'GEB-bloednacht-788', 'GEB-jongenshof': 'GEB-r10-jongenshof', 'GEB-val-lisk': 'GEB-lisk-brandt-Z6',
    'GEB-haremwet': 'GEB-haremwet-ardemar', 'GEB-kroon-saelith': 'GEB-r10-eerste-kroon', 'GEB-eerste-registers': 'GEB-r10-eerste-register',
    'GEB-uitverkorenen': 'GEB-uitverkorenen-210-Z6', 'GEB-vonkpest': 'GEB-vonkkoorts', 'GEB-oorlog-zeven-kronen': 'GEB-zeven-kronen',
    'GEB-deelwet': 'GEB-deelwet-40', 'GEB-kharvos-inval': 'GEB-kharvos-720', 'GEB-orde-sticht': 'GEB-orde-90',
    'GEB-sterrensteen-val': 'GEB-Z17-sterrensteen-inslag',
    'GEB-grote-pest': 'GEB-pest-340', 'GEB-zegel': 'GEB-zegel-gelegd', 'GEB-melkstallen': 'GEB-r10-melkstallen',
    'GEB-ves-anath-verlaten': 'GEB-ves-anath-ontruimd', 'GEB-eerste-vonk': 'GEB-orric-vonk', 'GEB-schisma-stilte': 'GEB-stille-schisma',
    'GEB-ketenwake-ontstaat': 'GEB-r10-ketenwake', 'GEB-offer-dochters': 'GEB-dochteroffer', 'GEB-zaadbeurs': 'GEB-zaadbeurs-455',
    'GEB-zusters-heelsters': 'GEB-r10-zusterhuizen', 'GEB-rotatiewet': 'GEB-r10-rotatie', 'GEB-vonkkoningen': 'GEB-r10-varnath-opkomst',
}
NIEUW_GEB = [  # geen levende opvolger: nieuwe gebeurtenis, voorlopig, in de ideeënbank; jaar open (de oude jaartallen zijn vervallen)
    ('GEB-Z41-zegel-flakkert', 'GEB-zegel-verzwakt', '7 Barsten', 'Het zegellicht flakkert',
     'Het zegellicht flakkert, ergens in de Barsten vóór 801 (jaar open). In Ambergaard en de jungle worden meer jongens geboren dan het Zegel zou toelaten; de zegelwachters meten het en zwijgen. Voorstel uit Z41 (opvolger van het vervallen GEB-zegel-verzwakt), gedragen door HELD-SKELET-Z10-6 en THRL-fase7-zegelmeting.',
     'FASE-barsten;ORIGIN-10-Z36;REG-ambergaard'),
    ('GEB-Z41-kharvos-stichting', 'GEB-kharvos-stam', '1 Overvloed', 'Kharvos ontstaat',
     'Ballingen uit Saelith trekken naar het noordoosten, buiten het bereik van wat later het Zegel wordt, en stichten daar in de Overvloed het mannenrijk Kharvos (jaar open). Voorstel uit Z41 (opvolger van het vervallen GEB-kharvos-stam), gedragen door INTR-fase1-kharvos-moeder; leidt naar GEB-r10-kharvos-scheiding.',
     'FASE-overvloed;REG-kharvos-B1;GEB-r10-kharvos-scheiding'),
    ('GEB-Z41-raad-zegelplan', 'GEB-raad-ves-anath', '3 Brand', 'De raad kiest het Zegelplan',
     'Kort vóór jaar 0, in de Brand, besluit een raad van zusters in Ves-Anath de mannen terug te brengen tot een getal dat de wereld kan dragen, en kiest daarmee het Zegelplan. Eén raadsvrouw speelt voor de vonkkoningen. Voorstel uit Z41 (opvolger van het vervallen GEB-raad-ves-anath), gedragen door INTR-V2-raadsverraad; leidt naar GEB-dochteroffer en ORIGIN-10-Z36.',
     'FASE-brand;GEB-dochteroffer;ORIGIN-10-Z36'),
    ('GEB-Z41-kaldra-eed', 'GEB-kaldra-eed', '4 Noodtoestand', 'De eed van Kaldra',
     'Huis Kaldra krijgt in de Noodtoestand (jaar open) het leger van de grens in ruil voor Strijdontvangsten; de Tharn zweren mee en Kaldra betaalt hen later in vergif. Voorstel uit Z41 (opvolger van het vervallen GEB-kaldra-eed), gedragen door INTR-V2-tharn-eed; leidt naar GEB-r10-kaldra-krijg.',
     'FASE-noodtoestand;HUI-kaldra-Z6;VOLK-tharn;GEB-r10-kaldra-krijg'),
    ('GEB-Z41-mirre-vrijhaven', 'GEB-mirre-vrijhaven', '5 Ontvangst', 'Brakhaven wordt vrijhaven',
     'Huis Mirre weigert de Orde de tiende op zee. Na een oorlog van kaperij en mist houdt Mirre zijn haven als vrijhaven buiten de Orde, en daar groeien de zwarte markt en de Gemaskerde Veiling (jaar open). Voorstel uit Z41 (opvolger van het vervallen GEB-mirre-vrijhaven), gelezen uit OORLOG-Z9-16, BEST-huis-mirre en HELD-Z10-35.',
     'FASE-ontvangst;HUI-mirre;BEST-huis-mirre;OORLOG-Z9-16;RIT-gemaskerde-veiling'),
]
def stap_dood():
    for code, oud, tp, ond, feit, verw in NIEUW_GEB:
        if not c.execute('select 1 from canon where code=?', (code,)).fetchone():
            verw = ';'.join(dict.fromkeys(lev(x) for x in verw.split(';')))
            c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (code, 'Geschiedenis', ond, feit, feit, REDEN, 'voorlopig', RN, verw, verw, tp, 1, 'voorstel (architect Z41, geen besluit)'))
            S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
        OPVOLGER[oud] = code
    c.execute("update canon set epistemiek='voorstel (architect Z41, geen besluit)' where code like 'GEB-Z41-%' and epistemiek like 'aanname (architect Z41%'")
    for code, v in c.execute(f"select code,verwijst_naar from canon where status in {LEVEND} and verwijst_naar is not null").fetchall():
        if is_kern(code): continue
        delen = [x.strip() for x in re.split(r'[;,]\s*', v) if x.strip()]
        nieuw = list(dict.fromkeys(OPVOLGER.get(x, x) for x in delen))
        if nieuw != delen: zet_verw(code, ';'.join(nieuw), 'doodlopende gebeurtenis vervangen')
    toets('dood')

# ---------- 3 haken ----------
ZEGEL = 'ORIGIN-10-Z36'; ORDE = 'ORDE-orde'; KHARVOS = 'REG-kharvos-B1'; LIORA = 'PER-liora-profiel-Z32'
THALEN = 'PER-v4-thalen-orr-Z32'; YSA = 'PER-v4-ysa-maren'; HARROW = 'ORIGIN-Z1-harrow'
HAKEN = {  # elke keuze volgt uit een naam of ding dat letterlijk in de haak staat
    'HAAK-v4-stemklok': ['PER-v4-hesta-kael', 'ORIGIN-5', 'PER-ithrael', 'PER-morvane-profiel'],   # Hesta, de Wieg, Ithrael, Morvane-ir
    'ORIGIN-onthulplan': ['ORIGIN-5', 'VOLK-dhurn', YSA],                                         # Wiegkast, Dhurn-handen, schip Ysa
    'HAAK-V5-zegel-1': [THALEN, ORDE, 'REG-stille'],                                              # Thalen, de Orde, Stille Zusters
    'HAAK-V5-zegel-2': ['REG-stille', 'GEB-dochteroffer', 'LICH-dochters'],                       # Stille Zuster, Dochter in het Zegel
    'HAAK-V5-zegel-3': ['PLEK-Z4-hoog-1', 'TECHNO-zegelsteen'],                                   # de Sterrensteen
    'HAAK-V5-zegel-4': ['VOLK-orrim', 'TECHNO-zegelsteen'],                                       # de Orrim en hun voorouders in de steen
    'HAAK-V5-zegel-5': [YSA, THALEN],                                                             # Ysa's bevel, Thalen
    'HAAK-B1-1-1': ['BEST-orde-hoofd', 'PER-ithrael', ORDE],                                      # de Hoge Moeder (801: Ithrael)
    'HAAK-B1-1-2': ['BEST-orde-hoofd', ORDE],                                                     # het Conclaaf
    'HAAK-B1-1-3': ['BEST-orde-hoofd', 'ORIGIN-5'],                                               # Hoge Moeder, de machine
    'HAAK-B1-1-4': [ORDE, 'BEST-orde-hoofd'],                                                     # Orde-archivaris, kroniek
    'HAAK-B1-2-1': ['ERF-vonk', ORDE],                                                            # gaven-mannen verliezen hun vonk
    'HAAK-B1-2-2': [LIORA, THALEN],                                                               # Liora, Thalen
    'HAAK-B1-2-3': ['PER-aeron-profiel', LIORA],                                                  # Aeron, Liora
    'HAAK-B1-2-4': [ZEGEL, 'RIT-ontvangst'],                                                      # het Zegel vraagt om ja
    'HAAK-B1-3-1': [KHARVOS, HARROW, ORDE],                                                       # Kharvos-gezant, Harrow-kern
    'HAAK-B1-3-2': [KHARVOS, HARROW],                                                             # kaartplaat, waar de Harrow landde
    'HAAK-B1-3-3': [KHARVOS],                                                                     # gezantes in Kharvos
    'HAAK-B1-3-4': [KHARVOS, HARROW, 'UIT-VOLK-saelmor'],                                         # Kharvos-ingenieur, Saelmor-kapitein
    'HAAK-B1-5-1': ['HUI-kaldra-Z6', 'BEST-register'],                                            # Huis Kaldra, eigen register
    'HAAK-B1-5-2': [ORDE, 'RIT-ontvangst', 'REG-ambergaard'],                                     # graan, Ontvangsten
    'HAAK-B1-5-3': [ORDE, 'REG-ambergaard'],                                                      # dochter van een huis, Orde-zuster
    'HAAK-B1-5-4': ['PLEK-Z4-saelith-3', 'KOE-markt'],                                            # de Zaadbeurs
    'HAAK-B1-6-1': ['BEST-register', ORDE],                                                       # rekenzuster, fokcijfers
    'HAAK-B1-6-2': ['ERF-vonk', 'ZIEKTE-inteelt', ORDE],                                          # verwanten, vonk
    'HAAK-B1-6-3': [ORDE, 'ERF-vonk'],                                                            # karavaan gaven-mannen
    'HAAK-B1-6-4': ['ZIEKTE-inteelt', 'ERF-vonk'],                                                # eigen lijn, vonklicht
    'HAAK-Z1-harrow-1': ['TECH-ITEM-bio-1', 'PLEK-Z4-kharvos-5-Z5b', HARROW, KHARVOS],            # Leegteworm, Kharvos
    'HAAK-Z1-harrow-2': [HARROW, KHARVOS],                                                        # Harrow-ingenieur
    'HAAK-Z1-harrow-3': ['STAD-kharvos-hoornburg', KHARVOS],                                      # Hoornburg
    'HAAK-Z1-derdeweg-1': ['GEB-dochteroffer', 'LICH-dochters'],                                  # vrijgekomen Dochter
    'HAAK-Z1-derdeweg-2': ['PER-f3-dochter-elin', 'GEB-dochteroffer'],                            # Elin, de 49ste Dochter
    'HAAK-Z1-derdeweg-3': ['VOLK-orrim', ORDE],                                                   # de Orrim, de Orde
    'HAAK-Z1-derdeweg-4': [ZEGEL, 'RIT-ontvangst'],                                               # het Zegel vraagt
    'HAAK-Z17-zegel-6': [LIORA, ZEGEL, ORDE],                                                     # tijd van Liora, de Orde
}
def stap_haken():
    for code, extra in HAKEN.items():
        r = c.execute('select verwijst_naar from canon where code=?', (code,)).fetchone()
        if not r or is_kern(code): S['haak_overgeslagen'] += 1; continue
        delen = [x.strip() for x in re.split(r'[;,]\s*', r[0] or '') if x.strip()]
        nieuw = list(dict.fromkeys(delen + extra))
        if nieuw != delen: zet_verw(code, ';'.join(nieuw), 'haak krijgt knopen uit eigen tekst')
    toets('haken')

# ---------- 4 identiteit ----------
def stam(code):
    s = code
    for _ in range(4): s = re.sub(r'-(Z\d+[a-z]?|V\d+|B\d+|D\d+|G\d+|profiel|r\d+)$', '', s)
    return s
def stap_identiteit():
    # De tabel persoon_identiteit en view v_persoon zijn afgeleid: afgeleid_motor.persoon_identiteit() bouwt ze bij elke bouw.
    toets('identiteit')
    print('personen met meer dan één code:', c.execute('select count(*) from v_persoon where codes>1').fetchone()[0])


# ---------- 5 tijd ----------
FASE_GOED = {  # het verhaal speelt in 801: de personages en de queeste zijn van 801 (fase stond verkeerd)
    'QST-etappes-queeste': ('801 (nu)', 'de queeste van Liora (Teo, Aeron, Khaled, Morvane) speelt in 801'),
    'NU-conflict-schuld': ('801 (nu)', 'Selvine en Kreel leven in 801; NU- betekent het heden'),
}
LOS = {  # een link naar de verkeerde persoon met dezelfde naam
    'HELD-SKELET-Z10-6': ('PER-hethra', 'een andere Hethra (45, barstenwachter in fase 7), niet Hethra Brakmoeder uit fase 3; erfnaam'),
}
TIJD_UITZ = [  # bewust buiten de eigen fase: de Dochters leven in de steen van het Zegel tot 801
    ('HAAK-PER-romance', 'PER-ysara', 'Ysara hangt als Dochter in het Zegel; in 801 is zij er nog (stem in de steen)'),
    ('HAAK-PER-thriller', 'PER-ysara', 'Ysara hangt als Dochter in het Zegel; in 801 is zij er nog (stem in de steen)'),
    ('HAAK-Z1-derdeweg-2', 'PER-f3-dochter-elin', 'Elin hangt sinds jaar 0 in de steen; de derde weg maakt haar in 801 vrij'),
]
def stap_tijd():
    for code, (tp, waarom) in FASE_GOED.items():
        oud = c.execute('select tijdperk from canon where code=?', (code,)).fetchone()
        if oud and oud[0] != tp:
            c.execute('update canon set tijdperk=? where code=?', (tp, code)); S['tijdperk_gewijzigd'] += 1
            wijz(code, 'gewijzigd', 'canon.tijdperk (' + waarom + ')', oud[0], tp)
    for code, (weg, waarom) in LOS.items():
        r = c.execute('select verwijst_naar from canon where code=?', (code,)).fetchone()
        delen = [x.strip() for x in re.split(r'[;,]\s*', r[0] or '') if x.strip()]
        if weg in delen: zet_verw(code, ';'.join(x for x in delen if x != weg), waarom)
    for code, per, reden in TIJD_UITZ:
        if not c.execute("select 1 from toets_uitzondering where toets='graaf_tijd' and code=? and detail=?", (code, per)).fetchone():
            c.execute('insert into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)', ('graaf_tijd', code, per, reden + ' [Z41]', None))
            S['uitzondering_nieuw'] += 1; wijz(code, 'toegevoegd', 'toets_uitzondering', None, 'graaf_tijd ' + per)
    toets('tijd')


# ---------- 6 personen801 ----------
def stap_personen801():
    """Twaalf personen voor 801, uit 2000 trekkingen gekozen (z41/personen.py) en uitgeschreven. Voorstel: ideeënbank, geen canon."""
    sys.path.insert(0, os.path.join(W, 'z41'))
    from personen_801_gekozen import GEKOZEN
    for g in GEKOZEN:
        if c.execute('select 1 from canon where code=?', (g['code'],)).fetchone(): continue
        verw = ';'.join(dict.fromkeys(lev(x) for x in g['verwijst'].split(';')))
        feit = (g['verhaal'] + ' ' + g['prijs'] + ' ' + g['naam'] + ': ' + g['volk'] + ', ' + str(g['leeftijd']) + ', ' + g['rol']
                + '; plek in de motor: ' + g['positie'] + '; eigen fout: ' + g['fout'] + '. Terugwerken: ' + g['terug'])
        c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (g['code'], 'Verhaal', g['titel'], feit, feit, REDEN + '; persoon getrokken als ' + g['trekking'] + ' (z41/personen.py, seed 41801)',
                   'voorlopig', RN, verw, verw, '801 (nu)', 1, 'voorstel (architect Z41, uit trekking ' + g['trekking'] + ', seed 41801)'))
        S['canon_nieuw'] += 1; wijz(g['code'], 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
    toets('personen801')

for s in STAPPEN: globals()['stap_' + s]()
c.commit()
print(dict(S))
