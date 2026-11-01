import sqlite3,random,collections,re,json
c=sqlite3.connect('canon.db')
# keuzelijst
L=['# Keuzelijst Z36: wat Rogier nog moet beslissen','','Alleen open punten. Per punt: citaat (met code) en aanbeveling met reden. Herkomstpunten: kandidaat-bronnen zijn heuristisch gevonden (verwijzingen), niet met de hand gelezen.','']
rows=c.execute("select code,soort,onderwerp,aanbeveling,citaat,draagkracht,impact from keuze where status='open' order by case soort when 'keuzepunt' then 0 when 'wrijving' then 1 else 2 end,case draagkracht when 'Kern' then 0 when 'Structuur' then 1 else 2 end,impact desc").fetchall()
nieuw=[('WRIJ-Z36-1',),('WRIJ-Z36-2',),('WRIJ-Z36-3',)]
L.append('## Nieuw in Z36 (wrijvingen uit stap 0)\n')
for (w,) in nieuw:
  t,b=c.execute('select titel,beschrijving from wrijving where code=?',(w,)).fetchone()
  L.append(f'### {w}: {t}\n{b}\n')
cur=None
for code,soort,ond,aanb,cit,dk,imp in rows:
  if soort!=cur: L.append(f'## {soort}\n');cur=soort
  L.append(f'### {code} ({dk}, impact {imp}): {ond}\n- Citaat: {cit}\n- {aanb}\n')
open('keuzelijst_Z36.md','w').write('\n'.join(L));open('z36/keuzelijst_Z36.md','w').write('\n'.join(L))
print('keuzelijst: open punten',len(rows),'+3 wrijvingen; "nog geen aanbeveling":',sum('nog geen aanbeveling' in (r[3] or '').lower() for r in rows),'; zonder citaat:',sum(not r[4] for r in rows))
# wijzigingen
W=c.execute("select code,soort,veld,oud,nieuw from wijziging where ronde='Z36'").fetchall()
tab=collections.Counter()
for code,s,v,o,n in W:
  t=v.split('.')[0] if v else 'canon';tab[(t if t not in('status',) else 'canon',s)]+=1
L=['# Wijzigingen Z36','','Bron: tabel wijziging (ronde Z36) en tellingen van de nieuwe tabellen. Niets verwijderd.','','| tabel | toegevoegd (rijen) | vervangen (rijen) | gewijzigd (veldwijzigingen) |','|---|---|---|---|']
tabs=sorted({t for t,_ in tab})
for t in tabs: L.append(f"| {t} | {tab[(t,'toegevoegd')]} | {tab[(t,'vervangen')]} | {tab[(t,'gewijzigd')]} |")
for t in ('verhaal_as','verhaal_profiel','doel','doelprofiel','gewichtset','ideeen_verwerking','lezersdata','toets_uitzondering'):
  n=c.execute(f'select count(*) from {t}').fetchone()[0] if t!='toets_uitzondering' else c.execute("select count(*) from toets_uitzondering where reden like 'overgedragen van de FASE-OVERZICHT%'").fetchone()[0]
  L.append(f'| {t} (nieuwe rijen, tabel nieuw of buiten wijziging) | {n} | 0 | 0 |')
L.append('| personage_profiel (afgeleid, elke bouw opnieuw) | %d | 0 | 0 |'%c.execute('select count(*) from personage_profiel').fetchone()[0])
L+=['','## 10 willekeurige voorbeelden (seed 36), oud en nieuw','']
rng=random.Random(36)
for code,s,v,o,n in rng.sample(W,10):
  if s=='toegevoegd' and (v in('canon','wrijving','zaadje','keuze')):
    t={'canon':'select feit from canon where code=?','wrijving':'select beschrijving from wrijving where code=?','zaadje':'select wat from zaadje where code=?','keuze':'select aanbeveling from keuze where code=?'}[v]
    n=(c.execute(t,(code,)).fetchone() or [n])[0]
  L.append(f'- **{code}** ({s}, {v}):\n  - oud: {(o or "(leeg)")[:400]}\n  - nieuw: {(n or "")[:400]}')
# twee vaste voorbeelden die elke lezer wil zien
for oud,nw in (('ORIGIN-10','ORIGIN-10-Z36'),('VERHAAL-fase2-Z35','VERHAAL-fase2-Z36')):
  a=c.execute('select feit from canon where code=?',(oud,)).fetchone()[0];b=c.execute('select feit from canon where code=?',(nw,)).fetchone()[0]
  L.append(f'- **{oud} → {nw}** (vervangen):\n  - oud: {a[:500]}\n  - nieuw: {b[:500]}')
open('wijzigingen_Z36.md','w').write('\n'.join(L)+'\n');open('z36/wijzigingen_Z36.md','w').write('\n'.join(L)+'\n')
print('\n'.join(L[:20]))
