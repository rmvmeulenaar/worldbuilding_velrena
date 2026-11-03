# Z45 · Gebruik, gewone uitvindingen en de weg naar een gewone tijd

**Status: voorstel en simulatie. Niets hiervan is canon.** Rogier beslist via `KEUZE-Z45-*` (`keuzelijst_Z45.md`).

Wat Rogier vroeg (2026-11-02):
- Waar worden de uitvindingen voor gebruikt?
- De techniek moet passen bij het verloop van het verhaal, en niet te raar zijn.
- Na een tijd moet de wereld grofweg naar een gewone tijd groeien.
- Gewone uitvindingen mogen erbij, als ze passen bij de nieuwe.
- Een uitvinding moet een meetbaar effect hebben, problemen oplossen, en het verhaal of de machtsbalans bewegen.
- In de middeleeuwen ging innovatie heel langzaam: kijk wat de patronen zijn.

## Wat er nieuw is

**Gebruik.** Elke knoop zegt nu waar hij voor gebruikt wordt, door wie, waar hij in onze wereld op lijkt, in welk tijdperk hij hoort, en of hij magisch is (`v_tech_gebruik`). Een paar voorbeelden:

| Knoop | Gebruik | Lijkt op |
|---|---|---|
| Spiermolen | de molen van het dorp: een vat gekweekte spier die maalt en pompt, en elke dag graan eet | watermolen, later motor |
| Sporendruk | almanakken, pamfletten en verboden boeken, gedrukt door schimmel op harsvel | blokdruk |
| Lichtnet | spiegeltorens op de heuvels | optische telegraaf |
| Heelkweek | het gasthuis: heelslijm en gekweekte organen | ziekenhuis |

**Gewone uitvindingen, elk met een Velmara-voorganger.** Een vereiste `A|B` betekent A of B, zodat er vaak een Velmara-weg en een Kharvos-weg is.

| Gewone uitvinding | Komt voort uit | Vervangt |
|---|---|---|
| Water- en windmolens | rust | de spiermolen als enige molen |
| Kharvos-ambacht | contact met Kharvos | het idee dat machines van de vijand zijn |
| Uurwerk en kompas | Kharvos-ambacht | de tempelklok als enige maat van de dag |
| Glazen lenzen | steenlens of Kharvos-ambacht | de Sterrensteen als enige lens |
| De drukpers | sporendruk of uurwerk, met lakijzer of Kharvos-ambacht | het laatste woord van de kerk |
| Kruit | Kharvos-ambacht (salpeter uit de oude stallen) | de drager als zekerheid in de oorlog |
| De stoommachine | Kharvos-ambacht en roestlak | de spiermolen: een ketel eet hout, geen graan |
| Spoorweg en stoomschip | stoom | de Leegteworm |
| Elektriciteit | stoom, en lading, lichtcellen of echonet | de lading als enige stroom |
| Telegraaf | elektriciteit en lichtnet | lichtnet en echonet |
| Kiemleer en vaccinatie | lenzen, en heelkweek of kweekakkers | de schimmel als straf |

**Kharvos als brug** (`GESCH4-kharvos`). De Harrow koos voor machines (`BESLUIT-3`, vastgesteld). Het contact met Kharvos groeit met handel en met de dreiging die van Kharvos uitgaat, en het opent het Kharvos-ambacht. Wie die kennis binnenhaalt, heet verrader.

**Correctie op Z44.** `ORIGIN-2` zegt "geen brandstof voor de scheepskernen", niet "geen brandstof". Hout en houtskool bestaan, en in Hoogvrouwe wordt zilver gewonnen. Stoom en kruit zijn dus niet onmogelijk, alleen laat. Ze staan nu op `vervangen`, met verwijzing naar `TN-stoom` en `TN-kruit`. Of er steenkool is, zegt de canon niet. Dat is `KEUZE-Z45-kolen`.

## Het patroon van echte geschiedenis

