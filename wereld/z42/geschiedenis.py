"""Ronde Z42, geschiedenismotor: geschiedenis na 801 met zeven motoren en golvende magie die nooit verdwijnt.
Simulatie, geen canon. Stap = 20 jaar.
Bodem van de magie: Orrim sterven niet maar verstenen tot groeve (D1-orrim-dood); in hun lichaam groeit
Sterrensteen (VOLK-orrim); een splinter is een vesting waard (D1-orrim-geld). Zolang er Orrim zijn, komt er steen bij.
Golf van de magie: lading is erfelijk via dragerlijnen; gesloten elites concentreren haar, open samenlevingen verdunnen haar.
Pieken: fragmenten (negen cellen, reservekern, Sterrensteen-splinters).
Zeven motoren: bevolking/voedsel, elites, geld/staat, oorlog/buren, uitvindingen, ziekte/klimaat, geloof."""
import random, math, sys, json
STAP = 20
AXES = ['beslisser','betaler','vervalst','ontdekt','schaal']

def O(i, naam, beslisser, betaler, vervalst, ontdekt, schaal, blijvend, **eff):
    return dict(id=i, naam=naam, beslisser=beslisser, betaler=betaler, vervalst=vervalst, ontdekt=ontdekt, schaal=schaal, blijvend=blijvend, eff=eff)

