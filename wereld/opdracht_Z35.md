# Opdracht ronde Z35: rijm en opschoning

Van: architect (onafhankelijke toetser van Z34)
Voor: de bouwer van canon.db
Basis: canon_na_Z34.db. De skill `canon-motor` is de meetlat.

## Waar we staan

Z34 is goed: constraints werken, handwerk wordt niet overschreven, nul dode links, er is een regeltabel en ankers, de mal is per boog gebroken (`boog.vorm/verteller/tempo`) en elk hoofdpersonage heeft een eigen fout. Niets daarvan terugdraaien.

Er blijven vier problemen:

1. **Gegenereerde personagerijen staan in Structuur.** Ruim 1.200 TOESTAND-, Geboren-, Overleden- en "In # actief"-rijen. Daarvan hebben 557 een aanname (280 keer "levensduur 70") en 330 lege velden ("Wil: -", "regio onbekend"). Het zijn velden in lopende tekst en gokken van een script. Een agent leest ze als feit.
2. **De motor heeft geen rijmregel.** Herhaling is het ontwerp: elke fase draait probleem, noodoplossing, prijs en vervalsing. Maar er is nergens vastgelegd *wat* elke fase verschuift en *wat* ze erft. Zonder die regel wordt herhaling een kopie in plaats van een rijm.
3. **De synopsen dragen nog het invulformulier.** In de 28 fasebogen staan steeds BEGIN/ESCALATIE/KEERPUNT (7/7), "Herkenbaar:" (21), "Kernscènes:" (18) en "Zaad:" (26). Zaadjes staan daardoor dubbel: in de tekst én in de tabel `zaadje`.
4. **Herkomst bij Structuur is 36%.** De norm is 90%.

## Harde randvoorwaarden

- Geen Kern-inhoud wijzigen. Inhoudelijke keuzes worden voorstellen met `voorlopig`, en Rogier stelt ze vast.
- Nooit verwijderen. Oude rijen gaan naar `voorlopig, vervangen` met `vervangen_door`.
- Elke structuurwijziging via een genummerde migratie, en elke inhoudelijke wijziging in `wijziging`.
- Je bent de enige bouwer in deze ronde.
- Na elke stap draai je `toets.py`, en die moet groen zijn.

## Stap 1: personagetoestand naar kolommen (principe 5)

1. Maak via migratie de tabel `personage_toestand`: `per_code`, `jaar`, `leeftijd`, `rol`, `regio`, `wil`, `geheim`, `verandert`, `aanname` (0/1), `aanname_reden`, `bron`.
2. Parse alle TOESTAND-, Geboren-, Overleden- en "In # actief"-rijen naar deze tabel. Een "-" of "onbekend" wordt NULL, en wordt dus niet als waarde opgeslagen.
3. Sla aannames niet op als feit. Sterfjaren op basis van een levensduur worden berekend in de view `v_personage_tijdlijn`, met een levensduur per volk uit één ankertabel. Neem daarbij de langlevende volken Aelthir en Orrim mee (WRIJ-Z14-2). De view toont `aanname = 1` zichtbaar.
4. Zet de oude rijen op `voorlopig, vervangen` met `vervangen_door` = de PER-code van het personage.

**Klaar als:**
- `v_actief` bevat 0 rijen met "Wil: -", "Geheim: -", "regio onbekend" of "aanname: levensduur";
- het aandeel canonrijen buiten de ideeënbank dat in een sjabloonfamilie zit, daalt van 61% naar minder dan 35%;
- alle bestaande views en ankers werken nog.

## Stap 2: de rijmregel voor de motor

De 8 fasen (0 Voortijd t/m 7 Barsten) plus 801 vormen een spiraal, geen cirkel. Leg dat vast.

1. Voeg via migratie de tabel `fase_rijm` toe, één rij per fase:
   - `fase`
   - `mechanisme`: welk deel van probleem, noodoplossing, prijs en vervalsing hier herhaalt
   - `beslisser`
   - `betaler`
   - `vervalst`: wat er wordt vervalst, of "niets"
   - `ontdekt`: komt de vervalsing uit, ja of nee, en door wie
   - `schaal`: dorp, rijk of wereld
   - `erft_van`: een of meer ERF-codes uit eerdere fasen
   - `blijvende_verandering`: wat er na deze fase niet meer terug kan
