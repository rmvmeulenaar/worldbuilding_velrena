# Ronde B1: Rogier volgt alle 15 suggesties (idempotent)
import sqlite3,shutil,os,re
RONDE=29;TAG='B1';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
VR=f' [Ronde B1 {D}: vastgesteld, Rogier volgt suggestie'
if not os.path.exists('canon_backup_B1.db'): shutil.copy('canon.db','canon_backup_B1.db')
c=sqlite3.connect('canon.db');n=0;vast=[];verv=[]
def add(code,cat,ond,feit,reden,refs,tech='geen',status='voorlopig',**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar','techniek']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech]+list(kw.values()));n+=1
def F(code):
  r=c.execute("select feit from canon where code=?",(code,)).fetchone();return r[0] if r else ''
def vervang(old,new,feit,besl,status='vastgesteld'):
  r=c.execute("select categorie,onderwerp,verwijst_naar,jaar,tijdperk,functie,techniek from canon where code=?",(old,)).fetchone()
  if not r: return
  add(new,r[0],r[1],feit,f'vervangt {old} ({besl}); Rogier volgt suggestie {D}',';'.join(x for x in [old,besl,r[2] or ''] if x),tech=r[6] or 'geen',status=status,jaar=r[3],tijdperk=r[4],functie=r[5])
  if c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde {TAG}: vervangen door {new}, {besl}]',old)).rowcount: verv.append(old)
def vaststel(code,besl):
  if c.execute("update canon set status='vastgesteld', reden=reden||? where code=? and status='voorlopig'",(f'{VR} ({besl})]',code)).rowcount: vast.append(code)
def besluit(i,ond,keuze,feit,refs,tech='geen'):
  add(f'BESLUIT-{i}','Besluit',f'Besluit {i}: {ond}',f'Gekozen: {keuze}. '+feit+GR,f'Rogier volgt suggestie {D} (BESLUITEN_belangrijk nr {i})',refs,tech=tech,status='vastgesteld')
def haken(i,lst):
  for j,(fu,o,t) in enumerate(lst,1): add(f'HAAK-B1-{i}-{j}','Verhaal',f'Haak besluit {i}: {o}',t+GR,f'verhaalhaak uit BESLUIT-{i}',f'BESLUIT-{i}',functie=fu)
def vraag(q,i,a):
  c.execute("update open_vraag set status='beantwoord', antwoord=coalesce(antwoord||' ','')||? where code=? and status!='beantwoord'",(f'[B1 {D}, BESLUIT-{i}] {a}',q))
