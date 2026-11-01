# Ronde Z15b: "volg de canon" (WRIJ-Z15-6/7): stemming na de Muiterij, Hesta is de vijfde stem. Idempotent; data in z15b/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z15b'); from data import MAP,JAAR,LABEL
RONDE=45;TAG='Z15b';D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z15b.db'): shutil.copy('canon.db','canon_backup_Z15b.db')
c=sqlite3.connect(DB); S={'toegevoegd':0,'vervangen':[],'aangevuld':[]}
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
CAT=c.execute("select categorie from canon where code='ROMANCE-SKELET-Z10-10'").fetchone()[0]
def put(code,cat,ond,feit,status,ver,jaar,intens=None,weet=None,functie='VERH',reden=None):
  feit=feit if 'Veiligheidslabel' in feit else feit+LABEL
  r=(cat,ond,feit,status,reden or f'Ronde {TAG} {D}: volg de canon (besluit Rogier)',ver,RONDE,code,ver,jaar,tp(jaar),intens,weet,functie,'geen')
  if c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('update canon set categorie=?,onderwerp=?,feit=?,status=?,reden=?,hangt_samen_met=?,ronde=?,verwijst_naar=?,jaar=?,tijdperk=?,intensiteit=?,weet=?,functie=?,techniek=? where code=?',r[:7]+r[8:]+(code,))
  else:
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',r); S['toegevoegd']+=1
def vervang(oud,nieuw):
  c.execute("update canon set status='voorlopig, vervangen', reden=coalesce(reden,'')||? where code=? and status!='voorlopig, vervangen'",(f' [Ronde {TAG}: vervangen door {nieuw}]',oud)); S['vervangen'].append(oud)
def ap(code,txt):
  m='[Z15b]'; f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if not f: S.setdefault('niet_gevonden',[]).append(code); return
  if m not in f[0]: c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code))
  S['aangevuld'].append(code)
# 1 besluiten
put('BESLUIT-Z15b-1','Besluit','Stemming 5-4 na de Muiterij','Gekozen door Rogier ("volg de canon"): de stemming 5 tegen 4 valt NA de Koude Muiterij, in -1238 in de eerste nederzetting (ORIGIN-4). Ysa wint met de doden als bewijs dat machines muiten (BESLUIT-V5-ysa). In beatplan 03 zijn Hesta\'s ruil en de stemming beats 19 en 20. Lost WRIJ-Z15-6 op. Keuze van Rogier, 2026-10-31.','vastgesteld','ORIGIN-4;BESLUIT-V5-ysa;ROMANCE-Z15b-ysa-beat-20;WRIJ-Z15-6',-1238,functie='META',weet='Orde: nee. Volk: nee. Lezer: ja.')
put('BESLUIT-Z15b-2','Besluit','Hesta is de vijfde stem','Gekozen door Rogier ("volg de canon"): Hesta Kael is zelf de beslissende vijfde stem. De nacht vóór de stemming slapen Corran en Hesta samen (beiden volwassen en instemmend) en spreken af tegen Ysa te stemmen; Thalen ziet hen vanuit de baan (ORIGIN-WAAROM-6). Op het laatste moment verraadt Hesta Corran, in ruil voor het beheer van de laatste machines; Corran stemt tegen en wordt verbannen naar de bergen (ORIGIN-WAAROM-7). Corran kantelt nergens. Lost WRIJ-Z15-7 op. Keuze van Rogier, 2026-10-31.','vastgesteld','ORIGIN-WAAROM-6;ORIGIN-WAAROM-7;YSA-Z15b-6;ROMANCE-Z15b-ysa-beat-18;ROMANCE-Z15b-ysa-beat-19;WRIJ-Z15-7',-1238,functie='META',weet='Orde: nee. Volk: nee. Lezer: ja.')
# 2 beats opnieuw
txt=open('verhalen/beatplan_03_ysa.md').read(); beats=[]
for m in re.finditer(r'^\| (\d+) \| \*\*(.+?)\*\*(.*?)\| (.+?) \| (.+?) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d) \| (\d+) \|\s*$',txt,re.M):
  n=int(m.group(1)); beats.append(n); jaar=JAAR.get(n,-1240)
  E,R,H,Sp,A,Ag=m.group(6,7,8,9,10,11)
  weet=('Lezer: Ysa\'s bevel (sinds beat 8). ' if n>=8 else 'Lezer: Ysa\'s motief. ')+'Thalen: '+('weet het bevel (sinds 13)' if n>=13 else 'weet niets')+(' en van Hesta en Corran (sinds 18)' if n>=18 else '')+'. Ysa: denkt dat niemand het weet.'
  put(f'ROMANCE-Z15b-ysa-beat-{n:02d}',CAT,f'Ysa-beat {n}: {m.group(2).strip(" .")}',f'Beat {n} van "Ysa\'s verloren liefde" (versie Z15b). {(m.group(2)+m.group(3)).replace("**","").strip()} POV/plek: {m.group(4).strip()}. Duwt: {m.group(5).strip()}. Genres 0-3: erotiek {E}, romantiek {R}, horror {H}, spanning {Sp}, actie {A}, angst {Ag}.','voorlopig','ROMANCE-Z15b-ysa-beatplan;BESLUIT-Z15b-1;BESLUIT-Z15b-2',jaar,int(m.group(12)),weet,'VERH;LUST' if int(E)>=2 else 'VERH')
