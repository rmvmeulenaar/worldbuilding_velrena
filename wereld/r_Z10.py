# Ronde Z10: kinkfuncties, Saw, comedy, romantiek, helden, nerd/degen/ontwaak, integratie, optimalisatie (idempotent); data in z10/*.py
import sqlite3,shutil,os,sys,re
sys.path.insert(0,'z10')
import kinkfunc as KF,saw,comedy,romance,held,nerd,degen,ontwaak
RONDE=39;TAG='Z10';D='2026-10-31'
GR=" Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; geweld en horror mogen hard."
if not os.path.exists('canon_backup_Z10.db'): shutil.copy('canon.db','canon_backup_Z10.db')
c=sqlite3.connect('canon.db');n=0
BEST={r[0] for r in c.execute("select code from canon where code is not null")}
CAT={r[0]:r[1] for r in c.execute("select code,categorie from canon where code is not null")}
FALLBACK={'Kinks en situaties':['BEST-orde-hoofd','ECO-geld','GOD-ysa'],'Horror':['GEH-zegel-Z1','BEST-orde-hoofd','REG-saelith'],
 'Comedy':['BEST-register','STAD-brakhaven','ORDE-rangen'],'Romantiek':['KAL-kalender','DAG-werk','BEST-register'],'Held':['SEKTE-annalisten','KAL-kalender','ORDE-doel-geloof'],
 'Personage':['BEST-register','DAG-werk','REG-saelith'],'Verhaal':['QST-queeste','GEH-zegel-Z1','BEST-orde-hoofd'],'Genre':['REG-overzicht','BEST-orde-hoofd','GEH-zegel-Z1']}
def R(refs,cat='Verhaal',minimum=3):
  k=[x for x in refs.split(';') if x in BEST]
  for f in FALLBACK.get(cat,FALLBACK['Verhaal']):
    if len(set(k))>=minimum: break
    if f in BEST: k.append(f)
  return ';'.join(dict.fromkeys(k))
def add(code,cat,ond,feit,reden,refs,tech='geen',functie='VERH',afst=None,status='voorlopig',gr=True):
  global n
  refs=R(refs,cat)
  if code in BEST and c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("update canon set feit=?,verwijst_naar=?,hangt_samen_met=? where code=? and ronde=?",(feit+(GR if gr else ''),refs,refs,code,RONDE)); return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie,afstoting) values(?,?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit+(GR if gr else ''),status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,tech,functie,afst));n+=1
  BEST.add(code);CAT[code]=cat
def ond(code): r=c.execute("select onderwerp from canon where code=?",(code,)).fetchone(); return r[0] if r else code
# 1. kinkfuncties
NET={}
def kf(i,old,doms,tekst,refs):
  ds=doms.split(';');refs=';'.join([old]+[KF.DOM[d] for d in ds]+refs.split(';'))
  add(f'KINKFUNC-Z10-{i}','Kinks en situaties',f'Kinkfunctie: {ond(old)}',f'Functie in de wereld ({", ".join(KF.DOMNAAM[d] for d in ds)}): {tekst} Haak: wie deze functie kent, kan haar misbruiken; elke kink is zo ook een intrigemiddel.','kinks krijgen een functie in de wereld (wens Rogier)',refs,'geen','|'.join(ds))
  for d in ds: NET.setdefault(KF.DOMNAAM[d],[]).append(old)
i=0
for old,(doms,t,r) in KF.K.items(): i+=1;kf(i,old,doms,t,r)
for j,(d,t,r) in enumerate(KF.R7,1): i+=1;kf(i,f'EROS-RAUW-Z7-{j}',d,t+'.',r)
for j,d in enumerate(KF.B8D,1):
  i+=1;t=KF.B8F.get(j,f'{ond(f"BODY-Z8-{j}").replace("Vorming: ","")} is in de wereld een zaak van {KF.DOMNAAM[d]}: wie dit beheerst heeft invloed bij de gilden en de huizen')
  kf(i,f'BODY-Z8-{j}',d,t+'.',f'BEST-gilden;LICH-gaven-vervorming;BODY-Z8-5')
