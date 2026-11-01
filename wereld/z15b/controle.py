import sqlite3,subprocess,os,re
subprocess.run(['python3','genereer.py'],check=True)
if os.path.exists('/tmp/rt15b.db'): os.remove('/tmp/rt15b.db')
print(subprocess.run(['python3','importeer.py','WERELD_VELMARA.md','/tmp/rt15b.db'],check=True,capture_output=True,text=True).stdout)
a=sqlite3.connect('canon.db');b=sqlite3.connect('/tmp/rt15b.db')
TAB={'canon':'code,categorie,onderwerp,feit,reden,status,ronde,hangt_samen_met,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,afstoting,aantrekking_bron,aantrekking,techniek','wrijving':'code,titel,delen_die_botsen,beschrijving,type,status,verwijst_naar','open_vraag':'code,vraag,waarom_belangrijk,status,antwoord,verwijst_naar','logboek':'id,datum,wat'}
tot=0
for t,cols in TAB.items():
  x=set(a.execute(f'select {cols} from {t}'));y=set(b.execute(f'select {cols} from {t}'));d=len(x^y);tot+=d
  print(f'roundtrip {t}: {len(x)} vs {len(y)}, verschillen {d}')
print('roundtrip totaal verschillen:',tot)
W=open('WERELD_VELMARA.md').read()
cs=[r[0] for r in a.execute("select code from canon where ronde=45 or reden like '%Ronde Z15b%'")]
print('grep Z14-codes in WERELD_VELMARA.md:',sum(x in W for x in cs),'/',len(cs))
K=open('bijbel/29_ysa-thalen.md').read();print('27_kwaliteit.md:',len(K),'tekens; inhoudsopgave:', '28_restpunten' in open('bijbel/00_inhoud.md').read() if os.path.exists('bijbel/00_inhoud.md') else [f for f in os.listdir('bijbel') if f.startswith('00')])
# grep-controle harde regels in Z13-wijzigingen
bad=[]
for code,f in a.execute("select code,feit from canon where feit like '%[Z15b]%' or ronde=45"):
  z=f[f.find('[Z15b]'):] if '[Z15b]' in f else f
  if re.search(r'\b(kind|kinderen|minderjarig|meisje|jongetje|dier|vee|beest)\w*',z,re.I) and re.search(r'seks|erot|kink|lust',z,re.I): bad.append(code)
print('grep harde regels (Z14-tekst met minderjarige/dier + seksueel):',len(bad),bad[:10])
print('integrity_check:',a.execute('pragma integrity_check').fetchone()[0])
import shutil; shutil.copy('canon.db','verhalen/canon_lees.db'); print('canon_lees.db bijgewerkt:', sqlite3.connect('verhalen/canon_lees.db').execute('select count(*) from canon').fetchone()[0],'rijen')
import hashlib
for f in ('verhaal_01_brakhaven.md','verhaal_02_komedie.md','beatplan_02_komedie.md'): print(f, os.path.getmtime('verhalen/'+f))
# extra controles Z15b
codes=set(r[0] for r in a.execute('select code from canon'))
kap=[]
for code,h,v in a.execute("select code,hangt_samen_met,verwijst_naar from canon where ronde=45 or reden like '%Z15b%'"):
  for x in re.split(r'[;,]\s*',(h or '')+';'+(v or '')):
    x=x.strip()
    if x and not x.startswith('WRIJ') and x not in codes: kap.append((code,x))
print('kapotte verwijzingen Z15b:',kap)
print('duplicaten code:',a.execute('select code,count(*) from canon group by code having count(*)>1').fetchall())
print('wrijving dubbel:',a.execute('select code,count(*) from wrijving group by code having count(*)>1').fetchall())
print('WRIJ-Z15-6/7:',a.execute("select code,status from wrijving where code in ('WRIJ-Z15-6','WRIJ-Z15-7')").fetchall())
print('jaren beats:',a.execute("select code,jaar,tijdperk from canon where code like 'ROMANCE-Z15b-ysa-beat-%' and jaar not in (-1240,-1238,-1237,-1200,801)").fetchall())
print('levende rijen met oude beatcodes:',a.execute("select code from canon where status!='voorlopig, vervangen' and (hangt_samen_met like '%ROMANCE-Z15-ysa%' or verwijst_naar like '%ROMANCE-Z15-ysa%' or hangt_samen_met like '%YSA-Z15-6;%')").fetchall())
print('levende rijen waar Corran kantelt / stemming voor Muiterij:',a.execute("select code,status from canon where status!='voorlopig, vervangen' and (feit like '%Corran kantelt%' or feit like '%levert Corrans stem%' or feit like '%ruilt Corrans stem%' or feit like '%Corrans stem voor%')").fetchall())
print('stemming-jaar ORIGIN-4/WAAROM-7, Muiterij ORIGIN-3:',a.execute("select code,jaar from canon where code in ('ORIGIN-3','ORIGIN-4','ORIGIN-WAAROM-7','BESLUIT-Z15b-1')").fetchall())
