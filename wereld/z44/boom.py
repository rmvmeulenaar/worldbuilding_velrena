"""Ronde Z44: de technologieboom van Velmara na 801. Gegevens, geen motor.

Ontwerpregel (review 1): een uitvinding ontstaat pas als de wereld haar mogelijk maakt (vereisten en materiaal),
de geschiedenis haar nodig of aantrekkelijk maakt (noodzaak), en haar bestaan de volgende geschiedenis verandert (gevolg).

Alles komt uit de vier technieken die de canon al kent (TECHNO-REGEL-V4): bio, gave, zegelsteen en metaal, met hun
grondstoffen, energie, kosten en faalwijze (TECHNO-bio, TECHNO-gave, TECHNO-zegelsteen, TECHNO-metaal), en de mengvormen
uit TECHNO-MIX-V4. De beperkingen zijn die van de canon:
  - geen brandstof en weinig erts (ORIGIN-2), en de roestschimmel eet legering (YSA-Z17-6);
  - metaal kan niemand maken, alleen herstellen en kannibaliseren (TECHNO-metaal);
  - levende techniek moet eten (TECHNO-bio); lading kost de gever dagen (TECHNO-gave) en vraagt na 801 zijn eigen ja (BESLUIT-Z36-4);
  - zegelsteen komt uit Orrim-lichamen en de Sterrensteen, en barst bij overgebruik (TECHNO-zegelsteen, D1-orrim-geld).

Elke knoop: (code, naam, familie, domein, vereist, materiaal-voorwaarde als tekst + test, noodzaak (crisissoorten),
uitvinder (machtsleutel), gevolg (effect op toestand en macht), wat het breekt, prijs, canonbronnen)."""

AFSTOTING = {'bio': 8, 'gave': 4, 'zegelsteen': 3, 'metaal': 5}   # TECHNO-SCHAAL; mengvormen erven de hoogste

def K(code, naam, familie, domein, vereist, materiaal, test, noodzaak, uitvinder, gevolg, breekt, prijs, bron):
    fam = familie.split('+')
    return dict(code=code, naam=naam, familie=familie, domein=domein, vereist=vereist, materiaal=materiaal, test=test,
                noodzaak=noodzaak, uitvinder=uitvinder, gevolg=gevolg, breekt=breekt, prijs=prijs, bron=bron,
                afstoting=max(AFSTOTING[f] for f in fam))

