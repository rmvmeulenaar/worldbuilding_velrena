# Wijzigingen Z40 (r_Z40.py, idempotent; niets verwijderd; Kern ongewijzigd)

| soort | veld | aantal |
|---|---|---|
| gewijzigd | keuze.aanbeveling | 7 |
| gewijzigd | keuze.status | 6 |
| toegevoegd | boog | 3 |
| toegevoegd | canon | 16 |
| toegevoegd | keuze | 5 |
| toegevoegd | regel | 1 |
| vervangen | status | 3 |

Nieuwe canonrijen: BESLUIT-Z40-1, BESLUIT-Z40-2, BESLUIT-Z40-3, BESLUIT-Z40-4, BESLUIT-Z40-5, BESLUIT-Z40-6, BESLUIT-Z40-7, BESLUIT-Z40-8, VERHAAL-fase4-d-Z40, VERHAAL-fase4-e-Z40, VERHAAL-fase4-f-Z40, IDEE-Z40-1, IDEE-Z40-2, IDEE-Z40-3, IDEE-Z40-4, IDEE-Z40-5

Vervangen: IDEE-Z39-4 → VERHAAL-fase4-d-Z40; IDEE-Z39-6 → VERHAAL-fase4-e-Z40; IDEE-Z39-7 → VERHAAL-fase4-f-Z40.

Simulatieruns: personen_z40: 1000; personen_z40_f5: 50; personen_z40_gevoeligheid: 600; ziekte: 1000; ziekte_gevoeligheid: 400; ziekte_zonder_sluiting: 200

Nieuwe regels in sim_regel: SIM-schrijfsters, SIM-registerbereik, ZIEKTE-* (14). Nieuwe gebeurtenistypen: ziekte_index, ziekte_besmetting_regio, ziekte_sterfte, ziekte_route_dicht.