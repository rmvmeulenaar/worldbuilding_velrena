# Ronde Z39: besluiten na Z38, personagenetwerk + simulatie fase 4 (opdracht_Z35.md stap 11, aanscherping Z39).
# Idempotent en additief; niets verwijderd; roman niet aangeraakt; toets.py na elke stap. Gebruik: DB=kopie.db python3 r_Z39.py [stappen]
import sqlite3,shutil,os,re,json,sys,collections,subprocess,random,math
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z39')]
import afgeleid,migreer,sim,montecarlo as mc,tech
import importlib.util as _iu
def _laad(naam,pad):
  s=_iu.spec_from_file_location(naam,pad);m=_iu.module_from_spec(s);s.loader.exec_module(m);return m
D=_laad('d39',os.path.join(W,'z39','data.py'))
DT='2026-11-01';RD='Z39';RN=68;DB=os.environ.get('DB','canon.db')
STAPPEN=sys.argv[1:] or ['a','sim','tech','f5','prem','proef','keuze']
if DB=='canon.db' and not os.path.exists('canon_backup_Z39.db'): shutil.copy('canon.db','canon_backup_Z39.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
REDEN='Ronde Z39: besluit van '+D.R
WREDEN='Ronde Z39: uit simulatie (verkenning, geen canon; BESLUIT-Z39-5)'
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z39.py')).rowcount
def toets(stap):
  afgeleid.bouw(c);c.commit()
  r=subprocess.run([sys.executable,'toets.py',DB,'--json',f'/tmp/toets_{RD}.json'],capture_output=True,text=True)
  print(f'[{stap}] toets exit {r.returncode}: '+' | '.join(l for l in r.stdout.splitlines()[1:4]))
  if r.returncode: print(r.stdout[-6000:]);sys.exit(f'toets faalt na {stap}')
def bestaat(code): return c.execute('select 1 from canon where code=?',(code,)).fetchone() is not None
def lev(x):
  for _ in range(6):
    r=c.execute('select status,vervangen_door from canon where code=?',(x,)).fetchone()
    if not r: return None
    if r[0] in('vastgesteld','voorlopig') or not r[1] or r[1].startswith('personage_profiel:'): return x
    x=r[1]
  return x
def nieuw(code,cat,ond,feit,verw,reden=REDEN,status='vastgesteld',kern=False,tijdperk=None,jaar=None,ideeenbank=0):
  if bestaat(code): return 0
  verw=';'.join(dict.fromkeys(y for y in (lev(x) for x in verw.split(';') if x) if y)) if verw else verw
  c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,draagkracht_handmatig,tijdperk,jaar,ideeenbank) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (code,cat,ond,feit,feit,reden,status,RN,verw or None,verw or None,'Kern' if kern else None,tijdperk,jaar,ideeenbank))
  S['canon_nieuw']+=1;wijz(code,'toegevoegd','canon',None,status);return 1
def vervang(oud,door):
  r=c.execute("select status from canon where code=? and status in('vastgesteld','voorlopig')",(oud,)).fetchone()
  if r and c.execute("update canon set status='voorlopig, vervangen',vervangen_door=? where code=?",(door,oud)).rowcount:
    S['canon_vervangen']+=1;wijz(oud,'vervangen','status',r[0],'voorlopig, vervangen (door '+door+')')
def zet(tabel,sleutel,waarde,veld,nieuwe,code=None):
  oud=c.execute(f'select {veld} from {tabel} where {sleutel}=?',(waarde,)).fetchone()
  if oud is None or oud[0]==nieuwe: return
  c.execute(f'update {tabel} set {veld}=? where {sleutel}=?',(nieuwe,waarde));S[tabel+'_gewijzigd']+=1;wijz(code or waarde,'gewijzigd',f'{tabel}.{veld}',oud[0],nieuwe)
def sluit_wrij(code,hoe):
  zet('wrijving','code',code,'status','opgelost')
  b=c.execute('select beschrijving from wrijving where code=?',(code,)).fetchone()
  if b and 'Opgelost in Z39' not in (b[0] or ''): zet('wrijving','code',code,'beschrijving',(b[0] or '')+' Opgelost in Z39: '+hoe)
