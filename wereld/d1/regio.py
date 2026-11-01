# regio -> lijst (soort, naam, tekst, functie, techniek); dieren nooit in seksuele rol
R={}
R['saelith']=[
('plant','Tempellelie','Witte waterlelie op de zeven eilanden; geur gebruikt bij elke Ontvangst. Medicijn: kalmeert. Prijs: plukken is voorbehouden aan novicen. Haak (intrige): leliepollen bewijst wie in de tempel was.','INTR','geen'),
('plant','Zaadriet','Riet waarvan het merg naar zaad ruikt; gebruikt voor zaadas-brood. Haak (thriller): het riet rot waar de zegellijn zwakker wordt.','THRL','gave'),
('plant','Inktmos','Mos dat Zegelinkt bindt; registers worden ermee geschreven. Haak (intrige): mos uit een andere vijver vervalst een register.','INTR','zegelsteen'),
('dier','Registerkraai','Kraai die de Orde traint om berichten te dragen; leeft van tempelafval. Haak (thriller): een kraai brengt een register naar de verkeerde.','THRL','geen'),
('dier','Rivierpaling','Vette paling, hoofdvoedsel van Orvane. Gevaar: palingkoorts bij rauw eten. Haak (intrige): een Moeder sterft aan "palingkoorts".','INTR','geen'),
('dier','Witte reiger','Heilig dier van Ysa; doden is een misdaad. Haak (humor): een rebel steelt alle reigers voor het Lampfeest.','HUM','geen'),
('eten','Saelith-keuken','Witte vis, lelierijst, zaadasbrood, honing van Kluwers; alles wit en zoet. Een gewone vrouw eet rogge en paling. Haak (intrige): wat de Orde eet, laat zien wie rijk is.','INTR','gave'),
('handel','Gunstbriefmarkt van Saelith','Officiële markt voor gunstbrieven; prijzen worden op de tempeltrap geroepen. Prijs: wachtlijsten van jaren. Haak (intrige): een veiling van één brief van Teo.','INTR','gave'),
('weer','Lenteoverstroming','Elke lente lopen de lage eilanden onder; registerkelders lopen gevaar. Haak (thriller): een overstroming als dekmantel voor een inbraak.','THRL','geen')]
R['ambergaard']=[
('plant','Amberkoren','Goudkleurig graan, basis van Velmara\'s brood. Haak (intrige): een misoogst dreigt.','INTR','geen'),
('plant','Stalklaver','Klaver voor het vee; stalmannen krijgen daarnaast klaverbrood dat de zaadproductie verhoogt. Prijs: de mannen worden zwaar en traag. Haak (rebellie): de stalopstand verbrandt de klaver.','INTR','bio'),
('plant','Oogstpapaver','Papaver voor pijnstilling en de Oogstnacht-roes (instemmende volwassenen). Haak (thriller): overdosis op een feest.','THRL','bio'),
('dier','Amberos','Trekdier en melkvee; de os is ook het scheldwoord voor gewone mannen. Haak (humor/pijn): een os heet beter dan een man.','INTR','geen'),
('dier','Zaadrover-hond','Waakhonden tegen zaadrovers. Haak (thriller): de honden worden vergiftigd.','THRL','geen'),
('dier','Stalbij','Bijen in de stallen tegen vliegen. Haak (intrige): Kluwers claimen ze.','INTR','bio'),
('eten','Oogstbrood','Zwaar roggebrood, kaas, worst, bier; boerinnencollectieven koken samen. Gewone vreugde: de eerste broden na de oogst. Haak (romance).','ROM','geen'),
('handel','Graanbeurs van Hallowyn','Graan bepaalt de Druppel; Varenne speculeert. Haak (intrige): een hongersnood gemaakt door de beurs.','INTR','geen'),
('weer','Droge zomer','Lange droogte, stof, bosbranden. Haak (thriller): brand op de oogstnacht.','THRL','geen')]
R['hoogvrouwe']=[
('plant','IJsbes','Rode bes onder sneeuw; vitamine voor de winter. Haak (romance).','ROM','geen'),
('plant','Steenvaren','Varen die op Sterrensteen-puin groeit en zwak gloeit; lampen voor arme gezinnen. Haak (thriller): de varens gloeien feller.','THRL','zegelsteen'),
('plant','Wolfswortel','Giftige wortel; ook een verdovingsmiddel van heelsters. Haak (intrige): een moord.','INTR','bio'),
('dier','Sneeuwwolf','Gevaarlijkste roofdier; krijgsvrouwen dragen de pels. Haak (thriller): een wolvenroedel achtervolgt een vluchteling.','THRL','geen'),
('dier','Bergyak','Draagdier en bron van melk en wol. Haak (gewone vreugde): de yakkenmarkt.','ROM','geen'),
('dier','Mijnkanarie','Waarschuwt voor gas en zegellek. Haak (thriller): de kanaries vallen stil.','THRL','zegelsteen'),
('eten','Kaldrun-keuken','Gezouten vlees, yakkenboter, gerstsoep; Strijdmaal voor de slag. Haak (intrige).','INTR','geen'),
('handel','Zilvermarkt van Kaldrun','Zilver en Sterrensteen; Kaldra belast. Haak (intrige).','INTR','zegelsteen'),
('weer','Witte Maand','Een maand van sneeuwstorm; alle oorlog stopt. Haak (romance): opgesloten met de vijand.','ROM','geen')]
R['zoutkust']=[
('plant','Zoutriet','Riet voor rum en daken. Haak (intrige).','INTR','geen'),
('plant','Grijswortel','Wortel die ontbindt; rebellen smokkelen hem. Haak (rebellie).','INTR','bio'),
('plant','Mistmos','Mos dat mist vasthoudt; schepen verbergen zich. Haak (thriller).','THRL','geen'),
('dier','Zeeslang','Groot zeemonster; navigators vrezen het. Haak (thriller).','THRL','geen'),
('dier','Brakkrab','Voedsel en lokaas. Haak (humor).','HUM','geen'),
('dier','Inktvis','Inkt voor stormrum en vervalste brieven. Haak (intrige).','INTR','bio'),
('eten','Brakhaven-keuken','Vissoep, gefrituurde krab, rum; havenkroegen. Haak (romance).','ROM','geen'),
('handel','Zwarte markt van Brakhaven','Mannen, zaad, splinters, grijswortel. Haak (thriller).','THRL','gave'),
('weer','Stormseizoen','Herfststormen; schepen liggen stil. Haak (intrige).','INTR','geen')]
R['groenmuil']=[
('plant','Maankruid','Anticonceptie; de Orde wil het verbieden. Haak (intrige).','INTR','bio'),
('plant','Vuurbloesem','Lustopwekker tussen instemmende volwassenen. Haak (erotiek, 18+).','LUST','bio'),
('plant','Wurgliaan','Liaan die wurgt; ook touw. Haak (thriller).','THRL','bio'),
('dier','Rivierslang','Gif voor medicijn en moord. Haak (thriller).','THRL','bio'),
('dier','Brulaap','Waarschuwt voor indringers. Haak (humor).','HUM','geen'),
('dier','Gloeikever','Licht in de jungle; levende lampen. Haak (romance).','ROM','bio'),
('eten','Tuaro-keuken','Fruit, gegrilde vis, schimmelkaas van de Myrrhen. Haak (intrige).','INTR','bio'),
('handel','Kruidenmarkt van Tuaro','Maankruid, vuurbloesem, gif. Haak (intrige).','INTR','bio'),
('weer','Regentijd','Drie maanden regen; rivieren overstromen. Haak (thriller).','THRL','geen')]
R['rosse']=[
('plant','Woestijngras','Basis van Ishvar-brood. Haak (intrige).','INTR','geen'),
('plant','Dadelpalm','Zoete vrucht; rijkdom. Haak (romance).','ROM','geen'),
('plant','Zandroos','Bloem die alleen in de nacht bloeit; parfum van de harem. Haak (erotiek, 18+).','LUST','geen'),
('dier','Kameel','Draagdier en melk. Haak (humor).','HUM','geen'),
('dier','Schorpioen','Gif; doodstraf. Haak (thriller).','THRL','bio'),
('dier','Woestijnvalk','Jachtvogel van Khaled-Ir. Haak (intrige).','INTR','geen'),
('eten','Qesh-keuken','Lamsvlees, dadels, yoghurt, specerijen. Haak (intrige).','INTR','geen'),
('handel','Karavaanmarkt','Glas, specerijen, paarden, zout. Haak (intrige).','INTR','geen'),
('weer','Zandstorm','Dagenlang; karavanen verdwijnen. Haak (thriller).','THRL','geen')]
R['kharvos']=[
('plant','Schaduwgerst','Gerst voor Kharvos-bier. Haak (intrige).','INTR','geen'),
('plant','Ijzerdoorn','Haag rond slavenmarkten. Haak (thriller).','THRL','geen'),
('plant','Slaapzaad','Verdovingsmiddel. Haak (thriller).','THRL','bio'),
('dier','Strijdhoornvee','Karrûk-vee. Haak (intrige).','INTR','geen'),
('dier','Jachthond van Kharvos','Getraind om vluchtelingen te vinden. Haak (thriller).','THRL','geen'),
('dier','Grauwe gier','Ruimt slagvelden op. Haak (horror).','THRL','geen'),
('eten','Kharvos-keuken','Bier, wild, brood; mannen eten eerst. Haak (intrige).','INTR','geen'),
('handel','Slavenmarkt van Kharvos','Vrouwen als handelswaar; donker thema, gelabeld. Haak (thriller).','THRL','geen'),
('weer','Schaduwvlakte','Altijd bewolkt; zegelschaduw. Haak (thriller).','THRL','zegelsteen')]
R['stille']=[
('plant','Zoutbloem','Bloem voor koelmagie en zaadbewaring. Haak (intrige).','INTR','gave'),
('plant','Stiltekruid','Kruid tegen verlangen naar mannen; Orde noemt het ketterij. Haak (romance).','ROM','bio'),
('plant','Zeekool','Hoofdvoedsel. Haak (gewone vreugde).','ROM','geen'),
('dier','Zeehond','Vriend en voedsel. Haak (romance).','ROM','geen'),
('dier','Stormvogel','Waarschuwt; heilig. Haak (thriller).','THRL','geen'),
('dier','Zoutgarnaal','Voedsel. Haak (humor).','HUM','geen'),
('eten','Kloosterkeuken','Vis, zeekool, zoutbrood. Haak (romance).','ROM','geen'),
('handel','Zaadkluismarkt','Gekocht bewaard zaad. Haak (intrige).','INTR','gave'),
('weer','Zoutmist','Mist die alles bedekt. Haak (thriller).','THRL','geen')]
