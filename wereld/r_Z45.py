# Ronde Z45: de zinnelijke lange tijd en de fantasy-wezens.
# Opdracht van Rogier (2 november 2026): tot 810 flinke seksuele excessen; alles net wat erotischer en sensueler, omdat kracht via bloed en zaad
# reisde; veel polyamorie die doorloopt maar minder wordt; alles wat bij fantasy hoort (draken enzovoort) op de tijdlijn; flink wat ruimte voor
# erotische verhalen, niet verplicht, wel mogelijk.
# Bronnen: mythen/oorsprong.yaml (16 nieuwe fantasy-oorsprongen, door koppel.py aan de canon gekoppeld), tijd/wezens.yaml (zeden) en
# tijd/uitkomst.json (zedencurve per tijdperk). Alles is VOORSTEL (ideeënbank). Harde lijnen: alleen volwassenen, altijd een ja, geen dieren.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 mythen/koppel.py && python3 mythen/toets_mythen.py && python3 tijd/verlies.py
#   && python3 r_Z45.py && python3 velmara.py tekst && python3 velmara.py toets
import sqlite3, os, sys, json, collections, subprocess, yaml
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z45'; RN = 74; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); m = sqlite3.connect(os.path.join(W, 'mythen', 'mythen.db'))
S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig'); U = json.load(open('tijd/uitkomst.json'))
REDEN = 'Ronde Z45: zinnelijke lange tijd en fantasy-wezens (opdracht van Rogier 2026-11-02); geschreven vanuit de rijen waarnaar verwezen wordt'
T = {9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 12: '12 Het Vertrek (na 801)',
     13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)', 15: '15 Het Zwevende Gat (na 801)', 16: '16 Tijd van het Schrift (na 801)'}
TIJD = {0: '0 Voortijd', 1: '1 Overvloed', 2: '2 Vonk', 3: '3 Brand', 4: '4 Noodtoestand', 5: '5 Ontvangst', 6: '6 Markt', 7: '7 Barsten', 8: '801 (nu)', 9: None}

def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z45.py')).rowcount
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
def nieuw(code, cat, ond, feit, verw, tijdperk, epi):
    if c.execute('select 1 from canon where code=?', (code,)).fetchone(): return
    for x in verw:
        if not c.execute('select 1 from canon where code=?', (x,)).fetchone(): sys.exit(f'{code}: verwijzing {x} bestaat niet')
    v = ';'.join(dict.fromkeys(lev(x) for x in verw))
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (code, cat, ond, feit, feit, REDEN, 'voorlopig', RN, v, v, tijdperk, 1, epi))
    S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:4]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

# ---------- 1. fantasy-wezens: MYTHE-rijen voor de clusters die er nog niet zijn ----------
def stap_mythen():
    cl = {x['id']: x for x in yaml.safe_load(open('mythen/clusters.yaml'))}
    for o in yaml.safe_load(open('mythen/oorsprong.yaml')):
        if c.execute('select 1 from canon where code=?', ('MYTHE-Z43-' + o['cluster'],)).fetchone(): continue
        code = 'MYTHE-Z45-' + o['cluster']
        sc = m.execute('select max(score) from koppel_score where cluster=?', (o['cluster'],)).fetchone()[0] or 0
        verw = ';'.join(dict.fromkeys(lev(x) for x in o['canon']))
        m.execute('insert or replace into oorsprong(cluster,laag,canon_codes,voorstel,score,status,regels,verlies,boek) values(?,?,?,?,?,?,?,?,?)',
                  (o['cluster'], TIJD[o['laag']] or 'doorlopend', verw, code, sc, 'voorstel', ','.join(o['regels']), o['verlies'], o['boek']))
        for i, t in enumerate(o['keten'], 1):
            m.execute('insert or replace into vervorming(cluster,stap,eeuw,tekst,regel) values(?,?,?,?,?)',
                      (o['cluster'], i, ['Velmara', 'Midden-aarde en het zwevende gat', 'de aarde'][i - 1], t, ','.join(o['regels'])))
        nieuw(code, 'Mythe', cl[o['cluster']]['naam'], o['rij'], o['canon'], TIJD[o['laag']], 'voorstel (mytheplan M3, Z45)')
    m.commit(); toets('mythen')