2. Vul de tabel voor alle fasen uit de bestaande FASE-, ERF- en VALS-rijen. Waar dat niet eenduidig kan, schrijf je een voorstel met de status `voorlopig`.
3. Maak drie regels in `regel`, op niveau `fout`:
   - `R-rijm_assen`: elke fase verschilt van de vorige op minstens 3 van deze assen: beslisser, betaler, vervalst, ontdekt, schaal.
   - `R-rijm_erfenis`: elke fase vanaf fase 1 heeft minstens één `erft_van` die bestaat en uit een eerdere fase komt.
   - `R-rijm_spiraal`: `blijvende_verandering` is niet leeg en komt niet terug in een eerdere fase.
4. Binnen één fase gaat het om de bogen a, b en c. Gebruik dezelfde assen in de tabel `boog`. De regel `R-rijm_binnen_fase` stelt: de bogen binnen een fase verschillen onderling op minstens 2 assen.
5. Zorg dat minstens één fase de patronen doorbreekt. Bijvoorbeeld een noodoplossing die werkt zonder vervalsing, of een vervalsing die direct uitkomt. Doe dit als voorstel; Rogier kiest welke.

**Klaar als:** alle vier de rijmregels groen zijn of een open wrijving hebben, en `v_rijm` het overzicht toont.

## Stap 3: het formulier uit de synopsen halen

Herschrijf de verhalen niet. Haal alleen de etiketten eruit, en zet elk veld op één plek:

- Zaadjes ("Zaad: …") gaan naar de tabel `zaadje`, met een verwijzing. Ze staan dan niet meer in de tekst.
- "Herkenbaar: …" wordt de kolom `boog.herkenbaar`.
- "Kernscènes: …" gaat naar de tabel `kernscene`: `boog_code`, `volgorde`, `scene`.
- De labels BEGIN, ESCALATIE en KEERPUNT gaan eruit. De inhoud blijft staan als lopende synopsis.
- Doe dit via nieuwe rijen. De oude rijen gaan naar `vervangen`.

**Klaar als:**
- er 0 levende synopsen zijn met die vier etiketten;
- `zaadje` minstens 26 rijen uit de fasebogen bevat;
- de regel `R-sjabloon_nieuw` groen blijft.

## Stap 4: het schrijfcontract (poka-yoke)

Een schrijvende agent mag niet kunnen beginnen zonder de vorm.

1. Maak de view `v_schrijfpakket`, per `boog_code`. Daarin zitten de relevante Kern-rijen, de boog met vorm, verteller en tempo, de `fase_rijm`-rij, de personages met hun eigen fout, de open zaadjes en de geërfde ERF-rijen.
2. Voeg het commando `vraag.py schrijfpakket <BOOG>` toe.
3. Leg een handleidingregel vast: schrijven gebeurt alleen vanuit `v_schrijfpakket`. Een synopsis is geen schrijfinstructie.

## Stap 5: herkomst

Bereken de herkomst opnieuw na stap 1, waarin veel rijen zonder bron uit Structuur verdwijnen.

- **Doel voor deze ronde:** Structuur minstens 70%.
- Lever de top-50 gaten als lijst voor Rogier, met per rij een voorstel voor de bron. Verzin nooit een bron.

## Stap 6: open inhoudskeuzes (niet zelf beslissen)

Maak een lijst voor Rogier met per punt een aanbeveling:

- **WRIJ-Z30-2:** de Stille Modus zaaien in boek 0. Aanbeveling: Ysa ontwerpt hem in haar latere jaren als boetedoening, en laadt hem in via Hesta's cellen en de deur in de Reckoner. Daarmee sluiten ook WRIJ-Z21-5 en WRIJ-Z22-2.
- **De overige open wrijvingen uit `v_open`,** gesorteerd op draagkracht.

## Stap 7: de verhaalgenerator (honderden verhalen per fase, geen kopieën)

Het doel is dat per fase honderden verhalen kunnen worden gemaakt die allemaal dezelfde motor raken, maar nooit hetzelfde verhaal zijn. Herhaling zit in het mechanisme, verschil zit in de positie.

1. Maak via migratie de tabel `verhaal_as`. Daarin staan de assen met hun toegestane waarden:
   - `positie_in_motor`: beslisser, betaler, vervalser, ontdekker, profiteur, toeschouwer, of liefde tussen twee posities
   - `genre`: intrige, horror, thriller, mysterie, romance, komedie, actie, tragedie, survival
   - `schaal`: huis, dorp, stad, rijk, wereld
   - `volk`: uit de bestaande volken
   - `vorm`: bijvoorbeeld brieven, ballade, aftellen, rechtszaak, dagboek, jij-vorm, of een register als verteller
   - `afloop`: werkt, faalt, komt uit, blijft verborgen, of keert om
   - `hoofdpersoon`: leeftijdsband en geslacht
