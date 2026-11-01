# Scorekaart Z39 (2026-11-01): personagenetwerk en simulatie, fase 4 Noodtoestand als proefomgeving

Basis: canon_backup_Z39.db (= canon_na_Z38.db). Resultaat: canon.db = /workspace/canon_na_Z39.db.
- toets.py groen na elke stap (38 regels; 0 nieuwe fouten). Nieuw: R-sim_harde_lijn en R-epistemiek.
- Roundtrip: 52 tabellen, 0 verschillen.
- Terugdraaitest (backup + r_Z39.py): 0 verschillen.
- Tweede run: 0 wijzigingen.
- md5 van de roman: af212ef0abde2bb41d71b1cb63f8b484, vóór en na gelijk.

## De 8 metingen van de canon-motor (vóór → na, z33/meet.py)

| # | meting | vóór | na |
|---|---|---|---|
| 1 | veranderproef (Thalen sterfjaar): plekken te wijzigen | 11 | 11 |
| 2 | duplicatiegraad: kopieën van ankerwaarden | 51 (1,5 per anker) | 51 (1,5) |
| 2b | letterlijke kopieën | 542 | 542 |
| 3 | dode links | 0 | 0 |
| 4 | herkomst: Kern met bron | 107/109 (98,2%) | 111/111 (100%) |
| 4 | herkomst: Structuur met bron | 1470/2612 (56,3%) | 1483/2625 (56,5%) |
| 5 | toetsen: exit, nieuw falend, aantal controles | 0, 0, 36 | 0, 0, 38 |
| 6 | roundtrip: tabellen, verschillen | 42, 0 | 52, 0 |
| 7 | terugdraaien | werkt | 0 verschillen in 52 tabellen |
| 8 | koude lezer (canon) | 10/10 | 10/10 |

Kern-lagen na Z39: hard 103, bijbel 8. EROS-GRENZEN-Z7 heeft nu BESLUIT-Z30-4 als bron (hard); GES-officiele-versie de wereldbijbel.

## Acceptatiecriteria van de aanscherping

### 1. Geen nieuwe canonfeiten

Er zijn 15 nieuwe canonrijen:
- 5 besluiten van Rogier (BESLUIT-Z39-1 tot -5);
- 10 premisses in de ideeënbank, met status voorlopig, ideeenbank=1 en epistemiek simulatie.

De simulatie zelf schrijft alleen in de simulatietabellen. De motor draait op bestaande canon:
- de 28 benoemde fase-4-personages uit personage_profiel;
- regels met een canonbron;
- de beroepen uit de tabel beroep.

Getallen die de canon niet geeft, zijn als aanname gemarkeerd in sim_regel.aanname en in de epistemiek:
- de bevolking per regio;
- de reistijd;
- de levensduur 70 (al een aanname in het anker).

### 2. Epistemiek

Elke rij in verblijf, kennis, per_relatie, sim_figuur, sim_regel, gebeurtenis_type, tech_gebeurtenistype, sim_run, sim_gebeurtenis en steekproef heeft een epistemiek, net als elke Z39-canonrij.
- R-epistemiek toetst dit; simulatierijen moeten run-id en seed noemen.
- Kennis die uit de canon komt (eigen geheim, Relaties) heet 'feit', met de kanttekening dat het jaartal een aanname is.

### 3. Werkt het netwerk? De informatieproef

Dezelfde 200 seeds zijn twee keer gedraaid: met informatieverschillen, en met iedereen weet alles. Elke beslissing heeft een eigen toevalsstroom per personage en seizoen (common random numbers). Verschillen komen dus door de kennis, niet door het toeval.

| uitkomst | runs met een andere uitkomst |
|---|---|
| wie chanteert, verraadt, verbindt of zweert wie | 200/200 (100%) |
| instituten of hun jaar | 163/200 (82%) |
| sterfjaren van canonpersonages | 6/200 |
| gemiddelde Jaccard-afstand tussen de relatiesets | 0.846 |
| chantage per run (gemiddeld) | 62 → 288 |
| verraad per run (gemiddeld) | 32 → 88 |

Oordeel: het criterium slaagt.
- Als iedereen alles weet, ontstaan er 4,6 keer zoveel chantages en 2,8 keer zoveel verraad, en de intriges gaan tussen andere mensen.
- Sterfjaren veranderen bijna niet. Dat komt doordat canonpersonages beschermd zijn tot hun canonjaar.
- Dat ook de instituten verschuiven, komt doordat kennis via de Zusters terugwerkt op wie wanneer leeft en waar is. Dat is een echt netwerkeffect, maar ook een teken dat de motor gevoelig is.

