# Ronde Z43: de geschiedenis verklaart zichzelf.
# Na review 1 van Z42 (z42/REVIEW_1.md): elke fase krijgt als eigen velden de oorzaak (welke toestand de drempel passeerde),
# de actor en zijn macht, het mechanisme en de handhaver, het gedeelde mechanisme waarmee ze rijmt, waarvan ze erft en
# wat er 60 jaar later anders is. Wetten krijgen een wetgever met macht, rechtsgebied, handhaver, aanleiding en verval;
# huizen bloed, aanspraak en gezag. Motor: z43/geschiedenis.py. Nieuwe tabellen sim_fase, sim_wet, sim_huis (migratie 010),
# elk gebruikt door een view en een toetsregel. Alles simulatie of aanname; niets in de canon gezet.
# Gebouwd door de architect op verzoek van Rogier (2026-11-02). Idempotent, additief. Gebruik: DB=kopie.db python3 r_Z43.py
import sqlite3, shutil, os, sys, json, collections, importlib.util
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties')]
import afgeleid, migreer
_s = importlib.util.spec_from_file_location('z43_geschiedenis', os.path.join(W, 'z43', 'geschiedenis.py')); G = importlib.util.module_from_spec(_s); _s.loader.exec_module(G)
DT = '2026-11-02'; RD = 'Z43'; DB = os.environ.get('DB', 'canon.db'); MOD = 'geschiedenis_z43'
N_RUNS = 1000; SEED0 = 420000; GEKOZEN = [3, 1, 2, 5, 8, 13]   # dezelfde seeds als Z42, zodat je kunt vergelijken
if DB == 'canon.db' and not os.path.exists('canon_backup_Z43.db'): shutil.copy('canon.db', 'canon_backup_Z43.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
CODES = {r[0] for r in c.execute('select code from canon')}
def bestaat(*codes):
    for x in codes:
        for y in (x or '').split(';'):
            if y and y not in CODES: sys.exit(f'bron {y} bestaat niet in canon')

# ---------- 1 regels van de motor (sim_regel) ----------
REGELS = [
 ('GESCH2-macht', 'Een noodoplossing kan alleen doorgezet worden door wie minstens een tiende van de macht heeft; anders blijft de crisis onopgelost en komt ze 200 jaar niet terug.', 'macht_min', '0,10', 'MACHT-twee-soorten-mannen;REGEL-regeringsvorm-Z12'),
 ('GESCH2-rijm', 'Een fase rijmt: ze deelt minstens één mechanisme met een eerdere fase (ook de fasen tot 801 uit fase_rijm) en verschilt op minstens 3 van 5 assen van de vorige; 3 of 4 assen krijgen voorrang.', 'rijm', '1 mechanisme, 3 assen', 'BESLUIT-Z36-4;FASE-noodtoestand-Z38'),
 ('GESCH2-erfenis', 'Elke fase noemt de jongste eerdere fase of gebeurtenis die raakte aan wat haar crisis voedt; grote eenmalige gebeurtenissen werken 400 jaar door, andere 100.', 'venster', '100 of 400 jaar', 'ORIGIN-Z1-harrow;YSA-Z21-3'),
 ('GESCH2-gevolg', 'Het gevolg van een fase is het verschil in toestand en macht tussen vlak ervoor en 60 jaar erna.', 'gevolg', '60 jaar', 'FASE-markt'),
 ('GESCH2-wetverval', 'Een wet vervalt door opheffing, door een voorwaarde (de verhouding), of als haar wetgever 60 jaar lang minder dan 6 procent van de macht heeft; na 200 jaar is een wet gewoonte en vervalt ze alleen nog door opheffing; een vervallen wet komt pas na 300 jaar terug.', 'wet_verval', '0,06; 60 jaar; 200 jaar; 300 jaar', 'WET-deelwet-recht;WET-wie-gewone-man'),
 ('GESCH2-elite', 'Edelen zakken ook weer af (sterfte, armoede, verval): drie procent van het overschot per 20 jaar.', 'afzakken', '0,03', 'FASE-markt'),
 ('GESCH2-steden-kerk', 'De steden groeien met techniek en handel; de kerk groeit en krimpt met het geloof.', 'groei', '0,015 en 0,01', 'REGEL-regeringsvorm-Z12'),
]
for code, oms, par, waarde, bron in REGELS:
    bestaat(bron)
    S['sim_regel'] += c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
        (code, MOD, oms, par, waarde, bron, 1, 801, None, 'voorlopig', f'aanname (motorontwerp Z43, bron {bron})')).rowcount
S['tech_gebeurtenistype'] += c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',
    ('gesch_onopgelost', MOD, 'Een crisis waarvoor niemand met genoeg macht een oplossing heeft die rijmt.', 'komt 200 jaar niet terug', 'GESCH2-macht', 'aanname (moduleontwerp Z43, bron GESCH2-macht)')).rowcount

