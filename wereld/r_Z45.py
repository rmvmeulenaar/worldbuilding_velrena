# Ronde Z45: gebruik, gewone uitvindingen, kennis en verspreiding (op verzoek van Rogier, 2026-11-02).
# Per uitvinding: waar ze voor gebruikt wordt, door wie, waar ze in onze wereld op lijkt. Gewone uitvindingen komen erbij, elk met
# een Velmara-voorganger, met Kharvos (de Harrow koos machines, BESLUIT-3) als brug. Uitvinden volgt het patroon van echte
# geschiedenis: traag zolang de kennisvoorraad klein is, sneller met steden, handel en drukwerk; een uitvinding verspreidt zich
# langzaam (S-curve) en haar effect groeit mee; elke uitvinding wordt gemeten op het probleem waarvoor ze kwam. Magische techniek
# gaat verloren als haar bron opdroogt. Doel: de wereld groeit grofweg naar een gewone tijd. Motor: z45/geschiedenis.py, boom: z45/boom.py.
# Correctie op Z44: ORIGIN-2 gaat over brandstof voor de scheepskernen, niet over hout; stoom en kruit zijn mogelijk, maar laat.
# ---- hieronder de opbouw van Z44, aangepast voor Z45 ----
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
G = laad('z45_geschiedenis', 'z45/geschiedenis.py'); B = G.B
DT = '2026-11-02'; RD = 'Z45'; DB = os.environ.get('DB', 'canon.db'); MOD = 'geschiedenis_z45'
N_RUNS = 1000; SEED0 = 420000; GEKOZEN = [3, 1, 2, 5, 8, 13]
if DB == 'canon.db' and not os.path.exists('canon_backup_Z45.db'): shutil.copy('canon.db', 'canon_backup_Z45.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
CODES = {r[0] for r in c.execute("select code from canon where status in ('vastgesteld','voorlopig')")}
def bestaat(*codes):
    for x in codes:
        for y in (x or '').split(';'):
            if y and y not in CODES: sys.exit(f'bron {y} bestaat niet (levend) in canon')
B.controleer()

# ---------- 1 de boom (tech_knoop): nieuwe knopen, gebruik bij bestaande, herziene onmogelijke ----------
def wijz(code, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
        (RD, code, 'gewijzigd', veld, None if oud is None else str(oud), str(nieuw), DT, 'r_Z45.py')).rowcount
OPV = B.OPVOLGER
for k in B.BOOM:
    bestaat(k['bron'])
    vereist = ';'.join(k['vereist']) or None
    S['tech_knoop'] += c.execute('insert or ignore into tech_knoop(code,naam,familie,domein,status,vereist,materiaal,noodzaak,uitvinder,gevolg,breekt,prijs,afstoting,reden,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (k['code'], k['naam'], k['familie'], k['domein'], 'mogelijk', vereist, k['materiaal'], ';'.join(k['noodzaak']), k['uitvinder'],
         json.dumps(k['gevolg'], ensure_ascii=False), k['breekt'], k['prijs'], k['afstoting'], None, k['bron'], f"voorstel (architect Z45, uit {k['bron']})")).rowcount
    nu = dict(zip(('gebruik','voor_wie','aards','tijdperk','soort','vervalt_bij','opvolger'), c.execute('select gebruik,voor_wie,aards,tijdperk,soort,vervalt_bij,opvolger from tech_knoop where code=?', (k['code'],)).fetchone()))
    doel = dict(gebruik=k['gebruik'], voor_wie=k['voor_wie'], aards=k['aards'], tijdperk=k['tijdperk'], soort=k['soort'], vervalt_bij=k.get('vervalt_bij'), opvolger=OPV.get(k['code']))
    for veld, w in doel.items():
        if nu[veld] != w and w is not None:
            c.execute(f'update tech_knoop set {veld}=? where code=?', (w, k['code'])); wijz(k['code'], 'tech_knoop.' + veld, nu[veld], w)
for code, (status, reden) in B.HERZIEN.items():
    if code == 'TK-x-staal': continue
    oud = c.execute('select status,reden from tech_knoop where code=?', (code,)).fetchone()
    if oud and (oud[0], oud[1]) != (status, reden):
        c.execute('update tech_knoop set status=?,reden=? where code=?', (status, reden, code)); wijz(code, 'tech_knoop.status en reden (correctie Z45)', f'{oud[0]}: {oud[1]}', f'{status}: {reden}')
