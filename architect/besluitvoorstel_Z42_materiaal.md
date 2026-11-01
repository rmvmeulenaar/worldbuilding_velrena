# Besluitvoorstel Z42: het materiaal van de Makers en waarom de wereld biologisch werd

Voorgesteld door de architect na het gesprek met Rogier (2 november 2026). **Status: voorstel.** Wordt pas canon met een BESLUIT-rij van Rogier. De romantekst verandert niet.

## De omkering (van Rogier)
Niet een vreemde wereld met een speciale schimmel, maar **een vreemd schip op een gewone wereld**. Velmara is de aarde in haar diepe voortijd. Het schip is gebouwd met de materiaaltechniek van de kolonisten, en die vergaat op aarde.

## Besluit (voorstel)
1. **De materiaaltechniek van de Makers is silicium.**
   - De romp is een legering van aluminium en silicium, met siliciumcomposieten.
   - Rekenen, kernen en geheugen draaien op siliciumkristal.
   - Het hart van het schip (de kern, de Reckoner) is een grijs siliciumkristal dat breekt als glas.
2. **Silicium is op deze wereld opgesloten, niet afwezig.** Het zit overal in zand en steen, maar zuiver silicium maken vraagt een vlamboogoven van rond de 2.000 °C. Daarvoor zijn energie en brandstof nodig, en die zijn er niet: de kernen raken op. De kolonisten kunnen dus geen nieuw schipmateriaal maken.
3. **Gewone schimmel van deze wereld eet het schip.** Voor de kolonisten is het "Velmara fungus". Het is gewone schimmel die de legering en de coatings aantast. De ruimte was steriel, deze wereld niet. De romp vergaat, het siliciumhart blijft.
4. **Daarom kiezen de Makers het lichaam** (ORIGIN-4 blijft): leven herstelt zichzelf, groeit vanzelf en raakt niet op.
5. **Gewoon metaal bestaat, maar niet bij de landing.** In de delta van Saelith is geen erts. Later vinden mensen ijzer in de bergen (Hoogvrouwe, de Dhurn) en in Kharvos. IJzer komt langzaam in de geschiedenis.
6. **Alle magie is techniek van de Makers:** vonkcellen, gaven, het Zegel, de Wieg, de Stemklok. Ze dooft na 801 langzaam uit en wordt mythe. Zegelglas en Sterrensteen zijn scherven van de siliciumkern.
7. **Wat er op de aarde van nu over is:** geen schip, alleen vreemde grijze stenen, de hemelstenen van de mythen.

## Waarom de roman al klopt
De roman blijft letterlijk waar:

| Zin in de roman | Lezing na het besluit |
|---|---|
| h2: *"Velmara fungus, strain 4. Metabolises alloy."* / *"Not oxidation. It eats."* | gewone schimmel van deze wereld eet de aluminium-siliciumlegering |
| h2: *"This is a hull coupon."* | een proefstuk van de romp |
| h2: *"No fissile rock. No easy metal near the surface."* | de delta van de landing heeft geen erts |
| h33: *"A heart of grey stone in a vault of metal"* / *"Grey stone with an edge like broken glass"* | het siliciumkristal |

## Wat er in de canon verandert
| Rij | Nu | Wordt |
|---|---|---|
| ORIGIN-WAAROM-2 (Kern) | "Velmara heeft geen metaal of brandstof"; "een roestschimmel van Velmara vreet scheepsmetaal" | "geen makkelijk metaal en geen brandstof rond de landingsplek; de schimmel van deze wereld eet de legering van het schip" |
| YSA-Z17-6 | "de roestschimmel eet legering" | blijft; toevoegen: gewone schimmel van deze wereld, voor de kolonisten vreemd |
| TECHNO-REGEL-V4 en TECHNO-metaal-* | "onbekend metaal dat niet roest", lichtlansen, torens van naadloos metaal | Makersmateriaal = silicium en composiet; wat eeuwen overleeft, is kristal en glas in droge, afgesloten kluizen |
| TECHNO-zegelsteen | zegelglas en Sterrensteen | scherven van de siliciumkern |
| rijen met ijzer (154) | ijzer overal | elk krijgt een vroegste fase: vanaf de vondst van erts in de bergen; vóór die fase vervangen door been, steen, zegelglas, hout of pees |

## Uitvoering (voor de bouwer, na het besluit)
- Rondescript `r_Z42.py`: BESLUIT-rij, de vervangingen hierboven (oude rijen worden `voorlopig, vervangen` met opvolger), en een indeling van de 154 ijzerrijen in drie groepen: past (fase na de ertsvondst, Kharvos, zeldzaam bezit), ander materiaal, of wrijving.
- Toets groen, roundtrip gelijk, Kern alleen via de BESLUIT-rij.

**Zekerheid van de architect:** ongeveer 85%. De analyse is sterk: de roman blijft waar en er verandert maar één Kern-rij. Het patroongewicht is ook sterk: een vreemd schip op een herkenbare wereld werkt beter dan een vreemde wereld.
