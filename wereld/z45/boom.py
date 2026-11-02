"""Ronde Z45: de technologieboom, tweede laag. Gegevens, geen motor.
Een vereiste "A|B" betekent: A of B. Een gewone uitvinding heeft zo vaak een Velmara-weg en een Kharvos-weg.

Op verzoek van Rogier (2026-11-02):
  1 per uitvinding staat waar ze voor gebruikt wordt, door wie, wat ze een gewoon mens kost, en waar ze in onze wereld op lijkt;
  2 gewone uitvindingen komen erbij (molen, uurwerk, lens, drukpers, kruit, stoom, spoor, elektriciteit, telegraaf, vaccin),
    maar elk groeit uit een Velmara-voorganger, zodat ze passen bij wat er al is;
  3 de brug naar gewone techniek is Kharvos: de Harrow koos voor machines (BESLUIT-3, ORIGIN-Z1-harrow) en buiten Velmara
    is techniek machinaal (TECH-GESCH-12-V4); via handel, oorlog en spionage komt het smeden en het raderwerk binnen;
  4 magische techniek (gave, zegelsteen) gaat verloren als haar bron opdroogt; de kennis blijft, de praktijk niet.
    Zo groeit de wereld grofweg naar een gewone tijd, rond onze negentiende eeuw.

Correctie op Z44: ORIGIN-2 zegt 'geen brandstof voor de scheepskernen', niet 'geen brandstof'. Hout en houtskool bestaan
(de wouden van de Aelthir, de jungle van Groenmuil), en in Hoogvrouwe wordt zilver gewonnen (REG-hoogvrouwe). Stoom en kruit
zijn daarom niet onmogelijk, alleen laat: ze hebben metaal nodig, en dat komt via Kharvos en roestlak."""
import importlib.util as _iu, os
_s = _iu.spec_from_file_location('z44_boom', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'z44', 'boom.py'))
Z44 = _iu.module_from_spec(_s); _s.loader.exec_module(Z44)
Z44.AFSTOTING['gewoon'] = 2   # gewone techniek: nauwelijks afstotend
K = Z44.K
AFSTOTING = Z44.AFSTOTING

# 1 gebruik in het dagelijks leven bij de knopen van Z44: (gebruik, voor wie, aards equivalent, tijdperk, soort)
GEBRUIK = {
 'TK-kweekakker': ('schimmelbedden onder het graan; een dorp oogst ook in een koude zomer', 'dorpen met een kweker', 'kunstmest, gewassenveredeling', 'Ruwe Jaren', 'magisch-arm'),
 'TK-sporennet': ('briefjes in geur, van markt tot markt; alleen verwanten kunnen ze lezen', 'kooplieden en families', 'postdienst', 'Ruwe Jaren', 'magisch-arm'),
 'TK-roestlak': ('een laag levende hars over ploegijzer en zwaard', 'smeden en boeren met geld', 'roestwerende verf, verzinken', 'Smeedtijd', 'magisch-arm'),
 'TK-spiermolen': ('de molen van het dorp: een vat gekweekte spier die maalt en pompt, en elke dag graan eet', 'dorpen met overschot', 'watermolen, later motor', 'Smeedtijd', 'magisch-arm'),
 'TK-heelkweek': ('het gasthuis: heelslijm en gekweekte organen', 'iedereen met een gasthuis in de buurt', 'ziekenhuis, transplantatie', 'Smeedtijd', 'magisch-arm'),
 'TK-sporendruk': ('almanakken, pamfletten en verboden boeken, gedrukt door schimmel op harsvel', 'iedereen die kan lezen', 'blokdruk, vroege drukpers', 'Lange Afbouw', 'magisch-arm'),
 'TK-vrijladen': ('een laadster in elke stad laadt lampen, messen en hemden met het ja van een drager', 'wie betalen kan', 'ambacht met een zeldzame grondstof', 'Ruwe Jaren', 'magisch'),
 'TK-echonet': ('ringparen tussen hof en grensforten; een bericht in een ademtocht', 'de kroon en de legers', 'koeriersdienst, later telefoon', 'Smeedtijd', 'magisch'),
 'TK-laadwerkplaats': ('werkplaatsen waar dragers hun lading in werktuigen leggen', 'gilden in de steden', 'manufactuur', 'Smeedtijd', 'magisch'),
 'TK-lichtnet': ('spiegeltorens op de heuvels; berichten in lichtcodes', 'de kroon', 'optische telegraaf', 'Ruwe Jaren', 'magisch'),
 'TK-steenlens': ('vergrootglazen van Sterrensteen voor artsen en slijpers', 'gilden en gasthuizen', 'lens, microscoop', 'Smeedtijd', 'magisch'),
 'TK-lichtcel': ('lampen en werktuigen die op opgeslagen licht lopen, in rijke huizen', 'de rijken', 'batterij, gaslicht', 'Lange Afbouw', 'magisch'),
 'TK-kluisherstel': ('een hersteld kluiswerktuig in de kanselarij: een rekenrol, een lamp zonder vuur', 'de kroon en de Dhurn', 'herontdekte oudheid (zoals Grieks schrift in de renaissance)', 'Smeedtijd', 'magisch-arm'),
 'TK-lakijzer': ('ijzeren zwaarden en ploegen, gelakt tegen de schimmel', 'legers en rijke boeren', 'ijzertijd', 'Smeedtijd', 'magisch-arm'),
 'TK-gaveglas': ('de duurste lamp van Velmara: licht en warmte in één', 'de huizen', 'kroonluchter, centrale verwarming', 'Smeedtijd', 'magisch'),
 'TK-sporenkern': ('een dode kern die door schimmel weer brandt; verboden werkplaatsen', 'smokkelaars en durfals', 'vroege, gevaarlijke kernkracht', 'Lange Afbouw', 'magisch'),
 'TK-vleesmetaal': ('Leegtewormen met een kluiskern in de maag: snelle vaart, waanzinnige worm', 'de kroon en de Wormvaarders', 'stoomschip', 'Smeedtijd', 'magisch'),
}
# bron waarvan magische techniek leeft: als die 100 jaar wegvalt, gaat de praktijk verloren
VERVAL = {
 'TK-vrijladen': ('lading', 'magie onder 0,32'), 'TK-echonet': ('lading', 'magie onder 0,32'), 'TK-laadwerkplaats': ('lading', 'magie onder 0,32'),
 'TK-gaveglas': ('lading', 'magie onder 0,32'), 'TK-lichtnet': ('steen', 'geen steen meer uit de groeven'), 'TK-steenlens': ('steen', 'geen steen meer uit de groeven'),
 'TK-lichtcel': ('steen', 'geen steen meer uit de groeven'), 'TK-sporenkern': ('lading', 'magie onder 0,32'), 'TK-vleesmetaal': ('lading', 'magie onder 0,32'),
}

