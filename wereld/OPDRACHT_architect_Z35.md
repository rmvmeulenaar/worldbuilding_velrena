# Opdracht ronde Z35 (en vervolg): rijm en opschoning
Van: architect (onafhankelijke toetser van Z34). Voor: de bouwer van canon.db. Basis: canon_na_Z34.db (= /workspace/wereld/canon.db na Z34). Meetlat: skill canon-motor.

## Waar we staan
Z34 is goed: constraints werken, handwerk wordt niet overschreven, nul dode links, regeltabel en ankers, mal per boog gebroken (boog.vorm/verteller/tempo), elk hoofdpersonage heeft een eigen fout. Niets terugdraaien.
Vier problemen:
1. Gegenereerde personagerijen staan in Structuur: ruim 1.200 TOESTAND-, Geboren-, Overleden- en "In # actief"-rijen. 557 hebben een aanname (280x "levensduur 70"), 330 lege velden ("Wil: -", "regio onbekend"). Velden in lopende tekst en gokken van een script; een agent leest ze als feit.
2. De motor heeft geen rijmregel. Herhaling is het ontwerp (probleem, noodoplossing, prijs, vervalsing per fase), maar nergens staat wat elke fase verschuift en erft. Zonder regel wordt herhaling een kopie i.p.v. een rijm.
3. De synopsen dragen nog het invulformulier: in de 28 fasebogen steeds BEGIN/ESCALATIE/KEERPUNT (7/7), "Herkenbaar:" (21), "Kernscènes:" (18), "Zaad:" (26). Zaadjes staan dubbel: in tekst én in tabel zaadje.
4. Herkomst bij Structuur is 36%, norm 90%.

## Harde randvoorwaarden
- Geen Kern-inhoud wijzigen. Inhoudelijke keuzes worden voorstellen (voorlopig); Rogier stelt vast.
- Nooit verwijderen. Oude rijen naar 'voorlopig, vervangen' met vervangen_door.
- Elke structuurwijziging via een genummerde migratie, elke inhoudelijke wijziging in tabel wijziging.
- Je bent de enige bouwer.
- Na elke stap toets.py draaien; moet groen zijn.

## Stap 1: personagetoestand naar kolommen (principe 5)
1. Migratie: tabel personage_toestand: per_code, jaar, leeftijd, rol, regio, wil, geheim, verandert, aanname (0/1), aanname_reden, bron.
2. Parse alle TOESTAND-, Geboren-, Overleden- en "In # actief"-rijen naar deze tabel. "-" of "onbekend" wordt NULL (niet opgeslagen als waarde).
3. Sla aannames niet op als feit. Sterfjaren op basis van levensduur worden berekend in view v_personage_tijdlijn, met levensduur per volk uit één ankertabel; neem de langlevende volken Aelthir en Orrim mee (WRIJ-Z14-2). De view toont aanname = 1 zichtbaar.
4. Oude rijen naar 'voorlopig, vervangen' met vervangen_door = de PER-code van het personage.
Klaar als: v_actief bevat 0 rijen met "Wil: -", "Geheim: -", "regio onbekend" of "aanname: levensduur"; het aandeel canonrijen buiten de ideeënbank dat in een sjabloonfamilie zit daalt van 61% naar <35%; alle bestaande views en ankers werken nog.

