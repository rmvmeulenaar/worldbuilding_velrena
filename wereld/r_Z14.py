# Ronde Z14: restpunten Z13 oplossen en haken met de hand herschrijven (idempotent); data in z14/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z14')
H={}
for m in 'abcd': H.update(__import__('haken_'+m).H)
RONDE=43;TAG='Z14';D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z14.db'): shutil.copy('canon.db','canon_backup_Z14.db')
c=sqlite3.connect(DB)
A="status not like '%vervangen%' and status!='vervallen'"
S={}
def ap(code,mark,txt,jaar=None,tijdperk=None):
  r=c.execute("select feit from canon where code=?",(code,)).fetchone()
  if not r: S.setdefault('niet_gevonden',[]).append(code); return False
  if mark in (r[0] or ''): 
    if jaar is not None: c.execute("update canon set jaar=?,tijdperk=coalesce(?,tijdperk) where code=?",(jaar,tijdperk,code))
    return True
  c.execute("update canon set feit=feit||?, reden=coalesce(reden,'')||? where code=?",(' '+mark+' '+txt,f' [Ronde {TAG} {D}: {mark.strip("[]")}]',code))
  if jaar is not None: c.execute("update canon set jaar=?,tijdperk=coalesce(?,tijdperk) where code=?",(jaar,tijdperk,code))
  return True
def tp(j):
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
# ---------- 1 dood maar later actief ----------
DOOD=[
 ('OORLOG-Z9-31','fout in de rij (naam als titel)','[Z14 dood-actief]','"Tamsin" is hier een titel: de Tharn noemen een menselijke aanvoerster naar Tamsin Dijkvrouw (overleden ca. -520, PER-tamsin). In 120 leidt dus een latere mens hen; Tamsin zelf leeft alleen voort in hun liederen.',None),
 ('TOESTAND-Z11-PER-orric-3','fout in jaar (versteend, niet gestorven)','[Z14 correctie]','Orric sterft niet ca. -110 maar versteent zichzelf ca. -95 in de kroonstrijd (OORLOG-Z9-6, LICH-orric-steen); zijn versteende lichaam ligt in de kerkers van Saelith en zijn standbeeld "spreekt" soms. De aanname levensduur 70 vervalt.',-95),
 ('TOESTAND-Z11-PER-varnath-3','fout in jaar','[Z14 correctie]','Varnath sterft in jaar -6, vermoord door zijn gebonden vrouwen na negen dagen Grijswortel (GEB-r10-varnath-dood, VERHAAL-fase3-b). De aanname "overleden ca. -50" vervalt. Hij werd dus ca. 114: sterke vonk rekt het leven (5x genezing, MAGIE-kracht-duur); dat is een aanname en blijft voorlopig.',-6),
 ('ACTIE-Z9-13','fout in jaar (mediaan-datering Z13)','[Z14 correctie]','Gedateerd op ca. -75 (fase 2 Vonk), binnen het leven van Tesk de Melkknecht (ca. -110 tot -40): dit zijn de vroege melkstallen van de vonkkoningen rond de zaadkruiken (GEB-r10-zaadkruiken), niet de grote melkstallen van 350-400 (GEB-r10-melkstallen). De Z13-datering 150 vervalt.',-75),
 ('ACTIE-Z9-12','geen fout (oorsprong)','[Z14 dood-actief]','De verwijzing naar Ilwa Klifvleugel (overleden ca. -20) is een verwijzing naar de stichteres van het Skerra-klif; de jagers in 370 zijn haar nazaten. Geen fout.',None),
 ('TOESTAND-Z11-PER-ysara-3','fout in jaar + echo','[Z14 correctie]','Ysara sterft niet ca. 39 maar in jaar 0 in Ves-Anath, als eerste Dochter in de steen opgenomen (BESLUIT-Z12-wortelstem). Haar stem leeft voort in de Wortel; vermeldingen in 801 (HAAK-PER-romance, HAAK-PER-thriller) gaan over die stem of over haar geschiedenis, geen fout.',0),
 ('HAAK-PER-romance','geen fout (historisch)','[Z14 dood-actief]','Ysara en Mira staan hier onder "Historisch": hun lijn speelt in jaar -1; de rij is een overzicht in 801, geen bewering dat zij in 801 leven.',None),
 ('HAAK-PER-thriller','geen fout (geest/echo)','[Z14 dood-actief]','"De stem in de Wortel (Ysara?)" is beslist: de stem heet Ysara en Thalen Orr is erin opgegaan (BESLUIT-Z12-wortelstem). Ysara zelf stierf in jaar 0.',None),
 ('HELD-SKELET-Z10-6','naamgenoot','[Z14 dood-actief]','Deze Hethra (45 in 720, geboren ca. 675) is Hethra de Barstenwachter, een naamgenote van Hethra Brakmoeder (PER-hethra, fase 3), naar wie de Sael-mor hun dochters vernoemen. Zelfde persoon als in HELD-Z10-50.',None),
 ('HELD-Z10-50','naamgenoot','[Z14 dood-actief]','De barstenwachter van fase 6/7 is Hethra de Barstenwachter (zie HELD-SKELET-Z10-6), niet Hethra Brakmoeder.',None),
 ('BESLUIT-Z12-8','geen fout (besluit noemt historische persoon)','[Z14 dood-actief]','Zarah de Pestmoeder leefde ca. 310-380; het besluit van 801 noemt haar als historisch bewijs, niet als levend personage.',None),
 ('PLEKTOESTAND-Z11-registerkraai-2','geen fout (opname/echo)','[Z14 dood-actief]','"Hesta\'s stem" is een opname uit de kluizen die de kraaien in 205 oppikten (BESLUIT-Z7-KRAAI); Hesta Kael zelf leefde ca. -1270 tot -1200.',None),
 ('PLEKTOESTAND-Z11-registerkraai-1','geen fout (opname/echo)','[Z14 dood-actief]','In 205 pikken de kraaien de opname met Hesta\'s stem op; Hesta Kael zelf is dan al lang dood.',None),
 ('TOESTAND-Z11-PER-aelthir-schurk-ileth-V5-3','fout in levensduur (Aelthir)','[Z14 correctie]','Ileth is Aelthir en leeft nog in 801, ca. 860 jaar oud, binnen de Aelthir-levensduur van ca. 900 jaar (PER-aelthir-schurk-ileth-V5). De aanname "overleden ca. 10" (levensduur 70) vervalt.',801),
]
dood=[]
for code,besl,mark,txt,j in DOOD:
  ap(code,mark,txt,j,tp(j) if j is not None else None); dood.append((code,besl))
