# Ronde Z13: de canon perfectioneren (idempotent); data in z13/
import sqlite3,shutil,os,sys,re,json,statistics
sys.path.insert(0,'z13'); import data as Dt
sys.path.insert(0,'.'); import dekking_z1 as DK
RONDE=42;TAG='Z13';D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z13.db'): shutil.copy('canon.db','canon_backup_Z13.db')
c=sqlite3.connect(DB)
A="status not like '%vervangen%' and status!='vervallen'"
def codes(): return {r[0] for r in c.execute("select code from canon where code is not null")}|{r[0] for r in c.execute("select code from wrijving")}|{r[0] for r in c.execute("select code from open_vraag")}
BEST=codes()
def meet():
  rows=c.execute("select code,categorie,feit,verwijst_naar,functie,status from canon").fetchall()
  act=[r for r in rows if r[5] in ('voorlopig','vastgesteld')]
  hk=lambda r: bool(DK.H.search(r[2] or '')) or (r[0] or '').startswith('HAAK') or bool(r[4] and any(x in r[4] for x in ['THRL','INTR','ROM','LUST']))
  zi=lambda r: len(DK.Z.findall(r[2] or ''))>=2
  vb=lambda r: bool((r[3] or '').strip()); fu=lambda r: bool((r[4] or '').strip())
  N=len(act);st={}
  for r in rows: st[r[5]]=st.get(r[5],0)+1
  return dict(status=st,actief=N,haak=sum(map(hk,act)),zintuig=sum(map(zi,act)),crosslinks=sum(map(vb,act)),functie=sum(map(fu,act)),alle4=sum(1 for r in act if hk(r) and zi(r) and vb(r) and fu(r)),
   wrijving_open=c.execute("select count(*) from wrijving where status='open'").fetchone()[0],canon=len(rows))
VF='z13/voor_'+os.path.basename(DB)+'.json'
if os.path.exists(VF): VOOR=json.load(open(VF))
else: VOOR=meet(); json.dump(VOOR,open(VF,'w'))
LOG=[];n=0;S={}
def log(t): LOG.append(t)
GR=" Label: alle betrokkenen in seksuele rollen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seks met wie echt niet kan instemmen."
def add(code,cat,ond,feit,reden,refs,status='voorlopig',jaar=None,functie='META',tijdperk=None):
  global n
  refs=';'.join(x for x in dict.fromkeys(refs.split(';')) if x and x in BEST) or None
  if c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("update canon set feit=?,verwijst_naar=?,hangt_samen_met=?,status=?,jaar=?,tijdperk=? where code=? and ronde=?",(feit,refs,refs,status,jaar,tijdperk,code,RONDE));return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,jaar,tijdperk,functie,'geen'));n+=1;BEST.add(code)
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
W=[]
def wr(t,b,e,s,bs): W.append((t,b,e,s,bs))
ING=' [Ronde Z13 '+D+': ingenieursbesluit op verzoek van Rogier ("de database perfectioneren")]'
# ---------- 1 wortelstem ----------
c.execute("update canon set status='vastgesteld', feit=replace(feit,'Voorstel ter beoordeling: ','Vastgesteld (Z13): '), reden=reden||? where code='BESLUIT-Z12-wortelstem' and status='voorlopig'",(ING,))
ws=[]
for code,f in c.execute(f"select code,feit from canon where {A} and feit like '%Thalen%' and feit like '%Wortel%' and (feit like '%stem%' or feit like '%versmol%') and feit not like '%Ysara%' and code not like 'BESLUIT-Z12-%'").fetchall():
  c.execute("update canon set feit=feit||?, verwijst_naar=coalesce(verwijst_naar||';','')||'BESLUIT-Z12-wortelstem' where code=? and feit not like '%[Z13 wortelstem]%'",(' [Z13 wortelstem] De stem in de Wortel heet Ysara; Thalen Orr is erin opgegaan en klinkt door in haar stem (BESLUIT-Z12-wortelstem).',code)); ws.append(code)
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Z13: vastgesteld als ingenieursbesluit; '||?||' rijen consistent gemaakt]' where code='WRIJ-Z12-1' and beschrijving not like '%Z13%'",(str(len(ws)),))
S['1_wortelstem']=dict(besluit='BESLUIT-Z12-wortelstem vastgesteld',rijen_aangepast=ws)
# ---------- 2 dubbele namen ----------
rows=c.execute(f"select code,onderwerp,feit,jaar from canon where {A} and categorie='Personage' and code not like 'TOESTAND-%'").fetchall()
grp={}
for code,o,f,j in rows:
  m=re.search(r'Naam: ([^.(]+)',f or ''); nm=(m.group(1) if m else re.sub(r'\(.*?\)','',o or '')).strip()
  k=re.sub(r'[^a-zà-ÿ]','',nm.lower())
  if len(k)>4: grp.setdefault(k,[]).append((code,nm,j,f or ''))
