# Mytheplan: alle mythen van de aarde krijgen hun oorsprong in Velmara

Versie 0.1, 1 november 2026. Opdrachtgever: Rogier. Uit te voeren in Claude Code. De rollen architect, tester en bouwer staan in `BOUWPLAN.md`.

## Uitgangspunt
**Dit is fantasie, geen wetenschap.** We gebruiken kennis (mythologie, folklore, geschiedenis) als gereedschap om alles **aannemelijk** te maken, niet om iets te bewijzen. De lezer moet steeds vaker denken: *"hé, dit herken ik"*. Tegen het eind van de reeks moet hij vermoeden dat onze mythen herinneringen zijn aan Velmara.

De grote lijn:
1. **Boek 0 tot en met de finale.** De acht lagen lopen naar 801. Daar komt de ja terug in het Zegel: meer mannen worden geboren, mensen mogen vervormingen en gaven weigeren, en wat genomen werd, valt weg.
2. **Na 801.** De magie sterft langzaam, want alleen gegeven kracht blijft, en die wordt elke generatie zwakker.
3. **De mythische tijd**, zoals Midden-aarde: helden en gaven worden legende.
4. **Onze wereld.** Wat overbleef, zijn onze mythen. Het zijn vervormde herinneringen.
5. **Later:** de recentere wereldgeschiedenis als echo en rijm.

Het trucje "de goden waren ruimtevaarders" (von Däniken) is vrij te gebruiken. Velmara draait het om: de goden waren de Makers, en de godin was een vrouw.

## Stap 1: verzamelen
Een kernset van **100 tot 150 grote motieven**, uit de catalogi als gereedschapskist:
- **Thompson, Motif-Index:** de motieven;
- **Aarne-Thompson-Uther:** de verhaaltypes;
- **Berezkin:** waar ter wereld een motief voorkomt;
- **Witzel:** de gedeelde verhaallijn van schepping tot einde.

**Breed putten:** Grieks, Noors, Keltisch, Mesopotamisch, Egyptisch, Bijbels, Indiaas, Chinees, Japans, Afrikaans, Amerikaans en Oceanisch.

Per motief leggen we vast:

```yaml
- motief: gestolen hemelvuur
  codes: {thompson: A1415, atu: null}
  voorbeelden: [Prometheus (Grieks), Maui (Polynesisch), Matarisvan (Indiaas)]
  kern: iemand haalt de kracht van de goden naar de mensen en wordt gestraft
  verspreiding: [Europa, Zuid-Azië, Oceanië, Noord-Amerika]
```

## Stap 2: clusteren
Motieven die op veel plekken terugkomen, horen samen. Een paar voorbeelden van clusters:
- de **zwanenmaagd**: selkie, Japanse hemelvrouw, Valkyrie-huid;
- de **vloed met de ark**: Noach, Utnapishtim, Manu;
- het **gestolen vuur**: Prometheus, Maui;
- de **afdaling in de onderwereld**: Persephone, Inanna, Orpheus;
- de **vormwisselaar**: kitsune, wolfsman, selkie;
- het **labyrint met monster**;
- de **eerste vrouw die alles opent**: Pandora, Eva;
- de **schemering van de goden**: Ragnarök.

**Hoe meer culturen een cluster heeft, hoe waardevoller het is.** Precies die universaliteit verklaart één oorsprong in Velmara.

## Stap 3: plaatsen in de lagen van Velmara
Elk cluster krijgt een oorsprong in een laag, volgens deze verdeling:

| Verhaallijn | Laag | Voorbeelden van oorsprong |
|---|---|---|
| schepping, aankomst, ark | 0 Voortijd | het zaaischip Ysa met elfduizend slapers; de Makers als goden |
| eerste vrouw die opent | 0 Voortijd | Hesta opent de stemkist vóór de stemming (Pandora) |
| gouden tijd, het eerste erfrecht | 1 Overvloed | de koningen van de delta |
| gestolen hemelvuur | 2 Vonk | Orric raakt de Sterrensteen aan; de Vonkkoorts als dagelijkse straf (Prometheus) |
| vloed, offer, onderwereld | 3 Brand | het Zegel, het Offer der Dochters, de Dochters in de steen (Persephone) |
| wetten, orde, verborgen kinderen | 4 Noodtoestand | Deelwet, register, Jongenshof |
| goden, tempels, heilige gemeenschap | 5 Ontvangst | het zegellicht, de Ontvangst |
| monsters, labyrinten, helden | 6 Markt | reuzenstieren onder Saelith (Minotaurus), de Pest |
| schemering der goden | 7 Barsten | het Zegel lekt, Kharvos valt aan (Ragnarök) |
| het einde van de oude tijd | 801 | de ja keert terug |
| raven die namen dragen | doorlopend | de registerkraaien met de klik van Ysa's stem (Hugin en Munin) |
| zwanenmaagden en vormwisselaars | doorlopend | Sael-mor, Ves-Lethi |
| verzonken stad | 6 Markt | Ves-Anath, in 603 ontruimd (Atlantis) |

