# Gedeelde helpers voor de gatenrondes G1-G4 (idempotent)
import sqlite3,shutil,os,re
GR=' Label: alle betrokkenen volwassen (18+); geen minderjarigen of dieren in een seksuele rol; geen seksuele inhoud met wie niet kan instemmen; donkere thema\'s gelabeld.'
class Ronde:
  def __init__(s,nr):
    s.nr=nr;s.tag=f'G{nr}'
    if not os.path.exists(f'canon_backup_G{nr}.db'): shutil.copy('canon.db',f'canon_backup_G{nr}.db')
    s.c=sqlite3.connect('canon.db');s.n=0;s.codes=[]
  def add(s,code,cat,ond,feit,reden,refs,**kw):
    s.codes.append(code)
    if s.c.execute("select 1 from canon where code=?",(code,)).fetchone(): return
    cols=['categorie','onderwerp','feit','status','reden','hangt_samen_met','ronde','code','verwijst_naar']+list(kw)
    s.c.execute(f"insert into canon({','.join(cols)}) values({','.join('?'*len(cols))})",[cat,ond,feit,'voorlopig',f'Ronde {s.tag}: '+reden,refs,s.nr+18,code,refs]+list(kw.values()));s.n+=1
  def wrij(s,t,d,b,ty):
    if s.c.execute("select 1 from wrijving where titel=?",(t,)).fetchone(): return
    m=max(int(r[0][5:]) for r in s.c.execute("select code from wrijving where code like 'WRIJ-%'"))
    s.c.execute("insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,'open',?,?)",(t,d,b,ty,f'WRIJ-{m+1:03d}',d.replace('; ',';')))
  def vraag(s,v,w,r):
    if s.c.execute("select 1 from open_vraag where vraag=?",(v,)).fetchone(): return
    m=max(int(r_[0][6:]) for r_ in s.c.execute("select code from open_vraag where code like 'VRAAG-%'"))
    s.c.execute("insert into open_vraag(vraag,waarom_belangrijk,status,code,verwijst_naar) values(?,?,'open',?,?)",(v,w,f'VRAAG-{m+1:03d}',r))
  def log(s,wat):
    if not s.c.execute("select 1 from logboek where wat like ?",(f'Ronde {s.tag}:%',)).fetchone():
      s.c.execute("insert into logboek(datum,wat) values('2026-10-30',?)",(f'Ronde {s.tag}: '+wat,))
  def klaar(s):
    s.c.commit()
    codes={r[0] for r in s.c.execute('select code from canon')}
    mis=sorted({x for (v,) in s.c.execute("select verwijst_naar from canon where ronde=?",(s.nr+18,)) for x in (v or '').split(';') if x and x not in codes})
    tot=s.c.execute("select count(*) from canon where ronde=?",(s.nr+18,)).fetchone()[0]
    print(f'{s.tag}: nieuw {s.n}, totaal in ronde {tot}, canon {len(codes)}; ontbrekende verwijzingen: {mis}')