## Stap 2: de rijmregel voor de motor
De 8 fasen (0 Voortijd t/m 7 Barsten) plus 801 vormen een spiraal, geen cirkel. Leg dat vast.
1. Migratie: tabel fase_rijm, één rij per fase: fase; mechanisme (welk deel van probleem/noodoplossing/prijs/vervalsing hier herhaalt); beslisser; betaler; vervalst (wat, of "niets"); ontdekt (komt de vervalsing uit, ja/nee, en door wie); schaal (dorp/rijk/wereld); erft_van (een of meer ERF-codes uit eerdere fasen); blijvende_verandering (wat er na deze fase niet meer terug kan).
2. Vul voor alle fasen uit bestaande FASE-, ERF- en VALS-rijen. Waar niet eenduidig: voorstel met status voorlopig.
3. Regels in tabel regel, niveau fout: R-rijm_assen (elke fase verschilt van de vorige op minstens 3 van de assen beslisser, betaler, vervalst, ontdekt, schaal); R-rijm_erfenis (elke fase vanaf 1 heeft minstens één erft_van die bestaat en uit een eerdere fase komt); R-rijm_spiraal (blijvende_verandering niet leeg en komt niet terug in een eerdere fase).
4. Binnen één fase: bogen a, b, c. Gebruik dezelfde assen in tabel boog. Regel R-rijm_binnen_fase: bogen binnen een fase verschillen onderling op minstens 2 assen.
5. Zorg dat minstens één fase de patronen doorbreekt (noodoplossing werkt zonder vervalsing, of vervalsing komt direct uit). Als voorstel; Rogier kiest.
Klaar als: alle vier rijmregels groen zijn of een open wrijving hebben, en v_rijm het overzicht toont.

## Stap 3: het formulier uit de synopsen halen
Herschrijf de verhalen niet; haal alleen de etiketten eruit en zet elk veld op één plek:
- Zaadjes ("Zaad: ...") naar tabel zaadje, met verwijzing; niet meer in de tekst.
- "Herkenbaar: ..." wordt kolom boog.herkenbaar.
- "Kernscènes: ..." naar tabel kernscene (boog_code, volgorde, scene).
- Labels BEGIN, ESCALATIE, KEERPUNT eruit; inhoud blijft als lopende synopsis.
- Via nieuwe rijen; oude rijen naar vervangen.
Klaar als: 0 levende synopsen met die vier etiketten; zaadje minstens 26 rijen uit de fasebogen bevat; R-sjabloon_nieuw groen blijft.

## Stap 4: het schrijfcontract (poka-yoke)
1. View v_schrijfpakket per boog_code: relevante Kern-rijen, de boog met vorm/verteller/tempo, de fase_rijm-rij, personages met hun eigen fout, open zaadjes, geërfde ERF-rijen.
2. Commando vraag.py schrijfpakket <BOOG>.
3. Handleidingregel: schrijven gebeurt alleen vanuit v_schrijfpakket; een synopsis is geen schrijfinstructie.

## Stap 5: herkomst
Bereken herkomst opnieuw na stap 1. Doel deze ronde: Structuur minstens 70%. Lever de top-50 gaten als lijst voor Rogier, per rij een voorstel voor de bron. Verzin nooit een bron.

## Stap 6: open inhoudskeuzes (niet zelf beslissen)
Lijst voor Rogier met per punt een aanbeveling:
- WRIJ-Z30-2: Stille Modus zaaien in boek 0. Aanbeveling: Ysa ontwerpt hem in haar latere jaren als boetedoening en laadt hem in via Hesta's cellen en de deur in de Reckoner; sluit ook WRIJ-Z21-5 en WRIJ-Z22-2.
- De overige open wrijvingen uit v_open, gesorteerd op draagkracht.