WET = {'graanwet': ('W-graanwet', 'De graanwet: de oogst gaat eerst naar de schuren van de kroon', []), 'kloostermaal': ('W-kloosterhorig', 'Wie van het klooster eet, staat ingeschreven bij het klooster', []), 'ambtsadel': ('W-ambtsadel', 'Titels zijn ambten en kunnen gekocht worden', []), 'verbanning': ('W-zonenbanning', 'Tweede zonen van edelen mogen het rijk niet in', []), 'dragerstoernooi': ('W-toernooirecht', 'Rang onder dragers wordt beslecht in het toernooi', []), 'munt': ('W-muntrecht', 'Belasting en schuld worden in munt betaald, niet in zaad', ['WET-erfrecht']), 'steenmunt': ('W-steendekking', 'De munt is gedekt door Orrim-steen', []), 'bankiers': ('W-schuldrecht', 'Staatsschuld is verhandelbaar', []), 'verdedigingsbond': ('W-pasbond', 'De vorsten van de bond leveren elk een leger aan de pas', []), 'schimmelmuren': ('W-ringrecht', 'Wie besmet is, woont in de buitenring', []), 'brandritueel': ('W-lijkbrand', 'De doden worden verbrand', []), 'artsengilde': ('W-artsenrecht', 'Alleen het artsengilde mag lijken openen', []), 'nieuwkerk': ('W-jarecht', 'Niemand mag ja zeggen namens een ander lichaam', ['WET-wie-gewone-man', 'WET-deelwet-recht']), 'ketterjacht': ('W-ketterwet', 'Twijfel aan de kerk is een misdaad', []), 'ongeloof': ('W-vrijgeloof', 'Geloof is een eigen zaak', ['W-ketterwet']), 'dragerskoningen': ('W-ladingkroon', 'De kroon gaat naar de sterkste drager', ['W-gaveverbod']), 'gaveverbod': ('W-gaveverbod', 'Een gave gebruiken is verboden', ['WET-wie-gaven-man', 'RECHT-gavenrecht', 'W-ladingkroon']), 'smeden': ('W-zegelplicht', 'Wie het kleine zegel dient, laat zich binden', []), 'lijnhuwelijk': ('W-lijnwet', 'Dragers trouwen alleen met dragers', []), 'orrimrecht': ('W-orrimdoden', 'De Orrim houden hun doden; mijnen in een groeve is grafroof', ['W-orrimfok', 'WET-wie-vreemd-volk']), 'orrimfok': ('W-orrimfok', 'De Orrim zijn fokbezit van de mijnhuizen', ['W-orrimdoden']), 'jachtorde': ('W-jachtrecht', 'Wie een wezen doodt, krijgt het land waar het leefde', []), 'grensverdrag': ('W-wezengrens', 'Het wezenvolk heeft een eigen land achter een heilige grens', ['W-jachtrecht']), 'nachtwet': ('W-nachtwet', 'Niemand slaapt alleen; een open raam na zonsondergang wordt beboet', []), 'censuur': ('W-boekverbod', 'Boeken over het schip zijn verboden', []), 'erkenning': ('W-schipwaar', 'Het schip is erkend als geschiedenis', ['W-boekverbod'])}
MENU = {
 'honger': [
  O('graanwet','De graanwet: de staat koopt de oogst op','de kroon','de boeren','hoeveel er in de schuren lag','deels','rijk','Brood is politiek; wie de schuren heeft, heeft het land.', S=-.1, F=.05, L=.05),
  O('trek','De grote trek naar het noorden','de dorpen zelf','wie achterbleef','waarom ze vertrokken','nee','regio','Een nieuw land, gesticht door hongerigen; het noorden spreekt een ander dialect.', P=-.15, O=.1),
  O('dragersakkers','Dragers laten de akkers groeien','de dragers','wie hun lading ontvangt','wat het de ontvangers kost','nee','dorp','Een goede oogst heeft een man nodig; vruchtbaarheid is weer een gave.', F=.1, M=.05, dragers=.15),
  O('kloostermaal','De kloosters voeden wie zich laat inschrijven','de kerk','wie zich inschreef en niet meer weg mocht','wie er niet meer uit kwam','deels','rijk','Wie at van de kerk, behoort de kerk toe.', kerk=.15, L=.05),
 ],
 'elitestrijd': [
  O('burgeroorlog','De oorlog van de neven','de huizen','gewone mannen als soldaten','wie begon','nee','rijk','Een generatie edelen is dood; de rest is moe en kleiner.', E=-.4, S=-.15, C=-.15, P=-.05),
  O('verbanning','De overtollige zonen worden verbannen','de kroon','de verbannen zonen','waar ze heen gingen','nee','rijk','Over de zee bestaat een land van verbannen edelen.', E=-.25, O=.05),
  O('ambtsadel','Edelen worden ambtenaren','de kroon','de oude huizen','dat de titels gekocht zijn','ja','rijk','Een titel is een baan; adel zonder land is een nieuw soort mens.', E=-.2, S=.1, staat=.1),
  O('dragerstoernooi','Het toernooi van de lading','de dragers','de verliezers, die verbranden','hoeveel er verbrandden','deels','stad','Rang wordt bevochten in het licht; de sterkste lading erft.', E=-.2, M=.05, dragers=.1),
 ],
 'bankroet': [
  O('munt','Zaad wordt vervangen door munt','de kroon','de dragers, wier zaad zijn waarde verliest','wat de munt gedekt hield','ja','rijk','Geld is metaal of papier, niet meer een lichaam.', S=.3, dragers=-.15, M=-.05, T=.03),
  O('steenmunt','Munt gedekt door Orrim-steen','de kroon','de Orrim','waar de dekking vandaan komt','nee','rijk','Elke munt is een stukje van een levend volk.', S=.3, mijn=.3),
  O('kerkschat','De kerk leent de staat haar schat','de kerk','de gelovigen, via de tiende','dat de kerk nu eigenaar is','deels','rijk','De kroon staat in het krijt bij het altaar.', S=.25, kerk=.15),
  O('bankiers','Een huis van bankiers neemt de schuld over','de bankiers','de belastingbetalers','hoeveel rente er stond','nee','wereld','Een familie zonder land bezit alle landen.', S=.3, steden=.15, O=.05),
 ],
 'invasie': [
  O('nederlaag','Het noorden valt aan Kharvos','Kharvos','het grensvolk','de vrede die gesloten werd','deels','rijk','De machinemannen wonen nu aan deze kant van de pas.', S=-.15, buren=-.2, O=.1, T=.04),
  O('verdedigingsbond','De bond van de pas','een raad van vorsten','de grensdorpen','wat de bond kostte','ja','wereld','Wie de pas houdt, houdt het rijk bij elkaar.', S=-.1, staat=.1, buren=-.15),
  O('dragerleger','Een leger van dragers','de dragers','de dragers zelf, die opbranden','hoeveel er niet terugkwamen','nee','rijk','Een oorlog is weer een zaak van lading.', M=.1, dragers=.2, buren=-.2),
  O('verdragkern','Het verdrag om de kern','een vorst','de Orrim, als steengroeve','wat er geruild werd','nee','wereld','Kharvos en het zuiden delen een geheim, en dat geheim is een machine.', buren=-.25, mijn=.2),
 ],
 'epidemie': [
  O('schimmelmuren','De schimmelmuren','de artsenkloosters','de besmetten achter de muur','hoeveel er achter de muur bleven','deels','stad','Een stad heeft een binnenring voor de levenden.', P=-.1, steden=.05),
  O('brandritueel','Het brandritueel','de kerk','de doden en wie bij hen waakte','dat het vuur de schimmel doodt en geen zonde','nee','rijk','De doden worden verbrand; begraven is heidens.', kerk=.15, P=-.08),
  O('artsengilde','Het artsengilde vindt de schimmel onder glas','de artsen','de proefpersonen','wie er in de proeven stierf','ja','stad','Ziekte heeft een oorzaak die je kunt zien.', T=.06, P=-.06),
 ],
 'uitvinding': [
  O('drukpers','De drukpers','de steden','de kopiisten van de kerk','niets: het wordt te veel om te verbergen','ja','wereld','Een tekst bestaat in duizend exemplaren; niemand kan alles meer verbranden.', T=.05, L=-.1, W=.15, f=.08),
  O('stoom','Machines op water en vuur','de bankiers','de wevers en de boeren','dat de Makers dit al kenden','deels','wereld','Kracht komt uit kolen, niet uit lichamen.', T=.08, F=.15, dragers=-.15, O=.1),
  O('ijzer','Het ijzeren zwaard','de smeden','de gaven-mannen, die nu te verslaan zijn','dat de schimmel het ijzer ooit vrat','nee','rijk','Een gewone man met ijzer verslaat een drager.', T=.05, dragers=-.1),
  O('steenlens','De steenlens: Sterrensteen geslepen tot werktuig','de dragers en de smeden samen','de Orrim','wat de lens eigenlijk is','nee','stad','Magie en techniek worden één ambacht.', T=.05, M=.08, mijn=.15),
 ],
 'geloof': [
  O('nieuwkerk','De kerk van het eigen ja','een profetes','de oude priesteressen','dat de profetes een drager was','deels','rijk','Wie ja zegt, bidt; het ja van een ander is heiligschennis.', L=.3, kerk=.2, rit=.2),
  O('ketterjacht','De jacht op ketters','de kerk','de twijfelaars','wat de ketters echt geloofden','nee','rijk','Twijfel is een misdaad.', L=.15, kerk=.1, C=-.05),
  O('scheuring','De scheuring tussen noord en zuid','twee kerken','families langs de grens','wie de scheuring begon','deels','wereld','Er zijn twee waarheden, en elk heeft een leger.', L=.1, O=-.05),
  O('ongeloof','Het grote twijfelen','de geleerden','de kerk','niets','ja','stad','God is een vraag geworden.', L=.05, kerk=-.2, T=.03, rit=-.1),
 ],
 'opleving': [
  O('dragerskoningen','Dragers worden koning','de dragers','gewone mannen als soldaten','dat de koningen ooit gewone jongens waren','nee','rijk','Koningschap volgt de lading; een kroon gloeit.', dragers=.25),
  O('gaveverbod','Het gave-verbod en de jacht','de kerk','gaven-mannen en hun vrouwen','dat de heiligen zelf gaven hadden','deels','rijk','Een gave is een zonde; wie gloeit, verbergt het.', kerk=.2, M=-.1, askoud=.2),
  O('smeden','Een kleiner zegel wordt gesmeed','wie de fragmenten heeft','wie in de nieuwe steen wordt gebonden','dat het een zegel is','nee','rijk','Er zegt weer iets ja namens anderen, kleiner dan het eerste Zegel.', Z=.5, M=.15),
  O('lijnhuwelijk','Dragers mogen alleen nog met dragers','de huizen','liefdes over de lijn','wie er uit de registers verdween','nee','huis','Lading wordt erfgoed van een kaste.', O=-.15, huizen=.15),
 ],
 'orrim': [
  O('orrimopstand','De opstand van de groeven','de Orrim','de mijnwerkers','dat de Orrim ooit mensen waren','ja','regio','De groeven zingen terug; steen is niet meer gratis.', mijn=-.3, orrim=.1, S=-.1),
  O('orrimrecht','De Orrim krijgen het recht op hun doden','een raad van vrouwen','de mijnhuizen','hoeveel er al gemijnd was','ja','rijk','Een volk mag zijn doden houden; wie een groeve roeft, is een grafrover.', mijn=-.25, L=.05),
  O('orrimfok','De Orrim worden gefokt','de mijnhuizen','de Orrim','dat het mensen zijn','nee','rijk','Een volk is een mijn geworden.', mijn=.3, orrim=.15, M=.1),
 ],
 'wezens': [
  O('jachtorde','Een jachtorde wordt gesticht','het jagersgilde','het vervormde volk','dat de wezens mensen waren','nee','regio','Er bestaan monsters, officieel; wie ze doodt, krijgt land.', isolatie=.5),
  O('grensverdrag','Een grensverdrag met het wezenvolk','een vorst','de grensdorpen','wat er in het verdrag staat','deels','rijk','Het wezenvolk heeft een eigen land; de grens is heilig.', isolatie=.7),
  O('nachtwet','De nachtwet: niemand slaapt alleen','de dorpsmoeders','wie alleen woont','waarom alleen slapen gevaarlijk is','nee','dorp','Slapen doe je samen; een open raam is een schande.', nacht=-.3),
 ],
 'vondst': [
  O('censuur','De kerk verbrandt de vondst','de kerk','de geleerden','de vondst zelf','nee','stad','Er zijn verboden boeken, en dus een markt voor verboden boeken.', W=-.1),
  O('erkenning','Het schip wordt erkend','de geleerden','de kerk, die haar wonder verliest','niets: de waarheid wint, maar te laat om iets te voelen','ja','wereld','Het schip was echt. Men weet het, en het verandert niets aan wat men voelt.', W=.3, kerk=-.15, f=.2),
  O('wieg','De Wieg wordt gevonden en antwoordt','de geleerden en een drager','wie haar eerst aanraakte','wat de Wieg zei','deels','wereld','De machine onder de berg vraagt nog steeds om een ja.', M=.15, W=.2, T=.05),
 ],
}
VERSIE = [
 (.60, "Liora hing Thalens sleutel op Ysa's slot, en sindsdien opent het alleen met het ja van wie het draagt.", None),
 (.45, "Een boerendochter uit Ambergaard brak het Zegel, en de Orde viel.", None),
 (.30, "De heilige Lior gaf haar licht, opdat elke vrouw zelf zou kiezen.", "De heks Lior doofde de ster en bracht de honger."),
 (.15, "Het meisje dat de ster uitblies.", "Het meisje dat de ster stal."),
 (.05, "Lior, Lior, doe de deur dicht, anders komt het licht.", None),
 (0,   "Een kinderrijm. Niemand weet meer wie Lior was.", None),
]
LIJN = {
 'nacht': ['dragerlozen: verbrande ontvangers', 'nachtvlerken in de ruïnes', 'het vlerkvolk', 'de merries', 'de nachtmerrie'],
 'worm':  ['wormvaarders', 'wormbroeders', 'de wyrmen', 'draken op de kern', 'de draak met de schat'],
 'schim': ['schimmelbezetenen', 'de dwalers', 'de stille stoeten', 'de ondoden', 'de wandelende doden'],
 'askoud':['askouden', 'koudbloeden', 'het nachtadel', 'bloeddrinkers', 'de vampier'],
 'aelthir':['de Aelthir', 'de Langlevenden', 'het heuvelvolk', 'het verborgen volk', 'de feeën'],
}
HUIZEN_801 = [('Varenne','HUI-varenne'),('Kaldra','HUI-kaldra-Z6'),('Mirre','HUI-mirre'),('Qesh','HUI-qesh-Z6')]
PLAATS = ['Saelith','Ambergaard','Hoogvrouwe','de Zoutkust','Groenmuil','de Rosse','de Pas','de Stille eilanden']
WET_801 = ['WET-deelwet-recht','WET-erfrecht','WET-wie-gewone-man','WET-wie-gaven-man','RECHT-gavenrecht','WET-wie-vreemd-volk','WET-grijswortel','WET-wie-weigert']
LIJN_CANON = {'nacht':'ORIGIN-WAAROM-9','worm':'NAV-wormwording-B1','schim':'HORROR-SKELET-Z9-6','askoud':'BESLUIT-Z6-WRIJ-065','aelthir':'VOLK-aelthir-V5'}
RUST_GENRES = {'lading':'romance, erotiek, intrige aan het hof','kronen':'romance, komedie, dorpsintrige','steden':'komedie, mysterie, familiesaga','machines':'mysterie, familiesaga, stille horror'}
GEBEURTENIS = [
 ('kern_valt','De kern onder Hoornburg valt stil. Kharvos heeft een nieuwe nodig.', .03, lambda s,y: y < 1800, dict(buren=.3)),
 ('kern_in_worm','Wormvaarders vinden het Harrow-teken en de reservekern in een worm.', .015, lambda s,y: True, dict(puls=.5, worm=.2)),
 ('negen_cellen','De negen cellen van Hesta duiken op uit een kluis.', .015, lambda s,y: True, dict(puls=.4)),
 ('splinter','Een nieuwe splinter Sterrensteen wordt gevonden in de woestijn.', .03, lambda s,y: True, dict(puls=.25)),
 ('grote_drager','Er wordt een man geboren met de lading van een Vonkkoning.', .04, lambda s,y: s['K'] > .4, dict(puls=.2, dragers=.1)),
 ('schimmeljaar','Een natte zomer: de schimmel komt de steden in.', .05, lambda s,y: True, dict(schim=.4)),
 ('koude_eeuw','Een koude eeuw: de oogsten mislukken.', .025, lambda s,y: True, dict(F=-.2)),
 ('goede_eeuw','Een warme, natte eeuw: overvloed.', .03, lambda s,y: True, dict(F=.15)),
 ('aelthir_trek','De Aelthir verlaten hun wouden en trekken de heuvels in.', .03, lambda s,y: s['M'] < .5, dict(aelthir=-.2, isolatie=.2)),
 ('archief','In een ingestorte kelder ligt een archief van de Stille Zusters.', .03, lambda s,y: s['T'] > .2, dict(W=.15, f=.08)),
 ('nachtplaag','Een winter van nachtvlerken: in elk dorp sterven slapers.', .05, lambda s,y: s['nacht'] > .3, dict(nacht=.2, C=-.05)),
]

