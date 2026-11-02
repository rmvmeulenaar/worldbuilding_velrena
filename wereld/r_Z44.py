# Ronde Z44: de lange tijd. Van de landing tot nu op één tijdas, met de tijdperken na 801 en een verhaal voor elk tijdperk en elk wezen.
# Opdracht van Rogier (2 november 2026): het verloop uitwerken (de ja komt terug, de wezens blijven eerst, dan gaat het verloren,
# richting Midden-aarde zoals Tolkien, en verder), voor alles een verhaal, en de database slim verder opbouwen.
# Bronnen: tijd/wezens.yaml (parameters met canonbron), tijd/verlies.py (simulatie + anker op de aarde), tijd/uitkomst.json.
# Alles na 801 en het anker is VOORSTEL (ideeënbank). FASE-voortijd is afgeleid uit bestaande canon (landing -1240, FASE-overvloed).
# Slim opbouwen: geen nieuwe bron; de tijdas (tijdas, tijdperk_label, v_tijdlijn) is afgeleid in afgeleid_motor.tijdas() en wordt
# gebruikt door de nieuwe signaalregel R-tijdperk_onbekend.
# Gebruik (vanuit wereld/): python3 velmara.py bouw && python3 tijd/verlies.py && python3 r_Z44.py && python3 velmara.py tekst && python3 velmara.py toets
import sqlite3, os, sys, json, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z44'; RN = 73; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
U = json.load(open('tijd/uitkomst.json'))
REDEN = 'Ronde Z44: de lange tijd (opdracht van Rogier 2026-11-02); jaren uit tijd/verlies.py, verhalen geschreven vanuit de rijen waar ze naar verwijzen'
EPI_V = 'voorstel (Z44, jaren uit simulatie tijd/verlies.py)'

def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z44.py')).rowcount
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
def nieuw(code, cat, ond, feit, verw, tijdperk, epi, ib=1, status='voorlopig'):
    if c.execute('select 1 from canon where code=?', (code,)).fetchone(): return
    for x in verw:
        if not c.execute('select 1 from canon where code=?', (x,)).fetchone(): sys.exit(f'{code}: verwijzing {x} bestaat niet')
    v = ';'.join(dict.fromkeys(lev(x) for x in verw))
    c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (code, cat, ond, feit, feit, REDEN, status, RN, v, v, tijdperk, ib, epi))
    S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, status + (' (ideeënbank)' if ib else ''))
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

A = U['anker_bp_801']; E = U['tijdperk_eind_na_801']
rond = lambda x: int(round(x / 10.0) * 10)
J = {'ja': 801 + rond(E['ja'][1]), 'volken': 801 + rond(E['volken'][1]), 'helden': 801 + rond(E['helden'][1]), 'vertrek': 801 + rond(E['vertrek'][1])}
BP801 = rond(A[1]); jaar_bp = lambda bp: 801 + BP801 - bp
J['mensen'] = jaar_bp(19000); J['smelt'] = jaar_bp(8200); J['gat'] = jaar_bp(5200); J['nu'] = jaar_bp(0)
nl = lambda n: f'{n:,}'.replace(',', '.')
T = {9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 12: '12 Het Vertrek (na 801)',
     13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)', 15: '15 Het Zwevende Gat (na 801)', 16: '16 Tijd van het Schrift (na 801)'}

