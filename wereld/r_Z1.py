# Ronde Z1: drie B1-wrijvingen + zintuiglijke verdieping (idempotent)
import sqlite3,shutil,os,re
from r_Z1_data import VB,MOT,REGIO
RONDE=30;TAG='Z1';D='2026-10-30'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud zonder instemming; donkere thema's gelabeld."
if not os.path.exists('canon_backup_Z1.db'): shutil.copy('canon.db','canon_backup_Z1.db')
c=sqlite3.connect('canon.db');n=0;verv=[]
def add(code,cat,ond,feit,reden,refs,tech='geen',status='voorlopig',**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar','techniek']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech]+list(kw.values()));n+=1
def F(code):
  r=c.execute("select feit from canon where code=?",(code,)).fetchone();return r[0] if r else ''
def vervang(old,new,feit,why):
  r=c.execute("select categorie,onderwerp,verwijst_naar,jaar,tijdperk,functie,techniek,status from canon where code=?",(old,)).fetchone()
  if not r: return
  add(new,r[0],r[1],feit,f'vervangt {old} ({why})',';'.join(x for x in [old,r[2] or ''] if x),tech=r[6] or 'geen',status='voorlopig',jaar=r[3],tijdperk=r[4],functie=r[5])
  if c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde {TAG}: vervangen door {new}]',old)).rowcount: verv.append(old)
def wrij(w,a):
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and status!='opgelost'",(f' [Opgelost Z1 {D}: {a}]',w))
# ---- WRIJ-B1-1 Harrow
add('ORIGIN-Z1-harrow','Oorsprong','De Harrow: één schip, twee sporen','De Harrow was het tweede zaaischip van dezelfde vloot als de Ysa (zelfde kernmerken, HAAK-B1-3-4). In de stemming koos de Harrow voor machines. Bij de landing brak het schip in tweeën: de voorsteven met de hoofdkern landde in Kharvos (onder de burcht van Hoornburg; dempt het Zegel aan de rand, daarom 1 op 3 jongens). Het achterschip met het ruim, de slaapkisten met volwassen bemanning en een reservekern, werd door de Leegtewormen opgeslokt toen die in de Leegte jaagden; daarom draagt het ruim van de wormen het Harrow-teken (ORIGIN-WAAROM-12). Reden (ingenieur): één schip in plaats van twee verklaart beide feiten met één oorzaak, verbindt Kharvos, wormen en Makers, en maakt de reservekern tot de inzet van boek 2-3: wie hem heeft, kan Kharvos óf het Zegel sturen. De hoofdkern hapert sinds ca. 790; Kharvos zoekt een vervangende kern, en dat is waarom het de wormen en de Sterrensteen wil.'+GR,'lost WRIJ-B1-1 op','BESLUIT-3;ORIGIN-WAAROM-12;REG-kharvos-B1;NAV-wormwording-B1;STAD-kharvos-hoornburg',tech='metaal+bio',jaar=0,functie='GEH')
for i,(o,t) in enumerate([('De reservekern','Kharvos en de Orde sturen elk een expeditie om een Leegteworm te vangen; de navigator weet dat de worm sterft als de kern wordt uitgesneden.'),('De slaper die wakker wordt','Een gewekte Harrow-ingenieur (volwassen) ziet Velmara en Kharvos en zegt: "Wij hadden gelijk, en jullie ook." Beide kanten willen hem.'),('De haperende lamp','Als de witte lamp boven Hoornburg flikkert, worden er in Kharvos minder jongens geboren; het volk merkt het voor de vorst het toegeeft.')],1):
  add(f'HAAK-Z1-harrow-{i}','Verhaal',f'Haak Harrow: {o}',t+GR,'verhaalhaak uit ORIGIN-Z1-harrow','ORIGIN-Z1-harrow',functie='THRL;INTR')
