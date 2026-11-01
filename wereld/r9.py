# Ronde 9 (eenmalig; niet opnieuw draaien)
import sqlite3;c=sqlite3.connect('canon.db')
c.execute("update canon set status='vervallen' where categorie in('Tijdperk','Geschiedenis') and ronde=8")
def add(cat,code,o,f,r,refs,jaar=None,tp=None,ins=None,weet=None):
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet) values(?,?,?,'voorlopig',?,?,9,?,?,?,?,?,?)",(cat,o,f,r,refs,code,refs,jaar,tp,ins,weet))
F=[
('FASE-overvloed','De Overvloed en de Kroon',-600,-150,'institutie na overvloed','Overleven en voedsel (de delta geeft overschot)',
 'Wie verdeelt het overschot?','Koningschap en erfrecht via de vader.','Vrouwen worden erfgoed; kuisheid als wet.','Koningen en hun zonen.','Vrouwen en dochters.',
 'Officieel: “de tijd van de wrede mannen”. Verborgen: de Zusters van Ysa groeiden in die tijd uit tot een schaduwmacht met kennis van kruiden, geboorte en Sterrensteen.',
 'Voedsel: overschot. Bevolking: ±1 op 2, snelle groei. Macht: koningen. Geloof: Ysa als oogstgodin. Magie: Sterrensteen valt (-480), nog niet begrepen.',
 'Paarvorming en harems; kuisheid voor vrouwen, losbandigheid voor koningen; vrouwenliefde in het geheim in Zusterhuizen; Oogstfeesten als enige vrije nacht.',
 'Weinig: gezonde lichamen, kraamsterfte, eerste brandwonden bij wie Sterrensteen aanraakt.',
 [('GEB-sterrensteen-inslag',-480,'Inslag van de Sterrensteen','Meteoriet in het Hoogvrouwe-gebergte; gloeit bij levend bloed.','REG-hoogvrouwe;RIT-wijding','Volk: geschenk van Ysa. Orde: bron van de Vonk. Niemand: herkomst.'),
  ('GEB-haremwet-ardemar',-300,'De Haremwet van Ardemar III','Eén koning, honderden vrouwen; kuisheid voor alle anderen.','KINK-harem-gunst;REG-saelith','Volk: als zonde onthouden. Orde: verzwegen model voor het latere systeem.'),
  ('GEB-zusterburcht',-220,'De Zusterburcht van Ves-Anath','Vrouwen vluchten uit harems; Zusters leren bloedmagie met Sterrensteen.','REG-stille;ORDE-orde','Orde: ja. Volk: nee.')]),
('FASE-vonk','De Vonk',-150,-40,'omslag in magie: uitbreiding','Technologie en magie (de Vonk ontwaakt in mannen)',
 'Een kracht die alleen sommige mannen hebben, zonder regels.','Vonkdragers worden koningen; hun zaad maakt vrouwen-legers sterk.','De Vonkkoorts: wie niet ontlaadt, verbrandt van binnen.','Vonkkoningen.','Gewone mannen, vrouwen als krachtbron en buit.',
 'Officieel: er waren geen gaven vóór jaar 210. Verborgen: de Vonk is de echte oorsprong van de gave, en de Zegel heeft haar alleen geconcentreerd.',
 'Voedsel: nog overschot. Bevolking: 1 op 2. Macht: Vonkkoningen. Geloof: mannen als halfgoden. Magie: zaad-kracht ontdekt.',
 'Zaad wordt koopwaar; vrouwen zoeken vonkdragers; de eerste Strijdontvangsten; ontlading wordt een plicht van de partner.',
 'Vonkkoorts, verbrande huid, de eerste zaad-verslaving bij vrouwen (trillen, honger).',
 [('GEB-orric-vonk',-150,'Orric, de eerste vonkdrager','Mijnwerker krijgt stormkracht na aanraking van Sterrensteen.','MAGIE-wat-gaven-man;GES-herkomst-gave','Orde: ja. Volk: nee.'),
  ('GEB-zaadkracht-ontdekt',-120,'De zaad-kracht ontdekt','Vrouwen rond Orric worden sterker na seks met hem.','MAGIE-zaadkracht;MAGIE-kracht-duur','Volk: denkt dat het altijd zo was.'),
  ('GEB-vonkkoorts',-60,'De Vonkkoorts','Vonkdragers die niet ontladen worden gek; steden branden.','KINK-ontlading-na-magie;LICH-vonkkoorts','Volk: als vloek.')]),
('FASE-brand','De Grote Brand',-40,0,'crisis','Overleven (oorlog en honger)',
 'Vonkkoningen vernietigen de wereld; driekwart van de vrouwen verliest haar huis.','De Zegel: mannen terugbrengen tot 1 op 100.','Het Offer der Dochters: honderd Zusters geven lichaam en leven.','De Zusters (later de Orde).','De Zusters zelf en alle ongeboren zonen.',
 'Officieel: Ysa nam de wrede mannen weg. Verborgen: vrouwen deden het zelf, met bloedmagie, en betaalden met hun lichaam.',
 'Voedsel: hongersnood. Bevolking: instorting. Macht: van koningen naar de Raad. Geloof: wanhoop. Magie: bloedzegel.',
 'Seks als oorlogsbuit (donker, niet uitgewerkt); in Zusterhuizen vrouwen onder elkaar als schuilplaats.',
 'Verbrande steden, oorlogswonden, de Dochters verdorren tot ze sterven.',
 [('GEB-zeven-kronen',-40,'Oorlog der Zeven Kronen','Zeven Vonkkoningen vechten om de Sterrensteen.','GES-officiele-versie','Volk: ja.'),
  ('GEB-lisk-brandt',-22,'Lisk brandt','Vonkkoning Varnath laat Lisk verbranden.','REG-saelith;PER-morvane','Volk: ja.'),
  ('GEB-dochteroffer',-1,'Het Offer der Dochters','Hoge Zuster Anath en honderd Zusters binden hun leven aan de Sterrensteen.','GEH-zegel;LICH-dochters','Alleen de Moeders.')]),
('FASE-noodtoestand','De Noodtoestand',0,130,'noodoplossing','Bevolking en geslachtsverhouding (bijna geen jongens)',
 'Hoe overleeft een volk met 1 man op 100?','De Deelwet, registers en het Jongenshof.','Mannen worden gedeeld en bewaakt; verwantschap wordt het grootste gevaar.','De Zusters, die registers beheren.','De laatste mannen (uitgeput) en vrouwen zonder kind.',
 'Officieel: de godin gaf ons de Deelwet. Verborgen: de Zusters schreven die wet en hielden de enige registers.',
 'Voedsel: herstel. Bevolking: 1 op 100, langzame groei. Macht: Zusters. Geloof: rouw wordt dank. Magie: zegel werkt; de gave wordt erfelijk.',
 'Losbandigheid uit noodzaak; mannen gedeeld; eerste Oogstbed en Melkrite; vrouwenliefde wordt de basis van het gezin.',
 'Zegel-mutaties bij geboorte; uitgeputte mannen; eerste gevallen van zegelgeboorten.',
 [('GEB-zegel-gelegd',0,'De Zegel wordt gelegd','Mannelijke vruchten vergaan; hun kracht stroomt naar de overlevenden.','GEH-zegel;REGEL-verhouding;LICH-zegelgeboorte','Niemand: dat de gave uit de dode zonen komt.'),
  ('GEB-deelwet-40',40,'De Deelwet','Elke man moet vele vrouwen bevruchten.','REGEL-seksuele-normen;RIT-oogstbed;RIT-melkrite','Volk: goddelijk bevel.'),
  ('GEB-orde-90',90,'De Orde van de Ontvangst','De Zusters worden priesteressen in Saelith.','ORDE-orde;ECO-geld','Volk: ja.')]),
('FASE-ontvangst','De Heilige Ontvangst',130,340,'institutie en uitbreiding','Geloof en betekenis (zegellicht verschijnt)',
 'Hoe maak je een noodwet tot iets wat mensen willen?','Het geloof: verlangen is gebed; tempels, gunstbrieven, Uitverkorenen.','Tempelseks voedt in het geheim de zegel; vrijheid wordt ritueel.','De Orde.','Wie niet gelooft: de Stille Zusters, die vertrekken.',
 'Officieel: zegellicht is Ysa die kijkt. Verborgen: het is de zegel die eet.',
 'Voedsel: stabiel. Bevolking: groeit. Macht: Orde. Geloof: hoogtepunt. Magie: Uitverkorenen erkend.',
 'Tempelnachten, Ontvangst, Gunstnacht, Wijding; vrouwenliefde heilig; eerste extreme proeven.',
 'Eerste tekenen bij gaven-mannen: aderen die gloeien, huid die verhardt; vrouwen met zaadlittekens.',
 [('GEB-eerste-zegellicht',130,'Het eerste zegellicht','Bij een Ontvangst in de tempel gloeien de stenen.','RIT-ontvangst;SFEER-zegellicht;RIT-zegelvoeding','Volk: wonder. Orde: zegelvoeding.'),
  ('GEB-uitverkorenen-210',210,'De Uitverkorenen erkend','De gave wordt officieel goddelijk.','MACHT-gaven-mannen;RIT-gunstnacht','Volk: “eerste gaven-mannen” (vals).'),
  ('GEB-stille-schisma',290,'Het Schisma der Stilte','Zusters die mannen afwijzen vertrekken naar het zuidwesten.','REG-stille','Volk: ja.')]),
('FASE-markt','De Markt van het Lichaam',340,720,'uitbreiding en verstarring','Macht en instituties (de huizen; na de Pest wordt het lichaam koopwaar)',
 'De Pest doodt een derde van de mannen; hoe houd je het systeem draaiend?','Rotatie, melkstallen, de Zaadbeurs, fokkerij in tempels.','Mannen worden vee; lichamen worden gefokt en aangepast; extreme riten worden normaal.','Huizen Varenne, Kaldra, Mirre en Qesh.','Gewone mannen, gebonden vrouwen, tempelgefokte lichamen.',
 'Officieel: de Pest was een straf; de rotatie een zegen. Verborgen: de Pest ontstond in de tempelfokkerij (open vraag), en Ves-Anath werd verlaten omdat de zegelsteen lichamen vervormde.',
 'Voedsel: Ambergaard voedt het rijk. Bevolking: dip, dan groei. Macht: huizen naast de Orde. Geloof: verstarring, ritueel zonder betekenis. Magie: fokken op gave.',
 'Veilingen, harems, Zevenvoudige Ontvangst, Ketenwake, Duel; handel in lichamen; diversiteit van voorkeuren per regio.',
 'Pestbuilen; gefokte mannen met overgrote klieren; Leegte-ziekte bij vrouwen; eerste vervorming bij oude gaven-mannen.',
 [('GEB-pest-340',340,'De Grote Pest','Koorts doodt een derde van de mannen.','LICH-pest;MACHT-gewone-mannen','Volk: straf van Ysa.'),
  ('GEB-zaadbeurs-455',455,'De Zaadbeurs','Huis Varenne organiseert de handel in mannen.','HUI-varenne;RIT-veiling','Volk: ja.'),
  ('GEB-qesh-512',512,'Het Zonvorstendom','Khaled-Ar weigert de Orde en sticht Qesh.','HUI-qesh;PER-khaled;RIT-vuurgloed','Volk: ja.'),
  ('GEB-ves-anath-ontruimd',603,'Ves-Anath ontruimd','De Orde verlaat Ves-Anath en verzwijgt waarom.','GEH-zegel;LICH-ves-anath-gruwel','Moeders weten het.')]),
('FASE-barsten','De Barsten',720,801,'barsten en nieuwe crisis','Bevolking en magie (de zegel lekt)',
 'De zegel verzwakt, Kharvos valt aan, duistere gaven-mannen bouwen eigen rijken.','De Orde plant de Zegelbinding; huizen zoeken eigen gaven-mannen.','Steeds extremere riten; lichamen breken.','Morvane-ir, Khaled-Ir, Kharvos.','Gebonden vrouwen, gewone mannen, het volk.',
 'Officieel: de goden beproeven ons. Verborgen: de zegel sterft, en met hem de gave.',
 'Voedsel: druk door oorlog. Bevolking: meer jongens in Ambergaard en Groenmuil. Macht: versplintering. Geloof: twijfel en ketterij. Magie: wilde gaven, mutaties.',
 'Bloedverbinding, Strijdontvangsten, Zwijgende Rit als ventiel; vrije liefde als verzet.',
 'Meer zegelgeboorten, verbrande gaven-mannen, Leegte die dagen duurt.',
 [('GEB-kharvos-720',720,'Eerste grote Kharvos-inval','Kharvos rooft vrouwen en gaven-mannen.','REG-kharvos;RIT-kharvosrite','Volk: ja.'),
  ('GEB-bloednacht-788',788,'De Bloednacht van Lisk','Morvane-ir doodt een raad van priesteressen.','PER-morvane;RIT-bloedverbinding','Volk: ja.'),
  ('GEB-teo-801',801,'Teo’s Wijding','Teo blijkt een verborgen gave te hebben.','PER-liora;PER-gewone-mannen;QST-doel-reden-gevaar','Volk: nee.')]),
]
for code,naam,v,t,pat,kracht,prob,opl,prijs,prof,bet,ov,vijf,sex,lich,evs in F:
  add('Tijdperk',code,naam,f"{v} tot {t}. Fase: {pat}. Omslagkracht: {kracht}. Probleem: {prob} Oplossing: {opl} Prijs: {prijs} Profiteerde: {prof} Betaalde: {bet} {ov} Vijf krachten: {vijf} Seksuele cultuur en rituelen: {sex} Lichaam: {lich}",'Fase van een systeem (ronde 9): crisis, noodoplossing, institutie, uitbreiding, verstarring, barsten.','GES-tijdlijn;GEH-zegel',v,naam)
  for gc,j,o,w,refs,weet in evs:
    add('Geschiedenis',gc,o,f'Jaar {j}. {w}','Sleutelgebeurtenis in '+naam+'.',code+';'+refs,j,naam,None,weet)
