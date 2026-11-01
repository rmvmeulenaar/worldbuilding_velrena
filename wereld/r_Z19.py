# Ronde Z19: keuzes h13-18 vastgelegd (Rogier: leg alles vast). Idempotent; data in z19/
import sqlite3,shutil,os,sys,json,importlib
sys.path.insert(0,'z19'); data=importlib.import_module('data'); sys.path.pop(0)
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
TAG='Z19';D=data.D;R=data.REDEN;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z19.db'): shutil.copy('canon.db','canon_backup_Z19.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'status_gewijzigd':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z19-1'").fetchone() else RONDE+1
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,ver,jaar,functie):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd',?,'geen')",(cat,ond,feit+LABEL,f'Ronde {TAG} {D}: {R}',ver,RONDE,code,ver,jaar,functie));S['toegevoegd']+=1
for n,o,f,j,v in data.B: put(f'BESLUIT-Z19-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}',v,j,'META')
for n,o,f,j,b in data.Y: put(f'YSA-Z19-{n}',CAT,o,f'{f} Nieuw bedacht (roman {b}); vastgesteld door Rogier.','ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',j,'VERH')
for k in ('ORIGIN-6','ORIGIN-WAAROM-4'):
  if c.execute("select 1 from canon where code=? and status='voorlopig'",(k,)).fetchone():
    c.execute("update canon set status='vastgesteld', reden=coalesce(reden,'')||? where code=?",(f' [Ronde {TAG}: vastgesteld incl. [Z18b]-aanvulling; {R}]',k)); S['status_gewijzigd'].append(k)
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z19]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z19] {txt}',f' [Ronde {TAG} {D}: aangevuld]',code)); S['aangevuld'].append(code)
for h,(t,i,w,fn) in data.H.items():
  k=f'ROMAN-Z16-h{h}'
  ap(k,f'Jaar -1240 (0 Voortijd); intensiteit {i}; weet: {w}; functie: {fn}. {t} {data.NAMEN}')
  c.execute("update canon set intensiteit=coalesce(intensiteit,?), weet=coalesce(weet,?) where code=?",(i,w,k))
for i,(t,d,b,s,v) in enumerate(data.W,1):
  if not c.execute('select 1 from wrijving where code=?',(f'WRIJ-Z19-{i}',)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z19',s,f'WRIJ-Z19-{i}',v))
c.execute("delete from logboek where wat like 'Ronde Z19: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z19: ORIGIN-6/-WAAROM-4 vastgesteld; BESLUIT-Z19-1..5; YSA-Z19-1..15 vastgesteld; ROMAN-Z16-h13..h18 aangevuld; WRIJ-Z19-1..2.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z19/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
