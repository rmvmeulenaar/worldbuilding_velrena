# Ronde Z31: robuust tegen kettingschade (Rogier, 2026-10-31). Idempotent, additief, niets verwijderd, roman niet aangeraakt.
import sqlite3,shutil,os,json,re,subprocess,sys
sys.path.insert(0,'migraties');sys.path.insert(0,'z31')
import afgeleid,migreer
from ankers import ANKERS
from data import W,V,VR,H
DT='2026-10-31';RD='Z31';R='Rogier: database robuust maken tegen kettingschade (ronde Z31), 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z31.db'): shutil.copy('canon.db','canon_backup_Z31.db')
c=sqlite3.connect(DB);S={'migraties':[],'anker':0,'links_hersteld':[],'wrijving':[],'voorstel':[],'vraag':[],'handleiding':0,'naam_markering':0,'uitzondering':0,'wijziging':0}
S['migraties']=migreer.draai(c)
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='VOORSTEL-Z31-mal-1'").fetchone() else RONDE+1
def wijz(code,soort,veld,oud,nieuw,bron,ronde=RD,datum=DT):
  n=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(ronde,code,soort,veld or '',oud,nieuw,datum,bron)).rowcount;S['wijziging']+=n
# 1 ankers
for a in ANKERS: S['anker']+=c.execute('insert or ignore into anker(sleutel,waarde,bron_code,toelichting,patroon,bereik) values(?,?,?,?,?,?)',a).rowcount
# 1b bronrijen van getal/jaar-ankers zijn tijdlijn-ankers -> Kern via draagkracht_handmatig (alleen vastgesteld en levend)
S['kern_handmatig']=[]
for (b,) in c.execute("select distinct bron_code from anker where sleutel not like '%naam%'").fetchall():
  r=c.execute("select status,draagkracht_handmatig from canon where code=?",(b,)).fetchone()
  if r and r[0]=='vastgesteld' and r[1] is None:
    c.execute("update canon set draagkracht_handmatig='Kern' where code=?",(b,));S['kern_handmatig'].append(b)
  if r and r[0]=='vastgesteld': wijz(b,'draagkracht handmatig','draagkracht_handmatig',None,'Kern','anker-bronrij (tijdlijn-anker)')
# 2 eenduidige dode links herstellen (alleen het token in verwijst_naar/hangt_samen_met)
for code,oud,nieuw in [('BESLUIT-Z19-2','PER-v4-corran','PER-v4-corran-velt'),('BESLUIT-Z26-1','ROMAN-Z16-h5','ROMAN-Z16-h05')]:
  for veld in ('verwijst_naar','hangt_samen_met'):
    v=c.execute(f'select {veld} from canon where code=?',(code,)).fetchone()[0] or ''
    t=[x.strip() for x in re.split(r';',v)]
    if oud in t:
      nv=';'.join(nieuw if x==oud else x for x in t);c.execute(f'update canon set {veld}=? where code=?',(nv,code));wijz(code,'link hersteld',veld,v,nv,'WRIJ-Z30-4 (eenduidig)');S['links_hersteld'].append(f'{code}.{veld}: {oud}->{nieuw}')
# 3 wrijvingen, voorstellen, vragen, handleiding
c.commit();afgeleid.bouw(c)
subprocess.run([sys.executable,'toets.py',DB,'--json','z31/toets_voor.json'],capture_output=True)
B=json.load(open('z31/toets_voor.json'))
EXPL={'Mira ~ Mira de Twijfelende Dochter':'WRIJ-Z31-6','Ilse Varenne ~ Ilse Varo':'WRIJ-Z31-7','Saske Registerhoofd ~ Saskia Stalheelster':'WRIJ-Z31-8','Sabe Mehr ~ Sabe Zoutstem':'WRIJ-Z31-9'}
naam=[b for b in B if b[0]=='naam']; N=len([b for b in naam if b[2] not in EXPL])
for code,t,d,b,ty,st,v in W:
  b=b.replace('{N}',str(N))
  if not c.execute('select 1 from wrijving where code=?',(code,)).fetchone():
    c.execute('insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)',(t,d,b,ty,st,code,v));S['wrijving'].append(code);wijz(code,'toegevoegd','wrijving',None,st,'r_Z31.py')
