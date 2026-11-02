# Z42 · De geschiedenismotor na 801

**Status: simulatie en aanname. Niets hiervan is canon.** Lees ook `REVIEW_1.md` (eerste nakijkronde en wat daarop is aangepast) en `NAKIJKVRAGEN.md` (de opdracht voor een nakijker). Rogier beslist via de open keuzes `KEUZE-Z42-*` (tabel `keuze`, en `keuzelijst_Z42.md`). Pas een BESLUIT-rij van Rogier zet iets in de canon.

## Waarom dit bestaat

Alles wat er tot Z41 in de canon staat, loopt tot 801. In 801 verandert één ding blijvend: het Zegel kan niet meer ja zeggen namens een lichaam (`BESLUIT-Z36-4`). Rogier wil weten wat er daarna gebeurt: hoe de samenleving verandert, hoe wetten komen en gaan, welke huizen heersen, hoe wezens ontstaan en sprookje worden, hoe het verhaal van 801 verbastert, en dat de magie golft maar nooit verdwijnt.

`fase_rijm` kan dat niet beantwoorden. Het is een toets: het controleert of een fase rijmt met de vorige, maar maakt zelf geen fasen. Deze motor maakt ze wel, uit regels die al in de canon staan, en legt de toets van `fase_rijm` (minstens 3 van 5 assen anders) op elke nieuwe fase.

## Hoe je het opnieuw maakt

Vanuit `wereld/`:

```
python3 velmara.py bouw          # canon.db uit canon_tekst/
python3 r_Z42.py                 # idempotent: een tweede keer voegt niets toe
python3 velmara.py tekst
python3 velmara.py toets         # 0 nieuwe fouten, roundtrip gelijk
python3 z42/geschiedenis.py 420003   # één run op het scherm (seed 420000 + runnummer)
```

Dezelfde seed geeft altijd dezelfde geschiedenis.

## De motor in één alinea

Stap = 20 jaar, van 801 tot 5000. Elke stap veranderen bevolking, voedsel, edelen, kas, buren, techniek, geloof, openheid, de verhouding jongens/meisjes en de magie. Dan vallen er toevallige gebeurtenissen (vondsten, schimmeljaren, een koude eeuw). Daarna wordt per soort crisis de druk berekend. Passeert de grootste druk de drempel, dan kiest de motor een noodoplossing uit een lijst van ongeveer 40, met de eis dat ze op minstens 3 van 5 assen (beslisser, betaler, vervalst, ontdekt, schaal) verschilt van de vorige fase. Elke noodoplossing heeft een prijs, een blijvende verandering, en vaak een wet die ingaat of vervalt.

## De regels (`sim_regel`, module `geschiedenis`, codes `GESCH-*`)

