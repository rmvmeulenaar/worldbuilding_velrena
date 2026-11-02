# Ronde Z46: alles verrijken. tijd/fantasie.py toonde per tijdperk welke genres leeg zijn en welke fantasieën nog kunnen.
# Deze ronde vult de lege genrecellen van fase 9-12 en de gaten vóór 801 (Vonk, Brand, Noodtoestand), en voegt erotische fantasieën toe die pas
# na 801 kunnen bestaan. Alles VOORSTEL (ideeënbank). Harde lijnen: alleen volwassenen, altijd een ja; dwang alleen als gelabeld donker thema.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 r_Z46.py && python3 velmara.py tekst && python3 velmara.py toets && python3 tijd/fantasie.py
import sqlite3, os, sys, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z46'; RN = 75; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
REDEN = 'Ronde Z46: verrijking van lege genrecellen en fantasieën na 801 (opdracht van Rogier 2026-11-02; gaten uit tijd/fantasie.py)'
T = {2: '2 Vonk', 3: '3 Brand', 4: '4 Noodtoestand', 9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 12: '12 Het Vertrek (na 801)'}
CAT = {'horror': ('Horror', 'HORROR'), 'comedy': ('Comedy', 'COMEDY'), 'oorlog': ('Oorlog', 'OORLOG'), 'held': ('Held', 'HELD'), 'actie': ('Actie', 'ACTIE'),
       'thriller': ('Verhaal', 'THRILL'), 'intrige': ('Verhaal', 'INTR'), 'romantiek': ('Romantiek', 'ROM'), 'erotiek': ('Romantiek', 'EROS')}
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z46.py')).rowcount
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