def wrij(w,i,a):
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and status!='opgelost'",(f' [Opgelost B1 {D}, BESLUIT-{i}: {a}]',w))
# 1 Zegel
besluit(1,'Wie legde het Zegel','B, de Makers bouwden het, de priesteressen ontdekten en kaapten het','De noodstand 1 op 100 werd in jaar 0 door Ysa Maren en de Makers in het zaaischip aangezet. Rond jaar 0 tot 1 verborg de machinekennis zich; ca. 800 jaar vóór 801 vonden de eerste priesteressen van Ves-Anath de bediening (de Stemklok-kamer onder de tempel) en maakten er geloof en machtsmiddel van: de "legging van het bloedzegel" is in werkelijkheid de KAPING. Twee lagen geheim: de Orde verbergt dat zij het Zegel bedient en niet bouwde; daaronder ligt Ysa\'s schuld. Verklaart waarom het Zegel op Ontvangsten in tempels draait: de priesteressen leerden de voeding via zaad, maar begrijpen de machine niet.','GEH-zegel;GEH-zegel-B1;BESLUIT-V5-ysa;ORIGIN-onthulplan-ysa','metaal+zegelsteen')
vervang('GEH-zegel','GEH-zegel-B1',F('GEH-zegel').replace('Achthonderd jaar geleden legden de eerste priesteressen in Ves-Anath een bloedzegel over het hele land: een betovering die','Het Zegel is een noodstand van het zaaischip Ysa, door de Makers in jaar 0 aangezet (BESLUIT-1). Achthonderd jaar geleden ontdekten de eerste priesteressen in Ves-Anath de bediening ervan en namen het zegel over: ze noemden het hun bloedzegel, een betovering die').replace('Kharvos ligt buiten de zegel; daarom zijn daar veel mannen.','Kharvos ligt aan de rand van de zegel en had bovendien een eigen zaaischip (BESLUIT-3).')+' Wat de Orde zegt: "wij legden het". Wat waar is: "wij vonden het en hielden het".','BESLUIT-1')
for k in ['BESLUIT-V5-ysa','ORIGIN-onthulplan-ysa','ORIGIN-3','ORIGIN-10','ORIGIN-WAAROM-11']: vaststel(k,'BESLUIT-1')
vraag('VRAAG-012',1,'Ja, als twee lagen: de Makers bouwden, de priesteressen kaapten.')
haken(1,[('THRL','De kamer onder het altaar','Een novice vindt achter het hoogaltaar een deur zonder steen: metaal, koud, met letters in de dode taal. De Hoge Moeder laat de gang dichtmetselen, met de novice erachter, tot een Zuster haar bevrijdt.'),
('INTR','De twee boeken van het Conclaaf','Het Conclaaf bewaart een tweede kroniek: "wat wij vonden". Wie die steelt, kan de Orde breken door haar alleen te laten zien dat ze niet de maker is.'),
('THRL','De bediening sleet','De priesteressen kennen maar drie handgrepen van de machine; de vierde, die het lek dicht, is vergeten. Elke Hoge Moeder probeert hem op de gok.'),
('ROM','De ketter en de archivaris','Een Orde-archivaris en een rebel (beiden volwassen) lezen samen de gekaapte kroniek; hun liefde groeit in de nachten van vertalen, en elke zin die ze vertalen maakt haar trouw aan de Orde onmogelijker.')])
# 2 Thalen
besluit(2,'Herstellen of breken','A, Thalen wil herstellen, de rebellen willen breken, Liora kiest een derde weg','Regel: bij breken doven de gaven langzaam uit (over één generatie), zodat er druk is om te kiezen. Liora\'s derde weg: de instemmingssleutel niet herstellen in het Zegel maar aan iedereen teruggeven: elke Ontvangst vraagt dan opnieuw ja; dat kost de Orde haar macht en maakt de 1 op 100 traag ongedaan. Die weg moet verdiend worden (zij moet eerst zelf kiezen zoals Ysa). Rijen die uitgaan van "zegel breken = gewonnen" vervallen als einde.','BESLUIT-V5-thalen;HAAK-V5-zegel-1;LIJN-quest','zegelsteen+metaal')
vaststel('BESLUIT-V5-thalen','BESLUIT-2')
for i in range(1,7): vaststel(f'HAAK-V5-zegel-{i}','BESLUIT-2')
vraag('VRAAG-013',2,'Ja, maar langzaam: bij breken doven de gaven over een generatie uit.')
vraag('VRAAG-019',2,'Ja, in de finale; de derde weg maakt de verborgen functie publiek.')
wrij('WRIJ-115',2,'Ysa blijft moordenares met tragisch motief; dat is een bewuste verhaalbron en spiegel van Liora\'s eindkeuze.')
haken(2,[('THRL','Het uitdoven','Na een proefbreuk bij een rebellencel verliezen de gaven-mannen in één vallei langzaam hun vonk; de Orde wijst de rebellen aan, de rebellen de Orde.'),
('INTR','De derde partij','Liora\'s derde weg maakt van haar een vijand van zowel Thalen als de rebellen; beide willen haar gebruiken als symbool en haar keuze dan zelf invullen.'),
('ROM','Aeron en de uitdovende vonk','Als de gaven uitdoven, verliest Aeron wat hem waardevol maakt; Liora moet weten of ze hem liefheeft of zijn kracht.'),
('LUST','De vraag terug','In de eerste nacht na de derde weg vraagt het Zegel twee volwassen geliefden om hun ja; de seks is trager, banger en sterker dan ooit, omdat nee nu kan.')])
# 3 Kharvos
besluit(3,'Kharvos','B, vijand na het lek, met een eigen zaaischip dat voor machines koos','Kharvos werd bevolkt door een tweede zaaischip (de Harrow) dat in de stemming voor machines koos; zijn kern dempt het Zegel aan de rand, daarom 1 op 3 jongens. Tot ca. 715 was Kharvos handelspartner (verkoop van mannen via Mirre, GEB-r10-kharvos-handel). Na het lek (718, spionnen melden het) wil Kharvos de Sterrensteen en wordt het vijand: het nieuwe jaartal van de breuk is 718-730. Kharvos blijft in boek 1 een gerucht en een grens.','REG-kharvos;REG-kharvos-B1;GEB-r10-kharvos-handel;GEB-r10-kharvos-ziet;GEB-r10-kharvos-scheiding','metaal')
vervang('REG-kharvos','REG-kharvos-B1',F('REG-kharvos').replace('(ze weten waarom niet, of houden het geheim)','(de oorzaak: een eigen zaaischip, de Harrow, dat voor machines koos; zijn kern dempt het Zegel; de vorsten houden dit geheim)').replace('Vijandig: Kharvos rooft','Tot ca. 715 handelspartner; sinds het lek (718-730) vijandig: Kharvos rooft')+' (BESLUIT-3)','BESLUIT-3')
for k in ['GEB-r10-kharvos-handel','GEB-r10-kharvos-ziet','GEB-r10-kharvos-scheiding']: vaststel(k,'BESLUIT-3')
vraag('VRAAG-016',3,'Ja, vijand, maar pas na het lek, en als spiegel met eigen zaaischip.')
vraag('VRAAG-032',3,'Tussen 718 en 730, na het lek.')
wrij('WRIJ-057',3,'Kharvos handelde tot 715 en werd vijand na het lek.')
haken(3,[('INTR','De gezant met metalen hand','Een Kharvos-gezant draagt een werkende machinehand; de Orde ziet de Harrow-kern achter zijn diplomatie.'),
('THRL','De roof van de kaartplaat','Kharvos wil de kaartplaat met de drie werelden: daarop staat waar de Harrow landde, en dat bewijst dat zijn vorsten ook kolonisten zijn.'),
('LUST','Omgekeerde macht','Een Velmaraanse gezantes (volwassen) ervaart in Kharvos voor het eerst hoe mannen begeren als zij schaars is; ze kiest bewust een minnaar en gebruikt hem als informant.'),
('ROM','Twee schepen, één bed','Een Kharvos-ingenieur en een Saelmor-kapitein (beiden volwassen) ontdekken dat hun schepen dezelfde kernmerken dragen: hun liefde is het bewijs dat beide volken van dezelfde vloot komen.')])
# 4 Boek 1
besluit(4,'Volken in boek 1','C, drie volken diep, de rest als kleur','Diep: Karrûk, Sael-mor, Aelthir. Kleur langs de route: de andere elf. Bewaard voor boek 2: Kluwers, Oevrin, Skerra.','BOEK1-scenelijn;VOLK-karrûk;VOLK-sael-mor;VOLK-aelthir-V5')
add('BOEK1-scenelijn','Verhaal','Scènelijn boek 1','Boek 1 heeft drie volken diep: Karrûk (krijgers: strijdontlading, kampkeuze, bloedeed; scènes van vuur en ontlading), Sael-mor (zee: schepen, zout, havens; reis en smokkel) en Aelthir (lang leven, geheugen, mist; het levende bewijs van de Makers). Elk volk krijgt minstens één eigen scènelijn met een intrige-, romance- en erotiekmoment. De andere volken verschijnen als kleur langs de route (één ontmoeting, één detail, geen eigen lijn). Kluwers, Oevrin en Skerra worden bewaard voor boek 2.'+GR,'Rogier volgt suggestie (BESLUIT-4)','BESLUIT-4;VOLK-karrûk;VOLK-sael-mor;VOLK-aelthir-V5',status='vastgesteld',functie='VERHAAL')
for (code,) in c.execute("select code from canon where status='voorlopig' and (code like 'SEKS-VOLK-karruk%' or code like 'SEKS-VOLK-saelmor%' or code like 'SEKS-VOLK-aelthir%')").fetchall(): vaststel(code,'BESLUIT-4')
for k in ['VOLK-karrûk','VOLK-sael-mor','VOLK-aelthir-V5']: vaststel(k,'BESLUIT-4')
c.execute("update canon set reden=reden||' [B1: later boek (BESLUIT-4)]' where status='voorlopig' and code like 'SEKS-VOLK-%' and reden not like '%later boek%'")
for q in ['VRAAG-041','VRAAG-044','VRAAG-036']: vraag(q,4,'Karrûk, Sael-mor en Aelthir diep in boek 1; alle volken blijven, de rest als kleur; Kluwers, Oevrin, Skerra in boek 2.')
# 5 Bestuur
besluit(5,'Wie regeert echt','B, dubbel bestuur','De Orde beheert zaad, register, Ontvangsten en rechtspraak over lijnen; de geregistreerde huizen beheren land, geld, leger en belasting. Geen van beide kan zonder de ander: de Orde heeft het land nodig om te eten, de huizen het register om erfgenamen te hebben. Schema: Hoge Moeder en Conclaaf ↔ Raad der Huizen; ontmoeting in de Zaadbeurs en de Raad der Moeders.','BEST-orde-hoofd;BEST-raad-moeders;BEST-huis-varenne;BEST-huis-kaldra;BEST-B1-schema')
add('BEST-B1-schema','Bestuur','Schema van het dubbele bestuur','Orde (zaad, register, Ontvangsten, lijnrecht) | Huizen (land, geld, leger, belasting). Gedeeld: de Zaadbeurs (prijs van zaadbeloften), huwelijkspolitiek, opvolging (een huis erft pas als het register de lijn erkent). Breukpunten: een huis dat zijn eigen register bijhoudt (ketterij), een Orde die land koopt (verboden).'+GR,'BESLUIT-5','BESLUIT-5;BEST-orde-hoofd;BEST-raad-moeders',status='vastgesteld',functie='POL')
for (code,) in c.execute("select code from canon where status='voorlopig' and code like 'BEST-%'").fetchall(): vaststel(code,'BESLUIT-5')
for code,f in c.execute("select code,feit from canon where status='voorlopig' and (categorie like 'Wet%' or code like 'WET-%') and (feit like '%alleen de Orde%' or feit like '%alleen de orde%')").fetchall():
  vervang(code,code+'-B1',f.replace('alleen de Orde','de Orde (over zaad en register; land en geld liggen bij de huizen, BESLUIT-5)').replace('alleen de orde','de orde (over zaad en register; land en geld bij de huizen, BESLUIT-5)'),'BESLUIT-5')
