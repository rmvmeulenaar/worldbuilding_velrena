# Hoe we hier kwamen

Verslag van de samenwerking tussen Rogier (canonhouder) en de architect, tot en met 1 november 2026. Het laat per periode zien wat er gebeurde, welke beslissingen vielen en waarom, en welke correcties van Rogier de koers bepaalden.

Waarom staat het hier? Zodat elke volgende sessie, mens of LLM, niet opnieuw dezelfde omwegen maakt.

Het ruwe gesprek staat **niet** in de repo, omdat het persoonlijke gegevens bevat die niets met Velmara te maken hebben. Dit is de samenvatting met alles wat inhoudelijk telt.

---

## 1. De roman en de wereld (boek 0)

- Rogier liet *The Body Is the Price* (boek 0, pseudoniem Iris Calloway) lezen. De roman gaat over Ysa Maren, de landing van het zaaischip, de stemming van de Makers en het Zegel.
- Oordeel van de architect: sterk wereldontwerp, met een eigen motor ("de prijs van een lichaam"). Er werd een rekenfout gevonden en verbeterd: 800 tegenover 2.000 jaar (de canon rekent in Zegeljaren).
- Wattpad-voorbereiding:
  - genre, subgenres, tags en leeftijdsgroep;
  - een prompt voor de cover;
  - publicatieritme: een reeks hoofdstukken direct, daarna een vast ritme;
  - een HTML-export van de hoofdstukken (`wattpad_hoofdstukken.html`). Die staat **niet** in deze repo, omdat de romantekst van Rogier is. Zie CLAUDE.md.

## 2. De canon als database (Z27–Z34)

- De wereld staat in een SQLite-database (canon.db), gebouwd in rondes door "de bouwer", een andere LLM. De architect toetst onafhankelijk.
- Vroege kritiek van de architect:
  - **Sjablonen:** veel rijen waren invulzinnen.
  - **Herkomst:** veel bronnen waren eigenlijk context.
  - **Dunne personages.**
  - **Verhaallijnen herhaalden hetzelfde patroon** in plaats van te rijmen.
- Rogier: "alles vastleggen geeft geen flexibiliteit". De oplossing werd **draagkracht**:
  - Kern: alleen via een besluit;
  - Structuur: mag schuiven met een wrijving;
  - Kleur: vrij.

  Daarnaast een ideeënbank.
- Architectuurprincipes die erin kwamen: één bron van waarheid, normalisatie, het MVVM-achtig scheiden van data en weergave, toetsen als invarianten, en een graafmodel.
- **De methode werd een skill: `canon-motor`**, de algemene manier om een kennisbasis te bouwen, te toetsen en te laten groeien. Die staat nu ook in `architectuur/methode/canon-motor/`. Rogier zag dat het principe overal toepasbaar is: software, films, boekhoudprogramma's, recht. "Het is als algebra: vanuit elke kant los je het op, de formule blijft dezelfde."

## 3. De verhalenmachine (Z35–Z38)

- Opdracht Z35 en Z36 (`architect/`):
  - verhaalassen;
  - een generator op "verste punt";
  - doelprofielen en gewichten (paarsgewijs, swing);
  - Pareto-selectie en greedy op marginale winst;
  - **afdruk in 801**: elk verhaal laat iets na in het heden, zodat verhalen samenkomen via wat ze nalaten, niet via het plot;
  - **fase_rijm**: per fase dezelfde misdaad in een andere vorm.
- **De Stille Modus** (Z36) als besluit, motief 1+3+6: Ysa's veiligheidsfilter op het X-chromosoom (1 op 100), en de uitknop via Thalens gebroken sleutel. Er kwam een voorstel voor een passage in hoofdstuk 32. De roman zelf bleef onaangeroerd.
- Besluiten na Z36 en Z37:
  - herkomst in lagen: hard, bijbel, context, onbekend;
  - premisses zonder sjabloon;
  - beroepen;
  - gaven;
  - een feeënlaag;
  - "een feeënafspraak gaat nooit over seks".

## 4. Simulatie (Z39–Z40)

- Rogier: "wat is de gelijkenis met Foundation en psychohistorie?" Antwoord: het rekenen met de massa.
- Een agent-based simulatie van fase 4 (de Noodtoestand). Daarna Monte Carlo, techniek en beroepen.
- De bouwer had geen credits meer, dus de architect maakte Z40 af:
  - **het schriftverbod als rem**: het rooster komt pas als genoeg vrouwen kunnen schrijven;
  - **het register verspreidt zich per regio**;
  - **de fase-overgang**;
  - **een SEIR-model van de Pest van 340**.

  Rogier corrigeerde exponentiële groei: het werd logistisch.
