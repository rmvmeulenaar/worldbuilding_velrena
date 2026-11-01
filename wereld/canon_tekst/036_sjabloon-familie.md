# SJABLOON_FAMILIE
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Rol|Wil|Geheim|Verandert
- **grootte:** 406
- **prefixen:** TOESTAND:406
- **markering:** structuur-voorstel
- **voorstel:** Niet meer als tekst: maak er een berekende view van (toestand per persoon per jaar uit PER-rijen). De rij wordt dan afgeleid, niet geschreven.
- **voorbeeld:** Jaar 801, leeftijd 35, regio onbekend. Rol: Aeron-as (lieve gaven-man). Wil: -. Geheim: -. Verandert: dit is het moment waarop de rij speelt.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Naam|Volk|Regio|Huis|Rol|Fase|Wil|Durft
- **grootte:** 258
- **prefixen:** PER:258
- **markering:** structuur-voorstel
- **voorstel:** Splits het veldenblok naar kolommen in een eigen tabel persoon; de tekstrij krijgt alleen nog wat níet in een veld past: één zin die alleen bij deze persoon hoort. Z36: de velden staan nu in kolommen in personage_profiel (afgeleid, herbouwd door afgeleid_motor.py); de tekstrijen blijven levend omdat ankers, relaties en naamtoetsen ernaar wijzen. Vervangen pas als die drie op personage_profiel lezen.
- **voorbeeld:** Naam: Vaelorn Hoogaelthir. Volk: aelthir. Regio: groenmuil. Huis: -. Rol: Aelthir-geheugenhoudster. Fase: 1 Overvloed, jaar -400. Wil: het Lange Geheugen bewaren. Durft: de Kroon weigeren. Verbergt: d
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Geboren ca. # (#
- **grootte:** 250
- **prefixen:** TOESTAND:250
- **markering:** structuur-voorstel
- **voorstel:** Geen rij: het geboortejaar is een anker, de leeftijd wordt uitgerekend. Bewaar alleen de aanname (waarom dit jaar) als bronnotitie.
- **voorbeeld:** Geboren ca. 766 (7 Barsten), regio onbekend. Aanname: geen jaar: 801 aangenomen omdat de rij geen fase noemt (heden).
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Gevoel|Licht|Vreemd|Haak
- **grootte:** 204
- **prefixen:** ZINT:204
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Verdieping van GEB-r10-grijswortel (Grijswortel ontdekt). Geur: bittere aarde. Geluid: gefluister. Gevoel: wortels. Licht: bleek licht. Vreemd: grijswortel laat je stemmen horen. Haak: De eerste eter 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Geboren ca. -# (#
- **grootte:** 168
- **prefixen:** TOESTAND:168
- **markering:** structuur-voorstel
- **voorstel:** Zelfde behandeling als de positieve jaren, maar markeer welke van de 168 een gok zijn (aanname) zodat een schrijver weet waar hij vrij is.
- **voorbeeld:** Geboren ca. -210 (1 Overvloed), regio ambergaard. Aanname: geen leeftijd: 30 op het knooppunt aangenomen (midden van het volwassen leven, waarborgt 18+).
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Historisch: overleden ca. #
- **grootte:** 166
- **prefixen:** TOESTAND:166
- **markering:** structuur-voorstel
- **voorstel:** Vervang de standaardzin "leeft voort in annalen, kraaien of afstammelingen" door per dode één concreet spoor (een graf, een lied, een kleindochter) of door niets.
- **voorbeeld:** Historisch: overleden ca. 0 (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Functie in de wereld
- **grootte:** 126
- **prefixen:** KINKFUNC:126
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Functie in de wereld (geneeskunde, techniek): Ishvar-heelsters gebruiken de gloeiende hand om zegelsplinters in de buik op te sporen; de gloed wordt sterker bij steen. Haak: wie deze functie kent, kan
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Uit de roman (h#),
- **grootte:** 111
- **prefixen:** YSA:111
- **markering:** structuur-voorstel
- **voorstel:** Dit is een citatenregister uit de roman; vorm mag gelijk blijven (het is een index, geen verzonnen tekst). Wel: koppel elk citaat aan het hoofdstuk via de relatietabel in plaats van in de tekst.
- **voorbeeld:** Uit de roman (h01), vastgelegd 2026-10-31: Eerste zin: "Six days before landing, Ysa Maren decided to kill four thousand people." Het model: "A third now ... or half, in forty years, chosen by the mac
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Historisch: overleden ca. -#
- **grootte:** 107
- **prefixen:** TOESTAND:107
- **markering:** structuur-voorstel
- **voorstel:** Laat de sterfjaren berekenen uit geboortejaar + levensduur; schrijf alleen een rij als de dood zelf verhaal is (hoe, door wie).
- **voorbeeld:** Historisch: overleden ca. -140 (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:In # actief, leeftijd
- **grootte:** 101
- **prefixen:** TOESTAND:101
- **markering:** structuur-voorstel
- **voorstel:** Leeftijd in 801 is afleidbaar; vervang door een berekende kolom en schrap de handgeschreven variant uit het zicht (niet uit de db).
- **voorbeeld:** In 801 actief, leeftijd 35.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Functie|Maker|Prijs|Risico|Verhaalhaak|Zintuig
- **grootte:** 85
- **prefixen:** VOOR:56,TECH:29
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Voorwerp van aelthir (gereedschap). Functie: geknoopt koord dat een eeuw telt. Maker: aelthir. Prijs: onverkoopbaar. Risico: wie het leest kent geheimen. Verhaalhaak: het koord vermeldt een val van ee
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Kern|Naam|Volk|Regio|Huis|Rol|Fase|Wil
- **grootte:** 81
- **prefixen:** PERS:81
- **markering:** structuur-voorstel
- **voorstel:** Dubbel van PER-rijen ("verwijzing naar bestaand personage"): maak er een relatie van (PERS -> PER) en geen tekst. Z36: de velden staan nu in kolommen in personage_profiel (afgeleid, herbouwd door afgeleid_motor.py); de tekstrijen blijven levend omdat ankers, relaties en naamtoetsen ernaar wijzen. Vervangen pas als die drie op personage_profiel lezen.
- **voorbeeld:** Verwijzing naar bestaand personage PER-f1-dhurn-garra (geen dubbel). Rol in de keten van de Dhurn: mijnvrouw in fase 1 Overvloed (-600..-150). Kern: Naam: Garra Steenvoeler. Volk: dhurn. Regio: hoogvr
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Archetype, geen vaste persoon.
- **grootte:** 80
- **prefixen:** TOESTAND:80
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Archetype, geen vaste persoon. Besluit: speelt standaard in 801 (Barsten), volwassen tussen 25 en 45; bij gebruik in een verhaal krijgt de figuur een eigen tijdlijn met geboortejaar = verhaaljaar min 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Oorzaak|Gevolg
- **grootte:** 75
- **prefixen:** GESCH:75
- **markering:** structuur-voorstel
- **voorstel:** Vertel elk volksverhaal vanuit één eigen vorm: het ene als spreekwoord, het andere als ruzie tussen twee oudsten, een derde als liedregel. Oorzaak/gevolg blijft data in de relatietabel.
- **voorbeeld:** Oorsprong. De Aelthir leven al eeuwen in de hoge wouden boven Hoogvrouwe als traag ceremonieel volk; de Sterrensteen valt in hun jeugd. Oorzaak: De val van de Sterrensteen. Gevolg: Hun vruchtbaarheid 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Prijs|Haak
- **grootte:** 74
- **prefixen:** ROMANCE:49,SAW:25
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** de ruïnes zitten vol oude vallen die op gave reageren. Zintuig: koud metaal, eigen adem, tikkende steen. Prijs: lichaam of loyaliteit. Haak: wie de val overleeft draagt een kerf en een geheim.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Volk|Fase|Rol|Verandert|Zintuiglijk|Haak|Verdiept (Z#)|Geur
- **grootte:** 63
- **prefixen:** PERS:63
- **markering:** structuur-voorstel
- **voorstel:** Kies per persoon één ding dat de lezer onthoudt (een gewoonte, een zin, een litteken) en laat de rest weg; de haak per persoon moet verschillen, nooit "zijn keuze botst met...". Z36: de velden staan nu in kolommen in personage_profiel (afgeleid, herbouwd door afgeleid_motor.py); de tekstrijen blijven levend omdat ankers, relaties en naamtoetsen ernaar wijzen. Vervangen pas als die drie op personage_profiel lezen.
- **voorbeeld:** Volk: Dhurn. Fase: 7 Barsten (720..801). Rol: jonge kluislezeres (24). Verandert: Leest de plaat met de vrouwenstem en vertaalt het eerste woord van de dode taal. Zintuiglijk: Zoemende metaalgeur, haa
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Betrokken|Motief|Wending|Gevolg
- **grootte:** 59
- **prefixen:** INTR:59
- **markering:** ideeenbank
- **voorstel:** Intriges: schrijf per fase hooguit één uit, als scène met dialoog; de rest gaat naar de ideeënbank (gebeurt al voor de niet-gebruikte).
- **voorbeeld:** Intrige, fase 1 Overvloed. Betrokken: Dhurn-mijnwerker en koning Orric. Motief: mijnrecht. Wending: het monster is van Orrim-lichaam. Gevolg: Orric koopt woestijn.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Dreiging|Opbouw|Afstoting|Wat de personages verliezen|Haak|Zo schrijf je het|Techniek
- **grootte:** 59
- **prefixen:** HORROR:59
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Dreiging: Wormen kruipen door de aarde en volgen warmte. Opbouw: eerst trillen, dan gaten, dan het eerste slachtoffer. Zintuig dat de gruwel draagt: trillende grond, slijm, zure aarde. Afstoting: 8/10
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Haak|Functie|Crosslinks
- **grootte:** 54
- **prefixen:** BESLUIT:32,GEB:13,ORDE:3,BEST:2
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Ze zijn de kern van het geloof. Hun zaad is het kostbaarste. Sommigen zijn vriendelijk, anderen duister. Zij kiezen; hun gunst is de grootste munt. Zintuig: De lucht van vonk in een kamer waar een gav
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wat in Velmara|Wie (volwassen)|Afspraak/stopwoord|Zintuig|Risico en prijs|Haak|Techniek
- **grootte:** 54
- **prefixen:** KINK:54
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wat in Velmara: de hand als volledige overgave; bij de Myrrhen een vertrouwensrite. Wie (volwassen): Myrrhen, Saelith-vormhuizen. Afspraak/stopwoord: schimmelolie, langzaam tellen, stopwoord van het v
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Locatie|Wie (volwassen)|Wapen/gave|Zintuig|Wending|Wat het kost|Haak|Techniek
- **grootte:** 49
- **prefixen:** ACTIE:49
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Locatie: de getijdengangen onder de Pekelrij. Wie (volwassen): Jorrit en Sef met een buidel zegelsteen. Wapen/gave: haakmes en koelslakken. Zintuig: pekel, rottend wier, water dat tot de borst stijgt.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Situatie|Type|Haak|Zintuig
- **grootte:** 47
- **prefixen:** COMEDY:47
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Situatie: een Orrim-afgezant analyseert grappen als militaire codes. Type: droog. Haak: hij kraakt per ongeluk een echte code. Zintuig: gelach, gekraak van lak en papier, de geur van stof en inkt.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Metadoel|Heersers halen eruit|Volk haalt eruit/gelooft|Overschreden taboe|Moment|Band|Als het wegvalt
- **grootte:** 45
- **prefixen:** SYS:45
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Metadoel: macht, geloofsintegratie, selectie, zegel. Heersers halen eruit: status, voyeurisme via getuigen, loyale huizen. Volk haalt eruit/gelooft: zegen en kracht; gelooft dat Ysa haar ziet. Oversch
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Aandeel|Voorkeuren|Officieel en feitelijk
- **grootte:** 42
- **prefixen:** SEKS:42
- **markering:** ideeenbank
- **voorstel:** Per volk één tegenstrijdigheid tussen wat officieel mag en wat gebeurt, als korte anekdote in plaats van vier velden.
- **voorbeeld:** Verkopen herinneringen voor felle nachten met mensen tot ze leeg zijn. Aandeel: ±2%. Voorkeuren: VOOR-geest:5, VOOR-overgave:5. Officieel en feitelijk: zie kern; afwijken kost status of verbanning. Al
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Romance (met belemmering), fase
- **grootte:** 41
- **prefixen:** ROM:41
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Romance (met belemmering), fase 2 Vonk. Krijgsvrouw en verlegen vonkdrager. Belemmering: zaadhonger maakt verlangen onbetrouwbaar. Zie VERHAAL-fase2.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Aanraking|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 40
- **prefixen:** ZINT:32,DAG:4,PLEK:3,STAD:1
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: was van honderd kaarsen en de zure inkt van verse besluiten. Geluid: één stem tegelijk, en het tikken van ringen op marmer als instemming. Aanraking: koude stenen banken die elke Moeder met eige
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Waarom vereerd|Omslag en aanbidders|Wat het doet|Prijs|Haak|Zintuig
- **grootte:** 40
- **prefixen:** NERD:40
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Waarom vereerd: hij kan de oude Maker-tekens lezen. Omslag en aanbidders: de Annalisten knielen; huizen sturen geschenken. Wat het doet: hij/zij leert dat verering een kooi van goud is. Prijs: hij is 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Vorm|Stappen van de afglijding|Wat de omgeving doet|Uitkomst|Zintuig|Haak
- **grootte:** 40
- **prefixen:** DEGEN:40
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Vorm: lust. Stappen van de afglijding: één extra nacht > verslaving aan aanbidding > bindingsdwang. Wat de omgeving doet: de huizen moedigen het aan. Uitkomst: terugkeer na de Leegte. Zintuig: wat eer
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Volk/klasse|Zintuigen veranderen|Wat de wereld zegt|Prijs en haak
- **grootte:** 40
- **prefixen:** ONTWAAK:40
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Volk/klasse: mens/Saelith-ambtenares. De eerste keer dat ze/hij durft te willen: ze vraagt voor het eerst zelf om een plek op de lijst. Zintuigen veranderen: inkt ruikt opeens naar huid. Wat de wereld
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Gekozen door Rogier ("alles
- **grootte:** 40
- **prefixen:** BESLUIT:40
- **markering:** structuur-voorstel
- **voorstel:** Besluiten van Rogier: vorm blijft (herkomst is hier juist het punt). Geen actie, behalve dat een nieuw besluit niet de oude openingszin kopieert.
- **voorbeeld:** Gekozen door Rogier ("alles zoals aanbevolen", 2026-10-31): Close third person, verleden tijd, per hoofdstuk afwisselend YSA / THALEN (label in de kop); geen ik-vorm, zodat het geheim niet lekt.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Volk|Fase|Rol|Verandert|Zintuiglijk|Haak
- **grootte:** 39
- **prefixen:** PERS:39
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Volk: Karrûk. Fase: 2 Vonk (-150..-40). Rol: clanmoeder. Verandert: Verkoopt de clans aan de vonkkoningen voor zaad, zodat haar krijgsters sterker worden; zo begint de huurkracht. Zintuiglijk: Het lee
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Toestand|Verandert
- **grootte:** 35
- **prefixen:** TOESTAND:35
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar 781 (-), leeftijd 25, plaats: Zoutkust. Toestand: krijgt eerste schip; trouwt rond 788 met Maelis van Varenne. Verandert: relatie Varenne begint.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Aandeel/positie|Voorkeuren|Officieel|Feitelijk|Spanning|Kosten van afwijken
- **grootte:** 34
- **prefixen:** SEKS:34
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Monogaam per eeuw, hetero en homo gelijk geaccepteerd; trage, ritualistische seks. Aandeel/positie: ±55%, de Raad. Voorkeuren: VOOR-teder:2, VOOR-ritueel:3. Officieel: de norm. Feitelijk: vaak na twee
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:In # leeftijd #;
- **grootte:** 34
- **prefixen:** TOESTAND:34
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** In 801 leeftijd 43; ouder geworden sinds het knooppunt; toestand verder open.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Daad|Zintuig|Prijs|Haak
- **grootte:** 33
- **prefixen:** HELD:33
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Daad: ze bracht een vloot door de Wrakkust. Zintuig: zout, donder. Prijs: haar schip. Haak: ze smokkelde gaven-mannen mee.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Regio|Functie|Sfeer|Geheim|Scènetypes|Personages|Kink-plek|Verhaalhaken
- **grootte:** 32
- **prefixen:** PLEK:19,STAD:13
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Regio: ambergaard. Functie: graandorp, Liora's thuis. Sfeer: stro, bier, zonnige velden, stalhuizen. Geheim: Liora's moederhuis is diep in schuld. Scènetypes: oogst, afscheid, terugkeer. Personages: P
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Functie|Ontwerper|Prijs|Risico
- **grootte:** 32
- **prefixen:** TECH:32
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Voorwerp (gave). Functie: communicatie op afstand. Ontwerper: Laadster Velith. Prijs: 2 maanden loon. Risico: sterft als de gever sterft.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Functie|Techniek|Prijs|Risico|Verhaalhaak|Zintuig
- **grootte:** 32
- **prefixen:** VOOR:32
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Voorwerp van klasse top (ceremonieel). Functie: staf met kluiskern en Sterrensteen. Techniek: gave/metaal/zegelsteen. Prijs: onschatbaar. Risico: de kern is bijna leeg. Verhaalhaak: Ithrael verbergt d
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie (volwassen)|Zintuig|Wat het kost|Intrige|Haak
- **grootte:** 31
- **prefixen:** EROS:31
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie (volwassen): een kustvrouw en kapitein Ondessa. Zintuig: teer, natte touwen, zout op de huid. Wat het kost: ze verliest haar plek aan boord als het uitlekt. Intrige: Ondessa bindt haar zo aan zich
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Hoofdpersoon (volwassen)|Opbouw|Climax|Einde|Haak
- **grootte:** 30
- **prefixen:** COMEDY:10,ROMANCE:10,HELD:10
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Hoofdpersoon (volwassen): Annaliste Mops (60). Opbouw: genealogieën om de Rekenaar te vervelen. Climax: de Rekenaar vertelt zelf een grap. Einde: de grap is een toestemmingscode. Haak: de grap opent e
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Naam|Volk|Rol|Fase
- **grootte:** 28
- **prefixen:** PER:28
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Naam: Ysmeriel van de Twaalf. Volk: aelthir. Rol: held van de volkgeschiedenis. Fase: 7 Barsten. Jongste oudste (212 jaar); breekt de zwijgplicht en vertelt de Stille Zusters wat Ileth verkocht. Verli
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Licht|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 27
- **prefixen:** ZINT:20,PLEK:4,DAG:2,STAD:1
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: perkament, inktmos en het zweet van klerken in wollen mouwen. Geluid: krassende pennen, de registerkraaien die namen naroepen. Licht: smalle stralen stof in hoge vensters, koud op de huid. Herke
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Soort|Wie (volwassen)|Zintuig dat draagt|Wat verandert|Wat het kost|Haak voor intrige
- **grootte:** 27
- **prefixen:** EROS:27
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Soort: eerste aanraking. Wie (volwassen): Liora en Tobin, Zoutkust. Zintuig dat draagt: geur van zout op zijn hals. Wat verandert: zij ontdekt dat hij haar gloed niet wil kopen. Wat het kost: haar arg
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wat hongerig maakt|Lichaam|Haak (intrige)
- **grootte:** 27
- **prefixen:** EROS:27
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wat hongerig maakt: de schaarste: één gaven-man per honderd, en een nacht kracht die 8-12 uur duurt. Lichaam: hitte in de schoot, warme huid die naar ozon ruikt zodra hij de kamer binnenkomt. Haak (in
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Gevoel|Licht|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 27
- **prefixen:** ZINT:27
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: kaneel, peper en saffraan die in je neus blijft hangen tot na het slapen. Geluid: het tikken van koperen weegschaaltjes en een verkoopster die prijzen zingt. Gevoel: korrelig poeder dat geel aan
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Voor wie|Hoe vaak|Als het wegvalt|Afstoting|Bron van aantrekking|Oorsprong in inteelt|Wie ziet|Wie verbergt
- **grootte:** 25
- **prefixen:** LICH:25
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Een gebonden vrouw ruikt haar meester over mijlen; zijn geur maakt haar loom en willig, anderen walgen van de zoete rotlucht. [Functie eerst (r12): FUNC-HECHT, FUNC-LUST. Voor wie: donkere heren, Kald
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Wat het kost|Haak|Techniek|Verbonden met|Zintuig erbij|Haak
- **grootte:** 25
- **prefixen:** BODY:25
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Zintuig: zwaar, compact, metaalglans in de huid door ertsstof. Wat het kost: longen worden stijf. Haak: Dhurn-huid zoemt bij zegelsteen. Techniek: zegelsteen. Functie in de wereld (status): Ideaal van
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Oorzaak|Actie|Reactie / onbedoeld gevolg|Won|Verloor|Verzet|Officiële versie
- **grootte:** 24
- **prefixen:** GEB:24
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar 1..12 · Regio: overal · Wie: volk. Oorzaak: GEB-zegel-gelegd. Actie: Nauwelijks jongens geboren; koningslegers sterven uit zonder opvolging. Reactie / onbedoeld gevolg: Paniek; oude koningen houd
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Licht|Aanraking|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 24
- **prefixen:** ZINT:24
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: verse inkt en verbrand perkament. Geluid: krassende pennen in een stille zaal, een kraai die op het dak loopt. Licht: één kaars. Aanraking: perkament nog warm van het schrapen. Herkenbaar: Een v
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Hoofdpersoon (volwassen)|Opbouw|Climax|Einde
- **grootte:** 24
- **prefixen:** NERD:8,DEGEN:8,ONTWAAK:8
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Hoofdpersoon (volwassen): Ysel (24). Opbouw: ze leest de plaat. Climax: de Rekenaar kiest haar. Einde: ze wordt vereerd en gevreesd.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Regio|Zintuiglijk motief|Politiek gewicht|Scènesoort|Haak|Verdiept (Z#)|Geur|Geluid
- **grootte:** 23
- **prefixen:** PLEK:23
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Regio: REG-rosse. Zintuiglijk motief: Kamelenmelk, veel kinderen, sterrenhemel. Politiek gewicht: Bewijs dat het Zegel niet overal werkt. Scènesoort: ontdekking, gevaar. Haak: Een Orde-moordenares. Ve
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Kleur|Materiaal|Licht|Geur|Geluid|Bouwstijl|Genre
- **grootte:** 22
- **prefixen:** ESTH:22
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Kleur: zwart, as, hoorngrijs. Materiaal: basalt, hoorn, ketting, ongelooide huid. Licht: rood vuur, rook. Geur: as, zweet, ijzer, bloed. Geluid: trommen, kettingen, geschreeuw. Bouwstijl: forten van z
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Dagelijks|Ceremonieel|Signaleert
- **grootte:** 22
- **prefixen:** KLEED:22
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Dagelijks: ongelooide huid, ketting, hoorn. Ceremonieel: hoornhelmen, zwarte mantels. Signaleert: bezit (donker thema), macht.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Kleur|Gebruik
- **grootte:** 22
- **prefixen:** ZINT:22
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur van koude regen op oude boeken; een zacht klokgelui in hun stemmen. Kleur: zilvergrijs. Gebruik: herhaal het motief bij elke scène op deze plek of met dit volk, zonder de naam te noemen.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Intensiteit|Oorsprong|Hoort bij|Relatie|Taboe
- **grootte:** 21
- **prefixen:** VOOR:21
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Bedekt of gevuld worden met zaad, het teveel aan kracht. Intensiteit: 4. Oorsprong: GEB-zaadkracht-ontdekt. Hoort bij: RIT-zevenvoudige-ontvangst;MAGIE-kracht-duur. Relatie: versterkt VOOR-groep. Tabo
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Woorden|Geluid|Haak
- **grootte:** 21
- **prefixen:** EROS:21
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Woorden: 'tarief' als kosewoord: 'je bent je tarief waard'. Geluid: gefluister boven het gerinkel van munten. Haak: wie het verkeerde woord kiest, verraadt zijn afkomst.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie|Plek|Regels|Stappen|Effect
- **grootte:** 20
- **prefixen:** RIT:20
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wie: Vrouw (18+) met gunstbrief, gaven-man, Ontvangsters, getuigen. Plek: Tempel, altaarbed. Regels: Alleen met instemming van de gaven-man en de vrouw; zegellicht moet branden. Stappen: Bad en zalvin
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Sexy|Fetisj|Verboden of ondeugend|Regel
- **grootte:** 20
- **prefixen:** KLEED:20
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Sexy: mannen tonen borst en littekens als bezit-pronk; donker thema: vrouwen in kettingen zijn gevangenen, geen erotiek. Fetisj: alleen buiten Kharvos: ex-gevangenen die de ketting heroveren als eigen
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Smaak|Aanraking|Licht|Temperatuur|Herkenbaar|Vreemd
- **grootte:** 20
- **prefixen:** ZINT:20
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: gebakken inktvis, rum met kruidnagel, natte touwen. Geluid: honderd scheepsbellen die elk een ander uur slaan, omdat elk schip zijn eigen tijd houdt. Smaak: zwart bier dat naar rook en zeewier s
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Regio|Zintuiglijk motief|Politiek gewicht|Scènesoort|Haak
- **grootte:** 20
- **prefixen:** PLEK:20
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Regio: REG-saelith. Zintuiglijk motief: Wierook en warm marmer; een koor dat nooit stopt; zegellicht dat de warmte uit je vingers trekt. Politiek gewicht: Zetel van de Orde; wie hier ontvangt, stijgt 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Oorzaak|Zintuig|Prijs|Haak|Techniek|Zintuig|Haak|Functie
- **grootte:** 20
- **prefixen:** OORLOG:20
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Oorzaak: rituele oorlog om ontvangstrecht; partijen: huizen Kaldra en Varenne; tactiek: nachtgevechten met fakkels, vrouwen als bevelhebbers. Zintuig: fakkels, trommels, zweet. Prijs: honderd doden in
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Oorzaak|Actie|Reactie / onbedoeld gevolg|Won|Verloor|Verzet|Officiële versie|Zintuig
- **grootte:** 19
- **prefixen:** GEB:19
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar -6 · Regio: Saelith · Wie: zijn eigen gebonden vrouwen. Oorzaak: GEB-r10-varnath-opkomst;GEB-r10-grijswortel. Actie: Zijn vrouwen nemen Grijswortel en vermoorden hem. Reactie / onbedoeld gevolg: 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Prijs|Haak (intrige)
- **grootte:** 18
- **prefixen:** BEST:14,D1:3,GELD:1
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Water uit de diepe putten van Qesh, zonder zegelstof; heilig voor Ishvar, ketterij voor de Orde. Prijs: een kruik kost een Kroon in Saelith. Haak (intrige): smokkel van putwater naar Moeders van de St
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Afwijkingen|Functie|Waarom hier nodig|Wie ziet het|Wie verbergt het|Scènetypes en verhaallijnen
- **grootte:** 17
- **prefixen:** PLEK:17
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Afwijkingen: LICH-tempelfokkerij, LICH-melkman, LICH-pest. Functie: FUNC-ECO, FUNC-VOORT. Waarom hier nodig: Zonder goedkope voorraad draait de tempelvoeding niet. Wie ziet het: stalzusters, gefokte m
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Kern|Naam|Volk|Rol|Fase|Haak
- **grootte:** 17
- **prefixen:** PERS:17
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Verwijzing naar bestaand personage PER-saelmor-schurk-vessa (geen dubbel). Rol in de keten van de Sael-mor: schurk in fase 6 Markt (340..720). Kern: Naam: Kapitein Vessa. Volk: sael-mor. Rol: schurk v
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Daad|Zintuig|Prijs|Haak|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 17
- **prefixen:** HELD:17
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Daad: hij smeedde valse boeien die openklikken. Zintuig: heet ijzer, hamerslag. Prijs: zijn smidse werd verwoest. Haak: de boeien gaan open op een woord. Zintuig: Heet ijzer en hamerslag in een Dhurn-
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Vastgelegd door Rogier (#-#-#):
- **grootte:** 16
- **prefixen:** BESLUIT:16
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Vastgelegd door Rogier (2026-10-31): In h27 zegt Hesta eerst "But I keep the last cells. Seven of them. The ones that still hold a charge." Ysa antwoordt "Seven", Hesta: "Nine, by now. I've been busy.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Verhaal|Haak|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 15
- **prefixen:** BESLUIT:15
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Varnath liet in 512 de havenwijk van Lisk branden, niet de stad; zijn hof lag op het eiland ervoor. De vrouwen die de brand overleefden gingen juist daardoor naar de Zusters. Verhaal: de Zusters van L
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Woord of teken|Wanneer wel en niet|Haak
- **grootte:** 15
- **prefixen:** EROS:15
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Woord of teken: de hamerslag: twee keer met de knokkels op steen. Wanneer wel en niet: in rituelen verplicht; in geheim spel soms bewust 'vergeten' als gelabeld donker spel, met schande als prijs. Haa
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie (volwassen)|Zintuig en taal|Wat het kost|Haak|Verbonden met|Zintuig erbij|Haak
- **grootte:** 15
- **prefixen:** VERLEID:15
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie (volwassen): aanraken pas na drie nachten kijken. Zintuig en taal: kou, adem die zichtbaar wordt. Wat het kost: ongeduld is een belediging. Haak: de derde nacht is een val. Verbonden met: De Aelth
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Haak|Kan het beter
- **grootte:** 15
- **prefixen:** PER:5,WET:4,VOORW:3,LICH:1
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Vroegere vrouw van Ondessa (788-795), zijlijn van Huis Varenne; liet met een fles rum één registerregel veranderen zodat Ondessa naar haar zou komen; bekent zelf; wordt tweede kapitein van de Kraaienb
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Voor wie|Hoe vaak|Als het wegvalt|Afstoting|Bron van aantrekking
- **grootte:** 14
- **prefixen:** LICH:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Vrouwen die jarenlang vaak gaven-zaad ontvangen krijgen gouden aderen onder de huid, gevoelige, altijd opgewonden zenuwen en vroege grijze haren. Mooi en gebroken tegelijk; een teken van rang. Seksuel
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Keten bij uitval|Wie saboteert de functie
- **grootte:** 14
- **prefixen:** FAAL:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Keten bij uitval: Geen binding → harems en legers lopen weg → donkere hoven vallen of worden wreder. Wie saboteert de functie: Grijswortel, Aeron-as (die niet bindt).
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie|Systeemfunctie
- **grootte:** 14
- **prefixen:** RIT:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Ritueel van de Aelthir, vorm van hun extreme kern (zie SEKS-VOLK-aelthir-kern). Wie: alleen volwassenen (18+) die vooraf instemmen, met een hoedster die stopt. Systeemfunctie: houdt de functie van het
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Waarom|Haak
- **grootte:** 14
- **prefixen:** HOOFDPERS:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Hoofdpersoon voor verhalen vanuit de Karrûk: Brem Tweezijde (PERS-Z4-karruk-7-2). Waarom: staat in fase 7 Barsten (720..801) op het kruispunt van de eigen geschiedenis en de hoofdlijn (Liora, Zegel). 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Fase # Voortijd (Makers,
- **grootte:** 14
- **prefixen:** VOLK:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Fase 0 Voortijd (Makers, ca. -1240): Corran Velt (PERS-Z4-dhurn-0-1) en Mirel Velt (PERS-Z4-dhurn-0-2). Fase 1 Overvloed (-600..-150): Garra Steenvoeler (PERS-Z4-dhurn-1-1) en Brom Steenhand (PERS-Z4-
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Verleiding|Zintuig|Taal en tempo|Wat opwindt|Taboe|Instemming|Diversiteit|Haak
- **grootte:** 14
- **prefixen:** EROS:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Verleiding: ruiters dagen uit met een race. Zintuig: warm paardenzweet, ruwe handpalmen. Taal en tempo: snel, lachend, kort. Wat opwindt: snelheid en winnen. Taboe: liefde in de schaduw van een zegell
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Passende genres en rijen|Sterkste genres
- **grootte:** 14
- **prefixen:** VOLK:14
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Passende genres en rijen: oorlog: OORLOG-Z9-24 (1); comedy: COMEDY-Z10-40 (1); romantiek: ROMANCE-Z10-27 (1); helden: HELD-Z10-14 (1); nerd: NERD-Z10-8 (1); ontwaking: ONTWAAK-Z10-27 (1). Sterkste gen
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie|Plek|Regels/veiligheid|Stappen|Kern|Effect|Kink-schaal
- **grootte:** 13
- **prefixen:** RIT:13
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wie: Vrouw (18+) die een gaven-man wil naderen buiten de rij; Ontvangsters. Plek: Tempelgalerij Saelith. Regels/veiligheid: Heilig woord “Ysa-rust” stopt alles; Ontvangster waakt. Stappen: Geboeid aan
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Herkenbaar|Kernscènes|Zaad
- **grootte:** 13
- **prefixen:** VERHAAL:13
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Saelith, 789. De Stille Hand komt vannacht. Annike verbrandt haar archief kast voor kast, elk kwartier een kast, terwijl de Lampentoren slaat. Dirk moet Veere ophouden die buiten wacht, en Veere is de
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Voorstel vastgesteld|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 13
- **prefixen:** BESLUIT:13
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Voorstel vastgesteld: ontvoering in het lege uur na grote magie of met Grijswortel. Zintuig: De doffe stilte van het lege uur na grote magie. Haak: Kharvose ontvoerders wachten met Grijswortel op het 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Leger|Zintuig|Prijs|Haak|Techniek|Zintuig|Haak|Functie
- **grootte:** 13
- **prefixen:** OORLOG:13
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Leger: stoomwerktuigen en metaal-oud harnassen; agressie uit hebzucht naar oud metaal; krijgskunst: tunnels en ondergraven. Zintuig: stoom, zwavel, gehamer. Prijs: hun harnassen vergiftigen de drager 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Situatie|Type|Haak|Zintuig|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 13
- **prefixen:** COMEDY:13
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Situatie: de Dhurn noemen alle mensen 'ladders'. Type: volk. Haak: een Dhurn-diplomaat gebruikt het als compliment. Zintuig: gelach, gekraak van lak en papier, de geur van stof en inkt. Zintuig: Een D
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Intensiteit|Oorsprong|Hoort bij|Relatie|Taboe|Zintuig|Haak|Functie
- **grootte:** 12
- **prefixen:** VOOR:12
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Langzame, liefdevolle seks met één partner. Intensiteit: 1. Oorsprong: GEB-zusterburcht. Hoort bij: RIT-tweegelofte;RIT-gunstnacht;RIT-spiegelnacht;RIT-melkzegen;PER-aeron;PER-liora. Relatie: botst me
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Intimiteit|Rivaliteit|Geheim
- **grootte:** 11
- **prefixen:** DAG:11
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Intimiteit: in Kharvos wonen mannen bij één vrouw of meerdere naar keuze; de koning houdt vrouwen als gijzelaars (donker thema). Rivaliteit: de Orde. Geheim: Kharvos valt deels buiten het Zegel en ken
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Gekozen|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 11
- **prefixen:** BESLUIT:11
- **markering:** kern (niet aanraken)
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Gekozen: B, vijand na het lek, met een eigen zaaischip dat voor machines koos. Kharvos werd bevolkt door een tweede zaaischip (de Harrow) dat in de stemming voor machines koos; zijn kern dempt het Zeg
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Toestand|Verandert|Minderjarig op dit moment
- **grootte:** 11
- **prefixen:** TOESTAND:11
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar 756 (Stilmaan), leeftijd 0, plaats: Isla Mirre. Toestand: geboren in Huis Mirre, dochter van een kaapvaarster. Verandert: oorsprong; zee in het bloed. Minderjarig op dit moment: geen enkele seksu
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Hoofdpersoon (volwassen)|Tegenspeler (volwassen)|Doel|Wending|Einde|Haak
- **grootte:** 10
- **prefixen:** VERLEID:10
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Hoofdpersoon (volwassen): Liora. Tegenspeler (volwassen): een onbekende op het maskerbal. Doel: de sleutel van de kluis. Wending: het is Sef. Einde: verraad wordt verbond. Haak: het einde opent een vo
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Hoofdpersoon (volwassen)|Dreiging|Opbouw|Climax|Einde en prijs|Haak
- **grootte:** 10
- **prefixen:** HORROR:10
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Hoofdpersoon (volwassen): Liora. Dreiging: de Wortel onder Saelith. Opbouw: warme grond, hartslag, een stem. Climax: de stem spreekt met Thalen. Einde en prijs: Liora snijdt een wortel door en verlies
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Opbouw|Regels|De keuze|Prijs|Wending|Zintuig|Afstoting|Haak
- **grootte:** 10
- **prefixen:** SAW:10
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Opbouw: een gevangene wordt wakker in een kamer van zegelsteen die langzaam warm wordt. Regels: elk uur zakt een plaat; de deur opent alleen als iemand zijn eigen gave opgeeft. De keuze: de gave afsni
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Hoofdpersoon (volwassen)|Opbouw|Climax|Einde en prijs|Haak
- **grootte:** 10
- **prefixen:** SAW:10
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Hoofdpersoon (volwassen): een kopiist (28) die een registerfout ontdekt. Opbouw: hij volgt de fout naar Quills vallen. Climax: hij moet zijn eigen fout bekennen in het schuldspel. Einde en prijs: Quil
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Gekozen door Rogier (#-#-#)|Reden|Gevolgen in de canon|Label|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 10
- **prefixen:** BESLUIT:10
- **markering:** kern (niet aanraken)
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Gekozen door Rogier (2026-10-31): B. De Makers bouwden het Zegel (noodstand van zaaischip Ysa, jaar 0); de priesteressen van Ves-Anath ontdekten de bediening ca. jaar 130 en kaapten het. "Achthonderd 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie (volwassen)|Zintuig|Wat het kost|Intrige|Haak|Donker thema (gelabeld)
- **grootte:** 9
- **prefixen:** EROS:9
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie (volwassen): een Orde-inspectrice, gevangen door smokkelaars. Zintuig: ruim vol teer, deining, haar adem in het donker. Wat het kost: losgeld of verraad. Intrige: de spanning tussen haar en de stu
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Prijs|Haak|Techniek|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 9
- **prefixen:** OORLOG:9
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Ondessa won de zeeslag bij de Wrakkust met drie schepen tegen twaalf. Zintuig: teer, wind. Prijs: ze verloor haar oog en haar vrouw. Haak: ze vertelt het verhaal elke keer anders. Techniek: geen. Zint
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Alternatieven|Keuze|Reden|Effect op verhalen|Haak|Zintuig|Haak|Functie
- **grootte:** 9
- **prefixen:** BESLUIT:9
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Alternatieven: 1 op 100 (Stille Modus) | 1 op 300 | 1 op 20. Keuze: 1 op 100 als noodstand, met de derde weg die over decennia naar 1 op 20 schuift. Reden: het is de noodstand van het schip, niet natu
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Zintuig|Wat het kost|Haak|Techniek
- **grootte:** 9
- **prefixen:** BODY:9
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Zintuig: een bad van warm kweekvlees dat ruikt naar melk en ijzer; de huid tintelt als duizend tongen. Wat het kost: elke kuurdag kost een maand zaadrecht. Haak: op de bodem van een kuip ligt een ring
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:POV/plek|Duwt|Genres #-#
- **grootte:** 9
- **prefixen:** ROMANCE:9
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Beat 2 van "Ysa's verloren liefde" (versie Z15b). Het getal. Ysa in het lab, zes dagen voor de landing. De simulatie draait voor de honderdste keer: de kernen zijn binnen twee generaties op, en de Rek
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie|Plek|Regels|Stappen|Effect|Kink-schaal
- **grootte:** 8
- **prefixen:** RIT:8
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wie: Twee volwassenen (vrouwen onder elkaar, of vrouw en gewone man die zij bezit of vrijkoopt). Plek: Binnenhof, onder getuigen van het moederhuis. Regels: Vrijwillig; bindt niet exclusief (het geloo
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Kern|Naam|Volk|Rol|Fase
- **grootte:** 8
- **prefixen:** PERS:8
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Verwijzing naar bestaand personage PER-dhurn-held-brakka (geen dubbel). Rol in de keten van de Dhurn: held in fase 7 Barsten (720..801). Kern: Naam: Mijnmeester Brakka. Volk: dhurn. Rol: held van de v
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur en gevoel|Stijl|Haak
- **grootte:** 8
- **prefixen:** EROS:8
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur en gevoel: zaadbeurzen, parfum en ijzer. Stijl: onderhandeld, met contract. Instemming wordt gevraagd in de taal van de streek (zie EROS-TAAL-Z6). Haak: wie de streekregel breekt, verraadt waar h
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Genres in fase #
- **grootte:** 8
- **prefixen:** FASE:8
- **markering:** kern (niet aanraken)
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Genres in fase 0 Makers en Val: actie: ACTIE-Z9-35 (1); oorlog: OORLOG-Z9-1, OORLOG-Z9-2 (2); horror: HORROR-Z9-1, HORROR-Z9-2, HORROR-Z9-3, HORROR-Z9-4, HORROR-Z9-5, HORROR-Z9-6, HORROR-Z9-7, HORROR-
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Naam|Rol
- **grootte:** 8
- **prefixen:** PER:8
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Naam: Velith Ringzuster. Rol: uitvinder van Gavetechniek (technologie van magie). Laadster van de Orde die ontdekte dat twee voorwerpen van één man elkaar horen; vond de Echoring uit om haar verbannen
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Prijs|Haak (onthulling)
- **grootte:** 8
- **prefixen:** MET:7,GELD:1
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Vergeten metaal in fase 1 Overvloed: metalen ploeg uit een lander, gebruikt als heilig werktuig. Niemand weet dat het van het zaaischip Ysa komt; men gebruikt het als relikwie, niet als gewone technie
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Passende genres en rijen|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 8
- **prefixen:** REGIO:8
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Passende genres en rijen: actie: ACTIE-Z9-1, ACTIE-Z9-8, ACTIE-Z9-22, ACTIE-Z9-46 (4); saw: SAW-Z10-11, SAW-Z10-37 (2); comedy: COMEDY-Z10-4, COMEDY-Z10-23, COMEDY-Z10-38, COMEDY-Z10-53, COMEDY-Z10-60
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Oorzaak|Actie|Reactie / onbedoeld gevolg|Won|Verloor|Verzet|Officiële versie|Haak
- **grootte:** 7
- **prefixen:** GEB:7
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar -105 · Regio: Zoutkust · Wie: vrouwenleger van Zoutkust. Oorzaak: GEB-r10-zaadkruiken. Actie: Voor de slag ontvangen veertig krijgsvrouwen één vonkdrager. Reactie / onbedoeld gevolg: Ze winnen; m
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Vervuld door|Probleem|Mechanisme|Belang|Wereld|Huis|Individu|Wie heeft het nodig
- **grootte:** 7
- **prefixen:** FUNC:7
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Functiecategorie politiek. Vervuld door: LICH-dochters, LICH-pest, LICH-liora, LICH-macht-en-lichaam. Ook elders te krijgen (via geld, wetten, rituelen of wapens); body horror is hier een versterker, 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Aanraking|Geluid|Geur|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 7
- **prefixen:** ZINT:7
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Aanraking: huid die gloeit, overgevoelig, elke aanraking als een vonk. Geluid: een lach die geen reden heeft. Geur: ozon en zweet. Herkenbaar: Na een spannende dag samen uitrazen. Vreemd: Het lichaam 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie|Wat|Conflict|Haken
- **grootte:** 7
- **prefixen:** MEGA:7
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wie: de Kluwers, met hoofdpersoon HOOFDPERS-Z4-kluwer. Wat: Een korf wordt bewust en eist een stem in de raad na het Zegel. Conflict: de Orde wil de was, niet de stem; de korf kan de Pest stoppen of v
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Licht|Geluid|Aanraking|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 7
- **prefixen:** ZINT:7
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: inkt. Licht: kaars. Geluid: pennen. Aanraking: perkament. Herkenbaar: Een scriptorium. Vreemd: Zusters kopiëren de echte annalen. Scène: geheim. Haak: Een kopie lekt.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Functie|Quest|Bron van aantrekking
- **grootte:** 6
- **prefixen:** PLEK:6
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wastelands van grijs gesteente waar de zegellijnen zichtbaar gloeien; askouden, wilde askouden, de Asgrenswacht. Functie: afschrikking en navigatie. Quest: de laatste etappe naar de Zegel. [Functie: F
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Functie|Aantrekking
- **grootte:** 6
- **prefixen:** LICH:6
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Uitgeputte tempelstieren bij wie de zaadklieren necrotisch worden maar blijven produceren: zaad met etter en een zoete rottingsgeur. Het zaad is extra krachtig voor één uur. Functie: PROD;ECO. Afstoti
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Overvloed.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 1 Overvloed. In de Zusterburcht gebruikt Ildra bloed van gevangenen; een gevangene ontsnapt met haar notities. Zie VERHAAL-fase1.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Vonk.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 2 Vonk. Een kamerdame laat een diefstal gebeuren om haar bazin te vervangen. Zie VERHAAL-fase2.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Vonk.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 2 Vonk. Klok: drie dagen voor het leger uitrukt. Wie steelt de zaadkruiken? Zie VERHAAL-fase2.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Brand.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 3 Brand. Varr scheidt zich af omdat hij van de Zegel hoorde voordat die gelegd was. Zie VERHAAL-fase3.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Noodtoestand.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 4 Noodtoestand. Een volwassen geworden jongen uit het Jongenshof vlucht; de meesteres liet hem gaan. Zie VERHAAL-fase4.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Ontvangst.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 5 Ontvangst. Velk verkoopt Sterrensteen aan de Orde en weet dat tempels op lijnen staan. Zie VERHAAL-fase5.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Ontvangst.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 5 Ontvangst. Klok: één nacht voordat de cel gereinigd wordt. Zie VERHAAL-fase5.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Markt.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 6 Markt. De Hoge Moeder keurde de fokstal goed. Zie VERHAAL-fase6.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Markt.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 6 Markt. Pluu ontdekt dat zijn gangen de pest verspreiden. Zie VERHAAL-fase6.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Barsten.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 7 Barsten. Twee donkere heren. Zie VERHAAL-fase7.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Barsten.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 7 Barsten. Annike verbrandt haar archief. Zie VERHAAL-fase7.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geluid|Geur|Aanraking|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 6
- **prefixen:** ZINT:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geluid: zang van vroedvrouwen die van toonsoort wisselen. Geur: kamille, bloed, warm water. Aanraking: dampende doeken. Herkenbaar: Een geboorte met de hele familie in de keuken. Vreemd: Het lied vera
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Toestand|Verandert|Volgorde binnen de Oogstmaan
- **grootte:** 6
- **prefixen:** TOESTAND:6
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Jaar 801 (Oogstmaan), leeftijd 26, plaats: Brakhaven -> slikgang -> Nevelveen. Toestand: spioneert voor Ondessa, verkoopt Liora aan de Orde voor vrijheid (haar naam en de valse zwangerschapsregel uit 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Overvloed.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 1 Overvloed. Oda laat zonen uit de harem als doodgeboren registreren, zodat de kroon zonder erfgenaam blijft en van de Zusters afhangt. Eerste bewijs dat registers macht zijn. Zi
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Thrillerlijn, fase # Brand.
- **grootte:** 6
- **prefixen:** THRL:6
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Thrillerlijn, fase 3 Brand. Klok: negen dagen ontwenning onder Varnaths ogen; een spionne in het kamp. Zie VERHAAL-fase3.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** O:Intrige-affaire, fase # Noodtoestand.
- **grootte:** 6
- **prefixen:** INTR:6
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Intrige-affaire, fase 4 Noodtoestand. Saske dwingt Ylva te spioneren na het sparen van Halvar. Zie VERHAAL-fase4.
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Voordeel|Nadeel|Bron van aantrekking
- **grootte:** 5
- **prefixen:** DEG:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Ambergaardse rand en verlaten stallen. Ontsnapte of verlaten reuzenstieren, verder gegroeid door zegelwater; drie meter, gewapend, in benden. Voordeel: enorme kracht, ziekte-immuun. Nadeel: dom door h
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Eigenaar|Vorm van (voor)instemming|Label|Harde grens
- **grootte:** 5
- **prefixen:** LIJN:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Eigenaar: Orde. Vorm van (voor)instemming: gelofte, vaak onder geloofsdruk; vervalst bij ingeteelde Dochters. Volgt LIJN-fase-1 t/m 5; laatste echte keuze bij de Drempel (eind fase 1); vanaf fase 3 ge
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Haak (thriller)|Zintuig
- **grootte:** 5
- **prefixen:** D1:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Ze vloeken in woorden van het zaaischip zonder te weten wat ze betekenen; hun zwaarste vloek is "kern-leeg" (kernen op). Haak (thriller): een Dhurn hoort de vloek en herkent een machineterm. Zintuig: 
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Haak (intrige)|Zintuig
- **grootte:** 5
- **prefixen:** D1:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Bier van gist uit de diepe mijnen; licht gloeiend. Afrodisiacum voor de Vreemdelingsnacht. Haak (intrige): gist uit een nieuwe gang gloeit te fel; Orvald verzwijgt dat de gang naar een kluis leidt. Zi
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Levert|Zintuig|Haak|Functie|Crosslinks
- **grootte:** 5
- **prefixen:** BESLUIT:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Nee zeggen mag altijd met het heilige woord; weigeren vooraf kost rang. Wie niet kan weigeren (gebonden Dochters, Orrim) is de donkere kern. Levert: elke rite heeft een instemmingsspanning. Zintuig: H
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie (volwassen)|Zintuig en taal|Wat het kost|Haak
- **grootte:** 5
- **prefixen:** VERLEID:5
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie (volwassen): Saelith-dochter verleidt een gaven-man. Zintuig en taal: waaier, jasmijn, een blik die drie tellen te lang blijft. Wat het kost: haar huis verliest zaadrecht als het mislukt. Haak: hi
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie in de canon|Psychologie|Motief|Zintuig|Haak
- **grootte:** 5
- **prefixen:** SAW:5
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie in de canon: een uitgestoten Wortelbroeder met half vergroeide hand. Psychologie: gelooft dat lijden zuivert; hij huilt bij elke val. Motief: de Wortel voeden zodat Thalen sterft. Zintuig: het tik
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Geur|Geluid|Aanraking|Licht|Herkenbaar|Vreemd|Scène|Haak
- **grootte:** 5
- **prefixen:** ZINT:5
- **markering:** ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Geur: warme mest, hooi, natte vacht. Geluid: zwaar gesnuif, hoeven op klinkers. Aanraking: ruwe, warme flanken; een os leunt tegen je als hij je vertrouwt. Licht: ogen die bij zegellicht groen oplicht
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wie (volwassen)|Zintuig en taal|Wat het kost|Haak|Verbonden met|Overzicht|Zintuig erbij|Haak
- **grootte:** 5
- **prefixen:** VERLEID:5
- **markering:** al ideeenbank
- **voorstel:** Besluit Z36: blijft kaart in de ideeënbank; de verhalenmachine leest deze rijen als ideeën (ideeen_verwerking) en entert alleen wat ver genoeg van de canon ligt. Niet herschrijven zolang niets erop leunt.
- **voorbeeld:** Wie (volwassen): hofdame en een buitenlandse gezant. Zintuig en taal: wijn, kandelaars, een brief onder het kussen. Wat het kost: onthoofding bij ontdekking. Haak: beiden zijn spion voor dezelfde mees
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Historisch|Let op
- **grootte:** 5
- **prefixen:** TOESTAND:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Historisch: overleden ca. -80 (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen. Let op: dit volk leeft eeuwen (Aelthir ca. 900 jaar; Orrim zeer lang); het overlijdensjaar me
<!-- /REC -->
<!-- REC sjabloon_familie -->
### None · None
- **sig:** L:Wanneer|Waarom hier
- **grootte:** 5
- **prefixen:** VERHAALTIJD:5
- **markering:** structuur-voorstel
- **voorstel:** Besluit Z36: velden naar kolommen in een afgeleide view (voorbeeld personage_profiel); de tekst blijft als bron. Een rij die canon-gewicht krijgt, wordt eerst in eigen woorden herschreven.
- **voorbeeld:** Wanneer: fase 0, ca. -1240. Waarom hier: eerste prequel (goedgekeurd); stemming 5 tegen 4. Uitgewerkt in VERHAALTIJD-Z15-ysa en ROMANCE-Z15-ysa-beatplan.
<!-- /REC -->

<!-- SECTIE: SJABLOON_LID -->