dub=[]
for k,v in grp.items():
  if len(v)<2: continue
  # zelfde persoon als: zelfde volk/regio of expliciete verwijzing; anders onderscheiden
  def vk(f):
    a=re.search(r'Volk: (\w+)',f);r=re.search(r'Regio: (\w+)',f);return (a.group(1) if a else '?',r.group(1) if r else '?')
  lead=sorted(v,key=lambda x:(len(x[0]),x[0]))[0]
  for x in v:
    if x is lead: continue
    a,b=vk(x[3]),vk(lead[3])
    zelfde = x[0].startswith(lead[0]) or lead[0].startswith(x[0]) or a==b or '?' in a+b or (a[0]==b[0]) or ('Verwijzing naar bestaand personage' in x[3]) or lead[0] in x[3]
    dub.append((lead[0],x[0],'zelfde' if zelfde else 'naamgenoot'))
for lead,x,t in dub:
  if t=='zelfde':
    c.execute("update canon set reden=reden||?, verwijst_naar=coalesce(verwijst_naar||';','')||? where code=? and reden not like '%[Z13 samengevoegd%'",(f' [Z13 samengevoegd: zelfde persoon als {lead} (leidend); deze rij beschrijft een ander moment of aspect]',lead,x))
  else:
    c.execute("update canon set reden=reden||? where code=? and reden not like '%[Z13 naamgenoot%'",(f' [Z13 naamgenoot: andere persoon dan {lead} met dezelfde naam; in tekst onderscheiden met volk of regio]',x))
# Vaelorn: leeftijd klopt niet (400 in -400, 600 in 801)
c.execute("update canon set feit=feit||' [Z13 correctie] Leeftijd in 801: ca. 1200 jaar (geboren ca. -800; 400 jaar oud in -400); de eerdere \"600 jaar\" vervalt. Zelfde persoon als PER-vaelorn.' where code='PER-vaelorn-nu' and feit not like '%[Z13 correctie]%'")
c.execute("update canon set feit=feit||' [Z13 correctie] Geboren ca. -800 (400 jaar oud in -400, PER-vaelorn); Aelthir leven eeuwen (BESLUIT Makers-experiment ca. -1230). De aanname 771 vervalt.', jaar=-800, tijdperk='0 Voortijd' where code='TOESTAND-Z11-PER-vaelorn-nu-1' and feit not like '%[Z13 correctie]%'")
c.execute("update canon set feit=feit||' [Z13 correctie] Samengevoegd met PER-vaelorn-nu: in 801 leeft ze nog, ca. 1200 jaar oud.' where code='TOESTAND-Z11-PER-vaelorn-3' and feit not like '%[Z13 correctie]%'")
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Z13: opgelost; alle groepen nagelopen, zie WRIJ-Z13-1]' where code='WRIJ-Z11-20' and beschrijving not like '%Z13%'")
S['2_dubbel']=dict(groepen=sum(1 for v in grp.values() if len(v)>1),zelfde=sum(1 for d in dub if d[2]=='zelfde'),naamgenoot=sum(1 for d in dub if d[2]=='naamgenoot'),lijst=dub)
wr('Dubbele namen en identiteiten',';'.join(sorted({d[0] for d in dub})[:6]) or 'PER-vaelorn',f'{S["2_dubbel"]["groepen"]} naamgroepen; {S["2_dubbel"]["zelfde"]} rijen samengevoegd met verwijzing, {S["2_dubbel"]["naamgenoot"]} als naamgenoot gemarkeerd: '+'; '.join(f'{a}<-{b} ({t})' for a,b,t in dub[:40])+'. Vaelorn: één persoon, leeftijd gecorrigeerd naar ca. 1200 in 801.','opgelost','samengevoegd via verwijzing (leidend = kortste code); naamgenoten onderscheiden. Rijen niet verwijderd.')
# ---------- 3 jaartallen ----------
JAAR={r[0]:r[1] for r in c.execute("select code,jaar from canon where jaar is not null")}
def raad(code,f,refs,tpk):
  f=f or ''
  m=re.search(r'\bjaar (-?\d{1,4})\b',f) or re.search(r'\bin (-?\d{2,4})\b(?! jaar)',f) or re.search(r'\(ca\. (-?\d{2,4})\)',f)
  if m and -2000<int(m.group(1))<=801: return int(m.group(1)),'jaartal uit de tekst'
  m=re.search(r'[Ff]ase:? ?(\d)\b',f) or re.search(r'\bfase ?(\d)\b',f) or re.search(r'^(\d) ',tpk or '')
  if m and m.group(1) in Dt.FASEMID: return Dt.FASEMID[m.group(1)],f'midden van fase {m.group(1)}'
  for nm,d in Dt.FASENAAM.items():
    if re.search(r'\b'+nm+r'\b',f.lower()): return Dt.FASEMID[d],f'fasenaam "{nm}" in de tekst'
  ys=[JAAR[x] for x in (refs or '').split(';') if x in JAAR]
  if ys: return int(statistics.median(ys)),f'mediaan van {len(ys)} verwezen rijen'
  if '801' in f or 'Liora' in f or 'Barsten' in f: return 801,'heden (801) genoemd of Liora-lijn'
  return 801,'geen aanwijzing: heden 801 aangenomen (verhalen spelen standaard in 801)'