- Lessen:
  - een simulatie wordt nooit vanzelf canon (BESLUIT-Z40-2, met regel 7 in afgeleid.py);
  - de steekproef bestaat voortaan uit 183 rijen (Clopper-Pearson, bovengrens < 2%).

## 5. Rogiers correctie: het doel is verhalen, niet een model dat klopt

- De architect dreef af naar het valideren van het model. Rogier: "wat probeer je nu te maken? Dat het model klopt of dat je alle verhaallijnen kunt overzien?"
- Eerste reactie: een selector met filters. Rogier: "nee, niet filteren, alle verhaallijnen moeten in de database staan, kloppen, en via knopen te enten zijn."
- **De Knopenkaart**: elke verhaallijn als knoop, verbonden via gedeelde personages, plekken, gebeurtenissen en zaadjes. Met controle (klopt het?) en entpunten (rijke knopen met weinig verhaal).

## 6. Ronde Z41: de graaf laten kloppen

- 851 draden naar oude versies → 0. Gevolgd naar de levende opvolger.
- 19 + 22 doodlopende verwijzingen → 0. Naar de opvolger, of vijf nieuwe gebeurtenissen als voorstel in de ideeënbank.
- 35 zwevende haken kregen knopen uit hun eigen tekst.
- **Eén persoon = één knoop** (`persoon_identiteit`, afgeleid): 133 personen stonden onder twee codes.
- Fasefouten hersteld: Liora's queeste en het Selvine-conflict horen in 801.
- Ontdekt en hersteld: de kaart telde aanvankelijk alleen de categorie "Verhaal". Met de genre-skeletten erbij zijn het 1.279 verhaallijnen.
- Rogier: "heb je niet veel gesloopt?" Controle: 0 rijen verwijderd, 0 statussen veranderd.

## 7. Van overzicht naar nieuwe verhalen

- Rogier: "ik dacht dat je allerlei verhalen kon maken." Het eerlijke antwoord: er waren ongeveer 30 uitgewerkte bogen, ongeveer 170 premisses en ongeveer 430 kiemen.
- Rogier stelde voor: **willekeurige personen maken en kijken welke de beste verhaallijnen geven, met de grootste diversiteit.** Dat is quality-diversity (MAP-Elites).
- **Van 801 naar achteren**, zodat de hoofdlijn niet verstoord raakt (Rogier).
- `z41/personen.py`: 2.000 personen, samengesteld uit fragmenten van bestaande mensen; botsingen als score; een raster volk × positie. Verbeterd na het lezen:
  - geslachtsfouten eruit;
  - de hoofdlijn trekt niet alles naar zich toe;
  - tweelingcodes tellen niet dubbel.
- **Regel ontdekt:** een geleend geheim wordt kennis over de ander, nooit een tweede dader. Zo ontstonden de driehoek Jorna, Kerr en Orl.
- 12 verhalen voor 801 in de ideeënbank (`VERHAAL-Z41-801-01..12`).

## 8. Rijkdom, raarheid, Tolkien en mythen

- Rogier: "**rijkdom is raarheid**", dus diversiteit. De architect scherpte aan: het gaat om raarheid die klopt, wat logisch volgt uit de regels en alleen hier kan bestaan.
- Criteria voor verbreding (Rogier): interessant, horror, erotiek, spanning, suspense, actie, thriller, verwondering, plus wat helpt na de breuk van het Zegel.
- Principe: **verleden, smaak, toekomst** voor elk nieuw ding.
- Rogier: Velmara als vergeten aarde? Afweging:
  - **letterlijk** breekt de Kern;
  - **thematisch** (na de breuk groeit de wereld naar de onze toe) past;
  - de aarde blijft een vermoeden, nooit bevestigd.
- Rogier wees op Tolkien: The Lord of the Rings gaat over het verval van Midden-aarde en het verdwijnen van de magie. Gevolg: **verwondering zit in verlies.** De gaven kunnen bij de breuk uitdoven.
- Rogier: **aardse mythen hebben hun oorsprong in Velmara.** De lezer herkent ze steeds meer, er zijn verhalen in de wereld van nu mogelijk, en er wordt ruimer geput uit mythologie.
  - Uitwerking: gebruik motieven die wereldwijd voorkomen. Zwanenmeisje, selkie en hemelvrouw zijn één oorsprong. De Ves-Lethi passen op de vossenvrouwen.
  - Meer ruimte voor spicy versies, met een warmteknop. De harde lijnen gelden altijd.

## 9. De repo

