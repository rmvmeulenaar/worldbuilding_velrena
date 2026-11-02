# Nakijkvragen voor Z42

Geef de nakijker drie dingen: de database, `z42/LEESMIJ.md` en `CLAUDE.md`. Liefst ook `z42/geschiedenis.py`; zonder die stukken kan hij niet alles toetsen.

## Opdracht

Je krijgt `canon.db` (SQLite) van de wereld Velmara. Ronde Z42 voegde een geschiedenismotor toe voor de tijd na 801. Alles uit Z42 herken je aan:
- module `geschiedenis`
- de codes `GESCH-*` (regels), `gesch_*` (soorten gebeurtenissen, als `type_code` in `sim_gebeurtenis`, geen eigen tabellen), `Z42-GESCH-*` (runs) en `KEUZE-Z42-*` (keuzes)

Lees eerst de wereldkern (canonrijen `REGEL-`, `ORIGIN-`, `BESLUIT-`) en de leesmij.

Beantwoord elke vraag met drie dingen:
- je oordeel: klopt, klopt niet, of twijfel
- het bewijs: een query met uitkomst, of een code
- wat je zou veranderen

Houd uit elkaar wat rechtstreeks uit de database komt en wat je zelf invult. Wat je zelf bedenkt, presenteer je nooit als feit uit de database. Wees streng: een fout vinden is nuttiger dan een compliment.

## G. Kun je er goede verhalen uit halen, en passen die? (belangrijkste)

1. **Trek drie verhalen.** Elk uit een andere run en uit een andere tijd: een ruwe tijd, een rustige tijd, en de tijd van de machines. Schrijf per verhaal in vijf regels:
   - de hoofdpersoon
   - wat die wil
   - wat het kost
   - welk geheim of welke vervalsing erin zit
   - hoe het afloopt

   Noem bij elk punt de rij waar het vandaan komt, of zeg dat je het zelf hebt bedacht.
2. **Passen ze in Velmara?** Toets ze aan:
   - de wereldkern
   - de regel dat elke oplossing de prijs voor de volgende fase wordt
   - het principe dat verwondering in verlies zit
   - de eis dat rijkdom raarheid is die klopt

   Zou een lezer die Velmara tot 801 kent ze herkennen als dezelfde wereld?
3. **Wat moest je zelf verzinnen?** Dat is de lijst met wat de motor mist.
4. **Verschillen de runs echt?** Leveren ze ook andere menselijke conflicten op, of alleen andere jaartallen, namen en uitvindingen? Meet het verschil in oorzaken, niet in uiterlijk.

## H. Zijn de uitvindingen geloofwaardig?

5. **Volgorde.** Komen de uitvindingen (`gesch_crisis_uitvinding`) in een volgorde die kan? Een stoommachine zonder ijzer, of een drukpers zonder metaal?
6. **Grondstoffen.** Passen ze bij de grondstoffen in de canon? Velmara is arm aan metaal en brandstof (`ORIGIN-2`), en de schimmel vreet metaal.
7. **Biologische weg.** Welke uitvindingen zou deze wereld echt doen, nu alle techniek van de Makers biologisch werd (`ORIGIN-4`)?
8. **Tempo.** Klopt het dat de tijd van de machines gemiddeld rond 3381 begint?
9. **Wat niet nodig is.** Welke technologieën zijn in Velmara onmogelijk, overbodig of economisch onaantrekkelijk, juist omdat de wereld andere natuurlijke mogelijkheden heeft?

## A. Klopt de database?

10. **Verwijzingen.** Bestaat elke code in `sim_regel.bron_code` en in `sim_gebeurtenis.canon_code` voor module `geschiedenis` echt in `canon`, en is die rij levend?
11. **Canon ongemoeid.** Is er door Z42 iets in de canon zelf veranderd? Kijk in `canon`, `wijziging` (ronde Z42) en `logboek`.
12. **Epistemiek.** Heeft elke Z42-rij een epistemiek, en noemt elke simulatierij een run-id en een seed?

## B. Klopt de motor met de canon?

13. **Tegenspraak.** Spreekt een regel `GESCH-*` de canon tegen? Let vooral op `BESLUIT-Z36-4`, `BESLUIT-2`, `ORIGIN-10-Z36` en `D1-orrim-dood`.
14. **De bodem van de magie.** Is "de magie verdwijnt nooit" af te leiden uit de canon? Zo ja, uit welke bron: de Orrim-steen of de vonkcellen?
15. **De filter.** Mag de filter na 801 langzaam verslappen (`BESLUIT-2`)? En in welk tempo?
16. **Ysa.** Blijft het verhaal van 801 trouw aan `BESLUIT-Z18b-2`? En is per versie te zien wat waar is en wat verteld wordt?

## C. Werkt de geschiedenis als geschiedenis?

17. **Oorzaken.** Volgt elke crisis uit de toestand ervoor? Is er per crisis een actor met macht, een mechanisme en een gevolg?
18. **Wetten.** Heeft elke wet een wetgever met macht, een rechtsgebied, een handhaver, een aanleiding en een manier waarop ze vervalt?
19. **Huizen.** Is in de stamboom van de huizen het verschil tussen bloed, aanspraak en feitelijk gezag zichtbaar?
20. **Rust.** Zijn de rustige tijden politiek rustig? En verandert er wel iets in economie of samenleving?
21. **Rijm.** Rijmt elke fase met de vorige: minstens één gedeeld mechanisme, minstens drie assen anders, en een aantoonbaar gevolg van de vorige fase?

## D. Levert het verhalen op?

22. **Sterk en dood.** Noem drie sterke en drie dode momenten. Wat maakt het verschil?
23. **Wezens.** Is te volgen hoe een wezenlijn van volk tot draak of sprookje verbastert?
24. **Leefwereld.** Wat mist een schrijver die een roman in jaar 1400 zet?

## E. Harde lijnen

25. **Seks en instemming.** Bevat iets uit Z42 seksuele inhoud, of iets wat later tot een verhaal tegen de harde lijnen van `CLAUDE.md` kan leiden? Kijk vooral naar de nachtvlerken, `W-orrimgroeve` en `W-zegelplicht`.

## F. Eindoordeel

26. **Keuzes.** Geef per keuze `KEUZE-Z42-*` aan: aannemen, aanpassen of afwijzen, met een zin waarom.
27. **Nieuwe zwaktes.** Noem de drie grootste zwaktes die de leesmij en `REVIEW_1.md` nog niet noemen.