## Stap 7 (Z36): de verhaalgenerator (honderden verhalen per fase, geen kopieën)
Herhaling zit in het mechanisme, verschil in de positie.
1. Migratie: tabel verhaal_as met assen en toegestane waarden: positie_in_motor (beslisser, betaler, vervalser, ontdekker, profiteur, toeschouwer, of liefde tussen twee posities); genre (intrige, horror, thriller, mysterie, romance, komedie, actie, tragedie, survival); schaal (huis, dorp, stad, rijk, wereld); volk (uit bestaande volken); vorm (brieven, ballade, aftellen, rechtszaak, dagboek, jij-vorm, register als verteller, ...); afloop (werkt, faalt, komt uit, blijft verborgen, keert om); hoofdpersoon (leeftijdsband en geslacht).
2. Elke boog en elk nieuw verhaal krijgt in boek een waarde op elke as.
3. Functie afstand(a,b): aantal assen waarop twee verhalen verschillen.
4. Regel R-verhaal_afstand (fout): nieuw verhaal verschilt binnen dezelfde fase op minstens 3 assen van elk bestaand verhaal.
5. Regel R-positie_dekking (signaal): per fase is elke positie minstens één keer bezet voordat een positie een derde keer wordt gebruikt.
6. Generator vraag.py bedenk <FASE> <N>: N nieuwe verhaalprofielen via farthest-point sampling (steeds het profiel dat het verst ligt van alles wat er is). Rijmregel van stap 2 en harde grenzen gelden. Per profiel ook de ERF-rij die het raakt en de v_kern-rijen die het niet mag breken.
7. Uitvoer altijd in de ideeënbank (voorlopig); Rogier kiest welke canon worden.
8. Test: 20 profielen voor fase 4 Noodtoestand; rapporteer kleinste en gemiddelde onderlinge afstand en dekking per positie.
Klaar als: regels groen, minimale onderlinge afstand ≥3, alle 7 posities gedekt.

## Stap 8 (Z36): optimaliseren op waarde (multi-objectief)
1. Tabel doel: code, omschrijving, gewicht, bron_gewicht (Rogier/aanname/data), richting (max/min). Vijf doelen: nieuwheid (afstand uit stap 7); verbondenheid (aantal open zaadjes dat het verhaal oogst + aantal ERF-rijen dat het raakt + centraliteit in relatie); seriewaarde (raakt het de hoofdlijn: Liora, Stille Modus, Thalen, derde weg); lezersvraag (aanname per genre/trope, later data); kosten (geschatte schrijfomvang, min).
2. Harde grenzen zijn filters, nooit scores: v_kern, harde lijnen, rijmregels, R-verhaal_afstand. Een profiel dat een filter niet haalt valt af.
3. Kies de collectie greedy op marginale winst (submodulair; afnemende meeropbrengst).
4. Commando vraag.py pareto <FASE> <N>: toont het Pareto-front, per profiel waarom het op het front ligt. Geen verborgen gewichtsom als eindoordeel; Rogier kiest.
5. Tabel lezersdata: boog_code of hoofdstuk, bron (bv. Wattpad), datum, reads, afmaakpercentage, reacties; lezersvraag Bayesiaans bijwerken. vraag.py volgende: bandit met Thompson sampling (~80% wat aantoonbaar werkt, ~20% verkennen).
6. Test: pareto voor fase 6 Markt met 10 profielen; rapporteer per profiel de vijf scores en marginale winst.
Klaar als: filter laat nooit een profiel door dat een harde grens schendt (test met expres fout profiel); front klopt (geen frontprofiel op alle doelen overtroffen); gewichten in doel met herkomst.

