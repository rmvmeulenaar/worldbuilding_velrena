# Opdracht ronde Z36: afmaken, vastleggen, en de verhalenmachine aanzetten

Van: architect (onafhankelijke toetser)
Voor: de bouwer van canon.db
Basis: canon_na_Z35.db. Meetlat: de skill `canon-motor`. Details van stap 7 tot en met 9: zie `opdracht_Z35.md`.

## Oordeel over Z35

Technisch goed: Kern ongewijzigd, personagetoestand in kolommen, synopsen schoon, `fase_rijm` sterk, roundtrip en terugdraaien werken.

Maar drie doelen zijn niet gehaald, en dat is het punt van deze ronde:
- het sjabloonaandeel staat op 47,1% (doel was onder 35%);
- de herkomst van Structuur staat op 54,4% (doel was minstens 70%);
- 22 punten op de keuzelijst zeggen "niet inhoudelijk gelezen".

Markeren, uitstellen en "niet gelezen" tellen niet als werk. Deze ronde haalt alles in.

## Prioriteit: het werk is wereldbouw

De database is gereedschap voor wereldbouw en verhalen. Elke stap wordt gewogen op één vraag: levert dit betere of meer bruikbare verhalen op?

- **Blokkerend (de ronde is pas klaar als dit af is):** stap 0 (besluiten), stap 2 (de verhalenmachine) en stap 1c (de keuzelijst echt lezen, inclusief de dubbele namen).
- **Alleen voor zover de machine het nodig heeft:** stap 1a. Zet de personageprofielen om naar kolommen als de generator of het personagenetwerk ze gebruikt. Het percentage onder 35% is geen doel op zich deze ronde.
- **Doorlopend, niet blokkerend:** stap 1b (herkomst). Meld de stand in de scorekaart. Verder geen werk, behalve de top-50-lijst voor Rogier.

Volgorde: stap 0, stap 1c, stap 1a (alleen het benodigde deel), stap 2.

## Werkregels (gelden voor elke stap)

1. **Markeren is geen oplossen.** Een rij die alleen een vlag, label of familie krijgt zonder dat het probleem weg is, telt als niet gedaan.
2. **Geen "niet gelezen".** Elk punt waar je een aanbeveling over geeft, lees je eerst. Het bewijs: per punt citeer je één zin uit de rijen die je las (met code), en geef je een aanbeveling met ja, nee of een alternatief, plus een reden. "Nog geen aanbeveling" is niet toegestaan.
3. **Elk klaar-als bewijs je.** Per criterium lever je de SQL-query of het commando, de uitkomst voor en na, en of het gehaald is. Een criterium zonder query telt als niet gehaald.
4. **Niet gehaald? Dan lever je geen eindrapport, maar werk je door.** Lukt het echt niet, lever dan per criterium de concrete blokkade met bewijs (welke rijen, waarom), en het werk dat je wél deed.
5. **Geen nieuwe tabel zonder gebruik.** Elke nieuwe tabel of view wordt in dezelfde ronde door een regel, een view of een commando gebruikt.
6. **Het blijft verboden:** Kern-inhoud wijzigen zonder BESLUIT, rijen verwijderen, en de tekst van de roman (`roman_ysa_VOLLEDIG.md`) aanraken. Wijzigingen aan de roman zijn van Rogier.
7. **Steekproef door de architect.** Na de ronde trek ik willekeurig 50 gewijzigde of nieuwe rijen. Ligt het foutpercentage (sjabloon, onjuist, onverbonden of verzonnen bron) met 95%-bovengrens boven 2%, dan gaat de ronde terug.

## Stap 0: besluiten van Rogier vastleggen

Leg deze besluiten vast als BESLUIT-Z36-*-rijen. Rogier bevestigt ze bij overhandiging van deze opdracht. Wat hij doorstreept, vervalt.