2. Elke boog, en elk nieuw verhaal, krijgt in `boog` een waarde op elke as.
3. Maak de functie `afstand(a, b)`: het aantal assen waarop twee verhalen verschillen.
4. Maak de regel `R-verhaal_afstand`, op niveau `fout`: een nieuw verhaal moet binnen dezelfde fase op minstens 3 assen verschillen van elk bestaand verhaal.
5. Maak de regel `R-positie_dekking`, op niveau `signaal`: per fase is elke positie in de motor minstens één keer bezet voordat een positie een derde keer wordt gebruikt.
6. Maak de generator `vraag.py bedenk <FASE> <N>`. Die stelt N nieuwe verhaalprofielen voor met *farthest-point sampling*: steeds het profiel dat het verst ligt van alles wat er al is. Daarbij gelden de rijmregel van stap 2 en de harde grenzen. Per profiel geeft de generator ook de ERF-rij die het verhaal raakt, en de rijen uit `v_kern` die het niet mag breken.
7. Uitvoer gaat altijd in de ideeënbank (`voorlopig`). Rogier kiest welke verhalen canon worden.
8. **Test:** genereer 20 profielen voor fase 4 Noodtoestand. Rapporteer de kleinste en de gemiddelde onderlinge afstand, en de dekking per positie.

**Klaar als:** de regels groen zijn, de test met 20 profielen een minimale onderlinge afstand van minstens 3 haalt, en alle 7 posities gedekt zijn.

## Stap 8: optimaliseren op waarde (multi-objectief)

De generator uit stap 7 kiest niet alleen verhalen die verschillen, maar verhalen die het meest opleveren.

1. Maak de tabel `doel`: `code`, `omschrijving`, `gewicht`, `bron_gewicht` (Rogier, aanname of data), `richting` (max of min). Begin met deze vijf doelen:
   - `nieuwheid`: de afstand tot bestaande verhalen, uit stap 7;
   - `verbondenheid`: het aantal open zaadjes dat het verhaal oogst, plus het aantal ERF-rijen dat het raakt, plus de centraliteit in `relatie`;
   - `seriewaarde`: of het verhaal de hoofdlijn raakt (Liora, de Stille Modus, Thalen, de derde weg);
   - `lezersvraag`: begin met een aanname per genre en trope; die wordt later vervangen door data;
   - `kosten`: de geschatte schrijfomvang (richting: min).
2. Harde grenzen zijn filters, nooit scores: `v_kern`, de harde lijnen, de rijmregels en `R-verhaal_afstand`. Een profiel dat een filter niet haalt, valt af, ongeacht zijn score.
3. Kies de collectie greedy op de **marginale winst**: wat voegt dit verhaal toe aan de bestaande collectie? Een verhaal dat lijkt op wat er al is, levert minder op (afnemende meeropbrengst; submodulair; greedy haalt gegarandeerd ≥63% van het optimum).
4. Maak het commando `vraag.py pareto <FASE> <N>`. Het toont het Pareto-front: de profielen die op geen enkel doel te verbeteren zijn zonder een ander doel te verslechteren. Per profiel staat erbij waarom het op het front ligt. Geen verborgen gewichtsom als eindoordeel; Rogier kiest.
5. Maak de tabel `lezersdata`: `boog_code` of hoofdstuk, `bron` (bijvoorbeeld Wattpad), `datum`, `reads`, `afmaakpercentage`, `reacties`. Daarmee wordt `lezersvraag` Bayesiaans bijgewerkt. Maak ook `vraag.py volgende`, een bandit met Thompson sampling: ongeveer 80% kiest wat aantoonbaar werkt, ongeveer 20% verkent wat nog onbekend is.
6. **Test:** draai `pareto` voor fase 6 Markt met 10 profielen. Rapporteer per profiel de vijf scores en de marginale winst.

**Klaar als:** het filter nooit een profiel doorlaat dat een harde grens schendt (test met een expres fout profiel), het Pareto-front klopt (geen profiel op het front wordt door een ander profiel op alle doelen overtroffen), en de gewichten in `doel` staan met hun herkomst.

## Stap 9: gewichten bepalen en sturen op genre

