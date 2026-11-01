# Ronde Z12: de 15 beslissingen van Rogier (31-10-2026) verwerken (idempotent); data in z12/
import sqlite3,shutil,os,sys,re,json
sys.path.insert(0,'z12'); import data as Dt
RONDE=41;TAG='Z12';D='2026-10-31'
GR=" Label: alle betrokkenen in seksuele rollen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seks met wie echt niet kan instemmen; het Jongenshof en zijn riten zijn volledig niet-seksueel."
if not os.path.exists('canon_backup_Z12.db'): shutil.copy('canon.db','canon_backup_Z12.db')
c=sqlite3.connect('canon.db')
A="status not like '%vervangen%' and status!='vervallen'"
BEST={r[0] for r in c.execute("select code from canon where code is not null")}
n=0;vast={i:[] for i in Dt.B};verv=[];per={i:0 for i in Dt.B}
def add(code,cat,ond,feit,reden,refs,status='voorlopig',jaar=None,functie='META',gr=True,besl=None):
  global n
  refs=';'.join(x for x in dict.fromkeys(refs.split(';')) if x and x in BEST)
  feit=feit+(GR if gr else '')
  if besl: per[besl]+=1
  if c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("update canon set feit=?,verwijst_naar=?,hangt_samen_met=?,status=? where code=? and ronde=?",(feit,refs,refs,status,code,RONDE));return
  c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar,functie,techniek) values(?,?,?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,status,f'Ronde {TAG}: '+reden,refs,RONDE,code,refs,jaar,functie,'geen'));n+=1;BEST.add(code)
def vaststel(code,i):
  if c.execute("update canon set status='vastgesteld', reden=reden||? where code=? and status='voorlopig'",(f' [Ronde {TAG} {D}: vastgesteld door BESLUIT-Z12-{i}]',code)).rowcount: vast[i].append(code)
# 1 besluitrijen
for i,(o,k,f,w,g,refs) in Dt.B.items():
  add(f'BESLUIT-Z12-{i}','Besluit',f'Besluit Z12-{i}: {o}',f'Gekozen door Rogier ({D}): {k}. {f} Reden: {w} Gevolgen in de canon: {g}',f'Rogier kiest {k} (BESLISSEN_belangrijk nr {i}); bevestigt BESLUIT-{i} uit B1',f'BESLUIT-{i};{refs}','vastgesteld',801,besl=i)
add('BESLUIT-Z12-5-schema','Besluit','Schema dubbel bestuur','ORDE (Saelith, Ves-Anath): zaad, register, Ontvangsten, gunstbrieven, rechtspraak over lijnen, wijding van huizen, geloof. | HUIZEN (geregistreerd): land, geld, leger, belasting, havens, handel, huwelijkscontracten. | GEDEELD: de Raad van Zegel en Zilver (Orde + vijf grootste huizen) beslist over oorlog en Kharvos. | Drukmiddelen: de Orde kan een huis uit het register schrappen (geen zaad); de huizen kunnen de tempels droogleggen (geen geld). | Verhaalmotor: elke verraadlijn loopt over de grens tussen register en geld.','schema bij besluit 5','BESLUIT-Z12-5;BEST-B1-schema;REGEL-regeringsvorm','vastgesteld',801,besl=5)
# 2 vaststellen
for i,codes in Dt.VAST.items():
  for x in codes: vaststel(x,i)
for i in range(1,16):
  vaststel(f'BESLUIT-{i}',i)
for code, in c.execute(f"select code from canon where code like 'SEKS-VOLK-%' and {A}").fetchall():
  v=code.split('-')[2]
  if v in ('karruk','saelmor','aelthir'): vaststel(code,4)
  else: c.execute("update canon set reden=reden||? where code=? and reden not like '%Ronde Z12%'",(' [Ronde Z12: kleur in boek 1'+(', diep in boek 2' if v in ('kluwer','oevrin','skerra') else ', later boek')+' (BESLUIT-Z12-4)]',code))
# 3 vervangen
for old,new,feit,i,st in Dt.NIEUW:
  r=c.execute("select categorie,onderwerp,jaar from canon where code=?",(old,)).fetchone()
  add(new,r[0],r[1],feit,f'vervangt {old} (BESLUIT-Z12-{i})',f'{old};BESLUIT-Z12-{i};BESLUIT-{i}',st,r[2],gr=False,besl=i)
  if c.execute("update canon set status='voorlopig, vervangen', reden=reden||? where code=? and status not like '%vervangen%'",(f' [Ronde {TAG}: vervangen door {new}]',old)).rowcount: verv.append(old)
c.execute("update canon set reden=reden||' [Ronde Z12: stem heet Ysara, Thalen Orr erin opgegaan; zie BESLUIT-Z12-wortelstem]' where code='BESLUIT-Z1-derdeweg' and reden not like '%Ronde Z12%'")
# 4 vragen en oude wrijvingen bevestigen
VR={1:['VRAAG-012'],2:['VRAAG-013','VRAAG-019'],6:['VRAAG-030','VRAAG-065'],7:['VRAAG-017','VRAAG-018','VRAAG-055'],8:['VRAAG-024','VRAAG-046'],14:['VRAAG-020'],15:['VRAAG-054']}
for i,qs in VR.items():
  for q in qs: c.execute("update open_vraag set status='beantwoord', antwoord=coalesce(antwoord,'')||? where code=? and coalesce(antwoord,'') not like '%Z12%'",(f' [Z12 {D}: bevestigd door Rogier, BESLUIT-Z12-{i}]',q))
