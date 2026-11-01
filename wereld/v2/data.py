def H(slug,naam,fase,t): return (slug,naam,fase,t)
VOLKEN={
'aelthir':([
 (1,"De Aelthir leven al eeuwen in de hoge wouden boven Hoogvrouwe als traag ceremonieel volk; de Sterrensteen valt in hun jeugd.","De val van de Sterrensteen.","Hun vruchtbaarheid zakt tot één kind per eeuw; ze beginnen de Rekening bij te houden.","GEB-sterrensteen-val;REG-hoogvrouwe"),
 (2,"De Oudstenraad verkoopt herinnering aan de vonkkoningen: wie wil weten hoe het vroeger was, betaalt in vreemd bloed.","Geen kinderen, dus geen toekomst; alleen geheugen is nog handelswaar.","De Aelthir worden het archief van de Vonktijd en rijk.","GEB-vonkkoningen"),
 (3,"In de Grote Brand weigeren de Aelthir partij te kiezen; brandende vonkkoningen zetten hun wouden in vuur.","Neutraliteit wordt gelezen als verraad.","Een derde van de oudsten sterft; met hen sterft geheugen dat nergens anders bestaat.","GEB-r10-brandvelden"),
 (4,"Oudste Ileth verkoopt het geheim van het Zegelleggen aan de jonge Orde in ruil voor bescherming.","Angst voor een tweede brand.","De Orde krijgt haar stichtingsverhaal; de Aelthir worden stil medeplichtig.","GEB-orde-sticht;ORDE-orde"),
 (5,"De Orde koopt in het geheim Aelthir-zaad dat de Leegte tijdelijk geneest en verbiedt tegelijk elke omgang.","Zij hebben het medicijn, de Orde de macht.","Een verborgen handel die beide kanten kan chanteren.","ORDE-financien;KETEN-isolatie"),
 (7,"In 801 herinneren nog twaalf oudsten zich de tijd vóór het Zegel; de Stille Zusters willen hun getuigenis, de Orde hun zwijgen.","Het Zegel verzwakt en het bewijs van wat het was wordt goud waard.","Elke oudste is een wandelend staatsgeheim en een doelwit.","GEB-zegel-verzwakt;REG-stille")],
 H('aelthir-held-ileth-jong','Ysmeriel van de Twaalf',7,"Jongste oudste (212 jaar); breekt de zwijgplicht en vertelt de Stille Zusters wat Ileth verkocht. Verliefd op een sterfelijke Zuster, wat haar Rekening opmaakt."),
 H('aelthir-schurk-ileth','Oudste Ileth',4,"Verkocht het Zegelgeheim aan de Orde; leeft nog in 801 en bewaakt haar leugen met gif en herinneringen die ze laat 'vergeten'.")),
'karrûk':([
 (2,"Mensen in de zegelschaduw van Kharvos krijgen opvallend veel jongens en een wilde vonk die ontladen moet.","De zwakke Zegel (nog vóór het Zegel: een zwakke plek in de Vonk zelf).","De eerste clans ontstaan rond kampioenen.","REG-kharvos;GEB-kharvos-stam"),
 (3,"Clans verhuren zich als stoottroep in de Grote Brand en leren dat kracht verkocht kan worden.","Oorlog betaalt beter dan akkers.","De Storm-religie ontstaat: kracht moet eruit, anders verbrandt hij je.","GEB-r10-brandvelden"),
 (4,"Na het Zegel kookt hun huid als ze niet vechten; de kookhuidjaren doden duizenden.","Het Zegel maakt de gave erfelijk en de vonkkoorts blijvend.","Het jaarlijkse kampioengevecht wordt verplicht ontladen.","GEB-zegel-gelegd;GEB-r10-kharvos-scheiding"),
 (6,"Kampioen Durgh verkoopt zijn eigen clanmannen als ruw zaad aan Varenne.","Honger en een belofte van wapens.","Bloedvete tussen clans die tot 801 duurt; de zwarte zaadroute ontstaat.","HUI-varenne;GEB-zaadbeurs"),
 (6,"De Orde noemt hen 'ruw vee' en verbiedt hun zaad, maar Tempelwacht koopt hen als huurlingen.","Hypocrisie: de Orde heeft spierkracht nodig.","Haat voor de 'melkers' wordt identiteit.","ORDE-tempelwacht"),
 (7,"In 801 trekken de Karrûk mee met de Kharvos-inval; een deel wil overlopen naar Velmara.","De Kharvos-heer belooft land, Velmara belooft vrouwen die kiezen.","Een verdeeld volk aan de Amberpas: perfecte grond voor verraad.","GEB-kharvos-720;GEB-kharvos-inval")],
 H('karruk-held-asha','Asha Driekerf',7,"Eerste vrouwelijke kampioen; won het gevecht van haar eigen broer en wil de zaadverkoop stoppen."),
 H('karruk-schurk-durgh','Kampioen Durgh',6,"Verkocht zijn clan; zijn kerven worden nog in 801 op verraders gekrast.")),
'dhurn':([
 (1,"Mijnwerkers van koning Orric delven de net gevallen Sterrensteen.","De steen is rijkdom en macht.","Ze verdragen straling en raken gesloten.","GEB-sterrensteen-inslag;GEB-r10-steenkoorts"),
 (2,"Orric verandert in de mijn en versteent; de Dhurn zien hem als redder.","Zijn vonk ontlaadt in de steen in plaats van in de mijnwerkers.","Orric-cultus en schuldcultuur.","GEB-orric-vonk;GEB-r10-mijnzonen"),
 (3,"Ze leveren steen aan beide kanten van de Brand en worden door beide gehaat.","Handel boven trouw.","De mijnen worden afgesloten met hun families erin.","GEB-r10-brandvelden"),
 (4,"Zonder Dhurn geen Zegelinkt: de Orde dwingt hen tot levering met hun eigen dochters als borg.","Het Zegel moet onderhouden worden.","Bittere onderwerping en verborgen sabotage.","GEB-eerste-zegellicht;ORDE-orde"),
 (6,"Mijnmeester Brakka ziet barsten in de steen en wordt het zwijgen opgelegd.","De Orde wil geen lek erkennen.","De Dhurn weten 200 jaar eerder dan wie ook dat het Zegel lekt.","KETEN-zegelproef-lek"),
 (7,"De gildenraad overweegt de levering te stoppen; dat zou het Zegel doen vallen.","Het lek is nu zichtbaar.","De machtigste stille chantage van 801.","GEB-zegel-verzwakt")],
 H('dhurn-held-brakka','Mijnmeester Brakka',6,"Schreef de barsten in steen in plaats van op papier, zodat de Orde ze niet kon verbranden."),
 H('dhurn-schurk-orvald','Gildemeester Orvald',7,"Verkoopt het lekbewijs aan de hoogste bieder, Orde of Kharvos.")),
'sael-mor':([
 (3,"Vrouwen vluchten in de Grote Brand de zee op en blijven daar.","Op land brandt alles.","Ze blijven buiten bereik van de Zegel: 1 op 20.","GEB-r10-brandvelden;REG-zoutkust"),
 (4,"Schepen leren mannen te delen en een mondeling register te zingen.","Geen papier op zee.","Hun bloed blijft schoon; zij worden de levensader tegen inteelt.","GEB-eerste-registers"),
 (5,"Bij de eerste Ontvangsten weigeren zij hun mannen af te staan.","Trouw aan het schip.","De Orde verklaart hen ketters.","GEB-eerste-ontvangst"),
 (6,"Kapitein Vessa verraadt een vloot aan de Zaadbeurs; dertig mannen worden geveild.","Schuld bij Varenne.","Het schip Vessa wordt sindsdien niet meer bij naam genoemd.","GEB-zaadbeurs;HUI-varenne"),
 (6,"Ze verkopen Grijswortel en mannen aan Mirre en worden onmisbaar en gehaat.","Geld en vrijheid.","Mirre wordt hun vaste haven.","GEB-mirre-vrijhaven;HUI-mirre"),
 (7,"In 801 roeien hun schepen lekkinderen weg van de Orde.","Mededogen en handel tegelijk.","Smokkelnetwerk dat de hoofdquest raakt.","GEB-r10-lekgeboorten;PER-saelmor-wenna")],
 H('saelmor-held-tamsin','Kapitein Tamsin Zoutvel',7,"Smokkelt lekkinderen naar Mirre; haar geliefde is een Oevrin-loods."),
 H('saelmor-schurk-vessa','Kapitein Vessa',6,"Verkocht een vloot; haar naam is een vloek.")),
'grauwen':([
 (4,"Dorpen zonder register paren binnen de eigen kring na de Noodtoestand.","De registers bereikten hen nooit.","Inteeltgebreken in één generatie: de nevenramp.","GEB-r10-neven-ramp"),
 (5,"Verstoten lampenkinderen voegen zich bij hen.","De Orde wil geen vervormden zien.","Een eigen volk met eigen tederheid.","GEB-r10-eerste-vervorming"),
 (6,"De Pest treft hen het hardst; de Orde sluit hun dalen af.","Angst voor besmetting.","Ze vereren de Vergane Zonen als voorouders.","GEB-grote-pest"),
 (6,"Ze stelen Karrûk-mannen; bloedige grensroof.","Uitgesloten van de rotatie.","Vete met de Karrûk.","GEB-r10-mannenroof"),
 (6,"De Orde gebruikt hen als preek: zo eindigt wie het register breekt.","Angst is goedkoper dan dwang.","Hun gezichten staan op tempelreliëfs.","ORDE-orde;GEB-r10-schaamte-hervorming"),
 (7,"De Stille Zusters brengen hen in 801 vreemd bloed; de Orde noemt het ketterij.","Het Zegel lekt en oude regels breken.","Een volk dat eindelijk kan genezen, of uitgeroeid wordt.","REG-stille")],
 H('grauwen-held-moeder-wrak','Moeder Wrak',7,"Dorpsraadsvrouw met dubbele irissen; leidt de Ontsluiering en onderhandelt met de Zusters."),
 H('grauwen-schurk-kael','Kael de Rover',6,"Grauwe roofleider die mannen stal en verkocht in plaats van deelde.")),
'ishvar':([
 (1,"Woestijnfamilies van Qesh drinken uit putten zonder steenstof.","Geografie.","Ze blijven gewoon: 1 op 2.","GEB-r10-qesh-afwijking;HUI-qesh"),
 (2,"Ze zien de vonkkoningen als zieken.","Geen gave, dus geen begeerte ernaar.","Trots op gewoonheid.","GEB-vonkkoningen"),
 (4,"Het Zegel raakt hen niet; ze worden een ketterij in levende lijve.","Ze bewijzen dat het Zegel niet overal is.","De Orde zwijgt hun bestaan dood.","GEB-zegel-gelegd"),
 (6,"Zonvorst Ammar levert Ishvar-vrouwen aan gaven-heren; ze krijgen brandwonden.","Hebzucht.","Eed van de families: nooit meer.","GEB-zonvorstendom"),
 (6,"Qesh gebruikt hen als geheim wapen: spionnen die geen zegellicht verraden.","Zij gloeien niet.","Qesh-spionage bloeit.","GEB-qesh-512"),
 (7,"Khaled-Ir, half Ishvar, sluit het pact.","Het Zegel lekt; gewone mannen worden waardevol.","Ishvar-mannen gezocht als rustige partners.","PER-khaled-pact;GEB-r10-khaled-pact")],
 H('ishvar-held-nouri','Nouri van de Putten',7,"Ishvar-spionne in Saelith; verliefd op een gaven-man die ze niet mag aanraken."),
 H('ishvar-schurk-ammar','Zonvorst Ammar',6,"Leverde zijn eigen volk uit; vermoord door zijn dochter.")),
'vathren':([
 (4,"Zegelgeboren jongens ontvluchten het Jongenshof en vormen een groep.","Gloeiende littekens en angst van de Orde.","Een volk van alleen mannen.","GEB-jongenshof;GEB-r10-jongenshof"),
 (5,"Ze nemen vrouwelijke gezellen op die kiezen voor de gevaarlijke nabijheid.","Liefde en nieuwsgierigheid.","Kinderen bijna allemaal zegelgeboren.","GEB-eerste-ontvangst"),
 (6,"Zieners voorspellen de Pest; niemand luistert.","Zij voelen het Zegel als hartslag.","Na de Pest worden ze gevreesd als onheilsbrengers.","GEB-grote-pest"),
 (6,"De Orde jaagt op hen; Morvane-ir zoekt ze als wapen.","Kracht zonder rem.","Ziener-raad gaat ondergronds.","KETEN-varnath-morvane"),
 (7,"Lekkinderen sinds 750 vullen het volk aan.","Het lek.","De Vathren groeien voor het eerst.","GEB-r10-lekgeboorten"),
 (7,"In 801 voorspellen ze de val van het Zegel binnen één generatie.","De hartslag zwakt.","Iedereen wil hun voorspelling.","GEB-zegel-verzwakt")],
 H('vathren-held-sorrel','Ziener Sorrel',7,"Dove ziener die het lek kan horen in zijn botten; helpt de quest."),
 H('vathren-schurk-dax','Dax Brandader',6,"Vathren die zich aan Morvane verhuurde en dorpen uitbrandde.")),
'kluwer':([
 (1,"Korven in de warme dalen, ouder dan de mensen.","Eigen evolutie.","Zijde en honing als handel.","REG-groenmuil"),
 (4,"Het Zegel doodt hun darren; de korf wordt de oplossing.","Het Zegel treft ook hen.","Broedmoeders mengen zaad: geen inteelt.","GEB-zegel-gelegd"),
 (5,"De Orde probeert de korf na te bootsen en faalt.","Jaloezie op een oplossing.","Kluwers worden geheim bewaakt.","GEB-eerste-ontvangst"),
 (6,"Honingwas geneest zaadslijtage; de stallen worden afhankelijk.","Stalnood.","Rijk en kwetsbaar.","GEB-melkstallen"),
 (6,"Een korf wordt verbrand na een vervalste beschuldiging van Pestverspreiding.","Varenne wil de prijs omlaag.","Kluwers vertrouwen niemand meer met geur.","GEB-grote-pest;HUI-varenne"),
 (7,"In 801 weigeren drie korven te leveren.","Wraak.","De stallen sterven sneller.","PER-f4-kluwer-zzak")],
 H('kluwer-held-zirr','Werkster Zirr-van-Zeven',7,"Werkster die als ik spreekt; onderhandelt namens drie korven."),
 H('kluwer-schurk-broedmoeder','Broedmoeder Vasse',6,"Broedmoeder die zaad van gestolen mensenmannen mengde.")),
'myrrhen':([
 (6,"Na de Pest van 470 laten stervenden zich overgroeien door veenzwam.","De Leegte.","Een nieuw volk met sporen.","GEB-r10-tweede-pest"),
 (6,"Het net onthoudt de doden; Zusters slaan bewijs op.","Een levend archief.","Bondgenootschap met de Stille Zusters.","REG-stille"),
 (6,"De Orde verbrandt hun bossen.","Bewijs moet weg.","Ze trekken naar de Nevel-eilanden.","GEB-r10-eilanden-weigering"),
 (7,"Spore-inenting beschermt jongens: hun geheim lekt.","Een gevangen Myrrhen praat.","Jacht op hun kinderen.","KETEN-waarheid"),
 (7,"De Orde wil de inenting stelen.","Oplossing voor het mannentekort.","Oorlog dreigt.","ORDE-conflicten"),
 (7,"In 801 dromen ze de Lampentoren en Liora.","Het net weet meer dan het zegt.","Bron voor de quest.","PER-liora")],
 H('myrrhen-held-veen','Veen-die-onthoudt',7,"Myrrhen die het bewijs van de Pest draagt."),
 H('myrrhen-schurk-rhoss','Rhoss Sporenmeester',7,"Verkoopt de inentingsformule aan de Orde.")),
'oevrin':([
 (1,"Moerasvolk met uitwendige bevruchting.","Eigen evolutie.","Evenveel mannen als vrouwen.","REG-zoutkust"),
 (3,"Ze redden vluchtelingen door het slik.","Mededogen.","Kennis van geheime watergangen.","GEB-r10-brandvelden"),
 (4,"Het Zegel raakt hen nauwelijks.","Kuit buiten het lichaam.","Ze worden een raadsel en een doelwit.","GEB-zegel-gelegd"),
 (5,"De Orde laat hun poelen vergiftigen.","Hun bestaan ondermijnt de leer.","Oevrin worden smokkelaars uit wrok.","ORDE-orde"),
 (6,"Ze trekken boten met zaad buiten de registers.","Handel en wraak.","Smokkelnet van de Zoutkust.","GEB-zaadbeurs"),
 (7,"In 801 dient de loods Glu de quest.","Vriendschap.","Oevrin bepalen welke boten aankomen.","PER-oevrin-glu")],
 H('oevrin-held-glu-moeder','Poelmoeder Kwaar',7,"Hoeder van de laatste grote broedpoel."),
 H('oevrin-schurk-slik','Slikvorst Brok',6,"Verkocht watergangen aan de Tempelwacht.")),
'tharn':([
 (1,"Reuzen bouwen de dijken van de Overvloed.","Hun kracht.","De delta bloeit.","GEB-r10-delta-dijken"),
 (2,"Vonkkoningen proberen Tharn te temmen.","Status.","De eerste Tharn-ketens.","GEB-vonkkoningen"),
 (4,"Het Zegel treft hen het hardst: één kind per vijftig jaar.","Het Zegel.","Langzaam uitsterven.","GEB-zegel-gelegd"),
 (6,"Kaldra betaalt in gaven-zaad; hun vrouwen vergiftigen.","Hoop.","Rouwliederen van uren.","HUI-kaldra;GEB-kaldra-eed"),
 (6,"Ze verraden Kaldra niet, zelfs bij de Kaldra-verraad-crisis.","Eer.","Kaldra leeft dankzij hen.","GEB-r10-kaldra-verraad"),
 (7,"Minder dan 900; ze bewaken de Amberpas.","Plicht.","Eén Tharn houdt een leger tegen.","GEB-kharvos-inval")],
 H('tharn-held-orund','Orund Littekenzang',7,"Tharn die de Amberpas houdt; draagt de hele geschiedenis in zijn huid."),
 H('tharn-schurk-gaarde','Gaarde de Ketenbreker',2,"Tharn die vonkkoningen hielp andere Tharn te ketenen.")),
'orrim':([
 (1,"Woestijnwezens ademen steenstof in.","Eigen evolutie.","Sterrensteen groeit in hun lichaam.","GEB-sterrensteen-val"),
 (3,"Vrouwen die het Zegel leggen, oogsten hun steen.","Nood.","Het Zegel bestaat uit Orrim.","GEB-dochteroffer;GEB-zegel-gelegd"),
 (4,"Dat staat in geen enkele annaal.","Schaamte.","Orrim weten het, mensen niet.","GEB-r10-vervalste-annalen"),
 (6,"Heimelijke oogst door de Orde.","Steen nodig voor merk en inkt.","Verdwijningen.","ORDE-stille-hand"),
 (6,"Orrim-recht verbiedt wraak.","Hun wet.","Mensen zien hen als stil.","KETEN-isolatie"),
 (7,"In 801 eisen ze hun voorouders terug.","Het Zegel lekt.","Als Orrim stoppen, valt het Zegel.","GEB-zegel-verzwakt")],
 H('orrim-held-sliep','Sliep-van-de-Eerste-Steen',7,"Orrim die de waarheid over het Zegel eist."),
 H('orrim-schurk-graal','Graal Steenvreter',6,"Orrim die zijn soort aan de Orde verkocht.")),
'skerra':([
 (2,"Vonkkoningen veranderen vrouwen met kliffvogel-riten.","Wens naar boodschappers.","Gevleugelden.","GEB-vonkkoningen"),
 (4,"Het Zegel maakt het erfelijk.","Het Zegel.","Een volk.","GEB-r10-gave-erfelijk"),
 (5,"Ze vliegen registers.","Snelheid.","Informatiemacht.","GEB-eerste-registers"),
 (6,"Orde en Varenne vechten om hun trouw.","Informatie.","Verdeelde nesten.","HUI-varenne"),
 (6,"Ze weigeren mannen te verkopen.","Eer.","De Orde wil hun mannen.","ORDE-conflicten"),
 (7,"In 801 dragen ze lekmeldingen.","Het lek.","Wie Skerra heeft, weet het eerst.","GEB-zegel-verzwakt")],
 H('skerra-held-kira','Kira Valvang',7,"Koerierster die een vervalst bericht onderschept."),
 H('skerra-schurk-hesk','Hesk Klifmeester',6,"Verkocht berichten aan beide kanten.")),
'ves-lethi':([
 (6,"Lichamen worden instabiel in Kharvos-grensdorpen.","Zegelschaduw.","Een vormwisselend volk.","REG-kharvos"),
 (6,"Ze spioneren voor wie betaalt.","Overleving.","Spionnenvolk.","ORDE-stille-hand"),
 (6,"Mannelijke fase is vruchtbaar: bedreiging.","Biologie.","De Orde vreest hen.","ORDE-conflicten"),
 (7,"Een Ves-Lethi wordt Orde-priester.","Infiltratie.","Schandaal.","PER-f7-veslethi-nara-oud"),
 (7,"De Orde jaagt; Kharvos koopt.","Hun vruchtbaarheid.","Oorlog om hen.","GEB-kharvos-720"),
 (7,"In 801 verliezen te veel hun gezicht.","Te vaak wisselen.","Een volk zonder vaste namen.","GEB-heden")],
 H('veslethi-held-lan','Lan-de-Twee',7,"Ves-Lethi die als man een kind verwekte en vlucht."),
 H('veslethi-schurk-mirror','De Lege Spiegel',7,"Ves-Lethi die zijn gezicht verloor en van iedereen wordt.")),
}
_I="""1|graanhuwelijk|Het dubbele graanhuwelijk|twee schuurheren en de bruid Tessel|land|Tessel trouwt beiden in het geheim|de Schuurherenvete|GEB-r10-schuurheren
1|dijkgeld|Het verzwegen dijkgeld|Tharn-dijkbouwer en een kroonschatmeester|zilver|de Tharn weet van de diefstal|de eerste Tharn-eed|GEB-r10-delta-dijken;VOLK-tharn
1|zoutgif|Het zoutgif|een zoutkoopvrouw en de kroonprins|troonopvolging|het gif zat in de bruidstaart|Zoutopstand|GEB-r10-zoutopstand
1|steenmonster|Het vervalste steenmonster|Dhurn-mijnwerker en koning Orric|mijnrecht|het monster is van Orrim-lichaam|Orric koopt woestijn|VOLK-dhurn;VOLK-orrim
1|oogstbrief|De oogstnachtbrief|een moeder en haar minnaar|afkomst|het kind is van de koning|eerste bastaardwet|GEB-r10-oogstnacht
1|aelthir-ruil|Herinnering voor bloed|Aelthir-oudste en een kroonvrouw|kennis|de herinnering is vals|kroon vertrouwt Aelthir niet|VOLK-aelthir
1|kroonhuwelijk|Het eerste kroonhuwelijk|Saelith en Ardemar|eenheid|de bruidegom is al getrouwd|Haremwet|GEB-kroon-saelith;GEB-haremwet
1|nevelmoeder|Het moederrecht van de Nevel|Nevel-moeders en de kroon|erfrecht|moederrecht blijkt ouder|Nevel blijft eigen|GEB-r10-nevel-moederrecht
1|graanmeesterzoon|De zoon van de graanmeester|graanmeester en dochter|opvolging|de zoon is een vermomde dochter|INTR-fase1-graanmeester|INTR-fase1-graanmeester
2|vonkveiling|De eerste vonkveiling|vonkkoning Varnath en kooplieden|macht|de vonk is nep|Vonkmarkt|GEB-r10-vonkmarkt
2|skerra-riten|De kliffvogel-riten|vonkkoning en klifpriesteressen|boodschappers|de vrouwen stemden in maar werden bedrogen over de prijs|Skerra ontstaan|VOLK-skerra
2|tharn-keten|De Tharn-keten|Gaarde en vonkkoning|status|Gaarde wil zelf koning worden|Tharn-scheuring|VOLK-tharn
2|vonkkoorts-gif|De vonkkoortsgifmenger|een heelster en twee vonkkoningen|wraak|de koorts was gif|Vonkpest-gerucht|GEB-vonkpest
2|zeven-kronen-bruid|De bruid van zeven kronen|een prinses en zeven koningen|vrede|zij verloofde zich met allen|Oorlog der Zeven Kronen|GEB-oorlog-zeven-kronen
2|aelthir-archief|Het verkochte archief|Aelthir en vonkkoningen|rijkdom|archief vervalst|vonkkoning verbrandt woud|VOLK-aelthir
2|zaadkruik|De eerste zaadkruik|een vrouw die kruiken verkoopt|onafhankelijkheid|de kruiken zijn van één man|zaadkruikenhandel|GEB-r10-zaadkruiken
2|karruk-huur|De eerste huurovereenkomst|Karrûk-kampioen en Lisk|land|Lisk betaalt in vals zilver|Lisk brandt later|VOLK-karrûk;GEB-val-lisk
2|mijnzonenrecht|Het recht van de mijnzonen|Dhurn en vonkkoningen|erkenning|mijnzonen zijn koningsbloed|INTR-fase1-verzwegen-zonen|VOLK-dhurn;GEB-r10-mijnzonen
3|raadsverraad|Verraad in de Raad van Ves-Anath|raadsvrouwen|het Zegelplan|een raadsvrouw speelt voor de vonkkoningen|Offer der Dochters versneld|GEB-raad-ves-anath
3|grijswortelplot|Het grijswortelplot|Mira en een vonkheer|bevrijding|de wortel verdooft niet maar maakt vrij|eerste Stille Zuster|GEB-r10-grijswortel
3|orrim-oogst|De oogst van de Orrim|Zegelmakers en Orrim|steen|Orrim stemmen in maar worden misleid over aantallen|Orrim-wrok|VOLK-orrim
3|aelthir-brand|Het woud dat brandde|Aelthir en Lisk|neutraliteit|Lisk stak zelf het vuur|Aelthir zwijgen|VOLK-aelthir
3|kruisverbond|Het kruisverbond|vrouwen van twee vijandige steden|overleven|een van hen is spionne|Kruisverbond|GEB-r10-kruisverbond
3|zoutvloot|De vloot die bleef|Sael-mor-kapiteinsvrouwen|vrijheid|een schip keert terug om te verraden|Sael-mor ontstaan|VOLK-sael-mor
3|mael|Het schisma van Mael|priesteressen|leer|Mael heeft een minnaar|Mael-schisma|GEB-r10-mael-schisma
3|lisk-overlevenden|De overlevenden van Lisk|vluchtelingen|wraak|een overlevende stak het vuur|bloedschuld|GEB-r10-lisk-overlevenden
4|deelwetstem|De stem over de Deelwet|raadsvrouwen|macht|stem gekocht met een man|Deelwet|GEB-deelwet-40
4|jongenshofrapport|Het jongenshofrapport|Orde en een opzichteres|geheim|de jongens ontvluchten|Vathren|GEB-jongenshof;VOLK-vathren
4|registerbrand|De registerbrand|schrijfster en Orde|macht|het oude register brandt niet|eerste vervalsing|GEB-eerste-registers
4|dhurn-borg|De dochters als borg|Orde en Dhurn-gilde|levering|een borg trouwt de gildemeester|Dhurn-sabotage|VOLK-dhurn
4|tharn-eed|De eed van de Tharn|Tharn en Kaldra|bescherming|Kaldra betaalt in vergif|Kaldra-eed|GEB-kaldra-eed;VOLK-tharn
4|ileth-verkoop|Ileths verkoop|Ileth en de Orde|bescherming|het geheim is half|Orde-stichtingsverhaal|PER-aelthir-schurk-ileth
4|bloedmerk|Het eerste bloedmerk|merkzetter en raad|controle|het merk kan vervalst worden|bloedmerk|GEB-r10-bloedmerk
4|laatste-koning|De laatste koning|koning en zijn vrouw|troon|zij verkoopt hem aan de Orde|einde koningschap|GEB-r10-laatste-koning
4|kluwer-korf|Het korfgeheim|Kluwer en Orde|oplossing|de Orde steelt een broedmoeder|eerste korfdiefstal|VOLK-kluwer
5|uitverkorenen|De lijst der uitverkorenen|Orde-moeders|gunst|de lijst is gekocht|Uitverkorenen|GEB-uitverkorenen
5|dankpreek|De dankpreek|Moeder Iresse|leer|preek verbergt een lek|Ontvangst geheiligd|GEB-r10-dankpreek
5|tempelbouw|De tempelbouw|bouwmeesteres en Orde|geld|stenen van Orrim|tempels|GEB-r10-tempelbouw;VOLK-orrim
5|gunstbrief|De gunstbrief|Orde en huizen|status|vervalst|gunstbrieven|GEB-r10-gunstbrief
5|oevrin-poel|De vergiftigde poel|Orde en Oevrin|leer|gif kwam van een rivaliserende clan|Oevrin-wrok|VOLK-oevrin
5|veiling-heilig|De heilige veiling|Orde en kooplieden|geld|man op veiling is gestolen|heilige veiling|GEB-r10-eerste-veiling-heilig
5|annalen|De vervalste annalen|Orde-schrijfsters|geschiedenis|één schrijfster bewaart het origineel|vervalste annalen|GEB-r10-vervalste-annalen
5|skerra-nest|Het verdeelde nest|Skerra-nesten|trouw|een nest verkoopt|nestoorlog|VOLK-skerra
5|ishvar-stilte|De doodgezwegen Ishvar|Orde|leer|een priesteres trouwt Ishvar|stilte breekt|VOLK-ishvar
6|zaadbeurs|De val van de Zaadbeurs|Varenne en Mirre|krediet|Mirre kocht schuld op|Varenne-crash|GEB-r10-varenne-crash;HUI-varenne;HUI-mirre
6|pest-qesh|De Pest uit Qesh|Qesh en Orde|schuld|Pest begon in Orde-stallen|Qesh beschuldigd|GEB-r10-pest-qesh;HUI-qesh
6|karruk-verkoop|Durghs verkoop|Durgh en Varenne|wapens|wapens waren roestig|bloedvete|PER-karruk-schurk-durgh
6|ves-anath|Ves-Anath ontruimd|Orde en raad|geheim|ontruiming verbergt lek|Ves-Anath leeg|GEB-ves-anath-ontruimd
6|weduwen|De weduwenopstand|weduwen en Orde|rechten|leidster is Orde-spionne|weduwenrecht|GEB-r10-weduwenopstand
6|kaldra-verraad|Het Kaldra-verraad|Kaldra en Kharvos|overleven|verrader is Kaldra-erfgenaam|Kaldra-crisis|GEB-r10-kaldra-verraad;HUI-kaldra
6|kluwer-brand|De verbrande korf|Varenne en Kluwers|prijs|beschuldiging vervalst|korfwrok|VOLK-kluwer
6|ammar|De dood van Ammar|Ammar en dochter|wraak|dochter wordt zonvorst|Ishvar-eed|PER-ishvar-schurk-ammar
6|myrrhen-bos|Het brandende bos|Orde en Myrrhen|bewijs|net bewaarde alles|Myrrhen-vlucht|VOLK-myrrhen
7|tribunaal|Het tribunaal|Orde en vervalsersgilde|macht|rechter is vervalser|tribunaal|GEB-r10-tribunaal
7|bloednacht|De Bloednacht van Lisk|huizen|opvolging|gastvrouw schonk gif|Bloednacht|GEB-bloednacht-788
7|orvald|Orvalds veiling|Orvald, Orde en Kharvos|geld|bewijs wordt gekopieerd|lek publiek|PER-dhurn-schurk-orvald
7|rhoss|De gestolen formule|Rhoss en Orde|macht|formule werkt alleen in het net|Orde faalt|PER-myrrhen-schurk-rhoss
7|lan|Lans kind|Lan en Orde|vrijheid|kind is gezien|jacht op Ves-Lethi|PER-veslethi-held-lan
7|asha|Asha's gevecht|Asha en broer|zaadverkoop stoppen|broer liet haar winnen|Karrûk-scheuring|PER-karruk-held-asha
7|ysmeriel|Ysmeriels getuigenis|Ysmeriel en Ileth|waarheid|Ileth vergiftigt de Zuster|Aelthir-scheuring|PER-aelthir-held-ileth-jong
7|khaled|Het pact van Khaled|Khaled-Ir en Orde|Ishvar-mannen|pact verbergt huwelijk|Qesh-Velmara|GEB-r10-khaled-pact"""
INTRIGE=[]
for l in _I.split('\n'):
  f,s,t,p,m,w,g,r=l.split('|');INTRIGE.append((s,int(f),t,p,m,w,g,r))
