# Ronde Z43: de geschiedenis verklaart zichzelf

Gebouwd door de architect op verzoek van Rogier (2026-11-02), na review 1 van Z42. Script: `r_Z43.py` (idempotent). Motor: `z43/geschiedenis.py`. Uitleg: `z43/LEESMIJ.md`. Open beslissingen: `keuzelijst_Z43.md`.

## Wat erbij kwam

| wat | aantal | |
|---|---|---|
| migratie `010_z43_keten.py` | 3 tabellen, 3 views | `sim_fase`, `sim_wet`, `sim_huis`; `v_sim_keten`, `v_sim_wetboek`, `v_sim_stamboom` |
| regel | 4 | `R-sim_oorzaak`, `R-sim_rijm`, `R-sim_wetgever`, `R-sim_huis` (niveau fout) |
| sim_regel | 7 | `GESCH2-*` |
| tech_gebeurtenistype | 1 | `gesch_onopgelost` |
| sim_run | 1000 | `Z43-GESCH-0001` tot `-1000`, dezelfde seeds als Z42 |
| sim_fase / sim_wet / sim_huis | 70 / 98 / 30 | de zes gekozen runs |
| sim_gebeurtenis | 853 | gebeurtenissen, onopgeloste crises, rust, toestand, 801 met waarheidslabel, wezens |
| keuze | 4 | `KEUZE-Z43-*` |
| logboek | 1 | |

Om de nieuwe tabellen in de tekst mee te nemen: `importeer.py` draait nu ook migraties `01x`, en `importeer.py` en `genereer.py` kennen de drie tabellen. Geen canonrij gewijzigd of verwijderd; roman en Kern niet aangeraakt.

## Controles

| meting | voor | na |
|---|---|---|
| toetsregels | 39 | 43 |
| nieuwe fouten | 0 | 0 |
| signalen | 1734 | 1734 |
| roundtrip (ook `sim_fase`, `sim_wet`, `sim_huis`) | gelijk | gelijk |
| tweede run van `r_Z43.py` | | 0 rijen erbij |
| drie expres aangebrachte fouten in een kopie | | alle drie gevonden door de nieuwe regels |
