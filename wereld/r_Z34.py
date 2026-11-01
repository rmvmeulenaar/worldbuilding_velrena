# Ronde Z34: geen sjablonen (Rogier, 2026-11-01: "heel veel herhalingen.. heel veel templates.. en dat gaan we niet doen").
# Idempotent en additief: niets verwijderd, geen tekst van bestaande canonrijen gewijzigd, geen Kern-inhoud gewijzigd, roman niet aangeraakt.
# Gebruik: DB=kopie.db python3 r_Z34.py
import sqlite3,shutil,os,re,json,sys,collections,subprocess
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z34')]
import afgeleid,migreer,herhaling as H
from data import B,P,FAM_VOORSTEL,CATALOGUS_PREF,REGISTER_HOUDEN
DT='2026-11-01';RD='Z34';RN=63;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z34.db'): shutil.copy('canon.db','canon_backup_Z34.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z34.py')).rowcount
LEV="status in('vastgesteld','voorlopig')"
# ---- 1. sjabloonfamilies vastleggen (eenmalig: de nulmeting is de basis; een tweede run voegt niets toe) ----
if not c.execute('select 1 from sjabloon_familie').fetchone():
  R=c.execute(f"select code,feit_schoon,draagkracht,coalesce(ideeenbank,0),draagkracht_handmatig from canon where {LEV}").fetchall();T={r[0]:r for r in R}
  F=H.families([(r[0],r[1]) for r in R])
  ref={n for (n,) in c.execute(f"select v.naar_code from verwijzing v join canon a on a.code=v.van_code where a.{LEV.replace('status','status')} and coalesce(a.ideeenbank,0)=0")}
  ref|={r[0] for r in c.execute('select bron_code from anker')}|{r[0] for r in c.execute('select per_code from personage')}|{r[0] for r in c.execute('select code from boog')}
  for sig,leden in sorted(F.items(),key=lambda x:-len(x[1])):
    mk=[]
    for code in leden:
      _,ft,dk,idee,hand=T[code];pf=re.split(r'[-_]',code)[0]
      if dk=='Kern': m='kern (niet aanraken)'
      elif idee: m='al ideeenbank'
      elif hand: m='handmatig (niet aanraken)'
      elif (pf in CATALOGUS_PREF or sig=='O:Archetype, geen vaste persoon.') and code not in ref: m='ideeenbank'
      elif dk=='Kleur': m='kleur'
      else: m='structuur-voorstel'
      mk.append(m);S['lid']+=c.execute('insert or ignore into sjabloon_lid(sig,code,markering) values(?,?,?)',(sig,code,m)).rowcount
    fm=collections.Counter(mk).most_common(1)[0][0]
    pref=','.join(f'{k}:{v}' for k,v in collections.Counter(re.split(r'[-_]',x)[0] for x in leden).most_common(4))
    vb=re.sub(r'\s+',' ',(T[leden[0]][1] or ''))[:200]
    S['familie']+=c.execute('insert or ignore into sjabloon_familie(sig,grootte,prefixen,markering,voorstel,voorbeeld) values(?,?,?,?,?,?)',(sig,len(leden),pref,fm,FAM_VOORSTEL.get(sig),vb)).rowcount
  wijz('SJABLOON','toegevoegd','sjabloon_familie',None,f"{S['familie']} families, {S['lid']} leden")
nidee=c.execute("select count(*) from sjabloon_lid where markering='ideeenbank'").fetchone()[0]
# ---- 2. regel, handleiding, besluiten ----
REG=[('R-sjabloon_nieuw','verhaal',"Geen sjablonen: rijen vanaf ronde Z34 (ronde>=63) vormen onderling geen sjabloonfamilie (>=3 met dezelfde signatuur) en zijn geen bijna-kopie (Jaccard woord-3-grepen >= 0,5) van een andere levende rij.",'py:sjabloon_nieuw','BESLUIT-Z34-1; HANDL-Z34-1','Rogier (2026-11-01)','actief','fout'),
('R-herhaling_categorie','verhaal',"Signaal: meer dan 35% van de levende canonrijen (buiten de ideeënbank) van een categorie (n>=10) zit in een sjabloonfamilie (>=5 rijen met dezelfde label- of openingssignatuur).",'py:herhaling_categorie','BESLUIT-Z34-1; z34/herhaling.py','Rogier (2026-11-01)','actief','signaal'),
('R-boog_uniek','verhaal',"Geen twee bogen met dezelfde vorm, verteller, toon, tempo of afloop.",'py:boog_uniek','BESLUIT-Z34-1; BESLUIT-Z34-2','Rogier (2026-11-01)','actief','fout'),
('R-personage_fout_uniek','verhaal',"Geen twee personages met dezelfde soort eigen fout.",'py:personage_fout_uniek','BESLUIT-Z34-1; BESLUIT-Z34-4','Rogier (2026-11-01)','actief','fout')]
for r in REG:
  n=c.execute('insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)',r).rowcount
  if n: S['regel']+=1;wijz(r[0],'toegevoegd','regel',None,RD)
