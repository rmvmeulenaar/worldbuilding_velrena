# Wijzigingen Z38 (2026-11-01, r_Z38.py, idempotent; niets verwijderd)

## Telling uit tabel wijziging

| soort | veld | aantal |
|---|---|---|
| toegevoegd | canon | 116 |
| gewijzigd | verhaal_profiel.premisse | 115 |
| gewijzigd | verhaal_profiel.premisse_codes | 115 |
| gewijzigd | verhaal_profiel.drager | 35 |
| vervangen | status | 23 |
| gewijzigd | verhaal_profiel.status | 17 |
| gewijzigd | verhaal_profiel.uitslag | 17 |
| gewijzigd | verhaal_profiel.vervangen_door | 17 |
| vervangen | vervangen_door | 8 |
| gewijzigd | canon.bron_handmatig | 5 |
| gewijzigd | keuze.aanbeveling | 3 |
| gewijzigd | wrijving.beschrijving | 3 |
| gewijzigd | wrijving.status | 3 |
| gewijzigd | anker.bron_code | 2 |
| gewijzigd | keuze.status | 2 |
| toegevoegd | keuze | 2 |
| toegevoegd | regel | 2 |
| toegevoegd | toets_uitzondering | 2 |
| toegevoegd | wrijving | 2 |
| toegevoegd | anker | 1 |

## Nieuwe canonrijen (116)