# ---------- 2. de Losbandige Jaren, 801-810 ----------
def stap_losbandig():
    nieuw('GEB-Z45-losbandige-jaren', 'Geschiedenis', 'De Losbandige Jaren (802-810)',
          'Tussen 802 en 810 viert Velmara de ja tot het pijn doet. Vier dingen vallen samen. De ja is nieuw: wie nooit zelf mocht kiezen, wil het elke nacht opnieuw doen (HAAK-B1-2-4). '
          'Het Lichtconvent van 806 verklaart geloften ongeldig, en de stallen gaan open (BESLUIT-Z6-WRIJ-077). Duizenden mannen die bezit waren, zijn ineens vrij en gewild. '
          'De gaven doven, en iedereen wil de laatste vonk voordat hij weg is (BESLUIT-Z12-2). Zonder Orde is er niemand die de Ontvangst nog regelt. Zo ontstaan feesten die dagen duren, huizen met vijf of zes volwassenen, '
          'en een markt voor wie nog vonk heeft. Het is uitbundig en het is niet onschuldig: wie gewend was te nemen, probeert dat nog, en waar dat gebeurt, is het een gelabeld donker thema. '
          'Na 810 blijft de vrijheid, en de roes trekt weg.',
          ['BESLUIT-Z12-2', 'BESLUIT-Z6-WRIJ-077', 'HAAK-B1-2-4', 'BESLUIT-7', 'FASE-z44-ja'], T[9], 'voorstel (Z45, gebeurtenis)')
    nieuw('VERHAAL-Z45-losbandig', 'Verhaal', 'De laatste vonk van Ambergaard',
          'Saske de Jonge was stalschrijver en heeft twintig jaar namen genoteerd van mannen die geen nee mochten zeggen. In 807 opent ze het register op het marktplein en leest het voor, naam voor naam, '
          'terwijl rond haar het feest van de vrije stallen al drie dagen duurt. Een van de namen staat op en vraagt haar of ze met hem danst. Ze weet niet of ze dat mag, en vraagt het. '
          'Hij zegt ja, en dan lacht hij, omdat hij het voor het eerst hardop zegt. Het verhaal volgt hen door de roes van die jaren: de huizen vol vrienden en minnaars, de jaloezie die niemand kent omdat ze nooit hoefde, '
          'en de ochtend in 810 waarop zijn vonk niet meer komt, en ze toch blijven. Alle betrokkenen zijn volwassen, en elke stap begint met een vraag.',
          ['GEB-Z45-losbandige-jaren', 'BESLUIT-Z6-WRIJ-077', 'HAAK-B1-2-4'], T[9], 'voorstel (Z45, verhaal)')
    toets('losbandig')

