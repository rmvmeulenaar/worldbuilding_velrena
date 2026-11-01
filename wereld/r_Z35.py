# Ronde Z35: rijm en opschoning (opdracht architect, OPDRACHT_architect_Z35.md, stap 1-6). Idempotent en additief.
# Niets verwijderd; geen Kern-inhoud gewijzigd; roman niet aangeraakt. toets.py na elke stap (exit 0 vereist).
# Gebruik: DB=kopie.db python3 r_Z35.py
import sqlite3,shutil,os,re,json,sys,collections,subprocess
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z35')]
import afgeleid,migreer
from toestand import parse,per_code
import data as Dz
DT='2026-11-01';RD='Z35';RN=64;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z35.db'): shutil.copy('canon.db','canon_backup_Z35.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z35.py')).rowcount
def toets(stap):
  afgeleid.bouw(c);c.commit()
  r=subprocess.run([sys.executable,'toets.py',DB,'--json',f'/tmp/toets_{RD}.json'],capture_output=True,text=True)
  print(f'[{stap}] toets exit {r.returncode}: '+' | '.join(l for l in r.stdout.splitlines()[1:4]))
  if r.returncode: print(r.stdout[-3000:]);sys.exit(f'toets faalt na {stap}')
LEV="status in('vastgesteld','voorlopig')"
codes=lambda:{r[0] for r in c.execute('select code from canon')}
CANONKOL=[r[1] for r in c.execute('pragma table_info(canon)') if r[1]!='id']
# ================= STAP 1: personagetoestand naar kolommen =================
for r in [('aelthir',900,'canon','PER-aelthir-schurk-ileth-V5','ca. 900 jaar ("binnen de Aelthir-levensduur van ca. 900 jaar"). Botst met Vaelorn, ca. 1200 jaar oud in 801 (PER-vaelorn-nu): open in WRIJ-Z14-2.'),
          ('orrim',None,'onbekend','VOLK-orrim','"eeuwenoud" (VOLK-orrim); geen getal in de canon, dus geen sterfjaar berekenen (WRIJ-Z14-2).'),
          ('*',70,'aanname','script ronde Z11','Standaard voor alle andere volken. Geen canonbron: elk sterfjaar dat hiermee berekend wordt, toont aanname = 1.')]:
  if c.execute('insert or ignore into levensduur(volk,jaren,soort,bron,toelichting) values(?,?,?,?,?)',r).rowcount: wijz('LEVENSDUUR-'+r[0],'toegevoegd','levensduur',None,r[1])
C=codes()
R=c.execute(f"select code,feit_schoon,verwijst_naar,status from canon where status in('voorlopig','vastgesteld') and code like 'TOESTAND-%' and coalesce(ideeenbank,0)=0 and draagkracht!='Kern' and draagkracht_handmatig is null order by id").fetchall()
volk={}
for code,ft in c.execute("select code,feit_schoon from canon where (code like 'PER%' or code like 'HOOFDPERS%') and feit_schoon like '%Volk: %'"):
  m=re.search(r'Volk: ([A-Za-zûë-]+)',ft or '')
  if m: volk[code]=m.group(1).lower()
rijen=[];niet=[]
for code,ft,v,st in R:
  p=parse(ft);per=per_code(v,C)
  if p and st=='vastgesteld' and p['soort']=='toestand': p=None  # handgeschreven verhaaltijdlijn: blijft staan
  if p: p['status_oud']=st
  if p and p['soort']=='samengevoegd': per=p.pop('doel') if p.get('doel') in C else None
  if not p or not per: niet.append(code);continue
  p['per_code']=per;p['bron']=code
  if p['soort']=='geboren': p['volk']=volk.get(per)
  rijen.append(p)