Per oorsprong leggen we vast:

```yaml
- cluster: gestolen hemelvuur
  oorsprong: {laag: 2, canon: [GEB-orric-vonk, FASE-vonk], nieuw: null}
  vervorming:                      # door de eeuwen, van Velmara naar de aarde
    - "Orric raakt de steen uit de hemel aan en krijgt de storm"
    - "een man steelt het vuur van de goden"
    - "Prometheus; elke dag eet een adelaar zijn lever (= de Vonkkoorts)"
  herkenning: "de straf die elke dag terugkomt"
  verlies: "na 801 dooft de vonk; het vuur wordt een verhaal"
  boek: 2
  smaak: {verwondering: 5, horror: 2, erotiek: 1}
```

## Stap 4: vervormingsregels (de mythemotor)
Zo wordt geschiedenis een mythe. Elke keten gebruikt er twee tot vier:
- **een mens wordt een god**: de Makers, Ysa;
- **een machine wordt een wezen of een orakel**: de Reckoner, de Wieg;
- **een getal wordt een symbool**: 1 op 100, honderd Dochters;
- **een besluit wordt een straf of een vloek**: de Stille Modus wordt een goddelijke vloek;
- **een groep wordt één held of één monster**;
- **een gefokt lichaam wordt een mengwezen**: de reuzenstier wordt de Minotaurus;
- **schuld verschuift** van wie het besloot naar wie het onderging;
- **de plek verschuift** naar een bekende plek op aarde;
- **het erotische wordt verhuld** tot een huwelijk met een god, of een verboden vrucht.

## Stap 5: door de poort
Elke oorsprong moet kloppen met de canon. Ze gaat als voorstel de ideeënbank in, en Rogier beslist wat canon wordt. Daarbij gelden twee dingen:
- **De harde lijnen gelden ook voor mythen.** Veel oude mythen bevatten ontvoering of dwang. In Velmara wordt dat een gelabeld donker thema tussen volwassenen, of het blijft weg. Nooit minderjarigen.
- **We nemen motieven, geen teksten.** Motieven zijn van iedereen. Moderne bewerkingen en de werelden van andere auteurs nemen we niet over: niet van Tolkien, niet van Star Wars. Een knipoog in een zin mag.

## Stap 6: in het plot zetten
- Per boek een handvol herkenningen, steeds duidelijker. In boek 1 alleen een detail, in de finale vallen de stukken samen.
- De **finale** opent "de andere werelden": de kaartplaat met drie werelden en de vloot van de Ysa en de Harrow. Dat is de deur naar de aarde. Nooit bevestigd, alleen vermoed.
- Daarna, in eigen boeken: **de mythische tijd** (de heldentijd na de magie) en **verhalen in de wereld van nu** (urban fantasy), met sporen als een Sterrensteen-meteoriet, een familie met de gave, en een woord in drie talen.

## Stap 7: recentere wereldgeschiedenis (later)
Na de mythen volgen de oudheid en latere tijdperken, als **echo en rijm**. Hetzelfde patroon van de prijs van een lichaam keert terug in een historische vorm. Echte volken en levende godsdiensten worden niet belachelijk gemaakt en niet tot product van Velmara verklaard. Hun motieven mogen we wel gebruiken, zoals alle fantasy dat doet.

## Opleveringen
| # | Wat | Waar |
|---|---|---|
| M1 | kernset motieven (100–150) | `wereld/mythen/motieven.yaml` |
| M2 | clusters met verspreiding | `wereld/mythen/clusters.yaml` |
| M3 | oorsprongen in Velmara met vervormingsketen | `wereld/mythen/oorsprong.yaml` + voorstellen in de ideeënbank via een rondescript (`r_Z42.py`) |
| M4 | vervormingsregels | `wereld/mythen/vervorming.yaml` (later de mythemotor, F-Z4) |
| M5 | plotplaatsing per boek | `wereld/mythen/plot.md` |
| M6 | mythekaart: per laag welke aardse mythen eruit voortkomen | uitbreiding van de knopenkaart |

## Toetsen
- Elke oorsprong verwijst naar bestaande canonrijen, of is een nieuw voorstel met epistemiek "voorstel". De canon-toets moet groen blijven.
- Elk cluster komt in minstens drie culturen voor, of het is bewust als lokaal gemarkeerd.
- Elke vervormingsketen heeft twee tot vier regels uit stap 4. De aardse mythe moet herkenbaar zijn aan het herkenningsdetail.
- De harde lijnen worden op elke oorsprong getoetst.
- Rogier leest een steekproef van tien en kiest welke canon worden.

## Volgorde
M1 en M2 (verzamelen en clusteren), dan M3 voor de twintig sterkste clusters, dan M4 en M5, dan M6. Daarna de rest van de clusters.
