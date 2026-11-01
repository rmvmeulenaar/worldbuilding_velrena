# Ronde 13: andere volken, functie eerst (idempotent)
import sqlite3;c=sqlite3.connect('canon.db')
F=['Functie','Oorsprong','Geslachtsverhouding en voortplanting','Cultuur','Religie','Politiek','Zaadsysteem en Orde','Lichaam en body horror','Seksuele cultuur','Regio, huizen, conflict']
V=[
('VOLK-aelthir','De Aelthir (de Langlevenden)','INFO;DIPLO','REG-nevel-eilanden-noord;REG-hoogvrouwe',
["Geheugen van de wereld: zij herinneren zich de tijd vóór de Zegel; de Orde heeft hen nodig om oude kennis, de Stille Zusters om bewijs.",
 "Ouder dan de mensen: een volk dat al bestond toen de Sterrensteen viel; de steen kortte hun leven niet maar hun vruchtbaarheid.",
 "Ongeveer gelijk, maar slechts één kind per eeuw; ze zijn het omgekeerde van de mensen: veel mannen, bijna geen kinderen. Ze leven 400 jaar en zijn volwassen in menselijke maat.",
 "Traag, ceremonieel, alles in herhaling; schoonheid als discipline.","Geen goden, wel de Rekening: elk leven heeft een vaste hoeveelheid verlangen.","Raad van Oudsten; wie het meest herinnert, beslist.",
 "Hun mannen hebben geen gave, maar hun zaad geneest de Leegte tijdelijk; de Orde koopt het in het geheim (verboden handel).",
 "De prijs van lang leven: hun huid wordt doorschijnend, je ziet aderen en organen; na 300 jaar verliezen ze gevoel. Afstoting 3.",
 "Zeldzaam, langzaam, ritueel; trekken mensen aan om verlangen te voelen dat ze zelf kwijt zijn (VOOR-teder, VOOR-ritueel, VOOR-oudere-vrouw).",
 "Leven in de mist van de verre Nevel-eilanden en in grotten van Hoogvrouwe; handel via Huis Mirre; conflict: de Orde wil hun geheugen stilhouden."],
 'HUI-mirre;REG-stille;GEB-sterrensteen-inslag;LICH-leegteziekte;VOOR-teder;VOOR-ritueel;VOOR-oudere-vrouw;PLEK-LICH-nevel;PLEK-LICH-stille-klooster'),
('VOLK-karrûk','De Karrûk (het krijgersvolk)','MIL;HECHT','REG-kharvos',
["Huurkracht en grensmuur: Kharvos gebruikt hen als stoottroep; voor Velmara zijn ze de reden dat de Amberpas bewaakt moet worden.",
 "Afsplitsing: mensen in de zegelschaduw van Kharvos, waar de Zegel zwak is; ze kregen geen 1 op 100 maar 1 op 3, en hun vonk ontladen ze in strijd.",
 "1 man op 3; vrouwen kiezen mannen in wedstrijden. Weinig inteelt, veel bloedvetes.",
 "Eer, schuld en wraak; elke dode wordt gedragen als ingekerfd teken.","De Storm: kracht moet ontladen, anders verbrandt hij je (een religie gebouwd op vonkkoorts).","Clans met een kampioen die elk jaar herkozen wordt in een gevecht.",
 "Ze verachten de Orde ('melkers'); hun mannen worden in Velmara op de zwarte markt verkocht als ruw zaad, wat de Orde verbiedt en Varenne heimelijk koopt.",
 "Kookhuid en blaren bij wie niet ontlaadt (zoals LICH-grensmannen); oudere krijgers hebben verkoolde handen. Afstoting 4.",
 "Competitie, kracht, rolwissel (vrouwen kiezen en leiden), ontlading na strijd (VOOR-competitie, VOOR-rolwissel, VOOR-ontlading, VOOR-dominante-vrouw).",
 "Kharvos-hooglanden; vijand van Kaldra; Khaled-Ir zoekt hen als bondgenoot; conflict bij de Amberpas."],
 'REG-kharvos;HUI-kaldra;PER-khaled;LICH-grensmannen;LICH-vonkkoorts;VOOR-competitie;VOOR-rolwissel;VOOR-ontlading;VOOR-dominante-vrouw;PLEK-LICH-zegelschaduw;PLEK-LICH-slagveld-amberpas;GEB-r10-kharvos-scheiding'),
('VOLK-dhurn','De Dhurn (het bergvolk)','ECO;INFO','REG-hoogvrouwe',
["Mijnwerkers van de Sterrensteen: alleen zij kunnen hem bewerken zonder te verbranden; zonder hen geen Zegelinkt, geen merkweefsel, geen wijdingsgoud.",
 "Gevolg van de Sterrensteen: nazaten van de mijnwerkers van Orric die eeuwenlang straling verdroegen; ze zijn gesloten en ingeteeld geraakt.",
 "Vrouwen zijn onvruchtbaar tot ze een jaar bij de steen hebben gewoond; kinderen zijn zeldzaam en ingeteeld; ze kopen vreemd bloed via bloedgezanten.",
 "Zwijgzaam, ambachtelijk, schuld-cultuur: ze voelen zich schuldig aan Orric.","Ze vereren Orric als heilige die versteende om hen te redden.","Gildenraad van mijnmeesters.",
 "Leveranciers van de Orde, maar tegen hun zin; ze weten dat de Zegel lekt (ze zien het in de steen).",
 "Steenhuid op knieën en handen, zwarte nagels, ogen die gloeien in het donker; inteeltgebreken (bloedspiegel-ogen). Afstoting 3.",
 "Uithouding, binding, het verbodene (verwantschap is hun grootste angst én obsessie: VOOR-uithouding, VOOR-verboden, VOOR-binding).",
 "Hoogvrouwe-gebergte rond Ves-Anath; conflict met de Orde over de steen; Liora en Teo hebben hen nodig als gids."],
 'REG-hoogvrouwe;GEB-orric-vonk;GEB-r10-eerste-vervorming;LICH-bloedspiegel;LICH-merkweefsel;LICH-orric-steen;LICH-vreemdbloed;VOOR-uithouding;VOOR-verboden;VOOR-binding;PLEK-LICH-ves-anath;PLEK-LICH-pelgrimsweg'),
('VOLK-sael-mor','De Sael-mor (het zeevolk)','DIPLO;ECO','REG-zoutkust;REG-nevel-eilanden',
["Dragers van vreemd bloed: zij brengen nieuw bloed tussen regio's en zijn daarom de levensader tegen inteelt.",
 "Afsplitsing: vrouwen die tijdens de Grote Brand op zee bleven, buiten bereik van de Zegel; ze leven op schepen en zijn half aan het water aangepast.",
 "1 man op 20; mannen worden gedeeld tussen schepen; kinderen worden aan boord geboren en het register is mondeling.",
 "Nomadisch, handelend, vrolijk-cynisch; trouw aan het schip, niet aan land.","De Diepe Moeder: de zee neemt en geeft; een verdrinking is een terugkeer.","Kapiteinsraad; schepen stemmen.",
 "Ze verkopen mannen en Grijswortel aan Mirre; de Orde noemt hen ketters maar heeft hun bloed nodig.",
 "Zoutkorsten op de huid, kieuwachtige spleten in de hals die bloeden op het land; na jaren aan land rotten ze. Afstoting 3.",
 "Reizigers, anonieme liefde, groep en ruil (VOOR-reiziger, VOOR-anoniem, VOOR-groep, VOOR-handel).",
 "Zoutkust en Nevel-eilanden; partner van Huis Mirre; conflict met Varenne om de mannenhandel."],
 'HUI-mirre;HUI-varenne;REG-zoutkust;LICH-vreemdbloed;LICH-gijzelaarsband;VOOR-reiziger;VOOR-anoniem;VOOR-groep;VOOR-handel;PLEK-LICH-mirre-havens;PLEK-LICH-nevel'),
('VOLK-grauwen','De Grauwen (het vervormde randvolk)','AFSCHR;SELECT','REG-groenmuil',
["Levend schrikbeeld: zij zijn wat er gebeurt als je het register breekt; de Orde gebruikt hen als waarschuwing.",
 "Gevolg van inteelt: nazaten van dorpen zonder register (de nevenramp) en van verstoten lampenkinderen; een eigen volk geworden.",
 "1 man op 100 zoals de mensen, maar ze delen binnen het volk; inteeltgebreken in elke generatie.",
 "Hecht, beschermend, verbitterd; ze zorgen voor elkaar zoals niemand anders.","Ze vereren de Vergane Zonen als hun voorouders.","Geen leiders; dorpsraden.",
 "Uitgesloten van de rotatie; ze stelen of kopen mannen van de Karrûk; de Orde wil hen uitsterven laten, de Stille Zusters helpen hen.",
 "Vergroeide vingers, dubbele irissen, witte vlekken, botgroei; het zwaarste body horror. Afstoting 5.",
 "Tederheid binnen, wantrouwen buiten; sommige mensen zoeken hen op uit angstlust (VOOR-teder, VOOR-verboden). Alleen volwassenen.",
 "Groenmuil-moerassen; conflict met de Orde; toevlucht voor Liora en Teo."],
 'REG-groenmuil;GEB-r10-neven-ramp;LICH-lampenkinderen;LICH-bloedspiegel;LICH-vergane-zonen;VOOR-teder;VOOR-verboden;PLEK-LICH-lampenfeest;PLEK-LICH-stille-klooster'),
('VOLK-ishvar','De Ishvar (zij die de Zegel niet voelen)','INFO;POL','REG-rosse',
["Ijkpunt: alleen bij hen zie je hoe mensen zonder Zegel zijn; voor Qesh zijn ze een geheim wapen, voor de Orde een ketterij.",
 "Woestijnvolk van Qesh dat nooit Sterrensteen-stof in het water kreeg (zie GEB-r10-qesh-afwijking); de Zegel raakt hen niet.",
 "1 op 2, paarvorming, kleine families; geen gave, geen Leegte.","Strikt, woordvast, trots op gewoonheid.","Zon als getuige; geen offer, alleen eden.","Families met een zonvorst als bemiddelaar; Khaled-Ir is half Ishvar.",
 "Hun mannen hebben geen zaad-kracht en zijn waardeloos voor de Orde; daardoor vrij. Maar in Velmara worden ze gezocht als gewone, rustige partners.",
 "Geen body horror van de Zegel, maar wel van de woestijn: zonbrand, gelooide huid; bij ontvangst van gaven-zaad krijgen hun vrouwen brandwonden. Afstoting 2.",
 "Trouw, tweegelofte, tederheid; voor Velmara-vrouwen het exotische 'één man voor jou alleen' (VOOR-teder, RIT-tweegelofte).",
 "Rosse Woestijn; onder Qesh; conflict: de Orde wil hun bestaan geheim houden."],
 'REG-rosse;HUI-qesh;PER-khaled;GEB-r10-qesh-afwijking;GEB-r10-khaled-pact;RIT-tweegelofte;VOOR-teder;PLEK-LICH-qesh'),
('VOLK-vathren','De Vathren (zegelgeborenen)','INFO;REL','REG-hoogvrouwe',
["Zegelvoelers: zij voelen de Zegel als hartslag en kunnen een lek voorspellen; de Orde heeft hen nodig en vreest hen.",
 "Gevolg van de Zegel: volwassen zegelgeboorten die het Jongenshof ontvluchtten of verstoten werden en samen een volk vormden; aangevuld met lekkinderen sinds 750.",
 "Alleen mannen bij oorsprong; ze nemen vrouwelijke gezellen op; hun kinderen zijn bijna allemaal zegelgeboren.",
 "Mystiek, gebroken, gemeenschap van overlevenden.","Zij vereren de Zegel als een levend wezen dat sterft.","Ziener-raad.",
 "Hun zaad is gevaarlijk: kracht zonder rem; de Orde jaagt op hen, Morvane-ir wil ze gebruiken.",
 "Gloeiende littekens, doofheid, aderen van zegellicht; afstoting 4.",
 "Angstlust en ontzag; ze worden gezocht door wie de grens wil voelen (VOOR-geest, VOOR-pijn-genot). Alleen volwassenen.",
 "Rond Ves-Anath; conflict met de Orde en met Morvane-ir; sleutel voor Liora's quest."],
 'REG-hoogvrouwe;LICH-zegelgeboorte;GEB-r10-lekgeboorten;PER-morvane;PER-liora;VOOR-geest;VOOR-pijn-genot;PLEK-LICH-jongenshof;PLEK-LICH-ves-anath'),
]
n=0
for code,nm,fu,reg,vals,refs in V:
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): continue
  feit=' '.join(f"{k}: {v}" for k,v in zip(F,vals))+" Alle seksuele rollen alleen volwassen (18+), humanoïde en sprekend. [Waar zaad-kracht of zegelwerking meespeelt: hangt af van magietheorie; voorlopig.]"
  import re; af=int(re.search(r'[Aa]fstoting (\d)',vals[7]).group(1))
  r=refs+';'+';'.join('FUNC-'+x for x in fu.split(';'))+';'+reg.replace('REG-nevel-eilanden-noord','').replace('REG-nevel-eilanden','').strip(';')
  r=';'.join(dict.fromkeys(x for x in r.split(';') if x))
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,functie,afstoting) values('Volken',?,?,'voorlopig','Ronde 13: volken, functie eerst',?,13,?,?,?,?)",(nm,feit,r,code,r,fu,af));n+=1
W=[('WRIJ-062','Karrûk 1 op 3 versus 1 op 100','VOLK-karrûk; REGEL-verhouding','De zegelschaduw moet een lokale uitzondering zijn; past bij WRIJ-054 en WRIJ-061.','mogelijke fout','VOLK-karrûk;REGEL-verhouding'),
('WRIJ-063','Aelthir ouder dan de mensen','VOLK-aelthir; GES-officiele-versie','Een volk dat zich alles herinnert maakt de vervalste annalen kwetsbaar: waarom spreken ze niet?','bron van verhalen','VOLK-aelthir'),
('WRIJ-064','Vathren en het Jongenshof','VOLK-vathren; GEB-r10-jongenshof','Ontsnapte zegelgeborenen moeten volwassen zijn wanneer ze zich bij het volk voegen; leeftijd en route vastleggen.','mogelijke fout','VOLK-vathren;GEB-r10-jongenshof')]
for code,t,d,b,ty,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone(): c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,'open',?,?)",(t,d,b,ty,code,v));n+=1
Q=[('VRAAG-036','Welke van de 7 volken houdt Rogier, en hoe zichtbaar zijn ze in het verhaal?','Bepaalt de schaal van de wereld.','VOLK-aelthir'),('VRAAG-037','Zijn er volken met een wezenlijk andere lichaamsbouw (niet-menselijk), of blijven alle volken humanoïde varianten van mensen?','Raakt geloofwaardigheid en de harde grenzen.','VOLK-dhurn')]
for code,v,w,r in Q:
  if not c.execute("select 1 from open_vraag where code=?",(code,)).fetchone(): c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,code,r));n+=1
if not c.execute("select 1 from logboek where wat like 'Ronde 13:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30','Ronde 13: 7 volken (VOLK-), functie eerst, met oorsprong uit Sterrensteen, Zegel, zegelschaduw of inteelt; nieuw domeinbestand 15_volken.md.')")
c.commit();print('wijzigingen',n)
codes={r[0] for r in c.execute('select code from canon')}
print('ontbrekend',{x for (v,) in c.execute("select verwijst_naar from canon where ronde=13") for x in v.split(';') if x not in codes})
