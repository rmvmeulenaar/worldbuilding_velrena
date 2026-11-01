import sqlite3,subprocess,os,re
subprocess.run(['python3','genereer.py'],check=True)
if os.path.exists('/tmp/rt13.db'): os.remove('/tmp/rt13.db')
print(subprocess.run(['python3','importeer.py','WERELD_VELMARA.md','/tmp/rt13.db'],check=True,capture_output=True,text=True).stdout)
a=sqlite3.connect('canon.db');b=sqlite3.connect('/tmp/rt13.db')
TAB={'canon':'code,categorie,onderwerp,feit,reden,status,ronde,hangt_samen_met,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,afstoting,aantrekking_bron,aantrekking,techniek','wrijving':'code,titel,delen_die_botsen,beschrijving,type,status,verwijst_naar','open_vraag':'code,vraag,waarom_belangrijk,status,antwoord,verwijst_naar','logboek':'id,datum,wat'}
tot=0
for t,cols in TAB.items():
  x=set(a.execute(f'select {cols} from {t}'));y=set(b.execute(f'select {cols} from {t}'));d=len(x^y);tot+=d
  print(f'roundtrip {t}: {len(x)} vs {len(y)}, verschillen {d}')
print('roundtrip totaal verschillen:',tot)
W=open('WERELD_VELMARA.md').read()
cs=[r[0] for r in a.execute("select code from canon where ronde=42 or reden like '%Z13%'")]
print('grep Z13-codes in WERELD_VELMARA.md:',sum(x in W for x in cs),'/',len(cs))
K=open('bijbel/27_kwaliteit.md').read();print('27_kwaliteit.md:',len(K),'tekens; inhoudsopgave:', '27_kwaliteit' in open('bijbel/00_inhoud.md').read() if os.path.exists('bijbel/00_inhoud.md') else [f for f in os.listdir('bijbel') if f.startswith('00')])
# grep-controle harde regels in Z13-wijzigingen
bad=[]
for code,f in a.execute("select code,feit from canon where feit like '%[Z13%' or ronde=42"):
  z=f[f.find('[Z13'):] if '[Z13' in f else f
  if re.search(r'\b(kind|kinderen|minderjarig|meisje|jongetje|dier|vee|beest)\w*',z,re.I) and re.search(r'seks|erot|kink|lust',z,re.I): bad.append(code)
print('grep harde regels (Z13-tekst met minderjarige/dier + seksueel):',len(bad),bad[:10])
print('integrity_check:',a.execute('pragma integrity_check').fetchone()[0])
