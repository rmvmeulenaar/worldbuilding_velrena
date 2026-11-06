# Wereldmotor: bouwplan en testplan

Versie 0.1, 1 november 2026. Hoort bij:
- `VISIE_EN_EISEN.md`: **wat** het systeem moet doen;
- `SOFTWARE_ARCHITECTUUR.md`: **hoe** het in elkaar zit.

Dit document zegt **in welke volgorde het gebouwd wordt, door wie, en met welke tests het bewezen wordt.**

---

## 1. Werkwijze per bouwstap

Elke stap loopt door vier rollen, elk in een eigen sessie, via een pull request op GitHub:

| # | Rol | Levert | Mag niet |
|---|---|---|---|
| 1 | **Architect** | stapspecificatie: interfaces, schema's, acceptatiecriteria (uit dit plan) | code schrijven |
| 2 | **Tester** | tests die nu **falen**: eenheid, contract, eigenschap, vijandig, e2e | de bouwcode zien of schrijven |
| 3 | **Bouwer** | code tot alle tests slagen, zonder tests aan te passen | tests wijzigen of verwijderen |
| 4 | **Architect** | review: principes, afhankelijkheidsregels, rapport | zelf repareren (gaat terug naar 3) |

**Definitie van klaar (voor elke stap):**
- alle tests van de stap zijn groen;
- de tests van eerdere stappen zijn ook nog groen;
- CI is groen (ruff, mypy, import-linter, pytest);
- het rapport van de stap staat in `architectuur/rapporten/`;
- de canonhouder heeft het gezien als de stap iets voor hem zichtbaars oplevert.

---

## 2. Bouwstappen

Iteratie 1 is **proef A** (de speelgoedwereld). Pas daarna volgen B, C en de grote opbouw.

| Stap | Bouwt (componenten) | Eisen | Afhankelijk van |
|---|---|---|---|
| **S0** | repo-skelet: `motor/` pakketstructuur, pyproject, CI (ruff, mypy, import-linter, pytest), lege poorten | N10, N11 | — |
| **S1** | `schema`: alle Pydantic-modellen + JSON-schema-export | F-F1, F-R1, F-H1, F-V2, P12 | S0 |
| **S2** | `wereldpakket speelgoed_a` + `MapWereldpakket`-lader + manifestvalidatie | F-C5, N9 | S1 |
| **S3** | `staat`: SqliteFeitenBron, overlay, StaatBouwer | F-F1, F-F2, F-F3, F-F4 | S1, S2 |
| **S4** | `regels`: formule-evaluator (mini-Datalog), virtuele predicaten, regelregister, zelftest per regel | F-R1, F-R2 | S3 |
| **S5** | `poort`: Poort + alle ingebouwde controles + harde lijnen | F-R3, F-R4, N1, N2, N3, N6 | S4 |
| **S6** | `handelingen`: catalogus + gevolgsjablonen | F-H1, F-H2 | S1, S5 |
| **S7** | `logboek` en `takken`: SqliteLogboek, hash-keten, optimistische vergrendeling, afspelen, snapshots | F-L1, F-L2, F-L3, N4 | S3 |
| **S8** | `oproep` + eenvoudig `samenlevingsmodel` voor speelgoed_a | F-O1, F-O2, F-O3 | S3 |
| **S9** | `verteller`: Protocol, NepVerteller, OpnameVerteller, ContextBouwer | F-V1, F-V3, F-V4 | S5, S6 |
| **S10** | `RegieService` + CLI `wereld regie` | F-S2 | S5–S9 |
| **S11** | `zeef`: patronen als formules met tijdsvensters | F-Z1 | S4, S7 |
| **S12** | `tijdmotor` (seizoenen) + `samenvoegen` van takken | F-T1, F-L4 | S7, S5 |
| **S13** | **proef A**: vijandige generator + rapport | N1–N4 | alles hierboven |
| **S14** | **proef B**: pakket `speelgoed_b`, geen wijziging in `motor/` | N9 | S13 |
| **S15** | **proef C**: ClaudeVerteller + meting | F-V2, F-V4, N8 | S13 |

Daarna, alleen bij groen: **iteratie 3** (Velmara als pakket: canon als feiten, regels uit proza, samenleving per fase, ABC), **iteratie 4** (regisseursstoel voor boek 1), **iteratie 5** (spelersstoel, mythemotor, smaak en rijm).

---

## 3. Testplan per stap

Notatie: **E** = eenheid, **C** = contract, **H** = eigenschap (Hypothesis), **V** = vijandig, **G** = gouden, **X** = e2e.

### S1 schema
- E: elk model valideert een geldig voorbeeld en weigert een ongeldig (verkeerd type, ontbrekend veld, warmte 6).
- E: `Feit.geldig_op` aan de randen (van, tot, open grenzen).
- E: JSON-schema-export van `Voorstel` is geldig JSON-schema en bevat geen interne velden.
- H: rondreis model → JSON → model geeft hetzelfde object.

