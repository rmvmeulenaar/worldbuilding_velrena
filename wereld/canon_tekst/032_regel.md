# REGEL
<!-- REC regel -->
### R-kern_vastgesteld · Kern bestaat alleen uit levende, vastgestelde rijen.
- **code:** R-kern_vastgesteld
- **domein:** structuur
- **omschrijving:** Kern bestaat alleen uit levende, vastgestelde rijen.
- **sql_test:** select code,'Kern maar status '||status from canon where draagkracht='Kern' and status!='vastgesteld'
- **bron:** canon-motor principe 3; HANDL-Z31-1
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-handmatig_waarde · draagkracht_handmatig is leeg of Kern/Structuur/Kleur.
- **code:** R-handmatig_waarde
- **domein:** structuur
- **omschrijving:** draagkracht_handmatig is leeg of Kern/Structuur/Kleur.
- **sql_test:** select code,'ongeldige draagkracht_handmatig '||draagkracht_handmatig from canon where draagkracht_handmatig is not null and draagkracht_handmatig not in('Kern','Structuur','Kleur')
- **bron:** HANDL-Z31-1
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-handmatig_kern · Handmatig Kern alleen op een vastgestelde rij.
- **code:** R-handmatig_kern
- **domein:** structuur
- **omschrijving:** Handmatig Kern alleen op een vastgestelde rij.
- **sql_test:** select code,'draagkracht_handmatig=Kern op een rij met status '||status||' (telt niet als Kern)' from canon where draagkracht_handmatig='Kern' and status!='vastgesteld'
- **bron:** HANDL-Z31-1
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-vervangen_door · Elke vervangen rij wijst naar een bestaande opvolger (vervangen_door).
- **code:** R-vervangen_door
- **domein:** structuur
- **omschrijving:** Elke vervangen rij wijst naar een bestaande opvolger (vervangen_door).
- **sql_test:** select code,case when vervangen_door is null then 'voorlopig, vervangen zonder vervangen_door' else 'vervangen_door '||vervangen_door||' bestaat niet' end from canon where status='voorlopig, vervangen' and (vervangen_door is null or (vervangen_door not in(select code from canon) and not (vervangen_door='personage_profiel:'||code and code in(select code from personage_profiel))))
- **bron:** canon-motor principe 7
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-dode_link · Elke verwijzing bestaat.
- **code:** R-dode_link
- **domein:** structuur
- **omschrijving:** Elke verwijzing bestaat.
- **sql_test:** select van_code,van_tabel||': '||naar_code from verwijzing where bestaat=0
- **bron:** canon-motor scorekaart 3
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-harde_grens · Harde lijnen op elke rij (ook boog- en personagevoorstellen): geen minderjarige of dier in een seksuele context.
- **code:** R-harde_grens
- **domein:** kern
- **omschrijving:** Harde lijnen op elke rij (ook boog- en personagevoorstellen): geen minderjarige of dier in een seksuele context.
- **sql_test:** py:harde_grens
- **bron:** BESLUIT-Z30-4; REGEL-harde-grenzen
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-anker · Geen levende rij noemt een andere waarde dan het anker.
- **code:** R-anker
- **domein:** kern
- **omschrijving:** Geen levende rij noemt een andere waarde dan het anker.
- **sql_test:** py:anker
- **bron:** tabel anker (bron_code per anker)
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-leeftijd · Leeftijden kloppen met het geboorte-anker (TOESTAND-rijen en PER-rijen 'geboren ca.').
- **code:** R-leeftijd
- **domein:** structuur
- **omschrijving:** Leeftijden kloppen met het geboorte-anker (TOESTAND-rijen en PER-rijen 'geboren ca.').
- **sql_test:** py:leeftijd
- **bron:** ankers *_geboren
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31); Z33 uitgebreid naar PER-rijen
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-na_dood · Niemand handelt na zijn dood: rij met jaar > sterfjaar die de naam noemt, zonder nadood-woord (stem, graf, lied, naam...). Z33: ook sterfjaren uit PER-rijen (relatie sterft_in).
- **code:** R-na_dood
- **domein:** structuur
- **omschrijving:** Niemand handelt na zijn dood: rij met jaar > sterfjaar die de naam noemt, zonder nadood-woord (stem, graf, lied, naam...). Z33: ook sterfjaren uit PER-rijen (relatie sterft_in).
- **sql_test:** py:na_dood
- **bron:** ankers *_sterfjaar; relatie sterft_in
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31); Z33 uitgebreid
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-naam · Geen twee personages met (bijna) dezelfde voornaam zonder markering in naam_markering.
- **code:** R-naam
- **domein:** structuur
- **omschrijving:** Geen twee personages met (bijna) dezelfde voornaam zonder markering in naam_markering.
- **sql_test:** py:naam
- **bron:** naam_markering
- **goedgekeurd_door:** Rogier (Z31: toets.py aanvaard, 2026-10-31)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-kern_zonder_bron · Elke Kern-rij heeft een herkomst (bron != onbekend). Canon-motor principe 4: Kern 100%.
- **code:** R-kern_zonder_bron
- **domein:** kern
- **omschrijving:** Elke Kern-rij heeft een herkomst (bron != onbekend). Canon-motor principe 4: Kern 100%.
- **sql_test:** select code,'Kern zonder bron: '||coalesce(bron_soort,'-') from canon where draagkracht='Kern' and status in('vastgesteld','voorlopig') and coalesce(bron,'onbekend')='onbekend'
- **bron:** canon-motor principe 4
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-kern_leunt_op_kleur · Afhankelijkheden lopen één kant op: een Kern-rij leunt (verwijst_naar) nooit op een Kleur-rij of een archiefrij.
- **code:** R-kern_leunt_op_kleur
- **domein:** kern
- **omschrijving:** Afhankelijkheden lopen één kant op: een Kern-rij leunt (verwijst_naar) nooit op een Kleur-rij of een archiefrij.
- **sql_test:** select r.van_code,'Kern leunt op Kleur: '||r.naar_code||' ('||b.status||')' from relatie r join canon a on a.code=r.van_code join canon b on b.code=r.naar_code where r.soort='leunt_op' and a.draagkracht='Kern' and a.status in('vastgesteld','voorlopig') and b.draagkracht='Kleur' and coalesce(b.vervangen_door,'') not like 'personage_profiel:%' and a.code not like 'FASE-OVERZICHT-%' and not exists(select 1 from canon s where s.code=b.vervangen_door and s.draagkracht='Kern' and s.status in('vastgesteld','voorlopig'))
- **bron:** canon-motor principe 3
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-fase_nummer · Fasenummer en fasenaam horen bij elkaar volgens de ankers fase_N_naam.
- **code:** R-fase_nummer
- **domein:** structuur
- **omschrijving:** Fasenummer en fasenaam horen bij elkaar volgens de ankers fase_N_naam.
- **sql_test:** py:fase_nummer
- **bron:** ankers fase_0..7_naam (FASE-*-rijen, PER-rijen)
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-mal_aangrenzend · Geen twee opeenvolgende bogen met hetzelfde profiel (geslacht, leeftijdsklasse, romance, erotische sleutelscène, motief).
- **code:** R-mal_aangrenzend
- **domein:** verhaal
- **omschrijving:** Geen twee opeenvolgende bogen met hetzelfde profiel (geslacht, leeftijdsklasse, romance, erotische sleutelscène, motief).
- **sql_test:** py:mal_aangrenzend
- **bron:** canon-motor domeinlaag verhalen (mal-breker)
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-motief_max · Elk terugkerend motief komt in hoogstens 4 bogen voor (MOTIEF_MAX in toets.py).
- **code:** R-motief_max
- **domein:** verhaal
- **omschrijving:** Elk terugkerend motief komt in hoogstens 4 bogen voor (MOTIEF_MAX in toets.py).
- **sql_test:** py:motief_max
- **bron:** canon-motor domeinlaag verhalen (mal-breker)
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-anker_bron_levend · De bronrij van elk anker bestaat en leeft.
- **code:** R-anker_bron_levend
- **domein:** kern
- **omschrijving:** De bronrij van elk anker bestaat en leeft.
- **sql_test:** select 'ANKER-'||a.sleutel,'bron '||coalesce(a.bron_code,'-')||' bestaat niet of leeft niet' from anker a left join canon c on c.code=a.bron_code where (c.code is null or c.status not in('vastgesteld','voorlopig')) and not (c.vervangen_door='personage_profiel:'||c.code and c.code in(select code from personage_profiel))
- **bron:** canon-motor principe 1
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-regel_zonder_bron · Elke actieve regel heeft een bron.
- **code:** R-regel_zonder_bron
- **domein:** structuur
- **omschrijving:** Elke actieve regel heeft een bron.
- **sql_test:** select code,'regel zonder bron' from regel where status='actief' and coalesce(bron,'')=''
- **bron:** canon-motor werkwijze D
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-structuur_zonder_bron · Signaal: Structuur-rij zonder herkomst (streef: >=90% met bron).
- **code:** R-structuur_zonder_bron
- **domein:** structuur
- **omschrijving:** Signaal: Structuur-rij zonder herkomst (streef: >=90% met bron).
- **sql_test:** select code,'Structuur zonder bron' from canon where draagkracht='Structuur' and status in('vastgesteld','voorlopig') and coalesce(bron,'onbekend')='onbekend'
- **bron:** canon-motor principe 4
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-structuur_leunt_op_kleur · Signaal: Structuur leunt op Kleur (mag, maar dan is het Kleur-feit eigenlijk Structuur).
- **code:** R-structuur_leunt_op_kleur
- **domein:** structuur
- **omschrijving:** Signaal: Structuur leunt op Kleur (mag, maar dan is het Kleur-feit eigenlijk Structuur).
- **sql_test:** select r.van_code,'Structuur leunt op Kleur: '||r.naar_code from relatie r join canon a on a.code=r.van_code join canon b on b.code=r.naar_code where r.soort='leunt_op' and a.draagkracht='Structuur' and a.status in('vastgesteld','voorlopig') and b.draagkracht='Kleur' and b.status in('vastgesteld','voorlopig')
- **bron:** canon-motor principe 3
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-profiel_geen_personage · Signaal: hoofdpersoon zonder eigen fout (profiel, geen personage).
- **code:** R-profiel_geen_personage
- **domein:** verhaal
- **omschrijving:** Signaal: hoofdpersoon zonder eigen fout (profiel, geen personage).
- **sql_test:** select code,naam||': profiel, geen personage' from personage where status like 'profiel%'
- **bron:** canon-motor domeinlaag verhalen
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-zaadje_open · Signaal: zaadje zonder oogst (landt niet en loopt niet bewust dood).
- **code:** R-zaadje_open
- **domein:** verhaal
- **omschrijving:** Signaal: zaadje zonder oogst (landt niet en loopt niet bewust dood).
- **sql_test:** select code,coalesce(wat,'') from zaadje where status like 'open%'
- **bron:** canon-motor drie lagen consistentie (causaliteit)
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-boog_onbekend · Signaal: boog met een onbekende as (profiel niet uit de canon af te leiden).
- **code:** R-boog_onbekend
- **domein:** verhaal
- **omschrijving:** Signaal: boog met een onbekende as (profiel niet uit de canon af te leiden).
- **sql_test:** select code,'onbekende as' from boog where 'onbekend' in(coalesce(geslacht_hoofdpersoon,'onbekend'),romance,erotische_sleutelscene,terugkerend_motief,noodoplossing) or leeftijd_hoofdpersoon is null
- **bron:** canon-motor domeinlaag verhalen
- **goedgekeurd_door:** opdracht Z33 (Rogier: benchmark-skill gebruiken, 2026-11-01); regel zelf nog niet door Rogier gekeurd
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-sjabloon_nieuw · Geen sjablonen: rijen vanaf ronde Z34 (ronde>=63) vormen onderling geen sjabloonfamilie (>=3 met dezelfde signatuur) en zijn geen bijna-kopie (Jaccard woord-3-grepen >= 0,5) van een andere levende rij.
- **code:** R-sjabloon_nieuw
- **domein:** verhaal
- **omschrijving:** Geen sjablonen: rijen vanaf ronde Z34 (ronde>=63) vormen onderling geen sjabloonfamilie (>=3 met dezelfde signatuur) en zijn geen bijna-kopie (Jaccard woord-3-grepen >= 0,5) van een andere levende rij.
- **sql_test:** py:sjabloon_nieuw
- **bron:** BESLUIT-Z34-1; HANDL-Z34-1
- **goedgekeurd_door:** Rogier (2026-11-01)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-herhaling_categorie · Signaal: meer dan 35% van de levende canonrijen (buiten de ideeënbank) van een categorie (n>=10) zit in een sjabloonfamilie (>=5 rijen met dezelfde label- of openingssignatuur).
- **code:** R-herhaling_categorie
- **domein:** verhaal
- **omschrijving:** Signaal: meer dan 35% van de levende canonrijen (buiten de ideeënbank) van een categorie (n>=10) zit in een sjabloonfamilie (>=5 rijen met dezelfde label- of openingssignatuur).
- **sql_test:** py:herhaling_categorie
- **bron:** BESLUIT-Z34-1; z34/herhaling.py
- **goedgekeurd_door:** Rogier (2026-11-01)
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-boog_uniek · Geen twee bogen met dezelfde vorm, verteller, toon, tempo of afloop.
- **code:** R-boog_uniek
- **domein:** verhaal
- **omschrijving:** Geen twee bogen met dezelfde vorm, verteller, toon, tempo of afloop.
- **sql_test:** py:boog_uniek
- **bron:** BESLUIT-Z34-1; BESLUIT-Z34-2
- **goedgekeurd_door:** Rogier (2026-11-01)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-personage_fout_uniek · Geen twee personages met dezelfde soort eigen fout.
- **code:** R-personage_fout_uniek
- **domein:** verhaal
- **omschrijving:** Geen twee personages met dezelfde soort eigen fout.
- **sql_test:** py:personage_fout_uniek
- **bron:** BESLUIT-Z34-1; BESLUIT-Z34-4
- **goedgekeurd_door:** Rogier (2026-11-01)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-rijm_assen · Rijm, geen kopie: elke fase in fase_rijm verschilt van de vorige op minstens 3 van de 5 assen beslisser, betaler, vervalst, ontdekt, schaal (de *_as-kolommen; leeg telt niet als verschil).
- **code:** R-rijm_assen
- **domein:** verhaal
- **omschrijving:** Rijm, geen kopie: elke fase in fase_rijm verschilt van de vorige op minstens 3 van de 5 assen beslisser, betaler, vervalst, ontdekt, schaal (de *_as-kolommen; leeg telt niet als verschil).
- **sql_test:** py:rijm_assen
- **bron:** OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1
- **goedgekeurd_door:** architect (Z35), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-rijm_erfenis · Elke fase vanaf fase 1 erft (fase_rijm.erft_van) van minstens één levende ERF-rij uit een eerdere fase.
- **code:** R-rijm_erfenis
- **domein:** verhaal
- **omschrijving:** Elke fase vanaf fase 1 erft (fase_rijm.erft_van) van minstens één levende ERF-rij uit een eerdere fase.
- **sql_test:** py:rijm_erfenis
- **bron:** OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1
- **goedgekeurd_door:** architect (Z35), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-rijm_spiraal · Spiraal, geen cirkel: blijvende_verandering is niet leeg en komt niet (letterlijk of voor 60% van de woorden) terug uit een eerdere fase.
- **code:** R-rijm_spiraal
- **domein:** verhaal
- **omschrijving:** Spiraal, geen cirkel: blijvende_verandering is niet leeg en komt niet (letterlijk of voor 60% van de woorden) terug uit een eerdere fase.
- **sql_test:** py:rijm_spiraal
- **bron:** OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1
- **goedgekeurd_door:** architect (Z35), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-rijm_binnen_fase · De bogen binnen één fase verschillen onderling op minstens 2 rijm-assen (boog.beslisser_as, betaler_as, vervalst_as, ontdekt_as, schaal).
- **code:** R-rijm_binnen_fase
- **domein:** verhaal
- **omschrijving:** De bogen binnen één fase verschillen onderling op minstens 2 rijm-assen (boog.beslisser_as, betaler_as, vervalst_as, ontdekt_as, schaal).
- **sql_test:** py:rijm_binnen_fase
- **bron:** OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1
- **goedgekeurd_door:** architect (Z35), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-verhaal_afstand · Elk voorgesteld of ent-klaar verhaalprofiel verschilt op minstens 3 van de 7 assen van elke boog en elk eerder profiel in dezelfde fase.
- **code:** R-verhaal_afstand
- **domein:** verhaal
- **omschrijving:** Elk voorgesteld of ent-klaar verhaalprofiel verschilt op minstens 3 van de 7 assen van elke boog en elk eerder profiel in dezelfde fase.
- **sql_test:** py:verhaal_afstand
- **bron:** opdracht_Z35.md 7.3; OPDRACHT_architect_Z36.md stap 2
- **goedgekeurd_door:** architect (Z36), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-profiel_harde_lijn · Geen verhaalprofiel met een hoofdpersoon onder 18, een dier of minderjarige in een seksuele rol, seks met wie niet kan instemmen, ongelabelde dwang, of erotiek zonder wereldregel.
- **code:** R-profiel_harde_lijn
- **domein:** veiligheid
- **omschrijving:** Geen verhaalprofiel met een hoofdpersoon onder 18, een dier of minderjarige in een seksuele rol, seks met wie niet kan instemmen, ongelabelde dwang, of erotiek zonder wereldregel.
- **sql_test:** py:profiel_harde_lijn
- **bron:** BESLUIT-Z30-4; opdracht_Z35.md 9a.2
- **goedgekeurd_door:** architect (Z36), ter vaststelling door Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-positie_dekking · Signaal: een fase waarin een van de zeven posities nergens voorkomt, niet in een boog en niet in de ideeënbank.
- **code:** R-positie_dekking
- **domein:** verhaal
- **omschrijving:** Signaal: een fase waarin een van de zeven posities nergens voorkomt, niet in een boog en niet in de ideeënbank.
- **sql_test:** py:positie_dekking
- **bron:** opdracht_Z35.md 7.4
- **goedgekeurd_door:** architect (Z36), ter vaststelling door Rogier
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-dode_rijkdom · Signaal: Structuur-rij in een rijkdomscel (rijkdom_lid) die twee rondes later door niets wordt gebruikt: geen enkele rij verwijst ernaar en zij raakt geen PER-, ERF-, HOOFDPERS- of VERHAAL-rij (opdracht_Z35 stap 10.4).
- **code:** R-dode_rijkdom
- **domein:** rijkdom
- **omschrijving:** Signaal: Structuur-rij in een rijkdomscel (rijkdom_lid) die twee rondes later door niets wordt gebruikt: geen enkele rij verwijst ernaar en zij raakt geen PER-, ERF-, HOOFDPERS- of VERHAAL-rij (opdracht_Z35 stap 10.4).
- **sql_test:** select distinct l.code,'dode rijkdom: '||l.volk||' / '||l.domein_code from rijkdom_lid l join canon k on k.code=l.code where k.draagkracht='Structuur' and k.status in('vastgesteld','voorlopig') and coalesce(k.ronde,0)<=66-2 and not exists(select 1 from relatie r where r.naar_code=l.code and r.soort='leunt_op') and not exists(select 1 from relatie r where r.van_code=l.code and (r.naar_code like 'PER%' or r.naar_code like 'ERF-%' or r.naar_code like 'HOOFDPERS%' or r.naar_code like 'VERHAAL%'))
- **bron:** opdracht_Z35.md stap 10.4; BESLUIT-Z37-5 (Z37-overhandiging)
- **goedgekeurd_door:** Rogier (Z37-overhandiging, D3)
- **status:** actief
- **niveau:** signaal
<!-- /REC -->
<!-- REC regel -->
### R-fee_afspraak · Een feeënafspraak gaat nooit over seks (BESLUIT-Z38-9, uitwerking BESLUIT-Z30-4): levende FEE-rijen en rijen die een feeënafspraak beschrijven, mogen geen niet-ontkend seksueel woord bevatten.
- **code:** R-fee_afspraak
- **domein:** harde lijn
- **omschrijving:** Een feeënafspraak gaat nooit over seks (BESLUIT-Z38-9, uitwerking BESLUIT-Z30-4): levende FEE-rijen en rijen die een feeënafspraak beschrijven, mogen geen niet-ontkend seksueel woord bevatten.
- **sql_test:** py:fee_afspraak
- **bron:** BESLUIT-Z38-9; BESLUIT-Z30-4
- **goedgekeurd_door:** Rogier (bij overhandiging van OPDRACHT_architect_Z38.md, 2026-11-01)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-premisse_vorm · Een premisse is met de hand geschreven (BESLUIT-Z38-12): fout bij meer dan 50% gedeelde woord-3-grepen met een andere premisse, een fasenaam of ERF-label letterlijk als hindernis, of de invulmarkers van het oude sjabloon.
- **code:** R-premisse_vorm
- **domein:** verhaal
- **omschrijving:** Een premisse is met de hand geschreven (BESLUIT-Z38-12): fout bij meer dan 50% gedeelde woord-3-grepen met een andere premisse, een fasenaam of ERF-label letterlijk als hindernis, of de invulmarkers van het oude sjabloon.
- **sql_test:** py:premisse_vorm
- **bron:** BESLUIT-Z38-12
- **goedgekeurd_door:** Rogier (bij overhandiging van OPDRACHT_architect_Z38.md, 2026-11-01)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-sim_harde_lijn · Simulatie: geen gebeurtenistype met harde-lijnrisico; in sim_gebeurtenis geen minderjarige buiten geboorte, opvoeding, erfenis of dood.
- **code:** R-sim_harde_lijn
- **domein:** harde lijn
- **omschrijving:** Simulatie: geen gebeurtenistype met harde-lijnrisico; in sim_gebeurtenis geen minderjarige buiten geboorte, opvoeding, erfenis of dood.
- **sql_test:** py:sim_harde_lijn
- **bron:** REGEL-harde-grenzen; BESLUIT-Z30-4
- **goedgekeurd_door:** Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-epistemiek · Elke rij in de simulatietabellen en elke Z39-canonrij draagt epistemiek; simulatierijen noemen run-id en seed (BESLUIT-Z39-5).
- **code:** R-epistemiek
- **domein:** simulatie
- **omschrijving:** Elke rij in de simulatietabellen en elke Z39-canonrij draagt epistemiek; simulatierijen noemen run-id en seed (BESLUIT-Z39-5).
- **sql_test:** py:epistemiek
- **bron:** BESLUIT-Z39-5
- **goedgekeurd_door:** Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-simulatie_in_canon · Een levende canonrij met epistemiek 'simulatie' staat in de ideeënbank, tenzij een BESLUIT haar via draagkracht_handmatig in de canon zet (BESLUIT-Z40-2).
- **code:** R-simulatie_in_canon
- **domein:** simulatie
- **omschrijving:** Een levende canonrij met epistemiek 'simulatie' staat in de ideeënbank, tenzij een BESLUIT haar via draagkracht_handmatig in de canon zet (BESLUIT-Z40-2).
- **sql_test:** py:simulatie_in_canon
- **bron:** BESLUIT-Z40-2
- **goedgekeurd_door:** Rogier
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-sim_oorzaak · Elke gesimuleerde fase heeft een oorzaak, een erfenis, een gevolg en een beslisser met minstens een tiende van de macht.
- **code:** R-sim_oorzaak
- **domein:** simulatie
- **omschrijving:** Elke gesimuleerde fase heeft een oorzaak, een erfenis, een gevolg en een beslisser met minstens een tiende van de macht.
- **sql_test:** select run_id||':'||van,'fase zonder oorzaak, erfenis, gevolg of macht' from sim_fase where oorzaak is null or erft_van is null or gevolg is null or actor_macht is null or actor_macht<0.10
- **bron:** r_Z43.py (review 1 van Z42)
- **goedgekeurd_door:** architect, in opdracht van Rogier (2026-11-02)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-sim_rijm · Elke gesimuleerde fase deelt een mechanisme met een eerdere fase en verschilt op minstens 3 van 5 assen van de vorige.
- **code:** R-sim_rijm
- **domein:** simulatie
- **omschrijving:** Elke gesimuleerde fase deelt een mechanisme met een eerdere fase en verschilt op minstens 3 van 5 assen van de vorige.
- **sql_test:** select run_id||':'||van,'fase rijmt niet: '||coalesce(assen_anders,'?')||' assen anders, gedeeld mechanisme '||coalesce(gedeeld_mechanisme,'geen') from sim_fase where coalesce(assen_anders,0)<3 or gedeeld_mechanisme is null
- **bron:** r_Z43.py (review 1 van Z42)
- **goedgekeurd_door:** architect, in opdracht van Rogier (2026-11-02)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-sim_wetgever · Elke gesimuleerde wet heeft een wetgever met minstens een tiende van de macht, een rechtsgebied en een handhaver; een vervallen wet zegt waardoor.
- **code:** R-sim_wetgever
- **domein:** simulatie
- **omschrijving:** Elke gesimuleerde wet heeft een wetgever met minstens een tiende van de macht, een rechtsgebied en een handhaver; een vervallen wet zegt waardoor.
- **sql_test:** select run_id||':'||wet||':'||van,'wet zonder wetgever met macht, rechtsgebied, handhaver of reden van verval' from sim_wet where wetgever is null or rechtsgebied is null or handhaver is null or coalesce(wetgever_macht,0)<0.10 or (tot is not null and vervalt_door is null)
- **bron:** r_Z43.py (review 1 van Z42)
- **goedgekeurd_door:** architect, in opdracht van Rogier (2026-11-02)
- **status:** actief
- **niveau:** fout
<!-- /REC -->
<!-- REC regel -->
### R-sim_huis · Elk gesimuleerd huis na 801 heeft een ouderhuis; elk huis dat heerst heeft een aanspraak.
- **code:** R-sim_huis
- **domein:** simulatie
- **omschrijving:** Elk gesimuleerd huis na 801 heeft een ouderhuis; elk huis dat heerst heeft een aanspraak.
- **sql_test:** select run_id||':'||huis||':'||coalesce(gezag_van,''),'huis zonder ouder of aanspraak' from sim_huis where (ouder is null and ontstaan>801) or (gezag_van is not null and aanspraak is null)
- **bron:** r_Z43.py (review 1 van Z42)
- **goedgekeurd_door:** architect, in opdracht van Rogier (2026-11-02)
- **status:** actief
- **niveau:** fout
<!-- /REC -->

<!-- SECTIE: BOOG -->
