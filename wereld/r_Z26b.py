# Ronde Z26b: 'the ones' i.p.v. 'five' (Rogier: leg alles vast). Idempotent, niets verwijderen.
import sqlite3,shutil,os,json
D='2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z26b.db'): shutil.copy('canon.db','canon_backup_Z26b.db')
c=sqlite3.connect(DB);S={'aangevuld':[]}
T='Tekst h16 nu: "Including the ones who had not been on the third ring at all. It had counted them too, before any of them had died." Alle doden buiten ring drie (ring twee bij de junction, de drie van E-7, de twee bij C-4: samen meer dan vijf) zijn vooraf door de Reckoner meegeteld in 3.454; de tekst noemt geen aantal.'
for code in ('BESLUIT-Z26-2','ROMAN-Z16-h16'):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()[0]
  if '[Z26b]' not in f:
    c.execute("update canon set feit=feit||?, reden=coalesce(reden,'')||? where code=?",(' [Z26b] '+T,f' [Ronde Z26b {D}: aangevuld]',code));S['aangevuld'].append(code)
b=c.execute("select beschrijving from wrijving where code='WRIJ-Z26-1'").fetchone()[0]
if '[Z26b]' not in b: c.execute("update wrijving set status='opgelost', beschrijving=beschrijving||? where code='WRIJ-Z26-1'",(' [Z26b] '+T,));S['aangevuld'].append('WRIJ-Z26-1')
if not c.execute("select 1 from logboek where wat like 'Ronde Z26b:%'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,"Ronde Z26b: h16 'the ones' i.p.v. 'five'; [Z26b] bij BESLUIT-Z26-2, ROMAN-Z16-h16, WRIJ-Z26-1 (opgelost)."))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
os.makedirs('z26',exist_ok=True);json.dump(S,open('z26/stats_b.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