geb_aanname={p['per_code'] for p in rijen if p['soort']=='geboren' and p.pop('had_aanname',0)}
geb_echt={p['per_code']:p['jaar'] for p in rijen if p['soort']=='geboren' and not p.get('aanname') and p.get('jaar') is not None}
for p in rijen:
  if p['soort'] in('knooppunt','actief','later') and p['per_code'] in geb_aanname and p['per_code'] in geb_echt and p.get('jaar') is not None:
    p['leeftijd']=p['jaar']-geb_echt[p['per_code']];p['aanname']=0;p['aanname_reden']=None  # gecorrigeerd geboortejaar: leeftijd herberekend
    continue
  if p['soort'] in('knooppunt','actief','later') and p['per_code'] in geb_aanname and not p.get('aanname'):
    p['aanname']=1;p['aanname_reden']='leeftijd volgt uit een aangenomen geboortejaar of een aangenomen leeftijd 30 (zie de geboren-rij)'
K=['per_code','jaar','leeftijd','rol','regio','wil','geheim','verandert','aanname','aanname_reden','bron','soort','volk','toestand','maan','rest','status_oud']
for p in rijen:
  p.setdefault('aanname',0)
  S['toestand']+=c.execute(f"insert or ignore into personage_toestand({','.join(K)}) values({','.join('?'*len(K))})",[p.get(k) for k in K]).rowcount
  if c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=? and status in('voorlopig','vastgesteld')",(p['per_code'],p['bron'])).rowcount:
    S['toestand_vervangen']+=1;wijz(p['bron'],'vervangen','status',p['status_oud'],'voorlopig, vervangen (naar personage_toestand; vervangen_door '+p['per_code']+')')
print('stap 1: geparst',len(rijen),'niet zeker (blijven staan):',len(niet),niet)
toets('stap 1')
# ================= STAP 2: rijmregel =================
e=Dz.ERF_VOORTIJD
if not c.execute('select 1 from canon where code=?',(e[0],)).fetchone() and c.execute("insert or ignore into canon(code,categorie,onderwerp,feit,reden,status,ronde,verwijst_naar,hangt_samen_met) values(?,?,?,?,?,'voorlopig',?,?,?)",(e[0],e[1],e[2],e[3],e[4],RN,e[5],e[5])).rowcount: wijz(e[0],'toegevoegd','canon',None,'voorstel (voorlopig)')
FK=['fase','volgorde','mechanisme','beslisser','beslisser_as','betaler','betaler_as','vervalst','vervalst_as','ontdekt','ontdekt_as','schaal','erft_van','blijvende_verandering','bron','status']
for r in Dz.RIJM:
  if c.execute(f"insert or ignore into fase_rijm({','.join(FK)}) values({','.join('?'*len(FK))})",r).rowcount: S['fase_rijm']+=1;wijz('RIJM-'+r[0],'toegevoegd','fase_rijm',None,r[15])
for code,(a,b,v,o,s) in Dz.BOOG.items():
  for k,x in zip(('beslisser_as','betaler_as','vervalst_as','ontdekt_as','schaal'),(a,b,v,o,s)):
    if x is not None and c.execute(f'update boog set {k}=? where code=? and {k} is null',(x,code)).rowcount: S['boog_as']+=1;wijz(code,'gewijzigd','boog.'+k,None,x)
REG=[('R-rijm_assen','verhaal',"Rijm, geen kopie: elke fase in fase_rijm verschilt van de vorige op minstens 3 van de 5 assen beslisser, betaler, vervalst, ontdekt, schaal (de *_as-kolommen; leeg telt niet als verschil).",'py:rijm_assen','OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1','architect (Z35), ter vaststelling door Rogier','actief','fout'),
('R-rijm_erfenis','verhaal',"Elke fase vanaf fase 1 erft (fase_rijm.erft_van) van minstens één levende ERF-rij uit een eerdere fase.",'py:rijm_erfenis','OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1','architect (Z35), ter vaststelling door Rogier','actief','fout'),
('R-rijm_spiraal','verhaal',"Spiraal, geen cirkel: blijvende_verandering is niet leeg en komt niet (letterlijk of voor 60% van de woorden) terug uit een eerdere fase.",'py:rijm_spiraal','OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1','architect (Z35), ter vaststelling door Rogier','actief','fout'),
('R-rijm_binnen_fase','verhaal',"De bogen binnen één fase verschillen onderling op minstens 2 rijm-assen (boog.beslisser_as, betaler_as, vervalst_as, ontdekt_as, schaal).",'py:rijm_binnen_fase','OPDRACHT_architect_Z35.md stap 2; HANDL-Z35-1','architect (Z35), ter vaststelling door Rogier','actief','fout')]
for r in REG:
  if c.execute('insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)',r).rowcount: S['regel']+=1;wijz(r[0],'toegevoegd','regel',None,RD)
