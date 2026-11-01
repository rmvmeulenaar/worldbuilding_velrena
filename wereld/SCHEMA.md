# SCHEMA canon.db (vanaf ronde Z30)

**Bij twijfel wint het verhaal, behalve bij Kern.**
Harde lijnen (één regel, BESLUIT-Z30-4): alleen volwassenen (18+) in seksuele rollen; geen minderjarigen; geen dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; dwang tussen volwassenen alleen als gelabeld donker thema.

## Draagkracht
- **Kern** (89 rijen): oorzaak van de wereld, Zegel, 1-op-100, harde grenzen, hoofdbesluiten, tijdlijn-ankers. Alleen wijzigen via een nieuw BESLUIT.
- **Structuur**: mag schuiven; elke afwijking krijgt een wrijving-rij. Alles wat niet zeker is, valt hier.
- **Kleur**: vrij (catalogi, zintuigvoorbeelden, archief). Twee Kleur-rijen botsen = geen wrijving, het verhaal wint.
Regels: zie `afgeleid.py` (REGELS) en tabel `handleiding`.

## Lezen (schrijvers)
| View | Inhoud |
|---|---|
| `v_kern` | heilige rijen |
| `v_actief` | levende canon (vastgesteld + voorlopig, geen ideeënbank), schone tekst |
| `v_ideeenbank` | catalogi en skeletten (inspiratie) |
| `v_open` | open wrijvingen + open vragen |
| `v_dode_links` | verwijzingen naar niet-bestaande codes |

Hulpscript: `python3 vraag.py kern | open | tel | code <CODE> | zoek <woord> [kern|structuur|kleur]` (`DB=verhalen/canon_lees.db` voor de leeskopie).

