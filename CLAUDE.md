# Velmara: regels voor elke sessie

Dit is de canon van de wereld Velmara (zegelpunk, erotische donkere fantasy met verborgen sciencefiction). De auteur is Rogier (pseudoniem Iris Calloway). Jij werkt als **bouwer** of **architect**. Rogier beslist wat canon wordt.

## Bron van waarheid
- De bron is **tekst**: `wereld/canon_tekst/`. Dat is WERELD_VELMARA.md, opgeknipt per hoofdstuk.
- `canon.db` wordt daaruit gebouwd en staat **niet** in git.
- Bewerk `canon_tekst/` nooit met de hand. Wijzig via een rondescript op `canon.db` en schrijf daarna terug met `velmara.py tekst`.
- Werkwijze per ronde, vanuit `wereld/`:
  1. `python3 velmara.py bouw`: bouwt canon.db uit de tekst en draait de toets.
  2. Het rondescript draaien (`r_Znn.py`, idempotent).
  3. `python3 velmara.py tekst`: schrijft de database terug naar canon_tekst/ en maakt bijbel/ en canon.md opnieuw.
  4. `python3 velmara.py toets`: toets.py plus de roundtrip. Er mogen 0 nieuwe fouten zijn en de roundtrip moet gelijk zijn.
  5. Commit op een eigen tak. Rogier of de architect voegt samen.
- `python3 velmara.py kaart` maakt `kaart/knopenkaart.html`: alle verhaallijnen en de knopen waaraan ze hangen.

## Harde lijnen (gelden voor elke rij, elk verhaal, elke simulatie, op elk warmteniveau)
- Alleen volwassenen (18+) in seksuele rollen, ook historisch en in rituelen. Geen minderjarigen.
- Geen dieren in seksuele rollen.
- Nooit seks met iemand die niet echt kan instemmen.
- Dwang tussen volwassenen mag alleen als gelabeld donker thema.
- Kinderen komen in de simulatie alleen voor als geboorte, opvoeding of erfenis (niet-seksueel).
- Een feeënafspraak gaat nooit over seks.

## Wat nooit mag
- **Kern** wijzigen zonder BESLUIT-rij van Rogier.
- Rijen **verwijderen**. Triggers verbieden het. Je vervangt een rij met `status='voorlopig, vervangen'` en `vervangen_door`.
- De **romantekst** aanraken. Die is van Rogier.
- **Simulatie of voorstel als canon** behandelen. Rijen met `epistemiek` 'simulatie…' of 'voorstel…' gaan automatisch naar de ideeënbank (Kleur). Alleen een besluit van Rogier zet ze in de canon.
- Een **nieuwe tabel zonder gebruik**. Elke tabel moet in dezelfde ronde door een regel, view of commando gebruikt worden.
- **Sjabloonzinnen**. Elke nieuwe rij wordt geschreven vanuit de rijen die ze raakt. De toets faalt op gedeelde openingen.

## Werkregels
- Markeren is geen oplossen. Elk klaar-als-criterium bewijs je met de query, de waarde ervoor en erna, en of het gehaald is.
- Nieuwe verwijzingen wijzen naar de levende opvolger, nooit naar een vervangen rij (`lev()` in r_Z41.py).
- Eén persoon is één knoop. Personagecodes met dezelfde stam of naam worden samengevoegd in `persoon_identiteit`, die afgeleid is.
- Een geleend geheim van een bestaand persoon wordt **kennis over** die persoon, nooit een tweede dader.
- Werk van 801 naar achteren. De hoofdlijn ligt vast: Liora, Teo, Aeron en Ithrael worden geraakt, maar hun afloop verandert niet.

## Principes (Rogier)
- **Verzinnen mag altijd, de canon beslist of het past.** De bron groeit en wordt rijker. Wat past, komt erbij.
- **Rijkdom is raarheid die klopt**: wat alleen in deze wereld kan bestaan en logisch volgt uit haar regels.
- Elk nieuw ding krijgt een **verleden** (vroegste fase waarin het kan bestaan), een **smaak** (genre, verwondering) en een **toekomst** (wat ermee gebeurt als het Zegel niet meer ja kan zeggen namens een lichaam).
- **Verwondering zit in verlies.** Wat mooi is en bij de breuk verdwijnt, weegt zwaar (zoals bij Tolkien).
- **Elke oplossing wordt het probleem van de volgende fase.** Verhalen zijn de plekken waar iemand die prijs betaalt.

## Kaart van de map
- `wereld/canon_tekst/`: de canon als tekst. **Bron.**
- `wereld/velmara.py`: bouw, tekst, toets, kaart.
- `wereld/toets.py`, `roundtrip.py`, `afgeleid.py`, `afgeleid_motor.py`, `migraties/`: integriteit en afgeleide tabellen.
- `wereld/r_Z*.py`: rondescripts, in volgorde. `bouw.py`, `ronde3.py`, `r6.py` en `r7.py` nooit draaien (zie README_VOOR_LLM.md).
- `wereld/z39/`, `z40/`: simulatie (fase 4, Pest van 340). `wereld/z41/personen.py`: personen trekken en schiften (quality-diversity).
- `wereld/graaf_export.py` en `kaart/`: de verhalengraaf en de knopenkaart.
- `wereld/scorekaart_Z*.md`, `keuzelijst_Z*.md`, `wijzigingen_Z*.md`: per ronde wat er gebeurde en wat Rogier nog beslist.
- `architect/`: opdrachten en besluitdocumenten van de architect.
