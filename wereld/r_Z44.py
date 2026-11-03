# Ronde Z44: de technologieboom van Velmara.
# Uitvindingen komen niet meer uit drempels op een getal, maar uit een boom (z44/boom.py) die gebouwd is op de vier technieken
# van de canon (TECHNO-REGEL-V4: bio, gave, zegelsteen, metaal) en hun mengvormen (TECHNO-MIX-V4), met de beperkingen van de
# canon: geen brandstof en weinig erts (ORIGIN-2), roestschimmel (YSA-Z17-6), metaal niet te maken (TECHNO-metaal).
# Ontwerpregel (review 1): een uitvinding ontstaat pas als de wereld haar mogelijk maakt, de geschiedenis haar nodig of
# aantrekkelijk maakt, en haar bestaan de volgende geschiedenis verandert. De boom bevat ook wat Velmara niet doet, met reden.
# Motor: z44/geschiedenis.py (bouwt op Z43). Nieuwe tabellen tech_knoop en sim_uitvinding (migratie 011), met views en regels.
# Alles voorstel of simulatie; niets in de canon gezet.
# Gebouwd door de architect op verzoek van Rogier (2026-11-02). Idempotent, additief. Gebruik: DB=kopie.db python3 r_Z44.py
import sqlite3, shutil, os, sys, json, collections, importlib.util
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
def laad(naam, pad):
    s = importlib.util.spec_from_file_location(naam, os.path.join(W, pad)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
G = laad('z44_geschiedenis', 'z44/geschiedenis.py'); B = G.B
DT = '2026-11-02'; RD = 'Z44'; DB = os.environ.get('DB', 'canon.db'); MOD = 'geschiedenis_z44'
N_RUNS = 1000; SEED0 = 420000; GEKOZEN = [3, 1, 2, 5, 8, 13]
if DB == 'canon.db' and not os.path.exists('canon_backup_Z44.db'): shutil.copy('canon.db', 'canon_backup_Z44.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
CODES = {r[0] for r in c.execute("select code from canon where status in ('vastgesteld','voorlopig')")}
def bestaat(*codes):
    for x in codes:
        for y in (x or '').split(';'):
            if y and y not in CODES: sys.exit(f'bron {y} bestaat niet (levend) in canon')
B.controleer()

# ---------- 1 de boom (tech_knoop) ----------
for k in B.BOOM:
    bestaat(k['bron'])
    S['tech_knoop'] += c.execute('insert or ignore into tech_knoop(code,naam,familie,domein,status,vereist,materiaal,noodzaak,uitvinder,gevolg,breekt,prijs,afstoting,reden,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (k['code'], k['naam'], k['familie'], k['domein'], 'mogelijk', ';'.join(k['vereist']) or None, k['materiaal'], ';'.join(k['noodzaak']), k['uitvinder'],
         json.dumps(k['gevolg'], ensure_ascii=False), k['breekt'], k['prijs'], k['afstoting'], None, k['bron'], f"voorstel (architect Z44, uit {k['bron']})")).rowcount
for code, naam, status, reden, bron in B.ONMOGELIJK:
    bestaat(bron)
    S['tech_knoop'] += c.execute('insert or ignore into tech_knoop(code,naam,familie,domein,status,vereist,materiaal,noodzaak,uitvinder,gevolg,breekt,prijs,afstoting,reden,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (code, naam, None, None, status, None, None, None, None, None, None, None, None, reden, bron, f'voorstel (architect Z44, uit {bron})')).rowcount

# ---------- 2 motorregels (sim_regel) en toetsregels (regel) ----------
REGELS = [
 ('GESCH3-boom', 'Een uitvinding ontstaat alleen uit de boom: al haar vereisten bestaan al, haar materiaalvoorwaarde klopt, en haar uitvinder heeft minstens 5 procent van de macht.', 'boom', '17 knopen', 'TECHNO-REGEL-V4;TECHNO-MIX-V4'),
 ('GESCH3-nood', 'Nood maakt vindingrijk: een uitvinding waar een crisis van de laatste 100 jaar om vroeg, is per 20 jaar ruim tien keer zo waarschijnlijk als een die alleen aantrekkelijk is.', 'kans', '0,06 maal (0,2 of 2,7) maal (0,5 + beschaving)', 'TECHNO-REGEL-V4'),
 ('GESCH3-gevolg', 'Een uitvinding verandert toestand en macht meteen (gevolg in tech_knoop); latere crises kunnen van haar erven.', 'gevolg', 'per knoop', 'TECHNO-REGEL-V4'),
 ('GESCH3-staat', 'Edelen kosten de staat geld: de kas daalt met 0,045 maal het aantal edelen per 20 jaar (Turchin); te veel edelen en een lege kas geven strijd.', 'kosten', '0,045', 'FASE-markt;FASE-barsten'),
 ('GESCH3-techniek', 'Techniek groeit zelf nog maar half zo snel als in Z43; de rest komt uit uitvindingen.', 'groei', '0,003', 'TECHNO-REGEL-V4'),
]
for code, oms, par, waarde, bron in REGELS:
    bestaat(bron)
    S['sim_regel'] += c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
        (code, MOD, oms, par, waarde, bron, 1, 801, None, 'voorlopig', f'aanname (motorontwerp Z44, bron {bron})')).rowcount
TOETS = [
 ('R-tech_boom', 'Elke mogelijke knoop van de technologieboom heeft materiaal, noodzaak, uitvinder, gevolg, prijs en een bron, en haar vereisten bestaan in de boom; elke onmogelijke of onnodige knoop heeft een reden.',
  "select code,'knoop onvolledig of vereiste bestaat niet' from tech_knoop k where (status='mogelijk' and (materiaal is null or noodzaak is null or uitvinder is null or gevolg is null or prijs is null or bron is null)) or (status in ('onmogelijk','onnodig','onmogelijk en onnodig') and reden is null) union select k.code,'vereiste '||v.value||' bestaat niet' from tech_knoop k, json_each('[\"'||replace(coalesce(k.vereist,''),';','\",\"')||'\"]') v where v.value!='' and v.value not in (select code from tech_knoop)"),
 ('R-sim_uitvinding', 'Elke gesimuleerde uitvinding is een mogelijke knoop, komt na al haar vereisten in dezelfde run, en heeft een uitvinder met minstens 5 procent macht, een noodzaak en een gevolg.',
  "select u.run_id||':'||u.knoop,'uitvinding zonder geldige knoop, uitvinder, noodzaak of gevolg' from sim_uitvinding u where u.knoop not in (select code from tech_knoop where status='mogelijk') or coalesce(u.uitvinder_macht,0)<0.05 or u.noodzaak is null or u.gevolg is null union select u.run_id||':'||u.knoop,'uitvinding vóór haar vereiste '||j.key from sim_uitvinding u, json_each(u.vereist_met) j where j.value>=u.jaar or not exists(select 1 from sim_uitvinding v where v.run_id=u.run_id and v.knoop=j.key and v.jaar=j.value)"),
]
for code, oms, sq in TOETS:
    S['regel'] += c.execute("insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
        (code, 'simulatie', oms, sq, 'r_Z44.py (review 1 van Z42, blok H)', 'architect, in opdracht van Rogier (2026-11-02)', 'actief', 'fout')).rowcount
S['tech_gebeurtenistype'] += c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',
    ('gesch_uitvinding_boom', MOD, 'Een uitvinding uit de technologieboom (zie sim_uitvinding).', 'nooit vóór haar vereisten', 'GESCH3-boom', 'aanname (moduleontwerp Z44, bron GESCH3-boom)')).rowcount

