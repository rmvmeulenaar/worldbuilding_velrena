# M0: mythen van de aarde oogsten uit Wikidata (CC0) naar mythen.db. Idempotent; bewaart ruwe antwoorden in ruw/.
import json, os, sqlite3, sys, time, urllib.parse, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(H, 'ruw'), exist_ok=True)
EP = 'https://query.wikidata.org/sparql'
KLASSEN = {'wezen': 'Q2239243', 'god': 'Q178885', 'geest': 'Q3743'}   # mythisch wezen, godheid, geest
def sparql(q, naam):
    p = os.path.join(H, 'ruw', naam + '.json')
    if os.path.exists(p): return json.load(open(p))
    for poging in range(4):
        try:
            req = urllib.request.Request(EP + '?' + urllib.parse.urlencode({'query': q, 'format': 'json'}),
                                         headers={'User-Agent': 'VelmaraMythen/0.1 (worldbuilding; rmvmeulenaar)'})
            d = json.loads(urllib.request.urlopen(req, timeout=300).read().decode("utf-8", "replace"), strict=False); json.dump(d, open(p, 'w')); return d
        except Exception as e:
            print(naam, 'poging', poging, e); time.sleep(10 * (poging + 1))
    sys.exit('oogst mislukt: ' + naam)
def q_klasse(qid):
    return f"""SELECT ?x ?xLabel ?xDescription ?nl ?klasseLabel ?cultuurLabel ?landLabel ?n WHERE {{
  ?x wdt:P31/wdt:P279* wd:{qid} . ?x wdt:P31 ?klasse .
  OPTIONAL {{ ?x wdt:P1080|wdt:P361 ?cultuur . }}
  OPTIONAL {{ ?x wdt:P495 ?land . }}
  OPTIONAL {{ ?x rdfs:label ?nl FILTER(lang(?nl)='nl') }}
  OPTIONAL {{ ?x wikibase:sitelinks ?n }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }} }}"""
def bouw():
    c = sqlite3.connect(os.path.join(H, 'mythen.db'))
    c.executescript(open(os.path.join(H, 'schema.sql')).read())
    for soort, qid in KLASSEN.items():
        d = sparql(q_klasse(qid), soort)
        for b in d['results']['bindings']:
            g = lambda k: b.get(k, {}).get('value')
            i = g('x').rsplit('/', 1)[1]; naam = g('xLabel')
            if not naam or naam == i: continue
            c.execute('insert or ignore into entiteit(id,naam,naam_nl,soort,beschrijving,bekendheid,bron) values(?,?,?,?,?,?,?)',
                      (i, naam, g('nl'), soort, g('xDescription'), int(g('n') or 0), 'wikidata'))
            for k, w in (('klasse', g('klasseLabel')), ('cultuur', g('cultuurLabel')), ('land', g('landLabel'))):
                if w and not w.startswith('Q'): c.execute('insert or ignore into kenmerk(entiteit,kenmerk,waarde) values(?,?,?)', (i, k, w))
    c.commit()
    for soort, n in c.execute('select soort,count(*) from entiteit group by 1'): print(soort, n)
    print('kenmerken', c.execute('select count(*) from kenmerk').fetchone()[0])
if __name__ == '__main__': bouw()
