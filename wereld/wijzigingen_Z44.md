# Ronde Z44: de lange tijd, van de landing tot nu

Opdracht van Rogier (2 november 2026): het verloop uitwerken van aankomst tot nu, voor alles een verhaal, en de database slim verder opbouwen.

## Het basisverhaal in één alinea
Na de landing kan niemand meer zelf ja zeggen: de sleutel breekt, de Stemklok leest namens het lichaam, en het Zegel zegt ruim tweeduizend jaar ja namens ieder lichaam (-1240 tot 801). Daardoor is er magie: vonk, gaven, zegellicht, en volken die het Zegel vormde. In 801 geeft Liora de sleutel aan iedereen. Vanaf dan kan elk lichaam nee zeggen, ook tegen de magie. Er zijn dan nog heel veel wezens, maar wat het Zegel droeg, slijt per generatie. Eerst verdwijnen de gaven, dan de volken die het Zegel erfelijk maakte, dan de lang levenden en de steen, dan de laatste wonderen. Wat overblijft, is Midden-aarde, dan een wereld van alleen mensen, dan de grote smelt die het land van Velmara onder zee zet, dan de stilte, en dan ons schrift.

## De tijdas (afgeleid: tabel `tijdas`, view `v_tijdlijn`)
| Fase | Naam | Zegeljaar | Jaren geleden (BP) | Status |
|---|---|---|---|---|
| 0 | 0 Voortijd | -1240 tot -600 | 27.191 tot 26.551 | canon |
| 1 | De Overvloed en de Kroon | -600 tot -150 | 26.551 tot 26.101 | canon |
| 2 | De Vonk | -150 tot -40 | 26.101 tot 25.991 | canon |
| 3 | De Grote Brand | -40 tot 0 | 25.991 tot 25.951 | canon |
| 4 | De Noodtoestand | 0 tot 130 | 25.951 tot 25.821 | canon |
| 5 | De Heilige Ontvangst | 130 tot 340 | 25.821 tot 25.611 | canon |
| 6 | De Markt van het Lichaam | 340 tot 720 | 25.611 tot 25.231 | canon |
| 7 | De Barsten | 720 tot 801 | 25.231 tot 25.150 | canon |
| 8 | 801 (nu) | 801 tot 802 | 25.150 tot 25.149 | canon |
| 9 | 9 Tijd van de Ja (na 801) | 801 tot 1531 | 25.150 tot 24.420 | voorstel |
| 10 | 10 Tijd der Volken (na 801) | 1531 tot 3011 | 24.420 tot 22.940 | voorstel |
| 11 | 11 Heldentijd (na 801) | 3011 tot 3761 | 22.940 tot 22.190 | voorstel |
| 12 | 12 Het Vertrek (na 801) | 3761 tot 5831 | 22.190 tot 20.120 | voorstel |
| 13 | 13 Tijd der Mensen (na 801) | 5831 tot 6951 | 20.120 tot 19.000 | voorstel |
| 14 | 14 De Grote Smelt (na 801) | 6951 tot 17751 | 19.000 tot 8.200 | voorstel |
| 15 | 15 Het Zwevende Gat (na 801) | 17751 tot 20751 | 8.200 tot 5.200 | voorstel |
| 16 | 16 Tijd van het Schrift (na 801) | 20751 tot 25951 | 5.200 tot 0 | voorstel |

Anker: 801 ligt op 25.148 BP (band 21.802 tot 26.661); vandaag is het ongeveer Zegeljaar 25.950. Wat het hardst knelt: Velmara moet op droog plat leven (laag water) en de mythen moeten gevormd zijn vóór Amerika.

