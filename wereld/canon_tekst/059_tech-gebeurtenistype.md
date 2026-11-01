# TECH_GEBEURTENISTYPE
<!-- REC tech_gebeurtenistype -->
### uitvinding · Een techniek ontstaat in haar oorsprongsregio.
- **code:** uitvinding
- **module:** technologie
- **omschrijving:** Een techniek ontstaat in haar oorsprongsregio.
- **invariant:** geen verspreiding vóór uitvinding
- **bron_code:** GENRE-wet2-V4
- **epistemiek:** aanname (moduleontwerp Z39, bron GENRE-wet2-V4)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### verspreiding · Een techniek bereikt een buurregio langs een route (reistijd).
- **code:** verspreiding
- **module:** technologie
- **omschrijving:** Een techniek bereikt een buurregio langs een route (reistijd).
- **invariant:** alleen vanuit een regio die haar heeft
- **bron_code:** KAART-seizoenen
- **epistemiek:** aanname (moduleontwerp Z39, bron KAART-seizoenen)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### prijs · Een verspreiding kost lichamen; wie betaalt komt uit de canon.
- **code:** prijs
- **module:** technologie
- **omschrijving:** Een verspreiding kost lichamen; wie betaalt komt uit de canon.
- **invariant:** prijs > 0 bij elke verspreiding
- **bron_code:** GENRE-wet2-V4
- **epistemiek:** aanname (moduleontwerp Z39, bron GENRE-wet2-V4)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### vergeten · Een techniek verdwijnt uit een regio.
- **code:** vergeten
- **module:** technologie
- **omschrijving:** Een techniek verdwijnt uit een regio.
- **invariant:** vergeten techniek verspreidt niet meer vanuit die regio
- **bron_code:** GENRE-wet2-V4
- **epistemiek:** aanname (moduleontwerp Z39, bron GENRE-wet2-V4)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### beroep · Een beroep ontstaat in een regio waar zijn techniek bestaat.
- **code:** beroep
- **module:** beroepen
- **omschrijving:** Een beroep ontstaat in een regio waar zijn techniek bestaat.
- **invariant:** geen beroep zonder techniek in de regio
- **bron_code:** ERF-noodtoestand
- **epistemiek:** aanname (moduleontwerp Z39, bron ERF-noodtoestand)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### zwarte_tweeling · De zwarte tweeling van een beroep ontstaat waar het beroep al bestaat.
- **code:** zwarte_tweeling
- **module:** beroepen
- **omschrijving:** De zwarte tweeling van een beroep ontstaat waar het beroep al bestaat.
- **invariant:** geen tweeling vóór het beroep
- **bron_code:** ERF-noodtoestand
- **epistemiek:** aanname (moduleontwerp Z39, bron ERF-noodtoestand)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### ziekte_index · Het eerste geval ontstaat in de stallen van Hal-Neth.
- **code:** ziekte_index
- **module:** ziekte
- **omschrijving:** Het eerste geval ontstaat in de stallen van Hal-Neth.
- **invariant:** geen sterfte vóór het indexgeval
- **bron_code:** GEB-r10-pest-oorsprong
- **epistemiek:** aanname (moduleontwerp Z40, bron GEB-r10-pest-oorsprong)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### ziekte_besmetting_regio · De koorts bereikt een regio.
- **code:** ziekte_besmetting_regio
- **module:** ziekte
- **omschrijving:** De koorts bereikt een regio.
- **invariant:** alleen via een route met een besmette regio
- **bron_code:** GEB-pest-340
- **epistemiek:** aanname (moduleontwerp Z40, bron GEB-pest-340)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### ziekte_sterfte · Mannen sterven aan de koorts (telling per regio en maand).
- **code:** ziekte_sterfte
- **module:** ziekte
- **omschrijving:** Mannen sterven aan de koorts (telling per regio en maand).
- **invariant:** telling klopt per regio (S+E+I+R+D = mannen)
- **bron_code:** GEB-pest-340
- **epistemiek:** aanname (moduleontwerp Z40, bron GEB-pest-340)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### ziekte_route_dicht · Qesh sluit de karavaanroutes.
- **code:** ziekte_route_dicht
- **module:** ziekte
- **omschrijving:** Qesh sluit de karavaanroutes.
- **invariant:** na het gerucht
- **bron_code:** GEB-r10-pest-qesh
- **epistemiek:** aanname (moduleontwerp Z40, bron GEB-r10-pest-qesh)
<!-- /REC -->

<!-- SECTIE: SIM_RUN -->