wrij('WRIJ-B1-1','Ja, hetzelfde schip: de Harrow brak bij de landing; voorsteven in Kharvos, achterschip met ruim in de wormen (ORIGIN-Z1-harrow).')
# ---- WRIJ-B1-2 jaartelling
KAP=' De kaping valt NIET op jaar 0. Tijdlijn (Z1): jaar 0 de Raad der Moeders en de Dochters binden het Zegel en zetten zonder het te weten Ysa\'s noodstand aan (ORIGIN-10); jaar 90 de Zusters worden de Orde (GEB-r10-orde-naam); ca. 128-130 ontdekken priesteressen onder de tempel van Ves-Anath de bediening (de Stemklok-kamer) en verschijnt het eerste zegellicht (GEB-Z1-kaping); in 205 herschrijft de Orde de annalen: "wij legden het" (GEB-r10-vervalste-annalen). De bekende zin "achthonderd jaar geleden" slaat op het Zegel zelf (jaar 0, in 801 ruim 800 jaar), niet op de kaping; de Orde beheert het Zegel sinds ca. 670 jaar.'
add('GEB-Z1-kaping','Geschiedenis','Jaar 130: de priesteressen vinden de bediening','Jaar 128-130 · Regio: Ves-Anath · Wie: Hoge Moeder Thessaly en drie priesteressen. Actie: onder de tempel vinden ze de Stemklok-kamer; ze leren drie handgrepen (HAAK-B1-1-3) en zien zegellicht verschijnen als er in de tempel wordt ontvangen. Gevolg: tempels op zegellijnen (GEB-r10-tempelbouw, 140) en de Orde als bediener van het Zegel. Ruim een eeuw na jaar 0, dus "eeuwen later" wordt "ruim een eeuw later".'+GR,'lost WRIJ-B1-2 op','GEB-eerste-ontvangst;GEB-r10-orde-naam;GEB-r10-vervalste-annalen;PER-thessaly;BESLUIT-1-Z1',tech='metaal+zegelsteen',jaar=130,tijdperk='5 Ontvangst')
b1=F('BESLUIT-1')
vervang('BESLUIT-1','BESLUIT-1-Z1',b1.replace('Rond jaar 0 tot 1 verborg de machinekennis zich; ca. 800 jaar vóór 801 vonden de eerste priesteressen van Ves-Anath de bediening','Na jaar 0 verborg de machinekennis zich; ca. jaar 130, ruim een eeuw later, vonden de priesteressen van Ves-Anath de bediening').replace(GR,'')+KAP+GR,'WRIJ-B1-2')
g=F('GEH-zegel-B1')
vervang('GEH-zegel-B1','GEH-zegel-Z1',g.replace('Achthonderd jaar geleden ontdekten de eerste priesteressen in Ves-Anath de bediening ervan en namen het zegel over','Achthonderd jaar geleden werd het Zegel gebonden; ruim een eeuw later (ca. jaar 130) ontdekten de priesteressen in Ves-Anath de bediening ervan en namen het zegel over')+KAP,'WRIJ-B1-2')
wrij('WRIJ-B1-2','"800 jaar" blijft voor het Zegel zelf (jaar 0); de kaping is ca. 130, de vervalsing 205; BESLUIT-1 en GEH-zegel-B1 vervangen (BESLUIT-1-Z1, GEH-zegel-Z1, GEB-Z1-kaping).')
# ---- WRIJ-B1-3 derde weg
add('BESLUIT-Z1-derdeweg','Besluit','Derde weg: wat gebeurt er met de Dochters en Orrim in het Zegel','Gekozen (voorlopig): de Dochters en Orrim worden gewekt, niet gedood. Als Liora de instemmingssleutel aan iedereen teruggeeft, vraagt het Zegel ook zijn eigen dragers voor het eerst om hun ja. Van de honderd Dochters en de Orrim-lichamen zegt een deel nee: zij komen vrij, maar na 800 jaar in de steen leven ze nog maar dagen tot een paar jaar (vergroeid, half steen, met herinneringen aan jaar 0). Een deel zegt ja en blijft vrijwillig, en wordt daarmee de eerste dragers die instemmen. Het Zegel draait daarna op minder kracht: de gaven doven gedeeltelijk, de 1 op 100 schuift langzaam (decennia) richting 1 op 20. Prijs: Ysara (de stem in de Wortel, BESLUIT-15) kiest om te blijven, zodat Liora haar niet kan redden; Aerons vonk dooft verder (BESLUIT-2/7); Thalen verliest zijn kans op herstel naar zijn plan. Reden (ingenieur): geen zuivere overwinning, elke kant verliest iets, en de keuze herhaalt het kernthema (toestemming) op de dragers zelf; het levert een finale met echte getuigen uit jaar 0 die de waarheid over Ysa kunnen vertellen.'+GR,'lost WRIJ-B1-3 op','BESLUIT-2;BESLUIT-V5-thalen;BESLUIT-15;GEB-offer-dochters;VOLK-orrim;PER-ysara;PER-liora',tech='zegelsteen+metaal',status='voorlopig')
for i,(f,o,t) in enumerate([('THRL','De getuigen uit de steen','Een vrijgekomen Dochter heeft nog drie dagen; ze weet wie het bevel gaf. Iedereen wil haar laatste dagen.'),('ROM','Blijven of gaan','Elin, de 49ste Dochter (volwassen), moet kiezen tussen vrijheid met een kort leven en blijven bij de vrouw die naast haar in de steen hing.'),('INTR','Wie spreekt voor de Orrim','De Orrim eisen dat hun doden niet als dragers worden vereerd maar als slachtoffers; de Orde weigert.'),('LUST','De eerste ja','Twee volwassen geliefden zijn de eerste die het Zegel vraagt; zij antwoorden in het bed en voelen voor het eerst hoe hun ja de kracht zachter maakt.')],1):
  add(f'HAAK-Z1-derdeweg-{i}','Verhaal',f'Haak derde weg: {o}',t+GR,'verhaalhaak uit BESLUIT-Z1-derdeweg','BESLUIT-Z1-derdeweg',functie=f)
