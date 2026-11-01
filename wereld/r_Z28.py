# Ronde Z28: alle details van "The Body Is the Price" (Rogier: leg alles vast). Idempotent, niets verwijderen.
import sqlite3,shutil,os,json
from z28_data import D as DATA
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
DT='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z28.db'): shutil.copy('canon.db','canon_backup_Z28.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'wrijving':0}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='YSA-Z28-1'").fetchone() else RONDE+1
for i,(h,o,f,j) in enumerate(DATA,1):
  code=f'YSA-Z28-{i}'
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): continue
  ver=f'ROMAN-Z16-{h};ROMAN-Z16-roman'
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Verhaal',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','VERH','geen')",(f'[{h}] '+o,f'Uit de roman ({h}), vastgelegd {DT}: '+f+LABEL,R,'ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',RONDE,code,ver,j));S['toegevoegd']+=1
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z28]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z28] {txt}',f' [Ronde Z28 {DT}: aangevuld]',code));S['aangevuld'].append(code)
ap('YSA-Z16-13','Tekst is leidend: het protocol halveert de kolonie "in forty years, give or take" (h1, h5, h15, h16). De 31 jaar is Ysa\'s levensduur na de landing (h32), niet de protocoltermijn (WRIJ-Z28-1).')
ap('YSA-Z19-13','Achterhaald door BESLUIT-Z24-2/-8: elke lander maakt na de eerste afdaling nog twee afdalingen; lander zes ging op dag 2 met 406 (WRIJ-Z28-2).')
ap('YSA-Z18-11','Tekst h11: om 09:40 checkt Thalen lander één; 09:41 als rood-licht-tijd komt alleen uit de novelle, niet in de roman (WRIJ-Z28-3).')
ap('PER-v4-thalen-orr','Roman-details: vlieginstructeur Edo Raske (31) stierf acht jaar voor de landing; wit litteken over één knokkel; handen verbrand op C-4; 72 in jaar 40, sterft op de 209e dag van zijn 75e levensjaar (YSA-Z28-12, -38, -44, -45).')
ap('PER-v4-ysa-maren','Roman-details: geboren in de telringen ("head", "there, counted"); hoofd biologie; snijdt haar eigen haar (scheve scheiding); draagt het oortje van lander één aan een koord (YSA-Z28-14, -37).')
W=[('WRIJ-Z28-1','Protocoltermijn: 31 jaar (YSA-Z16-13) vs "forty years" (roman)','YSA-Z16-13 (novelle) tegen h1/h5/h15/h16','Aanbeveling: tekst leidend, 40 jaar; canon aangevuld. Tekst niet gewijzigd.','opgelost','YSA-Z16-13'),
('WRIJ-Z28-2','Eén afdaling per lander (YSA-Z19-13) vs twee extra afdalingen','YSA-Z19-13 tegen h16/h19 en BESLUIT-Z24','Aanbeveling: Z24 en de tekst gelden; YSA-Z19-13 aangevuld als achterhaald. Tekst niet gewijzigd.','opgelost','YSA-Z19-13;BESLUIT-Z24-2'),
('WRIJ-Z28-3','Rood licht 09:41 (novelle) staat niet in de roman','YSA-Z18-11 tegen h11','Aanbeveling: geen botsing, alleen preciseren; laat 09:41 als novelle-detail staan. Tekst niet gewijzigd.','opgelost','YSA-Z18-11'),
('WRIJ-Z28-4','Dieren op het schip/kamp (geit, hond) waren niet in de canon','h25 (hond), h29/h30 (geiten), h23 (vis)','Aanbeveling: vastgelegd als meegebrachte dieren uit de zaadvoorraad/veestapel (alleen achtergrond, nooit in seksuele rol). Controleer bij de hoofdserie of er al ander vee bestaat. Tekst niet gewijzigd.','open (klein)','YSA-Z28-37;YSA-Z28-41;YSA-Z28-42'),
('WRIJ-Z28-5','"Three hundred kilometres" (h25) vs KAART-afstanden Saelith-Brakhaven 300 km','h25 tegen KAART-afstanden','Geen botsing: in h25 is het de baanhoogte boven de hut, geen kaartafstand. Alleen genoteerd.','opgelost','KAART-afstanden;YSA-Z28-37')]
for code,t,d,b,st,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z28',st,code,v));S['wrijving']+=1
if not c.execute("select 1 from logboek where wat like 'Ronde Z28: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(DT,f'Ronde Z28: volledige detailcontrole roman (h1-h33): YSA-Z28-1..{len(DATA)} vastgesteld; [Z28] bij YSA-Z16-13, YSA-Z19-13, YSA-Z18-11, PER-v4-thalen-orr, PER-v4-ysa-maren; WRIJ-Z28-1..5; register verhalen/roman_ysa_register.md.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
os.makedirs('z28',exist_ok=True);json.dump(S,open('z28/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
