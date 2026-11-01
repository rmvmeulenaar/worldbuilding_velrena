# Opdracht ronde D1+D2+BESTUUR+CROSSLINKS (Velmara)
Start pas NA ronde V5 (kolom `techniek` bestaat dan). Regels: alleen 18+, geen minderjarigen, geen dieren in seksuele rol, geen seks met wie niet kan instemmen. Backup canon_backup_D1.db eerst. Niets verwijderen. Idempotent r_D1.py. Alles voorlopig. Elke nieuwe rij krijgt ook `techniek` (gave/metaal/bio/zegelsteen/mengvorm/geen). Daarna genereer.py, importeer.py roundtrip, grep-controle. Rapporteer kort in het Nederlands: aantallen + 5 mooiste voorbeelden.
Regels voor interessant maken (Rogier): (1) alles raakt het kernthema (zaad, toestemming, bloedlijnen, Zegel, Makers); (2) elk item heeft een prijs en een verlies (wie profiteert, wie betaalt, wat als het ontbreekt); (3) één verhaalhaak per item voor intrige/romance/erotiek/thriller; (4) herkenbaar en toch vreemd; (5) één sterke eigenaardigheid per volk/regio, de rest gewoon; (6) zintuigen (geur, smaak, geluid). Ook humor en gewone vreugde.
## D1 basis van het leven (per volk en regio, ca. 3-5 rijen per onderwerp)
Eten en drank (incl. heilig/verboden, afrodisiaca, drugs, wat zaadkracht culinair betekent), geld en handel (wat is waardevol, prijs, beurzen, smokkel), eigen planten en dieren (per regio 5-8 soorten met functie in eten, medicijn, kleding, seks of gevaar; dieren nooit in seksuele rol), ziekten en geneeskunde.
## D2 cultuur en einde
Dood en rouw, muziek en instrumenten, spelen en sport, kunst en verhalen, humor en gewone vreugde (grappen, schelden, vriendschap, feesten), weer, sterrenhemel, kalender en feesten (hemel als aanwijzing voor de Makers/zaaischip), taal en vloeken per volk.
## BESTUUR (ontbreekt nog)
Hoe wordt Velmara bestuurd: Orde, huizen, Raad der Moeders, stadsbestuur, belasting, rechtspraak, leger/wacht, ambtenaren/register, verkiezing/erfopvolging, bestuur per volk en regio, bestuur van de gave-mannen, geheime besturen, corruptie, hoe machtswisselingen gaan. Minstens 60 rijen (BEST-), met verhaalhaken en functie.
## CROSSLINKS
Voeg veel verwijzingen toe (verwijst_naar/hangt_samen_met): minstens 600 nieuwe verbindingen tussen bestaande en nieuwe rijen: personage<->plek<->voorwerp<->gebeurtenis<->volk<->technologie<->Maker/oorsprong<->ritueel<->subcultuur<->rebel. Doe dit systematisch (op volk, regio, techniek, fase, personage) en bouw een dekkingsrapport: welke rijen nog geen verbindingen hebben (los die op) en bijbelbestand 18_crosslinks.md met het netwerk per volk/techniek/fase. Alles via bestaande codes; geen ontbrekende verwijzingen.
## Afsluiting
Wrijvingen, open vragen, logboek, genre-balans herzien (humor, gewone vreugde, eten, muziek).

## EXTRA (uit ronde V5, doe als eerste)
- Label de 65 onduidelijke rijen met de hand (zie /workspace/wereld/v5/techniek_rapport.json) en verbeter de te ruime/te krappe labels uit de steekproef (bijv. gewone personages niet op 'gave'; de Ontladingssteen en andere echte techniekvoorwerpen niet op 'geen').
- Vul de gaten uit 17_techniek-overzicht.md: gave-techniek bij Grauwen, Kluwers, Myrrhen; zegelsteen-techniek bij de 10 volken die dat missen; metaal in de fases waar het ontbreekt (als vergeten/gebruikte relikwie, niet als gewone techniek). Nieuwe voorwerpen, rijen en verhaalhaken met label.
- Pas export.py aan zodat canon.md de kolom techniek toont.
