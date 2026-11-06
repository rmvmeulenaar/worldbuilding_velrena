# Ronde Z49: verhaalpaden die de fantasieën na 801 mogelijk maken (opdracht van Rogier, 2 november 2026: "het zijn verhalen ... verhaalpaden
# ... in lijn met alle andere verhaalpaden en wat in de wereld bestaat ... divers, geen templates").
# Elk pad is een rij in verhaal_profiel (het bestaande systeem van verhaalpaden): fase, positie, genre, schaal, volk, vorm, afloop, hoofdpersoon,
# instemming, drager (de DRAGER-rij uit Z48 die het pad mogelijk maakt), kern_codes (de fantasieën die het pad echt maakt, de LOT-rij, het
# tijdperkverhaal), en een met de hand geschreven premisse. De bestaande regels bewaken het: R-verhaal_afstand (min. 3 van 7 assen verschillend
# binnen een tijdperk), R-premisse_vorm (geen gedeelde woordreeksen, geen invulmarkers), R-profiel_harde_lijn (volwassen, ja, wereldregel).
# Alles VOORSTEL (ideeënbank). Gebruik (vanuit wereld/): python3 r_Z49.py && python3 velmara.py tekst && python3 velmara.py toets && python3 velmara.py kaart
import sqlite3, os, sys, collections, subprocess, hashlib, itertools
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z49'; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter()
T = {9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)'}
ASSEN = ['positie', 'genre', 'schaal', 'volk', 'vorm', 'afloop', 'hoofdpersoon']
G = ['g_romance', 'g_erotiek', 'g_horror', 'g_suspense', 'g_actie', 'g_intrige', 'g_komedie', 'g_tragiek']
P = [  # fase, drager, positie, genre, schaal, volk, vorm, afloop, (leeftijdsband, leeftijd, geslacht), gewichten (rom, ero, hor, sus, act, int, kom, tra), kern, premisse
 (9, 'DRAGER-Z48-gave-9', 'beslisser', 'romance', 'huis', 'mens', 'brieven', 'keert om', ('26-35', 31, 'v'), (4, 4, 0, 2, 0, 1, 1, 3),
  ['VOOR-Z46-laatste-vonk', 'KINK-Z8-29', 'LOT-Z44-gaven-mannen', 'VERHAAL-Z44-tijdperk-9'],
  'Merel erft van haar moeder een kettinkje gaveglas dat nog warm is. In brieven aan haar zus beschrijft ze hoe zij en haar man het om beurten dragen en hoe het elke maand kouder wordt. '
  'Dan ontdekt ze dat de warmte niet van een dode komt maar van een man die nog in Saelith leeft, en dat hij het glas elke nieuwe maan bijvult; ze moet kiezen tussen het glas en hem.'),
 (9, 'DRAGER-Z48-ontvangst-9', 'toeschouwer', 'komedie', 'stad', 'ishvar', 'kamerspel', 'werkt', ('36-50', 44, 'm'), (2, 3, 0, 1, 0, 1, 5, 0),
  ['RIT-nacht-duizend-lampen', 'VOOR-groep', 'LOT-Z44-zegellicht', 'VOLK-ishvar'],
  'Een Ishvar-man die de Orde altijd waardeloos noemde, omdat zijn zaad geen kracht heeft, wordt bij de eerste Vrije Ontvangst van Saelith tot hoedster gekozen: hij is de enige die niet met vonk kan pronken. '
  'In één zaal en één nacht moet hij een feest leiden waarvan niemand de regels nog weet, en hij merkt dat juist zijn gewoonheid begeerd wordt.'),
 (9, 'DRAGER-Z48-stal-9', 'betaler', 'thriller', 'rijk', 'mens', 'getuigenverslag', 'blijft verborgen', ('26-35', 34, 'm'), (1, 3, 2, 5, 1, 3, 0, 3),
  ['RIT-gemaskerde-veiling', 'VOOR-veiling', 'VOOR-Z46-stalspel', 'GEB-Z45-losbandige-jaren'],
  'In een Huis van Spel in Ambergaard speelt Tobin, twaalf jaar stalman, elke week vrijwillig de veiling na die hij vroeger echt onderging. Een getuige vertelt hoe een klant op een avond het afgesproken woord niet hoort, '
  'hoe het huis de zaak stilhoudt om zijn naam te beschermen, en hoe Tobin zelf bepaalt wat er met de klant gebeurt. Het incident is een gelabeld donker thema; al het andere spel is gekozen.'),
 (10, 'DRAGER-Z48-vleugel-10', 'ontdekker', 'survival', 'dorp', 'skerra', 'aftellen', 'faalt', ('18-25', 23, 'v'), (4, 4, 2, 4, 4, 0, 0, 4),
  ['VOOR-valparing', 'RIT-volk-skerra', 'LOT-Z44-skerra', 'VERHAAL-Z44-tijdperk-10'],
  'Ilse en Ravn hebben één zweefhuid voor twee, de vleugelhuid van Ilses grootmoeder. Op het zomerfeest springen ze samen van de klifwand, zoals hun voorouders deden, om elkaar in de val te vangen. '
  'Het verhaal telt de seconden van die sprong af, en in die seconden ontdekken ze dat de huid hen maar half houdt en dat er maar één veilig kan landen.'),
 (10, 'DRAGER-Z48-vorm-10', 'liefde tussen posities', 'romance', 'dorp', 'ves-lethi', 'jij-vorm', 'keert om', ('26-35', 29, 'v'), (5, 4, 1, 2, 0, 1, 1, 2),
  ['VOOR-vormwissel', 'RIT-volk-ves-lethi', 'LOT-Z44-ves-lethi', 'MYTHE-Z43-gedaantewisselaar'],
  'Jij hebt wisselbloed: bij volle maan ben je twee nachten een man, en daarna weer jezelf. Je geliefde weet het en wacht op die nachten; het dorp hoort een gehuil en zoekt een wolf. '
  'Als de jagers bij jullie deur staan, besluit je je niet te verstoppen, en dat verandert wat het dorp denkt dat een wolf is.'),
 (10, 'DRAGER-Z48-korf-10', 'profiteur', 'intrige', 'stad', 'kluwer', 'kasboek', 'komt uit', ('36-50', 47, 'v'), (1, 3, 0, 2, 0, 5, 2, 1),
  ['VOOR-korf', 'RIT-volk-kluwer', 'LOT-Z44-kluwers', 'INTR-Z46-10-intrige'],
  'Een Kluwer-werkster zonder korf verkoopt in Brakhaven wasnachten aan wie de korfgeur eens wil voelen, en haar kasboek wordt rijker dan dat van een huis. '
  'Uit de cijfers blijkt wat ze niemand vertelt: de was raakt op, en de families die de rechten op de laatste korf claimen, kopen haar klanten één voor één weg.'),
 (10, 'DRAGER-Z48-geheugen-10', 'beslisser', 'mysterie', 'huis', 'aelthir', 'twee stemmen', 'blijft verborgen', ('36-50', 48, 'm'), (4, 3, 1, 3, 0, 2, 0, 3),
  ['RIT-volk-aelthir', 'KINK-Z8-10', 'LOT-Z44-aelthir', 'FEE-Z37-myrrhen-ringen'],
  'Een Aelthir en een sterfelijke houtsnijder gaan samen in een feeënring liggen en laten het net hun herinneringen ruilen. Ze vertellen het in twee stemmen. '
  'Tussen zijn herinneringen vindt zij iets wat hij niet weet dat hij heeft gezien, en tussen de hare vindt hij wat Ileth ooit verkocht. Ze moeten kiezen wat ze aan de ander teruggeven.'),
 (10, 'DRAGER-Z48-zoem-10', 'vervalser', 'komedie', 'dorp', 'dhurn', 'realtime', 'werkt', ('26-35', 33, 'm'), (2, 3, 0, 1, 1, 1, 5, 0),
  ['KINK-Z8-45', 'KINK-Z8-15', 'LOT-Z44-dhurn', 'GEB-Z42-eerste-ijzer'],
  'Grom, smid met een kwart Dhurn-bloed, verkoopt zingend ijzer op de jaarmarkt, ook al weet hij de toon niet. Hij slaat maar wat. '
  'In één middag, verteld zoals het gebeurt, komen drie klanten terug om te klagen en een vierde om te bedanken, want zijn verkeerde toon blijkt beter te werken dan de echte.'),
 (10, 'DRAGER-Z48-maat-10', 'toeschouwer', 'horror', 'rijk', 'tharn', 'lijst die krimpt', 'faalt', ('18-25', 24, 'm'), (2, 3, 5, 3, 1, 2, 0, 4),
  ['VOOR-maatverschil', 'RIT-volk-tharn', 'LOT-Z44-tharn', 'UIT-VOLK-tharn'],
  'Hal is drie meter lang en heeft reuzenbloed, en aan het hof van een rijke huisvrouw staat hij op een lijst van gasten die hem willen. Hij stemt toe, eerst uit nieuwsgierigheid. '
  'De lijst wordt korter naarmate zijn botten blijven groeien, en hij ziet hoe begeerte omslaat in angst. Aan het einde staat er niemand meer op, behalve de arts die zijn geraamte wil.'),
 (10, 'DRAGER-Z48-steen-10', 'betaler', 'actie', 'stad', 'orrim', 'documenten', 'keert om', ('36-50', 41, 'v'), (2, 3, 1, 4, 5, 3, 0, 1),
  ['VOOR-versteening', 'RIT-volk-orrim', 'LOT-Z44-orrim', 'OORLOG-Z46-10-oorlog'],
  'Uit vrachtbrieven, een gestolen kaart en een getuigenis: hoe hoedster Ennika de laatste voorraad Orrim-stof uit een belegerde groeve smokkelt naar haar badhuis, waar de beeldnachten worden gehouden. '
  'De Orrim van wie de stof is, staan stil in de groeve en kunnen niet zeggen of ze het willen; Ennika vraagt het hun toch, en wacht.'),
 (10, 'DRAGER-Z48-storm-10', 'ontdekker', 'actie', 'wereld', 'karrûk', 'ballade', 'komt uit', ('26-35', 27, 'v'), (3, 4, 0, 2, 5, 1, 1, 2),
  ['RIT-volk-karruk', 'KINK-Z8-18', 'LOT-Z44-karruk-storm', 'VOLK-karrûk-Z6-Z38'],
  'In een ballade van de Amberpas: een Karrûk-vechtster wint het jaarlijkse gevecht, en in de tent erna ontdekt ze dat haar kampioen geen vonk meer heeft om te ontladen. '
  'Ze blijven toch tot de ochtend, en het lied vertelt hoe de clans na die nacht het gevecht en de tent houden, zonder de Storm die het ooit nodig maakte.'),
 (11, 'DRAGER-Z48-gave-11', 'beslisser', 'horror', 'huis', 'myrrhen', 'dagboek', 'faalt', ('36-50', 38, 'v'), (2, 4, 5, 3, 0, 1, 0, 4),
  ['VOOR-sporenroes', 'KINK-Z8-55', 'LOT-Z44-gaven-mannen', 'VERHAAL-Z44-tijdperk-11'],
  'Een heelster op de Nevel-eilanden houdt een dagboek bij van de sporennachten die ze met haar geliefde deelt, omdat de sporen geven wat de vonk vroeger gaf. '
  'Elke week staan er minder dingen in die ze zich herinnert, en op een dag leest ze haar eigen beschrijving van een vrouw die ze niet meer kent: zichzelf.'),
 (11, 'DRAGER-Z48-zee-11', 'liefde tussen posities', 'survival', 'wereld', 'sael-mor', 'wij-vorm', 'werkt', ('26-35', 30, 'm'), (4, 4, 1, 3, 3, 0, 1, 1),
  ['RIT-volk-saelmor', 'LOT-Z44-sael-mor', 'VOLK-sael-mor', 'VERHAAL-Z44-tijdperk-11'],
  'Wij, de bemanning van een kustschip, nemen een man van het land mee naar de springtijnacht ver uit de kust, omdat onze kapiteinsvrouw met havenbloed dat wil. '
  'Hij kan niet zwemmen zoals wij, en de nacht in het water wordt een strijd om hem levend door het tij te krijgen. Hij komt boven, en hij blijft.'),
 (13, 'DRAGER-Z48-ontvangst-13', 'toeschouwer', 'romance', 'dorp', 'mens', 'ballade', 'werkt', ('18-25', 20, 'v'), (5, 4, 0, 1, 0, 0, 1, 1),
  ['VOOR-Z46-vuurnacht', 'EROS-Z45-haak-8', 'LOT-Z44-zegellicht', 'VERHAAL-Z44-tijdperk-13'],
  'Een lied van het plat: Aru is twintig en staat voor het eerst bij het vuur van de kortste nacht, waar wie wil een of meer gezellen kiest. Ze kijkt alleen, de hele nacht, en wordt drie keer gevraagd. '
  'Pas tegen de ochtend vraagt ze zelf, en het lied eindigt bij het antwoord.'),
 (13, 'DRAGER-Z48-stal-13', 'profiteur', 'komedie', 'dorp', 'ishvar', 'rondes', 'keert om', ('36-50', 50, 'm'), (1, 3, 0, 1, 0, 2, 5, 0),
  ['RIT-gemaskerde-veiling', 'VOOR-handel', 'GEB-Z45-losbandige-jaren', 'VERHAAL-Z44-tijdperk-13'],
  'Bij het oogstspel biedt de zuinigste boer van het dorp zichzelf gemaskerd aan, omdat hij denkt dat niemand zal bieden en hij dan het feest gratis krijgt. Ronde na ronde gaat het bod omhoog. '
  'Aan het eind heeft het dorp een nieuw dak, en hij een nacht die hij niet had durven vragen.'),
 (13, 'DRAGER-Z48-vleugel-13', 'betaler', 'thriller', 'dorp', 'skerra', 'rechtszaak', 'komt uit', ('26-35', 32, 'v'), (2, 2, 1, 5, 2, 3, 0, 3),
  ['RIT-volk-skerra', 'VOOR-valparing', 'LOT-Z44-skerra', 'FASE-z44-mensen'],
  'Bij het klifspringfeest komt een van twee geliefden niet boven. De vrouw die wel bovenkwam, staat terecht voor de dorpsraad, want er zijn getuigen die zeggen dat ze losliet. '
  'Het proces brengt aan het licht dat het loslaten bij het oude spel hoort, en dat iemand anders het water op die plek ondieper had gemaakt.'),
 (13, 'DRAGER-Z48-vorm-13', 'beslisser', 'mysterie', 'huis', 'mens', 'zelfportret', 'blijft verborgen', ('36-50', 45, 'v'), (3, 4, 2, 3, 0, 2, 0, 3),
  ['RIT-spiegelnacht', 'VOOR-sporenroes', 'LOT-Z44-ves-lethi', 'DRAGER-Z48-gave-11'],
  'Een weduwe schildert zichzelf elke keer na een sporenspiegel, de nacht waarin ze met een lage dosis sporen in haar nieuwe geliefde haar oude man ziet. '
  'De portretten tonen een vrouw die steeds minder weet welk gezicht ze kust. Ze moet beslissen of ze de laatste schildert of verbrandt.'),
 (14, 'DRAGER-Z48-zang-14', 'liefde tussen posities', 'romance', 'wereld', 'oevrin', 'lichaam als verteller', 'faalt', ('26-35', 28, 'v'), (5, 4, 0, 2, 1, 0, 0, 4),
  ['VOOR-Z46-zang-zonder-aanraking', 'RIT-volk-oevrin', 'LOT-Z44-oevrin', 'VERHAAL-Z44-tijdperk-14'],
  'Verteld door het lichaam van een vrouw die bij laag tij in de zangpoel staat met een Oevrin-man die ze nooit zal aanraken: hoe de zang door haar huid gaat, hoe het water elke maand hoger staat. '
  'Op de laatste avond dat de poel nog bestaat, zingen ze tot het tij hem neemt, en haar lichaam weet daarna wat geen woord kan zeggen.'),
]
def code_van(p): return 'VP-' + str(p[0]) + '-' + hashlib.sha1((p[1] + p[-1]).encode()).hexdigest()[:8]
# 1. diversiteit vooraf: binnen een tijdperk op minstens 3 van 7 assen verschillend (ook tegen bestaande paden)
rij = lambda p: [p[2], p[3], p[4], p[5], p[6], p[7], f'{p[8][0]}|{p[8][2]}']
for f in T:
    eigen = [p for p in P if p[0] == f]
    for a, b in itertools.combinations(eigen, 2):
        d = sum(1 for x, y in zip(rij(a), rij(b)) if x != y)
        if d < 3: sys.exit(f'te weinig afstand ({d}) tussen {a[1]} en {b[1]}')