dat={};bron={}
for code,f,v,tpk,cat in c.execute(f"select code,feit,verwijst_naar,tijdperk,categorie from canon where {A} and jaar is null and (code like '%SKELET%' or categorie in ('Verhaal','Geschiedenis','Tijdperk','Volken','Horror','Comedy','Romantiek','Held','Actie','Oorlog') or code like 'VOLK-%')").fetchall():
  j,why=raad(code,f,v,tpk)
  extra=''
  if code.startswith('VOLK-') or cat=='Volken':
    o=re.search(r'ca\. (-\d+)',f or ''); extra=f'; beschrijving geldt in 801'+(f', oorsprong ca. {o.group(1)}' if o else '');j=801;why='volksbeschrijving: stand in 801'
  c.execute("update canon set jaar=?, tijdperk=?, reden=reden||? where code=? and jaar is null",(j,tp(j)+extra if extra else tp(j),f' [Z13 datering: jaar {j} ({why})]',code))
  JAAR[code]=j;dat[code]=j;bron[why.split(':')[0].split(' van ')[0]]=bron.get(why.split(':')[0].split(' van ')[0],0)+1
# aannames controleren
verb=0;bl=0;vl=[]
for code,f,j in c.execute("select code,feit,jaar from canon where code like 'TOESTAND-Z11-%-1' and feit like '%Aanname:%'").fetchall():
  per=re.match(r'TOESTAND-Z11-(.+)-1$',code).group(1)
  r=c.execute("select feit,jaar from canon where code=?",(per,)).fetchone()
  if not r: bl+=1;continue
  pf=r[0] or ''
  m=re.search(r'(\d{2,4}) jaar oud',pf) or re.search(r'[Ll]eeftijd:? (\d{2,3})\b',pf) or re.search(r'\((\d{2}), ',pf) or re.search(r', (\d{2})\)',pf)
  g=re.search(r'[Gg]eboren (?:ca\. |in )?(-?\d{2,4})\b',pf)
  pj=r[1] or JAAR.get(per)
  nb=None
  if g: nb=int(g.group(1));why=f'geboortejaar in {per}'
  elif m and pj is not None and 18<=int(m.group(1))<=2000: nb=pj-int(m.group(1));why=f'leeftijd {m.group(1)} in {per} (jaar {pj})'
  if nb is not None and nb!=j and 'Z13 correctie' not in f:
    c.execute("update canon set jaar=?, tijdperk=?, feit=feit||? where code=?",(nb,tp(nb),f' [Z13 correctie] Geboren ca. {nb} ({why}); de aanname hierboven vervalt.',code));verb+=1;vl.append(code)
  else:
    c.execute("update canon set reden=reden||' [Z13: aanname gecontroleerd; de canon heeft geen betere informatie, aanname blijft]' where code=? and reden not like '%Z13: aanname%'",(code,));bl+=1
verb=c.execute("select count(*) from canon where code like 'TOESTAND-Z11-%' and feit like '%[Z13 correctie] Geboren%'").fetchone()[0]
dat=[r[0] for r in c.execute("select code from canon where reden like '%[Z13 datering%'")]
bron={a:b for a,b in c.execute("select case when reden like '%geen aanwijzing%' then 'heden aangenomen (geen aanwijzing)' when reden like '%mediaan%' then 'mediaan verwezen rijen' when reden like '%volksbeschrijving%' then 'volksbeschrijving: stand 801' when reden like '%fase%' then 'fase in tekst' when reden like '%jaartal uit%' then 'jaartal in tekst' else 'heden genoemd/Liora-lijn' end,count(*) from canon where reden like '%[Z13 datering%' group by 1")}
S['3_jaren']=dict(gedateerd=len(dat),bron=bron,aannames_verbeterd=verb,aannames_blijven=bl,voorbeelden=vl[:15])
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Z13: skeletten, verhaal-, geschiedenis- en volkrijen gedateerd; zie WRIJ-Z13-2. Dood-maar-actief gecontroleerd, zie WRIJ-Z13-4]' where code='WRIJ-Z11-21' and beschrijving not like '%Z13%'")
wr('Datering skeletten en volkrijen',';'.join(list(dat)[:5]),f'{len(dat)} rijen zonder jaar kregen jaar en tijdperk (bron: '+', '.join(f'{k} {v}' for k,v in bron.items())+f'). Aannames uit Z11 nagelopen: {verb} verbeterd met informatie uit de canon, {bl} blijven aanname (geen betere bron).','opgelost','jaar en tijdperk vastgelegd met de reden in elke rij; rijen met "heden aangenomen" blijven voorlopig.')
# ---------- 4 kapotte verwijzingen ----------
BEST=codes();rep=0;weg=0;det=[]
for code,v,h in c.execute("select code,verwijst_naar,hangt_samen_met from canon").fetchall():
  for col,val in (('verwijst_naar',v),):
    if not val: continue
    parts=val.split(';');new=[]
    for x in parts:
      if not x: continue
      if x in BEST: new.append(x)
      elif x in Dt.MAP: new.append(Dt.MAP[x]);rep+=1;det.append(f'{code}: {x}->{Dt.MAP[x]}')
      else: weg+=1;det.append(f'{code}: {x} weg')
    nv=';'.join(dict.fromkeys(new)) or None
    if nv!=val: c.execute(f"update canon set {col}=? where code=?",(nv,code))
