"""Z34 meting. Gebruik: python3 z34/meet.py [db] [uit.json]"""
import sqlite3,sys,os,json,collections,re,statistics
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from herhaling import *
DB=sys.argv[1] if len(sys.argv)>1 else 'canon.db';c=sqlite3.connect(DB)
R=c.execute("select code,categorie,feit_schoon,draagkracht,coalesce(ideeenbank,0),ronde from canon where status in('vastgesteld','voorlopig') order by id").fetchall()
T={r[0]:r for r in R};rows=[(r[0],r[2]) for r in R]
F=families(rows);inF={x for v in F.values() for x in v}
canonR=[r for r in R if r[4]==0];inF_canon=[r for r in canonR if r[0] in inF]
uit={'levend':len(R),'families':len(F),'rijen_in_familie':len(inF),'aandeel_in_familie':round(len(inF)/len(R),4),
 'canon_niet_ideeenbank':len(canonR),'canon_in_familie':len(inF_canon),'aandeel_canon_in_familie':round(len(inF_canon)/max(1,len(canonR)),4)}
# (a) per categorie
pc={}
for cat in sorted({r[1] for r in R}):
  rr=[r for r in R if r[1]==cat];L=[len((r[2] or '').split()) for r in rr]
  op=collections.Counter(' '.join((r[2] or '').split()[:5]) for r in rr).most_common(1)[0]
  pc[cat]={'n':len(rr),'in_familie':sum(r[0] in inF for r in rr),'aandeel':round(sum(r[0] in inF for r in rr)/len(rr),3),
   'top_opening5':op,'lengte_mediaan':statistics.median(L),'lengte_cv':round(statistics.pstdev(L)/max(1,statistics.mean(L)),2)}
uit['per_categorie']=pc
uit['categorieen_boven_drempel']=sorted([k for k,v in pc.items() if v['aandeel']>CAT_DREMPEL and v['n']>=10])
uit['top20']=[(s,len(v),v[:3],collections.Counter(T[x][1] for x in v).most_common(3),(T[v[0]][2] or '')[:160]) for s,v in sorted(F.items(),key=lambda x:-len(x[1]))[:20]]
# (b) near-dups
nd=near_dups(rows);binnen=sum(T[a][1]==T[b][1] for a,b,_ in nd)
uit['near_dup_paren']=len(nd);uit['near_dup_binnen_cat']=binnen;uit['near_dup_tussen_cat']=len(nd)-binnen
uit['near_dup_rijen']=len({x for a,b,_ in nd for x in (a,b)});uit['near_dup_voorbeelden']=sorted(nd,key=lambda x:-x[2])[:8]
# (c) catalogusblokken per prefix
pref=collections.defaultdict(list)
for r in R: pref[re.split(r'[-_]',r[0])[0]].append(r[0])
uit['prefix']={p:{'n':len(v),'in_familie':sum(x in inF for x in v),'grootste_fam':max((sum(x in set(fv) for x in v) for fv in F.values()),default=0)} for p,v in pref.items() if p in('KINKFUNC','KINK','ACTIE','HORROR','COMEDY','ROMANCE','HELD','SAW','NERD','DEGEN','THRL','VERLEID','OORLOG','HAAK','FASE','GESCH','TOESTAND','PERS','ZINT','VOOR','INTR','VOLK','ONTWAAK','TECH','DAG')}
# (d) boog en personage
B=c.execute('select code,geslacht_hoofdpersoon,leeftijd_hoofdpersoon,romance,erotische_sleutelscene,terugkerend_motief,noodoplossing,vorm,toon,afloop from boog order by id').fetchall()
fam=lambda m:(m or '').split('/')[0].strip()
mot=collections.Counter(fam(b[5]) for b in B)
prof=collections.Counter((b[1],'21-35' if (b[2] or 0) in range(21,36) else 'anders',b[3],b[4],fam(b[5])) for b in B)
uit['boog']={'n':len(B),'motief':dict(mot),'register_bogen':mot.get('register',0),'profiel_gedeeld_bogen':sum(v for v in prof.values() if v>1),
 'vorm_onbekend':sum(1 for b in B if (b[7] or 'onbekend')=='onbekend'),'vorm_dubbel':sum(v for v in collections.Counter(b[7] for b in B if b[7] and b[7]!='onbekend').values() if v>1),
 'toon_dubbel':sum(v for v in collections.Counter(b[8] for b in B if b[8] and b[8]!='onbekend').values() if v>1),
 'nood_verdeling':dict(collections.Counter(b[6] for b in B)),'aangrenzend_zelfde_profiel':sum(1 for x,y in zip(B,B[1:]) if (x[1],x[3],x[4],fam(x[5]))==(y[1],y[3],y[4],fam(y[5])))}
P=c.execute('select code,soort_fout,status from personage').fetchall()
uit['personage']={'n':len(P),'profiel_geen_personage':sum(1 for p in P if (p[2] or '').startswith('profiel')),'soort_fout_dubbel':sum(v for v in collections.Counter((p[1] or '-').split(' (')[0] for p in P if p[1] and p[1]!='-').values() if v>1)}
# (e) Z29-Z33 rijen: herhaalde zinnen, namen, getallen
NZ=[r for r in R if re.search(r'Z(29|3[0-3])',r[0] or '')]
zt=collections.Counter(z for r in NZ for z in set(zinnen(r[2])))
uit['nieuw_Z29_Z33']={'n':len(NZ),'in_familie':sum(r[0] in inF for r in NZ),'zinnen_meer_dan_1x':sum(1 for v in zt.values() if v>1),
 'top_zinnen':[(z[:120],n) for z,n in zt.most_common(6) if n>1],
 'top_getallen':collections.Counter(g for r in NZ for g in set(re.findall(r'\b-?\d{2,5}\b',r[2] or ''))).most_common(8),
 'top_namen':collections.Counter(n for r in NZ for n in set(re.findall(r'\b(Ysa|Thalen|Liora|Teo|Hesta|Corran|Annike|Joris|Aukje|Nerys|Saske|Ylva|Liane|Zegel|Rekenaar|Wortel)\b',r[2] or ''))).most_common(8)}
json.dump(uit,open(sys.argv[2] if len(sys.argv)>2 else 'z34/meting.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps({k:v for k,v in uit.items() if k not in('per_categorie','top20','prefix','near_dup_voorbeelden')},ensure_ascii=False,default=str))