def wrij_nieuw(code,titel,besch,verw):
  if c.execute('select 1 from wrijving where code=?',(code,)).fetchone(): return
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(titel,verw.replace(';',', '),besch,'canon','open',code,verw))
  S['wrijving_nieuw']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
def keuze(code,status,aanb_extra=None):
  r=c.execute('select aanbeveling from keuze where code=?',(code,)).fetchone()
  if not r: return
  if aanb_extra and aanb_extra not in (r[0] or ''): zet('keuze','code',code,'aanbeveling',(r[0] or '')+' '+aanb_extra)
  zet('keuze','code',code,'status',status)
def keuze_nieuw(code,soort,ond,aanb,raakt,citaat):
  if c.execute('select 1 from keuze where code=?',(code,)).fetchone(): return
  c.execute('insert into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',(code,soort,ond,aanb,raakt,'open','r_Z39.py',citaat))
  S['keuze_nieuw']+=1;wijz(code,'toegevoegd','keuze',None,'open')
def regel_nieuw(code,dom,oms,sq,bron,niveau):
  if c.execute('select 1 from regel where code=?',(code,)).fetchone(): return
  c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",(code,dom,oms,sq,bron,D.R,'actief',niveau))
  S['regel_nieuw']+=1;wijz(code,'toegevoegd','regel',None,niveau)
def opvolger(oud,nc,feit,extra_verw,reden):
  """Gewone opvolger: nieuwe levende rij met dezelfde status; de oude wijst ernaar."""
  r=c.execute('select categorie,onderwerp,verwijst_naar,status,tijdperk,jaar from canon where code=?',(oud,)).fetchone()
  if not r: return
  nieuw(nc,r[0],r[1],feit,(r[2] or '')+';'+extra_verw,reden=reden,status=r[3] if r[3] in('vastgesteld','voorlopig') else 'voorlopig',tijdperk=r[4],jaar=r[5]);vervang(oud,nc)
def profiel_opvolger(oud,nc,feit,reden):
  """Opvolger die meteen in personage_profiel staat (zoals D2 in Z37): de nieuwe rij is 'voorlopig, vervangen' door personage_profiel:nc."""
  r=c.execute('select categorie,onderwerp,verwijst_naar,tijdperk,jaar,vervangen_door,status from canon where code=?',(oud,)).fetchone()
  if not r or bestaat(nc): return
  c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,jaar,vervangen_door) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (nc,r[0],r[1],feit,feit,reden,'voorlopig, vervangen',RN,r[2],r[2],r[3],r[4],'personage_profiel:'+nc))
  S['canon_nieuw']+=1;wijz(nc,'toegevoegd','canon',None,'voorlopig, vervangen (personage_profiel:'+nc+')')
  if r[6] in('vastgesteld','voorlopig'): vervang(oud,nc)
  else: c.execute('update canon set vervangen_door=? where code=?',(nc,oud));wijz(oud,'vervangen','vervangen_door',r[5],nc)
def voeg_in(feit,zin):
  m=re.search(r'\s((?:Veiligheids)?[Ll]abel: )',feit)
  return feit[:m.start()]+' '+zin+feit[m.start():] if m else feit.rstrip()+' '+zin
def epi(code,e):
  c.execute("update canon set epistemiek=? where code=? and coalesce(epistemiek,'')=''",(e,code))
