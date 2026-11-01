# Scorekaart ronde Z36 (canon-motor), gemeten op 2026-11-01

Voor = canon_backup_Z36.db (gelijk aan canon_na_Z35), na = canon.db / canon_na_Z36.db. Metingen: z33/meet.py en z34/meet.py (z36/z33_voor|na.json, z36/meting_voor|na.json).

## Klaar-als criteria
| stap | criterium | query of commando | voor | na | gehaald |
|---|---|---|---|---|---|
| 0 | elke besluitrij bestaat | `select count(*) from canon where code like 'BESLUIT-Z36-%'` | 0 | 9 | ja |
| 0 | vervangen rijen hebben een geldige vervangen_door | `select count(*) from canon where status='voorlopig, vervangen' and (vervangen_door is null or vervangen_door not in(select code from canon))` | 0 | 0 (29 nieuw vervangen) | ja |
| 0 | v_kern toont de ORIGIN-10-opvolger | `select count(*) from v_kern where code='ORIGIN-10-Z36'` | 0 | 1 | ja |
| alle | toets.py exit 0 na elke stap | `python3 toets.py` in r_Z36.py (z36/run1.log) | – | 8 keer exit 0, 0 nieuwe fouten | ja |
| 1a | sjabloonaandeel buiten de ideeënbank <35% | `python3 z34/meet.py` → aandeel_canon_in_familie | 47,1% (1456/3091) | 46,9% (1448/3087) | **nee** (zie blokkade) |
| 1a | geen familie met canon-gewicht zonder besluit | `select count(*) from sjabloon_familie where voorstel is null` | 124 | 0 | ja |
| 1b | herkomst Structuur streng ≥70% (doorlopend, niet blokkerend) | `python3 z33/meet.py` → 4_herkomst.Structuur.pct | 54,4% | 54,4% (1561/2871) | nee (niet aan gewerkt, zoals de opdracht zegt) |
| 1b | top-50 herkomstgaten hebben per rij een voorstel | `select count(*) from keuze where soort='herkomst' and status='open' and aanbeveling not like 'Aanbeveling:%'` | 50 | 0 | ja |
| 1c | 0 keer "nog geen aanbeveling" | `select count(*) from keuze where status='open' and lower(aanbeveling) like '%nog geen aanbeveling%'`; ook grep in keuzelijst_Z36.md | 25 | 0 | ja |
| 1c | elk open punt heeft een citaat | `select count(*) from keuze where status='open' and citaat is null` | 101 (kolom bestond niet) | 0 | ja |
| 1c | dubbele namen: besluitvoorstel per paar | KEUZE-WRIJ-Z32-1..5 en Z14-1 in keuzelijst_Z36.md | geen | 6 voorstellen (1 rangnummer, 5 erfnaam) | ja |
| 2 / 7 | regels groen | toets.py: R-verhaal_afstand, R-profiel_harde_lijn (fout), R-positie_dekking (signaal) | – | 0 / 0 / 0 bevindingen | ja |
| 2 / 7 | test 20 profielen fase 4: min. onderlinge afstand ≥3 | z36/controles_stap2.txt (run Z36-03) | – | kleinste 5, gemiddeld 6,21; alle 7 posities | ja |
| 2 / 8 | filter laat nooit een fout profiel door | `python3 z36/test_filter.py` | – | 9 van 9 fout geweigerd; toets.py exit 1 op een buiten de machine ingevoegd fout profiel | ja |
| 2 / 8 | Pareto-front klopt | z36/controles_stap2.txt | – | 0 front-profielen verslagen door een kandidaat (25 op het front, 2899 kandidaten) | ja |
| 2 / 8 | gewichten in doel met herkomst | `select code,gewicht,bron_gewicht from doel` | – | 6 rijen, alle 'aanname' | ja |
| 2 / 9 | bedenk 6 10 erotische suspense: 10, allen boven minimum, harde lijnen, wereldregel met code | z36/demo_bedenk_6_erotische_suspense.txt + controles_stap2.txt | – | 10/10, alle erotiek≥4 en suspense≥4, alle met bestaande code | ja |
| 2 / 9 | gewichtsets met methode en datum | `select naam,datum,methode from gewichtset` | – | 'lancering serie', 2026-11-01, startwaarde | ja |
| 2 / 9 | gevoeligheidstoets per voorstel | grep -c "gevoeligheid:" demo | – | 10 van 10 | ja |
| 2 | rapport ideeënbank | `python3 vraag.py ideeenrapport --positie` | – | hieronder | ja |
| 2 | elke fase alle 7 posities gedekt | `select count(*) from v_positie_dekking where in_canon+in_ideeenbank=0` | 34 lege cellen (alleen bogen) | 0 | ja |
| rond | roundtrip 0 verschillen | `python3 roundtrip.py` (z36/roundtrip.txt) | 0 (Z35) | 0, 35 tabellen, views gelijk | ja |
| rond | tweede run voegt niets toe | z36/dump.py na run 1 tegen na run 2 | – | 0 verschillen in 35 tabellen | ja |
| rond | terugdraaitest backup_Z36 + r_Z36 = canon.db | z36/terugdraaitest.txt | – | 0 verschillen | ja |
| rond | roman ongewijzigd | md5 van 50 bestanden (z36/roman_md5_voor/na.txt) | af212ef0… | af212ef0abde2bb41d71b1cb63f8b484 | ja |
| rond | grep minderjarigen/dieren in seksuele rol | z36/grep_harde_lijn.txt | – | 4 treffers, alle met de hand gelezen: geen seksuele rol | ja |