for w,i in (('WRIJ-057',3),('WRIJ-050',8),('WRIJ-080',15)):
  c.execute("update wrijving set beschrijving=beschrijving||? where code=? and beschrijving not like '%Z12%'",(f' [Z12: bevestigd, BESLUIT-Z12-{i}'+('; stem nu Ysara met Thalen erin opgegaan, zie WRIJ-Z12-1' if w=='WRIJ-080' else '')+']',w))
# 5 ketencontrole
KEYS={1:['GEH-zegel','GEH-zegel-Z1','GEH-zegel-B1','BESLUIT-1','BESLUIT-1-Z1'],2:['BESLUIT-2','BESLUIT-V5-thalen'],3:['REG-kharvos','REG-kharvos-B1','BESLUIT-3'],4:['BESLUIT-4'],5:['REGEL-regeringsvorm','BESLUIT-5','BEST-B1-schema'],6:['BESLUIT-6'],7:['BESLUIT-7','PER-sef','PER-aeron'],8:['LICH-pest','LICH-pest-B1','REGEL-walgingsschaal','BESLUIT-8'],9:['BESLUIT-9'],10:['LIJN-overzicht','BESLUIT-10'],11:['REGEL-verhouding','GEB-r10-eerste-lek','BESLUIT-11'],12:['NAV-wormwording','NAV-wormwording-B1','NAV-hartstem','BESLUIT-12'],13:['BESLUIT-13'],14:['RIT-hofproef','BESLUIT-14'],15:['BESLUIT-15','BESLUIT-Z4-wortelstem','LIJN-quest']}
PAT=[r'priesteressen (bouwden|maakten|schiepen) (het|de) [Zz]egel',r'1 op (de )?300(?! vervalt)',r'1 op 90\b',r'stem in de [Ww]ortel is Thalen',r'(jongens?|zonen)[^.]{0,40}(vertrek\w*|naar het Jongenshof)[^.]{0,20}\b(1[0-9]|zestien|twaalf|tien)\b',r'Kharvos[^.]*(altijd|eeuwenlang) (vijand|vijandig)',r'[Bb]loedafstand[^.]{0,30}(bewezen|absoluut)',r'Liora[^.]*(trouwt|kiest voor) (Sef|Ruy)',r'Drempel[^.]{0,40}(volledig|geheel) (terug|genees)']
rows=c.execute(f"select code,feit,verwijst_naar,hangt_samen_met from canon where {A}").fetchall()
keten={};treffers=[]
for code,f,v,h in rows:
  refs=set((v or '').split(';'))|set((h or '').split(';'))
  for i,ks in KEYS.items():
    if refs & set(ks) or any(k in (f or '') for k in ks): keten.setdefault(i,set()).add(code)
  for p in PAT:
    m=re.search(p,f or '')
    if m and not code.startswith(('BESLUIT-','WRIJ')) : treffers.append((code,m.group(0)[:70]))
c.execute("delete from wrijving where code like 'WRIJ-Z12-%'")
W=list(Dt.W)
W.append(('Ketencontrole Z12',';'.join(x for x,_ in treffers[:5]) or 'BESLUIT-Z12-1','Rijen in de keten per besluit: '+', '.join(f'{i}: {len(keten.get(i,()))}' for i in range(1,16))+f'. Strijdige patronen in actieve rijen: {len(treffers)} ('+'; '.join(f'{a}: "{b}"' for a,b in treffers[:20])+').','open' if treffers else 'opgelost','geen strijdige actieve rijen meer' if not treffers else 'handmatig nalopen in een volgende ronde.'))
for j,(t,b,e,s,bs) in enumerate(W,1):
  c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)",(t,b,e+' Besluit: '+bs,'Z12',s,f'WRIJ-Z12-{j}',b))
# 6 verhaal-aanpassingen (verhalen NIET herschreven)
for j,(v,t) in enumerate(Dt.A,1):
  add(f'VERHAAL-AANPASSING-Z12-{j}','Verhaal',f'Verhaal-aanpassing Z12-{j} ({v})',f'{t} Status: nog niet uitgevoerd; het verhaal is NIET herschreven.','gevolg van de beslissingen voor de verhalen','VERHAALTIJD-Z11-3;VERHAALTIJD-Z11-6;PER-sef;BESLUIT-Z12-7;BESLUIT-Z12-14','voorlopig',None,gr=False)
c.execute("delete from logboek where wat like 'Ronde Z12:%'")
c.execute("insert into logboek(datum,wat) values(?,?)",(D,f'Ronde Z12: de 15 beslissingen van Rogier verwerkt (1B 2A 3B 4C 5B 6B 7C 8B 9B 10B 11B 12C 13B 14A 15C); {sum(len(x) for x in vast.values())} rijen vastgesteld, {len(verv)} vervangen, {len(W)} wrijvingen; stem in de Wortel ter beoordeling.'))
# roundtrip: lege tekst ('') wordt NULL (importeer.py leest '' als NULL); inhoudelijk gelijk
for col in ('verwijst_naar','hangt_samen_met'): c.execute(f"update canon set {col}=NULL where {col}=''")
c.execute("update open_vraag set verwijst_naar=NULL where verwijst_naar=''")
c.commit()
S=dict(nieuw=n,vastgesteld={i:v for i,v in vast.items() if v},vervangen=verv,keten={i:len(keten.get(i,())) for i in range(1,16)},treffers=treffers,wrijvingen=len(W),open=[w[0] for w in W if w[3]=='open'],canon=c.execute('select count(*) from canon').fetchone()[0],status=c.execute('select status,count(*) from canon group by status').fetchall(),integriteit=c.execute('pragma integrity_check').fetchone()[0])
json.dump(S,open('z12/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps(S,ensure_ascii=False))