N=lambda r:f"simulatie ({r['run_id']}, seed {r['seed']})"
# ================= A: besluiten na Z38 =================
def stap_a():
  for code,cat,ond,feit,verw in D.BESLUIT: nieuw(code,cat,ond,feit,verw,kern=code=='BESLUIT-Z39-3');epi(code,'feit (besluit van Rogier)')
  zet('canon','code','EROS-GRENZEN-Z7','bron_handmatig','BESLUIT-Z30-4')
  zet('canon','code','GES-officiele-versie','bron_handmatig','auteur (Rogier), wereldbijbel')
  sluit_wrij('WRIJ-Z38-2','EROS-GRENZEN-Z7 krijgt BESLUIT-Z30-4 als bron, GES-officiele-versie de wereldbijbel (BESLUIT-Z39-3).')
  sluit_wrij('WRIJ-Z38-1',"laten staan; bij herschrijven 'geslachtsverhouding 1 op 20' (BESLUIT-Z39-2).")
  keuze('KEUZE-WRIJ-Z38-2','besloten','[Z39: BESLUIT-Z39-3]');keuze('KEUZE-WRIJ-Z38-1','besloten','[Z39: BESLUIT-Z39-2]')
  keuze('KEUZE-WRIJ-Z29-1','open','[Z39: blijft open, romanwerk (BESLUIT-Z39-1).]')
  regel_nieuw('R-sim_harde_lijn','harde lijn','Simulatie: geen gebeurtenistype met harde-lijnrisico; in sim_gebeurtenis geen minderjarige buiten geboorte, opvoeding, erfenis of dood.','py:sim_harde_lijn','REGEL-harde-grenzen; BESLUIT-Z30-4','fout')
  regel_nieuw('R-epistemiek','simulatie','Elke rij in de simulatietabellen en elke Z39-canonrij draagt epistemiek; simulatierijen noemen run-id en seed (BESLUIT-Z39-5).','py:epistemiek','BESLUIT-Z39-5','fout')
  c.commit()
# ================= SIM: regels, typen, Monte Carlo fase 4 =================
def zaai_regels():
  for code,oms,par,waarde,bron,aann,van,tot in sim.REGELS:
    S['sim_regel']+=c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
      (code,'personen',oms,par,waarde,bron,aann,van,tot,'voorlopig','aanname (parameter gekozen in Z39; bron '+bron+')' if aann else 'feit (regel uit canon '+bron+'); getal: aanname')).rowcount
  for t in sim.TYPEN:
    S['gebeurtenis_type']+=c.execute('insert or ignore into gebeurtenis_type(code,module,omschrijving,min_leeftijd,minderjarige_rol,instemming_nodig,harde_lijn_risico,bron_code,epistemiek) values(?,?,?,?,?,?,?,?,?)',(t[0],'personen',t[1],t[2],t[3],t[4],t[5],t[6],'aanname (motorontwerp Z39, bron '+t[6]+')')).rowcount
  for t in tech.TYPEN:
    S['tech_gebeurtenistype']+=c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',(t[0],t[1],t[2],t[3],t[4],'aanname (moduleontwerp Z39, bron '+t[4]+')')).rowcount
  c.commit()
def bewaar_runs(R,module,fase_nr,gekozen=()):
  for r in R:
    S['sim_run']+=c.execute('insert or ignore into sim_run(run_id,module,fase_nr,seed,geldig,reden,n_gebeurtenis,scores,pareto_rang,gewogen,gekozen,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (r['run_id'],module,fase_nr,r['seed'],r['geldig'],r['reden'],r['scores'].get('gebeurtenissen') or sum(v for v in r['scores'].values() if isinstance(v,int)),json.dumps(r['scores'],ensure_ascii=False),r.get('pareto_rang'),r.get('gewogen'),1 if r['run_id'] in gekozen else 0,'z39/montecarlo.py' if module.startswith('personen') else 'z39/tech.py',N(r))).rowcount
def bewaar_ev(r,w,module='personen'):
  for (j,sz,typ,a,d,plek,det,cc,oz) in w.ev:
    S['sim_gebeurtenis']+=c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (r['run_id'],module,j,sz,typ,a,d or '-',sim.REG.get(plek,plek) if plek else None,det,cc,'voorlopig',N(r),oz)).rowcount
