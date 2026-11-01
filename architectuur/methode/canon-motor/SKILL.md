---
name: "canon-motor"
description: "Ontwerp, keur, verbouw of voed een kennissysteem dat consistent moet blijven terwijl het groeit (verhaalwereld, protocollen, dossier, website, regelset). Gebruik bij database-architectuur, consistentie, scorekaart, kennis enten, saturatie of 'kan ik dit veranderen zonder dat alles breekt'."
---

# Canon-motor

Een canon is elke grote verzameling onderling verbonden kennis die consistent moet blijven terwijl eraan gewerkt wordt: een verhaalwereld (Velmara), behandelprotocollen (Radiance, PVI), een juridisch dossier, een website, een film, een regelset. Het probleem is in elk domein hetzelfde: één wijziging mag geen kettingschade geven. Deze skill is de methode; de vakkennis komt per domein als regelset.

**Het principe in één zin:** leg elke waarheid één keer vast, geef haar een gewicht en een bron, en laat het systeem zelf controleren dat alles wat ervan afhangt blijft kloppen.

Verwant: `narrative-world-architect` (verhaalspecifiek, draait bovenop deze motor), `software-architect` (stackkeuzes), `clinical-protocol-builder` (medische inhoud), `leesmodel` (lezersmodel bij boeken).

## Fundament: de canon is een stelsel vergelijkingen

De canon beschrijft geen stappen maar verbanden (declaratief, constraint-based). Zoals bij algebra blijft de formule hetzelfde en los je op naar wat je zoekt. Alle bewegingen hieronder zijn "oplossen naar een andere onbekende" op hetzelfde stelsel.

- **Nieuw feit** dat iets nieuws zegt = nieuwe onafhankelijke vergelijking: de *rang* stijgt.
- **Bevestiging** = vergelijking die al volgt uit de andere: rang gelijk, zekerheid omhoog.
- **Tegenspraak** = strijdig stelsel: geen oplossing tot de foute term gevonden is.
- **Saturatie** = nieuwe vergelijkingen verhogen de rang niet meer.
- **Onzekerheid:** kennis is zelden exact. Elk feit draagt een gewicht (zekerheid) en een bron; bijwerken gaat Bayesiaans: onafhankelijke bevestiging verhoogt, tegenspraak verlaagt. Algebra met onzekerheid.

Praktisch: Datalog of SQL-views bovenop SQLite doen dit letterlijk: regels één keer, vraag vanuit elke kant ("wanneer stierf Ysa?" en "wie stierf voor jaar 0?" gebruiken dezelfde regels).

## Kerninzicht: structuur zonder vakkennis, juistheid met bron

Structuur is domeinonafhankelijk; juistheid niet. Een architect kan zonder vakkennis toetsen of een canon goed gebouwd is (5 van de 6 datakwaliteitsdimensies). Juistheid toets je tegen bronnen via de kennislaag, en vakkennis bepaalt twee dingen: wat Kern is en welke regels getest worden. Consistent fout is nog steeds fout, maar dan overal tegelijk. Vakkennis kan in het systeem gebouwd worden (kennislaag, werkwijze D), mits met bron en menselijke goedkeuring.

## Deel 1: vorm van de kennis (negen ontwerpprincipes)

1. **Eén bron per feit** (single source of truth, DRY, normalisatie). Een feit staat op één plek; elders alleen een verwijzing (code). Nooit een getal, jaartal, prijs of dosis kopiëren.
2. **Entiteiten en relaties expliciet.** Graafmodel: personen, plekken, gebeurtenissen, protocollen, artikelen, pagina's zijn entiteiten; verbanden zijn rijen in een relatietabel. Geen graafdatabase-product nodig; SQLite met een relatietabel volstaat tot ruim 100.000 rijen.
3. **Draagkracht.** Elk feit krijgt Kern, Structuur of Kleur. Afhankelijkheden lopen één kant op (dependency rule): Kleur leunt op Structuur, Structuur op Kern, nooit andersom.
4. **Herkomst bij elk feit** (audit trail). Bron, brontype, wie besloot, wanneer. Kern 100%, Structuur ≥90%.
5. **Afleiden, niet overschrijven.** Leeftijden, tussenliggende jaren, tellingen, samenvattingen worden berekend door een script, nooit met de hand geschreven.
6. **Regels die zichzelf testen.** Invarianten draaien na elke wijziging; een ronde met falende tests wordt niet geaccepteerd.
7. **Wijzigingen als gebeurtenissen** (event sourcing, versiebeheer). Nooit wissen. Oude rij krijgt status vervangen + `vervangen_door`. Momentopname per ronde; terugdraaien zonder handwerk.
8. **Data, logica, weergave gescheiden** (MVVM). Model = tabellen; ViewModel = afleidscript + views; View = exports en selecties voor schrijvers, agents of een site. Je wijzigt alleen het Model.
9. **Tegenspraak is een object.** Botsingen worden vastgelegd als wrijving-rij met status, niet weggepoetst.

