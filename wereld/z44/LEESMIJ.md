# Z44 · De technologieboom van Velmara

**Status: voorstel en simulatie. Niets hiervan is canon.** Rogier beslist via `KEUZE-Z44-*` (`keuzelijst_Z44.md`).

Na review 1 waren de uitvindingen het zwakste deel van de motor:
- de volgorde was willekeurig: stoom kwam vóór ijzer
- stoom op kolen botste met de canon
- de lijst was de aardse reeks

Z44 vervangt die lijst door een boom die uit de canon zelf groeit.

## De ontwerpregel

> Een uitvinding ontstaat pas als **de wereld haar mogelijk maakt** (alle vereisten bestaan en de materiaalvoorwaarde klopt), **de geschiedenis haar nodig of aantrekkelijk maakt** (een crisis vroeg erom, of het loont gewoon), en **haar bestaan de volgende geschiedenis verandert** (toestand en macht veranderen, en latere crises kunnen van haar erven).

## Waar de boom vandaan komt

De canon kent vier technieken (`TECHNO-REGEL-V4`), elk met eigen bouwstoffen, energie, kosten, bewaking en faalwijze:
- **bio** (`TECHNO-bio`): vlees, bloed, schimmel en bot; moet eten; faalt door inteelt en uitbraken
- **gave** (`TECHNO-gave`): lading van levende mannen; kost de gever dagen; na 801 alleen met zijn eigen ja (`BESLUIT-Z36-4`)
- **zegelsteen** (`TECHNO-zegelsteen`): komt uit Orrim-lichamen en de Sterrensteen; barst bij overgebruik
- **metaal** (`TECHNO-metaal`): niemand kan het maken; het kan alleen hersteld en gekannibaliseerd worden

De mengvormen komen uit `TECHNO-MIX-V4`, de afstoting uit `TECHNO-SCHAAL`. De harde grenzen: er is geen brandstof en weinig erts (`ORIGIN-2`), en de roestschimmel eet legering (`YSA-Z17-6`).

## De boom (`tech_knoop`, view `v_tech_boom`)

| Familie | Knoop | Vereist | Breekt |
|---|---|---|---|
| bio | Kweekakkers | | de dragers als redders van de oogst |
| bio | Het sporennet | | de kerk als enige die weet wat er gebeurt |
| bio | Roestlak | | maakt metaal weer bruikbaar |
| bio | Spiermolens | kweekakkers | de dragers als enige krachtbron |
| bio | Heelkweek | kweekakkers | de kloosters als enige plek om te genezen |
| bio | Sporendruk | sporennet | de kerk als enige die schrijft |
| gave | Vrije laadsters | | het laadmonopolie van de Registerkamer |
| gave | Het echonet | vrije laadsters | de afstand tussen hof en grens |
| gave | Laadwerkplaatsen | vrije laadsters | (maakt dragers juist onmisbaar) |
| zegelsteen | Het lichtnet | | de afstand tussen kroon en provincies |
| zegelsteen | De steenlens | lichtnet | de onzichtbaarheid van wat ziek maakt |
| zegelsteen | Lichtcellen | steenlens | de dragers als enige krachtbron, maar de vraag naar Orrim-steen stijgt |
| metaal | Kluisherstel | een vondst | het geheim van de Orde-kluizen |
| metaal | Lakijzer | roestlak | de drager als onverslaanbare krijger |
| gave + zegelsteen | Gaveglas | vrije laadsters, lichtnet | het donker van de winter, voor wie betaalt |
| bio + metaal | De sporenkern | kluisherstel, roestlak | de grens tussen levende en dode techniek |
| bio + metaal | Vleesmetaal | kluisherstel | de lengte van een Leegtevaart (de worm wordt waanzinnig) |

Elke knoop heeft verder een materiaalvoorwaarde, de crises waar hij uit kan voortkomen, een uitvinder, een gevolg, een prijs en een canonbron.

Twee paden concurreren met elkaar. Spiermolens en lichtcellen maken de dragers overbodig als krachtbron. Laadwerkplaatsen maken ze juist onmisbaar. Welk pad een geschiedenis neemt, hangt af van haar crises.

