# Ronde 11: functies van de lichaamslaag + afstoting/aantrekking (idempotent)
import sqlite3;c=sqlite3.connect('canon.db')
cols=[r[1] for r in c.execute('pragma table_info(canon)')]
for col,t in [('functie','text'),('afstoting','integer'),('aantrekking_bron','text'),('aantrekking','integer')]:
  if col not in cols: c.execute(f'alter table canon add column {col} {t}')
F={'MIL':'militair','POL':'politiek','REL':'religieus','ECO':'economisch','LUST':'seksueel/lust','HECHT':'hechting/loyaliteit','ID':'identiteit/status','CTRL':'controle/straf','INFO':'informatie/waarneming','VOORT':'voortplanting','OVERG':'rituele overgang','AFSCHR':'afschrikking'}
# code: (functies, voor wie, hoe vaak, wat misgaat als het wegvalt, afstoting 1-5, bron van aantrekking, aantrekking 0-5, toelichting)
L={
'LICH-zaadslijtage':('ID;ECO;INFO','Orde, rijke ontvangsters, drager zelf','dagelijks zichtbaar bij duizenden tempelvrouwen','geen zichtbaar bewijs van hoeveel iemand ontvangen heeft; status moet weer met papier','3','macht/status (gouden aderen = veel gaven-zaad)','2','De aderen zelf jeuken en zien eruit als wormen; aantrekkelijk is alleen wat ze betekenen.'),
'LICH-leegteziekte':('CTRL;AFSCHR;HECHT','Orde, gaven-mannen','duizenden gevallen per jaar','vrouwen zouden onbeperkt ontvangen; geen rem op gaven-mannen','4','geen (alleen voor een kleine groep met angstlust: VOOR-ontzegging)','0','Voor drager en omgeving puur ellende.'),
'LICH-gebonden-lichaam':('HECHT;MIL;CTRL','heersers, donkere gaven-heren, Kaldra','elk leger en elke harem van een gaven-man','legers en harems zouden vrij weglopen; loyaliteit moet weer gekocht worden','4','macht (voor de meester), fetisj (VOOR-binding, VOOR-overgave)','2','Geur en afhankelijkheid zijn walgelijk voor buitenstaanders; de meester geniet van de macht, niet van het lichaam.'),
'LICH-gaven-vervorming':('ID;AFSCHR;INFO','Orde, gaven-man zelf, huizen','elke sterke gaven-man na jaren','geen zichtbare rang; gaven-mannen zouden zich kunnen verbergen of vervalsen','4','macht/gave (de vervorming = sterkte), angstlust','2','Glazige ogen en stenen huid stoten af; de kracht erachter trekt aan.'),
'LICH-vonkkoorts':('AFSCHR;CTRL;LUST','Orde (rechtvaardiging van ontladingsplicht)','zeldzaam nu, steeds dreigend','de ontladingsplicht en de Deelwet verliezen hun noodargument','5','functie (ontlading als plicht en redding)','1','Blaren en waanzin zijn walgelijk; aantrekking zit alleen in het redden door ontlading.'),
'LICH-zegelgeboorte':('INFO;CTRL;REL','Orde (geheim)','enkelen per jaar, stijgend','de Orde verliest het vroegste signaal dat de Zegel lekt','5','geen','0','Alleen gruwel en verborgen verdriet.'),
'LICH-vergane-zonen':('REL;CTRL;VOORT','Orde, volk','bij elke miskraam van een zoon','het geloof verliest zijn tastbare bewijs dat Ysa kijkt','4','geen','0','Rouw, geen lust.'),
'LICH-dochters':('REL;POL;AFSCHR','Moeders van de Orde','permanent (de Zegel)','de Zegel valt; de gave verdwijnt; het systeem stort in','5','geen (alleen ontzag)','0','Het fundament van alles, en het afschuwelijkste ding in de wereld.'),
'LICH-tempelfokkerij':('ECO;VOORT;MIL','Orde, Varenne','honderden mannen tegelijk, geheim','geen goedkope zaadvoorraad voor tempels en legers','5','economie (volume), fetisj bij een kleine groep (VOOR-overvloed, VOOR-melken)','1','Overgrote klieren zijn walgelijk; aantrekking is handel.'),
'LICH-ontvangstersbouw':('REL;ID;LUST;OVERG','Orde, ontvangsters zelf','elke Wijding van een ontvangster','geen klasse die zegelvoeding kan verdragen; Ontvangst wordt gevaarlijk','3','functie/status, gewenning (wie ermee opgroeit vindt het mooi)','3','Vergroeiingen en littekens blijven verontrustend; de heilige rol en de status maken het begeerlijk.'),
'LICH-pest':('AFSCHR;POL;CTRL','Orde (als straf-verhaal)','eenmalig 340, herhaald 470','geen schrikbeeld om mannen in stallen te houden','5','geen','0','Alleen dood en angst.'),
'LICH-krijgsvrouw':('MIL;ID;AFSCHR','Kaldra, krijgsvrouwen zelf','elk leger, honderden ontvangsten','geen zichtbaar veteranendom; vijand wordt niet afgeschrikt','3','macht/kracht, fetisj (VOOR-dominante-vrouw, VOOR-competitie)','3','Littekens en een lege buik zijn hard om te zien; haar kracht trekt aan.'),
'LICH-ves-anath-gruwel':('AFSCHR;INFO;REL','Orde (verboden zone)','permanent rond de zegelsteen','niets houdt pelgrims en Kharvos weg van de steen','5','angstlust (zeldzaam)','0','Vergroeide lichamen; puur walging.'),
'LICH-melkman':('ECO;CTRL;ID','Orde, Ambergaard, Varenne','vier keer per dag, duizenden mannen','tempels krijgen geen dagelijkse voorraad; gewone mannen zouden zelf onderhandelen','4','economie, fetisj (VOOR-melken, VOOR-vernedering, VOOR-onderdanige-man)','1','Dik, zacht, pijnlijk; voor de man en zijn omgeving vernedering.'),
'LICH-bloedgave-prijs':('MIL;HECHT;CTRL','Morvane-ir en donkere heren','voortdurend, elke maand nieuwe vrouwen','de donkere heer verliest zijn kracht; zijn rijk valt','5','macht (bij hem), angstlust (VOOR-bloed, VOOR-pijn-genot)','1','Uitgeteerde vrouwen; walgelijk; zijn macht is het enige wat trekt.'),
'LICH-liora':('INFO;POL;VOORT','Liora zelf, de Orde, Stille Zusters','uniek','geen levend bewijs dat de Zegel sterft; de quest heeft geen sleutel','2','gave (zij verdraagt wat anderen breekt), gewenning','2','Haar gloed is vreemd en eng, ook voor haarzelf; aantrekking komt uit wat ze kan.'),
'LICH-macht-en-lichaam':('POL;ID;REL','heersers, Moeders','bij elke machtige','macht zou kosteloos lijken; het volk ziet geen offer en verliest ontzag','4','macht','1','Blinde Moeders en stenen heren; ontzag, geen lust.'),
'LICH-mutatie-ritueel':('OVERG;REL;ID','Orde, volk, dragers','bij elke Wijding en rouw','vervorming kan niet in betekenis worden omgezet; dragers worden verstoten','3','functie (ritueel maakt het draaglijk), gewenning','2','Het goud bedekt wat walgelijk blijft.'),
}
n=0
for code,(fu,wie,vaak,mis,af,bron,aan,toel) in L.items():
  names=', '.join(F[x] for x in fu.split(';'))
  blok=f" [Functie (r11): {names} (FUNC-{fu.replace(';',', FUNC-')}). Voor wie: {wie}. Hoe vaak: {vaak}. Als het wegvalt: {mis}. Afstoting: {af}/5 (nooit 0). Bron van aantrekking: {bron}; aantrekking {aan}/5. {toel}]"
  r=c.execute("select feit from canon where code=?",(code,)).fetchone()
  if r and '[Functie (r11)' not in r[0]:
    c.execute("update canon set feit=feit||?,functie=?,afstoting=?,aantrekking_bron=?,aantrekking=?,verwijst_naar=verwijst_naar||? where code=?",(blok,fu,int(af),bron,int(aan),';'+';'.join('FUNC-'+x for x in fu.split(';')),code));n+=1
