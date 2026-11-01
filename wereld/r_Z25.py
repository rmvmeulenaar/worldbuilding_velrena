# Ronde Z25: laatste feedback (Rogier: leg alles vast). Idempotent.
import sqlite3,shutil,os,json
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
D='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z25.db'): shutil.copy('canon.db','canon_backup_Z25.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z25-1'").fetchone() else RONDE+1
def put(code,ond,feit,ver,jaar):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','META','geen')",(ond,f'Vastgelegd door Rogier ({D}): '+feit+LABEL,R,ver,RONDE,code,ver,jaar));S['toegevoegd']+=1
B=[('Oortje stil: twee jaar','In h26 heeft het oortje "not made a sound in two years" (niet anderhalf jaar): de stemming valt aan het eind van jaar twee, en h29 zegt "for two years".','ROMAN-Z16-h26;ROMAN-Z16-h29',-1238),
('Lander één omgebouwd met stoelrekken','Op de landingsdag (eerste golf, vracht) zaten in lander één 46 mensen en in lander drie 40 in een vrachtframe. Lander één werd daarna terug omhoog gehaald en omgebouwd voor de laatste afdaling: vrachtframes losgeschroefd, stoelrekken (412 stoelen) erin. h19: "Lander one has been refitted: the cargo frames are unbolted and the seat racks are in."','ROMAN-Z16-h19;ROMAN-Z16-h16;ROMAN-Z16-h17;BESLUIT-Z25-8',-1240),
('Mess en lange hal zijn één zaal','De "mess" (h10) en de "long hall" (h15) zijn dezelfde zaal aan boord: de mess, ook wel de lange hal genoemd. Tekst blijft zoals hij is.','ROMAN-Z16-h10;ROMAN-Z16-h15;ROMAN-Z16-h12',-1240)]
for i,(o,f,v,j) in enumerate(B,1): put(f'BESLUIT-Z25-{i}',o,f,v,j)
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z25]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z25] {txt}',f' [Ronde Z25 {D}: aangevuld]',code));S['aangevuld'].append(code)
H={'h10':'De mess is dezelfde zaal als de lange hal (BESLUIT-Z25-3).',
'h15':'"long hall" = de mess uit h10 (BESLUIT-Z25-3).',
'h19':'"Lander one has been refitted: the cargo frames are unbolted and the seat racks are in." (BESLUIT-Z25-2).',
'h26':'"It had not made a sound in two years." (BESLUIT-Z25-1).'}
for h,t in H.items(): ap('ROMAN-Z16-'+h,'Laatste feedback: '+t)
W=[('WRIJ-Z25-1','Oortje: anderhalf of twee jaar','h26 "a year and a half" vs h29 "for two years"','Opgelost: "two years" (BESLUIT-Z25-1).','BESLUIT-Z25-1;ROMAN-Z16-h26'),
('WRIJ-Z25-2','Stoelen in lander één','46 in vrachtframe op landingsdag vs 412 stoelen later','Opgelost: omgebouwd, stoelrekken erin (BESLUIT-Z25-2).','BESLUIT-Z25-2;ROMAN-Z16-h19')]
for code,t,d,b,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z25','opgelost',code,v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z25: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z25: BESLUIT-Z25-1..3 (laatste feedback); [Z25] bij ROMAN-Z16-h10/h15/h19/h26; WRIJ-Z25-1..2 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z24/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
