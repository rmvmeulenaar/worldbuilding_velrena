# Ronde Z17: keuzes h1-6 en open punten Z16. Idempotent; data in z17/
import sqlite3,shutil,os,sys,json
sys.path.insert(0,'z17'); import importlib; data=importlib.import_module('data'); B,Y,D=data.B,data.Y,data.D
sys.path.pop(0)
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
RONDE=47;TAG='Z17';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z17.db'): shutil.copy('canon.db','canon_backup_Z17.db')
c=sqlite3.connect(DB); S={'toegevoegd':0,'vervangen':[],'aangevuld':[]}
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,status,ver,jaar,functie='VERH',intens=None,weet=None):
  feit=feit if 'Veiligheidslabel' in feit else feit+LABEL
  r=(cat,ond,feit,status,f'Ronde {TAG} {D}: keuzes h1-6 en open punten Z16',ver,RONDE,code,ver,jaar,tp(jaar),intens,weet,functie,'geen')
  if c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('update canon set categorie=?,onderwerp=?,feit=?,status=?,reden=?,hangt_samen_met=?,ronde=?,verwijst_naar=?,jaar=?,tijdperk=?,intensiteit=?,weet=?,functie=?,techniek=? where code=?',r[:7]+r[8:]+(code,))
  else:
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',r); S['toegevoegd']+=1
def vervang(oud,nieuw):
  c.execute("update canon set status='voorlopig, vervangen', reden=coalesce(reden,'')||? where code=? and status!='voorlopig, vervangen'",(f' [Ronde {TAG}: vervangen door {nieuw}]',oud)); S['vervangen'].append(oud)
def ap(code,txt):
  m='[Z17]'; f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if not f: S.setdefault('niet_gevonden',[]).append(code); return
  if m not in f[0]: c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code))
  S['aangevuld'].append(code)
def cat(code): return c.execute('select categorie from canon where code=?',(code,)).fetchone()[0]
for n,o,f,j,v in B:
  put(f'BESLUIT-Z17-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}','vastgesteld',v,j,'META')
for n,o,f,j,bron in Y:
  put(f'YSA-Z17-{n}',CAT,o,f'{f} Nieuw bedacht (roman {bron}); voorstel, wacht op goedkeuring van Rogier.','voorlopig','ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',j)
# Ves-Anath / inslag
put('GEB-Z17-sterrensteen-inslag',cat('GEB-sterrensteen-inslag'),'Sterrensteen-inslag bij Ves-Anath','Jaar -480. Het zaaischip valt als de Sterrensteen in de zuidelijke uitlopers van het Hoogvrouwe-gebergte, waar het overgaat in het dal van Groenmuil; gloeit bij levend bloed. Rond de inslag groeit later de heilige stad Ves-Anath (BESLUIT-Z17-6). Splinter in de Rosse Woestijn blijft.','vastgesteld','BESLUIT-Z17-6;YSA-Z16-18;PLEK-ves-anath-ruines',-480,'GEB')
vervang('GEB-sterrensteen-inslag','GEB-Z17-sterrensteen-inslag')
for k in ('PLEK-ves-anath-ruines','PLEK-HEILIG-ves-anath','REG-groenmuil','YSA-Z16-18','ORIGIN-8','TOESTAND-Z15-PER-v4-thalen-orr-4'):
  ap(k,'Ves-Anath ligt in de zuidelijke uitlopers van Hoogvrouwe, waar het overgaat in het dal van Groenmuil; de inslag van -480 ligt daar (BESLUIT-Z17-6).')