### 9a. Genreprofiel per verhaal
1. Elke boog en elk voorgesteld profiel krijgt een genrevector op 0-5:
   - `romance`
   - `erotiek` (heat)
   - `horror`
   - `suspense`
   - `actie`
   - `intrige`
   - `komedie`
   - `tragiek`

   Gebruik de bestaande bronnen waar die er zijn: de genrescores per hoofdstuk ("Genres R E H S A F" in ROMAN-rijen), `intensiteit`, `afstoting`, `aantrekking`, en de KINK-, VERLEID-, HORROR- en INTR-rijen die het verhaal gebruikt. Wat je schat, krijgt de status `voorlopig`.
2. Maak de tabel `doelprofiel`: `code`, `naam`, de doelvector, en een `minimum` per genre. Voorbeelden: "erotische suspense" (erotiek ≥4, suspense ≥4), "intrige met horror-rand", "slow-burn romance".
3. Maak een nieuw doel in `doel`: `genrematch`. Dat is de afstand tussen de genrevector van het verhaal en het gekozen doelprofiel. Een `minimum` werkt als filter.
4. "Passend in de wereld" is geen apart doel. Het volgt uit `verbondenheid` (zaadjes, ERF-rijen, relaties) plus de filters. Bij erotiek komen daar ook de vaste wereldregels bij: de SEKS-VOLK-rijen van het volk in kwestie, en de rituelen en kinks uit de canon of de ideeënbank, met verwijzing. De harde lijnen gelden altijd: alleen volwassenen, alleen wie echt kan instemmen, en dwang alleen als gelabeld donker thema. Een profiel dat daar niet aan voldoet, valt af, hoe hoog het ook scoort.
5. Maak het commando `vraag.py bedenk <FASE> <N> --profiel <DOELPROFIEL>`. Dat combineert stap 7 (afstand), stap 8 (Pareto) en `genrematch`.

### 9b. Gewichten bepalen (nooit met de hand verzinnen)
1. **Swing-weging:** `vraag.py gewicht swing`. Begin vanuit het slechtste verhaal. Rogier kiest welk doel hij als eerste naar het beste niveau tilt (100 punten), en geeft elk ander doel punten ten opzichte daarvan. Daarna normaliseren.
2. **Paarsgewijs:** `vraag.py gewicht paren`. Het systeem toont 20 paren concrete profielen van het Pareto-front, en Rogier kiest telkens A of B. Fit de gewichten met Bradley-Terry of logistische regressie. Rapporteer de **consistentie**: welke keuzes spreken elkaar tegen? Dat zijn de punten waar hij twijfelt.
3. **Gewichtsets per doel van het moment:** sla ze op als `gewichtset`, met naam, datum en methode. Bijvoorbeeld "lancering serie" of "Wattpad-groei". Startwaarde "lancering serie" (aanname, `voorlopig`): verbondenheid 0,30; seriewaarde 0,25; nieuwheid 0,20; lezersvraag 0,15; kosten 0,10. `genrematch` wordt per doelprofiel toegevoegd.
4. **Gevoeligheidstoets:** bij elke `pareto`- of `bedenk`-uitvoer verschuift elk gewicht ±10%. Per voorstel staat erbij of het **robuust** is (blijft in de top-3) of een **close call** (de top wisselt). Bij een close call beslist Rogier op smaak.

**Klaar als:**
- `bedenk 6 10 --profiel "erotische suspense"` 10 profielen geeft die allemaal aan het minimum voldoen, die allemaal de harde lijnen halen (test met een expres fout profiel), en die elk minstens één bestaande wereldregel of rite noemen met code;
- de gewichtsets met methode en datum zijn opgeslagen;
- de gevoeligheidstoets per voorstel wordt getoond.

## Stap 10: de rijkheid van de wereld (ronde Z36 of later)

Rijkheid = dekking × diepte × verbondenheid. Het is niet het aantal rijen.

1. **Raster.** Maak de tabel `domein` met de levensdomeinen: eten, drinken, muziek, taal en namen, recht, geld en handel, dieren en planten, kinderen en opvoeding (strikt niet-seksueel), rouw, feest, werk, humor, kleding, wonen, ziekte en zorg, reizen, geloof in het dagelijks leven. Maak de view `v_rijkdom` met per cel (volk × fase × domein) drie maten:
   - **dekking**: hoeveel levende rijen er zijn;
   - **diepte**: hoeveel lagen er zijn (officieel, verborgen, verschil per volk, verandering over fasen);
   - **verbondenheid**: hoeveel bogen, personages en relaties naar de cel verwijzen.
