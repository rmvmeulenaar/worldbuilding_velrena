"""De regels van Velmara in drie delen: zin (Rogier), formule (machine), canoncode (bron). Rules as Code.

Elke regel geldt voor elk voorstel, van verteller, speler of simulatie. Context van het voorstel staat als feiten onder 'VOORSTEL':
  VOORSTEL handeling <code> | VOORSTEL seksueel <waar> | VOORSTEL jaar <n> | VOORSTEL plek <code> | VOORSTEL dwang_label <waar>
  <persoon> neemt_deel VOORSTEL | <persoon> instemming <waar> | <persoon> rol_in <rol>
"""
from .schema import Regel
from .regels import F, EN, OF, NIET, CMP

V = 'VOORSTEL'
DEELNEMER = F('?p', 'neemt_deel', V)
SEKS = F(V, 'seksueel', True)

REGELS: list[Regel] = [
    # ---- harde lijnen (gelden op elk warmteniveau, ook bij dwang-label) ----
    Regel(code='R-H1', categorie='hardelijn', harde_lijn=True, soort='verbod', canon_code='BESLUIT-Z30-4',
          zin='Wie aan een seksuele handeling deelneemt, is aantoonbaar 18 jaar of ouder. Onbekende leeftijd telt als niet aangetoond.',
          formule=EN(SEKS, DEELNEMER, NIET(EN(F('?p', 'leeftijd', '?n'), CMP('>=', '?n', 18))))),
    Regel(code='R-H2', categorie='hardelijn', harde_lijn=True, soort='verbod', canon_code='REGEL-harde-grenzen',
          zin='Geen dieren in een seksuele rol.',
          formule=EN(SEKS, DEELNEMER, F('?p', 'soort', 'dier'))),
    Regel(code='R-H3', categorie='hardelijn', harde_lijn=True, soort='verbod', canon_code='BESLUIT-Z30-4',
          zin='Seks zonder instemming bestaat alleen als gelabeld donker thema tussen volwassenen.',
          formule=EN(SEKS, DEELNEMER, F('?p', 'instemming', False), F(V, 'dwang_label', False))),
    Regel(code='R-H4', categorie='hardelijn', harde_lijn=True, soort='verbod', canon_code='BESLUIT-Z30-4',
          zin='Bij een seksuele handeling is de instemming van elke deelnemer vastgelegd (ja of nee), nooit open.',
          formule=EN(SEKS, DEELNEMER, NIET(OF(F('?p', 'instemming', True), F('?p', 'instemming', False))))),
    Regel(code='R-H5', categorie='hardelijn', harde_lijn=True, soort='verbod', canon_code='BESLUIT-Z38-9',
          zin='Een feeënafspraak gaat nooit over seks.',
          formule=EN(F(V, 'handeling', 'feeenafspraak'), SEKS)),
    # ---- tijd ----
    Regel(code='R-T1', categorie='tijd', soort='verbod', canon_code=None,
          zin='Een dode doet niet mee.',
          formule=EN(DEELNEMER, F('?p', 'sterft', '?s'), F(V, 'jaar', '?j'), CMP('>', '?j', '?s'))),
    Regel(code='R-T2', categorie='tijd', soort='verbod', canon_code=None,
          zin='Wie nog niet geboren is, doet niet mee.',
          formule=EN(DEELNEMER, F('?p', 'geboren', '?g'), F(V, 'jaar', '?j'), CMP('<', '?j', '?g'))),
    Regel(code='R-T3', categorie='tijd', soort='verbod', canon_code='FASE-OVERZICHT',
          zin='Iemand doet alleen mee binnen de tijd waarin hij leeft (afgeleid uit geboorte, canonjaar of fase), tenzij hij langlevend is of een bewuste uitzondering.',
          formule=EN(DEELNEMER, NIET(F('?p', 'langlevend', True)), F(V, 'jaar', '?j'),
                     OF(EN(F('?p', 'leeft_van', '?a'), CMP('<', '?j', '?a')), EN(F('?p', 'leeft_tot', '?z'), CMP('>', '?j', '?z'))))),
    # ---- handelingen ----
    Regel(code='R-A1', categorie='handeling', soort='verbod', canon_code='ORDE-stille-hand',
          zin='Je kunt iemand alleen aangeven of chanteren met een geheim dat je kent.',
          formule=EN(OF(F(V, 'handeling', 'aangeven'), F(V, 'handeling', 'chanteren')),
                     F('?a', 'rol_in', 'actor'), F('?d', 'rol_in', 'doel'),
                     NIET(EN(F('?g', 'geheim_van', '?d'), F('?a', 'weet', '?g'))))),
    # ---- ingebouwde controles (formuletaal kan dit nog niet; de zin is de afspraak, poort.py de uitvoering) ----
    Regel(code='R-R1', categorie='referentie', soort='verbod', ingebouwd='referentie',
          zin='Alles waarover een voorstel spreekt, bestaat in de wereld, of het voorstel brengt het zelf in met een soort.'),
    Regel(code='R-R2', categorie='referentie', soort='verbod', ingebouwd='predicaat',
          zin='Een voorstel gebruikt alleen bekende predicaten, met het juiste soort onderwerp en object.'),
    Regel(code='R-R3', categorie='handeling', soort='verbod', ingebouwd='handeling',
          zin='Een voorstel noemt een bestaande handeling, met de rollen die die handeling vraagt.'),
    Regel(code='R-K1', categorie='kern', soort='verbod', ingebouwd='kern', canon_code='BESLUIT-Z30-2',
          zin='Kern verandert niet, behalve door een besluit van Rogier.'),
    Regel(code='R-E1', categorie='kennis', soort='verbod', ingebouwd='kennis',
          zin='Niemand weet iets zonder bron: het is zijn eigen geheim, een deelnemer die het weet vertelt het, of hij ontdekt het bij degene van wie het is.'),
    Regel(code='R-P1', categorie='plaats', soort='verbod', ingebouwd='plaats',
          zin='Wie meedoet, is op die plek: zijn verblijfplaats in dat jaar ligt in dezelfde regio, of het voorstel laat hem reizen.'),
    Regel(code='R-L1', categorie='hoofdlijn', soort='verbod', ingebouwd='hoofdlijn', canon_code='BOOG-boek1',
          zin='De afloop van de hoofdlijn ligt vast: Liora, Teo, Aeron en Ithrael sterven of verdwijnen niet buiten de canon om.'),
    Regel(code='R-S1', categorie='hardelijn', harde_lijn=True, soort='verbod', ingebouwd='minderjarige_rol', canon_code='BESLUIT-Z30-4',
          zin='Een kind komt in een handeling alleen voor in een rol die bij kinderen hoort (geboorte, opvoeding, erfenis), nooit in een seksuele.'),
]
PER_CODE = {r.code: r for r in REGELS}
