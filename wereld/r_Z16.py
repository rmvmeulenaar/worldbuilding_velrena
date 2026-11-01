# Ronde Z16: roman "The Body Is the Price" in de canon. Idempotent; data in z16/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z16'); from data import LABEL,JAAR,B,Y
RONDE=46;TAG='Z16';D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z16.db'): shutil.copy('canon.db','canon_backup_Z16.db')
c=sqlite3.connect(DB); S={'toegevoegd':0,'vervangen':[],'aangevuld':[]}
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
CAT=c.execute("select categorie from canon where code='ROMANCE-Z15b-ysa-beatplan'").fetchone()[0]
def put(code,cat,ond,feit,status,ver,jaar,intens=None,weet=None,functie='VERH',reden=None):
  feit=feit if 'Veiligheidslabel' in feit else feit+LABEL
  r=(cat,ond,feit,status,reden or f'Ronde {TAG} {D}: roman Ysa (Wattpad)',ver,RONDE,code,ver,jaar,tp(jaar),intens,weet,functie,'geen')
  if c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('update canon set categorie=?,onderwerp=?,feit=?,status=?,reden=?,hangt_samen_met=?,ronde=?,verwijst_naar=?,jaar=?,tijdperk=?,intensiteit=?,weet=?,functie=?,techniek=? where code=?',r[:7]+r[8:]+(code,))
  else:
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',r); S['toegevoegd']+=1
def vervang(oud,nieuw):
  c.execute("update canon set status='voorlopig, vervangen', reden=coalesce(reden,'')||? where code=? and status!='voorlopig, vervangen'",(f' [Ronde {TAG}: vervangen door {nieuw}]',oud)); S['vervangen'].append(oud)
def ap(code,txt):
  m='[Z16]'; f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if not f: S.setdefault('niet_gevonden',[]).append(code); return
  if m not in f[0]: c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code))
  S['aangevuld'].append(code)
# 1 besluiten
for n,o,f in B:
  put(f'BESLUIT-Z16-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}','vastgesteld','ROMAN-Z16-roman;VERHAAL-Z16-novelle',-1240 if n not in('8',) else -1209,functie='META')
# 2 nieuwe feiten
for n,o,f,j,bron in Y:
  put(f'YSA-Z16-{n}',CAT,o,f'{f} Nieuw bedacht ({bron}); voorstel, wacht op goedkeuring van Rogier.','voorlopig','ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',j)
# 3 hoofdstukken
P=open('verhalen/roman_ysa_hoofdstukplan.md').read()
INT={int(m.group(1)):int(m.group(2)) for m in re.finditer(r'^\| (\d+)(?: ★)? \| [^|]+ \| \d \| \d \| \d \| \d \| (\d+)[^|]*\|',P,re.M)}
n=0
for m in re.finditer(r'^\| (\d+) \| \*\*(.+?)\*\*(.*?)\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| ([\d ]+) \| (.+?) \| (.+?) \| (\d+) \|\s*$',P,re.M):
  h=int(m.group(1)); n+=1; tit,ex,pov,klok,wat,vraag,eind,gen,heat,iro,wd=[x.strip() for x in m.groups()[1:]]
  g=gen.split(); E=int(g[1]) if len(g)>1 else 0
  put(f'ROMAN-Z16-h{h:02d}',CAT,f'Roman Ysa h{h}: {tit}',f'Hoofdstuk {h} van "The Body Is the Price" (Wattpad). POV: {pov}. Klok/plek: {klok}. {wat.replace("**","")} Vraag van de lezer: {vraag} Einde: {eind.replace("**","")} Genres R E H S A F: {gen}. Heat: {heat}. Ca. {wd} woorden.','voorlopig','ROMAN-Z16-roman',JAAR.get(h,-1240),INT.get(h),f'Ironie: {iro}','VERH;LUST' if E>=2 else 'VERH')