BOOM = [
 # ---------- bio: vlees, bloed, schimmel, bot (TECHNO-bio) ----------
 K('TK-kweekakker', 'Kweekakkers', 'bio', 'voedsel', [],
   'rust (beschaving 0,3) en kwekers in de steden', lambda x: x['C'] >= .3 and x['aandeel']('steden') >= .06,
   ['honger'], 'steden', dict(F=.15, dragers=-.05, schim=.1),
   'de dragers als enigen die een mislukte oogst kunnen redden', 'kweekstammen worden ziek door inteelt; een uitbraak kan uit de akker komen',
   'TECHNO-bio;TECH-GESCH-1'),
 K('TK-sporennet', 'Het sporennet', 'bio', 'communicatie', [],
   'handel (openheid 0,3)', lambda x: x['O'] >= .3,
   ['geloof', 'vondst'], 'steden', dict(O=.05, W=.05, f=.03),
   'de kerk als enige die weet wat er in het land gebeurt', 'leest alleen voor verwanten; sporen in de longen van wie leest',
   'TECH-ITEM-bio-3;VOLK-myrrhen-Z6'),
 K('TK-roestlak', 'Roestlak', 'bio', 'bouw', [],
   'kwekers in de steden (aandeel 0,08)', lambda x: x['aandeel']('steden') >= .08,
   ['invasie', 'bankroet'], 'steden', dict(T=.03),
   'niets direct; het maakt metaal weer bruikbaar', 'lakkers ademen sporen; de lak leeft en moet gevoerd worden',
   'YSA-Z17-6;VOLK-kluwer;VOLK-myrrhen-Z6'),
 K('TK-spiermolen', 'Spiermolens', 'bio', 'kracht', ['TK-kweekakker'],
   'voedseloverschot, want spier moet eten (voedsel 5% boven bevolking)', lambda x: x['F'] >= 1.05 * x['P'],
   ['honger', 'bankroet'], 'steden', dict(T=.06, steden=.06, dragers=-.06, F=-.05),
   'de dragers als enige krachtbron naast mens en dier', 'het vlees lijdt en moet eten; in een hongerjaar eet de molen eerst',
   'TECHNO-bio;ORIGIN-4;ORIGIN-2'),
 K('TK-heelkweek', 'Heelkweek', 'bio', 'geneeskunde', ['TK-kweekakker'],
   'beschaving 0,4', lambda x: x['C'] >= .4,
   ['epidemie'], 'steden', dict(schim=-.2, P=.05),
   'de kloosters als enige plek waar je beter wordt', 'organen komen van iemand; de stam verwildert als je hem niet bewaakt',
   'TECHNO-bio;TECH-ITEM-bio-2'),
 # ---------- gave: lading van levende mannen (TECHNO-gave), na 801 alleen met hun eigen ja ----------
 K('TK-vrijladen', 'Vrije laadsters', 'gave', 'ambacht', [],
   'genoeg lading in de wereld (magie 0,4)', lambda x: x['M'] >= .4,
   ['opleving', 'elitestrijd'], 'dragers', dict(dragers=.05, kerk=-.03),
   'het laadmonopolie van de Registerkamer (TECHNO-TIJDLIJN fase 4)', 'de gever droogt uit; een geladen voorwerp kost hem dagen',
   'TECHNO-gave;BESLUIT-Z36-4;GAVE-Z37-ja'),
 K('TK-echonet', 'Het echonet', 'gave', 'communicatie', ['TK-vrijladen'],
   'magie 0,5', lambda x: x['M'] >= .5,
   ['invasie'], 'dragers', dict(O=.05, staat=.03),
   'de afstand tussen hof en grens', 'het net sterft met de gever',
   'TECH-ITEM-gave-1'),
 K('TK-laadwerkplaats', 'Laadwerkplaatsen', 'gave', 'kracht', ['TK-vrijladen'],
   'magie 0,55', lambda x: x['M'] >= .55,
   ['bankroet', 'honger'], 'dragers', dict(T=.05, dragers=.05, steden=.02),
   'niets; het maakt de dragers juist onmisbaar', 'uitputting van de gevers; wie te vaak geeft, wordt grijs',
   'TECH-ITEM-V4-gave-5;TECHNO-gave'),
 # ---------- zegelsteen: Sterrensteen en zegelglas (TECHNO-zegelsteen) ----------
 K('TK-lichtnet', 'Het lichtnet', 'zegelsteen', 'communicatie', [],
   'steen uit de groeven (mijnbouw 0,25)', lambda x: x['mijn'] >= .25,
   ['invasie', 'geloof'], 'staat', dict(staat=.05, O=.03),
   'de afstand tussen de kroon en haar provincies', 'Orrim-steen; elk bericht is af te luisteren',
   'TECH-ITEM-zegelsteen-3;TECHNO-zegelsteen'),
 K('TK-steenlens', 'De steenlens', 'zegelsteen', 'werktuig', ['TK-lichtnet'],
   'mijnbouw 0,3 en Dhurn in de steden', lambda x: x['mijn'] >= .3 and x['aandeel']('steden') >= .05,
   ['epidemie', 'vondst'], 'steden', dict(T=.05, schim=-.1),
   'de onzichtbaarheid van wat ziek maakt', 'koud licht dat de slijper verstijft; Orrim-steen',
   'VOLK-dhurn;TECHNO-zegelsteen'),
 K('TK-lichtcel', 'Lichtcellen', 'zegelsteen', 'kracht', ['TK-steenlens'],
   'mijnbouw 0,4', lambda x: x['mijn'] >= .4,
   ['bankroet', 'honger'], 'staat', dict(T=.07, dragers=-.05, mijn=.15),
   'de dragers als enige krachtbron', 'de vraag naar steen stijgt: meer Orrim in de groeven; de Sterrensteen barst bij overgebruik',
   'TECHNO-zegelsteen;D1-orrim-geld'),
 # ---------- metaal: niemand kan het maken, alleen herstellen (TECHNO-metaal, ORIGIN-2) ----------
 K('TK-kluisherstel', 'Kluisherstel', 'metaal', 'werktuig', [],
   'een vondst: een archief, de reservekern of de negen cellen', lambda x: bool(x['vondsten']),
   ['vondst', 'invasie'], 'staat', dict(T=.05, staat=.04),
   'het geheim van de Orde-kluizen', 'elk onderdeel is voorgoed weg; kernen stralen',
   'TECHNO-metaal;TECH-ITEM-metaal-4'),
 K('TK-lakijzer', 'Lakijzer', 'metaal', 'wapen', ['TK-roestlak'],
   'techniek 0,25; erts is schaars (ORIGIN-2)', lambda x: x['T'] >= .25,
   ['invasie', 'elitestrijd'], 'steden', dict(dragers=-.08, volk=.03, staat=.02),
   'de drager als onverslaanbare krijger', 'erts is schaars en mijnwerkers sterven; zonder lak eet de schimmel het zwaard',
   'ORIGIN-2;YSA-Z17-6'),
 K('TK-sporendruk', 'Sporendruk', 'bio', 'schrift', ['TK-sporennet'],
   'steden met macht (aandeel 0,10)', lambda x: x['aandeel']('steden') >= .10,
   ['geloof', 'vondst'], 'steden', dict(kerk=-.08, W=.1, f=.05, O=.03),
   'de kerk als enige die schrijft en bewaart', 'kopiisten verliezen hun werk; sporen in elk boek',
   'TECH-ITEM-bio-3;VOLK-myrrhen-Z6'),
 # ---------- mengvormen (TECHNO-MIX-V4) ----------
 K('TK-gaveglas', 'Gaveglas', 'gave+zegelsteen', 'licht', ['TK-vrijladen', 'TK-lichtnet'],
   'magie 0,5 en mijnbouw 0,3', lambda x: x['M'] >= .5 and x['mijn'] >= .3,
   ['geloof'], 'huizen', dict(C=.03, huizen=.03),
   'het donker van de winter voor wie het kan betalen', 'de duurste lamp van Velmara; een gever en een Orrim in elke lamp',
   'TECHNO-MIX-V4'),
 K('TK-sporenkern', 'De sporenkern', 'bio+metaal', 'kracht', ['TK-kluisherstel', 'TK-roestlak'],
   'techniek 0,5', lambda x: x['T'] >= .5,
   ['bankroet'], 'steden', dict(T=.1, schim=.25, puls=.1),
   'de grens tussen levende en dode techniek', 'verboden en onvoorspelbaar; uit de kern kan een uitbraak komen',
   'TECHNO-MIX-V4'),
 K('TK-vleesmetaal', 'Vleesmetaal', 'bio+metaal', 'schip', ['TK-kluisherstel'],
   'er zijn Leegtewormen', lambda x: x['worm'] > .1,
   ['invasie'], 'staat', dict(O=.05, worm=.2),
   'de lengte van een Leegtevaart', 'de worm lijdt pijn en wordt waanzinnig',
   'TECHNO-MIX-V4;TECH-ITEM-bio-1'),
]

