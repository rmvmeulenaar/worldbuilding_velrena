# Z37 D1.2: de ideeënbank opnieuw gemeten. Onbekende as = onbekend (geen gelijkheid, geen verschil). Afstand alleen over de assen
# die bij beide bekend zijn, minimaal 4 vergeleken assen; anders 'onbekend: te weinig assen'. Assen uit de rij gelezen met dezelfde
# heuristiek als Z36 (z36/ideeen.py: trefwoorden, code-prefix, tijdperk, jaar), dus niet met de hand gelezen.
import re,collections,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','z36'))
import machine as M, ideeen as I
MIN_VERGELEKEN=4;MIN_AFSTAND=3
def verwerk(c):
  FN={r[1]:r[0] for r in c.execute("select fase,volgorde from fase_rijm")}
  volken=sorted({r[0] for r in c.execute('select volk from personage_profiel where volk is not null')}|{'mens'})
  bogen=collections.defaultdict(list)
  for r in c.execute('select g.fase,'+','.join('a.'+k for k in M.ASSEN)+',a.boog_code from boog_as a join boog g on g.code=a.boog_code'): bogen[r[0]].append(dict(zip(M.ASSEN+['code'],r[1:])))
  n=collections.Counter()
  for code,tp,jaar,ft in c.execute("select code,tijdperk,jaar,feit_schoon from canon where ideeenbank=1 and status in('vastgesteld','voorlopig') order by id").fetchall():
    r=c.execute('select fase,uitslag,verbinding from ideeen_verwerking where code=?',(code,)).fetchone()
    if not r: continue
    fase,oud,links=r;t=ft or '';pre=re.match(r'[A-Z]+',code).group(0)
    p={'positie':I.zoek(I.POS,t),'genre':I.GENRE.get(pre),'volk':next((v for v in volken if v!='mens' and re.search(v.replace('û','[uû]'),t,re.I)),None),'schaal':I.zoek(I.SCH,t),'afloop':I.zoek(I.AF,t),
       'vorm':next((v for v in M.VORMEN if v!='nog niet gekozen' and re.search(r'\b'+re.escape(v)+r'\b',t,re.I)),None)}
    bek={k:v for k,v in p.items() if v}
    if oud.startswith('uitval: filter') or oud=='uitval: geen fase': u,rd,vg,dm=oud,'zelfde als Z36 (filter of fase gaat vóór afstand)',len(bek),None
    else:
      bs=bogen.get(fase,[]);vg=len(bek)
      if not bs: u,rd,dm='ent-klaar' if links else 'uitval: verbinding','geen boog in deze fase om mee te vergelijken',None
      elif vg<MIN_VERGELEKEN: u,rd,dm='onbekend: te weinig assen',f'{vg} bekende assen ({",".join(bek) or "-"}); minimaal {MIN_VERGELEKEN}',None
      else:
        ds=[(sum(1 for k,v in bek.items() if b.get(k) and v!=b[k]),sum(1 for k in bek if b.get(k)),b['code']) for b in bs]
        ds=[d for d in ds if d[1]>=MIN_VERGELEKEN] or ds
        dm,nv,dicht=min(ds)
        if dm<MIN_AFSTAND: u,rd='uitval: afstand',f'afstand {dm} op {nv} vergeleken assen tot {dicht}'
        elif not links: u,rd='uitval: verbinding',f'afstand {dm} op {nv} assen tot {dicht}, maar geen ERF-rij of zaadje geraakt'
        else: u,rd='ent-klaar',f'afstand {dm} op {nv} vergeleken assen tot {dicht}; verbonden met {links.split(";")[0]}'
    c.execute('update ideeen_verwerking set vergeleken=?,afstand_z37=?,uitslag_z37=?,reden_z37=? where code=?',(vg,dm,u,rd+' (Z37, heuristisch)',code));n[u]+=1
  return n
def rapport(c):
  rows=c.execute("""select coalesce(fase,'(geen fase)'),coalesce(positie,'-'),count(*),sum(uitslag='ent-klaar'),sum(uitslag_z37='ent-klaar'),sum(uitslag='uitval: afstand'),sum(uitslag_z37='uitval: afstand'),sum(uitslag_z37 like 'onbekend%'),sum(uitslag_z37='uitval: verbinding')
    from ideeen_verwerking group by 1,2 order by 1,2""").fetchall()
  s=['| fase | positie | instroom | ent-klaar Z36 (onbekend=gelijk) | ent-klaar Z37 | uitval afstand Z36 | uitval afstand Z37 | onbekend (<4 assen) Z37 | uitval verbinding Z37 |','|---|---|---|---|---|---|---|---|---|']
  tot=[0]*7
  for r in rows:
    s.append('| '+' | '.join(str(x) for x in r)+' |');tot=[a+(b or 0) for a,b in zip(tot,r[2:])]
  s.append('| **totaal** | | '+' | '.join(str(x) for x in tot)+' |')
  return '\n'.join(s)
