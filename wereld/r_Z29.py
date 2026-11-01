# Ronde Z29: alle details van "The Body Is the Price" (Rogier: leg alles vast). Idempotent, niets verwijderen.
import sqlite3,shutil,os,json
from z29_data import D as DATA
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
DT='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z29.db'): shutil.copy('canon.db','canon_backup_Z29.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'wrijving':0}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='YSA-Z29-1'").fetchone() else RONDE+1
for i,(h,o,f,j) in enumerate(DATA,1):
  code=f'YSA-Z29-{i}'
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): continue
  ver=f'ROMAN-Z16-{h};ROMAN-Z16-roman'
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Verhaal',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','VERH','geen')",(f'[{h}] '+o,f'Uit de roman ({h}), vastgelegd {DT}: '+f+LABEL,R,'ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',RONDE,code,ver,j));S['toegevoegd']+=1
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z29]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z29] {txt}',f' [Ronde Z29 {DT}: aangevuld]',code));S['aangevuld'].append(code)
ap('YSA-Z20-17','Tekst h27: Ysa noemt "C-4-R" en "three times", maar alleen Thalen leerde dat (h24, van de Reckoner); zie WRIJ-Z29-1.')
ap('ROMAN-Z16-roman','Ronde Z29: hoofdstuk voor hoofdstuk volledig gelezen; sfeerdetails, gebaren, liederen, rituelen, motieven en ironie per hoofdstuk vastgelegd als YSA-Z29-* (register verhalen/roman_ysa_register.md).')
W=[('WRIJ-Z29-1','Ysa weet van C-4-R en "three times" (h27) zonder bron','h27 tegen h8/h24 (alleen Thalen hoorde het van de Reckoner)','Aanbeveling: wijzig in h27 "The crawl. C-4-R. You went down it three times. Before I ever gave an order." in iets als "The crawl behind the third press. You\'d been down it before I ever gave an order." (Ysa kent de route uit h8). Of laat staan als bewuste gok. Tekst niet gewijzigd.','open','YSA-Z20-17;BESLUIT-Z24-1'),
('WRIJ-Z29-2','"Seven thousand voices" na het vertrek van 211 (h31)','h31 tegen h30','Geen echte botsing: afgerond getal (ca. 6.800). Alleen genoteerd; tekst niet gewijzigd.','opgelost','ROMAN-Z16-h31;ROMAN-Z16-h30'),
('WRIJ-Z29-3','Labkoffie (h32) naast de thee-running-gag (h1, h2, h10)','h32 tegen h1/h2/h10','Geen botsing: in het lab dronken ze koffie, in de Warm Ring thee. Alleen genoteerd.','opgelost','ROMAN-Z16-h32')]
for code,t,d,b,st,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z29',st,code,v));S['wrijving']+=1
if not c.execute("select 1 from logboek where wat like 'Ronde Z29: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(DT,f'Ronde Z29: sfeerdetails roman (h1-h33 volledig gelezen): YSA-Z29-1..{len(DATA)} vastgesteld; [Z29] bij YSA-Z20-17, ROMAN-Z16-roman; WRIJ-Z29-1..3; register bijgewerkt.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
os.makedirs('z29',exist_ok=True);json.dump(S,open('z29/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
