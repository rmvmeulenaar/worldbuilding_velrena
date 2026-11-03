# Ronde Z42: de geschiedenismotor na 801.
# Legt een motor vast die uit de regels van de canon geschiedenis maakt van 801 tot 5000: zeven motoren van geschiedenis
# (bevolking en voedsel, edelen, geld en staat, buren en oorlog, uitvindingen, ziekte en klimaat, geloof), golvende magie
# die nooit verdwijnt (bodem: Orrim-steen; golf: gesloten dragerlijnen; pieken: fragmenten), wetten die ingaan en vervallen,
# heersende huizen met afstamming, rustige tijden, wezens die van slachtoffer tot sprookje schuiven, en hoe het verhaal
# van 801 per eeuw verschuift. Alles is simulatie of aanname: niets hiervan is canon tot Rogier besluit (KEUZE-Z42-*).
# Alleen bestaande tabellen: sim_regel, tech_gebeurtenistype, sim_run, sim_gebeurtenis, keuze, logboek.
# Gebouwd door de architect op verzoek van Rogier (2026-11-02). Idempotent, additief: niets verwijderd, roman en Kern niet
# aangeraakt. Gebruik: DB=kopie.db python3 r_Z42.py   (motor: z42/geschiedenis.py, uitleg: z42/LEESMIJ.md)
import sqlite3, shutil, os, sys, json, collections, subprocess
W = os.path.dirname(os.path.abspath(__file__)); os.chdir(W); sys.path[:0] = [W, os.path.join(W, 'migraties'), os.path.join(W, 'z42')]
import afgeleid, migreer, geschiedenis as G
DT = '2026-11-02'; RD = 'Z42'; DB = os.environ.get('DB', 'canon.db'); MOD = 'geschiedenis'
N_RUNS = 1000; SEED0 = 420000; GEKOZEN = [3, 1, 2, 5, 8, 13]
if DB == 'canon.db' and not os.path.exists('canon_backup_Z42.db'): shutil.copy('canon.db', 'canon_backup_Z42.db')
c = sqlite3.connect(DB); migreer.draai(c)
S = collections.Counter()
CODES = {r[0] for r in c.execute('select code from canon')}
def bestaat(*codes):
    for x in codes:
        for y in (x or '').split(';'):
            if y and y not in CODES: sys.exit(f'bron {y} bestaat niet in canon')