### 4. Parameters, aannames en seeds

Alle 18 regels staan in sim_regel, met parameter, waarde, bron_code en aanname (0/1); de typen staan in gebeurtenis_type. Seeds:
- fase 4: 390000–390999;
- zonder Kernbescherming: 390000–390199;
- alwetend: 390000–390199;
- technologie: 391000–391999;
- fase 5: 395000–395049.

Elke run is reproduceerbaar via sim.Wereld(seed,…).run(). De terugdraaitest bewijst dat: 2.450 runs geven bit voor bit dezelfde tabellen.

### 5. Tien handgeschreven premisses

Zie hieronder. Elke premisse heeft codes naar de canon in verwijst_naar.

### 6. Een andere fase zonder codewijziging

Fase 5 Ontvangst (130–340) is gedraaid met 50 runs. Er waren 28 benoemde personages; 50/50 runs waren geldig. Gemiddeld per run: intrige 32.6, gebeurtenissen 476.22.

Eerlijk: de motor draait in fase 5, maar begint zonder de eindtoestand van fase 4. Daardoor 'ontstaan' Deelwet en register opnieuw. Voor echte fase-5-verhalen is een fase-overgang nodig (KEUZE-Z39-validatie).

### 7. Bestaande tests

Alle 36 oude toetsregels draaien nog, 2 zijn erbij gekomen.
- Er is geen ongeautoriseerde canonwijziging. Op Kern-rijen veranderde alleen bron_handmatig van EROS-GRENZEN-Z7 en GES-officiele-versie, op besluit van Rogier.
- Reproduceerbaarheid, idempotentie, roundtrip en terugdraaien zijn groen.

### 8. Meetbare maten

- **Causale samenhang:** 4892/4892 gebeurtenissen in de bewaarde runs (100%) hebben een oorzaak die terugleidt naar een sim_regel, een canonrij, een kennisrij of een eerdere gebeurtenis. Kanttekening: bij gebeurtenissen zonder specifieke oorzaak is dat de bronregel van hun type. Dat is een keten tot een parameter, maar wel een grove.
- **Canonconsistentie:** toets.py is groen. Er zijn 0 botsingen met v_kern: geen Kern-rij is overschreven of vervangen.
- **Diversiteit:** de minimale onderlinge afstand tussen de premisses is 4 van 5 assen (personen, plek, patroon, belang, geheim); het dichtstbijzijnde paar is IDEE-Z39-2 en IDEE-Z39-4. Doel ≥ 3: gehaald.
- **Spanning per premisse:** zie de tabel hieronder. Dit zijn handmatige tellingen van de architect, geen automatische meting.

## Premisses en succescriterium

| code | personages | belang | botsende belangen | onomkeerbare keuzes | relevante geheimen | max. 3-grepen-overlap met een bestaande rij | personages + belang al samen in een rij? |
|---|---|---|---|---|---|---|---|
| IDEE-Z39-1 | PER-ondrea, PER-kesh-lijn, PER-nessa-weerstand | dorp laten bestaan | 3 | 1 | 2 | 2.9% (PER-kesh-lijn) | nee |
| IDEE-Z39-2 | PER-f4-clan-rover-gunnar, PER-f4-ylva, PER-f4-eiland-moeder-runa | niet nog eens verkocht worden | 2 | 1 | 1 | 2.7% (VOLK-GESCHIEDENIS-OVERZICHT-Z4-saelmor-Z32) | nee |
| IDEE-Z39-3 | PER-f4-registerzuster-tine, PER-f4-buurvrouw-aaltje, PER-f4-brecht | eigen schuld kwijt | 2 | 1 | 2 | 3.4% (DAG-TOP-ithrael-geheim) | nee |
| IDEE-Z39-4 | PER-f4-dochter-edrun, PER-f4-saske, PER-orvath, PER-f4-edrun | afkomst geheim houden | 3 | 2 | 2 | 3.3% (VERHAAL-fase4-Z35) | nee |
| IDEE-Z39-5 | PER-f4-jongenshof-meester, PER-ithra-oud | het Hof veilig houden | 2 | 1 | 1 | 2.7% (ZINT-Z2-wetten-3) | nee |
| IDEE-Z39-6 | PER-f4-zuster-ondrea-leerling, PER-f4-gedeelde-man-ruben, PER-f4-orde-moeder-iris | het rooster eerlijk maken | 3 | 1 | 2 | 3.1% (INTR-fase4-rustmaanden) | nee |
| IDEE-Z39-7 | PER-orvath, PER-f4-eiland-moeder-runa | volk verbergen | 2 | 1 | 1 | 4.8% (VERHAAL-fase2-Z36) | nee |
| IDEE-Z39-8 | PER-f4-orde-moeder-iris, PER-f4-zuster-ondrea-leerling, PER-f4-jongenshof-meester | opvolging | 2 | 1 | 2 | 7.0% (PER-f4-orde-moeder-iris) | nee |
| IDEE-Z39-9 | PER-f4-boerin-lise, PER-f4-tharn-bula | eigen leven | 2 | 1 | 1 | 7.9% (PER-f4-tharn-bula) | nee |
| IDEE-Z39-10 | PER-f4-veerman-dries, PER-f4-edrun, PER-f4-saske, PER-f4-buurvrouw-aaltje | herberg en ring houden | 3 | 1 | 1 | 2.9% (ROM-fase6-hork-lezen) | nee |