# ---------- 1. de tijdas: Voortijd, anker, fasen na 801, signaalregel ----------
def stap_tijdas():
    nieuw('FASE-voortijd', 'Tijdperk', 'De Voortijd',
          '-1240 tot -600. Van de landing van het zaaischip tot de eerste koningen van de delta: de Makers, de Koude Muiterij, de stemming van 5 tegen 4, '
          'de Stille Modus van jaar 28, de val van de Sterrensteen in -480. Afgeleid uit de landing (ORIGIN-1) en het begin van de Overvloed (FASE-overvloed).',
          ['ORIGIN-1', 'FASE-overvloed', 'GEB-Z17-sterrensteen-inslag', 'BESLUIT-Z36-1'], '0 Voortijd', 'feit (afgeleid uit ORIGIN-1 en FASE-overvloed)', ib=0)
    nieuw('TIJD-anker', 'Tijdperk', 'Waar 801 op de aarde ligt',
          f'Het jaar 801 ligt op ongeveer {nl(BP801)} jaar voor heden (band {nl(A[0])} tot {nl(A[2])}), de landing dus rond {nl(BP801 + 2041)} jaar geleden. '
          'Velmara leeft in het laatste glaciale maximum, toen de zee ongeveer 120 meter lager stond, op continentaal plat dat nu onder water ligt. '
          'Zo zijn er geen sporen: de schimmel at het schip, het ijzer roestte, en de zee kwam eroverheen. De mythen moeten zijn gevormd voordat mensen Amerika in trokken, '
          'en daarna zwijgt de wereld duizenden jaren tot het eerste schrift. Geschat met tijd/verlies.py uit de canon en uit wat bekend is over ijstijd, Amerika en schrift; fantasie, aannemelijk gemaakt.',
          ['BESLUIT-Z42-1', 'ORIGIN-1', 'BESLUIT-Z11-tijdlijn'], None, EPI_V)
    F = [
        (9, 'FASE-z44-ja', f'801 tot {J["ja"]}. Na de derde weg vraagt het Zegel elk lichaam om een ja, en daarmee kan iedereen nee zeggen. In decennia schuift de verhouding van één jongen op honderd naar één op twintig, en later verder. '
            'Gaven doven per generatie, de stallen gaan open, de laatste reuzenstieren sterven, de Grauwen gaan op in de dorpen, kinderen van de Vathren worden gewone kinderen. Het tijdperk eindigt met de Doving: het laatste zegellicht in Saelith gaat uit.'),
        (10, 'FASE-z44-volken', f'{J["ja"]} tot {J["volken"]}. Zonder Zegel leven de volken nog een tijd naast elkaar, maar wat het Zegel erfelijk maakte, slijt. Skerra-kinderen komen steeds vaker zonder vleugels, Ves-Lethi houden één gezicht, '
            'de korven van de Kluwers vallen uiteen in families, en de kraaien vergeten de stem van Ysa. Kharvos houdt zijn wonderen het langst, op de kern van de Harrow, tot die kern bezwijkt bij de Val van Hoornburg.'),
        (11, 'FASE-z44-helden', f'{J["volken"]} tot {J["helden"]}. Midden-aarde: mensen zijn de meesten, de oude volken de laatsten. De Aelthir trekken zich terug in de mist, de hallen van de Dhurn lopen leeg, '
            'de laatste Tharn bewaken poorten die niemand meer aanvalt, Orrim staan stil als beelden. Helden met een restje gave zoeken de laatste werkende kluizen. Het eindigt met de Laatste Gloed: de Sterrensteen wordt een gewone grijze steen.'),
        (12, 'FASE-z44-vertrek', f'{J["helden"]} tot {J["vertrek"]}. Wat nog leeft van de Makers, gaat weg of valt stil. De laatste Leegtewormen sterven in de diepte en spoelen aan als zeeslangen, de stem in de Wortel zwijgt, '
            'en de laatste Aelthir gaan met een lander naar het Kluisschip dat nog vliegt. Het eindigt als de bewegende ster niet meer beweegt.'),
        (13, 'FASE-z44-mensen', f'{J["vertrek"]} tot {J["mensen"]}. Alleen mensen, met wat bloed van de volken in zich, en twee dingen die het Zegel nooit raakte: de Oevrin in het slik en het schimmelnet van de Myrrhen. '
            'Over het droge plat trekken families naar alle kanten, ook over de landbrug naar het oosten, en ze nemen hun verhalen mee. De geschiedenis wordt mythe.'),
        (14, 'FASE-z44-smelt', f'{J["mensen"]} tot {J["smelt"]}. Het ijs smelt en de zee stijgt ongeveer 120 meter. De delta, de Zoutkust en het slik van de Oevrin verdwijnen onder water; wat de zee neemt, is voorgoed weg. '
            'Over de oude herinnering aan de Brand en aan Ves-Anath legt zich een tweede, echte ondergang: daar komen de vloed en de verzonken stad vandaan.'),
        (15, 'FASE-z44-gat', f'{J["smelt"]} tot {J["gat"]}. Dit is het zwevende gat. Niemand weet meer wat er gebeurde; alleen vaste formules overleven het doorvertellen, zoals de prijs van het lichaam en de vrouw die opende. '
            'De eerste boeren zaaien op nieuwe kusten. Wat vreemd was, wordt vertrouwd, en de Makers worden goden.'),
        (16, 'FASE-z44-schrift', f'{J["gat"]} tot {J["nu"]}. Pas het eerste schrift legt de mythen vast: Inanna, Atrahasis, later de Grieken en de Edda. Wat er van Velmara over is, is geen steen op steen, maar herkenning: '
            'feeënringen in het gras, grijze hemelstenen, een woord dat in drie talen terugkomt. Vandaag is het ongeveer Zegeljaar ' + nl(J['nu']) + '.'),
    ]
    for f, code, tekst in F:
        nieuw(code, 'Tijdperk', T[f].split(' ', 1)[1].replace(' (na 801)', ''), tekst, ['TIJD-anker', 'BESLUIT-Z12-2'], T[f], EPI_V)
    if not c.execute("select 1 from regel where code='R-tijdperk_onbekend'").fetchone():
        c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
                  ('R-tijdperk_onbekend', 'tijd', 'Een levende rij heeft een tijdperk-label dat niet op de tijdas valt (tijdperk_label.fase is leeg).',
                   "select k.code,'tijdperk niet op de tijdas: '||k.tijdperk from canon k join tijdperk_label l on l.label=k.tijdperk where l.fase is null and k.status in ('vastgesteld','voorlopig')",
                   'Z44 (afgeleid_motor.tijdas)', 'architect Z44 (signaal)', 'actief', 'signaal'))
        S['regel_nieuw'] += 1; wijz('R-tijdperk_onbekend', 'toegevoegd', 'regel', None, 'actief (signaal)')
    toets('tijdas')