# 2 gewone uitvindingen, elk met een Velmara-voorganger (vereist) en een plek in het dagelijks leven
GEWOON = [
 K('TN-molen', 'Water- en windmolens', 'gewoon', 'kracht', [],
   'rust (beschaving 0,25)', lambda x: x['C'] >= .25,
   ['honger'], 'steden', dict(F=.08, T=.02),
   'de spiermolen als enige molen: water en wind eten niet', 'molenaars worden machtig; rivieren worden bezit',
   'REG-groenmuil;TECHNO-bio'),
 K('TN-kharvos', 'Kharvos-ambacht', 'gewoon', 'ambacht', [],
   'contact met Kharvos (handel, oorlog of spionage) van 0,3', lambda x: x['kharvos'] >= .3,
   ['invasie', 'bankroet'], 'steden', dict(T=.05, steden=.04, buren=-.03),
   'het idee dat machines van de vijand zijn', 'wie Kharvos-kennis haalt, heet verrader; overlopers en spionnen betalen',
   'BESLUIT-3;REG-kharvos-B1;ORIGIN-Z1-harrow;TECH-GESCH-12-V4'),
 K('TN-uurwerk', 'Uurwerk en kompas', 'gewoon', 'werktuig', ['TN-kharvos'],
   'techniek 0,3', lambda x: x['T'] >= .3,
   ['invasie', 'geloof'], 'steden', dict(O=.04, T=.03),
   'de tempelklok als enige maat van de dag', 'de kerk verliest de uren; schippers varen verder dan de Aelthir-kaarten reiken',
   'BESLUIT-3;KAL-kalender'),
 K('TN-lens', 'Glazen lenzen', 'gewoon', 'werktuig', ['TK-steenlens|TN-kharvos'],
   'glasblazers in de steden (aandeel 0,08)', lambda x: x['aandeel']('steden') >= .08,
   ['epidemie'], 'steden', dict(T=.03, schim=-.05),
   'de Sterrensteen als enige lens: gewoon glas vraagt geen Orrim', 'slijpers worden blind van het werk',
   'VOLK-dhurn;TECHNO-zegelsteen'),
 K('TN-drukpers', 'De drukpers', 'gewoon', 'schrift', ['TK-sporendruk|TN-uurwerk', 'TK-lakijzer|TN-kharvos'],
   'steden 0,10', lambda x: x['aandeel']('steden') >= .10,
   ['geloof', 'vondst'], 'steden', dict(kerk=-.08, W=.12, f=.06, O=.04),
   'het laatste woord van de kerk over wat waar is', 'kopiisten en sporendrukkers verliezen hun brood',
   'TECH-ITEM-bio-3;ORIGIN-2'),
 K('TN-kruit', 'Kruit', 'gewoon', 'wapen', ['TN-kharvos'],
   'techniek 0,35; salpeter uit de stallen', lambda x: x['T'] >= .35,
   ['invasie', 'elitestrijd'], 'staat', dict(dragers=-.1, staat=.05, volk=.02),
   'de drager en de muur als zekerheid in de oorlog', 'salpeter wordt gekrabd in de oude melkstallen; wie daar werkt, ademt de geschiedenis in',
   'FASE-markt;BESLUIT-3'),
 K('TN-stoom', 'De stoommachine', 'gewoon', 'kracht', ['TN-kharvos', 'TK-roestlak'],
   'techniek 0,45 en hout uit de wouden', lambda x: x['T'] >= .45,
   ['honger', 'bankroet'], 'steden', dict(T=.1, steden=.08, dragers=-.06, O=.04),
   'de spiermolen: een ketel eet hout, geen graan', 'de wouden van de Aelthir worden gekapt; mijnwerkers en stokers sterven jong',
   'BESLUIT-3;PLEK-Z4-nm-5-Z5b;ORIGIN-2'),
 K('TN-spoor', 'Spoorweg en stoomschip', 'gewoon', 'vervoer', ['TN-stoom'],
   'techniek 0,55', lambda x: x['T'] >= .55,
   ['honger', 'invasie'], 'staat', dict(O=.1, staat=.05, worm=-.15),
   'de Leegteworm als enige snelle reis', 'grond wordt onteigend; Wormvaarders verliezen hun vak',
   'TECHNO-bio-schip;TECH-ITEM-bio-1'),
 K('TN-elektriciteit', 'Elektriciteit', 'gewoon', 'kracht', ['TN-stoom', 'TK-vrijladen|TK-lichtcel|TK-echonet'],
   'techniek 0,6 en koper via Kharvos', lambda x: x['T'] >= .6 and x['kharvos'] >= .35,
   ['bankroet', 'geloof'], 'steden', dict(T=.1, steden=.06, dragers=-.08),
   'de lading als enige stroom: wat eerst een drager vroeg, vraagt nu een draad', 'koper uit Kharvos maakt de buren rijk; draden lopen door heilige grond',
   'TECHNO-gave;BESLUIT-3'),
 K('TN-telegraaf', 'Telegraaf', 'gewoon', 'communicatie', ['TN-elektriciteit', 'TK-lichtnet'],
   'techniek 0,65', lambda x: x['T'] >= .65,
   ['invasie'], 'staat', dict(O=.06, staat=.04),
   'het lichtnet en het echonet: een bericht heeft geen steen en geen gever meer nodig', 'spiegelwachters en ringdragers worden overbodig',
   'TECH-ITEM-zegelsteen-3;TECH-ITEM-gave-1'),
 K('TN-vaccin', 'Kiemleer en vaccinatie', 'gewoon', 'geneeskunde', ['TN-lens', 'TK-heelkweek|TK-kweekakker'],
   'beschaving 0,55', lambda x: x['C'] >= .55,
   ['epidemie'], 'steden', dict(schim=-.3, P=.06),
   'de schimmel als straf: onder de lens is het een levend ding', 'de eerste ingeënten zijn proefpersonen; de kerk noemt het heiligschennis',
   'TECHNO-bio;HORROR-SKELET-Z9-6'),
]
GEWOON_GEBRUIK = {
 'TN-molen': ('een molen aan elke beek; de molenaar is na de priesteres de rijkste van het dorp', 'elk dorp aan water of wind', 'watermolen, windmolen', 'Ruwe Jaren'),
 'TN-kharvos': ('smederijen en raderwerk naar Kharvos-model, vaak door overlopers opgezet', 'steden aan de pas', 'kennisoverdracht via handel en oorlog', 'Smeedtijd'),
 'TN-uurwerk': ('een klok op het stadhuis, een kompas op elk schip', 'steden en schippers', 'mechanisch uurwerk, kompas', 'Smeedtijd'),
 'TN-lens': ('brillen voor oude klerken, vergrootglazen voor artsen', 'wie kan lezen en wie geneest', 'bril, microscoop', 'Lange Afbouw'),
 'TN-drukpers': ('kranten, catechismussen en ketterse traktaten in duizenden', 'iedereen die kan lezen', 'drukpers (Gutenberg)', 'Lange Afbouw'),
 'TN-kruit': ('kanonnen aan de pas, musketten bij de stadswacht', 'legers', 'buskruit', 'Lange Afbouw'),
 'TN-stoom': ('pompen in de mijnen, weverijen in de steden', 'fabrieksheren en mijnen', 'stoommachine', 'Tijd van de werkplaatsen'),
 'TN-spoor': ('treinen tussen de steden, stoomboten op de Ysmer', 'reizigers en handel', 'spoorweg, stoomschip', 'Tijd van de werkplaatsen'),
 'TN-elektriciteit': ('lampen in de straten, motoren in de werkplaats', 'steden', 'elektriciteit', 'Het Gewone'),
 'TN-telegraaf': ('een telegraafkantoor in elke stad', 'kooplieden, kranten, de staat', 'telegraaf', 'Het Gewone'),
 'TN-vaccin': ('inenting tegen de schimmel; gasthuizen met een laboratorium', 'iedereen', 'vaccinatie, kiemtheorie', 'Het Gewone'),
}
for k in GEWOON:
    g = GEWOON_GEBRUIK[k['code']]
    k.update(gebruik=g[0], voor_wie=g[1], aards=g[2], tijdperk=g[3], soort='gewoon', vervalt_bij=None)
