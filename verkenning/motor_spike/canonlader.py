"""Canonlader: zet de hele canon (canon.db) om in tijdgebonden feiten. Leest alleen; de canon blijft de bron.

Wat expliciet een AANNAME is (bv. levensvensters afgeleid uit een fase), krijgt epistemiek 'aanname', zodat de poort
en de mens het verschil zien tussen wat de canon zegt en wat de motor veronderstelt.
"""
from __future__ import annotations
import sqlite3, re
from .schema import Feit, Bron, Epistemiek, Predicaat, Soort
from .feiten import Feiten

P = lambda naam, ond, obj, f=False, om='': (naam, Predicaat(naam=naam, onderwerp=tuple(ond), object=obj, functioneel=f, omschrijving=om))
PERS, ALLES = ('persoon',), tuple(s.value for s in Soort)
PREDICATEN = dict([
    P('soort', ALLES, 'tekst', True, 'wat voor entiteit dit is'),
    P('naam', ALLES, 'tekst', True), P('volk', PERS, 'tekst', True), P('regio', PERS + ('plek',), 'tekst', True),
    P('rol', PERS, 'tekst'), P('fase', PERS + ('canonrij',), 'getal'), P('geboren', PERS, 'jaar', True), P('sterft', PERS, 'jaar', True),
    P('leeft_van', PERS, 'jaar', True, 'aanname: vroegste jaar waarin de persoon leeft'),
    P('leeft_tot', PERS, 'jaar', True, 'aanname: laatste jaar waarin de persoon leeft'),
    P('leeftijd_band', PERS, 'tekst', True), P('canonjaar', PERS, 'jaar', True),
    P('wil', PERS, 'tekst'), P('verbergt', PERS, 'tekst'), P('einde', PERS, 'tekst', True),
    P('geheim_van', ('geheim',), 'entiteit:persoon', True), P('inhoud', ('geheim',), 'tekst', True),
    P('weet', PERS, 'entiteit:geheim', False, 'kennis: deze persoon weet dit geheim'),
    P('verblijft_in', PERS, 'entiteit:plek', True), P('woont_in', PERS, 'entiteit:plek', True),
    P('partner_van', PERS, 'entiteit:persoon'), P('ouder_van', PERS, 'entiteit:persoon'), P('kind_van', PERS, 'entiteit:persoon'),
    P('broer_zus_van', PERS, 'entiteit:persoon'), P('schuldig_aan', PERS, 'entiteit:persoon'), P('verraden_door', PERS, 'entiteit:persoon'),
    P('rivaal_van', PERS, 'entiteit:persoon'), P('eed_aan', PERS, 'entiteit:persoon'), P('wil_hetzelfde_als', PERS, 'entiteit:persoon'),
    P('verbonden_met', PERS, 'entiteit:persoon'), P('meester_van', PERS, 'entiteit:persoon'),
    P('tijdperk', ALLES, 'tekst', True), P('status', ALLES, 'tekst', True), P('onderwerp', ALLES, 'tekst', True),
    P('leunt_op', ALLES, 'entiteit:canonrij'), P('langlevend', PERS + ('volk',), 'waar', True),
    P('hoofdlijn', PERS, 'waar', True, 'afloop ligt vast in de canon (boek 1)'),
    P('in_regio', ('plek',), 'entiteit:plek', True),
    # context van een voorstel (alleen in de laag van de poort, nooit opgeslagen)
    P('handeling', ('voorstel',), 'tekst', True), P('seksueel', ('voorstel',), 'waar', True), P('jaar', ('voorstel',), 'jaar', True),
    P('plek', ('voorstel',), 'entiteit:plek', True), P('dwang_label', ('voorstel',), 'waar', True),
    P('neemt_deel', PERS + ('dier',), 'entiteit:voorstel'), P('instemming', PERS + ('dier',), 'waar', True), P('rol_in', PERS + ('dier',), 'tekst'),
])

# Fasevensters in Zegeljaren (uit FASE-rijen in de canon; Voortijd begint bij de landing, ca. -1240)
FASEVENSTER = {0: (-1260, -600), 1: (-600, -150), 2: (-150, -40), 3: (-40, 0), 4: (0, 130), 5: (130, 340), 6: (340, 720), 7: (720, 801), 801: (790, 801), 8: (790, 801)}
HOOFDLIJN_NAMEN = ('Liora', 'Teo van Hallowyn', 'Aeron-as', 'Hoge Moeder Ithrael')
LANGLEVEND_VOLK = ('aelthir',)   # aanname: de Aelthir (feeënhoven) leven eeuwen; Vaelorn leeft in fase 1 en in 801
LEVEND = ('vastgesteld', 'voorlopig')