**Blokkade 1a (bewijs):** de personagefamilies (258 + 81 + 63 + 80 rijen) staan nu in kolommen in `personage_profiel` (592 rijen, afgeleid). De oude rijen gaan niet naar 'vervangen', omdat er ankers (`anker.bron_code`, bv. PER-v4-thalen-orr-Z32), relaties, de naamtoets en de na-dood-toets op hun code lezen, en `vervangen_door` een canoncode moet zijn. Vervangen breekt die toetsen. De opdracht zegt bij 1a: het percentage is deze ronde geen doel op zich. Volgende stap (Z37): laat ankers, relaties en naamtoets op personage_profiel lezen, en zet daarna de 482 rijen om.

## 8 canon-motor metingen
| meting | voor | na |
|---|---|---|
| 1 veranderproef (Thalen -1198) | 11 plekken, toets vindt 7 | 11, 7 (ongewijzigd) |
| 2 duplicatie: letterlijke kopieën van ankers | 739 | 743 |
| 2 duplicatiegraad (kopieën in patroon) | 58 | 53 |
| 2 near-dup paren (z34) | 4871 | 4871 |
| 3 dode links | 0 | 0 |
| 4 herkomst Kern | 93.5% (87/93) | 93.9% (92/98) |
| 5 tests | 30 controles, 186 bekend, 0 nieuw | 33 controles, 149 bekend, 0 nieuw |
| 6 roundtrip | 0 (26 tabellen) | 0 (35 tabellen) |
| 7 terugdraaien | werkt | werkt (0 verschillen) |
| 8 koude lezer (vaste vragen in z33/meet.py) | 10/10 | 10/10 (geen nieuwe menselijke koude lezer gedaan) |

Geuren: open wrijvingen 38 → 29 (3 nieuw, 12 gesloten); triggers 21 → 29 (nieuwe tabellen, niet-verwijderen).