Succescriterium: elke premisse deelt hooguit 7,9% woord-3-grepen met een bestaande rij (grens 20%), en bij geen enkele komt de combinatie van personages en belang al in een bestaande rij voor. Gehaald.

Kanttekening bij de nieuwheidstoets: personages worden herkend aan hun code of voornaam, belangen aan het eerste woord. Dat is een heuristiek.
- IDEE-Z39-1 kreeg een andere cast omdat de eerste versie (Ondrea, Halvar, Brecht) samen in VERHAAL-fase4 stond.
- IDEE-Z39-2 kreeg Runa erbij omdat Gunnar en Ylva al in Gunnars eigen rij samen staan.

Herkomst van de premisses:
- 8 volgen direct uit gebeurtenissen of graafvragen in run Z39-F4-0203 (2, 3, 4, 5, 6, 7, 8, 10).
- IDEE-Z39-1 combineert graafuitkomsten met de canonrol van Kesh.
- IDEE-Z39-9 bouwt op Lise's migratie en verbintenis in Hoogvrouwe.

## De tien premisses


**IDEE-Z39-1** (PER-ondrea;PER-kesh-lijn;PER-nessa-weerstand;GEB-r10-eerste-register;GEB-r10-neven-ramp)

Ondrea de Telster wil dat het register ook de dorpen zonder papier telt, en het eerste dorp dat ze bezoekt is dat van Kesh van de Neven, waar de kinderen elkaars neven zijn. Nessa Weigeraar heeft daar mannen verstopt en wil dat vrouwen blijven kiezen. Kesh kan haar dorp redden door Nessa's schuilplaats te noemen, of het dorp opgeven door te zwijgen, en Ondrea schrijft op wat ze ook kiest.

**IDEE-Z39-2** (PER-f4-clan-rover-gunnar;PER-f4-ylva;PER-f4-eiland-moeder-runa;GEB-r10-mannenroof;REG-stille)

Gunnar Bootsman werd zelf ooit geroofd en vaart nu mee op Ylva's rooftochten naar de eilanden van Runa van de Mist. Een man die hij daar meesleepte herkent hem als iemand van een andere clan en wil ermee terug naar huis. Gunnar wil vooral nooit meer van eigenaar wisselen, dus geeft hij de jongen bij Ylva aan voordat die hem kan aangeven, en hij weet dat hij daarmee doet wat hem zelf is aangedaan.

**IDEE-Z39-3** (PER-f4-registerzuster-tine;PER-f4-buurvrouw-aaltje;PER-f4-brecht;VALS-noodtoestand;GEB-r10-deelwet-weerstand)

Zuster Tine Telster vervalste één blad in Ambergaard om Brecht te laten gaan. Aaltje Zonderman, die ooit zelf een man in haar schuur verborg, ziet dat het blad niet klopt. Tine dreigt dat oude geheim te noemen, maar Aaltje gaat toch naar Saelith. Na die reis heeft geen van beiden nog iemand in het dorp die voor haar wil liegen.

**IDEE-Z39-4** (PER-f4-dochter-edrun;PER-f4-saske;PER-orvath;PER-f4-edrun;GEB-r10-laatste-koning)

Isolde Edrunsdochter is negentien en weet dat Saske heeft gelogen over wie haar vader is. Om Saske voor te zijn klaagt ze Orvath de Moeras aan, die zijn beurten laat lopen voor een geroofde eilander. Saske slaat terug door Isoldes eigen blad open te leggen, en zo staat de dochter van de laatste koning ineens in het register waar ze zich voor verborg.