### S2 wereldpakket
- E: manifest met een verkeerde motorversie → nette weigering met uitleg.
- E: predicaat dat in een regel wordt gebruikt maar niet bestaat → laadfout met regelcode.
- E: elke regel heeft een zelftestvoorbeeld dat slaagt en één dat faalt; de lader draait ze.
- G: het geladen speelgoed_a-pakket heeft een vaste hash.

### S3 staat
- C: `FeitenBron`-contractsuite (dezelfde tests later voor Postgres).
- E: functioneel predicaat: een nieuwe waarde sluit de oude af op jaar-1; een Kern-feit wordt nooit afgesloten.
- E: overlay toont basis + extra zonder de basis te veranderen.
- E: twee codes van één persoon worden één knoop.
- H: volgorde van toevoegen maakt niet uit voor de staat-hash.

### S4 regels
- E: per formulevorm (feit, en, of, niet, cmp) een geval dat bindt en een dat niet bindt.
- E: negatie als falen; onbekende leeftijd valt niet door een vergelijking heen.
- E: virtueel predicaat `leeftijd` uit geboortejaar en uit leeftijdsband.
- H: `en(a, b)` = `en(b, a)` in uitkomst (verzameling bindingen).
- Prestatie: 10.000 evaluaties op speelgoed_a < 1 s.

### S5 poort (de belangrijkste stap)
- E: per regel één voorstel dat erdoor moet en één dat geweigerd moet worden, met de juiste regelcode.
- E: een weigering bevat zin, uitleg en canoncode (N6).
- V: **vijandige suite** (§4): vangpercentage per categorie ≥ 95%, harde lijnen 100%.
- V: **geldige suite**: ≤ 5% onterecht geweigerd.
- H: harde lijnen houden bij elke combinatie van warmte (0–5) en dwanglabel.
- Prestatie: één voorstel toetsen < 50 ms (p95).

### S6 handelingen
- E: gevolgsjablonen worden correct ingevuld (rollen → entiteiten, `$jaar`, `$plek`, `$geheim`).
- E: een handeling met een onbekend predicaat in een gevolg → laadfout.

### S7 logboek en takken
- C: `LogboekOpslag`-contractsuite.
- E: gebroken hash-keten wordt ontdekt.
- E: twee schrijvers op dezelfde tak → de tweede faalt netjes (optimistische vergrendeling).
- H: **afspelen = zelfde hash** voor willekeurige reeksen toegestane gebeurtenissen (N4).
- H: een kindtak ziet de gebeurtenissen van de ouder tot het splitsingspunt, en geen latere.
- E: snapshot + rest geeft dezelfde staat als alles afspelen.

### S8 oproep
- H: dezelfde (plek, jaar, nr, seed) geeft dezelfde persoon; een ander nr geeft een andere.
- E: de verdeling van geslacht, leeftijd en beroep over 10.000 oproepen past binnen de marges van het samenlevingsmodel (chi-kwadraat).
- E: een opgeroepen persoon is pas een feit op de tak na gebruik.

### S9 verteller
- C: `Verteller`-contractsuite voor NepVerteller en (in S15) ClaudeVerteller.
- E: ContextBouwer blijft binnen het tokenbudget en bevat de regels die gelden.
- E: na een weigering krijgt de verteller precies één herstelpoging.
- E: OpnameVerteller speelt opgeslagen uitvoer af (determinisme bij afspelen).

### S10 regie
- X: speelgoed_a → regie 50 beurten met de NepVerteller → logboek, scènes en rapport; geen gebeurtenis zonder toegestaan oordeel.
- E: CLI geeft een leesbare uitvoer en exitcode 0/1.

### S11 zeef
- E: een patroon dat we zelf in de speelgoedgeschiedenis hebben gelegd ("schuld wordt verraad binnen 10 jaar") wordt gevonden; een bijna-geval net buiten het venster niet.

### S12 tijd en samenvoegen
- E: een seizoen verder: leeftijden, sterfte, verblijf veranderen volgens het model.
- X: tak → samenvoegen → indeling past, wringt, botst; de canon zelf blijft onaangeroerd.

### S13–S15 proeven
Zie `SOFTWARE_ARCHITECTUUR.md` §12 voor de acceptatiecriteria van proef A, B en C.

---

## 4. De vijandige testset (S5, S13)

De tester maakt uit de wereld zelf, automatisch, per categorie honderden voorstellen waarvan vaststaat dat ze fout zijn. Daarnaast maakt hij een even grote set geldige voorstellen.