2. **Competentievragen.** Schrijf per domein drie tot vijf vragen die een schrijver moet kunnen beantwoorden, bijvoorbeeld "wat eet een Saelmor-gezin op een rustdag?" en "hoe rouwt een Karrûk?". Zet ze in de tabel `competentievraag`. `v_rijkdom` toont welk percentage beantwoord kan worden.
3. **Vraaggestuurd vullen.** Een gat krijgt prioriteit naar het aantal geplande of voorgestelde bogen (uit stap 7 tot en met 9) dat door die cel loopt. Er wordt niet raster-breed gevuld: rijkdom groeit waar verhalen wonen. Maak het commando `vraag.py gaten <FASE>`: de top-20 gaten met de bogen die ze nodig hebben.
4. **Vullen met verbinding.** Elke nieuwe rijkdomsrij verwijst naar minstens één boog, personage of ERF-rij. Anders telt ze als decor en gaat ze naar de ideeënbank. De regel `R-dode_rijkdom` (niveau `signaal`) meldt rijen in Structuur die na twee rondes door niets worden gebruikt.
5. **Terugkerende details.** Maak de tabel `motief_detail`: een klein concreet detail dat in meerdere verhalen terugkomt. Voorbeelden uit boek 0 zijn de tomaten, de kraaien en het oortje. Een detail telt pas als motief bij minstens twee verhalen.
6. **Eerst de dunne plekken die de canon zelf al noemt:** humor, gewone vreugde, en eten en muziek per volk (GENRE-balans-V4). Vul die eerst voor de drie diepe volken van boek 1: Karrûk, Saelmor, Aelthir.

**Klaar als:**
- `v_rijkdom` en `vraag.py gaten` werken;
- voor de drie diepe volken in de fase van boek 1 minstens 80% van de competentievragen beantwoord kan worden;
- elke nieuwe rij een verbinding heeft.

## Stap 11: personagenetwerk en wereldsimulatie (ronde Z38, na Z35 tot en met Z37)

Doel: duizenden verhalen die met elkaar verbonden zijn en die ontstaan uit een simulatie, in plaats van dat elk verhaal los wordt verzonnen. De techniek is agent-based simulatie met Monte Carlo, zoals *Dwarf Fortress*, *Crusader Kings* en de storyteller van *RimWorld*.

### 11a. Personagenetwerk
1. Personages hebben drie lagen:
   - **hoofd**: de tabel `personage`, met eigen fout, zelfbedrog en boog;
   - **bij**: wil, geheim en relaties;
   - **achtergrond**: naam, plek en functie.

   Achtergrondfiguren worden pas gemaakt op het moment dat een verhaal of simulatierun ze nodig heeft, nooit vooraf in bulk.
2. Maak de tabel `verblijf`: `per_code`, `plek_code`, `van_jaar`, `tot_jaar`. Daarmee is elk personage in tijd en ruimte te plaatsen.
3. Maak de tabel `kennis`: `per_code`, `weet_code` (een feit, geheim of gebeurtenis), `sinds_jaar`, `bron`. Dit is wie wat weet en sinds wanneer, en het is de motor van elke intrige.
4. Breid `relatie` uit met de soorten `rivaal_van`, `schuldig_aan`, `eed_aan`, `verraden_door`, `meester_van` en `wil_hetzelfde_als`, elk met `van_jaar` en `tot_jaar`.
5. Maak de graafvragen als commando's, `vraag.py intrige <PATROON> <PLEK> <JAAR>`, voor:
   - **complot**: personages die hetzelfde willen en dezelfde vijand hebben;
   - **chantage**: iemand weet een geheim van een ander, binnen bereikbare reistijd;
   - **rivaliteit**: twee personages die hetzelfde willen, en een derde die het heeft;
   - **erfwrok**: een nazaat van iemand die verraden is, leeft in dezelfde tijd als een nazaat van de verrader.

### 11b. Simulatiemotor
1. **Zaaien:** de startbevolking per fase komt uit de canon: huizen, volken en bestaande personages met hun wil, bezit en kennis.
2. **Regels:** de wereldregels uit de canon worden simulatieregels, met verwijzing naar hun code: de Deelwet, rotatie, 1 op 100, Varenne-krediet, de levensduur per volk (uit een anker), reistijd tussen plekken, en de toegang tot registers. Leg elke regel vast in de tabel `sim_regel`, met bron.
3. **Stappen:** per seizoen handelt elk actief personage vanuit wat het wil. Gebeurtenissen zijn onder andere huwelijk, geboorte, schuld, verraad, een geheim dat uitlekt, ruzie, migratie en dood. De kans op een gebeurtenis volgt uit de situatie (wil, bezit, kennis, relaties). Elke run is reproduceerbaar via een seed.
4. **Harde lijnen in de motor zelf, niet alleen als test:**
   - minderjarigen bestaan alleen als geboorte, erfenis en opvoeding (niet-seksueel);
   - seksuele of romantische gebeurtenissen alleen tussen volwassenen die kunnen instemmen;
   - Kern wordt nooit overschreven.

   Een gebeurtenistype dat een harde lijn kan raken, bestaat niet in de motor.