NKF=i
# netwerk: domeinen per kink
dpk={}
for code,refs in c.execute("select code,verwijst_naar from canon where code like 'KINKFUNC-Z10-%'"):
  ks=refs.split(';');old=ks[0];doms={CAT.get(x) for x in ks[1:] if CAT.get(x)}-{None}
  dpk[old]=len(doms)
weinig=[k for k,v in dpk.items() if v<4]
add('KINK-NETWERK-Z10','Kinks en situaties','Kink-netwerk Z10','Per domein: '+'; '.join(f'{d}: {len(v)} kinks (bv. {", ".join(v[:4])})' for d,v in sorted(NET.items()))+f'. Kinks met functie: {len(dpk)} van 150 (KINK-Z8 60, EROS-RAUW-Z7 40, BODY-Z8 50). Gemiddeld {sum(dpk.values())/len(dpk):.1f} categorieën per kink; minder dan 4: {len(weinig)} ({", ".join(weinig[:10])}). Geen kink zonder functie of domein.','overzicht kinknetwerk','KINK-Z8-1;BODY-Z8-1;EROS-RAUW-Z7-1;BEST-orde-hoofd','geen','META',gr=False)
# 2. Saw
k=0
for (nm,op,rg,ke,pr,wd,zi,af,r) in saw.V:
  k+=1;add(f'SAW-Z10-{k}','Horror',f'Saw-val: {nm}',f'Opbouw: {op}. Regels: {rg}. De keuze: {ke}. Prijs: {pr}. Wending: {wd}. Zintuig: {zi}. Afstoting: {af}/10. Haak: de moraal van de speler is de echte inzet. Geen seks; gruwel alleen.','Saw-achtige horror (wens Rogier)',r,'zegelsteen','HORROR',int(af))
for (nm,wie,ps,mo,r) in saw.M:
  k+=1;add(f'SAW-Z10-{k}','Horror',f'Spelmeester: {nm}',f'Wie in de canon: {wie}. Psychologie: {ps}. Motief: {mo}. Zintuig: het tikken van een zandloper, de geur van kalk en oude inkt. Haak: elke spelmeester wil gestopt worden door de juiste speler.','spelmeester',r,'geen','HORROR',8)
for (o,t,r) in saw.L:
  k+=1;add(f'SAW-Z10-{k}','Horror',f'Saw: {o}',f'{t}. Zintuig: koud metaal, eigen adem, tikkende steen. Prijs: lichaam of loyaliteit. Haak: wie de val overleeft draagt een kerf en een geheim.','Saw-achtige horror',r,'zegelsteen','HORROR',8)
for j,(t,hp,op,cl,e,r) in enumerate(saw.S,1):
  add(f'SAW-SKELET-Z10-{j}','Verhaal',f'Saw-skelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde en prijs: {e}. Haak: het spel was nooit het doel.','Saw-verhaalskelet',r+f';SAW-Z10-{j}')
# 3. Comedy
for j,(g,s,ty,r,h) in enumerate(comedy.C,1):
  add(f'COMEDY-Z10-{j}','Comedy',f'Comedy: {g}',f'Situatie: {s}. Type: {ty}. Haak: {h}. Zintuig: gelach, gekraak van lak en papier, de geur van stof en inkt.','comedy (wens Rogier)',r,'geen','COMEDY')
for j,(t,hp,op,cl,e,r) in enumerate(comedy.S,1):
  add(f'COMEDY-SKELET-Z10-{j}','Verhaal',f'Comedyskelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}. Haak: de grap opent een echt probleem.','comedyskelet',r)
# 5a romantiek
for j,(o,k_,z,p,h,r) in enumerate(romance.R,1):
  add(f'ROMANCE-Z10-{j}','Romantiek',f'Romantiek: {o}',f'{k_}. Zintuig: {z}. Prijs: {p}. Haak: {h}. Alle geliefden volwassen.','zoetsappige romantiek (wens Rogier)',r,'geen','ROM')