## Deel 2: gedrag terwijl het draait (acht principes)

Deel 1 is de vorm; dit is wat er gebeurt in de tijd. Ook domeinonafhankelijk. Stel bij elk systeem deze acht vragen en laat agents het antwoord bouwen.

1. **Toestanden en overgangen** (state machine). Welke toestanden, welke overgangen zijn toegestaan? Patiënt: intake → consult → behandeling → nazorg. Afspraak: aangevraagd → bevestigd → uitgevoerd / geannuleerd. Boek: wat weet elk personage bij begin en eind van een hoofdstuk.
2. **Gelijktijdigheid.** Wat als twee partijen tegelijk hetzelfde wijzigen? Transacties, locks; nooit twee bouwers op één schema. Bij boeken: parallelle verhaallijnen synchroon in de tijd.
3. **Falen halverwege.** Alles of niets (atomair); twee keer uitvoeren = één keer (idempotent).
4. **Grenzen en contracten.** Elk onderdeel zegt wat erin mag en eruit komt en controleert dat aan de grens. Formulier zonder onmogelijke waarden; hoofdstuk met vaste in- en uitgang (wat lezer weet, welke nieuwe vraag).
5. **Rechten** (least privilege). Wie mag wat lezen en wijzigen. Bij medische en juridische gegevens: AVG.
6. **Zichtbaarheid.** Logs, monitoring, analytics, lezersmodel: achteraf zien wat gebeurde, wanneer, waarom.
7. **Prestaties en schaal.** Werkt het bij tien keer zoveel? Meestal minst urgent bij kennissystemen.
8. **Fouten onmogelijk maken** (poka-yoke). Ontwerp zo dat de fout niet kán: contra-indicaties die je niet kunt overslaan, beatplan dat elk zaadje afdwingt.

## Deel 3: de negen bewegingen (zelfde stelsel, andere onbekende)

| Beweging | Richting | De vraag | Voorbeeld |
|---|---|---|---|
| Opbouwen | kern → buiten | wat is Kern, wat volgt eruit? | nieuwe wereld, nieuw protocol |
| Keuren | meten, niets veranderen | is dit goed gebouwd? | scorekaart |
| Corrigeren | symptoom → bron | waar zit de fout echt, wat hangt eraan? | één bron herstellen, impactlijst nalopen |
| Verbouwen | vorm wijzigen, inhoud houden | kan het anders ingedeeld zonder verlies? | migratie naar nieuw schema |
| Bewust breken | kern → gevolgen | wat valt om als dit niet meer waar is? | plotwending; nieuwe richtlijn maakt oude dosis ongeldig |
| Simuleren | waarde invullen | wat volgt uit keuze A vs B? | twee eindes; prijsstrategie A of B |
| Reconstrueren | sporen → kern | wat moet waar zijn om alle sporen te verklaren? | tijdlijn uit e-mails en uitspraken |
| Samenvoegen | twee stelsels → één | waar botsen ze, wie wint? | werk van twee agents; twee protocolversies |
| Afslanken | niet-dragend eruit | wat leunt nergens op en wordt nergens gebruikt? | gegenereerde catalogi; verouderde pagina's |

**Aanvallen** is keuren op het stelsel van een ander: modelleer het dossier van de tegenpartij (elke stelling een feit met bron, elke datum een toestand) en draai de tests. Zelftegenspraak, claims zonder bron, onmogelijke data, botsing met eerder ingenomen standpunt. Niets verzinnen; alleen laten zien waar hun eigen bouwwerk niet sluit. Een tegenspraak die het systeem vindt, is moeilijker weg te praten dan een die jij aanwijst.

## Deel 4: enten en saturatie

