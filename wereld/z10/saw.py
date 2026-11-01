# vallen: (naam, opbouw, regels, keuze, prijs, wending, zintuig, afst, refs)
V=[
("De Zegelklok","een gevangene wordt wakker in een kamer van zegelsteen die langzaam warm wordt","elk uur zakt een plaat; de deur opent alleen als iemand zijn eigen gave opgeeft","de gave afsnijden met de zegelmes of samen koken","een gaven-man verliest zijn vonk voor altijd","de deur was al open; de klok testte wie het eerst opgaf","hete steen, zweet, zoemen","9","GEH-zegel-Z1;TECH-REGEL;BEST-gavenmannen;HORROR-Z9-60"),
("De Kluisproef van 205","drie dieven in de kluis; de Rekenaar spreekt","beantwoord drie vragen over de Makers, fout antwoord sluit een gang","wie leest de vrouwenstem voor, en wie offert haar ogen aan de lezer","blindheid of opsluiting","de Rekenaar wilde alleen een lezer, niet de schat","koude lucht, metaalgezoem, oude stem","8","HORROR-Z9-59;ACTIE-Z9-14;BEST-makers;VOORW-Z7-registerkraai-oud"),
("Het Schuldspel van Brakhaven","schuldenaars in een zoutkelder, de vloed komt op","wie zijn schuld bekent, krijgt een trede hoger; wie liegt, laat het water stijgen","de schuld van een ander verraden voor je eigen trede","verdrinking of verraad aan je naaste","de spelmeester is de schuldeiser zelf, die wil weten wie liegt","pekel tot de kin, zout in de ogen","8","GEV-zoutkelders;STAD-brakhaven;GELD-smokkelroutes;ECO-geld"),
("De Vleesmachine","een kamer van kweekvlees die ademt en knijpt","de muren sluiten tenzij je ze voedt met je eigen vlees","een vinger, een oor, of de man naast je","zelfverminking","het vlees onthoudt wie het voedde en volgt hem","warme muren, natte adem, ijzerlucht","10","LICH-r17-vleesbrug;BODY-Z8-1;BEST-gilden;HORROR-Z9-9"),
("Het Orde-verhoor met de zandloper","een verdachte vastgebonden voor een tribunaal van één inspectrice","bij elke leugen stroomt zout zand op de borst; bij elke waarheid wordt een geliefde gehaald","de waarheid zeggen en een ander verraden of liegen en stikken","stikken of verraad","de inspectrice kent de waarheid al; ze test loyaliteit","zand, gekraak van ribben","8","RECHT-tribunaal;ORDE-stille-hand;GEV-kerkers-saelith;WET-wetten-straffen"),
("De Leegtetrap","een trap van twaalf treden in het Leegtehuis","elke trede vraagt een dag zaadkracht; boven wacht de uitgang","verder klimmen tot de Leegte je vreet of terugkeren naar de cel","de Leegte: koud, hol, zonder verlangen","boven is een spiegel waarin je ziet wat de Leegte van je maakte","holle maag, kou van binnen","9","PLEK-LICH-leegtehuis;LICH-leegteziekte;MAGIE-kracht-duur;HORROR-Z9-8"),
("De Wortelstoel","een stoel van levende wortel in het Jongenshof","de wortel groeit in de ruggengraat; wie spreekt, wordt losgelaten","spreek de naam van een rebel en word vrij","verraad of vergroeiing met de Wortel","de stoel ademt met de stem van Thalen","schors die zacht als huid wordt","10","HORROR-Z9-1;PER-thalen;PLEK-LICH-jongenshof;BEST-rebellen"),
("De Spiegelzaal van Kharvos","acht spelers in het Spiegelhuis, één spiegel is een deur","elke spiegel die je breekt, snijdt je; de echte deur bloedt niet","breken tot je bloedt of samenwerken met je vijand","snijwonden, bloedverlies","de deur is de spiegel van wie zich het eerst opofferde","glas, kou, eigen adem","8","PLEK-kharvos-spiegelhuis;REG-kharvos-B1;ACTIE-Z9-23;BEST-kharvos"),
("Het Lampenspel","een volwassen lampenwaker in een donkere crypte met één lamp","de lamp brandt op zijn eigen bloed; zonder licht komen de stille handen","bloeden voor licht of in het donker wachten","bloedverlies","de stille handen zijn de vorige spelers","olie, bloed, tasten in het donker","9","SEKTE-lampenwakers;HORROR-Z9-51;LICH-stille-handen;PLEK-LICH-lampenfeest"),
("De Groeveklem","twee mijnwerkers in de Sterrensteen-groeve, één steen klemt hun benen","de steen laat los als één de ander een herinnering schenkt","je eigen moeders naam vergeten of je maat laten sterven","geheugenverlies","de steen bewaart de herinneringen en spreekt ze later uit","ozon, gruis dat bloedt, hartslag in rots","9","HORROR-Z9-15;GEB-sterrensteen-val;ACTIE-Z9-35;BESLUIT-Z7-LIORA-KRACHT"),
]
# spelmeesters: (naam, wie in canon, psychologie, motief, refs)
M=[
("Meesteres Quill Vaarloos","voormalig registermeesteres in Saelith, ontslagen na een registerfout die een gezin kapotmaakte","ziet zichzelf als boekhouder van de moraal; elke val is een balans","bewijzen dat iedereen zijn eigen schuld kan dragen","BEST-register;PLEK-saelith-registerkelder;STAD-saelith;BEST-corruptie"),
("De Rekenaar","de Maker-machine in de kluis van 205","geen haat, alleen berekening: wie kiest correct?","een geschikte lezer vinden die de toestemming terugzet","HORROR-Z9-59;BEST-makers;GEB-zegel;VOORW-Z7-registerkraai-oud"),
("Broeder Halm","een uitgestoten Wortelbroeder met half vergroeide hand","gelooft dat lijden zuivert; hij huilt bij elke val","de Wortel voeden zodat Thalen sterft","SEKTE-wortelbroeders;PER-thalen;HORROR-Z9-2;PLEK-LICH-jongenshof"),
("Inspectrice Morra Dhal","Orde-inspectrice van de Stille Hand","geniet van de keuze, niet van de pijn","loyaliteit meten voor de Orde","ORDE-stille-hand;BEST-geheim-stillehand;RECHT-tribunaal;OORLOG-Z9-44"),
("De Zoutweduwe","schuldeiseres in Brakhaven, verloor haar man aan een smokkelaar","wraak verpakt als rechtvaardigheid","laten zien dat schulden met vlees betaald worden","STAD-brakhaven;GEV-zoutkelders;LICH-weduwhuid;GELD-smokkelroutes"),
]
# skeletten (titel, hoofdpersoon, opbouw, climax, einde, refs)
S=[
("Twaalf treden","een veteranen-krijgsvrouw (34) in het Leegtehuis","ze klimt dag na dag, ziet wat de Leegte maakt","de laatste trede: ze geeft haar laatste kracht aan een medegevangene","ze komt eruit, hol, met een missie tegen de Orde","PLEK-LICH-leegtehuis;OORLOG-Z9-42;LICH-krijgsvrouw"),
("De balans van Quill","een kopiist (28) die een registerfout ontdekt","hij volgt de fout naar Quills vallen","hij moet zijn eigen fout bekennen in het schuldspel","Quill laat hem leven en maakt hem haar opvolger","BEST-register;STAD-saelith;PER-liora"),
("Kluisproef","drie heistvrouwen in de kluis van 205","de Rekenaar stelt vragen","een vrouw biedt haar ogen voor een lezer","de Rekenaar zegt: lezer gevonden. Toestemming wacht","HORROR-Z9-59;ACTIE-Z9-14;BEST-makers"),
("Vloed","Jorrit (41) in het schuldspel van de Zoutweduwe","hij moet Bram verraden of verdrinken","hij verraadt de Zoutweduwe zelf","hij komt vrij, maar met een schuld aan de Orde","PER-Z7-jorrit;GEV-zoutkelders;STAD-brakhaven"),
("De stoel die ademt","een rebellenleider (30) gevangen in het Jongenshof","de Wortelstoel groeit in zijn rug","hij spreekt een valse naam","de Wortel weet het en neemt zijn stem","HORROR-Z9-1;BEST-rebellen;PLEK-LICH-jongenshof"),
("Spiegels","acht volwassenen van verschillende volken in Kharvos","wantrouwen tussen volken","een Oevrin liegt kleur om de groep te redden","ze ontsnappen met zeven","PLEK-kharvos-spiegelhuis;VOLK-oevrin;REG-kharvos-B1"),
("Zand","een huisdochter (22) voor inspectrice Dhal","zand stroomt, haar zuster wordt gehaald","ze bekent wat ze niet deed","Dhal neemt haar op in de Stille Hand","ORDE-stille-hand;BEST-huis-varenne;RECHT-tribunaal"),
("Het vlees onthoudt","een vormmeesteres (40) in de vleesmachine","ze moet haar eigen kunst voeden","ze vormt de muur tot een deur","het vlees volgt haar naar huis","BODY-Z8-5;LICH-r17-vleesbrug;BEST-gilden"),
("Lamp","een lampenwaker (25) in de crypte","bloed voor licht","de stille handen blijken geliefden","hij blijft vrijwillig in het donker","SEKTE-lampenwakers;HORROR-Z9-51;LICH-stille-handen"),
("Klem","twee mijnwerkers (30 en 45) in de groeve","de steen vraagt herinneringen","de oudste geeft al haar herinneringen","de steen spreekt later met haar stem tegen Liora","HORROR-Z9-15;ACTIE-Z9-35;PER-liora"),
]
# losse saw-rijen (onderwerp, tekst, refs) om tot >=40 te komen
L=[
("Moraal van de speler","in elk spel is de echte vraag niet overleven maar wat je nog bent erna","LEER-zonde-boete;GOD-leegte-godheid;HORROR-Z9-8"),
("Tikkende klokken: zandlopers van zegelglas","de Orde maakt zandlopers die op lichaamswarmte lopen: hoe banger, hoe sneller","TECH-REGEL;ORDE-stille-hand;TECHNO-gave"),
("Zelfverminking als prijs: de vingerschuld","in Brakhaven betaal je een speelschuld met een vingerkootje; het register telt ze","STAD-brakhaven;BEST-register;STRAF-boete"),
("Het spelersregister","Quill houdt een boek bij van elke speler, keuze en prijs; het boek is zelf een bewijsstuk","BEST-register;RECHT-tribunaal;SEKTE-annalisten"),
("Het publiek achter het rooster","sommige spelen worden bekeken door rijke huisvrouwen die wedden","BEST-corruptie;BEST-huis-mirre;ECO-geld"),
("Orde-verhoren als spel","de Stille Hand geeft verhoren de vorm van een spel om het tribunaal te omzeilen","ORDE-stille-hand;RECHT-tribunaal;WET-wetten-straffen"),
("Zegel-vallen in Ves-Anath","de ruïnes zitten vol oude vallen die op gave reageren","PLEK-ves-anath-ruines;GEH-zegel-Z1;OORLOG-Z9-15"),
("De wet tegen spelen","spelen zijn verboden, behalve als de Orde ze leidt","WET-wetten-straffen;BEST-orde-hoofd;BEST-corruptie"),
("Overlevenden van de spelen","overlevers dragen een kerf in het oor en vormen een geheim genootschap","BEST-rebellen;LICH-tribunaalteken;STAD-brakhaven"),
("Spelen in oorlogstijd","Kharvos gebruikt spellen om krijgsgevangenen te laten kiezen tussen overlopen en sterven","OORLOG-Z9-39;REG-kharvos-B1;BEST-leger"),
]
L+=[
("De zoutbril","een bril van zoutkristal die langzaam in de ogen groeit tenzij je de naam van je opdrachtgever zegt","REG-zoutkust;BEST-geheim-stillehand;WET-smokkel"),
("Het tweelingslot","twee geliefden aan één ketting; de sleutel zit in de buik van een van hen","ROMANCE;GEV-ijskooi;HORROR-Z9-21"),
("De zaadweegschaal","een gaven-man op een weegschaal; elk uur moet hij kracht geven of een gevangene zakt in het zuur","MAGIE-zaadkracht;BEST-gavenmannen;PLEK-LICH-zaadbeurs"),
("De Wormput","spelers in een put; de Wormen volgen warmte, wie het koudst blijft leeft","HORROR-Z9-3;REG-groenmuil;NAV-wormwording"),
("De Pestkamer","een kamer die naar zoete appels ruikt; één tegengif voor drie","GEB-grote-pest;HORROR-Z9-5;TECHNO-gave-genees"),
("Het brandmerkspel","kies welk merk je draagt: dief, verrader of hoer; het merk bepaalt je nieuwe leven","STRAF-brandmerk;LICH-merkweefsel;BEST-register"),
("De ijskooi van de Aelthir","een kooi zakt in ijswater; wie de anderen opwarmt met vonk, kookt van binnen","GEV-ijskooi;VOLK-aelthir;LICH-vonkkoorts"),
("De registerkraai als scheidsrechter","een oude kraai roept na elke ronde een naam: die speler sterft","VOORW-Z7-registerkraai-oud;HORROR-Z9-57;BEST-register"),
("De bloedspiegel","de spiegel toont je dood; wie hem breekt, ruilt die met een ander","LICH-bloedspiegel;HORROR-Z9-27;PLEK-kharvos-spiegelhuis"),
("De gunstbriefloterij","duizend gunstbrieven, één is echt; de valse branden in je hand","GELD-gunstbrief-crash;ECO-prijzen-mannen-zaad;ORDE-rol-orde"),
("Het Myrrhen-sporenspel","sporen maken je eerlijk; elke leugen laat zwammen uit je mond groeien","VOLK-myrrhen;HORROR-Z9-16;LICH-r17-zwamlijk"),
("De dijkproef","een speler houdt een zegeldijk met haar lichaam dicht terwijl de stad slaapt","ACTIE-Z9-20;TECH-REGEL;REG-saelith"),
("De Karrûk-wurgkring","twee krijgers met één koord; de kring vernauwt tot één opgeeft","VOLK-karrûk;ACTIE-Z9-33;KINK-Z8-18"),
("De gave-tol","in de Stille wacht een brug die alleen opengaat voor wie een herinnering betaalt","REG-stille;BESLUIT-Z7-LIORA-KRACHT;PLEK-stille-eiland"),
("Het laatste spel van Quill","Quill zet zichzelf in de val en laat haar slachtoffers beslissen","BEST-register;RECHT-tribunaal;LEER-zonde-boete"),
]