H=[('HANDL-Z35-1','Rijm, geen kopie',"De acht fasen plus 801 zijn een spiraal. Elke fase draait dezelfde motor (probleem, noodoplossing, prijs, vervalsing), maar verschuift wie beslist, wie betaalt, wat er vervalst wordt, of het uitkomt en op welke schaal; en elke fase laat iets na dat niet meer terug kan. Dat staat per fase in fase_rijm (view v_rijm), per boog in de rijm-assen van boog. Regels: R-rijm_assen, R-rijm_erfenis, R-rijm_spiraal, R-rijm_binnen_fase."),
   ('HANDL-Z35-2','Schrijven alleen vanuit het schrijfpakket',"Een schrijvende agent begint niet zonder python3 vraag.py schrijfpakket <BOOG> (view v_schrijfpakket): vorm, verteller en tempo van de boog, de fase_rijm-rij, de rijm-assen van de boog, de geërfde ERF-rijen, de personages met hun eigen fout, de open zaadjes, de kernscènes en de Kern-rijen die niet mogen breken. Een synopsis is geen schrijfinstructie: ze vertelt wat er gebeurt, niet hoe het geschreven wordt."),
   ('HANDL-Z35-3','Personagetijdlijn in kolommen',"Leeftijd, jaar, regio, rol, wil en geheim per personage staan in personage_toestand (view v_personage_tijdlijn), niet meer in TOESTAND-rijen. Leeg is NULL, nooit '-' of 'onbekend'. Een sterfjaar dat uit een levensduur volgt, wordt berekend uit tabel levensduur en draagt aanname = 1; dat is geen feit.")]
for h in H:
  if c.execute('insert or ignore into handleiding(code,onderwerp,tekst) values(?,?,?)',h).rowcount: S['handleiding']+=1;wijz(h[0],'toegevoegd','handleiding',None,RD)
# rijm-bevindingen: alleen als open wrijving vastleggen (niet wegpoetsen)
afgeleid.bouw(c);c.commit()
r=subprocess.run([sys.executable,'toets.py',DB,'--json','/tmp/t35.json'],capture_output=True,text=True)
U={(t,cd,d) for t,cd,d in c.execute('select toets,code,detail from toets_uitzondering')}
nieuw=[x for x in json.load(open('/tmp/t35.json')) if tuple(x) not in U and x[0].startswith('rijm_')]
if nieuw:
  W1=('WRIJ-Z35-1','Rijm: bogen in één fase die te veel op elkaar lijken',' ; '.join(f'{b}: {d}' for _,b,d in nieuw),
      "R-rijm_binnen_fase vindt bogen die op minder dan 2 rijm-assen verschillen: "+'; '.join(f'{b} ({d})' for _,b,d in nieuw)+". Het hoofdverhaal van fase 2 en boog 2-c vertellen hetzelfde verraad (Tarn beslist, Orric betaalt). Voorstel: VOORSTEL-Z35-verhaal-2.",'mogelijke fout','open')
  if c.execute('insert or ignore into wrijving(code,titel,verwijst_naar,beschrijving,type,status,delen_die_botsen) values(?,?,?,?,?,?,?)',(W1[0],W1[1],'VERHAAL-fase2;VERHAAL-fase2-c',W1[3],W1[4],W1[5],'VERHAAL-fase2;VERHAAL-fase2-c')).rowcount: wijz(W1[0],'toegevoegd','wrijving',None,'open')
  for t,cd,d in nieuw: S['uitzondering']+=c.execute('insert or ignore into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',(t,cd,d,'rijm-bevinding Z35; open tot Rogier kiest','WRIJ-Z35-1')).rowcount