S['beats']=len(beats); assert len(beats)==23
for o,nw in MAP.items(): vervang(f'ROMANCE-Z15-ysa-beat-{o:02d}',f'ROMANCE-Z15b-ysa-beat-{nw:02d}')
put('ROMANCE-Z15b-ysa-beatplan',CAT,'Ysa\'s verloren liefde (beatplan 03, versie Z15b)','Romance/tragedie, fase 0 Voortijd, -1240 (Muiterij) en -1238 (stemming), zaaischip Ysa en de landingsvlakte; ca. 9900 woorden, 7 hoofdstukken plus proloog, twee tussenstukken en epiloog, 23 beats (ROMANCE-Z15b-ysa-beat-01..23). Raamvertelling: Thalen alleen in de baan. Logline: zes dagen voor de landing beveelt Ysa Maren (30) de Rekenaar in stilte een derde te rantsoeneren; haar geliefde Thalen Orr (34) ziet het bevel, zwijgt en blijft in de baan met het bewijs. Twee jaar later wint Ysa de stemming 5-4 met de doden als bewijs; Hesta Kael is de vijfde stem en verraadt haar minnaar Corran, wat Thalen zag en verzwijgt. Motoren: klok, geheim (twee keer zwijgen), stemming na de Muiterij, de liefde zelf. Twee toppen: Muiterij (10-13) en stemming (20). Erotiek: beat 5 volledig, beat 15 donker, beat 18 kort buiten beeld; alle volwassen en instemmend. Thema: liefde kost iets in Velmara. Bestand: verhalen/beatplan_03_ysa.md. Vervangt ROMANCE-Z15-ysa-beatplan.','voorlopig','ROMANCE-SKELET-Z10-10;ROMANCE-Z10-23;PER-v4-ysa-maren;PER-v4-thalen-orr;PER-v4-hesta-kael;BESLUIT-Z15b-1;BESLUIT-Z15b-2',-1240,9,'Volk: legende ("koude gekte"). Orde: verzwijgt. Lezer: alles.')
vervang('ROMANCE-Z15-ysa-beatplan','ROMANCE-Z15b-ysa-beatplan')
put('YSA-Z15b-6',CAT,"Hesta's ruil (eigen stem)",'Bij zonsopgang na haar nacht met Corran biedt Hesta Kael Ysa haar eigen stem, in ruil voor het beheer van de laatste machines na de landing (volgt ORIGIN-WAAROM-7). Ysa zegt ja en ziet zichzelf in Hesta. Nieuw bedacht in beatplan 03 (de scène van de ruil); voorstel, wacht op goedkeuring van Rogier. Vervangt YSA-Z15-6.','voorlopig','ROMANCE-Z15b-ysa-beatplan;PER-v4-hesta-kael;ORIGIN-WAAROM-7;BESLUIT-Z15b-2',-1238)
vervang('YSA-Z15-6','YSA-Z15b-6')
put('YSA-Z15b-13',CAT,'Thalen ziet door de ogen van een lander','Thalen ziet Corran en Hesta de nacht vóór de stemming vanuit de baan, door de ogen (camera\'s) van een lander in de nederzetting, en hoort hun afspraak. Zo past ORIGIN-WAAROM-6 ("Thalen ziet hen") bij Thalen die in de baan blijft. Hij luistert ook de stemming mee over de lijn. Nieuw bedacht in Z15b; voorstel.','voorlopig','ORIGIN-WAAROM-6;ROMANCE-Z15b-ysa-beat-18;BESLUIT-Z15b-2',-1238)
put('YSA-Z15b-14',CAT,'De raad wil bewijs','In de raad (beat 4) gelooft niemand Ysa\'s cijfers; zonder bewijs dat machines muiten komt er geen stemming. Dat is haar tweede motief voor het bevel (sluit aan bij BESLUIT-V5-ysa en YSA-Z15-7). Nieuw bedacht in Z15b; voorstel.','voorlopig','BESLUIT-V5-ysa;YSA-Z15-7;ROMANCE-Z15b-ysa-beat-04',-1240)
put('HAAK-Z15b-4','Haak','Haak Ysa-verhaal: Na het verraad','Hesta\'s ruil (haar eigen stem voor het machinebeheer, BESLUIT-Z15b-2), Corrans verbanning naar de bergen en haar omweg om de sleutel zijn de oorsprong van "Na het verraad": wat de veiligheidsdienst na de landing met de machines deed, en de wrok van Corrans volgelingen (Dhurn).','voorlopig','ROMANCE-Z15b-ysa-beatplan;PER-v4-hesta-kael;PER-v4-corran-velt;ORIGIN-WAAROM-7',-1238)
vervang('HAAK-Z15-4','HAAK-Z15b-4')
# 3 verwijzingen in levende rijen naar nieuwe beatcodes
def remap(s):
  if not s: return s
  s=re.sub(r'ROMANCE-Z15-ysa-beat-(\d\d)',lambda m:f'ROMANCE-Z15b-ysa-beat-{MAP[int(m.group(1))]:02d}',s)
  return s.replace('ROMANCE-Z15-ysa-beatplan','ROMANCE-Z15b-ysa-beatplan').replace('YSA-Z15-6;','YSA-Z15b-6;').replace('HAAK-Z15-4','HAAK-Z15b-4')