def run(seed, params=None, eind=5000):
    """Eén geschiedenis van 801 tot eind. Geeft fasen, gebeurtenissen, wetten, huizen, rustige tijden en een log per stap."""
    R = random.Random(seed)
    p = dict(groei=R.uniform(.12,.22), buren_honger=R.uniform(.5,1.5), ev=R.uniform(.7,1.3), aelthir=R.uniform(.2,.8),
             filter=R.uniform(.02,.06))
    if params: p.update(params)
    s = dict(P=.7, F=1.0, E=1.2, S=.3, L=.25, T=.05, O=.3, K=.7, Q=.5, mijn=.3, orrim=1.0, puls=0, Z=0, M=.8, rit=.1,
             C=.15, W=.4, f=.6, nacht=0, isolatie=0, r=.01)
    macht = dict(staat=.15, huizen=.35, kerk=.10, steden=.10, dragers=.25, buren=.30, orrim=.05)
    lijn = {k: dict(n=(.3 if k in ('worm','askoud') else 0), stadium=0, t=0) for k in LIJN}; lijn['aelthir']['n'] = .6
    fasen, laatst_gebruikt, log, gebeurd, tw = [], {}, [], [], []
    wetboek = {w: 801 for w in WET_801}; wetten = []           # wetten: (jaar, 'in'/'uit', wetcode, tekst, door)
    huizen = [dict(naam=n, code=c, ouder=None, van=801, tot=None) for n, c in HUIZEN_801]
    heerser = ['Varenne']; huislog = [dict(jaar=801, soort='heerst', huis='Varenne', ouder=None)]
    rust = []
    vorig = dict(beslisser='Liora', betaler='Teo', vervalst='één registerblad', ontdekt='ja', schaal='wereld')
    laatste, vorige, tak, jaar = 801, None, 0, 801
    def wet_in(code, tekst, door):
        if code not in wetboek: wetboek[code] = jaar; wetten.append(dict(jaar=jaar, soort='in', wet=code, tekst=tekst, door=door))
    def wet_uit(code, door):
        if code in wetboek: del wetboek[code]; wetten.append(dict(jaar=jaar, soort='uit', wet=code, tekst='', door=door))
    def nieuw_huis(ouder, waarom):
        bestaand = {h['naam'] for h in huizen}
        for _ in range(40):
            naam = f"{ouder.split(' van ')[0]} van {R.choice(PLAATS)}"
            if naam not in bestaand: break
        else:
            naam = f"{ouder.split(' van ')[0]} de {len(bestaand)}e"
        huizen.append(dict(naam=naam, code=None, ouder=ouder, van=jaar, tot=None))
        huislog.append(dict(jaar=jaar, soort='ontstaat', huis=naam, ouder=ouder, waarom=waarom)); return naam
    def wissel_heerser(waarom, nieuw=None):
        oud = heerser[0]
        levend = [h for h in huizen if h['tot'] is None and h['naam'] != oud]
        nieuw = nieuw or (R.choice(levend)['naam'] if levend and R.random() < .6 else nieuw_huis(R.choice([h['naam'] for h in huizen if h['tot'] is None]), waarom))
        if R.random() < .5:
            for h in huizen:
                if h['naam'] == oud and h['tot'] is None: h['tot'] = jaar; huislog.append(dict(jaar=jaar, soort='valt', huis=oud, ouder=None, waarom=waarom))
        heerser[0] = nieuw; huislog.append(dict(jaar=jaar, soort='heerst', huis=nieuw, ouder=None, waarom=waarom))
    def zet(k, v):
        if k in macht: macht[k] = max(.02, macht[k] + v)
        elif k in lijn: lijn[k]['n'] = min(1, max(0, lijn[k]['n'] + v))
        elif k == 'nacht': s['nacht'] = max(0, s['nacht'] + v); lijn['nacht']['n'] = max(0, lijn['nacht']['n'] + v)
        elif k == 'askoud': lijn['askoud']['n'] = min(1, lijn['askoud']['n'] + v)
        elif k in s: s[k] = max(0, s[k] + v) if k in ('P','F','E','puls','Q') else min(1, max(0, s[k] + v))
    # 801 zelf: het Zegel zegt geen ja meer (BESLUIT-Z36-4); de Hoge Moeder kan niemand meer berechten
    jaar = 801; wet_uit('RECHT-gavenrecht', 'de val van de Orde')
    while jaar < eind:
        jaar += STAP
        for gid, tekst, kans, cond, eff in GEBEURTENIS:
            once = gid in ('kern_valt','kern_in_worm','negen_cellen')
            if once and any(g['id'] == gid for g in gebeurd): continue
            if cond(s, jaar) and R.random() < kans * p['ev']:
                for k, v in eff.items(): zet(k, v)
                gebeurd.append(dict(jaar=jaar, id=gid, tekst=tekst))
        # 0 de filter verslapt: meer jongens, minder van hen dragers (ORIGIN-10-Z36; KEUZE-Z42-verhouding)
        s['r'] += p['filter'] * (.5 - s['r'])
        dragers = min(1, .01 / s['r'])
        if s['r'] > .12: wet_uit('WET-deelwet-recht', 'er zijn weer genoeg mannen'); wet_in('W-huwelijk', 'Een man en een vrouw mogen weer trouwen', 'de moederhuizen')
        if s['r'] > .25: wet_uit('WET-wie-gewone-man', 'mannen zijn geen schaars bezit meer'); wet_in('W-mannenbezit', 'Een man mag bezit hebben en getuigen', 'de steden')
        if s['r'] > .4: wet_in('W-gelijkerfrecht', 'Zonen en dochters erven gelijk', 'de kroon')
        # 1 bevolking en voedsel
        s['F'] = max(.4, s['F'] * .98 + .02 * (1 + 2.5 * s['T']) + (.03 * s['M'] if macht['dragers'] > .2 else 0))
        s['P'] += p['groei'] * s['P'] * (1 - s['P'] / s['F'])
        # 2 elites: groeien als het volk goedkoop is
        s['E'] = max(.6, s['E'] + .07 * (s['P'] / s['F'] - .8) + .005)
        # 3 staat: belasting min kosten
        s['S'] = min(1, max(0, s['S'] + .05 * s['P'] * (.5 + s['L']) - .028 * s['E'] - .02 * (1 - s['C'])))
        macht['staat'] = max(.02, macht['staat'] + .02 * (s['S'] - .4))
        # 4 buren worden hongerig
        macht['buren'] = max(.05, macht['buren'] + .01 * p['buren_honger'] - .005)
        # 5 techniek: groeit in rust en openheid, trager als magie het werk doet
        s['T'] = min(1, s['T'] + .006 * (.5 + s['O']) * (1 - .5 * min(1, s['M'])) * (.5 + s['C']))
        s['O'] = min(1, max(0, s['O'] + .008 * (s['T'] - .15) + .006 * (macht['steden'] - macht['huizen']) - .03 * (s['E'] - 1.15)))
        # magie: bodem uit Orrim-steen, golf uit gesloten lijnen, pieken uit fragmenten
        s['Q'] += .03 * s['orrim']
        oogst = min(s['Q'], s['mijn'] * s['Q'] * .3)
        s['Q'] -= oogst
        s['orrim'] = min(1.5, max(.05, s['orrim'] + .01 - .05 * s['mijn'] * s['orrim']))
        s['K'] = min(1, max(0, s['K'] + .06 * ((1 - s['O']) - s['K'])))
        s['puls'] *= .75; s['Z'] = max(0, s['Z'] - .04)
        verdun = .35 + .65 * math.exp(-(jaar - 801) / 1500)
        bodem = .12 + .25 * min(1, oogst * 2) + .1 * s['rit']
        s['M'] = round(bodem + .55 * s['K'] * verdun + s['puls'] + .3 * s['Z'], 3)
        s['mijn'] = min(1, max(.05, s['mijn'] + .02 * (macht['huizen'] + macht['dragers'] - .5) - (.03 if 'W-orrimdoden' in wetboek else 0)))
        # wezens: lading doorgegeven aan wie haar niet draagt (ORIGIN-WAAROM-9)
        s['nacht'] = min(1, s['nacht'] * .93 + .12 * s['M'] * s['O'] * (1 - dragers) * (.5 if 'W-nachtwet' in wetboek else 1))
        lijn['nacht']['n'] = max(lijn['nacht']['n'] * .97, s['nacht'])
        lijn['askoud']['n'] = min(1, lijn['askoud']['n'] * .98 + .02 * s['M'])
        lijn['schim']['n'] *= .85
        # beschaving, geloof, waarheid
        s['C'] = min(1, s['C'] + .01 + .01 * s['T'])
        s['L'] = min(1, max(0, s['L'] + .012 * (macht['kerk'] - .15) - .012 * s['T'] + .004))
        verteller = max(macht, key=macht.get)
        d = .028 + (.02 if verteller in ('kerk','dragers','huizen') else 0) - .015 * p['aelthir'] * lijn['aelthir']['n'] - .02 * s['T']
        if 'W-boekverbod' in wetboek: d += .01
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
        tw.append(s['M']); gem = sum(tw[-15:]) / len(tw[-15:])
        eigen = s['S'] * s['P'] * (1 + macht['dragers'] * s['M'])
        druk = dict(
            honger = (s['P'] / s['F'] - .93) * 5,
            elitestrijd = (s['E'] - 1.4) * 1.2 * (1.3 - s['S']),
            bankroet = (.12 - s['S']) * 6,
            invasie = (macht['buren'] - eigen) * 1.5,
            epidemie = lijn['schim']['n'] * 2.0 * (.5 + s['O']),
            uitvinding = 0,
            geloof = (.38 - s['L']) * 4,
            opleving = (s['M'] - gem - .12) * 5,
            orrim = (s['mijn'] - .55) * 3 * s['orrim'],
            wezens = max(lijn['nacht']['n'], .7 * lijn['askoud']['n']) * 1.4,
            vondst = (s['T'] - .45) * 2 + s['W'] * .4 if s['T'] > .45 else 0,
        )
        for drempel in (.2, .35, .5, .65, .8):
            if s['T'] >= drempel and ('T%s' % drempel) not in laatst_gebruikt:
                druk['uitvinding'] = 1.5; laatst_gebruikt['T%s' % drempel] = jaar; break
        if vorige: druk[vorige] *= .5
        crisis = max(druk, key=druk.get)
        tijd = 'lading' if s['M'] > .9 else 'machines' if s['T'] > .6 else 'steden' if s['T'] > .35 else 'kronen'
        era = ('Smeedtijd' if s['Z'] > .15 else 'Ruwe Jaren' if s['C'] < .4 else 'Tijd van de ' + tijd)
        log.append(dict(jaar=jaar, M=s['M'], bodem=round(bodem,3), T=round(s['T'],3), P=round(s['P']/s['F'],3), S=round(s['S'],3),
                        E=round(s['E'],3), C=round(s['C'],3), f=round(s['f'],3), r=round(s['r'],3), L=round(s['L'],3), O=round(s['O'],3),
                        orrim=round(s['orrim'],3), era=era, tak=tak, heerser=heerser[0], wetten=len(wetboek),
                        macht={k: round(v,2) for k,v in macht.items()},
                        lijn={k:l['stadium'] for k,l in lijn.items() if l['n']>.1 or l['stadium']>0}))
        if druk[crisis] < .5 or jaar - laatste < 60: continue
        EENMALIG = ('erkenning','censuur','wieg','drukpers','stoom','ijzer','steenlens','smeden','orrimrecht')
        opties = [o for o in MENU[crisis] if jaar - laatst_gebruikt.get(o['id'], -9999) > 600 and not (o['id'] in EENMALIG and o['id'] in laatst_gebruikt)]
        if not opties: continue
        verschil = lambda o: sum(o[a] != vorig[a] for a in AXES)
        rijmend = [o for o in opties if verschil(o) >= 3]
        keuze = R.choice(rijmend or opties)
        terug = keuze['id'] in laatst_gebruikt
        laatst_gebruikt[keuze['id']] = jaar
        if keuze['id'] == 'erkenning': laatst_gebruikt['censuur'] = jaar + 9999
        for k, v in keuze['eff'].items(): zet(k, v)
        if keuze['id'] in WET:
            code, tekst, weg = WET[keuze['id']]
            for w in weg: wet_uit(w, keuze['beslisser'])
            wet_in(code, tekst, keuze['beslisser'])
        if crisis == 'honger': s['P'] *= .85
        if crisis == 'elitestrijd':
            s['E'] = max(.8, s['E'])
            if keuze['id'] in ('burgeroorlog','dragerstoernooi'): wissel_heerser(keuze['naam'])
            if keuze['id'] == 'verbanning': nieuw_huis(heerser[0], 'verbannen zonen')
        if crisis == 'invasie':
            macht['buren'] *= .6
            if keuze['id'] == 'nederlaag': wissel_heerser(keuze['naam'], nieuw_huis('Kharvos', 'de nederlaag in het noorden'))
        if keuze['id'] in ('dragerskoningen', 'bankiers', 'eedsteden'): wissel_heerser(keuze['naam'])
        if crisis == 'epidemie': lijn['schim']['n'] *= .4; s['P'] *= .85
        if crisis == 'wezens': lijn['nacht']['n'] *= .6; s['nacht'] *= .6
        if crisis in ('elitestrijd','invasie'): s['C'] = max(0, s['C'] - .1)
        if fasen: fasen[-1]['tot'] = jaar
        if jaar - laatste >= 200 and laatste > 801:
            rust.append(dict(van=laatste + STAP, tot=jaar - STAP, tijd=tijd, genres=RUST_GENRES[tijd]))
        fasen.append(dict(van=jaar, crisis=crisis, id=keuze['id'], naam=keuze['naam'], blijvend=keuze['blijvend'],
                          terug=terug, rijm=verschil(keuze), M=s['M'], era=era, heerser=heerser[0], **{a: keuze[a] for a in AXES}))
        vorig, laatste, vorige = keuze, jaar, crisis
    if fasen: fasen[-1]['tot'] = jaar
    if jaar - laatste >= 200: rust.append(dict(van=laatste + STAP, tot=jaar, tijd=tijd, genres=RUST_GENRES[tijd]))
    return dict(seed=seed, p={k:round(v,3) for k,v in p.items()}, fasen=fasen, log=log, gebeurd=gebeurd,
                wetten=wetten, wetboek_eind=sorted(wetboek), huizen=huizen, huislog=huislog, rust=rust)

def versie(f, tak):
    for d, a, b in VERSIE:
        if f >= d: return b if (tak and b) else a
    return VERSIE[-1][1]

if __name__ == '__main__':
    for sd in map(int, sys.argv[1:] or ['1']):
        o = run(sd); print('seed', sd, o['p'])
        print('   wetten:', [(w['jaar'], w['soort'], w['wet']) for w in o['wetten']][:14])
        print('   huizen:', [(h['jaar'], h['soort'], h['huis']) for h in o['huislog']][:10])
        print('   rust:', [(x['van'], x['tot'], x['tijd']) for x in o['rust']])
        for x in o['fasen']: print('  %d %-11s M=%.2f | %s%s' % (x['van'], x['crisis'], x['M'], x['naam'], ' (keert terug)' if x['terug'] else ''))
        ms=[x['M'] for x in o['log']]; print('   M min %.2f max %.2f eind %.2f  T eind %.2f' % (min(ms), max(ms), ms[-1], o['log'][-1]['T']))