# patroonbreuk-voorstellen gaan in stap 6 mee met de voorstelrijen (codes VOORSTEL-Z35-breuk-*), en staan per fase in fase_rijm.voorstel
for fase,vs in (('6 Markt','VOORSTEL-Z35-breuk-markt'),('5 Ontvangst','VOORSTEL-Z35-breuk-ontvangst'),('4 Noodtoestand','VOORSTEL-Z35-breuk-noodtoestand'),('801 Heden','VOORSTEL-Z35-kern-derde-weg'),('0 Voortijd','VOORSTEL-Z35-kern-voortijd-erf')):
  if c.execute('update fase_rijm set voorstel=? where fase=? and voorstel is null',(vs,fase)).rowcount: wijz('RIJM-'+fase,'gewijzigd','fase_rijm.voorstel',None,vs)
toets('stap 2')
# ================= STAP 3: formulier uit de synopsen =================
STOP=r'(?= Label:| Zintuig:| Herkenbaar:| Kernscènes:| Zaad:| \[|$)'
def splits_scenes(t):
  t=t.strip().rstrip('.')
  delen=re.split(r'(?:,|;) (?:en )?(?=(?:de|het|een|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf|honderd|haar|zijn|hun|kasten|Anath|Anaths|Corvina|Veere|Saske|Ylva|Mira|Kovan|Machteld|Joris|Odile|Dessa|Liane|Brom|Lenne|Merel|Tarn|Hanne|Maelis|Selva|Annike|Dirk|Joost)\b)',t)
  return [d.strip() for d in delen if d.strip()]
