import re
VOLKEN=['aelthir','karrûk','dhurn','sael-mor','grauwen','ishvar','vathren','kluwer','myrrhen','oevrin','tharn','orrim','skerra','ves-lethi']
FASEN=[('overvloed','FASE-overvloed'),('vonk','FASE-vonk'),('brand','FASE-brand'),('noodtoestand','FASE-noodtoestand'),('ontvangst','FASE-ontvangst'),('markt','FASE-markt'),('barsten','FASE-barsten')]
def refs(s): return [x for x in (s or '').split(';') if x]
def graaf(c):
  rows=c.execute("select code,categorie,verwijst_naar,techniek,tijdperk,status from canon").fetchall()
  codes={r[0] for r in rows}
  out={r[0]:[x for x in refs(r[2]) if x in codes and x!=r[0]] for r in rows}
  inn={k:0 for k in codes}
  for k,v in out.items():
    for x in v: inn[x]+=1
  broken=sum(1 for r in rows for x in refs(r[2]) if x not in codes)
  return rows,codes,out,inn,broken
def rapport(c):
  rows,codes,out,inn,broken=graaf(c)
  act=[r for r in rows if r[5] in('voorlopig','vastgesteld')]
  L=['# 18 · Crosslinks (netwerk)\n\nVerbindingen via `verwijst_naar` in canon.db. Alleen bestaande codes tellen.\n']
  L.append(f'\n- Rijen: {len(rows)} (actief {len(act)})\n- Geldige verbindingen: {sum(len(v) for v in out.values())}\n- Rijen zonder enige verbinding (in of uit): {sum(1 for k in codes if not out[k] and not inn[k])}\n- Verwijzingen naar niet-bestaande codes: {broken}\n')
  L.append('\n## Per volk\n')
  for v in VOLKEN:
    hub=[h for h in codes if re.fullmatch(f'VOLK-{re.escape(v)}(-V\\d+)?',h)]
    linked=[k for k,o in out.items() if any(h in o for h in hub)]
    cats={}
    for k in linked: 
      cat=next(r[1] for r in rows if r[0]==k); cats[cat]=cats.get(cat,0)+1
    L.append(f'\n### {v} ({len(linked)} rijen verwijzen naar {", ".join(sorted(hub))})\n- '+', '.join(f'{a} {b}' for a,b in sorted(cats.items(),key=lambda x:-x[1]))+'\n- Codes: '+', '.join(sorted(linked)[:80])+(' …' if len(linked)>80 else '')+'\n')
  L.append('\n## Per technologie\n')
  for t in ['gave','metaal','bio','zegelsteen']:
    hub='TECHNO-'+t; linked=[k for k,o in out.items() if hub in o]
    L.append(f'- **{t}**: {len(linked)} rijen verwijzen naar {hub}; {inn.get(hub,0)} inkomend.\n')
  L.append('\n## Per fase\n')
  for n,h in FASEN:
    linked=[k for k,o in out.items() if h in o]
    L.append(f'- **{n}** ({h}): {len(linked)} rijen.\n')
  L.append('\n## Knooppunten (meeste inkomende verbindingen)\n')
  for k,v in sorted(inn.items(),key=lambda x:-x[1])[:30]: L.append(f'- {k}: {v}\n')
  return ''.join(L)
