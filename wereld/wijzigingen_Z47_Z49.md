# Rondes Z47–Z49: fantasieën mogelijk maken met dragers en verhaalpaden

Opdracht van Rogier (2 november 2026): fantasieën mogelijk maken, de database rijker maken, intern consistent, verhaalpaden in lijn met de wereld en de andere paden, divers en zonder sjablonen.

## Wat er veranderde
1. **Z47, wat elke fantasie echt nodig heeft.** De 203 fantasieën zijn gelezen en ingedeeld (`tijd/fantasie_afh.yaml`), niet meer op zoekwoorden. Elke fantasie wijst nu met een link naar wat ze nodig heeft: de LOT-rij van haar wezen of instituut, `LOT-Z44-ishvar` als gewone mensen genoeg zijn, en de FASE-rij van haar verleden. Elf rijen bleken niet erotisch, zoals de Hofproef en de Zestienkeuze; die tellen niet meer mee.
2. **Z48, dragers.** Er zijn 18 nieuwe dingen in de wereld bijgekomen die een verdwenen behoefte opvolgen, zoals gaveglas, sporenroes, de Vrije Ontvangst, de vuurnacht, de Huizen van Spel, de zweefhuid, het wisselbloed, de wasnacht, de geheugenruil in de ring, zingend ijzer, het reuzenbloed, de beeldnacht, het havenbloed, de zangpoelen en het vuurkampgevecht. Ontwerp en criteria staan in `architectuur/DRAGERS.md`, met nieuwe regels: `R-drager_bron` (fout), `R-drager_tijd` (fout) en `R-fantasie_onmogelijk` (signaal).
3. **Z49, verhaalpaden.** Er zijn 18 paden in `verhaal_profiel`, één per drager, elk met een eigen positie, genre, schaal, volk, vorm, afloop en hoofdpersoon. De regels die er al waren, bewaken ze: minstens 3 van 7 assen verschillend binnen een tijdperk, geen gedeelde woordreeksen in de premissen, en de harde lijnen. In de knopenkaart hangen de paden aan hun drager, hun fantasieën en hun tijdperk.

## Afgeleid in de database (bij elke bouw)
`fantasie_kern`, `fantasie_status`, `drager`, `drager_bron` en `v_fantasie_matrix` (`afgeleid_motor.fantasie_tijd`).

## De matrix nu
| Tijdperk | Echt | Zeldzaam | Spel | Onmogelijk |
|---|---|---|---|---|
| 9 Tijd van de Ja (na 801) | 183 | 9 | 0 | 0 |
| 10 Tijd der Volken (na 801) | 184 | 6 | 0 | 2 |
| 11 Heldentijd (na 801) | 181 | 3 | 6 | 2 |
| 12 Het Vertrek (na 801) | 181 | 0 | 6 | 5 |
| 13 Tijd der Mensen (na 801) | 181 | 0 | 6 | 5 |
| 14 De Grote Smelt (na 801) | 181 | 0 | 6 | 5 |
| 15 Het Zwevende Gat (na 801) | 181 | 0 | 6 | 5 |
| 16 Tijd van het Schrift (na 801) | 181 | 0 | 6 | 5 |

Voor de dragers was dit per tijdperk 97 tot 122 echt, 62 tot 64 spel en 8 tot 31 onmogelijk.