L=[('LICH-zaadslijtage','Zaadslijtage','Vrouwen die jarenlang vaak gaven-zaad ontvangen krijgen gouden aderen onder de huid, gevoelige, altijd opgewonden zenuwen en vroege grijze haren. Mooi en gebroken tegelijk; een teken van rang.',3,'MAGIE-kracht-duur;MAGIE-verslaving;VOOR-overvloed'),
('LICH-leegteziekte','Leegteziekte','Na te vaak de Leegte: trillende handen, koude huid, een honger die nooit stopt; na jaren tandverlies en breekbare botten.',4,'MAGIE-kracht-duur;RIT-leegtewake'),
('LICH-gebonden-lichaam','Het gebonden lichaam','Gebonden vrouwen ruiken naar hun meester; hun lichaam reageert alleen nog op hem; zonder hem krimpen hun spieren.',5,'MAGIE-verslaving;PER-morvane;RIT-bloedverbinding'),
('LICH-gaven-vervorming','Vervorming van gaven-mannen','Hoe meer magie, hoe meer het element in het lijf groeit: stormmannen krijgen glazige ogen en litteken-bliksem, vuurmannen verkoolde vingertoppen, bloedmannen doorschijnende huid. Na 50 is een machtige gaven-man half monster.',4,'MAGIE-wat-gaven-man;PER-aeron;PER-khaled;PER-morvane'),
('LICH-vonkkoorts','Vonkkoorts','Een gaven-man die niet ontlaadt, verbrandt van binnen: koorts, blaren, waanzin, binnen dagen de dood.',4,'KINK-ontlading-na-magie;RIT-stormontlading'),
('LICH-zegelgeboorte','Zegelgeboorten','Soms overleeft een zoon de zegel half: geboren met gloeiende littekens, doofstom of met een te sterke gave. De Orde neemt hen mee; niemand ziet hen terug.',4,'GEH-zegel;RIT-geboortelied'),
('LICH-vergane-zonen','De vergane zonen','Vrouwen voelen de zegel: bij elke miskraam van een zoon gloeit hun buik kort rood. Het volk noemt het “Ysa’s kus”.',3,'GEH-zegel;CUL-zwangerschap-anticonceptie-onvruchtbaarheid'),
('LICH-dochters','Het lichaam van de Dochters','De honderd Dochters verdorden levend in de Sterrensteen; hun gezichten zijn nog te zien in de zegelsteen van Ves-Anath.',5,'GEH-zegel;GEB-dochteroffer'),
('LICH-tempelfokkerij','Tempelfokkerij','In verborgen tempelstallen worden gewone mannen gefokt op groot zaadvolume: overgrote klieren, trage geesten, een lichaam dat alleen nog produceert. Ze worden vereerd en beklaagd tegelijk.',5,'MACHT-gewone-mannen;RIT-melkrite;HUI-varenne'),
('LICH-ontvangstersbouw','Ontvangsterslichamen','Ontvangsters worden van jongs af opgeleid (seksueel pas vanaf 18) en na hun Wijding met zalven aangepast: verruimde gevoeligheid, ongevoelig voor de Leegte, maar onvruchtbaar.',3,'ORDE-orde;RIT-ontvangst;REGEL-harde-grenzen'),
('LICH-pest','De Pest van 340','Builen in de lies, koorts, dood van mannen binnen drie dagen; vrouwen dragen het maar sterven zelden. Overlevers zijn onvruchtbaar.',4,'GEB-pest-340;MACHT-gewone-mannen'),
('LICH-krijgsvrouw','Lichaam van de krijgsvrouw','Na honderden Strijdontvangsten: harde spieren, gloeiende littekens, geen menstruatie, slapeloosheid; ze vrijen ruw om te voelen.',3,'RIT-strijdontvangst;HUI-kaldra'),
('LICH-ves-anath-gruwel','De gruwel van Ves-Anath','Rond de zegelsteen groeien lichamen samen: Zusters die te lang bleven werden vergroeid met steen en elkaar. Daarom werd de stad verlaten.',5,'GEH-zegel;GEB-ves-anath-ontruimd;QST-etappes-queeste'),
('LICH-melkman','Lichaam van de melkman','Gewone mannen die vier keer per dag gemolken worden: dik, zacht, met pijnlijke klieren en een uitgeblust verlangen dat alleen nog door aanraking terugkomt.',3,'RIT-melkrite;PER-gewone-mannen'),
('LICH-bloedgave-prijs','De prijs van de bloedgave','Morvane-ir verbruikt het bloed van zijn vrouwen; hij moet steeds nieuwe binden om zijn eigen lijf heel te houden.',5,'PER-morvane;RIT-bloedverbinding'),
('LICH-liora','Liora’s afwijking','Liora verdraagt zaad-kracht zonder Leegte omdat de zegel in haar bloed zwak is; haar lichaam is een bewijs dat de zegel sterft en maakt haar begeerd door de Orde.',3,'PER-liora;GEH-zegel'),
('LICH-macht-en-lichaam','Lichaam en macht','Wie het meest macht heeft, betaalt het meest met het lichaam: Moeders worden blind van zegelkennis, gaven-mannen vervormen, gebonden vrouwen verliezen hun eigen honger. Lichamelijke tekens worden rangtekens en fetisj tegelijk.',3,'ORDE-orde;MACHT-gaven-mannen;VOOR-overgave'),
('LICH-mutatie-ritueel','Riten om het lichaam','Nieuwe riten ontstaan rond vervorming: het bedekken van gaven-littekens met goud, het verzorgen van vervormde mannen in tempels, de verering van zaadslijtage.',3,'MODE-gaven-mannen;SFEER-tempels-verleidingspaleizen')]
for code,o,b,i,refs in L:
  add('Lichaam en vervorming',code,o,b+' Seksuele elementen alleen tussen volwassenen.','Body horror: het lichaam als prijs voor macht (ronde 9).',refs,None,None,i)