for j,(t,hp,op,cl,e,r) in enumerate(romance.S,1):
  add(f'ROMANCE-SKELET-Z10-{j}','Verhaal',f'Romantiekskelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}. Haak: liefde kost iets in Velmara.','romantiekskelet',r)
# 5b helden
for j,(o,d,z,p,h,r) in enumerate(held.H,1):
  add(f'HELD-Z10-{j}','Held',f'Held: {o}',f'Daad: {d}. Zintuig: {z}. Prijs: {p}. Haak: {h}.','heldenverhalen (wens Rogier)',r,'geen','HELD')
for j,(t,hp,op,cl,e,r) in enumerate(held.S,1):
  add(f'HELD-SKELET-Z10-{j}','Verhaal',f'Heldenskelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}. Haak: de Orde zal dit verhaal herschrijven.','heldenskelet',r)
# 7 nerd/degen/ontwaak
for j,(w,wa,om,p,h,r) in enumerate(nerd.N,1):
  add(f'NERD-Z10-{j}','Personage',f'Underdog vereerd: {w}',f'Waarom vereerd: {wa}. Omslag en aanbidders: {om}. Wat het doet: hij/zij leert dat verering een kooi van goud is. Prijs: {p}. Haak: {h}. Zintuig: wierook en bloemen waar vroeger stof lag.','nerd/underdog die vereerd wordt (wens Rogier)',r,'geen','INTR')
for j,(t,hp,op,cl,e,r) in enumerate(nerd.S,1):
  add(f'NERD-SKELET-Z10-{j}','Verhaal',f'Underdog-skelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}.','underdogskelet',r)
for j,(w,v,st,om,u,r) in enumerate(degen.D,1):
  add(f'DEGEN-Z10-{j}','Personage',f'Degeneratie: {w}',f'Vorm: {v}. Stappen van de afglijding: {st}. Wat de omgeving doet: {om}. Uitkomst: {u}. Zintuig: wat eerst bitter smaakte, smaakt nu zoet. Haak: iemand ziet het als eerste en zwijgt.','morele degeneratie (wens Rogier)',r,'geen','INTR')
for j,(t,hp,op,cl,e,r) in enumerate(degen.S,1):
  add(f'DEGEN-SKELET-Z10-{j}','Verhaal',f'Degeneratieskelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}.','degeneratieskelet',r)
for j,(w,vk,ee,zi,we,ph,r) in enumerate(ontwaak.O,1):
  add(f'ONTWAAK-Z10-{j}','Volken seksualiteit',f'Ontwaking (volwassen): {w}',f'Volk/klasse: {vk}. De eerste keer dat ze/hij durft te willen: {ee}. Zintuigen veranderen: {zi}. Wat de wereld zegt: {we}. Prijs en haak: {ph}.','seksuele ontwaking van volwassenen (wens Rogier)',r,'geen','LUST')
for j,(t,hp,op,cl,e,r) in enumerate(ontwaak.S,1):
  add(f'ONTWAAK-SKELET-Z10-{j}','Verhaal',f'Ontwakingsskelet: {t}',f'Hoofdpersoon (volwassen): {hp}. Opbouw: {op}. Climax: {cl}. Einde: {e}.','ontwakingsskelet',r)