1. **De Stille Modus:** motief 1 + 3 + 6, volgens `stille_modus_Z36.md`, deel 1. Ysa ontwerpt hem in jaar 28 als veiligheidsmodus tegen de Vonk. Het is een X-gebonden filter (alleen zonen die de lading kunnen dragen, ongeveer 1 op 100). Hij gaat alleen uit met de ja van de dragers, via Thalens sleutel, en die is gebroken. Hij wordt geladen via Hesta's cellen en slaapt tot een raad hem bevestigt (jaar 0).
   - Vervang ORIGIN-10 door een nieuwe Kern-rij met het motief.
   - Sluit WRIJ-Z30-2, WRIJ-Z21-5 en WRIJ-Z22-2.
   - Leg de passage voor hoofdstuk 32 (deel 2) vast als `zaadje` met de status "wacht op roman (Rogier)". De roman verander je niet.
   - Leg de mogelijke botsing met GES-herkomst-gave (de gave "via de vader") vast als wrijving, met een voorstel.
2. **Kern-voorstellen Z35:** de erfenis van fase 0 (ERF-voortijd): ja. De hernummering van FASE-OVERZICHT: ja. De derde weg: ja, met deze formulering: "het Zegel kan niet meer ja zeggen namens een lichaam". Mensen kunnen het nog proberen, maar zonder dekking van het Zegel.
3. **Patroonbreuk:** A (de Markt) en B (Iresse wordt gehoord): ja. C: nee.
4. **De hoofdverhalen 1 tot en met 7 (Z35-voorstellen):** alle zeven ja.
5. **Teo en Liora als volgorde (WRIJ-Z34-1):** ja.

**Klaar als:** elke besluitrij bestaat, de vervangen rijen `vervangen_door` hebben, `toets.py` exit 0 geeft, en `v_kern` de nieuwe ORIGIN-10-opvolger toont.

## Stap 1: wat in Z35 niet af kwam

### 1a. Sjabloonaandeel onder 35%
- Zet de grote personagefamilies om naar kolommen, net als `personage_toestand`:
  - `L:Naam|Volk|Regio|Huis|Rol|Fase|Wil|Durft` (258),
  - `L:Kern|Naam|Volk|…` (81),
  - `L:Volk|Fase|Rol|Verandert|…` (63),
  - en "Archetype, geen vaste persoon" (80).
- Doel: de tabel `personage_profiel`, of een uitbreiding van `personage`. Lege velden worden NULL. Oude rijen gaan naar `vervangen` met `vervangen_door`.
- Overige families met canon-gewicht krijgen per familie een besluit: omzetten naar kolommen, naar de ideeënbank, of herschrijven (alleen als het werkelijk vertelling is). Lever per familie het besluit met reden.

**Klaar als:** het sjabloonaandeel buiten de ideeënbank onder 35% ligt (query bijgeleverd), en geen enkele familie met canon-gewicht zonder besluit is.

### 1b. Herkomst van Structuur minstens 70%, streng
- Alleen echte bronnen tellen: een besluit, de roman, de auteur, of een andere canonrij als bron met code. Het opdrachtspoor telt niet.
- Werkwijze: lees per rij zonder bron de verwijzingen (`verwijst_naar`, `relatie`) en de ronde-notities in `historie`. Is er een eenduidige bron, dan vul je die in. Is er geen bron, dan zijn er twee keuzes: de rij gaat naar Kleur (de ideeënbank), omdat het een voorstel zonder besluit is, of de rij komt op de lijst voor Rogier. Verzin nooit een bron.

**Klaar als:** de herkomst van Structuur volgens de strenge telling minstens 70% is, en de lijst met top-50 gaten voor Rogier per rij een voorstel heeft.

### 1c. Nul "niet gelezen" op de keuzelijst
- Alle 22 punten met "Nog geen aanbeveling" krijgen werkregel 2: een citaat met code, en een aanbeveling met reden.
- Dubbele namen (Vessa, Ardemar, Iska/Iskar, Hesk/Heske, Selvara) krijgen per paar een besluitvoorstel: hernoemen (met nieuwe naam), samenvoegen (met bewijs dat het dezelfde persoon is), of erfnaam.

**Klaar als:** `keuzelijst_Z36.md` nul keer "nog geen aanbeveling" bevat, en elk punt een citaat heeft.

## Stap 2: de verhalenmachine (stap 7, 8 en 9 uit opdracht_Z35.md, volledig)

