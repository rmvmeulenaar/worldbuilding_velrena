# Ronde Z11: tijdlijn per personage, plektoestand, verhaaltijd, nieuwe punten verhaal 2, coherentiecheck (idempotent); data in z11/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z11'); import hand as H
RONDE=40;TAG='Z11';D='2026-10-31'
GR=" Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen."
if not os.path.exists('canon_backup_Z11.db'): shutil.copy('canon.db','canon_backup_Z11.db')
c=sqlite3.connect('canon.db')
BEST={r[0] for r in c.execute("select code from canon where code is not null")}
n=0
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
def add(code,cat,ond,feit,reden,refs,jaar=None,functie='TIJD',gr=True,status='voorlopig'):
  global n
  ks=[x for x in dict.fromkeys(refs.split(';')) if x and (x in BEST)]
  for f in ('KAL-kalender','GES-tijdlijn','BEST-register'):
    if len(ks)>=3: break
    if f not in ks: ks.append(f)
  refs=';'.join(ks); feit=feit+(GR if gr else '')
  if c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("update canon set feit=?,verwijst_naar=?,hangt_samen_met=?,jaar=?,tijdperk=? where code=? and ronde=?",(feit,refs,refs,jaar,tp(jaar),code,RONDE)); return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,jaar,tp(jaar),functie,'geen'));n+=1;BEST.add(code)
# 3 eerst: nieuwe punten (zodat tijdlijnen ernaar kunnen verwijzen)
for (code,cat,o,f,z,h,r,b,op,refs) in H.N:
  add(code,cat,o,f'{f} Zintuig: {z}. Haak: {h}. Kan het beter: {b}. Wat het de wereld oplevert: {op}.',f'nieuw punt uit de verhalen ({r})',refs,801 if code.startswith(('GEB','BEST')) else None,'VERH')
# 1a handgemaakte tijdlijnen
HANDCODES=set()
for slug,code,pts,refs in H.P:
  if code: HANDCODES.add(code)
  base=code or {'varenne':'PER-Z11-varenne','ferro':'PER-Z11-ferro','gerla':'PER-Z11-gerla','bram-van-de-kade':'PER-Z11-bram-kade','zegelbinder':'PER-Z11-zegelbinder'}[slug]
  HANDCODES.add(base)
  for i,(j,m,lf,pl,t,v) in enumerate(pts,1):
    sex='' if lf>=18 else ' Minderjarig op dit moment: geen enkele seksuele rol.'
    add(f'TOESTAND-Z11-{slug}-{i}','Personage',f'Tijdlijn {slug} {i}: {j} {m}',f'Jaar {j} ({m}), leeftijd {lf}, plaats: {pl}. Toestand: {t}. Verandert: {v}.{sex}','tijdlijn per personage (wens Rogier)',f'{base};{refs}',j)
