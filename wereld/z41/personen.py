"""Z41: willekeurige personen uit de wereld trekken en de wereld laten schiften (quality-diversity, MAP-Elites).
Begint bij 801 (de hoofdlijn als anker) en werkt later naar achteren.
Een persoon wordt samengesteld uit fragmenten van verschillende bestaande personen uit dezelfde fase (wil van de een,
geheim van een ander, rol van een derde): willekeurig, maar altijd uit materiaal dat in de wereld bestaat.
Daarna wordt hij tussen de bestaande personen gezet: tegen wie loopt hij aan? Diepte van één botsing telt zwaarder dan het aantal.
Leest canon.db, schrijft alleen een json. Niets wordt canon zonder besluit van Rogier.
Gebruik: python3 z41/personen.py [fase_nr=801] [n=2000] [seed=41801]"""
import sqlite3, random, re, json, sys, collections, math, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE = int(sys.argv[1]) if len(sys.argv) > 1 else 801
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 41000 + FASE
rnd = random.Random(SEED)
c = sqlite3.connect(os.path.join(W, 'canon.db'))

HOOFDLIJN = {'PER-liora-profiel-Z32', 'PER-liora-Z6-Z32', 'PER-teo-Z32', 'PER-aeron-profiel', 'PER-ithrael'}  # afloop ligt vast
POSITIES = ['beslisser', 'betaler', 'vervalser', 'ontdekker', 'profiteur', 'toeschouwer', 'liefde tussen posities']
STOP = set('''de het een en van in op te dat die is zijn haar hem hij zij ze er voor met als aan om door bij uit naar
niet wat wie maar ook nog dan want zo of over tot zich wordt worden heeft hebben kan kunnen moet weet weten
eigen alle alles iemand niemand iets niets zelf haar zijn hun deze dit daar hier toen nu waar elke ieder'''.split())
def tok(s):
    return {w[:-2] if w.endswith('en') and len(w) > 6 else w for w in re.findall(r"[a-zà-ÿ\-]{4,}", (s or '').lower()) if w not in STOP}

P = [dict(zip(['code', 'naam', 'volk', 'regio', 'rol', 'wil', 'durft', 'verbergt', 'geheim', 'omgeving'], r))
     for r in c.execute("select code,naam,volk,regio,rol,wil,durft,verbergt,geheim,omgeving from personage_profiel where fase_nr=?", (FASE,))]
P = [p for p in P if p['naam'] and p['wil']]
# één persoon = één bron (persoon_identiteit): tweelingcodes tellen niet dubbel
_pid = dict(c.execute('select code,persoon from persoon_identiteit'))
_gezien = set(); _P = []
for p in P:
    k_ = _pid.get(p['code'], p['code'])
    if k_ not in _gezien: _gezien.add(k_); _P.append(p)
P = _P
HOOFDNAAM = re.compile(r'Liora|Teo|Aeron|Ithrael')
VUIL = re.compile(r'Haak:|zie PER|\bfase \d|PER-|Z\d+')
def geslacht_van(s):
    w = set(re.findall(r'[a-z]+', (s or '').lower()))
    m, v = bool(w & {'zijn', 'hij', 'hem'}), bool(w & {'haar', 'ze', 'zij'})
    return 'm' if m and not v else ('v' if v and not m else None)
MANROL = re.compile(r'gaven-man|\bman\b|-man\b|broeder|zoon|vader|heer\b|koning', re.I)
VROUWROL = re.compile(r'vrouw|moeder|ster\b|zuster|dochter|meesteres|priesteres|winnares|-in\b', re.I)
for p in P:
    p['T_wil'] = tok(p['wil']); p['T_durft'] = tok(p['durft']); p['T_verb'] = tok(p['verbergt']) | tok(p['geheim'])
FOUTEN = [r[0] for r in c.execute("select distinct soort_fout from personage where soort_fout is not null")]
BEROEPEN = [r[0] for r in c.execute("select naam from beroep")]
GAVEN = [r[0] for r in c.execute("select naam from gave where code!='GAVE-Z37-ja'")]
volk_w = collections.Counter(p['volk'] for p in P); regio_w = collections.Counter(p['regio'] for p in P if p['regio'])

def kies(cnt):
    k, w = zip(*cnt.items()); return rnd.choices(k, weights=w)[0]

def frag(pool, veld, g, volk, kort=False):
    """Een fragment uit de wereld dat bij dit geslacht en dit volk kan horen. Volkseigen fragmenten komen uit het eigen volk."""
    for _ in range(60):
        d = rnd.choice(pool); t = d[veld]
        if not t or VUIL.search(t): continue
        gg = geslacht_van(t)
        if gg and gg != g: continue                       # 'dat hij...' past niet bij een vrouw, en omgekeerd
        if HOOFDNAAM.search(t) and rnd.random() < 0.85: continue   # de hoofdlijn trekt niet alles naar zich toe
        if d['volk'] not in (volk, 'mens') and rnd.random() < 0.7: continue   # vreemde volken lenen zelden
        return d, t
    return None, None

