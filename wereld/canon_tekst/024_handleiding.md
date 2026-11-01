# HANDLEIDING
<!-- REC handleiding -->
### HANDL-Z30-1 · Bron en status
- **code:** HANDL-Z30-1
- **onderwerp:** Bron en status
- **tekst:** canon.db is de bron. Statussen: vastgesteld (Rogiers keuze), voorlopig (voorstel), voorlopig, vervangen (oud, zie vervangen_door), vervallen (negeren). Nooit rijen verwijderen: vervang door een nieuwe rij en zet de oude op voorlopig, vervangen.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z30-2 · Harde lijnen
- **code:** HANDL-Z30-2
- **onderwerp:** Harde lijnen
- **tekst:** Harde lijnen (gelden voor elke rij, elk verhaal): alleen volwassenen (18+) in seksuele rollen; geen minderjarigen; geen dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; dwang tussen volwassenen alleen als gelabeld donker thema. Dit is één regel (BESLUIT-Z30-4) en hoeft niet in elk feit te staan. veilig_18plus = 0 betekent alleen: in deze rij stond geen standaard-veiligheidslabel (meestal een niet-seksuele rij). Het betekent NOOIT dat de grens hier niet geldt. De harde lijnen gelden voor elke rij, met of zonder vlag.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z30-3 · Draagkracht
- **code:** HANDL-Z30-3
- **onderwerp:** Draagkracht
- **tekst:** Kern: alleen wijzigen via een nieuw BESLUIT. Structuur: mag schuiven, met een wrijving-rij. Kleur: vrij. Bij twijfel wint het verhaal, behalve bij Kern. Regels (afgeleid.py): 1. Status 'vervallen' of 'voorlopig, vervangen' -> Kleur (archief, buiten beeld in v_actief). 2. Status 'vastgesteld' EN (code past op KERN_RE of categorie in KERN_CAT) EN niet NIET_KERN -> Kern. 3. Code-prefix in IDEE_PREF of categorie in IDEE_CAT -> Kleur + ideeenbank=1. 4. Code-prefix ZINT (zintuigvoorbeelden) -> Kleur. 5. Al het andere (ook voorlopig: niet zeker = Structuur) -> Structuur.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z30-4 · Kleur-regel
- **code:** HANDL-Z30-4
- **onderwerp:** Kleur-regel
- **tekst:** Botsing tussen twee Kleur-rijen is geen wrijving: het verhaal wint, pas de rij aan. Alleen botsingen met Kern of Structuur krijgen een wrijving-rij.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z30-5 · Wat lezen
- **code:** HANDL-Z30-5
- **onderwerp:** Wat lezen
- **tekst:** Schrijvers: v_kern (heilig), v_actief (levende canon, schone tekst), v_open (open wrijvingen en vragen), v_ideeenbank (catalogi: inspiratie, geen canon). Hulpscript: python3 vraag.py kern|zoek <woord>|code <CODE>|open.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z30-6 · Afgeleide delen
- **code:** HANDL-Z30-6
- **onderwerp:** Afgeleide delen
- **tekst:** draagkracht, ideeenbank, veilig_*, feit_schoon, verwijzing, historie en veiligheid_varianten worden herbouwd met python3 afgeleid.py. Dode links: view v_dode_links.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-1 · Handmatige draagkracht
- **code:** HANDL-Z31-1
- **onderwerp:** Handmatige draagkracht
- **tekst:** Kolom draagkracht_handmatig (Kern/Structuur/Kleur) heeft voorrang op de berekende draagkracht. afgeleid.py schrijft deze kolom nooit. Een vervangen of vervallen rij wordt nooit Kern, ook niet handmatig (toets.py meldt het). Zet hem met: update canon set draagkracht_handmatig='Kern' where code='...'; daarna python3 afgeleid.py.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-2 · Harde lijnen en veilig_18plus
- **code:** HANDL-Z31-2
- **onderwerp:** Harde lijnen en veilig_18plus
- **tekst:** Harde lijnen (gelden voor elke rij, elk verhaal, ook zonder label of vlag): alleen volwassenen (18+) in seksuele rollen; geen minderjarigen; geen dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; dwang tussen volwassenen alleen als gelabeld donker thema. veilig_18plus = 0 betekent alleen: in deze rij stond geen standaard-veiligheidslabel (meestal een niet-seksuele rij). Het betekent NOOIT dat de grens hier niet geldt. De harde lijnen gelden voor elke rij, met of zonder vlag.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-3 · Ankers (elk feit op één plek)
- **code:** HANDL-Z31-3
- **onderwerp:** Ankers (elk feit op één plek)
- **tekst:** Tabel anker is de bron van waarheid voor sleutelgetallen, jaren en namen (Ysa -1270/-1209, Thalen -1272/-1198/74, 11.000/3.454/7.546, 1 op 100, jaar 0, 33 hoofdstukken, 801). Schrijf in nieuwe rijen liever "zie anker thalen_sterfjaar" of de broncode dan het getal opnieuw. Verander een anker alleen via een BESLUIT; toets.py toont dan welke rijen afwijken.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-4 · Tests na elke ronde
- **code:** HANDL-Z31-4
- **onderwerp:** Tests na elke ronde
- **tekst:** python3 toets.py (of python3 vraag.py toets). Exitcode 1 = nieuwe fout: ronde niet accepteren tot het opgelost is of geregistreerd met een wrijving in toets_uitzondering. Controles: Kern alleen vastgesteld, vervangen_door aanwezig, geen dode links, harde grenzen per zin, ankers, leeftijden, niemand handelt na zijn dood, naambotsingen zonder markering.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-5 · Wie leunt erop
- **code:** HANDL-Z31-5
- **onderwerp:** Wie leunt erop
- **tekst:** Voor je een Kern- of Structuur-rij verandert: python3 vraag.py wie-leunt-op <CODE>. Die rijen gaan mee in de controle.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z31-6 · Migraties en wijzigingen
- **code:** HANDL-Z31-6
- **onderwerp:** Migraties en wijzigingen
- **tekst:** Structuurwijzigingen alleen via een genummerd script in migraties/ (python3 migraties/migreer.py), vastgelegd in schema_versie. Inhoudelijke wijzigingen krijgen een regel in tabel wijziging (ronde, code, soort, veld, oud, nieuw).
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-1 · Meetlat: canon-motor
- **code:** HANDL-Z33-1
- **onderwerp:** Meetlat: canon-motor
- **tekst:** De database wordt gekeurd met de skill canon-motor (8 metingen: veranderproef, duplicatiegraad, dode links, herkomstdekking, tests, roundtrip, terugdraaien, koude lezer). Meten: python3 z33/meet.py canon.db uit.json. Uitslag voor/na: z33/scorekaart.md.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-2 · Herkomst
- **code:** HANDL-Z33-2
- **onderwerp:** Herkomst
- **tekst:** Kolommen canon.bron, bron_soort, besloten_door, besloten_op worden afgeleid (afgeleid_motor.py) uit de code (BESLUIT-/ORIGIN-), een BESLUIT-code in reden of feit, een hoofdstuk (h..) of een Rogier-notitie. Is niets eenduidig, dan staat er onbekend: nooit verzinnen. Gaten: view v_herkomst_gat. Bron geven = in reden of feit een BESLUIT-code noemen.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-3 · Regels
- **code:** HANDL-Z33-3
- **onderwerp:** Regels
- **tekst:** Tabel regel is de bron van de tests: code, domein, omschrijving, sql_test (SELECT code, detail ... of py:naam), bron, goedgekeurd_door, status (actief/signaal/voorstel/vervallen), niveau (fout = ronde faalt bij nieuwe bevinding; signaal = alleen melden). toets.py draait alle actieve regels. Nieuwe regel = nieuwe rij; nooit verwijderen.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-4 · Relaties en impact
- **code:** HANDL-Z33-4
- **onderwerp:** Relaties en impact
- **tekst:** Tabel relatie (afgeleid): leunt_op (uit verwijst_naar), vervangt (uit vervangen_door), sterft_in/geboren_in (JAAR:n uit PER-rijen en ankers), woont_in (REG-), partner_van, ouder_van, kind_van, broer_zus_van (uit Relaties: in PER-rijen, alleen als de naam eenduidig is). Vóór een wijziging: python3 vraag.py impact <CODE> (view v_impact, tot 2 niveaus).
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-5 · Ankerwaarde in plaats van kopie
- **code:** HANDL-Z33-5
- **onderwerp:** Ankerwaarde in plaats van kopie
- **tekst:** Schrijvers lezen v_actief_anker: elke levende rij met de ankers die hij kopieert en de ankerwaarde + bronrij. Schrijf in nieuwe rijen "zie anker <sleutel>" in plaats van het getal. Kopieën en risico: tabel anker_kopie, view v_anker, python3 vraag.py anker.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-6 · Mal-breker
- **code:** HANDL-Z33-6
- **onderwerp:** Mal-breker
- **tekst:** Tabel boog: per boog geslacht en leeftijd hoofdpersoon, romance, erotische sleutelscène, terugkerend motief (familie vóór de /), noodoplossing, wie betaalt, toon, vorm, afloop. Regels: R-mal_aangrenzend (geen twee opeenvolgende bogen met hetzelfde profiel) en R-motief_max (motief in hoogstens 4 bogen). Overzicht: view v_mal of python3 vraag.py mal. Voorstellen staan in boog.voorstel (voorlopig).
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-7 · Personage, geen profiel
- **code:** HANDL-Z33-7
- **onderwerp:** Personage, geen profiel
- **tekst:** Tabel personage: eigen_fout (de eigen ja namens een ander, of een andere fout), soort_fout (per personage een andere soort), wie_betaalt, zelfbedrog, daarna_doet. Status uit canon / deels uit canon / profiel, geen personage. Gaten: view v_personage_gat; voorstel per personage (voorlopig).
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-8 · Zaadjes
- **code:** HANDL-Z33-8
- **onderwerp:** Zaadjes
- **tekst:** Tabel zaadje: wat, geplant_in, oogst_in, status (geland / open / bewust dood). Open: view v_zaadje_open. Elk zaadje landt of loopt bewust dood.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z33-9 · Constraints
- **code:** HANDL-Z33-9
- **onderwerp:** Constraints
- **tekst:** Triggers weigeren: DELETE op canon, wrijving, open_vraag, regel, boog, personage, zaadje; een status buiten vastgesteld/voorlopig/voorlopig, vervangen/vervallen; draagkracht buiten Kern/Structuur/Kleur; een vervangen_door die niet bestaat. Wil je iets weghalen: status vervallen.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z34-1 · Geen sjablonen
- **code:** HANDL-Z34-1
- **onderwerp:** Geen sjablonen
- **tekst:** Vaste regel van Rogier (BESLUIT-Z34-1): elke boog, elk personage en elke uitwerking krijgt een eigen vorm. Wie een rij schrijft, kopieert geen opening, geen rij kopjes en geen standaardzin van een andere rij. Herhaling in nieuwe rijen is een fout (regel R-sjabloon_nieuw, toets.py faalt). Velden horen in kolommen, niet als 'Label: ... Label: ...' in de tekst. Sjabloonfamilies staan in de tabel sjabloon_familie (view v_sjabloon); gegenereerde catalogi zijn als ideeënbank gemarkeerd (sjabloon_lid). Meten: python3 z34/meet.py canon.db uit.json.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z35-1 · Rijm, geen kopie
- **code:** HANDL-Z35-1
- **onderwerp:** Rijm, geen kopie
- **tekst:** De acht fasen plus 801 zijn een spiraal. Elke fase draait dezelfde motor (probleem, noodoplossing, prijs, vervalsing), maar verschuift wie beslist, wie betaalt, wat er vervalst wordt, of het uitkomt en op welke schaal; en elke fase laat iets na dat niet meer terug kan. Dat staat per fase in fase_rijm (view v_rijm), per boog in de rijm-assen van boog. Regels: R-rijm_assen, R-rijm_erfenis, R-rijm_spiraal, R-rijm_binnen_fase.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z35-2 · Schrijven alleen vanuit het schrijfpakket
- **code:** HANDL-Z35-2
- **onderwerp:** Schrijven alleen vanuit het schrijfpakket
- **tekst:** Een schrijvende agent begint niet zonder python3 vraag.py schrijfpakket <BOOG> (view v_schrijfpakket): vorm, verteller en tempo van de boog, de fase_rijm-rij, de rijm-assen van de boog, de geërfde ERF-rijen, de personages met hun eigen fout, de open zaadjes, de kernscènes en de Kern-rijen die niet mogen breken. Een synopsis is geen schrijfinstructie: ze vertelt wat er gebeurt, niet hoe het geschreven wordt.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z35-3 · Personagetijdlijn in kolommen
- **code:** HANDL-Z35-3
- **onderwerp:** Personagetijdlijn in kolommen
- **tekst:** Leeftijd, jaar, regio, rol, wil en geheim per personage staan in personage_toestand (view v_personage_tijdlijn), niet meer in TOESTAND-rijen. Leeg is NULL, nooit '-' of 'onbekend'. Een sterfjaar dat uit een levensduur volgt, wordt berekend uit tabel levensduur en draagt aanname = 1; dat is geen feit.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z36-1 · De verhalenmachine
- **code:** HANDL-Z36-1
- **onderwerp:** De verhalenmachine
- **tekst:** Een verhaal is een punt op zeven assen (verhaal_as): positie, genre, schaal, volk, vorm, afloop, hoofdpersoon. Afstand is het aantal assen dat verschilt; minder dan 3 is een kopie (R-verhaal_afstand). Bestaande bogen staan op de assen in boog_as, nieuwe ideeën in verhaal_profiel (ideeënbank, nooit Kern). Opdrachten: vraag.py bedenk, pareto, volgende, gewicht, afstand, dekking, ideeenrapport. Een run ziet alleen eerdere runs; zo voegt opnieuw draaien niets toe.
<!-- /REC -->
<!-- REC handleiding -->
### HANDL-Z36-2 · Filters zijn geen scores
- **code:** HANDL-Z36-2
- **onderwerp:** Filters zijn geen scores
- **tekst:** De harde lijnen (BESLUIT-Z30-4), de wereldregels en de Kern sluiten een profiel uit voordat er iets gescoord wordt; machine.bewaar filtert opnieuw en weigert. Pas daarna wegen de doelen (tabel doel) met de gewichtset. Gewichten en priors zijn aannames tot Rogier ze met vraag.py gewicht swing of paren vastlegt of er lezersdata is.
<!-- /REC -->

<!-- SECTIE: LOGBOEK -->
