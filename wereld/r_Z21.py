# Ronde Z21: keuzes h19-24 vastgelegd (Rogier: leg alles vast). Idempotent; data in z21/
import sqlite3,shutil,os,sys,json,importlib
sys.path.insert(0,'z21'); data=importlib.import_module('data'); sys.path.pop(0)
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
TAG='Z21';D=data.D;R=data.REDEN;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z21.db'): shutil.copy('canon.db','canon_backup_Z21.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'status_gewijzigd':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z21-1'").fetchone() else RONDE+1
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,ver,jaar,functie):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd',?,'geen')",(cat,ond,feit+LABEL,f'Ronde {TAG} {D}: {R}',ver,RONDE,code,ver,jaar,functie));S['toegevoegd']+=1
for n,o,f,j,v in data.B: put(f'BESLUIT-Z21-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}',v,j,'META')
for n,o,f,j,b in data.Y: put(f'YSA-Z21-{n}',CAT,o,f'{f} Nieuw bedacht (roman {b}); vastgesteld door Rogier.','ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',j,'VERH')
def ap(code,txt,m='[Z21]'):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and m not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code)); S['aangevuld'].append(code)
for h,(t,i,w,fn) in data.H.items():
  k=f'ROMAN-Z16-h{h}'
  ap(k,f'{t.split(';')[0]} (0 Voortijd); intensiteit {i}; weet: {w}; functie: {fn}. {t}')
  c.execute("update canon set intensiteit=coalesce(intensiteit,?), weet=coalesce(weet,?) where code=?",(i,w,k))
for h,txt in data.N.items(): ap(f'ROMAN-Z16-h{h}','revisie-notitie: '+txt,'[Z21 revisie]')
put('MOTOREN-Z21',CAT,'Motorenkaart The Body Is the Price',data.MOT,'ROMAN-Z16-roman;BESLUIT-Z21-1',-1240,'META')
for i,(t,d,b,s,v) in enumerate(data.W,1):
  if not c.execute('select 1 from wrijving where code=?',(f'WRIJ-Z21-{i}',)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z21',s,f'WRIJ-Z21-{i}',v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z21: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z21: BESLUIT-Z21-1..5; YSA-Z21-1..19 vastgesteld; ROMAN-Z16-h25..h33 aangevuld, h16/17/22/26/27/28 revisie-notitie; MOTOREN-Z21; WRIJ-Z21-1..5.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z21/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))