**IDEE-Z39-5** (PER-f4-jongenshof-meester;GEB-r10-jongenshof;GEB-r10-mannenroof;PER-ithra-oud)

Hofmeesteres Gerdien weet welke jongens in het Hof verwant zijn, en ze houdt van een man die Ylva van de eilanden roofde. Hij heeft gezien hoe ze de lijsten schuift en wil met die kennis een boot naar huis kopen. Geeft ze hem de boot, dan gaat ook haar lijst mee naar wie hem op de eilanden wil lezen. Houdt ze hem vast, dan heeft ze de enige vreemde verraden die haar ooit om zichzelf koos.

**IDEE-Z39-6** (PER-f4-zuster-ondrea-leerling;PER-f4-gedeelde-man-ruben;PER-f4-orde-moeder-iris;GEB-r10-rotatie;GEB-r10-uitputting)

Fenna Rekenaarster schrijft rustmaanden in het rooster die niemand verdiend heeft. Ze merkt dat Ruben Gedeelde, beurt na beurt, nooit een kind verwekt. Laat ze dat staan, dan beschermt ze een onvruchtbare man die liever bij één geliefde blijft; meldt ze het, dan valt haar eigen gesjoemel mee om. Ze kiest voor Ruben en betaalt met de eerste vraag die Moeder Iris over het rooster stelt.

**IDEE-Z39-7** (PER-orvath;PER-f4-eiland-moeder-runa;GEB-r10-eilanden-weigering;UIT-VOLK-saelmor)

Orvath de Moeras deelt met Runa van de Mist een bed en een geheim: de Oevrin hebben één op twee en geen Zegel. Runa wil haar eilanden buiten de rotatie houden en ziet in de slikgangen een schuilplaats voor mannen. Orvath weet dat de Orde zijn volk gaat leegroven zodra iemand die gangen ziet. Hun weigering en hun liefde kunnen niet allebei geheim blijven.

**IDEE-Z39-8** (PER-f4-orde-moeder-iris;PER-f4-zuster-ondrea-leerling;PER-f4-jongenshof-meester;GEB-r10-orde-naam;GEB-r10-dankpreek)

Moeder Iris en Fenna zweren allebei trouw aan Gerdien, de vrouw die het Hof echt bestuurt. Iris schreef de eerste liturgie in het geheim en wil dat de Orde een kerk wordt; Fenna wil een eerlijk rooster. Wie van de twee Gerdien kiest, wordt opvolgster. De ander moet dan haar geheim zien te houden tegenover de vrouw die het al kent.

**IDEE-Z39-9** (PER-f4-boerin-lise;PER-f4-tharn-bula;REG-hoogvrouwe;KAART-seizoenen;WET-wie-weigert)

Lise Zonderkind wil geen kind, alleen een eigen leven, en vlucht met een Tharn-vrouw over de pas naar de dijken van Bula. In Hoogvrouwe kent niemand het register, maar de Zegel raakt ook de Tharn, en Bula heeft handen nodig, geen gasten. Lise moet kiezen: de dijk mee bouwen tot ze bij die mensen hoort, of terug naar een rooster dat haar weigering opschrijft.

**IDEE-Z39-10** (PER-f4-veerman-dries;PER-f4-edrun;PER-f4-saske;PER-f4-buurvrouw-aaltje;ZAAD-VERHAAL-fase4-a)

Dries Pontbaas bewaart de ring van koning Edrun en zou die voor geen register afgeven. Hij heeft Saske eens aangegeven om een schuld af te lossen. Nu klaagt een buurman hem aan omdat hij zijn beurt laat lopen voor Aaltje. Saske biedt hem een uitweg: de ring tegen een schone lei. Neemt Dries die, dan is het laatste bewijs van de laatste koning in handen van de vrouw die hem liet vallen.

## Monte Carlo fase 4 (1.000 runs) en validatie tegen de canon

Er zijn 0 runs weggegooid met Kernbescherming. Zonder Kernbescherming waren het 174/200 (87%), allemaal op de anker-invariant: een canonpersonage stierf vóór zijn canonjaar. De vaakst getroffen personages:
- Zzak: 28;
- Kerl: 18;
- Lise: 14;
- Runa: 9;
- Orvath: 9.

De andere invarianten zijn in geen enkele run gebroken: niemand handelt na zijn dood, niemand is op twee plekken, niemand weet iets vóór de bron bestaat.

