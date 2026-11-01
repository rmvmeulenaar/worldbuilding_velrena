import sqlite3, os  # let op: dit script maakt de basis (ronde 1) opnieuw aan en wist latere toevoegingen
if os.path.exists('canon.db'): os.remove('canon.db')
c = sqlite3.connect('canon.db')
c.executescript('''
CREATE TABLE canon(id INTEGER PRIMARY KEY, categorie TEXT, onderwerp TEXT, feit TEXT, status TEXT, reden TEXT, hangt_samen_met TEXT, ronde INTEGER);
CREATE TABLE wrijving(id INTEGER PRIMARY KEY, titel TEXT, delen_die_botsen TEXT, beschrijving TEXT, type TEXT, status TEXT);
CREATE TABLE open_vraag(id INTEGER PRIMARY KEY, vraag TEXT, waarom_belangrijk TEXT, status TEXT, antwoord TEXT);
CREATE TABLE logboek(id INTEGER PRIMARY KEY, datum TEXT, wat TEXT);
''')
K=[
('Demografie','Geslachtsverhouding','Bij de geboorte is ongeveer 1 op de 100 een jongen (voorlopig; voorstel 1 op 300 ligt open). Dit is een vast biologisch gegeven van de wereld.','vastgesteld','Schaarste van mannen is de basis van economie, geloof en macht.','Religie; Economie; Inteelt',1),
('Demografie','Nageslacht per man','Een man heeft gemiddeld 300 tot 500 kinderen.','vastgesteld','Het volk moet in stand blijven en de economie moet blijven draaien.','Inteelt; Afstamming',1),
('Maatschappij','Regeringsvorm','Een theocratie. Het geloof is door de machthebbers opgelegd en dient om hun positie als heilig te laten voelen.','vastgesteld','Religie is gereedschap, geen bron van macht.','Religie; Macht',1),
('Maatschappij','Seksuele normen','Losbandigheid wordt beloond; verlangen en overgave gelden als gebed. Alle deelnemers zijn volwassen.','vastgesteld','Het volk moet zich voortplanten; genot is heilig verklaard.','Religie',1),
('Macht','Twee soorten mannen','Gaven-mannen hebben magische kracht en macht en kunnen kiezen. Gewone mannen hebben geen gave en worden als bezit gehouden voor hun zaad.','vastgesteld','Macht komt uit wat je kunt afdwingen of onmisbaar maakt.','Religie; Magie',1),
('Macht','Gaven-mannen','Ze zijn de kern van het geloof. Hun zaad is het kostbaarste. Sommigen zijn vriendelijk, anderen duister. Zij kiezen; hun gunst is de grootste munt.','vastgesteld','Hun zaad is erfelijk waardevol (gezondheid, kracht, mogelijk gave).','Religie; Orde',1),
('Macht','Gewone mannen','Als productiemiddel gehouden door huizen, tempels en steden; verhandeld, bewaakt, gefokt.','vastgesteld','Zonder gave geen dwangmiddel.','Economie',1),
('Religie','Doel van het geloof','Het geloof is gericht op de gaven-mannen en hun zaad: verlangen en overgave aan hen zijn heilig. De orde beheert wie toegang krijgt.','vastgesteld','De elite wil het zaad van gaven-mannen.','Macht; Orde',1),
('Religie','De orde','Priesteressen bemiddelen tussen vrouwen en gaven-mannen, houden afstammingsregisters bij en beheren toegang.','voorlopig','Toegang is hun macht.','Inteelt; Afstamming',1),
('Afstamming','Registers en merken','Elk kind wordt bij de geboorte geregistreerd. Kinderen dragen een bloedlijnmerk van hun vader. Mannen reizen volgens rotatie langs steden.','voorlopig','Voorkomt inteelt bij honderden halfbroers en halfzussen.','Orde; Inteelt',1),
('Afstamming','Verwantschapstaboe','Seks tussen verwanten is het ergste taboe, de enige echte grens van het geloof. Het gebeurt soms toch, via verloren registers, afgelegen plekken of oplichting.','voorlopig','Tegenstelling met een geloof van losbandigheid.','Inteelt',1),
('Maatschappij','Overwegend vrouwelijke wereld','Vrouwen vormen het grootste deel van leger, handel, landbouw en bestuur. Afstamming loopt via de moeder.','voorlopig','Door de verhouding.','Demografie',1),
('Verhaal','Queeste','De queeste speelt in een ruwe, gevaarlijke wereld met een kwetsbare vrouw. Doel, reden en gevaar zijn nog niet bepaald.','voorlopig','Geeft de reis een klok en etappes langs plekken met eigen regels.','Wereld',1),
('Genre','Doelgroep en toon','Erotische fantasy voor volwassenen, met zowel spanning (erotisch) als directheid (geil). De wereld is ingericht op veel geladen situaties.','vastgesteld','Wens van de auteur.','Alles',1),
]
for i,k in enumerate(K,1): c.execute('INSERT INTO canon VALUES(?,?,?,?,?,?,?,?)',(i,)+k)
W=[
('Wie zegt nee?','Religie; Toestemming','Als overgave heilig is, wat gebeurt er met wie niet wil? Hoe verhoudt dat zich tot de gaven-mannen die wel mogen kiezen?','bron van verhalen','open'),
('Gewone man als bezit','Religie; Economie','De gewone man is uitgebuit terwijl het geloof zijn taak heilig noemt. Zijn enige hefboom is de weigering.','bron van verhalen','open'),
('Wie stuurt wie','Orde; Gaven-mannen','De gaven-man is het machtigst, maar de orde bepaalt wie hem ontmoet.','bron van verhalen','open'),
('Duistere gaven-man','Religie; Vrouwen','Een duistere gave-man kan een stad terroriseren terwijl weigeren verboden is.','bron van verhalen','open'),
('Populatiegroei','Demografie; Economie','Met 300-500 kinderen per man groeit het volk snel, tenzij iets de aantallen drukt (sterfte, oorlog, ziekte). Er is nog geen oorzaak vastgelegd.','mogelijke fout','open'),
('Verhouding en jongens','Demografie','Er is een oorzaak nodig waarom er zo weinig jongens worden geboren, en waarom dat zo blijft.','mogelijke fout','open'),
('Inteelt','Afstamming','Bij 300-500 kinderen per man is het risico groot. Registers en merken moeten overal werken.','mogelijke fout','open'),
('Bedreiging van buiten','Demografie; Leger','Een volk met weinig soldaten (alleen gaven-mannen als krijgers) is kwetsbaar voor buren met meer mannen.','bron van verhalen','open'),
]
for i,w in enumerate(W,1): c.execute('INSERT INTO wrijving VALUES(?,?,?,?,?,?)',(i,)+w)
V=[
('Is de verhouding 1 op 100, 1 op 300 of anders?','Bepaalt schaarste en hoe vaak personages mannen ontmoeten.','open'),
('Waar komt de gave vandaan (erfelijk, mutatie, goden, gemaakt)?','Bepaalt of vrouwen de gave kunnen stelen, kweken of vernietigen.','open'),
('Waarom worden er zo weinig jongens geboren?','Kan het diepste geheim en de motor van de queeste worden.','open'),
('Hoe diep gelooft het volk echt?','Bepaalt of het geloof oprecht, een machtsspel of allebei is.','open'),
('Wat gebeurt er met wie weigert?','Bepaalt de hardheid van het systeem.','open'),
('Hoe zeldzaam zijn gaven-mannen onder de mannen (voorstel 1 op 20)?','Bepaalt hoeveel machthebbers er zijn.','open'),
('Wat is het doel, de reden en het gevaar van de queeste?','Bepaalt de route door de wereld.','open'),
('Is de situatie van de mannen overal gelijk of per streek verschillend?','Bepaalt de variatie in steden langs de route.','open'),
('Land, klimaat en economie: hoe ziet de wereld eruit?','Volgende laag in de bouwvolgorde.','open'),
]
for i,v in enumerate(V,1): c.execute('INSERT INTO open_vraag VALUES(?,?,?,?,NULL)',(i,)+v)
c.execute("INSERT INTO logboek VALUES(1,'2026-10-29','Ronde 1: basis vastgelegd (demografie, macht, religie, afstamming).')")
c.commit()
# markdown export
with open('canon.md','w') as f:
    f.write('# Canon-bijbel (ronde 1)\n\n')
    cat=None
    for r in c.execute('SELECT categorie,onderwerp,feit,status,reden,hangt_samen_met FROM canon ORDER BY categorie,id'):
        if r[0]!=cat: cat=r[0]; f.write(f'\n## {cat}\n')
        f.write(f'- **{r[1]}** ({r[3]}): {r[2]} _Waarom:_ {r[4]} _Hangt samen met:_ {r[5]}\n')
    f.write('\n## Wrijvingenlijst\n')
    for r in c.execute('SELECT titel,delen_die_botsen,beschrijving,type,status FROM wrijving'):
        f.write(f'- **{r[0]}** [{r[3]}, {r[4]}] ({r[1]}): {r[2]}\n')
    f.write('\n## Open vragen\n')
    for r in c.execute('SELECT vraag,waarom_belangrijk FROM open_vraag'):
        f.write(f'- {r[0]} _({r[1]})_\n')