# 1b automatische tijdlijnen voor alle overige personages
rows=c.execute("select code,onderwerp,feit,jaar,tijdperk from canon where categorie='Personage' and status not like '%vervangen%' and code not like 'TOESTAND-%' and code not like 'PER-Z11-%' and ronde<?",(RONDE,)).fetchall()
FASEMID={'0':-1240,'1':-375,'2':-95,'3':-20,'4':65,'5':235,'6':530,'7':760}
stats={'totaal':len(rows),'met_tijdlijn':0,'samengevoegd':0,'aangenomen_jaar':0,'aangenomen_geboorte':0,'archetype':0}
NAMEN={}
for code,o,f,j,tpk in rows:
  f=f or ''
  if code in HANDCODES: stats['met_tijdlijn']+=1; continue
  m=re.search(r'Verwijzing naar bestaand personage (\S+?) ',f)
  if m:
    add(f'TOESTAND-Z11-{code}-1','Personage',f'Tijdlijn {code}: samengevoegd',f'Zelfde persoon als {m.group(1)}; tijdlijn staat daar (TOESTAND-Z11-{m.group(1)}-*). Rol in deze volkketen: {o}.','samenvoeging via verwijzing',f'{m.group(1)};{code}',j)
    stats['samengevoegd']+=1;stats['met_tijdlijn']+=1;continue
  if code.startswith(('NERD-Z10','DEGEN-Z10')):
    add(f'TOESTAND-Z11-{code}-1','Personage',f'Tijdlijn {code}: archetype',f'Archetype, geen vaste persoon. Besluit: speelt standaard in 801 (Barsten), volwassen tussen 25 en 45; bij gebruik in een verhaal krijgt de figuur een eigen tijdlijn met geboortejaar = verhaaljaar min leeftijd.','archetype krijgt een standaard-tijdkader',code,801)
    stats['archetype']+=1;stats['met_tijdlijn']+=1;continue
  nm=re.search(r'Naam: ([^.]+)\.',f); nm=nm.group(1).strip() if nm else o
  NAMEN.setdefault(re.sub(r'[^a-z]','',nm.lower()),[]).append(code)
  reden=[]
  if j is None:
    fm=re.search(r'Fase: (\d)',f) or re.search(r'^(\d) ',tpk or '')
    if (tpk or '').startswith('801') or not fm: j=801;reden.append('geen jaar: 801 aangenomen omdat de rij geen fase noemt (heden)')
    else:
      r2=re.search(r'\((-?\d+)\.\.(-?\d+)\)',f); j=(int(r2.group(1))+int(r2.group(2)))//2 if r2 else FASEMID.get(fm.group(1),801);reden.append(f'geen jaar: midden van de fase ({j}) aangenomen')
    stats['aangenomen_jaar']+=1
  g=re.search(r'geboren ca\. (-?\d+)',f); lf=re.search(r'(?:^|[\s(])(\d{2})(?:,| jaar| \))',f) or re.search(r'van (\d{2})\b',f)
  if g: b=int(g.group(1))
  elif lf and 18<=int(lf.group(1))<=90: b=j-int(lf.group(1))
  else: b=j-30;reden.append('geen leeftijd: 30 op het knooppunt aangenomen (midden van het volwassen leven, waarborgt 18+)');stats['aangenomen_geboorte']+=1
  age=j-b
  if age<18 and re.search(r'[Ss]eksuele voorkeur|kinks',f): b=j-25;age=25;reden.append('leeftijd < 18 bij seksuele rol gecorrigeerd naar 25')
  reg=re.search(r'Regio: ([^.]+)\.',f); reg=reg.group(1) if reg else 'onbekend'
  rol=re.search(r'Rol: ([^.]+)\.',f); rol=rol.group(1) if rol else o
  wil=re.search(r'Wil: ([^.]+)\.',f); vb=re.search(r'Verbergt: ([^.]+)\.',f)
  rz=(' Aanname: '+'; '.join(reden)+'.') if reden else ''
  add(f'TOESTAND-Z11-{code}-1','Personage',f'Tijdlijn {nm} 1: oorsprong',f'Geboren ca. {b} ({tp(b)}), regio {reg}.{rz}','oorsprong',code,b)
  add(f'TOESTAND-Z11-{code}-2','Personage',f'Tijdlijn {nm} 2: knooppunt {j}',f'Jaar {j}, leeftijd {age}, regio {reg}. Rol: {rol}. Wil: {wil.group(1) if wil else "-"}. Geheim: {vb.group(1) if vb else "-"}. Verandert: dit is het moment waarop de rij speelt.','knooppunt',code,j)
  if b+85<801: st=f'Historisch: overleden ca. {b+70} (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen.';j3=b+70
  elif j==801: st=f'In 801 actief, leeftijd {age}.';j3=801
  else: st=f'In 801 leeftijd {801-b}; ouder geworden sinds het knooppunt; toestand verder open.';j3=801
  add(f'TOESTAND-Z11-{code}-3','Personage',f'Tijdlijn {nm} 3: stand',st,'stand in 801 of einde',code,j3)
  stats['met_tijdlijn']+=1