**Wat Velmara niet doet**, en waarom. Dit staat ook in `tech_knoop`, met status `onmogelijk` of `onnodig`:
- **stoom en kolen:** er is geen brandstof
- **staal in grote hoeveelheid:** er is weinig erts, en de roestschimmel eet het op
- **kruit:** onnodig, want brandader, lichtspiegel en vonkpijl bestaan al
- **een stroomnet met draden:** onnodig, want lading en lichtcellen zijn de stroom
- **zelfgebouwde rekenmachines:** machinekennis is verboden en vergeten
- **nieuwe energiekernen:** die zijn niet bij te vullen

## In de motor (`z44/geschiedenis.py`, regels `GESCH3-*`)

- **Voorwaarde:** een knoop kan pas ontstaan als zijn vereisten er zijn, zijn materiaal klopt en zijn uitvinder minstens 5% van de macht heeft.
- **Nood maakt vindingrijk:** heeft een crisis in de laatste 100 jaar om de knoop gevraagd, dan is hij ruim tien keer zo waarschijnlijk.
- **Gevolg:** de uitvinding verandert direct toestand en macht, en latere crises kunnen van haar erven.
- **Techniek groeit zelf trager** dan in Z43; de rest komt uit uitvindingen.
- **Edelen kosten de staat geld (Turchin).** Zonder die regel verdween de strijd om posities, zodra de kweekakkers extra voedsel gaven.

## Uitkomsten (1000 runs, dezelfde seeds als Z42 en Z43)

- **Uitvindingen:** gemiddeld 10 per geschiedenis, waarvan 4 uit nood.
- **Volgorde:** **900 verschillende volgordes in 1000 runs.** Elke geschiedenis kiest een eigen technisch pad.
- **Hoe vaak elke knoop voorkomt:**
  - vrije laadsters: 913 van de 1000
  - kluisherstel: 866
  - spiermolens: 562
  - lichtcellen: 342
  - gaveglas: 145
- **De tijd van de werkplaatsen** (techniek boven 0,6) komt in 642 van de 1000 runs, gemiddeld vanaf 3811. In de rest blijft Velmara pre-industrieel.
- **Overig:** 11 fasen, 7 crises die niemand kon oplossen, en 11 golven van magie per geschiedenis.

## Lezen

```sql
select * from v_tech_boom;                                      -- de boom, ook wat onmogelijk is
select * from v_sim_uitvinding where run_id='Z44-GESCH-0003';  -- wat, wanneer, door wie, uit welke nood
select van, crisis, naam, erft_van from v_sim_keten
 where run_id='Z44-GESCH-0003' and erft_van like 'uitvinding%'; -- crises die van een uitvinding erven
select module, scores from sim_run where seed=420003;           -- Z42, Z43 en Z44 naast elkaar
```

## Toets

- 45 regels, 0 nieuwe fouten; de roundtrip is gelijk, ook voor `tech_knoop` en `sim_uitvinding`.
- **`R-tech_boom`:** de boom is volledig, en elke vereiste bestaat.
- **`R-sim_uitvinding`:** een uitvinding komt nooit vóór haar vereisten, en heeft een uitvinder met macht, een noodzaak en een gevolg.
- **Negatieve test:** drie expres aangebrachte fouten werden alle drie gevonden.

## Zwaktes die nog open zijn

1. **Geen regio's.** Er is nog geen verspreiding van een uitvinding van stad naar stad. De Z39-module `technologie` kan dat per regio, maar is nog niet gekoppeld.
2. **De boom is klein: 17 knopen.** Een tweede laag knopen ontbreekt nog, zoals wat er volgt op lichtcellen of sporendruk.
3. **Het gevolg is vast per knoop.** Het hangt niet af van wie de knoop uitvindt.
4. **Z44 is gebouwd en getoetst door dezelfde architect.** Laat de nakijker blok H uit `z42/NAKIJKVRAGEN.md` op Z44 draaien.
