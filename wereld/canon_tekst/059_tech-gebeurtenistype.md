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
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_honger · Crisis (honger): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_honger
- **module:** geschiedenis
- **omschrijving:** Crisis (honger): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-bevolking
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-bevolking)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_elitestrijd · Crisis (elitestrijd): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_elitestrijd
- **module:** geschiedenis
- **omschrijving:** Crisis (elitestrijd): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-elite
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-elite)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_bankroet · Crisis (bankroet): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_bankroet
- **module:** geschiedenis
- **omschrijving:** Crisis (bankroet): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-staat
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-staat)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_invasie · Crisis (invasie): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_invasie
- **module:** geschiedenis
- **omschrijving:** Crisis (invasie): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-buren
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-buren)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_epidemie · Crisis (epidemie): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_epidemie
- **module:** geschiedenis
- **omschrijving:** Crisis (epidemie): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-bevolking
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-bevolking)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_uitvinding · Crisis (uitvinding): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_uitvinding
- **module:** geschiedenis
- **omschrijving:** Crisis (uitvinding): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-techniek
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-techniek)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_geloof · Crisis (geloof): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_geloof
- **module:** geschiedenis
- **omschrijving:** Crisis (geloof): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-geloof
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-geloof)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_opleving · Crisis (opleving): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_opleving
- **module:** geschiedenis
- **omschrijving:** Crisis (opleving): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-golf
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-golf)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_orrim · Crisis (orrim): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_orrim
- **module:** geschiedenis
- **omschrijving:** Crisis (orrim): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-bodem
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-bodem)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_wezens · Crisis (wezens): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_wezens
- **module:** geschiedenis
- **omschrijving:** Crisis (wezens): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-wezens
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-wezens)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_crisis_vondst · Crisis (vondst): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **code:** gesch_crisis_vondst
- **module:** geschiedenis
- **omschrijving:** Crisis (vondst): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.
- **invariant:** rijmt op >=3 assen met de vorige fase
- **bron_code:** GESCH-techniek
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-techniek)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_gebeurtenis · Een toevallige gebeurtenis (vondst, klimaat, schimmel, trek, archief).
- **code:** gesch_gebeurtenis
- **module:** geschiedenis
- **omschrijving:** Een toevallige gebeurtenis (vondst, klimaat, schimmel, trek, archief).
- **invariant:** staat in GEBEURTENIS van z42/geschiedenis.py
- **bron_code:** GESCH-piek
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-piek)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_wet_in · Een wet gaat in.
- **code:** gesch_wet_in
- **module:** geschiedenis
- **omschrijving:** Een wet gaat in.
- **invariant:** een wet gaat pas uit als ze in is
- **bron_code:** GESCH-wetten
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-wetten)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_wet_uit · Een wet vervalt.
- **code:** gesch_wet_uit
- **module:** geschiedenis
- **omschrijving:** Een wet vervalt.
- **invariant:** alleen een geldende wet kan vervallen
- **bron_code:** GESCH-wetten
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-wetten)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_huis · Een huis ontstaat (met ouderhuis), gaat heersen of valt.
- **code:** gesch_huis
- **module:** geschiedenis
- **omschrijving:** Een huis ontstaat (met ouderhuis), gaat heersen of valt.
- **invariant:** elk nieuw huis heeft een ouder
- **bron_code:** GESCH-elite
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-elite)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_rust · Een rustige tijd van minstens 200 jaar.
- **code:** gesch_rust
- **module:** geschiedenis
- **omschrijving:** Een rustige tijd van minstens 200 jaar.
- **invariant:** geen crisis binnen de periode
- **bron_code:** GESCH-rust
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-rust)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_toestand · Toestand van de wereld per eeuw: magie, techniek, verhouding, geloof, macht.
- **code:** gesch_toestand
- **module:** geschiedenis
- **omschrijving:** Toestand van de wereld per eeuw: magie, techniek, verhouding, geloof, macht.
- **invariant:** magie > 0
- **bron_code:** GESCH-bodem
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-bodem)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_versie801 · Hoe het verhaal van 801 vanaf dit jaar verteld wordt.
- **code:** gesch_versie801
- **module:** geschiedenis
- **omschrijving:** Hoe het verhaal van 801 vanaf dit jaar verteld wordt.
- **invariant:** trouw daalt behalve na een vondst
- **bron_code:** GESCH-verhaal801
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-verhaal801)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_wezen · Een wezenlijn schuift een stadium op.
- **code:** gesch_wezen
- **module:** geschiedenis
- **omschrijving:** Een wezenlijn schuift een stadium op.
- **invariant:** stadium daalt nooit
- **bron_code:** GESCH-wezens
- **epistemiek:** aanname (moduleontwerp Z42, bron GESCH-wezens)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_onopgelost · Een crisis waarvoor niemand met genoeg macht een oplossing heeft die rijmt.
- **code:** gesch_onopgelost
- **module:** geschiedenis_z43
- **omschrijving:** Een crisis waarvoor niemand met genoeg macht een oplossing heeft die rijmt.
- **invariant:** komt 200 jaar niet terug
- **bron_code:** GESCH2-macht
- **epistemiek:** aanname (moduleontwerp Z43, bron GESCH2-macht)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_uitvinding_boom · Een uitvinding uit de technologieboom (zie sim_uitvinding).
- **code:** gesch_uitvinding_boom
- **module:** geschiedenis_z44
- **omschrijving:** Een uitvinding uit de technologieboom (zie sim_uitvinding).
- **invariant:** nooit vóór haar vereisten
- **bron_code:** GESCH3-boom
- **epistemiek:** aanname (moduleontwerp Z44, bron GESCH3-boom)
<!-- /REC -->
<!-- REC tech_gebeurtenistype -->
### gesch_techniek_verloren · Magische techniek gaat verloren omdat haar bron opdroogt (zie sim_uitvinding.verloren).
- **code:** gesch_techniek_verloren
- **module:** geschiedenis_z45
- **omschrijving:** Magische techniek gaat verloren omdat haar bron opdroogt (zie sim_uitvinding.verloren).
- **invariant:** alleen gave- en zegelsteentechniek
- **bron_code:** GESCH4-verval
- **epistemiek:** aanname (moduleontwerp Z45, bron GESCH4-verval)
<!-- /REC -->

<!-- SECTIE: SIM_RUN -->
