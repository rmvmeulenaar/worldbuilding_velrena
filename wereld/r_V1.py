# Ronde V1: mega-verhaal per fase, 140 nieuwe personages, ROM/INTR/THRL per fase, eigen gevoel per personage (idempotent)
import sqlite3,shutil,os,re,hashlib
RONDE=23;TAG='V1'
GR=" Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema's gelabeld."
SF=" SF-neutraal: geldig onder 'verborgen sf', 'open sf' en 'pure fantasy'; niets vastgelegd over sterren of technologie als oorsprong."
if not os.path.exists('canon_backup_V1.db'): shutil.copy('canon.db','canon_backup_V1.db')
c=sqlite3.connect('canon.db');n=0
def add(code,cat,ond,feit,reden,refs,**kw):
  global n
  if c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
  cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
  c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {TAG}: '+reden,refs,RONDE,code,refs]+list(kw.values()));n+=1
FASEN={1:('overvloed','1 Overvloed',-600,-150),2:('vonk','2 Vonk',-150,-40),3:('brand','3 Brand',-40,0),4:('noodtoestand','4 Noodtoestand',0,130),5:('ontvangst','5 Ontvangst',130,340),6:('markt','6 Markt',340,720),7:('barsten','7 Barsten',720,801)}
FN={v[0]:(k,v[1],v[2],v[3]) for k,v in FASEN.items()}
# 1. mega-verhalen
for i in range(1,8):
  L=open(f'v1/mega{i}.txt',encoding='utf-8').read().strip().split('\n')
  code,titel,refs=L[0].split('|');tekst=' '.join(L[1:])
  add(code,'Verhaal',titel,tekst+GR+SF,f'mega-verhaal fase {i}',refs,tijdperk=FASEN[i][1],jaar=FASEN[i][2],functie='VERHAAL')
L=open('v1/deel.txt',encoding='utf-8').read().strip().split('\n')
for j in range(0,len(L),2):
  code,titel,refs=L[j].split('|');i=int(code[12])
  add(code,'Verhaal',titel,L[j+1]+GR,f'deelverhaal fase {i}',refs+f';VERHAAL-fase{i}',tijdperk=FASEN[i][1],jaar=FASEN[i][2],functie='VERHAAL')
# 2. personages
for i in range(1,8):
  for ln in open(f'v1/per{i}.txt',encoding='utf-8'):
    f=ln.rstrip('\n').split('|')
    if len(f)!=20: raise SystemExit('veldfout: '+ln)
    slug,naam,volk,reg,huis,rol,fase,geb_j,wil,durf,verb,weet,voor,kink,lich,rel,geb,geh,einde,gev=f
    k,fnaam,a,b=FN[fase];gj=int(geb_j);jaar=max(a,min(b,gj+30))
    vs=[x.split(':') for x in voor.split(',') if ':' in x]
    vtxt=', '.join(f'{x} ({y}/5)' for x,y in vs) or 'geen seksuele rol'
    vc='' if volk=='mens' else 'VOLK-'+volk
    hc=huis if huis.startswith('HUI-') else ''
    refs=[r for r in [vc,'REG-'+reg,hc,geb,'FASE-'+fase,f'VERHAAL-fase{k}']+[x for x,_ in vs] if r]
    haken=(f"Romance: {rel}; belemmering: {verb}. Intrige: wil {wil}, maar verbergt {verb}. "
           f"Erotiek: {kink if kink!='-' else 'geen erotische rol'}. Thriller: geheim \"{geh}\" kan uitkomen; einde: {einde}.")
    feit=(f"Naam: {naam}. Volk: {volk}. Regio: {reg}. Huis: {huis}. Rol: {rol}. Fase: {fnaam}, jaar {jaar} (geboren ca. {gj}). "
          f"Wil: {wil}. Durft: {durf}. Verbergt: {verb}. Wat de omgeving weet: {weet}. Seksuele voorkeur: {vtxt}; kinks: {kink}. "
          f"Lichaam/vervorming: {lich}. Relaties: {rel}. Rol in de keten: {geb}. Geheim: {geh}. Einde: {einde}. "
          f"Verhaalhaken: {haken} Eigen gevoel: {gev}.")
    add('PER-'+slug,'Personage',naam,feit+GR,f'personage fase {fnaam} (mega-verhaal)',';'.join(dict.fromkeys(refs)),
        jaar=jaar,tijdperk=fnaam,intensiteit=max([int(y) for _,y in vs] or [0]))
