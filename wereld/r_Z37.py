# Ronde Z37: Rogiers besluiten A-C (stap 0), machine herstellen (D1), personage_profiel als bron (D2), rijkdom (D3). Idempotent en additief.
# Niets verwijderd; roman niet aangeraakt; toets.py na elke stap (exit 0 vereist). Gebruik: DB=kopie.db python3 r_Z37.py [stappen]
import sqlite3,shutil,os,re,json,sys,collections,subprocess
W=os.path.dirname(os.path.abspath(__file__));os.chdir(W);sys.path[:0]=[W,os.path.join(W,'migraties'),os.path.join(W,'z37'),os.path.join(W,'z36')]
import afgeleid,migreer
import importlib.util as _iu
def _laad(naam,pad):
  s=_iu.spec_from_file_location(naam,pad);m=_iu.module_from_spec(s);s.loader.exec_module(m);return m
D=_laad('d37',os.path.join(W,'z37','data.py'))
DT='2026-11-01';RD='Z37';RN=66;DB=os.environ.get('DB','canon.db')
STAPPEN=sys.argv[1:] or ['0','d1','d2','d3']
if DB=='canon.db' and not os.path.exists('canon_backup_Z37.db'): shutil.copy('canon.db','canon_backup_Z37.db')
c=sqlite3.connect(DB);migreer.draai(c)
S=collections.Counter()
REDEN='Ronde Z37: besluit van '+D.R
def wijz(code,soort,veld,oud,nieuw):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',None if oud is None else str(oud),str(nieuw),DT,'r_Z37.py')).rowcount
def toets(stap):
  afgeleid.bouw(c);c.commit()
  r=subprocess.run([sys.executable,'toets.py',DB,'--json',f'/tmp/toets_{RD}.json'],capture_output=True,text=True)
  print(f'[{stap}] toets exit {r.returncode}: '+' | '.join(l for l in r.stdout.splitlines()[1:4]))
  if r.returncode: print(r.stdout[-5000:]);sys.exit(f'toets faalt na {stap}')
def bestaat(code): return c.execute('select 1 from canon where code=?',(code,)).fetchone() is not None
def nieuw(code,cat,ond,feit,verw,reden=REDEN,status='vastgesteld',kern=False,tijdperk=None,jaar=None,ideeenbank=0):
  if bestaat(code): return 0
  def lev(x):
    for _ in range(6):
      r=c.execute('select status,vervangen_door from canon where code=?',(x,)).fetchone()
      if not r: return None  # alleen canoncodes in verwijst_naar (boog/zaadje staan in beroep.verbinding en in de tekst)
      if r[0] in('vastgesteld','voorlopig') or not r[1] or r[1].startswith('personage_profiel:'): return x
      x=r[1]
    return x
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
  if b and 'Opgelost in Z37' not in (b[0] or ''): zet('wrijving','code',code,'beschrijving',(b[0] or '')+' Opgelost in Z37: '+hoe)
def wrij_nieuw(code,titel,besch,verw):
  if c.execute('select 1 from wrijving where code=?',(code,)).fetchone(): return
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(titel,verw.replace(';',', '),besch,'canon','open',code,verw))
  S['wrijving_nieuw']+=1;wijz(code,'toegevoegd','wrijving',None,'open')
def keuze(code,status,aanb_extra=None):
  r=c.execute('select aanbeveling from keuze where code=?',(code,)).fetchone()
  if not r: return
  if aanb_extra and aanb_extra not in (r[0] or ''): zet('keuze','code',code,'aanbeveling',(r[0] or '')+' '+aanb_extra)
  zet('keuze','code',code,'status',status)
def per_opvolger(oud,nieuw_code,subs,extra,reden):
  r=c.execute('select categorie,onderwerp,feit,verwijst_naar,status,tijdperk,jaar,vervangen_door from canon where code=?',(oud,)).fetchone()
  if not r: return
  if (r[7] or '').startswith('personage_profiel:'): return profiel_opvolger(oud,nieuw_code,subs,extra)
  f=r[2]
  for a,b in subs:
    assert a in f,(oud,a);f=f.replace(a,b)
  f=re.sub(r'(Label: )',extra+' \\1',f,count=1) if 'Label: ' in f else f.rstrip()+' '+extra
  nieuw(nieuw_code,r[0],r[1],f,(r[3] or '')+';BESLUIT-Z37-5',reden=reden,status=r[4],tijdperk=r[5],jaar=r[6]);vervang(oud,nieuw_code)