# HAAK 800 jaar
put('HAAK-Z17-zegel-6',cat('HAAK-V5-zegel-6'),'Herstelproef met de sleutel (801)','Jaar 801, tijd van Liora. Bij een proef met de herstelde sleutel vraagt de kracht voor het eerst sinds de sleutelbreuk van -1240 (ruim 2000 jaar) instemming; twee volwassen geliefden ervaren wat seks met kracht kan zijn als beiden echt ja zeggen, en de Orde ziet haar macht verdampen (BESLUIT-Z17-7).','vastgesteld','BESLUIT-Z17-7;HAAK-V5-zegel-6;BESLUIT-Z15-2',801,'VERH;LUST')
vervang('HAAK-V5-zegel-6','HAAK-Z17-zegel-6')
ap('YSA-Z16-12','Besloten: het tweede deel van de kraaienzin is een toevoeging van de Orde (BESLUIT-Z17-8).')
ap('YSA-Z16-17','Besloten: vastgesteld als BESLUIT-Z17-9.')
# leeftijd Thalen
put('TOESTAND-Z17-PER-v4-thalen-orr-1','Tijdlijn','Thalen: geboren ca. -1272','Geboren ca. -1272, aan boord van het zaaischip Ysa. Leeftijd 32 in -1240 (h4), twee jaar ouder dan Ysa (YSA-Z17-9). Voorstel.','voorlopig','YSA-Z17-9',-1272,'TIJD')
vervang('TOESTAND-Z15-PER-v4-thalen-orr-1','TOESTAND-Z17-PER-v4-thalen-orr-1')
put('TOESTAND-Z17-PER-v4-thalen-orr-2','Tijdlijn','Thalen in -1240 (32)','Jaar -1240, leeftijd 32. Rol: piloot, ontwerper van vonkcellen en instemmingssleutel (gebouwd na de dood van Edo Raske, BESLUIT-Z17-1), geliefde van Ysa. Wil: met haar landen en samen oud worden. Geheim: zag haar bevel in het log en zwijgt. Verandert: blijft in de baan.','voorlopig','YSA-Z17-9;BESLUIT-Z17-1',-1240,'TIJD')
vervang('TOESTAND-Z15-PER-v4-thalen-orr-2','TOESTAND-Z17-PER-v4-thalen-orr-2')
put('TOESTAND-Z17-PER-v4-thalen-orr-3','Tijdlijn','Thalen: stem in de kluis, dood -1198 (74)','Ca. -1201/-1200 (jaar 39-40) bouwt Thalen zijn stem in de kernkamer en vergeeft Ysa hardop (zij is dan al dood, -1209). In -1198 (jaar 42) sterft de mens, 74 jaar oud (novelle); stem en wil leven door in de Rekenaar (BESLUIT-Z15-1). Voorstel.','voorlopig','YSA-Z17-9;YSA-Z16-11;BESLUIT-Z15-1',-1198,'TIJD')
vervang('TOESTAND-Z16-PER-v4-thalen-orr-3','TOESTAND-Z17-PER-v4-thalen-orr-3')
ap('YSA-Z15-1','Gecorrigeerd: 32 in -1240, geboren ca. -1272, twee jaar ouder dan Ysa (YSA-Z17-9).')
ap('YSA-Z16-11','Gecorrigeerd: 74 jaar bij zijn dood, niet 76 (novelle: "seventy-four"; YSA-Z17-9).')
ap('PER-v4-thalen-orr','Leeftijd 32 in -1240, sterft als mens in -1198 op 74 (YSA-Z17-9, voorstel). Wond: Edo Raske (BESLUIT-Z17-1).')
ap('PER-v4-ysa-maren','Afkomst: counting rings (BESLUIT-Z17-5). Alleen "Het lichaam is de prijs" is van haar (BESLUIT-Z17-8); stelt zelf het schriftverbod voor (BESLUIT-Z17-9).')
# hoofdstukken
H={1:'Geschreven, ca. 1835 woorden. Einde: "Shall I register it…" / "I\'ll wait." Ongeregistreerde paring (verboden liefde). Navigator Venn genoemd.',
2:'Geschreven, ca. 1890 woorden. Roestschimmel, strain 4 verdubbelt in 18 uur (YSA-Z17-6); Ysa\'s afkomst uit de counting rings (BESLUIT-Z17-5); Mira en tomaat Beatrix (YSA-Z17-7). Einde: "4,000", daaronder *Thalen*.',
3:'Geschreven, ca. 1920 woorden. Raad 4-4 in de observatiekoepel, Hesta het slot (YSA-Z17-5); testvlucht "this afternoon". Einde: het enige bewijs zijn de doden.',
4:'Geschreven, ca. 1830 woorden. Thalens wond: Edo Raske, "acceptable loss" (BESLUIT-Z17-1); Thalen 32 (YSA-Z17-9); moeder en Corran (YSA-Z17-1); log 03:12 kaart MAREN, Y. (YSA-Z17-4).',
5:'Geschreven, ca. 1720 woorden. Bevestiging op de VIERDE nacht, 4 d 03:14 (BESLUIT-Z17-2); mechanisme van het bevel (YSA-Z17-2); gat in de sleutel "Air does not pass through a human body. It passes through a room." (BESLUIT-Z17-4); "Consent records may not be erased." (YSA-Z17-3).',
6:'Geschreven, ca. 1720 woorden, blijft zo (BESLUIT-Z17-3). Tedere, expliciete scène, beiden volwassen en duidelijk ja; "navigation star" (YSA-Z17-8). Hij wil naar het log vragen en doet het niet.'}
for h,t in H.items(): ap(f'ROMAN-Z16-h{h:02d}',t)
for h in (9,32): ap(f'ROMAN-Z16-h{h:02d}','Aanpassing bij het schrijven: de opname is in de VIERDE nacht vóór de landing, niet de vijfde (BESLUIT-Z17-2).')
ap('VERHAAL-Z16-novelle','Bekende afwijking: r. 196 zegt "fifth night"; canon is de vierde nacht (BESLUIT-Z17-2). Tekst niet veranderd.')
# wrijvingen
for k in (1,4,5,6):
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and beschrijving not like '%[Z17]%'",(f' [Z17] Opgelost door BESLUIT-Z17-{ {1:6,4:7,5:8,6:9}[k] } (Rogier: alles zoals aanbevolen).',f'WRIJ-Z16-{k}'))
c.execute("delete from wrijving where code like 'WRIJ-Z17-%'")
c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",('Thalens leeftijd 34/76 tegen 32/74','YSA-Z15-1;TOESTAND-Z15-PER-v4-thalen-orr-1;YSA-Z16-11;ROMAN-Z16-h04;VERHAAL-Z16-novelle','Z15 gaf 34 in -1240 (geboren -1274) en Z16 76 bij de dood in -1198. De geschreven tekst zegt 32 in -1240 (h4: 24 + 8 jaar) en "Thalen was seventy-four" in de novelle. Opgelost door de tekst te volgen: geboren ca. -1272, 32 in -1240, 74 in -1198, twee jaar ouder dan Ysa (YSA-Z17-9, voorstel). Oude tijdlijnrijen vervangen; YSA-Z15-1 en YSA-Z16-11 aangevuld. Rogier kan nog anders kiezen.','Z17','opgelost','WRIJ-Z17-1','YSA-Z17-9'))
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
put('KWALITEIT-Z17','Besluit','Kwaliteitsrapport ronde Z17',f'Ronde Z17 ({D}): BESLUIT-Z17-1..9 vastgesteld; YSA-Z17-1..9 voorstel; Ves-Anath en inslag vastgelegd; HAAK-Z17-zegel-6 (801); leeftijd Thalen 32/74 (WRIJ-Z17-1); ROMAN-Z16-h01..h06 aangevuld; WRIJ-Z16-1,4,5,6 opgelost. Statussen: {st}.','voorlopig','ROMAN-Z16-roman',801,'META')
c.execute("delete from logboek where wat like 'Ronde Z17: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z17: keuzes h1-6 en open punten Z16; 9 besluiten, 9 voorstellen.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
S['vervangen']=sorted(set(S['vervangen']));S['aangevuld']=sorted(set(S['aangevuld']))
json.dump(S,open('z17/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
