# Ronde Z37: teksten van de besluiten en nieuwe rijen. Elke rij met de hand geschreven, elk een eigen vorm.
R='Rogier (bij overhandiging van OPDRACHT_architect_Z37.md, 2026-11-01)'
PASSAGE=open(__file__.replace('data.py','passage_h32.txt'),encoding='utf-8').read() if __import__('os').path.exists(__file__.replace('data.py','passage_h32.txt')) else ''
# (code, categorie, onderwerp, feit, verwijst_naar, kern)
BESLUIT=[
('BESLUIT-Z37-1','Magie','Twee lagen van de gave: draagvermogen via de moeder, lading via de vader',
 "Rogier, Z37 (A1): de gave heeft twee lagen. Wat een zoon kan dragen, ligt op zijn X-chromosoom en komt dus van de moeder; dat leest Ysa's filter, en daarmee beslist het welke zoon geboren wordt. De gave zelf is een lading die de vader in zijn zaad meegeeft, en die ontbrandt alleen in een zoon die haar kan dragen. Zo ontstaan de twee verhoudingen: 1 op 20 bij zonen van een gaven-man, 1 op 2000 bij zonen van een gewone man, wiens zaad weinig of niets meegeeft (MAGIE-zaadkracht). De moederlijn is de stille helft van elke gaven-zoon. Sluit WRIJ-Z36-1.",
 'BESLUIT-Z36-1;GES-herkomst-gave;BESLUIT-Z6-VRAAG-006;MAGIE-zaadkracht',1),
('BESLUIT-Z37-2','Oorsprong','Hoofdstuk 32: de lijn naar beneden ging dicht',
 "Voor hoofdstuk 32 koos Rogier (A2) de herziene passage in z37/stille_modus_Z37.md: drie jaar voor de brand speelt de Reckoner Thalen het protocol van de Mother voor, en dezelfde nacht gaan de cellen in de beveiligingsschuur stil 'as if a hand had closed over them'. Die passage vervangt deel 2 van stille_modus_Z36.md. In jaar 31 heeft de Reckoner dus geen weg naar beneden, en Thalen begrijpt het pas in jaar 38. Het zaadje ZAAD-Z36-h32-protocol blijft wachten op de roman; de roman zelf verandert niet. Sluit WRIJ-Z36-2.",
 'BESLUIT-Z36-1;ROMAN-Z16-roman',0),
('BESLUIT-Z37-3','Oorsprong',"Hesta breekt twee keer haar eigen ruil",
 "Jaar 3 en jaar 28 horen bij elkaar (Rogier, A3). In jaar 3 test Hesta de deur in de Reckoner, buiten de ruil met de raad om; dat is het blauwe licht. In jaar 28 zet haar hand de cellen aan, omdat Ysa het vraagt en niet de raad. Allebei breken ze hun eigen ruil, en de hand die in jaar 28 de cellen sluit (BESLUIT-Z37-2) is dezelfde. Sluit WRIJ-Z36-3.",
 'BESLUIT-Z36-1;ROMAN-Z16-roman',0),
('BESLUIT-Z37-4','Oorsprong','De Reckoner kent de titel Mother',
 "Ja op KEUZE-Z36-moeder (A4): de Reckoner kent de titel. De downlink naar Ysa's oortje leeft in h25 nog, en vanaf h21 heet ze in het kamp Mother; het zaadje in h32 hoeft dat niet uit te leggen.",
 'ROMAN-Z16-roman;BESLUIT-Z36-1',0),
('BESLUIT-Z37-5','Werkwijze','Aanbevelingen bij de wrijvingen van keuzelijst_Z36: ja, met twee kanttekeningen',
 "Onder het kopje wrijving in keuzelijst_Z36.md zei Rogier ja op alle aanbevelingen van de bouwer (B). Kanttekening 1, WRIJ-Z15-4: Thalen gaat op in Ysara in jaar 0, de nacht van het bloedzegel ('Dat is mooi'). Kanttekening 2, WRIJ-Z33-7: REGEL-harde-grenzen krijgt BESLUIT-Z30-4 als bron; voor REGEL-nageslacht-per-man, REGEL-seksuele-normen, REGEL-doelgroep-toon, MAGIE-zaadkracht en MAGIE-kracht-duur wijst Rogier zelf het besluit of de ronde aan, en 'auteur (Rogier), wereldbijbel, ronde onbekend' mag alleen als hij dat bevestigt. WRIJ-Z29-1 is tekstwerk aan de roman en blijft bij hem. Bij WRIJ-Z21-4 geldt de regel: grotere aantallen bergvolk komen later aan; de 211 van h30 blijven.",
 'BESLUIT-Z30-4;BESLUIT-Z15-7;REGEL-harde-grenzen',0),
('BESLUIT-Z37-6','Werkwijze','Herkomst: een verwijzing naar X is geen bron van X',
 "Nee op de herkomstpunten H01 tot en met H50 (C): ze vervallen, want de methode nam als bron van X een rij die naar X verwijst, en dat is de omgekeerde richting. Wat wel een bron is: een besluit, een hoofdstuk van de roman, een notitie van Rogier, of een rij waarnaar X zelf verwijst en die zelf een bron heeft. Rijen uit de oorspronkelijke wereldbijbel (rondes 1 tot en met 22) krijgen 'auteur (Rogier), ronde N' als hun historie die ronde noemt. Verder wordt niets verzonnen.",
 'BESLUIT-Z33-1',0),
]
# opvolgers (code, oud, categorie, onderwerp, feit, verwijst_naar, status)
OPVOLG=[
('BESLUIT-Z15-7-Z37','BESLUIT-Z15-7','Oorsprong','Thalen gaat op in Ysara: jaar 0, de nacht van het bloedzegel',
 "Thalen gaat op in Ysara in jaar 0, de nacht waarin de Raad het bloedzegel legt. Die nacht wordt de slapende Stille Modus bevestigd (BESLUIT-Z36-1), en langs dezelfde weg wordt zijn patroon wakker, dat de sleutel kent; via de Wortel reikt zijn stem uit de gevallen scheepskern naar het Zegel en versmelt met Ysara. De oude marge 'tussen 0 en ca. 130' vervalt. Rogiers kanttekening bij BESLUIT-Z37-5.",
 'BESLUIT-Z12-wortelstem;GEB-sterrensteen-inslag;PER-ysara;BESLUIT-Z36-1;BESLUIT-Z37-5','vastgesteld'),
('YSA-Z15-9-Z37','YSA-Z15-9','Personage','Thalen bouwt zijn stem en sterft op 74',
 "Als de baan zakt, rond jaar 39-40 na de landing (ca. -1200), bouwt Thalen zelf zijn stem in de kluis 'voor wie later komt' en vergeeft hij Ysa hardop. De mens sterft in -1198, vierenzeventig jaar oud, zoals het anker zegt (BESLUIT-Z18-3); Ysa is dan al dood (-1209). Dit vervangt de 76 uit Z16 (BESLUIT-Z37-5, WRIJ-Z33-8).",
 'ROMANCE-Z15b-ysa-beatplan;PER-v4-ysa-maren;PER-v4-thalen-orr;BESLUIT-Z18-3;BESLUIT-Z37-5','voorlopig'),
('HOOFDPERS-Z37-kluwer','HOOFDPERS-Z4-kluwer','Personage','Kluwers: hoofdpersoon in het Barsten',
 "Werkster Zirr-van-Zeven (PER-kluwer-held-zirr) blijft het gezicht van de Kluwer-verhalen, alleen staat ze in fase 7 Barsten, waar haar eigen rij haar zet, en niet in de Ontvangst. Ze spreekt als 'ik' en onderhandelt namens drie korven; dat is precies waar haar keuze met de rest van het volk botst. (BESLUIT-Z37-5, WRIJ-Z33-4.)",
 'PER-kluwer-held-zirr;PERS-Z4-kluwer-5-1;BESLUIT-Z37-5','vastgesteld'),
('HOOFDPERS-Z37-myrrhen','HOOFDPERS-Z4-myrrhen','Personage','Myrrhen: Ondal in de Markt, jaar 470',
 "Fase 4 kan niet: Myrrhen bestaan pas na de Pest van 470. Ondal Netwever, het lijk dat praat, wordt hoofdpersoon in fase 6 Markt (PER-myrr-ondal). Hij laat zich doorgroeien om niet te sterven en zwijgt over wat het netwerk van de doden onthoudt. (BESLUIT-Z37-5, WRIJ-Z33-4.)",
 'PER-myrr-ondal;PERS-Z4-myrrhen-4-1;BESLUIT-Z37-5','vastgesteld'),
('HOOFDPERS-Z37-veslethi','HOOFDPERS-Z4-veslethi','Personage','Ves-Lethi: Lan-de-Twee vlucht in het Barsten',
 "Bij de Ves-Lethi draagt Lan-de-Twee de verhalen, in fase 7 Barsten volgens PER-veslethi-held-lan en niet in de Noodtoestand. Lan verwekte in de mannelijke fase een kind en is op de vlucht: zo raakt Lan aan het zaadsysteem van de Orde. (BESLUIT-Z37-5, WRIJ-Z33-4.)",
 'PER-veslethi-held-lan;PERS-Z4-veslethi-4-1;BESLUIT-Z37-5','vastgesteld'),
]
VEE=('VEE-Z37-schip','Dieren','Vee van het schip: twee geiten en een hond',
 "Uit de veestapel van het schip kwamen in de roman twee geiten mee met Corran (h30, YSA-Z28-42) en een hond (h25). Ze zijn achtergrond en spelen nooit een seksuele rol (BESLUIT-Z30-4). De vis uit h23 staat er bewust niet bij: niet nagelezen. Of later vee van deze dieren afstamt, is open voor de hoofdserie.",
 'YSA-Z28-37;YSA-Z28-41;YSA-Z28-42;BESLUIT-Z30-4;BESLUIT-Z37-5')
