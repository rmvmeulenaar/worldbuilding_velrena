# Mytheplan: alle mythen van de aarde krijgen hun oorsprong in Velmara

Versie 0.2, 2 november 2026 (M0 tot en met M5 uitgevoerd in ronde Z43: zie `wereld/wijzigingen_Z43.md`). Opdrachtgever: Rogier. Uit te voeren in Claude Code. De rollen architect, tester en bouwer staan in `BOUWPLAN.md`.

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

### Theorieën over hoe mythen vervormen (gereedschap voor de motor)
| Theorie | Wat ze zegt | Wat de motor ermee doet |
|---|---|---|
| **Euhemerisme** (Euhemerus, ca. 300 v.Chr.) | goden waren ooit mensen die na hun dood vergoddelijkt werden | Makers, Ysa en gaven-mannen worden goden; dit is de ruggengraat van het hele plan |
| **Serial reproduction** (Bartlett, *Remembering*, 1932) | wie een verhaal doorvertelt, maakt het korter, logischer en passend bij de eigen cultuur; vreemde details verdwijnen of worden vervangen door vertrouwde | per eeuw doorvertellen: vreemde techniek wordt magie, onbekende dieren worden bekende |
| **Mondelinge overlevering** (Parry en Lord; Vansina) | vaste formules blijven, details zwerven; tussen de oorsprong en het recente verleden zit een "zwevend gat" | sommige zinnen blijven letterlijk staan ("de prijs van het lichaam"), de rest vervormt; het gat tussen 801 en onze tijd is dat zwevende gat |
| **Structuralisme** (Lévi-Strauss) | varianten van een mythe zijn transformaties van dezelfde tegenstellingen (natuur/cultuur, leven/dood) | elke variant is een andere oplossing van de tegenstelling geven/nemen, ja/nee |
| **Morfologie** (Propp) | verhalen bestaan uit vaste functies (verbod, overtreding, beproeving, terugkeer) | de vervormde mythe houdt de functies; personages en plekken wisselen |
| **Ziekte van de taal** (Max Müller) | een beeldspraak wordt letterlijk genomen ("de zon verslindt de dageraad" wordt een monster) | uitdrukkingen uit Velmara worden wezens en gebeurtenissen |
| **Geomythologie** (Adrienne Mayor) | mythen ontstaan uit vondsten: botten, fossielen, ruïnes | sporen van Velmara op aarde verklaren mythen (zie wezens) |
| **Stamboom van mythen** (d'Huy) | mythen veranderen langs verspreidingsroutes, zoals talen | toets: de verspreiding van een vervormde mythe moet geloofwaardig ogen |

### Hoe mythische wezens ontstaan, en wat ze in Velmara waren
Wezens ontstaan op een handvol manieren:
- **Botten en fossielen** (geomythologie): de griffioen uit fossielen van *Protoceratops* in de Gobi; de cycloop uit schedels van dwergolifanten met één groot neusgat (Abel, 1914).
- **Verkeerd beschreven echte dieren:** de eenhoorn uit de narwal en de neushoorn; de zeemeermin uit doejongs en lamantijnen.
- **Lichaam en ziekte:** de nachtmerrie en incubus/succubus uit slaapverlamming; de weerwolf en de vampier deels uit ziekte en ontbinding.
- **Samenvoegen** van delen: sfinx, chimaera, minotaurus.
- **Angsten en natuurkrachten** die een gezicht krijgen.
- **Mensen die goden worden** (euhemerisme).

In Velmara zijn de wezens **echt**. Body horror en volken zijn de oorsprong, en de vervorming doet de rest:

| Aards wezen | Oorsprong in Velmara | Mechanisme |
|---|---|---|
| **dwergen** (smeden in de berg) | de **Dhurn**: stralingstaai gefokt voor de mijnen, met handen die de machines nog herkennen | volk wordt soort |
| **elfen** (lang levend, geheugen, mist) | de **Aelthir**: hoven, het Lange Geheugen | volk wordt soort |
| **feeën, feeënringen, vooroudergeesten** | de **Myrrhen**: het Netwerk onthoudt de doden; feeënringen | schimmel wordt magie |
| **reuzen en trollen** | de **Tharn**: Bor de Poortreus, Grom de Reuzenstier | volk wordt soort |
| **minotaurus** | de **reuzenstieren** in de stallen onder Saelith | gefokt lichaam wordt mengwezen |
| **harpijen, engelen** | de **Skerra** met vleugels | volk wordt soort |
| **zeemeerminnen, selkies, zwanenmaagden** | de **Sael-mor** en **Oevrin** | volk wordt soort; huid die je aflegt |
| **weerwolven, kitsune, gedaantewisselaars** | de **Ves-Lethi** | volk wordt soort |
| **draken, zeeslangen, Jörmungandr** | de **Leegtewormen**, met het Harrow-ruim in hun buik | dier wordt monster |
| **vampiers** (koude die warmte steelt) | **zegellicht** dat de warmte uit ontvangsters trekt | ziekte wordt wezen |
| **incubus en succubus** | de **Ontvangst** in tempels, de stormontlading | ritueel wordt nachtmerrie |
| **wisselkinderen** | de **lekjongens**, verstopt en geruild om ze te redden | verborgen kind wordt feeënkind |
| **versteende wezens, gargouilles** | de **Dochters en Orrim** in de steen | lichaam wordt beeld |
| **vuurreuzen, ifrits** | gaven-mannen met de **Vonkkoorts** | ziekte wordt geest |
| **dondergod** (Zeus, Thor) | gaven-mannen met de **storm** | mens wordt god |
| **reuzenbotten in de aarde** | botten van reuzenstieren en Tharn, op aarde gevonden | geomythologie |

Zo is elk wezen tegelijk een **verlies** (Tolkien). Na de breuk sterven de volken uit of vermengen ze. Wat overblijft, zijn verhalen over dwergen en elfen.

### Het hele bovennatuurlijke veld, niet alleen wezens
| Soort | Voorbeelden op aarde | Oorsprong in Velmara (richting) |
|---|---|---|
| **spoken en geesten** | spookhuizen, stemmen in stenen, rusteloze doden | scherven van de Reckoner ("elk stuk bleef vragen"), Thalens patroon, Ysara's stem in de Wortel, het Netwerk van de Myrrhen, registerkraaien die namen van doden roepen |
| **demonen en bezetenheid** | iets wat in je lichaam kruipt en je wil overneemt | vonkcellen in het lichaam; een gave die zonder ja niet weg kan |
| **goden en halfgoden** | pantheons, kinderen van goden | Makers, Ysa, gaven-mannen, hun nakomelingen (euhemerisme) |
| **hiernamaals en onderwereld** | Hades, Hel, Valhalla, het paradijs | de steen van het Zegel, het Netwerk, de deep memory van de Reckoner |
| **heksen en tovenaressen** | kruidenvrouwen, vloeken, bezems | Zusterheelsters, Stille Zusters, kluisgeneeskunde |
| **vloeken en geboden** | erfvloek, taboe, verboden vrucht | de Stille Modus als vloek op zonen, de Deelwet, het schriftverbod |
| **heilige voorwerpen** | graal, ring, zwaard in de steen | Sterrensteen, de sleutel van Thalen, de kaartplaat, de logboekplaat |
| **plekken** | Atlantis, Avalon, de Olympus, het labyrint | Ves-Anath, de Wieg, de Stemklok-kamer, de stallen onder Saelith |
| **kosmologie en eindtijd** | Ragnarök, zondvloed, wereldboom | Barsten, Brand, de Wortel |
| **helden en bedriegers** | Herakles, Loki, Anansi | figuren uit de bogen per fase |

## Aanpak: hoe we dit met databases doen
Het is een grote klus, maar geen handwerk. We oogsten, koppelen en laten de machine voorstellen doen. Alleen het kiezen doet Rogier.

### Bronnen die als database bruikbaar zijn
| Bron | Wat | Gebruik |
|---|---|---|
| **Wikidata** (vrij, CC0, opvraagbaar met SPARQL) | duizenden legendarische wezens, goden, geesten, plekken en voorwerpen, met cultuur en eigenschappen | de ruggengraat: entiteiten en verbanden oogsten |
| **Project Gutenberg** (publiek domein) | oude mythologieën in volledige tekst: Edda, Bulfinch, Frazer (*The Golden Bough*), Grimm, Lang | verhalen en details ontginnen; vrij te gebruiken |
| **Motievencatalogi** (Thompson, ATU, Berezkin) | codes en indeling van motieven | alleen codes en indeling overnemen, geen tekst |
| **Wikipedia** | samenvattingen, overzichtslijsten | alleen als achtergrond; in eigen woorden, nooit kopiëren |

### Database (eigen bestand `wereld/mythen/mythen.db`, los van de canon)
```sql
create table entiteit(id text primary key,            -- bv. Wikidata-id
  naam text, soort text,                               -- wezen, geest, god, plek, voorwerp, vloek, held, ...
  cultuur text, regio text, periode text, bron text);
create table kenmerk(entiteit text, kenmerk text, waarde text);   -- vleugels, koud, steen, drinkt bloed, wisselt van vorm, ...
create table motief(entiteit text, systeem text, code text);      -- thompson, atu, berezkin
create table cluster(id text primary key, naam text, kern text);
create table lid(cluster text, entiteit text);
create table oorsprong(cluster text, laag text, canon_codes text, voorstel text, score real, status text);
create table vervorming(cluster text, stap int, eeuw text, tekst text, regel text);
```

### Pijplijn
| Stap | Wat | Wie |
|---|---|---|
| **M0 oogsten** | Wikidata opvragen (legendarische wezens, geesten, goden, plekken, voorwerpen) naar `entiteit`; teksten van Gutenberg ophalen | script |
| **M1 kenmerken** | per entiteit de kenmerken uit beschrijving en tekst halen (vleugels, koude, steen, bloed, vorm wisselen, onderwereld, ...) | LLM, met steekproef door de architect |
| **M2 clusteren** | groeperen op gedeelde kenmerken en motiefcodes, over culturen heen | script |
| **M3 koppelen** | de kenmerken van de clusters naast de kenmerken van Velmara-dingen (volken, lichaamsvormen, plekken, voorwerpen, gebeurtenissen uit de canon) leggen; de beste kandidaat-oorsprong per cluster, met score | script + LLM |
| **M4 vervormen** | per gekozen koppeling de keten van eeuw tot eeuw, met de theorieën hierboven | LLM, binnen de regels |
| **M5 door de poort** | canontoets en harde lijnen; als voorstel in de ideeënbank | motor + Rogier |
| **M6 plot** | per boek plaatsen; mythekaart | architect + Rogier |

**Waarom dit werkt:** dezelfde aanpak als bij de canon. De bronnen leveren de breedte, de kenmerken maken alles vergelijkbaar, de koppeling stelt voor, de poort bewaakt, en Rogier kiest. Elke keer dat er iets wordt toegevoegd, wordt het geheel rijker.

**Netwerk:** Wikidata en Gutenberg zijn vanaf een gewone computer bereikbaar. In een afgeschermde cloudsessie kunnen ze geblokkeerd zijn. Draai M0 dan lokaal, in Claude Code op je eigen machine.

## De lijn: één plek, door diepe tijd
**Kolonisten uit de sterren (lang geleden, ver weg) → Velmara → Midden-aarde → de aarde.**

Velmara **is** de aarde, in haar vergeten diepe voortijd. Er hoeft niets "naar de aarde te komen". De herinnering blijft op dezelfde grond en vervormt mee met de tijd.
- De **kolonisten** komen uit een sterrenbeschaving, met de vloot van de Ysa en de Harrow en de kaartplaat met drie werelden. Dat is onze eigen versie van "lang geleden, in een sterrenstelsel ver weg". Een knipoog naar Star Wars mag, hun wereld overnemen niet.
- **Velmara**: de acht lagen tot 801 (canon).
- **Midden-aarde**: na de ja sterft de magie, de volken vervagen of vermengen, en de gaven worden legende. De heldentijd.
- **De aarde**: wat blijft, zijn onze mythen, wezens en spoken als vervormde herinnering. Ook het landschap draagt sporen.

## Tijd: veel tellingen, één onderliggende as, en de data beslist
**"800 jaar" is de telling van de Orde.** Elk volk en elk tijdperk telt anders: Zegeljaren, de telling van de Orde ("achthonderd jaar geleden" voor een gebeurtenis die in werkelijkheid in jaar 130 werd gekaapt), jaren na de landing, de tellingen van de volken, de mythische "lang geleden". De motor slaat alles op één **onderliggende tijdas** op en rekent elke telling daarnaar om.

| Telling | Van wie | Nulpunt |
|---|---|---|
| jaren na de landing | Makers, Reckoner | de landing (Zegeljaar ca. −1240) |
| Zegeljaren | canon, register | jaar 0: het Zegel |
| Ordetelling | Orde van de Ontvangst | de "legging" volgens de leer (vervalst) |
| volkstellingen | per volk (Aelthir, Karrûk, ...) | eigen nulpunten (per volk in het wereldpakket) |
| jaren geleden (BP) | de aarde van nu | heden |

**Niet vragen, schatten.** Waar Velmara op de as van de aarde ligt (hoeveel jaar geleden 801 was), hoe lang Midden-aarde duurt en hoe snel de magie sterft: dat bepaalt Rogier niet met de hand. De motor schat het uit de gegevens, met dezelfde methode als de simulatie met ijkpunten (Approximate Bayesian Computation):
1. **Beperkingen verzamelen** uit drie bronnen.
   - **Mythen.** Elk cluster heeft een tijdvenster uit zijn verspreiding. Wat op alle continenten voorkomt, moet ouder zijn dan de verspreiding van de mens over Amerika. Wat alleen in Eurazië voorkomt, kan jonger zijn. De eerste geschreven mythen zijn een ondergrens.
   - **Canon.** De snelheden die erin staan: de verhouding schuift in decennia van 1 op 100 naar 1 op 20; de gaven doven binnen een generatie bij breken, gedeeltelijk bij de derde weg; de volken hebben een eigen voortplanting en levensduur.
   - **Landschap** (geomythologie). Het einde van de laatste ijstijd: zeespiegelstijging, verdronken land zoals Doggerland, Sundaland en Beringia, inslagkraters. Die maken vloed, verzonken steden en hemelstenen aannemelijk.
2. **Simuleren.** Veel lopen met verschillende ankers en duren: hoe snel sterft de magie, hoe snel sterven de volken uit of vermengen ze, hoe snel vervormt een verhaal.
3. **Houden wat past.** Alleen de lopen die de meeste beperkingen halen. Het resultaat is een aannemelijke bandbreedte per tijdvak, met de beperkingen die het hardst knellen.
4. **Wrijvingen melden.** Waar beperkingen elkaar tegenspreken, ontstaat een wrijving. Die gaat naar de keuzelijst, met een voorstel.

Elke oorsprong in `oorsprong.yaml` krijgt daarom de velden `as_venster` (geschat, op de onderliggende as) en `telling` (in welke telling de bron het noemt).

**Het landschap als bewijsstuk.** De kaart van Velmara wordt gelegd op de aarde van de diepe voortijd. De delta van Saelith, de Zoutkust, de bergen van Hoogvrouwe en de Leegte krijgen elk een aannemelijke plek. Wat daarna verdronk of veranderde, wordt de stof van Atlantis- en vloedmythen. Dat is een eigen oplevering (M7), na de mythen zelf.

**Het zwevende gat.** Tussen Midden-aarde en de eerste geschreven mythen ligt een lange periode waarover niemand iets weet (Vansina). Dat is ruimte voor verhalen: de laatste gaven-man, de eerste generatie die het niet meer weet, een stam die een scherf vindt.

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

**Moderne mythen als knipoog.** Ook moderne mythen kunnen uit Velmara komen. Het verhaal dat de goden ruimtevaarders waren (von Däniken), of een sekte-mythe over zielen van een gevallen ruimtevloot die aan mensen kleven, leest als een slecht doorvertelde herinnering aan de landing van de Ysa. Altijd als knipoog, nooit bij naam: een sekte in een verhaal op aarde, die de lezer zelf herkent.

## Opleveringen
| # | Wat | Waar |
|---|---|---|
| M1 | kernset motieven (100–150) | `wereld/mythen/motieven.yaml` |
| M2 | clusters met verspreiding | `wereld/mythen/clusters.yaml` |
| M3 | oorsprongen in Velmara met vervormingsketen | `wereld/mythen/oorsprong.yaml` + 59 voorstellen in de ideeënbank via `r_Z43.py` (gedaan) |
| M4 | vervormingsregels + theorieën (Bartlett, euhemerisme, Propp, Lévi-Strauss, geomythologie) | `wereld/mythen/vervorming.yaml` (later de mythemotor, F-Z4) |
| M4b | mythische wezens: per aards wezen de oorsprong in Velmara en het mechanisme | in `wereld/mythen/oorsprong.yaml` (wezens zijn clusters zoals de andere) |
| M5 | plotplaatsing per boek | `wereld/mythen/plot.md` |
| M6 | mythekaart: per laag welke aardse mythen eruit voortkomen | uitbreiding van de knopenkaart |
| M7 | tijdas met tellingen + geschatte vensters (ABC) + Velmara op de kaart van de diepe voortijd | `wereld/mythen/tijd.yaml`, `wereld/mythen/landschap.yaml` |

## Toetsen
- Elke oorsprong verwijst naar bestaande canonrijen, of is een nieuw voorstel met epistemiek "voorstel". De canon-toets moet groen blijven.
- Elk cluster komt in minstens drie culturen voor, of het is bewust als lokaal gemarkeerd.
- Elke vervormingsketen heeft twee tot vier regels uit stap 4. De aardse mythe moet herkenbaar zijn aan het herkenningsdetail.
- De harde lijnen worden op elke oorsprong getoetst.
- Rogier leest een steekproef van tien en kiest welke canon worden.

## Volgorde
M1 en M2 (verzamelen en clusteren), dan M3 voor de twintig sterkste clusters, dan M4 en M5, dan M6. Daarna de rest van de clusters.
