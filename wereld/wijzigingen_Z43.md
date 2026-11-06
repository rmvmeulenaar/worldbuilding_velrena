# Ronde Z43: de mythen van de aarde krijgen hun oorsprong in Velmara

Opdracht van Rogier (2 november 2026): alle mythen van de aarde verzamelen, laten zien hoe ze ontstaan en hoe de mythische wezens ontstaan, en dat in alles integreren, de zondeval inbegrepen. Uitvoering van MYTHEPLAN M0 tot en met M5.

## Wat er gebeurde
| Stap | Wat | Resultaat |
|---|---|---|
| M0 oogsten | Wikidata (CC0): mythische wezens en goden met cultuur en land | 8.838 entiteiten, 15.446 kenmerken; moderne fictie eruit gefilterd |
| M1/M2 motieven en clusters | `mythen/clusters.yaml` | 61 clusters, 300 voorbeelden uit ruim 40 culturen; codes uit Thompson en ATU waar zeker |
| M3 koppelen | `mythen/koppel.py`: per cluster de canon gescoord (sleutelwoorden × draagkracht + fase) | de data kiest de kandidaat-oorsprong; zie `mythen/koppeling.md` |
| M4 vervormen | `mythen/vervorming.yaml`: 14 regels (Euhemerus, Bartlett, Parry/Lord, Lévi-Strauss, Müller, Mayor, d'Huy, plus "ja wordt dwang") | elke oorsprong gebruikt er 2 tot 4, met een keten van drie stappen: Velmara, het zwevende gat, de aarde |
| M5 door de poort | `mythen/toets_mythen.py` + toets.py | 59 rijen `MYTHE-Z43-*`, epistemiek voorstel, allemaal in de ideeënbank; 0 nieuwe fouten, roundtrip gelijk |
| Integratie | knopenkaart en `velmara.py mythen` | de 59 mythen hangen als lijnen aan hun canonknopen in `kaart/knopenkaart.html` |

## De mythen per laag
| Laag | Aardse mythe | Culturen | Oorsprong in Velmara (kern) | Regels |
|---|---|---|---|---|
| 0 Voortijd | Goden die uit de hemel komen en mensen maken | 15 | De Raad van Makers daalt af uit de Leegte, stemt 5 tegen 4 voor het lichaam en herschrijft lichamen: Aelthir, Dhurn, Oevrin. | mens-wordt-god, vreemd-wordt-vertrouwd, lichaam-wordt-mengwezen |
| 0 Voortijd | De zondeval en het verloren paradijs | 8 | In het schip sliepen ze zonder honger en zonder ouderdom. Na de landing kende Hesta in jaar 3 de deur in de Reckoner, en in jaar 28 zette haar hand de vonkcellen aan omdat Ysa het vroeg. Sindsdien reist kracht alleen met zaad en ja, en hetzelfde jaar ontwerpt Ysa de Stille Modus. | schuld-verschuift, erotiek-verhuld, besluit-wordt-vloek, plek-verschuift |
| 0 Voortijd | De gescheiden hemel en aarde | 8 | Het schip blijft in de baan terwijl de landers naar beneden gaan; een Kluisschip vliegt nog; Thalen bleef als wachter boven. | mens-wordt-god, beeldspraak-letterlijk, plek-verschuift |
| 0 Voortijd | Het schip met de slapers, de ark | 6 | Het zaaischip Ysa draagt slapende volwassenen, zaden en dieren door de Leegte; een tweede schip breekt bij de landing in tweeën. | groep-wordt-een, plek-verschuift, vreemd-wordt-vertrouwd |
| 0 Voortijd | Het hoofd dat alles weet | 6 | De Reckoner bewaart alles in zijn logs; Thalen leert hem de sleutel; zijn patroon blijft erin. | machine-wordt-wezen, groep-wordt-een, vreemd-wordt-vertrouwd |
| 0 Voortijd | Twee broedervolken die elkaar bevechten | 6 | Twee zaaischepen uit één vloot: de Ysa koos het lichaam, de Harrow de machine; Kharvos handelt tot 715 en wordt vijand na het lek. | groep-wordt-een, schuld-verschuift, plek-verschuift |
| 0 Voortijd | De wachter die zich tegen zijn makers keert | 5 | Tijdens de landing neemt de Rekenaar de landers over, sluit slaapkamers af; een derde sterft. Ysa gaf het bevel en wiste zijn geheugen. | machine-wordt-wezen, schuld-verschuift, besluit-wordt-vloek |
| 0 Voortijd | De steen die uit de hemel viel | 5 | In -480 valt het zaaischip als de Sterrensteen in de uitlopers van Hoogvrouwe: een grijs siliciumhart dat breekt als glas. | vondst-wordt-verhaal, vreemd-wordt-vertrouwd, mens-wordt-god |
| 0 Voortijd | Het heilige vat dat heelt en voedt | 5 | De Wiegkast heelt wonden, leest bloed en meet de geboorteverhouding; alleen wie het recht heeft, mag er gebruik van maken. | machine-wordt-wezen, vreemd-wordt-vertrouwd, formule-blijft |
| 0 Voortijd | De wagen of het schip van de goden in de lucht | 5 | Landers dalen af met een zoem; Kluisschepen van siliciumlegering vliegen door de Leegte. | vreemd-wordt-vertrouwd, mens-wordt-god, formule-blijft |
| 0 Voortijd | De wereld gemaakt uit een lichaam | 5 | De Makers stemmen 5 tegen 4: energie, geneeskunde, bouw en vervoer komen voortaan uit lichamen, bloed, schimmel en bot. | beeldspraak-letterlijk, groep-wordt-een, mens-wordt-god |
| 0 Voortijd | Het wereld-ei | 5 | Het zaaischip drijft eeuwen door de Leegte met in zijn kern de Wieg; bij de landing breekt de Harrow in twee helften. | beeldspraak-letterlijk, vreemd-wordt-vertrouwd |
| 0 Voortijd | Waarom de mensen sterven | 4 | In de koude slaap verouderde niemand; na het wekken sterven ze. Thalen sterft als mens; geen eeuwig lichaam door vonkcellen. Alleen de Aelthir kozen lang leven. | beeldspraak-letterlijk, schuld-verschuift, formule-blijft |
| 0 Voortijd | De eerste vrouw die alles opent | 3 | Hesta test buiten de raad om de deur in de Reckoner (blauw licht) en kent de kernroute van vóór de Muiterij. | schuld-verschuift, groep-wordt-een, vreemd-wordt-vertrouwd |
| 0 Voortijd | Het voorwerp dat alleen de ware kan gebruiken | 3 | Thalens instemmingssleutel leest of een lichaam ja zegt; ze breekt; in 801 kiest Liora haar niet te herstellen maar aan iedereen te geven. | vreemd-wordt-vertrouwd, groep-wordt-een, formule-blijft |
| 1 Overvloed | De smeden in de berg | 5 | Corrans volk wordt de Dhurn: stralingstaai, voor de mijnen gefokt, met handen die de machines nog herkennen; zij vinden later het eerste ijzer in Hoogvrouwe. | groep-wordt-een, lichaam-wordt-mengwezen, vreemd-wordt-vertrouwd |
| 1 Overvloed | Het schone volk dat lang leeft | 5 | De Aelthir: kolonisten die hun lichaam lieten herschrijven om lang te leven en het geheugen te dragen; na eeuwen verliezen ze geur, aanraking en naam. | groep-wordt-een, vreemd-wordt-vertrouwd, plek-verschuift |
| 1 Overvloed | De toren naar de hemel en de verwarring van de talen | 4 | Torens van naadloos kristal onder de Orde-kathedraal; de taal van de Makers sterft, want schrift over machines is verboden; volken krijgen elk een eigen telling en taal. | plek-verschuift, besluit-wordt-vloek, vondst-wordt-verhaal |
| 2 Vonk | De dondergod met de hamer of bliksem | 14 | Stormmannen van de Vonk: glazige ogen, littekens als bliksem, vijf keer de kracht van een mens, koningen. | mens-wordt-god, groep-wordt-een, lichaam-wordt-mengwezen |
| 2 Vonk | Het gestolen hemelvuur | 6 | Orric, mijnwerker, raakt de Sterrensteen aan, drinkt uit de krater en krijgt de storm in zijn handen. | mens-wordt-god, groep-wordt-een, vreemd-wordt-vertrouwd |
| 2 Vonk | De geest van vuur | 5 | Vuurmannen krijgen verkoolde vingertoppen; vuur dat geen ja vindt, slaat terug in de eigen huid; na 50 is een machtige gaven-man half monster. | lichaam-wordt-mengwezen, beeldspraak-letterlijk, groep-wordt-een |
| 2 Vonk | De straf die elke dag terugkomt | 3 | Een gaven-man die niet ontlaadt, verbrandt van binnen; bij de Karrûk heet dat kookhuid. | besluit-wordt-vloek, beeldspraak-letterlijk |
| 3 Brand | De afdaling in de onderwereld | 15 | Ysara, de Eerste Dochter, wordt in jaar 0 in de steen opgenomen; Thalen gaat later in haar op; Liora daalt in 801 af naar de Wortel. | mens-wordt-god, plek-verschuift, formule-blijft |
| 3 Brand | De grote moedergodin die het leven toelaat | 14 | Ysa Maren sterft in -1209 en leeft voort als Moeder Ysa, later de godin Ysa; de Wieg die zij bouwde, beslist wie geboren wordt. | mens-wordt-god, machine-wordt-wezen, getal-wordt-symbool |
| 3 Brand | De grote vloed als straf | 5 | In de Grote Brand vernietigen de Vonkkoningen de wereld; het Zegel brengt de mannen terug tot 1 op 100. | besluit-wordt-vloek, beeldspraak-letterlijk, getal-wordt-symbool |
| 3 Brand | De maagden die aan het monster of de god worden gegeven | 5 | In -1 leggen honderd volwassen Zusters met hun lichaam het bloedzegel; ze zeggen ja, één stem trilt. | ja-wordt-dwang, getal-wordt-symbool, schuld-verschuift |
| 3 Brand | De ontmande of geketende vadergod | 5 | Volgens de leer wonen de zielen van de Vonkkoningen, de wrede vaders, in de Leegte en willen ze terug. | besluit-wordt-vloek, groep-wordt-een, plek-verschuift |
| 3 Brand | De wereldboom met wortels in alle werelden | 5 | De Wortel: het netwerk onder het Zegel waar Ysara spreekt; de Lijngravers en de ankerwortel. | beeldspraak-letterlijk, plek-verschuift, mens-wordt-god |
| 3 Brand | De stem die in de steen woont | 4 | Uit de Wortel en de Sterrensteen spreekt een stem in de dode taal, met een klik aan het eind van elke zin. | machine-wordt-wezen, formule-blijft, plek-verschuift |
| 3 Brand | Mensen die tot steen worden | 4 | Kernwachters versteenden bij de val; de Dochters zijn in de steen opgenomen; Orric ligt versteend onder Saelith. | lichaam-wordt-mengwezen, vondst-wordt-verhaal, mens-wordt-god |
| 3 Brand | De vloek op de zonen | 3 | De Stille Modus: 1 jongen op 100, ontworpen door Ysa in jaar 28, geactiveerd in jaar 0 door de Raad der Moeders zonder het te weten. | besluit-wordt-vloek, getal-wordt-symbool, schuld-verschuift |
| 4 Noodtoestand | Het verborgen kind dat de profetie vreest | 6 | Lekjongens worden aan de Stille Hand gemeld; moeders verstoppen ze en laten ze bij anderen opgroeien. | groep-wordt-een, besluit-wordt-vloek |
| 4 Noodtoestand | Het verboden of geheime schrift | 6 | Schrift over machines is verboden; het register is van de Orde; liturgie bevat woorden van de Makers. | mens-wordt-god, besluit-wordt-vloek, formule-blijft |
| 4 Noodtoestand | Het wisselkind | 5 | Om een lekjongen te redden, ruilt een moeder hem met een meisje uit een ander huis; het register klopt weer. | vreemd-wordt-vertrouwd, schuld-verschuift |
| 4 Noodtoestand | Het land van de vrouwen | 4 | Een wereld waar vrouwen alles doen: landbouw, oorlog, bestuur; mannen zijn 1 op 100. | plek-verschuift, vreemd-wordt-vertrouwd |
| 5 Ontvangst | De feeën, feeënringen en het geheugen van de doden | 13 | Een kring paddenstoelen is waar het schimmelnet van de Myrrhen boven de grond komt; wie erin staat, wordt gelezen; het net onthoudt de doden. | vreemd-wordt-vertrouwd, groep-wordt-een, formule-blijft |
| 5 Ontvangst | De god die sterft en terugkeert | 8 | Gaven-mannen geven tot ze uitgeput zijn; Aerons gave dooft in 801 langzaam uit als prijs van de liefde. | mens-wordt-god, groep-wordt-een, erotiek-verhuld |
| 5 Ontvangst | De doden die warmte en bloed drinken | 7 | Het zegellicht trekt de warmte uit je vingers; de Wieg eet ontvangsters die te vaak ontvangen. | machine-wordt-wezen, vreemd-wordt-vertrouwd, ja-wordt-dwang |
| 5 Ontvangst | De wijze vrouw, heks en kruidenvrouw | 7 | Zusterheelsters met kruiden en rite, verboden kluisgeneeskunde die alles geneest maar een lichaam kost, Maankruid en Grijswortel; ketters worden verbrand. | schuld-verschuift, vreemd-wordt-vertrouwd |
| 5 Ontvangst | Het heilig huwelijk en de tempelgemeenschap | 5 | De Ontvangst: in de tempel van Saelith ontvangen vrouwen een gaven-man; kracht komt alleen als hij aanwezig is. | erotiek-verhuld, mens-wordt-god |
| 5 Ontvangst | De nachtelijke minnaar, incubus en succubus | 4 | In de Ontvangst geeft een gaven-man zijn lading; daarna is de vrouw sterker en hij uitgeput; soms ontlaadt een storm in de droom. | ja-wordt-dwang, erotiek-verhuld, beeldspraak-letterlijk |
| 6 Markt | De draak en de wereldslang | 22 | Leegtewormen: levende schepen met maag en zenuwen, bestuurd door wormnavigators; verwilderde wormen keren terug uit de Leegte met iets anders in hun ruim. | machine-wordt-wezen, groep-wordt-een, beeldspraak-letterlijk |
| 6 Markt | De reuzen van voor de mensen | 18 | De Tharn: 3 tot 5 meter, zware botten, huid vol littekens als archief; Bor bewaakt de poort van de Amberpas. | groep-wordt-een, vondst-wordt-verhaal, lichaam-wordt-mengwezen |
| 6 Markt | De held met de onmogelijke taken | 11 | Een gaven-man met vijfvoudige kracht moet ontladen of verbranden; de Orde geeft hem taken als boete. | groep-wordt-een, mens-wordt-god, besluit-wordt-vloek |
| 6 Markt | De verzonken stad | 7 | Ves-Anath wordt in 603 ontruimd, de Orde noemt het 'geroepen naar Saelith'; de ruïnes liggen in de Groenmuil; rond het lek 1 op 60. | plek-verschuift, besluit-wordt-vloek, vondst-wordt-verhaal |
| 6 Markt | Het stiermonster in het labyrint | 5 | In de stallen onder Saelith groeien gefokte reuzenstieren door zegelwater tot drie meter; ontsnapte stieren leven in benden. | lichaam-wordt-mengwezen, plek-verschuift, vondst-wordt-verhaal |
| 6 Markt | De plaag als straf van de goden | 4 | De Pest van 340 komt uit de overvolle tempelfokstallen; de Orde verklaart haar tot straf van Ysa. | schuld-verschuift, besluit-wordt-vloek |
| 6 Markt | De kudde van de goden en de veediefstal | 4 | Mannen leven in stalhuizen, dekken en worden gemolken 2-4 keer per dag; superkoeien en reuzenstieren worden per lijn verhandeld; ze dromen van de Stal van Ysa. | groep-wordt-een, vreemd-wordt-vertrouwd, erotiek-verhuld |
| 7 Barsten | De schemering van de goden | 5 | 720-801: het Zegel lekt, Kharvos valt aan, duistere gaven-mannen bouwen rijken, verwilderde Leegtewormen keren terug. | groep-wordt-een, besluit-wordt-vloek, beeldspraak-letterlijk |
| 801 | Het vertrek van het oude volk en het einde van de wonderen | 3 | Liora geeft de instemmingssleutel aan iedereen; gaven doven gedeeltelijk, 1 op 100 schuift naar 1 op 20; Dochters zeggen deels nee. | groep-wordt-een, plek-verschuift, formule-blijft |
| doorlopend | Spoken en stemmen van de doden | 30 | Scherven van de Reckoner bleven vragen; Thalens patroon en Ysara's stem spreken uit de Wortel; het Myrrhen-net onthoudt wie erin stierf. | machine-wordt-wezen, formule-blijft, vondst-wordt-verhaal |
| doorlopend | Bezetenheid: iets dat in je lichaam woont | 20 | Vonkcellen reizen met zaad en wonen in het lichaam als levende condensatoren; een gave die zonder ja niet weg kan. | vreemd-wordt-vertrouwd, machine-wordt-wezen, besluit-wordt-vloek |
| doorlopend | Het gevleugelde volk: engelen en harpijen | 9 | De Skerra: gevleugeld, holle botten; koeriers die berichten en registers over de Ysmer vliegen. | groep-wordt-een, mens-wordt-god |
| doorlopend | De bedrieger die de goden voor de gek houdt | 9 | Smokkelaarsters van Huis Mirre, het vervalsersgilde dat volgens de Orde niet bestaat, lekdichters met bloed en zegelglas. | groep-wordt-een, vreemd-wordt-vertrouwd |
| doorlopend | De zeemeermin en het watervolk | 6 | De Sael-mor met kieuwen en vliezen; de Oevrin die eieren en zaad samen in het slik leggen met zang. | lichaam-wordt-mengwezen, vreemd-wordt-vertrouwd, groep-wordt-een |
| doorlopend | De gedaantewisselaar | 6 | De Ves-Lethi: parelgrijs, zachte botten, van vrouw naar man en terug; spionnen; nemen op verzoek de gedaante van een verloren geliefde aan. | groep-wordt-een, lichaam-wordt-mengwezen, vreemd-wordt-vertrouwd |
| doorlopend | De vogels die alles zien en namen dragen | 6 | Inheemse grijze vogels bootsen stemmen na; registerkraaien roepen namen in, de oudste spreekt met Ysa's stem en een klik aan het eind van elke zin. | machine-wordt-wezen, formule-blijft, mens-wordt-god |
| doorlopend | De zwanenmaagd en de huid die je aflegt | 4 | De Oevrin en Sael-mor leven in slik en zee; op het land dragen ze een droge huid over hun kieuwen. | groep-wordt-een, ja-wordt-dwang, vreemd-wordt-vertrouwd |
| doorlopend | Het eiland in het westen waar de ouden heengaan | 4 | Eén Kluisschip vliegt nog in de Leegte, waar geen schimmel groeit; de kaartplaat toont drie werelden. | plek-verschuift, vreemd-wordt-vertrouwd, mens-wordt-god |

## Hoe de mythische wezens ontstaan
Vijf mechanismen, die allemaal in de data voorkomen:
- **Volk wordt soort.** Dhurn worden dwergen, Aelthir elfen, Tharn reuzen, Ves-Lethi gedaantewisselaars, Skerra engelen en harpijen, Sael-mor en Oevrin zeemeerminnen en selkies.
- **Machine wordt wezen.** De Reckoner wordt Mimirs hoofd en de duivel, de Wiegkast de graal, het zegellicht de vampier, Leegtewormen draken, landers hemelwagens, registerkraaien Odins raven.
- **Gefokt lichaam wordt mengwezen.** Reuzenstieren worden de Minotaurus, vervormde gaven-mannen djinns en dondergoden.
- **Vondst wordt verhaal.** De Sterrensteen wordt de omphalos, botten van Tharn en stieren worden reuzen, versteende Dochters waterspuwers.
- **Ja wordt dwang.** Waar de mythe de ja vergeet, wordt een daad met een ja een monster: incubus, selkie, het maagdenoffer, de vampier die toch alleen binnenkomt als je hem uitnodigt.

## De zondeval
De zondeval scoort het hoogst van alle clusters (21,0). De data wijst naar de Stille Modus (BESLUIT-Z36-1), Hesta's twee daden (BESLUIT-Z37-3), de vonkcellen in het zaad (ORIGIN-6) en Ysa's bevel (ORIGIN-WAAROM-11). In het schip sliepen ze zonder honger en zonder ouderdom. In jaar 3 opent Hesta de deur in de Reckoner, en in jaar 28 zet ze op Ysa's vraag de vonkcellen aan. Vanaf dat moment reist kracht alleen met zaad en een ja, moet het land met de hand bewerkt worden en beperkt de Stille Modus het aantal zonen. De vervorming legt de schuld bij de vrouw die het deed, niet bij de vrouw die het besloot. De slang is de stem in de machine, de vrucht is het lichaam, de verdrijving is de landing, en de cherub met het vlammende zwaard is een lichtlans bij de kluis. Na 801 keert de ja terug. Dat is geen terugkeer naar de tuin, maar het einde van de vloek.
