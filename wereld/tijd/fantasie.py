# Ronde Z46: kan elke erotische fantasie, en elk genre, in elk tijdperk? (vraag van Rogier, 2 november 2026)
# Per fantasie (VOOR-, KINK-, RIT- in de canon) de afhankelijkheden uit de tekst (gave, binding, Ontvangst, stal, volk ...), daarna per tijdperk
# met tijd/uitkomst.json de status: 'echt' (het ding bestaat), 'zeldzaam', 'spel' (de macht of het instituut is weg, de fantasie kan als rollenspel
# tussen volwassenen), 'onmogelijk' (het lichaam of volk bestaat niet meer). Verleden = tijdperk van de oorsprongrij. Genres: aantal verhaalrijen
# per tijdperk per genre, en de lege cellen. Uitvoer: tijd/fantasie.md en tijd/fantasie.json. Leest alleen, schrijft niets in canon.db.
import json, os, re, sqlite3, collections
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(H)
c = sqlite3.connect(os.path.join(W, os.environ.get('DB', 'canon.db'))); U = json.load(open(os.path.join(H, 'uitkomst.json')))
L = "status in ('vastgesteld','voorlopig')"
FASEN = [9, 10, 11, 12, 13, 14, 15, 16]
E = U['tijdperk_eind_na_801']; A = U['anker_bp_801'][1]
MID = {9: E['ja'][1] / 2, 10: (E['ja'][1] + E['volken'][1]) / 2, 11: (E['volken'][1] + E['helden'][1]) / 2, 12: (E['helden'][1] + E['vertrek'][1]) / 2,
       13: A - 19500, 14: A - 13600, 15: A - 6700, 16: A - 2600}
# afhankelijkheid: (regex op de tekst, naam, soort). soort 'macht' -> kan als spel; 'lichaam' -> onmogelijk als het weg is
DEP = [
    (r'\bvonk|gave|gaven-m|zaadkracht|kracht \dx|ontla[ad]|vonkkoorts|Uitverkoren', 'gaven-mannen', 'macht'),
    (r'binding|gebonden|ontzegging|bloedverbind|bloedgave', 'bloedbinding', 'macht'),
    (r'Ontvangst|Ontvangster|zegellicht|tempel', 'ontvangst-feest', 'macht'),
    (r'melk|stalhuis|\bstal|dekk|veiling|Zaadbeurs|rotatie|wachtrij|Registratri|register|Deelwet|tiende|superkoe', 'stalsysteem', 'macht'),
    (r'Ves-Lethi|vormwissel|spiegelnacht', 'ves-lethi', 'lichaam'), (r'Skerra|valparing|vleugel', 'skerra', 'lichaam'),
    (r'Kluwer|korf', 'kluwers', 'lichaam'), (r'Oevrin|paai', 'oevrin', 'lichaam'), (r'Myrrhen|sporen|zwam', 'myrrhen', 'lichaam'),
    (r'Aelthir', 'aelthir', 'lichaam'), (r'Tharn', 'tharn', 'lichaam'), (r'Dhurn', 'dhurn', 'lichaam'), (r'Orrim', 'orrim', 'lichaam'),
    (r'Sael-mor', 'sael-mor', 'lichaam'), (r'Karrûk|Karruk', 'karruk-storm', 'macht'), (r'Vathren', 'vathren', 'lichaam'),
    (r'Lijngraver|ankerwortel', 'stalsysteem', 'macht'), (r'zegelglas|Sterrensteen', 'sterrensteen', 'macht'),
]
def aanwezig(naam, t):
    if naam == 'stalsysteem': return 1.0 if t <= 9 else 0.0          # stallen open na het Lichtconvent van 806 (BESLUIT-Z6-WRIJ-077)
    if naam in U.get('zeden', {}):
        f = next(f for f, m in MID.items() if abs(m - t) < 1e-6); return U['zeden'][naam][str(f)][1]
    w = U['wezens'].get(naam)
    if not w or w['zeldzaam'] is None: return 1.0
    if t < w['zeldzaam'][1]: return 0.75
    if t < w['legende'][1]: return 0.3
    if w['verdwenen'] and t < w['verdwenen'][1]: return 0.05
    return 0.0