V = [  # (fase, genre, titel, verwijzingen, tekst)
 (2, 'comedy', 'De visser die gloeit', ['VERHAAL-fase2-a-Z35', 'GEB-zaadkracht-ontdekt'],
  'Roel, de verlegen visser met een vonk van een jaar oud, gloeit als hij bloost, en hij bloost voortdurend. Op de markt van de Zoutkust weet iedereen dus wanneer hij verliefd is, en de krijgsvrouwen wedden erom. '
  'Hij probeert het te verbergen onder natte netten, onder een emmer, in een kist. Het hele dorp lacht, tot hij in een storm de boten naar huis brengt omdat hij het enige licht op zee is.'),
 (2, 'romantiek', 'De warme bron', ['VERHAAL-Z34-fase2', 'GEB-orric-vonk'],
  'Voordat Ysel en Orric drie keer worden uitgehuwelijkt, vinden ze elkaar bij een warme bron in de uitlopers, waar het water naar ijzer ruikt. Hij weet nog niet dat hij straks de storm in zijn handen heeft; zij weet niet dat ze zijn eerste en laatste keus zal zijn. '
  'Een liefdesverhaal tussen twee volwassenen, voor de wereld hen verdeelt, dat ze elkaar later op elk feest anders vertellen.'),
 (3, 'actie', 'De weigering bij de sluis', ['PERS-Z4-karruk-3-1', 'FASE-brand-Z38'],
  'In de laatste weken van de Brand krijgt de kampioen van de Karrûk het bevel van Varnath om de sluis open te zetten en het dal te laten verdrinken. Hij weigert, en moet daarna met zijn clans over de brandende pas zien te komen, '
  'terwijl Varnaths vuurmannen hen achtervolgen. Een achtervolging van drie dagen door rook en sneeuw, en een man die weet dat hij zijn naam kwijtraakt om levens te redden.'),
 (4, 'romantiek', 'De eerste gedeelde man', ['VERHAAL-fase4-Z36', 'BESLUIT-Z12-5'],
  'Edrun, de laatste koning van Saelith, wordt in jaar 14 de eerste gedeelde man van de Zoutkust-clan, en Ylva is een van de twaalf vrouwen die over hem stemt. Wat als straf begint, wordt in een winter iets anders: '
  'een man die leert vragen en vrouwen die leren dat ze nee mogen zeggen tegen wat de Deelwet hun toestaat. Erotisch en teder tussen volwassenen, met jaloezie die niemand een naam mag geven.'),
 (4, 'actie', 'Het blad dat goud waard is', ['VERHAAL-fase4-c-Z35', 'VERHAAL-fase4-d-Z40'],
  'Een rijke clan biedt Saske goud voor één blad uit het eerste register, en als ze weigert, laten ze het stelen. Ondrea en een Zoutkust-roofster jagen de dief door de nachtelijke kades van Saelith, '
  'over daken en door de sluizen, terwijl het blad in zijn jas nat wordt en de inkt begint te lopen. Wie het blad terugkrijgt, bepaalt wie de vader is van een heel huis.'),
 (9, 'horror', 'De Lijngravers die geen antwoord hebben', ['REGEL-toestemming-navigators', 'BESLUIT-Z32-11', 'BESLUIT-Z12-2'],
  'Na de derde weg vraagt het Zegel elk lichaam om een ja, ook de Lijngravers diep in de stallen. Hun vermogen om toe te stemmen is per fase verdwenen; ze kunnen niet ja zeggen en niet nee. '
  'Een heelster die ze verzorgt, merkt dat het Zegel blijft vragen, elke nacht, en dat de lichamen eronder beginnen te trillen. Donker thema: wat doe je met mensen die geen antwoord meer hebben, in een wereld die alleen nog op antwoorden draait?'),
 (9, 'comedy', 'De Registratrix zoekt werk', ['BESLUIT-Z12-5', 'FASE-z44-ja'],
  'Na het Lichtconvent heeft de Orde geen registers meer nodig, en Registratrix Hedwig, die veertig jaar elke dekking noteerde, weet niet wat ze met haar handen moet. Ze wordt koppelaarster in Ambergaard en houdt alles bij: '
  'wie met wie, hoe vaak, en met welk resultaat, tot het hele dorp haar smeekt op te houden. Ze kan het niet laten, en het dorp eigenlijk ook niet.'),
 (9, 'oorlog', 'De Bloedkerk weigert', ['SEKTE-bloedkerk', 'RIT-bloedverbinding', 'BESLUIT-Z6-WRIJ-077'],
  'De kerk van de Bloedvorst van Lisk erkent het Lichtconvent niet: haar priesteressen zijn gebonden, en gebonden blijft gebonden, zegt de kerk. Steden die gebonden vrouwen vrijlaten, worden aangevallen. '
  'Het is de eerste oorlog over de ja zelf, en aan beide kanten vechten vrouwen. Dwang en binding zijn hier het gelabelde donkere thema; de vraag is of een vrijlating die je niet wilt ook dwang is.'),
 (9, 'held', 'De kampioen van de overlopers', ['GESCH-karrûk-6', 'VOLK-karrûk-Z6-Z38'],
  'De Karrûk die in 801 wilden overlopen, staan na de derde weg tussen twee rijken in: Kharvos noemt hen verraders, Velmara vertrouwt hen niet. Hun kampioen houdt een maand lang een smalle pas open zodat de families erdoor kunnen, '
  'terwijl zijn vonk elke dag zwakker wordt. Hij wint de pas en verliest zijn kracht, en dat is de enige prijs die hij wilde betalen.'),
 (9, 'actie', 'De race naar de Wiegkast', ['TECHNO-metaal-genees', 'TOESTAND-Z11-varenne-7', 'GENEES-heelsters'],
  'Een heelster hoort dat Huis Varenne een werkende Wiegkast laat ophalen uit een verlaten kluis in de bergen, om er genezing voor de rijken mee te verkopen. Met een smokkelaarster en een Dhurn-gids gaat ze er eerst heen. '
  'Een race door sneeuw en kluisgangen, een tweede ploeg op hun hielen, en aan het eind een machine die maar één keer meer kan genezen.'),
 (9, 'thriller', 'De vonkvervalser', ['OORSPRONG-gave-8', 'GEB-Z45-losbandige-jaren'],
  'In de Losbandige Jaren verkoopt iemand vonk aan wie de laatste vonk wil, en de kopers worden ziek. Een voormalige Stille Hand-agente, die zelf niet meer weet wat recht is, volgt het spoor van vervalste ladingen naar een stal '
  'waarvan iedereen dacht dat die al open was. Thriller: wie verdient aan het verlangen naar iets wat verdwijnt?'),
 (9, 'intrige', 'De Zoutloodsen', ['TOESTAND-Z11-ondessa-7', 'REG-zoutkust'],
  'Ondessa staat in 802 voor de keus tussen Huis Mirre en Liora. Na de derde weg wordt die keus een strijd om de Zoutloodsen, de pakhuizen waar het zaad van de kust werd bewaard en verhandeld. '
  'Wie de loodsen houdt, houdt de havens; wie ze sluit, sluit een hele economie. Intrige over schulden, zeekaarten en een oude liefde die nog niet betaald is.'),
 (10, 'horror', 'De gezichtsrot', ['LICH-r17-gezichtsrot', 'VOLK-ves-lethi-Z6', 'LOT-Z44-ves-lethi'],
  'In de Tijd der Volken lopen steeds meer Ves-Lethi vast tussen twee gezichten, omdat hun lichaam de wissel niet meer vasthoudt. Hun huid schilfert af in lagen van gedaanten. '
  'In een grensdorp sterft een spiegelzangeres die honderd gezichten heeft gedragen, en onder elke laag ligt iemand die ze ooit was. Horror van verlies: een volk dat zichzelf vergeet terwijl je kijkt.'),
 (10, 'comedy', 'De post te voet', ['VOLK-skerra', 'D1-skerra-ziekte'],
  'Een Skerra-familie zonder vleugels weigert haar koeriersrecht op te geven en bezorgt de post voortaan te voet, met ladders, katrollen en een trots die groter is dan de berg. '
  'Ze zijn trager dan elke mensenbode en zeggen dat dat de schuld van de wind is. Het hele dal betaalt hen toch, omdat niemand het hart heeft het te zeggen.'),
 (10, 'oorlog', 'De groevenoorlog', ['VOLK-dhurn', 'BESLUIT-3', 'VOLK-orrim'],
  'Als de Sterrensteen zwakker wordt, wordt elke groeve met nog wat gloed goud waard. De Dhurn hebben hem nodig voor hun vruchtbaarheid, Kharvos voor de kern van de Harrow, en de Orrim zijn zelf de groeve. '
  'Een oorlog van tunnels en ingestorte gangen, waarin het niet om land gaat maar om een licht dat toch uitgaat.'),
 (10, 'held', 'De laatste vlucht', ['VOLK-skerra', 'VERHAAL-Z44-tijdperk-10'],
  'De laatste Skerra met vleugels krijgt de opdracht de kust te waarschuwen voor wat er in Hoornburg gaat gebeuren. Haar botten zijn hol en oud, de wind staat verkeerd, en niemand na haar kan nog vliegen. '
  'Ze haalt de kust, en de havens lopen op tijd leeg. Daarna vouwt ze haar vleugels voor het laatst.'),
 (10, 'actie', 'Rijden op de waanzinnige worm', ['TECHNO-MIX-V4', 'MYTHE-Z45-kraken'],
  'Een smokkelbende neemt de laatste vleesmetaal-worm, gek van pijn door de kluiskern in zijn maag, mee door een storm naar de vrijhaven. De worm wil naar beneden, de bemanning wil naar huis. '
  'Actie op zee met touwen, haken en een navigator die moet kiezen tussen haar lading en het lijden van het dier dat haar draagt.'),
 (10, 'thriller', 'Wat de kraai zei', ['BESLUIT-Z7-KRAAI', 'LOT-Z44-registerkraaien-stem'],
  'Een registerkraai herhaalt op een markt in Brakhaven telkens dezelfde zin, met de stem van een vermoorde vrouw. Iedereen denkt dat het nog Ysa\'s klik is, tot een oude Registratrix de stem herkent. '
  'Thriller: de kraaien vergeten de stem van het schip, maar de stem van de dode van vorige week weten ze nog.'),
 (10, 'intrige', 'De korf zonder Broedmoeder', ['VOLK-kluwer', 'LOT-Z44-kluwers'],
  'Als de Broedmoeder van de grootste Kluwer-korf sterft, komt er geen nieuwe: de darren leven nu langer en de korf heeft haar niet meer nodig. De werksters splitsen in families, en elke familie wil de honingwasrechten. '
  'Intrige in geur en zang, over wie wat erft van een geheel dat er niet meer is.'),
 (11, 'horror', 'De veenlopers', ['MYTHE-Z45-ondoden', 'GESCH-myrrhen-1'],
  'Op de Nevel-eilanden lopen in de Heldentijd nog doodgezwamden rond die vergeten zijn dat ze dood zijn. Een groep reizigers zoekt schuil in een veenhal en merkt dat de bewoners niet slapen. '
  'Horror met vuur als enige uitweg, en de vraag of de lopers nog iemand zijn.'),
 (11, 'comedy', 'De laatste der laatsten', ['VOLK-tharn', 'VOLK-dhurn', 'LOT-Z44-tharn'],
  'Een Tharn en een Dhurn zitten bij dezelfde poort en ruziën al twintig jaar over wie van hen de laatste van zijn volk is. Elke reiziger moet beslissen; elke reiziger kiest verkeerd. '
  'Als er een tweede Tharn opduikt, zijn ze allebei gekwetst.'),
 (11, 'oorlog', 'De mannenlegers keren terug', ['FASE-brand-Z38', 'FASE-z44-helden', 'BESLUIT-Z11-tijdlijn'],
  'Na eeuwen zijn er weer bijna evenveel mannen als vrouwen, en voor het eerst sinds de Brand vormen koningen weer mannenlegers. Een oude krijgsvrouw die de liederen over de Vonkkoningen kent, ziet het gebeuren. '
  'Elke oplossing wordt het probleem van de volgende fase: een oorlog die rijmt met de Brand, zonder vonk maar met ijzer.'),
 (11, 'held', 'De kluiswachter', ['MYTHE-Z45-tovenaar', 'TAAL-dode-taal'],
  'Een oude vrouw kent als enige nog de drie woorden waarmee de laatste kluis opengaat. Ze loopt met een staf die alleen in haar hand licht geeft door een land in oorlog om de deur te openen voor wie er schuilen moet. '
  'Als de deur dicht is, is haar staf een stok. Daarna zien de mensen haar nooit meer.'),
 (11, 'actie', 'De instorting van de Dhurn-hal', ['VOLK-dhurn', 'LOT-Z44-sterrensteen'],
  'Als de Sterrensteen in de grote hal van de Dhurn zijn laatste gloed verliest, houden de stutten van kristal het niet meer. Een mijnmeesteres en haar bloedgezanten halen het gilde naar buiten terwijl de berg kraakt. '
  'Ze redden de mensen en verliezen de steen.'),
 (11, 'thriller', 'De jacht op het geheugen', ['VOLK-aelthir-V5', 'D1-aelthir-ziekte'],
  'Iemand ontvoert Aelthir voordat ze in de mist verdwijnen, omdat hun geheugen het enige is wat nog weet waar de kluizen liggen. Een mensenvrouw die een van hen liefheeft, volgt het spoor. '
  'Thriller: wie het verleden bezit, bezit de laatste wonderen.'),
 (11, 'intrige', 'Bloed met handen', ['VOLK-dhurn', 'LOT-Z44-dhurn', 'GEB-Z42-eerste-ijzer'],
  'Families met Dhurn-bloed hebben handen die nog net een kluis kunnen openen, en ineens wil iedereen met hen trouwen. Een nuchtere smidsdochter met Dhurn-grootmoeder krijgt zeven aanzoeken in een jaar. '
  'Intrige over huwelijk en erfenis, en over een hand die zijn waarde verliest zodra de laatste kluis zwijgt.'),
 (12, 'horror', 'De verlaten kweekpoel', ['MYTHE-Z45-hydra', 'OORSPRONG-bio-4'],
  'Na Het Vertrek verzorgt niemand meer de kweekpoelen in de Groenmuil. Wat erin groeide, groeit door, en wat je eraf snijdt, komt dubbel terug. '
  'Een dorp aan de rand van het moeras merkt dat het water elk jaar dichterbij komt, en dat er iets in zit. Horror met fakkels.'),
 (12, 'comedy', 'Waarom ga je dan?', ['VOLK-aelthir-V5', 'VERHAAL-Z44-tijdperk-12'],
  'Een Aelthir probeert een mensendorp uit te leggen waarom ze met de lander vertrekt, en elk antwoord wordt verkeerd begrepen: de dorpelingen denken eerst dat ze ruzie heeft, dan dat ze trouwt, en dan dat ze gek is. '
  'Ze vertrekt na een feest waarvan niemand weet wat het viert.'),
 (12, 'oorlog', 'De strijd om de plaatsen', ['VERHAAL-Z44-tijdperk-12', 'TECHNO-metaal-schip-Z42'],
  'Er is één lander met plaats voor weinigen, en iedereen die weet dat er een schip in de Leegte vliegt, wil mee. Een kortstondige, wrede oorlog aan de kust, '
  'waarin de Aelthir de laatste zijn die nog willen vechten, en de eersten die besluiten het niet te doen.'),
 (12, 'held', 'De laatste navigator', ['TECHNO-bio-schip', 'LOT-Z44-leegtewormen'],
  'De laatste wormnavigator weet hoe je een lander bestuurt, omdat haar handen het van haar moeder leerden. Ze brengt het schip omhoog en weet dat ze niet terug kan. '
  'Een heldin zonder lied, omdat niemand die het zag het kon navertellen.'),
 (12, 'actie', 'Lancering onder vuur', ['VERHAAL-Z44-tijdperk-12', 'OORSPRONG-bio-8'],
  'Op de ochtend van het vertrek komt een verwilderde worm uit zee naar de kust, aangetrokken door het zoemen van de lander. Terwijl de laatste passagiers aan boord gaan, houden mensen met speren en vuur hem op afstand. '
  'Actie tot de lander loskomt, en dan stilte.'),
 (12, 'thriller', 'De verstekeling', ['VERHAAL-Z44-tijdperk-12', 'VOLK-ves-lethi-Z6'],
  'Aan boord van de lander zit iemand die er niet hoort: een Ves-Lethi die nog één keer van gedaante kon wisselen en zich als Aelthir heeft voorgedaan. '
  'Thriller in de laatste uren voor de start: wie is het, en wat wil iemand die zijn volk achterlaat?'),
 (12, 'intrige', 'De Raad van de Laatsten', ['VERHAAL-Z44-tijdperk-12', 'BESLUIT-Z38-9'],
  'De vertegenwoordigers van de volken die nog bestaan, vergaderen over wie mee mag. De Myrrhen willen niet, de Oevrin kunnen niet, de mensen willen allemaal. '
  'Intrige in een raad waar iedere stem iets wil en niemand mag vragen wat een feeënvolk ervoor terug wil.'),
]
FANT = [  # erotische fantasieën die pas na 801 kunnen bestaan
 ('VOOR-Z46-de-vraag', 'De vraag zelf', 9, 'Opwinding van de vraag: na eeuwen waarin het Zegel ja zei namens ieder lichaam, is vragen en het antwoord afwachten het spannendste wat er is. Oorsprong: GEB-Z45-losbandige-jaren. Tussen volwassenen; het nee is deel van het spel.', ['GEB-Z45-losbandige-jaren', 'HAAK-B1-2-4']),
 ('VOOR-Z46-laatste-vonk', 'De laatste vonk', 9, 'Verlangen naar een kracht die verdwijnt: een nacht met iemand die nog een restje vonk heeft, wetend dat het de laatste keer is. Oorsprong: GEB-Z45-losbandige-jaren. Alleen volwassenen; de schaarste maakt het zoet en gevaarlijk.', ['GEB-Z45-losbandige-jaren', 'MAGIE-kracht-duur']),
 ('VOOR-Z46-stalspel', 'Het stalspel', 10, 'Rollenspel van de oude orde: volwassen geliefden spelen Registratrix en stalman, of Ontvangster en Uitverkorene, juist omdat het niet meer echt is. Oorsprong: FASE-z44-volken. Altijd met een afgesproken woord; een herinnering die een spel werd.', ['FASE-z44-volken', 'VOOR-dominante-vrouw']),
 ('VOOR-Z46-vervagen', 'Vervagen', 11, 'Liefde met iemand die verdwijnt: een Aelthir die de aanraking verliest, een Skerra met de laatste vleugels. Het zinnelijke zit in het tellen van wat nog kan. Oorsprong: FASE-z44-helden. Volwassenen, allebei kiezend.', ['FASE-z44-helden', 'D1-aelthir-ziekte']),
 ('VOOR-Z46-vuurnacht', 'De vuurnacht', 13, 'Kiezen bij het vuur van de kortste nacht, een of meer gezellen, een gewoonte waarvan de reden vergeten is. Oorsprong: FASE-z44-mensen. Volwassenen; de vrijheid van een feest dat niemand meer uitlegt.', ['FASE-z44-mensen', 'EROS-Z45-haak-8']),
 ('VOOR-Z46-zang-zonder-aanraking', 'Zang zonder aanraking', 14, 'Verlangen dat zingt in plaats van aanraakt, zoals het paaifeest van de Oevrin. Oorsprong: FASE-z44-smelt. Tussen volwassenen van land en zee; spanning in wat niet gebeurt.', ['FASE-z44-smelt', 'D1-oevrin-feest']),
]
def stap_verrijk():
    for f, g, titel, verw, tekst in V:
        cat, pre = CAT[g]; nieuw(f'{pre}-Z46-{f}-{g}', cat, titel, tekst, verw, T[f], f'voorstel (Z46, verrijking genre {g})')
    toets('genres')
def stap_fantasie():
    TT = {9: T[9], 10: T[10], 11: T[11], 13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)'}
    for code, ond, f, tekst, verw in FANT: nieuw(code, 'Voorkeuren', ond, tekst, verw, TT[f], 'voorstel (Z46, fantasie na 801)')
    toets('fantasieën')
for s in (sys.argv[1:] or ['verrijk', 'fantasie']): globals()['stap_' + s]()
c.commit(); print(dict(S))