BESLUIT-Z38-1, BESLUIT-Z38-10, BESLUIT-Z38-11, BESLUIT-Z38-12, BESLUIT-Z38-13, BESLUIT-Z38-14, BESLUIT-Z38-2, BESLUIT-Z38-3, BESLUIT-Z38-4, BESLUIT-Z38-5, BESLUIT-Z38-6, BESLUIT-Z38-7, BESLUIT-Z38-8, BESLUIT-Z38-9, FASE-brand-Z38, FASE-noodtoestand-Z38, FUNC-VOORT-Z38, GAVE-VERHOUDINGEN-Z38, GES-herkomst-gave-Z38, HAAK-techno-bio-1-Z38, MAGIE-GESCH-5-Z38, OORSPRONG-bio-3-V4-Z38, PER-oevrin-held-glu-moeder-Z38, PER-skerra-held-kira-Z38, PER-vathren-schurk-dax-Z38, PERS-Z4-aelthir-0-1-Z5b-Z38, PERS-Z4-aelthir-1-2-Z38, PERS-Z4-aelthir-3-2-Z5b-Z38, PERS-Z4-aelthir-4-1-Z38, PERS-Z4-aelthir-6-2-Z5b-Z38, PERS-Z4-dhurn-0-2-Z38, PERS-Z4-dhurn-4-1-Z38, PERS-Z4-dhurn-7-1-Z38, PERS-Z4-grauwen-6-2-Z38, PERS-Z4-grauwen-7-2-Z38, PERS-Z4-ishvar-3-2-Z5b-Z38, PERS-Z4-ishvar-4-2-Z38, PERS-Z4-skerra-3-1-Z5b-Z38, PERS-Z4-vathren-0-2-Z38, PERS-Z4-veslethi-1-2-Z5b-Z38, PERS-Z4-veslethi-3-2-Z5b-Z38, PERS-Z4-veslethi-4-2-Z5b-Z38, PLEK-Z1-kharvos-6-Z38, PLEKTOESTAND-Z11-wortel-2-Z38, REGEL-feeenafspraak-Z38, RIJK-Z38-mens-ambergaard-dieren, RIJK-Z38-mens-ambergaard-drinken, RIJK-Z38-mens-ambergaard-eten, RIJK-Z38-mens-ambergaard-feest, RIJK-Z38-mens-ambergaard-geloof, RIJK-Z38-mens-ambergaard-handel, RIJK-Z38-mens-ambergaard-humor, RIJK-Z38-mens-ambergaard-kinderen, RIJK-Z38-mens-ambergaard-kleding, RIJK-Z38-mens-ambergaard-muziek, RIJK-Z38-mens-ambergaard-recht, RIJK-Z38-mens-ambergaard-reizen, RIJK-Z38-mens-ambergaard-rouw, RIJK-Z38-mens-ambergaard-taal, RIJK-Z38-mens-ambergaard-werk, RIJK-Z38-mens-ambergaard-werk-2, RIJK-Z38-mens-ambergaard-wonen, RIJK-Z38-mens-ambergaard-zorg, RIJK-Z38-mens-brakhaven-dieren, RIJK-Z38-mens-brakhaven-drinken, RIJK-Z38-mens-brakhaven-eten, RIJK-Z38-mens-brakhaven-feest, RIJK-Z38-mens-brakhaven-geloof, RIJK-Z38-mens-brakhaven-handel, RIJK-Z38-mens-brakhaven-humor, RIJK-Z38-mens-brakhaven-kinderen, RIJK-Z38-mens-brakhaven-kleding, RIJK-Z38-mens-brakhaven-muziek, RIJK-Z38-mens-brakhaven-recht, RIJK-Z38-mens-brakhaven-reizen, RIJK-Z38-mens-brakhaven-rouw, RIJK-Z38-mens-brakhaven-taal, RIJK-Z38-mens-brakhaven-werk, RIJK-Z38-mens-brakhaven-wonen, RIJK-Z38-mens-brakhaven-zorg, RIJK-Z38-mens-saelith-dieren, RIJK-Z38-mens-saelith-drinken, RIJK-Z38-mens-saelith-eten, RIJK-Z38-mens-saelith-feest, RIJK-Z38-mens-saelith-geloof, RIJK-Z38-mens-saelith-handel, RIJK-Z38-mens-saelith-humor, RIJK-Z38-mens-saelith-kinderen, RIJK-Z38-mens-saelith-kleding, RIJK-Z38-mens-saelith-muziek, RIJK-Z38-mens-saelith-recht, RIJK-Z38-mens-saelith-reizen, RIJK-Z38-mens-saelith-rouw, RIJK-Z38-mens-saelith-taal, RIJK-Z38-mens-saelith-werk, RIJK-Z38-mens-saelith-wonen, RIJK-Z38-mens-saelith-zorg, RIJK-Z38-mens-zoutkust-dieren, RIJK-Z38-mens-zoutkust-drinken, RIJK-Z38-mens-zoutkust-eten, RIJK-Z38-mens-zoutkust-feest, RIJK-Z38-mens-zoutkust-geloof, RIJK-Z38-mens-zoutkust-handel, RIJK-Z38-mens-zoutkust-humor, RIJK-Z38-mens-zoutkust-kinderen, RIJK-Z38-mens-zoutkust-kleding, RIJK-Z38-mens-zoutkust-muziek, RIJK-Z38-mens-zoutkust-recht, RIJK-Z38-mens-zoutkust-reizen, RIJK-Z38-mens-zoutkust-rouw, RIJK-Z38-mens-zoutkust-taal, RIJK-Z38-mens-zoutkust-werk, RIJK-Z38-mens-zoutkust-wonen, RIJK-Z38-mens-zoutkust-zorg, RIT-B1-zwangerschap-Z38, VOLK-karrûk-Z6-Z38

## Vervangen (oud → opvolger)