for code,cat,o,f,v in V:
  if not c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar) values(?,?,?,?,?,?,?,?,?)',(cat,o,f,'voorlopig',R+'; voorstel van een externe review, wacht op Rogier.',v,RONDE,code,v));S['voorstel'].append(code);wijz(code,'toegevoegd','canon',None,'voorlopig','r_Z31.py')
for code,vr,w,st,a,v in VR:
  if not c.execute('select 1 from open_vraag where code=?',(code,)).fetchone():
    c.execute('insert into open_vraag(vraag,waarom_belangrijk,status,antwoord,code,verwijst_naar) values(?,?,?,?,?,?)',(vr,w,st,a,code,v));S['vraag'].append(code);wijz(code,'toegevoegd','open_vraag',None,st,'r_Z31.py')
for code,o,t in H:
  if not c.execute('select 1 from handleiding where code=?',(code,)).fetchone(): c.execute('insert into handleiding(code,onderwerp,tekst) values(?,?,?)',(code,o,t));S['handleiding']+=1
# HANDL-Z30-2 aanvullen met de veilig_18plus-zin (alleen tekst in de handleiding, geen canonfeit)
from data import VEILIG0
t=c.execute("select tekst from handleiding where code='HANDL-Z30-2'").fetchone()[0]
if VEILIG0 not in t: c.execute("update handleiding set tekst=? where code='HANDL-Z30-2'",(t+' '+VEILIG0,));wijz('HANDL-Z30-2','tekst aangevuld','tekst',t,t+' '+VEILIG0,'toets 3')
# 4 naammarkeringen + bekende uitzonderingen
for t_,code,d in naam:
  a,b=d.split(' ~ ')
  if d=='Mira ~ Mira de Twijfelende Dochter': soort,st,toel='erfnaam/echo (voorstel)','voorstel, wacht op Rogier','Aanbeveling: bewuste erfnaam (Ysa/Mira en Ysara/Mira).'
  elif d in EXPL: soort,st,toel='botsing','open','Aanbeveling: hernoemen in de bijverhalen; roman blijft.'
  elif d.startswith('Vaelorn Hoogaelthir ~'): soort,st,toel='zelfde personage (twee tijden)','te beoordelen','PER-vaelorn-nu lijkt dezelfde persoon in 801.'
  else: soort,st,toel='te beoordelen','te beoordelen','Gevonden door toets.py (Z31).'
  S['naam_markering']+=c.execute('insert or ignore into naam_markering(naam_a,naam_b,codes,soort,status,wrijving,toelichting) values(?,?,?,?,?,?,?)',(a,b,code,soort,st,EXPL.get(d,'WRIJ-Z31-10'),toel)).rowcount
MAP={'dode_link':'WRIJ-Z31-1','harde_grens':None,'leeftijd':None,'na_dood':None}
def wr_anker(code,d):
  if 'thalen' in d: return 'WRIJ-Z31-2'
  if 'overlevenden' in d: return 'WRIJ-Z31-3'
  if 'roman_woorden' in d: return 'WRIJ-Z31-4'
FP={'SEKS-VOLK-grauwen-kern':'Nagekeken Z31: "kinderen willen" = nageslacht met een verwante (incesttaboe tussen volwassenen), geen minderjarige.','SEKS-VOLK-orrim-kern':'Nagekeken Z31: "kind" = nakomeling/geheugen in steen, geen seksuele rol van een minderjarige.'}
for t_,code,d in B:
  if t_=='naam': continue  # naam_markering dekt dit (toets slaat gemarkeerde paren over)
  if t_=='anker': w,reden=wr_anker(code,d),'Bekende afwijking van een anker; zie wrijving.'
  elif t_=='harde_grens' and code in FP: w,reden='-',FP[code]
  elif t_=='harde_grens' and code=='SYS-wijding': w,reden='WRIJ-Z31-5','Formulering, geen minderjarige in een seksuele rol (moment: 18e jaar); zie wrijving.'
  elif t_=='dode_link': w,reden='WRIJ-Z31-1','Niet eenduidig; zie wrijving.'
  else: w,reden=None,None
  if w: S['uitzondering']+=c.execute('insert or ignore into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',(t_,code,d,reden,w)).rowcount