# 3. romances, intriges, thrillerlijnen
SP={'ROM':'Romance (met belemmering)','INTR':'Intrige-affaire','THRL':'Thrillerlijn'}
import glob
for fn in sorted(glob.glob('v1/lijn*.txt')):
  for ln in open(fn,encoding='utf-8'):
    if not ln.strip(): continue
    t,i,slug,titel,tekst,refs=ln.rstrip('\n').split('|');i=int(i)
    add(f'{t}-fase{i}-{slug}','Verhaal',f'{SP[t]}: {titel}',f'{SP[t]}, fase {FASEN[i][1]}. {tekst} Zie VERHAAL-fase{i}.'+GR,
        f'{SP[t].lower()} fase {i}',refs+f';FASE-{FASEN[i][0]};VERHAAL-fase{i}',tijdperk=FASEN[i][1],jaar=FASEN[i][2],functie=t)
# 2b. vaste zin 'Herkenbaar gevoel' vervangen door een eigen gevoel per personage
def veld(feit,naam):
  m=re.search(naam+r': (.*?)\. [A-Z][a-z /]+: ',feit);return m.group(1) if m else ''
T=["angst dat in de eigen kring ({r}) uitkomt wat verborgen blijft: {v}",
   "verlangen, al jaren: {w}; en de vermoeidheid van het steeds weer moeten wachten",
   "eenzaamheid: voor de buitenwereld \u2018{o}\u2019, van binnen het geheim: {v}",
   "trots op wat durf vraagt ({d}), en het stille twijfelen of het de prijs waard was",
   "schaamte over wat verborgen blijft ({v}), en opluchting zodra iemand het toch ziet",
   "heimwee naar wie dit personage was voordat het dit ging willen: {w}",
   "jaloezie op wie zonder moeite krijgt waar dit personage voor vecht: {w}",
   "de spanning van een dubbel leven: gezien als \u2018{o}\u2019, maar met een geheim: {v}",
   "liefde en plicht in de eigen banden ({r}), die steeds botsen met wat dit personage wil: {w}",
   "schuld na wat het durfde ({d}), en de nachten waarin dat terugkomt"]
rep=0
for rid,feit in c.execute("select id,feit from canon where (feit like '%Herkenbaar gevoel: verlangen en schaamte%' or (feit like '%Eigen gevoel:%' and ronde<?))",(RONDE,)).fetchall():
  v=veld(feit,'Verbergt') or 'een geheim';w=veld(feit,'Wil') or 'iets eigens';d=veld(feit,'Durft') or 'iets durft';o=veld(feit,'Wat de omgeving weet') or 'alles gewoon is';r=(veld(feit,'Relaties') or 'de naasten').split(';')[0]
  h=int(hashlib.md5(str(rid).encode()).hexdigest(),16)%len(T)
  g=T[h].format(v=v.rstrip('.'),w=w,d=d,o=o,r=r)
  nieuw=re.sub(r'(Herkenbaar gevoel: verlangen en schaamte\s*rond wat ze verbergt|Eigen gevoel: .*?)\.(?= Label:)','Eigen gevoel: '+g.replace('\\','')+'.',feit,count=1)
  if nieuw!=feit:
    c.execute("update canon set feit=? where id=?",(nieuw,rid));rep+=1
    c.execute("update canon set reden=reden||' | Ronde V1: eigen gevoel i.p.v. vaste zin' where id=? and reden not like '%Ronde V1: eigen gevoel%'",(rid,))
# 4. genre-balans, wrijvingen, vragen, logboek
add('HAAK-genre-balans-V1','Verhaal','Genre-balans van de canon (na V1)',
"Romance: nu in alle zeven fasen minstens zes lijnen met belemmering (ROM-fase1..7), plus een centrale liefde per mega-verhaal; sterkst Ysara-Mira (fase 3), Liane-Daeran (fase 5), Annike-Joost (fase 7); nog dun in Kharvos en in de top van de huizen in 801. "
"Intrige: per fase zes affaires (INTR-), met een doorlopende draad van het register als wapen (Oda, Saske, Corvina, Ilse Varenne, het vervalsersgilde, Veere); nog dun in de Rosse en bij de Aelthir. "
"Thriller: de historische fasen 1-4 hebben nu klokken en achtervolgingen (THRL-), dus geen pure kroniek meer; sterkste klokken: de Oogstnacht (1), negen dagen Grijswortel (3), de Lampentoren (7). "
"Erotiek: de mega-verhalen voegen vooral gewone, herkenbare erotiek toe (graanzolder, veerpont, werkplaats, rustmaand), wat de eerder te zware extreme kant in balans brengt. Extreem blijft gedoseerd. "
"Escapisme: elke fase heeft nu een openings- en slotbeeld voor schrijvers. Open: volken als hoofdpersoon in een mega-verhaal (nu meest mensen)."+GR,
'genre-balans na V1','HAAK-genre-balans;VERHAAL-fase1;VERHAAL-fase3;VERHAAL-fase5;VERHAAL-fase7')
def wrij(t,d,b,ty):
  if c.execute("select 1 from wrijving where titel=?",(t,)).fetchone(): return
  m=max(int(r[0][5:]) for r in c.execute("select code from wrijving where code like 'WRIJ-%'"))
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,'open',?,?)",(t,d,b,ty,f'WRIJ-{m+1:03d}',d.replace('; ',';')))
def vraag(v,w,r):
  if c.execute("select 1 from open_vraag where vraag=?",(v,)).fetchone(): return
  m=max(int(x[0][6:]) for x in c.execute("select code from open_vraag where code like 'VRAAG-%'"))
  c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,f'VRAAG-{m+1:03d}',r))
