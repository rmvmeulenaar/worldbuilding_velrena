# Ronde Z4: beslissingen Rogier, mensen per volk en fase, sleutelplekken, kernwrijvingen, bijschrijven (idempotent)
import sqlite3,shutil,os
from r_Z4_mensen import M
from r_Z4_plekken import P,ROUTE
from r_Z4_herschrijf import H
RONDE=33;TAG='Z4';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
FN=['0 Voortijd (Makers, ca. -1240)','1 Overvloed (-600..-150)','2 Vonk (-150..-40)','3 Brand (-40..0)','4 Noodtoestand (0..130)','5 Ontvangst (130..340)','6 Markt (340..720)','7 Barsten (720..801)']
if not os.path.exists('canon_backup_Z4.db'): shutil.copy('canon.db','canon_backup_Z4.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='ZINT',status='voorlopig'):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+GR,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie));n+=1
def vervang(old,new):
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z4: vervangen door {new}]',old))
# 1 besluiten
B={
'VRAAG-014':('liora','Liora is een boerendochter van 25 uit Hallowyn.','Een buitenstaander ontdekt de wereld tegelijk met de lezer; 25 is oud genoeg voor eigen keuzes, erotiek en verantwoordelijkheid.','Twijfel: ze hoort nergens bij, dus elke partij wil haar. Beslissend moment: zij kiest de derde weg omdat ze geen kant verschuldigd is.','PER-liora;STAD-hallowyn;BESLUIT-Z1-derdeweg'),
'VRAAG-026':('fasen','De 7 fasen (plus de Voortijd als fase 0) en het skelet van ruim 80 gebeurtenissen zijn de vaste tijdlijn; uitbreidbaar, volgorde ligt vast. Aanpassing Rogier: elk volk heeft een eigen geschiedenis en in elke fase zijn een aantal mensen belangrijk (PERS-Z4-*, VOLK-GESCHIEDENIS-OVERZICHT-Z4-*).','Een vaste volgorde voorkomt tegenspraak; mensen per fase maken van de tabel een keten van keuzes.','Elk verhaal kan op een ander moment spelen; verraad in fase 3 wordt erfschuld in fase 7.','TIJD-V4-fasejaren;FASE-overvloed;FASE-barsten'),
'VRAAG-031':('skelet','Zie BESLUIT-Z4-fasen: het skelet van ronde 10 blijft, aangevuld met mensen per volk en fase.','Zelfde reden als de fasen.','Zelfde gevolg.','BESLUIT-Z4-fasen'),
'VRAAG-042':('volken','De percentages per volk kloppen; elk volk krijgt één hoofdpersoon (HOOFDPERS-Z4-*).','Een hoofdpersoon maakt van een volksgeschiedenis een verhaal; volken kunnen elkaar tegenspreken.','Veertien perspectieven: wie de lezer vertrouwt, hangt af van wiens ogen hij leent.','VOLK-dhurn;VOLK-orrim'),
'VRAAG-057':('plekken','Rogier vindt vijf plekken te weinig. Besluit: een lijst sleutelplekken wereldwijd (PLEK-Z4-*, minstens 4 per regio plus plekken van niet-menselijke volken) en een boek-1-route over 10 plekken in 6 regio\'s (ROUTE-Z4-boek1).','Een wereld leeft van afwisseling; elke regio moet scènes kunnen dragen.','Boek 1 wordt een reis van rand naar hart, met telkens een ander zintuiglijk motief.','ROUTE-Z4-boek1;LIJST-Z4-boeken'),
'VRAAG-060':('prequel','Het eerste prequel-boek is de Muiterij op Ysa: Hesta\'s verraad, Ysa Marens bevel en de stemming 5 tegen 4.','Het begin van alles; vergroot de dramatische ironie van boek 1.','Twijfel: Thalen zag het verraad. Verraad: Hesta verkoopt Corran. Beslissend moment: de vijfde stem.','PER-v4-ysa-maren;PER-v4-hesta-kael;PER-v4-corran-velt;ORIGIN-WAAROM-7'),
'VRAAG-062':('nietmens','Elk niet-menselijk volk krijgt een eigen mega-verhaal (MEGA-Z4-*), kleiner dan de hoofdlijn.','Hun logica is anders; dat geeft wederzijds onbegrip en eigen conflicten.','Zeven verhalen die elkaar en de hoofdlijn kruisen.','VOLK-kluwer;VOLK-orrim'),
'VRAAG-D1-1':('ster','De bewegende ster is bewoond, maar verborgen; voorlopig alleen aanwijzingen (Lirra Sterrenkijkster telt een signaal).','Past bij de verborgen sciencefiction en geeft een lange boog.','Twijfel: is het de Ysa zelf of iets anders? Onthulling pas laat in de serie.','ORIGIN-8;PERS-Z4-skerra-7-2'),
'VRAAG-D1-3':('mannenraad','De Mannenraad krijgt laat en met een prijs echte macht; de Orde en de huizen keren zich ertegen.','Geen macht = stilstand, te snel = geen spanning.','Beslissend moment laat in fase 7 of daarna; prijs: een nieuw conflict met Orde of huizen.','PER-bram;PER-gewone-mannen'),
}
for v,(k,feit,why,gev,refs) in B.items():
  code=f'BESLUIT-Z4-{k}'
  add(code,'Besluit',f'Besluit Rogier: {v}',f'{feit} Waarom: {why} Gevolg voor de verhalen: {gev} Haak: elke keuze laat een spoor van twijfel achter.','besluit Rogier (pt112u), vastgesteld',refs+';'+v,'geen','BESL','vastgesteld')
  r=c.execute("select status from open_vraag where code=?",(v,)).fetchone()
  if r and r[0]!='beantwoord (Rogier)':
    c.execute("update open_vraag set status='beantwoord (Rogier)', antwoord=? where code=?",(f'Z4: {feit} Zie {code}.',v))