def add(code,o,f,refs):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar) values('Lichaam en vervorming',?,?,'voorlopig','Ronde 11: functies van de lichaamslaag',?,11,?,?)",(o,f,refs,code,refs));n+=1
ENKEL={'AFSCHR':'De Orde en de heersers hebben geen leger groot genoeg om iedereen te bewaken; alleen zichtbare gruwel (Pest, Ves-Anath, Leegte) houdt mensen weg zonder soldaten.',
'HECHT':'Loyaliteit is in een wereld van gedeelde mannen niet te kopen of te erven; alleen lichamelijke binding maakt een leger of harem echt trouw.',
'INFO':'Registers zijn te vervalsen (vervalsersgilde); alleen het lichaam (zegelgeboorten, gouden aderen, Liora) liegt niet over wat de Zegel doet en wie wat ontvangen heeft.',
'ID':'Rang van gaven-mannen en ontvangsters kan met kleding of papier worden nagemaakt; vervorming is het enige onvervalsbare teken.',
'REL':'Een geloof dat op een verzwegen daad rust heeft tastbaar bewijs nodig; de vergane zonen en de Dochters zijn dat bewijs.'}
for k,nm in F.items():
  items=[code for code,v in L.items() if k in v[0].split(';')]
  f=f"Functiecategorie {nm}. Vervuld door: {', '.join(items) or '—'}."
  if k in ENKEL: f+=f" Niet elders te krijgen: {ENKEL[k]}"
  else: f+=" Ook elders te krijgen (via geld, wetten, rituelen of wapens); body horror is hier een versterker, geen noodzaak."
  add(f'FUNC-{k}',f'Functie: {nm}',f,';'.join(items))
add('FUNC-overzicht','Waarom heersers de body horror nodig hebben',"Body horror is altijd afstotelijk (afstoting 1-5, nooit 0). Aantrekking zit nooit in de vervorming zelf, maar in de functie, de macht, de fetisj van een groep, gewenning of angstlust (aantrekking 0-5; vaak 0). Vijf functies krijgen heersers nergens anders: afschrikking zonder leger, loyaliteit die niet te kopen is, waarheid die niet te vervalsen is, rang die niet na te maken is, en tastbaar bewijs voor een vals geloof. Daarom bestrijdt de Orde de vervorming niet maar beheert ze die.",';'.join('FUNC-'+k for k in ENKEL))
if not c.execute("select 1 from logboek where wat like 'Ronde 11:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30','Ronde 11: kolommen functie, afstoting, aantrekking_bron, aantrekking toegevoegd; 18 LICH-rijen aangevuld met functieblok (geen rijen verwijderd); 12 FUNC-categorieën en FUNC-overzicht. Correctie Rogier: geen geilheidsscore, maar afstoting 1-5 (nooit 0) plus bron van aantrekking en aantrekking 0-5.')")
c.commit();print('gewijzigd/nieuw',n)
