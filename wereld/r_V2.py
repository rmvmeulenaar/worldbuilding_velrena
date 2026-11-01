# Ronde V2: volkgeschiedenis, intrige, magie- en techniekgeschiedenis (idempotent)
import sqlite3,shutil,os
RONDE=24;TAG='V2'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
if not os.path.exists('canon_backup_V2.db'): shutil.copy('canon.db','canon_backup_V2.db')
c=sqlite3.connect('canon.db');n=0
codes={r[0] for r in c.execute('select code from canon')}
def add(code,cat,ond,feit,reden,refs,**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  refs=';'.join(r for r in refs.split(';') if r)
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1
FASE={1:('1 Overvloed',-400),2:('2 Vonk',-100),3:('3 Brand',-20),4:('4 Noodtoestand',60),5:('5 Ontvangst',250),6:('6 Markt',500),7:('7 Barsten',801)}
STAP=['Oorsprong','Bloei','Ramp','Verraad of oorlog','Verhouding tot Zegel en Orde','Heden (801)']
exec(open('v2/data.py',encoding='utf-8').read())
# 1. volkgeschiedenis
for volk,(evs,held,schurk) in VOLKEN.items():
  for i,(fase,tekst,oorzaak,gevolg,refs) in enumerate(evs,1):
    t,j=FASE[fase]
    add(f'GESCH-{volk}-{i}','Geschiedenis',f'{STAP[i-1]} van de {volk} (fase {t})',
        f'{STAP[i-1]}. {tekst} Oorzaak: {oorzaak} Gevolg: {gevolg}'+GR,'volkgeschiedenis',
        f'VOLK-{volk};{f"GESCH-{volk}-{i-1}" if i>1 else ""};{refs}',jaar=j,tijdperk=t)
  for soort,(slug,naam,fase,tekst) in (('held',held),('schurk',schurk)):
    t,j=FASE[fase]
    add('PER-'+slug,'Personage',naam,f'Naam: {naam}. Volk: {volk}. Rol: {soort} van de volkgeschiedenis. Fase: {t}. {tekst}'+GR,
        f'{soort} volk {volk}',f'VOLK-{volk};GESCH-{volk}-1',jaar=j,tijdperk=t)
# 2. intrige
for slug,fase,titel,per,motief,wending,gevolg,refs in INTRIGE:
  t,j=FASE[fase]
  add(f'INTR-V2-{slug}','Verhaal',f'Intrige-affaire: {titel}',
      f'Intrige, fase {t}. Betrokken: {per}. Motief: {motief}. Wending: {wending}. Gevolg: {gevolg}.'+GR,
      f'intrige fase {fase}',refs+f';VERHAAL-fase{fase}',jaar=j,tijdperk=t,functie='INTR')
# 3/4. magie- en techniekgeschiedenis
for pre,lijst in (('MAGIE-GESCH',MAGIE),('TECH-GESCH',TECH)):
  for i,(fase,titel,tekst,refs) in enumerate(lijst,1):
    t,j=FASE[fase]
    add(f'{pre}-{i}','Magie' if pre[0]=='M' else 'Techniek',titel,tekst,pre.lower(),refs,jaar=j,tijdperk=t)
add('TECH-REGEL','Techniek','Techniekregel van Velmara (na V2)',TECHREGEL,'techniekregel, vervangt de strikte biopunkregel','GENRE-zegelpunk;TECH-GESCH-1;TECH-GESCH-12;MAGIE-GESCH-1')
add('HAAK-genre-balans-V2','Verhaal','Genre-balans van de canon (na V2)',BALANS+GR,'genre-balans na V2','HAAK-genre-balans-V1;GENRE-zegelpunk')
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
if not c.execute("select 1 from logboek where wat like 'Ronde V2:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",('Ronde V2: geschiedenis per volk (14 x 6 GESCH-rijen, held en schurk per volk), 60 nieuwe intriges (INTR-V2-), MAGIE-GESCH-1..12, TECH-GESCH-1..12 en TECH-REGEL (verborgen sf toegestaan: machinale resten van buiten Velmara; oorsprong Zegel/Vonk blijft open); genre-balans herzien.',))
c.commit()
codes={r[0] for r in c.execute('select code from canon')}
mis=sorted({x for (v,) in c.execute("select verwijst_naar from canon where ronde=?",(RONDE,)) for x in (v or '').split(';') if x and x not in codes})
print(f'V2: nieuw {n}, canon {len(codes)}; ontbrekende verwijzingen: {mis}')
