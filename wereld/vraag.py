#!/usr/bin/env python3
"""Hulpscript (Z30, uitgebreid Z31).
python3 vraag.py kern | open | ideeen [woord] | tel | code <CODE> | zoek <woord> [kern|structuur|kleur]
                 impact <CODE> | anker-waarde [sleutel] | kopieen [n] | herkomst <CODE> | mal | personage [naam] | zaadjes | regels | wie-leunt-op <CODE> [diepte]   (wat breekt als ik deze rij verander: rijen die ernaar verwijzen, recursief)
                 anker | toets               [DB=pad]
  Z36:          bedenk <fase> <n> [--profiel naam] [--run R --bewaar] | pareto <fase> <n> [--profiel] | volgende | gewicht swing a:10,b:40,.. [--bewaar] | gewicht paren <bestand> | afstand <A> <B> | dekking | ideeenrapport [--positie]
  Z37:          gaten <fase_nr> [n]  (rijkdomsgaten volk x domein, gewogen naar vraag)
  Z35:          schrijfpakket <BOOG>  (verplicht vertrekpunt voor wie schrijft, HANDL-Z35-2) | rijm | tijdlijn <PER-code> | keuzes [soort]"""
import sqlite3,sys,os,subprocess
DB=os.environ.get('DB','canon.db');c=sqlite3.connect(DB);a=sys.argv[1:] or ['tel']
p=lambda rs:[print(' | '.join('' if x is None else str(x) for x in r)) for r in rs]
if a[0] in('bedenk','pareto','volgende','gewicht','afstand','dekking','ideeenrapport'):
  sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'z36'));import machine_cli;machine_cli.CMD[a[0]](c,a)
elif a[0]=='intrige':  # Z39 11a.5: vraag.py intrige <complot|chantage|rivaliteit|erfwrok> [PLEK|-] [JAAR]
  sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'z39'));import intrige
  P=a[2] if len(a)>2 and a[2]!='-' else None;J=a[3] if len(a)>3 else 130
  for r in intrige.vraag(c,a[1],P,J): print(' | '.join(str(x) for x in r))
elif a[0]=='kern': p(c.execute('select code,onderwerp from v_kern order by id'))
elif a[0]=='open': p(c.execute('select soort,code,status,wat from v_open'))
elif a[0]=='ideeen':
  w=f'%{a[1]}%' if len(a)>1 else '%'
  p(c.execute('select code,categorie,onderwerp from v_ideeenbank where feit like ? or onderwerp like ? order by id limit 200',(w,w)))
elif a[0]=='tel': p(c.execute('select draagkracht,count(*) from canon group by 1'))
elif a[0]=='anker': p(c.execute('select sleutel,waarde,bron_code,toelichting from anker order by id'))
elif a[0]=='toets': sys.exit(subprocess.call([sys.executable,os.path.join(os.path.dirname(os.path.abspath(__file__)),'toets.py'),DB]+a[1:]))
elif a[0]=='code':
  p(c.execute('select code,draagkracht,draagkracht_handmatig,status,onderwerp,feit_schoon,vervangen_door from canon where code=?',(a[1],)))
  print('-> verwijst naar:',[r[0] for r in c.execute('select naar_code from verwijzing where van_code=?',(a[1],))]);print('<- genoemd door:',[r[0] for r in c.execute('select van_code from verwijzing where naar_code=?',(a[1],))])
  print('ankers met deze bron:',[r[0] for r in c.execute('select sleutel from anker where bron_code=?',(a[1],))])
elif a[0]=='wie-leunt-op':
  diep=int(a[2]) if len(a)>2 else 2;gezien={a[1]};laag=[a[1]];dk=lambda x:(c.execute('select draagkracht,status from canon where code=?',(x,)).fetchone() or ('-','(wrijving/vraag)'))
  print(f'{a[1]} ({"/".join(dk(a[1]))}); ankers: {[r[0] for r in c.execute("select sleutel from anker where bron_code=?",(a[1],))]}')
  for n in range(1,diep+1):
    nieuw=[]
    for x in laag:
      for t,v in c.execute('select distinct van_tabel,van_code from verwijzing where naar_code=?',(x,)).fetchall():
        if v not in gezien: gezien.add(v);nieuw.append(v);print(f'{"  "*n}niveau {n}: {v} [{t}, {"/".join(dk(v))}] leunt op {x}')
    laag=nieuw
  print(f'totaal {len(gezien)-1} rijen leunen (tot diepte {diep}) op {a[1]}; controleer die bij een wijziging.')
