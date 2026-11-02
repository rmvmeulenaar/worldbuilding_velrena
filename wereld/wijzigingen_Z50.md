# Ronde Z50: personen na 801, een verhaal voor elke fantasie, de catalogus zonder sjablonen

Opdracht van Rogier (2 november 2026): "kan je dat gewoon maken". Uitgevoerd met vier schrijvers tegelijk. Hun werk staat in `z50/`, en `r_Z50.py` heeft het getoetst en ingelezen.

## Bewijs
| Meting | Voor | Na | Gehaald |
|---|---|---|---|
| fantasieën in een sjabloonfamilie (`herhaling.families`, min 3) | 144 | 3 | ja (de rest hangt aan Kern, zie keuzelijst) |
| bijna-kopieën onder fantasieën (Jaccard ≥ 0,5) | 91 | 0 | ja |
| fantasieën die in een verhaal of pad voorkomen | 70 van 199 | 196 van 198 | ja |
| personen na 801 | 0 | 91 | ja |
| paden na 801 met een persoon als drager | 0 van 18 | 109 van 109 | ja |
| toets: nieuwe fouten / roundtrip | 0 / gelijk | 0 / gelijk | ja |

## Wat er gebeurde
- **Catalogus.** 140 rijen hebben een opvolger `<code>-Z50` gekregen: dezelfde inhoud, codes en harde lijnen, maar in een eigen vorm vanuit hun volk en plek. 1048 verwijzingen in niet-Kern-rijen en 57 in verhaalpaden wijzen nu naar de opvolger. Vier rijen bleven staan omdat Kern-rijen (Liora en Aeron) erop leunen: VOOR-teder, VOOR-overgave, VOOR-onderdanige-man en VOOR-vrouwenliefde.
- **Personen.** Er zijn 91 personen bijgekomen, `PER-Z50-*`, verspreid over de tijdperken 9 tot 16. Het zijn voorstellen in de ideeënbank. Elk heeft een afkomst (huis, volk of lijn), wil, geheim en prijs, en links naar andere verhaallijnen. Ongeveer 40% is hoofdpersoon in twee paden, zodat de lijnen elkaar kruisen. Niemand stamt af van Liora, Teo, Aeron of Ithrael.
- **Verhaalpaden.** Er zijn 91 nieuwe paden in `verhaal_profiel` (22 in fase 9, 19 in fase 10, 15 in fase 11, 9 in fase 12, 12 in fase 13, 11 in fase 14, 9 in fase 15 en 12 in fase 16). Binnen elk tijdperk verschillen alle paden op minstens 3 van de 7 assen. De premissen delen hoogstens 10% van hun woordreeksen. De harde lijnen zijn getoetst. In `drager` staat nu de persoon, net als in de oudere paden; de DRAGER-rij staat in de kerncodes. De 18 paden van Z49 hebben er ook een persoon bij gekregen.