for code, naam, status, reden, bron in B.ONMOGELIJK:
    bestaat(bron)
    oud = c.execute('select naam,reden,bron from tech_knoop where code=?', (code,)).fetchone()
    if oud is None:
        S['tech_knoop'] += c.execute('insert into tech_knoop(code,naam,status,reden,bron,epistemiek) values(?,?,?,?,?,?)', (code, naam, status, reden, bron, f'voorstel (architect Z45, uit {bron})')).rowcount
    elif oud != (naam, reden, bron):
        c.execute('update tech_knoop set naam=?,reden=?,bron=? where code=?', (naam, reden, bron, code)); wijz(code, 'tech_knoop.naam/reden/bron (aangescherpt Z45)', ' | '.join(map(str, oud)), f'{naam} | {reden} | {bron}')

# ---------- 2 motorregels (sim_regel) en toetsregels (regel) ----------
REGELS = [
 ('GESCH4-kennis', 'Uitvinden hangt af van de kennisvoorraad, tot de derde macht: traag zolang die klein is (zoals in de middeleeuwen), sneller met steden, handel en schrift; sporendruk en drukpers versnellen de groei, oorlog en epidemie kosten kennis, een boekverbod halveert de groei (Kremer, Mokyr).', 'kennis', 'start 0,25; kans 1,0 maal kennis^3 maal noodzaak', 'TECHNO-REGEL-V4;TECH-GESCH-11'),
 ('GESCH4-verspreiding', 'Een uitvinding verspreidt zich langs een S-curve; handel, drukwerk en netten (lichtnet, echonet, telegraaf, spoor) versnellen. Haar effect groeit en slinkt mee met het gebruik.', 'verspreiding', '0,3 per 20 jaar maal (1 + handel + 2,5 drukwerk + 2 netten)', 'TECHNO-REGEL-V4'),
 ('GESCH4-verval', 'Gave- en zegelsteentechniek gaat verloren als haar bron 100 jaar wegvalt (magie onder 0,32, of geen steen uit de groeven); de kennis blijft, de praktijk slinkt, en haar gewone opvolger wordt nodig.', 'verval', '100 jaar', 'BESLUIT-2;D1-orrim-dood'),
 ('GESCH4-kharvos', 'Het contact met Kharvos groeit met handel en met de dreiging van Kharvos; het opent het Kharvos-ambacht (smeden, raderwerk, koper).', 'contact', 'start 0,2', 'BESLUIT-3;REG-kharvos-B1;ORIGIN-Z1-harrow'),
 ('GESCH4-gewoon', 'Het Gewone begint als stoom, drukpers, elektriciteit, vaccin en spoor elk voor de helft verspreid zijn.', 'gewoon', '5 uitvindingen op 50%', 'TECH-GESCH-12-V4'),
]
for code, oms, par, waarde, bron in REGELS:
    bestaat(bron)
    S['sim_regel'] += c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
        (code, MOD, oms, par, waarde, bron, 1, 801, None, 'voorlopig', f'aanname (motorontwerp Z44, bron {bron})')).rowcount
# R-tech_boom (Z44) kent nu ook vereisten 'A|B' en eist een reden bij elke status behalve 'mogelijk'
SQL_BOOM = ("select code,'knoop onvolledig of vereiste bestaat niet' from tech_knoop k where (status='mogelijk' and (materiaal is null or noodzaak is null "
            "or uitvinder is null or gevolg is null or prijs is null or bron is null)) or (status!='mogelijk' and reden is null) union "
            "select k.code,'vereiste '||v.value||' bestaat niet' from tech_knoop k, json_each('[\"'||replace(replace(coalesce(k.vereist,''),'|',';'),';','\",\"')||'\"]') v "
            "where v.value!='' and v.value not in (select code from tech_knoop)")
oud = c.execute("select sql_test from regel where code='R-tech_boom'").fetchone()
if oud and oud[0] != SQL_BOOM:
    c.execute("update regel set sql_test=? where code='R-tech_boom'", (SQL_BOOM,)); wijz('R-tech_boom', 'regel.sql_test (A|B en reden bij elke status)', oud[0], SQL_BOOM)