def trek(i):
    volk = kies(volk_w)
    man = rnd.random() < 0.2             # mannen zijn schaars in 801
    g = 'm' if man else 'v'
    gave = rnd.choice(GAVEN) if man and rnd.random() < 0.05 else None
    while True:
        dw, wil = frag(P, 'wil', g, volk); dv, verb = frag(P, 'verbergt', g, volk); dg, geh = frag(P, 'geheim', g, volk)
        if dw and dv and dg and len({dw['code'], dv['code'], dg['code']}) == 3: break
    for _ in range(60):
        rol = rnd.choice(BEROEPEN) if rnd.random() < 0.25 else rnd.choice(P)['rol']
        if not rol or VUIL.search(rol): continue
        if (MANROL.search(rol) and not man) or (VROUWROL.search(rol) and man): continue
        if 'gaven-man' in rol and not gave: continue
        break
    donors = [dw, dv, dg]
    return dict(id=f'K{FASE}-{i:04d}', volk=volk, regio=kies(regio_w), geslacht='m' if man else 'v',
                leeftijd=rnd.randint(19, 68), gave=gave, rol=rol, positie=rnd.choice(POSITIES), fout=rnd.choice(FOUTEN),
                wil=wil, verbergt=verb, geheim=geh, donors=[d['code'] for d in donors])

def ov(a, b):
    return len(a & b) / math.sqrt(len(a) * len(b)) if a and b else 0.0

def botsingen(k):
    Tw, Tv = tok(k['wil']), tok(k['verbergt']) | tok(k['geheim'])
    uit = []
    for p in P:
        if p['code'] in k['donors']: continue
        nabij = 1.0 if p['regio'] == k['regio'] else (0.6 if p['volk'] == k['volk'] else 0.35)
        if p['wil'] == k['wil'] or p['geheim'] == k['geheim'] or p['verbergt'] == k['verbergt']: continue  # tweeling van een bron
        riv = ov(Tw, p['T_wil']) * 0.7                 # willen hetzelfde (minder rijk dan een geheim)
        dre = ov(Tv, p['T_wil'] | p['T_durft'])        # de ander wil wat hem blootlegt
        hef = ov(Tw, p['T_verb'])                      # hij wil wat de ander verbergt
        s = nabij * (1.0 * riv + 1.5 * dre + 1.2 * hef)
        if s > 0.15:
            soort = max((riv, 'rivaal'), (dre * 1.5, 'dreiging'), (hef * 1.2, 'hefboom'))[1]
            uit.append((round(s, 3), p['code'], p['naam'], soort))
    uit.sort(reverse=True)
    return uit

def score(k):
    b = k['botsingen']
    if not b: return 0.0
    s = b[0][0] + 0.5 * (b[1][0] if len(b) > 1 else 0) + 0.15 * math.log1p(len(b))
    raakt = [x for x in b[:3] if x[1] in HOOFDLIJN]
    if raakt and k['positie'] in ('beslisser', 'betaler'):
        s *= 0.4; k['hoofdlijn'] = 'afgewaardeerd: zou de afloop van ' + raakt[0][2] + ' raken'
    elif raakt:
        k['hoofdlijn'] = 'raakt ' + raakt[0][2] + ' zonder de afloop te veranderen'
    if Tself(k): s *= 0.7                              # wil en geheim die elkaar al uitleggen: minder spanning
    return round(s, 3)

def Tself(k): return ov(tok(k['wil']), tok(k['verbergt'])) > 0.5

K = []
for i in range(N):
    k = trek(i); k['botsingen'] = botsingen(k)[:6]; k['score'] = score(k); K.append(k)

# MAP-Elites: één elite per (volk, positie)
cel = {}
for k in K:
    key = (k['volk'], k['positie'])
    if k['score'] > 0 and (key not in cel or k['score'] > cel[key]['score']): cel[key] = k
elites = sorted(cel.values(), key=lambda k: -k['score'])

# verste-punt selectie over de elites voor de leesronde (diversiteit), gewogen met score
def afst(a, b):
    return sum(a[f] != b[f] for f in ('volk', 'positie', 'regio', 'fout', 'geslacht', 'rol')) + (a['gave'] != b['gave'])
gekozen = [elites[0]]
while len(gekozen) < min(30, len(elites)):
    best = max((e for e in elites if e not in gekozen), key=lambda e: e['score'] * (1 + min(afst(e, g) for g in gekozen)))
    gekozen.append(best)

uit = dict(fase=FASE, n=N, seed=SEED, bron_personen=len(P), met_botsing=sum(1 for k in K if k['score'] > 0),
           cellen=len(cel), elites=elites, leesronde=gekozen,
           verdeling=dict(score_mediaan=sorted(k['score'] for k in K)[N // 2], score_max=elites[0]['score'] if elites else 0))
pad = os.path.join(W, 'z41', f'personen_{FASE}.json')
json.dump(uit, open(pad, 'w'), ensure_ascii=False, indent=1)
print(f"fase {FASE}: {N} getrokken uit {len(P)} bronpersonen; {uit['met_botsing']} lopen ergens tegenaan; {len(cel)} cellen gevuld; leesronde {len(gekozen)} -> {pad}")