S['verwijzing_bijgewerkt']=[]
for code,h,v in c.execute("select code,hangt_samen_met,verwijst_naar from canon where status!='voorlopig, vervangen' and (hangt_samen_met like '%ROMANCE-Z15-ysa-%' or verwijst_naar like '%ROMANCE-Z15-ysa-%')").fetchall():
  c.execute('update canon set hangt_samen_met=?,verwijst_naar=? where code=?',(remap(h),remap(v),code)); S['verwijzing_bijgewerkt'].append(code)
# 4 notities bij rijen die beatnummers of de oude volgorde noemen
ap('BESLUIT-Z15-5','Na Z15b heet het gevecht om de kern beat 12 (was 14).')
ap('BESLUIT-Z15-3','Na Z15b: het motief komt in beat 2-4; de breuk in beat 14 (was 16).')
ap('BESLUIT-Z15-4','Na Z15b: de donkere scène is beat 15 (was 17).')
ap('BESLUIT-Z15-6','Na Z15b: de sprong naar de scherf is beat 23 (was 22).')
ap('YSA-Z15-12','Corran vecht mee om de kern (beat 12); bij de stemming stemt hij tegen en wordt verbannen (BESLUIT-Z15b-2).')
ap('PER-v4-hesta-kael','In het Ysa-verhaal is zij de vijfde stem en verraadt Corran na hun nacht (BESLUIT-Z15b-2, YSA-Z15b-6).')
ap('PER-v4-corran-velt','In het Ysa-verhaal vecht hij met Thalen om de kern, rekent op Hesta en wordt na de stemming verbannen (BESLUIT-Z15b-2).')
ap('TOESTAND-Z15-PER-v4-thalen-orr-6','De scherf-scène is nu beat 23 (ROMANCE-Z15b-ysa-beat-23).')
ap('VERHAALTIJD-Z15-ysa','Na Z15b: kern -1240 (Muiterij) en -1238 (stemming, BESLUIT-Z15b-1); beatplan ROMANCE-Z15b-ysa-beatplan.')
ap('ORIGIN-WAAROM-6','Thalen ziet hen vanuit de baan, door de ogen van een lander (YSA-Z15b-13, beat 18).')
# 5 wrijvingen
for w,b in (('WRIJ-Z15-6','BESLUIT-Z15b-1'),('WRIJ-Z15-7','BESLUIT-Z15b-2')):
  c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code=? and beschrijving not like '%[Z15b]%'",(f' [Z15b] Opgelost: besluit Rogier "volg de canon" (vastgesteld, {b}); beatplan en beatrijen aangepast.',w))
