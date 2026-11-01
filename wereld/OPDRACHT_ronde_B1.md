# Opdracht ronde B1: Rogier volgt mijn 15 suggesties uit BESLISSEN_belangrijk.md
Lees /workspace/wereld/BESLISSEN_belangrijk.md. Rogier kiest voor alle 15 beslissingen de SUGGESTIE (zoals in het document: 1 B, 2 A, 3 B, 4 C, 5 B, 6 B, 7 C, 8 B, 9 B, 10 B, 11 B, 12 C, 13 B, 14 A, 15 C). Verwerk in canon.db:
- Backup canon_backup_B1.db eerst. Niets verwijderen: rijen die de gekozen lijn tegenspreken krijgen status 'voorlopig, vervangen' (of 'vervallen' alleen als ze echt dubbel zijn) met reden. Gekozen rijen en de beslissingen zelf krijgen status 'vastgesteld' (reden: Rogier volgt suggestie, datum 2026-10-30). Nieuwe BESLUIT-1..15-rijen (code BESLUIT-n) met de gekozen variant, reden, en verwijst_naar de rijen die eraan hangen.
- Pas inconsistente rijen aan (nieuwe rij schrijven, oude 'voorlopig, vervangen'): o.a. GEH-zegel (Makers bouwden, priesteressen ontdekten en kaapten), Kharvos-oorzaak (eigen zaaischip met machines), Ves-Anath 1 op 60, bestuur dubbel (Orde beheert zaad en register, huizen land en geld), bloedafstand deels waar, enz. Ruim NAV-wormwording (voorlopig, vervangen) op.
- Sluit de bijbehorende open vragen en wrijvingen met reden en nummer van het besluit.
- Voeg verhaalhaken toe waar het besluit die oplevert (minstens 3 per besluit voor 1, 2, 3, 5, 6).
- Zet de scènelijn voor boek 1 vast (3 volken diep, rest als kleur) in een rij BOEK1-scenelijn.
- genereer.py, importeer.py roundtrip, grep-controle, logboek, genre-balans. Elke nieuwe rij ook een techniek-label.
- Regels: alleen 18+, geen minderjarigen, geen dieren, geen seks zonder instemming.
Rapporteer kort in het Nederlands: aantallen, welke rijen zijn vastgesteld/vervangen, welke nieuwe wrijvingen door de keuzes ontstonden en 5 mooiste voorbeelden.