c.execute("update canon set feit=replace(feit,'Historisch: overleden ca. -110','Historisch: versteend ca. -95') where code='TOESTAND-Z11-PER-orric-3'")
S['1_dood_actief']=dict(gevallen=13,rijen_aangepast=len(dood),besluiten=dood)
# andere langlevenden met automatische levensduur 70
LL=[]
for code,f in c.execute(f"select code,feit from canon where {A} and code like 'TOESTAND-Z11-PER-%-3' and feit like 'Historisch: overleden ca.%'").fetchall():
  if '[Z14 correctie]' in f: continue
  per=re.match(r'TOESTAND-Z11-(.+)-3$',code).group(1)
  pf=(c.execute("select feit from canon where code=?",(per,)).fetchone() or [''])[0] or ''
  if re.search(r'Volk: (aelthir|orrim)',pf,re.I): LL.append(code)
for code in LL: ap(code,'[Z14 levensduur]','Let op: dit volk leeft eeuwen (Aelthir ca. 900 jaar; Orrim zeer lang); het overlijdensjaar met levensduur 70 is waarschijnlijk te vroeg. Nog niet per persoon herberekend.')
LLTXT=' [Z14 levensduur] Let op: dit volk leeft eeuwen (Aelthir ca. 900 jaar; Orrim zeer lang); het overlijdensjaar met levensduur 70 is waarschijnlijk te vroeg. Nog niet per persoon herberekend.'
c.execute("update canon set feit=replace(feit,?,''), reden=replace(reden,' [Ronde Z14 2026-10-31: Z14 levensduur]','') where feit like '%[Z14 correctie]%[Z14 levensduur]%'",(LLTXT,))
S['1_langlevend_gemarkeerd']=LL
# ---------- 2 twee plekken ----------
TP=[('TOESTAND-Z11-sef-5','Volgorde binnen de Oogstmaan: dag 1-4 (verhaal 1, VERHAALTIJD-Z11-6): Brakhaven, dan de slikgang, aan het eind Nevelveen. Dit is een reis, niet twee plekken tegelijk.'),
 ('TOESTAND-Z11-sef-6','Volgorde binnen de Oogstmaan: vanaf dag 5, na verhaal 1: Nevelveen. Volgt op TOESTAND-Z11-sef-5.'),
 ('TOESTAND-Z11-liora-5','Volgorde binnen de Oogstmaan: dag 1-4 (verhaal 1): Brakhaven, Zoutkelders, slikgang. Reis, geen dubbele plek.'),
 ('TOESTAND-Z11-liora-6','Volgorde binnen de Oogstmaan: vanaf dag 5: Nevelveen, op weg naar Saelith. Volgt op TOESTAND-Z11-liora-5.'),
 ('TOESTAND-Z11-zegelbinder-2','Volgorde binnen de Oogstmaan: dag 3 van verhaal 1, in de Zoutkelders onder Brakhaven (zelfde stad, onder de grond).'),
 ('TOESTAND-Z11-zegelbinder-3','Volgorde binnen de Oogstmaan: dag 4 en daarna, in Brakhaven boven de grond: hij leeft, leeg en zonder gave voor een maan (besluit Z11).')]