TOETS = [
 ('R-tech_gebruik', 'Elke mogelijke knoop zegt waar ze voor gebruikt wordt, door wie, waar ze in onze wereld op lijkt, in welk tijdperk en of ze magisch is.',
  "select code,'knoop zonder gebruik, voor wie, aards equivalent, tijdperk of soort' from tech_knoop where status='mogelijk' and (gebruik is null or voor_wie is null or aards is null or tijdperk is null or soort is null)"),
 ('R-sim_effect', 'Elke gesimuleerde uitvinding van Z45 heeft een meetbaar gevolg (toestand of macht) en de druk van haar probleem bij de uitvinding en 100 jaar later.',
  "select run_id||':'||knoop,'uitvinding zonder meetbaar gevolg of meting van haar probleem' from sim_uitvinding where module='geschiedenis_z45' and (druk_voor is null or druk_na is null or (json_extract(gevolg,'$.toestand')='{}' and json_extract(gevolg,'$.macht')='{}'))"),
]
for code, oms, sq in TOETS:
    S['regel'] += c.execute("insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
        (code, 'simulatie', oms, sq, 'r_Z45.py (Rogier 2026-11-02: meetbaar effect, gebruik, gewone tijd)', 'architect, in opdracht van Rogier (2026-11-02)', 'actief', 'fout')).rowcount
S['regel'] += c.execute("insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
    ('R-sim_convergentie', 'simulatie', 'Signaal: minder dan 80 procent van de Z45-geschiedenissen bereikt Het Gewone vóór 5000.',
     "select 'geschiedenis_z45','maar '||round(100.0*sum(json_extract(scores,'$.gewoon') is not null)/count(*))||'% bereikt Het Gewone' from sim_run where module='geschiedenis_z45' group by module having 1.0*sum(json_extract(scores,'$.gewoon') is not null)/count(*)<0.8",
     'r_Z45.py', 'architect, in opdracht van Rogier (2026-11-02)', 'actief', 'signaal')).rowcount
S['tech_gebeurtenistype'] += c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',
    ('gesch_techniek_verloren', MOD, 'Magische techniek gaat verloren omdat haar bron opdroogt (zie sim_uitvinding.verloren).', 'alleen gave- en zegelsteentechniek', 'GESCH4-verval', 'aanname (moduleontwerp Z45, bron GESCH4-verval)')).rowcount

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
        seed = SEED0 + i; rid = f'Z45-GESCH-{i:04d}'; epi = f'simulatie ({rid}, seed {seed})'
        o = G.run(seed); ms = [x['M'] for x in o['log']]
        gekozen = int(i in GEKOZEN); n = 0
        U = o['uitvindingen']
        scores = dict(fasen=len(o['fasen']), onopgelost=len(o['onopgelost']), uitvindingen=[(u['code'], u['jaar']) for u in U],
                      uit_nood=sum(not u['noodzaak'].startswith('aantrekkelijk') for u in U), gewoon=o['gewoon'],
                      per_eeuw={f'{a}-{b}': round(sum(a <= u['jaar'] < b for u in U) / ((b - a) / 100), 2) for a, b in ((801, 1500), (1500, 2500), (2500, 3500), (3500, 5000))},
                      verloren=[u['code'] for u in U if u['verloren']],
                      probleem_kleiner=sum(1 for u in U if u['druk_voor'] is not None and u['druk_voor'] > .3 and u['druk_na'] < u['druk_voor']), magie_min=min(ms), magie_eind=ms[-1], golven=golven(ms),
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
                    gevolg=json.dumps(u['gevolg'], ensure_ascii=False), epistemiek=epi, probleem=u['probleem'], druk_voor=u['druk_voor'], druk_na=u['druk_na'],
                    macht_voor=u['macht_voor'], macht_na=u['macht_na'], kennis=u['kennis'], verspreid_jaar=u['verspreid_jaar'], verloren=u['verloren'],
                    verloren_door=u['verloren_door'])); n += 1
                if u['verloren']:
                    geb(rid, epi, u['verloren'], 'gesch_techniek_verloren', u['uitvinder'], u['code'], f"{u['naam']} gaat verloren: {u['verloren_door']}. Opvolger: {B.OPVOLGER.get(u['code'], 'geen')}.", None, 'GESCH4-verval'); n += 1
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
            (rid, MOD, 9, seed, 1, None, n or len(o['fasen']) + len(U), json.dumps(scores, ensure_ascii=False), None, None, gekozen, 'r_Z45.py', epi)).rowcount