wrij('Moeder Iresse in 128 en in 300','GEB-r10-dankpreek; GEB-r10-iresse-verraad; PER-f5-iresse-tweede','De keten noemt Moeder Iresse in 128 (preek) en in 300 (lek). V1 lost het voorlopig op met een tweede Moeder die haar naam droeg; kan ook een fout in de keten zijn.','mogelijke fout')
wrij('Annike is Marit Schrijfster','PER-f7-annike; PER-gew-marit; VERHAAL-fase7','V1 maakt de vervalster van Liora\'s blad en de marktschrijfster van 801 tot dezelfde vrouw (81 jaar in 801). Klopt met Marits geheim, maar haar leeftijd stond niet vast.','bron van verhalen')
wrij('De koningszoon uit de graanzolder als stamvader van de Vonk','VERHAAL-fase1; GEB-r10-mijnzonen; GEB-orric-vonk','V1 laat de verzwegen koningszoon van Ardemar III de voorvader van de mijnzonen worden: koningsbloed in de eerste vonk. Botst niet, maar maakt de Vonk deels erfelijk vóór de Zegel.','bron van verhalen')
wrij('Tarn als stamvader van Kaldra','PER-f2-tarn; HUI-kaldra','V1 noemt Tarns nakomelingen de Kaldra; de oorsprong van Huis Kaldra was nog niet vastgelegd.','bron van verhalen')
wrij('Saske als eerste vervalser','PER-f4-saske; GEB-r10-bloedmerk; GEB-r10-vervalser-gilde','Het bloedmerk heet onvervalsbaar, maar Saske vervalst haar eigen blad: alleen wie het merk kan lezen, kan het vervalsen. Sluit aan bij de aanbeveling "magisch merk, alleen te verbergen".','bron van verhalen')
wrij('Ylva ziet Halvar in jaar 45, Deelwet in 40','VERHAAL-fase4; GEB-deelwet-40; GEB-r10-deelwet-weerstand','Volgorde in VERHAAL-fase4 controleren: weerstand 41-60 valt na de Deelwet; klopt, maar de Deelwet moet vóór de chantage liggen.','mogelijke fout')
vraag('Welk mega-verhaal wordt het eerste prequel-boek?','Bepaalt waar de schrijver na de hoofdquest heen gaat.','VERHAAL-fase1;VERHAAL-fase3;VERHAAL-fase5;VERHAAL-fase7')
vraag('Wordt fantasy gecombineerd met science fiction (verborgen sf, open sf of pure fantasy)?','V1 legt bewust niets vast; de keuze raakt de oorsprong van de Sterrensteen, de Zegel en de Leegte.','GEB-sterrensteen-val;GEB-zegel-gelegd')
vraag('Moeten niet-menselijke volken een eigen mega-verhaal per fase krijgen?','V1 heeft per fase mensen als hoofdpersoon; volken zijn bijfiguren.','HAAK-genre-balans-V1')
if not c.execute("select 1 from logboek where wat like 'Ronde V1:%'").fetchone():
  c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",('Ronde V1: zeven mega-verhalen (VERHAAL-fase1..7) en 21 deelverhalen; 140 nieuwe personages (20 per fase); per fase 6 ROM, 6 INTR, 6 THRL; vaste zin "Herkenbaar gevoel" vervangen door een eigen gevoel per personage; genre-balans herzien; sf-richting bewust open gelaten.',))
c.commit()
codes={r[0] for r in c.execute('select code from canon')}
mis=sorted({x for (v,) in c.execute("select verwijst_naar from canon where ronde=?",(RONDE,)) for x in (v or '').split(';') if x and x not in codes})
print(f'V1: nieuw {n}, gevoel vervangen {rep}, canon {len(codes)}; ontbrekende verwijzingen: {mis}')