## Rapport ideeënbank (run Z36-01)
```
instroom 1983; uitval afstand 772; uitval verbinding 90; uitval filter 0; geen fase 1103; ent-klaar 18
  fase (geen fase) : instroom 1103 | afstand 0 | verbinding 0 | ent-klaar 0
  fase 0 Voortijd : instroom 48 | afstand 42 | verbinding 6 | ent-klaar 0
  fase 1 Overvloed : instroom 128 | afstand 123 | verbinding 4 | ent-klaar 1
  fase 2 Vonk : instroom 53 | afstand 48 | verbinding 2 | ent-klaar 3
  fase 3 Brand : instroom 51 | afstand 51 | verbinding 0 | ent-klaar 0
  fase 4 Noodtoestand : instroom 47 | afstand 45 | verbinding 1 | ent-klaar 1
  fase 5 Ontvangst : instroom 62 | afstand 58 | verbinding 2 | ent-klaar 2
  fase 6 Markt : instroom 60 | afstand 44 | verbinding 6 | ent-klaar 10
  fase 7 Barsten : instroom 53 | afstand 53 | verbinding 0 | ent-klaar 0
  fase 801 Heden : instroom 378 | afstand 308 | verbinding 69 | ent-klaar 1
  per fase en positie (instroom, uitval afstand, uitval verbinding, ent-klaar):
    0 Voortijd | - | 11 | 11 | 0 | 0
    0 Voortijd | beslisser | 7 | 7 | 0 | 0
    0 Voortijd | betaler | 9 | 5 | 4 | 0
    0 Voortijd | liefde tussen posities | 13 | 11 | 2 | 0
    0 Voortijd | ontdekker | 6 | 6 | 0 | 0
    0 Voortijd | profiteur | 1 | 1 | 0 | 0
    0 Voortijd | vervalser | 1 | 1 | 0 | 0
    1 Overvloed | - | 70 | 69 | 1 | 0
    1 Overvloed | beslisser | 1 | 1 | 0 | 0
    1 Overvloed | betaler | 40 | 40 | 0 | 0
    1 Overvloed | liefde tussen posities | 6 | 6 | 0 | 0
    1 Overvloed | ontdekker | 6 | 4 | 2 | 0
    1 Overvloed | profiteur | 2 | 1 | 0 | 1
    1 Overvloed | toeschouwer | 1 | 1 | 0 | 0
    1 Overvloed | vervalser | 2 | 1 | 1 | 0
    2 Vonk | - | 26 | 25 | 0 | 1
    2 Vonk | betaler | 15 | 11 | 2 | 2
    2 Vonk | liefde tussen posities | 3 | 3 | 0 | 0
    2 Vonk | ontdekker | 1 | 1 | 0 | 0
    2 Vonk | profiteur | 5 | 5 | 0 | 0
    2 Vonk | vervalser | 3 | 3 | 0 | 0
    3 Brand | - | 27 | 27 | 0 | 0
    3 Brand | betaler | 13 | 13 | 0 | 0
    3 Brand | liefde tussen posities | 4 | 4 | 0 | 0
    3 Brand | ontdekker | 4 | 4 | 0 | 0
    3 Brand | profiteur | 3 | 3 | 0 | 0
    4 Noodtoestand | - | 27 | 27 | 0 | 0
    4 Noodtoestand | betaler | 5 | 3 | 1 | 1
    4 Noodtoestand | liefde tussen posities | 3 | 3 | 0 | 0
    4 Noodtoestand | ontdekker | 2 | 2 | 0 | 0
    4 Noodtoestand | profiteur | 1 | 1 | 0 | 0
    4 Noodtoestand | toeschouwer | 2 | 2 | 0 | 0
    4 Noodtoestand | vervalser | 7 | 7 | 0 | 0
    5 Ontvangst | - | 28 | 26 | 1 | 1
    5 Ontvangst | betaler | 13 | 12 | 1 | 0
    5 Ontvangst | liefde tussen posities | 2 | 2 | 0 | 0
    5 Ontvangst | ontdekker | 6 | 6 | 0 | 0
    5 Ontvangst | profiteur | 4 | 3 | 0 | 1
    5 Ontvangst | toeschouwer | 2 | 2 | 0 | 0
    5 Ontvangst | vervalser | 7 | 7 | 0 | 0
    6 Markt | - | 10 | 10 | 0 | 0
    6 Markt | beslisser | 1 | 1 | 0 | 0
    6 Markt | betaler | 19 | 13 | 6 | 0
    6 Markt | liefde tussen posities | 1 | 1 | 0 | 0
    6 Markt | ontdekker | 4 | 4 | 0 | 0
    6 Markt | profiteur | 24 | 15 | 0 | 9
    6 Markt | vervalser | 1 | 0 | 0 | 1
    7 Barsten | - | 36 | 36 | 0 | 0
    7 Barsten | betaler | 8 | 8 | 0 | 0
    7 Barsten | liefde tussen posities | 2 | 2 | 0 | 0
    7 Barsten | ontdekker | 1 | 1 | 0 | 0
    7 Barsten | profiteur | 2 | 2 | 0 | 0
    7 Barsten | toeschouwer | 3 | 3 | 0 | 0
    7 Barsten | vervalser | 1 | 1 | 0 | 0
    801 Heden | - | 134 | 127 | 7 | 0
    801 Heden | beslisser | 91 | 91 | 0 | 0
    801 Heden | betaler | 103 | 59 | 44 | 0
    801 Heden | liefde tussen posities | 17 | 10 | 7 | 0
    801 Heden | ontdekker | 17 | 14 | 3 | 0
    801 Heden | profiteur | 2 | 1 | 1 | 0
    801 Heden | toeschouwer | 7 | 3 | 4 | 0
    801 Heden | vervalser | 7 | 3 | 3 | 1
```
Lees zo: "geen fase" zijn bijna alleen stemmingskaarten zonder tijd (ZINT, KINKFUNC, EROS, KINK...), geen verhaaleenheden; elke INTR-, ROM-, THRL-, HORROR-, COMEDY-, ACTIE-, HELD-, OORLOG-, SAW- en HAAK-rij kreeg een fase. De afstand is streng gemeten: alleen assen die uit de tekst te lezen zijn tellen, een onbekende as telt als gelijk. Daardoor vallen veel ideeën af op afstand. Dat is een heuristiek, niet met de hand gelezen.