| Code | Wat | Bron in de canon |
|---|---|---|
| GESCH-filter | Na 801 verslapt de X-filter; jongens schuiven naar de helft, dragers blijven schaars | ORIGIN-10-Z36, BESLUIT-Z36-4 |
| GESCH-bodem | Magie heeft een bodem: Orrim verstenen tot groeve, Sterrensteen groeit in hen | D1-orrim-dood, VOLK-orrim, D1-orrim-geld |
| GESCH-golf | Gesloten dragerlijnen concentreren lading; open tijden verdunnen haar | ORIGIN-10-Z36, GAVE-Z37-ja |
| GESCH-piek | Vondsten laten de magie kort oplaaien | YSA-Z21-3, ORIGIN-Z1-harrow, ORIGIN-8 |
| GESCH-verdunning | Over eeuwen wordt de golf kleiner, nooit nul | BESLUIT-2, BESLUIT-Z36-4 |
| GESCH-bevolking | Bevolking groeit tot het voedsel op is | FASE-overvloed |
| GESCH-elite | Te veel edelen en een lege kas geven strijd | FASE-markt |
| GESCH-staat | Kas onder 0,12 is bankroet | FASE-barsten |
| GESCH-buren | Kharvos wordt hongeriger en valt aan als het sterker is | REG-kharvos-B1, ORIGIN-Z1-harrow |
| GESCH-techniek | Techniek groeit in rust en openheid, trager waar magie werkt | ORIGIN-4, ORIGIN-2 |
| GESCH-geloof | Geloof groeit met de kerk, slijt met techniek | REGEL-seksuele-normen |
| GESCH-verhaal801 | Het verhaal van 801 verbastert; heilige of heks naar wie vertelt | BESLUIT-Z36-4, BESLUIT-Z18b-2, VOLK-aelthir-V5 |
| GESCH-wezens | Lading in wie haar niet draagt maakt nachtvlerken; lijnen gaan van slachtoffer tot sprookje | ORIGIN-WAAROM-9, NAV-wormwording-B1, BESLUIT-Z6-WRIJ-065 |
| GESCH-rijm | Minstens 3 van 5 assen anders dan de vorige fase | (R-rijm_assen) |
| GESCH-spiraal | Een oplossing pas na 600 jaar opnieuw; sommige maar één keer | (R-rijm_spiraal) |
| GESCH-rust | 200 jaar zonder crisis is een rustige tijd | |
| GESCH-wetten | Deelwet vervalt boven 12% jongens, mannen krijgen bezit boven 25%, gelijk erfrecht boven 40% | WET-deelwet-recht, WET-wie-gewone-man, WET-erfrecht |

De exacte formules staan in `z42/geschiedenis.py`. Alle getallen zijn aannames (`aanname=1`), niet geijkt.

## Wat er in de database staat

- `sim_run`, module `geschiedenis`: 1000 runs, `Z42-GESCH-0001` tot `Z42-GESCH-1000`, seed 420001 tot 421000. Kolom `scores` (JSON): aantal fasen, magie min/max/eind, aantal golven, wanneer de tijd van de machines begint, langste stilte, rustige jaren, aantal heersende huizen, wetten in en uit, hoe trouw 801 aan het eind verteld wordt, en de getrokken parameters.
- `sim_gebeurtenis`, module `geschiedenis`: alle details van de zes gekozen runs (`gekozen=1`: 0001, 0002, 0003, 0005, 0008, 0013). Soorten (`tech_gebeurtenistype`, codes `gesch_*`):
  - `gesch_crisis_*`: een fase. `actor` = wie beslist, `doel` = wie betaalt, `detail` = naam, wat verzwegen wordt, of het ontdekt wordt, schaal, blijvende verandering, tijd, heersend huis, rijm.
  - `gesch_gebeurtenis`: een toevallige gebeurtenis, met `canon_code` waar die bestaat.
  - `gesch_wet_in` en `gesch_wet_uit`: `doel` = de wet (WET-/RECHT-codes uit de canon, of W-codes die de motor invoert), `actor` = wie haar maakte of afschafte.
  - `gesch_huis`: een huis ontstaat (`doel` = ouderhuis), gaat heersen, of valt. Zo is de stamboom van de huizen te volgen.
  - `gesch_rust`: een rustige tijd met de genres die erbij passen.
  - `gesch_toestand`: per eeuw de hele toestand als JSON (magie, bodem, techniek, aandeel jongens, honger, kas, edelen, geloof, openheid, Orrim, beschaving, tijd, heerser, aantal wetten, machtsverdeling).
  - `gesch_versie801`: vanaf welk jaar het verhaal van 801 anders verteld wordt, en hoe.
  - `gesch_wezen`: een wezenlijn schuift een stadium op (slachtoffer, groep, volk, monster, sprookje), met `canon_code` naar de bron van die lijn.
- `keuze`: negen open keuzes `KEUZE-Z42-*` (de negende, `KEUZE-Z42-bodem-bron`, komt uit review 1).
- `logboek`: één regel voor Z42.