def soort_van(code: str, categorie: str = '') -> str:
    p = code.split('-')[0]
    if p in ('PER', 'PERS', 'SIMF', 'OP'): return 'persoon'
    if p in ('REG', 'STAD', 'PLEK'): return 'plek'
    if p == 'VOLK': return 'volk'
    if p in ('HUI', 'HUIS'): return 'huis'
    if p == 'GEB': return 'gebeurtenis'
    if categorie in ('Dieren', 'Planten en dieren') and p in ('DIER', 'FAUNA', 'BEEST'): return 'dier'
    return 'canonrij'


def laad(db_pad: str) -> Feiten:
    c = sqlite3.connect(db_pad)
    F = Feiten(PREDICATEN)
    CAN = Bron(soort='canon')
    def b(code=None, detail=None, soort='canon'): return Bron(soort=soort, code=code, detail=detail)
    def voeg(s, p, o, van=None, tot=None, bron=CAN, epi=Epistemiek.feit, kern=False):
        if o is None or o == '': return
        F.voeg(Feit(onderwerp=s, predicaat=p, object=o, van=van, tot=tot, bron=bron, epistemiek=epi, kern=kern))

    # 1. canonrijen (levend): soort, onderwerp, tijdperk, status; Kern gemarkeerd
    for code, cat, ond, st, tp, dk in c.execute(f"select code,categorie,onderwerp,status,tijdperk,draagkracht from canon where code is not null and status in {LEVEND}"):
        kern = dk == 'Kern'; s = soort_van(code, cat or '')
        if s == 'persoon': s = 'canonrij'   # personen komen uit persoon_identiteit (stap 2); PER-canonrijen zijn beschrijvingen
        if (cat or '') in ('Dieren',) : s = 'dier'
        voeg(code, 'soort', s, bron=b(code), kern=kern); voeg(code, 'onderwerp', ond, bron=b(code), kern=kern)
        voeg(code, 'tijdperk', tp, bron=b(code), kern=kern); voeg(code, 'status', st, bron=b(code), kern=kern)
    for code, ond in c.execute(f"select code,onderwerp from canon where status in {LEVEND} and (code like 'REG-%' or code like 'STAD-%' or code like 'PLEK-%')"):
        voeg(code, 'naam', ond)
    # regio van plekken (STAD/PLEK -> REG via verwijzing of tekst)
    regios = {r[0]: r[0].split('-')[1] for r in c.execute("select code from canon where code like 'REG-%' and status in ('vastgesteld','voorlopig')")}
    regio_code = {}
    for code, kort in regios.items(): regio_code.setdefault(kort, code)
    for code, feit in c.execute(f"select code,feit from canon where status in {LEVEND} and (code like 'STAD-%' or code like 'PLEK-%')"):
        m = re.search(r'Regio:\s*([a-zà-ÿ\-]+)', feit or '', re.I)
        if m and m.group(1).lower() in regio_code: voeg(code, 'in_regio', regio_code[m.group(1).lower()])
    for code in regios: voeg(code, 'in_regio', code)

    # 2. personen: één persoon = één knoop (persoon_identiteit)
    pid = dict(c.execute('select code,persoon from persoon_identiteit'))
    rel_jaar = {}
    for a, s_, b_ in c.execute("select van_code,soort,naar_code from relatie where soort in ('sterft_in','geboren_in')"):
        m = re.match(r'JAAR:(-?\d+)', b_ or '')
        if m: rel_jaar[(pid.get(a, a), s_)] = int(m.group(1))
    cols = ['code', 'naam', 'volk', 'regio', 'rol', 'fase_nr', 'jaar', 'geboren', 'leeftijd_band', 'wil', 'verbergt', 'geheim', 'einde']
    per = {}
    for r in c.execute('select ' + ','.join(cols) + ' from personage_profiel'):
        d = dict(zip(cols, r)); p = pid.get(d['code'], d['code']); per.setdefault(p, []).append(d)
    for p, ds in per.items():
        voeg(p, 'soort', 'persoon')
        for d in ds:
            bp = b(d['code'], 'personage_profiel')
            for k, pred in (('naam', 'naam'), ('volk', 'volk'), ('leeftijd_band', 'leeftijd_band'), ('einde', 'einde')):
                if d[k] and not F.een(p, pred): voeg(p, pred, d[k], bron=bp)
            if d['regio'] and not F.een(p, 'regio'): voeg(p, 'regio', regio_code.get(d['regio'].lower(), 'REG-' + d['regio'].lower()), bron=bp)
            for k in ('rol', 'wil', 'verbergt'): voeg(p, k, d[k], bron=bp)
            if d['fase_nr'] is not None: voeg(p, 'fase', int(d['fase_nr']), bron=bp)
            if d['geboren'] is not None and not F.een(p, 'geboren'): voeg(p, 'geboren', int(d['geboren']), bron=bp)
            if d['jaar'] is not None and not F.een(p, 'canonjaar'): voeg(p, 'canonjaar', int(d['jaar']), bron=bp)
            if d['geheim']:
                g = p + '#geheim'
                voeg(g, 'soort', 'geheim', bron=bp); voeg(g, 'geheim_van', p, bron=bp); voeg(g, 'inhoud', d['geheim'], bron=bp)
                voeg(p, 'weet', g, bron=bp)
        for s_, pred in (('geboren_in', 'geboren'), ('sterft_in', 'sterft')):
            if (p, s_) in rel_jaar and not F.een(p, pred): voeg(p, pred, rel_jaar[(p, s_)], bron=b(p, 'relatie ' + s_))
        volk = F.een(p, 'volk')
        if volk in LANGLEVEND_VOLK: voeg(p, 'langlevend', True, bron=b(None, 'aanname langlevend volk'), epi=Epistemiek.aanname)
        naam = F.een(p, 'naam') or ''
        if any(naam.startswith(h) for h in HOOFDLIJN_NAMEN): voeg(p, 'hoofdlijn', True, bron=b(p, 'hoofdlijn boek 1'))
        _levensvenster(F, p)

    # 3. simulatiefiguren, verblijf en kennis (epistemiek: simulatie)
    for code, naam, volk, gesl, plek, geb, run in c.execute('select code,naam,volk,geslacht,plek_code,geboren,run_id from sim_figuur'):
        bs = b(run, 'sim_figuur', 'simulatie')
        for pr, o in (('soort', 'persoon'), ('naam', naam), ('volk', volk), ('regio', plek), ('geboren', geb)):
            voeg(code, pr, o, bron=bs, epi=Epistemiek.simulatie)
        _levensvenster(F, code)
    for per_, plek, van, tot, epi in c.execute('select per_code,plek_code,van_jaar,tot_jaar,epistemiek from verblijf'):
        if plek and plek.startswith('REG-'):
            voeg(pid.get(per_, per_), 'verblijft_in', plek, van, tot, b(None, 'verblijf', 'simulatie'), Epistemiek.simulatie)
    for per_, weet, sinds, epi in c.execute('select per_code,weet_code,sinds_jaar,epistemiek from kennis'):
        p = pid.get(per_, per_); g = weet.split('#')[0]; g = pid.get(g, g) + ('#geheim' if '#' in weet else '')
        if not F.bestaat(g):
            voeg(g, 'soort', 'geheim', bron=b(None, 'kennis')); voeg(g, 'geheim_van', g.split('#')[0], bron=b(None, 'kennis'))
        voeg(p, 'weet', g, sinds, None, b(None, 'kennis', 'simulatie'), Epistemiek.simulatie if (epi or '').startswith('sim') else Epistemiek.aanname)

    # 4. sociale relaties uit de canon (niet de simulatie: die gaat als gebeurtenissen door het logboek)
    for a, s_, b_, vj, tj, br in c.execute("select van_code,soort,naar_code,van_jaar,tot_jaar,bron from relatie where soort in ('partner_van','ouder_van','kind_van','broer_zus_van','woont_in','meester_van')"):
        a2, b2 = pid.get(a, a), pid.get(b_, b_)
        if s_ == 'woont_in': b2 = b2 if b2.startswith(('REG', 'STAD', 'PLEK')) else b2
        voeg(a2, s_, b2, vj, tj, b(None, 'relatie ' + (br or '')))
    # 5. verwijzingsgraaf (voor ophalen van context door de verteller)
    for a, b_ in c.execute("select van_code,naar_code from relatie where soort='leunt_op'"):
        voeg(pid.get(a, a), 'leunt_op', pid.get(b_, b_))
    # 6. uitzonderingen op tijd (bewust buiten de eigen fase, toets_uitzondering graaf_tijd)
    for code, per_ in c.execute("select code,detail from toets_uitzondering where toets='graaf_tijd'"):
        voeg(pid.get(per_, per_), 'langlevend', True, bron=b(code, 'toets_uitzondering graaf_tijd'), epi=Epistemiek.aanname)
    return F


def _levensvenster(F: Feiten, p: str):
    """Aanname over wanneer iemand leeft, als de canon geen geboorte- of sterfjaar geeft. Gebruikt door regel R-T3."""
    A = Bron(soort='afleiding', code=p, detail='levensvenster')
    g, s, cj = F.een(p, 'geboren'), F.een(p, 'sterft'), F.een(p, 'canonjaar')
    fasen = [f.object for f in F.vind(p, 'fase')]
    if g is not None: van, tot = g, (s if s is not None else g + 90)
    elif cj is not None: van, tot = cj - 70, (s if s is not None else cj + 70)
    elif fasen:
        vs = [FASEVENSTER.get(int(x)) for x in fasen if int(x) in FASEVENSTER]
        if not vs: return
        van, tot = min(v[0] for v in vs) - 60, max(v[1] for v in vs) + 60
    else: return
    F.voeg(Feit(onderwerp=p, predicaat='leeft_van', object=van, bron=A, epistemiek=Epistemiek.aanname))
    F.voeg(Feit(onderwerp=p, predicaat='leeft_tot', object=tot, bron=A, epistemiek=Epistemiek.aanname))