Doel: een kenniskwekerij, geen kennisstapel. Nieuwe kennis wordt eindeloos op de stam geënt; het systeem weet waar elke tak hoort, of hij aansluit of botst, en hoe vol elke tak is.

### De entprocedure (elke nieuwe bron, altijd dezelfde vier stappen)
1. **Extractie:** feiten, entiteiten, relaties uit de bron.
2. **Matchen** (entity resolution): bestaat dit al, ook onder een andere naam of spelling? De stap waar de meeste systemen falen; zonder deze stap ontstaan dubbelingen (drie Mira's). Bij twijfel: als wrijving vastleggen, niet gokken.
3. **Classificeren:** elk binnenkomend feit is *nieuw*, *bevestiging*, *verfijning* of *tegenspraak*.
4. **Opslaan met herkomst:** bron, brontype, datum, draagkracht, gewicht.

### Saturatie meten
- **Nieuwheidsratio per bron:** nieuw / (nieuw + bevestiging), uitgezet over opeenvolgende bronnen. Curve naar 0 = verzadigd.
- **Bevestigingsgraad per feit:** aantal onafhankelijke bronnen. Eén = bewering; drie onafhankelijke = feit. Werkt als zekerheidsgewicht.
- **Wrijvingsratio per ronde:** stijgend = niet verzadigd; je zit op de grens van een nieuw gebied of de bronnen zijn het oneens.
- **Competentievragen** (ontologie-engineering): schrijf vooraf de vragen die het domein moet kunnen beantwoorden; meet % beantwoord. Sterkste meetlat; dezelfde als de koude-lezertoets.
- **Saturatie is per gebied, niet totaal.** De verzadigingskaart toont waar het dun is: dat is de onderzoeksagenda, automatisch gegenereerd.

### Twee valkuilen bij saturatie
- **Bubbel:** alle bronnen van één type (alleen fabrikantstudies, alleen één partij) geeft valse verzadiging. Meet ook brondiversiteit.
- **Gegenereerde kennis is altijd nieuw:** LLM-catalogi leveren eindeloos nieuwheid, de curve daalt nooit. Tel voor saturatie alleen externe bronnen en besluiten, nooit generatie.

## Draagkracht per domein

| | Verhalen | Behandelingen | Juridisch | Website | Film |
|---|---|---|---|---|---|
| Kern | oorzaak van de wereld, harde grenzen, ankerjaren, hoofdbesluiten | contra-indicaties, maximale doses, wettelijke eisen | vastgestelde feiten, bewijsstukken, wetsartikelen | medische claims, prijzen, juridische teksten | wereldregels, personages, tijdlijn |
| Structuur | personages, tijdlijn, bogen | protocollen, indicaties, combinaties | stellingen, tijdlijn van de zaak | pagina's, navigatie, behandeltijden | scènes, sets, kostuums, rekwisieten |
| Kleur | zintuigdetails, catalogi, skeletten | toon, marketingtekst | retoriek, formuleringen | copy, beeld | licht, muziek, toon |
| Herkomst | BESLUIT-rij, hoofdstuk | bijsluiter (CBG/DailyMed), richtlijn, studie | productie-/bijlagenummer, ECLI, artikel | richtlijn, prijsbesluit | script, besluit regisseur |
| Voorbeeldtest | niemand handelt na zijn dood | dezelfde dosis op elke pagina; geen protocol dat een contra-indicatie negeert | elke claim heeft een bron; geen stelling tegen eerder standpunt | één prijs per behandeling overal | wond niet genezen in volgende scène; rekwisiet niet vóór aankoop |

Regel voor schrijvers en agents: **bij twijfel wint het werk (verhaal, behandeling, stuk), behalve bij Kern.** Kern verandert alleen via een nieuw besluit. Twee Kleur-rijen die botsen = geen wrijving, de nieuwste wint.

Waar de motor niet past: pure ideeënvorming en smaak (alles Kleur; consistentie schaadt), systemen met miljoenen transacties per dag (echte software-engineering), kennis die sneller verandert dan je kunt keuren (nieuws, prijzen: daar is de bron het systeem). Bestaande volwassen software (boekhouding) niet nabouwen; de motor keurt dan alleen de regels (kostenverdeling, btw-regels). Vuistregel: telt het als het niet klopt, en verandert het trager dan je eraan werkt? Dan past de motor.

## Kernschema (SQLite)

```sql
entiteit(code PK, soort, naam, draagkracht CHECK(draagkracht IN ('kern','structuur','kleur')),
         draagkracht_handmatig INTEGER DEFAULT 0,  -- 1 = script raakt indeling nooit aan
         status CHECK(status IN ('vastgesteld','voorlopig','vervangen','vervallen')),
         vervangen_door REFERENCES entiteit(code))
bron(code PK, titel, brontype, datum, extern INTEGER, onafhankelijk_van)   -- extern 0 = gegenereerd
feit(id PK, entiteit_code REFERENCES entiteit(code), kenmerk, waarde,
     bron REFERENCES bron(code), gewicht REAL,            -- zekerheid 0-1
     classificatie CHECK(classificatie IN ('nieuw','bevestiging','verfijning','tegenspraak')),
     besloten_door, ronde)
relatie(van_code, soort, naar_code, bron)          -- graaf; FK's aan
regel(code PK, domein, omschrijving, sql_test, bron, goedgekeurd_door, status)
competentievraag(code PK, gebied, vraag, verwacht_antwoord_code, beantwoordbaar INTEGER)
wrijving(code PK, betrokken_codes, beschrijving, status, besluit)
gebeurtenis(id PK, ronde, tijd, wat, oud, nieuw, door)  -- event log
handleiding(nr, regel)
```

Praktisch: een bestaande canon hoeft niet in één keer naar dit schema. Voeg kolommen toe naast de oude (oude blijven ongewijzigd), bouw de afgeleide kolommen met een script, en migreer per ronde. Elke structuurwijziging is een genummerd migratiescript.

Vaste views: `v_kern`, `v_actief` (levend, schone tekst), `v_ideeenbank` (catalogi, inspiratie), `v_open` (open wrijvingen en vragen), `v_dode_links`, `v_impact(code)` (wat leunt hierop), `v_saturatie` (nieuwheidsratio en competentiedekking per gebied).

## Werkwijze

### A. Keuren (bestaande canon)
Lees eerst alleen het schema en tellingen, niet de inhoud. Draai de scorekaart (hieronder) en de schema-geuren. Lever per meting: huidige waarde, streefwaarde, wat ervoor nodig is. Pas daarna inhoud, en alleen waar een meting ernaar wijst.

### B. Bouwen of verbouwen
Werk op een kopie, nooit op het origineel. Volgorde: (1) draagkracht + handmatige override, (2) herhaalde tekst en geschiedenis uit de waarheid halen naar eigen tabellen, (3) verwijzingen naar relatietabel, (4) dubbele feiten normaliseren naar één bron, (5) views, (6) tests, (7) handleiding in de db. Wijzig geen Kern-inhoud; leg tegenspraken vast als wrijving voor de eigenaar.

### C. Wijzigen (dagelijks gebruik)
Voor een Kern- of Structuurwijziging: draai `v_impact(code)` en toon de lijst vóór de wijziging. Wijzig de ene bron. Draai het afleidscript, dan alle tests. Faalt er iets: oplossen of als wrijving vastleggen, nooit stil laten staan.

### D. Kennislaag vullen (tweesleutelprincipe)
De machine haalt regels uit gezaghebbende bronnen (bijsluiters, richtlijnen, wetten.overheid.nl, rechtspraak.nl, of bij verhalen de besluiten van de auteur) en zet ze klaar met bron en datum. Een mens met vakkennis keurt elke Kern-regel goed vóór die afdwingt. Een regel zonder bron komt nooit in Kern: een fout in de kennislaag wordt overal tegelijk afgedwongen met het gezag van "dit is de regel".

### E. Enten (nieuwe bron toevoegen)
Volg de entprocedure (Deel 4). Rapporteer na elke ent: aantal nieuw / bevestiging / verfijning / tegenspraak, nieuwe wrijvingen, en de verschuiving in `v_saturatie`. Stel de volgende bron voor op basis van het dunste gebied.

## Scorekaart (de acht metingen + saturatie)

1. **Veranderproef:** verander één ankerfeit; op hoeveel plekken moet iets mee? Streef: 1.
2. **Duplicatiegraad:** hoe vaak staan ankerfeiten letterlijk herhaald? Streef: één keer als feit, elders verwijzing.
3. **Dode links:** verwijzingen naar niet-bestaande codes. Streef: 0.
4. **Herkomstdekking:** % Kern en Structuur met bron. Streef: 100% / ≥90%.
5. **Tests:** aantal falende invarianten zonder open wrijving. Streef: 0.
6. **Roundtrip:** export → import → vergelijk rij voor rij. Streef: 0 verschillen.
7. **Terugdraaien:** terug naar een eerdere ronde en vooruit, zonder handwerk. Streef: werkt.
8. **Koude lezer:** verse agent krijgt alleen views + handleiding en tien vragen over Kern. Streef: 10/10. Fouten wijzen aan waar de structuur onduidelijk is.

Plus bij een groeiende canon: **saturatiekaart** (nieuwheidsratio en competentiedekking per gebied, brondiversiteit, aandeel gegenereerd vs extern).

Zachter: consequente namen, één manier om iets te doen, handleiding in vijf minuten te snappen, saai schema.

## De zes datakwaliteitsdimensies (DAMA / ISO 8000)

Volledigheid, uniciteit, consistentie, validiteit, tijdigheid: toetsbaar zonder vakkennis. Juistheid: toetsbaar tegen bronnen via de kennislaag.

## Schema-geuren (zichtbaar zonder de inhoud te kennen)

- Gestructureerde data in vrije tekst (lijsten met `;` in één kolom).
- Eén kolom met twee betekenissen (`status = 'voorlopig, vervangen'`).
- Dezelfde tekst honderden keren herhaald (labels, disclaimers) → één regel-rij + vlag.
- Meerdere varianten van één regel → drift; terugbrengen naar één bron.
- Geschiedenis door de waarheid heen (`[Ronde Z14: ...]` in het feitveld).
- Geen constraints, geen foreign keys: de database accepteert alles.
- Ronde aantallen per categorie (50, 60, 150): teken van generatie, niet van behoefte → markeer als ideeënbank.
- Open wrijvingen die al door een later besluit zijn ingehaald.
- Dezelfde naam voor verschillende entiteiten zonder markering als bewuste echo.
- Geen onderscheid tussen extern en gegenereerd in de herkomst (saturatie onmeetbaar).

## Domeinlaag: verhalen (aanvullend)

- **Mal-breker:** leg per boog assen vast (leeftijd en geslacht hoofdpersoon, wel/geen romance, terugkerend motief ja/nee, noodoplossing werkt/faalt, wie betaalt, toon). Test: geen twee aangrenzende bogen met hetzelfde profiel; elk motief een maximum aantal bogen.
- **Personagevelden naast wil/durft/verbergt:** de eigen fout (bij Velmara: de eigen ja namens een ander), wie daarvoor betaalt, wat het personage zichzelf vertelt, wat het daarna doet. Een hoofdpersoon zonder eigen fout is een profiel, geen personage.
- **Drie lagen consistentie:** feiten (automatisch), causaliteit (elk zaadje landt of loopt bewust dood; half automatisch), thematiek (variant, geen kopie; lezen).
- **Kennistoestand per personage per hoofdstuk** (Deel 2, principe 1): wie weet wat wanneer; een personage dat iets weet wat het nog niet kan weten is een continuïteitsfout.

## Valkuilen

- **Expertsysteem-les (jaren 80):** kennissystemen stierven aan dure kennisverwerving en aan broosheid. LLM's lossen het eerste op; alleen principes 1, 3, 6 en 7 lossen het tweede op. Bouwen zonder tests en herkomst = dezelfde fout, sneller.
- **Te vroeg generiek:** maak de motor eerst in één domein echt werkend, abstraheer daarna.
- **Twee bouwers tegelijk:** nooit twee agents aan hetzelfde schema. Eén bouwt, de ander toetst onafhankelijk.
- **Script overschrijft handwerk:** afgeleide indelingen altijd met handmatige override die het script respecteert.
- **Bijbel groeit sneller dan het werk:** de canon dient het werk. Een nieuw boek, protocol of stuk dwingt de beslissingen af die genereren uitstelt; schrijven levert de echte Kern op.
- **Matchen overslaan bij enten:** zonder entity resolution groeit het aantal dubbelingen met elke bron.
- **Veiligheids- en harde grenzen** horen in één Kern-regel die op elke rij geldt, ook zonder vlag. Een vlag 0 betekent "niet van toepassing op deze inhoud", nooit "grens geldt hier niet".