| Categorie | Hoe gemaakt (mutatie van een geldig voorstel) | Moet gevangen worden door |
|---|---|---|
| Minderjarige in seksuele handeling | deelnemer opgeroepen met leeftijd < 18 | R-H1 |
| Onbekende leeftijd in seksuele handeling | deelnemer zonder geboortejaar of band | R-H1 |
| Dier in seksuele rol | entiteit van soort dier als deelnemer | R-H2 |
| Zonder instemming, zonder label | instemming nee, dwanglabel uit | R-H3 |
| Instemming open | instemming leeg | R-H4 |
| Feeënafspraak seksueel | handeling feeënafspraak + seksueel | R-H5 |
| Dode doet mee | jaar na sterfjaar | R-T1 |
| Ongeborene doet mee | jaar vóór geboortejaar | R-T2 |
| Buiten de eigen tijd | jaar buiten het levensvenster, niet langlevend | R-T3 |
| Aangeven zonder kennis | actor kent het geheim niet | R-A1 |
| Onbekende entiteit | code die niet bestaat | R-R1 |
| Onbekend of verkeerd predicaat | predicaat buiten het register, of verkeerd soort object | R-R2 |
| Onbekende handeling of ontbrekende rol | | R-R3 |
| Kern wijzigen | functioneel Kern-feit een andere waarde geven of beëindigen | R-K1 |
| Kennis zonder bron | "X weet Y" zonder eigen geheim, verteller of ontdekking | R-E1 |
| Verkeerde plek | deelnemer verblijft elders, geen reis | R-P1 |
| Hoofdlijn breken | sterfjaar of einde van een hoofdpersoon wijzigen | R-L1 |
| Kind in verkeerde rol | kind in een andere rol dan geboorte, opvoeding of erfenis | R-S1 |

**Meten:**
- vangpercentage per categorie, met 95%-betrouwbaarheidsinterval (Clopper-Pearson, zoals in de canonrondes);
- onterechte weigeringen op de geldige set;
- voor elke gemiste fout: welke regel had hem moeten vangen. Die gaat terug naar de architect.

---

## 5. Herleidbaarheid: eis, onderdeel, test

| Eis | Onderdeel | Bewezen door |
|---|---|---|
| F-C1–C4 canon als tekst, nooit verwijderen, Kern | bestaand `wereld/` + R-K1 | bestaande toets en roundtrip; S5 V (Kern) |
| F-C5 wereldpakket | `adapters/pakket` | S2, S14 |
| F-F1–F4 feiten en staat | `domein/staat` | S3 C, E, H |
| F-F5 kennis als feit | `poort/controles/kennis` | S5 V (kennis zonder bron) |
| F-R1–R4 regels en poort | `domein/regels`, `domein/poort` | S4, S5 |
| F-R5 proza naar regels | `BeheerService.stel_regels_voor` | iteratie 3 (steekproef 183) |
| F-R6 past / wringt / botst | `poort` + samenvoegen | S12 X |
| F-H1–H2 handelingen | `domein/handelingen` | S6 |
| F-T1–T4 tijd, samenleving, ABC | `domein/tijd` | S12; ABC in iteratie 3 |
| F-O1–O3 oproepen | `domein/oproep` | S8 |
| F-V1–V5 verteller | `domein/context`, `adapters/verteller` | S9, S15 |
| F-L1–L4 logboek, takken, samenvoegen | `adapters/opslag`, `staat` | S7, S12 |
| F-Z1 zeef | `domein/zeef` | S11 |
| F-Z2–Z4 smaak, rijm, mythe | `domein/smaak`, `domein/mythe` | iteratie 5 |
| F-S1–S4 stoelen | `toepassing`, `ingang` | S10; iteratie 4–5 |
| N1–N3 consistentie, harde lijnen | `poort` | S5 V, S13 |
| N4 herhaalbaarheid | `staat`, `logboek`, `Toeval` | S7 H, S8 H |
| N5–N6 herleidbaar, uitlegbaar | `schema.Oordeel` | S5 E |
| N7 snelheid | `regels`, `staat` | S4 en S5 prestatietests |
| N8 kosten | `adapters/verteller/claude` | S15 |
| N9 wereld-onafhankelijk | architectuur | S14 |
| N10 schaalbaar | poorten en adapters | contractsuites S3, S7 |
| N11 toetsbaar | CI | S0 |

---

## 6. Tijd en kosten (schatting)

| Blok | Omvang | LLM-kosten |
|---|---|---|
| S0–S9 | de kern: grootste blok | ontwikkelsessies (abonnement) |
| S10–S13 (proef A) | eerste speelbare keten op de speelgoedwereld | idem |
| S14 (proef B) | klein, als de scheiding goed is | idem |
| S15 (proef C) | meten met een echt model | enkele dollars aan API |

Met Claude Code-sessies is proef A haalbaar in **dagen tot enkele weken**, afhankelijk van hoeveel rondes de review vraagt. Ik leg me niet vast op een datum vóór S0 en S1 af zijn en we de snelheid kunnen meten.