S['hoofdstukken']=n; assert n==33,n
put('ROMAN-Z16-roman',CAT,'Roman "The Body Is the Price" (Wattpad)','Engelse Wattpad-roman van Ysa en Thalen, fase 0 Voortijd (-1240 tot -1238, sprongen naar -1200, -1198 en ca. 801). 33 hoofdstukken (ROMAN-Z16-h01..h33), ca. 61.000 woorden, vier aktes; close third, afwisselend Ysa/Thalen; tijdsregel in elke kop; geen trage proloog, drie ORBIT-flitsen (h9, 22, 33). Twists in h5, 15, 20, 24, 29, 33. Expliciete scènes h6 (teder) en h18 (donker, beiden expliciet ja); h25 buiten beeld. Motoren: klok, bevel (ironie), liefde, Thalens zwijgen, stemming, Hesta/Corran, mysterie Reckoner. Bestanden: verhalen/roman_ysa_hoofdstukplan.md, roman_ysa_h01.md (geschreven). Bouwt op beatplan 03 (ROMANCE-Z15b-ysa-beatplan) en de novelle (VERHAAL-Z16-novelle).','voorlopig','ROMANCE-Z15b-ysa-beatplan;VERHAAL-Z16-novelle;BESLUIT-Z16-1;BESLUIT-Z16-3;BESLUIT-Z16-6',-1240,9,'Volk: legende. Orde: verzwijgt. Lezer: alles.')
put('VERHAAL-Z16-novelle',CAT,'Novelle "The Body Is the Price" (verhaal 03)','Engelse novelle, ca. 9450 woorden: proloog in de baan, 7 hoofdstukken, twee tussenstukken (jaar 3, jaar 40), epiloog met de scherf. Bestand: verhalen/verhaal_03_ysa_en.md; rapport verhaal_03_ysa_rapport.md; glossarium glossary_03_en.md. Volgt beatplan 03 (Z15b). Revisiecijfer ca. 8. Basis voor de roman ROMAN-Z16-roman.','voorlopig','ROMANCE-Z15b-ysa-beatplan;ROMAN-Z16-roman;BESLUIT-Z16-6',-1240,9,'Lezer: alles.')
# 4 botsende rijen vervangen
put('TOESTAND-Z16-PER-v4-ysa-maren-3','Tijdlijn','Ysa: dood in -1209','Ysa Maren sterft in -1209 (jaar 31 na de landing), ca. 61 jaar oud (BESLUIT-Z16-8). Leeft voort als Moeder Ysa en later de godin Ysa.','vastgesteld','BESLUIT-Z16-8;PER-v4-ysa-maren',-1209,functie='TIJD')
vervang('TOESTAND-Z11-PER-v4-ysa-maren-3','TOESTAND-Z16-PER-v4-ysa-maren-3')
put('TOESTAND-Z16-PER-v4-thalen-orr-3','Tijdlijn','Thalen: stem in de kluis, dood -1198','Ca. -1201/-1200 (jaar 39-40) bouwt Thalen zijn stem in de kernkamer/kluis en vergeeft Ysa hardop (zij is dan al dood, -1209). In -1198 (jaar 42) sterft de mens, 76 jaar oud; stem en wil leven door in de Rekenaar (BESLUIT-Z15-1). Voorstel (YSA-Z16-11).','voorlopig','YSA-Z16-11;BESLUIT-Z15-1;BESLUIT-Z16-8',-1198,functie='TIJD')
vervang('TOESTAND-Z15-PER-v4-thalen-orr-3','TOESTAND-Z16-PER-v4-thalen-orr-3')
ap('YSA-Z15-9','Precisering: stem gebouwd in jaar 39-40, de mens sterft in -1198 op 76 (YSA-Z16-11); Ysa is dan al dood (-1209).')
ap('YSA-Z15-4','Exact: 3454 van ca. 11.000 Makers (BESLUIT-Z16-9).')
ap('YSA-Z15-11','Engels: "Consent broken. Consent sought." / "Consent found. The Reckoner waits." (BESLUIT-Z16-7).')
ap('PER-v4-ysa-maren','Sterft in -1209 (BESLUIT-Z16-8).')
ap('PER-v4-thalen-orr','Sterft als mens in -1198, 76 jaar (YSA-Z16-11, voorstel).')
ap('PER-v4-hesta-kael','Kende de kernroute vóór de Muiterij (YSA-Z16-5); wond: "nobody keeps what they don\'t hold".')
ap('PER-v4-corran-velt','Trekt na de verbanning naar de bergen (YSA-Z16-7).')
ap('ORIGIN-WAAROM-11','Aantallen: 3454 doden van ca. 11.000; ca. 7000 landen (BESLUIT-Z16-9).')
# 5 wrijvingen
c.execute("delete from wrijving where code like 'WRIJ-Z16-%'")
W=[('Ves-Anath als inslagplek','GEB-sterrensteen-inslag;REG-groenmuil;PLEK-ves-anath-ruines;PLEK-HEILIG-ves-anath;ORIGIN-8;YSA-Z16-18','Verhaal 1 zegt dat de Sterrensteen "in Ves-Anath uit de hemel was gevallen"; LICH-dochters en GEB-r10-eerste-lek leggen de steen bij Ves-Anath. Maar GEB-sterrensteen-inslag en ORIGIN-8 leggen de hoofdinslag (-480) in het Hoogvrouwe-gebergte, de splinter in de Rosse Woestijn, terwijl REG-groenmuil en PLEK-ves-anath-ruines Ves-Anath in Groenmuil plaatsen; PLEK-HEILIG-ves-anath noemt het "officieel de plek waar Ysa neerdaalde". De novelle ("northern hills", heilige stad) past bij beide. Aanbeveling: Ves-Anath ligt in de zuidelijke uitlopers van Hoogvrouwe, waar het gebergte overgaat in het hete dal van Groenmuil; de hoofdinslag van -480 ligt daar en de heilige stad is eromheen gebouwd. Zo kloppen verhaal 1, de novelle en beide regio\'s zonder tekstwijziging. Rogier beslist.','open'),
('Sterfjaar Ysa','TOESTAND-Z11-PER-v4-ysa-maren-3;BESLUIT-Z16-8','Oude aanname: Ysa overleden ca. -1200 (levensduur 70). Nieuw besluit: -1209. Opgelost: nieuwe rij TOESTAND-Z16-PER-v4-ysa-maren-3, oude vervangen.','opgelost'),
('Thalens sterfjaar en leeftijd','TOESTAND-Z15-PER-v4-thalen-orr-3;YSA-Z16-11','Oud: ca. -1200, ca. 74. Novelle: stem gebouwd jaar 39-40, dood -1198 op 76. Opgelost met nieuwe tijdlijnrij (voorstel); oude vervangen.','opgelost'),
('"800 jaar" in HAAK-V5-zegel-6','HAAK-V5-zegel-6;BESLUIT-Z15-2','HAAK-V5-zegel-6 zegt "voor het eerst in 800 jaar" bij jaar -1238, wat niet past bij BESLUIT-Z15-2 (800 jaar = Thalens tijd in de baan). Aanbeveling: lees het als de herstelproef in de tijd van Liora (ruim 2000 jaar na de sleutelbreuk) en zet het jaar op 801 bij een volgende ronde. Rogier beslist.','open'),
('Kraaienzin verhaal 1','YSA-Z16-12','Verhaal 1: "Het lichaam is de prijs. Wie nee zegt, wordt niet gevraagd." Alleen het eerste deel is van Ysa. Aanbeveling: het tweede deel is een toevoeging van de Orde aan haar stem (vervalsing in de kraaien), wat het thema verraad versterkt. Rogier beslist.','open'),
('Ysa stelt schriftverbod voor','YSA-Z16-17','Nieuw: Ysa stelt het schriftverbod zelf voor, zonder stemming. Geen eerdere rij botst; wel nieuw voor de godsdienst (de godin verbood zelf het schrift). Voorstel.','open')]
for i,(t,d,b,s) in enumerate(W,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z16',s,f'WRIJ-Z16-{i}',d))
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
put('KWALITEIT-Z16','Besluit','Kwaliteitsrapport ronde Z16',f'Ronde Z16 ({D}): roman "The Body Is the Price" in de canon. BESLUIT-Z16-1..9 vastgesteld; YSA-Z16-1..20 voorstel; ROMAN-Z16-roman, 33 hoofdstukken, VERHAAL-Z16-novelle. Ysa en Thalen tijdlijn bijgewerkt. Wrijvingen WRIJ-Z16-1..6. Statussen: {st}.','voorlopig','ROMAN-Z16-roman',801,functie='META')
c.execute("delete from logboek where wat like 'Ronde Z16: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z16: roman Ysa (Wattpad) in de canon; 9 besluiten, 20 voorstellen, 33 hoofdstukken.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
S['vervangen']=sorted(set(S['vervangen']));S['aangevuld']=sorted(set(S['aangevuld']))
json.dump(S,open('z16/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