c.commit()
# 6 integratie
PRE={'actie':'ACTIE-Z9-','oorlog':'OORLOG-Z9-','horror':'HORROR-Z9-','saw':'SAW-Z10-','comedy':'COMEDY-Z10-','romantiek':'ROMANCE-Z10-','helden':'HELD-Z10-','nerd':'NERD-Z10-','degeneratie':'DEGEN-Z10-','ontwaking':'ONTWAAK-Z10-','kinkfunctie':'KINKFUNC-Z10-'}
ALLE={g:[(r[0],r[1],r[2]) for r in c.execute("select code,onderwerp,verwijst_naar from canon where code like ? and code not like '%SKELET%'",(p+'%',))] for g,p in PRE.items()}
GEBF={'GEB-ysa-oogstcultus':0,'GEB-sterrensteen-val':0,'GEB-sterrensteen-inslag':0,'GEB-zegel':0,'GEB-zegel-gelegd':0,'GEB-eerste-vonk':1,'GEB-vonkkoningen':1,'GEB-val-lisk':1,'GEB-zusterburcht':2,'GEB-orric-vonk':2,'GEB-kaldra-eed':2,'GEB-vonkpest':3,'GEB-schisma-stilte':3,'GEB-grote-pest':4,'GEB-deelwet':4,'GEB-melkstallen':4,'GEB-zaadbeurs':5,'GEB-mirre-vrijhaven':5,'GEB-ves-anath-verlaten':5,'GEB-gunstbrief-crash':5,'GEB-kharvos-inval':6,'GEB-zegel-verzwakt':6,'GEB-bloednacht-lisk':7,'GEB-heden':7,'OORLOG-Z9-1':0,'GOD-ysa':0,'FASE-vonk':1,'FASE-ontvangst':4,'FASE-markt':5,'FASE-barsten':6}
def fase(code,ond_,refs):
  m=re.search(r'fase (\d)',ond_ or '')
  if m: return int(m.group(1))
  fs=[GEBF[x] for x in (refs or '').split(';') if x in GEBF]
  return min(fs) if fs else 7
FASEN={f:{} for f in range(8)}
for g in ['actie','oorlog','horror','romantiek','helden','saw','degeneratie']:
  for code,o,r in ALLE[g]: FASEN[fase(code,o,r)].setdefault(g,[]).append(code)
NAAM=['0 Makers en Val','1 Vonk','2 Brand','3 Noodtoestand','4 Ontvangst','5 Markt','6 Barsten','7 Heden (801)']
for f in range(8):
  d=FASEN[f];txt='; '.join(f'{g}: {", ".join(v[:12])}{" …" if len(v)>12 else ""} ({len(v)})' for g,v in d.items()) or 'nog geen genre-rijen; kans voor een volgende ronde'
  add(f'FASE-OVERZICHT-Z10-{f}','Tijdperk',f'Genre-overzicht fase {NAAM[f]}',f'Genres in fase {NAAM[f]}: {txt}. Haak: elke fase heeft zijn eigen soort held, gruwel en liefde.','tijdlijn-integratie',(f'LIJN-fase-{f};' if 1<=f<=5 else '')+'GEB-heden;GEH-zegel-Z1;KAL-kalender;'+';'.join(sum(d.values(),[])[:6]),'geen','META',gr=False)
def genres_voor(sleutels):
  out={}
  for g,rows in ALLE.items():
    for code,o,r in rows:
      if any(s in (r or '').split(';') for s in sleutels): out.setdefault(g,[]).append(code)
  return out
VOLKEN=[r[0] for r in c.execute("select code from canon where categorie='Volken' and code like 'VOLK-%' and code not like 'VOLK-GENRES%' and status not like '%vervangen%'")]
for v in VOLKEN:
  g=genres_voor([v]);kort=v.replace('VOLK-','')
  txt='; '.join(f'{k}: {", ".join(x[:8])} ({len(x)})' for k,x in g.items())
  add(f'VOLK-GENRES-Z10-{kort}','Volken',f'Genres bij {ond(v)}',f'Passende genres en rijen: {txt or "nog weinig; kans"}. Sterkste genres: {", ".join(sorted(g,key=lambda k:-len(g[k]))[:3])}.','genres per volk',f'{v};GENRE-KAART-Z10;FASE-OVERZICHT-Z10-7;'+';'.join(sum(g.values(),[])[:4]),'geen','META',gr=False)