## Stap 9 (Z36): gewichten bepalen en sturen op genre
9a. Genreprofiel per verhaal:
1. Elke boog en elk voorgesteld profiel krijgt genrevector 0-5: romance, erotiek (heat), horror, suspense, actie, intrige, komedie, tragiek. Gebruik bestaande bronnen (genrescores per hoofdstuk "Genres R E H S A F" in ROMAN-rijen, intensiteit, afstoting, aantrekking, KINK-/VERLEID-/HORROR-/INTR-rijen). Wat je schat: voorlopig.
2. Tabel doelprofiel: code, naam, doelvector, minimum per genre (bv. "erotische suspense" erotiek ≥4 en suspense ≥4; "intrige met horror-rand"; "slow-burn romance").
3. Nieuw doel genrematch (afstand tot gekozen doelprofiel); minimum werkt als filter.
4. "Passend in de wereld" volgt uit verbondenheid + filters; bij erotiek ook de vaste wereldregels (SEKS-VOLK-rijen van het volk, rituelen en kinks uit canon of ideeënbank, met verwijzing). Harde lijnen altijd: alleen volwassenen, alleen wie echt kan instemmen, dwang alleen als gelabeld donker thema. Profiel dat daar niet aan voldoet valt af.
5. vraag.py bedenk <FASE> <N> --profiel <DOELPROFIEL> combineert afstand, Pareto en genrematch.
9b. Gewichten bepalen (nooit met de hand verzinnen):
1. vraag.py gewicht swing: swing-weging vanuit het slechtste verhaal; Rogier tilt één doel naar 100 punten, geeft de rest punten t.o.v. dat; normaliseren.
2. vraag.py gewicht paren: 20 paren profielen van het Pareto-front, Rogier kiest A of B; fit Bradley-Terry of logistische regressie; rapporteer consistentie (tegenstrijdige keuzes = twijfel).
3. Gewichtsets per doel van het moment als tabel gewichtset (naam, datum, methode). Startwaarde "lancering serie" (aanname, voorlopig): verbondenheid 0,30; seriewaarde 0,25; nieuwheid 0,20; lezersvraag 0,15; kosten 0,10; genrematch per doelprofiel erbij.
4. Gevoeligheidstoets: bij elke pareto-/bedenk-uitvoer elk gewicht ±10%; per voorstel robuust (blijft top-3) of close call.
Klaar als: bedenk 6 10 --profiel "erotische suspense" geeft 10 profielen die aan minimum voldoen, harde lijnen halen (test met expres fout profiel), en elk minstens één bestaande wereldregel of rite met code noemen; gewichtsets met methode en datum opgeslagen; gevoeligheidstoets per voorstel getoond.

## Stap 10 (Z37): de rijkheid van de wereld
Rijkheid = dekking × diepte × verbondenheid, niet aantal rijen.
1. Tabel domein: eten, drinken, muziek, taal en namen, recht, geld en handel, dieren en planten, kinderen en opvoeding (strikt niet-seksueel), rouw, feest, werk, humor, kleding, wonen, ziekte en zorg, reizen, geloof in het dagelijks leven. View v_rijkdom per cel (volk × fase × domein): dekking (levende rijen), diepte (lagen: officieel, verborgen, verschil per volk, verandering over fasen), verbondenheid (bogen, personages en relaties die naar de cel verwijzen).
2. Competentievragen: per domein 3-5 vragen die een schrijver moet kunnen beantwoorden ("wat eet een Saelmor-gezin op een rustdag?", "hoe rouwt een Karrûk?") in tabel competentievraag; v_rijkdom toont percentage beantwoord.
3. Vraaggestuurd vullen: gat krijgt prioriteit naar aantal geplande/voorgestelde bogen (stap 7-9) dat door die cel loopt; niet raster-breed. vraag.py gaten <FASE>: top-20 gaten met de bogen die ze nodig hebben.
4. Elke nieuwe rijkdomsrij verwijst naar minstens één boog, personage of ERF-rij, anders ideeënbank. Regel R-dode_rijkdom (signaal): rijen in Structuur die na twee rondes door niets worden gebruikt.
5. Tabel motief_detail: klein concreet detail dat in meerdere verhalen terugkomt (tomaten, kraaien, oortje uit boek 0); pas motief bij minstens twee verhalen.
6. Eerst de dunne plekken die de canon noemt: humor, gewone vreugde, eten en muziek per volk (GENRE-balans-V4); eerst voor de drie diepe volken van boek 1: Karrûk, Saelmor, Aelthir.
Klaar als: v_rijkdom en vraag.py gaten werken; voor de drie diepe volken in de fase van boek 1 ≥80% van de competentievragen beantwoord kan worden; elke nieuwe rij een verbinding heeft.

## Op te leveren
1. canon_na_Z35.db
2. Alle scripts (toets.py, afgeleid.py, afgeleid_motor.py, vraag.py, export.py, importeer.py, meet.py, map migraties/)
3. scorekaart_Z35.md vóór en na: de 8 metingen van de canon-motor; sjabloonaandeel; rijmregels; herkomst; roundtrip (export naar import, rij voor rij); terugdraaien naar Z34 en weer vooruit.
4. Lijst met keuzes voor Rogier (stap 5 en 6).
Daarna voert de architect een onafhankelijke toets uit, inclusief koude lezer.
