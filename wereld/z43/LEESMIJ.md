# Z43 · De geschiedenis verklaart zichzelf

**Status: simulatie en aanname. Niets hiervan is canon.** Rogier beslist via `KEUZE-Z43-*` (`keuzelijst_Z43.md`).

Z43 is de reactie op review 1 van Z42 (`z42/REVIEW_1.md`), samengevat: niet meer geschiedenis maken, maar zorgen dat de geschiedenis zichzelf kan verklaren. De motor (`z43/geschiedenis.py`) bouwt op die van Z42: dezelfde toestand, gebeurtenissen en noodoplossingen. Hij draait met dezelfde seeds (420001 tot 421000), zodat je elke run van Z42 kunt vergelijken met dezelfde run in Z43.

## Wat er nieuw is

| Vraag van de nakijker | Antwoord in Z43 |
|---|---|
| Waarom kan het artsengilde een wet maken? | Een oplossing kan alleen gekozen worden als de beslisser minstens 10% van de macht heeft. Bij het artsengilde staat nu dat de stad het gilde het alleenrecht geeft. Heeft niemand genoeg macht, dan blijft de crisis onopgelost (`gesch_onopgelost`). |
| Elke crisis een toestand, actor, mechanisme en gevolg | `sim_fase` heeft daarvoor eigen velden: `oorzaak`, `druk`, `tweede_druk`, `beslisser`, `actor_macht`, `mechanisme`, `handhaver`, `erft_van` en `gevolg`. |
| "5 van 5 assen" is geen rijm | Een fase moet minstens één mechanisme delen met een eerdere fase, ook met de fasen tot 801. Daarnaast moet ze op minstens 3 assen verschillen; 3 of 4 krijgt voorrang. Zie `gedeeld_mechanisme`, `rijmt_met` en `assen_anders`. |
| Een wet heeft een wetgever met macht, gebied, handhaver en verval nodig | `sim_wet`. Een wet vervalt door opheffing, door een voorwaarde (de verhouding), of doordat haar wetgever 60 jaar geen macht meer heeft. Na 200 jaar is een wet gewoonte en vervalt ze alleen nog door opheffing. |
| Bloed, aanspraak en gezag scheiden | `sim_huis`: `ouder` (bloed), `aanspraak` (lading, zwaard, geld, bloed) en `gezag_van`/`gezag_tot`. |
| Waarheidslabel bij de versies van 801 | `gesch_versie801`: het label staat in `doel`: waar, deels waar, vervalst, mythe, kinderrijm of vergeten. |
| Rust is niet hetzelfde als stilstand | `gesch_rust` beschrijft per laag: politiek, economie, samenleving en magie. |

Drie aannames die bij het bouwen nodig bleken (`KEUZE-Z43-standen`):
- Zonder ze groeide het aantal edelen onbegrensd.
- Zonder ze sloot de wereld zich eindeloos af.
- Zonder ze werden de steden nooit sterk.

De oplossing: edelen zakken ook weer af, de steden groeien met techniek en handel, en de kerk groeit en krimpt met het geloof.

## Toetsregels (in `regel`, draaien bij elke `velmara.py toets`)

- `R-sim_oorzaak`: elke fase heeft een oorzaak, erfenis, gevolg en een beslisser met minstens 10% macht.
- `R-sim_rijm`: elke fase deelt een mechanisme met een eerdere fase en verschilt op minstens 3 assen.
- `R-sim_wetgever`: elke wet heeft een wetgever met minstens 10% macht, een rechtsgebied en een handhaver. Een vervallen wet zegt waardoor.
- `R-sim_huis`: elk huis na 801 heeft een ouder; elk heersend huis heeft een aanspraak.

Bewezen dat ze werken: drie expres aangebrachte fouten in een kopie van de database werden alle drie gevonden.

## Lezen

```sql
-- de keten van run 3: wat gebeurde, waarom, door wie, met welk gevolg
select * from v_sim_keten where run_id='Z43-GESCH-0003';
-- de wetten, met hoe lang ze golden en waardoor ze vervielen
select * from v_sim_wetboek where run_id='Z43-GESCH-0003';
-- bloed, aanspraak en gezag van de huizen
select * from v_sim_stamboom where run_id='Z43-GESCH-0003';
-- crises waarin niemand kon ingrijpen
select jaar, doel, detail from sim_gebeurtenis where run_id='Z43-GESCH-0003' and type_code='gesch_onopgelost';
-- dezelfde seed in Z42 en Z43 naast elkaar
select module, scores from sim_run where seed=420003;
```

## Uitkomsten (1000 runs)

| Meting | Z43 | Z42 |
|---|---|---|
| fasen per geschiedenis | 11 (4 tot 21) | 20 |
| crises die niemand kon oplossen | 7 (2 tot 19) | niet gemeten |
| fasen die rijmen met een fase van vóór 801 | 3 per run | niet gemeten |
| assen anders (3 / 4 / 5) | 2606 / 5159 / 3417 | vooral 5 |
| wetten per geschiedenis | 16 | 19 |
| rustige jaren | 1780 | 2620 |
| laagste magie | 0,12 tot 0,39 (nooit nul) | 0,34 |

Z43 heeft minder fasen, omdat een fase nu een beslisser met macht én een rijm nodig heeft. Wat daar niet aan voldoet, is in Z43 een crisis waarin niemand kon ingrijpen.

## Zwaktes die nog open zijn

1. **Wetten als gewoonte overleven hun reden.** `W-zegelplicht` blijft gelden als het kleine zegel allang gedoofd is. Een wet zou moeten vervallen als haar onderwerp verdwijnt.
2. **De machtsverdeling is grof:** acht partijen, geen regio's. Een wet geldt "in Velmara" of "in de steden", niet per dorp. De leefwereld die een schrijver in jaar 1400 nodig heeft (prijzen, taal, reizen, recht per dorp) zit er nog niet in.
3. **Het gevolg wordt gemeten, niet verklaard.** Het verschil na 60 jaar is zichtbaar, maar niet welk deel van dat verschil van de fase zelf komt.
4. **De uitvindingen zijn nog de lijst uit Z42.** De technologieboom is de volgende stap.
5. **Z43 is gebouwd en getoetst door dezelfde architect.** De nakijker hoort blok G uit `z42/NAKIJKVRAGEN.md` te draaien, op Z42 als nulmeting en op Z43 als vergelijking.