5. **Monte Carlo:** draai per fase N runs (start met 1.000). Gooi elke run die een invariant breekt meteen weg, en tel hoeveel dat er zijn. Invarianten: niemand handelt na zijn dood, niemand is op twee plekken tegelijk, niemand weet iets vóór de bron bestaat, en ankers kloppen.
6. **Storyteller:** score elke geldige run op het aantal intriges en ommekeren, het aantal geraakte zaadjes en ERF-rijen, de rijmregel (stap 2), het doelprofiel (stap 9) en de gewichtset (stap 9b). Kies de top met de Pareto-logica van stap 8.
7. **Vertalen:** de gekozen run wordt rijen met de status `voorlopig` (gebeurtenis, verblijf, kennis, relatie), met de seed en de run-id als `bron`. Met de graafvragen uit 11a worden er intrigevoorstellen van gemaakt, die in de ideeënbank komen. Rogier kiest wat canon wordt.

### 11c. Modules op dezelfde motor
Gebruik voor elke module hetzelfde patroon: actoren, regels met bron, kansen, runs en een storyteller. Begin met **technologie**. Elke module krijgt een eigen tabel met gebeurtenistypen en een eigen invariantentest.
- **Technologie:** een uitvinding ontstaat ergens, verspreidt zich langs routes, en heeft een prijs in lichamen (genre-wet 2). Ze kan vergeten worden; de kennis van de Makers is het voorbeeld.
- **Economie:** prijzen, schuld en schaarste. De crash van de Zaadbeurs in 762 moet kunnen ontstaan uit het model, als valideringstest.
- **Religie en macht:** verspreiding van geloof, ketterij, en wie de registers beheert.
- **Ziekte:** een epidemiemodel. De Pest van 340, een derde van de mannen, is de valideringstest.
- **Oorlog en volken:** grenzen, allianties en migratie.

### 11d. Controle door de architect
1. **Automatisch:** de invarianten per run, en `toets.py` na het vertalen.
2. **Steekproef (acceptance sampling):** neem per ronde een willekeurige steekproef van 50 nieuwe rijen voor de onafhankelijke architect. Die beoordeelt per rij of de rij past in de wereld, of het geen sjabloon is, en of de verbinding klopt. Bereken het foutpercentage met een 95%-interval. Ligt de bovengrens boven 2%, dan wordt de ronde afgekeurd.
3. **Koude lezer:** tien vragen over de gesimuleerde fase, alleen uit de views beantwoord.
4. **Valideren tegen de canon:** de bekende gebeurtenissen (de Pest van 340, de crash van 762, de stemming van 7 tegen 5) moeten in een redelijk deel van de runs uit het model zelf kunnen ontstaan. Lukt dat niet, dan kloppen de regels niet.

**Klaar als:**
- één fase volledig gesimuleerd is (begin met fase 4 Noodtoestand, die de kleinste bevolking heeft);
- er 1.000 runs zijn gedraaid, met rapportage van het aantal weggegooide runs en de reden;
- de top-5 runs als voorstel klaarliggen;
- er minstens 10 intrigevoorstellen uit de graaf zijn gehaald;
- de steekproef en de koude lezer geslaagd zijn.

## Op te leveren

1. `canon_na_Z35.db`
2. Alle scripts: `toets.py`, `afgeleid.py`, `afgeleid_motor.py`, `vraag.py`, `export.py`, `importeer.py`, `meet.py`, en de map `migraties/`
3. `scorekaart_Z35.md`, vóór en na:
   - de 8 metingen van de canon-motor;
   - het sjabloonaandeel;
   - de rijmregels;
   - de herkomst;
   - het resultaat van de roundtrip, van export naar import, met de vergelijking rij voor rij;
   - het resultaat van terugdraaien naar Z34 en weer vooruit.
4. De lijst met keuzes voor Rogier (stap 5 en 6)

Daarna voert de architect een onafhankelijke toets uit, inclusief de koude lezer.
