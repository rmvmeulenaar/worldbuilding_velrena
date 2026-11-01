# Opdracht ronde Z35 (werkbrief)

Volledige opdracht: `OPDRACHT_architect_Z35.md`. Deze ronde: stap 1 t/m 6. Stap 7 t/m 10 zijn voor later; niets hier mag ze blokkeren.

Aanleiding: Rogier: "je moet de kern verhalen veranderen". Waar de rijmregel botst met Kern komen concrete voorstelrijen (voorlopig, met impact) in de tabel `keuze`, zodat hij in één keer kan goedkeuren.

Werkwijze: backup `canon_backup_Z35.db`; migratie `migraties/005_z35_rijm.py`; idempotent script `r_Z35.py` (ronde 64); hulpbestanden in `z35/`. toets.py na elke stap exit 0; roundtrip 0 verschillen; tweede run voegt niets toe; terugdraaitest Z34→Z35.

Harde regels: niets verwijderen (vervangen + vervangen_door); geen Kern-inhoud wijzigen; elke wijziging in `wijziging`; roman ongemoeid (md5 voor/na); geen sjablonen; bij twijfel NULL, niet gokken.
