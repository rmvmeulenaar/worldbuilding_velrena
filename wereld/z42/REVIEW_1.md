# Review 1 van Z42 en de reactie van de architect

Nakijker: een andere LLM, op `velmara_canon_Z42.db`, zonder `LEESMIJ.md`, `CLAUDE.md` en de broncode (eigen vertrouwen: 95% structureel, 70% inhoudelijk). Datum: 2026-11-02.

**Eindoordeel van de nakijker:**
- als technisch experiment veelbelovend
- als geschiedenismotor nog onvoldoende bewezen
- als canon nog niet

Kernadvies: niet meer geschiedenis genereren, maar zorgen dat de geschiedenis zichzelf kan verklaren.

## Per punt: wat klopt en wat niet

| Punt van de nakijker | Reactie |
|---|---|
| De soorten `gesch_toestand`, `gesch_huis` enz. "ontbreken als tabellen" | **Vergissing.** Het zijn waarden van `sim_gebeurtenis.type_code`, geen tabellen; dat staat in de leesmij. De nakijker gebruikte ze later zelf (82 versies van 801, de huizen van run 0003). |
| Canonverwijzingen, epistemiek, canon ongemoeid | Klopt. |
| `BESLUIT-2` zegt dat de derde weg de 1 op 100 traag ongedaan maakt | **Klopt, en is sterker dan Z42 zelf zei.** `GESCH-filter` moet op `BESLUIT-2` steunen, niet alleen op `BESLUIT-Z36-4`. |
| Orrim-steen is geen blijvende energiebron | **Klopt.** Volgens `VOLK-orrim` ademden de Orrim Sterrensteen-stof in tot ze erdoor doorgroeid werden; de steen groeit bij voortplanting uit mineralen. Groeiende steen is nog geen groeiende lading. Beter onderbouwd: de lading zit in vonkcellen, levende cellen die erfelijk zijn (`YSA-Z18-1`, `ORIGIN-10-Z36`); die verdunnen maar sterven niet uit zolang er dragerlijnen zijn. De steen is versterker en lezer (`ORIGIN-5`: de Wieg is levend-kristallijn). De bodem van de magie moet daarom naar de vonkcellen. Open als nieuwe keuze voor Rogier. |
| Elke crisis heeft een voorafgaande toestand, actor met macht, mechanisme en gevolg nodig | Klopt. Dit is de belangrijkste verbetering. |
| Wetten zonder wetgever met macht, rechtsgebied, handhaving, vervalmechanisme | Klopt. Voorbeeld: het artsengilde maakt een wet zonder dat iemand die bevoegdheid geeft. |
| Stamboom, aanspraak en gezag scheiden | Klopt. |
| Rust is niet gelijk aan stilstand | Klopt; onderscheid politieke rust, economie, sociale verandering, oorlog. |
| "5 van 5 assen anders" is geen rijm | **Klopt, en raakt ook `fase_rijm`.** Rijm vraagt continuïteit én verandering: minstens één gedeeld mechanisme, minstens drie assen anders, en een aantoonbaar gevolg van de vorige fase. De assen moeten aparte velden worden, niet tekst in `detail`. |
| Versies van 801 hebben een waarheidslabel nodig | Klopt. |
| Wezenlijnen missen de tussenschakel (hoe wordt een volk een draak) | Klopt. |
| Een schrijver mist in jaar 1400 de leefwereld (prijzen, taal, recht per dorp, reizen, huwelijk) | Klopt. Dat is de laag onder de geschiedenis. |
| Nachtvlerken op slapers en Orrim-voortplanting zijn een risico voor de harde lijnen | **Klopt. Direct opgelost** (zie hieronder). |

## Wat direct is aangepast (harde lijnen, 2026-11-02)

- **`GESCH-wezens`** zegt nu expliciet: een nachtvlerk ontlaadt via huidcontact op de borst van een slaper (`YSA-Z18-1`). Dat is horror en nooit seks, want een slaper kan niet instemmen.
- **Noodoplossing "De Orrim worden gefokt" is vervangen** door "De Orrim worden in de groeven vastgehouden", met wet `W-orrimgroeve`. Die gaat over gevangenschap en het mijnen van doden, is gelabeld als donker thema en is niet-seksueel. In de zes opgeslagen runs kwam de oude versie niet voor.
- **`W-zegelplicht`** zegt nu: in de steen gebonden worden zoals de Dochters in jaar 0, donker thema, geen seksuele rite (3 rijen bijgewerkt).
- Alle wijzigingen staan in de tabel `wijziging` (ronde Z42). Toets: 0 nieuwe fouten, roundtrip gelijk.

## Volgorde voor de volgende ronde

1. **De geschiedenis laat zichzelf verklaren**, eerst op één run. Elke fase krijgt als aparte velden:
   - de toestand die de crisis veroorzaakte, met de waarden die over de drempel gingen
   - de actor en waar zijn macht vandaan komt
   - het mechanisme
   - het gevolg in de volgende stappen
   - de vijf assen

   Elke wet krijgt een wetgever met macht, een rechtsgebied, een handhaver en een manier waarop ze vervalt.
2. **Een eigen technologieboom voor Velmara**, uit grondstoffen en biologie, niet de aardse reeks. Ontwerpregel: een uitvinding ontstaat pas als de wereld haar mogelijk maakt, de geschiedenis haar nodig of aantrekkelijk maakt, en ze de volgende geschiedenis verandert.
3. **Dezelfde zes runs opnieuw**, getoetst met blok G uit `NAKIJKVRAGEN.md`.