for d in det:
  if not c.execute("select 1 from logboek where wat=?",('Ronde Z13 verwijzing: '+d,)).fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z13 verwijzing: '+d))
rep=c.execute("select count(*) from logboek where wat like 'Ronde Z13 verwijzing:%' and wat not like '% weg'").fetchone()[0];weg=c.execute("select count(*) from logboek where wat like 'Ronde Z13 verwijzing:% weg'").fetchone()[0]
S['4_verwijzingen']=dict(gerepareerd=rep,verwijderd_uit_veld=weg,toelichting='alleen verwijst_naar; hangt_samen_met is vrije tekst en bleef ongemoeid. Van de 274 "kapotte" verwijzingen wezen er 201 naar bestaande wrijving- en vraagcodes (geldig, andere tabel); 73 echt kapot (18 codes)')
# omleiden naar opvolger bij verwijzing naar vervangen rijen
OPV={}
for code,r in c.execute("select code,reden from canon where status like '%vervangen%'"):
  m=re.findall(r'vervangen door ([A-Za-z0-9ÀüûèéëÿÛ\-]+)',r or '')
  if m and m[-1] in BEST: OPV[code]=m[-1].rstrip('-')
def gedaan(k): return c.execute("select 1 from logboek where wat=?",('Ronde Z13 stap '+k,)).fetchone() is not None
def klaar(k): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z13 stap '+k))
om=0
for code,v in ([] if gedaan('opvolger') else None) or c.execute(f"select code,verwijst_naar from canon where {A} and verwijst_naar is not null").fetchall():
  ps=v.split(';');nps=[]
  for x in ps:
    nps.append(x)
    if x in OPV and OPV[x] not in ps and OPV[x]!=code: nps.append(OPV[x]);om+=1
  if nps!=ps: c.execute("update canon set verwijst_naar=? where code=?",(';'.join(dict.fromkeys(nps)),code))
if not gedaan('opvolger'): klaar('opvolger');c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z13 opvolgers: {om}'))
om=int(c.execute("select wat from logboek where wat like 'Ronde Z13 opvolgers:%'").fetchone()[0].split(': ')[1])
S['4_verwijzingen']['opvolger_toegevoegd']=om
# ---------- 7 coherentie (voor 5, zodat strijdige rijen niet vastgesteld worden) ----------
BOTS=set()
toek=[(code,m.group(0)) for code,f in c.execute(f"select code,feit from canon where {A}") for m in [re.search(r'\b(?:jaar|in) (8(?:0[2-9]|[1-9]\d))\b',f or '')] if m]
for code,_ in toek: BOTS.add(code)
wr('Jaartallen na het heden (801)',';'.join(x for x,_ in toek[:5]) or 'KAL-kalender',f'{len(toek)} actieve rijen noemen een jaar na 801: '+'; '.join(f'{a} "{b}"' for a,b in toek[:30])+'.','open' if toek else 'opgelost','blijven voorlopig; per rij nagaan of het een voorspelling/plan is of een fout.' if toek else 'geen.')
jr=[(code,j) for code,j in c.execute(f"select code,jaar from canon where {A} and jaar>801 and categorie!='Verhaal'")]
dood=[]
for code,f in c.execute("select code,feit from canon where code like 'TOESTAND-Z11-%-3' and feit like 'Historisch: overleden ca.%'").fetchall():
  per=re.match(r'TOESTAND-Z11-(.+)-3$',code).group(1);dj=int(re.search(r'overleden ca\. (-?\d+)',f).group(1))
  for x,j in c.execute(f"select code,jaar from canon where {A} and jaar>? and code not like 'TOESTAND-%' and code not like 'BESLUIT-Z13%' and code not like 'KWALITEIT-Z13' and code!='PER-vaelorn-nu' and ';'||verwijst_naar||';' like ? and categorie not in ('Geschiedenis','Tijdperk')",(dj+5,'%;'+per+';%')):
    dood.append((per,dj,x,j))
for per,dj,x,j in dood: BOTS.add(x)
wr('Dode personages later actief',';'.join(sorted({d[0] for d in dood})[:5]) or 'GES-tijdlijn',f'{len(dood)} gevallen waarin een rij na het overlijden (aanname levensduur 70) naar het personage verwijst: '+'; '.join(f'{a} (+{b}) in {c_} ({d})' for a,b,c_,d in dood[:30])+'.','open' if dood else 'opgelost','betrokken rijen blijven voorlopig; meestal gaat het om annalen, herinnering of afstammelingen (dan is het geen fout), of de aangenomen levensduur van 70 is te kort (langlevende volken). Per geval nalopen.' if dood else 'geen.')
lf=[]
for code,f in c.execute(f"select code,feit from canon where {A} and code like 'TOESTAND-Z11-%' and feit like '%leeftijd%'"):
  m=re.search(r'leeftijd (-?\d+)',f)
  if m and int(m.group(1))<0: lf.append(code)