M={'GEB-uitverkorenen':'GEB-uitverkorenen-210','GEB-deelwet':'GEB-deelwet-40','GEB-melkstallen':'GEB-pest-340','GEB-ketenwake-ontstaat':'GEB-pest-340','GEB-zaadbeurs':'GEB-zaadbeurs-455','GEB-zonvorstendom':'GEB-qesh-512','GEB-kaldra-eed':'FASE-markt','GEB-eerste-ontvangst':'GEB-eerste-zegellicht','GEB-zaad-ontdekking':'GEB-zaadkracht-ontdekt','GEB-vonkpest':'GEB-vonkkoorts','GEB-bloednacht-lisk':'GEB-bloednacht-788','GEB-zusters-heelsters':'GEB-zusterburcht','GEB-zustersburcht':'GEB-zusterburcht','GEB-schisma-stilte':'GEB-stille-schisma','GEB-orde-sticht':'GEB-orde-90','GEB-vonkkoningen':'FASE-vonk','GEB-grote-pest':'GEB-pest-340','GEB-rotatiewet':'FASE-markt','GEB-mirre-vrijhaven':'FASE-markt','GEB-kharvos-inval':'GEB-kharvos-720','GEB-eerste-vonk':'GEB-orric-vonk'}
for code,v in c.execute("select code,verwijst_naar from canon where status!='vervallen'").fetchall():
  if v:
    n=';'.join(dict.fromkeys(M.get(x,x) for x in v.split(';')))
    if n!=v: c.execute('update canon set verwijst_naar=? where code=?',(n,code))