HANDL=('HANDL-Z34-1','Geen sjablonen',"Vaste regel van Rogier (BESLUIT-Z34-1): elke boog, elk personage en elke uitwerking krijgt een eigen vorm. Wie een rij schrijft, kopieert geen opening, geen rij kopjes en geen standaardzin van een andere rij. Herhaling in nieuwe rijen is een fout (regel R-sjabloon_nieuw, toets.py faalt). Velden horen in kolommen, niet als 'Label: ... Label: ...' in de tekst. Sjabloonfamilies staan in de tabel sjabloon_familie (view v_sjabloon); gegenereerde catalogi zijn als ideeënbank gemarkeerd (sjabloon_lid). Meten: python3 z34/meet.py canon.db uit.json.")
if c.execute('insert or ignore into handleiding(code,onderwerp,tekst) values(?,?,?)',HANDL).rowcount: S['handleiding']+=1;wijz(HANDL[0],'toegevoegd','handleiding',None,RD)
REDEN="Rogier, 2026-11-01: \"heel veel templates.. en dat gaan we niet doen\" (opdracht ronde Z34)."
imp={}
for code in B:
  out=subprocess.run([sys.executable,'vraag.py','impact',code],capture_output=True,text=True,env={**os.environ,'DB':DB}).stdout
  m=re.search(r'totaal (\d+) rijen',out);imp[code]=int(m.group(1)) if m else 0
gewijzigde_as=[k for k,v in B.items() if v.get('extra')]
CANON=[
('BESLUIT-Z34-1','Besluit','Geen sjablonen (vaste regel)',"Vanaf nu geen sjablonen meer in Velmara. Een boog, een personage of een uitwerking die dezelfde vorm heeft als een andere, is fout, ook als de inhoud anders is. Wat al gegenereerd is als catalogus, gaat naar de ideeënbank; wat canon-gewicht draagt, krijgt per familie een eigen herschrijfvoorstel (tabel sjabloon_familie). De toets bewaakt het voortaan: R-sjabloon_nieuw, R-boog_uniek, R-personage_fout_uniek, met R-herhaling_categorie als signaal.",'vastgesteld','HANDL-Z34-1;BESLUIT-Z34-2;BESLUIT-Z34-4','Structuur'),
('BESLUIT-Z34-2','Besluit','Dertig bogen, dertig vormen',"De voorstellen uit Z33 zijn doorgevoerd en de bogen zonder voorstel kregen er een: elke boog heeft nu een andere verteller, vorm, tempo, toon en afloop (tabel boog, kolommen verteller en tempo zijn nieuw). Boek 0 en boek 1 blijven zoals ze zijn. Op deze assen wijkt de boog af van de oorspronkelijke VERHAAL-rij, en dan gaat de boog voor: "+'; '.join(f"{k} ({', '.join(f'{a}={b}' for a,b in B[k]['extra'].items())})" for k in gewijzigde_as)+". Rijen die op die bogen leunen (vraag.py impact): "+', '.join(f'{k} {imp[k]}' for k in gewijzigde_as)+"; die zijn niet herschreven, zie WRIJ-Z34-2.",'vastgesteld','BESLUIT-Z34-1;BESLUIT-Z34-3;WRIJ-Z34-2;'+';'.join(B),'Structuur'),
('BESLUIT-Z34-3','Besluit','Register en vervalsing: nog vier bogen',"Het motief register/vervalsing blijft alleen waar het iets begint of beëindigt. "+' '.join(f'{k}: {v}' for k,v in REGISTER_HOUDEN.items())+" De andere dertien register-bogen kregen elk een eigen motief, en geen twee hetzelfde.",'vastgesteld','BESLUIT-Z32-5;BESLUIT-Z34-2;'+';'.join(k for k in REGISTER_HOUDEN if not k.startswith('BOOG-')),'Structuur'),
('BESLUIT-Z34-4','Besluit','Achttien fouten van achttien soorten',"De achttien profielen zijn nu personages: elk heeft een eigen fout, en geen soort fout komt twee keer voor in de tabel personage. Drie voorstellen uit Z33 leken te veel op elkaar (Corran, Vaelorn en Thalen zwegen alle drie), dus Corran bewondert nu de vijand en Vaelorn verzint een mooiere mythe. Ida vervalste in Z33 haar meting, en dat was het register-motief in een andere jas; nu meet ze gewoon niet meer. Teo stelt uit. Hij blijft strikt niet-seksueel.",'vastgesteld','BESLUIT-Z34-1;WRIJ-Z34-1;'+';'.join(r[0] for r in c.execute('select per_code from personage where code in (%s) order by id'%','.join('?'*len(P)),list(P)) if r[0] and c.execute('select 1 from canon where code=?',(r[0],)).fetchone()),'Structuur'),
]
for k,v in B.items():
  slug=k.replace('VERHAAL-','').replace('-Z32','')
  CANON.append((f'VERHAAL-Z34-{slug}','Verhaal',f"Uitwerking {slug}: {v['vorm']}",v['tekst'],'vastgesteld',f'{k};BESLUIT-Z34-2',None))