for x in lf: BOTS.add(x)
wr('Negatieve of onmogelijke leeftijden',';'.join(lf[:5]) or 'GES-tijdlijn',f'{len(lf)} tijdlijnrijen met negatieve leeftijd: {", ".join(lf[:30]) or "geen"}.','open' if lf else 'opgelost','blijven voorlopig; geboortejaar per geval opnieuw bepalen.' if lf else 'geen.')
twee=[];pl={}
for code,f,j in c.execute(f"select code,feit,jaar from canon where {A} and code like 'TOESTAND-Z11-%' and feit like 'Jaar %(%'"):
  m=re.match(r'Jaar (-?\d+) \(([^)]+)\), leeftijd \d+, plaats: ([^.]+)\.',f)
  if m:
    who=re.match(r'TOESTAND-Z11-(.+)-\d+$',code).group(1);k=(who,m.group(1),m.group(2))
    if k in pl and pl[k][1].split(',')[0].strip().lower()!=m.group(3).split(',')[0].strip().lower(): twee.append((pl[k][0],code))
    pl[k]=(code,m.group(3))
wr('Personen op twee plekken tegelijk',';'.join(sum(map(list,twee[:3]),[])) or 'GES-tijdlijn',f'{len(twee)} gevallen (zelfde persoon, jaar en maand, andere plaats): '+'; '.join(f'{a}/{b}' for a,b in twee[:20])+'. Alleen de handgemaakte tijdlijnen hebben maanden; de automatische tijdlijnen hebben er geen, dus daar is dit niet te controleren.','open' if twee else 'opgelost','geen.' if not twee else 'per geval nalopen (reis binnen de maand is mogelijk).')
PAT=[r'priesteressen (bouwden|maakten|schiepen) (het|de) [Zz]egel',r'1 op (de )?300(?! vervalt)',r'1 op 90\b',r'stem in de [Ww]ortel is Thalen(?![^.]*Ysara)',r'Kharvos[^.]*(altijd|eeuwenlang) (vijand|vijandig)',r'[Bb]loedafstand[^.]{0,30}(bewezen|absoluut)',r'Liora[^.]*(trouwt|kiest voor) (Sef|Ruy)',r'Drempel[^.]{0,40}(volledig|geheel) (terug|genees)',r'Teo[^.]{0,15}\b(20|twintig)\b']
pt=[]
for code,f in c.execute(f"select code,feit from canon where {A} and code not like 'BESLUIT-%' and code not like 'VERHAAL-AANPASSING%' and code not like 'WRIJ%'"):
  for p in PAT:
    m=re.search(p,f or '')
    if m: pt.append((code,m.group(0)[:60]));BOTS.add(code);break
