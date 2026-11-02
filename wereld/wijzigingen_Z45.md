# Ronde Z45: gebruik, gewone uitvindingen en de weg naar een gewone tijd

Gebouwd door de architect op verzoek van Rogier (2026-11-02). Script: `r_Z45.py` (idempotent). Boom: `z45/boom.py`. Motor: `z45/geschiedenis.py`. Uitleg: `z45/LEESMIJ.md`. Open beslissingen: `keuzelijst_Z45.md`.

## Wat erbij kwam en wat veranderde

| wat | aantal | |
|---|---|---|
| migratie `012_z45_gebruik.py` | 7 + 9 kolommen, 1 view | gebruik en effect bij `tech_knoop` en `sim_uitvinding`; `v_tech_gebruik` |
| tech_knoop | 11 nieuw | gewone uitvindingen `TN-*` |
| tech_knoop bijgewerkt | 17 knopen | gebruik, voor wie, aards equivalent, tijdperk, soort, verval, opvolger (elk veld in `wijziging`) |
| tech_knoop herzien | 4 | `TK-x-stoom` en `TK-x-kruit` naar `vervangen`, `TK-x-kolen` naar `open`, `TK-x-staal` aangescherpt (correctie op Z44) |
| regel | 3 nieuw, 1 aangepast | `R-tech_gebruik`, `R-sim_effect`, `R-sim_convergentie` (signaal); `R-tech_boom` kent nu `A|B` |
| sim_regel | 5 | `GESCH4-*` |
| tech_gebeurtenistype | 1 | `gesch_techniek_verloren` |
| sim_run | 1000 | `Z45-GESCH-0001` tot `-1000`, dezelfde seeds |
| sim_fase / sim_wet / sim_huis / sim_uitvinding | 83 / 104 / 35 / 159 | de zes gekozen runs |
| sim_gebeurtenis | 1072 | |
| keuze | 5 | `KEUZE-Z45-*` |
| wijziging | 165 | elke aanpassing aan een bestaande rij |

Geen canonrij gewijzigd of verwijderd; roman en Kern niet aangeraakt.

## Controles

| meting | voor | na |
|---|---|---|
| toetsregels | 45 | 48 |
| nieuwe fouten | 0 | 0 |
| signalen | 1734 | 1734 (convergentie haalt de 80%: 83,6%) |
| roundtrip | gelijk | gelijk |
| tweede run van `r_Z45.py` | | 0 rijen erbij |
| drie expres aangebrachte fouten en een te lage convergentie | | alle vier gevonden |