def per_b():
  """B-personages (Ardemar, Selvara): na D2, zodat de nieuwe PER-rijen meteen in personage_profiel landen."""
  per_opvolger('PER-ardemar','PER-ardemar-iv-Z37',[('Naam: Koning Ardemar de Graanvorst.','Naam: Koning Ardemar IV de Graanvorst.')],'Erfnaam: draagt de naam van Ardemar III, als kleinzoon (BESLUIT-Z37-5, WRIJ-Z32-1).',REDEN+' (B, WRIJ-Z32-1)')
  per_opvolger('PER-f1-ardemar-derde','PER-f1-ardemar-derde-Z37',[('jaar -270 (geboren ca. -300)','jaar -290 (geboren ca. -330)')],'Jaar -290 omdat hij in -285 sterft (GEB-r10-ardemar-val); geboortejaar mee verschoven, anders was hij als heer van de harem tien (Z37, ter controle bij Rogier).',REDEN+' (B, WRIJ-Z32-1)')
  per_opvolger('PER-f6-selvara-jong-Z32','PER-f6-selvara-eerste-Z37',[('Naam: Selvara Varenne de Jongere.','Naam: Selvara Varenne de Eerste.')],'Haar achternicht, de stichteres van de Zaadbeurs in 455 (PER-selvara), is naar haar vernoemd (BESLUIT-Z37-5, WRIJ-Z32-2).',REDEN+' (B, WRIJ-Z32-2)')
