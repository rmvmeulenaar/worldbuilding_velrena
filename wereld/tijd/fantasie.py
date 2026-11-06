# Ronde Z46/Z47: kan elke erotische fantasie, en elk genre, in elk tijdperk? (vraag van Rogier, 2 november 2026)
# Z47: de fantasieën komen niet meer uit zoekwoorden maar uit de database: de afgeleide tabellen fantasie_kern en fantasie_status
# (afgeleid_motor.fantasie_tijd). Die lezen per fantasie de links naar LOT-Z44-rijen (waar ze echt van afhangt) en naar FASE-rijen (verleden).
# Genres: aantal verhaalrijen per tijdperk per genre, en de lege cellen. Uitvoer: tijd/fantasie.md en tijd/fantasie.json. Leest alleen.
import json, os, re, sqlite3, collections
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(H)
c = sqlite3.connect(os.path.join(W, os.environ.get('DB', 'canon.db')))
L = "status in ('vastgesteld','voorlopig')"
FASEN = [9, 10, 11, 12, 13, 14, 15, 16]
FASE_NR = dict(c.execute('select label,fase from tijdperk_label').fetchall())
st_ = collections.defaultdict(dict)
for code, f, k in c.execute('select code,fase,status from fantasie_status'): st_[code][f] = k
uit = []; tel = {f: collections.Counter() for f in FASEN}
for code, ond, afh, soort, vf, lf in c.execute('select code,naam,afh,soort,verleden_fase,verlies_fase from fantasie_kern order by code'):
    st = st_.get(code)
    if not st: uit.append(dict(code=code, naam=ond, afh=[], verleden=vf, laatst_echt=None, status=None)); continue
    for f in FASEN: tel[f][st[f]] += 1
    uit.append(dict(code=code, naam=ond, afh=[a.replace('LOT-Z44-', '').replace('GEB-Z45-losbandige-jaren', 'stalsysteem') for a in afh.split(';')],
                    verleden=vf, laatst_echt=max([f for f in FASEN if st[f] == 'echt'], default=None), status=st))
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
o += ['', '## Per fantasie', '', 'Kolommen: **hangt af van** = wat er echt moet bestaan (link naar de LOT-rij van dat wezen of instituut; *ishvar* = alleen gewone mensen). **Verleden** = vroegste fase waarin de fantasie kan bestaan. **Laatst echt** = het laatste tijdperk na 801 waarin ze nog echt kan; daarna is ze zeldzaam, een spel of onmogelijk. Codes per tijdperk: E echt, z zeldzaam, s spel, - onmogelijk.', '', '| Code | Fantasie | Hangt af van | Verleden | Laatst echt | 9 | 10 | 11 | 12 | 13-16 |', '|---|---|---|---|---|---|---|---|---|---|']
kort = {'echt': 'E', 'zeldzaam': 'z', 'spel': 's', 'onmogelijk': '-'}
for x in sorted(uit, key=lambda x: (x['laatst_echt'] or 0, x['code'])):
    s = x['status']
    if s is None: o.append(f"| `{x['code']}` | {x['naam']} | nog niet ingedeeld | {x['verleden'] if x['verleden'] is not None else '?'} | ? | ? | ? | ? | ? | ? |"); continue
    o.append(f"| `{x['code']}` | {x['naam']} | {', '.join(x['afh']) or 'alleen mensen'} | {x['verleden'] if x['verleden'] is not None else '?'} | {x['laatst_echt'] or '-'} | " + ' | '.join(kort[s[f]] for f in (9, 10, 11, 12)) + f" | {kort[s[13]]}{kort[s[16]]} |")
open(os.path.join(H, 'fantasie.md'), 'w').write('\n'.join(o) + '\n'); print('\n'.join(o[:34]))