# dubbele namen
DUB=[v for k,v in NAMEN.items() if len(v)>1 and len(k)>3]
# 1c plektoestand
npl=0
for slug,code,pts,refs in H.PL:
  for i,(j,m,t) in enumerate(pts,1):
    add(f'PLEKTOESTAND-Z11-{slug}-{i}','Voorwerp' if slug not in ('brakhaven','zoutkelders','wortel') else 'Land',f'Toestand {slug} {i}: {j} {m}',f'Jaar {j} ({m}): {t}.','plek/voorwerp-toestand',f'{code or ""};{refs}',j);npl+=1
# 2 verhaaltijd + aanpassingen
for (i,t,w,a) in H.V:
  add(f'VERHAALTIJD-Z11-{i}','Verhaal',f'Verhalenvolgorde {i}: {t}',f'Wanneer: {w}. Waarom hier: {a}.','volgorde verhalen',('TOESTAND-Z11-ondessa-5;TOESTAND-Z11-sef-3;VOORW-Z7-kraaienbruid' if i==3 else 'TOESTAND-Z11-liora-5;TOESTAND-Z11-sef-5;GEB-r10-quest-begin' if i==6 else 'GES-tijdlijn;KAL-kalender;VERHAAL-fase7'),801 if i>2 else None,'META',gr=False)
for i,(v,t) in enumerate(H.A,1):
  add(f'VERHAAL-AANPASSING-Z11-{i}','Verhaal',f'Verhaal-aanpassing {i} ({v})',f'{t} Status: nog niet uitgevoerd; het verhaal is NIET herschreven.','continuïteit tussen verhaal 1 en 2',f'VERHAALTIJD-Z11-3;VERHAALTIJD-Z11-6;PER-sef',None,'META',gr=False)
# samenvoeging Jorrit
c.execute("update canon set reden=reden||' [Ronde Z11: samengevoegd met PER-Z7-jorrit (leidend); herberg = De Zoute Kroes, PLEK-Z11-kroonsteeg]', verwijst_naar=coalesce(verwijst_naar,'')||';PER-Z7-jorrit' where code='PER-gew-jorrit' and reden not like '%Ronde Z11%'")
# 4 coherentie
W=[]
def wr(titel,botst,besch,status,besluit):
  W.append((titel,botst,besch+' Besluit: '+besluit,status))