# ---------- 4 keuzes voor Rogier ----------
KEUZES = [
 ('KEUZE-Z45-kharvos', 'wereld', 'Kharvos is de brug naar gewone techniek', 'Bevestig dat smeden, raderwerk en koper via Kharvos binnenkomen (handel, oorlog, spionage), omdat de Harrow voor machines koos.', 'BESLUIT-3;REG-kharvos-B1;ORIGIN-Z1-harrow',
  'Rogier (2026-11-02): yes, maar het moet passend zijn bij de nieuwe uitvindingen.'),
 ('KEUZE-Z45-gewoon', 'wereld', 'De wereld groeit naar een gewone tijd', 'Bevestig de eis dat minstens 80 procent van de geschiedenissen vóór 5000 Het Gewone bereikt (stoom, drukpers, elektriciteit, vaccin en spoor). Nu: 87 procent, gemiddeld rond 3661.', 'TECH-GESCH-12-V4',
  'Rogier (2026-11-02): het moet na een tijdje wel grosso modo naar de normale tijd evolueren, en niet te raar zijn.'),
 ('KEUZE-Z45-tempo', 'wereld', 'Uitvinden gaat traag tot de kennis groeit', 'Bevestig het patroon: rond 0,27 grote uitvinding per eeuw in de eerste zeven eeuwen na 801, rond 1 per eeuw vlak voor Het Gewone.', 'TECH-GESCH-11',
  'Rogier (2026-11-02): in de middeleeuwen ging innovatie heel langzaam; kijk wat de patronen zijn.'),
 ('KEUZE-Z45-effect', 'wereld', 'Elke uitvinding lost iets op en verschuift macht', 'Bevestig dat een uitvinding wordt gemeten op het probleem waarvoor ze kwam. Nu: 99 procent heeft een meetbaar gevolg, 84 procent geeft de uitvinder meer macht, en waar het probleem speelde is het 100 jaar later in 63 procent kleiner.', 'TECHNO-REGEL-V4',
  'Rogier (2026-11-02): de uitvinding moet een meetbaar effect hebben, problemen oplossen en het verhaal voortstuwen of machtsbalansen verbeteren.'),
 ('KEUZE-Z45-kolen', 'wrijving', 'Heeft Velmara steenkool?', 'Beslis of er steenkool is. De canon zegt alleen dat er geen brandstof is voor de scheepskernen (ORIGIN-2). Zonder kolen draait stoom op hout, en dat kapt de wouden van de Aelthir.', 'ORIGIN-2;PLEK-Z4-nm-5-Z5b',
  'Correctie Z45: in Z44 las de architect ORIGIN-2 te ruim.'),
]
for code, soort, ond, aanb, raakt, citaat in KEUZES:
    bestaat(raakt)
    S['keuze'] += c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',
        (code, soort, ond, aanb, raakt, 'open', 'r_Z44.py', citaat)).rowcount
if not c.execute("select 1 from logboek where wat like 'Ronde Z45:%'").fetchone():
    c.execute('insert into logboek(datum,wat) values(?,?)', (DT, 'Ronde Z45: gebruik, gewone uitvindingen, kennis en verspreiding (z45/boom.py, z45/geschiedenis.py). 11 gewone knopen met Velmara-voorganger en Kharvos-brug; gebruik, aards equivalent, tijdperk en soort bij alle knopen (migratie 012); correctie op Z44 (stoom en kruit mogelijk, kolen open). Regels R-tech_gebruik, R-sim_effect, R-sim_convergentie (signaal); R-tech_boom kent nu A|B. 5 motorregels GESCH4-*, 1000 runs Z45-GESCH-0001..1000, zes gekozen runs met alle details, vijf open keuzes KEUZE-Z45-*. Alles voorstel of simulatie.')); S['logboek'] += 1
afgeleid.bouw(c); c.commit()
print(dict(S))