# ---------- 2 toetsregels die de nieuwe tabellen gebruiken (regel) ----------
TOETS = [
 ('R-sim_oorzaak', 'Elke gesimuleerde fase heeft een oorzaak, een erfenis, een gevolg en een beslisser met minstens een tiende van de macht.',
  "select run_id||':'||van,'fase zonder oorzaak, erfenis, gevolg of macht' from sim_fase where oorzaak is null or erft_van is null or gevolg is null or actor_macht is null or actor_macht<0.10"),
 ('R-sim_rijm', 'Elke gesimuleerde fase deelt een mechanisme met een eerdere fase en verschilt op minstens 3 van 5 assen van de vorige.',
  "select run_id||':'||van,'fase rijmt niet: '||coalesce(assen_anders,'?')||' assen anders, gedeeld mechanisme '||coalesce(gedeeld_mechanisme,'geen') from sim_fase where coalesce(assen_anders,0)<3 or gedeeld_mechanisme is null"),
 ('R-sim_wetgever', 'Elke gesimuleerde wet heeft een wetgever met minstens een tiende van de macht, een rechtsgebied en een handhaver; een vervallen wet zegt waardoor.',
  "select run_id||':'||wet||':'||van,'wet zonder wetgever met macht, rechtsgebied, handhaver of reden van verval' from sim_wet where wetgever is null or rechtsgebied is null or handhaver is null or coalesce(wetgever_macht,0)<0.10 or (tot is not null and vervalt_door is null)"),
 ('R-sim_huis', 'Elk gesimuleerd huis na 801 heeft een ouderhuis; elk huis dat heerst heeft een aanspraak.',
  "select run_id||':'||huis||':'||coalesce(gezag_van,''),'huis zonder ouder of aanspraak' from sim_huis where (ouder is null and ontstaan>801) or (gezag_van is not null and aanspraak is null)"),
]
for code, oms, sq in TOETS:
    S['regel'] += c.execute("insert or ignore into regel(code,domein,omschrijving,sql_test,bron,goedgekeurd_door,status,niveau) values(?,?,?,?,?,?,?,?)",
        (code, 'simulatie', oms, sq, 'r_Z43.py (review 1 van Z42)', 'architect, in opdracht van Rogier (2026-11-02)', 'actief', 'fout')).rowcount

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
if c.execute('select count(*) from sim_run where module=?', (MOD,)).fetchone()[0] < N_RUNS:
    for i in range(1, N_RUNS + 1):
        seed = SEED0 + i; rid = f'Z43-GESCH-{i:04d}'; epi = f'simulatie ({rid}, seed {seed})'
        o = G.run(seed); ms = [x['M'] for x in o['log']]
        gekozen = int(i in GEKOZEN); n = 0
        scores = dict(fasen=len(o['fasen']), onopgelost=len(o['onopgelost']), magie_min=min(ms), magie_eind=ms[-1], golven=golven(ms),
                      assen=dict(collections.Counter(f['assen_anders'] for f in o['fasen'])),
                      rijmt_met_canon=sum(not f['rijmt_met'].startswith('fase') for f in o['fasen']),
                      erft_van_801=sum(f['erft_van'].startswith('de toestand') for f in o['fasen']),
                      heersers=len({h['huis'] for h in o['huizen'] if h['gezag_van']}), wetten=len(o['wetten']),
                      rustige_jaren=sum(r['tot'] - r['van'] for r in o['rust']), macht_eind=o['log'][-1]['macht'], parameters=o['p'])
        if gekozen:
            for f in o['fasen']:
                S['sim_fase'] += c.execute('insert or ignore into sim_fase(run_id,module,van,tot,crisis,oplossing,naam,beslisser,macht_sleutel,actor_macht,mechanisme,handhaver,betaler,vervalst,ontdekt,schaal,oorzaak,druk,tweede_druk,erft_van,gedeeld_mechanisme,rijmt_met,assen_anders,gevolg,blijvend,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (rid, MOD, f['van'], f['tot'], f['crisis'], f['oplossing'], f['naam'], f['beslisser'], f['macht_sleutel'], f['actor_macht'], f['mechanisme'], f['handhaver'],
                     f['betaler'], f['vervalst'], f['ontdekt'], f['schaal'], json.dumps(f['oorzaak'], ensure_ascii=False), f['druk'], f['tweede_druk'], f['erft_van'],
                     f['gedeeld_mechanisme'], f['rijmt_met'], f['assen_anders'], json.dumps(f['gevolg'], ensure_ascii=False), f['blijvend'], epi)).rowcount; n += 1
            for w in o['wetten']:
                S['sim_wet'] += c.execute('insert or ignore into sim_wet(run_id,module,wet,tekst,wetgever,macht_sleutel,wetgever_macht,rechtsgebied,handhaver,aanleiding,van,tot,vervalt_door,canon_code,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (rid, MOD, w['wet'], w['tekst'], w['wetgever'], w['macht_sleutel'], w['wetgever_macht'], w['rechtsgebied'], w['handhaver'], w['aanleiding'],
                     w['van'], w['tot'], w['vervalt_door'], w['wet'] if w['wet'] in CODES else None, epi)).rowcount; n += 1
            for h in o['huizen']:
                S['sim_huis'] += c.execute('insert or ignore into sim_huis(run_id,module,huis,ouder,ontstaan,aanspraak,gezag_van,gezag_tot,gevallen,canon_code,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
                    (rid, MOD, h['huis'], h['ouder'], h['ontstaan'], h['aanspraak'], h['gezag_van'], h['gezag_tot'], h['gevallen'], h['canon'], epi)).rowcount; n += 1
            for x in o['onopgelost']:
                geb(rid, epi, x['jaar'], 'gesch_onopgelost', '-', x['crisis'], f"Crisis {x['crisis']} (druk {x['druk']}, oorzaak {json.dumps(x['oorzaak'], ensure_ascii=False)}): {x['reden'] or 'niemand met genoeg macht had een oplossing die rijmt'}.", None, 'GESCH2-macht'); n += 1
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
            (rid, MOD, 9, seed, 1, None, n or len(o['fasen']), json.dumps(scores, ensure_ascii=False), None, None, gekozen, 'r_Z43.py', epi)).rowcount