- FASE-brand → FASE-brand-Z38
- FASE-noodtoestand → FASE-noodtoestand-Z38
- FUNC-VOORT → FUNC-VOORT-Z38
- GES-herkomst-gave → GES-herkomst-gave-Z38
- HAAK-techno-bio-1 → HAAK-techno-bio-1-Z38
- MAGIE-GESCH-5 → MAGIE-GESCH-5-Z38
- OORSPRONG-bio-3-V4 → OORSPRONG-bio-3-V4-Z38
- PER-oevrin-held-glu-moeder → PER-oevrin-held-glu-moeder-Z38
- PER-skerra-held-kira → PER-skerra-held-kira-Z38
- PER-vathren-schurk-dax → PER-vathren-schurk-dax-Z38
- PERS-Z4-aelthir-0-1-Z5b → PERS-Z4-aelthir-0-1-Z5b-Z38
- PERS-Z4-aelthir-1-2 → PERS-Z4-aelthir-1-2-Z38
- PERS-Z4-aelthir-3-2-Z5b → PERS-Z4-aelthir-3-2-Z5b-Z38
- PERS-Z4-aelthir-4-1 → PERS-Z4-aelthir-4-1-Z38
- PERS-Z4-aelthir-6-2-Z5b → PERS-Z4-aelthir-6-2-Z5b-Z38
- PERS-Z4-dhurn-0-2 → PERS-Z4-dhurn-0-2-Z38
- PERS-Z4-dhurn-4-1 → PERS-Z4-dhurn-4-1-Z38
- PERS-Z4-dhurn-7-1 → PERS-Z4-dhurn-7-1-Z38
- PERS-Z4-grauwen-6-2 → PERS-Z4-grauwen-6-2-Z38
- PERS-Z4-grauwen-7-2 → PERS-Z4-grauwen-7-2-Z38
- PERS-Z4-ishvar-3-2-Z5b → PERS-Z4-ishvar-3-2-Z5b-Z38
- PERS-Z4-ishvar-4-2 → PERS-Z4-ishvar-4-2-Z38
- PERS-Z4-skerra-3-1-Z5b → PERS-Z4-skerra-3-1-Z5b-Z38
- PERS-Z4-vathren-0-2 → PERS-Z4-vathren-0-2-Z38
- PERS-Z4-veslethi-1-2-Z5b → PERS-Z4-veslethi-1-2-Z5b-Z38
- PERS-Z4-veslethi-3-2-Z5b → PERS-Z4-veslethi-3-2-Z5b-Z38
- PERS-Z4-veslethi-4-2-Z5b → PERS-Z4-veslethi-4-2-Z5b-Z38
- PLEK-Z1-kharvos-6 → PLEK-Z1-kharvos-6-Z38
- PLEKTOESTAND-Z11-wortel-2 → PLEKTOESTAND-Z11-wortel-2-Z38
- RIT-B1-zwangerschap → RIT-B1-zwangerschap-Z38
- VOLK-karrûk-Z6 → VOLK-karrûk-Z6-Z38

## Overig
- anker: gave_verhoudingen (1 op 100; 1 op 20; 1 op 2000 → GAVE-VERHOUDINGEN-Z38); fase_3_naam/fase_4_naam wijzen naar FASE-brand-Z38/FASE-noodtoestand-Z38.
- regels: R-fee_afspraak (fout, BESLUIT-Z38-9), R-premisse_vorm (fout, BESLUIT-Z38-12).
- wrijvingen: WRIJ-Z37-1, WRIJ-Z37-2, WRIJ-Z33-7 opgelost; nieuw open: WRIJ-Z38-1, WRIJ-Z38-2. WRIJ-Z29-1 en WRIJ-Z34-2 blijven open.
- verhaal_profiel: 17 samengevoegd (vervangen_door), 110 handgeschreven premissen, 5 zonder drager → geen premisse; drager bijgewerkt naar de -Z38 opvolgers (Wil).
- ideeen_verwerking: fase/fase_bron/assen_z38/uitslag_z38/reden_z38 voor 1902 rijen.
- competentievraag +3 (volk mens); competentie_antwoord +219 met regio.
- schema: migraties/008_z38_herkomst.py (canon.context, herkomst_laag, bron_handmatig; verhaal_profiel.vervangen_door; ideeën-kolommen; competentievraag.volk; competentie_antwoord.regio; view v_rijkdom).
- code: afgeleid_motor.py (herkomst in lagen, gedeelde-waardetoets), toets.py (2 py-regels), z36/machine.py (premisse uit tabel, geen sjabloon), z37/rijkdom.py (Z38-codes), importeer.py (glob 008), genereer.py (bron_handmatig), z36/dump.py (kolommen gesorteerd, alleen volgorde; backup dump_backup_Z38.py). Backups *_backup_Z38.py.
