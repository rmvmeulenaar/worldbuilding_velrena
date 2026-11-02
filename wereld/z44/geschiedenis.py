"""Ronde Z44, geschiedenismotor 3: uitvindingen uit de technologieboom (z44/boom.py). Simulatie, geen canon.
Bouwt op Z43. Nieuw: een uitvinding ontstaat pas als de wereld haar mogelijk maakt (vereisten en materiaal), de geschiedenis
haar nodig of aantrekkelijk maakt (noodzaak), en haar gevolg de volgende geschiedenis verandert (effect op toestand en macht,
en latere crises kunnen van een uitvinding erven). De oude drempels op techniek en de lijst drukpers/stoom/ijzer zijn weg.
Wat volgt is de beschrijving van Z43:
Bouwt op z42/geschiedenis.py (dezelfde toestand, gebeurtenissen en noodoplossingen) en voegt toe wat review 1 vroeg:
  1 oorzaak     elke fase legt vast welke toestand de drempel passeerde, met de waarden, en de tweede druk ernaast;
  2 macht       een noodoplossing kan alleen gekozen worden als haar beslisser genoeg macht heeft (aandeel >= MACHT_MIN);
                anders blijft de crisis onopgelost, en dat wordt ook vastgelegd;
  3 mechanisme  per oplossing: hoe ze wordt afgedwongen en wie handhaaft;
  4 gevolg      wat er 60 jaar later anders is (toestand en macht);
  5 rijm        een fase moet minstens één mechanisme delen met een eerdere fase (ook de fasen tot 801 uit fase_rijm)
                én op minstens 3 van 5 assen verschillen van de vorige; voorkeur voor 3 of 4 assen;
  6 erfenis     elke fase noemt de eerdere fase of gebeurtenis waarvan ze een gevolg is;
  7 wetten      elke wet heeft een wetgever met macht, een rechtsgebied, een handhaver en een aanleiding; ze vervalt
                door opheffing, door een voorwaarde (de verhouding) of doordat haar wetgever zijn macht verliest;
                na 200 jaar is ze gewoonte en vervalt ze alleen nog door opheffing;
  8 huizen      bloed (ouderhuis), aanspraak (lading, zwaard, geld, eed) en gezag (van/tot) apart;
  9 waarheid    elke versie van 801 krijgt een label: waar, deels waar, vervalst, mythe, kinderrijm, vergeten;
 10 rust        een rustige tijd wordt per laag beschreven: politiek, economie, samenleving, magie."""