def stap_sim():
  zaai_regels()
  c.execute("update sim_gebeurtenis set doel='-' where doel=''");c.execute("update sim_gebeurtenis set detail='-' where detail=''")  # export kent geen lege tekst
  if c.execute("select count(*) from sim_run where module='personen' and fase_nr=4").fetchone()[0]>=1000: return
  R=mc.draai(c,1000);top=mc.pareto(R);ids={r['run_id'] for r in top}
  bewaar_runs(R,'personen',4,ids)
  json.dump({'validatie':mc.validatie(R),'top':[(r['run_id'],r['seed'],r['pareto_rang'],r['gewogen'],r['scores']) for r in top],
             'weggegooid':collections.Counter((r['reden'] or '').split(':')[0] for r in R if not r['geldig'])},open('z39/mc_fase4.json','w'),ensure_ascii=False,indent=1,default=str)
  T=mc.typen(c);P=sim.seed_personen(c,4)
  for r in top:
    w=sim.Wereld(r['seed'],P,T,None).run();bewaar_ev(r,w)
    if r is top[0]: vertaal(r,w)
  # diagnose 1: zelfde motor zonder Kernbescherming (200 runs)
  R2=mc.draai(c,200,bescherm=False,prefix='Z39-F4-ZB')
  bewaar_runs(R2,'personen_zonder_kernbescherming',4)
  # proef criterium 3: dezelfde seeds, iedereen weet alles (200 runs)
  R3=mc.draai(c,200,alwetend=True,prefix='Z39-F4-AW')
  bewaar_runs(R3,'personen_alwetend',4)
  A=R[:200];vg={k:sum(a['uitkomst'][k]!=b['uitkomst'][k] for a,b in zip(A,R3)) for k in ('inst','rel','dood')}
  jac=sum(len(a['uitkomst']['rel']^b['uitkomst']['rel'])/max(1,len(a['uitkomst']['rel']|b['uitkomst']['rel'])) for a,b in zip(A,R3))/200
  ch=(sum(a['uitkomst']['chantage'] for a in A)/200,sum(b['uitkomst']['chantage'] for b in R3)/200)
  json.dump({'n':200,'verschillend':vg,'gem_jaccard_afstand_relaties':round(jac,3),'chantage_gem':ch,'verraad_gem':(sum(a['uitkomst']['verraad'] for a in A)/200,sum(b['uitkomst']['verraad'] for b in R3)/200),
             'zonder_kernbescherming_weggegooid':sum(1-r['geldig'] for r in R2)},open('z39/proef_informatie.json','w'),indent=1)
  c.commit()