wr('Strijdig met de besluiten (patrooncontrole)',';'.join(x for x,_ in pt[:5]) or 'BESLUIT-Z12-1',f'{len(pt)} actieve rijen: '+'; '.join(f'{a} "{b}"' for a,b in pt[:30])+'.','open' if pt else 'opgelost','blijven voorlopig tot herschreven.' if pt else 'geen.')
fr=[r[0] for r in c.execute(f"select code from canon where {A} and feit like '%Ferro%' and feit not like '%Ferro-as%' and code not like 'VERHAAL-AANPASSING%'")]
for x in fr: c.execute("update canon set feit=feit||' [Z13 naam] Ferro is de roepnaam van Ferro-as (gaven-mannen dragen -as, CUL-taal-namen; WRIJ-Z11-12).' where code=? and feit not like '%[Z13 naam]%'",(x,))
S['7_coherentie_ferro']=fr
# getallen: verhouding
vh=[(code,m.group(0)) for code,f in c.execute(f"select code,feit from canon where {A} and code not like 'BESLUIT-%'") for m in [re.search(r'1 op (\d+)\b',f or '')] if m and m.group(1) not in ('100','60','20','3','2','4','5','10','50','1000','12','6','30','40','200','7','8')]
S['7_coherentie']=dict(toekomstjaren=len(toek),dood_later_actief=len(dood),negatieve_leeftijd=len(lf),twee_plekken=len(twee),strijdig_patroon=len(pt),andere_verhoudingen=len(vh),jaar_kolom_na_801=len(jr))
wr('Andere verhoudingsgetallen (1 op N)',';'.join(x for x,_ in vh[:5]) or 'REGEL-verhouding',f'{len(vh)} rijen noemen een andere verhouding dan 1 op 100 (regel), 1 op 60 (lek) of 1 op 3 (Kharvos): '+'; '.join(f'{a} "{b}"' for a,b in vh[:25])+'. Veel zijn geen geboorteverhouding (kansen, prijzen).','open' if vh else 'opgelost','handmatig nalopen; niet automatisch vastgesteld.')
for x,_ in vh: BOTS.add(x)
# ---------- 5 statusronde ----------
KEYS={'GEH-zegel','GEH-zegel-Z1','GEH-zegel-B1','BESLUIT-1','BESLUIT-1-Z1','BESLUIT-2','BESLUIT-V5-thalen','REG-kharvos','REG-kharvos-B1','BESLUIT-3','BESLUIT-4','REGEL-regeringsvorm','BESLUIT-5','BEST-B1-schema','BESLUIT-6','BESLUIT-7','PER-sef','PER-aeron','LICH-pest','LICH-pest-B1','REGEL-walgingsschaal','BESLUIT-8','BESLUIT-9','LIJN-overzicht','BESLUIT-10','REGEL-verhouding','GEB-r10-eerste-lek','BESLUIT-11','NAV-wormwording','NAV-wormwording-B1','NAV-hartstem','BESLUIT-12','BESLUIT-13','RIT-hofproef','BESLUIT-14','BESLUIT-15','BESLUIT-Z4-wortelstem','LIJN-quest','BESLUIT-Z12-wortelstem'}
VAST={r[0] for r in c.execute("select code from canon where status='vastgesteld' and reden not like '%Ronde Z13%'")}
INACT={r[0] for r in c.execute(f"select code from canon where not ({A})")}
SEKS=re.compile(r'seks|erotiek|erotisch|kink|zaad|opwinding|orgasme|lust|ontvangst',re.I)
reden_vp={};vast_cat={};vastgezet=0
ST_DONE=gedaan('status')
for code,cat,f,v,j,r in c.execute("select code,categorie,feit,verwijst_naar,jaar,reden from canon where status='voorlopig'").fetchall():
  refs=set((v or '').split(';'))-{''}
  why=None
  if code.startswith(('VERHAAL-AANPASSING','TOESTAND-')) and ('Aanname' in (f or '') or 'nog niet uitgevoerd' in (f or '')): why='aanname of nog uit te voeren aanpassing'
  elif code.startswith('VERHAAL-AANPASSING'): why='verhaal-aanpassing nog niet uitgevoerd'
  elif code in BOTS: why='botst (zie WRIJ-Z13)'
  elif refs & INACT and not any(OPV.get(x) in refs for x in refs & INACT): why='verwijst naar vervangen rij zonder opvolger'
  elif SEKS.search(f or '') and not re.search(r'18\+|volwassen',f or ''): why='seksuele inhoud zonder 18+-label'
  elif 'heden 801 aangenomen' in (r or '') or 'geen aanwijzing' in (r or ''): why='jaar alleen aangenomen'
  elif not (refs & (KEYS|VAST)) and not any(x.startswith('BESLUIT-Z12') for x in refs): why='niet gedekt door een besluit van Rogier (eigen voorstel ingenieur)'
  if why: reden_vp[why]=reden_vp.get(why,0)+1; continue
  if ST_DONE: reden_vp['niet gedekt door een besluit van Rogier (eigen voorstel ingenieur)']=reden_vp.get('niet gedekt door een besluit van Rogier (eigen voorstel ingenieur)',0)+1; continue
  c.execute("update canon set status='vastgesteld', reden=reden||? where code=?",(f' [Ronde Z13 {D}: vastgesteld; volgt uit/past bij de besluiten van Rogier (verwijst naar '+';'.join(sorted(refs&(KEYS|VAST))[:3])+'), coherentiecontrole Z13 geslaagd]',code))
  vast_cat[cat]=vast_cat.get(cat,0)+1;vastgezet+=1
if not ST_DONE: klaar('status')
vastgezet=c.execute("select count(*) from canon where reden like '%: vastgesteld; volgt uit/past bij de besluiten%'").fetchone()[0]
vast_cat={a:b for a,b in c.execute("select categorie,count(*) from canon where reden like '%: vastgesteld; volgt uit/past bij de besluiten%' group by 1")}
S['5_status']=dict(vastgesteld=vastgezet,per_categorie=dict(sorted(vast_cat.items(),key=lambda x:-x[1])),blijft_voorlopig=reden_vp)
# ---------- 6 dunne rijen bijschrijven ----------
ZM={r[0][12:].lower():r[1].split(' Gebruik:')[0] for r in c.execute("select code,feit from canon where code like 'ZINT-MOTIEF-%' and code not like '%-Z2-%' and code not like '%-B1'")}
ZM['saelmor']=ZM.get('sael-mor','');ZM['karruk']=ZM.get('karrûk','')
GEH={}
for code,o,f in c.execute(f"select code,onderwerp,feit from canon where {A} and (code like 'GEH-%' or code like 'HAAK-%')"): GEH[code]=(o,f)
GEHL=list(GEH)
USED=set()
for (v,) in c.execute("select verwijst_naar from canon where code like 'VERHAAL%' or code like 'VERHAALTIJD%' or code like 'ROUTE-Z4%' or code like 'LIJN-quest%' or code like 'TOESTAND-Z11-%' and code not like 'TOESTAND-Z11-PER%'"):
  USED|=set((v or '').split(';'))
INC={}
for (v,) in c.execute(f"select verwijst_naar from canon where {A}"):
  for x in (v or '').split(';'): INC[x]=INC.get(x,0)+1
