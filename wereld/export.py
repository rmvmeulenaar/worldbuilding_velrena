import sqlite3
c=sqlite3.connect("canon.db")
# Ronde Z30: regels bovenaan, Kern apart, ideeënbank in ideeenbank.md, archief onderaan. Tekst = feit_schoon (origineel in kolom feit).
H=c.execute("select tekst from handleiding where code='HANDL-Z30-2'").fetchone()
L=['# Canon Velmara\n','> **Bij twijfel wint het verhaal, behalve bij Kern.**','> '+(H[0] if H else ''),'> **veilig_18plus = 0 betekent alleen dat er geen standaardlabel in de rij stond; het betekent nooit dat de grens hier niet geldt. De harde lijnen gelden voor elke rij.**','> Draagkracht: Kern = alleen via BESLUIT; Structuur = mag schuiven met een wrijving-rij; Kleur = vrij. Twee Kleur-rijen die botsen: het verhaal wint, geen wrijving. Catalogi staan in ideeenbank.md. Zie SCHEMA.md. Handmatige draagkracht (draagkracht_handmatig) wint altijd. Ankers (bron van waarheid): tabel anker. Tests: python3 toets.py.\n']
def item(o,f,s,r,h,ro,te,dk,vd=None):
  return f'- **{o}** ({s}, {dk}, ronde {ro}, techniek: {te or "-"}): {f}'+(f' → vervangen door {vd}' if vd else '')+f'\n  - Reden: {r} | Hangt samen met: {h}'
Q='select onderwerp,feit_schoon,status,reden,hangt_samen_met,ronde,techniek,draagkracht,vervangen_door from canon where '
L.append('\n## KERN\n')
for x in c.execute(Q+"draagkracht='Kern' order by id"): L.append(item(*x))
seen=[]
for (k,) in c.execute("select categorie from canon order by id"):
  if k not in seen: seen.append(k)
L.append('\n# Levende canon (Structuur en Kleur)\n')
for k in seen:
  rs=c.execute(Q+"categorie=? and draagkracht!='Kern' and coalesce(ideeenbank,0)=0 and status in('vastgesteld','voorlopig') order by id",(k,)).fetchall()
  if rs: L.append(f'\n## {k}\n'); L+= [item(*x) for x in rs]
L.append('\n## Wrijvingen\n')
for i,t,d,b,ty,s in c.execute('select id,titel,delen_die_botsen,beschrijving,type,status from wrijving'): L.append(f'{i}. **{t}** [{ty}, {s}] ({d}): {b}')
L.append('\n## Open vragen\n')
for i,v,w,s,a in c.execute('select id,vraag,waarom_belangrijk,status,antwoord from open_vraag'): L.append(f'{i}. {v} [{s}] — {w}'+(f' — {a}' if a else ''))
L.append('\n# Archief (vervallen en vervangen; niet gebruiken)\n')
for x in c.execute(Q+"status in('vervallen','voorlopig, vervangen') order by id"): L.append(item(*x))
open('canon.md','w').write('\n'.join(L)+'\n')
I=['# Ideeënbank Velmara (Kleur, geen canon)\n','Catalogi en skeletten (KINKFUNC, KINK, ACTIE, HORROR, COMEDY, SAW, NERD, ROMANCE, ROM, HELD, THRL, HAAK, VERLEID, DEGEN, OORLOG en verwante categorieën). Inspiratie; het verhaal wint altijd.\n']
for k in seen:
  rs=c.execute(Q+"categorie=? and ideeenbank=1 and status in('vastgesteld','voorlopig') order by id",(k,)).fetchall()
  if rs: I.append(f'\n## {k}\n'); I+=[item(*x) for x in rs]
open('ideeenbank.md','w').write('\n'.join(I)+'\n')
for t in ['canon','wrijving','open_vraag','logboek','handleiding','verwijzing','historie','veiligheid_varianten','anker','naam_markering','toets_uitzondering','wijziging','schema_versie']: print(t,c.execute(f'select count(*) from {t}').fetchone())
