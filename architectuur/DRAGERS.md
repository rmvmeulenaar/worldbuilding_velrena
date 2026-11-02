# Dragers: fantasieën mogelijk maken in elk tijdperk (ontwerp Z47/Z48)

Opdracht van Rogier (2 november 2026): "je moet fantasieën mogelijk maken", "de database rijker maken", "intern consistent".

## Het idee
Elke erotische fantasie hangt af van iets dat bestaat. Bijvoorbeeld de gave, een volk, een instituut of een stof. Na 801 verdwijnt veel daarvan (`LOT-Z44-*`). Een **drager** is iets nieuws in een later tijdperk dat dezelfde behoefte vervult. Het volgt uit de regels van de wereld, en het maakt de fantasie daar weer **echt**. Zo groeit de wereld waar ze anders leeg zou raken.

Datamodel (geen nieuwe bron, alleen canonrijen en afgeleide tabellen):
- Een drager is een canonrij `DRAGER-Z48-<behoefte>-<fase>`, categorie `Drager`, met epistemiek "voorstel".
- Haar `verwijst_naar` bevat drie dingen:
  1. de LOT- of GEB-rij die ze opvolgt (de **behoefte**);
  2. minstens één bestaande rij die het mechanisme levert (de **bron**);
  3. de FASE-rij van haar tijdperk.
- Een fantasie hangt af van een behoefte via een link naar die LOT-rij (`r_Z47.py`).
- `afgeleid_motor.fantasie_tijd()` rekent het per tijdperk uit. Een fantasie is **echt** als haar behoefte nog bestaat, of als er voor die behoefte een drager geldt. Een drager geldt vanaf haar eigen tijdperk tot de volgende drager voor dezelfde behoefte.

## Ontwerpcriteria
| # | Criterium | Waarom | Hoe getoetst |
|---|---|---|---|
| 1 | **Afleiding**: elke drager volgt uit een bestaande, levende bronrij die het mechanisme levert (volk, stof, ritueel, voorwerp). | Verzinnen mag, maar de canon beslist of het past. | regel `R-drager_bron` (fout): een drager zonder levende bron naast de behoefte en de fase |
| 2 | **Tijd**: een drager bestaat niet eerder dan haar bron. Haar tijdperk ligt op of na het verleden van de bron. | Geen anachronisme. | regel `R-drager_tijd` (fout): het tijdperk van de drager ligt vóór dat van haar bron |
| 3 | **Wereldregels**: geen kracht zonder Makerstechniek of biologie (BESLUIT-Z42-1, TECHNO-REGEL-V4-Z42). Na 801 werkt alles met een ja (BESLUIT-Z12-2). | Rijkdom is raarheid die klopt. | lezing door de architect; kracht zonder ja is alleen spel of een gelabeld donker thema |
| 4 | **Verval**: elke drager is zwakker of anders dan het origineel en zegt wat ze niet meer kan. | Verwondering zit in verlies. | lezing; staat in de tekst van de drager |
| 5 | **Prijs**: elke drager kost iets. | Elke oplossing wordt het probleem van de volgende fase. | lezing; staat in de tekst |
| 6 | **Harde lijnen**: alleen volwassenen; geen dieren in een seksuele rol; nooit zonder echte instemming. | Altijd, op elk warmteniveau. | `R-harde_grens` (bestaand) |
| 7 | **Uniek**: geen sjabloonzinnen; per behoefte en tijdperk hoogstens één drager. | Rijkdom, geen herhaling. | `R-sjabloon_nieuw` (bestaand) en de primaire sleutel in de afgeleide tabel |
| 8 | **Verleden, smaak, toekomst**: waar het vandaan komt, hoe het voelt, wat ermee gebeurt. | Principe uit CLAUDE.md. | lezing |
| 9 | **Dekking**: elke erotische fantasie kan in elk tijdperk 9 tot en met 16 echt of als spel; onmogelijk alleen als er geen aannemelijke drager is. | Ruimte voor erotische verhalen in elk tijdperk. | `v_fantasie_matrix` en het signaal `R-fantasie_onmogelijk` |
