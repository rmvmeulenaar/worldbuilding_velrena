# Ronde Z44: de technologieboom van Velmara

Gebouwd door de architect op verzoek van Rogier (2026-11-02). Script: `r_Z44.py` (idempotent). Boom: `z44/boom.py`. Motor: `z44/geschiedenis.py`. Uitleg: `z44/LEESMIJ.md`. Open beslissingen: `keuzelijst_Z44.md`.

## Wat erbij kwam

| wat | aantal | |
|---|---|---|
| migratie `011_z44_boom.py` | 2 tabellen, 2 views | `tech_knoop`, `sim_uitvinding`; `v_tech_boom`, `v_sim_uitvinding` |
| regel | 2 | `R-tech_boom`, `R-sim_uitvinding` (niveau fout) |
| tech_knoop | 24 | 17 mogelijke knopen, 7 onmogelijke of onnodige technieken met reden |
| sim_regel | 5 | `GESCH3-*` |
| tech_gebeurtenistype | 1 | `gesch_uitvinding_boom` |
| sim_run | 1000 | `Z44-GESCH-0001` tot `-1000`, dezelfde seeds als Z42 en Z43 |
| sim_fase / sim_wet / sim_huis / sim_uitvinding | 72 / 105 / 35 / 78 | de zes gekozen runs |
| sim_gebeurtenis | 962 | |
| keuze | 4 | `KEUZE-Z44-*` |
| logboek | 1 | |

`importeer.py` en `genereer.py` kennen de twee nieuwe tabellen. Geen canonrij gewijzigd of verwijderd; roman en Kern niet aangeraakt.

## Controles

| meting | voor | na |
|---|---|---|
| toetsregels | 43 | 45 |
| nieuwe fouten | 0 | 0 |
| signalen | 1734 | 1734 |
| roundtrip (ook de nieuwe tabellen) | gelijk | gelijk |
| tweede run van `r_Z44.py` | | 0 rijen erbij |
| drie expres aangebrachte fouten in een kopie | | alle drie gevonden |