# ---------- 3. zeden per tijdperk + ruimte voor erotische verhalen ----------
def z(naam, f): return U['zeden'][naam][str(f)][1]
ZEDEN = {
 9: lambda: f'Na de Losbandige Jaren blijft Velmara een wereld waarin delen gewoon is: polyamorie staat op {z("polyamorie",9):.0%} van het niveau van 801, lichaamsopenheid op {z("lichaamsopenheid",9):.0%}. '
            'Huizen met meer volwassenen houden stand, de Ontvangst wordt een feest zonder priesteres, en wie exclusief liefheeft, is niet meer ketters maar een beetje ouderwets-nieuw. Ruimte voor erotische verhalen: groot. '
            'Het nieuwe is de vraag zelf; elke scène kan draaien om wie wat durft te vragen, nu nee kan.',
 10: lambda: f'In de Tijd der Volken is delen een keuze geworden: polyamorie op {z("polyamorie",10):.0%}, het Ontvangstfeest bijna verdwenen ({z("ontvangst-feest",10):.0%}), lichaamsopenheid op {z("lichaamsopenheid",10):.0%}. '
             'Jaloezie wordt een gewoon gevoel, en de volken hebben elk hun eigen gebruiken die langzaam vervagen: de Skerra op hun kliffen, de Ves-Lethi met hun spiegelnacht, de Sael-mor op hun schepen. '
             'Ruimte voor erotische verhalen: ruim, vooral tussen volken, waar het laatste van iets moois in een nacht past.',
 11: lambda: f'In de Heldentijd is het grote huis met vele minnaars iets van oude families en verre volken: polyamorie op {z("polyamorie",11):.0%}, lichaamsopenheid op {z("lichaamsopenheid",11):.0%}. '
             'Liefde wordt vaker een paar, en een paar dat drie wordt, is een verhaal. De wereld is sensueler dan de onze, omdat de herinnering aan de vonk in liederen en gewoonten zit. '
             'Ruimte voor erotische verhalen: gemiddeld; tussen gezellen op een tocht, tussen een mens en een vervagende Aelthir.',
 12: lambda: f'In Het Vertrek staat de gewone zede op de vloer die in elke tijd blijft: delen bij een op de zeven huishoudens ({z("polyamorie",12):.0%}), naakt zalven bij feesten ({z("lichaamsopenheid",12):.0%}). '
             'Wat erotisch is in dit tijdperk, is het afscheid: wie blijft en wie gaat, de laatste nacht voor de lander opstijgt. Ruimte voor erotische verhalen: klein in aantal, groot in gewicht.',
 13: lambda: 'Op het droge plat leeft de oude zede voort in de vuurfeesten: in de kortste nacht kiest wie wil, een of meer, bij het vuur. Er is geen kracht meer mee gemoeid, alleen een gewoonte die ouder is dan iemand weet. '
             'Ruimte voor erotische verhalen: de vuurnacht als vaste plek, steeds verder van haar oorsprong.',
 14: lambda: 'Terwijl het water stijgt, trouwen mensen en Oevrin vaker, omdat de oude grenzen samen verdrinken. Het paaifeest van de Oevrin, zang in het tij zonder aanraking, wordt voor mensen het sensueelste wat er is. '
             'Ruimte voor erotische verhalen: verlangen dat niet aanraakt, en liefde over de grens van land en zee.',
 15: lambda: 'In het zwevende gat blijft één formule over uit de tijd van het Zegel: wie een ander wil, vraagt het drie keer en wacht. Niemand weet meer waarom; het is gewoon hoe het hoort bij een huwelijk of een vuurnacht. '
             'Ruimte voor erotische verhalen: rituelen die de ja bewaren zonder te weten wat ze bewaren.',
 16: lambda: 'In onze tijd is van de zede van Velmara weinig over: een vuurfeest in juni, de vraag bij een huwelijk, een grootmoeder die zegt dat liefde gedeeld moet worden. '
             'Ruimte voor erotische verhalen: urban fantasy, waarin iemand met een restje vonk of een Oevrin-stem de oude zinnelijkheid wakker maakt in een gewone stad.',
}
HAKEN = [
 (9, 'De eerste nacht van de vrije stal', ['GEB-Z45-losbandige-jaren', 'DAG-dag-man', 'BESLUIT-Z6-WRIJ-077'],
  'Een man die twaalf jaar in een stalhuis heeft gewoond, mag voor het eerst zelf kiezen met wie hij de nacht doorbrengt, en hij weet niet hoe dat moet. Een vrouw die hem vroeger alleen op de lijst zag staan, '
  'vraagt het hem, en hij zegt nee, en dan ja, en het nee maakt het ja zwaarder. Alle betrokkenen volwassen; de scène draait om de vraag.'),
 (9, 'Het feest van het laatste vuur', ['GEB-Z45-losbandige-jaren', 'MAGIE-kracht-duur', 'KETEN-kruik-ontvangst'],
  'In een dorp aan de Zoutkust heeft nog één man een vonk die een kaars aansteekt. Op het oogstfeest wil iedereen hem; hij besluit wie, en zij beslissen of ze dat willen. '
  'Een uitbundige, warme nacht met meer volwassenen, en in de ochtend de wetenschap dat dit de laatste keer is.'),
 (10, 'De laatste spiegelnacht', ['SEKS-VOLK-ves-lethi-kern', 'MYTHE-Z45-toverspiegel', 'VOLK-ves-lethi-Z6'],
  'Een weduwe vraagt een Ves-Lethi om één nacht de gedaante van haar overleden man aan te nemen. De Ves-Lethi weet dat ze daarna misschien nooit meer wisselt, want haar lichaam houdt het niet meer vast. '
  'Allebei volwassen, allebei kiezend; het is tederheid en rouw in één bed.'),
 (10, 'Het schip met drie kapiteins', ['VOLK-sael-mor', 'RIJK-Z37-saelmor-humor'],
  'Op een Sael-mor-schip delen drie kapiteinsvrouwen al jaren dezelfde stuurman, en dat gaat goed tot een van hen hem alleen voor zichzelf wil. '
  'Jaloezie is voor hen een nieuw gevoel, en ze weten niet of ze het moeten verbieden of vieren. Volwassenen, humor, en een vloot die meekijkt.'),
 (11, 'De laatste aanraking', ['VOLK-aelthir-V5', 'D1-aelthir-ziekte', 'LOT-Z44-aelthir'],
  'Een Aelthir weet dat ze over een jaar de aanraking kwijt is, zoals haar volk na de geur eerst de huid verliest. Ze kiest een mens om dat jaar mee door te brengen, '
  'en ze willen allebei alles nog één keer voelen. Volwassenen; zinnelijk, langzaam, met het einde in zicht.'),
 (11, 'Drie gezellen, één deken', ['VERHAAL-Z44-tijdperk-11', 'VOLK-dhurn', 'VOLK-karrûk-Z6-Z38'],
  'Een mensenvrouw, een Dhurn en een vrouw met Karrûk-bloed zijn op tocht naar de laatste kluis en delen in de bergen één deken. Wat begint als warmte, wordt een vraag die ze elkaar stellen, '
  'en een antwoord dat hun tocht verandert. Drie volwassenen, alles met een ja.'),
 (12, 'De nacht voor de lander', ['VERHAAL-Z44-tijdperk-12', 'TECHNO-metaal-schip-Z42'],
  'Een mens en de Aelthir die morgen met de lander vertrekt, hebben nog één nacht. Zij komt nooit terug, en voor haar staat de tijd daarna stil. '
  'Een erotische afscheidsscène tussen twee volwassenen, waarin de ochtend het grootste gewicht heeft.'),
 (13, 'De kortste nacht', ['FASE-z44-mensen', 'MYTHE-Z43-heilig-huwelijk'],
  'Bij het vuur van de kortste nacht kiest wie wil een of meer gezellen, zoals het altijd ging. Een jonge vrouw die er voor het eerst bij is, vraagt haar grootmoeder waarom. '
  'Die weet het niet meer, alleen dat je eerst vraagt. Volwassenen bij het vuur; een feest waarvan de herkomst vergeten is.'),
 (14, 'Zang in het tij', ['VOLK-oevrin', 'D1-oevrin-feest', 'VERHAAL-Z44-tijdperk-14'],
  'Een mensenvrouw en een Oevrin-man houden samen een veer terwijl het water stijgt. Hun liefde kan niet zoals bij mensen, want zijn volk bevrucht buiten het lichaam en paart met zang. '
  'Wat ze samen vinden, is een verlangen dat zingt in plaats van aanraakt. Volwassenen; zinnelijk zonder dat het lichaam het werk doet.'),
 (15, 'Drie keer vragen', ['FASE-z44-gat', 'BESLUIT-Z12-2'],
  'Bij een huwelijk aan een nieuwe kust moet de bruidegom drie keer vragen en drie keer wachten, en de bruid mag drie keer weigeren. Een bruid weigert twee keer om hem te plagen en de derde keer echt, '
  'en het dorp weet niet wat het met een echt nee moet. Volwassenen; erotiek als spel van wachten.'),
 (16, 'Een vonk in de stad', ['VERHAAL-Z44-tijdperk-16', 'MYTHE-Z43-feeen', 'LOT-Z44-myrrhen'],
  'In een stad van nu ontdekt een man dat zijn aanraking een kaars kan aansteken, en een vrouw die hem ontmoet in een stadspark met een feeënring weet waarom: haar grootmoeder vertelde het. '
  'Urban fantasy met een erotische lijn tussen twee volwassenen, die ontdekken wat er van Velmara over is.'),
]
def stap_zeden():
    for f, tekst in ZEDEN.items():
        nieuw(f'ZEDEN-Z45-fase-{f}', 'Cultuur', 'Zeden en ruimte voor erotiek: ' + T[f].split(' ', 1)[1].replace(' (na 801)', ''), tekst(),
              ['FASE-z44-' + {9: 'ja', 10: 'volken', 11: 'helden', 12: 'vertrek', 13: 'mensen', 14: 'smelt', 15: 'gat', 16: 'schrift'}[f], 'BESLUIT-7', 'KETEN-kruik-ontvangst'],
              T[f], 'voorstel (Z45, zedencurve uit simulatie tijd/verlies.py)')
    for i, (f, titel, verw, tekst) in enumerate(HAKEN, 1):
        nieuw(f'EROS-Z45-haak-{i}', 'Romantiek', titel, tekst, verw, T[f], 'voorstel (Z45, erotische haak)')
    toets('zeden')

for s in (sys.argv[1:] or ['mythen', 'losbandig', 'zeden']): globals()['stap_' + s]()
c.commit(); print(dict(S))