wrij('WRIJ-B1-3','Dochters en Orrim worden gevraagd; een deel gaat (kort leven), een deel blijft vrijwillig; zie BESLUIT-Z1-derdeweg.')
# ---- 2a voorbeelden
for (k,o,reg,tech,z,h,v,s,hk,refs) in VB:
  add(f'ZINT-VOORBEELD-{k}','Zintuigen',f'Zintuiglijk: {o}',f'{z} Herkenbaar: {h} Vreemd: {v} Scène: {s}. Haak: {hk}'+GR,'zintuiglijke verdieping, voorbeeld voor Rogier',f'{reg};{refs}',tech=tech,functie='ZINT')
# ---- 2b motieven
for code,o,f in MOT:
  add(f'ZINT-MOTIEF-{code.split("-",1)[1].replace("-B1","")}','Zintuigen',f'Motief: {o}',f+' Gebruik: herhaal het motief bij elke scène op deze plek of met dit volk, zonder de naam te noemen.','terugkerend zintuiglijk motief',code,functie='ZINT')
# ---- 2c regio
for reg,(rc,rows) in REGIO.items():
  for i,(soort,o,f,hk,refs,tech) in enumerate(rows,1):
    add(f'{soort}-Z1-{reg}-{i}','Zintuigen' if soort!='STAD' else 'Land',f'{o}',f+f' Haak: {hk}'+GR,f'verdieping dunne regio {reg}',f'{rc};{refs};ZINT-MOTIEF-{rc.split("-",1)[1].replace("-B1","")}',tech=tech,functie='ZINT')
c.commit()
# ---- 2d meting
import dekking_z1
txt=dekking_z1.meet(c)
c.execute("delete from canon where code='ZINT-DEKKING'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Dekking: haken, zintuigen, verbindingen',txt,'voorlopig','Ronde Z1: meting (wordt bij elke run herberekend)','',RONDE,'ZINT-DEKKING','REG-overzicht','geen','META'))
c.execute("delete from logboek where wat like 'Ronde Z1:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z1: WRIJ-B1-1/2/3 opgelost (ORIGIN-Z1-harrow, GEB-Z1-kaping, BESLUIT-1-Z1, GEH-zegel-Z1, BESLUIT-Z1-derdeweg + haken); 20 ZINT-VOORBEELD, 22 ZINT-MOTIEF, 40 regiorijen (Zoutkust, Groenmuil, Rosse, Kharvos, Stille), ZINT-DEKKING, bijbel 19_zintuigen.md.'))
c.commit();print('nieuw',n,'vervangen',verv)
