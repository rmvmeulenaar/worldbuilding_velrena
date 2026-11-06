# Ronde Z46: kan elke fantasie in elk tijdperk, en alles verrijken

Vraag van Rogier (2 november 2026): kijk bij alle erotische fantasieën of ze kunnen, net zoals bij thriller en de andere genres, en verrijk alles.

## Het hulpmiddel: `tijd/fantasie.py`
Leest de canon en `tijd/uitkomst.json`; schrijft niets in de database. Per erotische fantasie (VOOR-, KINK-, RIT-) haalt het uit de tekst waar ze van afhangt (gave, binding, Ontvangst, stalsysteem, een volk) en geeft per tijdperk na 801 de status: **echt** (het ding bestaat nog), **zeldzaam**, **spel** (de macht of het instituut is weg; kan als rollenspel tussen volwassenen) of **onmogelijk** (het lichaam of volk bestaat niet meer). Ook telt het per tijdperk de verhaalrijen per genre. Resultaat: `tijd/fantasie.md`.

## Uitkomst voor de fantasieën (203 na deze ronde)
- 88 kunnen in elk tijdperk echt: ze hebben alleen mensen nodig.
- 92 worden na het einde van stal, binding en gave een spel tussen volwassenen. Zo leeft de oude orde voort als fantasie.
- 23 worden onmogelijk als hun volk vervaagt, zoals de vormwissel van de Ves-Lethi, de valparing van de Skerra en de korfgeur van de Kluwers. Dat is verlies, en dus verwondering.

## Verrijking (39 rijen, allemaal voorstel)
- **Gaten vóór 801 gevuld:** Vonk (comedy, romantiek), Brand (actie), Noodtoestand (romantiek met erotiek, actie).
- **Fase 9 tot 12, elk genre minstens één verhaal:** horror, comedy, oorlog, held, actie, thriller, intrige (28 verhalen). Voorbeelden zijn de Lijngravers die geen antwoord hebben (horror), de Bloedkerk die het Lichtconvent weigert (oorlog), de mannenlegers die in de Heldentijd terugkeren, rijmend met de Brand (oorlog), en de verstekeling op de lander (thriller).
- **Zes fantasieën die pas na 801 bestaan:** de vraag zelf, de laatste vonk, het stalspel, vervagen, de vuurnacht, zang zonder aanraking.

## Bewijs (lege genrecellen, query in `tijd/fantasie.py`)
| | Voor | Na | Gehaald |
|---|---|---|---|
| Lege cellen in fase 2-4 | 6 | 0 | ja |
| Lege cellen in fase 9-12 (zonder mythe) | 28 | 0 | ja |
| Lege cellen in fase 13-16 | 28 | 28 | nog niet, volgende ronde |