import random, math, sys, json, os
import importlib.util as _iu
_spec = _iu.spec_from_file_location('z42_geschiedenis', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'z42', 'geschiedenis.py'))
Z = _iu.module_from_spec(_spec); _spec.loader.exec_module(Z)
_sb = _iu.spec_from_file_location('z44_boom', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boom.py'))
B = _iu.module_from_spec(_sb); _sb.loader.exec_module(B)
KNOOP = {k['code']: k for k in B.BOOM}
UITVIND_KANS = .06   # per 20 jaar, maal noodzaak en beschaving
STAP, AXES, MENU, WET, LIJN, GEBEURTENIS = Z.STAP, Z.AXES, Z.MENU, Z.WET, Z.LIJN, Z.GEBEURTENIS
HUIZEN_801, PLAATS, WET_801, LIJN_CANON, RUST_GENRES = Z.HUIZEN_801, Z.PLAATS, Z.WET_801, Z.LIJN_CANON, Z.RUST_GENRES
MACHT_MIN = .10      # aandeel macht dat een beslisser nodig heeft om een oplossing door te zetten
WET_VERVAL = .06     # onder dit aandeel verliest een wet de wetgever die haar draagt
GEVOLG_STAPPEN = 3   # 60 jaar
GEWOONTE = 200      # na 200 jaar is een wet gewoonterecht en vervalt ze niet meer vanzelf

# Mechanismen van de fasen tot 801, gelezen uit fase_rijm.mechanisme (één of twee per fase)
CANON_MECH = [('0 Voortijd', {'namens-beslissen', 'verbergen'}), ('1 Overvloed', {'erven', 'verdelen'}), ('2 Vonk', {'lading-is-macht'}),
              ('3 Brand', {'binden', 'namens-beslissen', 'verbergen'}), ('4 Noodtoestand', {'registreren'}), ('5 Ontvangst', {'geloof-maakt-wet', 'verbergen'}),
              ('6 Markt', {'lichaam-is-waar'}), ('7 Barsten', {'noodwet'}), ('801 Heden', {'namens-beslissen'})]
# per oplossing: (machtsleutel, mechanismen, handhaver, hoe het wordt afgedwongen)
OPL = {
 'graanwet': ('staat', {'verdelen','noodwet'}, 'de schuurwachten van de kroon', 'de kroon verzegelt de schuren en int de oogst in natura'),
 'trek': ('volk', {'verdelen'}, 'niemand: wie gaat, gaat', 'hele dorpen pakken op voordat iemand het kan verbieden'),
 'dragersakkers': ('dragers', {'lading-is-macht','lichaam-is-waar'}, 'de dragers zelf', 'dragers ontladen in de akkers; wie oogst wil, huurt hun lading'),
 'kloostermaal': ('kerk', {'registreren','geloof-maakt-wet'}, 'de kloosterboeken', 'wie eet, wordt ingeschreven, en het register houdt hem vast'),
 'burgeroorlog': ('huizen', {'erven','namens-beslissen'}, 'de huislegers', 'de neven bewapenen hun lijfwachten; de opvolging wordt op het veld beslist'),
 'verbanning': ('staat', {'erven','verbergen'}, 'de grenswacht', 'de kroon schrapt tweede zonen uit het erfregister en zet ze over de grens'),
 'ambtsadel': ('staat', {'registreren','verdelen'}, 'de kanselarij', 'titels worden ambten op een loonlijst; wie niet tekent, verliest zijn land'),
 'dragerstoernooi': ('dragers', {'lading-is-macht'}, 'de scheidsvrouwen van het toernooi', 'rang wordt beslecht in een gevecht van lading, voor publiek'),
 'munt': ('staat', {'verdelen','lichaam-is-waar'}, 'de muntmeesters', 'de kroon slaat munt en weigert zaad als betaling van belasting'),
 'steenmunt': ('staat', {'lichaam-is-waar'}, 'de muntmeesters', 'de munt wordt gedekt door Orrim-steen in de kluis van de kroon'),
 'kerkschat': ('kerk', {'geloof-maakt-wet','verdelen'}, 'de tiendheffers', 'de kerk leent de kroon haar schat en neemt de tiende als onderpand'),
 'bankiers': ('steden', {'verdelen','registreren'}, 'de schuldboeken van de steden', 'een bankiershuis koopt de staatsschuld en daarmee de belasting'),
 'nederlaag': ('buren', {'verdelen'}, 'de bezetter', 'Kharvos verslaat het leger aan de pas en neemt het noorden'),
 'verdedigingsbond': ('staat', {'registreren','noodwet'}, 'de bondsraad', 'elke vorst levert op een lijst een leger aan de pas'),
 'dragerleger': ('dragers', {'lading-is-macht','noodwet'}, 'de dragers', 'dragers ontladen op het slagveld'),
 'verdragkern': ('staat', {'namens-beslissen','lichaam-is-waar'}, 'de gezanten', 'een vorst ruilt Orrim-steen tegen vrede, zonder de Orrim te vragen'),
 'schimmelmuren': ('steden', {'noodwet','registreren'}, 'de stadswacht', 'de stad bouwt een binnenring; wie koorts heeft, gaat naar buiten'),
 'brandritueel': ('kerk', {'geloof-maakt-wet'}, 'de priesters', 'de kerk verklaart begraven heidens en verbrandt de doden'),
 'artsengilde': ('steden', {'registreren','verbergen'}, 'de stadsraad die het gilde erkent', 'de stad geeft het artsengilde het alleenrecht op lijken, in ruil voor de oorzaak van de ziekte'),
 'drukpers': ('steden', {'verbergen'}, 'niemand: de drukkers zijn met te veel', 'drukkers in de steden verspreiden wat de kerk niet meer kan verbranden'),
 'stoom': ('steden', {'lichaam-is-waar','verdelen'}, 'de fabrieksheren', 'kracht komt voortaan uit vuur en water, en wie de machines bezit, bezit het werk'),
 'ijzer': ('steden', {'lading-is-macht'}, 'de smeden', 'een gewone man met ijzer kan een drager verslaan'),
 'steenlens': ('dragers', {'lading-is-macht','lichaam-is-waar'}, 'het slijpersgilde', 'Sterrensteen wordt geslepen tot werktuig; lading wordt een ambacht'),
 'nieuwkerk': ('kerk', {'geloof-maakt-wet','namens-beslissen'}, 'de nieuwe priesteressen', 'een profetes preekt dat niemand ja mag zeggen voor een ander, en de kerk neemt haar leer over'),
 'ketterjacht': ('kerk', {'geloof-maakt-wet','verbergen'}, 'de kerkrechters', 'wie twijfelt, wordt voor de kerkrechter gebracht'),
 'scheuring': ('kerk', {'geloof-maakt-wet','verdelen'}, 'twee kerkrechtbanken', 'noord en zuid erkennen elkaars priesters niet meer'),
 'ongeloof': ('steden', {'verbergen'}, 'niemand', 'de steden houden op de tiende te innen; de kerk kan niet meer dwingen'),
 'dragerskoningen': ('dragers', {'lading-is-macht','erven'}, 'de dragerswacht', 'de sterkste lading neemt de kroon, en de wacht volgt de lading'),
 'gaveverbod': ('kerk', {'geloof-maakt-wet','binden'}, 'de kerkrechters', 'de kerk verbiedt elke gave en laat dragers aangeven'),
 'smeden': ('huizen', {'binden','namens-beslissen'}, 'de wachters van de steen', 'wie de fragmenten heeft, bindt dienaren in nieuwe steen en laat die ja zeggen namens anderen'),
 'lijnhuwelijk': ('huizen', {'erven','registreren'}, 'de registers van de huizen', 'dragers mogen alleen met dragers trouwen; het register weigert de rest'),
 'orrimopstand': ('orrim', {'lichaam-is-waar'}, 'de groeven zelf', 'de Orrim zingen de groeven dicht en de mijnwerkers kunnen niet meer naar binnen'),
 'orrimrecht': ('huizen', {'erven'}, 'de moederraden', 'een raad van vrouwen erkent dat de Orrim hun doden houden'),
 'orrimgroeve': ('huizen', {'lichaam-is-waar','binden'}, 'de mijnwachten', 'de mijnhuizen sluiten de groeven af en mijnen de doden'),
 'jachtorde': ('steden', {'verdelen'}, 'het jagersgilde', 'wie een wezen doodt, krijgt van de stad het land waar het leefde'),
 'grensverdrag': ('staat', {'verdelen','verbergen'}, 'de grenswacht', 'een vorst trekt een grens en verbiedt beide kanten haar over te steken'),
 'nachtwet': ('huizen', {'noodwet','registreren'}, 'de dorpsmoeders', 'elk huis houdt bij wie waar slaapt, en een open raam wordt beboet'),
 'censuur': ('kerk', {'verbergen'}, 'de kerkrechters', 'de kerk verbrandt de vondst en vervolgt wie haar zag'),
 'erkenning': ('steden', {'verbergen'}, 'de geleerden', 'de steden erkennen het schip als geschiedenis; de kerk kan het niet meer tegenhouden'),
 'wieg': ('steden', {'namens-beslissen','lading-is-macht'}, 'de geleerden en een drager', 'de Wieg wordt gevonden en vraagt om een ja'),
 'onopgelost': (None, set(), None, None),
}
for k in MENU.values():
    for o in k: assert o['id'] in OPL, o['id']
# welke toestand een crisis voedt (voor oorzaak en erfenis)
CR_VARS = {'honger': ['P/F'], 'elitestrijd': ['E', 'S'], 'bankroet': ['S', 'E'], 'invasie': ['buren', 'eigen'], 'epidemie': ['schim', 'O'],
           'uitvinding': ['T'], 'geloof': ['L', 'T'], 'opleving': ['M', 'gem'], 'orrim': ['mijn', 'orrim'], 'wezens': ['nacht', 'askoud'], 'vondst': ['T', 'W']}
CR_KEYS = {'honger': {'P','F'}, 'elitestrijd': {'E','S','huizen','dragers'}, 'bankroet': {'S','E'}, 'invasie': {'buren','S','staat'},
           'epidemie': {'schim','O'}, 'uitvinding': {'T','O','C'}, 'geloof': {'L','kerk','T','rit'}, 'opleving': {'M','K','O','puls','Z','dragers'},
           'orrim': {'mijn','orrim'}, 'wezens': {'nacht','askoud','isolatie','worm'}, 'vondst': {'T','W','f'}}
EV_EFF = {g[0]: set(g[4]) for g in GEBEURTENIS}
VERSIE = [(.60, 'waar'), (.45, 'deels waar: Ysa en het schip ontbreken'), (.30, 'vervalst'), (.15, 'mythe'), (.05, 'kinderrijm'), (0, 'vergeten')]
AANSPRAAK = {'burgeroorlog': 'zwaard', 'dragerstoernooi': 'lading', 'dragerskoningen': 'lading', 'bankiers': 'geld', 'eedsteden': 'eed', 'nederlaag': 'zwaard', 'verbanning': 'bloed'}

def label801(f):
    for d, l in VERSIE:
        if f >= d: return l
    return 'vergeten'

def run(seed, params=None, eind=5000):
    R = random.Random(seed)
    p = dict(groei=R.uniform(.12,.22), buren_honger=R.uniform(.5,1.5), ev=R.uniform(.7,1.3), aelthir=R.uniform(.2,.8), filter=R.uniform(.02,.06))
    if params: p.update(params)
    s = dict(P=.7, F=1.0, E=1.2, S=.3, L=.25, T=.05, O=.3, K=.7, Q=.5, mijn=.3, orrim=1.0, puls=0, Z=0, M=.8, rit=.1,
             C=.15, W=.4, f=.6, nacht=0, isolatie=0, r=.01)
    macht = dict(staat=.15, huizen=.35, kerk=.10, steden=.10, dragers=.25, buren=.30, orrim=.05, volk=.08)
    aandeel = lambda k: macht.get(k, 0) / sum(macht.values())
    lijn = {k: dict(n=(.3 if k in ('worm','askoud') else 0), stadium=0, t=0) for k in LIJN}; lijn['aelthir']['n'] = .6
    fasen, onopgelost, laatst_gebruikt, log, gebeurd, tw = [], [], {}, [], [], []
    uitgevonden, uitvindingen = {}, []
    wetten = {}          # wetcode -> rij (open)
    wetlog = []          # alle wetten, ook vervallen
    huizen = [dict(huis=n, ouder=None, ontstaan=None, canon=c_, aanspraak=None, gezag_van=None, gezag_tot=None, gevallen=None) for n, c_ in HUIZEN_801]
    heerser = ['Varenne']; huizen[0].update(aanspraak='bestaand gezag in 801', gezag_van=801)
    rust = []
    vorig = dict(beslisser='Liora', betaler='Teo', vervalst='één registerblad', ontdekt='ja', schaal='wereld', mech={'namens-beslissen'})
    mech_hist = [(naam, m) for naam, m in CANON_MECH]
    laatste, vorige, tak, jaar = 801, None, 0, 801
    blok = {}   # crisis -> jaar tot wanneer ze na een mislukte oplossing niet opnieuw opkomt

    def wet_in(code, tekst, wetgever, sleutel, rechtsgebied, handhaver, aanleiding):
        if code in wetten: return
        if any(w['wet'] == code and w['tot'] is not None and jaar - w['tot'] < 300 for w in wetlog): return
        rij = dict(_zwak=0, wet=code, tekst=tekst, wetgever=wetgever, macht_sleutel=sleutel, wetgever_macht=round(aandeel(sleutel), 3),
                   rechtsgebied=rechtsgebied, handhaver=handhaver, aanleiding=aanleiding, van=jaar, tot=None, vervalt_door=None)
        wetten[code] = rij; wetlog.append(rij)
    def wet_uit(code, door):
        if code in wetten: wetten[code].update(tot=jaar, vervalt_door=door); del wetten[code]
    def huis_nieuw(ouder, aanspraak):
        bestaand = {h['huis'] for h in huizen}
        stam = ouder.split(' van ')[0]
        for _ in range(40):
            naam = f"{stam} van {R.choice(PLAATS)}"
            if naam not in bestaand: break
        else: naam = f"{stam} de {len(bestaand)}e"
        huizen.append(dict(huis=naam, ouder=ouder, ontstaan=jaar, canon=None, aanspraak=aanspraak, gezag_van=None, gezag_tot=None, gevallen=None))
        return naam
    def wissel(oplossing, nieuw=None):
        oud = heerser[0]; aanspraak = AANSPRAAK.get(oplossing, 'macht')
        for h in huizen:
            if h['huis'] == oud and h['gezag_van'] is not None and h['gezag_tot'] is None: h['gezag_tot'] = jaar
        if R.random() < .5:
            for h in huizen:
                if h['huis'] == oud and h['gevallen'] is None: h['gevallen'] = jaar
        if nieuw is None:
            levend = [h['huis'] for h in huizen if h['gevallen'] is None and h['huis'] != oud]
            nieuw = R.choice(levend) if levend and R.random() < .6 else huis_nieuw(R.choice([h['huis'] for h in huizen if h['gevallen'] is None] or [oud]), aanspraak)
        for h in huizen:
            if h['huis'] == nieuw and h['gezag_van'] is not None and h['gezag_tot'] is not None:
                huizen.append(dict(h, gezag_van=jaar, gezag_tot=None, aanspraak=aanspraak)); break
        else:
            for h in huizen:
                if h['huis'] == nieuw: h.update(gezag_van=jaar, aanspraak=h['aanspraak'] or aanspraak)
        heerser[0] = nieuw
    def zet(k, v):
        if k in macht: macht[k] = max(.02, macht[k] + v)
        elif k in lijn: lijn[k]['n'] = min(1, max(0, lijn[k]['n'] + v))
        elif k == 'nacht': s['nacht'] = max(0, s['nacht'] + v); lijn['nacht']['n'] = max(0, lijn['nacht']['n'] + v)
        elif k == 'askoud': lijn['askoud']['n'] = min(1, lijn['askoud']['n'] + v)
        elif k in s: s[k] = max(0, s[k] + v) if k in ('P','F','E','puls','Q') else min(1, max(0, s[k] + v))

    # de wetten van 801: gemaakt door de Orde en de huizen, gehandhaafd door de Orde (canon)
    for w in WET_801:
        wet_in(w, 'canonwet bij 801', 'de Orde en de huizen', 'huizen', 'Velmara', 'de Orde en de huisgerechten', 'geldend recht in 801')
    jaar = 801; wet_uit('RECHT-gavenrecht', 'de Hoge Moeder kan na de val van de Orde niemand meer berechten')
    while jaar < eind:
        jaar += STAP
        for gid, tekst, kans, cond, eff in GEBEURTENIS:
            once = gid in ('kern_valt','kern_in_worm','negen_cellen')
            if once and any(g['id'] == gid for g in gebeurd): continue
            if cond(s, jaar) and R.random() < kans * p['ev']:
                for k, v in eff.items(): zet(k, v)
                gebeurd.append(dict(jaar=jaar, id=gid, tekst=tekst))
        s['r'] += p['filter'] * (.5 - s['r'])
        dragers = min(1, .01 / s['r'])
        sterk = max(('huizen','steden','staat'), key=aandeel)
        if s['r'] > .12: wet_uit('WET-deelwet-recht', 'er zijn weer genoeg mannen (verhouding boven 12%)'); wet_in('W-huwelijk', 'Een man en een vrouw mogen weer trouwen', f'de {sterk}', sterk, 'Velmara', 'de moederraden', 'verhouding boven 12%')
        if s['r'] > .25: wet_uit('WET-wie-gewone-man', 'mannen zijn geen schaars bezit meer (verhouding boven 25%)'); wet_in('W-mannenbezit', 'Een man mag bezit hebben en getuigen', f'de {sterk}', sterk, 'Velmara', 'de gerechten', 'verhouding boven 25%')
        if s['r'] > .4: wet_in('W-gelijkerfrecht', 'Zonen en dochters erven gelijk', f'de {sterk}', sterk, 'Velmara', 'de gerechten', 'verhouding boven 40%')
        # bevolking, elites, staat, buren, techniek, openheid (zoals Z42)
        s['F'] = max(.4, s['F'] * .98 + .02 * (1 + 2.5 * s['T']) + (.03 * s['M'] if macht['dragers'] > .2 else 0))
        s['P'] += p['groei'] * s['P'] * (1 - s['P'] / s['F'])
        s['E'] = max(.6, s['E'] + .07 * (s['P'] / s['F'] - .8) + .005 - .03 * (s['E'] - 1.0))   # edelen zakken ook af
        s['S'] = min(1, max(0, s['S'] + .05 * s['P'] * (.5 + s['L']) - .045 * s['E'] - .02 * (1 - s['C'])))   # edelen kosten de staat geld (Turchin)
        macht['staat'] = max(.02, macht['staat'] + .02 * (s['S'] - .4))
        macht['buren'] = max(.05, macht['buren'] + .01 * p['buren_honger'] - .005)
        macht['volk'] = max(.03, .05 + .3 * max(0, s['P'] / s['F'] - .85))
        macht['steden'] = max(.03, macht['steden'] + .015 * (s['T'] + .5 * s['O'] - .2))   # steden groeien met techniek en handel
        macht['kerk'] = max(.03, macht['kerk'] + .01 * (s['L'] - .3))                  # de kerk groeit met het geloof
        s['T'] = min(1, s['T'] + .003 * (.5 + s['O']) * (1 - .5 * min(1, s['M'])) * (.5 + s['C']))
        s['O'] = min(1, max(0, s['O'] + .008 * (s['T'] - .15) + .006 * (macht['steden'] - macht['huizen']) - .015 * (s['E'] - 1.15)))
        s['Q'] += .03 * s['orrim']; oogst = min(s['Q'], s['mijn'] * s['Q'] * .3); s['Q'] -= oogst
        s['orrim'] = min(1.5, max(.05, s['orrim'] + .01 - .05 * s['mijn'] * s['orrim']))
        s['K'] = min(1, max(0, s['K'] + .06 * ((1 - s['O']) - s['K'])))
        s['puls'] *= .75; s['Z'] = max(0, s['Z'] - .04)
        verdun = .35 + .65 * math.exp(-(jaar - 801) / 1500)
        bodem = .12 + .25 * min(1, oogst * 2) + .1 * s['rit']
        s['M'] = round(bodem + .55 * s['K'] * verdun + s['puls'] + .3 * s['Z'], 3)
        s['mijn'] = min(1, max(.05, s['mijn'] + .02 * (macht['huizen'] + macht['dragers'] - .5) - (.03 if 'W-orrimdoden' in wetten else 0)))
        s['nacht'] = min(1, s['nacht'] * .93 + .12 * s['M'] * s['O'] * (1 - dragers) * (.5 if 'W-nachtwet' in wetten else 1))
        lijn['nacht']['n'] = max(lijn['nacht']['n'] * .97, s['nacht'])
        lijn['askoud']['n'] = min(1, lijn['askoud']['n'] * .98 + .02 * s['M'])
        lijn['schim']['n'] *= .85
        s['C'] = min(1, s['C'] + .01 + .01 * s['T'])
        s['L'] = min(1, max(0, s['L'] + .012 * (macht['kerk'] - .15) - .012 * s['T'] + .004))
        verteller = max(macht, key=macht.get)
        d = .028 + (.02 if verteller in ('kerk','dragers','huizen') else 0) - .015 * p['aelthir'] * lijn['aelthir']['n'] - .02 * s['T']
        if 'W-boekverbod' in wetten: d += .01
        s['f'] = max(0, s['f'] * (1 - max(.004, d)))
        if verteller in ('dragers','buren'): tak = 1
        elif verteller in ('kerk','huizen'): tak = 0
        s['W'] = max(0, s['W'] - .006)
        for k, l in lijn.items():
            if l['n'] > .1 or l['stadium'] > 0:
                l['t'] += 1
                tempo = 16 if k == 'aelthir' else max(3, 8 - 4 * s['isolatie'])
                if l['t'] >= tempo and l['stadium'] < 3: l['stadium'] += 1; l['t'] = 0
                if s['T'] > .6 and l['stadium'] == 3 and l['t'] >= 6: l['stadium'] = 4
        lijn['aelthir']['n'] = max(.05, lijn['aelthir']['n'] * (1 - .006 * s['T']))
        s['isolatie'] *= .96
        # 7 institutioneel geheugen: een wet zonder wetgever met macht vervalt
        for code, w in list(wetten.items()):
            if jaar - w['van'] >= GEWOONTE: continue   # een wet die zo lang geldt, is gewoonte: alleen opheffing maakt er een eind aan
            w['_zwak'] = w['_zwak'] + 1 if aandeel(w['macht_sleutel']) < WET_VERVAL else 0
            if w['_zwak'] >= 3:   # instituties zijn traag: pas na 60 jaar zonder dragende macht
                wet_uit(code, f"60 jaar lang had de wetgever ({w['wetgever']}) niet meer de macht om haar te handhaven")
        # ---------- uitvindingen uit de boom ----------
        recent = {f['crisis'] for f in fasen if f['van'] >= jaar - 100} | {x['crisis'] for x in onopgelost if x['jaar'] >= jaar - 100}
        ctx = dict(C=s['C'], O=s['O'], M=s['M'], mijn=s['mijn'], T=s['T'], F=s['F'], P=s['P'], worm=lijn['worm']['n'], aandeel=aandeel,
                   vondsten=[g for g in gebeurd if g['id'] in ('archief', 'kern_in_worm', 'negen_cellen')])
        kand = [k for k in B.BOOM if k['code'] not in uitgevonden and all(v in uitgevonden for v in k['vereist'])
                and k['test'](ctx) and aandeel(k['uitvinder']) >= .05]
        R.shuffle(kand)
        for k in kand:
            nood = sorted(set(k['noodzaak']) & recent)
            if R.random() < UITVIND_KANS * (.2 + 2.5 * bool(nood)) * (.5 + s['C']):   # nood maakt vindingrijk; zonder nood zelden
                for e, v in k['gevolg'].items(): zet(e, v)
                uitgevonden[k['code']] = jaar
                uitvindingen.append(dict(code=k['code'], naam=k['naam'], familie=k['familie'], jaar=jaar, uitvinder=k['uitvinder'],
                                         uitvinder_macht=round(aandeel(k['uitvinder']), 3),
                                         noodzaak=', '.join(nood) if nood else 'aantrekkelijk: geen crisis vroeg erom',
                                         materiaal=k['materiaal'], vereist_met={v: uitgevonden[v] for v in k['vereist']},
                                         breekt=k['breekt'], prijs=k['prijs'], _eff=list(k['gevolg']), _i=len(log)))
                break
        tw.append(s['M']); gem = sum(tw[-15:]) / len(tw[-15:])
        eigen = s['S'] * s['P'] * (1 + macht['dragers'] * s['M'])
        waarde = {'P/F': s['P'] / s['F'], 'E': s['E'], 'S': s['S'], 'buren': macht['buren'], 'eigen': eigen, 'schim': lijn['schim']['n'], 'O': s['O'],
                  'T': s['T'], 'L': s['L'], 'M': s['M'], 'gem': gem, 'mijn': s['mijn'], 'orrim': s['orrim'], 'nacht': lijn['nacht']['n'],
                  'askoud': lijn['askoud']['n'], 'W': s['W']}
        druk = dict(
            honger=(s['P'] / s['F'] - .93) * 5, elitestrijd=(s['E'] - 1.3) * 2.0 * (1.3 - s['S']), bankroet=(.12 - s['S']) * 6,
            invasie=(macht['buren'] - eigen) * 1.5, epidemie=lijn['schim']['n'] * 2.0 * (.5 + s['O']), uitvinding=0,
            geloof=(.38 - s['L']) * 4, opleving=(s['M'] - gem - .12) * 5, orrim=(s['mijn'] - .55) * 3 * s['orrim'],
            wezens=max(lijn['nacht']['n'], .7 * lijn['askoud']['n']) * 1.4, vondst=(s['T'] - .45) * 2 + s['W'] * .4 if s['T'] > .45 else 0)
        if vorige: druk[vorige] *= .5
        for k_, t_ in blok.items():
            if jaar < t_: druk[k_] = 0
        orde = sorted(druk, key=druk.get, reverse=True); crisis = orde[0]
        tijd = 'lading' if s['M'] > .9 else 'machines' if s['T'] > .6 else 'steden' if s['T'] > .35 else 'kronen'   # 'machines' heet in de tekst 'werkplaatsen'
        era = 'Smeedtijd' if s['Z'] > .15 else 'Ruwe Jaren' if s['C'] < .4 else 'Tijd van de ' + {'machines': 'werkplaatsen'}.get(tijd, tijd)
        log.append(dict(jaar=jaar, M=s['M'], bodem=round(bodem,3), T=round(s['T'],3), P=round(s['P']/s['F'],3), S=round(s['S'],3), E=round(s['E'],3),
                        C=round(s['C'],3), f=round(s['f'],3), r=round(s['r'],3), L=round(s['L'],3), O=round(s['O'],3), orrim=round(s['orrim'],3),
                        era=era, tak=tak, heerser=heerser[0], wetten=len(wetten), macht={k: round(aandeel(k),3) for k in macht},
                        lijn={k:l['stadium'] for k,l in lijn.items() if l['n']>.1 or l['stadium']>0}))
        if druk[crisis] < .5 or jaar - laatste < 60: continue
        EENMALIG = ('erkenning','censuur','wieg','drukpers','stoom','ijzer','steenlens','smeden','orrimrecht')
        opties = [o for o in MENU[crisis] if jaar - laatst_gebruikt.get(o['id'], -9999) > 600 and not (o['id'] in EENMALIG and o['id'] in laatst_gebruikt)]
        if not opties: continue   # alles al eens gebruikt (spiraal): geen nieuwe crisis, gewoon geen nieuwe vondst of uitvinding
        # 2 macht: alleen wie genoeg macht heeft, kan de oplossing doorzetten
        opties = [o for o in opties if aandeel(OPL[o['id']][0]) >= MACHT_MIN]
        if crisis == 'wezens':
            nacht_dom = lijn['nacht']['n'] >= .7 * lijn['askoud']['n']
            opties = [o for o in opties if (o['id'] == 'nachtwet') == nacht_dom]
        # 5 rijm: gedeeld mechanisme met een eerdere fase én 3 of meer assen anders; voorkeur 3-4 assen
        def verschil(o): return sum(o[a] != vorig[a] for a in AXES)
        def gedeeld(o):
            for naam, m in reversed(mech_hist):
                hit = OPL[o['id']][1] & m
                if hit: return sorted(hit)[0], naam
            return None, None
        geldig = [o for o in opties if verschil(o) >= 3 and gedeeld(o)[0]]
        voorkeur = [o for o in geldig if verschil(o) <= 4] or geldig
        oorzaak = {v: round(waarde[v], 3) for v in CR_VARS[crisis]}
        if not voorkeur:
            onopgelost.append(dict(jaar=jaar, crisis=crisis, druk=round(druk[crisis], 2), oorzaak=oorzaak,
                                   reden='niemand met genoeg macht heeft een oplossing die rijmt' if opties == [] or not geldig else ''))
            s['C'] = max(0, s['C'] - .03); laatste = jaar; vorige = crisis; blok[crisis] = jaar + 200
            continue
        keuze = R.choice(voorkeur)
        sleutel, mech, handhaver, hoe = OPL[keuze['id']]
        mech_g, rijmt_met = gedeeld(keuze)
        # 6 erfenis: de jongste eerdere fase of gebeurtenis die raakte aan wat deze crisis voedt
        erft = None
        for f in reversed(fasen):
            if set(f['_eff']) & CR_KEYS[crisis]: erft = f"fase {f['van']}: {f['naam']}"; break
        for g in reversed(gebeurd):
            venster = 400 if g['id'] in ('kern_valt', 'kern_in_worm', 'negen_cellen') else 100
            if g['jaar'] >= jaar - venster and EV_EFF.get(g['id'], set()) & CR_KEYS[crisis]:
                if erft is None or int(g['jaar']) > int(erft.split(':')[0].split()[-1]): erft = f"gebeurtenis {g['jaar']}: {g['tekst']}"
                break
        for u in reversed(uitvindingen):
            if set(u['_eff']) & CR_KEYS[crisis]:
                vj = int(erft.split(':')[0].split()[-1]) if erft else -1
                if u['jaar'] > vj: erft = f"uitvinding {u['jaar']}: {u['naam']}"
                break
        if erft is None: erft = 'de toestand bij 801 (BESLUIT-Z36-4)'
        terug = keuze['id'] in laatst_gebruikt
        laatst_gebruikt[keuze['id']] = jaar
        if keuze['id'] == 'erkenning': laatst_gebruikt['censuur'] = jaar + 9999
        macht_voor = round(aandeel(sleutel), 3)
        for k, v in keuze['eff'].items(): zet(k, v)
        if keuze['id'] in WET:
            code, tekst, weg = WET[keuze['id']]
            for w in weg: wet_uit(w, f"opgeheven door {keuze['beslisser']} ({keuze['naam']})")
            wet_in(code, tekst, keuze['beslisser'], sleutel, keuze['schaal'], handhaver, f"{crisis} in {jaar}")
        if crisis == 'honger': s['P'] *= .85
        if crisis == 'elitestrijd':
            s['E'] = max(.8, s['E'])
            if keuze['id'] in ('burgeroorlog','dragerstoernooi'): wissel(keuze['id'])
            if keuze['id'] == 'verbanning': huis_nieuw(heerser[0], 'bloed (verbannen zonen)')
        if crisis == 'invasie':
            macht['buren'] *= .6
            if keuze['id'] == 'nederlaag': wissel('nederlaag', huis_nieuw('Kharvos', 'zwaard'))
        if keuze['id'] in ('dragerskoningen', 'bankiers'): wissel(keuze['id'])
        if crisis == 'epidemie': lijn['schim']['n'] *= .4; s['P'] *= .85
        if crisis == 'wezens': lijn['nacht']['n'] *= .6; s['nacht'] *= .6
        if crisis in ('elitestrijd','invasie'): s['C'] = max(0, s['C'] - .1)
        if fasen: fasen[-1]['tot'] = jaar
        if jaar - laatste >= 200 and laatste > 801:
            rust.append(dict(van=laatste + STAP, tot=jaar - STAP, tijd=tijd))
        fasen.append(dict(van=jaar, tot=None, crisis=crisis, oplossing=keuze['id'], naam=keuze['naam'], beslisser=keuze['beslisser'],
                          macht_sleutel=sleutel, actor_macht=macht_voor, mechanisme=hoe, handhaver=handhaver,
                          betaler=keuze['betaler'], vervalst=keuze['vervalst'], ontdekt=keuze['ontdekt'], schaal=keuze['schaal'],
                          oorzaak=oorzaak, druk=round(druk[crisis], 2), tweede_druk=f"{orde[1]} {round(druk[orde[1]], 2)}",
                          erft_van=erft, gedeeld_mechanisme=mech_g, rijmt_met=rijmt_met, assen_anders=verschil(keuze),
                          blijvend=keuze['blijvend'], terug=terug, era=era, heerser=heerser[0], _eff=list(keuze['eff']), _i=len(log) - 1))
        mech_hist.append((f"fase {jaar} ({keuze['naam']})", mech))
        vorig = dict(keuze, mech=mech); laatste, vorige = jaar, crisis
    if fasen: fasen[-1]['tot'] = jaar
    if jaar - laatste >= 200: rust.append(dict(van=laatste + STAP, tot=jaar, tijd=tijd))
    # 4 gevolg: 60 jaar na de fase vergeleken met het moment ervoor
    for f in fasen:
        i = f.pop('_i'); f.pop('_eff')
        a, b = log[max(0, i - 1)], log[min(len(log) - 1, i + GEVOLG_STAPPEN)]
        dv = {k: round(b[k] - a[k], 3) for k in ('M','T','P','S','E','L','O','C','r') if abs(b[k] - a[k]) >= .02}
        dm = sorted(((k, round(b['macht'][k] - a['macht'][k], 3)) for k in a['macht']), key=lambda x: -abs(x[1]))[:3]
        f['gevolg'] = dict(toestand=dv, macht={k: v for k, v in dm if abs(v) >= .01}, heerser_na=b['heerser'])
    for u in uitvindingen:
        i = min(u.pop('_i'), len(log) - 1); u.pop('_eff')
        a, b = log[max(0, i - 1)], log[min(len(log) - 1, i + GEVOLG_STAPPEN)]
        dv = {k: round(b[k] - a[k], 3) for k in ('M','T','P','S','E','L','O','C','r') if abs(b[k] - a[k]) >= .02}
        dm = sorted(((k, round(b['macht'][k] - a['macht'][k], 3)) for k in a['macht']), key=lambda x: -abs(x[1]))[:3]
        u['gevolg'] = dict(toestand=dv, macht={k: v for k, v in dm if abs(v) >= .01})
    # 10 rust per laag
    for r_ in rust:
        a = next(x for x in log if x['jaar'] >= r_['van']); b = [x for x in log if x['jaar'] <= r_['tot']][-1]
        w_in = sum(1 for w in wetlog if r_['van'] <= w['van'] <= r_['tot']); w_uit = sum(1 for w in wetlog if w['tot'] and r_['van'] <= w['tot'] <= r_['tot'])
        r_.update(politiek='geen crisis', economie=f"honger {a['P']}→{b['P']}, kas {a['S']}→{b['S']}",
                  samenleving=f"jongens {a['r']}→{b['r']}, {w_in} wetten in, {w_uit} uit, geloof {a['L']}→{b['L']}",
                  magie=f"{a['M']}→{b['M']}", genres=RUST_GENRES[r_['tijd']])
    for h in huizen:
        if h['ouder'] is None and h['ontstaan'] is None: h['ontstaan'] = 801
    return dict(seed=seed, p={k: round(v,3) for k,v in p.items()}, fasen=fasen, onopgelost=onopgelost, log=log, gebeurd=gebeurd, uitvindingen=uitvindingen,
                wetten=wetlog, huizen=huizen, rust=rust)

def versie(f, tak): return Z.versie(f, tak)

if __name__ == '__main__':
    for sd in map(int, sys.argv[1:] or ['420003']):
        o = run(sd); print('seed', sd, o['p'])
        for f in o['fasen']:
            print(f"  {f['van']} {f['crisis']:<11} {f['naam']} | {f['beslisser']} ({f['actor_macht']}) | rijmt met {f['rijmt_met']} via {f['gedeeld_mechanisme']} | {f['assen_anders']} assen | erft van {f['erft_van'][:50]}")
            print(f"       oorzaak {f['oorzaak']} | gevolg {f['gevolg']}")
        print('  onopgelost:', [(x['jaar'], x['crisis']) for x in o['onopgelost']])
        for u in o['uitvindingen']: print(f"  UITVINDING {u['jaar']} {u['naam']} door {u['uitvinder']} ({u['uitvinder_macht']}) | noodzaak {u['noodzaak']} | vereist {u['vereist_met']} | gevolg {u['gevolg']}")
        print('  wetten:', [(w['wet'], w['van'], w['tot'], (w['vervalt_door'] or '')[:30]) for w in o['wetten']][:12])
        print('  huizen:', [(h['huis'], h['ouder'], h['aanspraak'], h['gezag_van'], h['gezag_tot']) for h in o['huizen']])