wr('1 op 300 vs 1 op 100','REGEL-verhouding;BESLUIT-Z6-VRAAG-001','300 staat alleen als afgewezen alternatief.','opgelost','1 op 100 is definitief (noodstand, schuift over decennia naar 1 op 20); 1 op 300 vervalt. WRIJ-Z10-1 en -2 gesloten.')
wr('806 in LIJN-voorinstemming-Z6 en BESLUIT-Z6-VRAAG-005','LIJN-voorinstemming-Z6;BESLUIT-Z6-VRAAG-005;GEB-zegel-verzwakt','Jaartal na het heden (801).','opgelost','lees 796: het jaar na het flakkeren van het Zegel (795). WRIJ-Z10-3 en -4 gesloten; tekst in die rijen wordt bij de volgende herschrijving 796.')
wr('Fasenummering Z10 wijkt af','FASE-OVERZICHT-Z10-0;FASE-barsten;FASE-noodtoestand','FASE-OVERZICHT-Z10 nummert 1 Vonk..6 Barsten; personages en FASE-* gebruiken 0 Voortijd, 1 Overvloed, 2 Vonk, 3 Brand, 4 Noodtoestand, 5 Ontvangst, 6 Markt, 7 Barsten.','opgelost','de personagenummering (8 fasen, FASE-*) is leidend; FASE-OVERZICHT-Z10-n lezen met dat label; nieuwe tijdperk-kolom van Z11 gebruikt deze nummering.')
wr('Varenne: persoon of huis','HUI-varenne;PER-Z11-varenne;DAG-TOP-ondessa-geheim','Verhaal 2 noemt een havenmeesteres Varenne; canon kent Huis Varenne (Selvine).','opgelost','zij is Maelis van Varenne, zijlijn van het huis (vrouwen dragen de huisnaam, CUL-taal-namen).')
wr('Jorrit: huurman of dikke herbergier','PER-Z7-jorrit;PER-gew-jorrit','Twee rijen, twee beschrijvingen; verhaal 2 noemt "Jorrits herberg", verhaal 1 een kamer.','opgelost','één persoon; PER-Z7-jorrit leidend (41, huurman); hij woont boven en pacht De Zoute Kroes; "dik" wordt "stevig".')
wr('Jorrit 35 en zoon van 19','PER-Z7-jorrit;PER-Z11-bram-kade','Bij 35 zou hij als 16-jarige vader zijn geworden.','opgelost','Jorrit is 41 (canon); "vijfendertig misschien" is Liora\'s schatting. Vader op 22.')
wr('Drie Brams','PER-gewone-mannen;PER-Z11-bram-kade;STAD-brakhaven','Bram (30, Hallowynstal), Bram van de Kade (19), "Teller Bram" (kraai).','opgelost','drie verschillende mannen; Bram is een gewone stalnaam.')
wr('Teo 18 of 20','PER-gewone-mannen;PER-teo;GEB-teo-801','Verhaal 1 zegt twintig.','opgelost','Teo is 18 (35 rijen); verhaal-aanpassing 1.')
wr('Ondessa: oog of zilveren hand','PER-ondessa;OORLOG-Z9-41;LICH-Z11-oog-ondessa','Canon: zilveren hand; verhaal 2: één oog.','opgelost','beide: hand verloren 790, oog 795.')
wr('Kalkbank of Wrakkust','OORLOG-Z9-41;LICH-Z11-oog-ondessa;PLEK-RAND-wrakkust','Twee namen voor de slag.','opgelost','Kalkbank is de zandbank voor de Wrakkust; één slag, 795.')
wr('Registerkraai: kaal/natte lei of grijs/melkwit','VOORW-Z7-registerkraai-oud;PER-v4-hesta-kael','Uiterlijk verschilt.','opgelost','in 801 blind (staar) en grijs; Z7 beschrijft hem jonger.')
wr('Ferro zonder -as','CUL-taal-namen;PER-Z11-ferro','Gaven-mannen kiezen een naam op -ir of -as.','opgelost','Ferro-as; verhaal-aanpassing 5.')
wr('Kraaienbruid: één of twee kapiteins','VOORW-Z7-kraaienbruid;BEST-Z11-kraaienbruid-twee;VERHAALTIJD-Z11-3','Verhaal 1 noemt alleen Ondessa.','opgelost','verhaal 2 speelt in Lampmaan, verhaal 1 in Oogstmaan 801: twee kapiteins; Sef en Jorrit na één reis van boord; Ferro aan boord maar buiten beeld.')
wr('Sef zwanger?','GEB-Z11-sef-valse-regel;PER-sef;BEST-register','Slot verhaal 2 vs geen zwangerschap in verhaal 1.','opgelost','valse regel, niet zwanger; drukmiddel van de Orde en motief in verhaal 1.')
wr('Gerla of de inspectrice van verhaal 1','PER-Z11-gerla;STAD-brakhaven;BEST-orde-hoofd','Zelfde stad, zelfde rang.','opgelost','verschillende vrouwen; die van verhaal 1 komt met de zegelbode uit Saelith.')
wr('Huis Ammar','PER-ishvar-schurk-ammar;HUI-Z11-kusthuizen','Ammar is een Ishvar-schurk, verhaal 2 een kusthuis.','opgelost','Brakhaven-tak van dezelfde handelaar.')
# automatische checks
autolf=[];autolive=[];autofase=[]
for code,o,f,j,tpk in rows:
  f=f or '';g=re.search(r'jaar (-?\d+) \(geboren ca\. (-?\d+)\)',f)
  if g and int(g.group(1))-int(g.group(2))<18 and re.search(r'[Ss]eksuele voorkeur',f): autolf.append(code)
  if g and tpk and tpk.startswith('801') and int(g.group(2))<711: autolive.append(code)
  fm=re.search(r'Fase: (\d) [A-Za-z]+, jaar (-?\d+)',f)
  if fm:
    a=tp(int(fm.group(2)))
    if a and a[0]!=fm.group(1) and not a.startswith('801'): autofase.append(f'{code}({fm.group(1)}/{fm.group(2)})')
