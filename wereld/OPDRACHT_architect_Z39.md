# Besluiten na Z38 (Rogier) en opdracht Z39

Leg vast als BESLUIT-Z39-*-rijen (besloten_door=Rogier):
1. WRIJ-Z29-1 blijft open (romanwerk).
2. WRIJ-Z38-1: ja, laten staan; bij herschrijven "geslachtsverhouding 1 op 20".
3. WRIJ-Z38-2: EROS-GRENZEN-Z7 krijgt als bron BESLUIT-Z30-4 (zelfde harde regel); GES-officiele-versie krijgt "auteur (Rogier), wereldbijbel".
4. De oude ideeënbank is te dun voor enten (ent-klaar blijft 18). Stop met het minen ervan; houd haar als inspiratie. Nieuwe verhalen komen uit de generator met handgeschreven premisses.

Opdracht Z39: stap 11 uit opdracht_Z35.md (personagenetwerk, detailniveaus, simulatie met Monte Carlo, modules, beroepen), beginnend bij fase 4 Noodtoestand. Werkregels als in opdracht_Z36.md.

---
# Aanscherping Z39 (tweede reviewer, aangescherpt door de architect)

Opdracht Z39 = stap 11 uit opdracht_Z35.md, beperkt tot fase 4 Noodtoestand als proefomgeving, met deze acceptatiecriteria:

1. Gebruik bestaande canon, omstandigheden, beroepen en relaties. Geen nieuwe canonfeiten om de simulatie werkend te krijgen.
2. Elke rij en gebeurtenis krijgt een kolom epistemiek: feit (canon), aanname (afgeleid, met reden), of simulatie (run-id + seed). Simulatie wordt nooit canon zonder besluit van Rogier.
3. Het personagenetwerk moet aantoonbaar werken. Proef: draai dezelfde seeds met en zonder informatieverschillen (iedereen weet alles). Rapporteer hoeveel uitkomsten veranderen. Verandert er weinig, dan faalt het criterium.
4. Monte Carlo is voor verkenning en gevoeligheid, niet voor canon. Documenteer parameters, aannames en seeds.
5. Minstens tien handgeschreven premisses, inhoudelijk verschillend, elk met codes naar de canon waaruit ze volgen.
6. Toon dat de modules los uitbreidbaar zijn naar een andere fase: draai een korte run in fase 5 zonder codewijziging.
7. Behoud alle bestaande tests: geen ongeautoriseerde canonwijziging, reproduceerbaarheid, idempotentie, regressie.
8. Scorekaart met meetbare maten:
   - causale samenhang: % gebeurtenissen in de gekozen runs met een oorzakenketen tot een parameter of canonrij (doel 100%);
   - spanning: per premisse het aantal botsende belangen, onomkeerbare keuzes en relevante geheimen;
   - diversiteit: minimale onderlinge afstand tussen premisses (doel >= 3);
   - canonconsistentie: toets.py groen, en nul botsingen met v_kern.

Succescriterium: het systeem brengt vanuit fase 4 nieuwe conflicten voort. Meetbaar: elke premisse deelt minder dan 20% woord-3-grepen met elke bestaande rij, en bevat een combinatie van personages en belangen die nog in geen enkele bestaande rij samen voorkomt.

Werkregels als in opdracht_Z36.md. Daarna steekproef door de architect.