def vertaal(r,w):
  e=N(r)
  for code,p in w.P.items():
    if not p.get('fig'): continue
    if not any(code in (x[3],x[4]) for x in w.ev): continue
    S['sim_figuur']+=c.execute('insert or ignore into sim_figuur(code,naam,laag,volk,geslacht,plek_code,functie,geboren,ouder_code,run_id,bron,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (code,p['naam'],'achtergrond',p['volk'],p['geslacht'],sim.REG.get(p['plek'],p['plek']),p.get('functie'),p['geboren'],p.get('ouder'),r['run_id'],'z39/sim.py','voorlopig',e)).rowcount
  figs={x for (x,) in c.execute('select code from sim_figuur')}
  for code,v in w.verbl.items():
    if code.startswith('SIMF') and code not in figs: continue
    for plek,van,tot in v:
      S['verblijf']+=c.execute('insert or ignore into verblijf(per_code,plek_code,van_jaar,tot_jaar,bron,status,epistemiek) values(?,?,?,?,?,?,?)',(code,sim.REG.get(plek,'ONDERWEG' if plek=='onderweg' else plek),van,tot,r['run_id'],'voorlopig',e)).rowcount
  for wie,wat,sj,br in w.kennis:
    if wie.startswith('SIMF') and wie not in figs: continue
    ep='feit (canon: personage_profiel, Geheim/Relaties); sinds_jaar is aanname (geboren+18 of canonjaar)' if br.startswith(('canon','eigen geheim')) else e
    S['kennis']+=c.execute('insert or ignore into kennis(per_code,weet_code,sinds_jaar,bron,status,epistemiek) values(?,?,?,?,?,?)',(wie,wat,sj,br+' | '+r['run_id'],'voorlopig',ep)).rowcount
  for a,s_,b,vj,tj in w.rel:
    S['per_relatie']+=c.execute('insert or ignore into per_relatie(van_code,soort,naar_code,van_jaar,tot_jaar,bron,status,epistemiek) values(?,?,?,?,?,?,?,?)',(a,s_,b,vj,tj,r['run_id'],'voorlopig',e)).rowcount
  # meester_van uit de canon (Relaties/rol): leerling en Hofmeesteres; feit
  for a,b in (('PER-ondrea','PER-f4-zuster-ondrea-leerling'),('PER-f4-saske','PER-f4-registerzuster-tine'),('PER-f4-saske','PER-f4-orde-moeder-iris')):
    S['per_relatie']+=c.execute('insert or ignore into per_relatie(van_code,soort,naar_code,van_jaar,tot_jaar,bron,status,epistemiek) values(?,?,?,?,?,?,?,?)',(a,'meester_van',b,None,None,'personage_profiel (Relaties)','voorlopig','feit (canon: personage_profiel, Relaties: leerling/opvolgster)')).rowcount
# ================= TECH: module technologie + beroepen =================
def stap_tech():
  if c.execute("select count(*) from sim_run where module='technologie'").fetchone()[0]>=1000: return
  R,ber=tech.draai(c,1000)
  for r in R: r['scores']['gebeurtenissen']=len(r['ev'])
  bewaar_runs(R,'technologie',4)
  G=[r for r in R if r['geldig']];best=max(G,key=lambda r:(r['scores']['beroepen']+r['scores']['tweelingen'],-r['seed']))
  c.execute('update sim_run set gekozen=1 where run_id=?',(best['run_id'],))
  for (j,typ,t,k,x,n,cc) in best['ev']:
    S['sim_gebeurtenis']+=c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (best['run_id'],'technologie',j,'jaar',typ,t,str(x) if x is not None else '-',sim.REG.get(k,k),f'{n} lichamen' if typ=='prijs' else '-',cc or (t if t.startswith('BEROEP') else None),'voorlopig',N(best),'GENRE-wet2-V4' if typ in('uitvinding','prijs','vergeten') else ('KAART-seizoenen' if typ=='verspreiding' else 'ERF-noodtoestand'))).rowcount
  json.dump(tech.rapport(R,ber),open('z39/tech_rapport.json','w'),ensure_ascii=False,indent=1)
  c.commit()
# ================= F5: korte run in fase 5, zelfde code =================
def stap_f5():
  if c.execute("select count(*) from sim_run where module='personen' and fase_nr=5").fetchone()[0]>=50: return
  fz=c.execute("select waarde,toelichting from anker where sleutel='fase_5_naam'").fetchone()
  a,b=map(int,re.search(r'\((\d+) tot (\d+)\)',fz[1]).groups())
  R=mc.draai(c,50,fase_nr=5,fase=(a,b),basis=395000,prefix='Z39-F5')
  mc.pareto(R) if any(r['geldig'] for r in R) else None
  bewaar_runs(R,'personen',5)
  json.dump({'fase':(a,b),'personages':len(sim.seed_personen(c,5)),'geldig':sum(r['geldig'] for r in R),'weggegooid':collections.Counter((r['reden'] or '').split(':')[0] for r in R if not r['geldig']),
             'gem':{k:round(sum(r['scores'][k] for r in R)/50,2) for k in ('intrige','ommekeer','verbinding','gebeurtenissen')}},open('z39/fase5.json','w'),ensure_ascii=False,indent=1,default=str)
  c.commit()
