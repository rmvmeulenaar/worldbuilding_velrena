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
<!-- REC sim_regel -->
### GESCH-filter · Na 801 verslapt de X-filter: het aandeel jongens schuift per 20 jaar met een vaste fractie naar de helft; het aantal dragers blijft gelijk, dus een steeds kleiner deel van de mannen kan lading dragen.
- **code:** GESCH-filter
- **module:** geschiedenis
- **omschrijving:** Na 801 verslapt de X-filter: het aandeel jongens schuift per 20 jaar met een vaste fractie naar de helft; het aantal dragers blijft gelijk, dus een steeds kleiner deel van de mannen kan lading dragen.
- **parameter:** filter
- **waarde:** 0,02 tot 0,06 per stap (per run getrokken)
- **bron_code:** ORIGIN-10-Z36;BESLUIT-Z36-4
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron ORIGIN-10-Z36;BESLUIT-Z36-4)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-bodem · De magie heeft een bodem: Orrim sterven niet maar verstenen tot groeve, in hun lichaam groeit Sterrensteen, en wat er gemijnd wordt houdt de lading in de wereld.
- **code:** GESCH-bodem
- **module:** geschiedenis
- **omschrijving:** De magie heeft een bodem: Orrim sterven niet maar verstenen tot groeve, in hun lichaam groeit Sterrensteen, en wat er gemijnd wordt houdt de lading in de wereld.
- **parameter:** bodem
- **waarde:** 0,12 plus mijnopbrengst
- **bron_code:** D1-orrim-dood;VOLK-orrim;D1-orrim-geld
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron D1-orrim-dood;VOLK-orrim;D1-orrim-geld)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-golf · De magie golft met de edelen: sluiten de dragerlijnen zich af, dan komt de lading samen; opent de wereld zich door handel en steden, dan verdunt ze.
- **code:** GESCH-golf
- **module:** geschiedenis
- **omschrijving:** De magie golft met de edelen: sluiten de dragerlijnen zich af, dan komt de lading samen; opent de wereld zich door handel en steden, dan verdunt ze.
- **parameter:** golf
- **waarde:** 0,55 maal concentratie
- **bron_code:** ORIGIN-10-Z36;GAVE-Z37-ja
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron ORIGIN-10-Z36;GAVE-Z37-ja)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-piek · Vondsten laten de magie kort oplaaien: de negen cellen van Hesta, de reservekern van de Harrow, splinters Sterrensteen. Een piek dooft met een kwart per stap.
- **code:** GESCH-piek
- **module:** geschiedenis
- **omschrijving:** Vondsten laten de magie kort oplaaien: de negen cellen van Hesta, de reservekern van de Harrow, splinters Sterrensteen. Een piek dooft met een kwart per stap.
- **parameter:** puls
- **waarde:** 0,2 tot 0,5
- **bron_code:** YSA-Z21-3;ORIGIN-Z1-harrow;ORIGIN-8
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron YSA-Z21-3;ORIGIN-Z1-harrow;ORIGIN-8)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-verdunning · Over de eeuwen verdunt de geërfde lading omdat niets haar voedt zoals het Zegel deed; de golf wordt kleiner maar nooit nul.
- **code:** GESCH-verdunning
- **module:** geschiedenis
- **omschrijving:** Over de eeuwen verdunt de geërfde lading omdat niets haar voedt zoals het Zegel deed; de golf wordt kleiner maar nooit nul.
- **parameter:** verdun
- **waarde:** 0,35 + 0,65·e^(-(jaar-801)/1500)
- **bron_code:** BESLUIT-2;BESLUIT-Z36-4
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron BESLUIT-2;BESLUIT-Z36-4)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-bevolking · Bevolking groeit tot het voedsel op is; techniek en dragers op de akkers verhogen het voedsel; honger is druk boven 93 procent.
- **code:** GESCH-bevolking
- **module:** geschiedenis
- **omschrijving:** Bevolking groeit tot het voedsel op is; techniek en dragers op de akkers verhogen het voedsel; honger is druk boven 93 procent.
- **parameter:** groei
- **waarde:** 0,12 tot 0,22 per stap
- **bron_code:** FASE-overvloed
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron FASE-overvloed)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-elite · Edelen groeien in aantal als het volk goedkoop is; te veel edelen en een lege kas geven een strijd om posities (golf van eeuwen).
- **code:** GESCH-elite
- **module:** geschiedenis
- **omschrijving:** Edelen groeien in aantal als het volk goedkoop is; te veel edelen en een lege kas geven een strijd om posities (golf van eeuwen).
- **parameter:** elite
- **waarde:** drempel 1,4
- **bron_code:** FASE-markt
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron FASE-markt)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-staat · De staat leeft van belasting naar bevolking en geloof en betaalt de edelen; zakt de kas onder 0,12, dan is ze blut.
- **code:** GESCH-staat
- **module:** geschiedenis
- **omschrijving:** De staat leeft van belasting naar bevolking en geloof en betaalt de edelen; zakt de kas onder 0,12, dan is ze blut.
- **parameter:** kas
- **waarde:** drempel 0,12
- **bron_code:** FASE-barsten
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron FASE-barsten)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-buren · Kharvos wordt elke stap hongeriger; is het sterker dan kas maal bevolking maal lading, dan valt het aan.
- **code:** GESCH-buren
- **module:** geschiedenis
- **omschrijving:** Kharvos wordt elke stap hongeriger; is het sterker dan kas maal bevolking maal lading, dan valt het aan.
- **parameter:** buren
- **waarde:** 0,5 tot 1,5 honger
- **bron_code:** REG-kharvos-B1;ORIGIN-Z1-harrow
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron REG-kharvos-B1;ORIGIN-Z1-harrow)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-techniek · Techniek groeit in rust en openheid en trager waar magie het werk doet; bij vijf drempels komt een uitvinding.
- **code:** GESCH-techniek
- **module:** geschiedenis
- **omschrijving:** Techniek groeit in rust en openheid en trager waar magie het werk doet; bij vijf drempels komt een uitvinding.
- **parameter:** techniek
- **waarde:** drempels 0,2 0,35 0,5 0,65 0,8
- **bron_code:** ORIGIN-4;ORIGIN-2
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron ORIGIN-4;ORIGIN-2)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-geloof · Geloof groeit met de macht van de kerk en slijt met de techniek; onder 0,38 wankelt het.
- **code:** GESCH-geloof
- **module:** geschiedenis
- **omschrijving:** Geloof groeit met de macht van de kerk en slijt met de techniek; onder 0,38 wankelt het.
- **parameter:** geloof
- **waarde:** drempel 0,38
- **bron_code:** REGEL-seksuele-normen
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron REGEL-seksuele-normen)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-verhaal801 · Het verhaal van 801 wordt per stap minder trouw verteld; sneller als kerk, huizen of dragers vertellen, trager met het geheugen van de Aelthir en met techniek; kerk en huizen maken er een heilige van, dragers en buren een heks.
- **code:** GESCH-verhaal801
- **module:** geschiedenis
- **omschrijving:** Het verhaal van 801 wordt per stap minder trouw verteld; sneller als kerk, huizen of dragers vertellen, trager met het geheugen van de Aelthir en met techniek; kerk en huizen maken er een heilige van, dragers en buren een heks.
- **parameter:** trouw
- **waarde:** start 0,6
- **bron_code:** BESLUIT-Z36-4;BESLUIT-Z18b-2;VOLK-aelthir-V5
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron BESLUIT-Z36-4;BESLUIT-Z18b-2;VOLK-aelthir-V5)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-wezens · Lading die wordt doorgegeven aan wie haar niet kan dragen, maakt nachtvlerken; de omweg werkt op slapers. Een nachtvlerk ontlaadt via huidcontact op de borst van een slaper (YSA-Z18-1); dat is horror en nooit seks, want een slaper kan niet instemmen (harde lijn). Wezenlijnen schuiven van slachtoffer naar groep, volk, monster en sprookje; afzondering versnelt dat.
- **code:** GESCH-wezens
- **module:** geschiedenis
- **omschrijving:** Lading die wordt doorgegeven aan wie haar niet kan dragen, maakt nachtvlerken; de omweg werkt op slapers. Een nachtvlerk ontlaadt via huidcontact op de borst van een slaper (YSA-Z18-1); dat is horror en nooit seks, want een slaper kan niet instemmen (harde lijn). Wezenlijnen schuiven van slachtoffer naar groep, volk, monster en sprookje; afzondering versnelt dat.
- **parameter:** nacht
- **waarde:** 0,12 maal magie maal openheid maal niet-dragers
- **bron_code:** ORIGIN-WAAROM-9;NAV-wormwording-B1;BESLUIT-Z6-WRIJ-065
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron ORIGIN-WAAROM-9;NAV-wormwording-B1;BESLUIT-Z6-WRIJ-065)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-rijm · Een noodoplossing moet op minstens 3 van 5 assen (beslisser, betaler, vervalst, ontdekt, schaal) verschillen van de vorige fase, zoals R-rijm_assen voor fase_rijm.
- **code:** GESCH-rijm
- **module:** geschiedenis
- **omschrijving:** Een noodoplossing moet op minstens 3 van 5 assen (beslisser, betaler, vervalst, ontdekt, schaal) verschillen van de vorige fase, zoals R-rijm_assen voor fase_rijm.
- **parameter:** rijm
- **waarde:** 3 van 5
- **bron_code:** BESLUIT-Z36-4
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron BESLUIT-Z36-4)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-spiraal · Een noodoplossing komt pas na 600 jaar terug; uitvindingen, vondsten, het kleine zegel en het Orrim-recht maar één keer.
- **code:** GESCH-spiraal
- **module:** geschiedenis
- **omschrijving:** Een noodoplossing komt pas na 600 jaar terug; uitvindingen, vondsten, het kleine zegel en het Orrim-recht maar één keer.
- **parameter:** spiraal
- **waarde:** 600 jaar
- **bron_code:** BESLUIT-Z36-4
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron BESLUIT-Z36-4)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-rust · Twee eeuwen zonder crisis is een rustige tijd: verhalen op de schaal van huis en dorp.
- **code:** GESCH-rust
- **module:** geschiedenis
- **omschrijving:** Twee eeuwen zonder crisis is een rustige tijd: verhalen op de schaal van huis en dorp.
- **parameter:** rust
- **waarde:** 200 jaar
- **bron_code:** FASE-overvloed
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron FASE-overvloed)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH-wetten · Wetten volgen de verhouding: boven 12 procent jongens vervalt de Deelwet, boven 25 procent krijgen mannen bezit, boven 40 procent erven zonen en dochters gelijk. Andere wetten komen en gaan met de noodoplossingen.
- **code:** GESCH-wetten
- **module:** geschiedenis
- **omschrijving:** Wetten volgen de verhouding: boven 12 procent jongens vervalt de Deelwet, boven 25 procent krijgen mannen bezit, boven 40 procent erven zonen en dochters gelijk. Andere wetten komen en gaan met de noodoplossingen.
- **parameter:** wet
- **waarde:** 0,12 0,25 0,40
- **bron_code:** WET-deelwet-recht;WET-wie-gewone-man;WET-erfrecht
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z42, bron WET-deelwet-recht;WET-wie-gewone-man;WET-erfrecht)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-macht · Een noodoplossing kan alleen doorgezet worden door wie minstens een tiende van de macht heeft; anders blijft de crisis onopgelost en komt ze 200 jaar niet terug.
- **code:** GESCH2-macht
- **module:** geschiedenis_z43
- **omschrijving:** Een noodoplossing kan alleen doorgezet worden door wie minstens een tiende van de macht heeft; anders blijft de crisis onopgelost en komt ze 200 jaar niet terug.
- **parameter:** macht_min
- **waarde:** 0,10
- **bron_code:** MACHT-twee-soorten-mannen;REGEL-regeringsvorm-Z12
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron MACHT-twee-soorten-mannen;REGEL-regeringsvorm-Z12)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-rijm · Een fase rijmt: ze deelt minstens één mechanisme met een eerdere fase (ook de fasen tot 801 uit fase_rijm) en verschilt op minstens 3 van 5 assen van de vorige; 3 of 4 assen krijgen voorrang.
- **code:** GESCH2-rijm
- **module:** geschiedenis_z43
- **omschrijving:** Een fase rijmt: ze deelt minstens één mechanisme met een eerdere fase (ook de fasen tot 801 uit fase_rijm) en verschilt op minstens 3 van 5 assen van de vorige; 3 of 4 assen krijgen voorrang.
- **parameter:** rijm
- **waarde:** 1 mechanisme, 3 assen
- **bron_code:** BESLUIT-Z36-4;FASE-noodtoestand-Z38
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron BESLUIT-Z36-4;FASE-noodtoestand-Z38)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-erfenis · Elke fase noemt de jongste eerdere fase of gebeurtenis die raakte aan wat haar crisis voedt; grote eenmalige gebeurtenissen werken 400 jaar door, andere 100.
- **code:** GESCH2-erfenis
- **module:** geschiedenis_z43
- **omschrijving:** Elke fase noemt de jongste eerdere fase of gebeurtenis die raakte aan wat haar crisis voedt; grote eenmalige gebeurtenissen werken 400 jaar door, andere 100.
- **parameter:** venster
- **waarde:** 100 of 400 jaar
- **bron_code:** ORIGIN-Z1-harrow;YSA-Z21-3
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron ORIGIN-Z1-harrow;YSA-Z21-3)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-gevolg · Het gevolg van een fase is het verschil in toestand en macht tussen vlak ervoor en 60 jaar erna.
- **code:** GESCH2-gevolg
- **module:** geschiedenis_z43
- **omschrijving:** Het gevolg van een fase is het verschil in toestand en macht tussen vlak ervoor en 60 jaar erna.
- **parameter:** gevolg
- **waarde:** 60 jaar
- **bron_code:** FASE-markt
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron FASE-markt)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-wetverval · Een wet vervalt door opheffing, door een voorwaarde (de verhouding), of als haar wetgever 60 jaar lang minder dan 6 procent van de macht heeft; na 200 jaar is een wet gewoonte en vervalt ze alleen nog door opheffing; een vervallen wet komt pas na 300 jaar terug.
- **code:** GESCH2-wetverval
- **module:** geschiedenis_z43
- **omschrijving:** Een wet vervalt door opheffing, door een voorwaarde (de verhouding), of als haar wetgever 60 jaar lang minder dan 6 procent van de macht heeft; na 200 jaar is een wet gewoonte en vervalt ze alleen nog door opheffing; een vervallen wet komt pas na 300 jaar terug.
- **parameter:** wet_verval
- **waarde:** 0,06; 60 jaar; 200 jaar; 300 jaar
- **bron_code:** WET-deelwet-recht;WET-wie-gewone-man
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron WET-deelwet-recht;WET-wie-gewone-man)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-elite · Edelen zakken ook weer af (sterfte, armoede, verval): drie procent van het overschot per 20 jaar.
- **code:** GESCH2-elite
- **module:** geschiedenis_z43
- **omschrijving:** Edelen zakken ook weer af (sterfte, armoede, verval): drie procent van het overschot per 20 jaar.
- **parameter:** afzakken
- **waarde:** 0,03
- **bron_code:** FASE-markt
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron FASE-markt)
<!-- /REC -->
<!-- REC sim_regel -->
### GESCH2-steden-kerk · De steden groeien met techniek en handel; de kerk groeit en krimpt met het geloof.
- **code:** GESCH2-steden-kerk
- **module:** geschiedenis_z43
- **omschrijving:** De steden groeien met techniek en handel; de kerk groeit en krimpt met het geloof.
- **parameter:** groei
- **waarde:** 0,015 en 0,01
- **bron_code:** REGEL-regeringsvorm-Z12
- **aanname:** 1
- **actief_van:** 801
- **actief_tot:** 
- **status:** voorlopig
- **epistemiek:** aanname (motorontwerp Z43, bron REGEL-regeringsvorm-Z12)
<!-- /REC -->

<!-- SECTIE: GEBEURTENIS_TYPE -->