# ---------- 2. een verhaal voor elk tijdperk ----------
VT = {
 9: ('De eerste nee', ['FASE-z44-ja', 'BESLUIT-Z12-2', 'HAAK-B1-2-4', 'BESLUIT-Z6-WRIJ-077', 'DEG-stalreus'],
     'Hanne is stalmeesteres in Ambergaard als het Lichtconvent van 806 de geloften ongeldig verklaart. Haar mannen mogen nu weigeren, en de eerste die het doet, '
     'is de man die ze het meest vertrouwt. In dertig jaar zien haar dochters wat zij nooit zag: broers. Tegelijk sterven in de achterste stal de reuzenstieren, '
     'onvruchtbaar en woedend, een voor een. Ze laat de deuren openstaan. Als haar kleindochter het laatste zegellicht in Saelith ziet uitgaan, denkt ze dat het de lamp van een kapel is.'),
 10: ('De Val van Hoornburg', ['FASE-z44-volken', 'BESLUIT-3', 'ORIGIN-Z1-harrow', 'VOLK-ves-lethi-Z6', 'VOLK-skerra'],
     'Kharvos is het laatste land waar de machines nog zoemen, op de kern van de Harrow onder de burcht van Hoornburg. Ves-Lethi trekken erheen omdat hun gezicht daar nog wisselt; '
     'Skerra zonder vleugels laten zich er dragen door luchtschepen die niemand meer kan bouwen. Een Kharvos-vorstin weigert te geloven dat de kern op raakt en laat hem harder draaien. '
     'Hij bezwijkt in één nacht. Wat de overlevenden aan de kust vertellen, is het verhaal van een trots land dat de goden te veel vroeg.'),
 11: ('De laatste kluis', ['FASE-z44-helden', 'VOLK-dhurn', 'VOLK-aelthir-V5', 'UIT-VOLK-tharn', 'BESLUIT-Z4-sterrensteen'],
     'Een mensenvrouw met een vonk die nauwelijks een kaars aansteekt, een Dhurn met de laatste handen die een kluis kunnen openen, en een Aelthir die haar eigen naam aan het vergeten is, '
     'zoeken een kluis waar nog een Wiegkast zou werken. Onderweg laat een Tharn hen door een poort die al eeuwen niet meer verdedigd wordt, alleen om iemand te spreken. '
     'De kluis werkt nog één keer. Daarna gloeit de Sterrensteen niet meer, en de Dhurn weet dat zijn volk geen dochters meer zal krijgen.'),
 12: ('Het schip naar de bewegende ster', ['FASE-z44-vertrek', 'TECHNO-metaal-schip-Z42', 'YSA-Z32-6', 'OORSPRONG-bio-8'],
     'De laatste Aelthir verzamelen zich aan de kust waar een lander van de Makers ligt die nog één vlucht heeft. Een mens die ze liefheeft, mag niet mee; aan boord stopt de tijd voor wie gaat, '
     'niet voor wie blijft. In dezelfde jaren spoelen de laatste Leegtewormen aan, met lege ruimen, en zwijgt de stem in de Wortel na een laatste vraag. '
     'Als de lander opstijgt, ziet de mens de bewegende ster nog een winter lang. Dan staat hij stil.'),
 13: ('Over de landbrug', ['FASE-z44-mensen', 'VOLK-oevrin', 'FEE-Z37-myrrhen-ringen', 'VOLK-ishvar'],
     'Een familie met Ishvar-bloed en een grootmoeder die nog zingt in de akkoorden van de Oevrin trekt achter de rendieren aan, het droge plat over, naar het oosten waar de zon opkomt. '
     'Ze nemen geen voorwerpen mee, alleen verhalen: een vrouw die opende, een slang die de wereld rond voer, een man die vuur haalde. Elke winter vertellen ze ze anders. '
     'Waar ze stoppen, groeien in het gras kringen paddenstoelen, en de grootmoeder zegt dat de doden daar dansen.'),
 14: ('Het water komt', ['FASE-z44-smelt', 'VOLK-oevrin', 'BESLUIT-Z12-11', 'REG-zoutkust'],
     'Elk jaar staat het water een handbreed hoger aan de oude kust van de Zoutkust. De Oevrin merken het eerst: hun paaipoelen verzilten, hun slikgangen lopen vol. '
     'Een Oevrin-vrouw en een mensenman die samen een veer houden, moeten kiezen tussen de zee in of het land op. Achter hen verdwijnen de ruïnes van Ves-Anath onder water. '
     'Kinderen die nooit iets van de stad wisten, horen later van een stad die verzonk om haar trots, en van klokken die je nog hoort bij stil weer.'),
 15: ('De laatste die het wist', ['FASE-z44-gat', 'TAAL-dode-taal', 'ORIGIN-WAAROM-11'],
     'In een dorp aan een nieuwe kust leeft een oude vrouw die drie woorden kent waarvan niemand de betekenis weet: ysa, kern, wieg. Ze zingt ze bij elke geboorte. '
     'Haar kleinzoon vraagt wat ze betekenen; ze weet het niet meer, alleen dat je ze moet zeggen. Na haar dood zingt hij ze verkeerd, en zijn dochter maakt er een godin van. '
     'Zo verdwijnt het laatste wat een mens van de Makers wist, en zo begint het eerste geloof.'),
 16: ('Een grijze steen in een museum', ['FASE-z44-schrift', 'BESLUIT-Z42-1', 'MYTHE-Z43-hemelsteen', 'MYTHE-Z43-feeen'],
     'In onze tijd beschrijft een geologe een grijze steen uit een kraterveld die breekt als glas en die geen bekende inslag verklaart. Haar moeder hield vroeger kippen in een tuin vol feeënringen '
     'en had een vonk die nooit iemand geloofde. Op een avond legt de geologe de steen op tafel en hoort, zacht, een klik aan het eind van een zin die ze niet verstaat. '
     'Ze schrijft het op en gooit het weg. De lezer weet beter.'),
}
def stap_verhalen():
    for f, (titel, verw, tekst) in VT.items():
        nieuw(f'VERHAAL-Z44-tijdperk-{f}', 'Verhaal', titel, tekst, verw, T[f], 'voorstel (Z44, verhaal bij het tijdperk)')
    toets('verhalen tijdperken')