haken(5,[('INTR','Het huis met het tweede register','Huis Kaldra houdt in het geheim een eigen register bij; wie het vindt, kan het huis laten vallen of de Orde ontmaskeren als niet onmisbaar.'),
('INTR','De graanstaking','De huizen houden graan tegen tot de Orde een gaven-man vrijgeeft; de Orde antwoordt door alle Ontvangsten in hun land te schrappen.'),
('ROM','Een huwelijk tussen twee machten','Een dochter van een huis en een Orde-zuster die uittreedt (beiden volwassen) worden tot huwelijkspion gemaakt; ze kiezen elkaar echt, en dat breekt beide plannen.'),
('THRL','De moord op de beursmeester','De meester van de Zaadbeurs sterft vlak voor de prijs van zaadbeloften valt; beide machten hebben een motief.')])
# 6 Bloedafstand
besluit(6,'Bloedafstand-theorie','B, deels waar','Meer bloedafstand geeft iets meer vonk, maar echte kracht hangt ook af van vonkcellen en instemming (liefde versterkt). De Orde gelooft de theorie als officiële leer en overdrijft haar (fokpolitiek, gedwongen koppels over grenzen). De rijen met magietheorie zijn vastgesteld als "officiële leer".','VRAAG-030;VRAAG-065;GEB-r10-eerste-lek','gave+bio')
for code,f in c.execute("select code,feit from canon where status='voorlopig' and (feit like '%magietheorie%' or reden like '%magietheorie%')").fetchall():
  nf=re.sub(r'\[Hangt af van de nog niet goedgekeurde magietheorie[^\]]*\]','[Officiële leer van de Orde: bloedafstand = kracht; deels waar (BESLUIT-6).]',f)
  if nf==f: nf=f+' [Officiële leer; deels waar (BESLUIT-6).]'
  c.execute("update canon set feit=?, status='vastgesteld', reden=reden||? where code=?",(nf,f'{VR} (BESLUIT-6)]',code));vast.append(code)
