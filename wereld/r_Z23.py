# Ronde Z23: eindfeedback (Rogier: leg alles vast). Idempotent.
import sqlite3,shutil,os,json
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
D='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z23.db'): shutil.copy('canon.db','canon_backup_Z23.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z23-1'").fetchone() else RONDE+1
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,ver,jaar,functie):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values(?,?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd',?,'geen')",(cat,ond,feit+LABEL,f'Ronde Z23 {D}: {R}',ver,RONDE,code,ver,jaar,functie));S['toegevoegd']+=1
B=[('Hesta\'s cellen in h27: zeven bij het bod, negen inmiddels','In h27 zegt Hesta eerst "But I keep the last cells. Seven of them. The ones that still hold a charge." Ysa antwoordt "Seven", Hesta: "Nine, by now. I\'ve been busy." Canon: zeven cellen bij het bod (wat de raad en Ysa kennen), negen in Hesta\'s schuur inmiddels (twee extra in stilte verzameld). Verduidelijkt YSA-Z21-3, YSA-Z22-5 en ROMAN-Z16-h27; die rijen blijven staan.','ROMAN-Z16-h27;YSA-Z21-3;YSA-Z22-5;MOTOREN-Z22',-1231),
('"Mother" als titel pas vanaf h21','De titel "Mother" voor Ysa ontstaat pas in h21, op de grond. Aan boord gebruikt Corran haar naam: in h16 "You showed us a branch, Ysa." en in h17 "Ysa\'s ghost protocol". Vanaf h21 mag "Mother" (o.a. h23, h27, h29).','ROMAN-Z16-h16;ROMAN-Z16-h17;ROMAN-Z16-h21',-1240),
('Slot h30','H30 eindigt op "He found the old recorder in the lab the next morning, and pressed the button, and did not know yet what to say into it." De losse regel "It was always there." is geschrapt.','ROMAN-Z16-h30;YSA-Z22-6',-1231),
('Eén kop in roman_ysa_VOLLEDIG.md','De dubbele kop (tweede titel met content-regel) is uit verhalen/roman_ysa_VOLLEDIG.md verwijderd: één titel, één auteursregel (Iris Calloway), één content warning. Daarna is het boek klaar om te posten (cijfer reviewer 8,5).','ROMAN-Z16-roman',-1240)]
for i,(o,f,v,j) in enumerate(B,1): put(f'BESLUIT-Z23-{i}','Besluit',o,f'Vastgelegd door Rogier ({D}): {f}',v,j,'META')
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z23]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z23] {txt}',f' [Ronde Z23 {D}: aangevuld]',code));S['aangevuld'].append(code)
N7='Celtelling verduidelijkt (BESLUIT-Z23-1): Hesta zegt eerst "Seven of them", Ysa "Seven", Hesta "Nine, by now": zeven bij het bod, negen inmiddels. Waar hier "Nine of them" of negen cellen staat, geldt: negen is de huidige stand, zeven het bod.'
for k in ('ROMAN-Z16-h27','YSA-Z21-3','YSA-Z22-5','MOTOREN-Z22'): ap(k,N7)
ap('ROMAN-Z16-h16','Corran zegt "You showed us a branch, Ysa." (niet "Mother"; die titel ontstaat pas in h21). BESLUIT-Z23-2.')
ap('ROMAN-Z16-h17','Corran zegt "Ysa\'s ghost protocol"; nog geen "Mother" aan boord. BESLUIT-Z23-2.')
ap('ROMAN-Z16-h30','Slot: "...and did not know yet what to say into it." De losse regel "It was always there." is geschrapt. BESLUIT-Z23-3.')
if not c.execute("select 1 from wrijving where code='WRIJ-Z23-1'").fetchone():
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",('Zeven of negen cellen (h27)','ROMAN-Z16-h27 tekst vs YSA-Z21-3/YSA-Z22-5','Revisie liet Hesta "Nine of them" zeggen vóór Ysa\'s "Seven"; teruggezet naar "Seven of them". Opgelost: zeven bij het bod, negen inmiddels (BESLUIT-Z23-1).','Z23','opgelost','WRIJ-Z23-1','BESLUIT-Z23-1;ROMAN-Z16-h27'))
if not c.execute("select 1 from logboek where wat like 'Ronde Z23: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z23: BESLUIT-Z23-1..4 (eindfeedback); [Z23] bij h16/h17/h27/h30, YSA-Z21-3, YSA-Z22-5, MOTOREN-Z22; WRIJ-Z23-1 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z23/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