## Tabellen en kolommen
- `canon`: alle oude kolommen ongewijzigd (`feit` = origineel). Nieuw: `draagkracht`, `ideeenbank` (0/1), `veilig_18plus` (0/1), `veilig_variant` (id's in `veiligheid_varianten`), `vervangen_door`, `feit_schoon` (feit zonder herhaald standaardlabel en zonder [Ronde…]-notities).
- `veiligheid_varianten`: de 11 labelteksten, aantal, afwijking, strippen (1 = uit feit_schoon gehaald; themalabels en Jongenshof-label blijven in de tekst).
- `verwijzing(van_tabel, van_code, naar_code, bestaat)`: uit `verwijst_naar` (tekstkolom blijft).
- `historie`: elke rondenotitie + het volledige originele feit als het verschilt van feit_schoon.
- `handleiding`: werkregels in de db zelf.
- `wrijving`, `open_vraag`, `logboek`: ongewijzigd van vorm.

## Werken
- Nooit verwijderen: nieuwe rij + oude op `voorlopig, vervangen` (+ `vervangen_door`).
- Status: vastgesteld / voorlopig / voorlopig, vervangen / vervallen.
- Na elke ronde: `python3 afgeleid.py` (herbouwt draagkracht, feit_schoon, verwijzing, historie, varianten), dan genereer.py, export.py (canon.md + ideeenbank.md), roundtrip importeer.py.

---
# Vanaf ronde Z31: robuust tegen kettingschade

**Harde lijnen gelden voor elke rij, met of zonder vlag.** `veilig_18plus = 0` betekent alleen: in deze rij stond geen standaard-veiligheidslabel (meestal een niet-seksuele rij). Het betekent **nooit** dat de grens hier niet geldt. (Zelfde tekst in handleiding HANDL-Z30-2/HANDL-Z31-2 en bovenaan canon.md.)

## Lagen (MVVM, licht)
| Laag | Wat | Waar |
|---|---|---|
| Model | de bron: tabellen `canon` (kolom `feit` = origineel), `wrijving`, `open_vraag`, `logboek`, `handleiding`, `anker`, `naam_markering`, `toets_uitzondering`, `wijziging`, `schema_versie`; plus `draagkracht_handmatig` | canon.db |
| ViewModel | rekent en filtert, nooit met de hand bewerken: `afgeleid.py` (draagkracht, feit_schoon, veilig_*, vervangen_door, verwijzing, historie, veiligheid_varianten) en de views `v_kern`, `v_actief`, `v_ideeenbank`, `v_open`, `v_dode_links` | afgeleid.py, views |
| View | wat een schrijver of agent leest: `canon.md`, `ideeenbank.md`, `bijbel/*.md`, `WERELD_VELMARA.md`, selecties per verhaal (`vraag.py`, `scene.py`, `verhalen/canon_lees.db`) | gegenereerd |
Regel: verander alleen het Model; draai daarna de pijplijn hieronder, de rest volgt.

## Nieuw in Z31
- `canon.draagkracht_handmatig` (Kern/Structuur/Kleur): wint altijd van de berekende draagkracht; `afgeleid.py` schrijft hem nooit. Een vervangen/vervallen rij wordt nooit Kern (toets meldt het). De bronrijen van de getal/jaar-ankers staan hierop op Kern (BESLUIT-Z16-8, -Z16-9, -Z18-3, -Z26-1, REGEL-verhouding-Z12, BESLUIT-Z30-1, PER-liora-profiel).
- `anker(sleutel, waarde, bron_code, toelichting, patroon, bereik)`: bron van waarheid voor sleutelgetallen, jaren en namen (26 stuks). `patroon` = regex waarmee `toets.py` levende rijen vindt die een andere waarde noemen.
- `naam_markering(naam_a, naam_b, codes, soort, status, wrijving, toelichting)`: bewuste erfnaam/echo, zelfde persoon, of open botsing. Gemarkeerde paren laten de naamtoets niet falen.
- `toets_uitzondering(toets, code, detail, reden, wrijving)`: bekende bevindingen die met een wrijving geregistreerd zijn (baseline). Alleen NIEUWE bevindingen laten de toets falen.
- `wijziging(ronde, code, soort, veld, oud, nieuw, datum, bron)`: licht event sourcing. Gevuld uit vervangen_door, historie-notities, gesloten wrijvingen en het logboek; vanaf Z31 schrijft elke ronde zijn eigen regels. Oudere rondes: ronde/datum vaak '?' (niet betrouwbaar te reconstrueren).
- `schema_versie` + `migraties/NNN_naam.py` + `migraties/migreer.py`: structuurwijzigingen alleen via een genummerd, idempotent script.

## Scripts
- `python3 toets.py [db] [--rapport f.md] [--json f.json] [--alles]`: exit 1 bij een nieuwe fout. Controles: kern_vastgesteld, handmatig_waarde, handmatig_kern, vervangen_door, dode_link, harde_grens (per zin, labels en ontkenningen eruit), anker, leeftijd (TOESTAND jaar-leeftijd constant en gelijk aan geboorte-anker), na_dood (jaar > sterfjaar zonder nadood-woorden), naam (gelijke/bijna gelijke voornamen zonder markering).
- `python3 vraag.py wie-leunt-op <CODE> [diepte] | kern | open | ideeen [woord] | anker | toets | code <CODE> | zoek <woord> [dk] | tel`
- `python3 roundtrip.py`: WERELD_VELMARA.md -> importeer -> migraties -> afgeleid -> vergelijk alle tabellen (zonder id) en views.

## Pijplijn na elke ronde
backup -> r_ZNN.py -> `python3 migraties/migreer.py` -> `python3 afgeleid.py` -> `python3 toets.py` (moet 0 geven) -> `python3 genereer.py` -> `python3 export.py` -> `python3 roundtrip.py` (moet 0 geven) -> kopie naar `verhalen/canon_lees.db`.

---
# Vanaf ronde Z33: canon-motor als meetlat

Meetlat: skill canon-motor (8 metingen). Meten: `python3 z33/meet.py canon.db uit.json` (koude lezer: `z33/koude_lezer.py`). Voor/na: `z33/scorekaart.md`.

## Model (bron, met de hand of via besluit; geëxporteerd in WERELD_VELMARA.md)
- `regel(code, domein, omschrijving, sql_test, bron, goedgekeurd_door, status, niveau)`: de tests. `sql_test` = SELECT die (code, detail) per overtreding geeft, of `py:<naam>` (controle in toets.py). `niveau` fout (ronde faalt bij een nieuwe bevinding) of signaal (alleen melden). 22 regels (17 fout, 5 signaal).
- `boog(code, fase, boek, hoofdpersoon, leeftijd_hoofdpersoon, geslacht_hoofdpersoon, romance, erotische_sleutelscene, terugkerend_motief, noodoplossing, wie_betaalt, toon, vorm, afloop, bron, status, voorstel, voorstel_status)`: mal-breker. Motief: de familie staat vóór de `/` (bijv. `register/...`).
- `personage(code, naam, per_code, fase, rol, eigen_fout, soort_fout, wie_betaalt, zelfbedrog, daarna_doet, bron, status, voorstel, voorstel_status)`: status `uit canon`, `deels uit canon` of `profiel, geen personage`.
- `zaadje(code, wat, geplant_in, oogst_in, status, bron)`: causaliteit (geland / open / bewust dood).
- `anker`: uitgebreid naar 69 (fasenamen 0-7, jaren, geboortejaren en namen van hoofdpersonen).

## ViewModel (afgeleid, `afgeleid_motor.py`, aangeroepen door `afgeleid.py`)
- `canon.bron`, `bron_soort`, `besloten_door`, `besloten_op`: herkomst. `onbekend` = niet eenduidig af te leiden (nooit verzonnen).
- `relatie(van_code, soort, naar_code, bron)`: leunt_op, vervangt, sterft_in, geboren_in (`JAAR:n`), woont_in (`REG-`), partner_van, ouder_van, kind_van, broer_zus_van.
- `anker_kopie(sleutel, code, waarde_in_rij, afwijkt, draagkracht, risico)`: levende kopieën van ankerwaarden (via patroon) met een risicoscore.

## Views
`v_impact` (code → wie leunt erop, 2 niveaus), `v_anker` (anker + bron + aantal kopieën), `v_actief_anker` (v_actief + de ankerwaarden die de rij kopieert: lees hier het getal, niet uit de tekst), `v_herkomst_gat`, `v_mal` (mal_score 0-5), `v_personage_gat`, `v_zaadje_open`.

## Constraints (triggers, migratie 003)
Geen DELETE op canon, wrijving, open_vraag, regel, boog, personage, zaadje. Status alleen vastgesteld / voorlopig / voorlopig, vervangen / vervallen. Draagkracht en draagkracht_handmatig alleen Kern / Structuur / Kleur. vervangen_door moet bestaan. (importeer.py maakt een kale db; de triggers komen erbij via `migraties/migreer.py`.)

## vraag.py (nieuw)
`impact <CODE>`, `anker-waarde [sleutel]`, `kopieen [n]`, `herkomst <CODE>`, `mal`, `personage [naam]`, `zaadjes`, `regels`.

## Pijplijn (ongewijzigd, plus r_Z33)
backup -> r_ZNN.py -> migreer -> afgeleid -> toets (exit 0) -> genereer -> export -> roundtrip (0) -> kopie naar verhalen/canon_lees.db.

## Ronde Z34: geen sjablonen (migratie 004)
- `sjabloon_familie(sig, grootte, prefixen, markering, voorstel, voorbeeld)`: elke gemeten sjabloonfamilie (>=5 levende rijen met dezelfde signatuur: label-skelet `L:Geur|Geluid|...` of openingsskelet `O:eerste 4 woorden`, getallen als #). Eenmalig vastgelegd uit de nulmeting van Z34.
- `sjabloon_lid(sig, code, markering)`: lidmaatschap. markering `ideeenbank` -> afgeleid.py zet ideeenbank=1 en Kleur (nooit Kern, nooit over draagkracht_handmatig heen). Andere markeringen: `al ideeenbank`, `kern (niet aanraken)`, `kleur`, `structuur-voorstel`.
- view `v_sjabloon`; boog heeft nieuwe kolommen `verteller` en `tempo`.
- Regels: R-sjabloon_nieuw (fout), R-boog_uniek (fout), R-personage_fout_uniek (fout), R-herhaling_categorie (signaal). Drempels in z34/herhaling.py: FAM_MIN=5, JACC=0.5 (woord-3-grepen), CAT_DREMPEL=0.35; nieuwe rijen = ronde>=63.
- Meten: `python3 z34/meet.py canon.db uit.json`.
- Pijplijn: backup canon_backup_Z34.db -> r_Z34.py -> migreer -> afgeleid -> toets (0) -> genereer -> export -> roundtrip (0) -> kopie verhalen/canon_lees.db.

## Ronde Z35 (migratie 005_z35_rijm, ronde-nummer 64)
- `personage_toestand`: één rij per moment per personage (geboren/knooppunt/actief/later/overleden), kolommen jaar, leeftijd, rol, regio, wil, geheim, verandert, aanname (0/1) + aanname_reden, bron = oude TOESTAND-code. Oude TOESTAND-rijen: 'voorlopig, vervangen'.
- `levensduur`: per volk (aelthir 900 canon, orrim onbekend, '*' 70 aanname).
- `v_personage_tijdlijn`: toestand plus berekend sterfjaar (relatie sterft_in > levensduur volk > '*'; aanname=1).
- `fase_rijm` + boog-kolommen beslisser_as, betaler_as, vervalst_as, ontdekt_as, schaal, herkenbaar, zintuig, haak, synopsis_code; view `v_rijm`; regels rijm_assen, rijm_erfenis, rijm_spiraal, rijm_binnen_fase.
- `kernscene`: kernscènes per boog (uit de synopsen gehaald).
- `v_schrijfpakket` / `python3 vraag.py schrijfpakket <BOOG>`: verplicht vertrekpunt voor schrijven (HANDL-Z35-2). Ook: `vraag.py rijm`, `tijdlijn <PER>`, `keuzes [soort]`.
- `keuze`: keuzelijst voor Rogier (wrijving, voorstel kern/breuk/hoofdverhaal, herkomst top-50).
- `canon.bron_spoor` (afgeleid): het opdrachtbestand van de ronde; spoor, telt niet als bron.