for code,t in TP: ap(code,'[Z14 tijdlijn]',t)
S['2_twee_plekken']=dict(opgelost=3,rijen=len(TP))
# ---------- 3 verhoudingen ----------
VH=[('GES-herkomst-gave','bewuste uitzondering: andere grootheid','"1 op de 20" en "1 op 2000" zijn de kans dat een zoon de gave erft, geen geslachtsverhouding bij de geboorte; ze staan los van 1 op 100 (REGEL-verhouding-Z12) en kloppen met BESLUIT-Z6-VRAAG-006.'),
 ('DEG-askoude-Z6','bewuste uitzondering: andere grootheid','"1 op 400" is het deel van de Leegtezieken dat askoud wordt (BESLUIT-Z6-WRIJ-065), geen geboorteverhouding.'),
 ('REGEL-verhouding-Z12','geen afwijking (valse melding)','"1 op 300" staat hier alleen als vervallen alternatief ("1 op 300 vervalt"); de regel is 1 op 100, lek 1 op 60, Kharvos 1 op 3.')]
for code,b,t in VH: ap(code,'[Z14 verhouding]',t)
# breder: elke actieve rij met 1 op 300/1 op 90 als geboorteverhouding
ex=[]
for code,f in c.execute(f"select code,feit from canon where {A} and (feit like '%1 op 300%' or feit like '%1 op 90 %') and code not in ('REGEL-verhouding-Z12') and code not like 'BESLUIT-%'").fetchall():
  if re.search(r'1 op 300(?! vervalt)',f) and '[Z14 verhouding]' not in f:
    ex.append(code); ap(code,'[Z14 verhouding]','1 op 300 is vervallen; de regel is 1 op 100 (REGEL-verhouding-Z12, BESLUIT-Z6-VRAAG-001).')
S['3_verhoudingen']=dict(nagelopen=[v[0] for v in VH]+ex,besluiten=[(v[0],v[1]) for v in VH])
# ---------- 4 jaren na 801 ----------
TK=[('LIJN-voorinstemming-Z6','voorspelling/skelet','"806" is een toekomstskelet: het Lichtconvent van 806 ligt na het heden (801) en na boek 1; het is een geplande uitkomst (BESLUIT-Z6-WRIJ-077), geen vastgestelde geschiedenis.'),
 ('BESLUIT-Z6-WRIJ-077','voorspelling/skelet','Het Lichtconvent van 806 ligt na het heden (801): toekomstskelet voor latere boeken.'),
 ('BESLUIT-Z6-VRAAG-005','fout in formulering','Lees "sinds 806" als "vanaf 806": dat jaar ligt na het heden (801); in 801 geldt de gelofte nog. Toekomstskelet.'),
 ('BESLUIT-Z11-tijdlijn','voorspelling/skelet','806 (Lichtconvent) is een toekomstskelet na het heden.'),
 ('PER-Z11-bram-kade','plan (voorspelling)','"Wordt in 802 verkocht" is een plan: in 801 staat Bram op de verkooplijst van het Jongenshof voor 802; Liora wil dat voorkomen. Nog niet gebeurd.'),
 ('TOESTAND-Z11-bram-van-de-kade-3','plan (voorspelling)','De verkoop in 802 is gepland, niet voltrokken (zie PER-Z11-bram-kade).'),
 ('NU-conflict-zegelbinding','deadline','"De Lege Dag van 802" is de deadline van de klok: de eerstvolgende Lege Dag na de Oogstmaan van 801.'),
 ('NU-volgende-crisis-Z6','deadline','"De Bloedmaan van 802" is de komende Bloedmaan: een voorspelde klok, geen voltrokken gebeurtenis.')]
