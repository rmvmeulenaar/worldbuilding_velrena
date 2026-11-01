# Ronde Z24: eindrapport consistentie (Rogier: leg alles vast). Idempotent.
import sqlite3,shutil,os,json
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
D='2026-10-31';R='Rogier: leg alles vast, 2026-10-31';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z24.db'): shutil.copy('canon.db','canon_backup_Z24.db')
c=sqlite3.connect(DB);S={'toegevoegd':0,'aangevuld':[]}
RONDE=c.execute("select max(ronde) from canon").fetchone()[0]
RONDE=RONDE if c.execute("select 1 from canon where code='BESLUIT-Z24-1'").fetchone() else RONDE+1
def put(code,ond,feit,ver,jaar):
  if c.execute('select 1 from canon where code=?',(code,)).fetchone(): return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,functie,techniek) values('Besluit',?,?,'vastgesteld',?,?,?,?,?,?,'0 Voortijd','META','geen')",(ond,f'Vastgelegd door Rogier ({D}): '+feit+LABEL,R,ver,RONDE,code,ver,jaar));S['toegevoegd']+=1
B=[('Hesta\'s bezoeken aan C-4-R: 12, 9 en 5 dagen vóór de landing','Hesta ging door de kruipgang C-4-R op 12, 9 en 5 dagen vóór de landing; de laatste op de avond van de 4-4-raad, die op vijf dagen lag (niet zes). Corrigeert YSA-Z20-17 (dat 6 zei); die rij blijft staan met [Z24]-notitie.','YSA-Z20-17;ROMAN-Z16-h24;ROMAN-Z16-h27;ROMAN-Z16-h16',-1240),
('Lander zes: 406 mensen','Lander zes nam bij de golfafdaling op dag 2, bij dageraad, 406 mensen mee (h17: "Four hundred and six"), door de Reckoner gevlogen. Past bij ~410 stoelen per lander (lander één 412).','ROMAN-Z16-h17;YSA-Z20-1',-1240),
('Ilse Varo\'s man leeft','Ilse Varo stierf in kwartier 340 (h16). Haar man (seed stock, ongeveer 50, kwam terug met lander drie) leeft en loopt in h21 bij "Mother Ysa" alleen over het veld, met één hand op zijn eigen arm. Nog naamloos; de hoofdserie mag hem een naam geven.','ROMAN-Z16-h16;ROMAN-Z16-h21',-1240),
('Pellam T. lag op de brits','Pellam T. (kwartier 301) lag op de brits (h16); in h21 staat op Ysa\'s blad "Supine. No struggle." Old Pellam is zijn broer. In h31 is het voorbeeld op het blad "Seated. Together." (de Daskers).','ROMAN-Z16-h16;ROMAN-Z16-h21;ROMAN-Z16-h31',-1240),
('Microfoon van lander zeven nooit open','Thalen heeft de microfoon van lander zeven nooit opengezet vóór de nacht van h25 (vervangt "stopped using it in the first winter"); hij keek wel via de downlink (h22/h24).','ROMAN-Z16-h25;ROMAN-Z16-h22;ROMAN-Z16-h24',-1239),
('Wren Tallis in de baai','Wren Tallis stond in de baai toen Thalen "Someone has to hold the ship" zei (in de luchtsluis); zo kwam de zin de eerste week in het kamp. Vervangt "off the flight net".','ROMAN-Z16-h27;ROMAN-Z16-h20',-1240),
('Opname in de warme kernkamer bij C-4','De opname "Fourth night before landing. Third hour. Eleven minutes" is gemaakt in de warme kernkamer bij C-4, niet in de koude kluis; de koude kluis bewaart haar alleen. De opname begint met dezelfde eerste zin als in h5 ("Last night you ran the continuation model for me.").','ROMAN-Z16-h32;ROMAN-Z16-h05',-1240),
('Landers: twee afdalingen na de eerste','Corran in h16: "Each has two more descents in it. Maybe." (h19 herhaalt dat). Telling: ongeveer 11.000 aan boord, 3.454 dood, dus ongeveer 7.500 overlevenden. Eerste afdaling 40-46 per lander (vooral zaad en bemanning, ~500). Daarna golven over dag 2-5 met twee afdalingen per lander: 12 x 2 x ~410 = ~9.800 plaatsen, ruim genoeg voor ~7.000; lander zes 406 (dag 2), lander één als laatste: 412 stoelen, 409 passagiers (dag 5). Totaal ~7.500 omlaag; op de grond "seven thousand, a little more" (h21/h29).','ROMAN-Z16-h16;ROMAN-Z16-h19;ROMAN-Z16-h17;YSA-Z20-1',-1240),
('Raad van negen; hoofd biologie raadslid zonder stem','De scheepsraad heeft negen stemmen (4 + 4 + Hesta). Ysa is als hoofd biologie raadslid zonder stem ("council member", indiener); haar stem telt dus niet in de 4-4 en de 5-4. Op de grond weigerde ze de raad in de eerste week; in h29 staat de stoel van biologie leeg naast de negen. Tekst niet aangepast (geen tegenspraak).','ROMAN-Z16-h29;ROMAN-Z16-h24;ROMAN-Z16-h15',-1240)]
for i,(o,f,v,j) in enumerate(B,1): put(f'BESLUIT-Z24-{i}',o,f,v,j)
def ap(code,txt):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if f and '[Z24]' not in f[0]:
    c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' [Z24] {txt}',f' [Ronde Z24 {D}: aangevuld]',code));S['aangevuld'].append(code)