for code,o in c.execute("select code,onderwerp from canon where categorie='Voorkeuren'").fetchall():
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()[0]
  for a,b in M.items(): f=f.replace('Oorsprong: '+a+'.','Oorsprong: '+b+'.')
  c.execute('update canon set feit=? where code=?',(f,code))
# Kharvos-oplossing
c.execute("update canon set feit=feit||' Ronde 9: de verhouding in Kharvos is 1 op 3 jongens doordat Kharvos in de “zegelschaduw” ligt: de rand van de zegel dempt zonen gedeeltelijk.' where code='REG-kharvos'")
W=[('Kharvos 1 op 3 versus 1 op 2','REG-kharvos; GEH-zegel','Opgelost met de zegelschaduw: de rand van de zegel dempt zonen gedeeltelijk. Gevolg: Kharvos heeft belang bij het breken van de zegel.','mogelijke fout','voorstel','REG-kharvos;GEH-zegel'),
('Gave vóór de Zegel','FASE-vonk; GEH-wie-weet-wat','GEH-wie-weet-wat zegt dat de zegel de gave veroorzaakt; nu is de Vonk ouder. Oplossing: de Vonk was zeldzaam en wild; de zegel maakte haar erfelijk en sterker. Breekt de zegel, dan keert de gave terug naar wild en zeldzaam.','mogelijke fout','voorstel','GEH-wie-weet-wat;FASE-vonk'),
('Ontvangsters opgeleid van jongs af','LICH-ontvangstersbouw; REGEL-harde-grenzen','Opleiding vóór 18 is alleen kennis en zorg; elke lichaamsaanpassing of seksuele rol pas na de Wijding.','mogelijke fout','opgelost','LICH-ontvangstersbouw;REGEL-harde-grenzen'),
('Vervorming en begeerte','LICH-gaven-vervorming; MACHT-gaven-mannen','Als machtige gaven-mannen vervormen, waarom blijven ze begeerd? Bron van verhalen: vervorming wordt fetisj en rangteken; Aeron-as verbergt zijn tekens.','bron van verhalen','open','LICH-gaven-vervorming;PER-aeron'),
('Zegelgeboorten verdwijnen','LICH-zegelgeboorte; ORDE-orde','Wat doet de Orde met half-overleefde zonen? Groot geheim en verhaalbron.','bron van verhalen','open','LICH-zegelgeboorte;ORDE-orde'),
('Pest uit de tempelfokkerij?','LICH-pest; LICH-tempelfokkerij','Als de Pest uit de fokstallen kwam, is de Orde schuldig aan haar eigen ramp.','bron van verhalen','open','LICH-pest;LICH-tempelfokkerij')]
n=c.execute('select max(id) from wrijving').fetchone()[0]
for t,d,b,ty,s,v in W:
  n+=1;c.execute('insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)',(t,d,b,ty,s,f'WRIJ-{n:03d}',v))