elif a[0]=='impact':
  code=a[1];dk=lambda x:(c.execute('select draagkracht,status from canon where code=?',(x,)).fetchone() or ('-','(wrijving/vraag)'))
  print(f'{code} ({"/".join(dk(code))}); ankers met deze bron: {[r[0] for r in c.execute("select sleutel from anker where bron_code=?",(code,))]}')
  rs=c.execute('select leunt,min(niveau),via from v_impact where code=? group by leunt order by 2,1',(code,)).fetchall()
  for l,n,v in rs: print(f'{"  "*n}niveau {n}: {l} [{"/".join(dk(l))}] via {v}')
  print('relaties:',c.execute("select soort,naar_code from relatie where van_code=? and soort not in('leunt_op')",(code,)).fetchall())
  print(f'totaal {len(rs)} rijen leunen op {code} (tot 2 niveaus, view v_impact).')
elif a[0]=='anker-waarde': p(c.execute('select sleutel,waarde,bron_code,levende_kopieen,afwijkend from v_anker where sleutel like ?',('%'+(a[1] if len(a)>1 else '')+'%',)))
elif a[0]=='kopieen': p(c.execute('select sleutel,code,waarde_in_rij,afwijkt,draagkracht,risico from anker_kopie order by risico desc limit ?',(int(a[1]) if len(a)>1 else 10,)))
elif a[0]=='gaten':
  sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'z37'));import rijkdom
  print('score | volk | domein | dekking | diepte | verbonden | beantwoord | vraag | bogen/profielen | personages')
  p([(f'{r[0]:.2f}',)+r[1:8]+(','.join(r[8]),r[9]) for r in rijkdom.gaten(c,int(a[1]) if len(a)>1 else 801,int(a[2]) if len(a)>2 else 20)])
elif a[0]=='herkomst': p(c.execute('select code,draagkracht,bron,bron_soort,besloten_door,besloten_op from canon where code=?',(a[1],)))
elif a[0]=='mal': p(c.execute('select code,hoofdpersoon,leeftijd_hoofdpersoon,geslacht_hoofdpersoon,romance,erotische_sleutelscene,terugkerend_motief,mal_score from v_mal'))
elif a[0]=='personage': p(c.execute('select naam,status,soort_fout,eigen_fout,voorstel from personage where naam like ?',('%'+(a[1] if len(a)>1 else '')+'%',)))
elif a[0]=='zaadjes': p(c.execute('select code,geplant_in,oogst_in,status from zaadje order by status,code'))
elif a[0]=='regels': p(c.execute('select code,niveau,status,omschrijving from regel order by id'))
elif a[0]=='schrijfpakket':
  rs=c.execute('select stap,onderdeel,code,tekst from v_schrijfpakket where boog_code=? order by stap,code',(a[1],)).fetchall()
  if not rs: sys.exit(f'geen boog {a[1]}; zie: '+', '.join(r[0] for r in c.execute('select code from boog order by id')))
  print(f'# Schrijfpakket {a[1]} (HANDL-Z35-2: schrijf alleen vanuit dit pakket; de synopsis is geen schrijfinstructie)')
  vorig=None
  for st,o,cd,t in rs:
    if o!=vorig: print(f'\n## {o}');vorig=o
    print(f'- {cd}: {t}')
elif a[0]=='rijm': p(c.execute('select volgorde,fase,beslisser,betaler,vervalst,ontdekt,schaal,erft_van,blijvende_verandering,status,voorstel from v_rijm'))
elif a[0]=='tijdlijn': p(c.execute('select jaar,leeftijd,soort,rol,regio,wil,geheim,verandert,aanname,aanname_reden from v_personage_tijdlijn where per_code=? order by jaar is null,jaar',(a[1],)))
elif a[0]=='keuzes': p(c.execute("select code,soort,draagkracht,impact,onderwerp,aanbeveling from keuze where soort like ? order by case draagkracht when 'Kern' then 0 when 'Structuur' then 1 else 2 end,impact desc",('%'+(a[1] if len(a)>1 else '')+'%',)))
elif a[0]=='zoek':
  dk=f" and draagkracht='{a[2].capitalize()}'" if len(a)>2 else ''
  p(c.execute(f"select code,draagkracht,onderwerp from v_actief where (feit like ? or onderwerp like ?){dk} limit 50",(f'%{a[1]}%',)*2))