vraag('VRAAG-030',6,'Deels waar; officiële leer die de Orde overdrijft.');vraag('VRAAG-065',6,'Deels waar.')
haken(6,[('INTR','De vervalste tabellen','Een rekenzuster ontdekt dat de fokcijfers van de Orde gekleurd zijn; ware cijfers tonen dat koppels met instemming sterker kinderen krijgen.'),
('ROM','Liefde als kracht','Twee verwante volwassenen, door de Orde verboden, krijgen een kind met meer vonk dan elk gedwongen koppel; hun liefde wordt bewijs en gevaar.'),
('THRL','De fokreis','De Orde stuurt een karavaan gaven-mannen naar verre volken voor "afstand"; onderweg verdwijnen ze één voor één.'),
('LUST','Gekozen tegen de leer','Een gaven-man en een vrouw uit zijn eigen lijn (beiden volwassen, niet verwant in de eerste graad) kiezen elkaar bewust; hun nacht is ketterij en het vonklicht is feller dan in de tempel.')])
# 7 Liora
besluit(7,'Liora\'s romantische eindpunt','C, Aeron als hoofdlijn, exclusieve liefde als ketterij, open einde met een prijs','Sef en Ruy blijven verleiding. Exclusieve liefde is ketterij omdat ze zaad onttrekt aan het register. Het einde blijft open en kost iets (bijvoorbeeld Aerons uitdovende vonk, BESLUIT-2).','PER-liora-profiel;PER-aeron-profiel;VRAAG-017;VRAAG-018;VRAAG-055')
for k in ['PER-liora-profiel','PER-aeron-profiel','PER-liora','PER-aeron']: vaststel(k,'BESLUIT-7')
for q in ['VRAAG-017','VRAAG-055']: vraag(q,7,'Aeron-as als hoofdlijn; open einde met prijs.')
vraag('VRAAG-018',7,'Ja, exclusieve liefde is ketterij.')
# 8 Body horror
besluit(8,'Body horror en Pest','B, schaal opnieuw ijken, de Pest kwam uit de tempelfokkerij','10 alleen op enkele plekken (Ves-Anath-gruwel, fokstallen, diepwormen). De Pest van 340 en 470 ontstond in de overvolle tempelfokstallen: de Orde is schuldig aan haar eigen ramp en noemt haar een straf voor mannen.','REGEL-walgingsschaal;LICH-pest;KOE-pestlink','bio')
vaststel('REGEL-walgingsschaal','BESLUIT-8');vaststel('KOE-pestlink','BESLUIT-8')
vervang('LICH-pest','LICH-pest-B1',F('LICH-pest')+' Oorsprong (BESLUIT-8): ontstaan in de overvolle tempelfokstallen met verwante lijnen (KOE-pestlink); de Orde verkondigt haar als straf voor mannen en verbergt dat de stallen de bron zijn.','BESLUIT-8')
for q in ['VRAAG-028','VRAAG-046']: vraag(q,8,'Schaal opnieuw geijkt; 10 alleen bij Ves-Anath, fokstallen en diepwormen.')
vraag('VRAAG-024',8,'De tempelfokkerij.')
wrij('WRIJ-050',8,'De Pest kwam uit de tempelfokkerij.');wrij('WRIJ-111',8,'Kweekstam in de tempelfokstallen; uitbraken 340 en 470 blijven.')
# 9-15
besluit(9,'Drempel terugdraaien','B, gedeeltelijk, met een prijs','De Myrrhen-zwam kan de Drempel (fase 1) gedeeltelijk terugdraaien: de wil komt terug, maar de genezene verliest jaren aan herinnering. Basis voor een smokkelthriller.','VRAAG-049;VOLK-myrrhen','bio')
vraag('VRAAG-049',9,'Gedeeltelijk, met verlies van herinnering.')
besluit(10,'Ankerwortel en Lijngravers','B, half-geheim, de naam Lijngravers blijft','De stallen weten het, het volk kent geruchten.','KOE-ankerwortel;WET-ankerwortel;VRAAG-050;VRAAG-051','bio')
vaststel('KOE-ankerwortel','BESLUIT-10');vaststel('WET-ankerwortel','BESLUIT-10')
vraag('VRAAG-050',10,'Half-geheim.');vraag('VRAAG-051',10,'Ja, Lijngravers is definitief.')
besluit(11,'Lek rond Ves-Anath','B, 1 op 60, de Orde verzwijgt het','Het volk kent alleen geruchten ("gezegende jaren"). Het lek is de klok van de thriller.','GEB-r10-eerste-lek;REGEL-verhouding','zegelsteen')
vaststel('GEB-r10-eerste-lek','BESLUIT-11');vaststel('REGEL-verhouding','BESLUIT-11')
vraag('VRAAG-033',11,'1 op 60; alleen geruchten.')
besluit(12,'Navigator in de hoofdrol','C, een hartstem als gids die halverwege worm wordt, met een lijnlezer als achtervolger','NAV-wormwording en de fasen zijn opgeschoond in NAV-wormwording-B1.','NAV-hartstem;NAV-wormwording-B1;VRAAG-038;VRAAG-045','bio+zegelsteen')
add('NAV-wormwording-B1','Navigatie','Wormwording van navigators (opgeschoond)','Een navigator die te lang in zegelschaduw, lekwater of Leegte werkt, verandert langzaam in een wormachtig wezen: het Zegel herschrijft het lichaam tot een orgaan dat zegellijnen voelt. Vijf fasen (samengevat uit NAV-wormfase-1..5): 1 gladde vochtige huid en jeuk naar de lijnen; 2 ringplooien en zachte botten, dromen in lijnen; 3 stompen en zuigmond, nog sprekend; 4 blind, tunnels langs de lijnen, alleen beelden; 5 tot 20 meter rond Ves-Anath, hoort het Zegel zelf. De quest-gids (een Vathren-hartstem) begint in fase 1 en bereikt halverwege boek 1 fase 3; de lijnlezer achtervolgt. Verzorgers zijn volwassenen; intimiteit alleen met instemming en alleen in fase 1-2, zolang de navigator nog spreekt en kan kiezen; daarna niet meer.'+GR,'opschoning (BESLUIT-12)','NAV-wormwording;NAV-wormfase-1;NAV-wormfase-5;NAV-hartstem;BESLUIT-12',tech='bio+zegelsteen',status='vastgesteld',functie='NAV',afstoting=8)
vaststel('NAV-hartstem','BESLUIT-12')
c.execute("update canon set reden=reden||' [B1: opgeschoond in NAV-wormwording-B1]' where code like 'NAV-worm%' and code!='NAV-wormwording-B1' and reden not like '%NAV-wormwording-B1%'")
vraag('VRAAG-038',12,'Hartstem als gids, lijnlezer als achtervolger.');vraag('VRAAG-045',12,'Ja, halverwege boek 1 bereikt de gids fase 3.')
besluit(13,'Superkoe-perspectief','B, korte hoofdstukken vanuit hem, vanaf boek 2','Volwassen, sprekend en denkend; de hoofdstukken tonen zijn binnenwereld en zijn verloren wil (geen seksuele scènes vanuit zijn perspectief zonder instemming).','KOE-toestemming;VRAAG-039','bio')
vraag('VRAAG-039',13,'Korte hoofdstukken vanuit hem, vanaf boek 2.')
besluit(14,'Jongenshof','A, vertrek op 6, met een niet-seksuele afscheidsrite en een zwangerschapsrite','RIT-hofproef blijft op 16 en volledig niet-seksueel.','RIT-hofproef;GEB-r10-jongenshof;RIT-B1-afscheid;RIT-B1-zwangerschap')
add('RIT-B1-afscheid','Rituelen','Het Afscheid aan de Poort (niet-seksueel)','Wie: moeder, zusters, de jongen van 6 en twee leraressen. De moeder snijdt een lok, vlecht die in een koord dat de jongen draagt; zij krijgt zijn eerste schoen terug. Bij de poort mag ze één zin zeggen die hij onthoudt. Geur van wierook en natte wol; het knarsen van de poort. Volledig niet-seksueel; schrijnende moederscènes.','BESLUIT-14','BESLUIT-14;PLEK-LICH-jongenshof',status='vastgesteld',functie='ID;HECHT')
add('RIT-B1-zwangerschap','Rituelen','De Telling van de Buik (niet-seksueel)','Wie: zwangere volwassen vrouw, haar moeder of vriendinnen, een vroedvrouw. In de vijfde maand legt de vroedvrouw zout en zaad op de buik en vraagt "jongen of dochter, wij houden van wat komt"; gezegd omdat 1 op 100 een jongen is die naar het Jongenshof gaat. Volledig niet-seksueel.','BESLUIT-14','BESLUIT-14;REGEL-verhouding',status='vastgesteld',functie='ID;REL')
vaststel('RIT-hofproef','BESLUIT-14');vaststel('GEB-r10-jongenshof','BESLUIT-14')
vraag('VRAAG-027',14,'Op 6.');vraag('VRAAG-020',14,'Ja: RIT-B1-afscheid en RIT-B1-zwangerschap.')
besluit(15,'Wortels','C, eerst gebruiken, later bevrijden met schuld','De stem in de Wortel is Ysara, de Eerste Dochter; dat verbindt de quest met de Ysa-lijn.','LIJN-quest;VRAAG-048;VRAAG-054','bio+zegelsteen')
vaststel('LIJN-quest','BESLUIT-15')
vraag('VRAAG-048',15,'Eerst gebruiken, later bevrijden, met schuld.');vraag('VRAAG-054',15,'Ja, Ysara.')
# nieuwe wrijvingen door keuzes
def nwrij(code,t,d,refs):
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,refs,d,'B1','open',code,refs))
nwrij('WRIJ-B1-1','Twee zaaischepen in één stemming?','BESLUIT-3 laat Kharvos een eigen zaaischip (Harrow) hebben; V4 zegt dat het ruim van de wormen de kern bevat van een ander zaaischip dat voor machines koos. Zijn dat dezelfde (voorstel: ja, de Harrow)?','BESLUIT-3;ORIGIN-WAAROM-12')
nwrij('WRIJ-B1-2','Priesteressen: 800 jaar geleden vs. Makers jaar 0','BESLUIT-1: er moet een gat van eeuwen zijn tussen jaar 0 en de kaping (ca. jaar 1 in jaartelling van 801?). Controleer de jaartelling: 801 min 800 = jaar 1, dus de kaping valt bijna gelijk met jaar 0; mogelijk "800 jaar" verhogen of de kaping eerder plaatsen.','BESLUIT-1;GEH-zegel-B1')
nwrij('WRIJ-B1-3','Liora\'s derde weg vs. Thalens herstel','Als de sleutel aan iedereen teruggaat, wat gebeurt er met de Dochters en Orrim in het Zegel? Moet nog bepaald.','BESLUIT-2;BESLUIT-V5-thalen')
c.execute("delete from logboek where wat like 'Ronde B1:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde B1: Rogier volgt alle 15 suggesties (1B 2A 3B 4C 5B 6B 7C 8B 9B 10B 11B 12C 13B 14A 15C). BESLUIT-1..15, BOEK1-scenelijn, haken, GEH-zegel/REG-kharvos/LICH-pest vervangen, NAV-wormwording opgeschoond, vragen en wrijvingen gesloten, 3 nieuwe wrijvingen.'))
c.commit()
print('nieuw',n,'vastgesteld',len(vast),'vervangen',verv)