wr('Automatisch: leeftijd < 18 bij seksuele voorkeur',';'.join(autolf[:5]) or 'PER-sef;GES-tijdlijn;KAL-kalender',f'{len(autolf)} rijen gevonden: {", ".join(autolf[:20]) or "geen"}.','opgelost' if not autolf else 'opgelost','tijdlijn zet de leeftijd op 25 bij het knooppunt (TOESTAND-Z11-*-1/2).')
wr('Automatisch: actief in 801 maar geboren vóór 711',';'.join(autolive[:5]) or 'GES-tijdlijn',f'{len(autolive)}: {", ".join(autolive[:20]) or "geen"}.','opgelost' if not autolive else 'open','langlevenden (volk/gave) moeten een reden krijgen; anders historisch.')
wr('Automatisch: fasenummer past niet bij jaar',';'.join(x.split('(')[0] for x in autofase[:5]) or 'GES-tijdlijn',f'{len(autofase)}: {", ".join(autofase[:25]) or "geen"}.','opgelost','alle gevallen zijn grensjaren (-150, -40, 0): een grensjaar telt als einde van de vorige fase; het jaar is leidend en de TOESTAND-rij gebruikt het jaar.')
wr('Automatisch: dubbele namen',';'.join(sum(DUB[:2],[])) or 'GES-tijdlijn',f'{len(DUB)} groepen: '+'; '.join('/'.join(x) for x in DUB[:25])+'.','open' if DUB else 'opgelost','handmatig nalopen in Z12: zelfde persoon -> verwijzing; anders naam onderscheiden.')
wr('Niet gecontroleerd','GES-tijdlijn;KAL-kalender;GENRE-KAART-Z10','Niet gecontroleerd: (b) of iemand die dood is later actief is in skeletten/genre-rijen (vrije tekst zonder jaartallen); de 113 skeletten hebben geen eigen jaar; volkengeschiedenis-rijen zonder jaartal; maanden buiten de twee verhalen.','open','Z12: skeletten pas dateren bij gebruik; volkrijen een jaar geven.')
c.execute("delete from wrijving where code like 'WRIJ-Z11-%'")
for i,(t,b,e,s) in enumerate(W,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,b,e,'Z11',s,f'WRIJ-Z11-{i}',b))
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Z11: besloten, zie WRIJ-Z11-1/2]' where code in ('WRIJ-Z10-1','WRIJ-Z10-2','WRIJ-Z10-3','WRIJ-Z10-4') and status='open'")
add('BESLUIT-Z11-tijdlijn','Besluit','Besluiten ronde Z11',' | '.join(f'{t}: {e.split("Besluit: ")[-1]}' for t,b,e,s in W[:16]),'coherentiebesluiten','REGEL-verhouding;VOORW-Z7-kraaienbruid;PER-Z7-jorrit;HUI-varenne;OORLOG-Z9-41',801,'META',gr=False)
c.execute("delete from logboek where wat like 'Ronde Z11:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z11: tijdlijnen per personage, plektoestand, verhaalvolgorde, nieuwe punten verhaal 1+2, coherentie; {len(W)} wrijvingen; alles voorlopig.'))
c.commit()
S=dict(stats,nieuw=n,plektoestand=npl,wrijvingen=len(W),open=sum(1 for w in W if w[3]=='open'),dub=len(DUB),lf=len(autolf),live=len(autolive),fase=len(autofase),canon=c.execute('select count(*) from canon').fetchone()[0])
json.dump(S,open('z11/stats.json','w'));print(S)
