# Verliessimulatie na 801 (ronde Z44). Per wezen wanneer het zeldzaam (P<0.5), legende (P<0.1) en verdwenen (P<0.01) wordt,
# Monte Carlo over de bandbreedtes in tijd/wezens.yaml. De tijdperken na 801 eindigen als hun groep legende is geworden.
# Daarna het anker op de aarde (ABC met afwijzing): waar ligt 801 in jaren BP, gegeven laag water, Amerika en schrift.
# Fantasie, aannemelijk gemaakt met kennis; de getallen beslissen, niet de wens. Uitvoer: tijd/uitkomst.json en tijd/verlies.md.
import json, math, os, random, statistics, yaml
H = os.path.dirname(os.path.abspath(__file__)); random.seed(801)
P = yaml.safe_load(open(os.path.join(H, 'wezens.yaml'))); W = P['wezens']; A = P['aarde']
N = 20000; DREMPEL = {'zeldzaam': 0.5, 'legende': 0.1, 'verdwenen': 0.01}
GROEPEN = ['ja', 'volken', 'helden', 'vertrek', 'mensen']
u = lambda ab: random.uniform(*ab)

def tijd(w, x, h):
    m = w['model']
    if m == 'generatie': return w['gen'] * math.log(x) / math.log(w['_f'])
    if m == 'steen': return h * (-math.log2(x)) / w['_d']
    if m == 'demo': return math.log(x) / w['_r']
    return math.inf

runs = []
for _ in range(N):
    h = u(P['steen_halfwaarde']); r = {'_H': h}
    for naam, w in W.items():
        w = dict(w)
        if 'f' in w: w['_f'] = u(w['f'])
        if 'd' in w: w['_d'] = u(w['d'])
        if 'r' in w: w['_r'] = u(w['r'])
        r[naam] = {k: tijd(w, x, h) for k, x in DREMPEL.items()}
    eind, vorige = {}, 0.0
    for g in GROEPEN[:-1]:
        t = max(r[n]['legende'] for n, w in W.items() if w['groep'] == g)
        vorige = eind[g] = max(vorige, t)
    r['_eind'] = eind; runs.append(r)

# anker op de aarde: 801 ligt op A jaar BP. Afwijzen wat niet past.
acc = []
for r in runs:
    a = random.uniform(15000, 40000); amer = u(A['amerika'])
    velmara_begin = a + 2041                      # landing -1240 tot 801
    c1 = A['laag_water'][1] <= a and velmara_begin <= A['laag_water'][0]   # Velmara leeft op het droge plat
    c2 = a - r['_eind']['vertrek'] >= amer          # de mythen zijn gevormd voor de mensen Amerika in trekken
    c3 = a - r['_eind']['vertrek'] - A['schrift'] >= 3000   # zwevend gat (Vansina) van minstens 3000 jaar tot het schrift
    if c1 and c2 and c3: acc.append((a, r))

q = lambda xs, p: sorted(xs)[int(p * (len(xs) - 1))]
def band(xs): xs = [x for x in xs if math.isfinite(x)]; return [round(q(xs, .1)), round(q(xs, .5)), round(q(xs, .9))] if xs else None
uit = {'runs': N, 'geaccepteerd': len(acc), 'anker_bp_801': band([a for a, _ in acc]),
       'tijdperk_eind_na_801': {g: band([r['_eind'][g] for _, r in acc]) for g in GROEPEN[:-1]},
       'wezens': {n: {k: band([r[n][k] for _, r in acc]) for k in DREMPEL} for n in W},
       'steen_halfwaarde': band([r['_H'] for _, r in acc]),
       'knelt': {}}
# welke beperking knelt het hardst: aandeel afwijzingen per beperking (los getoetst)
tel = {'c1 laag water': 0, 'c2 voor Amerika': 0, 'c3 zwevend gat': 0}
for r in runs[:5000]:
    a = random.uniform(15000, 40000); amer = u(A['amerika'])
    tel['c1 laag water'] += not (A['laag_water'][1] <= a and a + 2041 <= A['laag_water'][0])
    tel['c2 voor Amerika'] += not (a - r['_eind']['vertrek'] >= amer)
    tel['c3 zwevend gat'] += not (a - r['_eind']['vertrek'] - A['schrift'] >= 3000)
uit['knelt'] = {k: round(v / 5000, 2) for k, v in tel.items()}
json.dump(uit, open(os.path.join(H, 'uitkomst.json'), 'w'), indent=1, ensure_ascii=False)

a50 = uit['anker_bp_801'][1]
o = ['# Verliessimulatie na 801', '', f"{N} lopen, {len(acc)} geaccepteerd door de aarde-beperkingen. Bandbreedte = 10e, 50e en 90e percentiel. Jaren na 801.", '',
     f"**Anker:** 801 ligt op {uit['anker_bp_801'][1]:,} jaar BP (band {uit['anker_bp_801'][0]:,} tot {uit['anker_bp_801'][2]:,}). De landing (-1240) ligt dan op ongeveer {a50 + 2041:,} BP".replace(',', '.') + ", midden in het laatste glaciale maximum, op droog continentaal plat dat nu onder zee ligt.", '',
     f"**Wat knelt** (aandeel afgewezen per beperking, los getoetst): " + ', '.join(f'{k} {v:.0%}' for k, v in uit['knelt'].items()), '',
     '## Tijdperken (einde, jaren na 801)', '| Groep wordt legende | 10% | 50% | 90% |', '|---|---|---|---|']
for g, b in uit['tijdperk_eind_na_801'].items(): o.append(f'| {g} | {b[0]} | {b[1]} | {b[2]} |')
o += ['', '## Per wezen (jaren na 801, mediaan; zeldzaam / legende / verdwenen)', '| Wezen | Groep | Zeldzaam | Legende | Verdwenen | Waarom (canon) |', '|---|---|---|---|---|---|']
fmt = lambda b: '-' if b is None else str(b[1])
for n, w in sorted(W.items(), key=lambda kv: (GROEPEN.index(kv[1]['groep']), (uit['wezens'][kv[0]]['legende'] or [0, 1e9])[1])):
    b = uit['wezens'][n]
    o.append(f"| {n} | {w['groep']} | {fmt(b['zeldzaam'])} | {fmt(b['legende'])} | {fmt(b['verdwenen'])} | {w['waarom']} ({', '.join(w['bron'])}) |")
open(os.path.join(H, 'verlies.md'), 'w').write('\n'.join(o) + '\n'); print('\n'.join(o[:12]))