STADREG={'STAD-brakhaven':'REG-zoutkust','STAD-saelith':'REG-saelith','STAD-isla-mirre':'REG-saelith','STAD-lisk':'REG-ambergaard','STAD-ijsgraf':'REG-hoogvrouwe','STAD-qesh':'REG-rosse','STAD-kharvos-hoornburg':'REG-kharvos-B1','STAD-stille-zoutklooster':'REG-stille','PLEK-dhurn-baden':'REG-hoogvrouwe','PLEK-groen-korf':'REG-groenmuil','PLEK-kharvos-grensfort':'REG-kharvos-B1','PLEK-kharvos-spiegelhuis':'REG-kharvos-B1','PLEK-saelith-gondelwerf':'REG-saelith','PLEK-saelith-registerkelder':'REG-saelith','PLEK-LICH-melkstal-amber':'REG-ambergaard','VOORW-Z7-kraaienbruid':'REG-zoutkust'}
for rg in ['REG-saelith','REG-ambergaard','REG-hoogvrouwe','REG-zoutkust','REG-groenmuil','REG-rosse','REG-stille','REG-kharvos-B1']:
  g=genres_voor([rg]+[s for s,x in STADREG.items() if x==rg]);kort=rg.replace('REG-','')
  txt='; '.join(f'{k}: {", ".join(x[:8])} ({len(x)})' for k,x in g.items())
  add(f'REGIO-GENRES-Z10-{kort}','Regio',f'Genres in {ond(rg)}',f'Passende genres en rijen: {txt or "nog weinig; kans"}.','genres per regio',f'{rg};GENRE-KAART-Z10;FASE-OVERZICHT-Z10-7;'+';'.join(sum(g.values(),[])[:4]),'geen','META',gr=False)