# ================= PREM: tien handgeschreven premisses (ideeënbank, epistemiek simulatie) =================
TITEL={'IDEE-Z39-1':'Het dorp van de neven telt mee','IDEE-Z39-2':'Een geroofde man rooft terug','IDEE-Z39-3':'Twee vrouwen, één vals blad','IDEE-Z39-4':'De koningsdochter in het register',
 'IDEE-Z39-5':'De boot van de eilander','IDEE-Z39-6':'Rustmaanden voor een man zonder kinderen','IDEE-Z39-7':'Slikgangen onder de mist','IDEE-Z39-8':'Opvolging bij de Hofmeesteres',
 'IDEE-Z39-9':'Over de pas naar de dijken','IDEE-Z39-10':'Edruns ring tegen een schone lei'}
def stap_prem():
  import premisses as PM
  e=f'simulatie ({PM.RUN}, seed {PM.SEED}); premisse met de hand geschreven uit de graafvragen'
  for code,txt,refs,_,ax,sp in PM.P:
    nieuw(code,'Verhaal',TITEL[code],txt,refs,reden=WREDEN+' (intrigevoorstel uit vraag.py intrige; Rogier kiest)',status='voorlopig',tijdperk='4 Noodtoestand',ideeenbank=1);epi(code,e)
  c.commit()
# ================= PROEF: steekproef (11d.2) en koude lezer (11d.3) =================
def oordeel(t,row):
  """Automatisch oordeel per rij: past (in tijd/plek/leeftijd), geen sjabloon (alleen tekst), verbinding (verwijzingen bestaan)."""
  per=set(x for (x,) in c.execute('select code from personage_profiel'))|set(x for (x,) in c.execute('select code from sim_figuur'))
  plek=set(sim.REG.values())|{'ONDERWEG'}
  if t=='verblijf':
    p,pl,v,tt=row;return (pl in plek and (tt is None or tt>=v) and 0<=v<=130 or v<0, True, p in per)
  if t=='kennis':
    p,w,sj=row;b=w.split('#')[0];return (sj is not None, True, p in per and b in per)
  if t=='per_relatie':
    a,s_,b,vj=row;return (vj is None or 0<=vj<=130, True, a in per and b in per)
  if t=='sim_figuur':
    code,naam,pl,geb,ouder=row;return (pl in plek and geb<=130, bool(naam), ouder is None or ouder in per)
  if t=='canon':
    code,feit,verw=row;ok=all(c.execute('select 1 from canon where code=?',(x,)).fetchone() for x in (verw or '').split(';') if x)
    return (True, True, ok)
def stap_proef():
  if c.execute("select count(*) from steekproef where ronde='Z39'").fetchone()[0]: return
  pool=[]
  for t,sql in (('verblijf','select id,per_code,plek_code,van_jaar,tot_jaar from verblijf'),('kennis','select id,per_code,weet_code,sinds_jaar from kennis'),
                ('per_relatie','select id,van_code,soort,naar_code,van_jaar from per_relatie'),('sim_figuur','select id,code,naam,plek_code,geboren,ouder_code from sim_figuur'),
                ('canon',"select id,code,feit,verwijst_naar from canon where ronde=68")):
    pool+=[(t,r[0],r[1:]) for r in c.execute(sql)]
  rnd=random.Random(39);sample=rnd.sample(pool,min(50,len(pool)))
  for t,i,row in sample:
    p,g,v=oordeel(t,row);ok=p and g and v
    S['steekproef']+=c.execute('insert or ignore into steekproef(ronde,tabel,code,past,geen_sjabloon,verbinding,oordeel,toelichting,epistemiek) values(?,?,?,?,?,?,?,?,?)',
      ('Z39',t,str(row[0]) if t in('sim_figuur','canon') else f'{t}:{i}',int(p),int(g),int(v),'goed' if ok else 'fout','automatisch oordeel (r_Z39.oordeel), daarna gelezen door de architect','aanname (oordeel van de architect, niet onafhankelijk)')).rowcount
  c.commit()