# 4 wrijvingen
W={'WRIJ-074':('sterrensteen','De Sterrensteen is verhard Orrim-weefsel: lichaam én mineraal. Kernwachters die bij de val in de kern werden opgenomen versteenden; hun weefsel groeit als kristal.','Verklaart de pulserende reliekschilfer, de stem in de steen, de afstoting en waarom Orrim pijn voelen bij het hakken.','Geur: ozon en bloedend gruis. Geluid: een hartslag in de rots. Haak: Krie Barstzang zegt "hij is van ons"; hakken is lijkschennis.','VOLK-orrim;GEB-sterrensteen-inslag;PERS-Z4-orrim-7-2'),
'WRIJ-080':('wortelstem','De stem in de Wortel is Thalen Orr, langzaam versmolten met het Zegel; het Zegel kan zijn stem overnemen.','Houdt het een mens met een keuze, maar maakt elke zin twijfelachtig.','Geluid: een stem die telt en soms midden in een zin van toon wisselt. Haak: is dit nog hij?','PER-v4-thalen-orr;ORIGIN-WAAROM-12;LIJN-fase-5')}
for w,(k,feit,why,zt,refs) in W.items():
  code=f'BESLUIT-Z4-{k}'
  add(code,'Besluit',f'Kernwrijving beslist: {w}',f'{feit} Waarom: {why} {zt}','ingenieursbesluit (pt112u akkoord met voorstellen)',refs+';'+w,'zegelsteen','BESL')
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and status!='opgelost'",(f' | Oplossing Z4: {feit} Zie {code}.',w))
# 2 mensen
for vk,(vn,vc,F,hp) in M.items():
  keten=[]
  for f in range(8):
    namen=[]
    for i,(naam,rol,ver,zin,hk,refs,best) in enumerate(F[f],1):
      code=f'PERS-Z4-{vk}-{f}-{i}'
      if best:
        bf=c.execute("select substr(feit,1,160) from canon where code=?",(best,)).fetchone()[0].split(' Label:')[0]
        add(code,'Personage',f'{naam} ({vn}, fase {FN[f]})',f'Verwijzing naar bestaand personage {best} (geen dubbel). Rol in de keten van de {vn}: {rol} in fase {FN[f]}. Kern: {bf} Haak: zie {best}.','belangrijk persoon per volk en fase (verwijzing)',f'{best};{vc}','geen','VERW')
      else:
        add(code,'Personage',f'{naam} ({vn}, fase {FN[f]})',f'Volk: {vn}. Fase: {FN[f]}. Rol: {rol}. Verandert: {ver} Zintuiglijk: {zin} Haak: {hk}','belangrijk persoon per volk en fase',f'{refs};{vc}','geen','PER')
      namen.append(f'{naam} ({code})')
    keten.append(f'Fase {FN[f]}: '+' en '.join(namen)+'.')
  add(f'VOLK-GESCHIEDENIS-OVERZICHT-Z4-{vk}','Geschiedenis',f'Geschiedenis van de {vn} als keten van mensen',' '.join(keten)+f' Elke fase geeft de volgende een erfenis of een schuld. Haak: wie in fase 0 een geheim meenam, bepaalt wat de {vn} in fase 7 vinden.','volksgeschiedenis als keten van mensen',vc,'geen','GESCH')
  f,i=hp;naam=F[f][i][0]
  add(f'HOOFDPERS-Z4-{vk}','Personage',f'Hoofdpersoon van de {vn}: {naam}',f'Hoofdpersoon voor verhalen vanuit de {vn}: {naam} (PERS-Z4-{vk}-{f}-{i+1}). Waarom: staat in fase {FN[f]} op het kruispunt van de eigen geschiedenis en de hoofdlijn (Liora, Zegel). Haak: zijn of haar keuze botst met wat de rest van het volk wil.','hoofdpersoon per volk (VRAAG-042)',f'PERS-Z4-{vk}-{f}-{i+1};{vc};BESLUIT-Z4-volken','geen','PER')