- **Kennis** (`GESCH4-kennis`). De kans op een uitvinding stijgt met de kennisvoorraad tot de derde macht. Die voorraad groeit met steden, handel en schrift, versnelt met sporendruk en drukpers, en slinkt in oorlog en epidemie. Dit volgt Kremer en Mokyr: hoe meer mensen bewaren en delen, hoe sneller het gaat. Na een instorting gaat het weer langzaam, zoals na Rome.
- **S-curve** (`GESCH4-verspreiding`). Een uitvinding verspreidt zich langzaam, en haar effect groeit mee met het gebruik. Vroeg duurt dat ongeveer 280 jaar, laat ongeveer 140, omdat drukwerk, netten en handel versnellen.
- **Verval** (`GESCH4-verval`). Gave- en zegelsteentechniek gaat verloren als haar bron 100 jaar wegvalt. De kennis blijft, het gebruik verdwijnt, en haar gewone opvolger wordt nodig. Verwondering zit in verlies.

Uitkomsten (1000 runs, dezelfde seeds als Z42 tot Z44):

| Periode | Grote uitvindingen per eeuw |
|---|---|
| 801 tot 1500 | 0,27 (zoals de vroege middeleeuwen) |
| 1500 tot 2500 | 0,48 |
| 2500 tot 3500 | 0,98 (na drukwerk en netten) |
| 3500 tot 5000 | 0,42 (de boom raakt op) |

- **Het Gewone** (stoom, drukpers, elektriciteit, vaccin en spoor elk voor de helft verspreid): in **836 van de 1000** geschiedenissen, gemiddeld rond **3661**. De rest blijft hangen in een tijd van werkplaatsen of kronen. Dat zijn geschiedenissen waarin het niet lukt, ook dat is een verhaal.
- **Effect** (gemeten in 200 runs):
  - 99% van de uitvindingen heeft een meetbaar gevolg
  - bij 84% krijgt de uitvinder meer macht
  - als het probleem echt speelde, is het 100 jaar later in 63% van de gevallen kleiner
  - 25% van de latere crises erft van een uitvinding

## Toets

- **Regels:** 48, met 0 nieuwe fouten. De roundtrip is gelijk, ook met de nieuwe kolommen, en een tweede run voegt niets toe.
- **Nieuwe regels:**
  - `R-tech_gebruik`: elke knoop heeft gebruik, gebruiker, aards equivalent, tijdperk en soort
  - `R-sim_effect`: elke uitvinding heeft een meetbaar gevolg en een meting van haar probleem
  - `R-sim_convergentie` (signaal): minder dan 80% van de geschiedenissen bereikt Het Gewone
- **Aangepaste regel:** `R-tech_boom` kent nu `A|B`.
- **Negatieve test:** drie fouten die ik expres aanbracht, werden alle drie gevonden, en het signaal over Het Gewone ging af.

## Lezen

```sql
select * from v_tech_gebruik;                                             -- wat is het, wie gebruikt het, waar lijkt het op
select jaar, knoop, uitvinder, noodzaak, probleem, druk_voor, druk_na, verspreid_jaar, verloren
  from sim_uitvinding where run_id='Z45-GESCH-0003' order by jaar;        -- hoe de techniek van run 3 groeit
select json_extract(scores,'$.gewoon'), json_extract(scores,'$.per_eeuw') from sim_run where module='geschiedenis_z45';
```

## Zwaktes die nog open zijn

1. **Een knoop staat voor een hele generatie techniek.** "Stoom" is één stap, waar het in werkelijkheid tientallen uitvindingen waren. Daardoor ligt het aantal per eeuw lager dan in echte geschiedenis. Het patroon klopt, de schaal is grover.
2. **Geen regio's.** Verspreiding gebeurt in heel Velmara tegelijk, niet van stad naar stad.
3. **Het Gewone eindigt rond onze negentiende eeuw.** Wat daarna komt (motoren, radio, de vondst van het schip als wetenschap) is een volgende laag.
4. **Gebouwd en getoetst door dezelfde architect.** Laat de nakijker blok H uit `z42/NAKIJKVRAGEN.md` op Z45 draaien.
