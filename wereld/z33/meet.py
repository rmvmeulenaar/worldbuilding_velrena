#!/usr/bin/env python3
"""Ronde Z33: scorekaart canon-motor (8 metingen) + schema-geuren. Gebruik: python3 z33/meet.py [db] [uit.json]
Meet echt: veranderproef en terugdraaien op tijdelijke kopieën."""
import sqlite3,sys,os,re,json,shutil,tempfile,subprocess,collections
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));os.chdir(W)
DB=sys.argv[1] if len(sys.argv)>1 else 'canon.db';UIT=sys.argv[2] if len(sys.argv)>2 else None
c=sqlite3.connect(DB);q=lambda s,*a:c.execute(s,a).fetchall()
LEV="status in('vastgesteld','voorlopig')"
cols=[r[1] for r in q('pragma table_info(canon)')];tabs={r[0] for r in q("select name from sqlite_master where type='table'")}
R={}
def toets_json(db):
  d=tempfile.mkdtemp();j=os.path.join(d,'t.json')
  p=subprocess.run([sys.executable,'toets.py',db,'--json',j],capture_output=True,text=True)
  return p.returncode,json.load(open(j)),p.stdout
# 1 veranderproef: Thalens sterfjaar -1198 -> -1197 op een kopie
d=tempfile.mkdtemp();k=os.path.join(d,'k.db');shutil.copy(DB,k)
_,voor,_=toets_json(k);kc=sqlite3.connect(k)
kc.execute("update anker set waarde='-1197' where sleutel='thalen_sterfjaar'");kc.commit()
_,na,_=toets_json(k)
mee=sorted({x[1] for x in na if x[0]=='anker' and 'thalen_sterfjaar' in x[2]}-{x[1] for x in voor if x[0]=='anker' and 'thalen_sterfjaar' in x[2]})
lit=[r[0] for r in q(f"select code from canon where {LEV} and feit_schoon like '%1198%' and feit_schoon like '%Thalen%'")]
lit_all=[r[0] for r in q(f"select code from canon where {LEV} and feit_schoon like '%1198%'")]
viaref=[r[0] for r in q(f"select code from canon where {LEV} and (feit_schoon like '%anker thalen_sterfjaar%' or feit_schoon like '%{{thalen_sterfjaar}}%')")]
R['1_veranderproef']={'anker':'thalen_sterfjaar -1198','toets_vindt_mee_te_wijzigen':len(mee),'levende_rijen_Thalen_en_1198':len(lit),'levende_rijen_met_1198':len(lit_all),'rijen_die_via_verwijzing_volgen':len(viaref),'plekken_te_wijzigen':1+len(lit),'voorbeeld':lit[:12]}
# 2 duplicatiegraad: per anker levende rijen die de waarde letterlijk noemen (via patroon)
dup={}
for sl,w,pat in q('select sleutel,waarde,patroon from anker where patroon is not null'):
  n=set()
  for code,ft in q(f'select code,feit_schoon from canon where {LEV}'):
    for p in pat.split(' || '):
      if re.search(p,ft or ''): n.add(code)
  dup[sl]=len(n)
lit={}
for sl,w in q('select sleutel,waarde from anker'):
  ctx=q('select waarde from anker where sleutel=?',sl.split('_')[0]+'_naam')
  if not re.search(r'\d',w): continue
  rx=re.compile(r'(?<![\d.,-])'+re.escape(w)+r'(?![\d.,])')
  n=[code for code,ft in q(f'select code,feit_schoon from canon where {LEV}') if rx.search(ft or '') and (not ctx or ctx[0][0].split()[0] in (ft or ''))]
  lit[sl]=len(n)
R['2b_letterlijke_kopieen']={'totaal':sum(lit.values()),'per_anker':dict(sorted(lit.items(),key=lambda x:-x[1]))}
R['2_duplicatiegraad']={'ankers_met_patroon':len(dup),'kopieen_totaal':sum(dup.values()),'gemiddeld_per_anker':round(sum(dup.values())/max(1,len(dup)),1),'per_anker':dup,'ankers_totaal':q('select count(*) from anker')[0][0]}
# 3 dode links
R['3_dode_links']={'dode_links':q('select count(*) from verwijzing where bestaat=0')[0][0],'van_levende_canon':q(f"select count(*) from verwijzing v join canon c on c.code=v.van_code where v.bestaat=0 and c.{LEV}")[0][0]}
# 4 herkomstdekking
h={}
for dk in('Kern','Structuur'):
  tot=q(f"select count(*) from canon where draagkracht=? and {LEV}",dk)[0][0]
  if 'bron' in cols: met=q(f"select count(*) from canon where draagkracht=? and {LEV} and bron is not null and bron not like 'onbekend%'",dk)[0][0]
  else: met=0
  proxy=q(f"select count(*) from canon where draagkracht=? and {LEV} and (reden like '%BESLUIT-%' or reden like '%Rogier%' or code like 'BESLUIT-%')",dk)[0][0]
  h[dk]={'totaal':tot,'met_bron':met,'pct':round(100*met/max(1,tot),1),'proxy_reden_noemt_besluit_of_Rogier':proxy,'proxy_pct':round(100*proxy/max(1,tot),1)}
