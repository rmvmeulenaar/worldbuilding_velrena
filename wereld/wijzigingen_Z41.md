# Ronde Z41: de verhalengraaf laten kloppen

Gebouwd door de architect op verzoek van Rogier (2026-11-01). Script: `r_Z41.py` (idempotent: een tweede run wijzigt niets). Elke wijziging staat in de tabel `wijziging` met ronde `Z41`.

## Uitkomst

| meting (graaf_export.py) | voor | na |
|---|---|---|
| verhaallijnen | 919 | 919 |
| draden naar een oude versie van een rij | 851 | **0** |
| doodlopende verwijzingen | 19 | **0** |
| zwevende haken (alleen aan een besluit) | 35 | **0** (1 Kern-rij overgeslagen) |
| verhalen met een signaal | 83 | **8** |
| verhalen met een pad naar 801 | 903 | **915** |
| personages die onder twee codes staan | 133 (gesplitst) | 133 samengevoegd tot één knoop |

Controles:
- `toets.py` geeft 0 nieuwe fouten.
- Roundtrip: alle tabellen hebben 0 verschillen (na `genereer.py`).
- De 111 Kern-rijen zijn ongewijzigd.
- Er is niets verwijderd: 7.264 rijen werden 7.268.
- Dode links: 0.

## Wat er gebeurde

1. **Draden** (2.110 rijen). Een verwijzing naar een vervangen rij wijst nu naar de levende opvolger. Voorbeeld: PER-liora gaat naar PER-liora-Z6-Z32. Kern-rijen zijn niet aangeraakt; daar is een BESLUIT voor nodig.
2. **Doodlopend.**
   - 15 vervallen gebeurtenissen wijzen nu naar hun levende tweeling. Voorbeelden: GEB-vonkpest gaat naar GEB-vonkkoorts, GEB-rotatiewet naar GEB-r10-rotatie.
   - Voor 4 gebeurtenissen bestond geen opvolger. Daarvoor zijn nieuwe gebeurtenissen gemaakt, als **voorlopig in de ideeënbank** en zonder jaar (de oude jaartallen waren vervallen):

     | nieuwe gebeurtenis | fase |
     |---|---|
     | GEB-Z41-zegel-flakkert | 7 |
     | GEB-Z41-kharvos-stichting | 1 |
     | GEB-Z41-raad-zegelplan | 3 |
     | GEB-Z41-kaldra-eed | 4 |
3. **Haken.** 34 haken kregen knopen op grond van een naam of ding dat letterlijk in hun eigen tekst staat. Voorbeelden: Elin, Kharvos, de Wieg, de Zaadbeurs, de Orrim.
4. **Identiteit.** Er is een nieuwe afgeleide tabel `persoon_identiteit` met de view `v_persoon`, gebouwd in `afgeleid_motor.py`. Personagecodes met dezelfde codestam of dezelfde naam vormen één persoon. Gecontroleerd: één samenvoeging overspant twee fasen, Vaelorn Hoogaelthir (fase 1 en 801). Dat klopt, want zij is een Aelthir en dus langlevend.
5. **Tijd.**
   - QST-etappes-queeste en NU-conflict-schuld stonden in fase 6, maar spelen in 801 (Liora's queeste, Selvine en Kreel). Hun fase is aangepast.
   - HELD-SKELET-Z10-6 wees naar Hethra Brakmoeder (fase 3). Het gaat om een andere Hethra (erfnaam), dus die link is verwijderd.
   - Ysara en Elin in verhalen uit 801 staan als bewuste uitzondering in `toets_uitzondering` (graaf_tijd): de Dochters leven in de steen.

## Wat Rogier nog kan beslissen

- De 4 nieuwe gebeurtenissen: houden, een jaar geven, of schrappen.
- De 8 overgebleven signalen zijn echte vragen, geen fouten:

  | verhaal | vraag |
  |---|---|
  | HORROR-SKELET-Z9-5 | Brams naam in fase 6: profetie of fout? |
  | HORROR-SKELET-Z9-3 | Brakka uit fase 6 in fase 1 |
  | ORIGIN-onthulplan, -ysa | Kern; plan, geen verhaal |
  | HAAK-B1-5-4, COMEDY-SKELET-Z10-5, HORROR-SKELET-Z9-9 en Z9-10 | eilanden: knopen die nog geen tweede verhaal dragen, en dus entpunten |