nieuwe={}
for oid,code,f,st,hand in c.execute(f"select id,code,feit,status,draagkracht_handmatig from canon where {LEV} and code like 'VERHAAL-fase%' and code not like '%-Z35' order by id").fetchall():
  nc=re.sub(r'-Z32$','',code)+'-Z35';f0=f;seeds=[]
  for i,(span,oogst) in enumerate(Dz.SEED.get(code,[])):
    assert span in f,(code,span[:40]);f=f.replace(' '+span,'',1) if (' '+span) in f else f.replace(span,'',1)
    w=Dz.SEED_WAT.get((code,i)) or re.sub(r'^(?:Het )?[Zz]aad voor fase \d: ','',span)
    seeds+=[(x,oogst) for x in (w if isinstance(w,list) else [w])]
  f=re.sub(r'(^|(?<=[.!?"”)] ))(?:BEGIN|ESCALATIE|KEERPUNT|CLIMAX|NASLEEP)\. ',r'\1',f)
  herk=[m.strip() for m in re.findall(r' Herkenbaar: (.*?)'+STOP,f,re.S)];f=re.sub(r' Herkenbaar: (.*?)'+STOP,'',f,flags=re.S)
  ks=re.findall(r' Kernscènes: (.*?)'+STOP,f,re.S);f=re.sub(r' Kernscènes: (.*?)'+STOP,'',f,flags=re.S)
  zd=re.findall(r' Zaad: (.*?)'+STOP,f,re.S);f=re.sub(r' Zaad: (.*?)'+STOP,'',f,flags=re.S)
  tail=re.search(r' Zintuig: (.*?) Haak: (.*?) Functie: (.*?) Crosslinks: (.*)$',f,re.S);zint=haak=None;extra=[]
  if tail:
    zint,haak=tail.group(1).strip(),tail.group(2).strip();extra=[x.strip(' .') for x in tail.group(4).split(',')];f=f[:tail.start()]
  f=re.sub(r'  +',' ',f).strip()
  if not f.endswith(('.','!','?','"','”',')')): f+='.'
  for z in zd:
    zc='ZAAD-'+code;z=z.strip();oud=c.execute('select wat from zaadje where code=?',(zc,)).fetchone()
    if not oud: S['zaadje']+=c.execute("insert or ignore into zaadje(code,wat,geplant_in,oogst_in,status,bron) values(?,?,?,?,?,?)",(zc,z,code,'later (fase/jaar in de tekst)','open (verhaal nog niet geschreven)',code+' (Z35: uit de synopsis gehaald)')).rowcount
    elif oud[0].strip()!=z: print('LET OP: zaadje wijkt af van tekst',zc)
  for i,(wat,oogst) in enumerate(seeds,1):
    zc=f'ZAAD-{nc}-{i}'
    if c.execute("insert or ignore into zaadje(code,wat,geplant_in,oogst_in,status,bron) values(?,?,?,?,?,?)",(zc,wat,code,oogst,'open (verhaal nog niet geschreven)',code+' (Z35: zaad-zin uit de hoofdsynopsis)')).rowcount: S['zaadje']+=1;wijz(zc,'toegevoegd','zaadje',None,code)
  old=dict(zip(CANONKOL,c.execute(f"select {','.join(CANONKOL)} from canon where id=?",(oid,)).fetchone()))
  vn=[x for x in (old['verwijst_naar'] or '').split(';') if x]
  vn+= [x for x in extra if x and x not in vn and x in C]
  if not c.execute('select 1 from canon where code=?',(nc,)).fetchone():
    new={k:old[k] for k in ('categorie','onderwerp','hangt_samen_met','jaar','tijdperk','intensiteit','weet','functie','afstoting','aantrekking_bron','aantrekking','techniek','draagkracht_handmatig')}
    new.update(code=nc,feit=f,status=st,ronde=RN,verwijst_naar=';'.join(vn),reden=(old['reden'] or '')+f' [Ronde Z35: formulier eruit (Herkenbaar, Kernscènes, Zaad, BEGIN/ESCALATIE/KEERPUNT); verhaal ongewijzigd; was {code}]')
    c.execute(f"insert into canon({','.join(new)}) values({','.join('?'*len(new))})",list(new.values()));S['synopsis_nieuw']+=1;wijz(nc,'toegevoegd','canon',None,'synopsis zonder formulier (was '+code+')')
  if c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=? and status in('vastgesteld','voorlopig')",(nc,code)).rowcount: wijz(code,'vervangen','status',st,'voorlopig, vervangen -> '+nc)
  for cd,dt,rd,wr in c.execute("select toets,detail,reden,wrijving from toets_uitzondering where code=?",(code,)).fetchall():
    c.execute('insert or ignore into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',(cd,nc,dt,(rd or '')+' (overgenomen van '+code+' in Z35)',wr))
  upd={'synopsis_code':nc,'herkenbaar':' '.join(herk) or None,'zintuig':zint,'haak':haak}
  for k,v in upd.items():
    if v and c.execute(f'update boog set {k}=? where code=? and {k} is null',(v,code)).rowcount: wijz(code,'gewijzigd','boog.'+k,None,v[:120])
  for k_ in ks:
    for i,sc in enumerate(splits_scenes(k_),1): S['kernscene']+=c.execute('insert or ignore into kernscene(boog_code,volgorde,scene,bron) values(?,?,?,?)',(code,i,sc,code)).rowcount
  nieuwe[code]=nc
print('stap 3: synopsen',len(nieuwe))
C=codes()
toets('stap 3')
# ================= STAP 4: schrijfcontract (view in migratie 005, handleiding HANDL-Z35-2, vraag.py schrijfpakket) =================
n=c.execute('select count(distinct boog_code) from v_schrijfpakket').fetchone()[0];print('stap 4: v_schrijfpakket bogen',n)
toets('stap 4')
# ================= STAP 5 en 6: voorstellen, herkomst, keuzelijst =================
for code,cat,ond,feit,raakt,soort in Dz.VOORSTEL:
  vn=';'.join(x for x in raakt.split(';') if x in C)
  if not c.execute('select 1 from canon where code=?',(code,)).fetchone() and c.execute("insert or ignore into canon(code,categorie,onderwerp,feit,reden,status,ronde,verwijst_naar,hangt_samen_met) values(?,?,?,?,?,'voorlopig',?,?,?)",(code,cat,ond,feit,f'Ronde Z35: voorstel ({soort}) ter keuze door Rogier; niet besloten. Raakt: {raakt}.',RN,vn,vn)).rowcount: S['voorstel']+=1;wijz(code,'toegevoegd','canon',None,'voorstel '+soort)