In de tekst staat dit in `canon_tekst/057_sim-regel.md`, `059_tech-gebeurtenistype.md`, `060_sim-run.md`, `062_sim-gebeurtenis.md` (en de vervolgdelen) en `042_keuze.md`.

## Een run lezen

```sql
-- het hele verloop van run 3, in volgorde
select jaar, type_code, actor, doel, detail from sim_gebeurtenis
 where run_id='Z42-GESCH-0003' and type_code not in ('gesch_toestand') order by jaar, id;

-- alleen de fasen
select jaar, substr(type_code,14) crisis, actor beslist, doel betaalt, detail from sim_gebeurtenis
 where run_id='Z42-GESCH-0003' and type_code like 'gesch_crisis_%' order by jaar;

-- welke wetten golden wanneer
select jaar, type_code, doel wet, detail, actor door from sim_gebeurtenis
 where run_id='Z42-GESCH-0003' and type_code like 'gesch_wet_%' order by jaar;

-- de stamboom van de huizen
select jaar, detail, actor huis, doel ouder from sim_gebeurtenis
 where run_id='Z42-GESCH-0003' and type_code='gesch_huis' order by jaar;

-- hoe 801 verteld wordt
select jaar, detail from sim_gebeurtenis where run_id='Z42-GESCH-0003' and type_code='gesch_versie801' order by jaar;

-- over alle 1000 runs
select json_extract(scores,'$.fasen'), json_extract(scores,'$.magie_min'), json_extract(scores,'$.golven')
  from sim_run where module='geschiedenis';
```

## Wat de 1000 runs laten zien

- Gemiddeld 20 fasen tussen 801 en 5000 (van 11 tot 39).
- De magie zakt nooit onder 0,34 (begin 0,8) en golft gemiddeld 12 keer.
- De tijd van de machines begint gemiddeld rond 3381 (tussen 2001 en 4501).
- Gemiddeld 2620 jaar van de ruim 4200 is rustige tijd. Dat is bewust: rust hoort bij geschiedenis (`KEUZE-Z42-rust`).
- Gemiddeld 3 heersende huizen, 6 huizen in totaal, 14 wetten die ingaan en 5 die vervallen.
- Aan het eind is het verhaal van 801 gemiddeld nog voor 29% trouw.

## Wat een nakijker moet weten (zwaktes, eerlijk)

1. **De getallen zijn aannames.** Niets is geijkt op de fasen tot 801. Een volgende stap is de motor ook vanaf −600 te draaien en te zien of hij iets oplevert dat op de zeven bestaande fasen lijkt.
2. **De lijst noodoplossingen is met de hand geschreven** (ongeveer 40). Daardoor komt een oplossing na 600 jaar terug, gemarkeerd als "keert terug". Oplossingen uit de assen laten opbouwen is de volgende verbetering.
3. **Huisnamen worden gemaakt als "ouderhuis van plaats".** Ze zijn plaatshouders, geen canonnamen.
4. **De motor kent geen personen.** Stambomen van mensen zitten in de personensimulatie (`z41/personen.py`, tabellen `sim_figuur`, `per_relatie`). Die twee koppelen is nog niet gedaan.
5. **De motor maakt geen seksuele inhoud.** Hij beschrijft instellingen, wetten en wezens. De harde lijnen uit `CLAUDE.md` blijven gelden voor alles wat er later uit geschreven wordt.
6. **Twee bestaande wrijvingen gevonden** en als keuze vastgelegd: wanneer de instemmingssleutel brak (`KEUZE-Z42-sleutelbreuk`) en of Ves-Anath in 603 of 610 werd ontruimd (`KEUZE-Z42-vesanath`).

## Toets

Vóór Z42 en na Z42: 39 regels, 0 nieuwe fouten, dezelfde 91 bekende fouten en dezelfde 1734 signalen. Roundtrip gelijk. Bestaande canonrijen zijn niet gewijzigd.
