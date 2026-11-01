# Wijzigingen Z39 (2026-11-01, r_Z39.py, idempotent; niets verwijderd; roman niet aangeraakt)

## Canon en beheer (tabel wijziging)

| soort | veld | aantal |
|---|---|---|
| toegevoegd | canon | 15 |
| toegevoegd | keuze | 6 |
| gewijzigd | keuze.aanbeveling | 3 |
| gewijzigd | canon.bron_handmatig | 2 |
| gewijzigd | keuze.status | 2 |
| gewijzigd | wrijving.beschrijving | 2 |
| gewijzigd | wrijving.status | 2 |
| toegevoegd | regel | 2 |

- Nieuwe canonrijen:
  - BESLUIT-Z39-1 tot -5 (besloten_door Rogier; Kern: Z39-3);
  - IDEE-Z39-1 tot -10 (ideeënbank, voorlopig, epistemiek simulatie).
- bron_handmatig gezet: EROS-GRENZEN-Z7 = BESLUIT-Z30-4; GES-officiele-versie = 'auteur (Rogier), wereldbijbel'.
- Wrijvingen opgelost: WRIJ-Z38-1 en WRIJ-Z38-2. WRIJ-Z29-1 blijft open.
- Keuzes:
  - besloten: KEUZE-WRIJ-Z38-1 en KEUZE-WRIJ-Z38-2;
  - nieuw: 6 keuzes (KEUZE-Z39-*).
- Regels: R-sim_harde_lijn (fout) en R-epistemiek (fout).

## Nieuwe tabellen (migraties/009_z39_simulatie.py), met aantallen

| tabel | rijen | gebruikt door |
|---|---|---|
| sim_regel | 18 | sim.py (regels met bron) |
| gebeurtenis_type | 18 | sim.laad_typen (de motor laadt alleen deze; geen type met harde-lijnrisico) |
| tech_gebeurtenistype | 6 | tech.py |
| sim_run | 2450 | montecarlo.py en tech.py (alle runs) |
| sim_gebeurtenis | 4892 | top-5 runs + beste tech-run; v_sim_validatie |
| sim_figuur | 21 | achtergrondfiguren uit de gekozen run; v_personage_laag |
| verblijf | 189 | intrige.plek; v_sim_waar |
| kennis | 265 | intrige.chantage; v_sim_wie_weet |
| per_relatie | 205 | afgeleid_motor.per_relaties → relatie (met van_jaar/tot_jaar); intrige |
| steekproef | 50 | 11d.2 |

Kolommen:
- relatie.van_jaar en relatie.tot_jaar;
- epistemiek op alle nieuwe tabellen en op canon;
- sim_gebeurtenis.oorzaak.

Views: v_personage_laag, v_sim_fase, v_sim_wie_weet, v_sim_waar, v_sim_top, v_sim_validatie.

## Code

Alle oude versies staan als *_backup_Z39.py.
- Nieuw in z39/:
  - sim.py: motor, regels, typen, invarianten, storyteller-scores;
  - montecarlo.py: runs, Pareto, validatie;
  - tech.py: module technologie en beroepen;
  - intrige.py: graafvragen;
  - premisses.py;
  - nieuwheid.py;
  - koude_lezer.py;
  - data.py.
- vraag.py: nieuw commando `intrige <complot|chantage|rivaliteit|erfwrok> [PLEK|-] [JAAR]`.
- afgeleid_motor.py:
  - per_relaties() zet per_relatie in relatie;
  - het relatieschema heeft jaarkolommen;
  - een bron_handmatig die met BESLUIT begint, telt als laag hard (BESLUIT-Z39-3).
- toets.py: py_sim_harde_lijn en py_epistemiek. PY wordt nu na alle py_-functies gebouwd.
- genereer.py en importeer.py: nieuwe tabellen in export en import; canon.epistemiek; migratieglob 00[56789].