# ---------- 3. een verhaal voor elk wezen: hoe het verdwijnt ----------
def j(n, k='legende'):
    b = U['wezens'][n][k]; return None if b is None else 801 + rond(b[1])
def fase_van(jaar):
    if jaar is None: return T[16]
    for f, k in ((9, 'ja'), (10, 'volken'), (11, 'helden'), (12, 'vertrek'), (13, 'mensen'), (14, 'smelt'), (15, 'gat')):
        if jaar <= J[k]: return T[f]
    return T[16]
LOT = {
 'reuzenstieren': (['DEG-stalreus', 'MYTHE-Z43-minotaurus', 'MYTHE-Z43-stal-van-de-goden'],
    lambda: f'Als de stallen opengaan, blijft één stalknecht bij de reuzenstieren die niet weg kunnen, te groot voor elke weg. Ze zijn onvruchtbaar en sterven jong, en rond {j("reuzenstieren")} is de laatste dood. '
            'Hij begraaft hem in de gang onder de oude stal. Eeuwen later vindt iemand daar een schedel die te groot is voor een stier, in een doolhof van gangen.'),
 'vathren': (['VOLK-vathren-Z6', 'MYTHE-Z43-vloek-op-zonen'],
    lambda: f'Een Vathren-ziener die het Zegel altijd als hartslag voelde, hoort het na 801 zachter worden. Haar zoon voelt niets meer en lacht erom. Rond {j("vathren")} leeft er niemand meer die een lek kan voorspellen. '
            'Ze rouwt om een stem die haar pijn deed, en weet niet of dat verlies of genezing is.'),
 'zegellicht': (['PLEK-Z4-saelith-1', 'MYTHE-Z43-vampier', 'MYTHE-Z43-heilig-huwelijk'],
    lambda: f'In de Ontvangstzaal van Saelith trekt het zegellicht elk jaar minder warmte uit je vingers. De laatste priesteres die het nog onderhoudt, zit er rond {j("zegellicht")} alleen. '
            'Op de nacht dat het uitgaat, is de zaal voor het eerst warm. Wat ze eraan overhoudt, is de gewoonte om niemand binnen te laten die niet gevraagd is.'),
 'gaven-mannen': (['BESLUIT-Z12-2', 'MAGIE-kracht-duur', 'MYTHE-Z43-dondergod', 'MYTHE-Z43-held-taken'],
    lambda: f'Een oude stormman uit de Barsten leeft lang genoeg om zijn kleinzoon een vonk te zien geven die nog net een kaars aansteekt. Elke generatie geeft minder, want alleen gegeven kracht blijft. '
            f'Rond {j("gaven-mannen")} is een stormman iets uit liederen; de laatste die de bliksem nog in zijn handen voelde, wordt in de bergen een god genoemd.'),
 'grauwen': (['VOLK-grauwen'],
    lambda: f'Zonder register is er niemand meer die de Grauwen uitsluit. Een Grauwen-dorpsraad besluit zich niet langer apart te houden, en binnen een paar generaties trouwen hun kinderen overal. '
            f'Rond {j("grauwen")} weet niemand meer welk dorp ooit Grauw was. Het is het enige volk waarvan het verdwijnen een overwinning is.'),
 'karruk-storm': (['VOLK-karrûk-Z6-Z38', 'MYTHE-Z43-dondergod'],
    lambda: f'De kampioen van de Karrûk vecht het jaarlijkse gevecht en merkt dat zijn vonk er niet meer is om te ontladen. De Storm-religie verliest haar reden. '
            f'Rond {j("karruk-storm")} vechten ze nog steeds elk jaar, maar alleen om de eer, en de priesters zeggen dat de Storm slaapt.'),
 'skerra': (['VOLK-skerra', 'D1-skerra-ziekte', 'MYTHE-Z43-vleugelvolk'],
    lambda: f'Een Skerra-moeder broedt een ei uit op een klif en het kind krijgt geen vleugels. Zonder Zegel slijt wat het Zegel erfelijk maakte, en elke generatie heeft er minder. '
            f'Rond {j("skerra")} vliegt de laatste. Zij die niet meer kunnen vliegen, blijven op de kliffen wonen en vertellen hun kinderen over boden die uit de hemel kwamen.'),
 'ves-lethi': (['VOLK-ves-lethi-Z6', 'MYTHE-Z43-gedaantewisselaar'],
    lambda: f'Een Ves-Lethi-spion merkt dat ze na 801 bij elke maan moeilijker van gedaante wisselt. In Kharvos lukt het nog, op de kern van de Harrow; elders blijft het lichaam staan. '
            f'Rond {j("ves-lethi")} houdt de laatste één gezicht en noemt dat rust. Haar kinderen worden geboren als jongen of meisje, en ze vertelt hun over vossen die vrouwen werden.'),
 'kluwers': (['VOLK-kluwer'],
    lambda: f'In de korven van de Kluwers sterven de darren na hun paartijd niet meer. De korf is niet meer nodig en valt langzaam uiteen in families met een eigen naam. '
            f'Rond {j("kluwers")} is er geen Broedmoeder meer. Hun honingwas blijft, en de mensen houden bijen zonder te weten waarom ze tegen de korf praten.'),
 'registerkraaien-stem': (['BESLUIT-Z7-KRAAI', 'BESLUIT-Z27-1', 'MYTHE-Z43-raven'],
    lambda: f'Elke kraaiengeneratie kopieert de stem van Ysa iets minder goed. Eerst verdwijnt de helderheid, dan de woorden, ten slotte blijft alleen de klik. '
            f'Rond {j("registerkraaien-stem")} doet geen kraai meer een stem na. Mensen zeggen nog lang dat raven de namen van de doden kennen.'),
 'aelthir': (['VOLK-aelthir-V5', 'D1-aelthir-ziekte', 'MYTHE-Z43-elfen', 'MYTHE-Z43-einde-der-magie'],
    lambda: f'Een Aelthir is vierhonderd jaar en trekt zich terug in de mist, zoals haar volk doet. Ze krijgt één kind per eeuw en er komen er niet genoeg bij. '
            f'Rond {j("aelthir")} ziet geen mens er nog een. In de mist verliezen ze geur, aanraking en naam, en wie het laatst aan een mens dacht, vertrekt met het schip naar het westen.'),
 'wiegkasten': (['TECHNO-metaal-genees', 'GENEES-heelsters', 'MYTHE-Z43-graal'],
    lambda: f'Een heelster weet een kluis waar nog een Wiegkast werkt en brengt er stervenden heen. Elke genezing kost de kern iets. '
            f'Rond {j("wiegkasten")} heelt de laatste niets meer. Wat de heelster nalaat, is een verhaal over een schaal die alleen de waardige vindt.'),
 'dhurn': (['VOLK-dhurn', 'GEB-Z42-eerste-ijzer', 'MYTHE-Z43-dwergen'],
    lambda: f'Dhurn-vrouwen worden pas vruchtbaar na een jaar bij de steen, en de steen gloeit steeds zwakker. De mijnmeesters sturen hun bloedgezanten vaker naar de mensen. '
            f'Rond {j("dhurn")} is er geen volbloed Dhurn meer. Hun ijzer blijft en hun bloed ook, in mensen die klein en taai zijn en goed zijn met een hamer.'),
 'tharn': (['VOLK-tharn', 'UIT-VOLK-tharn', 'MYTHE-Z43-reuzen'],
    lambda: f'De Tharn weten al eeuwen dat ze uitsterven en zingen er steenliederen over die uren duren. Na 801 komen er iets meer kinderen, maar niet genoeg, en de draagtijd blijft drie jaar. '
            f'Rond {j("tharn")} staat de laatste Tharn bij een poort waar niemand meer langs wil. Zijn botten blijven er liggen.'),
 'sterrensteen': (['BESLUIT-Z42-1', 'BESLUIT-Z4-sterrensteen', 'MYTHE-Z43-hemelsteen', 'MYTHE-Z43-stem-in-de-steen'],
    lambda: f'Het siliciumhart van het schip gloeit na 801 steeds minder, en met de gloed dooft alles wat erop draait. Nieuw kristal kan niemand maken. '
            f'Rond {j("sterrensteen")} is het een grijze steen die breekt als glas. Pelgrims blijven er nog eeuwen heen gaan, en weten niet meer waarvoor.'),
 'orrim': (['VOLK-orrim', 'BESLUIT-Z32-11', 'MYTHE-Z43-versteende'],
    lambda: f'Zonder Sterrensteen-stof stopt de groei in de lichamen van de Orrim. Ze slijpen elkaar nog, maar de fragmenten worden niet meer volwassen. '
            f'Rond {j("orrim")} staan de laatsten stil in hun woestijn, en mensen denken dat het beelden zijn. Soms is een beeld in de nacht warm.'),
 'leegtewormen': (['TECHNO-bio-schip', 'OORSPRONG-bio-8', 'MYTHE-Z43-draken'],
    lambda: f'Zonder navigators en zonder Makersbiologie verwilderen de laatste Leegtewormen in de diepte. Rond {j("leegtewormen")} spoelt er een aan op een kust waar niemand ze meer kent, '
            'met een leeg ruim zo groot als een zaal. Wie het geraamte ziet, vertelt over een slang die de wereld rond voer.'),
 'wortelstem': (['YSA-Z32-6', 'BESLUIT-Z12-wortelstem', 'MYTHE-Z43-afdaling-onderwereld', 'MYTHE-Z43-wereldboom'],
    lambda: f'Na de derde weg vraagt Thalens patroon aan Ysara of ze wil blijven, en ze zegt ja. Ze spreekt zolang de steen spreekt. Wie daalt nog af om te luisteren? '
            f'Rond {j("wortelstem")} hoort niemand haar meer. De plek blijft heilig: een boom op een heuvel waar mensen linten hangen.'),
 'kluisschip': (['TECHNO-metaal-schip-Z42', 'MYTHE-Z43-eiland-der-gelukzaligen', 'MYTHE-Z43-hemelvaartuig'],
    lambda: f'In de Leegte groeit geen schimmel, dus het laatste Kluisschip vliegt het langst van alles, zonder dat iemand de koers kiest. De Skerra-sterrenkijkers zagen het als een bewegende ster. '
            f'Rond {j("kluisschip")} raakt de kern op en staat de ster stil. Dan is er geen weg meer naar het westen.'),
 'sael-mor': (['VOLK-sael-mor', 'MYTHE-Z43-zwanenmaagd', 'MYTHE-Z43-zeemeermin'],
    lambda: f'De Sael-mor leven op hun schepen en brengen vreemd bloed van haven naar haven, zoals altijd. Zonder Zegel zijn ze niet meer nodig tegen inteelt, en ze mengen zich met de havenvolken. '
            f'Rond {j("sael-mor")} is hun volk opgegaan in de kustmensen. Wie een spleet in de hals heeft die bloedt op het land, heet nog lang een kind van de zee.'),
 'oevrin': (['VOLK-oevrin', 'D1-oevrin-feest', 'MYTHE-Z43-zeemeermin'],
    lambda: 'Het Zegel raakte de Oevrin nooit, en de ja verandert niets aan hun poelen. Ze blijven tot de zee stijgt in de Grote Smelt en hun slik verzilt. '
            'Daarna trekken ze de diepte in. Zeelieden blijven duizenden jaren vertellen over zang op het water bij laag tij.'),
 'myrrhen': (['VOLK-myrrhen-Z6', 'FEE-Z37-myrrhen-ringen', 'MYTHE-Z43-feeen'],
    lambda: 'Schimmel heeft geen ja nodig. Het net van de Myrrhen onthoudt wat erin sterft, ook na 801, ook na de Smelt, ook nu. '
            'De mensen van de veenhallen gaan op in de dorpen, maar het net zelf leeft nog en komt boven als kring paddenstoelen in het gras. Het is het enige van Velmara dat je vandaag nog kunt aanraken.'),
 'ishvar': (['VOLK-ishvar'],
    lambda: 'De Ishvar hadden nooit een Zegel en nooit een gave, en ze waren daar trots op. Na 801 worden de andere volken zoals zij. '
            'Het woestijnvolk dat het ijkpunt was, wordt het begin van de gewone mensheid: wie nu een eed zweert bij de zon, spreekt hun taal zonder het te weten.'),
}
def stap_wezens():
    for n, (verw, tekst) in LOT.items():
        t = tekst(); jaar = j(n) if n in U['wezens'] else None
        nieuw(f'LOT-Z44-{n}', 'Verhaal', f'Het verdwijnen: {n}', t, verw, fase_van(jaar), 'voorstel (Z44, jaren uit simulatie tijd/verlies.py)')
    toets('verhalen wezens')

for s in (sys.argv[1:] or ['tijdas', 'verhalen', 'wezens']): globals()['stap_' + s]()
c.commit(); print(dict(S)); print('jaren:', J)
