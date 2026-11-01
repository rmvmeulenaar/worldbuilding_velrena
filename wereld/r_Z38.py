# Ronde Z38: Rogiers besluiten A1-A10, herkomst in lagen (B1), premissen met de hand (B2), ideeënbank (B3), rijkdom mens 801 (C).
# Idempotent en additief: niets verwijderd; roman niet aangeraakt; toets.py na elke stap (exit 0 vereist). Gebruik: DB=kopie.db python3 r_Z38.py [stappen]
import sqlite3,shutil,os,re,json,sys,collections,subprocess
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z38'),os.path.join(W,'z37'),os.path.join(W,'z36')]
import afgeleid,migreer
import importlib.util as _iu
def _laad(naam,pad):
  s=_iu.spec_from_file_location(naam,pad);m=_iu.module_from_spec(s);s.loader.exec_module(m);return m
D=_laad('d38',os.path.join(W,'z38','data.py'));PR=_laad('p38',os.path.join(W,'z38','premisses.py'));RD38=_laad('r38',os.path.join(W,'z38','rijkdom_data.py'))
DT='2026-11-01';RD='Z38';RN=67;DB=os.environ.get('DB','canon.db')
STAPPEN=sys.argv[1:] or ['a','b1','b2','b3','c']
if DB=='canon.db' and not os.path.exists('canon_backup_Z38.db'): shutil.copy('canon.db','canon_backup_Z38.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
REDEN='Ronde Z38: besluit van '+D.R
WREDEN='Ronde Z38: voorstel van de architect, voorlopig (OPDRACHT_architect_Z38.md, bevestigd door '+D.R+')'
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z38.py')).rowcount
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
  if b and 'Opgelost in Z38' not in (b[0] or ''): zet('wrijving','code',code,'beschrijving',(b[0] or '')+' Opgelost in Z38: '+hoe)
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
  c.execute('insert into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',(code,soort,ond,aanb,raakt,'open','r_Z38.py',citaat))
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
# ================= A: Rogiers besluiten =================
def stap_a():
  for code,cat,ond,feit,verw,kern in D.BESLUIT: nieuw(code,cat,ond,feit,verw,kern=bool(kern))
  # A1: bron van de vijf Kern-rijen
  for k in D.KERN5: zet('canon','code',k,'bron_handmatig',D.BRON_A1)
  # A3: ankerrij + anker, gave-rijen verwijzen ernaar
  a=D.ANKER;nieuw(a[0],a[1],a[2],a[3],a[4],kern=True)
  s,w,b,t=D.ANKER_RIJ
  if not c.execute('select 1 from anker where sleutel=?',(s,)).fetchone():
    c.execute('insert into anker(sleutel,waarde,bron_code,toelichting,patroon) values(?,?,?,?,?)',(s,w,b,t,None));S['anker_nieuw']+=1;wijz('ANKER-'+s,'toegevoegd','anker',None,w)
  for oud in D.GAVE_RIJEN:
    r=c.execute('select feit,status,vervangen_door from canon where code=?',(oud,)).fetchone()
    if not r: continue
    nc=oud+'-Z38'
    if r[1] in('vastgesteld','voorlopig') or bestaat(nc):
      opvolger(oud,nc,voeg_in(r[0],'De getallen 1 op 100, 1 op 20 en 1 op 2000 staan in GAVE-VERHOUDINGEN-Z38 (één bron per feit, BESLUIT-Z38-3).'),'GAVE-VERHOUDINGEN-Z38',REDEN+' (A3: verwijzing naar de ankerrij)')
  # wrijvingen en keuzes
  sluit_wrij('WRIJ-Z37-1','jaar 85 is het jaar waarin het register het patroon ziet; een ontdekkingsscène (BESLUIT-Z38-2).')
  sluit_wrij('WRIJ-Z37-2','drie getallen met elk een betekenis in één ankerrij GAVE-VERHOUDINGEN-Z38 (BESLUIT-Z38-3); de geslachtsverhouding 1 op 20 staat apart in WRIJ-Z38-1.')
  sluit_wrij('WRIJ-Z33-7','REGEL-harde-grenzen kreeg in Z37 BESLUIT-Z30-4; de andere vijf kregen in Z38 de bron auteur (Rogier), wereldbijbel, ronde onbekend (BESLUIT-Z38-1).')
  keuze('KEUZE-WRIJ-Z37-1','besloten','[Z38: BESLUIT-Z38-2]');keuze('KEUZE-WRIJ-Z37-2','besloten','[Z38: BESLUIT-Z38-3]');keuze('KEUZE-WRIJ-Z33-7','besloten','[Z38: BESLUIT-Z38-1]')
  keuze('KEUZE-WRIJ-Z34-2','besloten','[Z38: per boog, als die boog aan de beurt is (BESLUIT-Z38-5); de wrijving blijft open als werklijst.]')
  keuze('KEUZE-WRIJ-Z29-1','open','[Z38: blijft open, de roman beslist (BESLUIT-Z38-4).]')
  for code,titel,besch,verw in D.WRIJ_NIEUW: wrij_nieuw(code,titel,besch,verw)
  # A9: harde regel feeënafspraak
  f=D.FEE_REGEL;nieuw(f[0],f[1],f[2],f[3],f[4],kern=True)
  regel_nieuw('R-fee_afspraak','harde lijn','Een feeënafspraak gaat nooit over seks (BESLUIT-Z38-9, uitwerking BESLUIT-Z30-4): levende FEE-rijen en rijen die een feeënafspraak beschrijven, mogen geen niet-ontkend seksueel woord bevatten.','py:fee_afspraak','BESLUIT-Z38-9; BESLUIT-Z30-4','fout')
  # A7: Wil voor de twintig meest gebruikte dragers; de opvolger staat meteen in personage_profiel
  for oud,wil in D.WIL.items():
    r=c.execute('select feit from canon where code=?',(oud,)).fetchone()
    if not r: continue
    nc=oud+'-Z38'
    if not bestaat(nc): profiel_opvolger(oud,nc,voeg_in(r[0],f'Wil: {wil} (BESLUIT-Z38-7).'),REDEN+' (A7: Wil uit de eigen rij afgeleid)')
    for (vp,) in c.execute('select code from verhaal_profiel where drager=?',(oud,)).fetchall(): zet('verhaal_profiel','code',vp,'drager',nc)
  c.execute("update canon set verwijst_naar=null where ronde=? and verwijst_naar=''",(RN,));c.execute("update canon set hangt_samen_met=null where ronde=? and hangt_samen_met=''",(RN,))
  # ankers volgen hun opvolger; Kern-besluiten die al op deze Kleur-rijen leunden, blijven bekende bevinding onder WRIJ-Z33-2
  for s_,b_ in c.execute('select sleutel,bron_code from anker').fetchall():
    if b_ in D.GAVE_RIJEN and bestaat(b_+'-Z38'): zet('anker','sleutel',s_,'bron_code',b_+'-Z38','ANKER-'+s_)
  afgeleid.bouw(c)
  for k,x in c.execute("select r.van_code,r.naar_code from relatie r join canon a on a.code=r.van_code join canon b on b.code=r.naar_code where a.draagkracht='Kern' and b.draagkracht='Kleur' and a.status in('vastgesteld','voorlopig')").fetchall():
    if x not in D.GAVE_RIJEN: continue
    st=c.execute('select status from canon where code=?',(x,)).fetchone()[0];det=f'Kern leunt op Kleur: {x} ({st})'
    if not c.execute('select 1 from toets_uitzondering where toets=? and code=? and detail=?',('kern_leunt_op_kleur',k,det)).fetchone():
      c.execute('insert into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',('kern_leunt_op_kleur',k,det,'Z38 A3: oud besluit verwijst naar een gave-rij die nu een opvolger heeft (bekend, WRIJ-Z33-2)','WRIJ-Z33-2'));S['uitzondering_nieuw']+=1
  zonder_bron()
  c.commit()
def zonder_bron():
  w=[x for x in D.WRIJ_NIEUW if x[0]=='WRIJ-Z38-2'][0];codes=w[3].split(';')[:2]
  for code,bs in c.execute("select code,bron_soort from canon where draagkracht='Kern' and status in('vastgesteld','voorlopig') and coalesce(bron,'onbekend')='onbekend'").fetchall():
    if code in codes and not c.execute('select 1 from toets_uitzondering where toets=? and code=? and detail=?',('kern_zonder_bron',code,'Kern zonder bron: '+bs)).fetchone():
      c.execute('insert into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',('kern_zonder_bron',code,'Kern zonder bron: '+bs,'Z38 B1: C1-keten zonder gedeelde waarde; bron moet van Rogier komen','WRIJ-Z38-2'));S['uitzondering_nieuw']+=1;wijz(code,'toegevoegd','toets_uitzondering',None,'kern_zonder_bron')
# ================= B1: herkomst in lagen =================
def stap_b1():
  afgeleid.bouw(c)  # afgeleid_motor.herkomst schrijft bron, context en herkomst_laag (BESLUIT-Z38-11)
  w=[x for x in D.WRIJ_NIEUW if x[0]=='WRIJ-Z38-2'][0];codes=w[3].split(';')[:2]
  for code,bs in c.execute("select code,bron_soort from canon where draagkracht='Kern' and status in('vastgesteld','voorlopig') and coalesce(bron,'onbekend')='onbekend'").fetchall():
    if code in codes and not c.execute('select 1 from toets_uitzondering where toets=? and code=? and detail=?',('kern_zonder_bron',code,'Kern zonder bron: '+bs)).fetchone():
      c.execute('insert into toets_uitzondering(toets,code,detail,reden,wrijving) values(?,?,?,?,?)',('kern_zonder_bron',code,'Kern zonder bron: '+bs,'Z38 B1: C1-keten zonder gedeelde waarde; bron moet van Rogier komen','WRIJ-Z38-2'));S['uitzondering_nieuw']+=1;wijz(code,'toegevoegd','toets_uitzondering',None,'kern_zonder_bron')
  keuze_nieuw('KEUZE-WRIJ-Z38-2','herkomst','Twee Kern-rijen zonder bron na B1','Noem per rij een bron, of wijs de wereldbijbel aan zoals bij A1. Tot dan bekende bevinding van R-kern_zonder_bron.','GES-officiele-versie;EROS-GRENZEN-Z7',w[2])
  keuze_nieuw('KEUZE-WRIJ-Z38-1','canon','"1 op 20" als geslachtsverhouding',"Laten staan; bij een herschrijving 'geslachtsverhouding 1 op 20' schrijven, zodat het niet met de gave-kans (GAVE-VERHOUDINGEN-Z38) verward wordt.",'UIT-VOLK-saelmor;GESCH-sael-mor-1;ZINT-Z5-seksualiteit-11;BESLUIT-Z32-11',D.WRIJ_NIEUW[0][2])
  c.commit()
# ================= B2: premissen met de hand =================
def groepen():
  P=c.execute("select code,drager,erf_code,marginale_winst from verhaal_profiel").fetchall()
  naam={}
  for code,d,e,m in P:  # zelfde persoon onder twee codes (PER- en PERS-Z4-rij, of een opvolger)
    if d:
      r=c.execute('select naam from personage_profiel where code=?',(d,)).fetchone()
      naam[d]=(r[0].split()[0].lower() if r and r[0] else d)
  g=collections.defaultdict(list)
  for code,d,e,m in P:
    if d: g[(naam[d],e)].append((m or 0,code))
  keep={};ret={}
  for k,l in g.items():
    l.sort(key=lambda x:(-x[0],x[1]));keep[l[0][1]]=k
    for _,x in l[1:]: ret[x]=l[0][1]
  return keep,ret
def stap_b2():
  regel_nieuw('R-premisse_vorm','verhaal','Een premisse is met de hand geschreven (BESLUIT-Z38-12): fout bij meer dan 50% gedeelde woord-3-grepen met een andere premisse, een fasenaam of ERF-label letterlijk als hindernis, of de invulmarkers van het oude sjabloon.','py:premisse_vorm','BESLUIT-Z38-12','fout')
  keep,ret=groepen()
  for x,k in ret.items():
    zet('verhaal_profiel','code',x,'vervangen_door',k);zet('verhaal_profiel','code',x,'uitslag','samengevoegd');zet('verhaal_profiel','code',x,'status','vervangen')
  for code,d,e,rg,zd in c.execute('select code,drager,erf_code,wereldregel_code,zaadje_code from verhaal_profiel').fetchall():
    if code in ret: continue
    if code in PR.P:
      zet('verhaal_profiel','code',code,'premisse',PR.P[code]);zet('verhaal_profiel','code',code,'premisse_codes',';'.join(x for x in (d,e,rg,zd) if x))
    elif not d: zet('verhaal_profiel','code',code,'premisse','geen premisse: geen drager (nieuw personage nodig)');zet('verhaal_profiel','code',code,'premisse_codes',None)
    else: zet('verhaal_profiel','code',code,'premisse','geen premisse: de rijen dragen er geen (BESLUIT-Z38-12)');zet('verhaal_profiel','code',code,'premisse_codes',None)
  S['b2_behouden']=len(keep);S['b2_samengevoegd']=len(ret)
  c.commit()
# ================= B3: ideeënbank =================
def stap_b3():
  import ideeen38
  S.update({'b3_'+k:v for k,v in ideeen38.verwerk(c).items()});c.commit()
# ================= C: rijkdom mens 801 =================
def stap_c():
  for code,dom,v in RD38.EXTRA: S['competentievraag']+=c.execute('insert or ignore into competentievraag(code,domein_code,vraag,volk) values(?,?,?,?)',(code,dom,v,'mens')).rowcount
  VR=collections.defaultdict(list)
  for code,dom in c.execute("select code,domein_code from competentievraag where volk is null or volk='mens'"): VR[dom].append(code)
  for regio,dom,tekst,verw in RD38.R:
    code=f'RIJK-Z38-mens-{regio}-{dom}'
    nieuw(code,'Dagelijks leven',f'Mens in {regio.capitalize()}, 801: {dom}',tekst,verw,reden=WREDEN+' (C, rijkdom mens 801; beantwoordt de competentievragen van domein '+dom+' voor '+regio+')',status='voorlopig',tijdperk='801 Heden',jaar=801)
    for q in VR[dom]: S['competentie_antwoord']+=c.execute('insert or ignore into competentie_antwoord(vraag_code,volk,fase_nr,antwoord_code,regio) values(?,?,?,?,?)',(q,'mens',801,code,regio)).rowcount
  code,tekst,verw=RD38.HALLOWYN
  nieuw(code,'Dagelijks leven','Een dag in Hallowyn: wie Liora tegenkomt',tekst,verw,reden=WREDEN+' (C, beroepen uit Z37 in het dagelijks leven)',status='voorlopig',tijdperk='801 Heden',jaar=801)
  for q in VR['werk']: S['competentie_antwoord']+=c.execute('insert or ignore into competentie_antwoord(vraag_code,volk,fase_nr,antwoord_code,regio) values(?,?,?,?,?)',(q,'mens',801,code,'ambergaard')).rowcount
  c.execute("update canon set verwijst_naar=null where ronde=? and verwijst_naar=''",(RN,))
  c.commit()
def klaar_c():
  nq=c.execute("select count(*) from competentievraag where volk is null or volk='mens'").fetchone()[0]
  return {r:(c.execute("select count(distinct vraag_code) from competentie_antwoord where volk='mens' and fase_nr=801 and regio=?",(r,)).fetchone()[0],nq) for r in ('ambergaard','saelith','brakhaven','zoutkust')}
# ================= MAIN =================
if __name__=='__main__':
  if 'a' in STAPPEN: stap_a();toets('A besluiten')
  if 'b1' in STAPPEN: stap_b1();toets('B1 herkomst')
  if 'b2' in STAPPEN: stap_b2();toets('B2 premissen')
  if 'b3' in STAPPEN: stap_b3();toets('B3 ideeënbank')
  if 'c' in STAPPEN: stap_c();toets('C rijkdom');print('klaar-als C:',klaar_c())
  print(dict(S))
