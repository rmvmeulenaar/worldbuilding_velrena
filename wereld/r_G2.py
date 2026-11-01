# Ronde G2: personages per fase (idempotent); data in r_G2_data.txt
from gaten_lib import Ronde,GR
R=Ronde(2);A=R.add
FN={'overvloed':'1 Overvloed','vonk':'2 Vonk','brand':'3 Brand','noodtoestand':'4 Noodtoestand','ontvangst':'5 Ontvangst','markt':'6 Markt','barsten':'7 Barsten','nu':'801 (nu)'}
BEST={'liora','aeron','morvane','khaled'}
for ln in open('r_G2_data.txt',encoding='utf-8'):
  f=ln.rstrip('\n').replace("\\'","'").split('|')
  if len(f)!=19: raise SystemExit('fout veldaantal: '+ln)
  slug,naam,volk,reg,huis,rol,fase,jaar,wil,durf,verb,weet,voor,kink,lich,rel,geb,geh,einde=f
  code='PER-'+slug+('-profiel' if slug in BEST else '')
  vc='' if volk=='mens' else 'VOLK-'+volk
  vs=[x.split(':') for x in voor.split(',') if ':' in x]
  vtxt=', '.join(f'{c} ({i}/5)' for c,i in vs) or 'geen seksuele rol'
  refs=[r for r in [vc,'REG-'+reg, huis if huis.startswith('HUI-') else '', geb, 'FASE-'+fase if fase!='nu' else 'GEB-heden']+[c for c,_ in vs]+(['PER-'+slug] if slug in BEST else []) if r]
  haken=(f"Romance: {rel}; belemmering: {verb}. Intrige: wil {wil}, maar verbergt {verb}. "
         f"Erotiek: {kink if kink!='-' else 'geen erotische rol'}. Thriller: geheim \"{geh}\" kan uitkomen; {('einde: '+einde) if einde!='open' else 'lot nog open (klok loopt in 801)'}.")
  feit=(f"Naam: {naam}. Volk: {volk}. Regio: {reg}. Huis: {huis}. Rol: {rol}. Fase: {FN[fase]}, jaar {jaar}. "
        f"Wil: {wil}. Durft: {durf}. Verbergt: {verb}. Wat de omgeving weet: {weet}. Seksuele voorkeur: {vtxt}; kinks: {kink}. "
        f"Lichaam/vervorming: {lich}. Relaties: {rel}. Rol in de keten: {geb}. Geheim: {geh}. Einde: {einde}. "
        f"Verhaalhaken: {haken} Herkenbaar gevoel: {'verlangen en schaamte' if 'verb' else ''} rond wat ze verbergt.")
  A(code,'Personage',naam,feit+GR,f'personage fase {FN[fase]}',';'.join(dict.fromkeys(refs)),jaar=int(jaar),tijdperk=FN[fase],
    intensiteit=max([int(i) for _,i in vs] or [0]))
