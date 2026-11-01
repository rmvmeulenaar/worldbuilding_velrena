# Scorekaart Z40 (2026-11-01)

**Gebouwd door de architect**, omdat de bouwer geen credits had. Dat betekent dat Z40 niet onafhankelijk is gekeurd: laat de andere LLM Z40 toetsen (KEUZE-Z40-onafhankelijk).

**Basis:** `canon_backup_Z40.db` (= `canon_na_Z39.db`). Resultaat: `canon.db` (= `canon_na_Z40.db`).

## Controles

- `toets.py` groen na elke stap: 39 regels, 0 nieuwe fouten. Nieuwe regel: R-simulatie_in_canon.
- Roundtrip: 52 tabellen, 0 verschillen, views gelijk.
- Idempotent: een tweede run voegt niets toe.
- Schone herbouw vanaf de backup: deterministisch via seeds. Gedraaid en gebruikt als eindversie.
- Kern: 0 rijen gewijzigd, 0 verwijderd, 0 nieuw.
- Z39 reproduceerbaar: de Z39-seeds 390203, 390000 en 390731 geven met de nieuwe `sim.py` exact dezelfde gebeurtenissen. De nieuwe opties staan standaard uit.
- Koude lezer (`z39/koude_lezer.py`): 10/10.
- Steekproef van 183 rijen (BESLUIT-Z40-7), gelaagd: alle 16 nieuwe canonrijen, 3 bogen en 16 regels, plus 148 willekeurige simulatierijen.
  - Uitslag: 183 goed, 0 fout. De 95%-bovengrens van het foutpercentage is 1,6% (Clopper-Pearson), dus de ronde slaagt.
  - Canonrijen, bogen en regels heeft de architect daarnaast zelf gelezen.
  - Kanttekening: in een eerdere versie van de steekproef faalden 4 rijen. Dat kwam door een fout in de keurfunctie zelf (verwijzingen naar `personage_profiel:` werden niet herkend). De keurfunctie is hersteld, niet de rijen.

## A. Herstel en besluiten

- **IDEE-Z39-1..10 staan weer in de ideeënbank.**
  - Oorzaak van de fout: `afgeleid.py` rekende `ideeenbank` opnieuw uit op basis van het codevoorvoegsel, en IDEE- stond niet in die lijst.
  - Oplossing: regel 7 in `afgeleid.py` (epistemiek 'simulatie' → ideeënbank, tenzij `draagkracht_handmatig` gezet is), en de toets R-simulatie_in_canon.
- **IDEE-Z39-4, -6 en -7 zijn bogen geworden** (BESLUIT-Z40-5): VERHAAL-fase4-d/e/f-Z40, met rijen in `boog`. De maltests en rijmtests zijn groen.
- **De scorekaart van Z39 is hersteld:** "De kennis van de Makers is in 89.2% van de runs in 130 jaar in alle regio's vergeten."
- **8 besluiten vastgelegd** (BESLUIT-Z40-1..8).

## B. Rem (schriftverbod) en registerbereik — 1.000 runs, fase 4

Geldig: 1.000 van 1.000. De nieuwe opties in `sim.py` (`rem`, `bereik`) staan alleen aan in Z40-runs.

| canongebeurtenis | canon | Z39 (zonder rem) | Z40 (rem, 20 jaar per leerling) |
|---|---|---|---|
| eerste register | 22 | 20 | 20 |
| Deelwet | 40 | 29 | 29 |
| rooster (rotatie) | 78 | 51 | **55** |
| Orde | 90 | 60 | **62** |
| nevenramp in Groenmuil | 33–38 | 2% van de runs | **19,5%** van de runs, mediaan jaar 36 |
| stemming 7–5 (jaar -3) | 7–5 | meest voorkomend | meest voorkomend (24,7%) |

**Gevoeligheid voor de leertijd** (jaren per leerling, 200 runs per waarde):

| leertijd | rooster (mediaan) | Orde (mediaan) | nevenramp |
|---|---|---|---|
| 15 jaar | 52 | 60 | 8% |
| 20 jaar (basis) | 55 | 62 | 19,5% |
| 25 jaar | 68,5 | 71 | 29,5% |
| **30 jaar** | **80** (canon 78) | **82** (canon 90) | 41% |