| canongebeurtenis | canonjaar | ontstaat in % runs | binnen ±10 jaar | mediaan jaar |
|---|---|---|---|---|
| GEB-deelwet-40 | 40 | 100.0% | 46.6% | 29.0 |
| GEB-r10-eerste-register | 22 | 100.0% | 96.0% | 20.0 |
| GEB-r10-jongenshof | 50 | 99.2% | 25.6% | 35.0 |
| GEB-r10-rotatie | 78 | 100.0% | 0.2% | 51.0 |
| GEB-r10-orde-naam | 90 | 100.0% | 0.2% | 60.0 |
| GEB-r10-eilanden-weigering | 100-130 | 99.9% | 12.1% | 86 |
| GEB-r10-mannenroof | 18-35 | 100.0% | 100.0% | 15.0 |
| GEB-r10-neven-ramp | 33-38 | 2.0% | 2.0% | 36.0 |
| GEB-r10-deelwet-weerstand | 41-60 | 98.2% | 34.9% | 29.0 |
| GEB-r10-uitputting | 60-80 | 59.2% | 0.6% | 123.0 |
| Raad der Moeders 7 tegen 5 (jaar -3) | -3 | 24.7% precies 7-5 | – | meest voorkomende uitslag: 7-5 |

| canongebeurtenis buiten fase 4 | uitkomst |
|---|---|
| Pest van 340 | 0%: niet te toetsen. Er is geen ziektemodule, en fase 6 is niet gesimuleerd. |
| Crash van de Zaadbeurs in 762 | 0%: niet te toetsen. Er is geen prijs- of schuldmechaniek, en fase 7 is niet gesimuleerd. |

Wat dit zegt over de regels:
- De volgorde ontstaat vanzelf: roof → register → Deelwet → weerstand → rooster → Orde → eilanden. Mannenroof en register vallen goed in hun venster.
- Rooster en Orde ontstaan wel, maar 25–30 jaar te vroeg. Er ontbreekt een rem die de canon kent maar de regels niet: KEUZE-Z39-tijdlijn.
- De inteeltramp ontstaat bijna nooit (2%), omdat het register te snel overal is: KEUZE-Z39-nevenramp.
- De stemming 7-5 is in deze aanname-parameters de meest waarschijnlijke uitslag (25%). Dat is plausibel, maar niet afgeleid: de stemkansen zijn aannames.
- Monte Carlo is hier verkenning, geen bewijs: ik heb niet bijgesteld tot het past.

## Module technologie en beroepen (1.000 runs, eigen invariant: 0 overtredingen)

| techniek | ontstaat | mediaan | canon | binnen ±10 j |
|---|---|---|---|---|
| register | 99.9% | 12 | 22 | 36.8% |
| bloedmerk | 99.9% | 21 | 28 | 38.4% |
| jongenshof | 98.7% | 32 | 50 | 19.6% |
| rooster | 89.4% | 46.0 | 78 | 11.7% |

De kennis van de Makers is in 89.2% van de runs in 130 jaar in alle regio's vergeten. Prijs in lichamen: zie sim_gebeurtenis, type prijs.

Beroepen:
- jongensverstopster: 100% van de runs, met zwarte tweeling;
- naamgever: 100%, met zwarte tweeling;
- nee-getuige: 100%, met zwarte tweeling. De koppeling van nee-getuige aan het register is een aanname.
- De andere 8 Z37-beroepen horen niet in fase 4: de techniek van hun wereldregel bestaat dan nog niet.

## Controle (11d)

### Steekproef

- 50 willekeurige nieuwe rijen (seed 39), automatisch beoordeeld en daarna door mij gelezen: 0 fout.
- De 95%-bovengrens van het foutpercentage is 7,1% (Clopper-Pearson). Volgens de regel (bovengrens > 2% = afkeuren) is de ronde daarom formeel afgekeurd. Dat komt niet door fouten: het criterium is met n=50 onhaalbaar. Daarvoor zijn minstens 183 foutloze rijen nodig (KEUZE-Z39-steekproef).
- Ik ben niet onafhankelijk: ik heb de rijen zelf gemaakt.

### Koude lezer

- Eerste poging: 8/10. View v_sim_validatie groepeerde per type, waardoor een lezer de verkeerde rij kon pakken. De view is verbeterd (zie z39/koude_lezer_eerste_poging.txt).
- Daarna: 10/10, alleen uit de views beantwoord en vergeleken met een directe telling (z39/koude_lezer.txt).
- Kanttekening: de vragen zijn door mij gesteld, dus het is geen echt koude lezer.
