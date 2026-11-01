# Ronde Z27: kraaien, inheemse planeet, tijdlijn (Rogier: leg alles vast). Idempotent, niets verwijderen.
import sqlite3,shutil,os,json
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
D='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z27.db'): shutil.copy('canon.db','canon_backup_Z27.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z27-1'").fetchone() else RONDE+1
def put(code,ond,feit,ver,jaar):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','META','geen')",(ond,f'Vastgelegd door Rogier ({D}): '+feit+LABEL,R,ver,RONDE,code,ver,jaar));S['toegevoegd']+=1
B=[('Kraaien: de grijze nabootsvogels van de rivier','Inheemse vogels van Velmara: grijs als het gras, stijve poten, zware zwarte snavels; ze bootsen geluiden en stemmen na. h21 (landingsdag, rivieroever): "One opened its beak and made a small wet sound, a boot coming out of mud. Hers, from the ramp." h31 (derde zomer): "The grey birds the weir boys called crows" zeggen het kamp terug ("a laugh, a child\'s name, mind the line"); een kraai op het stokje aan het eind van haar tomatenrij zegt in Ysa\'s eigen ruwe stem van de stemming "the body is the price" en vliegt op "still saying it". h33 (801, Brakhaven): "Up on the gutter a crow was talking in a woman\'s voice, to nobody." Dit zijn de voorouders van de registerkraaien. Zo draagt een cultuur zonder schrift Ysa\'s zin; de klikstem uit de kluizen komt er pas in 205 bij (BESLUIT-Z7-KRAAI) en "Wie nee zegt, wordt niet gevraagd" is later door de Orde toegevoegd (BESLUIT-Z17-8). Geen nieuwe grote lijn. Dieren alleen als symbool/geluid, nooit in een seksuele rol.','ROMAN-Z16-h21;ROMAN-Z16-h31;ROMAN-Z16-h33;BESLUIT-Z7-KRAAI;BESLUIT-Z17-8;YSA-Z16-12;ROMANCE-Z10-40',-1240),
('Inheemse planeet: geluid buiten het kamp','h21: "Something ticked in the reeds and stopped when she moved" (een onbekend klein dier of insect in het riet bij de rivier). h23: na de eerste vorst "something far out in the grass called for hours, two low notes and a gap, and nobody knew what it was or what it ate." Bestaande details blijven: grijs gras/riviergraan met een noot die naar rook smaakt (h21, h23), rivier, vorst, de Lady. Het dier blijft onbenoemd (dreiging op de achtergrond).','ROMAN-Z16-h21;ROMAN-Z16-h23;BESLUIT-Z21-3',-1239),
('Tijdlijn: "the year 801" is het jaar van de Zegel','Bron: BESLUIT-Z15-2 en YSA-Z15-800jaar (Muiterij/landing -1240, Liora 801: ruim 2040 jaar); GES-tijdlijn (Jaar 0 = Jaar van de Zegel); GEB-sterrensteen-inslag (-480: ca. 760 jaar in de baan, in h33 "seven hundred years"). Dus de roman speelt ca. 2040 jaar voor de hoofdboeken; de reviewer las 801 als jaren na de landing. Wattpad-pakket "about two thousand years" blijft en krijgt een verduidelijking ("year 801" is counted from the Seal; de landing ligt ca. twaalfhonderd jaar voor die jaartelling). Epiloogkop h33 nu: "The year 801 of the Seal · Brakhaven". De serienoot over de kraaien klopt nu met het boek (BESLUIT-Z27-1).','ROMAN-Z16-h33;BESLUIT-Z15-2;YSA-Z15-800jaar;GES-tijdlijn;GEB-sterrensteen-inslag',801)]
for i,(o,f,v,j) in enumerate(B,1): put(f'BESLUIT-Z27-{i}',o,f,v,j)
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z27]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z27] {txt}',f' [Ronde Z27 {D}: aangevuld]',code));S['aangevuld'].append(code)
H={'h21':'Rivieroever: tikken in het riet en grijze nabootsvogels die het geluid van haar laars nadoen (BESLUIT-Z27-1..2).',
 'h23':'Na de eerste vorst een onbekende nachtroep, twee lage tonen en een pauze (BESLUIT-Z27-2).',
 'h31':'Kraai op het stokje van de tomatenrij zegt "the body is the price" in Ysa\'s stem (BESLUIT-Z27-1).',
 'h33':'Kop "The year 801 of the Seal"; kraai met vrouwenstem op de goot in Brakhaven (BESLUIT-Z27-1, -3).'}
for h,t in H.items(): ap('ROMAN-Z16-'+h,'Worldbuilding-feedback: '+t)
W=[('WRIJ-Z27-1','Kraaien in serienoot, niet in boek','Wattpad-serienoot belooft "why the crows say The body is the price"; geen kraai in de roman','Opgelost: drie beats h21, h31, h33 (BESLUIT-Z27-1).','BESLUIT-Z27-1'),
('WRIJ-Z27-2','Kraaienstem: rivieroever (-1237) vs kluisopname (205)','Canon: de kraaienstem met klik is in 205 uit de kluizen opgepikt (BESLUIT-Z7-KRAAI); de roman laat kraaien de zin al na de stemming herhalen','Opgelost: twee lagen. De zin leeft sinds de rivier in Ysa\'s ruwe stem (zonder klik); in 205 komt de metalige klikstem uit de kluizen erbij; de tweede helft is een Orde-vervalsing (BESLUIT-Z17-8).','BESLUIT-Z27-1;BESLUIT-Z7-KRAAI;BESLUIT-Z17-8'),
('WRIJ-Z27-3','800 of 2000 jaar tussen roman en hoofdboeken','Review: epiloog "year 801" suggereert ca. 800 jaar; pakket zegt ca. 2000','Opgelost: 801 is het jaar van de Zegel; ca. 2040 jaar klopt (BESLUIT-Z15-2); kop en pakket verduidelijkt (BESLUIT-Z27-3).','BESLUIT-Z27-3;BESLUIT-Z15-2')]
for code,t,d,b,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z27','opgelost',code,v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z27: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z27: BESLUIT-Z27-1..3 (kraaien, inheemse planeet, tijdlijn 801 van de Zegel); [Z27] bij ROMAN-Z16-h21, h23, h31, h33; WRIJ-Z27-1..3 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
os.makedirs('z27',exist_ok=True);json.dump(S,open('z27/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
