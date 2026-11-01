# Ronde Z33: canon-motor als meetlat (Rogier: "het is een benchmark skill", 2026-11-01).
# Idempotent en additief: niets verwijderd, geen canonfeit of Kern-inhoud gewijzigd, roman niet aangeraakt.
# Bouwt: regel, boog, personage, zaadje (Model), ankers uitgebreid, wrijvingen, handleiding; daarna afgeleid (herkomst, relatie, anker_kopie)
# en registreert bevindingen van de NIEUWE regels als bekende bevindingen met een wrijving (baseline). Gebruik: DB=kopie.db python3 r_Z33.py [--geen-baseline]
import sqlite3,shutil,os,re,json,subprocess,sys,tempfile
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z33')]
import afgeleid,migreer
from data import *
DT='2026-11-01';RD='Z33';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z33.db'): shutil.copy('canon.db','canon_backup_Z33.db')
c=sqlite3.connect(DB);migreer.draai(c)
S={'regel':0,'anker':0,'boog':0,'personage':0,'zaadje':0,'wrijving':0,'handleiding':0,'uitzondering':0,'wijziging':0,'logboek':0}
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',oud,nieuw,DT,'r_Z33.py')).rowcount
def ins(t,cols,vals,code,teller):
  n=c.execute(f"insert or ignore into {t}({','.join(cols)}) values({','.join('?'*len(cols))})",vals).rowcount
  if n: S[teller]+=1;wijz(code,'toegevoegd',t,None,'Z33')
codes={r[0] for r in c.execute('select code from canon')}
for r in REGELS: ins('regel',['code','domein','omschrijving','sql_test','bron','goedgekeurd_door','status','niveau'],list(r),r[0],'regel')
for sl,w,bron,tl,pat,ber in ANKERS:
  if bron not in codes: raise SystemExit('anker-bron ontbreekt: '+bron)
  ins('anker',['sleutel','waarde','bron_code','toelichting','patroon','bereik'],[sl,w,bron,(tl or None),pat,ber],'ANKER-'+sl,'anker')
for sl,p in PATROON_UPDATES.items():
  o=c.execute('select patroon from anker where sleutel=?',(sl,)).fetchone()[0]
  if o!=p: c.execute('update anker set patroon=? where sleutel=?',(p,sl));wijz('ANKER-'+sl,'patroon aangescherpt','patroon',o,p);S['anker']+=1
for b in BOGEN:
  v=VOORSTEL.get(b[0])
  ins('boog',['code','fase','boek','hoofdpersoon','leeftijd_hoofdpersoon','geslacht_hoofdpersoon','romance','erotische_sleutelscene','terugkerend_motief','noodoplossing','wie_betaalt','toon','vorm','afloop','bron','status','voorstel','voorstel_status'],list(b[:15])+['afgeleid uit canon (Z33)',v,'voorlopig' if v else None],b[0],'boog')
for p in PERSONAGES:
  ins('personage',['code','naam','per_code','fase','rol','eigen_fout','soort_fout','wie_betaalt','zelfbedrog','daarna_doet','bron','status','voorstel','voorstel_status'],list(p)+['voorlopig' if p[12] else None],p[0],'personage')
# zaadjes, afgeleid uit canonrijen
LEV="status in('vastgesteld','voorlopig')"
Z=[]
for code,f in c.execute(f"select code,feit_schoon from canon where {LEV} and code like 'VERHAAL-%' and feit_schoon like '%Zaad:%' order by id").fetchall():
  t=re.search(r'Zaad: (.*?)(?:\.(?= [A-Z])|$)',f).group(1)[:300]
  Z.append(('ZAAD-'+code,t,code,'boek 1 (801)' if '801' in t else 'later (fase/jaar in de tekst)','open (verhaal nog niet geschreven)',code))
for code,f in c.execute(f"select code,feit_schoon from canon where {LEV} and feit_schoon like '%geplant h%' order by id").fetchall():
  m=re.search(r'geplant (h\d+)(?:, geoogst (h\d+))?',f)
  Z.append(('ZAAD-'+code,f[:300],'roman '+m.group(1),'roman '+m.group(2) if m.group(2) else '-','geland' if m.group(2) else 'open',code))
