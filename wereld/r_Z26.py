# Ronde Z26: telling 3.454 (Rogier: leg alles vast). Idempotent.
import sqlite3,shutil,os,json
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
D='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z26.db'): shutil.copy('canon.db','canon_backup_Z26.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z26-1'").fetchone() else RONDE+1
def put(code,ond,feit,ver,jaar):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','META','geen')",(ond,f'Vastgelegd door Rogier ({D}): '+feit+LABEL,R,ver,RONDE,code,ver,jaar));S['toegevoegd']+=1
B=[('De telling 3.454: voorspeld en uitgekomen','De Reckoner voorspelde in h5 "thirty-one point four percent" verlies van ca. 11.000 aan boord: 11.000 x 0,314 = 3.454. In h15 noemt hij "Three thousand four hundred and fifty-four ... I would prefer not to round." Ysas telling in h16 komt daar "to the person" op uit. Overlevenden: 11.000 - 3.454 = 7.546 ("approximately seven thousand" h5; "Seven thousand. A little more." h21).','ROMAN-Z16-h5;ROMAN-Z16-h15;ROMAN-Z16-h16;ROMAN-Z16-h21;BESLUIT-Z16-9;YSA-Z15-4',-1240),
('De Reckoner telde de doden buiten ring drie vooraf mee','De 3.454 is inclusief de doden buiten ring drie: de doden op ring twee bij de junction (afgesloten gangdeel), de drie mannen van de ontluchte gang E-7 en de twee gesneuvelden in het gevecht bij junction C-4. De Reckoner had hen al in zijn getal opgenomen voor ze stierven ("It had been sure all along"). h16, na "They matched. To the person.": "Including the five who had not been on the third ring at all. It had counted them too, before any of them had died." Dit maakt de Reckoner enger, niet de telling fout.','ROMAN-Z16-h16;ROMAN-Z16-h14;YSA-Z19-7;YSA-Z19-12;BESLUIT-Z26-1',-1240)]
for i,(o,f,v,j) in enumerate(B,1): put(f'BESLUIT-Z26-{i}',o,f,v,j)
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z26]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z26] {txt}',f' [Ronde Z26 {D}: aangevuld]',code));S['aangevuld'].append(code)
H={'h16':'"Including the five who had not been on the third ring at all. It had counted them too, before any of them had died." 3.454 is inclusief de doden buiten ring drie (BESLUIT-Z26-1..2).'}
for h,t in H.items(): ap('ROMAN-Z16-'+h,'Laatste feedback: '+t)
W=[('WRIJ-Z26-1','3.454 vs de vijf extra doden','h16 telt ring twee, E-7 (3) en C-4 (2) mee in 3.454, terwijl 31,4% alleen over de reductie leek te gaan','Opgelost: de Reckoner had die doden vooraf meegeteld; nieuwe regel in h16 (BESLUIT-Z26-2).','BESLUIT-Z26-2;ROMAN-Z16-h16')]
for code,t,d,b,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z26','opgelost',code,v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z26: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z26: BESLUIT-Z26-1..2 (telling 3.454); [Z26] bij ROMAN-Z16-h16; WRIJ-Z26-1 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z26/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