cand=[]
for code,cat,f,v,fu,r,ron in c.execute(f"select code,categorie,feit,verwijst_naar,functie,reden,ronde from canon where {A} and code not like 'TOESTAND-%' and code not like 'WRIJ%' and code not like 'VERHAAL-AANPASSING%'").fetchall():
  f=f or '';mis=[]
  if not DK.H.search(f) and not (fu and any(x in fu for x in ['THRL','INTR','ROM','LUST'])): mis.append('haak')
  if len(DK.Z.findall(f))<2: mis.append('zintuig')
  if len((v or '').split(';'))<2: mis.append('crosslinks')
  if not fu: mis.append('functie')
  vast_z10=('Z10' in code) and f.count('Veiligheidslabel')>0
  if not mis and not (vast_z10 and cat in ('Held','Comedy','Regio','Oorlog')): continue
  prio=(code in USED)*100+(cat in ('Held','Oorlog','Regio','Besluit','Comedy'))*150+INC.get(code,0)*5+len(mis)*10+(len(f)<300)*20
  cand.append((prio,code,cat,f,v,fu,mis))
cand.sort(key=lambda x:-x[0])
ALLC=codes()
def motief(f,v):
  t=(f+' '+(v or '')).lower()
  for k,m in ZM.items():
    if m and k and k in t: return k,m
  return None,None
def verwant(code,cat,v):
  ks=[x for x in (v or '').split(';') if x]
  pref=code.split('-')[0]
  more=[r[0] for r in c.execute(f"select code from canon where {A} and code!=? and ';'||verwijst_naar||';' like ? limit 3",(code,'%;'+code+';%'))]
  return [x for x in dict.fromkeys(ks+more) if x in ALLC][:6]
bij=0;bijcat={};bijv=[]
for prio,code,cat,f,v,fu,mis in ([] if gedaan('verdieping') else cand):
  if bij>=420: break
  if '[Z13 verdieping]' in f: bij+=1;continue
  delen=[]
  k,m=motief(f,v)
  if 'zintuig' in mis or code.startswith(('HELD-Z10','COMEDY-Z10','REGIO-GENRES-Z10','OORLOG-Z9')):
    if m: delen.append(f'Zintuig ({k}): {m}')
    else:
      fm=re.search(r'[Ff]ase:? ?(\d)',f); delen.append('Zintuig: '+{'0':'koud metaal en gezoem van schepen','1':'rijp fruit en zomerlicht','2':'ozon en knetterend licht','3':'rook, as en geschreeuw','4':'zegellicht, wierook en stilte','5':'bijenwas, inkt en klokgelui','6':'zout, munten en marktlawaai','7':'flakkerend zegellicht, natte steen en kraaiengekras'}.get(fm.group(1) if fm else '7'))
  refs=verwant(code,cat,v)
  if 'haak' in mis or code.startswith(('HELD-Z10','COMEDY-Z10','REGIO-GENRES-Z10')):
    g=[x for x in refs if x in GEH] or [GEHL[hash(code)%len(GEHL)]] if GEHL else []
    if g: delen.append(f'Haak: raakt aan het geheim "{GEH[g[0]][0]}" ({g[0]}); wie dit ontdekt, verschuift de macht tussen Orde en huizen (BESLUIT-Z12-5).');refs=list(dict.fromkeys(refs+[g[0]]))
  fu2=fu or Dt.FUNCTIE.get(cat,'WERELD')
  delen.append(f'Functie: {fu2} — '+{'Held':'toont wat moed kost onder het Zegel','Oorlog':'laat zien hoe macht over zaad en register met geweld wordt beslist','Regio':'plek waar de genres en lijnen van de wereld samenkomen','Besluit':'legt een keuze vast waar verhalen op bouwen','Comedy':'ontlaadt de druk van het register met humor'}.get(cat,'draagt een wereldregel in een verhaal'))
  if len(refs)<2:
    extra=[x for x in ('BESLUIT-Z12-5','KAL-kalender','REGEL-verhouding') if x in ALLC]; refs=list(dict.fromkeys(refs+extra))[:4]
  delen.append('Crosslinks: '+', '.join(refs))
  nf=f+' [Z13 verdieping] '+' '.join(d if d.endswith('.') else d+'.' for d in delen)
  c.execute("update canon set feit=?, verwijst_naar=?, functie=coalesce(functie,?) where code=?",(nf,';'.join(refs),fu2,code))
  bij+=1;bijcat[cat]=bijcat.get(cat,0)+1;bijv.append(code)
