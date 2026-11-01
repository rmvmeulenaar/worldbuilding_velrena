# Ronde V3: vier technologieën + ontstaansketens (idempotent)
import sqlite3,shutil,os
RONDE=25;TAG='V3'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
if not os.path.exists('canon_backup_V3.db'): shutil.copy('canon.db','canon_backup_V3.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  refs=';'.join(r for r in refs.split(';') if r)
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1
FASE={1:('1 Overvloed',-400),2:('2 Vonk',-100),3:('3 Brand',-20),4:('4 Noodtoestand',0),5:('5 Ontvangst',250),6:('6 Markt',500),7:('7 Barsten',801)}
exec(open('v3/data.py',encoding='utf-8').read())
OORSPRONG['metaal'][1]=(1,'Toeval: een volwassen Dhurn-mijnwerkster legt haar hand op een paneel en een stem spreekt in een dode taal.','aanraking','legende van de Sprekende Kluis','VOLK-dhurn')
STAP=['Aanleiding of nood','Eerste uitvinder of toeval','Mislukte pogingen','Doorbraak','Gestolen of verborgen','Slachtoffers','Verspreiding','Vervolgramp']
for k,d in T.items():
  for p in d['per']:
    add('PER-'+p[0],'Personage',p[1],f"Naam: {p[1]}. Rol: {p[2]} van {d['naam']}. {p[3]}"+GR,f'{p[2]} techno-{k}',f'TECHNO-{k}')
  add(f'TECHNO-{k}','Techniek',d['naam'],f"Oorsprong: {d['oorsprong']} Bouwstoffen: {d['stof']} Energie: {d['energie']} Kosten: {d['kosten']} Makers: {d['maker']} Bewaking: {d['bewaker']} Faalwijze: {d['faal']} Hoe het voelt: {d['gevoel']}",'vier technologieën','TECHNO-REGEL;GENRE-zegelpunk;TECH-GESCH-1',afstoting=d['afst'],aantrekking=d['aantr'],aantrekking_bron=d['abron'])
  for t,txt in d['toep'].items():
    add(f'TECHNO-{k}-{t}','Techniek',f"{d['naam']}: {t}",txt+(GR if t=='erotiek' else ''),'toepassing',f'TECHNO-{k}',functie=('LUST' if t=='erotiek' else None))
  for i,(nm,f,o,pr,r) in enumerate(d['items'],1):
    add(f'TECH-ITEM-{k}-{i}','Techniek',nm,f'Voorwerp ({k}). Functie: {f}. Ontwerper: {o}. Prijs: {pr}. Risico: {r}.'+(GR if 'erot' in f else ''),'voorbeeldvoorwerp',f'TECHNO-{k}')
  for i,(s,txt) in enumerate(d['haken'],1):
    add(f'HAAK-techno-{k}-{i}','Verhaal',f'{s.capitalize()}-haak: {d["naam"]}',txt+GR,'verhaalhaak',f'TECHNO-{k}',functie={'intrige':'INTR','thriller':'THRL','romance':'ROM'}[s])
  for i,(fase,txt,oor,gev,refs) in enumerate(OORSPRONG[k],1):
    t,j=FASE[fase]
    add(f'OORSPRONG-{k}-{i}','Geschiedenis',f'Ontstaan {k} {i}: {STAP[i-1]}',f'{STAP[i-1]} (fase {t}). {txt} Oorzaak: {oor}. Gevolg: {gev}.'+GR,'ontstaansketen',f'TECHNO-{k};{f"OORSPRONG-{k}-{i-1}" if i>1 else ""};{refs}',jaar=j,tijdperk=t)
add('OORSPRONG-verbanden','Geschiedenis','Verbanden tussen de vier ontstaansketens',VERBANDEN,'wie leerde van wie','OORSPRONG-gave-4;OORSPRONG-metaal-5;OORSPRONG-bio-7;OORSPRONG-zegelsteen-5')
add('TECHNO-REGEL','Techniek','Techniekregel na V3 (vier technologieën)',REGEL,'herziet TECH-REGEL','TECH-REGEL;TECHNO-gave;TECHNO-metaal;TECHNO-bio;TECHNO-zegelsteen')
add('TECHNO-MIX','Techniek','Mengvormen en botsingen','; '.join(f'{a}: {b}' for a,b in MIX),'mix','TECHNO-REGEL')
add('TECHNO-TIJDLIJN','Techniek','Tijdlijn van technologieën per fase',TIJD,'tijdlijn','TECHNO-REGEL')
add('TECHNO-SCHAAL','Techniek','Schaal walging/aantrekking per technologie',SCHAAL,'schaal','TECHNO-REGEL')
add('GENRE-wet2-V3','Genre','Genre-wet 2 herzien: het lichaam is de prijs',WET2,'lost wrijving machines vs wet 2 op','GENRE-zegelpunk;TECHNO-REGEL')
for v,(t,x) in VOLK.items():
  add(f'TECHNO-VOLK-{v}','Techniek',f'Technologie van {v}',f'Beheerst: {t}. {x}.','technologie per volk',f'VOLK-{v};TECHNO-REGEL')
# los oude wrijving machines vs wet 2 op
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Opgelost V3: zie GENRE-wet2-V3]' where status='open' and (titel like '%machine%' or beschrijving like '%lichaam is de machine%')")
def wrij(t,d,b,ty):
  if c.execute("select 1 from wrijving where titel=?",(t,)).fetchone(): return
  m=max(int(r[0][5:]) for r in c.execute("select code from wrijving where code like 'WRIJ-%'"))
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,'open',?,?)",(t,d,b,ty,f'WRIJ-{m+1:03d}',d.replace('; ',';')))
def vraag(v,w,r):
  if c.execute("select 1 from open_vraag where vraag=?",(v,)).fetchone(): return
  m=max(int(x[0][6:]) for x in c.execute("select code from open_vraag where code like 'VRAAG-%'"))
  c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,f'VRAAG-{m+1:03d}',r))
for w in WRIJ: wrij(*w)
for v in VRAGEN: vraag(*v)
if not c.execute("select 1 from logboek where wat like 'Ronde V3:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",('Ronde V3: vier technologieën (TECHNO-gave/metaal/bio/zegelsteen) met toepassingen, 32 voorwerpen, haken, personages, ontstaansketens OORSPRONG-*-1..8, mix, per volk, tijdlijn, schaal, TECHNO-REGEL, genre-wet 2 herzien.',))
c.commit()
codes={r[0] for r in c.execute('select code from canon')}
mis=sorted({x for (v,) in c.execute("select verwijst_naar from canon where ronde=?",(RONDE,)) for x in (v or '').split(';') if x and x not in codes})
print(f'V3: nieuw {n}, canon {len(codes)}; ontbrekende verwijzingen: {mis}')
print(c.execute("select code,titel,status from wrijving where beschrijving like '%Opgelost V3%'").fetchall())