MAGIE=[
(1,"De Vonk vóór het Zegel","De Vonk bestond al in de Overvloed als zeldzame, wilde kracht bij enkele mannen (mijnzonen, Orric); niet erfelijk, onvoorspelbaar. Ontdekt door Dhurn-mijnwerkers die zagen dat Orric gloeide. Oorsprong blijft open (VRAAG).","GEB-orric-vonk;GEB-r10-mijnzonen"),
(2,"Zaadkracht ontdekt","Een heelster merkt dat ontvangst van vonkzaad tijdelijk kracht geeft; de vonkmarkt ontstaat.","GEB-zaadkracht-ontdekt;MAGIE-zaadkracht"),
(2,"Vonkkoorts","Wie niet ontlaadt, verbrandt; de Karrûk maken er een religie van.","GEB-vonkkoorts;VOLK-karrûk"),
(3,"Het Zegelplan","De Raad van Ves-Anath ontwerpt een Zegel met Orrim-steen en het offer van dochters (volwassen vrijwilligsters).","GEB-raad-ves-anath;GEB-dochteroffer;VOLK-orrim"),
(3,"Het Zegel gelegd (jaar 0)","De Vonk wordt gebonden; 1 op 100; de gave wordt erfelijk.","GEB-zegel-gelegd;GEB-r10-gave-erfelijk"),
(4,"De Leegte","Wie gave-zaad ontvangt en niet blijft ontvangen, valt leeg: de keerzijde van het Zegel.","MAGIE-verslaving"),
(4,"Zegellijnen","De zegellijnen worden zichtbaar op huid; status en esthetiek.","GEB-eerste-zegellicht;GENRE-zegelpunk"),
(5,"Het licht dat eet","Liane ontdekt dat zegellicht ontvangsters opeet; de Orde verbergt het.","GEB-r10-zegellicht-eet;VERHAAL-fase5"),
(5,"Theorieën","Aelthir (Rekening), Orde (heilige gave) en Stille Zusters (wond) hebben elk een theorie. De bloedafstand-theorie blijft onbeslist (VRAAG-030).","ORDE-orde;REG-stille"),
(6,"Onderdrukking","Grijswortel en vervalste annalen verbergen wat de gave kost.","GEB-r10-grijswortel-verbod;GEB-r10-vervalste-annalen"),
(7,"Het lek","Sinds 750 lekt het Zegel; lekkinderen, Vathren-groei.","GEB-r10-eerste-lek;GEB-r10-lekgeboorten"),
(7,"Magie in 801","Zegel verzwakt; wie het weet: Dhurn, Vathren, Orrim, Myrrhen. Wie het verbergt: de Orde. Hint (voorlopig): Sterrensteen kan van buiten Velmara komen; niet bewezen.","GEB-zegel-verzwakt;GEB-sterrensteen-val")]
TECH=[
(1,"Fokkunst","Schuurheren tellen bloedlijnen van vee en mensen; begin van het register.","GEB-r10-schuurheren;KETEN-graan-register"),
(1,"Dijkbouw","Tharn bouwen dijken; bouwkunst van steen en reus.","GEB-r10-delta-dijken"),
(2,"Geneeskunst","Heelsters van de Zusters; Kluwer-honingwas.","GEB-zusters-heelsters;VOLK-kluwer"),
(2,"Bloedkunde","Bloedkunde om vonk te voorspellen.","GEB-r10-bloedkunde"),
(4,"Schrift en register","Registers, bloedmerk, Zegelinkt van Dhurn-steen.","GEB-eerste-registers;GEB-r10-bloedmerk"),
(5,"Tempelbouw","Bouw met Orrim-steen; licht-architectuur.","GEB-r10-tempelbouw"),
(5,"Buiten-lichaam bevruchting","Oevrin-kennis; Orde probeert het na te maken en faalt.","VOLK-oevrin"),
(6,"Stallen","Melkstallen en zaadmachines.","GEB-melkstallen"),
(6,"Navigatie","Lijnlezers, zaadkompas, zoutloodsen, wormnavigators.","NAV-lijnlezer;NAV-zaadkompas;NAV-zoutloods;NAV-wormwording"),
(6,"Wapens","Biopunk-wapens: brandader, steenpijl; daarnaast enkele machinale resten (vuurbuizen) in Orde-kluizen, van buiten Velmara.","ORDE-tempelwacht"),
(7,"Verloren kennis","Wat verbrandde: Myrrhen-bossen, Aelthir-archief; wat bewaard wordt: Orde-kluizen met machinale resten (metalen schepen, energiekernen) die niemand kan maken.","ORDE-stille-hand;VOLK-myrrhen"),
(7,"De grens met magie en buiten","Velmara: lichaam en materiaal. Buiten (Leegte, andere planeten, voorlopig): machinaal en geavanceerd. Grens: Sterrensteen is beide.","GEB-sterrensteen-val;MAGIE-GESCH-12")]
TECHREGEL=("Velmara kent vooral lichaams- en materiaaltechniek (biopunk): fokkerij, steen, honing, schimmel, zaad. Machinale techniek, energie, schepen en wapens bestaan alleen als zeldzame, verloren of door de Orde bewaakte resten van buiten Velmara. "
"Elders in de Leegte en op andere planeten is techniek gewoon machinaal en geavanceerd (verborgen sciencefiction, voorlopig). De oorsprong van Zegel en Vonk blijft open; een buitenwereldse oorsprong is hint, geen feit.")
BALANS=("Romance: volken hebben nu helden met liefdeslijnen (Ysmeriel, Nouri, Tamsin). Intrige: +60 affaires over alle fasen en volken; nu ook Aelthir, Rosse, Kharvos. Thriller: lek en Orde-kluizen. Erotiek: niet toegevoegd, in balans. Escapisme: verborgen sf als nieuwe laag.")
WRIJ=[
("Karrûk-vonk vóór het Zegel","GESCH-karrûk-1; VOLK-karrûk","Volk zegt zegelschaduw; V2 legt een zwakke plek al vóór het Zegel. Kies.","mogelijke fout"),
("Myrrhen-Pest 470 versus Pest 340","GESCH-myrrhen-1; GEB-pest-340","Twee pesten; Myrrhen komen uit de tweede.","bron van verhalen"),
("Orde-kluizen met machines versus biopunk","TECH-REGEL; GENRE-zegelpunk","Wet 2 'het lichaam is de machine' botst met machinale resten; resten zijn uitzondering.","bron van verhalen"),
("Ileth leeft in 801","PER-aelthir-schurk-ileth; GESCH-aelthir-4","Ileth zou ca. 800 jaar oud zijn; Aelthir leven 400 jaar.","mogelijke fout")]
VRAGEN=[
("Komt de Sterrensteen (en daarmee Zegel en Vonk) van buiten Velmara?","Verborgen sf mag; oorsprong blijft open.","MAGIE-GESCH-12;TECH-REGEL"),
("Wie maakte de machinale resten in de Orde-kluizen, en weet de Orde wat het zijn?","Grote thriller-haak.","TECH-GESCH-11"),
("Is de bloedafstand-theorie juist? (zie VRAAG-030, onbeslist)","Magiegeschiedenis hangt ervan af.","MAGIE-GESCH-9")]
