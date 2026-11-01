# Scorekaart canon-motor: nulmeting (na Z32) en nameting (na Z33)

Gemeten op 2026-11-01 met `z33/meet.py` (ruw: `z33/nulmeting_ruw.json`, `z33/nameting_ruw.json`). Veranderproef en terugdraaien zijn op tijdelijke kopieën gedraaid.

| # | Meting | Nulmeting (Z32) | Nameting (Z33) | Streef | Wat er nog voor nodig is |
|---|---|---|---|---|---|
| 1 | Veranderproef (Thalens sterfjaar -1198 → -1197 op een kopie) | 11 plekken te wijzigen (bron + 10 levende kopieën); toets.py vindt er 2 | nog steeds 11 plekken; toets.py vindt er nu 7 (scherpere patronen) | 1 | De 10 kopieën in de tekst vervangen door "zie anker thalen_sterfjaar". Niet gedaan: dan verandert de tekst van vastgestelde rijen, en dat is Rogiers besluit. |
| 2 | Duplicatiegraad | 14 ankers met patroon, 38 kopieën (2,7 per anker); 26 ankers | 33 ankers met patroon, 58 kopieën (1,8 per anker); 69 ankers. Letterlijke waarde + naam: 720 → 975 (stijgt omdat er meer ankers zijn; 801 alleen al 477) | elk ankerfeit één keer | Kopieën vervangen door verwijzingen (zelfde besluit als bij 1). Schrijvers lezen nu v_actief_anker. |
| 3 | Dode links | 0 | 0 | 0 | - |
| 4 | Herkomstdekking | geen bronkolom: 0% (alleen indirect: 92,5% Kern / 34,6% Structuur noemt een besluit of Rogier) | Kern 87/93 = 93,5%; Structuur 1.745/4.824 = 36,2% | 100% / ≥90% | 6 Kern-rijen (REGEL-nageslacht-per-man, REGEL-seksuele-normen, REGEL-doelgroep-toon, MAGIE-zaadkracht, MAGIE-kracht-duur, REGEL-harde-grenzen) en 3.079 Structuur-rijen hebben geen af te leiden bron. Rogier moet per Kern-rij een besluit noemen; Structuur vraagt een ronde waarin de rijen gelezen worden. Niet verzonnen. |
| 5 | Tests | 10 controles in code; 0 nieuw falend; 2 bekend | 22 regels in de tabel `regel` (17 fout, 5 signaal); 0 nieuw falend; 188 bekend, elk met een wrijving (WRIJ-Z33-1..11); 2 bekend zonder open wrijving (de Z31-nagekeken harde-grens-vals-positieven) | 0 falend zonder open wrijving | De 188 bekende bevindingen oplossen (vooral 170 × Kern leunt op Kleur). |
| 6 | Roundtrip | 13 tabellen, 0 verschillen | 19 tabellen + 12 views, 0 verschillen | 0 | - |
| 7 | Terugdraaien | werkt: backup_Z32 + r_Z32.py = huidige stand (0 verschillen) | werkt: backup_Z32 + r_Z32.py én backup_Z33 + r_Z33.py, 0 verschillen | werkt | - |
| 8 | Koude lezer (mechanisch: alleen v_kern, handleiding en v_anker; 10 vragen over Kern) | 7/10 | 10/10 | 10/10 | Dit is een zoekproef, geen LLM-lezer. De 3 fouten in de nulmeting (sterfjaar Thalen, aan boord, wie activeert in jaar 0) kwamen doordat het antwoord in een lange rij stond; met v_anker staat het op één plek. |

## Schema-geuren (voor → na)
- Lijsten met `;` in verwijst_naar: 6.185 → 6.185 (tekstkolom blijft voor oude scripts, maar er staat nu ook een getypeerde `relatie` naast: 25.784 relaties).
- Eén kolom met twee betekenissen (`voorlopig, vervangen`): 479 → 479 (niet aangeraakt, de pijplijn leunt erop; vervangen_door is wel verplicht).
- Geschiedenis in feit: 571 → 571 (feit_schoon is al schoon; feit blijft het origineel).
- Constraints: 0 triggers → 14 triggers (geen DELETE, geldige status/draagkracht, vervangen_door bestaat). Foreign keys: 0 → 0 (SQLite kan ze niet achteraf toevoegen zonder tabellen te herbouwen).
- Ronde aantallen buiten de ideeënbank: Magie 30, Ritueel systeem 60, Planten en dieren 60 (alleen gesignaleerd).
- Open wrijvingen: 23 → 34 (11 nieuw uit Z33).

## Eerlijk: wat niet bereikt is
- Principe 1 (één bron per feit) zit in de structuur (anker, anker_kopie, v_actief_anker), niet in de tekst. Daarom blijft de veranderproef op 11.
- Structuur heeft maar 36% herkomst.
- Kern leunt 170 keer op Kleur (vooral FASE-OVERZICHT-Z10 → ideeënbank). Dat is Kern-inhoud, dus het staat als wrijving.