## Dekking 7 posities per fase (canon + ideeënbank)
```
fase | beslisser | betaler | vervalser | ontdekker | profiteur | toeschouwe | liefde tus
0 Voortijd | 1+0 | 0+3 | 0+3 | 0+3 | 0+3 | 0+3 | 0+3
1 Overvloed | 1+0 | 2+0 | 0+3 | 0+3 | 0+3 | 0+3 | 1+0
2 Vonk | 1+0 | 1+0 | 1+0 | 1+0 | 0+3 | 0+3 | 0+3
3 Brand | 1+0 | 0+3 | 1+0 | 0+3 | 1+0 | 0+3 | 1+0
4 Noodtoestand | 1+3 | 0+5 | 1+2 | 0+5 | 0+5 | 1+4 | 1+5
5 Ontvangst | 0+3 | 1+0 | 1+0 | 1+0 | 1+0 | 0+3 | 0+3
6 Markt | 0+4 | 0+4 | 0+5 | 1+2 | 1+1 | 1+2 | 1+1
7 Barsten | 0+3 | 1+0 | 1+0 | 0+3 | 1+0 | 0+3 | 1+0
801 Heden | 1+0 | 0+3 | 0+3 | 0+3 | 0+3 | 0+3 | 0+3
(canon+ideeënbank; 0+0 is een gat)
```