## Wat wanneer verdwijnt (mediaan, Zegeljaar waarin het legende wordt)
| Wezen | Legende rond | Verhaal |
|---|---|---|
| aelthir | 1761 | `LOT-Z44-aelthir` (10 Tijd der Volken (na 801)) |
| dhurn | 2081 | `LOT-Z44-dhurn` (10 Tijd der Volken (na 801)) |
| kluwers | 2621 | `LOT-Z44-kluwers` (10 Tijd der Volken (na 801)) |
| orrim | 2991 | `LOT-Z44-orrim` (10 Tijd der Volken (na 801)) |
| registerkraaien-stem | 2101 | `LOT-Z44-registerkraaien-stem` (10 Tijd der Volken (na 801)) |
| sterrensteen | 2941 | `LOT-Z44-sterrensteen` (10 Tijd der Volken (na 801)) |
| tharn | 2211 | `LOT-Z44-tharn` (10 Tijd der Volken (na 801)) |
| wiegkasten | 1921 | `LOT-Z44-wiegkasten` (10 Tijd der Volken (na 801)) |
| leegtewormen | 3431 | `LOT-Z44-leegtewormen` (11 Heldentijd (na 801)) |
| sael-mor | 3131 | `LOT-Z44-sael-mor` (11 Heldentijd (na 801)) |
| kluisschip | 5801 | `LOT-Z44-kluisschip` (12 Het Vertrek (na 801)) |
| wortelstem | 4111 | `LOT-Z44-wortelstem` (12 Het Vertrek (na 801)) |
| ishvar | blijft | `LOT-Z44-ishvar` (16 Tijd van het Schrift (na 801)) |
| myrrhen | blijft | `LOT-Z44-myrrhen` (16 Tijd van het Schrift (na 801)) |
| oevrin | blijft | `LOT-Z44-oevrin` (16 Tijd van het Schrift (na 801)) |
| gaven-mannen | 1061 | `LOT-Z44-gaven-mannen` (9 Tijd van de Ja (na 801)) |
| grauwen | 981 | `LOT-Z44-grauwen` (9 Tijd van de Ja (na 801)) |
| karruk-storm | 1091 | `LOT-Z44-karruk-storm` (9 Tijd van de Ja (na 801)) |
| reuzenstieren | 841 | `LOT-Z44-reuzenstieren` (9 Tijd van de Ja (na 801)) |
| skerra | 1261 | `LOT-Z44-skerra` (9 Tijd van de Ja (na 801)) |
| vathren | 951 | `LOT-Z44-vathren` (9 Tijd van de Ja (na 801)) |
| ves-lethi | 1371 | `LOT-Z44-ves-lethi` (9 Tijd van de Ja (na 801)) |
| zegellicht | 1531 | `LOT-Z44-zegellicht` (9 Tijd van de Ja (na 801)) |

