"""Catalogus van handelingen: een vaste kern van werkwoorden plus alles wat de canon zelf als handeling kent
(rituelen, gebeurtenistypes van de simulatie). Voorwaarden en gevolgen zijn gegevens, geen code."""
from __future__ import annotations
import sqlite3
from .schema import Handeling

G = lambda **k: k
KERN = [
    Handeling(code='ontmoeten', naam='ontmoeten', rollen=('actor', 'doel'), genre=G(romance=1, intrige=1)),
    Handeling(code='vertellen', naam='een geheim vertellen', rollen=('actor', 'doel'), gevolgen=(('doel', 'weet', '$geheim'),), genre=G(intrige=3)),
    Handeling(code='ontdekken', naam='een geheim ontdekken', rollen=('actor', 'doel'), gevolgen=(('actor', 'weet', '$geheim'),), genre=G(spanning=3, intrige=3)),
    Handeling(code='aangeven', naam='aangeven bij de Orde', rollen=('actor', 'doel'), voorwaarden=('R-A1',), genre=G(spanning=3, tragiek=2), bron_code='ORDE-stille-hand'),
    Handeling(code='chanteren', naam='chanteren', rollen=('actor', 'doel'), voorwaarden=('R-A1',), gevolgen=(('doel', 'schuldig_aan', 'actor'),), genre=G(intrige=4, spanning=3)),
    Handeling(code='verleiden', naam='verleiden', rollen=('actor', 'doel'), seksueel=True, instemming_nodig=True, min_leeftijd=18, genre=G(erotiek=4, romance=2)),
    Handeling(code='samen_slapen', naam='met elkaar slapen', rollen=('actor', 'partner'), seksueel=True, instemming_nodig=True, min_leeftijd=18, genre=G(erotiek=5, romance=2)),
    Handeling(code='vervalsen', naam='een registerblad vervalsen', rollen=('actor', 'doel'), genre=G(intrige=4, spanning=2), bron_code='BEST-register'),
    Handeling(code='smokkelen', naam='smokkelen over de passen', rollen=('actor', 'doel'), genre=G(spanning=4, actie=2)),
    Handeling(code='reizen', naam='reizen', rollen=('actor',), gevolgen=(('actor', 'verblijft_in', '$plek'),), genre=G(verwondering=2)),
    Handeling(code='verraden', naam='verraden', rollen=('actor', 'doel'), gevolgen=(('doel', 'verraden_door', 'actor'),), genre=G(tragiek=4, intrige=3)),
    Handeling(code='schuld_aangaan', naam='in de schuld raken', rollen=('actor', 'doel'), gevolgen=(('actor', 'schuldig_aan', 'doel'),), genre=G(intrige=2)),
    Handeling(code='eed_zweren', naam='trouw zweren', rollen=('actor', 'doel'), gevolgen=(('actor', 'eed_aan', 'doel'),), genre=G(romance=1, intrige=2)),
    Handeling(code='rivaliseren', naam='rivaal worden', rollen=('actor', 'doel'), gevolgen=(('actor', 'rivaal_van', 'doel'),), genre=G(spanning=2)),
    Handeling(code='hetzelfde_willen', naam='hetzelfde willen', rollen=('actor', 'doel'), gevolgen=(('actor', 'wil_hetzelfde_als', 'doel'),), genre=G(intrige=2)),
    Handeling(code='verbinden', naam='zich verbinden', rollen=('actor', 'doel'), gevolgen=(('actor', 'verbonden_met', 'doel'),), genre=G(romance=2)),
    Handeling(code='trouwen', naam='zich binden als partners', rollen=('actor', 'partner'), gevolgen=(('actor', 'partner_van', 'partner'),), genre=G(romance=4)),
    Handeling(code='rouwen', naam='rouwen', rollen=('actor',), genre=G(tragiek=4, verwondering=2)),
    Handeling(code='werken', naam='het eigen ambacht doen', rollen=('actor',), genre=G(rust=4, verwondering=1)),
    Handeling(code='sterven', naam='sterven', rollen=('actor',), gevolgen=(('actor', 'sterft', '$jaar'),), genre=G(tragiek=5)),
    Handeling(code='doden', naam='doden', rollen=('actor', 'doel'), gevolgen=(('doel', 'sterft', '$jaar'),), genre=G(actie=4, horror=2, tragiek=3)),
    Handeling(code='feeenafspraak', naam='een feeënafspraak sluiten', rollen=('actor', 'doel'), genre=G(verwondering=5, spanning=2), bron_code='BESLUIT-Z38-9'),
]


def catalogus(db_pad: str) -> dict[str, Handeling]:
    """Kern + gebeurtenistypes van de simulatie + rituelen uit de canon."""
    H = {h.code: h for h in KERN}
    c = sqlite3.connect(db_pad)
    for code, oms, minl, minrol, inst, risico, bron in c.execute('select code,omschrijving,min_leeftijd,minderjarige_rol,instemming_nodig,harde_lijn_risico,bron_code from gebeurtenis_type'):
        if code in H: continue
        H[code] = Handeling(code=code, naam=oms or code, rollen=('actor', 'doel'), seksueel=bool(risico) and bool(inst),
                            instemming_nodig=bool(inst), min_leeftijd=int(minl or 0), bron_code=bron)
    for code, ond, cat in c.execute("select code,onderwerp,categorie from canon where status in ('vastgesteld','voorlopig') and ideeenbank=0 and (code like 'RIT-%' or code like 'HAND-%')"):
        seks = cat in ('Extreme rituelen', 'Rituele handelingen') or code.startswith('HAND-')
        H['ritueel:' + code] = Handeling(code='ritueel:' + code, naam=ond or code, rollen=('actor', 'doel'), seksueel=seks,
                                         instemming_nodig=seks, min_leeftijd=18 if seks else 0, bron_code=code, genre=G(erotiek=4 if seks else 0, verwondering=3))
    return H
