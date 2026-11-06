# Ronde Z48: dragers. Fantasieën mogelijk maken in elk tijdperk (opdracht van Rogier, 2 november 2026). Ontwerp en criteria: architectuur/DRAGERS.md.
# Elke drager volgt een verdwenen behoefte op (LOT-Z44-* of GEB-Z45-losbandige-jaren), leunt op een bestaande bronrij, heeft een tijdperk, een prijs en verval.
# Regels: R-drager_bron (fout), R-drager_tijd (fout), R-fantasie_onmogelijk (signaal). Alles VOORSTEL (ideeënbank). Harde lijnen gelden.
# Gebruik (vanuit wereld/, na r_Z47.py): python3 r_Z48.py && python3 velmara.py tekst && python3 velmara.py toets && python3 tijd/fantasie.py
import sqlite3, os, sys, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
DT = '2026-11-02'; RD = 'Z48'; RN = 77; DB = os.environ.get('DB', 'canon.db')
c = sqlite3.connect(DB); migreer.draai(c); S = collections.Counter(); LEVEND = ('vastgesteld', 'voorlopig')
REDEN = 'Ronde Z48: drager die een fantasie in een later tijdperk mogelijk maakt (architectuur/DRAGERS.md); geschreven vanuit de bronrijen'
T = {9: '9 Tijd van de Ja (na 801)', 10: '10 Tijd der Volken (na 801)', 11: '11 Heldentijd (na 801)', 12: '12 Het Vertrek (na 801)',
     13: '13 Tijd der Mensen (na 801)', 14: '14 De Grote Smelt (na 801)', 15: '15 Het Zwevende Gat (na 801)', 16: '16 Tijd van het Schrift (na 801)'}
F = {9: 'FASE-z44-ja', 10: 'FASE-z44-volken', 11: 'FASE-z44-helden', 12: 'FASE-z44-vertrek', 13: 'FASE-z44-mensen', 14: 'FASE-z44-smelt', 15: 'FASE-z44-gat', 16: 'FASE-z44-schrift'}
def wijz(code, soort, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
                                (RD, code, soort, veld or '', oud, str(nieuw), DT, 'r_Z48.py')).rowcount
def toets(stap):
    afgeleid.bouw(c); c.commit()
    r = subprocess.run([sys.executable, 'toets.py', DB, '--json', f'/tmp/toets_{RD}.json'], capture_output=True, text=True)
    print(f'[{stap}] toets exit {r.returncode}: ' + ' | '.join(l for l in r.stdout.splitlines()[1:5]))
    if r.returncode: print(r.stdout[-6000:]); sys.exit(f'toets faalt na {stap}')