for code,f in c.execute(f"select code,feit_schoon from canon where {LEV} and (feit_schoon like '%Plant:%' and feit_schoon like '%Oogst:%') order by id").fetchall():
  p=re.search(r'Plant: ([^.;]*)',f).group(1);o=re.search(r'Oogst: ([^.;]*)',f).group(1)
  Z.append(('ZAAD-'+code,f[:300],p[:120],o[:120],'geland' if o.strip() and o.strip()!='-' else 'open',code))
Z+=[('ZAAD-stille-modus','Stille Modus (1 jongen op 100, vonkcellen naar de overblijvende mannen): Ysa ontwerpt hem in boek 0 (ORIGIN-10, BESLUIT-Z30-1) maar de roman zaait hem niet.','boek 0 (nog niet gezaaid)','jaar 0 (Raad der Moeders) / boek 1','open (WRIJ-Z30-2)','WRIJ-Z30-2; ORIGIN-10'),
('ZAAD-hesta-vonkcellen','Hesta\'s negen vonkcellen zonder vervolg.','roman','-','open (WRIJ-Z21-5)','WRIJ-Z21-5'),
('ZAAD-blauw-licht','Blauw licht in jaar 3 tegen Hesta\'s ruil.','roman h31 / jaar 3','-','open (WRIJ-Z22-2)','WRIJ-Z22-2'),
('ZAAD-c4r','"C-4-R. You went down it three times." (h27): Ysa kan dit niet weten.','roman h24 (Thalen hoort het)','roman h27','open (WRIJ-Z29-1)','WRIJ-Z29-1')]
for z in Z: ins('zaadje',['code','wat','geplant_in','oogst_in','status','bron'],list(z),z[0],'zaadje')
for code,titel,delen,besch,verw,typ in WRIJ:
  if not c.execute('select 1 from wrijving where code=?',(code,)).fetchone():
    c.execute('insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)',(titel,delen,besch,typ,'open',code,verw));S['wrijving']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
for code,ond,t in HANDL: ins('handleiding',['code','onderwerp','tekst'],[code,ond,t],code,'handleiding')
if not c.execute("select 1 from logboek where wat like 'Ronde Z33%'").fetchone():
  i=c.execute('select max(id) from logboek').fetchone()[0]+1
  c.execute('insert into logboek(id,datum,wat) values(?,?,?)',(i,DT,'Ronde Z33: canon-motor als meetlat. Nieuw: herkomst (bron/besloten_door/besloten_op), regeltabel + toets.py uit regels, getypeerde relaties + v_impact, ankers uitgebreid + anker_kopie/v_actief_anker, mal-breker (boog), personagevelden (personage), zaadjes, triggers. Scorekaart voor/na: z33/scorekaart.md. Niets verwijderd; canonfeiten en Kern niet gewijzigd; roman niet aangeraakt.'));S['logboek']+=1
c.commit();afgeleid.bouw(c);c.commit()
# baseline: bevindingen van de Z33-regels/ankers registreren met hun wrijving (oude regels niet: die moeten 0 blijven)
MAP={'fase_nummer':'WRIJ-Z33-1','kern_leunt_op_kleur':'WRIJ-Z33-2','motief_max':'WRIJ-Z33-3','mal_aangrenzend':'WRIJ-Z33-6','kern_zonder_bron':'WRIJ-Z33-7','anker':'WRIJ-Z33-8','na_dood':'WRIJ-Z33-9','leeftijd':'WRIJ-Z33-10','naam':'WRIJ-Z33-11'}
NIEUWE_ANKERS={a[0] for a in ANKERS}
if '--geen-baseline' not in sys.argv:
  j=os.path.join(tempfile.mkdtemp(),'t.json');subprocess.run([sys.executable,'toets.py',DB,'--json',j],capture_output=True)
  U={(t,cd,d) for t,cd,d in c.execute('select toets,code,detail from toets_uitzondering')}
  for t,cd,d in json.load(open(j)):
    if (t,cd,d) in U or t not in MAP: continue
    if t=='anker' and d.split(':')[0] not in NIEUWE_ANKERS|set(PATROON_UPDATES): continue
    S['uitzondering']+=c.execute('insert or ignore into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',(t,cd,d,'Gevonden door Z33-regel; geregistreerd voor Rogiers besluit (niet zelf aangepast).',MAP[t])).rowcount
  c.commit()
os.makedirs('z33',exist_ok=True)
if DB=='canon.db': json.dump(S,open('z33/stats.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False))