# ---------- 1 regels van de motor (sim_regel) ----------
REGELS = [
 ('GESCH-filter', 'Na 801 verslapt de X-filter: het aandeel jongens schuift per 20 jaar met een vaste fractie naar de helft; het aantal dragers blijft gelijk, dus een steeds kleiner deel van de mannen kan lading dragen.', 'filter', '0,02 tot 0,06 per stap (per run getrokken)', 'ORIGIN-10-Z36;BESLUIT-Z36-4'),
 ('GESCH-bodem', 'De magie heeft een bodem: Orrim sterven niet maar verstenen tot groeve, in hun lichaam groeit Sterrensteen, en wat er gemijnd wordt houdt de lading in de wereld.', 'bodem', '0,12 plus mijnopbrengst', 'D1-orrim-dood;VOLK-orrim;D1-orrim-geld'),
 ('GESCH-golf', 'De magie golft met de edelen: sluiten de dragerlijnen zich af, dan komt de lading samen; opent de wereld zich door handel en steden, dan verdunt ze.', 'golf', '0,55 maal concentratie', 'ORIGIN-10-Z36;GAVE-Z37-ja'),
 ('GESCH-piek', 'Vondsten laten de magie kort oplaaien: de negen cellen van Hesta, de reservekern van de Harrow, splinters Sterrensteen. Een piek dooft met een kwart per stap.', 'puls', '0,2 tot 0,5', 'YSA-Z21-3;ORIGIN-Z1-harrow;ORIGIN-8'),
 ('GESCH-verdunning', 'Over de eeuwen verdunt de geërfde lading omdat niets haar voedt zoals het Zegel deed; de golf wordt kleiner maar nooit nul.', 'verdun', '0,35 + 0,65·e^(-(jaar-801)/1500)', 'BESLUIT-2;BESLUIT-Z36-4'),
 ('GESCH-bevolking', 'Bevolking groeit tot het voedsel op is; techniek en dragers op de akkers verhogen het voedsel; honger is druk boven 93 procent.', 'groei', '0,12 tot 0,22 per stap', 'FASE-overvloed'),
 ('GESCH-elite', 'Edelen groeien in aantal als het volk goedkoop is; te veel edelen en een lege kas geven een strijd om posities (golf van eeuwen).', 'elite', 'drempel 1,4', 'FASE-markt'),
 ('GESCH-staat', 'De staat leeft van belasting naar bevolking en geloof en betaalt de edelen; zakt de kas onder 0,12, dan is ze blut.', 'kas', 'drempel 0,12', 'FASE-barsten'),
 ('GESCH-buren', 'Kharvos wordt elke stap hongeriger; is het sterker dan kas maal bevolking maal lading, dan valt het aan.', 'buren', '0,5 tot 1,5 honger', 'REG-kharvos-B1;ORIGIN-Z1-harrow'),
 ('GESCH-techniek', 'Techniek groeit in rust en openheid en trager waar magie het werk doet; bij vijf drempels komt een uitvinding.', 'techniek', 'drempels 0,2 0,35 0,5 0,65 0,8', 'ORIGIN-4;ORIGIN-2'),
 ('GESCH-geloof', 'Geloof groeit met de macht van de kerk en slijt met de techniek; onder 0,38 wankelt het.', 'geloof', 'drempel 0,38', 'REGEL-seksuele-normen'),
 ('GESCH-verhaal801', 'Het verhaal van 801 wordt per stap minder trouw verteld; sneller als kerk, huizen of dragers vertellen, trager met het geheugen van de Aelthir en met techniek; kerk en huizen maken er een heilige van, dragers en buren een heks.', 'trouw', 'start 0,6', 'BESLUIT-Z36-4;BESLUIT-Z18b-2;VOLK-aelthir-V5'),
 ('GESCH-wezens', 'Lading die wordt doorgegeven aan wie haar niet kan dragen, maakt nachtvlerken; de omweg werkt op slapers. Een nachtvlerk ontlaadt via huidcontact op de borst van een slaper (YSA-Z18-1); dat is horror en nooit seks, want een slaper kan niet instemmen (harde lijn). Wezenlijnen schuiven van slachtoffer naar groep, volk, monster en sprookje; afzondering versnelt dat.', 'nacht', '0,12 maal magie maal openheid maal niet-dragers', 'ORIGIN-WAAROM-9;NAV-wormwording-B1;BESLUIT-Z6-WRIJ-065'),
 ('GESCH-rijm', 'Een noodoplossing moet op minstens 3 van 5 assen (beslisser, betaler, vervalst, ontdekt, schaal) verschillen van de vorige fase, zoals R-rijm_assen voor fase_rijm.', 'rijm', '3 van 5', 'BESLUIT-Z36-4'),
 ('GESCH-spiraal', 'Een noodoplossing komt pas na 600 jaar terug; uitvindingen, vondsten, het kleine zegel en het Orrim-recht maar één keer.', 'spiraal', '600 jaar', 'BESLUIT-Z36-4'),
 ('GESCH-rust', 'Twee eeuwen zonder crisis is een rustige tijd: verhalen op de schaal van huis en dorp.', 'rust', '200 jaar', 'FASE-overvloed'),
 ('GESCH-wetten', 'Wetten volgen de verhouding: boven 12 procent jongens vervalt de Deelwet, boven 25 procent krijgen mannen bezit, boven 40 procent erven zonen en dochters gelijk. Andere wetten komen en gaan met de noodoplossingen.', 'wet', '0,12 0,25 0,40', 'WET-deelwet-recht;WET-wie-gewone-man;WET-erfrecht'),
]
for code, oms, par, waarde, bron in REGELS:
    bestaat(bron)
    S['sim_regel'] += c.execute('insert or ignore into sim_regel(code,module,omschrijving,parameter,waarde,bron_code,aanname,actief_van,actief_tot,status,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?)',
        (code, MOD, oms, par, waarde, bron, 1, 801, None, 'voorlopig', f'aanname (motorontwerp Z42, bron {bron})')).rowcount