# 5 licht event sourcing: wijziging vullen uit wat betrouwbaar af te leiden is
for code,vd,ronde in c.execute("select code,vervangen_door,ronde from canon where status='voorlopig, vervangen' and vervangen_door is not null").fetchall():
  wijz(code,'vervangen','status','vastgesteld/voorlopig (onbekend)','voorlopig, vervangen -> '+vd,'canon.vervangen_door (ronde van vervanging niet altijd bekend)',ronde='?',datum=None)
for code,notitie in c.execute("select code,notitie from historie where notitie!='origineel feit (volledig)'").fetchall():
  m=re.match(r'\[(?:Ronde )?([ZBGVDKr]\d+[a-z]?)',notitie)
  wijz(code,'notitie',None,None,notitie,'historie (rondenotitie)',ronde=m.group(1) if m else '?',datum=None)
for code,st,b in c.execute("select code,status,beschrijving from wrijving where status like 'opgelost%'").fetchall():
  m=re.findall(r'\[(?:Ronde )?(Z\d+[a-z]?)',b or '');wijz(code,'gesloten','status','open',st,'wrijving.status',ronde=m[-1] if m else '?',datum=None)
for i,d,w in c.execute("select id,datum,wat from logboek").fetchall():
  m=re.match(r'(?:Ronde )?([ZBGVDKr]?\d+[a-z]?)\b',w or '');wijz(f'LOGBOEK-{i}','ronde',None,None,(w or '')[:500],'logboek',ronde=m.group(1) if m else '?',datum=d)
# eigen Z31-wijzigingen altijd (idempotent) vastleggen
for code,*_ in W: wijz(code,'toegevoegd','wrijving',None,'open','r_Z31.py')
for code,*_ in V: wijz(code,'toegevoegd','canon',None,'voorlopig','r_Z31.py')
for code,*_ in VR: wijz(code,'toegevoegd','open_vraag',None,'open','r_Z31.py')
for code,oud,nieuw in [('BESLUIT-Z19-2','PER-v4-corran','PER-v4-corran-velt'),('BESLUIT-Z26-1','ROMAN-Z16-h5','ROMAN-Z16-h05')]:
  for veld in ('verwijst_naar','hangt_samen_met'): wijz(code,'link hersteld',veld,oud,nieuw,'WRIJ-Z30-4 (eenduidig)')
if not c.execute("select 1 from logboek where wat like 'Ronde Z31: %'").fetchone():
  c.execute("insert into logboek(datum,wat) values(?,?)",(DT,'Ronde Z31: robuust tegen kettingschade. Migraties 001/002 + schema_versie; kolom draagkracht_handmatig; tabellen anker, naam_markering, toets_uitzondering, wijziging; toets.py; vraag.py wie-leunt-op/kern/open/ideeen/toets; 2 dode links hersteld; WRIJ-Z31-1..14; VOORSTEL-Z31-mal-1..5, -liora-1, -thalen-1 (voorlopig); VRAAG-Z31-1..4; HANDL-Z31-1..6. Niets verwijderd; roman niet aangeraakt.'))
c.commit();afgeleid.bouw(c)
r=subprocess.run([sys.executable,'toets.py',DB,'--rapport','z31/toets_rapport.md','--alles'],capture_output=True,text=True);S['toets_exit']=r.returncode;S['toets_kop']=r.stdout.splitlines()[:3]
S['draagkracht']=dict(c.execute('select draagkracht,count(*) from canon group by 1').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z31/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
