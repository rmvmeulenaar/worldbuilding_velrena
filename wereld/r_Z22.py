# Ronde Z22: motorregel en zaaibeats vastgelegd (Rogier: leg alles vast). Idempotent; data in z22/
import sqlite3,shutil,os,sys,json,importlib
sys.path.insert(0,'z22'); data=importlib.import_module('data'); sys.path.pop(0)
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
TAG='Z22';D=data.D;R=data.REDEN;DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z22.db'): shutil.copy('canon.db','canon_backup_Z22.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[],'status_gewijzigd':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z22-1'").fetchone() else RONDE+1
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,ver,jaar,functie):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd',?,'geen')",(cat,ond,feit+LABEL,f'Ronde {TAG} {D}: {R}',ver,RONDE,code,ver,jaar,functie));S['toegevoegd']+=1
for n,o,f,j,v in data.B: put(f'BESLUIT-Z22-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}',v,j,'META')
for n,o,f,j,b,v in data.Y: put(f'YSA-Z22-{n}',CAT,o,f'{f} Nieuw bedacht (roman {b}, motorenronde); vastgesteld door Rogier.',v,j,'VERH')
def ap(code,txt,m='[Z22]'):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and m not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code)); S['aangevuld'].append(code)
for h,txt in data.H.items(): ap(f'ROMAN-Z16-h{h}','motorenronde: '+txt)
put('MOTOREN-Z22',CAT,'Motorenkaart Z22: overgangen (motor afloop -> volgende gezaaid)',data.MOT,'ROMAN-Z16-roman;MOTOREN-Z21;BESLUIT-Z22-1',-1240,'META')
for i,(t,d,b,s,v) in enumerate(data.W,1):
  if not c.execute('select 1 from wrijving where code=?',(f'WRIJ-Z22-{i}',)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z22',s,f'WRIJ-Z22-{i}',v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z22: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z22: BESLUIT-Z22-1 (motorregel); YSA-Z22-1..7 vastgesteld; MOTOREN-Z22; [Z22] bij h21/h22/h27/h30/h31; WRIJ-Z22-1..3.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z22/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
def ext(code,txt,m='[Z22 verruimd]'):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and m not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: verruimd]',code)); S['aangevuld'].append(code)
ext('BESLUIT-Z22-1',data.B_EXTRA); ext('MOTOREN-Z22',data.MOT_EXTRA,'[Z22 voeding]')
c.commit();print('verruimd:',S['aangevuld'])