Voer stap 7 (verhaalassen, afstand, farthest-point generator), stap 8 (doelen, filters, greedy op marginale winst, Pareto, lezersdata) en stap 9 (genreprofiel, doelprofielen, swing en paren, gewichtsets, gevoeligheid) volledig uit.

Extra voor Z36:
1. **De ideeënbank door de machine.** Haal alle verhaaleenheden uit de ideeënbank (skeletten, INTR, ROM, THRL, ROMANCE, HORROR, COMEDY, ACTIE, HELD, OORLOG, SAW, VERLEID, HAAK) door de generator:
   - geef elk een profiel op de assen;
   - verwerp wat binnen afstand 3 van een bestaand verhaal valt;
   - verwerp wat geen ERF-rij of zaadje raakt;
   - wat overblijft, krijgt een plek in een fase.

   Rapporteer: hoeveel er binnenkwamen, hoeveel afvielen op afstand, hoeveel op verbinding, en hoeveel ent-klaar zijn. Rapporteer dat per fase en per positie in de motor.
2. **Lege posities vullen.** Per fase: welke van de 7 posities in de motor (beslisser, betaler, vervalser, ontdekker, profiteur, toeschouwer, liefde tussen posities) nog geen verhaal hebben. Genereer voor elke lege positie 3 profielen met `bedenk`, en zet ze in de ideeënbank.
3. **Demonstratie.** Draai `vraag.py bedenk 6 10 --profiel "erotische suspense"` en `vraag.py pareto 4 10`, en lever de volledige uitvoer mee.

4. **De afdruk in 801 (convergentie zonder plan).** De verhalen komen niet samen via het plot, maar via wat ze nalaten.
   - Elk verhaal (boog, nieuw profiel, ent-klare eenheid) krijgt het veld `afdruk_801`. Dat zegt wat van dit verhaal in 801 nog bestaat: een voorwerp, een bloedlijn, een leugen in de annalen, een lied, naam of ritueel, een document, een plek of ruïne, of een stem (zoals een kraai of de Wortel).
   - Daarbij komt het veld `afdruk_code`: de code van de 801-rij, het zaadje of de ERF-rij waarin die afdruk landt. Bestaat die rij nog niet, dan maak je hem in de ideeënbank met de status `voorlopig`.
   - Maak de regel `R-afdruk_801`, op niveau `fout` voor nieuwe verhalen en `signaal` voor bestaande. Een verhaal zonder afdruk, of met een afdruk die niet bestaat, faalt.
   - Maak de view `v_801_sporen`: alles wat in 801 nog uit eerdere fasen bestaat, per plek, met het verhaal van herkomst. Dit is de wereld waar Liora doorheen loopt.
   - **Vrijheid blijft maximaal.** Verplicht zijn alleen Kern, rijm en afdruk. Genre, vorm, personages en afloop zijn vrij.

**Klaar als:** alle klaar-als-criteria van stap 7, 8 en 9 in `opdracht_Z35.md` gehaald zijn, elke bestaande boog een `afdruk_801` heeft, `v_801_sporen` werkt, het rapport over de ideeënbank er is, en elke fase alle 7 posities gedekt heeft (in canon of ideeënbank).

## Op te leveren

1. `canon_na_Z36.db`
2. Alle scripts, en de map `migraties/` (met nieuwe genummerde migraties)
3. `scorekaart_Z36.md`, met:
   - per klaar-als-criterium: de query of het commando, de waarde voor en na, en of het gehaald is;
   - de 8 metingen van de canon-motor, voor en na;
   - het rapport van de ideeënbank (instroom, uitval, ent-klaar, per fase en positie);
   - de demo-uitvoer van stap 2.3.
4. `keuzelijst_Z36.md`: alleen wat Rogier nog moet beslissen, met citaat en aanbeveling per punt.
5. `wijzigingen_Z36.md`: per tabel het aantal toegevoegde, vervangen en gewijzigde rijen, plus 10 willekeurige voorbeelden met oud en nieuw.

Daarna voert de architect de steekproef van 50 rijen uit, en de koude lezer.