# ---------- 2 soorten gebeurtenissen (tech_gebeurtenistype) ----------
CRISIS = {'honger':'GESCH-bevolking','elitestrijd':'GESCH-elite','bankroet':'GESCH-staat','invasie':'GESCH-buren','epidemie':'GESCH-bevolking',
          'uitvinding':'GESCH-techniek','geloof':'GESCH-geloof','opleving':'GESCH-golf','orrim':'GESCH-bodem','wezens':'GESCH-wezens','vondst':'GESCH-techniek'}
TYPES = [(f'gesch_crisis_{k}', f'Crisis ({k}): de druk passeert de drempel en de machtigste partij kiest een noodoplossing.', 'rijmt op >=3 assen met de vorige fase', v) for k, v in CRISIS.items()]
TYPES += [
 ('gesch_gebeurtenis', 'Een toevallige gebeurtenis (vondst, klimaat, schimmel, trek, archief).', 'staat in GEBEURTENIS van z42/geschiedenis.py', 'GESCH-piek'),
 ('gesch_wet_in', 'Een wet gaat in.', 'een wet gaat pas uit als ze in is', 'GESCH-wetten'),
 ('gesch_wet_uit', 'Een wet vervalt.', 'alleen een geldende wet kan vervallen', 'GESCH-wetten'),
 ('gesch_huis', 'Een huis ontstaat (met ouderhuis), gaat heersen of valt.', 'elk nieuw huis heeft een ouder', 'GESCH-elite'),
 ('gesch_rust', 'Een rustige tijd van minstens 200 jaar.', 'geen crisis binnen de periode', 'GESCH-rust'),
 ('gesch_toestand', 'Toestand van de wereld per eeuw: magie, techniek, verhouding, geloof, macht.', 'magie > 0', 'GESCH-bodem'),
 ('gesch_versie801', 'Hoe het verhaal van 801 vanaf dit jaar verteld wordt.', 'trouw daalt behalve na een vondst', 'GESCH-verhaal801'),
 ('gesch_wezen', 'Een wezenlijn schuift een stadium op.', 'stadium daalt nooit', 'GESCH-wezens'),
]
for code, oms, inv, bron in TYPES:
    S['tech_gebeurtenistype'] += c.execute('insert or ignore into tech_gebeurtenistype(code,module,omschrijving,invariant,bron_code,epistemiek) values(?,?,?,?,?,?)',
        (code, MOD, oms, inv, bron, f'aanname (moduleontwerp Z42, bron {bron})')).rowcount

# ---------- 3 runs (sim_run) en details van de gekozen runs (sim_gebeurtenis) ----------
EV_CANON = {'kern_valt':'ORIGIN-Z1-harrow','kern_in_worm':'ORIGIN-Z1-harrow','negen_cellen':'YSA-Z21-3','splinter':'ORIGIN-8','grote_drager':'GAVE-Z37-ja',
            'schimmeljaar':'HORROR-SKELET-Z9-6','aelthir_trek':'VOLK-aelthir-V5','nachtplaag':'ORIGIN-WAAROM-9','archief':'REG-stille'}
HUI = dict(G.HUIZEN_801)
bestaat(*EV_CANON.values(), *G.LIJN_CANON.values(), *HUI.values(), *G.WET_801)
def golven(ms):
    n = 0; lo = hi = ms[0]
    for v in ms:
        if v > hi: hi = v
        if hi - v >= .12 and hi - lo >= .12: n += 1; lo = hi = v
        if v < lo: lo = hi = v
    return n
