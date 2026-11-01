"""Verhalengraaf: alle verhaallijnen en de knopen waaraan ze hangen.
Leest canon.db, schrijft graaf.json. Wijzigt niets in de database."""
import sqlite3, json, collections, re, sys

DB = sys.argv[1] if len(sys.argv) > 1 else 'canon.db'
UIT = sys.argv[2] if len(sys.argv) > 2 else 'graaf.json'
c = sqlite3.connect(DB)

canon = {}
for code, cat, status, tp, vd, ond, feit, fs, ib, dk in c.execute(
        "select code,categorie,status,tijdperk,vervangen_door,onderwerp,feit,feit_schoon,ideeenbank,draagkracht from canon where code is not null"):
    canon[code] = dict(cat=cat, status=status or '', tp=tp, vd=vd, ond=ond, tekst=(fs or feit or ''), ib=ib, dk=dk)
zaad = {r[0]: dict(wat=r[1], oogst=r[2], status=r[3]) for r in c.execute("select code,wat,oogst_in,status from zaadje")}
pp = {r[0]: dict(naam=r[1], volk=r[2], fase=r[3], fase_nr=r[4], rol=r[5], wil=r[6])
      for r in c.execute("select code,naam,volk,fase,fase_nr,rol,wil from personage_profiel")}

ident = {}
if c.execute("select 1 from sqlite_master where name='persoon_identiteit'").fetchone():
    ident = {a: b for a, b in c.execute('select code,persoon from persoon_identiteit') if a != b}

pnaam = dict(c.execute('select persoon,max(naam) from persoon_identiteit group by persoon')) if ident is not None and c.execute("select 1 from sqlite_master where name='persoon_identiteit'").fetchone() else {}

def dood(x):
    s = canon[x]['status']
    return 'vervangen' in s or s == 'vervallen'

def los_op(x, n=0):
    """Volg vervangen_door naar de levende opvolger. Geeft (code, toestand)."""
    if x.startswith('personage_profiel:'):
        x = x.split(':', 1)[1]
        return (x, 'ok') if x in pp or x in canon else (x, 'mist')
    if x in zaad and x not in canon:
        return x, 'ok'
    if x in pp and (x not in canon or dood(x)):
        return x, 'ok'
    if x not in canon:
        return x, 'mist'
    if n > 10:
        return x, 'lus'
    if dood(x):
        vd = (canon[x]['vd'] or '').split(';')[0].strip()
        return los_op(vd, n + 1) if vd else (x, 'doodlopend')
    return x, 'ok'

def fase_nr(tp):
    if not tp: return None
    if 'na 801' in str(tp): return 9
    m = re.match(r'\s*(\d+)', str(tp))
    if not m: return None
    v = int(m.group(1))
    return 8 if v == 801 else (9 if 'na 801' in tp else v)

ACHTERGROND = ('FASE-', 'BESLUIT-', 'REGEL-', 'EROS-GRENZEN', 'MOTOREN-', 'LIJST-', 'VERHAALTIJD-', 'JAAR:')
def soort_knoop(code):
    p = code.split('-')[0] + '-'
    if code.startswith(ACHTERGROND): return 'achtergrond'
    if p in ('PER-', 'PERS-'): return 'personage'
    if p in ('PLEK-', 'STAD-', 'REG-'): return 'plek'
    if p == 'GEB-': return 'gebeurtenis'
    if p == 'ERF-': return 'erfenis'
    if p == 'ZAAD-': return 'zaadje'
    if p == 'VOLK-': return 'volk'
    if p in ('ROMAN-', 'YSA-'): return 'roman'
    return 'wereld'

# ---- verhalen ----
VERHAAL_CAT = ('Verhaal', 'Horror', 'Comedy', 'Romantiek', 'Oorlog', 'Held', 'Actie')  # genre-skeletten tellen mee
verhalen = {}
for code, d in canon.items():
    if d['cat'] in VERHAAL_CAT and not dood(code):
        verhalen[code] = dict(code=code, bron='canon', soort=code.split('-')[0],
                              fase=d['tp'], fnr=fase_nr(d['tp']), status=d['status'],
                              idee=d['ib'] or 0, dk=d['dk'], tekst=d['tekst'][:600], titel=d['ond'])
boog = {r[0]: r[1:] for r in c.execute("select code,synopsis_code,hoofdpersoon,vorm,toon,afloop,haak,verteller from boog")}
for bc, (syn, hp, vorm, toon, afloop, haak, vert) in boog.items():
    tgt, _ = los_op(syn) if syn else (bc, 'ok')
    if tgt in verhalen:
        verhalen[tgt].update(boog=bc, hp=hp, vorm=vorm, toon=toon, afloop=afloop, haak=haak, verteller=vert)
