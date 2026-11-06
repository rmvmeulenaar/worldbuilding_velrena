#!/usr/bin/env python3
"""Velmara: één ingang voor het werk aan de canon.

De BRON in git is tekst: de map canon_tekst/ (WERELD_VELMARA.md, opgeknipt per hoofdstuk zodat verschillen leesbaar zijn).
canon.db wordt daaruit gebouwd en staat niet in git. De roundtrip bewijst dat tekst -> database -> tekst verliesvrij is.

  python3 velmara.py bouw     tekst -> canon.db (importeer + migraties + afgeleid), daarna toets
  python3 velmara.py tekst    canon.db -> WERELD_VELMARA.md (genereer.py) -> canon_tekst/ ; daarna bijbel/ en canon.md
  python3 velmara.py toets    toets.py en roundtrip op canon.db
  python3 velmara.py kaart    knopenkaart.html (alle verhaallijnen en hun knopen) uit canon.db
  python3 velmara.py mythen   mythen/: Wikidata oogsten (gecachet in mythen/ruw), clusters koppelen aan de canon, mythentoets
  python3 velmara.py check    controleer dat canon_tekst/ samen exact WERELD_VELMARA.md vormt (na 'tekst')

Werkwijze per ronde: velmara.py bouw  ->  ronde-script (r_Znn.py) draaien  ->  velmara.py tekst  ->  velmara.py toets  ->  commit.
"""
import os, sys, re, subprocess, json, glob, shutil
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W)
TEKST = os.path.join(W, 'canon_tekst'); EEN = os.path.join(W, 'WERELD_VELMARA.md')
PY = sys.executable

def run(*a):
    print('$', ' '.join(a)); r = subprocess.run(a)
    if r.returncode: sys.exit(f'mislukt: {" ".join(a)}')

def knip():
    """WERELD_VELMARA.md -> canon_tekst/NNN_naam.md, geknipt vóór elke regel die met '# ' of '## ' begint. Samengevoegd is het byte-gelijk."""
    data = open(EEN, encoding='utf-8').read()
    delen, start = [], 0
    for m in re.finditer(r'^(#|##) .*$', data, re.M):
        if m.start() > start: delen.append(data[start:m.start()])
        start = m.start()
    delen.append(data[start:])
    # grote hoofdstukken (> 3 MB) verder knippen bij '### ' zodat GitHub en diffs ze aankunnen
    fijn = []
    for d in delen:
        if len(d.encode('utf-8')) <= 3_000_000: fijn.append(d); continue
        s = 0; buf = ''
        for m in re.finditer(r'^### .*$', d, re.M):
            if len((buf + d[s:m.start()]).encode('utf-8')) > 2_500_000 and buf:
                fijn.append(buf); buf = ''
            buf += d[s:m.start()]; s = m.start()
        buf += d[s:]; fijn.append(buf)
    if os.path.isdir(TEKST): shutil.rmtree(TEKST)
    os.makedirs(TEKST)
    for i, d in enumerate(fijn):
        kop = d.split('\n', 1)[0].lstrip('#').strip() or 'kop'
        naam = re.sub(r'[^a-z0-9]+', '-', kop.lower().replace('’', '').replace('·', ''))[:40].strip('-') or 'deel'
        open(os.path.join(TEKST, f'{i:03d}_{naam}.md'), 'w', encoding='utf-8', newline='').write(d)
    print(f'{len(fijn)} bestanden in canon_tekst/')

def plak():
    """canon_tekst/ -> WERELD_VELMARA.md (in bestandsvolgorde)."""
    delen = sorted(glob.glob(os.path.join(TEKST, '*.md')))
    if not delen: sys.exit('canon_tekst/ is leeg')
    open(EEN, 'w', encoding='utf-8', newline='').write(''.join(open(p, encoding='utf-8', newline='').read() for p in delen))

def check():
    tijdelijk = EEN + '.check'
    delen = sorted(glob.glob(os.path.join(TEKST, '*.md')))
    samen = ''.join(open(p, encoding='utf-8', newline='').read() for p in delen)
    ok = os.path.exists(EEN) and samen == open(EEN, encoding='utf-8', newline='').read()
    print('canon_tekst/ is exact WERELD_VELMARA.md' if ok else 'VERSCHIL tussen canon_tekst/ en WERELD_VELMARA.md'); return ok

def bouw():
    plak()
    if os.path.exists('canon.db'): shutil.copy('canon.db', 'canon_vorige.db')
    tmp = 'canon_nieuw.db'
    if os.path.exists(tmp): os.remove(tmp)
    run(PY, 'importeer.py', 'WERELD_VELMARA.md', tmp)
    sys.path[:0] = [W, os.path.join(W, 'migraties')]
    import sqlite3, migreer, afgeleid
    c = sqlite3.connect(tmp); migreer.draai(c); afgeleid.bouw(c); c.commit(); c.close()
    os.replace(tmp, 'canon.db'); print('canon.db gebouwd uit canon_tekst/')
    toets()

def tekst():
    run(PY, 'genereer.py'); run(PY, 'export.py'); knip(); check()

def toets():
    run(PY, 'toets.py', 'canon.db')
    if os.path.exists(EEN): run(PY, 'roundtrip.py', 'canon.db')

def kaart():
    os.makedirs('kaart', exist_ok=True)
    run(PY, 'graaf_export.py', 'canon.db', 'kaart/graaf.json')
    d = json.load(open('kaart/graaf.json'))
    for v in d['verhalen']:
        v['tekst'] = v['tekst'][:420]
        for k in ('status', 'dk', 'seriewaarde'): v.pop(k, None)
    for i in d['knopen'].values():
        if 'tekst' in i: i['tekst'] = i['tekst'][:240]
    s = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    open('kaart/knopenkaart.html', 'w').write(open('kaart/sjabloon.html').read().replace('__DATA__', s))
    print('kaart/knopenkaart.html')

def mythen():
    run(PY, 'mythen/oogst.py'); run(PY, 'mythen/koppel.py'); run(PY, 'mythen/toets_mythen.py')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'bouw': bouw, 'tekst': tekst, 'toets': toets, 'kaart': kaart, 'mythen': mythen, 'check': check, 'knip': knip, 'plak': plak}.get(cmd, lambda: print(__doc__))()
