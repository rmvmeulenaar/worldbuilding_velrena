# SIM_REGEL
<!-- REC sim_regel -->
### SIM-verhouding · Van de verwekte zonen wordt ongeveer één op honderd geboren (X-filter, Zegel).
- **code:** SIM-verhouding
- **module:** personen
- **omschrijving:** Van de verwekte zonen wordt ongeveer één op honderd geboren (X-filter, Zegel).
- **parameter:** p_zoon
- **waarde:** 0.01
- **bron_code:** GAVE-VERHOUDINGEN-Z38
- **aanname:** 0
- **actief_van:** 0
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GAVE-VERHOUDINGEN-Z38); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-gave · Een geboren zoon krijgt de gave met kans 1 op 20 bij een gaven-vader, 1 op 2000 bij een gewone vader.
- **code:** SIM-gave
- **module:** personen
- **omschrijving:** Een geboren zoon krijgt de gave met kans 1 op 20 bij een gaven-vader, 1 op 2000 bij een gewone vader.
- **parameter:** p_gave
- **waarde:** 0.05;0.0005
- **bron_code:** GAVE-VERHOUDINGEN-Z38
- **aanname:** 0
- **actief_van:** 0
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GAVE-VERHOUDINGEN-Z38); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-levensduur · Sterftekans per jaar volgt een Gompertz-curve rond de levensduur van het volk (mens 70: aanname; aelthir 900).
- **code:** SIM-levensduur
- **module:** personen
- **omschrijving:** Sterftekans per jaar volgt een Gompertz-curve rond de levensduur van het volk (mens 70: aanname; aelthir 900).
- **parameter:** levensduur
- **waarde:** mens=70;aelthir=900
- **bron_code:** ANKER:levensduur
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z39; bron ANKER:levensduur)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-deelwet · Als mannen schaars worden, kan de Registratrix de Deelwet afkondigen: één man voor vele vrouwen (vrouwen per man per jaar 1 -> 8).
- **code:** SIM-deelwet
- **module:** personen
- **omschrijving:** Als mannen schaars worden, kan de Registratrix de Deelwet afkondigen: één man voor vele vrouwen (vrouwen per man per jaar 1 -> 8).
- **parameter:** last
- **waarde:** 1->8
- **bron_code:** GEB-deelwet-40
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-deelwet-40); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-weigeren · Een vrouw mag een beurt weigeren (rang kost het); een man in een verbintenis die een beurt weigert, krijgt ruzie met het register. Geen beurt zonder instemming van beide volwassenen (harde lijn).
- **code:** SIM-weigeren
- **module:** personen
- **omschrijving:** Een vrouw mag een beurt weigeren (rang kost het); een man in een verbintenis die een beurt weigert, krijgt ruzie met het register. Geen beurt zonder instemming van beide volwassenen (harde lijn).
- **parameter:** instemming
- **waarde:** 2 volwassenen
- **bron_code:** WET-wie-weigert;REGEL-harde-grenzen
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon WET-wie-weigert;REGEL-harde-grenzen); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-uitputting · Last boven 3 geboorten per man per jaar verhoogt de sterftekans van mannen.
- **code:** SIM-uitputting
- **module:** personen
- **omschrijving:** Last boven 3 geboorten per man per jaar verhoogt de sterftekans van mannen.
- **parameter:** extra_sterfte
- **waarde:** 0.04 per last-eenheid boven 3
- **bron_code:** GEB-r10-uitputting
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z39; bron GEB-r10-uitputting)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-rotatie · Na uitputtingsdoden kan een rekenaarster een rooster invoeren: last gespreid, extra sterfte gehalveerd.
- **code:** SIM-rotatie
- **module:** personen
- **omschrijving:** Na uitputtingsdoden kan een rekenaarster een rooster invoeren: last gespreid, extra sterfte gehalveerd.
- **parameter:** rotatie
- **waarde:** last/2
- **bron_code:** GEB-r10-rotatie
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-rotatie); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-roof · Een clan met minder mannen per vrouw dan een buurregio kan mannen roven; dat zet een vete.
- **code:** SIM-roof
- **module:** personen
- **omschrijving:** Een clan met minder mannen per vrouw dan een buurregio kan mannen roven; dat zet een vete.
- **parameter:** roof
- **waarde:** clanleidster levend
- **bron_code:** GEB-r10-mannenroof
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-mannenroof); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-register · Na genoeg vetes publiceren de Zusters een register; wie het register leest, weet wie wiens kind is.
- **code:** SIM-register
- **module:** personen
- **omschrijving:** Na genoeg vetes publiceren de Zusters een register; wie het register leest, weet wie wiens kind is.
- **parameter:** register
- **waarde:** vetes>=3
- **bron_code:** GEB-r10-eerste-register;FASE-noodtoestand
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-eerste-register;FASE-noodtoestand); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-registertoegang · Alleen Zusters (later Orde) lezen het register; zij leren de geheimen van wie geregistreerd is.
- **code:** SIM-registertoegang
- **module:** personen
- **omschrijving:** Alleen Zusters (later Orde) lezen het register; zij leren de geheimen van wie geregistreerd is.
- **parameter:** toegang
- **waarde:** Zusters
- **bron_code:** ERF-noodtoestand
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon ERF-noodtoestand); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-inteelt · In een regio zonder register en met weinig mannen stapelt verwantschapsrisico op; boven de drempel volgt een inteeltramp.
- **code:** SIM-inteelt
- **module:** personen
- **omschrijving:** In een regio zonder register en met weinig mannen stapelt verwantschapsrisico op; boven de drempel volgt een inteeltramp.
- **parameter:** risico
- **waarde:** drempel 1.0
- **bron_code:** GEB-r10-neven-ramp
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z39; bron GEB-r10-neven-ramp)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-jongenshof · Zonen worden vanaf de stichting van het Jongenshof daar opgevoed (strikt niet-seksueel).
- **code:** SIM-jongenshof
- **module:** personen
- **omschrijving:** Zonen worden vanaf de stichting van het Jongenshof daar opgevoed (strikt niet-seksueel).
- **parameter:** jongenshof
- **waarde:** na register
- **bron_code:** GEB-r10-jongenshof;RIT-hofproef
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-jongenshof;RIT-hofproef); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-orde · Met register en rooster kan een Moeder de Zusters tot Orde maken.
- **code:** SIM-orde
- **module:** personen
- **omschrijving:** Met register en rooster kan een Moeder de Zusters tot Orde maken.
- **parameter:** orde
- **waarde:** register+rotatie
- **bron_code:** GEB-r10-orde-naam
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-orde-naam); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-eilanden · De Nevel-eilanden weigeren de rotatie zolang hun eilandmoeder leeft.
- **code:** SIM-eilanden
- **module:** personen
- **omschrijving:** De Nevel-eilanden weigeren de rotatie zolang hun eilandmoeder leeft.
- **parameter:** weigering
- **waarde:** Runa levend
- **bron_code:** GEB-r10-eilanden-weigering
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-r10-eilanden-weigering); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-reistijd · Reizen kost 1-2 seizoenen tussen buurregio's; winter sluit de Amberpas, lente maakt de delta onbegaanbaar.
- **code:** SIM-reistijd
- **module:** personen
- **omschrijving:** Reizen kost 1-2 seizoenen tussen buurregio's; winter sluit de Amberpas, lente maakt de delta onbegaanbaar.
- **parameter:** reistijd
- **waarde:** seizoenen
- **bron_code:** KAART-seizoenen;REG-overzicht
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z39; bron KAART-seizoenen;REG-overzicht)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-raad · Raad der Moeders (jaar -3): 12 stemmen; Zusters stemmen meestal voor, eilandvrouwen meestal tegen.
- **code:** SIM-raad
- **module:** personen
- **omschrijving:** Raad der Moeders (jaar -3): 12 stemmen; Zusters stemmen meestal voor, eilandvrouwen meestal tegen.
- **parameter:** raad
- **waarde:** 5 Zusters p=.85; 4 eiland p=.35; 3 Lisk p=.5
- **bron_code:** GEB-r10-raad-der-moeders;BESLUIT-Z3-WRIJ-055
- **aanname:** 1
- **actief_van:** -3
- **actief_tot:** -3
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z39; bron GEB-r10-raad-der-moeders;BESLUIT-Z3-WRIJ-055)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-varenne · Varenne-krediet en de Zaadbeurs bestaan pas vanaf 455; niet actief in fase 4.
- **code:** SIM-varenne
- **module:** personen
- **omschrijving:** Varenne-krediet en de Zaadbeurs bestaan pas vanaf 455; niet actief in fase 4.
- **parameter:** krediet
- **waarde:** uit
- **bron_code:** GEB-zaadbeurs-455
- **aanname:** 0
- **actief_van:** 455
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon GEB-zaadbeurs-455); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-kern · De motor overschrijft geen Kern: canonpersonages zijn in hun canonjaar in leven (anker-invariant), canonjaren worden niet verschoven.
- **code:** SIM-kern
- **module:** personen
- **omschrijving:** De motor overschrijft geen Kern: canonpersonages zijn in hun canonjaar in leven (anker-invariant), canonjaren worden niet verschoven.
- **parameter:** kern
- **waarde:** invariant
- **bron_code:** REGEL-harde-grenzen;BESLUIT-Z30-4
- **aanname:** 0
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** feit (regel uit canon REGEL-harde-grenzen;BESLUIT-Z30-4); getal: aanname
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-schrijfsters · Schrijven is een geheime kunst van de Zusters (schriftverbod, YSA-Z21-8). In jaar 0 kunnen 3 Zusters schrijven; elke schrijfster leidt gemiddeld één leerling op per 20 jaar (maximaal 300). Een rijksbreed rooster vraagt 40 schrijfsters.
- **code:** SIM-schrijfsters
- **module:** personen
- **omschrijving:** Schrijven is een geheime kunst van de Zusters (schriftverbod, YSA-Z21-8). In jaar 0 kunnen 3 Zusters schrijven; elke schrijfster leidt gemiddeld één leerling op per 20 jaar (maximaal 300). Een rijksbreed rooster vraagt 40 schrijfsters.
- **parameter:** start;opleiding;max;rooster
- **waarde:** 3;20;300;40
- **bron_code:** YSA-Z21-8;BESLUIT-Z17-9;BESLUIT-Z40-6
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron YSA-Z21-8;BESLUIT-Z17-9;BESLUIT-Z40-6)
<!-- /REC -->
<!-- REC sim_regel -->
### SIM-registerbereik · Het register ontstaat in Saelith en bereikt een buurregio met kans 0,25 per lente, gedeeld door de reistijd, als er twee schrijfsters per bereikte regio zijn. Tot een regio bereikt is, stapelt daar het inteeltrisico op.
- **code:** SIM-registerbereik
- **module:** personen
- **omschrijving:** Het register ontstaat in Saelith en bereikt een buurregio met kans 0,25 per lente, gedeeld door de reistijd, als er twee schrijfsters per bereikte regio zijn. Tot een regio bereikt is, stapelt daar het inteeltrisico op.
- **parameter:** spreiding;schrijfsters_per_regio
- **waarde:** 0.25/reistijd;2
- **bron_code:** GEB-r10-eerste-register;BESLUIT-Z40-4
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-r10-eerste-register;BESLUIT-Z40-4)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-beta_stal · beta_stal: GEB-r10-pest-oorsprong (overvolle stallen)
- **code:** ZIEKTE-beta_stal
- **module:** ziekte
- **omschrijving:** beta_stal: GEB-r10-pest-oorsprong (overvolle stallen)
- **parameter:** beta_stal
- **waarde:** 10.0
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-beta · beta: aanname: R0 ~1,8 onder mannen buiten de stallen
- **code:** ZIEKTE-beta
- **module:** ziekte
- **omschrijving:** beta: aanname: R0 ~1,8 onder mannen buiten de stallen
- **parameter:** beta
- **waarde:** 3.6
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-sigma · sigma: aanname: incubatie ~2 weken
- **code:** ZIEKTE-sigma
- **module:** ziekte
- **omschrijving:** sigma: aanname: incubatie ~2 weken
- **parameter:** sigma
- **waarde:** 2.0
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-gamma · gamma: aanname: ziekteduur ~2 weken
- **code:** ZIEKTE-gamma
- **module:** ziekte
- **omschrijving:** gamma: aanname: ziekteduur ~2 weken
- **parameter:** gamma
- **waarde:** 2.0
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-cfr · cfr: geijkt op GEB-pest-340 (een derde van de mannen); gevoeligheid: 0.3-0.5 in scorekaart
- **code:** ZIEKTE-cfr
- **module:** ziekte
- **omschrijving:** cfr: geijkt op GEB-pest-340 (een derde van de mannen); gevoeligheid: 0.3-0.5 in scorekaart
- **parameter:** cfr
- **waarde:** 0.35
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-vatbaar_verwant · vatbaar_verwant: GEB-r10-pest-oorsprong (verwante lijnen)
- **code:** ZIEKTE-vatbaar_verwant
- **module:** ziekte
- **omschrijving:** vatbaar_verwant: GEB-r10-pest-oorsprong (verwante lijnen)
- **parameter:** vatbaar_verwant
- **waarde:** 1.5
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-ontstaan · ontstaan: aanname: kans per maand per drukte-eenheid dat in Hal-Neth een koorts ontstaat
- **code:** ZIEKTE-ontstaan
- **module:** ziekte
- **omschrijving:** ontstaan: aanname: kans per maand per drukte-eenheid dat in Hal-Neth een koorts ontstaat
- **parameter:** ontstaan
- **waarde:** 0.004
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-drukte_sinds · drukte_sinds: aanname: de stallen raken vol vanaf 320 (fokkerij, GEB-r10-pest-oorsprong)
- **code:** ZIEKTE-drukte_sinds
- **module:** ziekte
- **omschrijving:** drukte_sinds: aanname: de stallen raken vol vanaf 320 (fokkerij, GEB-r10-pest-oorsprong)
- **parameter:** drukte_sinds
- **waarde:** 320
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-nieuws · nieuws: aanname: maanden voor het nieuws Qesh bereikt (karavaan, koeriers)
- **code:** ZIEKTE-nieuws
- **module:** ziekte
- **omschrijving:** nieuws: aanname: maanden voor het nieuws Qesh bereikt (karavaan, koeriers)
- **parameter:** nieuws
- **waarde:** 2
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-gerucht · gerucht: aanname: aantal doden voordat er een gerucht naar Qesh gaat
- **code:** ZIEKTE-gerucht
- **module:** ziekte
- **omschrijving:** gerucht: aanname: aantal doden voordat er een gerucht naar Qesh gaat
- **parameter:** gerucht
- **waarde:** 20
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-sluiten · sluiten: GEB-r10-pest-qesh: Qesh sluit de karavaanroutes; kans per maand na het nieuws (aanname)
- **code:** ZIEKTE-sluiten
- **module:** ziekte
- **omschrijving:** sluiten: GEB-r10-pest-qesh: Qesh sluit de karavaanroutes; kans per maand na het nieuws (aanname)
- **parameter:** sluiten
- **waarde:** 0.4
- **bron_code:** GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-mannen · Mannen per regio vóór de Pest (aanname; Hal-Neth apart).
- **code:** ZIEKTE-mannen
- **module:** ziekte
- **omschrijving:** Mannen per regio vóór de Pest (aanname; Hal-Neth apart).
- **parameter:** mannen
- **waarde:** {"halneth": 150, "saelith": 1200, "ambergaard": 900, "zoutkust": 600, "groenmuil": 400, "hoogvrouwe": 300, "stille": 150, "qesh": 500}
- **bron_code:** FASE-markt;REG-overzicht
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron FASE-markt;REG-overzicht)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-koppeling · Contact per maand tussen regio's (rotatiekringen, karavaan; afgesloten stallen).
- **code:** ZIEKTE-koppeling
- **module:** ziekte
- **omschrijving:** Contact per maand tussen regio's (rotatiekringen, karavaan; afgesloten stallen).
- **parameter:** koppeling
- **waarde:** {"halneth-saelith": 0.0001, "saelith-ambergaard": 0.04, "saelith-zoutkust": 0.04, "saelith-groenmuil": 0.02, "zoutkust-groenmuil": 0.04, "zoutkust-stille": 0.04, "ambergaard-hoogvrouwe": 0.04, "saelith-stille": 0.02, "saelith-qesh": 0.02}
- **bron_code:** GEB-r10-rotatie;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-r10-rotatie;GEB-r10-pest-oorsprong;GEB-r10-pest-qesh)
<!-- /REC -->
<!-- REC sim_regel -->
### ZIEKTE-alleen-mannen · Alleen mannen worden ziek (aanname op GEB-pest-340: de koorts zit in de mannenvertrekken).
- **code:** ZIEKTE-alleen-mannen
- **module:** ziekte
- **omschrijving:** Alleen mannen worden ziek (aanname op GEB-pest-340: de koorts zit in de mannenvertrekken).
- **parameter:** vatbaar
- **waarde:** mannen
- **bron_code:** GEB-pest-340
- **aanname:** 1
- **actief_van:** 
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (parameter gekozen in Z40; bron GEB-pest-340)
<!-- /REC -->

<!-- SECTIE: GEBEURTENIS_TYPE -->