WRIJ=[('WRIJ-Z34-1','Teo stelt uit; raakt Liora (Kern)','PERS-teo; BESLUIT-Z32-9 (Kern); PER-liora-profiel-Z32 (Kern)',"Teo's fout (uitstel) is nieuw en past bij BESLUIT-Z32-9: Liora besluit voor hem omdat hij zijn gave verzwijgt. De Kern-rij is niet gewijzigd. Rogier moet nog bevestigen dat Teo's zwijgen Liora's schuld niet kleiner maakt.",'BESLUIT-Z34-4;BESLUIT-Z32-9;PER-teo-Z32','raakvlak Kern'),
('WRIJ-Z34-2','Leunende rijen volgen de oude assen nog',', '.join(gewijzigde_as),"Bij "+str(len(gewijzigde_as))+" bogen is een as omgezet, bijvoorbeeld van wel naar geen erotische sleutelscène. Op die bogen leunen samen "+str(sum(imp[k] for k in gewijzigde_as))+" rijen tot twee niveaus diep (vraag.py impact): beats, zintuigrijen en crosslinks. Die zijn niet herschreven en kunnen de oude scène nog veronderstellen. Dat moet in een volgende ronde rij voor rij worden nagelezen.",'BESLUIT-Z34-2','structuur'),
('WRIJ-Z34-3','Sjabloonfamilies met canon-gewicht zonder voorstel','sjabloon_familie (markering structuur-voorstel, voorstel leeg)',"Families met vooral Structuur-rijen waarvoor nog geen eigen herschrijfvoorstel bestaat. Die staan in v_sjabloon, en elke familie moet een andere vorm krijgen dan de andere.",'BESLUIT-Z34-1','structuur')]
for code,cat,ond,feit,st,verw,hand in CANON:
  if not c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,draagkracht_handmatig) values(?,?,?,?,?,?,?,?,?,?)',(cat,ond,feit,st,REDEN,verw,RN,code,verw,hand))
    S['canon']+=1;wijz(code,'toegevoegd','canon',None,st)
for code,titel,delen,besch,verw,typ in WRIJ:
  if not c.execute('select 1 from wrijving where code=?',(code,)).fetchone():
    c.execute('insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)',(titel,delen,besch,typ,'open',code,verw));S['wrijving']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
# ---- 3. boog en personage ----
for k,v in B.items():
  nw={'terugkerend_motief':v['motief'],'verteller':v['verteller'],'vorm':v['vorm'],'tempo':v['tempo'],'toon':v['toon'],'afloop':v['afloop'],'voorstel_status':'vastgesteld (BESLUIT-Z34-2)',**v.get('extra',{})}
  oud=dict(zip(nw,c.execute(f"select {','.join(nw)} from boog where code=?",(k,)).fetchone()))
  for f,x in nw.items():
    if oud[f]!=x: c.execute(f'update boog set {f}=? where code=?',(x,k));wijz(k,'gewijzigd','boog.'+f,oud[f],x);S['boog_veld']+=1
for k,(sf,ef,wb,zb,dd) in P.items():
  nw={'soort_fout':sf,'eigen_fout':ef,'wie_betaalt':wb,'zelfbedrog':zb,'daarna_doet':dd,'status':'personage (BESLUIT-Z34-4)','voorstel_status':'vastgesteld (BESLUIT-Z34-4)'}
  oud=dict(zip(nw,c.execute(f"select {','.join(nw)} from personage where code=?",(k,)).fetchone()))
  for f,x in nw.items():
    if oud[f]!=x: c.execute(f'update personage set {f}=? where code=?',(x,k));wijz(k,'gewijzigd','personage.'+f,oud[f],x);S['personage_veld']+=1
if not c.execute("select 1 from logboek where wat like 'Ronde Z34%'").fetchone():
  i=c.execute('select max(id) from logboek').fetchone()[0]+1
  c.execute('insert into logboek(id,datum,wat) values(?,?,?)',(i,DT,f'Ronde Z34: geen sjablonen. Herhaling gemeten (z34/meet.py), sjabloonfamilies vastgelegd (sjabloon_familie/sjabloon_lid, v_sjabloon), {nidee} catalogusrijen als ideeënbank gemarkeerd zonder tekstwijziging, 4 regels (R-sjabloon_nieuw, R-herhaling_categorie, R-boog_uniek, R-personage_fout_uniek), bogen en personages elk een eigen vorm/fout (BESLUIT-Z34-1..4, VERHAAL-Z34-*). Niets verwijderd; Kern en roman niet aangeraakt.'));S['logboek']+=1
c.commit();afgeleid.bouw(c);c.commit()
print(json.dumps(dict(S),ensure_ascii=False),'ideeenbank-leden:',nidee)
