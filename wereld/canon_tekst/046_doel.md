# DOEL
<!-- REC doel -->
### nieuwheid · De afstand tot bestaande verhalen in dezelfde fase (aantal verschillende assen gedeeld door 7).
- **code:** nieuwheid
- **omschrijving:** De afstand tot bestaande verhalen in dezelfde fase (aantal verschillende assen gedeeld door 7).
- **gewicht:** 0.2
- **bron_gewicht:** aanname (startwaarde lancering serie, opdracht_Z35.md 9b.3)
- **richting:** max
<!-- /REC -->
<!-- REC doel -->
### verbondenheid · Open zaadje dat het verhaal oogst, ERF-rij die het raakt, en centraliteit in relatie van zijn ERF-rij en wereldregel (gemiddelde van drie delen).
- **code:** verbondenheid
- **omschrijving:** Open zaadje dat het verhaal oogst, ERF-rij die het raakt, en centraliteit in relatie van zijn ERF-rij en wereldregel (gemiddelde van drie delen).
- **gewicht:** 0.3
- **bron_gewicht:** aanname (startwaarde lancering serie)
- **richting:** max
<!-- /REC -->
<!-- REC doel -->
### seriewaarde · Raakt de hoofdlijn: Liora, de Stille Modus, Thalen, de derde weg, de sleutel (woorden in de geraakte ERF-rij en het zaadje, plus de fase).
- **code:** seriewaarde
- **omschrijving:** Raakt de hoofdlijn: Liora, de Stille Modus, Thalen, de derde weg, de sleutel (woorden in de geraakte ERF-rij en het zaadje, plus de fase).
- **gewicht:** 0.25
- **bron_gewicht:** aanname (startwaarde lancering serie)
- **richting:** max
<!-- /REC -->
<!-- REC doel -->
### lezersvraag · Bayesiaans: prior per genre (verhaal_as.prior, aanname) bijgewerkt met lezersdata (reads x afmaakpercentage).
- **code:** lezersvraag
- **omschrijving:** Bayesiaans: prior per genre (verhaal_as.prior, aanname) bijgewerkt met lezersdata (reads x afmaakpercentage).
- **gewicht:** 0.15
- **bron_gewicht:** aanname tot er lezersdata is
- **richting:** max
<!-- /REC -->
<!-- REC doel -->
### kosten · Geschatte schrijfomvang: woorden per vorm maal schaalfactor (gedeeld door 84).
- **code:** kosten
- **omschrijving:** Geschatte schrijfomvang: woorden per vorm maal schaalfactor (gedeeld door 84).
- **gewicht:** 0.1
- **bron_gewicht:** aanname (startwaarde lancering serie)
- **richting:** min
<!-- /REC -->
<!-- REC doel -->
### genrematch · 1 min de L1-afstand tussen genrevector en doelprofiel, gedeeld door 40. Het minimum van het doelprofiel werkt als filter.
- **code:** genrematch
- **omschrijving:** 1 min de L1-afstand tussen genrevector en doelprofiel, gedeeld door 40. Het minimum van het doelprofiel werkt als filter.
- **gewicht:** 0.2
- **bron_gewicht:** aanname: per doelprofiel 0,20 erbij, de rest naar rato x 0,8
- **richting:** max
<!-- /REC -->

<!-- SECTIE: DOELPROFIEL -->
