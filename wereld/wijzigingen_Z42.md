# Ronde Z42: de geschiedenismotor na 801

Gebouwd door de architect op verzoek van Rogier (2026-11-02). Script: `r_Z42.py` (idempotent: een tweede run voegt niets toe). Motor: `z42/geschiedenis.py`. Uitleg voor wie het nakijkt: `z42/LEESMIJ.md`. Open beslissingen: `keuzelijst_Z42.md`.

## Wat erbij kwam

Alleen in bestaande tabellen. Geen nieuwe tabel, geen canonrij gewijzigd of verwijderd, roman en Kern niet aangeraakt.

| tabel | rijen erbij | wat |
|---|---|---|
| sim_regel | 17 | de regels van de motor, `GESCH-*`, elk met bron in de canon en `aanname=1` |
| tech_gebeurtenistype | 19 | soorten gebeurtenissen, `gesch_*` |
| sim_run | 1000 | `Z42-GESCH-0001` tot `-1000`, seed 420001 tot 421000, samenvatting in `scores` |
| sim_gebeurtenis | 1142 | alle details van de zes gekozen runs: fasen, gebeurtenissen, wetten in en uit, huizen, rustige tijden, toestand per eeuw, verhaal van 801, wezens |
| keuze | 8 | `KEUZE-Z42-*`: zes over de motor, twee wrijvingen in de bestaande canon |
| logboek | 1 | |

## Controles

| meting | voor Z42 | na Z42 |
|---|---|---|
| toets: nieuwe fouten | 0 | 0 |
| toets: bekende fouten | 91 | 91 |
| toets: signalen | 1734 | 1734 |
| roundtrip | gelijk | gelijk |
| tweede run van r_Z42.py | | 0 rijen erbij |

## Wat de motor oplevert (1000 runs)

20 fasen per run (11 tot 39). Magie nooit onder 0,34, gemiddeld 12 golven. Tijd van de machines vanaf gemiddeld 3381. Gemiddeld 2620 rustige jaren. 3 heersende huizen, 14 wetten in, 5 uit. Het verhaal van 801 is aan het eind nog 29% trouw.

## Opmerking over canon_tekst

`velmara.py tekst` knipt grote hoofdstukken bij 3 MB. Omdat de simulatietabellen groeiden, verschuiven de nummers van de bestanden vanaf `061`. Git ziet dat als verwijderen en toevoegen; `velmara.py check` bevestigt dat de tekst samen exact gelijk is aan `WERELD_VELMARA.md`.