toets('stap 5-6 (voorstellen)')
# ---- stap 5: herkomst-gaten (top 50) en stap 6: keuzes voor Rogier, in tabel keuze (Model; keuzelijst.md wordt eruit gegenereerd) ----
afgeleid.bouw(c);c.commit()
DKR={'Kern':3,'Structuur':2,'Kleur':1}
def impact(cs):
  cs=[x for x in cs if x]
  if not cs: return 0
  return c.execute(f"select count(distinct leunt) from v_impact where code in({','.join('?'*len(cs))})",cs).fetchone()[0]
inkom=collections.Counter(r[0] for r in c.execute("select naar_code from relatie where soort='leunt_op'"))
gaten=c.execute(f"select code,onderwerp,bron_spoor,verwijst_naar,status from canon where {LEV} and draagkracht='Structuur' and coalesce(bron,'onbekend')='onbekend'").fetchall()
gaten.sort(key=lambda r:(-inkom[r[0]],r[0]))
GEZAG=('besluit','roman','auteur')
for i,(code,ond,sp,vn,st) in enumerate(gaten[:50],1):
  kand=[]
  for x in [y.strip() for y in (vn or '').split(';') if y.strip()]:
    b=c.execute("select bron,bron_soort from canon where code=? and coalesce(bron,'onbekend')!='onbekend'",(x,)).fetchone()
    if b and b[1].startswith(GEZAG): kand.append(f'{x} (die rij heeft bron {b[0]})')
  if kand: vb='kandidaat: '+'; '.join(kand[:2])+'. Bevestigen of de rij echt daaruit volgt.'
  elif sp: vb='geen bron met gezag gevonden; alleen het spoor '+sp.split(' (')[0]+'. Vaststellen met een besluit, naar de ideeënbank, of zo laten.'
  else: vb='geen kandidaat en geen spoor. Rogier noemt de bron, of de rij gaat naar de ideeënbank.'
  if c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,impact,draagkracht,status,bron) values(?,?,?,?,?,?,?,?,?)',(f'KEUZE-Z35-H{i:02d}','herkomst',f'{code}: {ond}',vb,code,inkom[code],'Structuur','open','r_Z35.py stap 5')).rowcount: S['keuze']+=1
for code,cat,ond,feit,raakt,soort in Dz.VOORSTEL:
  if c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,impact,draagkracht,status,bron) values(?,?,?,?,?,?,?,?,?)',('KEUZE-'+code,'voorstel '+soort,ond,feit,raakt,impact(raakt.split(';')),max((c.execute('select draagkracht from canon where code=?',(x,)).fetchone() or ('Kleur',))[0] for x in raakt.split(';')) if False else None,'open',code)).rowcount: S['keuze']+=1
for code,raakt in c.execute('select code,raakt from keuze where soort like ? and draagkracht is null',('voorstel%',)).fetchall():
  d=[(c.execute('select draagkracht from canon where code=?',(x,)).fetchone() or (None,))[0] for x in raakt.split(';')]
  c.execute('update keuze set draagkracht=? where code=?',(max((x for x in d if x),key=lambda x:DKR[x],default='-'),code))
for code,titel,dl,vn,st in c.execute("select code,titel,delen_die_botsen,verwijst_naar,status from wrijving where status like 'open%'").fetchall():
  cs=sorted({x.strip() for x in re.split(r'[;,]',(dl or '')+';'+(vn or '')) if x.strip()})
  d=[(c.execute('select draagkracht from canon where code=?',(x,)).fetchone() or (None,))[0] for x in cs]
  dk=max((x for x in d if x),key=lambda x:DKR[x],default='-')
  ab=Dz.AANBEVELING.get(code) or 'Nog geen aanbeveling: niet inhoudelijk gelezen in Z35.'
  if c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,impact,draagkracht,status,bron) values(?,?,?,?,?,?,?,?,?)',('KEUZE-'+code,'wrijving',titel,ab,';'.join(cs),impact(cs),dk,'open',code)).rowcount: S['keuze']+=1
toets('stap 5-6 (keuzes)')
c.commit()
json.dump(dict(S),open(f'z35/r_Z35_tellingen_{os.path.basename(DB)}.json','w'),ensure_ascii=False)
print('klaar',dict(S))