- Rogier: dit via Claude Code in een eigen repo. Opgezet: `rmvmeulenaar/worldbuilding_velrena`.
  - **De tekst is de bron** (`wereld/canon_tekst/`, 69 bestanden, byte-exact). De database wordt eruit gebouwd en is tabel voor tabel gelijk.
  - `velmara.py` (bouw, tekst, toets, kaart).
  - CLAUDE.md met alle regels.
  - CI.
- Databasevraag: SQLite houden, later zoeken op betekenis (sqlite-vec). Kuzu werd eerst aangeraden en daarna ingetrokken, omdat het in oktober 2025 door Apple werd overgenomen en stilgelegd.

## 10. Van canon naar wereldmotor

- Iedereen die ooit leefde, moet op te roepen zijn. Dat is procedureel, niet opslaan (zoals Dwarf Fortress).
- Rogier: het doel is een avontuur waarin je **beleeft**: strategie, erotiek, horror, spanning, of een rustig leven. Verhalen zijn een bijproduct. Schrijven met simulatie en spelen zijn **dezelfde machine met een andere stoel**.
- Onderzoek naar wat bestaat:

| Onderwerp | Wat er bestaat |
|---|---|
| levende geschiedenis en personen | Dwarf Fortress, Crusader Kings, De Sims |
| één wereld, veel schrijvers | Warhammer, SCP Foundation, D&D |
| LLM als verteller zonder canon | AI Dungeon |
| handelingen met voorwaarden en gevolgen | Story2Game, PANGeA |
| proza naar regels (Rules as Code) | Catala, RegelSpraak, Guan e.a. |
| simulatie met ijkpunten | Approximate Bayesian Computation |
| verhalen zeven | James Ryan, Felt en Winnow van Max Kreminski |
| rijm | structure mapping (Gentner), StoryAnalogy |
| mythen uit geschiedenis | Caves of Qud |
| spel wordt legende | Wildermyth |

- Conclusie: ongeveer 75% is na te maken. De echte uitvinding is klein: **proza naar toetsbare regels, en een maat voor rijm**, en beide hebben al een vertrekpunt.
- Rogier over weging in het recht: "ook weging kan geautomatiseerd worden." Ja: factorgebaseerd redeneren, mits de gewichten expliciet zijn.

## 11. De architectuur, en twee correcties van Rogier

1. De architect stelde een kleine proef voor op een stukje 801. Rogier: "we hebben een canon, ik ga geen uren in een klein ding steken." Daarna: "**ontwerp het alsof het een enorme game is**, bewijs dat de architectuur in zijn geheel werkt."
2. De architect begon te bouwen. Rogier: "**nee, eerst de grootste schets van de hele architectuur met requirements, dan een paar keer testen met simpele dingen, en als het werkt opnieuw opzetten maar dan groot, eventueel met een andere wereld.**" Het begonnen werk staat in `verkenning/motor_spike/` (niet gebruiken, alleen ter inzage).
3. De eerste schets was een functioneel ontwerp. Rogier: "dit is geen software-architectuur." Daarop volgde de software-architectuur (arc42 en C4). Daarna Rogier: "het functioneel ontwerp is goed, maar daar hoort ook bij hoe je het bouwt en met welke tests." Daarop volgde het bouwplan.

Resultaat, in `architectuur/`:
- `VISIE_EN_EISEN.md`: wat;
- `SOFTWARE_ARCHITECTUUR.md`: hoe;
- `BOUWPLAN.md`: in welke volgorde, met welke tests;
- `HISTORIE.md`: dit verslag.

---

## Lessen voor elke volgende sessie

1. **Vraag je af wat Rogier bouwt, niet wat jij interessant vindt.** Elke keer dat de architect afdreef naar validatie of gereedschap, corrigeerde Rogier naar verhalen en beleving.
2. **Gebruik de hele canon, geen speelgoedstukje van Velmara.** Klein proberen mag alleen met een aparte speelgoedwereld, om de architectuur te bewijzen.
3. **Eerst ontwerp, dan tests, dan bouw.** De rollen architect, tester en bouwer zijn gescheiden.
4. **Eerlijk tellen.** Zeg wat er is, en wat niet.
5. **Niets slopen.** Nooit verwijderen, altijd bewijzen dat er niets verloren ging.
6. **Bronnen van het onderzoek** staan in de documenten zelf. De belangrijkste: Story2Game (arXiv 2505.03547), PANGeA (arXiv 2404.19721), Catala (Microsoft Research), Translating Tax Law to Code (NLLP 2025), Guan e.a. (NeurIPS 2023), DIYABC (arXiv 0804.4372), Winnow (AIIDE 2021), Felt, Select the Unexpected (ICIDS 2022), StoryAnalogy (arXiv 2310.12874), en het nieuws over Kuzu (The Register, 14 oktober 2025).