**Bevinding:** het schriftverbod alleen verklaart de tijdlijn van de canon als een schrijfster ongeveer één leerling per loopbaan opleidt (30 jaar). Dat is niet bijgesteld tot het paste: het is een gevoeligheidsanalyse, en de keuze ligt bij Rogier (KEUZE-Z40-rem).

**Nieuw:** het model maakt ook een inteeltramp in Hoogvrouwe (in de gekozen run Z40-F4R-0931, jaar 42). Die staat niet in de canon: zie IDEE- en keuzelijst.

## C. Fase-overgang — 50 runs, fase 5 (130–340)

- Begint met de eindtoestand van run Z40-F4R-0931: Deelwet, register, rooster, Orde en eilanden zijn er al, met het registerbereik, de bevolking en de schrijfsters.
- Geldig: 50 van 50. Deelwet of register opnieuw ingesteld: **0 runs** (in Z39 ontstonden ze in fase 5 opnieuw).

## D. Module ziekte: de Pest van 340 — 1.000 runs

**Model:** stochastisch SEIR per regio, alleen mannen, per maand, jaar 330–350. De koorts begint in de afgesloten stallen van Hal-Neth en verspreidt zich langs de rotatiekringen en de karavaanroute naar Qesh.
- De sterfte onder zieken (0,35) is **geijkt** op "een derde van de mannen" (GEB-pest-340).
- De andere uitkomsten zijn **niet** geijkt, maar getoetst.

| toets | uitkomst |
|---|---|
| koorts ontstaat in Hal-Neth | 94,9% van de runs |
| koorts ontsnapt uit de afgesloten stallen | **40,5%** van de runs (anders blijft het bij Hal-Neth) |
| bij ontsnapping: sterfte onder mannen | mediaan **30,7%**; een derde (25–42%) in 99,5% van de runs |
| bij ontsnapping: jaren tussen eerste koorts en piek | **2** (canon: 338 → 340) |
| bij ontsnapping: Qesh minder dan half zo zwaar getroffen | 74,6% van de runs |
| Qesh-sterfte bij ontsnapping, met sluiting / zonder sluiting | **0% / 35%** |
| indexjaar (mediaan) | 336, 2 jaar vroeger dan de canon |

**Gevoeligheid voor de sterfte onder zieken:** bij 0,3 overlijdt 26,7% (een derde in 97,5% van de runs); bij 0,5 overlijdt 44,1% (een derde in 2,5%).

**Gekozen run Z40-ZIEKTE-0271:**
- de koorts begint in Hal-Neth in jaar 338, maand 6;
- ze bereikt Saelith in 338, maand 12;
- Qesh sluit in 339, maand 1;
- de piek valt in 340;
- 30,6% van de mannen sterft, 0% in Qesh.

**Bevindingen:**
1. De canon klopt als de stallen echt afgesloten waren en de koorts één keer ontsnapte.
2. Qesh ontsnapt alleen als het sluit op het eerste gerucht, nog voor er buiten Hal-Neth mannen sterven.

## E. Nieuwe premisses (ideeënbank)

IDEE-Z40-1..5 zijn met de hand geschreven uit de gebeurtenissen van Z40-ZIEKTE-0271 en Z40-F4R-0931. Ze hebben epistemiek 'simulatie' en staan in de ideeënbank.

## Bestanden

- `r_Z40.py`: de runner (stappen a, rem, overgang, ziekte, ideeen, proef, keuze).
- `z40/ziekte.py`: de ziektemodule.
- `z39/sim.py`: opties `rem`, `bereik`, `begin`, en `eindtoestand()`.
- `afgeleid.py`: regel 7.
- `toets.py`: `py_simulatie_in_canon`; `py_epistemiek` accepteert ook Z40-run-id's.
- Uitvoer: `z40/mc_fase4_rem.json`, `z40/eind_fase4.json`, `z40/overgang_fase5.json`, `z40/ziekte.json`.
- Backups: `*_backup_Z40.py`.