# mega-verhalen niet-menselijk
MEGA={'kluwer':('De korf die wilde stemmen','Een korf wordt bewust en eist een stem in de raad na het Zegel.','Conflict: de Orde wil de was, niet de stem; de korf kan de Pest stoppen of verspreiden.'),
'myrrhen':('Het net dat alles onthoudt','Het geheugennet bewaart de stemming 5 tegen 4 en het Hal-Neth-register.','Conflict: wie het net bezit, bezit de waarheid; Rhoss wil het verkopen.'),
'oevrin':('De slikgangen naar de lander','Oevrin-gangen leiden naar een lander met stroom.','Conflict: smokkelen of onthullen; Slikvorst Brok wil de lander voor zichzelf.'),
'tharn':('De dijken die stoppen met zingen','De reuzen waren ontworpen om te stoppen met groeien, en stoppen nu met zingen.','Conflict: zonder lied breken de dijken; de reuzen eisen vrijheid in ruil voor werk.'),
'orrim':('De gebonden voorouders','De Orrim ontdekken dat het Zegel en de Sterrensteen hun eigen doden zijn.','Conflict: bevrijden betekent het Zegel breken; Graal Steenvreter wil wraak.'),
'skerra':('Het signaal van de ster','Skerra-sterrenkijkers tellen een signaal van de bewegende ster.','Conflict: het nieuws vliegen of verbergen; de Orde wil de koeriers binden.'),
'veslethi':('De noodvoorraad wordt wakker','De vormwisselaars waren ontworpen als noodvoorraad voor het evenwicht en kunnen het Zegel misleiden.','Conflict: man worden en vrij zijn, of ingezet worden als wapen.')}
for vk,(t,wie,conf) in MEGA.items():
  vn,vc=M[vk][0],M[vk][1]
  add(f'MEGA-Z4-{vk}','Verhaal',f'Mega-verhaal {vn}: {t}',f'Wie: de {vn}, met hoofdpersoon HOOFDPERS-Z4-{vk}. Wat: {wie} {conf} Haken: kruist de hoofdlijn bij Liora en het Zegel; elke fase in VOLK-GESCHIEDENIS-OVERZICHT-Z4-{vk} levert een scène.','mega-verhaal niet-menselijk volk (VRAAG-062)',f'{vc};HOOFDPERS-Z4-{vk};BESLUIT-Z4-nietmens','geen','VERH')