ap('YSA-Z20-17','Gecorrigeerd: de bezoeken waren 12, 9 en 5 dagen vóór de landing (niet 6); de 4-4-raad lag op vijf dagen. BESLUIT-Z24-1.')
ap('YSA-Z20-1','Landers: ~410 stoelen elk, twee afdalingen na de eerste; lander zes 406. BESLUIT-Z24-2, -8.')
H={'h12':'De snijder van de paal met Ysa\'s gezicht is een man ("not the man who would carve her face").',
'h15':'"where they had sung last night"; log: "the next morning". Gegeven raad: Ysa is raadslid zonder stem (BESLUIT-Z24-9).',
'h16':'"Not in the dome. In the bridge annex"; "Five days out"; Corran: "Each has two more descents in it" (BESLUIT-Z24-8). Pellam op de brits (BESLUIT-Z24-4).',
'h17':'Lander zes: "Four hundred and six" (BESLUIT-Z24-2).',
'h19':'"*Two more descents in it,* Corran had said." (BESLUIT-Z24-8).',
'h21':'Ilse Varo\'s man loopt alleen (BESLUIT-Z24-3); Pellam "Supine. No struggle." (BESLUIT-Z24-4).',
'h24':'Hesta: "Nine days before landing. Five days before landing."; de 4-4-raad op vijf dagen (BESLUIT-Z24-1).',
'h25':'Thalen had de microfoon van lander zeven nooit opengezet (BESLUIT-Z24-5).',
'h27':'"in the dome five days before landing"; Wren Tallis stond in de baai (BESLUIT-Z24-6).',
'h30':'"He watched every day: at dawn, at noon, and then,".',
'h31':'Voorbeeld op het blad: "Seated. Together." (BESLUIT-Z24-4).',
'h32':'"in the warm chamber at C-4"; opname begint met "Last night you ran the continuation model for me."; "He heard her not leave." (BESLUIT-Z24-7).'}
for h,t in H.items(): ap('ROMAN-Z16-'+h,'Eindrapport-revisie: '+t)
W=[('WRIJ-Z24-1','Hesta\'s derde bezoek: 6 of 5 dagen','YSA-Z20-17 vs h3/h16/h24','Canon zei 6 dagen, tekst legt de 4-4-raad op vijf. Opgelost: 12, 9 en 5 (BESLUIT-Z24-1).','BESLUIT-Z24-1;YSA-Z20-17'),
('WRIJ-Z24-2','Landercapaciteit','h16 "one more descent" vs ~7.500 overlevenden','12 x ~410 x één afdaling = ~4.900. Opgelost met twee afdalingen (BESLUIT-Z24-8).','BESLUIT-Z24-8;ROMAN-Z16-h16'),
('WRIJ-Z24-3','Tiende stoel in h29','Raad van 9 vs lege stoel biologie','Opgelost: hoofd biologie is raadslid zonder stem (BESLUIT-Z24-9); tekst blijft.','BESLUIT-Z24-9;ROMAN-Z16-h29')]
for code,t,d,b,v in W:
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z24','opgelost',code,v))
if not c.execute("select 1 from logboek where wat like 'Ronde Z24: %'").fetchone(): c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z24: BESLUIT-Z24-1..9 (eindrapport); [Z24] bij YSA-Z20-17, YSA-Z20-1 en 12 ROMAN-Z16-h*; WRIJ-Z24-1..3 opgelost.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z24/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