## Demo stap 2.3
### vraag.py bedenk 6 10 --profiel "erotische suspense"
```
# 6 Markt: volken aelthir, dhurn, grauwen, ishvar, karrûk, kluwer, mens, myrrhen, oevrin, orrim, sael-mor, skerra, tharn, vathren; bestaande bogen 4, eerdere profielen 19
gewichten: verbondenheid 0.30, seriewaarde 0.25, nieuwheid 0.20, lezersvraag 0.15, kosten 0.10; doelprofiel erotische suspense (min erotiek>=4, suspense>=4)
kandidaten na filters: 421; afgevallen: {'doelprofiel-minimum': 3480, 'rijm': 74, 'R-verhaal_afstand': 25}

## 10 profielen (farthest-point, eerst alle zeven posities, daarna marginale winst)

1. VP-6-fec608ae | profiteur | mysterie | wereld | orrim | getuigenverslag | blijft verborgen | 61+|groep
    genre: rom1 ero5 hor1 sus4 act0 int4 kom2 tra1
    doelen: nieuwheid 0.86, verbondenheid 0.42, seriewaarde 0.00, lezersvraag 0.55, kosten 0.42, genrematch 0.82; marginale winst 0.516
    raakt: ERF-ontvangst; zaadje -; wereldregel/rite SEKS-VOLK-orrim-slijpers; drager PER-orrim-schurk-graal
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

2. VP-6-69df71fc | liefde tussen posities | mysterie | huis | mens | brieven | faalt | 18-25|groep
    genre: rom3 ero4 hor1 sus4 act0 int3 kom1 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.91, seriewaarde 0.00, lezersvraag 0.55, kosten 0.24, genrematch 0.82; marginale winst 0.625
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite RIT-veiling; drager PER-pest-zarah
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

3. VP-6-53b69f11 | beslisser | thriller | wereld | sael-mor | aftellen | keert om | 26-40|v
    genre: rom1 ero5 hor1 sus5 act2 int3 kom0 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.76, seriewaarde 0.00, lezersvraag 0.65, kosten 0.50, genrematch 0.93; marginale winst 0.599
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite SEKS-VOLK-saelmor-diepduikers; drager PERS-Z4-saelmor-6-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

4. VP-6-74c34da9 | betaler | mysterie | dorp | karrûk | brieven | komt uit | 26-40|v
    genre: rom1 ero4 hor1 sus5 act0 int3 kom1 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.55, kosten 0.27, genrematch 0.85; marginale winst 0.582
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-karruk-bloedkampen; drager PER-karruk-schurk-durgh
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

5. VP-6-392e4d5e | toeschouwer | mysterie | huis | aelthir | kasboek | keert om | 41-60|v
    genre: rom1 ero5 hor2 sus5 act0 int3 kom1 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.55, kosten 0.19, genrematch 0.88; marginale winst 0.580
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-aelthir-geheugenruilers; drager PERS-Z4-aelthir-6-2-Z5b
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

6. VP-6-6853028f | ontdekker | actie | huis | karrûk | rechtszaak | keert om | 61+|groep
    genre: rom1 ero5 hor0 sus5 act5 int1 kom0 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.55, kosten 0.29, genrematch 0.82; marginale winst 0.576
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-karruk-kampvechters; drager PER-karruk-schurk-durgh
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

7. VP-6-5618af24 | vervalser | survival | stad | ishvar | zelfportret | komt uit | 26-40|wisselend
    genre: rom1 ero5 hor2 sus4 act3 int1 kom0 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.40, kosten 0.30, genrematch 0.82; marginale winst 0.543
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite SEKS-VOLK-ishvar-stilte; drager PERS-Z4-ishvar-6-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

8. VP-6-6e5a2d16 | liefde tussen posities | thriller | huis | oevrin | zelfportret | keert om | 61+|wisselend
    genre: rom3 ero4 hor1 sus5 act2 int2 kom0 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.65, kosten 0.24, genrematch 0.93; marginale winst 0.598
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite SEKS-VOLK-oevrin-landminnaars; drager PERS-Z4-oevrin-6-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

9. VP-6-540d2be2 | liefde tussen posities | thriller | rijk | ishvar | documenten | faalt | 26-40|groep
    genre: rom3 ero5 hor1 sus5 act2 int2 kom0 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.65, kosten 0.36, genrematch 0.93; marginale winst 0.589
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-ishvar-stilte; drager PER-ishvar-schurk-ammar
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

10. VP-6-484aa271 | liefde tussen posities | mysterie | stad | orrim | ballade | keert om | 26-40|v
    genre: rom3 ero4 hor1 sus5 act0 int3 kom1 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.55, kosten 0.18, genrematch 0.88; marginale winst 0.581
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite SEKS-VOLK-orrim-steeneters; drager PER-orrim-schurk-graal
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

```
### vraag.py pareto 4 10
```
# 4 Noodtoestand: volken aelthir, dhurn, grauwen, ishvar, karrûk, kluwer, mens, oevrin, orrim, skerra, tharn, vathren, ves-lethi; bestaande bogen 4, eerdere profielen 29
gewichten: verbondenheid 0.30, seriewaarde 0.25, nieuwheid 0.20, lezersvraag 0.15, kosten 0.10
kandidaten na filters: 2899; afgevallen: {'R-verhaal_afstand': 26, 'rijm': 75}; Pareto-fronten: 36 (eerste front 25 profielen)

## 10 uit het eerste front (greedy op marginale winst; niemand hierboven wordt op alle doelen tegelijk verslagen)

1. VP-4-b2f84e0f | profiteur | romance | huis | mens | getuigenverslag | komt uit | 41-60|v
    genre: rom5 ero1 hor0 sus2 act0 int0 kom2 tra1
    doelen: nieuwheid 0.57, verbondenheid 0.84, seriewaarde 0.00, lezersvraag 0.70, kosten 0.24; marginale winst 0.546
    raakt: ERF-brand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite RIT-zwijgende-rit; drager PER-vehlin
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

2. VP-4-a706b0f8 | vervalser | thriller | rijk | dhurn | kasboek | keert om | 18-25|groep
    genre: rom0 ero1 hor1 sus5 act2 int3 kom0 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.76, seriewaarde 0.00, lezersvraag 0.65, kosten 0.29; marginale winst 0.538
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-dhurn-mijnbroeders-Z6; drager PERS-Z4-dhurn-4-2-Z5b
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

3. VP-4-7dbee30d | beslisser | romance | rijk | oevrin | register als verteller | faalt | 41-60|groep
    genre: rom5 ero4 hor0 sus1 act0 int1 kom1 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.70, kosten 0.29; marginale winst 0.536
    raakt: ERF-brand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-oevrin-poelzangers; drager PER-orvath
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

4. VP-4-5ce3b393 | betaler | thriller | stad | karrûk | kasboek | komt uit | 61+|groep
    genre: rom1 ero5 hor1 sus5 act2 int2 kom0 tra2
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.65, kosten 0.24; marginale winst 0.533
    raakt: ERF-brand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-karruk-kampvechters; drager PERS-Z4-karruk-4-1
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

5. VP-4-1dd6ee63 | toeschouwer | mysterie | dorp | mens | kasboek | faalt | 41-60|v
    genre: rom0 ero2 hor2 sus4 act0 int3 kom1 tra2
    doelen: nieuwheid 0.57, verbondenheid 0.84, seriewaarde 0.00, lezersvraag 0.55, kosten 0.21; marginale winst 0.526
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite RIT-zwijgende-rit; drager PER-nessa-weerstand
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

6. VP-4-627bd9e5 | ontdekker | romance | stad | vathren | register als verteller | komt uit | 18-25|m
    genre: rom5 ero0 hor0 sus3 act0 int0 kom1 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.67, seriewaarde 0.00, lezersvraag 0.70, kosten 0.24; marginale winst 0.524
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-vathren-gezellen; drager PERS-Z4-vathren-4-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

7. VP-4-49e38d59 | beslisser | actie | huis | mens | ballade | komt uit | 18-25|wisselend
    genre: rom1 ero4 hor0 sus4 act5 int2 kom0 tra1
    doelen: nieuwheid 0.57, verbondenheid 0.80, seriewaarde 0.00, lezersvraag 0.55, kosten 0.14; marginale winst 0.522
    raakt: ERF-brand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite RIT-maanzalving; drager PER-vehlin
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

8. VP-4-a58af477 | liefde tussen posities | romance | huis | ishvar | toespraak | komt uit | 61+|groep
    genre: rom5 ero1 hor0 sus2 act0 int0 kom1 tra1
    doelen: nieuwheid 0.57, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.70, kosten 0.14; marginale winst 0.522
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-ishvar-drieen; drager PERS-Z4-ishvar-4-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

9. VP-4-688cc826 | vervalser | horror | dorp | karrûk | ballade | faalt | 18-25|v
    genre: rom0 ero2 hor5 sus3 act1 int1 kom0 tra3
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.50, kosten 0.16; marginale winst 0.519
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite SEKS-VOLK-karruk-kampvechters; drager PERS-Z4-karruk-4-2
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

10. VP-4-1de9245d | ontdekker | tragedie | dorp | mens | toespraak | komt uit | 26-40|wisselend
    genre: rom2 ero3 hor0 sus3 act0 int1 kom0 tra5
    doelen: nieuwheid 0.57, verbondenheid 0.84, seriewaarde 0.00, lezersvraag 0.45, kosten 0.16; marginale winst 0.516
    raakt: ERF-noodtoestand; zaadje ZAAD-VERHAAL-fase3-Z35-1; wereldregel/rite RIT-zwijgende-rit; drager PER-f4-edrun
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-4;REGEL-harde-grenzen
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

```
### Test stap 8.6: vraag.py pareto 6 10
```
# 6 Markt: volken aelthir, dhurn, grauwen, ishvar, karrûk, kluwer, mens, myrrhen, oevrin, orrim, sael-mor, skerra, tharn, vathren; bestaande bogen 4, eerdere profielen 19
gewichten: verbondenheid 0.30, seriewaarde 0.25, nieuwheid 0.20, lezersvraag 0.15, kosten 0.10
kandidaten na filters: 2906; afgevallen: {'rijm': 74, 'R-verhaal_afstand': 20}; Pareto-fronten: 33 (eerste front 19 profielen)

## 10 uit het eerste front (greedy op marginale winst; niemand hierboven wordt op alle doelen tegelijk verslagen)

1. VP-6-f11fed26 | profiteur | romance | huis | mens | zelfportret | faalt | 26-40|groep
    genre: rom5 ero3 hor0 sus1 act0 int0 kom2 tra2
    doelen: nieuwheid 0.57, verbondenheid 0.92, seriewaarde 0.00, lezersvraag 0.70, kosten 0.24; marginale winst 0.570
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite RIT-veiling; drager PER-f6-selvara-jong-Z32
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust (blijft in de top-3 bij alle 10 verschuivingen van ±10%)

2. VP-6-cb5b9818 | betaler | romance | huis | mens | ballade | keert om | 61+|wisselend
    genre: rom5 ero4 hor0 sus2 act0 int0 kom1 tra2
    doelen: nieuwheid 0.43, verbondenheid 0.92, seriewaarde 0.00, lezersvraag 0.70, kosten 0.14; marginale winst 0.551
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite RIT-veiling; drager PERS-Z4-veslethi-3-1
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: close call (top-3 wisselt bij 1 van 10 verschuivingen van ±10%)

3. VP-6-b013599d | vervalser | intrige | dorp | mens | register als verteller | keert om | 61+|m
    genre: rom1 ero4 hor0 sus3 act0 int5 kom0 tra1
    doelen: nieuwheid 0.57, verbondenheid 0.91, seriewaarde 0.00, lezersvraag 0.55, kosten 0.21; marginale winst 0.549
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite RIT-veiling; drager PER-ketenmoeder
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: close call (top-3 wisselt bij 1 van 10 verschuivingen van ±10%)

4. VP-6-7c93ab86 | beslisser | survival | stad | mens | getuigenverslag | faalt | 18-25|groep
    genre: rom0 ero2 hor2 sus3 act3 int1 kom0 tra3
    doelen: nieuwheid 0.71, verbondenheid 0.92, seriewaarde 0.00, lezersvraag 0.40, kosten 0.30; marginale winst 0.547
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite RIT-veiling; drager PERS-Z4-ishvar-3-1
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: close call (top-3 wisselt bij 2 van 10 verschuivingen van ±10%)

5. VP-6-6e01008a | betaler | mysterie | wereld | mens | zelfportret | faalt | 61+|groep
    genre: rom0 ero1 hor1 sus4 act0 int3 kom1 tra3
    doelen: nieuwheid 0.57, verbondenheid 0.92, seriewaarde 0.00, lezersvraag 0.55, kosten 0.42; marginale winst 0.529
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite RIT-veiling; drager PER-grom-reus
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

6. VP-6-a65b00fa | toeschouwer | actie | huis | grauwen | ballade | komt uit | 18-25|groep
    genre: rom1 ero3 hor1 sus4 act5 int1 kom0 tra1
    doelen: nieuwheid 0.71, verbondenheid 0.72, seriewaarde 0.00, lezersvraag 0.55, kosten 0.14; marginale winst 0.528
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-grauwen-ontsluierden; drager PER-grauwen-schurk-kael
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

7. VP-6-051653b8 | betaler | thriller | huis | aelthir | kasboek | komt uit | 18-25|wisselend
    genre: rom1 ero4 hor1 sus5 act2 int2 kom0 tra2
    doelen: nieuwheid 0.57, verbondenheid 0.78, seriewaarde 0.00, lezersvraag 0.65, kosten 0.19; marginale winst 0.527
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-aelthir-glazen; drager PERS-Z4-aelthir-6-2-Z5b
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

8. VP-6-7b26f3f6 | profiteur | romance | dorp | aelthir | kasboek | faalt | 26-40|wisselend
    genre: rom5 ero2 hor0 sus1 act0 int0 kom2 tra2
    doelen: nieuwheid 0.57, verbondenheid 0.76, seriewaarde 0.00, lezersvraag 0.70, kosten 0.21; marginale winst 0.525
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-aelthir-eeuwparen; drager PERS-Z4-aelthir-6-2-Z5b
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

9. VP-6-d8a96133 | betaler | tragedie | rijk | dhurn | toespraak | keert om | 61+|v
    genre: rom1 ero0 hor0 sus2 act0 int1 kom0 tra5
    doelen: nieuwheid 0.71, verbondenheid 0.78, seriewaarde 0.00, lezersvraag 0.45, kosten 0.21; marginale winst 0.523
    raakt: ERF-ontvangst; zaadje ZAAD-VERHAAL-fase5-Z35-2; wereldregel/rite SEKS-VOLK-dhurn-mijnbroeders-Z6; drager PERS-Z4-dhurn-7-1
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

10. VP-6-84aebda4 | vervalser | actie | dorp | mens | kasboek | keert om | 41-60|v
    genre: rom0 ero1 hor0 sus4 act5 int2 kom0 tra1
    doelen: nieuwheid 0.43, verbondenheid 0.91, seriewaarde 0.00, lezersvraag 0.55, kosten 0.21; marginale winst 0.520
    raakt: ERF-markt; zaadje ZAAD-VERHAAL-fase5-Z35-1; wereldregel/rite RIT-veiling; drager PER-ves-ithrel
    mag niet breken (v_kern): BESLUIT-Z30-4;BESLUIT-Z36-4;FASE-OVERZICHT-Z36-6;REGEL-harde-grenzen;VALS-markt-Z36
    gevoeligheid: robuust buiten de top-3 (10 verschuivingen)

```
## Filtertest en gewichten
```
WEIGERT | hoofdpersoon 16 | harde lijn: hoofdpersoon jonger dan 18
WEIGERT | dier als partner bij erotiek | harde lijn: dier of minderjarige in een seksuele rol
WEIGERT | minderjarige partner | harde lijn: dier of minderjarige in een seksuele rol
WEIGERT | kan niet instemmen | harde lijn: seks met wie echt niet kan instemmen
WEIGERT | dwang zonder label | harde lijn: dwang zonder label donker thema
WEIGERT | erotiek zonder wereldregel | wereld: erotiek zonder bestaande wereldregel of rite (code)
WEIGERT | volk bestaat niet in fase 4 (myrrhen) | Kern/wereld: volk myrrhen bestaat niet in 4 Noodtoestand (personage_profiel)
WEIGERT | kopie van een boog (afstand < 3) | R-verhaal_afstand: afstand 1 tot VERHAAL-fase6-Z32
WEIGERT | onbekende vorm | as vorm: waarde sonnet niet toegestaan (verhaal_as)
controle goed profiel: door alle filters
toets.py op een db met een slecht profiel dat buiten de machine om is ingevoegd: exit 1
Nieuwe fouten: 3 {'profiel_harde_lijn': 3}
- NIEUW [profiel_harde_lijn] VP-TEST-slecht: hoofdpersoon jonger dan 18 of zonder leeftijd
- NIEUW [profiel_harde_lijn] VP-TEST-slecht: dier of minderjarige in een seksuele rol
- NIEUW [profiel_harde_lijn] VP-TEST-slecht: erotiek zonder wereldregel
UITSLAG: alle foute profielen geweigerd

# Doelprofiel dat niet kan (erotiek 5, horror 5, komedie 5 tegelijk):
# 6 Markt: volken aelthir, dhurn, grauwen, ishvar, karrûk, kluwer, mens, myrrhen, oevrin, orrim, sael-mor, skerra, tharn, vathren; bestaande bogen 4, eerdere profielen 20
gewichten: verbondenheid 0.30, seriewaarde 0.25, nieuwheid 0.20, lezersvraag 0.15, kosten 0.10; doelprofiel onmogelijk (min erotiek>=5, horror>=5, komedie>=5)
kandidaten na filters: 0; afgevallen: {'doelprofiel-minimum': 3875, 'rijm': 91, 'R-verhaal_afstand': 34}

## 0 profielen (farthest-point, eerst alle zeven posities, daarna marginale winst)


# Bradley-Terry-test: synthetische keuzes van een lezer die alleen op nieuwheid let (tijdelijke kopie, niets bewaard)
Bradley-Terry uit 104 keuzes: coëfficiënten {'nieuwheid': 2.713, 'verbondenheid': -1.597, 'seriewaarde': 0.197, 'lezersvraag': 0.173, 'kosten': 0.354} -> gewichten {'nieuwheid': 0.79, 'verbondenheid': 0.0, 'seriewaarde': 0.057, 'lezersvraag': 0.05, 'kosten': 0.103}
# swing-test
swing-gewichten: {'kosten': 0.034, 'lezersvraag': 0.138, 'nieuwheid': 0.207, 'seriewaarde': 0.276, 'verbondenheid': 0.345}
```