c.execute("delete from wrijving where code like 'WRIJ-Z15b-%'")
c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",('Hoe ziet Thalen Hesta en Corran vanuit de baan','ORIGIN-WAAROM-6;YSA-Z15b-13','ORIGIN-WAAROM-6 zegt "Thalen ziet hen", maar in -1238 is Thalen al in de baan. Voorstel: hij kijkt door de ogen van een lander (YSA-Z15b-13). Alternatief: hij daalt één keer af voor de stemming. Rogier beslist.','Z15b','open','WRIJ-Z15b-1','ORIGIN-WAAROM-6;YSA-Z15b-13'))
c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",('Lengte hoofdstuk 7 (tweede einde)','ROMANCE-Z15b-ysa-beatplan','Na de romance-climax (16) volgt een lang politiek hoofdstuk (18-21, ca. 2000 woorden). Risico van een tweede einde; opgevangen door beat 18 als spanningsscène. Bij het schrijven toetsen; eventueel beat 21 inkorten.','Z15b','open','WRIJ-Z15b-2','ROMANCE-Z15b-ysa-beatplan'))
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
put('KWALITEIT-Z15b','Besluit','Kwaliteitsrapport ronde Z15b',f'Ronde Z15b ({D}): "volg de canon". BESLUIT-Z15b-1 en -2 vastgesteld; WRIJ-Z15-6 en -7 opgelost. Beatplan 03 herzien naar 23 beats (stemming na de Muiterij, Hesta de vijfde stem, nieuwe beat 18). 22 oude beatrijen, het oude beatplan, YSA-Z15-6 en HAAK-Z15-4 vervangen. Opbouw: gemiddeld ca. 8,5 (continuïteit 6 naar 9). Statussen: {st}.','voorlopig','ROMANCE-Z15b-ysa-beatplan',801,functie='META')
c.execute("delete from logboek where wat like 'Ronde Z15b: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z15b: volg de canon; stemming na de Muiterij, Hesta vijfde stem; beatplan 03 naar 23 beats.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
S['vervangen']=sorted(set(S['vervangen']));S['aangevuld']=sorted(set(S['aangevuld']))
json.dump(S,open('z15b/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