# ================= STAP 0: Rogiers besluiten A, B en C =================
def stap0():
  for code,cat,ond,feit,verw,kern in D.BESLUIT: nieuw(code,cat,ond,feit,verw,kern=bool(kern))
  # A1-A4: wrijvingen en keuze sluiten
  sluit_wrij('WRIJ-Z36-1','twee lagen (BESLUIT-Z37-1). Getoetst: 1 op 2000 volgt uit MAGIE-zaadkracht (gewoon zaad geeft weinig of niets); de rest staat in WRIJ-Z37-1 en WRIJ-Z37-2.')
  sluit_wrij('WRIJ-Z36-2','herziene passage, zaadje bijgewerkt (BESLUIT-Z37-2).')
  sluit_wrij('WRIJ-Z36-3','Hesta breekt twee keer haar eigen ruil (BESLUIT-Z37-3).')
  for code,titel,besch,verw in D.WRIJ_NIEUW: wrij_nieuw(code,titel,besch,verw)
  keuze('KEUZE-Z36-moeder','besloten','[Z37: ja, BESLUIT-Z37-4]')
  # A2: zaadje + passage-bestand (roman niet aangeraakt)
  pas=open(os.path.join(W,'z37','passage_h32.txt'),encoding='utf-8').read()
  doel=os.path.join(W,'z37','stille_modus_Z37.md')
  if not os.path.exists(doel):
    open(doel,'w',encoding='utf-8').write('# Hoofdstuk 32: herziene passage (BESLUIT-Z37-2, voorstel aan Rogier)\n\nVervangt deel 2 van stille_modus_Z36.md. Plaats: na "which was how he knew it knew.", vóór "He was building his voice." De roman zelf is NIET gewijzigd.\n\n'+pas)
  zet('zaadje','code','ZAAD-Z36-h32-protocol','wat',"Drie jaar voor de brand (jaar 28) speelt de Reckoner Thalen een protocol voor dat 'from the ground' binnenkwam via de cellen in de beveiligingsschuur, in de stem van de Mother: een filter op geboorten, alleen zonen, 'one in a hundred, give or take', slapend tot een raad bevestigt, te beëindigen met het ja van de dragers via zijn gebroken sleutel. Dezelfde nacht gaan de cellen stil 'as if a hand had closed over them' (Hesta, BESLUIT-Z37-3); hij wist het niet en begreep het pas tien jaar later. Oogst van h7 ('Could a charge ride in a person?') en antwoord op 'Looking for what?'. Tekst: z37/stille_modus_Z37.md (BESLUIT-Z37-2).")
  zet('zaadje','code','ZAAD-Z36-h32-protocol','status','wacht op roman (Rogier)')
  # B: aanbevelingen bij de wrijvingen
  for code,oud,cat,ond,feit,verw,st in D.OPVOLG: nieuw(code,cat,ond,feit,verw,status=st);vervang(oud,code)
  # nieuw zichtbaar nu de leeftijdstoets personage_profiel leest (D2): PERS-Z4-saelmor-1-2 kopieert Nerys' oude jaren; de rij volgt het anker (zoals bij WRIJ-Z33-8)
  per_opvolger('PERS-Z4-saelmor-1-2','PERS-Z4-saelmor-1-2-Z37',[('jaar -280 (geboren ca. -310)','jaar -289 (geboren ca. -316)')],'Jaren volgen het anker nerys_geboren (PER-f1-nerys-Z32), Z37.',REDEN+' (rij volgt het anker)')
  v=D.VEE;nieuw(v[0],v[1],v[2],v[3],v[4],status='vastgesteld')
  cols=[r[1] for r in c.execute('pragma table_info(naam_markering)')]
  for a,b,codes,toel,*st in D.ERFNAMEN:
    ex=c.execute('select id,status from naam_markering where (naam_a=? and naam_b=?) or (naam_a=? and naam_b=?)',(a,b,b,a)).fetchone()
    if ex: zet('naam_markering','id',ex[0],'status',st[1] if st else 'erfnaam/echo (bewust)',code='NAAM-'+a);zet('naam_markering','id',ex[0],'toelichting',toel+' (BESLUIT-Z37-5)',code='NAAM-'+a)
    else:
      c.execute('insert into naam_markering(naam_a,naam_b,codes,soort,status,wrijving,toelichting) values(?,?,?,?,?,?,?)',(a,b,codes,st[0] if st else 'erfnaam',st[1] if st else 'erfnaam/echo (bewust)','BESLUIT-Z37-5',toel+' (BESLUIT-Z37-5)'));S['naam_markering_nieuw']+=1;wijz('NAAM-'+a,'toegevoegd','naam_markering',None,b)
  # oude open twijfel-rijen voor dezelfde personen ook als erfnaam markeren
  for nid,a,b in c.execute("select id,naam_a,naam_b from naam_markering where status='open (twijfel)'").fetchall():
    if any(x.split()[0] in a+b for x in ('Ardemar','Selvara','Iska','Hesk','Vessa')): zet('naam_markering','id',nid,'status','erfnaam/echo (bewust)',code='NAAM-'+a)
  lev=c.execute("select toelichting from levensduur where volk='aelthir'").fetchone()
  if lev and 'Vaelorn is een bewuste' not in lev[0]: zet('levensduur','volk','aelthir','toelichting',lev[0]+' Z37: Vaelorn is een bewuste uitzondering die het verhaal draagt: een geheugenhoudster die niet sterft omdat ze niet mag vergeten (BESLUIT-Z37-5, WRIJ-Z14-2).')
  for pc,per in (('PERS-anath','PER-f3-anath'),('PERS-corvina','PER-f5-corvina'),('PERS-edrun','PER-f4-edrun')):
    if bestaat(per): zet('personage','code',pc,'per_code',per)
  # REGEL-harde-grenzen: bron BESLUIT-Z30-4 (kanttekening 2)
  r=c.execute("select reden from canon where code='REGEL-harde-grenzen'").fetchone()
  if r and 'BESLUIT-Z30-4' not in (r[0] or ''): zet('canon','code','REGEL-harde-grenzen','reden',(r[0] or '').rstrip()+' [Ronde Z37: bron BESLUIT-Z30-4, aangewezen door Rogier (BESLUIT-Z37-5)]')
  # Z33-2: FASE-OVERZICHT-rijen zijn lijsten en mogen naar Kleur verwijzen
  sq=c.execute("select sql_test from regel where code='R-kern_leunt_op_kleur'").fetchone()[0]
  if 'FASE-OVERZICHT' not in sq: zet('regel','code','R-kern_leunt_op_kleur','sql_test',sq.replace("and b.draagkracht='Kleur'","and b.draagkracht='Kleur' and a.code not like 'FASE-OVERZICHT-%'"))
  HOE={'WRIJ-Z14-1':'erfnaam Varnath II (naam_markering).','WRIJ-Z14-2':'Vaelorn als bewuste uitzondering in tabel levensduur.','WRIJ-Z15-4':'jaar 0, de nacht van het bloedzegel (BESLUIT-Z15-7-Z37).',
   'WRIJ-Z15-9':'zo gelaten: Thalens stem binnen Ysara, Kleur.','WRIJ-Z15b-1':'de roman besliste (h25, YSA-Z28-37).','WRIJ-Z15b-2':'beatplan is archief; de roman heeft 33 hoofdstukken.',
   'WRIJ-Z20-2':'h25 koos lander zeven (YSA-Z28-37).','WRIJ-Z21-1':'zo gelaten; Wren Tallis in de baai is aannemelijk.','WRIJ-Z21-4':'211 blijven; later komen er aankomers bij (regel in BESLUIT-Z37-5).',
   'WRIJ-Z28-4':'vee vastgelegd in VEE-Z37-schip (geiten, hond; vis niet).','WRIJ-Z30-3':'BESLUIT-Z30-4 is de enige regel.','WRIJ-Z31-14':'de steekproef van de architect na de ronde wijst de Kern-rijen aan.',
   'WRIJ-Z32-1':'Ardemar IV (PER-ardemar-iv-Z37) en Ardemar III naar -290 (PER-f1-ardemar-derde-Z37).','WRIJ-Z32-2':'Selvara Varenne de Eerste (PER-f6-selvara-eerste-Z37), erfnaam.','WRIJ-Z32-3':'erfnaam.','WRIJ-Z32-4':'erfnaam.','WRIJ-Z32-5':'erfnaam, bewust.','WRIJ-Z32-6':'erfnaam; Nadir in 801.',
   'WRIJ-Z33-2':'regel R-kern_leunt_op_kleur slaat FASE-OVERZICHT-rijen over (lijsten).','WRIJ-Z33-4':'HOOFDPERS-Z37-kluwer/-myrrhen/-veslethi met de fase van hun PER-rij.','WRIJ-Z33-5':'de PER-rijen bestonden al (PER-f3-anath, PER-f5-corvina, PER-f4-edrun); tabel personage verwijst er nu naar.',
   'WRIJ-Z33-8':'YSA-Z15-9-Z37 zegt 74.','WRIJ-Z34-3':'per-familiebesluit in sjabloon_familie.voorstel goedgekeurd (BESLUIT-Z37-5).'}
  for w,hoe in HOE.items():
    sluit_wrij(w,hoe+' (BESLUIT-Z37-5)');keuze('KEUZE-'+w,'besloten','[Z37: ja (BESLUIT-Z37-5)]')
  keuze('KEUZE-WRIJ-Z33-7','open','[Z37: REGEL-harde-grenzen kreeg BESLUIT-Z30-4. De andere vijf wachten op Rogier.]')
  keuze('KEUZE-WRIJ-Z34-2','open','[Z37: gecontroleerd, zie wijzigingen_Z37.md; nog per boog te doen.]')
  # C: H01-H50 vervallen
  for (k,) in c.execute("select code from keuze where soort='herkomst' and status='open'").fetchall():
    keuze(k,'vervallen','[Z37 vervallen (BESLUIT-Z37-6): de methode was fout; een verwijzing naar X is geen bron van X.]')
  # export kent geen lege tekst: lege verwijzingen als NULL (roundtrip)
  c.execute("update canon set verwijst_naar=null where ronde=66 and verwijst_naar=''");c.execute("update canon set hangt_samen_met=null where ronde=66 and hangt_samen_met=''")
  c.commit()