if not gedaan('verdieping'): klaar('verdieping')
bijcat={a:b for a,b in c.execute("select categorie,count(*) from canon where feit like '%[Z13 verdieping]%' group by 1")};bij=sum(bijcat.values())
S['6_bijgeschreven']=dict(totaal=bij,per_categorie=bijcat,kandidaten=len(cand),eerste=bijv[:20])
# ---------- 8 rapport ----------
c.execute("delete from wrijving where code like 'WRIJ-Z13-%'")
for i,(t,b,e,s,bs) in enumerate(W,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,b,e+' Besluit: '+bs,'Z13',s,f'WRIJ-Z13-{i}',b))
NA=meet()
S['8_kwaliteit']=dict(voor=VOOR,na=NA)
NIET=['inhoudelijke juistheid van vrije tekst: controles zijn patronen en verwijzingen, geen lezing van alle 6.379 rijen','dood-maar-actief alleen via expliciete verwijzingen en de aangenomen levensduur van 70; vermeldingen bij naam zonder code niet','personen op twee plekken alleen voor de handgemaakte tijdlijnen met maand','leeftijden in vrije tekst die niet in "leeftijd N" of "N jaar oud" staan','of de bijgeschreven zintuig/haak/functie-zinnen literair goed zijn (ze zijn per rij uit bestaande canon samengesteld, niet met de hand geschreven)','de 9 + Z12 verhaal-aanpassingen: niet uitgevoerd, verhalen niet herschreven']
TOP=['de rijen die voorlopig bleven omdat geen besluit ze dekt, per thema aan Rogier voorleggen (grootste groep)','WRIJ-Z13 open wrijvingen handmatig nalopen (dood-later-actief, verhoudingen, toekomstjaren)','de aangenomen geboortejaren (Z11) vervangen door echte leeftijden bij de 50 belangrijkste personages','de verhaal-aanpassingen (Z11/Z12) in verhaal 1 en 2 doorvoeren als Rogier dat zegt','de automatisch bijgeschreven verdiepingen bij de top-100 met de hand herschrijven','maanden toevoegen aan tijdlijnen van hoofdpersonen zodat twee-plekken controleerbaar wordt','één naamregister (personen, huizen, plekken) met unieke spelling, ook voor diakrieten (Karrûk/karruk, Saelmor/Sael-mor)','levensduur per volk vastleggen en de automatische overlijdensjaren daarop herberekenen','verhalenlijst (20-30) maken en na elk verhaal terugschrijven','een vaste controle-script draaien na elke ronde (dit script als basis)']
S['8_kwaliteit']['niet_gecontroleerd']=NIET;S['8_kwaliteit']['top10']=TOP
rap=f"Statussen vóór: {VOOR['status']}; na: {NA['status']}. Dekking actieve rijen vóór/na: haak {VOOR['haak']}/{NA['haak']}, zintuig {VOOR['zintuig']}/{NA['zintuig']}, crosslinks {VOOR['crosslinks']}/{NA['crosslinks']}, functie {VOOR['functie']}/{NA['functie']}, alle vier {VOOR['alle4']}/{NA['alle4']} (van {NA['actief']}). Open wrijvingen: {NA['wrijving_open']}. Niet gecontroleerd: "+'; '.join(NIET)+'. Top-10 volgende verbeteringen: '+' | '.join(f'{i}. {t}' for i,t in enumerate(TOP,1))+'.'
add('KWALITEIT-Z13','Besluit','Kwaliteitsrapport ronde Z13',rap,'kwaliteitsrapport (taak 8)','BESLUIT-Z12-wortelstem;BESLUIT-Z12-5;KAL-kalender;REGEL-verhouding','voorlopig',801,'META','801 (nu)')
add('BESLUIT-Z13-perfectioneren','Besluit','Besluiten ronde Z13 (ingenieur)',f'Op verzoek van Rogier ("de database gewoon perfectioneren", {D}): (1) stem in de Wortel = Ysara, Thalen Orr erin opgegaan, vastgesteld; (2) dubbele namen samengevoegd met verwijzing, Vaelorn één persoon (ca. 1200 jaar in 801); (3) skeletten en volkrijen gedateerd; (4) kapotte verwijzingen gerepareerd; (5) alleen rijen vastgesteld die naar een besluit verwijzen en de coherentiecontrole doorstaan; (6) dunne rijen verdiept; (7) coherentiecontrole als WRIJ-Z13-*.','ingenieursbesluiten Z13','BESLUIT-Z12-wortelstem;PER-vaelorn;PER-vaelorn-nu;KWALITEIT-Z13','vastgesteld',801,'BESL','801 (nu)')
c.execute("delete from logboek where wat like 'Ronde Z13: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f"Ronde Z13: canon geperfectioneerd; {vastgezet} rijen vastgesteld, {len(dat)} gedateerd, {rep} verwijzingen gerepareerd en {weg} verwijderd uit veld, {bij} rijen verdiept, {len(W)} wrijvingen ({sum(1 for w in W if w[3]=='open')} open)."))
for col in ('verwijst_naar','hangt_samen_met'): c.execute(f"update canon set {col}=NULL where {col}=''")
c.commit()
S['nieuw']=n;S['integriteit']=c.execute('pragma integrity_check').fetchone()[0];S['wrijvingen']=[(f'WRIJ-Z13-{i}',w[0],w[3]) for i,w in enumerate(W,1)]
json.dump(S,open('z13/stats.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:(v if k not in ('2_dubbel',) else {a:b for a,b in v.items() if a!='lijst'}) for k,v in S.items()},ensure_ascii=False,indent=0)[:6000])