FASE_NR = dict(c.execute('select label,fase from tijdperk_label').fetchall())
rij = c.execute(f"select code,categorie,onderwerp,feit,tijdperk from canon where {L} and (code like 'VOOR-%' or code like 'KINK-%' or code like 'RIT-%') and categorie in ('Voorkeuren','Kinks en situaties','Extreme rituelen','Rituelen')").fetchall()
uit = []; tel = {f: collections.Counter() for f in FASEN}
for code, cat, ond, feit, tp in rij:
    deps = {(n, s) for p, n, s in DEP if re.search(p, feit or '', re.I)}
    m = re.search(r'Oorsprong: ([A-Z][\w-]+)', feit or ''); verleden = None
    if m:
        o = c.execute('select tijdperk from canon where code=?', (m.group(1),)).fetchone(); verleden = FASE_NR.get(o[0]) if o and o[0] else None
    st = {}
    for f in FASEN:
        t = MID[f]; slechtst = 'echt'
        for n, s in deps:
            p = aanwezig(n, t)
            k = 'echt' if p >= 0.5 else ('zeldzaam' if p >= 0.1 else ('spel' if s == 'macht' else 'onmogelijk'))
            slechtst = max(slechtst, k, key=['echt', 'zeldzaam', 'spel', 'onmogelijk'].index)
        st[f] = slechtst; tel[f][slechtst] += 1
    toekomst = max([f for f in FASEN if st[f] == 'echt'], default=None)
    uit.append(dict(code=code, naam=ond, afh=sorted(n for n, _ in deps), verleden=verleden, laatst_echt=toekomst, status=st))
# genres per tijdperk (0-16): verhaalrijen in de canon en de ideeënbank
GEN = [('verhaal', r"^(Verhaal|Verhaalvoorstel)$", None), ('horror', r'^Horror$', r'Haak \(horror\)'), ('comedy', r'^Comedy$', r'Haak \(comedy\)|Haak \(humor\)'),
       ('romantiek', r'^Romantiek$', r'Haak \(romance\)'), ('oorlog', r'^Oorlog$', None), ('held', r'^Held$', None), ('actie', r'^Actie$', None),
       ('thriller', r'^$', r'Haak \(thriller\)|thriller'), ('intrige', r'^$', r'Haak \(intrige\)|^Intrige'), ('mythe', r'^Mythe$', None), ('erotiek', r'^(Kinks en situaties|Romantiek)$', r'erotisch|EROS')]
G = {f: collections.Counter() for f in range(17)}
for code, cat, feit, tp in c.execute(f"select code,categorie,feit,tijdperk from canon where {L} and tijdperk is not null"):
    f = FASE_NR.get(tp)
    if f is None: continue
    for g, cp, tx in GEN:
        if (cp != '^$' and re.match(cp, cat or '')) or (tx and re.search(tx, (feit or '')[:400], re.I)) or (g == 'thriller' and code.startswith('THRILL')) or (g == 'intrige' and code.startswith('INTR')):
            G[f][g] += 1
json.dump(dict(fantasieen=uit, telling={str(f): dict(v) for f, v in tel.items()}, genres={str(f): dict(v) for f, v in G.items()}), open(os.path.join(H, 'fantasie.json'), 'w'), ensure_ascii=False, indent=0)
naam = dict(c.execute('select fase,naam from tijdas').fetchall())
o = ['# Kan elke fantasie in elk tijdperk? (Z46)', '', f'{len(uit)} erotische fantasieën uit de canon (VOOR-, KINK-, RIT-). Status per tijdperk: echt (het bestaat nog), zeldzaam, spel (de macht of het instituut is weg; kan als rollenspel tussen volwassenen), onmogelijk (het lichaam of volk bestaat niet meer).', '',
     '| Tijdperk | Echt | Zeldzaam | Spel | Onmogelijk |', '|---|---|---|---|---|']
for f in FASEN: o.append(f"| {naam.get(f, '')} | {tel[f]['echt']} | {tel[f]['zeldzaam']} | {tel[f]['spel']} | {tel[f]['onmogelijk']} |")
o += ['', '## Genres per tijdperk (aantal rijen; 0 = lege cel om te verrijken)', '| Fase | ' + ' | '.join(g for g, _, _ in GEN) + ' |', '|' + '---|' * (len(GEN) + 1)]
for f in range(17): o.append(f'| {f} · {naam.get(f, "")} | ' + ' | '.join(str(G[f][g]) if G[f][g] else '**0**' for g, _, _ in GEN) + ' |')
o += ['', '## Per fantasie (verleden: tijdperk van de oorsprong; laatst echt: laatste tijdperk na 801 waarin het echt kan)', '| Code | Fantasie | Hangt af van | Verleden | Laatst echt | 9 | 10 | 11 | 12 | 13-16 |', '|---|---|---|---|---|---|---|---|---|---|']
kort = {'echt': 'E', 'zeldzaam': 'z', 'spel': 's', 'onmogelijk': '-'}
for x in sorted(uit, key=lambda x: (x['laatst_echt'] or 0, x['code'])):
    s = x['status']; o.append(f"| `{x['code']}` | {x['naam']} | {', '.join(x['afh']) or 'alleen mensen'} | {x['verleden'] if x['verleden'] is not None else '?'} | {x['laatst_echt'] or '-'} | " + ' | '.join(kort[s[f]] for f in (9, 10, 11, 12)) + f" | {kort[s[13]]}{kort[s[16]]} |")
open(os.path.join(H, 'fantasie.md'), 'w').write('\n'.join(o) + '\n'); print('\n'.join(o[:34]))
