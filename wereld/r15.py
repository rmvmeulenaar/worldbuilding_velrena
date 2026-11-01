# Ronde 15: uiterlijk en seksuele cultuur per volk (idempotent)
import sqlite3;c=sqlite3.connect('canon.db');n=0
K=['Uiterlijk','Lichaam en voortplanting','Partnerwisseling en paringsritueel','Tijdsritme','Wat hen opwindt','Voorkeuren','Rituelen','Taboes','Wat ze mensen bieden of willen','Contact met mensen en andere volken']
S=[
('aelthir','De Aelthir',['Lang en smal, doorschijnende huid waarin aderen en hartslag zichtbaar zijn; zilvergrijs haar, ogen zonder wit. Oud ogen ze jong, maar hun huid wordt met de eeuwen glaziger.',
 'Menselijke anatomie, maar met trage reactie: opwinding bouwt uren op; vrouwen zijn één keer per eeuw vruchtbaar, en dat voelen ze als een koorts van weken.',
 'Vaste paren per eeuw, met ritueel afscheid; in de vruchtbare koorts kiest de vrouw drie partners voor één nacht.','Eén lange nacht per maancyclus, die tot dageraad duurt; de rest van de tijd onthouding als discipline.',
 'Gevoel terugkrijgen: langzaamheid, aanraking die pas na uren iets opwekt, en de rauwe haast van mensen.','VOOR-teder:2;VOOR-ritueel:3;VOOR-oudere-vrouw:2;VOOR-geest:3;VOOR-ontzegging:3',
 'De Nacht van de Rekening: geliefden tellen samen hoeveel verlangen ze nog hebben.','Haast; verlangen verspillen; een nacht onderbreken.',
 'Ze bieden mensen geduld en kennis (en zaad dat de Leegte verlicht); ze willen van mensen de felheid die zij kwijt zijn.','Zeldzaam en duur; mensen ervaren het als bedwelmend traag; Mirre bemiddelt; de Orde verbiedt het officieel en koopt het heimelijk.'],'VOLK-aelthir;VOOR-teder;VOOR-ritueel;VOOR-oudere-vrouw;VOOR-geest;VOOR-ontzegging;LICH-leegteziekte;HUI-mirre'),
('karruk','De Karrûk',['Breed, zwaar gespierd, rossig tot koperen huid vol ingekerfde rouwtekens; oudere krijgers met verkoolde handen; tanden licht gevijld als clanteken.',
 'Menselijk, maar met de vonk: na de strijd stijgt de lichaamswarmte en moet een man ontladen, anders begint de kookhuid; vrouwen dragen kort (zeven maanden).',
 'Vrouwen kiezen na wedstrijden; elk seizoen nieuwe partners, behalve bij een bloedeed.','Na elke slag of wedstrijd een ontladingsnacht; in vredestijd elke volle maan het Vuurkamp.',
 'Kracht, uitdaging, winnen en verliezen, de hitte van de ontlading.','VOOR-competitie:4;VOOR-rolwissel:3;VOOR-ontlading:4;VOOR-dominante-vrouw:4;VOOR-groep:3;VOOR-pijn-genot:3',
 'Het Vuurkamp: worstelen waarbij de winnares kiest; de Kerfnacht, waarin een geliefde een litteken krijgt.','Een man die weigert te ontladen (brengt vuur over het kamp); seks met een verwante clan.',
 'Ze bieden ruw, krachtig zaad zonder Orde-regels; ze willen vrouwen die durven te vechten en mannen die durven te verliezen.','Op de zwarte markt en aan de grens; Velmara-vrouwen zoeken Karrûk uit rolwissel-verlangen; Kaldra verbiedt het, maar het gebeurt in elk grenskamp.'],'VOLK-karrûk;VOOR-competitie;VOOR-rolwissel;VOOR-ontlading;VOOR-dominante-vrouw;VOOR-groep;VOOR-pijn-genot;KINK-rolwissel-in-kharvos;LICH-grensmannen'),
('dhurn','De Dhurn',['Gedrongen, steenhuid op knieën, ellebogen en handen, zwarte nagels; ogen die in het donker zacht gloeien; veel bloedspiegel-ogen.',
 'Menselijk, maar vrouwen zijn pas vruchtbaar na een jaar bij de steen; de steenhuid maakt aanraking ruw; seks gebeurt bij voorkeur in warme mijnbaden.',
 'Strikt gecontroleerd door de Gildenraad om inteelt te vermijden; vaste paren per mijnseizoen; vreemd bloed is een feest.','Twee keer per jaar het Baden, in de warme mijnbronnen; verder zuinig.',
 'Uithouding, het verbodene (verwantschap is hun obsessie en grootste angst), en vreemdheid van buitenstaanders.','VOOR-uithouding:4;VOOR-verboden:3;VOOR-binding:3;VOOR-reiziger:3',
 'Het Baden; de Vreemdelingsnacht, waarin een bloedgezant wordt ontvangen door wie het gilde aanwijst.','Seks binnen de lijn; seks bij de steen zonder handschoen (verbrandt).',
 'Ze bieden mensen gidsen en Sterrensteen-werk; ze willen vers bloed, zonder dat het hun eigen lijnen vervuilt.','Via bloedgezanten (LICH-vreemdbloed); voor Liora en Teo betekent hulp vaak een Vreemdelingsnacht als prijs, met keuze en instemming.'],'VOLK-dhurn;VOOR-uithouding;VOOR-verboden;VOOR-binding;VOOR-reiziger;LICH-vreemdbloed;LICH-bloedspiegel'),
('saelmor','De Sael-mor',['Slank, met zoutkorsten op schouders en dijen, kieuwachtige spleten in de hals, zeegroene ogen; huid koel en vochtig; tatoeages van stromingen.',
 'Menselijk, maar paren vooral in het water; door de kieuwen kunnen ze lang onder blijven, wat seks onder water mogelijk maakt; kinderen worden aan boord geboren.',
 'Mannen (1 op 20) worden tussen schepen gedeeld; vrouwen onder elkaar is de norm aan boord; partners wisselen per haven.','Per haven en per getij: de Springtij-nachten zijn feest.',
 'Water, anonimiteit, ruil, het nieuwe en vreemde.','VOOR-reiziger:4;VOOR-anoniem:3;VOOR-groep:3;VOOR-handel:3;VOOR-vrouwenliefde:3',
 'Springtij-nacht; het Zoutkus-ritueel waarbij een nieuwe gezel zout van de huid likt als eed.','Seks op het droge met een kapitein; een geliefde vasthouden als het schip vertrekt.',
 'Ze bieden vreemd bloed en vrijheid; ze willen havenmannen en verhalen.','Vrij in Zoutkust en Mirre-havens; Varenne ziet hen als concurrent in de mannenhandel.'],'VOLK-sael-mor;VOOR-reiziger;VOOR-anoniem;VOOR-groep;VOOR-handel;VOOR-vrouwenliefde;HUI-mirre'),
('grauwen','De Grauwen',['Vergroeide vingers, dubbele irissen, witte vlekken, botgroei op schouders; ieder lichaam anders; ze dragen grauwe doeken.',
 'Menselijk maar met inteeltgebreken: velen onvruchtbaar of pijnlijk bij seks; ze gebruiken zalven en trage, zorgvuldige aanraking.',
 'Delen binnen het volk, met strenge eigen lijsten om verdere inteelt te stoppen; buitenstaanders zijn kostbaar.','Geen vast ritme; nabijheid is dagelijks, seks zeldzaam en zorgvuldig.',
 'Tederheid, geaccepteerd worden zoals je bent, een buitenstaander die niet wegkijkt.','VOOR-teder:2;VOOR-verboden:2;VOOR-vrouwenliefde:2;VOOR-lichaam:3',
 'De Ontsluiering: een geliefde neemt de doek af en kijkt.','Spot; kijken zonder ontsluiering; seks binnen dezelfde lijn.',
 'Ze bieden toevlucht en loyaliteit; ze willen vers bloed en waardigheid.','Mensen uit angstlust die hen opzoeken worden weggestuurd; wie blijft en kijkt, wordt familie.'],'VOLK-grauwen;VOOR-teder;VOOR-verboden;VOOR-vrouwenliefde;VOOR-lichaam;LICH-lampenkinderen'),
('ishvar','De Ishvar',['Donker gelooid door de zon, lange vlechten, gouden oorringen als gelofte; geen enkel zegelteken, wat in Velmara opvalt.',
 'Gewoon menselijk; geen gave, geen Leegte; Ishvar-vrouwen krijgen brandwonden als ze gaven-zaad ontvangen.',
 'Paren voor het leven met een tweegelofte; ontrouw is zeldzaam en wordt openbaar uitgesproken.','Dagelijks, na zonsondergang in de tent.',
 'Woordvastheid, trouw, langzaam opbouwen, het spreken tijdens seks (eden fluisteren).','VOOR-teder:2;VOOR-binding:2;VOOR-ritueel:2',
 'De Tweegelofte onder de zon; de Zonnacht na een huwelijk.','Delen van een partner; gaven-zaad.',
 'Ze bieden één man voor één vrouw, voor Velmara-vrouwen exotisch; ze willen niets van het zaadsysteem.','Velmara-vrouwen die met een Ishvar trouwen verlaten de Orde; Khaled-Ir gebruikt die huwelijken politiek.'],'VOLK-ishvar;VOOR-teder;VOOR-binding;VOOR-ritueel;RIT-tweegelofte;PER-khaled'),
('vathren','De Vathren',['Gloeiende littekens als zegelpatronen, aderen van zegellicht, vaak doof; ze communiceren met handen en hartslag.',
 'Mannen zonder rem: hun zaad geeft kracht maar ook koorts; partners moeten het in kleine doses ontvangen; kinderen zijn bijna allemaal zegelgeboren.',
 'Vrouwelijke gezellen worden opgenomen met instemming; Vathren delen gezellen binnen de Ziener-raad.','Seks volgt de hartslag van de Zegel: bij lekpieken worden ze onrustig en zoeken ze nabijheid.',
 'De grens voelen; seks als waarneming (ze voelen de Zegel door de partner heen).','VOOR-geest:4;VOOR-pijn-genot:3;VOOR-overgave:3;VOOR-ritueel:3',
 'De Hartnacht: met handen op elkaars borst tot de hartslagen samenvallen.','Seks tijdens een lek zonder ziener erbij; een gezel vasthouden die weg wil.',
 'Ze bieden voorspelling en navigatie; ze willen gezellen die hun gloed verdragen, zoals Liora.','Gevaarlijk: wie te veel ontvangt krijgt zegelkoorts; de Orde jaagt op contact, Morvane-ir zoekt het.'],'VOLK-vathren;VOOR-geest;VOOR-pijn-genot;VOOR-overgave;VOOR-ritueel;PER-liora;PER-morvane;NAV-hartstem'),
]
for k,nm,vals,refs in S:
  code='SEKS-VOLK-'+k
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): continue
  f=' '.join(f"{a}: {b}" for a,b in zip(K,vals))+" Alles tussen volwassen, sprekende, instemmende wezens (18+); geen dieren."
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar) values('Volken seksualiteit',?,?,'voorlopig','Ronde 15: uiterlijk en seksuele cultuur per volk',?,15,?,?)",(nm+': uiterlijk en seksuele cultuur',f,refs,code,refs));n+=1
if not c.execute("select 1 from open_vraag where code='VRAAG-041'").fetchone():
  c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values('Welke volken krijgen in de eerste boeken een eigen seksuele scènelijn?','Bepaalt welke culturen eerst diepte krijgen.','open','VRAAG-041','SEKS-VOLK-karruk;SEKS-VOLK-saelmor')");n+=1
if not c.execute("select 1 from wrijving where code='WRIJ-069'").fetchone():
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values('Ishvar-brandwonden versus Liora','SEKS-VOLK-ishvar; LICH-zegelkoorts-liora','Ishvar-vrouwen verbranden aan gaven-zaad; Liora juist niet. Is Liora deels Ishvar?','bron van verhalen','open','WRIJ-069','SEKS-VOLK-ishvar;PER-liora')");n+=1
if not c.execute("select 1 from logboek where wat like 'Ronde 15:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30','Ronde 15: uiterlijk en seksuele cultuur van alle 7 volken (SEKS-VOLK-), met VOOR-intensiteiten; nieuw bestand bijbel/16_volken-uiterlijk-en-seks.md.')")
c.commit();print('wijzigingen',n)
codes={r[0] for r in c.execute('select code from canon')}
print('ontbrekend',{x for (v,) in c.execute("select verwijst_naar from canon where ronde=15") for x in v.split(';') if x not in codes})
