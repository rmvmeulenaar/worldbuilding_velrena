# Ronde Z18b: 15 voorstellen definitief, vonkcel-besluit, toetsbesluit. Idempotent; data in z18b/
import sqlite3,shutil,os,sys,json,importlib
sys.path.insert(0,'z18b'); data=importlib.import_module('data'); sys.path.pop(0)
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
TAG='Z18b';D=data.D;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z18b.db'): shutil.copy('canon.db','canon_backup_Z18b.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'status_gewijzigd':[]}
RONDE=c.execute("select ronde from canon where code='BESLUIT-Z18-1'").fetchone()[0]
def put(code,ond,feit,ver,jaar,tp):
  feit+=LABEL
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,'vastgesteld',?,?,?,?,?,?,?,'META','geen')",(ond,feit,f'Ronde {TAG} {D}: gekozen door Rogier',ver,RONDE,code,ver,jaar,tp));S['toegevoegd']+=1
for n,o,f,j,v in data.B: put(f'BESLUIT-Z18b-{n}',o,f'Gekozen door Rogier ({D}): {f}',v,j,'0 Voortijd' if j<-600 else '801 (nu)')
for i in range(1,16):
  k=f'YSA-Z18-{i}'
  if c.execute("select 1 from canon where code=? and status='voorlopig'",(k,)).fetchone():
    c.execute("update canon set status='vastgesteld', feit=replace(feit,'voorstel, wacht op goedkeuring van Rogier','vastgesteld door Rogier'), reden=coalesce(reden,'')||? where code=?",(f' [Ronde {TAG}: {data.REDEN}]',k)); S['status_gewijzigd'].append(k)
for k,t in data.A.items():
  f=c.execute('select feit from canon where code=?',(k,)).fetchone()
  if f and '[Z18b]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z18b] {t}',f' [Ronde {TAG} {D}: aangevuld]',k)); S['aangevuld'].append(k)
c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||' [Z18b] Opgelost door BESLUIT-Z18b-1 (Rogier: ja, 2026-10-31).' where code='WRIJ-Z18-1' and status!='opgelost'")
c.execute("delete from logboek where wat like 'Ronde Z18b: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z18b: YSA-Z18-1..15 vastgesteld; BESLUIT-Z18b-1 (vonkcellen) en -2 (toetsbesluit); WRIJ-Z18-1 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z18b/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
