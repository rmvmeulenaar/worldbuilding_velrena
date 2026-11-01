# Z37 D1: seriewaarde en premisse opnieuw voor bestaande profielen; seriewaarde-test; ideeënbank opnieuw (onbekend = onbekend).
import re,collections,sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','z36'))
import machine as M
def herbereken(c):
  n=collections.Counter()
  for (fase,) in c.execute('select distinct fase from verhaal_profiel').fetchall():
    w=M.Wereld(c,fase)
    cols=[r[1] for r in c.execute('pragma table_info(verhaal_profiel)')]
    for row in c.execute('select * from verhaal_profiel where fase=?',(fase,)).fetchall():
      p=dict(zip(cols,row));oud=(p['seriewaarde'],p['premisse'])
      geraakt=[x for x in (p.get('erf_code'),p.get('zaadje_code'),p.get('wereldregel_code'),p.get('drager')) if x]
      d=[x for x in geraakt if x in w.H];b=[x for x in geraakt if x in w.buur]
      sw,rd=(1.0,f'direct: {d[0]} ({w.H[d[0]]})') if d else ((0.6,f'via relatie: {b[0]} - {w.buur[b[0]][0]} ({w.buur[b[0]][1]})') if b else (0.0,'raakt geen hoofdlijnrij (ook niet via een relatie)'))
      pr,pc=M.premisse(c,p)
      if not pr:  # Z37: drager zonder Wil -> opnieuw kiezen onder dragers met een Wil (zelfde volk en leeftijdsband)
        nd=M.kies_drager(w,p,(p.get('hoofdpersoon') or '|').split('|')[0])
        if nd and nd!=p.get('drager'):
          q=dict(p,drager=nd);pr2,pc2=M.premisse(c,q)
          if pr2: c.execute('update verhaal_profiel set drager=? where code=?',(nd,p['code']));n['drager opnieuw gekozen']+=1;p=q;pr,pc=pr2,pc2
      if (sw,pr)!=oud or p.get('seriewaarde_reden')!=rd:
        c.execute('update verhaal_profiel set seriewaarde=?,seriewaarde_reden=?,premisse=?,premisse_codes=? where code=?',(sw,rd,pr,pc,p['code']));n['bijgewerkt']+=1
      n[f'sw={sw}']+=1;n['met premisse' if pr else 'zonder premisse']+=1
  return n
def test_seriewaarde(c):
  """Een profiel dat MOET scoren (zaadje ZAAD-Z36-h32-protocol, direct) en een dat via een relatie moet scoren; plus een dat 0 moet geven."""
  out=[];ok=True
  w=M.Wereld(c,'0')
  basis={'fase':w.fase,'positie':'beslisser','genre':'thriller','schaal':'stad','volk':'mens','vorm':'dagboek','afloop':'komt uit','hoofdpersoon':'26-40|v','leeftijd':30,'heat':0}
  for naam,extra,verwacht in (('direct (zaadje Stille Modus h32)',{'zaadje_code':'ZAAD-Z36-h32-protocol','erf_code':'ERF-voortijd'},1.0),
                              ('via relatie (buur van de hoofdlijn)',{'zaadje_code':None,'erf_code':None,'drager':next(iter(sorted(x for x in w.buur if x.startswith('PER-'))),None)},0.6),
                              ('geen hoofdlijn',{'zaadje_code':None,'erf_code':None,'drager':None,'wereldregel_code':None},0.0)):
    p=dict(basis,**extra);p.setdefault('wereldregel_code',None);M.scores(w,p)
    goed=abs(p['seriewaarde']-verwacht)<1e-9;ok&=goed
    out.append(f"{'OK ' if goed else 'FOUT'} {naam}: seriewaarde {p['seriewaarde']:.2f} (verwacht {verwacht:.2f}); {p['seriewaarde_reden']}")
  return ok,out
