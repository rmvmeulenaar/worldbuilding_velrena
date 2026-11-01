# Scorekaart Z37 (canon-motor, 8 metingen: voor → na)
Bron: z37/z33_voor.json → z37/z33_na.json, plus z37/meting_voor.json → z37/meting_na.json.

| # | meting | voor | na |
|---|---|---|---|
| 1 | veranderproef: plekken te wijzigen (Thalen sterfjaar) | 11 | 11 |
| 2 | duplicatiegraad: kopieën van ankerwaarden | 53 (1,6/anker) | 51 (1,5) |
| 2b | letterlijke kopieën (totaal) | 743 | 541 |
| 3 | dode links | 0 | 0 |
| 4 | herkomst Kern met bron | 92/98 (93,9%) | 103/103 (100%)* |
| 4 | herkomst Structuur met bron | 1561/2871 (54,4%) | 2545/2545 (100%)* |
| 5 | toetsen: exit / nieuw falend / controles | 0 / 0 / 33 | 0 / 0 / 34 |
| 6 | roundtrip: tabellen / verschillen | 35 / 0 | 42 / 0 |
| 7 | terugdraaien (backup + r_Z37.py → canon.db) | werkt | 0 verschillen in 42 tabellen |
| 8 | koude lezer | 10/10 | 10/10 |

Extra:
- Aandeel van de canon in een sjabloonfamilie: 46,9% → 37,7%.
- Near-dup-paren: 4871 → 1683.
- Open wrijvingen: 29 → 5.

\* De herkomst van 100% is grotendeels heuristisch:
- 584 Structuur-rijen kregen "wereldbijbel" omdat hun historie hun eigen ronde (1–22) noemt.
- 8 Kern-rijen kregen een C1-ketenbron. Die ketens zijn formeel geldig maar niet met de hand gecontroleerd (keuzelijst 1).
- Elf Kleur-rijen houden "onbekend".

Let op bij meting 5: "bekend zonder open wrijving" ging van 2 → 87. De 85 bekende kern_leunt_op_kleur-vondsten rusten op WRIJ-Z33-2, en die is gesloten door BESLUIT-Z37-5 (B). Dat is dus geregistreerd door een besluit, niet vergeten.