# ================= D2: personage_profiel als bron; 482 rijen omzetten =================
FAM_OM=('L:Naam|Volk|Regio|Huis|Rol|Fase|Wil|Durft','L:Kern|Naam|Volk|Regio|Huis|Rol|Fase|Wil','L:Volk|Fase|Rol|Verandert|Zintuiglijk|Haak|Verdiept (Z5)|Geur')
def d2():
  # regels: vervangen_door mag naar personage_profiel wijzen; ankerbron mag in het profiel staan; Kern mag op een profielrij leunen
  R={'R-vervangen_door':"select code,case when vervangen_door is null then 'voorlopig, vervangen zonder vervangen_door' else 'vervangen_door '||vervangen_door||' bestaat niet' end from canon where status='voorlopig, vervangen' and (vervangen_door is null or (vervangen_door not in(select code from canon) and not (vervangen_door='personage_profiel:'||code and code in(select code from personage_profiel))))",
     'R-anker_bron_levend':"select 'ANKER-'||a.sleutel,'bron '||coalesce(a.bron_code,'-')||' bestaat niet of leeft niet' from anker a left join canon c on c.code=a.bron_code where (c.code is null or c.status not in('vastgesteld','voorlopig')) and not (c.vervangen_door='personage_profiel:'||c.code and c.code in(select code from personage_profiel))"}
  for k,v in R.items(): zet('regel','code',k,'sql_test',v)
  sq=c.execute("select sql_test from regel where code='R-kern_leunt_op_kleur'").fetchone()[0]
  if 'personage_profiel:' not in sq: zet('regel','code','R-kern_leunt_op_kleur','sql_test',sq.replace("and b.draagkracht='Kleur'","and b.draagkracht='Kleur' and coalesce(b.vervangen_door,'') not like 'personage_profiel:%'"))
  afgeleid.bouw(c)
  doel=[r for r in c.execute(f"select p.code,c.status,c.draagkracht from personage_profiel p join canon c on c.code=p.code where (p.familie in({','.join('?'*len(FAM_OM))}) or p.archetype=1) and c.status in('vastgesteld','voorlopig')",FAM_OM).fetchall()]
  S['d2_kern_overgeslagen']=sum(1 for _,_,d in doel if d=='Kern')
  for code,st,dk in doel:
    if dk=='Kern': continue
    vervang(code,'personage_profiel:'+code);S['d2_omgezet']+=1
  afgeleid.bouw(c)
  c.commit()