BOOM = []
for k in Z44.BOOM:
    g = GEBRUIK[k['code']]; v = VERVAL.get(k['code'])
    BOOM.append(dict(k, gebruik=g[0], voor_wie=g[1], aards=g[2], tijdperk=g[3], soort=g[4], vervalt_bij=v[1] if v else None, _bron_verval=v[0] if v else None))
for k in GEWOON: BOOM.append(dict(k, _bron_verval=None))
# de opvolger van een magische knoop (voor het verhaal: wat neemt zijn plaats in als hij verloren gaat)
OPVOLGER = {'TK-spiermolen': 'TN-stoom', 'TK-lichtcel': 'TN-elektriciteit', 'TK-lichtnet': 'TN-telegraaf', 'TK-echonet': 'TN-telegraaf',
            'TK-sporendruk': 'TN-drukpers', 'TK-steenlens': 'TN-lens', 'TK-vleesmetaal': 'TN-spoor', 'TK-heelkweek': 'TN-vaccin',
            'TK-vrijladen': 'TN-elektriciteit', 'TK-laadwerkplaats': 'TN-stoom', 'TK-gaveglas': 'TN-elektriciteit'}
GEWONE_TIJD = ['TN-stoom', 'TN-drukpers', 'TN-elektriciteit', 'TN-vaccin', 'TN-spoor']   # wanneer alle vijf er zijn: Het Gewone

