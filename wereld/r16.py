# Ronde 16: diversiteit van seksualiteit binnen elk volk (idempotent)
import sqlite3;c=sqlite3.connect('canon.db');n=0
# volk,slug,naam,aandeel/positie,beschrijving,VOOR,officieel,feitelijk,spanning,kosten
V=[
# Aelthir
('aelthir','eeuwparen','Eeuwparen (mainstream)','±55%, de Raad','Monogaam per eeuw, hetero en homo gelijk geaccepteerd; trage, ritualistische seks.','VOOR-teder:2;VOOR-ritueel:3','de norm','vaak na twee eeuwen alleen nog ritueel','verachten de Snellen','geen'),
('aelthir','koelen','De Koelen (aseksueel/gering verlangen)','±20%, gerespecteerd','Wie het verlangen opgebruikt heeft of nooit had; intimiteit door aanwezigheid.','VOOR-geest:1','geëerd als wijs','soms eenzaam; worden door de Orde gezocht als onkreukbare boden','Snellen noemen hen dood','geen, behalve onvruchtbaarheid'),
('aelthir','snellen','De Snellen (afwijkers)','±10%, jongere volwassenen','Zoeken mensen voor felheid; poly, pan, snel; ruilen geheugen voor gevoel.','VOOR-reiziger:4;VOOR-groep:3;VOOR-overvloed:3','afgekeurd: verspilling van verlangen','groeiende groep sinds het lek','met de Raad','verbanning uit het geheugenarchief'),
('aelthir','rekenaars','Rekenaarsters (ritueel-specialisten)','±5%, priesterlijk','Leiden de Nacht van de Rekening; dominant, kalm, beheersen andermans verlangen; meestal vrouwen, ook met vrouwen.','VOOR-dominante-vrouw:3;VOOR-ontzegging:4;VOOR-vrouwenliefde:3','heilig','machtig: ze bepalen wie in de vruchtbare koorts mag kiezen','met de Snellen','—'),
('aelthir','glazen','De Glazen (verboden minderheid)','±3%','Opgewonden door het doorschijnend worden van de huid: kijken naar organen en hartslag tijdens seks; uitgesproken kink.','VOOR-voyeurisme:4;VOOR-lichaam:4','verboden (onterend)','geheime salons op de eilanden','met Eeuwparen','uitstoting'),
# Karrûk
('karruk','kampvechters','Kampvechters (mainstream)','±60%','Hetero en bi; vrouwen kiezen na wedstrijd, seizoenspartners.','VOOR-competitie:4;VOOR-dominante-vrouw:3;VOOR-ontlading:4','de norm','—','met Eedbrekers','—'),
('karruk','bloedeed','Bloedeedparen (monogaam)','±15%','Twee krijgers, vaak man-man of vrouw-vrouw, met een bloedeed voor het leven; delen niemand.','VOOR-binding:3;VOOR-teder:2','geëerd in liederen','verdacht in vredestijd (ze doen niet mee aan het Vuurkamp)','met de kampnorm','minder status bij kampioensverkiezing'),
('karruk','verliezers','De Gewillige Verliezers (onderdanige mannen)','±10%','Mannen die opzettelijk verliezen om gekozen te worden en zich over te geven.','VOOR-onderdanige-man:4;VOOR-overgave:4;VOOR-vernedering:2','officieel bestaat het niet (verlies is schande)','iedereen weet het; populair bij leidsters','met eerzuchtige krijgers','spot'),
('karruk','vuurmoeders','Vuurmoeders (ritueel-specialisten)','±5%','Oudere vrouwen die kookkoppen en vonkdragers ontladen en kalmeren; pan, praktisch, intens.','VOOR-ontlading:5;VOOR-oudere-vrouw:3;VOOR-pijn-genot:3','heilig en nodig','raken zelf verbrand','met wie hen als werkvrouwen ziet','littekens, kort leven'),
('karruk','stillen','De Stille Kampen (aseksueel/afzijdig)','±5%','Krijgers die geen seks willen; ontladen alleen door gevecht.','VOOR-uithouding:2','verdacht: ze worden kookkop','sommigen kunnen het echt','met vuurmoeders','risico op kookhuid; men wantrouwt ze'),
# Dhurn
('dhurn','seizoenparen','Seizoenparen (mainstream)','±65%','Hetero, door gilde toegewezen per mijnseizoen; zuinig, warm, in baden.','VOOR-uithouding:3;VOOR-binding:2','de norm','vaak huwelijken van plicht','met Lijnzoekers','—'),
('dhurn','lijnzoekers','Lijnzoekers (verboden minderheid)','±3%','Aangetrokken tot het verbodene van eigen lijn; leven het uit in fantasie en rollenspel met niet-verwanten.','VOOR-verboden:4','zwaarst verboden','rollenspel wordt gedoogd zolang geen verwanten','met de Gildenraad','merkbranding als het verwanten blijkt'),
('dhurn','mijnbroeders','Mijnbroeders (mannen onder elkaar)','±15%','Mannen die in de diepe schachten samen werken en samen liggen; tolerantie omdat het geen kinderen geeft (dus geen inteelt).','VOOR-uithouding:3;VOOR-teder:2','gedoogd, praktisch','sterke loyaliteit','met vrouwen die mannen tekort komen','geen erfrecht'),
('dhurn','vreemdelingsgangers','Vreemdelingsgangers (ritueel-specialisten)','±7%','Vrouwen en mannen die gezanten ontvangen; pan, nieuwsgierig, hoge status.','VOOR-reiziger:4;VOOR-ritueel:3','eervol','begeerde positie, omkoping','met Seizoenparen','—'),
('dhurn','steenlust','Steenlust (lichaamsvariant)','±5%','Opgewonden door de ruwe steenhuid en pijn bij aanraking; dragen handschoenen niet.','VOOR-pijn-genot:4;VOOR-lichaam:3','afgekeurd (risico op brandwonden)','gedoogd in baden','met genezers','wonden'),
# Sael-mor
('saelmor','scheepsvrouwen','Scheepsvrouwen (mainstream)','±50%','Vrouwen onder elkaar aan boord, bi met havenmannen; poly.','VOOR-vrouwenliefde:3;VOOR-groep:3','de norm','—','met Landblijvers','—'),
('saelmor','havenmannen','Gedeelde mannen (1 op 20)','±5%','Mannen gedeeld tussen schepen; sommigen willen dit, anderen niet.','VOOR-overvloed:3;VOOR-reiziger:3','geëerd als schat','soms bezit, soms vrij','met kapiteinen','weinig zeggenschap'),
('saelmor','landblijvers','Landblijvers (monogaam)','±10%','Wie aan land blijft met één partner, ondanks rottende kieuwen.','VOOR-teder:3','verraad aan het schip','romantiek in liederen','met de vloot','huid rot, uitsluiting van het schip'),
('saelmor','diepduikers','Diepduiksters (lichaamsvariant)','±10%','Seks onder water met adem inhouden tot het randje; ademspel.','VOOR-pijn-genot:3;VOOR-overgave:3;VOOR-geest:3','gedoogd','dodelijke ongelukken','met ouderen','risico van verdrinking'),
('saelmor','zoutkussers','Zoutkussers (ritueel-specialisten)','±5%','Leiden het Zoutkus-ritueel en de Springtij-nacht; dominant, theatraal.','VOOR-exhibitionisme:4;VOOR-ritueel:4;VOOR-dominante-vrouw:3','heilig','machtig in de kapiteinsraad','met havenmannen','—'),
# Grauwen
('grauwen','zorgparen','Zorgparen (mainstream)','±50%','Monogaam of klein poly; teder, zorgvuldig, vaak vrouw-vrouw.','VOOR-teder:2;VOOR-vrouwenliefde:2','de norm','—','met Zoekers','—'),
('grauwen','geringen','De Geringen (aseksueel door pijn of keuze)','±25%','Seks is te pijnlijk of niet gewenst; intimiteit door aanraking en verzorging.','VOOR-teder:1','volledig aanvaard','groot deel van het volk','geen','geen'),
('grauwen','zoekers','Zoekers (buitenbeentjes)','±10%','Zoeken buitenstaanders voor vers bloed en avontuur; bi, pan.','VOOR-reiziger:3;VOOR-verboden:2','toegestaan maar gevaarlijk','worden soms misbruikt door mensen met angstlust','met zorgparen','risico van verraad buiten'),
('grauwen','ontsluierden','De Ontsluierden (exhibitionistisch)','±5%','Tonen het vervormde lichaam bewust; kracht in gezien worden.','VOOR-exhibitionisme:3;VOOR-lichaam:4','omstreden','sterk onder jongere volwassenen','met wie doeken draagt','spot van buiten'),
('grauwen','lijnhoeders','Lijnhoedsters (ritueel-specialisten)','±5%','Houden de lijsten bij en wijzen paren aan; streng, soms dominant.','VOOR-dominante-vrouw:2;VOOR-ritueel:3','gezaghebbend','macht door kennis','met zoekers','—'),
# Ishvar
('ishvar','tweegelofte','Tweegeloftepaar (mainstream)','±70%','Monogaam, hetero en homo; eden fluisteren tijdens seks.','VOOR-teder:2;VOOR-binding:2','de norm','—','met de Drieën','—'),
('ishvar','drieen','De Drieën (polyamoreus)','±8%','Drievoudige geloften; officieel niet bestaand.','VOOR-groep:2;VOOR-binding:3','verboden','gedoogd in de diepe woestijn','met familie-eer','verlies van erfrecht'),
('ishvar','zonzwervers','Zonzwervers (afwijkers)','±7%','Ishvar die naar Velmara trekken voor het zaadsysteem en losbandigheid.','VOOR-overvloed:3;VOOR-verboden:3','verstoten','Khaled-Ir gebruikt hen als spionnen','met families','verbanning'),
('ishvar','eedmeesters','Eedmeesters (ritueel-specialisten)','±5%','Leiden de Tweegelofte; dominant in woord, bewaken de eden.','VOOR-dominante-man:2;VOOR-ritueel:4;VOOR-geest:3','gezag','—','met de Drieën','—'),
('ishvar','stilte','De Woordlozen (gering verlangen)','±10%','Trouw zonder seks; geloftes zonder lichaam.','VOOR-geest:1','geaccepteerd','—','—','minder kinderen'),
# Vathren
('vathren','zieners','Zieners (mainstream)','±40%','Seks als waarneming; delen gezellen binnen de raad; bi en pan.','VOOR-geest:4;VOOR-ritueel:3','de norm','—','met Afwenders','—'),
('vathren','gezellen','Gezellen (vrouwen die toetreden)','±30%','Vrouwen die de gloed verdragen; poly, soms dominant tegenover de dove mannen.','VOOR-overgave:3;VOOR-dominante-vrouw:3','geëerd','sommigen zoeken alleen kracht','met zieners','zegelkoorts'),
('vathren','afwenders','Afwenders (aseksueel, uit angst)','±15%','Mijden seks om hun zaad niet te laten schaden.','VOOR-ontzegging:3','gerespecteerd','vaak de beste navigators','met de raad','eenzaamheid'),
('vathren','brandzoekers','Brandzoekers (uitgesproken kink)','±10%','Zoeken de koorts en de gloed tot het randje.','VOOR-pijn-genot:5;VOOR-overgave:4','afgekeurd','Morvane-ir rekruteert hier','met zieners','zegelkoorts, dood'),
('vathren','hartparen','Hartparen (monogaam)','±5%','Twee Vathren (vaak man-man) wier hartslag samenvalt; delen niemand.','VOOR-teder:3;VOOR-binding:3','verdacht: onttrekken zich aan de raad','—','met de raad','buitensluiting uit de Ziener-raad'),
]
for v,s,nm,aand,beschr,voor,off,feit,span,kost in V:
  code=f'SEKS-VOLK-{v}-{s}'
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): continue
  vc=[x.split(':')[0] for x in voor.split(';')]
  f=f"{beschr} Aandeel/positie: {aand}. Voorkeuren: {voor.replace(';',', ')}. Officieel: {off}. Feitelijk: {feit}. Spanning: {span}. Kosten van afwijken: {kost}. Alleen volwassen, instemmende wezens (18+); geen dieren."
  refs=';'.join([f'SEKS-VOLK-{v}']+vc)
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar) values('Volken seksualiteit',?,?,'voorlopig','Ronde 16: diversiteit binnen het volk',?,16,?,?)",(nm,f,refs,code,refs));n+=1
if not c.execute("select 1 from logboek where wat like 'Ronde 16:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30','Ronde 16: 35 varianten (5 per volk) van seksualiteit binnen de volken: mainstream, aseksueel, monogaam, poly, dominant/onderdanig, kinks, verboden minderheden en lichaamsvarianten.')")
if not c.execute("select 1 from open_vraag where code='VRAAG-042'").fetchone():
  c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values('Kloppen de percentages per volk, en wil Rogier per volk een variant als hoofdpersoon?','Diversiteit als verhaalbron.','open','VRAAG-042','SEKS-VOLK-karruk-verliezers;SEKS-VOLK-aelthir-glazen')")
if not c.execute("select 1 from wrijving where code='WRIJ-070'").fetchone():
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values('Mijnbroeders versus Dhurn-kindertekort','SEKS-VOLK-dhurn-mijnbroeders; VOLK-dhurn','Een volk met weinig kinderen gedoogt kinderloze paren: omdat ze geen inteelt geven. Geldt dit ook in Velmara zelf?','bron van verhalen','open','WRIJ-070','SEKS-VOLK-dhurn-mijnbroeders;VOLK-dhurn')")
c.commit();print('nieuw',n)
codes={r[0] for r in c.execute('select code from canon')}
print('ontbrekend',{x for (v,) in c.execute("select verwijst_naar from canon where ronde=16") for x in v.split(';') if x not in codes})