GK=[('erotiek','EROS-GRENZEN-Z7, EROS-RAUW-Z7-1..40, EROS-STOP-Z7-*','bijbel 21'),('kinks','KINK-Z8-1..60, KINKFUNC-Z10-1..150, KINK-NETWERK-Z10','bijbel 22, 24'),('lichaam','BODY-Z8-1..50, LICH-*','bijbel 14, 22'),('actie','ACTIE-Z9-1..50','bijbel 23'),('oorlog','OORLOG-Z9-1..50','bijbel 23'),('horror','HORROR-Z9-1..60','bijbel 23'),('Saw','SAW-Z10-1..40, SAW-SKELET-Z10-1..10','bijbel 24'),('comedy','COMEDY-Z10-1..60, COMEDY-SKELET-Z10-1..10','bijbel 24'),('romantiek','ROMANCE-Z10-1..50, ROMANCE-SKELET-Z10-1..10','bijbel 24'),('helden','HELD-Z10-1..50, HELD-SKELET-Z10-1..10','bijbel 24'),('underdog','NERD-Z10-1..40','bijbel 24'),('degeneratie','DEGEN-Z10-1..40','bijbel 24'),('ontwaking','ONTWAAK-Z10-1..40','bijbel 24'),('intrige','BEST-*, ORDE-stille-hand, BEST-geheim-*','bijbel 04, 05'),('sf','BEST-makers, HORROR-Z9-59 (Rekenaar), GEB-sterrensteen-*','bijbel 06, 11, 17')]
COMB='Combinaties: erotische komedie (COMEDY-SKELET-Z10-5 + KINK-Z8-58); Saw + romantiek (SAW-Z10-17 tweelingslot); held + degeneratie (HELD-Z10-47 -> DEGEN-Z10-30); underdog + ontwaking (NERD-Z10-17 -> ONTWAAK-Z10-8); horror + liefde (ROMANCE-Z10-43 ijsgraf); oorlog + romantiek (ROMANCE-Z10-9); sf + held (HELD-Z10-1 Ysa, HORROR-Z9-59); kink + spionage (KINKFUNC-Z10-8 latex-kap).'
add('GENRE-KAART-Z10','Genre','Genrekaart Velmara','; '.join(f'{a}: {b} ({c_})' for a,b,c_ in GK)+'. '+COMB+' Alles hangt aan één oorzaak: het Zegel (GEH-zegel-Z1).','genrekaart','GEH-zegel-Z1;KINK-NETWERK-Z10;HORROR-Z9-59;HELD-Z10-1;COMEDY-Z10-1;ROMANCE-Z10-1;SAW-Z10-1','geen','META',gr=False)
c.commit()
# 8 optimaliseren
# (a) 60 korte Z8/Z9-rijen bijschrijven (kinks met functie)
kort=[] if c.execute("select 1 from canon where code like '%-L10'").fetchone() else c.execute("select code,categorie,onderwerp,feit,verwijst_naar,techniek,functie,afstoting from canon where ronde in (37,38) and status='voorlopig' and (code like 'KINK-Z8-%' or code like 'BODY-Z8-%' or code like 'VERLEID-Z8-%' or code like 'ACTIE-Z9-%') order by length(feit) limit 60").fetchall()
KFMAP={r[1].split(';')[0]:(r[0],r[2]) for r in c.execute("select code,verwijst_naar,feit from canon where code like 'KINKFUNC-Z10-%'")}
nA=c.execute("select count(*) from canon where code like '%-L10'").fetchone()[0]
for code,cat,o,feit,refs,tech,fu,af in kort:
  nc=code+'-L10'
  extra=''
  if code in KFMAP: extra+=' '+KFMAP[code][1].split(' Haak:')[0].replace(GR,'')
  links=[x for x in (refs or '').split(';') if x in BEST][:4]
  extra+=' Verbonden met: '+'; '.join(f'{ond(x)} ({x})' for x in links)+'.'
  extra+=' Zintuig erbij: de geur van warme huid en lak, het zachte kraken van leer of touw.' if cat!='Actie' else ' Zintuig erbij: zweet, ijzer, het bonzen van eigen hart.'
  extra+=f' Haak: wat hier gebeurt, wordt gezien door iemand die het later gebruikt (zie {KFMAP[code][0] if code in KFMAP else "GENRE-KAART-Z10"}).'
  basis=feit.replace(GR,'').split(' Veiligheidslabel')[0]
  add(nc,cat,o,basis+extra,f'bijgeschreven versie van {code} (optimalisatie)',';'.join([code]+links+([KFMAP[code][0]] if code in KFMAP else [])),tech or 'geen',fu or 'LUST',af)
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde Z10: vervangen door {nc}]',code));nA+=1 if False else 0
# (b) dubbele rijen (zelfde genormaliseerd onderwerp, zelfde categorie)
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
seen={};dub=[]
for cid,code,cat,o in c.execute("select id,code,categorie,onderwerp from canon where status in ('voorlopig','vastgesteld') and code not like '%-L10' order by id").fetchall():
  key=(cat,norm(o))
  if len(key[1])<6: continue
  if key in seen: dub.append((code,seen[key]))
  else: seen[key]=code
for code,orig in dub:
  c.execute("update canon set status='voorlopig, vervangen', reden=reden||?, verwijst_naar=coalesce(verwijst_naar,'')||? where code=? and status not like '%vervangen%'",(f' [Ronde Z10: dubbel van {orig}, samengevoegd via verwijzing]',';'+orig,code))
# (c) tegenstrijdigheden: getallen en jaartallen
TEG=[]
pat={'verhouding':(r'\b1 op (\d{2,4})\b',lambda v:v in {'200','300','50','500'}),'jaren na 801':(r'\b(?:in|anno|sinds) (\d{3,4})\b',lambda v:801<int(v)<3000),'jaartal >801':(r'\bjaar (\d{4})\b',lambda v:int(v)>801)}
for nm,(p,bad) in pat.items():
  for code,feit in c.execute("select code,feit from canon where status in ('voorlopig','vastgesteld')"):
    for v in re.findall(p,feit or ''):
      if bad(v): TEG.append((nm,code,v))