# ---------- 4 keuzes voor Rogier ----------
KEUZES = [
 ('KEUZE-Z43-macht', 'wereld', 'Alleen wie macht heeft, kan een crisis oplossen', 'Bevestig dat een crisis onopgelost blijft als niemand met genoeg macht een passende oplossing heeft. Dat levert gemiddeld 7 crises per geschiedenis op waarin niemand kan ingrijpen: verhalen over machteloosheid.', 'GESCH2-macht',
  'Review 1 (2026-11-02): waarom kan een artsengilde een wet uitvaardigen? Welke regering erkent die bevoegdheid?'),
 ('KEUZE-Z43-rijm', 'wereld', 'Rijm is continuïteit én verandering', 'Bevestig dat een fase een mechanisme deelt met een eerdere fase en op minstens 3 van 5 assen verschilt. Overweeg dezelfde eis voor fase_rijm tot 801 (R-rijm_assen kent nu alleen de verandering).', 'GESCH2-rijm;FASE-noodtoestand-Z38',
  'Review 1 (2026-11-02): vijf van vijf assen anders is geen rijm maar een andere gebeurtenis.'),
 ('KEUZE-Z43-standen', 'wereld', 'Edelen zakken af, steden groeien met handel, de kerk met het geloof', 'Bevestig deze drie aannames; zonder ze sluit de wereld zich eindeloos af en worden steden nooit sterk.', 'GESCH2-elite;GESCH2-steden-kerk',
  'Gevonden bij het bouwen van Z43: zonder afzakken groeide het aantal edelen onbegrensd.'),
 ('KEUZE-Z43-referentie', 'verhaal', 'Welke motor is de maat: Z42 of Z43?', 'Gebruik Z43 als maat; Z42 blijft staan als eerste versie om tegen te vergelijken (dezelfde seeds).', 'GESCH2-rijm;GESCH2-macht',
  'Rogier (2026-11-02): eerst de geschiedenis zichzelf laten verklaren, daarna de technologieboom.'),
]
for code, soort, ond, aanb, raakt, citaat in KEUZES:
    S['keuze'] += c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',
        (code, soort, ond, aanb, raakt, 'open', 'r_Z43.py', citaat)).rowcount
if not c.execute("select 1 from logboek where wat like 'Ronde Z43:%'").fetchone():
    c.execute('insert into logboek(datum,wat) values(?,?)', (DT, 'Ronde Z43: de geschiedenis verklaart zichzelf (z43/geschiedenis.py, na review 1 van Z42). Nieuwe tabellen sim_fase, sim_wet, sim_huis (migratie 010) met views v_sim_keten, v_sim_wetboek, v_sim_stamboom en regels R-sim_oorzaak, R-sim_rijm, R-sim_wetgever, R-sim_huis. 7 motorregels GESCH2-*, 1000 runs Z43-GESCH-0001..1000 (dezelfde seeds als Z42), zes gekozen runs met alle details, vier open keuzes KEUZE-Z43-*. Alles simulatie of aanname; niets in de canon gezet.')); S['logboek'] += 1
afgeleid.bouw(c); c.commit()
print(dict(S))