for code,b,t in TK: ap(code,'[Z14 toekomst]',t)
fut=[r[0] for r in c.execute(f"select code from canon where {A} and code like 'TOESTAND-Z11-%' and jaar>801")]
for code in fut: ap(code,'[Z14 toekomst]','Vooruitblik na het heden (801): toestand na de verhalen, skelet voor latere boeken; geen vastgestelde canon.')
S['4_toekomst']=dict(besluiten=[(a,b) for a,b,_ in TK],tijdlijn_vooruitblik=fut)
# ---------- 5 haken met de hand ----------
FU={'Besluit':'BESL','Geschiedenis':'GES','Oorlog':'MIL','Held':'HELD','Personage':'PERS'}
hk=0;hcat={}
for code,(zin,haak,fz) in H.items():
  r=c.execute("select feit,categorie,functie from canon where code=?",(code,)).fetchone()
  if not r: continue
  f=r[0]
  m=re.search(r' \[Z1[34] verdieping[^\]]*\] .*?(Crosslinks: .*)$',f,re.S)
  if not m: continue
  oud=f[m.start():]
  fm=re.search(r'Functie: (\S+) —',oud); fc=fm.group(1) if fm else (r[2] or 'WERELD')
  nieuw=f' [Z14 verdieping, per rij geschreven] Zintuig: {zin[0].upper()+zin[1:]}. Haak: {haak} Functie: {fc} — {fz}. {m.group(1)}'
  if f[m.start():]!=nieuw:
    c.execute("update canon set feit=?, reden=coalesce(reden,'')||? where code=?",(f[:m.start()]+nieuw,'' if '[Ronde Z14: haak' in (c.execute('select reden from canon where code=?',(code,)).fetchone()[0] or '') else f' [Ronde {TAG}: haak, zintuig en functie per rij herschreven; de Z13-sjabloonzin is vervangen]',code))
  hk+=1;hcat[r[1]]=hcat.get(r[1],0)+1
rest=c.execute("select count(*) from canon where feit like '%[Z13 verdieping]%'").fetchone()[0]
S['5_haken']=dict(herschreven=hk,per_categorie=dict(sorted(hcat.items(),key=lambda x:-x[1])),nog_sjabloon=rest)
# ---------- 6 aangenomen jaren ----------
KW=[(r'derde weg|vrijgekomen Dochter|gewekte Dochter',None,'na de derde weg: toekomstskelet (na 801)'),
 (r'Varnath',-45,'Varnath-lijn (GEB-r10-varnath-opkomst)'),(r'Hal-Neth|Pestmoeder|Grote Pest',340,'de Pest van 340'),
 (r'Muiterij|Hesta|Ysa Maren|Corran',-1240,'Muiterij op Ysa'),(r'Iresse',300,'Iresse (GEB-r10-iresse-verraad)'),
 (r'Thessaly',135,'Thessaly (fase 5)'),(r'Orric',-150,'Orric (GEB-orric-vonk)'),(r'Offer der Dochters|Ysara en Mira',-1,'het Offer')]