cols = [r[1] for r in c.execute('pragma table_info(verhaal_profiel)')]
for row in c.execute("select * from verhaal_profiel where status='voorlopig'"):
    r = dict(zip(cols, row))
    verhalen[r['code']] = dict(code=r['code'], bron='profiel', soort='PROFIEL', fase=r['fase'], fnr=fase_nr(r['fase']),
        status='voorlopig', idee=r['ideeenbank'] or 0, tekst=r['premisse'] or '', titel=r['positie'] + ' · ' + (r['genre'] or ''),
        positie=r['positie'], genre=r['genre'], volk=r['volk'], vorm=r['vorm'], afloop=r['afloop'],
        leeftijd=r['leeftijd'], instemming=r['instemming'], dwang=r['dwang_label'], erotiek=r['g_erotiek'],
        g={k[2:]: r[k] for k in cols if k.startswith('g_')}, seriewaarde=r['seriewaarde'])

# ---- randen ----
rand = collections.defaultdict(set)
oud = collections.defaultdict(list)
fout = collections.defaultdict(list)
def koppel(v, b):
    t, s = los_op(b)
    if s == 'ok' and t != b and not (b.startswith('personage_profiel:') or t == ident.get(b)):
        oud[v].append([b, t])
    t = ident.get(t, t)
    if s == 'ok':
        if t != v: rand[v].add(t)
    else:
        fout[v].append(f'verwijst naar {b} ({s})')

for a, s, b in c.execute("select van_code,soort,naar_code from relatie where soort!='vervangt'"):
    if a in verhalen: koppel(a, b)
for row in c.execute("select code,drager,erf_code,zaadje_code,wereldregel_code,premisse_codes from verhaal_profiel where status='voorlopig'"):
    for f in row[1:]:
        for b in (f or '').split(';'):
            b = b.strip()
            if b: koppel(row[0], b)

# wereldgraad van elke knoop: hoeveel rijen in de hele database ernaar of ervandaan wijzen
wgraad = collections.Counter()
for a, b in c.execute("select van_code,naar_code from relatie where soort!='vervangt'"):
    x, y = los_op(a)[0], los_op(b)[0]
    wgraad[ident.get(x, x)] += 1; wgraad[ident.get(y, y)] += 1

knoop_verhalen = collections.defaultdict(set)
for v, ks in rand.items():
    for k in ks: knoop_verhalen[k].add(v)

def info(k):
    if k in verhalen: return dict(soort='verhaal')
    if k in pp:
        p = pp[k]; return dict(soort='personage', naam=p['naam'] or pnaam.get(k), fase=p['fase'], fnr=p['fase_nr'], tekst=f"{p['rol'] or ''} · wil: {p['wil'] or '?'}", volk=p['volk'])
    if k in zaad and k not in canon:
        z = zaad[k]; return dict(soort='zaadje', naam=k, tekst=f"{z['wat']} · oogst: {z['oogst']} · {z['status']}")
    d = canon.get(k)
    if d: return dict(soort=soort_knoop(k), naam=d['ond'] or k, fase=d['tp'], fnr=fase_nr(d['tp']), tekst=d['tekst'][:300])
    return dict(soort=soort_knoop(k), naam=k)

knopen = {}
for k in knoop_verhalen:
    if k in verhalen: continue
    i = info(k); i['wgraad'] = wgraad[k]; i['n'] = len(knoop_verhalen[k]); knopen[k] = i

# ---- toetsen ----
def deelknopen(v):
    return {k for k in rand[v] if (k in verhalen) or knopen.get(k, {}).get('soort') != 'achtergrond'}
buren = collections.defaultdict(set)
for k, vs in knoop_verhalen.items():
    if k in knopen and knopen[k]['soort'] == 'achtergrond': continue
    if len(vs) > 80 and knopen.get(k, {}).get('soort') != 'personage': continue   # hub: verbindt alles, zegt niets (personen tellen altijd)
    for v in vs:
        buren[v] |= vs - {v}
for v in verhalen:
    for k in rand[v]:
        if k in verhalen: buren[v].add(k); buren[k].add(v)

# afstand tot 801: hoeveel verhaal-stappen tot een verhaal in 801
from collections import deque
afst = {}
q = deque()
for v, d in verhalen.items():
    if d['fnr'] == 8: afst[v] = 0; q.append(v)
