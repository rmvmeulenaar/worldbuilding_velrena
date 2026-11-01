import sqlite3,sys,json,re,collections
def m(p):
  c=sqlite3.connect(p);q=lambda s,*a:c.execute(s,a).fetchall();L="status in('vastgesteld','voorlopig')"
  cols=[r[1] for r in q('pragma table_info(canon)')];vp=[r[1] for r in q('pragma table_info(verhaal_profiel)')];iv=[r[1] for r in q('pragma table_info(ideeen_verwerking)')]
  o={}
  o['1 Kern zonder bron (levend)']=q(f"select count(*) from canon where draagkracht='Kern' and {L} and coalesce(bron,'onbekend')='onbekend'")[0][0]
  if 'herkomst_laag' in cols:
    for d in('Kern','Structuur','Kleur'): o['2 lagen '+d]=dict(q(f"select coalesce(herkomst_laag,'-'),count(*) from canon where draagkracht=? and {L} group by 1",d))
  else: o['2 lagen']='geen kolom (vóór Z38: alleen bron ja/nee)'; o['2 bron ja/nee Kern']=dict(q(f"select bron!='onbekend',count(*) from canon where draagkracht='Kern' and {L} group by 1"))
  P=[r[0] for r in q("select premisse from verhaal_profiel where premisse is not null and premisse not like 'geen premisse%'"+(" and coalesce(vervangen_door,'')=''" if 'vervangen_door' in vp else ''))]
  def tg(s): w=re.findall(r'\w+',re.sub(r'\(.*?\)','',s.lower()));return {tuple(w[i:i+3]) for i in range(len(w)-2)}
  T=[tg(x) for x in P];mx=0
  for i in range(len(T)):
    for j in range(i+1,len(T)):
      if T[i] and T[j]: mx=max(mx,len(T[i]&T[j])/min(len(T[i]),len(T[j])))
  o['3 premissen (levend profiel)']=len(P);o['4 max gedeelde 3-grepen tussen premissen']=round(mx,2)
  o['5 premissen met sjabloonmarker']=sum(bool(re.search(r'staat in de weg|In de weg:|houdt dat tegen|zet door, tegen de prijs',x)) for x in P)
  o['6 ideeën zonder fase']=q("select count(*) from ideeen_verwerking where fase is null or fase=''")[0][0]
  k='uitslag_z38' if 'uitslag_z38' in iv else 'uitslag'
  o['7 ent-klaar ideeën']=q(f"select count(*) from ideeen_verwerking where {k}='ent-klaar'")[0][0]
  ca=[r[1] for r in q('pragma table_info(competentie_antwoord)')]
  if 'regio' in ca: o['8 mens 801 beantwoord per regio']={r:f'{n}/54' for r,n in q("select regio,count(distinct vraag_code) from competentie_antwoord where volk='mens' and fase_nr=801 group by 1")}
  else: o['8 mens 801 beantwoord']=q("select count(distinct vraag_code) from competentie_antwoord where volk='mens' and fase_nr=801")[0][0]
  o['open wrijvingen']=q("select count(*) from wrijving where status='open'")[0][0]
  return o
print(json.dumps({'voor':m(sys.argv[1]),'na':m(sys.argv[2])},ensure_ascii=False,indent=1))