verb=[];blijf={}
for code,cat,f,r in c.execute(f"select code,categorie,feit,reden from canon where {A} and reden like '%geen aanwijzing: heden 801%'").fetchall():
  if '[Z14 datering' in (r or ''): 
    verb.append(code) if 'Z14 datering: jaar' in r or 'toekomstskelet' in r else blijf.__setitem__(cat,blijf.get(cat,0)+1); continue
  hit=None
  for p,j,why in KW:
    if re.search(p,f or ''): hit=(j,why);break
  if hit:
    j,why=hit
    if j is None: c.execute("update canon set tijdperk='na 801 (skelet)', reden=reden||? where code=?",(f' [Z14 datering: {why}; jaar 801 blijft als ondergrens]',code))
    else: c.execute("update canon set jaar=?, tijdperk=?, reden=reden||? where code=?",(j,tp(j),f' [Z14 datering: jaar {j} ({why}); aanname 801 vervalt]',code))
    verb.append(code)
  else:
    c.execute("update canon set reden=reden||? where code=?",(' [Z14 datering gecontroleerd: tijdloze haak of concept zonder aanwijzing in tekst of canon; speelbaar in 801, aanname blijft]',code)); blijf[cat]=blijf.get(cat,0)+1
gb=[]
for code,f,j in c.execute("select code,feit,jaar from canon where code like 'TOESTAND-Z11-%-1' and feit like '%Aanname:%' and feit not like '%Geboren ca. % ([^)]*); de aanname hierboven vervalt%'").fetchall():
  if '[Z13 correctie] Geboren' in f or '[Z14 correctie] Geboren' in f: 
    if '[Z14 correctie] Geboren' in f: gb.append(code)
    continue
  per=re.match(r'TOESTAND-Z11-(.+)-1$',code).group(1)
  x=c.execute('select feit,jaar from canon where code=?',(per,)).fetchone()
  if not x: continue
  pf=x[0] or ''
  m=re.search(r'^(\d{2,3})[ ,]',pf) or re.search(r'\((\d{2})\)',pf)
  if not m: continue
  t2=c.execute("select jaar from canon where code=?",('TOESTAND-Z11-'+per+'-2',)).fetchone()
  pj=x[1] if x[1] is not None else (801 if re.search(r'801|\(nu\)',pf) or per in ('PER-aeron','PER-morvane','PER-khaled','PER-liora-Z6') else (t2[0] if t2 else None))
  if pj is None: continue
  nb=pj-int(m.group(1))
  if nb!=j:
    c.execute("update canon set jaar=?, tijdperk=?, feit=feit||? where code=?",(nb,tp(nb),f' [Z14 correctie] Geboren ca. {nb} (leeftijd {m.group(1)} in {per}, jaar {pj}); de aanname hierboven vervalt.',code)); gb.append(code)
gb_rest=c.execute("select count(*) from canon where code like 'TOESTAND-Z11-%-1' and feit like '%Aanname:%' and feit not like '%correctie] Geboren%'").fetchone()[0]
S['6_jaren']=dict(jaar801_verbeterd=len(verb),jaar801_blijft=blijf,geboorte_verbeterd=len(gb),geboorte_voorbeelden=gb,geboorte_blijft_aanname=gb_rest)
# ---------- wrijvingen ----------
for w,t in (('WRIJ-Z13-3','[Z14: opgelost; 8 rijen met 802/806 beslist als plan, deadline of toekomstskelet, 6 tijdlijnrijen na 801 als vooruitblik gemarkeerd]'),
 ('WRIJ-Z13-4','[Z14: opgelost; alle 13 gevallen gelezen: 5 fouten in jaar of levensduur gecorrigeerd (Orric, Varnath, Ysara, Ileth, ACTIE-Z9-13), 2 naamgenoten (Tamsin als titel, Hethra de Barstenwachter), 6 geen fout (annalen, echo, opname, oorsprong)]'),
 ('WRIJ-Z13-6','[Z14: opgelost; de drie gevallen zijn reizen binnen de Oogstmaan, volgorde per dag vastgelegd]'),
 ('WRIJ-Z13-8','[Z14: opgelost; 1 op 2000 en 1 op 400 zijn andere grootheden (erfkans, askoud-kans), 1 op 300 staat alleen als vervallen alternatief]')):
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' '||? where code=? and beschrijving not like '%[Z14:%'",(t,w))
c.execute("delete from wrijving where code like 'WRIJ-Z14-%'")
NW=[('Twee Varnaths?','PER-varnath;OORLOG-Z9-18;BESLUIT-Z6-WRIJ-052','Varnath Vuurkoning sterft in -6 (GEB-r10-varnath-dood), maar OORLOG-Z9-18 ("De Varnath-opkomst", fase 6) en BESLUIT-Z6-WRIJ-052 ("Varnath liet in 512 de havenwijk van Lisk branden") laten hem in fase 6 optreden. Voorstel: een gaven-generaal in fase 6 nam de naam Varnath aan (Varnath II); niet doorgevoerd, Rogier beslist.','open'),
 ('Levensduur 70 bij langlevende volken','TOESTAND-Z11-PER-aelthir-schurk-ileth-V5-3',f'{len(LL)} automatische overlijdensrijen van Aelthir/Orrim gebruiken levensduur 70; gemarkeerd met [Z14 levensduur], niet per persoon herberekend.','open' if LL else 'opgelost'),
 ('Twee mannen die Bram heten','PER-bram;PER-Z11-bram-kade','Bram-van-de-Hallowynstal (melkman, 30) en Bram van de Kade (zoon van Jorrit, 19) zijn twee personen; in HAAK-PER-romance is "Bram en Dagny" de melkman. Gemarkeerd als naamgenoten.','opgelost')]