## Verhalen per tijdperk
- **Een grijze steen in een museum** (`VERHAAL-Z44-tijdperk-16`): In onze tijd beschrijft een geologe een grijze steen uit een kraterveld die breekt als glas en die geen bekende inslag verklaart. Haar moeder hield vroeger kippen in een tuin vol feeënringen en had een vonk die nooit iemand geloofde. Op een avond legt de geologe de steen op tafel en hoort, zacht, een klik aan het eind van een zin die ze niet verstaat. Ze schrijft het op en gooit het weg. De lezer weet beter.
- **De laatste die het wist** (`VERHAAL-Z44-tijdperk-15`): In een dorp aan een nieuwe kust leeft een oude vrouw die drie woorden kent waarvan niemand de betekenis weet: ysa, kern, wieg. Ze zingt ze bij elke geboorte. Haar kleinzoon vraagt wat ze betekenen; ze weet het niet meer, alleen dat je ze moet zeggen. Na haar dood zingt hij ze verkeerd, en zijn dochter maakt er een godin van. Zo verdwijnt het laatste wat een mens van de Makers wist, en zo begint het eerste geloof.
- **Het water komt** (`VERHAAL-Z44-tijdperk-14`): Elk jaar staat het water een handbreed hoger aan de oude kust van de Zoutkust. De Oevrin merken het eerst: hun paaipoelen verzilten, hun slikgangen lopen vol. Een Oevrin-vrouw en een mensenman die samen een veer houden, moeten kiezen tussen de zee in of het land op. Achter hen verdwijnen de ruïnes van Ves-Anath onder water. Kinderen die nooit iets van de stad wisten, horen later van een stad die verzonk om haar trots, en van klokken die je nog hoort bij stil weer.
- **Over de landbrug** (`VERHAAL-Z44-tijdperk-13`): Een familie met Ishvar-bloed en een grootmoeder die nog zingt in de akkoorden van de Oevrin trekt achter de rendieren aan, het droge plat over, naar het oosten waar de zon opkomt. Ze nemen geen voorwerpen mee, alleen verhalen: een vrouw die opende, een slang die de wereld rond voer, een man die vuur haalde. Elke winter vertellen ze ze anders. Waar ze stoppen, groeien in het gras kringen paddenstoelen, en de grootmoeder zegt dat de doden daar dansen.
- **Het schip naar de bewegende ster** (`VERHAAL-Z44-tijdperk-12`): De laatste Aelthir verzamelen zich aan de kust waar een lander van de Makers ligt die nog één vlucht heeft. Een mens die ze liefheeft, mag niet mee; aan boord stopt de tijd voor wie gaat, niet voor wie blijft. In dezelfde jaren spoelen de laatste Leegtewormen aan, met lege ruimen, en zwijgt de stem in de Wortel na een laatste vraag. Als de lander opstijgt, ziet de mens de bewegende ster nog een winter lang. Dan staat hij stil.
- **De laatste kluis** (`VERHAAL-Z44-tijdperk-11`): Een mensenvrouw met een vonk die nauwelijks een kaars aansteekt, een Dhurn met de laatste handen die een kluis kunnen openen, en een Aelthir die haar eigen naam aan het vergeten is, zoeken een kluis waar nog een Wiegkast zou werken. Onderweg laat een Tharn hen door een poort die al eeuwen niet meer verdedigd wordt, alleen om iemand te spreken. De kluis werkt nog één keer. Daarna gloeit de Sterrensteen niet meer, en de Dhurn weet dat zijn volk geen dochters meer zal krijgen.
- **De Val van Hoornburg** (`VERHAAL-Z44-tijdperk-10`): Kharvos is het laatste land waar de machines nog zoemen, op de kern van de Harrow onder de burcht van Hoornburg. Ves-Lethi trekken erheen omdat hun gezicht daar nog wisselt; Skerra zonder vleugels laten zich er dragen door luchtschepen die niemand meer kan bouwen. Een Kharvos-vorstin weigert te geloven dat de kern op raakt en laat hem harder draaien. Hij bezwijkt in één nacht. Wat de overlevenden aan de kust vertellen, is het verhaal van een trots land dat de goden te veel vroeg.
- **De eerste nee** (`VERHAAL-Z44-tijdperk-9`): Hanne is stalmeesteres in Ambergaard als het Lichtconvent van 806 de geloften ongeldig verklaart. Haar mannen mogen nu weigeren, en de eerste die het doet, is de man die ze het meest vertrouwt. In dertig jaar zien haar dochters wat zij nooit zag: broers. Tegelijk sterven in de achterste stal de reuzenstieren, onvruchtbaar en woedend, een voor een. Ze laat de deuren openstaan. Als haar kleindochter het laatste zegellicht in Saelith ziet uitgaan, denkt ze dat het de lamp van een kapel is.

## Hoe de database slim verder groeit
- **Geen nieuwe bron, wel nieuwe afgeleiden.** `tijdas`, `tijdperk_label` en `v_tijdlijn` worden bij elke bouw uit de FASE-rijen en `TIJD-anker` gemaakt. Een nieuw tijdperk is gewoon een FASE-rij die begint met "X tot Y"; de as rekent de rest uit, ook de jaren BP.
- **Eén as voor alle tellingen.** Elk tijdperk-label in de canon (31 soorten, van "0 Voortijd" tot "Tijd der Koningen") wordt op de as gelegd; wat niet past, meldt de nieuwe signaalregel `R-tijdperk_onbekend`. Zo groeit de opschoning mee.
- **Simulatie als voorstel, data als bron.** `tijd/wezens.yaml` noemt bij elk getal de canonrij; `tijd/verlies.py` rekent de bandbreedte; de rijen dragen epistemiek "voorstel". Verandert de canon (bijvoorbeeld de levensduur van de Aelthir), dan draai je de simulatie opnieuw en schuiven de tijdperken mee.
- **Alles hangt aan elkaar.** Elk LOT-verhaal verwijst naar zijn volk en naar de MYTHE-rij van Z43; elk tijdperkverhaal naar zijn FASE-rij. In de knopenkaart zie je zo per wezen: oorsprong, mythe en verlies.