# ---------- 3 runs ----------
EV_CANON = {'kern_valt':'ORIGIN-Z1-harrow','kern_in_worm':'ORIGIN-Z1-harrow','negen_cellen':'YSA-Z21-3','splinter':'ORIGIN-8','grote_drager':'GAVE-Z37-ja',
            'schimmeljaar':'HORROR-SKELET-Z9-6','aelthir_trek':'VOLK-aelthir-V5','nachtplaag':'ORIGIN-WAAROM-9','archief':'REG-stille'}
bestaat(*EV_CANON.values(), *G.LIJN_CANON.values())
def golven(ms):
    n = 0; lo = hi = ms[0]
    for v in ms:
        if v > hi: hi = v
        if hi - v >= .12 and hi - lo >= .12: n += 1; lo = hi = v
        if v < lo: lo = hi = v
    return n
def geb(rid, epi, jaar, typ, actor, doel, detail, canon, oorzaak):
    S['sim_gebeurtenis'] += c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (rid, MOD, jaar, '-', typ, actor or '-', doel or '-', '-', detail, canon, 'voorlopig', epi, oorzaak)).rowcount
def ins(tabel, rij):
    S[tabel] += c.execute(f"insert or ignore into {tabel}({','.join(rij)}) values({','.join('?' * len(rij))})", list(rij.values())).rowcount