# verhaalhaken-overzicht per spoor
H=[('HAAK-PER-romance','Romantische lijnen (overzicht)','Liora tussen Aeron-as (veilige tederheid, maar zijn zaad bindt) en Sef (vrijheid, maar zij spioneert voor Ondessa); Bram en Dagny (eigenares en bezit: liefde over een machtskloof); Tharn Lunn en Bor (laatste vruchtbare man, Kaldra wil hem fokken); Tavik en een mens (gilde verbiedt); Ruy en Liora (hij hoort haar register in de Wortel). Historisch: Ysara en Mira (de nacht voor het Offer, de één vlucht), Tamsin en Gorrum. Belemmeringen zijn steeds het systeem: register, bezit, binding, verwantschap.','PER-liora-profiel;PER-aeron-profiel;PER-sef;PER-bram;PER-gew-dagny;PER-tharn-lunn;PER-tharn-bor;PER-ysara;PER-mira-dochter'),
('HAAK-PER-intrige','Intriges en verraad (overzicht)','Opvolging van Ithrael: Moeder Vessa (Stille Hand) tegen de Stille Twijfel (Imra, Ennia). Selvine laat de Orde failliet gaan via schuld. Ondessa preekt vrijheid maar houdt Zoutloodsen. Brannoch verbergt haar stemgave-broer Rhun-ir. Drask en Morvane-ir delen een pact dat elk wil breken. Verraders: Sorn (Aelthir voor de Stille Hand), Orl (Vathren-schuilplaats), Kara (geruchten), Iska (Ves-Lethi-kinderen in Saelith).','PER-ithrael;PER-sch-vessa;PER-imra;PER-selvine;PER-ondessa;PER-brannoch;PER-sch-rhun;PER-drask;PER-aelthir-sorn;PER-vathren-orl'),
('HAAK-PER-erotiek','Erotische situaties (overzicht, gedoseerd)','Vertrouwd: Lampenfeest-nachten, het Oogstbed, havennachten, vrouwenliefde in Brakhaven, Strijdontvangst voor de slag. Vreemd (sparzaam als contrast): Vuurkamp van de Karrûk, valparing van de Skerra, Spiegelnacht van de Ves-Lethi, paaipoel van de Oevrin. Extreem (alleen met functie): rotbed van de Myrrhen, Vleesgemeente. Altijd volwassenen die kiezen; dwang alleen als donker thema, geen scène met wie niet kan instemmen.','PER-gew-kara;PER-gew-dagny;PER-sef;PER-karruk-yssa;PER-skerra-ka;PER-veslethi-nara;PER-oevrin-vaa;PER-myrrhen-lys;PER-sch-mavra'),
('HAAK-PER-thriller','Thrillerklokken en geheimen (overzicht)','Klok 1: Teo staat als Lijngraver bijgeschreven (Drempelmoeder Ysolde); de Stille Hand heeft zijn blad. Klok 2: Drask sterft binnen vijf jaar en moet nu toeslaan. Klok 3: de Zegelbinding heeft Orrim-steen nodig (Sha, Dru). Geheimen die alles kantelen: Oude Grieta is Liora\'s grootmoeder; Marit vervalste Liora\'s register; de stem in de Wortel (Ysara?); Ommo, een vruchtbare Ves-Lethi-man.','PER-teo;PER-sch-ysolde;PER-sch-vessa;PER-drask;PER-orrim-sha;PER-grauwen-oud;PER-gew-marit;PER-ysara;PER-veslethi-ommo')]
for code,o,f,r in H: A(code,'Verhaal',o,f+GR,'verhaalhaken per genrespoor',r)
R.wrij('Vaelorn leeft 600 jaar vs Aelthir 400 jaar','PER-vaelorn-nu; VOLK-aelthir','Aelthir leven 400 jaar; Vaelorn leeft al sinds -400. Uitzondering (Sterrensteen?) of fout.','mogelijke fout')
R.wrij('Oude Grieta als grootmoeder van Liora','PER-grauwen-oud; PER-liora; LICH-liora','Een Grauwe grootmoeder maakt Liora ingeteeld; dat zou haar gloed verklaren (bloedafstand-theorie) maar botst met mogelijk Ishvar-bloed.','bron van verhalen')
R.wrij('Ves-Lethi-kinderen in Saelith','PER-barsten-veslethi; VOLK-ves-lethi; REGEL-verhouding','Als Iska kinderen verwekte, wat zijn hun geslachten en zitten ze in het register?','bron van verhalen')
R.wrij('Rhun-ir verborgen door Kaldra','PER-sch-rhun; PER-brannoch; MACHT-evenwicht','Een verborgen gaven-man breekt het monopolie; als de Orde het ontdekt, oorlog binnen Velmara.','bron van verhalen')
R.vraag('Is de stem in de Wortel Ysara, de Eerste Dochter?','Zou het Offer en de quest emotioneel verbinden.','PER-ysara;LIJN-fase-5')
R.vraag('Wie wordt het romantische eindpunt van Liora: Aeron-as, Sef, Ruy of niemand?','Hoofdspoor romance.','PER-liora-profiel;PER-aeron-profiel;PER-sef;PER-vathren-ruy')
R.log('personages per fase (8+ per fase, 801), per volk minstens 3, gewone mensen en schurken, met verhaalhaken per genrespoor.')
R.klaar()