D = [  # (behoefte-rij, korte naam, fase, bronnen, naam, tekst)
 ('LOT-Z44-gaven-mannen', 'gave', 9, ['TECHNO-MIX-V4', 'MAGIE-kracht-duur'], 'Gaveglas',
  'De laatste gaven-mannen laden zegelglas met hun vonk, en dat glas houdt een warmte vast die op de huid tintelt zoals een Ontvangst. Geliefden dragen het in een kettinkje of leggen het onder het bed. '
  'Het geeft geen kracht meer, alleen het gevoel ervan, en elke nacht wordt het iets kouder; wie eraan gewend raakt, voelt zonder glas minder. Na een paar generaties is gaveglas gewoon mooi glas.'),
 ('LOT-Z44-gaven-mannen', 'gave', 11, ['VOOR-sporenroes', 'KINK-Z8-55', 'VOLK-myrrhen-Z6'], 'Sporenroes als vonk',
  'Als het gaveglas koud is, nemen de Myrrhen-sporen het over: ingeademd maken ze alles intenser, zoals de vonk vroeger deed, en een nuchtere getuige waakt. '
  'Het is geen kracht van de Makers maar van de zwam, die geen ja nodig heeft om te groeien maar wel een ja om gedeeld te worden. De prijs zijn dagen van naweeën en soms een herinnering die wegvalt.'),
 ('LOT-Z44-zegellicht', 'ontvangst', 9, ['KETEN-kruik-ontvangst', 'RIT-nacht-duizend-lampen', 'GEB-Z45-losbandige-jaren'], 'De Vrije Ontvangst',
  'In de oude Ontvangstzalen houden volwassenen na het vertrek van de Orde hun eigen Ontvangsten, met lampen in plaats van zegellicht en een gekozen hoedster in plaats van een priesteres. '
  'Wat ooit plicht was, wordt een feest waarvoor je je opgeeft. Het verliest zijn heiligheid en zijn kracht, en de zalen worden te groot voor het aantal dat nog komt.'),
 ('LOT-Z44-zegellicht', 'ontvangst', 13, ['VOOR-Z46-vuurnacht', 'EROS-Z45-haak-8'], 'De vuurnacht',
  'Op het droge plat erft het vuur van de kortste nacht wat de Ontvangst was: kiezen, gekozen worden, een of meer gezellen, onder de sterren. Er is geen tempel en geen kracht, alleen de gewoonte. '
  'Wie vraagt waarom, krijgt een verhaal over een vrouw met een lamp. Het vuur blijft tot in onze tijd, en niemand weet nog wat het verving.'),
 ('GEB-Z45-losbandige-jaren', 'stal', 9, ['RIT-gemaskerde-veiling', 'RIT-halsbandwissel', 'KINK-sjerp-signalen'], 'De Huizen van Spel',
  'Oud-stalmeesteressen en vrijgekomen mannen openen na het Lichtconvent huizen waar de oude rollen worden gespeeld: veiling, halsband, register en rotatie, maar met contract, sjerp-signalen en een woord dat alles stopt. '
  'Wie er komt, kiest de rol die vroeger een lot was. De prijs is dat sommigen niet meer weten of ze spelen of herhalen; de huizen houden daarom een hoedster aan de deur.'),
 ('GEB-Z45-losbandige-jaren', 'stal', 13, ['RIT-gemaskerde-veiling'], 'Het oogstspel',
  'Bij de oogst verkoopt een dorp op het plat één nacht van wie zichzelf wil aanbieden, gemaskerd, zoals in Brakhaven. De opbrengst gaat naar de gemeenschap. '
  'Het is een spel geworden waarin het oude bezit alleen nog een maskerade is, en het verdwijnt pas als de laatste zaaiers vergeten zijn waarom het begon.'),
 ('LOT-Z44-skerra', 'vleugel', 10, ['VOLK-skerra', 'SEKS-VOLK-skerra-kern'], 'De zweefhuid',
  'Families met Skerra-bloed bewaren de vleugelhuid van hun moeders en grootmoeders als zweefhuid. Met zo\'n huid gespannen tussen armen en lichaam springen twee volwassenen van de klif en vangen elkaar op in de val, '
  'zoals hun voorouders paarden in vrije val. Het is gevaarlijker dan ooit, want de huid draagt maar half; elk jaar komen er minder terug. Het eindigt met de laatste huid.'),
 ('LOT-Z44-skerra', 'vleugel', 13, ['VOLK-skerra'], 'Het klifspringfeest',
  'Aan kusten met diep water springen geliefden in de zomer samen van de klif, hand in hand, en wie boven water komt, kust. Er zijn geen huiden meer, alleen het water dat hen opvangt. '
  'Het is het laatste dat er van de Val over is, en het blijft een feest tot in onze tijd.'),
 ('LOT-Z44-ves-lethi', 'vorm', 10, ['VOLK-ves-lethi-Z6', 'MYTHE-Z43-gedaantewisselaar'], 'Het wisselbloed',
  'Nazaten van Ves-Lethi en mensen wisselen niet meer van gezicht, maar bij volle maan soms nog van geslacht, een nacht of twee, en dan terug. Voor een geliefde die het weet, is dat een gave; voor een dorp dat het niet weet, een vloek. '
  'Daar komt de man vandaan die bij volle maan iets anders wordt. Het slijt per generatie, tot er alleen een gevoel van onrust bij volle maan overblijft.'),
 ('LOT-Z44-ves-lethi', 'vorm', 13, ['VOOR-sporenroes', 'RIT-spiegelnacht'], 'De sporenspiegel',
  'Met een kleine dosis Myrrhen-sporen ziet een geliefde in de ander wie ze verlangt, een gedaante die niet echt verandert maar wel zo voelt. Het is de spiegelnacht zonder Ves-Lethi. '
  'De prijs is dezelfde als vroeger: wie het te vaak doet, weet niet meer welk gezicht van de ander echt is.'),
 ('LOT-Z44-kluwers', 'korf', 10, ['VOLK-kluwer', 'SEKS-VOLK-kluwer-kern'], 'De wasnacht',
  'Als de korven uiteenvallen, blijft de honingwas. Verwarmd in een kleine kamer geeft hij een geur waarin een groep volwassenen elkaars genot half voelt, zoals vroeger in de korfgeur. '
  'Het is zwakker en korter, en de was raakt op omdat er geen Broedmoeder meer is. Wat blijft, zijn kaarsen van bijenwas in slaapkamers, en niemand weet waarom ze zo ruiken.'),
 ('LOT-Z44-aelthir', 'geheugen', 10, ['FEE-Z37-myrrhen-ringen', 'RIT-volk-aelthir'], 'Geheugenruil in de ring',
  'Twee geliefden die in een feeënring gaan liggen, laten het net van de Myrrhen hen lezen en proeven elkaars herinneringen, zoals Aelthir dat met de Nacht van de Rekening deden. '
  'Het net geeft het terug in flarden. De prijs is dat iets van jezelf in de ander blijft en iets in het net, en wie te vaak gaat, vergeet eerst geur, dan aanraking.'),
 ('LOT-Z44-dhurn', 'zoem', 10, ['GEB-Z42-eerste-ijzer', 'KINK-Z8-15'], 'Zingend ijzer',
  'Smeden met Dhurn-bloed leren ijzer zo te slaan dat het zoemt als je het aantikt, zoals de stenen van vroeger zoemden. Tegen de huid gelegd, gaat het tot in de botten. '
  'Het is gewone kunst, geen magie, en het werkt alleen zolang de smid de toon kent. Met de laatste smeden verdwijnt de toon, en het ijzer zwijgt.'),
 ('LOT-Z44-tharn', 'maat', 10, ['VOLK-tharn', 'UIT-VOLK-tharn'], 'Het reuzenbloed',
  'Er zijn families waarin elke paar generaties iemand geboren wordt die veel te groot is, met zware botten en handen als schoppen, en daar wordt gefluisterd over een Tharn-overgrootmoeder. '
  'Een volwassene met reuzenbloed wordt begeerd en gevreesd; maatverschil wordt een fantasie met een echte drager. Het zijn er steeds minder, en het laatste geraamte wordt een reus in een sage.'),
 ('LOT-Z44-orrim', 'steen', 10, ['VOLK-orrim', 'RIT-volk-orrim'], 'De beeldnacht',
  'Gemalen Orrim-stof in een warm bad maakt de huid voor een paar uur stijf en koel, zodat een volwassene stil ligt als een beeld terwijl de ander haar aanraakt, met een hoedster die het bad weer verwarmt. '
  'De stof raakt op, want de Orrim groeien niet meer. Daarna doen mensen het met klei en koud water, en dat is geen steen maar wel het spel.'),
 ('LOT-Z44-sael-mor', 'zee', 11, ['VOLK-sael-mor', 'RIT-volk-saelmor'], 'Het havenbloed',
  'In kustfamilies met Sael-mor-bloed hebben sommigen nog kieuwachtige spleten die bij springtij branden. Ze vieren de springtijnacht in het water, ver uit de kust, en voor een geliefde van het land is dat de nacht om mee te gaan. '
  'Het is gevaarlijk en het is mooi, en met elke generatie hebben minder mensen de spleten.'),
 ('LOT-Z44-oevrin', 'zang', 14, ['VOOR-Z46-zang-zonder-aanraking', 'EROS-Z45-haak-9'], 'De zangpoelen',
  'Als het slik onder zee verdwijnt, blijven er mensen die met de Oevrin zongen. Ze houden zangpoelen aan de nieuwe kust, waar geliefden bij laag tij in het water staan en zingen zonder elkaar aan te raken, tot het verlangen het werk doet. '
  'Het blijft bestaan als lied, lang nadat niemand meer weet waarvoor.'),
 ('LOT-Z44-karruk-storm', 'storm', 10, ['RIT-volk-karruk', 'VOLK-karrûk-Z6-Z38'], 'Het vuurkampgevecht',
  'De Karrûk vechten na het jaarlijkse gevecht nog steeds bij het vuur en eindigen samen in de tenten, ook zonder vonk die ontladen moet. Wat een noodzaak was, is een feest van zweet, roet en kiezen. '
  'De religie van de Storm verdwijnt; het gevecht en de nacht erna blijven, tot het een spel is op de bruiloften van hun nazaten.'),
]
def stap_dragers():
    for beh, kort, f, bron, naam, tekst in D:
        code = f'DRAGER-Z48-{kort}-{f}'
        if c.execute('select 1 from canon where code=?', (code,)).fetchone(): continue
        for x in [beh] + bron + [F[f]]:
            if not c.execute('select 1 from canon where code=?', (x,)).fetchone(): sys.exit(f'{code}: {x} bestaat niet')
        v = ';'.join([beh] + bron + [F[f]])
        c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,ideeenbank,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (code, 'Drager', naam, tekst, tekst, REDEN, 'voorlopig', RN, v, v, T[f], 1, 'voorstel (Z48, drager)'))
        S['canon_nieuw'] += 1; wijz(code, 'toegevoegd', 'canon', None, 'voorlopig (ideeënbank)')
    R = [('R-drager_bron', 'fout', 'Een drager zonder levende bronrij naast haar behoefte en fase (DRAGERS.md criterium 1).',
          "select d.code,'drager zonder bron' from drager d where not exists (select 1 from drager_bron b where b.drager=d.code) or d.behoefte is null"),
         ('R-drager_tijd', 'fout', 'Een drager bestaat eerder dan haar bron (DRAGERS.md criterium 2).',
          "select b.drager,'drager in fase '||d.fase||' vóór bron '||b.bron||' (fase '||b.bron_fase||')' from drager_bron b join drager d on d.code=b.drager where b.bron_fase is not null and d.fase is not null and d.fase<b.bron_fase"),
         ('R-fantasie_onmogelijk', 'signaal', 'Een erotische fantasie is in een tijdperk onmogelijk: zoek een drager (DRAGERS.md criterium 9).',
          "select code,'onmogelijk in fase '||fase from fantasie_status where status='onmogelijk'")]
    for code, niv, oms, sql in R:
        if not c.execute('select 1 from regel where code=?', (code,)).fetchone():
            c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
                      (code, 'tijd', oms, sql, 'Z48 (architectuur/DRAGERS.md)', f'architect Z48 ({niv})', 'actief', niv))
            S['regel_nieuw'] += 1; wijz(code, 'toegevoegd', 'regel', None, f'actief ({niv})')
    toets('dragers')
stap_dragers(); c.commit(); print(dict(S)); print(c.execute('select * from v_fantasie_matrix').fetchall())