def gebeurtenis(rid, epi, jaar, typ, actor, doel, detail, canon, oorzaak):
    S['sim_gebeurtenis'] += c.execute('insert or ignore into sim_gebeurtenis(run_id,module,jaar,seizoen,type_code,actor,doel,plek_code,detail,canon_code,status,epistemiek,oorzaak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (rid, MOD, jaar, '-', typ, actor or '-', doel or '-', '-', detail, canon, 'voorlopig', epi, oorzaak)).rowcount
if c.execute('select count(*) from sim_run where module=?', (MOD,)).fetchone()[0] < N_RUNS:
    for i in range(1, N_RUNS + 1):
        seed = SEED0 + i; rid = f'Z42-GESCH-{i:04d}'; epi = f'simulatie ({rid}, seed {seed})'
        o = G.run(seed); ms = [x['M'] for x in o['log']]
        gaps = [b['van'] - a['van'] for a, b in zip(o['fasen'], o['fasen'][1:])]
        mach = next((x['jaar'] for x in o['log'] if x['T'] > .6), None)
        scores = dict(fasen=len(o['fasen']), magie_min=min(ms), magie_max=max(ms), magie_eind=ms[-1], golven=golven(ms),
                      machinetijd_vanaf=mach, langste_stilte=max(gaps or [0]), rustige_jaren=sum(r['tot'] - r['van'] for r in o['rust']),
                      heersers=len({h['huis'] for h in o['huislog'] if h['soort'] == 'heerst'}), huizen=len(o['huizen']),
                      wetten_in=sum(w['soort'] == 'in' for w in o['wetten']), wetten_uit=sum(w['soort'] == 'uit' for w in o['wetten']),
                      trouw801_eind=o['log'][-1]['f'], parameters=o['p'])
        gekozen = int(i in GEKOZEN)
        n = 0
        if gekozen:
            for f in o['fasen']:
                det = (f"{f['naam']}. Verzwegen: {f['vervalst']}. Ontdekt: {f['ontdekt']}. Schaal: {f['schaal']}. Blijvend: {f['blijvend']} "
                       f"Tijd: {f['era']}. Heersend huis: {f['heerser']}. Rijm: {f['rijm']} van 5 assen anders{'; keert terug na 600 jaar' if f['terug'] else ''}.")
                gebeurtenis(rid, epi, f['van'], f"gesch_crisis_{f['crisis']}", f['beslisser'], f['betaler'], det, None, CRISIS[f['crisis']]); n += 1
            for g in o['gebeurd']:
                gebeurtenis(rid, epi, g['jaar'], 'gesch_gebeurtenis', '-', g['id'], g['tekst'], EV_CANON.get(g['id']), 'GESCH-piek'); n += 1
            for w in o['wetten']:
                tekst = w['tekst'] or 'vervalt'
                gebeurtenis(rid, epi, w['jaar'], f"gesch_wet_{w['soort']}", w['door'], w['wet'], tekst, w['wet'] if w['wet'] in CODES else None, 'GESCH-wetten'); n += 1
            for h in o['huislog']:
                gebeurtenis(rid, epi, h['jaar'], 'gesch_huis', h['huis'], h.get('ouder') or '-', f"{h['soort']}" + (f": {h['waarom']}" if h.get('waarom') else ''), HUI.get(h['huis']), 'GESCH-elite'); n += 1
            for r in o['rust']:
                gebeurtenis(rid, epi, r['van'], 'gesch_rust', '-', '-', f"Rustige tijd {r['van']} tot {r['tot']} (tijd van de {r['tijd']}); verhalen op de schaal van huis en dorp: {r['genres']}.", None, 'GESCH-rust'); n += 1
            vorige = None; stad = {}
            for x in o['log']:
                if (x['jaar'] - 801) % 100 == 0:
                    det = json.dumps(dict(magie=x['M'], bodem=x['bodem'], techniek=x['T'], jongens=x['r'], honger=x['P'], kas=x['S'], edelen=x['E'],
                                          geloof=x['L'], openheid=x['O'], orrim=x['orrim'], beschaving=x['C'], tijd=x['era'], heerser=x['heerser'],
                                          wetten=x['wetten'], macht=x['macht']), ensure_ascii=False)
                    gebeurtenis(rid, epi, x['jaar'], 'gesch_toestand', '-', '-', det, None, 'GESCH-bodem'); n += 1
                v = G.versie(x['f'], x['tak'])
                if v != vorige: gebeurtenis(rid, epi, x['jaar'], 'gesch_versie801', '-', '-', v, 'BESLUIT-Z36-4', 'GESCH-verhaal801'); vorige = v; n += 1
                for k, st in x['lijn'].items():
                    if stad.get(k) != st:
                        gebeurtenis(rid, epi, x['jaar'], 'gesch_wezen', k, ['slachtoffer','groep','volk','monster','sprookje'][st], G.LIJN[k][st], G.LIJN_CANON[k], 'GESCH-wezens'); stad[k] = st; n += 1
        S['sim_run'] += c.execute('insert or ignore into sim_run(run_id,module,fase_nr,seed,geldig,reden,n_gebeurtenis,scores,pareto_rang,gewogen,gekozen,bron,epistemiek) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (rid, MOD, 9, seed, 1, None, n or len(o['fasen']) + len(o['gebeurd']), json.dumps(scores, ensure_ascii=False), None, None, gekozen, 'r_Z42.py', epi)).rowcount

# ---------- 4 keuzes voor Rogier ----------
KEUZES = [
 ('KEUZE-Z42-bodem', 'wereld', 'De magie verdwijnt nooit: de Orrim zijn de bodem', 'Bevestig dat de magie na 801 nooit nul wordt omdat Orrim-steen blijft groeien, of kies een andere bron voor de bodem.', 'GESCH-bodem;D1-orrim-dood;VOLK-orrim',
  'Rogier (2026-11-02): de magie moet op een bepaald niveau blijven, golvend, en nooit verdwijnen.'),
 ('KEUZE-Z42-golf', 'wereld', 'De magie golft met gesloten en open tijden', 'Bevestig dat gesloten dragerlijnen de magie laten oplaaien en handel en steden haar verdunnen.', 'GESCH-golf;ORIGIN-10-Z36',
  'Rogier (2026-11-02): golvend, en het komt in fasen terug.'),
 ('KEUZE-Z42-verhouding', 'wereld', 'Na 801 verslapt de filter langzaam', 'Bevestig dat de verhouding over eeuwen naar de helft schuift en dat de Deelwet en de rechteloosheid van gewone mannen daardoor vervallen.', 'GESCH-filter;GESCH-wetten;ORIGIN-10-Z36;WET-deelwet-recht',
  'Rogier (2026-11-02): die verhouding moeten we beter krijgen, en mensen moeten gaven gewoon kunnen doorgeven.'),
 ('KEUZE-Z42-tijden', 'verhaal', 'De tijden na 801 als simulatie of als canon', 'Laat de 1000 geschiedenissen en de zes gekozen runs eerst door een ander nakijken; kies daarna welke run of welke tijden canon worden.', 'GESCH-rijm;GESCH-spiraal',
  'Rogier (2026-11-02): als het goed is, gaan we het als canon inzetten; de test is dat een ander de database nakijkt.'),
 ('KEUZE-Z42-rust', 'verhaal', 'Rustige tijden horen bij de geschiedenis', 'Bevestig dat eeuwen zonder crisis een eigen soort tijd zijn, met verhalen op de schaal van huis en dorp.', 'GESCH-rust',
  'Rogier (2026-11-02): soms is dat zo; je kan ook in rustige tijden mooie verhalen vertellen.'),
 ('KEUZE-Z42-mythe', 'verhaal', 'Het verhaal van 801 verbastert per eeuw', 'Bevestig de reeks van trouw naar kinderrijm en de twee takken (heilige of heks) naar wie vertelt.', 'GESCH-verhaal801;BESLUIT-Z18b-2',
  'Rogier (2026-11-02): over vele generaties worden het andere dingen, en dat is leuk.'),
 ('KEUZE-Z42-bodem-bron', 'wereld', 'Waar komt de bodem van de magie vandaan: steen of vonkcellen?', 'Verplaats de bodem van de Orrim-steen naar de vonkcellen: levende, erfelijke cellen die verdunnen maar niet uitsterven zolang er dragerlijnen zijn (YSA-Z18-1, ORIGIN-10-Z36). De Sterrensteen wordt dan versterker en lezer (ORIGIN-5), en groeit alleen uit mineralen bij Orrim-voortplanting (VOLK-orrim).', 'YSA-Z18-1;ORIGIN-10-Z36;ORIGIN-5;VOLK-orrim;D1-orrim-dood',
  'Review 1 (2026-11-02): groeiende Orrim-steen is nog geen groeiende lading; de bodem is als canonafleiding niet bewezen.'),
 ('KEUZE-Z42-sleutelbreuk', 'wrijving', 'Wanneer brak de instemmingssleutel?', 'Kies één jaar: bij de landing (-1240, HAAK-Z17-zegel-6, vastgesteld) of bij de val van de Sterrensteen (-480, ORIGIN-9 en ORIGIN-WAAROM-9, voorlopig). De motor na 801 hangt er niet van af, de magie vóór 0 wel.', 'HAAK-Z17-zegel-6;ORIGIN-9;ORIGIN-WAAROM-9',
  'Gevonden bij het lezen voor Z42: twee rijen noemen een ander jaar voor dezelfde breuk.'),
 ('KEUZE-Z42-vesanath', 'wrijving', 'Ves-Anath ontruimd in 603 of in 610?', 'Kies één jaar. GEB-ves-anath-ontruimd zegt 603, ZINT-Z4-tijdperk-11-b zegt 610.', 'GEB-ves-anath-ontruimd;ZINT-Z4-tijdperk-11-b',
  'Gevonden bij het lezen voor Z42.'),
]
for code, soort, ond, aanb, raakt, citaat in KEUZES:
    bestaat(raakt.replace('GESCH-bodem','').replace('GESCH-golf','').replace('GESCH-filter','').replace('GESCH-wetten','').replace('GESCH-rijm','').replace('GESCH-spiraal','').replace('GESCH-rust','').replace('GESCH-verhaal801',''))
    S['keuze'] += c.execute('insert or ignore into keuze(code,soort,onderwerp,aanbeveling,raakt,status,bron,citaat) values(?,?,?,?,?,?,?,?)',
        (code, soort, ond, aanb, raakt, 'open', 'r_Z42.py', citaat)).rowcount

# ---------- 5 veiligheid na review (2026-11-02): rijen die al bestonden bijwerken ----------
def wijz(code, veld, oud, nieuw):
    S['wijziging'] += c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',
        (RD, code, 'gewijzigd', veld, oud, nieuw, DT, 'r_Z42.py')).rowcount
nieuw = dict((x[0], x[1]) for x in REGELS)['GESCH-wezens']
oud = c.execute("select omschrijving from sim_regel where code='GESCH-wezens'").fetchone()[0]
if oud != nieuw:
    c.execute("update sim_regel set omschrijving=? where code='GESCH-wezens'", (nieuw,)); wijz('GESCH-wezens', 'sim_regel.omschrijving (harde lijn expliciet)', oud, nieuw)
zp = G.WET['smeden'][1]
for i, d in c.execute("select id,detail from sim_gebeurtenis where module=? and doel='W-zegelplicht' and detail!=?", (MOD, zp)).fetchall():
    c.execute('update sim_gebeurtenis set detail=? where id=?', (zp, i)); wijz(f'sim_gebeurtenis:{i}', 'detail (harde lijn expliciet)', d, zp)
if not c.execute("select 1 from logboek where wat like 'Ronde Z42:%'").fetchone():
    c.execute('insert into logboek(datum,wat) values(?,?)', (DT, 'Ronde Z42: geschiedenismotor na 801 (z42/geschiedenis.py). 17 motorregels (sim_regel GESCH-*), 19 gebeurtenissoorten (gesch_*), 1000 runs (Z42-GESCH-0001..1000), zes gekozen runs met alle details (fasen, gebeurtenissen, wetten, huizen, rustige tijden, toestand per eeuw, verhaal van 801, wezens), acht open keuzes (KEUZE-Z42-*, waarvan twee wrijvingen in de bestaande canon). Alles simulatie of aanname; niets in de canon gezet. Uitleg: z42/LEESMIJ.md.')); S['logboek'] += 1
afgeleid.bouw(c); c.commit()
print(dict(S))