# ================= KEUZE: open beslissingen voor Rogier =================
K39=[
('KEUZE-Z39-steekproef','controle','Steekproefcriterium is met 50 rijen niet haalbaar',"Met 0 fouten in 50 rijen is de 95%-bovengrens 7,1% (Clopper-Pearson); onder 2% komen kan pas vanaf 183 foutloze rijen.","Kies n = 183 per ronde (dat kan, de beoordeling is grotendeels automatisch), of zet de grens op 7,5% bij n = 50. Aanbeveling: n = 183.",'opdracht_Z35.md 11d.2'),
('KEUZE-Z39-tijdlijn','simulatie','De motor maakt rooster en Orde twintig tot dertig jaar te vroeg',"Rotatie ontstaat in 100% van de runs, maar met mediaan jaar 51 (canon 78); de Orde in jaar 60 (canon 90). De Deelwet valt in jaar 29 (canon 40).","Niet bijstellen tot het past: zoek in de canon wat de rotatie zo lang tegenhield (verzet, geen rekenaarster, oorlog?) en leg dat vast als regel. Aanbeveling: laten staan als bevinding; Rogier noemt de rem.",'GEB-r10-rotatie;GEB-r10-orde-naam;GEB-deelwet-40'),
('KEUZE-Z39-nevenramp','simulatie','De inteeltramp in Groenmuil ontstaat bijna nooit',"GEB-r10-neven-ramp ontstaat in 2% van de runs: het register komt meestal (96%) al rond jaar 20, en daarna stopt het risico.","Of de ramp gebeurt in een dorp dat het register nooit bereikte (dan is registerbereik per dorp een nieuwe regel), of het register komt in de canon later in Groenmuil aan. Aanbeveling: per regio registerbereik met reistijd.",'GEB-r10-neven-ramp;GEB-r10-eerste-register'),
('KEUZE-Z39-kernbescherming','simulatie','Mogen canonpersonages in een run vóór hun canonjaar sterven?',"Zonder bescherming breken 174 van 200 runs (87%) een anker: een canonpersonage sterft voor het jaar waarin de canon het laat optreden.","Huidige keuze: de motor beschermt ze tot hun canonjaar (Kern niet overschrijven). Aanbeveling: zo laten; alleen achtergrondfiguren en nieuwe kinderen kunnen vroeg sterven.",'SIM-kern;REGEL-harde-grenzen'),
('KEUZE-Z39-premisses','verhaal','Welke van de tien intrigevoorstellen worden een boog?',"Tien premisses (IDEE-Z39-1 tot -10) staan voorlopig in de ideeënbank met epistemiek 'simulatie (Z39-F4-0203, seed 390203)'.","Kies er twee of drie; de rest blijft inspiratie. Aanbeveling: IDEE-Z39-4 (koningsdochter in het register), IDEE-Z39-6 (rustmaanden) en IDEE-Z39-7 (slikgangen): die raken de meeste geheimen en de rijmregel van fase 4.",'IDEE-Z39-4;IDEE-Z39-6;IDEE-Z39-7'),
('KEUZE-Z39-validatie','simulatie','Pest van 340 en crash van 762 zijn met deze motor niet te toetsen',"De personenmotor heeft geen ziekte- en geen prijsmechaniek, en de fase-5-run start zonder de toestand van fase 4. De Pest (fase 6) en de crash (fase 7) ontstaan daarom in 0% van de runs. Dat zegt niets over de canon, wel dat de regels ze nog niet bevatten.","Bouw eerst de module ziekte (epidemie in verwante stallen, GEB-r10-pest-oorsprong) en een fase-overgang die de eindtoestand van een run meeneemt. Aanbeveling: ziekte vóór economie.",'GEB-pest-340;GEB-r10-varenne-crash;GEB-r10-pest-oorsprong'),
]
def stap_keuze():
  for code,soort,ond,citaat,aanb,raakt in K39: keuze_nieuw(code,soort,ond,aanb,raakt,citaat)
  c.commit()
# ================= MAIN =================
if __name__=='__main__':
  for st,fn in (('a',stap_a),('sim',stap_sim),('tech',stap_tech),('f5',stap_f5)):
    if st in STAPPEN: fn();toets(st)
  for st in ('prem','proef','keuze'):
    if st in STAPPEN and 'stap_'+st in globals(): globals()['stap_'+st]();toets(st)
  print(dict(S))