for p in P:
    for x in [p[1]] + p[10]:
        if not c.execute('select 1 from canon where code=?', (x,)).fetchone(): sys.exit(f'{p[1]}: {x} bestaat niet')
    if p[8][1] < 18: sys.exit('hoofdpersoon jonger dan 18')
# 2. invoegen
cols = ['code', 'run', 'fase', 'positie', 'genre', 'schaal', 'volk', 'vorm', 'afloop', 'hoofdpersoon', 'leeftijd', 'geslacht', 'partner', 'instemming', 'dwang_label'] + G + \
       ['wereldregel_code', 'kern_codes', 'herkomst', 'status', 'ideeenbank', 'drager', 'premisse', 'premisse_codes', 'reden']
for p in P:
    code = code_van(p)
    if c.execute('select 1 from verhaal_profiel where code=?', (code,)).fetchone(): continue
    dwang = 1 if 'donker thema' in p[-1] else 0
    v = [code, 'Z49', T[p[0]], p[2], p[3], p[4], p[5], p[6], p[7], f'{p[8][0]}|{p[8][2]}', p[8][1], p[8][2], 'volwassene', 'ja', dwang] + list(p[9]) + \
        ['BESLUIT-Z12-2', ';'.join([p[1]] + p[10]), 'drager (Z49): maakt fantasieën na 801 mogelijk', 'voorlopig', 1, p[1], p[-1], ';'.join(p[10]),
         'Ronde Z49: verhaalpad bij ' + p[1] + ' (architectuur/DRAGERS.md)']
    c.execute(f"insert into verhaal_profiel({','.join(cols)}) values({','.join('?' * len(cols))})", v)
    S['pad_nieuw'] += 1
    c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)', (RD, code, 'toegevoegd', 'verhaal_profiel', None, 'voorlopig', DT, 'r_Z49.py'))
afgeleid.bouw(c); c.commit()
r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
print('toets exit', r.returncode, ' | '.join(r.stdout.splitlines()[1:4]))
if r.returncode: print(r.stdout[-5000:]); sys.exit('toets faalt')
print(dict(S))