c.execute("delete from wrijving where code like 'WRIJ-Z10-%'")
for j,(nm,code,v) in enumerate(TEG[:30],1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(f'{nm}: {v} in {code}',f'{code};REGEL-verhouding;GEB-heden',f'Gevonden in Z10-controle: waarde {v} wijkt af van de canon (1 op 100, noodstand naar 1 op 20; heden = 801). Voorstel: lezen als historisch/lokaal of herschrijven in een volgende ronde.','Z10','open',f'WRIJ-Z10-{j}',code))
# (d) actieve rijen zonder functie of zonder crosslink
CATDEF={}
for cat,code in c.execute("select categorie,min(code) from canon where code is not null and status in ('voorlopig','vastgesteld') group by categorie"): CATDEF[cat]=code
zf=c.execute("select count(*) from canon where status in ('voorlopig','vastgesteld') and (functie is null or functie='')").fetchone()[0]
c.execute("update canon set functie='VERH' where status in ('voorlopig','vastgesteld') and (functie is null or functie='') and categorie in ('Verhaal','Personage')")
c.execute("update canon set functie='WERELD' where status in ('voorlopig','vastgesteld') and (functie is null or functie='')")
zl=0
for cid,cat,code in c.execute("select id,categorie,code from canon where status in ('voorlopig','vastgesteld') and (verwijst_naar is null or verwijst_naar='')").fetchall():
  d=CATDEF.get(cat,'GEH-zegel-Z1');d='GEH-zegel-Z1' if d==code else d
  c.execute("update canon set verwijst_naar=? where id=?",(d+';GENRE-KAART-Z10',cid));zl+=1
# (g) controle: nieuwe rijen met <3 bestaande verwijzingen
nieuw=c.execute("select code,verwijst_naar from canon where ronde=?",(RONDE,)).fetchall()
te_weinig=[cd for cd,r in nieuw if len({x for x in (r or '').split(';') if x in BEST and x!=cd})<3]
c.commit()
import dekking_z1
txt=dekking_z1.meet(c).replace('Nog dun:','[Z10] Nog dun:')
lagen={g:len(v) for g,v in ALLE.items()}
rap=f'Rijen per laag: {lagen}. Optimalisatie: {nA} korte rijen bijgeschreven, {len(dub)} dubbele samengevoegd, {len(TEG)} mogelijke tegenstrijdigheden (max 30 als wrijving), {zf} rijen zonder functie gevuld, {zl} rijen zonder verbinding verbonden. Nieuwe Z10-rijen met <3 echte verwijzingen: {len(te_weinig)}. {txt} Top-10 volgende ronde: 1) Z10-rijen per stuk tot Z1-lengte uitschrijven; 2) Saelith en Stille extra zintuig; 3) per fase 0-3 meer romantiek en helden; 4) Orrim/Ves-Lethi meer comedy; 5) Saw-vallen koppelen aan concrete plekken; 6) ontwaking per klasse uitbreiden; 7) degeneratie aan bestaande PER-rijen koppelen; 8) open WRIJ-Z10 beslissen; 9) skeletten testen met korte verhalen; 10) alle voorlopige rijen in blokken laten goedkeuren door Rogier.'
c.execute("delete from canon where code='ZINT-DEKKING-Z10'")
c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,techniek,functie) values(?,?,?,?,?,?,?,?,?,?,?)",('Zintuigen','Kwaliteitsrapport Z10',rap,'voorlopig','Ronde Z10: meting','ZINT-DEKKING-Z9',RONDE,'ZINT-DEKKING-Z10','REG-overzicht;ZINT-DEKKING-Z9;GENRE-KAART-Z10','geen','META'))
c.execute("update canon set status='voorlopig, vervangen', reden=reden||' [Ronde Z10: vervangen door ZINT-DEKKING-Z10]' where code='ZINT-DEKKING-Z9' and status not like '%vervangen%'")
c.execute("delete from logboek where wat like 'Ronde Z10:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z10: {NKF} kinkfuncties, saw/comedy/romantiek/helden/nerd/degen/ontwaak + skeletten, integratie (fase/volk/regio/genrekaart), optimalisatie; alles voorlopig.'))
c.commit()
print('nieuw',n,'canon',c.execute('select count(*) from canon').fetchone()[0]);print(rap);print('dubbel voorbeeld',dub[:8]);print('teg',TEG[:10]);print('te weinig',te_weinig[:10])