def profiel_opvolger(oud,nc,subs,extra):
  """Opvolger van een rij die al in personage_profiel staat: de nieuwe rij gaat meteen naar het profiel, de oude wijst naar de nieuwe."""
  r=c.execute('select categorie,onderwerp,feit,verwijst_naar,tijdperk,jaar,vervangen_door from canon where code=?',(oud,)).fetchone()
  if not r or bestaat(nc): return
  f=r[2]
  for a,b in subs:
    assert a in f,(oud,a);f=f.replace(a,b)
  f=f.rstrip()+' '+extra
  c.execute("insert into canon(code,categorie,onderwerp,feit,feit_schoon,reden,status,ronde,verwijst_naar,hangt_samen_met,tijdperk,jaar,vervangen_door) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (nc,r[0],r[1],f,f,REDEN+' (D2: rij volgt het anker)','voorlopig, vervangen',RN,r[3],r[3],r[4],r[5],'personage_profiel:'+nc))
  S['canon_nieuw']+=1;wijz(nc,'toegevoegd','canon',None,'voorlopig, vervangen (personage_profiel:'+nc+')')
  if c.execute("select status from canon where code=?",(oud,)).fetchone()[0] in('vastgesteld','voorlopig'): vervang(oud,nc)
  else: c.execute('update canon set vervangen_door=? where code=?',(nc,oud));wijz(oud,'vervangen','vervangen_door',r[6],nc)

# ================= D1: machine herstellen =================
def d1():
  import d1 as D1,ideeen37
  ok,regels=D1.test_seriewaarde(c)
  open(os.path.join(W,'z37','test_seriewaarde.txt'),'w').write('\n'.join(regels)+f"\nuitslag: {'geslaagd' if ok else 'MISLUKT'}\n")
  if not ok: sys.exit('seriewaarde-test mislukt')
  S.update({'d1_'+k:v for k,v in D1.herbereken(c).items()})
  S.update({'d1_ideeen_'+k:v for k,v in ideeen37.verwerk(c).items()})
  c.commit()
# ================= D3: rijkdom =================
def d3():
  RD3=_laad('rd37',os.path.join(W,'z37','rijkdom_data.py'));MD=_laad('md37',os.path.join(W,'z37','module_data.py'))
  RK=_laad('rk37',os.path.join(W,'z37','rijkdom.py'))
  for code,naam,toel in RD3.DOMEIN:
    S['domein']+=c.execute('insert or ignore into domein(code,naam,toelichting) values(?,?,?)',(code,naam,toel)).rowcount
  for dom,vs in RD3.VRAAG.items():
    for i,v in enumerate(vs,1): S['competentievraag']+=c.execute('insert or ignore into competentievraag(code,domein_code,vraag) values(?,?,?)',(f'CV-{dom}-{i}',dom,v)).rowcount
  SL={'karrûk':'karruk','sael-mor':'saelmor','aelthir':'aelthir'}
  for volk,dom,ond,feit,verw in RD3.RIJ:
    code=f'RIJK-Z37-{SL[volk]}-{dom}'
    nieuw(code,'Dagelijks leven',ond,feit,verw,reden=REDEN+' (D3, stap 10 rijkdom; beantwoordt de competentievragen van domein '+dom+')',status='voorlopig',tijdperk='801 Heden',jaar=801)
    for i in range(1,len(RD3.VRAAG[dom])+1):
      S['competentie_antwoord']+=c.execute('insert or ignore into competentie_antwoord(vraag_code,volk,fase_nr,antwoord_code) values(?,?,?,?)',(f'CV-{dom}-{i}',volk,801,code)).rowcount
  # beroepen, gaven, rite, feeënlaag: voorlopig in de ideeënbank, elk met wereldregel en code
  for code,naam,afg,tw,wr,verb,feit in MD.BEROEP:
    nieuw(code,'Beroep','Beroep: '+naam,feit,verb+';'+wr,reden=REDEN+' (D3, beroepen-module stap 11c-patroon; wereldregel '+wr+')',status='voorlopig',ideeenbank=1)
    S['beroep']+=c.execute('insert or ignore into beroep(code,naam,afgeleid_van,zwarte_tweeling,wereldregel_code,verbinding) values(?,?,?,?,?,?)',(code,naam,afg,tw,wr,verb)).rowcount
  for code,naam,el,prijs,ja,bron,feit,verw in MD.GAVE:
    nieuw(code,'Magie','Gave: '+naam,feit,verw,reden=REDEN+' (D3, gaven-stelsel; voorstel)',status='voorlopig',ideeenbank=1)
    S['gave']+=c.execute('insert or ignore into gave(code,naam,element,prijs,ja_regel,bron) values(?,?,?,?,?,?)',(code,naam,el,prijs,ja,bron)).rowcount
  code,cat,ond,feit,verw=MD.RITE;nieuw(code,cat,ond,feit,verw,reden=REDEN+' (D3, voorstel rite)',status='voorlopig',ideeenbank=1)
  for code,ond,feit,verw in MD.FEE: nieuw(code,'Volken',ond,feit,verw,reden=REDEN+' (D3, feeënlaag; voorstel)',status='voorlopig',ideeenbank=1)
  # R-dode_rijkdom (signaal)
  if not c.execute("select 1 from regel where code='R-dode_rijkdom'").fetchone():
    c.execute("insert into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",('R-dode_rijkdom','rijkdom',
      'Signaal: Structuur-rij in een rijkdomscel (rijkdom_lid) die twee rondes later door niets wordt gebruikt: geen enkele rij verwijst ernaar en zij raakt geen PER-, ERF-, HOOFDPERS- of VERHAAL-rij (opdracht_Z35 stap 10.4).',
      f"select distinct l.code,'dode rijkdom: '||l.volk||' / '||l.domein_code from rijkdom_lid l join canon k on k.code=l.code where k.draagkracht='Structuur' and k.status in('vastgesteld','voorlopig') and coalesce(k.ronde,0)<={RN}-2 and not exists(select 1 from relatie r where r.naar_code=l.code and r.soort='leunt_op') and not exists(select 1 from relatie r where r.van_code=l.code and (r.naar_code like 'PER%' or r.naar_code like 'ERF-%' or r.naar_code like 'HOOFDPERS%' or r.naar_code like 'VERHAAL%'))",
      'opdracht_Z35.md stap 10.4; BESLUIT-Z37-5 (Z37-overhandiging)','Rogier (Z37-overhandiging, D3)','actief','signaal'))
    S['regel_nieuw']+=1;wijz('R-dode_rijkdom','toegevoegd','regel',None,'signaal')
  afgeleid.bouw(c)
  for code,det,pat,codes,n,st in RK.motief(c,MD.MOTIEF):
    r=c.execute('select aantal,codes from motief_detail where code=?',(code,)).fetchone()
    if not r: c.execute('insert into motief_detail(code,detail,patroon,codes,aantal,status) values(?,?,?,?,?,?)',(code,det,pat,codes,n,st));S['motief_detail']+=1
    elif (r[0],r[1])!=(n,codes): c.execute('update motief_detail set aantal=?,codes=?,status=? where code=?',(n,codes,st,code))
  c.commit()
# ================= MAIN =================
if __name__=='__main__':
  if '0' in STAPPEN: stap0();toets('stap 0')
  if 'd1' in STAPPEN: d1();toets('D1 machine')
  if 'd2' in STAPPEN:
    voor=c.execute('select count(*) from personage_profiel').fetchone()[0];d2();toets('D2 omzetten');per_b();toets('B personages (na D2)')
    S['profiel_voor']=voor;S['profiel_na']=c.execute('select count(*) from personage_profiel').fetchone()[0]
  if 'd3' in STAPPEN: d3();toets('D3 rijkdom')
  print(dict(S))