# 3 plekken
for s,naam,reg,mo,pol,sc,hk,refs in P:
  add(f'PLEK-Z4-{s}','Land',f'Sleutelplek: {naam}',f'Regio: {reg}. Zintuiglijk motief: {mo} Politiek gewicht: {pol} Scènesoort: {sc}. Haak: {hk}','sleutelplek wereldwijd (VRAAG-057)',f'{reg};{refs};BESLUIT-Z4-plekken','geen','PLEK')
pn={p[0]:p[1] for p in P}
add('ROUTE-Z4-boek1','Verhaal','Boek-1-route over sleutelplekken','Route: '+' → '.join(f'{pn[s]} (PLEK-Z4-{s})' for s in ROUTE)+'. Zes regio\'s: Ambergaard, Saelith, Zoutkust, Groenmuil, Rosse, Hoogvrouwe, met een uitstap naar de Kharvos-schaduwvlakte. Elke halte wisselt zintuig (hooi, wierook, mist, kamille, ozon, ademende wortel). Haak: de route volgt de kale banen van het amberkoren naar de Wortel.','boek-1-route',';'.join('PLEK-Z4-'+s for s in ROUTE)+';BESLUIT-Z4-plekken','geen','VERH')
add('LIJST-Z4-boeken','Verhaal','Waar verhalen per boek en tijdperk kunnen spelen','Prequel (fase 0): de Ysa, de landers, PLEK-Z4-zout-4 (Wrakkust) en PLEK-Z4-kharvos-5 (Leegtewormen). Fase 1-2: PLEK-Z4-amber-4, PLEK-Z4-hoog-3, PLEK-Z4-nm-4. Fase 3: PLEK-Z4-amber-3, PLEK-Z4-hoog-2. Fase 4-5: PLEK-Z4-saelith-1, PLEK-Z4-saelith-2, PLEK-Z4-rosse-3. Fase 6: PLEK-Z4-saelith-3, PLEK-Z4-groen-3, PLEK-Z4-nm-7. Boek 1 (fase 7): ROUTE-Z4-boek1. Boek 2: PLEK-Z4-kharvos-1, PLEK-Z4-kharvos-4, PLEK-Z4-stille-2. Boek 3: PLEK-Z4-hoog-5, PLEK-Z4-nm-1 (de ster). Haak: elke plek komt in minstens twee tijdperken terug, telkens anders.','lijst per boek/tijdperk','ROUTE-Z4-boek1;BESLUIT-Z4-plekken','geen','VERH')
# 5 bijschrijven
for old,(z,h,v,s,hk,refs,tech) in H.items():
  r=c.execute("select categorie,onderwerp from canon where code=?",(old,)).fetchone()
  if not r: continue
  new=old.replace('Z3','Z4')+'-b'
  add(new,r[0],r[1],f'{z} Herkenbaar: {h} Vreemd: {v} Scène: {s}. Haak: {hk}',f'bijgeschreven, vervangt {old}',refs+';'+old,tech)
  vervang(old,new)
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z4] Nog dun:')
c.execute("delete from canon where code='ZINT-DEKKING-Z4'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking Z4',txt,'voorlopig','Ronde Z4: meting','ZINT-DEKKING-Z3',RONDE,'ZINT-DEKKING-Z4','REG-overzicht;ZINT-DEKKING-Z3','geen','META'))
vervang('ZINT-DEKKING-Z3','ZINT-DEKKING-Z4')
c.execute("delete from logboek where wat like 'Ronde Z4:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z4: besluiten Rogier (9 vragen), WRIJ-074/080, mensen per volk en fase, hoofdpersonen, mega-verhalen, {len(P)} sleutelplekken, route boek 1, {len(H)} rijen bijgeschreven.'))
c.commit()
print('nieuw',n)
print('open wrij',c.execute("select count(*) from wrijving where status!='opgelost'").fetchone(),'open vragen',c.execute("select count(*) from open_vraag where status='open'").fetchone(),'canon',c.execute('select count(*) from canon').fetchone())
print(txt)
