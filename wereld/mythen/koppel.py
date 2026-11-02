# M2/M3: clusters laden, leden uit Wikidata herkennen, universaliteit meten, en per cluster de canon scoren op kandidaat-oorsprongen.
# De data beslist de kandidaat: score = verschillende sleutelwoorden die raken x draagkracht (Kern 3, Structuur 2, Kleur 1) + fase-bonus.
# Gebruik (vanuit wereld/): python3 mythen/koppel.py  -> mythen/mythen.db (cluster, lid, koppel_score) en mythen/koppeling.md
import os, re, sqlite3, sys, collections, yaml
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(H)
FICTIE = re.compile(r'universe|earth-616|\bdc\b|marvel|one piece|evangelion|pok[eé]mon|video game|anime|manga|comic|fictional|film|novel|tolkien|middle-earth|warhammer|dungeons|d&d|beboks|digimon|yu-gi-oh|harry potter|television|tv series|role-playing', re.I)
DK = {'Kern': 3, 'Structuur': 2, 'Kleur': 1}

def cultuur_van(vb):
    m = re.search(r'\(([^)]+)\)\s*$', vb); return [x.strip() for x in re.split(r',| en ', m.group(1))] if m else []

def voorbeelden(c):
    # YAML-flowlijsten knippen '(Joods, Arabisch)' op de komma: plak stukken met een open haakje weer aan elkaar
    uit, buf = [], None
    for x in c['voorbeelden']:
        x = (next(iter(x)) + ': ' + str(next(iter(x.values())))) if isinstance(x, dict) else str(x)
        buf = x if buf is None else buf + ', ' + x
        if buf.count('(') <= buf.count(')'): uit.append(buf); buf = None
    if buf: uit.append(buf)
    return uit

def laad(m):
    m.executescript(open(os.path.join(H, 'schema.sql')).read())
    for t in ('cluster', 'lid', 'koppel_score'): m.execute(f'delete from {t}')
    cl = yaml.safe_load(open(os.path.join(H, 'clusters.yaml')))
    ent = m.execute('select id,naam,coalesce(beschrijving,"") from entiteit').fetchall()
    kenm = collections.defaultdict(list)
    for e, k, w in m.execute("select entiteit,kenmerk,waarde from kenmerk where kenmerk in ('cultuur','land')"): kenm[e].append(w)
    fictie = {e for e, n, b in ent if FICTIE.search(b) or any(FICTIE.search(w) for w in kenm[e])}
    for e in fictie: m.execute("insert or ignore into kenmerk values(?,?,?)", (e, 'fictie', '1'))
    for c in cl:
        culturen = set()
        for vb in voorbeelden(c):
            cs = cultuur_van(vb); culturen |= set(cs)
            m.execute('insert or ignore into lid(cluster,entiteit,voorbeeld,cultuur) values(?,?,?,?)', (c['id'], None, vb, ', '.join(cs)))
        pats = [re.compile(r'\b' + re.escape(w) + r'\b', re.I) for w in c.get('en') or []]
        landen = set()
        for e, n, b in ent:
            if e in fictie or not pats: continue
            if any(p.search(n) or p.search(b) for p in pats):
                cw = [w for w in kenm[e] if 'mythology' in w.lower() or 'folklore' in w.lower() or 'religion' in w.lower()]
                m.execute('insert or ignore into lid(cluster,entiteit,voorbeeld,cultuur) values(?,?,?,?)', (c['id'], e, n, ', '.join(cw)))
                culturen |= {w.replace(' mythology', '').replace(' folklore', '') for w in cw}
                landen |= {w for w in kenm[e] if 'mytholog' not in w.lower()}
        m.execute('insert or replace into cluster(id,naam,kern,herkenning,culturen,landen,lokaal) values(?,?,?,?,?,?,?)',
                  (c['id'], c['naam'], c['kern'], c.get('herkenning'), len(culturen), len(landen), 1 if c.get('lokaal') else 0))
    return cl

def scoor(m, cl):
    k = sqlite3.connect(os.path.join(W, os.environ.get('DB', 'canon.db')))
    rij = k.execute("select code,draagkracht,coalesce(tijdperk,''),feit from canon where status in ('vastgesteld','voorlopig') and coalesce(epistemiek,'') not like 'voorstel (mytheplan%'").fetchall()
    for c in cl:
        pats = [(str(w), re.compile(re.escape(str(w)), re.I)) for w in c.get('nl') or []]
        laag = str(c.get('laag', ''))
        best = []
        for code, dk, tp, feit in rij:
            raak = [w for w, p in pats if p.search(feit or '')]
            if len(raak) < 2: continue
            s = len(raak) * DK.get(dk, 1) + (1.5 if tp.startswith(laag) else 0)
            best.append((s, code, raak))
        for s, code, raak in sorted(best, reverse=True)[:8]:
            m.execute('insert or replace into koppel_score values(?,?,?,?)', (c['id'], code, s, ', '.join(raak)))

def rapport(m):
    o = ['# M2/M3: clusters, universaliteit en kandidaat-oorsprongen in de canon', '',
         'Gemaakt door `mythen/koppel.py`. Culturen = verschillende culturen in de voorbeelden plus mythologieën van herkende Wikidata-leden. '
         'Hoe meer culturen, hoe sterker de reden voor één oorsprong in Velmara. De kandidaten zijn de canonrijen met de hoogste score.', '',
         '| # | Cluster | Culturen | Wikidata-leden | Beste kandidaat (score) |', '|---|---|---|---|---|']
    rs = m.execute("select c.id,c.naam,c.culturen,c.lokaal,(select count(*) from lid l where l.cluster=c.id and l.entiteit is not null) from cluster c order by c.lokaal, c.culturen desc").fetchall()
    for i, (cid, naam, cu, lok, nw) in enumerate(rs, 1):
        b = m.execute('select canon_code,score from koppel_score where cluster=? order by score desc limit 1', (cid,)).fetchone()
        o.append(f"| {i} | {naam}{' (lokaal)' if lok else ''} | {cu} | {nw} | {b[0] + ' (' + format(b[1], '.1f') + ')' if b else '-'} |")
    o.append('')
    for cid, naam, *_ in rs:
        o.append(f'## {naam}')
        for code, s, raak in m.execute('select canon_code,score,treffers from koppel_score where cluster=? order by score desc', (cid,)):
            o.append(f'- `{code}` {s:.1f}: {raak}')
        o.append('')
    open(os.path.join(H, 'koppeling.md'), 'w').write('\n'.join(o))
    print('\n'.join(o[:len(rs) + 6]))

if __name__ == '__main__':
    m = sqlite3.connect(os.path.join(H, 'mythen.db'))
    cl = laad(m); scoor(m, cl); m.commit(); rapport(m)
