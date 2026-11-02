# Toetsen uit MYTHEPLAN: elke oorsprong verwijst naar bestaande canon; 2-4 regels uit vervorming.yaml; cluster >=3 culturen of lokaal;
# keten heeft drie stappen; harde lijnen: geen kind/minderjarige in een zin met seksuele woorden. Exit 1 bij fout.
import os, re, sqlite3, sys, yaml
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(H)
cl = {c['id']: c for c in yaml.safe_load(open(os.path.join(H, 'clusters.yaml')))}
oo = yaml.safe_load(open(os.path.join(H, 'oorsprong.yaml'))); rg = yaml.safe_load(open(os.path.join(H, 'vervorming.yaml')))
k = sqlite3.connect(os.path.join(W, os.environ.get('DB', 'canon.db'))); m = sqlite3.connect(os.path.join(H, 'mythen.db'))
cu = dict(m.execute('select id,culturen from cluster'))
KIND = re.compile(r'\b(kind|kinderen|meisje|jongetje|minderjarig\w*|tiener\w*|puber\w*)\b', re.I)
SEKS = re.compile(r'\b(seks\w*|ontvang\w*|zaad|gemolken|dekk\w*|minnaar|verenigt|genot|erot\w*)\b', re.I)
fout = []
for o in oo:
    c = o['cluster']
    if c not in cl: fout.append((c, 'cluster niet in clusters.yaml'))
    for x in o['canon']:
        if not k.execute('select 1 from canon where code=?', (x,)).fetchone(): fout.append((c, f'canon {x} bestaat niet'))
    if not 2 <= len(o['regels']) <= 4: fout.append((c, f'{len(o["regels"])} regels'))
    for r in o['regels']:
        if r not in rg: fout.append((c, f'regel {r} onbekend'))
    if len(o['keten']) != 3: fout.append((c, 'keten moet 3 stappen hebben'))
    if cu.get(c, 0) < 3 and not cl.get(c, {}).get('lokaal'): fout.append((c, f'maar {cu.get(c)} culturen'))
    for z in re.split(r'(?<=[.!?])\s+', o['rij'] + ' ' + ' '.join(o['keten'])):
        if KIND.search(z) and SEKS.search(z): fout.append((c, 'harde lijn: kind en seksueel woord in één zin: ' + z[:90]))
gedekt = {o['cluster'] for o in oo}; open_ = [c for c in cl if c not in gedekt and not cl[c].get('lokaal')]
print(f'oorsprongen: {len(oo)}, clusters zonder oorsprong (niet-lokaal): {len(open_)} {open_}')
for f in fout: print('FOUT', *f)
sys.exit(1 if fout else 0)