for i,(t,b,e,s) in enumerate(NW,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,b,e,'Z14',s,f'WRIJ-Z14-{i}',b))
ap('PER-Z11-bram-kade','[Z14 naamgenoot]','Niet dezelfde als Bram-van-de-Hallowynstal (PER-bram, melkman van 30).')
# ---------- rapport ----------
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
rap=(f"Ronde Z14 ({D}): (1) 13 dood-maar-actief-gevallen gelezen: 5 gecorrigeerd, 2 naamgenoten, 6 geen fout; {len(LL)} langlevende overlijdensrijen gemarkeerd. (2) 3 twee-plekken-gevallen opgelost als reis binnen de Oogstmaan. (3) 3 verhoudingen nagelopen: 2 andere grootheid, 1 valse melding. "
 f"(4) {len(TK)} rijen met 802/806 beslist (plan, deadline of toekomstskelet) en {len(fut)} tijdlijnrijen na 801 als vooruitblik gemarkeerd. (5) {hk} van de 420 Z13-verdiepingen met de hand herschreven (zintuig, haak, functie per rij); nog sjabloon: {rest}. "
 f"(6) {len(verb)} rijen met aangenomen jaar 801 verbeterd, {sum(blijf.values())} blijven aanname (tijdloze haken en concepten); {len(gb)} geboortejaren verbeterd uit leeftijden in de canon, {gb_rest} blijven aanname. Statussen: {st}. "
 "Niet gecontroleerd: de vrije tekst van de 6.000+ overige rijen; levensduur per persoon bij langlevende volken; tijdlijnen zonder maanden; de nieuw geschreven haken zijn niet door Rogier beoordeeld en blijven bij de status van hun rij. Verhalen niet herschreven. Alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; geen seks met wie echt niet kan instemmen.")
for code,ond,feit,st_ in (('KWALITEIT-Z14','Kwaliteitsrapport ronde Z14',rap,'voorlopig'),('BESLUIT-Z14-restpunten','Besluiten ronde Z14 (ingenieur)','Op verzoek van Rogier ("ja doe dat", 2026-10-31) zijn de open restpunten van Z13 per rij gelezen en beslist: zie WRIJ-Z13-3, -4, -6, -8 (nu opgelost) en WRIJ-Z14-*. Correcties staan als [Z14 correctie], beslissingen als [Z14 dood-actief], [Z14 tijdlijn], [Z14 verhouding] en [Z14 toekomst] in de rijen zelf. Geen rij verwijderd.','vastgesteld')):
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): c.execute("update canon set feit=? where code=?",(feit,code))
  else: c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,?,?,?,?,?,?,801,'801 (nu)','META','geen')",(ond,feit,st_,f'Ronde {TAG}: restpunten Z13','KWALITEIT-Z13;BESLUIT-Z13-perfectioneren',RONDE,code,'KWALITEIT-Z13;BESLUIT-Z13-perfectioneren'))
c.execute("delete from logboek where wat like 'Ronde Z14: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f"Ronde Z14: restpunten Z13 opgelost; {hk} haken met de hand herschreven; {len(verb)} jaren en {len(gb)} geboortejaren verbeterd."))
c.commit()
S['status']=st;S['integriteit']=c.execute('pragma integrity_check').fetchone()[0]
json.dump(S,open('z14/stats.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in S.items() if k not in ('1_dood_actief',)},ensure_ascii=False)[:4000])