while q:
    v = q.popleft()
    for w in buren[v]:
        if w not in afst: afst[w] = afst[v] + 1; q.append(w)

signaal = collections.defaultdict(list)
UITZ = set()
if c.execute("select 1 from sqlite_master where name='toets_uitzondering'").fetchone():
    UITZ = {(a_, ident.get(b_, b_)) for a_, b_ in c.execute("select code,detail from toets_uitzondering where toets='graaf_tijd'")}
for v, d in verhalen.items():
    if not deelknopen(v): signaal[v].append('zwevend: hangt alleen aan een besluit, nog geen personage, plek of gebeurtenis')
    elif not buren[v]: signaal[v].append('deelt geen knoop met een ander verhaal (eiland)')
    if v not in afst: signaal[v].append('geen pad naar 801: laat geen spoor na in het heden')
    if d['bron'] == 'profiel':
        if d.get('leeftijd') is not None and d['leeftijd'] < 18 and (d.get('erotiek') or 0) > 0:
            fout[v].append('HARDE LIJN: hoofdpersoon onder 18 met erotiekscore')
        if (d.get('instemming') or '') == 'nee' and not d.get('dwang'):
            fout[v].append('dwang zonder label')
    # personage uit een ver andere fase, zonder dat het verhaal over erfenis gaat
    if d['fnr'] is not None:
        for k in rand[v]:
            kn = knopen.get(k)
            if kn and kn['soort'] == 'personage' and kn.get('fnr') is not None and (v, k) not in UITZ:
                try: kf = int(kn['fnr'])
                except: continue
                kf = 8 if kf == 801 else kf
                if abs(kf - d['fnr']) >= 2 and d['fnr'] != 9:
                    signaal[v].append(f"personage {kn.get('naam') or k} hoort in fase {kn.get('fase')}")
    d['afst801'] = afst.get(v)
    d['knopen'] = sorted(rand[v]); d['buren'] = len(buren[v])
    d['oud'] = oud[v]; d['fout'] = fout[v]; d['signaal'] = signaal[v]

# ---- entpunten ----
entpunten = []
for k, i in knopen.items():
    if i['soort'] in ('achtergrond', 'roman'): continue
    score = i['wgraad'] / (1 + i['n'])
    if i['n'] <= 2 and i['wgraad'] >= 6:
        entpunten.append(dict(code=k, naam=i.get('naam'), soort=i['soort'], fase=i.get('fase'), wgraad=i['wgraad'], n=i['n'], score=round(score, 1)))
# knopen in de wereld die nog géén verhaal dragen
for k, g in wgraad.most_common():
    if k in knoop_verhalen or k in verhalen or g < 10: continue
    i = info(k)
    if i['soort'] in ('achtergrond', 'roman', 'verhaal'): continue
    if k not in canon and k not in pp and k not in zaad: continue
    if k in canon and dood(k): continue
    entpunten.append(dict(code=k, naam=i.get('naam'), soort=i['soort'], fase=i.get('fase'), wgraad=g, n=0, score=float(g)))
entpunten.sort(key=lambda e: -e['score'])
zaad_open = [dict(code=r[0], wat=r[1], in_=r[2], oogst=r[3]) for r in c.execute("select code,wat,geplant_in,oogst_in from zaadje where status like 'open%'")]
gaten = [dict(fase=r[0], positie=r[1], canon=r[2], idee=r[3]) for r in c.execute("select * from v_positie_dekking")]

# hard-lines in alle verhalen tellen
out = dict(verhalen=list(verhalen.values()), knopen=knopen, entpunten=entpunten[:400], zaadjes=zaad_open, posities=gaten,
           totaal=dict(verhalen=len(verhalen), knopen=len(knopen), randen=sum(len(x) for x in rand.values()),
                       oud=sum(len(x) for x in oud.values()), fout=sum(1 for v in verhalen if fout[v]),
                       signaal=sum(1 for v in verhalen if signaal[v]),
                       bereik801=sum(1 for v in verhalen if v in afst)))
json.dump(out, open(UIT, 'w'), ensure_ascii=False)
print(json.dumps(out['totaal'], ensure_ascii=False))
print('afstand tot 801:', collections.Counter(afst.get(v, 'geen') for v in verhalen))
print('fout-soorten:', collections.Counter(f.split(' (')[0][:50] for v in verhalen for f in fout[v]).most_common(8))
print('signaal-soorten:', collections.Counter(s[:40] for v in verhalen for s in signaal[v]).most_common(8))
print('entpunten top:', [(e['naam'], e['soort'], e['wgraad'], e['n']) for e in entpunten[:12]])
