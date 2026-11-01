# Opdracht ronde Z33 (Rogier, 2026-11-01): de canon-motor-skill als meetlat

Rogier: "het is een benchmark skill.. dus daardoor kan je de database vele malen beter inrichten."

A. Keuren: scorekaart van 8 metingen + schema-geuren (nulmeting, echt gemeten): z33/meet.py, z33/koude_lezer.py -> z33/scorekaart.md.
B. Verbouwen (op kopie, daarna canon.db), in de volgorde van de skill:
 1. herkomst (bron, bron_soort, besloten_door, besloten_op; onbekend = niet verzinnen) + regel Kern zonder bron
 2. regeltabel `regel`; toets.py draait uit de regels
 3. getypeerde relaties `relatie` + v_impact + vraag.py impact
 4. ankers uitgebreid; anker_kopie, v_anker, v_actief_anker; risicolijst
 5. mal-breker `boog` + regels mal_aangrenzend / motief_max + voorstellen (elk een eigen vorm)
 6. `personage` (eigen_fout, soort_fout, wie_betaalt, zelfbedrog, daarna_doet) + voorstellen (elk een andere soort fout)
 7. `zaadje` (geplant/oogst/status)
 8. triggers (geen DELETE, geldige status/draagkracht, vervangen_door bestaat)
 9. handleiding, SCHEMA.md, bijbel/00_HANDLEIDING.md, nameting.
Regels: nooit verwijderen; roman niet aanraken; geen inhoudelijke Kern-wijziging (tegenspraak = wrijving); alles inhoudelijks voorlopig.
Pijplijn: backup canon_backup_Z33.db -> r_Z33.py -> migreer -> afgeleid -> toets (0) -> genereer -> export -> roundtrip (0) -> kopie verhalen/canon_lees.db.