c.execute("update open_vraag set status='vervallen',antwoord='Vervangen in ronde 9 door 7 fasen.' where code='VRAAG-021'")
Q=[('Keur je de 7 fasen goed (Overvloed, Vonk, Brand, Noodtoestand, Ontvangst, Markt, Barsten)?','Basis voor de volgende ronde.','FASE-overvloed'),
('Op welke leeftijd vertrekken jongens naar het Jongenshof: 6 (nu) of 16?','Coming-of-age; de niet-seksuele riten rond 16 blijven.','CUL-wat-jongens-meemaken;RIT-hofproef'),
('Hoe ver mag de body horror gaan (vervorming, vergroeiing, tempelfokkerij)?','Bepaalt de toon.','LICH-ves-anath-gruwel'),
('Wat doet de Orde met de zegelgeboorten?','Mogelijk groot geheim.','LICH-zegelgeboorte')]
m=c.execute('select max(id) from open_vraag').fetchone()[0]
for v,w,r in Q:
  m+=1;c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,f'VRAAG-{m:03d}',r))
c.execute("update open_vraag set status='vervallen' where code='VRAAG-023'")
c.execute("insert into logboek(datum,wat) values('2026-10-30','Ronde 9: 9 tijdperken vervallen; 7 fasen als systeem, 22 gebeurtenissen, 18 onderdelen Lichaam en vervorming, Kharvos-zegelschaduw.')")
c.commit()