# Wat Velmara niet doet, en waarom (vraag 27 van de nakijker)
ONMOGELIJK = [
 ('TK-x-stoom', 'De stoommachine', 'onmogelijk en onnodig', 'Er is geen brandstof (ORIGIN-2); spiermolens en lichtcellen leveren kracht zonder vuur.', 'ORIGIN-2'),
 ('TK-x-kolen', 'Kolenmijnen', 'onmogelijk', 'Velmara heeft geen brandstof voor de kernen en geen fossiele voorraad (ORIGIN-2).', 'ORIGIN-2'),
 ('TK-x-staal', 'Staal in grote hoeveelheid', 'onmogelijk', 'Er is weinig erts (ORIGIN-2) en de roestschimmel eet legering (YSA-Z17-6); alleen lakijzer in kleine hoeveelheid.', 'ORIGIN-2;YSA-Z17-6'),
 ('TK-x-kruit', 'Vuurwapens met kruit', 'onnodig', 'Metaal is te schaars en brandader, lichtspiegel en vonkpijl doen het werk al.', 'TECH-GESCH-10-V4'),
 ('TK-x-draadnet', 'Een stroomnet met draden', 'onnodig', 'Koper is schaars; lading en lichtcellen zijn de stroom van Velmara, en het echonet en het lichtnet dragen berichten.', 'TECHNO-gave;TECHNO-zegelsteen'),
 ('TK-x-rekenmachine', 'Zelfgebouwde rekenmachines', 'onmogelijk', 'Machinekennis is verboden en vergeten (ORIGIN-7); er is alleen herstel van kluisresten (TECH-ITEM-metaal-8).', 'ORIGIN-7;TECH-ITEM-metaal-8'),
 ('TK-x-kern', 'Nieuwe energiekernen', 'onmogelijk', 'Kernen kunnen niet worden bijgevuld of gemaakt (ORIGIN-2, TECHNO-metaal).', 'ORIGIN-2;TECHNO-metaal'),
]

def controleer():
    codes = {k['code'] for k in BOOM}
    for k in BOOM:
        for v in k['vereist']: assert v in codes, (k['code'], v)
    # geen kringen
    seen = {}
    def diep(c, pad=()):
        assert c not in pad, ('kring', pad)
        for v in next(k for k in BOOM if k['code'] == c)['vereist']: diep(v, pad + (c,))
    for k in BOOM: diep(k['code'])
    return len(BOOM)

if __name__ == '__main__':
    print(controleer(), 'knopen,', len(ONMOGELIJK), 'onmogelijk of onnodig')
    for k in BOOM: print(f"{k['code']:<18} {k['familie']:<16} vereist {k['vereist']} | {k['materiaal']}")