if c.execute('select count(*) from sim_run where module=?', (MOD,)).fetchone()[0] < N_RUNS:
    for i in range(1, N_RUNS + 1):
        seed = SEED0 + i; rid = f'Z44-GESCH-{i:04d}'; epi = f'simulatie ({rid}, seed {seed})'
        o = G.run(seed); ms = [x['M'] for x in o['log']]
        gekozen = int(i in GEKOZEN); n = 0
        U = o['uitvindingen']
        scores = dict(fasen=len(o['fasen']), onopgelost=len(o['onopgelost']), uitvindingen=[(u['code'], u['jaar']) for u in U],
                      uit_nood=sum(not u['noodzaak'].startswith('aantrekkelijk') for u in U), magie_min=min(ms), magie_eind=ms[-1], golven=golven(ms),
                      techniek_eind=o['log'][-1]['T'], werkplaatsen_vanaf=next((x['jaar'] for x in o['log'] if x['T'] > .6), None),
                      heersers=len({h['huis'] for h in o['huizen'] if h['gezag_van']}), wetten=len(o['wetten']),
                      rustige_jaren=sum(r['tot'] - r['van'] for r in o['rust']), macht_eind=o['log'][-1]['macht'], parameters=o['p'])
        if gekozen:
            for f in o['fasen']:
                ins('sim_fase', dict(run_id=rid, module=MOD, van=f['van'], tot=f['tot'], crisis=f['crisis'], oplossing=f['oplossing'], naam=f['naam'], beslisser=f['beslisser'],
                    macht_sleutel=f['macht_sleutel'], actor_macht=f['actor_macht'], mechanisme=f['mechanisme'], handhaver=f['handhaver'], betaler=f['betaler'],
                    vervalst=f['vervalst'], ontdekt=f['ontdekt'], schaal=f['schaal'], oorzaak=json.dumps(f['oorzaak'], ensure_ascii=False), druk=f['druk'],
                    tweede_druk=f['tweede_druk'], erft_van=f['erft_van'], gedeeld_mechanisme=f['gedeeld_mechanisme'], rijmt_met=f['rijmt_met'],
                    assen_anders=f['assen_anders'], gevolg=json.dumps(f['gevolg'], ensure_ascii=False), blijvend=f['blijvend'], epistemiek=epi)); n += 1
            for w in o['wetten']:
                ins('sim_wet', dict(run_id=rid, module=MOD, wet=w['wet'], tekst=w['tekst'], wetgever=w['wetgever'], macht_sleutel=w['macht_sleutel'], wetgever_macht=w['wetgever_macht'],
                    rechtsgebied=w['rechtsgebied'], handhaver=w['handhaver'], aanleiding=w['aanleiding'], van=w['van'], tot=w['tot'], vervalt_door=w['vervalt_door'],
                    canon_code=w['wet'] if w['wet'] in CODES else None, epistemiek=epi)); n += 1
            for h in o['huizen']:
                ins('sim_huis', dict(run_id=rid, module=MOD, huis=h['huis'], ouder=h['ouder'], ontstaan=h['ontstaan'], aanspraak=h['aanspraak'], gezag_van=h['gezag_van'],
                    gezag_tot=h['gezag_tot'], gevallen=h['gevallen'], canon_code=h['canon'], epistemiek=epi)); n += 1
            for u in U:
                ins('sim_uitvinding', dict(run_id=rid, module=MOD, knoop=u['code'], jaar=u['jaar'], uitvinder=u['uitvinder'], uitvinder_macht=u['uitvinder_macht'],
                    noodzaak=u['noodzaak'], materiaal=u['materiaal'], vereist_met=json.dumps(u['vereist_met'], ensure_ascii=False), breekt=u['breekt'], prijs=u['prijs'],
                    gevolg=json.dumps(u['gevolg'], ensure_ascii=False), epistemiek=epi)); n += 1
                geb(rid, epi, u['jaar'], 'gesch_uitvinding_boom', u['uitvinder'], u['code'], f"{u['naam']} ({u['familie']}). Noodzaak: {u['noodzaak']}. Breekt: {u['breekt']}. Prijs: {u['prijs']}.", None, 'GESCH3-boom'); n += 1
            for x in o['onopgelost']:
                geb(rid, epi, x['jaar'], 'gesch_onopgelost', '-', x['crisis'], f"Crisis {x['crisis']} (druk {x['druk']}, oorzaak {json.dumps(x['oorzaak'], ensure_ascii=False)}): niemand met genoeg macht had een oplossing die rijmt.", None, 'GESCH2-macht'); n += 1
            for g in o['gebeurd']:
                geb(rid, epi, g['jaar'], 'gesch_gebeurtenis', '-', g['id'], g['tekst'], EV_CANON.get(g['id']), 'GESCH-piek'); n += 1
            for r in o['rust']:
                geb(rid, epi, r['van'], 'gesch_rust', '-', '-', f"Rustige tijd {r['van']} tot {r['tot']}. Politiek: {r['politiek']}. Economie: {r['economie']}. Samenleving: {r['samenleving']}. Magie: {r['magie']}. Verhalen op de schaal van huis en dorp: {r['genres']}.", None, 'GESCH-rust'); n += 1
            vorige = None; stad = {}
            for x in o['log']:
                if (x['jaar'] - 801) % 100 == 0:
                    geb(rid, epi, x['jaar'], 'gesch_toestand', '-', '-', json.dumps(dict(magie=x['M'], bodem=x['bodem'], techniek=x['T'], jongens=x['r'], honger=x['P'], kas=x['S'], edelen=x['E'],
                        geloof=x['L'], openheid=x['O'], orrim=x['orrim'], beschaving=x['C'], tijd=x['era'], heerser=x['heerser'], wetten=x['wetten'], macht=x['macht']), ensure_ascii=False), None, 'GESCH-bodem'); n += 1
                v = G.versie(x['f'], x['tak'])
                if v != vorige:
                    geb(rid, epi, x['jaar'], 'gesch_versie801', '-', G.label801(x['f']), f"{v} [waarheid: {G.label801(x['f'])}; trouw {x['f']}]", 'BESLUIT-Z36-4', 'GESCH-verhaal801'); vorige = v; n += 1
                for k, st in x['lijn'].items():
                    if stad.get(k) != st:
                        geb(rid, epi, x['jaar'], 'gesch_wezen', k, ['slachtoffer','groep','volk','monster','sprookje'][st], G.LIJN[k][st], G.LIJN_CANON[k], 'GESCH-wezens'); stad[k] = st; n += 1
        S['sim_run'] += c.execute('insert or ignore into sim_run(run_id,module,fase_nr,seed,geldig,reden,n_gebeurtenis,scores,pareto_rang,gewogen,gekozen,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (rid, MOD, 9, seed, 1, None, n or len(o['fasen']) + len(U), json.dumps(scores, ensure_ascii=False), None, None, gekozen, 'r_Z44.py', epi)).rowcount

# ---------- 4 keuzes voor Rogier ----------
KEUZES = [
 ('KEUZE-Z44-boom', 'wereld', 'De technologieboom van Velmara na 801', 'Bevestig de 17 knopen (tech_knoop, status mogelijk) of schrap en voeg toe. Elke knoop komt uit TECHNO-bio, -gave, -zegelsteen, -metaal of TECHNO-MIX-V4.', 'TECHNO-REGEL-V4;TECHNO-MIX-V4',
  'Rogier (2026-11-02): ja, begin met de technologieboom. Review 1: laat de boom vanuit Velmara ontstaan, niet uit de aardse reeks ijzer, stoom, elektriciteit.'),
 ('KEUZE-Z44-onmogelijk', 'wereld', 'Wat Velmara niet uitvindt', 'Bevestig de zeven onmogelijke of onnodige technieken (stoom, kolen, staal, kruit, stroomnet, rekenmachines, nieuwe kernen) met hun reden uit de canon.', 'ORIGIN-2;YSA-Z17-6;ORIGIN-7',
  'Review 1, vraag 27: welke technologieën zijn onmogelijk, onnodig of onaantrekkelijk, juist doordat de wereld andere mogelijkheden heeft?'),
 ('KEUZE-Z44-nood', 'wereld', 'Nood maakt vindingrijk', 'Bevestig dat een uitvinding waar een crisis om vroeg veel waarschijnlijker is. Daardoor verschilt de volgorde van uitvinden per geschiedenis (278 verschillende volgordes in 300 runs).', 'GESCH3-nood',
  'Review 1: meet de verschillen tussen runs causaal, niet cosmetisch.'),
 ('KEUZE-Z44-staat', 'wereld', 'Edelen kosten de staat geld', 'Bevestig dat het aantal edelen de kas uitput. Zonder die regel komt een strijd om posities bijna nooit voor.', 'GESCH3-staat;FASE-markt',
  'Gevonden bij het bouwen van Z44: met extra voedsel uit de kweekakkers verdween de strijd van te veel edelen.'),
]
for code, soort, ond, aanb, raakt, citaat in KEUZES:
    bestaat(raakt.replace('GESCH3-nood', '').replace('GESCH3-staat', ''))
    S['keuze'] += c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',
        (code, soort, ond, aanb, raakt, 'open', 'r_Z44.py', citaat)).rowcount
if not c.execute("select 1 from logboek where wat like 'Ronde Z44:%'").fetchone():
    c.execute('insert into logboek(datum,wat) values(?,?)', (DT, 'Ronde Z44: de technologieboom (z44/boom.py, z44/geschiedenis.py). Nieuwe tabellen tech_knoop (17 mogelijke en 7 onmogelijke of onnodige technieken, elk met canonbron) en sim_uitvinding (migratie 011), views v_tech_boom en v_sim_uitvinding, regels R-tech_boom en R-sim_uitvinding. 5 motorregels GESCH3-*, 1000 runs Z44-GESCH-0001..1000 (dezelfde seeds als Z42 en Z43), zes gekozen runs met alle details, vier open keuzes KEUZE-Z44-*. Alles voorstel of simulatie; niets in de canon gezet.')); S['logboek'] += 1
afgeleid.bouw(c); c.commit()
print(dict(S))
