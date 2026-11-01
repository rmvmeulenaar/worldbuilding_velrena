# Eenmalig/idempotent: voegt 'code' en 'verwijst_naar' toe en vult lege waarden.
import sqlite3,re,unicodedata
c=sqlite3.connect('canon.db')
for t in ['canon','wrijving','open_vraag']:
  cols=[r[1] for r in c.execute(f'pragma table_info({t})')]
  for k in ['code','verwijst_naar']:
    if k not in cols: c.execute(f'alter table {t} add column {k} text')
def slug(s,n=3):
  s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
  s=re.sub(r'\(.*?\)','',s);s=re.sub(r'[^a-z0-9 ]',' ',s)
  w=[x for x in s.split() if x not in('de','het','een','van','en','der','op','om','tot','als','huis','a')]
  return '-'.join(w[:n]) or 'x'
PRE={'Land':'REG','Regio':'REG','Sfeer en uiterlijk':'SFEER','Economie':'ECO','Macht':'MACHT','Wetten':'WET','Maatschappij':'REGEL','Demografie':'REGEL','Genre':'REGEL','Afstamming':'REGEL','Religie':'ORDE','Magie':'MAGIE','Oorsprong':'GES','Geschiedenis':'GES','Geheimen':'GEH','Cultuur':'CUL','Gezondheid':'CUL','Mode en kleding':'MODE','Riten':'RITE','Kinks en situaties':'KINK','Rituelen':'RIT','Extreme rituelen':'RIT','Rituele handelingen':'HAND','Ritueel systeem':'SYS','Personage':'PER','Verhaal':'QST'}
SPEC={'Huis Varenne':'HUI-varenne','Huis Kaldra':'HUI-kaldra','Huis Mirre':'HUI-mirre','Het Zonvorstendom van Qesh':'HUI-qesh','De Orde van de Ontvangst':'ORDE-orde','HET GEHEIM: de Zegel van Ves-Anath':'GEH-zegel','Kink-schaal':'RIT-kinkschaal','Zaad geeft tijdelijk kracht':'MAGIE-zaadkracht','Kracht en duur van zaad':'MAGIE-kracht-duur','Geslachtsverhouding':'REGEL-verhouding','Overzicht: het Vijfstromenrijk Velmara':'REG-overzicht'}
used=set(r[0] for r in c.execute('select code from canon where code is not null'))
for i,k,o in c.execute('select id,categorie,onderwerp from canon where code is null order by id').fetchall():
  p=PRE.get(k,'X')
  if p=='PER': base='PER-'+slug(o,1) if o not in('Bondgenoten','Tegenstanders','Gewone mannen') else 'PER-'+slug(o)
  elif p=='REG' and k=='Regio': base='REG-'+slug(o,1)
  else: base=SPEC.get(o) if o in SPEC and k not in('Rituele handelingen','Ritueel systeem') else p+'-'+slug(o)
  code=base;n=2
  while code in used: code=f'{base}-{n}';n+=1
  used.add(code);c.execute('update canon set code=? where id=?',(code,i))
for t,p in [('wrijving','WRIJ'),('open_vraag','VRAAG')]:
  c.execute(f"update {t} set code='{p}-'||printf('%03d',id) where code is null")
# verwijzingen: termen -> codes
rows=c.execute('select id,categorie,onderwerp,code,feit,hangt_samen_met from canon').fetchall()
T={}
def term(t,cd): T.setdefault(t.lower(),cd)
for i,k,o,cd,f,h in rows:
  if k in('Rituele handelingen','Ritueel systeem'): continue
  term(re.sub(r'\(.*?\)','',o).strip(),cd)
EX={'liora':'PER-liora','aeron':'PER-aeron','morvane':'PER-morvane','khaled':'PER-khaled','teo':'PER-gewone-mannen','bram':'PER-gewone-mannen','varenne':'HUI-varenne','kaldra':'HUI-kaldra','mirre':'HUI-mirre','qesh':'REG-rosse','saelith':'REG-saelith','ambergaard':'REG-ambergaard','hallowyn':'REG-ambergaard','kaldrun':'REG-hoogvrouwe','gebergte':'REG-hoogvrouwe','brakhaven':'REG-zoutkust','zoutkust':'REG-zoutkust','groenmuil':'REG-groenmuil','tuaro':'REG-groenmuil','lisk':'REG-saelith','woestijn':'REG-rosse','kharvos':'REG-kharvos','zusterschap':'REG-stille','orde':'ORDE-orde','zegel':'GEH-zegel','geheim':'GEH-zegel','zaad-kracht':'MAGIE-kracht-duur','kracht en duur':'MAGIE-kracht-duur','leegte':'MAGIE-kracht-duur','verslaving':'MAGIE-verslaving','binding':'MAGIE-verslaving','register':'REGEL-registers-merken','bloedlijn':'REGEL-registers-merken','verwantschap':'REGEL-verwantschapstaboe','inteelt':'REGEL-registers-merken','gaven-m':'MACHT-gaven-mannen','gewone m':'MACHT-gewone-mannen','economie':'ECO-wat-wordt-verhandeld','prijzen':'ECO-prijzen-mannen-zaad','gunstbrie':'ECO-geld','zwarte markt':'KINK-betalen-lichaam','leger':'MACHT-leger','queeste':'QST-doel-reden-gevaar','sjerp':'MODE-vrouwen-basis','heilig woord':'RIT-kinkschaal','weiger':'WET-wie-weigert','toestemming':'WET-wie-weigert','gezin':'CUL-gezin-wonen','moederhuis':'CUL-gezin-wonen','maankruid':'CUL-zwangerschap-anticonceptie','religie':'ORDE-doel-geloof','geloof':'ORDE-doel-geloof'}
codes=set(r[0] for r in c.execute('select code from canon'))
EX={k:v for k,v in EX.items() if v in codes}
def refs(text,self_code,extra=()):
  s=set(extra);tl=(text or '').lower()
  for k,v in EX.items():
    if k in tl: s.add(v)
  for t,v in T.items():
    if len(t)>5 and t in tl: s.add(v)
  s.discard(self_code);return ';'.join(sorted(x for x in s if x in codes))
for i,k,o,cd,f,h in rows:
  extra=[]
  if k in('Rituele handelingen','Ritueel systeem'):
    r=c.execute("select code from canon where onderwerp=? and categorie in('Rituelen','Extreme rituelen')",(o,)).fetchone()
    if r: extra=[r[0]]
  c.execute('update canon set verwijst_naar=? where id=? and verwijst_naar is null',(refs((h or '')+' '+f,cd,extra),i))
for t,a,b in [('wrijving','titel',"delen_die_botsen||' '||beschrijving"),('open_vraag','vraag',"waarom_belangrijk||' '||coalesce(antwoord,'')")]:
  for i,cd,x in c.execute(f'select id,code,{a}||\' \'||{b} from {t}').fetchall():
    c.execute(f'update {t} set verwijst_naar=? where id=? and verwijst_naar is null',(refs(x,cd),i))
c.commit()
print(c.execute('select count(*) from canon').fetchone())