WRIJ_NIEUW=[
('WRIJ-Z37-1','"Erfelijk vanaf jaar 85" tegen bevestiging in jaar 0',
 "BESLUIT-Z6-WRIJ-051 noemt de gave 'erfelijk vanaf jaar 85 (Stille Modus)', en GESCH-karrûk-3, FASE-noodtoestand, OORSPRONG-gave-4-V4 en MAGIE-GESCH-5 zeggen 'het Zegel maakt de gave erfelijk'. Volgens BESLUIT-Z37-1 bestond de lading van de vader al; het Zegel bevestigt in jaar 0 het filter dat beslist welke zoon geboren wordt. Voorstel (niet doorgevoerd): 'erfelijk' leest in die rijen als 'de dragende zonen worden geboren', en jaar 85 is het jaar waarin de registers het patroon voor het eerst zien, rond de derde generatie zonen onder het filter. Tekst niet gewijzigd; Rogier beslist.",
 'BESLUIT-Z6-WRIJ-051;GESCH-karrûk-3;FASE-noodtoestand;OORSPRONG-gave-4-V4;MAGIE-GESCH-5;BESLUIT-Z37-1'),
('WRIJ-Z37-2','"1 op 20" heeft drie betekenissen',
 "'1 op 20' staat voor drie dingen: de kans op de gave bij een zoon van een gaven-man (GES-herkomst-gave, BESLUIT-Z6-VRAAG-006), de geslachtsverhouding van de Sael-Mor (VOLK-sael-mor: 1 man op 20), en de verschuiving van 1 op 100 naar 1 op 20 in BESLUIT-Z32-11. De passage van h32 noemt 'one in a hundred' voor het filter op geboorten. Er is geen tegenspraak, wel verwarring. Voorstel: in nieuwe rijen altijd zeggen welke het is ('gavekans', 'geslachtsverhouding', 'geboortefilter'); oude rijen blijven zoals ze zijn.",
 'GES-herkomst-gave;BESLUIT-Z6-VRAAG-006;VOLK-sael-mor;BESLUIT-Z32-11;BESLUIT-Z37-1'),
]
# naam_markering: (naam_a, naam_b, codes, toelichting)
ERFNAMEN=[
('Varnath Vuurkoning','Varnath II','PER-varnath;OORLOG-Z9-18;BESLUIT-Z6-WRIJ-052','erfnaam: een gaven-generaal in fase 6 neemt de naam van de Vuurkoning (gestorven -6) aan (WRIJ-Z14-1)'),
('Selvara Varenne de Eerste','Selvara Varenne','PER-f6-selvara-eerste-Z37;PER-selvara','erfnaam: de stichteres van de Zaadbeurs (455) is een achternicht, naar de Eerste (375) vernoemd (WRIJ-Z32-2)'),
('Iska Spiegelhuid','Iskar Spiegelvader','PER-barsten-veslethi-Z6;PER-f7-veslethi-nara-oud','erfnaam: Iskar is de vader van Iska en vernoemde het kind naar zich (WRIJ-Z32-3)'),
('Hesk van Hal-Neth','Heske Halfgezicht','PER-f4-grauwe-heske;PER-hesk-kweker','erfnaam: Heske Halfgezicht (jaar 45) is de stammoeder; Hesk draagt haar naam (WRIJ-Z32-4)'),
('Kapitein Vessa','Moeder Vessa','PER-saelmor-schurk-vessa;PER-sch-vessa','erfnaam, bewust: Moeder Vessa neemt in 801 de naam aan die een vloek is (WRIJ-Z32-5)'),
('Nadir Een-Vrouw','Nadir Een-Vrouw (voorouder)','PER-ishvar-nadir;PERS-Z4-ishvar-5-1','erfnaam: de fase-5-rij is een voorouder met dezelfde naam; Nadir zelf leeft in 801 (WRIJ-Z32-6)'),
('Selva Kamerdame','Selvara Varenne de Eerste','PER-f2-selva;PER-f6-selvara-eerste-Z37','zelfde oordeel als bij de Jongere: verschillende tijd, naam verschilt genoeg (BESLUIT-Z32-14)','geen botsing','beoordeeld: verschillende tijd of volk, naam verschilt genoeg (BESLUIT-Z32-14)'),
('Koning Ardemar III','Koning Ardemar IV de Graanvorst','PER-ardemar-iv-Z37;PER-f1-ardemar-derde-Z37','erfnaam: twee koningen; de Graanvorst (-180) is Ardemar IV en draagt de naam van Ardemar III (WRIJ-Z32-1)'),
]
