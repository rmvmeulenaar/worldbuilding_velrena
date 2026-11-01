# Ronde Z18: keuzes h7-12 in de canon. Idempotent; data in z18/
import sqlite3,shutil,os,sys,json,importlib
sys.path.insert(0,'z18'); data=importlib.import_module('data'); sys.path.pop(0)
B,Y,D,H,W=data.B,data.Y,data.D,data.H,data.W
LABEL=' Veiligheidslabel: alleen volwassenen (18+) in seksuele rollen; geen minderjarigen of dieren in een seksuele rol; nooit seks met wie echt niet kan instemmen; donkere thema\'s gelabeld.'
RONDE=48;TAG='Z18';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z18.db'): shutil.copy('canon.db','canon_backup_Z18.db')
c=sqlite3.connect(DB); S={'toegevoegd':0,'aangevuld':[],'status_gewijzigd':[]}
def tp(j):
  if j is None: return None
  for a,b,nm in ((-99999,-600,'0 Voortijd'),(-600,-150,'1 Overvloed'),(-150,-40,'2 Vonk'),(-40,0,'3 Brand'),(0,130,'4 Noodtoestand'),(130,340,'5 Ontvangst'),(340,720,'6 Markt'),(720,801,'7 Barsten')):
    if a<=j<b: return nm
  return '801 (nu)' if j==801 else 'na 801'
CAT=c.execute("select categorie from canon where code='ROMAN-Z16-roman'").fetchone()[0]
def put(code,cat,ond,feit,status,ver,jaar,functie='VERH',intens=None,weet=None):
  feit=feit if 'Veiligheidslabel' in feit else feit+LABEL
  r=(cat,ond,feit,status,f'Ronde {TAG} {D}: keuzes h7-12',ver,RONDE,code,ver,jaar,tp(jaar),intens,weet,functie,'geen')
  if c.execute('select 1 from canon where code=?',(code,)).fetchone():
    c.execute('update canon set categorie=?,onderwerp=?,feit=?,status=?,reden=?,hangt_samen_met=?,ronde=?,verwijst_naar=?,jaar=?,tijdperk=?,intensiteit=?,weet=?,functie=?,techniek=? where code=?',r[:7]+r[8:]+(code,))
  else:
    c.execute('insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,tijdperk,intensiteit,weet,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',r); S['toegevoegd']+=1
def ap(code,txt,m='[Z18]'):
  f=c.execute('select feit from canon where code=?',(code,)).fetchone()
  if not f: S.setdefault('niet_gevonden',[]).append(code); return
  if m not in f[0]: c.execute('update canon set feit=feit||?, reden=coalesce(reden,\'\')||? where code=?',(f' {m} {txt}',f' [Ronde {TAG} {D}: aangevuld]',code))
  S['aangevuld'].append(code)
def vast(code,besl):
  if c.execute("select 1 from canon where code=? and status='voorlopig'",(code,)).fetchone():
    c.execute("update canon set status='vastgesteld', reden=coalesce(reden,'')||? where code=?",(f' [Ronde {TAG}: vastgesteld door {besl}]',code))
  S['status_gewijzigd'].append(code)
for n,o,f,j,v in B:
  put(f'BESLUIT-Z18-{n}','Besluit',o,f'Gekozen door Rogier ("alles zoals aanbevolen", {D}): {f}','vastgesteld',v,j,'META')
for n,o,f,j,bron in Y:
  put(f'YSA-Z18-{n}',CAT,o,f'{f} Nieuw bedacht (roman {bron}); voorstel, wacht op goedkeuring van Rogier.','voorlopig','ROMAN-Z16-roman;PER-v4-ysa-maren;PER-v4-thalen-orr',j)
for h,(t,j,i,w,fn) in H.items():
  ap(f'ROMAN-Z16-h{h:02d}',f'Jaar {j} ({tp(j)}); intensiteit {i}; weet: {w}; functie: {fn}. {t}')
  c.execute("update canon set intensiteit=coalesce(intensiteit,?), weet=coalesce(weet,?) where code=?",(i,w,f'ROMAN-Z16-h{h:02d}'))
ap('ROMAN-Z16-h32','Aanpassing bij het schrijven: "fifth night" wordt "fourth night" (BESLUIT-Z17-2, BESLUIT-Z18-6); de novelle zegt nog "fifth night".')
ap('ROMAN-Z16-h13','Aanpassing bij het schrijven: Mira woont in kwartier 3-61, niet "room 3-114" (WRIJ-Z18-2); override half open uit h11 (YSA-Z18-15); "rain on a hollow log" niet herhalen.')
ap('YSA-Z16-3','Besloten: ze kon tot het eind intrekken (BESLUIT-Z18-1); haar vier medestanders zitten met haar in lander 1 en overleven (BESLUIT-Z18-5).')
ap('PER-v4-hesta-kael','Wond: haar moeder verloor na een week ziekte haar post bij het water (BESLUIT-Z18-4). Kent de kernroute (YSA-Z18-7).')
ap('PER-v4-thalen-orr','Leeftijd vastgesteld: 32 in -1240, dood -1198 op 74 (BESLUIT-Z18-3).')
for k in ('YSA-Z17-9','TOESTAND-Z17-PER-v4-thalen-orr-1','TOESTAND-Z17-PER-v4-thalen-orr-2','TOESTAND-Z17-PER-v4-thalen-orr-3'): vast(k,'BESLUIT-Z18-3')
c.execute("delete from wrijving where code like 'WRIJ-Z18-%'")
for i,(t,d,b,s,v) in enumerate(W,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,d,b,'Z18',s,f'WRIJ-Z18-{i}',v))
st=dict(c.execute('select status,count(*) from canon group by status').fetchall())
put('KWALITEIT-Z18','Besluit','Kwaliteitsrapport ronde Z18',f'Ronde Z18 ({D}): BESLUIT-Z18-1..6 vastgesteld; YSA-Z18-1..15 voorstel; leeftijd Thalen vastgesteld; ROMAN-Z16-h07..h12 aangevuld; h13 en h32 aanpassingen genoteerd; WRIJ-Z18-1 open, 2-3 opgelost. Statussen: {st}.','voorlopig','ROMAN-Z16-roman',801,'META')
c.execute("delete from logboek where wat like 'Ronde Z18: %'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,'Ronde Z18: keuzes h7-12; 6 besluiten, 15 voorstellen, 3 wrijvingen.'))
c.commit()
S['status']=dict(c.execute('select status,count(*) from canon group by status').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
S['aangevuld']=sorted(set(S['aangevuld']));S['status_gewijzigd']=sorted(set(S['status_gewijzigd']))
json.dump(S,open('z18/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