h['kolom_bron_bestaat']='bron' in cols;R['4_herkomst']=h
# 5 tests
rc,b,out=toets_json(DB)
U={(t,cd,dd):w for t,cd,dd,w in q('select toets,code,detail,wrijving from toets_uitzondering')}
nieuw=[x for x in b if tuple(x) not in U]
ow={r[0] for r in q("select code from wrijving where status like 'open%'")}
zonder=[x for x in b if tuple(x) in U and U[tuple(x)] not in ow]
R['5_tests']={'exit':rc,'nieuw_falend':len(nieuw),'bekend':len(b)-len(nieuw),'bekend_zonder_open_wrijving':len(zonder),'aantal_controles':len(set(re.findall(r"f\('(\w+)'",open('toets.py').read())))+(q('select count(*) from regel')[0][0] if 'regel' in tabs else 0),'regeltabel':'regel' in tabs}
# 6 roundtrip
if DB=='canon.db':
  p=subprocess.run([sys.executable,'roundtrip.py'],capture_output=True,text=True)
  vs=[int(x) for x in re.findall(r'verschillen (\d+)',p.stdout)]
  R['6_roundtrip']={'exit':p.returncode,'tabellen':len(vs),'verschillen':sum(vs),'kolommen_kwijt':p.stdout.count('KWIJT')}
# 7 terugdraaien: backup Z32 (=stand na Z31) -> r_Z32.py vooruit -> vergelijk canon met canon_backup_Z33/huidig
def terug(backup,script,doel):
  d=tempfile.mkdtemp();k=os.path.join(d,'t.db');shutil.copy(backup,k)
  bew={f:open(f,'rb').read() for f in ['z32/stats.json','z33/stats.json'] if os.path.exists(f)}
  env=dict(os.environ,DB=k);p=subprocess.run([sys.executable,script],env=env,capture_output=True,text=True)
  for f,v in bew.items(): open(f,'wb').write(v)
  if p.returncode: return {'exit':p.returncode,'fout':p.stderr[-300:]}
  sys.path[:0]=[W,os.path.join(W,'migraties')];import afgeleid,migreer
  kc=sqlite3.connect(k);migreer.draai(kc);afgeleid.bouw(kc)
  oc=sqlite3.connect(doel);dv={}
  for t in ['canon','wrijving','open_vraag','anker','naam_markering']:
    cs=[r[1] for r in oc.execute(f'pragma table_info({t})') if r[1]!='id' and r[1] in [x[1] for x in kc.execute(f'pragma table_info({t})')]]
    A=collections.Counter(oc.execute(f"select {','.join(cs)} from {t}"));B=collections.Counter(kc.execute(f"select {','.join(cs)} from {t}"))
    dv[t]=sum(((A-B)+(B-A)).values())
  return {'exit':0,'verschillen':dv,'werkt':all(v==0 for v in dv.values())}
if DB=='canon.db':
  doel='canon_backup_Z33.db' if os.path.exists('canon_backup_Z33.db') and os.environ.get('NA') else 'canon.db'
  R['7_terugdraaien']={'Z31->Z32 (backup_Z32 + r_Z32.py)':terug('canon_backup_Z32.db','r_Z32.py','canon_backup_Z33.db' if os.path.exists('canon_backup_Z33.db') else 'canon.db')}
  if os.environ.get('NA'): R['7_terugdraaien']['Z32->Z33 (backup_Z33 + r_Z33.py)']=terug('canon_backup_Z33.db','r_Z33.py','canon.db')
if 'anker_kopie' in tabs: R['4b_risico_top10']=q('select sleutel,code,waarde_in_rij,afwijkt,draagkracht,risico from anker_kopie order by risico desc,code limit 10')
if 'boog' in tabs: R['extra']={'bogen':q('select count(*) from boog')[0][0],'bogen_mal_score_4plus':q('select count(*) from v_mal where mal_score>=4')[0][0],'personages':q('select count(*) from personage')[0][0],'profiel_geen_personage':q("select count(*) from personage where status like 'profiel%'")[0][0],'zaadjes':q('select status,count(*) from zaadje group by 1'),'relaties':q('select soort,count(*) from relatie group by 1'),'regels':q('select niveau,count(*) from regel group by 1'),'triggers':q("select count(*) from sqlite_master where type='trigger'")[0][0]}
# geuren
g={}
g['puntkomma_lijsten_in_verwijst_naar']=q("select count(*) from canon where verwijst_naar like '%;%'")[0][0]
g['status_met_twee_betekenissen']=q("select count(*) from canon where status='voorlopig, vervangen'")[0][0]
g['historie_in_feit']=q("select count(*) from canon where feit like '%[Ronde %' or feit like '%[Z1%' or feit like '%[Z2%'")[0][0]
g['veiligheidsvarianten']=q('select count(*) from veiligheid_varianten')[0][0]
g['triggers']=q("select count(*) from sqlite_master where type='trigger'")[0][0]
g['foreign_keys']=sum(len(c.execute(f'pragma foreign_key_list({t})').fetchall()) for t in tabs)
pc=collections.Counter(re.split(r'[-_]',x)[0] for (x,) in q(f'select code from canon where {LEV}'))
cc=collections.Counter(r[0] for r in q(f"select categorie from canon where {LEV} and coalesce(ideeenbank,0)=0"))
g['ronde_aantallen_buiten_ideeenbank']={k:v for k,v in cc.items() if v in(10,20,25,30,40,50,60,100,150)}
g['open_wrijvingen']=q("select count(*) from wrijving where status like 'open%'")[0][0]
R['geuren']=g
# 8 koude lezer: zie z33/koude_lezer.py (apart)
if os.path.exists('z33/koude_lezer.py'):
  p=subprocess.run([sys.executable,'z33/koude_lezer.py',DB],capture_output=True,text=True)
  try: R['8_koude_lezer']=json.loads(p.stdout.strip().splitlines()[-1])
  except Exception: R['8_koude_lezer']={'fout':p.stdout[-300:]+p.stderr[-300:]}
s=json.dumps(R,ensure_ascii=False,indent=1);print(s)
if UIT: open(UIT,'w').write(s)