# 3 wat Velmara niet doet: herzien
ONMOGELIJK = [x for x in Z44.ONMOGELIJK if x[0] not in ('TK-x-stoom', 'TK-x-kruit', 'TK-x-staal', 'TK-x-kolen')] + [
 ('TK-x-staal', 'Staal in grote hoeveelheid vóór het Kharvos-ambacht', 'onmogelijk', 'Erts is schaars (ORIGIN-2) en de roestschimmel eet legering (YSA-Z17-6); pas met roestlak en Kharvos-smeedkunst komt metaal in hoeveelheid.', 'ORIGIN-2;YSA-Z17-6;BESLUIT-3'),
]
HERZIEN = {   # Z44-knopen die in Z45 een andere status krijgen, met reden
 'TK-x-stoom': ('vervangen', 'Correctie Z45: ORIGIN-2 gaat over brandstof voor de scheepskernen, niet over hout. Stoom is mogelijk op hout, maar pas laat: zie TN-stoom (vereist Kharvos-ambacht en roestlak).'),
 'TK-x-kruit': ('vervangen', 'Correctie Z45: kruit is mogelijk (houtskool, salpeter uit de oude stallen), maar pas na het Kharvos-ambacht: zie TN-kruit.'),
 'TK-x-staal': ('vervangen', 'Aangescherpt in Z45: onmogelijk vóór het Kharvos-ambacht, zie TK-x-staal (nieuwe tekst).'),
 'TK-x-kolen': ('open', 'De canon zegt niets over steenkool; ORIGIN-2 noemt alleen brandstof voor de kernen. Open vraag voor Rogier (KEUZE-Z45-kolen).'),
}

def controleer():
    codes = {k['code'] for k in BOOM}
    for k in BOOM:
        for v in k['vereist']:
            for alt in v.split('|'): assert alt in codes, (k['code'], alt)
        for f in ('gebruik', 'voor_wie', 'aards', 'tijdperk', 'soort'): assert k.get(f), (k['code'], f)
    for a, b in OPVOLGER.items(): assert a in codes and b in codes
    def diep(c, pad=()):
        assert c not in pad, ('kring', pad)
        for v in next(k for k in BOOM if k['code'] == c)['vereist']:
            for alt in v.split('|'): diep(alt, pad + (c,))
    for k in BOOM: diep(k['code'])
    return len(BOOM)

if __name__ == '__main__':
    print(controleer(), 'knopen')
    for k in BOOM: print(f"{k['code']:<18} {k['soort']:<12} {k['tijdperk']:<24} vereist {k['vereist']} | lijkt op {k['aards']}")
