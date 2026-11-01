#!/usr/bin/env python3
"""Gebruik: python3 scene.py CODE [CODE...]  -> scene_pakket.md (wereldkern + onderdelen + 1 niveau verwijzingen + wrijvingen)."""
import sys,os,importlib.util,contextlib,io
D=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('g',os.path.join(D,'genereer.py'));g=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(g)
codes=sys.argv[1:]
onb=[x for x in codes if x not in g.by]
if onb: sys.exit('Onbekende codes: '+', '.join(onb))
def refs(x): return [y for y in (g.by[x]['verwijst_naar'] or '').split(';') if y in g.by]
lvl1=[]
for x in codes:
  for y in refs(x):
    if y not in codes and y not in lvl1: lvl1.append(y)
alle=set(codes)|set(lvl1)
out=[open(os.path.join(g.B,'00_WERELDKERN.md')).read(),'\n# Gevraagde onderdelen\n']+[g.render(x) for x in codes]
out+=['\n# Verwijzingen (één niveau)\n']+[g.render(y) for y in lvl1]
wr=[r for r in g.c.execute('select code,titel,type,beschrijving,verwijst_naar from wrijving') if set((r[4] or '').split(';'))&set(codes)]
out+=['\n# Relevante wrijvingen\n']+[f'- **{a} {b}** ({t}): {d}' for a,b,t,d,_ in wr]
open(os.path.join(D,'scene_pakket.md'),'w').write('\n'.join(out)+'\n')
print(f'scene_pakket.md: {len(codes)} gevraagd, {len(lvl1)} verwijzingen, {len(wr)} wrijvingen')
