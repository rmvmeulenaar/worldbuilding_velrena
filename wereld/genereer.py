#!/usr/bin/env python3
"""Genereert bijbel/ uit canon.db (bron van waarheid). Idempotent: map wordt elke keer volledig herschreven."""
import sqlite3,os,re,shutil
D=os.path.dirname(os.path.abspath(__file__));B=os.path.join(D,'bijbel')
c=sqlite3.connect(os.path.join(D,'canon.db'))
DOM=[('02_land-en-regios.md','Land en regio’s','Kaart, regio’s, steden, sfeer en uiterlijk.',['Land','Regio','Sfeer en uiterlijk','Planten en dieren']),
('03_economie.md','Economie','Geld, handel, prijzen van mannen en zaad, werk.',['Economie']),
('04_macht-en-huizen.md','Macht en huizen','Mannen als macht en bezit, huizen, leger, wetten.',['Macht','Wetten','Maatschappij','Bestuur']),
('05_geloof-en-orde.md','Geloof en orde','Demografie, het geloof, de orde, registers en taboes.',['Demografie','Religie','Afstamming','Genre']),
('06_magie-en-zaadkracht.md','Magie en zaadkracht','Regels van de gave, kracht en duur van zaad, verslaving.',['Magie']),
('07_rituelen.md','Rituelen','Alle rituelen met kink-schaal, handelingen en systeemfunctie; ook situaties en oude riten.',['Rituelen','Extreme rituelen','Riten','Kinks en situaties']),
('08_cultuur-en-mode.md','Cultuur en mode','Gezin, opvoeding, taal, eten, gezondheid, kleding.',['Cultuur','Gezondheid','Mode en kleding']),
('09_personages.md','Personages','Hoofdpersonen, bondgenoten, tegenstanders, gewone mannen.',['Personage']),
('10_geschiedenis-en-tijdlijn.md','Geschiedenis en tijdlijn','Officiële oorsprong, herkomst van de gave, tijdlijn.',['Tijdperk','Geschiedenis','Oorsprong']),
('11_geheimen.md','Geheimen','Wat het volk, de orde en niemand weet.',['Geheimen']),
('12_queeste.md','Queeste','Doel, reden, gevaar en etappes.',['Verhaal']),
('13_voorkeuren.md','Voorkeuren','Seksuele voorkeuren en kinks met intensiteit, oorsprong en koppelingen.',['Voorkeuren']),
('14_lichaam-en-vervorming.md','Lichaam en vervorming','Body horror: het lichaam als prijs voor macht.',['Lichaam en vervorming']),
('15_volken.md','Volken','Andere sprekende, volwassen volken: oorsprong, voortplanting, cultuur en functie.',['Volken']),
('16_volken-uiterlijk-en-seks.md','Volken: uiterlijk en seksuele cultuur','Per volk: uiterlijk, lichamelijke seks en voortplanting, opwinding, voorkeuren, rituelen, taboes en contact met mensen. Alleen volwassen, sprekende, instemmende wezens.',['Volken uiterlijk','Volken seksualiteit'])]
COLS='id,categorie,onderwerp,feit,status,reden,verwijst_naar,code,ronde,jaar,tijdperk,intensiteit,weet,functie,afstoting,aantrekking_bron,aantrekking,techniek,draagkracht,ideeenbank,feit_schoon'
rows=[dict(zip(COLS.split(','),r)) for r in c.execute(f'select {COLS} from canon order by id')]
by={r['code']:r for r in rows}
def ent(r,extra=''):
  v=r['verwijst_naar'] or '-'
  x=''.join(f"- **{k.capitalize()}:** {r[k]}\n" for k in ('jaar','tijdperk','intensiteit','weet','functie','afstoting','aantrekking_bron','aantrekking','techniek') if r.get(k) is not None)
  return f"### {r['code']} · {r['onderwerp']}\n- **Draagkracht:** {r.get('draagkracht') or '-'}{' · ideeënbank' if r.get('ideeenbank') else ''}\n- **Wat:** {r.get('feit_schoon') or r['feit']}\n- **Waarom:** {r['reden']}\n{x}{extra}- **Status:** {r['status']} (ronde {r['ronde']})\n- **Verwijst naar:** {v}\n"
def plaats(r):
  if r['code']=='GEH-zegel': return '11_geheimen.md'
  if r['categorie'] in('Rituele handelingen','Ritueel systeem'): return '07_rituelen.md'
  for f,_,_,cats in DOM:
    if r['categorie'] in cats: return f
  return None
# kink-niveaus
ks=by.get('RIT-kinkschaal',{}).get('feit','')
lvl={}
for m in re.finditer(r'(\d) [^:]*: ([^.]*)\.',ks):
  for n in m.group(2).split(','): lvl[n.strip().lower()]=m.group(1)
def niveau(o):
  m=re.search(r'Kink-schaal: (\d)',by_on.get(o,{}).get('feit',''))
  if m: return m.group(1)
  k=re.sub(r'^(de|het) ','',o.lower()).replace(' (18+)','')
  for n,v in lvl.items():
    if re.sub(r'^(de|het) ','',n)==k or k.startswith(n) or n.startswith(k): return v
  return '?'
by_on={r['onderwerp']:r for r in rows if r['categorie'] in('Rituelen','Extreme rituelen')}
def sub(cat,o): 
  for r in rows:
    if r['categorie']==cat and r['onderwerp']==o: return r
def blok(r):
  if r['categorie'] in('Rituelen','Extreme rituelen') and r['code']!='RIT-kinkschaal':
    e=f"- **Kink-schaal:** {niveau(r['onderwerp'])}\n"
    h=sub('Rituele handelingen',r['onderwerp']); s=sub('Ritueel systeem',r['onderwerp'])
    if h: e+=f"- **Handelingen ({h['code']}):** {h['feit']}\n"
    if s: e+=f"- **Systeem ({s['code']}):** {s['feit']}\n"
    return ent(r,e)
  return ent(r)
def render(code):
  r=by[code]
  if r['categorie'] in('Rituele handelingen','Ritueel systeem'):
    p=sub('Rituelen',r['onderwerp']) or sub('Extreme rituelen',r['onderwerp'])
    if p: return blok(p)
  return blok(r)
if os.path.isdir(B): shutil.rmtree(B)
os.makedirs(B)
def w(n,t): open(os.path.join(B,n),'w').write(t.strip()+'\n')
vs=sum(r['status']=='vastgesteld' for r in rows)
KERN=f"""# 00 · WERELDKERN Velmara
Erotische dark fantasy voor volwassenen (alle seksuele deelnemers 18+; dwang alleen als donker thema tussen volwassenen; geen dieren). Toon: zinnelijk, geladen, rauw, met echte inzet. Doel: een wereld die steeds nieuwe geile, spannende situaties oplevert.

**Grondregels (alles volgt hieruit)**
1. 1 op 100 geboorten is een jongen; rond Ves-Anath 1 op 60 (verzwegen lek), in Kharvos 1 op 3 (REGEL-verhouding-Z12).
2. Elke man verwekt 300-500 kinderen; ±4 per vrouw (REGEL-nageslacht-per-man).
3. Dubbel bestuur: de Orde beheert zaad en register, de geregistreerde huizen land en geld; het geloof is opgelegd door de machthebbers; religie is gereedschap (REGEL-regeringsvorm-Z12).
4. Macht komt uit wat je kunt afdwingen of onmisbaar maakt (MACHT-twee-soorten-mannen).
5. Losbandigheid is deugd; verlangen en overgave zijn gebed (REGEL-seksuele-normen).
6. Gaven-mannen: magisch, kiezen zelf, lief of duister; het geloof draait om hen (MACHT-gaven-mannen).
7. Gewone mannen: bezit, gemolken voor zaad (MACHT-gewone-mannen).
8. Zaad geeft tijdelijk kracht: gewoon +20%/1-3 u; gaven 5x/8-12 u, max 24 u; daarna de Leegte (MAGIE-kracht-duur).
9. Vaker dan 3x per maand gaven-zaad = binding/verslaving (MAGIE-verslaving).
10. Gave kost kracht; na grote magie moet hij ontladen (MAGIE-wat-gaven-man).
11. De Orde beheert registers, toegang en gunstbrieven (ORDE-orde).
12. Verwantschap is het enige absolute taboe; bloedlijnmerken en registers bewaken het (REGEL-verwantschapstaboe).
13. Harde grens: niemand onder de 18 in een seksuele rol, ook niet historisch; geen dieren (REGEL-harde-grenzen). Weigeren mag, maar kost rang; heilig woord stopt een rite (WET-wie-weigert).
14. Vrouwen doen al het werk en vormen het leger (REGEL-overwegend-vrouwelijke-wereld).
15. Geheim: het Zegel is door de Makers gebouwd en door de priesteressen van Ves-Anath gekaapt; het doodt zonen, wordt met tempelzaad gevoed, verzwakt nu en is de bron van de gave (GEH-zegel-Z12).
16. Rituelen zijn een systeem: macht, hechting, loyaliteit, liefde; publiek verhaal ≠ verborgen functie (07_rituelen.md).
17. Geschiedenis: -600 tot 801, jaar 0 = de Zegel; 7 fasen als systeem (FASE-...; oude TIJD-rijen zijn vervallen), gebeurtenissen GEB-...; voorkeuren VOOR-... met intensiteit 1-5; body horror LICH-...: het lichaam betaalt voor macht.
18. Queeste: Liora brengt Teo naar Ves-Anath (QST-doel-reden-gevaar).

**Status:** {vs} rijen vastgesteld (volgen uit Rogiers keuzes), {len(rows)-vs} voorlopig (moeten nog worden goedgekeurd).
**Verder lezen:** 01_INDEX.md → domeinbestand → 90_WRIJVINGEN.md. Voor één scène: `python3 scene.py <codes>`.
"""
w('00_WERELDKERN.md',KERN)
idx='# 01 · INDEX\n\n'+''.join(f'- **{f}** · {t}: {z}\n' for f,t,z,_ in DOM)+"""- **17_techniek-overzicht.md** t/m **20_mensen-en-plekken.md** · techniek, crosslinks, zintuigen, mensen en plekken.
- **21_erotiek.md** · erotische laag, stopwoorden, rauwe laag (Z6-Z7).
- **22_kinks-en-lichaam.md** · lichaamsvorming, verleiding, kinks (Z8).
- **23_actie-oorlog-horror.md** · actie, oorlog, horror (Z9).
- **24_kink-functies-saw-comedy.md** · kinkfuncties en kinknetwerk, Saw-horror, comedy, romantiek, helden, underdogs, degeneratie, ontwaking, genre-overzichten per fase/volk/regio en de GENRE-KAART-Z10 (Z10).
- **25_tijdlijn-personages.md** · tijdlijn per personage (TOESTAND-Z11), plek- en voorwerptoestand, verhalenvolgorde, verhaal-aanpassingen, nieuwe punten uit de verhalen en de coherentiebesluiten (Z11).
- **26_besluiten.md** · de 15 besluiten van Rogier (BESLUIT-Z12-*), schema dubbel bestuur, stem in de Wortel, nieuwe regels, verhaal-aanpassingen en wrijvingen van ronde Z12.
- **28_restpunten.md** · ronde Z14: restpunten Z13 opgelost (dood-maar-actief, twee plekken, verhoudingen, jaren na 801), 420 haken per rij herschreven, aangenomen jaren nagelopen (KWALITEIT-Z14, WRIJ-Z14-*).
- **29_ysa-thalen.md** · ronde Z15: Ysa's verloren liefde (beatplan 03): besluiten van Rogier (BESLUIT-Z15-*), nieuwe voorstellen (YSA-Z15-*), 22 beats, Thalens tijdlijn, haken naar andere boeken (HAAK-Z15-*), wrijvingen (WRIJ-Z15-*).
- **30_roman-ysa.md** · ronde Z16: Wattpad-roman "The Body Is the Price" (Ysa en Thalen): besluiten (BESLUIT-Z16-*), roman en novelle, 33 hoofdstukken (ROMAN-Z16-h*), nieuwe voorstellen (YSA-Z16-*), tijdlijn, wrijvingen (WRIJ-Z16-*); ronde Z17: BESLUIT-Z17-*, YSA-Z17-*, WRIJ-Z17-*; ronde Z18: BESLUIT-Z18-*, YSA-Z18-*, WRIJ-Z18-*; ronde Z18b/Z19: BESLUIT-Z18b-*, BESLUIT-Z19-*, YSA-Z19-*, WRIJ-Z19-*; ronde Z20: BESLUIT-Z20-*, YSA-Z20-*, WRIJ-Z20-*; ronde Z21: BESLUIT-Z21-*, YSA-Z21-*, MOTOREN-Z21, WRIJ-Z21-*; ronde Z22: BESLUIT-Z22-* (motorregel), YSA-Z22-*, MOTOREN-Z22, WRIJ-Z22-*; ronde Z23: BESLUIT-Z23-* (eindfeedback), WRIJ-Z23-*; ronde Z24: BESLUIT-Z24-* (eindrapport), WRIJ-Z24-*; ronde Z25: BESLUIT-Z25-* (laatste feedback), WRIJ-Z25-*; ronde Z26: BESLUIT-Z26-* (telling 3.454), WRIJ-Z26-*; ronde Z27: BESLUIT-Z27-* (kraaien, inheemse planeet, tijdlijn), WRIJ-Z27-*; ronde Z28: YSA-Z28-* (alle romandetails per hoofdstuk), WRIJ-Z28-*; ronde Z29: YSA-Z29-* (sfeerdetails per hoofdstuk), WRIJ-Z29-*; ronde Z30: BESLUIT-Z30-* (architectuur, draagkracht, Zegel jaar 0), WRIJ-Z30-*. Zie ook 00_HANDLEIDING.md en 40_ideeenbank.md.
- **27_kwaliteit.md** · kwaliteitsronde Z13: wortelstem vastgesteld, dubbele namen samengevoegd, datering, gerepareerde verwijzingen, statusronde, verdiepte rijen, coherentiecontrole (WRIJ-Z13-*) en kwaliteitsrapport (KWALITEIT-Z13).
- **90_WRIJVINGEN.md** · tegenstrijdigheden en verhaalbronnen.
- **91_OPEN_VRAGEN.md** · keuzes voor Rogier.
- **99_LOGBOEK.md** · wat per ronde veranderde.

## Conventies
- Codes: `PREFIX-slug` (FASE tijdperk, TIJD vervallen tijdperk, LICH lichaam, GEB gebeurtenis, VOOR voorkeur, REG regio, ECO, MACHT, HUI huis, WET, REGEL grondregel, ORDE, MAGIE, GES geschiedenis, GEH geheim, CUL, MODE, SFEER, RIT ritueel, HAND handelingen, SYS ritueel-systeem, RITE oude rite, KINK situatie, PER, QST queeste, WRIJ-nnn, VRAAG-nnn). Codes zijn stabiel; nooit hergebruiken.
- Status: `vastgesteld` = volgt uit Rogiers keuzes; `voorlopig` = voorstel; `vervallen` = vervangen, niet gebruiken.
- Uitbreiden: INSERT in canon.db met code en verwijst_naar, daarna `python3 genereer.py`. HAND- en SYS-rijen staan in 07 onder hun RIT-ritueel.
"""
w('01_INDEX.md',idx)
for f,t,z,cats in DOM:
  out=[f'# {t}\n\n{z}\n']
  for r in rows:
    if plaats(r)==f and r['categorie'] not in('Rituele handelingen','Ritueel systeem'): out.append(blok(r))
  if f=='07_rituelen.md':
    for r in rows:
      if r['categorie']=='Ritueel systeem' and r['onderwerp'] not in by_on: out.append(blok(r))
  w(f,'\n'.join(out))
wr=c.execute('select code,titel,type,status,delen_die_botsen,beschrijving,verwijst_naar from wrijving order by id').fetchall()
# 17 techniek-overzicht
import re as _re
def _volk(r):
  m=_re.search(r'Volk: ([\w\-û]+)',r['feit'] or '') or _re.search(r'VOLK-([\w\-û]+)',r['verwijst_naar'] or '') or _re.search(r'V4-([a-zû\-]+)-\d',r['code'] or '')
  return m.group(1) if m else '-'
def _klasse(r):
  m=_re.search(r'(?:KLASSE-|V4-|DAG-)(top|mid|laag|sub|rebel|TOP|MID|LAAG|SUB)',(r['code'] or '')+' '+(r['verwijst_naar'] or ''))
  return m.group(1).lower() if m else '-'
act=[r for r in rows if r['status']=='voorlopig' or r['status']=='vastgesteld']
T=['gave','metaal','bio','zegelsteen']
o=['# 17 · Techniek-overzicht\n\nPer technologie waar ze in de wereld zit (alleen actieve rijen). Mengvormen tellen bij beide. Kolom `techniek` in canon.db.\n']
for t in T:
  rs=[r for r in act if t in (r.get('techniek') or '').split('+')]
  o.append(f'\n## {t} ({len(rs)} rijen)\n')
  for lab,fn in (('Categorie',lambda r:r['categorie']),('Volk',_volk),('Klasse',_klasse),('Fase',lambda r:r['tijdperk'] or '-')):
    d={}
    for r in rs: d[fn(r)]=d.get(fn(r),0)+1
    o.append(f'- **{lab}:** '+', '.join(f'{k} {v}' for k,v in sorted(d.items(),key=lambda x:-x[1]))+'\n')
  o.append('- **Codes:** '+', '.join(r['code'] for r in rs)+'\n')
o.append('\n## Gaten\n')
volken=sorted({_re.sub(r'-V\d+$','',r['code'][5:]) for r in act if r['categorie']=='Volken'})
for t in T:
  heeft={_volk(r) for r in act if t in (r.get('techniek') or '')}
  o.append(f'- **{t}** ontbreekt bij volken: '+(', '.join(v for v in volken if v not in heeft) or 'geen')+'\n')
  fs={r['tijdperk'] for r in act if t in (r.get('techniek') or '') and r['tijdperk']}
  alle={r['tijdperk'] for r in act if r['tijdperk']}
  o.append(f'  - ontbreekt in fasen: '+(', '.join(sorted(alle-fs)) or 'geen')+'\n')
cats={}
for r in act:
  cats.setdefault(r['categorie'],[0,0]); cats[r['categorie']][0]+=1; cats[r['categorie']][1]+=(r.get('techniek') not in (None,'geen'))
o.append('- **Categorieën zonder technologie:** '+', '.join(k for k,(a,b) in cats.items() if b==0)+'\n')
w('17_techniek-overzicht.md',''.join(o))
import crosslinks_lib
w('18_crosslinks.md',crosslinks_lib.rapport(c))
_zr=c.execute("select code,onderwerp,feit,verwijst_naar,techniek from canon where categorie='Zintuigen' or code like 'ZINT-%' or code like '%-Z1-%' or code like '%-Z2-%' or code like '%-Z3-%' order by id").fetchall()
_zo=['# 19 · Zintuigen\n\nZintuiglijke verdieping (rondes Z1 en Z2): voorbeelden, motieven per volk en regio, regiorijen en de dekkingsmeting. Alleen uit canon.db.\n']
for _t,_f in (('Dekking',lambda r:r[0] in ('ZINT-DEKKING-Z4','ZINT-DEKKING-Z3','ZINT-DEKKING-Z2','ZINT-DEKKING')),('Voorbeelden',lambda r:r[0].startswith('ZINT-VOORBEELD')),('Motieven',lambda r:r[0].startswith('ZINT-MOTIEF')),('Regiorijen',lambda r:('-Z1-' in r[0] or ('-Z2-' in r[0] and not r[0].startswith('ZINT-'))) and not r[0].startswith('HAAK')),('Verdieping per categorie (Z2)',lambda r:r[0].startswith('ZINT-Z2-')),('Z3: bijgeschreven, gevuld en regio\'s',lambda r:r[0].startswith('ZINT-Z3-')),('Z4: bijgeschreven',lambda r:r[0].startswith('ZINT-Z4-'))):
  _zo.append(f'\n## {_t}\n')
  for r in _zr:
    if _f(r): _zo.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Techniek:** {r[4] or "geen"} · **Verwijst naar:** {r[3] or "-"}\n')
w('19_zintuigen.md',''.join(_zo))

_mo=['# 20 · Mensen en plekken\n\nRonde Z4: besluiten van Rogier, belangrijke mensen per volk en fase, hoofdpersonen, mega-verhalen van niet-menselijke volken, sleutelplekken en de boek-1-route. Alleen uit canon.db.\n']
for _t,_p in (('Besluiten Z4','BESLUIT-Z4-'),('Hoofdpersonen per volk','HOOFDPERS-Z4-'),('Volksgeschiedenis als keten van mensen','VOLK-GESCHIEDENIS-OVERZICHT-Z4-'),('Belangrijke mensen per volk en fase','PERS-Z4-'),('Mega-verhalen niet-menselijke volken','MEGA-Z4-'),('Sleutelplekken','PLEK-Z4-'),('Route en lijst per boek','ROUTE-Z4-'),('','LIJST-Z4-'),('Besluiten Z5 (Rogier akkoord)','BESLUIT-Z5-'),('Ter goedkeuring Z5','LIJST-Z5-')):
  if _t: _mo.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_p+'%',)):
    _mo.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Verwijst naar:** {r[3] or "-"}\n')
w('20_mensen-en-plekken.md',''.join(_mo))

_eo=['# 21 · Erotiek\n\nRondes Z6-Z7: erotische laag (alleen volwassenen 18+; dwang alleen als gelabeld donker thema). Alleen uit canon.db.\n']
for _t,_p in (('Grenzen','EROS-GRENZEN-Z7'),('Stopwoorden per volk','EROS-STOP-Z7-'),('Rauw en donker (Z7)','EROS-RAUW-Z7-'),('Per volk','EROS-Z6-VOLK-'),('Per regio','EROS-Z6-REG-'),('Geilheid','EROS-GEIL-Z6-'),('Scenesjablonen','EROS-SCENE-Z6-'),('Taal en geluid van lust','EROS-TAAL-Z6-'),('Besluiten Z6','BESLUIT-Z6-'),('Besluiten Z7 (verhaal 1)','BESLUIT-Z7-'),('Nieuw uit verhaal 1','PER-Z7-'),('Voorwerpen uit verhaal 1','VOORW-Z7-')):
  _eo.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_p+'%',)):
    _eo.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Verwijst naar:** {r[3] or "-"}\n')
w('21_erotiek.md',''.join(_eo))

_kl=['# 22 · Kinks en lichaam\n\nRonde Z8: lichaamsvorming/bimbofication, verleiding, expliciete kinks (alleen volwassenen 18+; dwang alleen als gelabeld donker thema). Alleen uit canon.db.\n']
for _t,_p in (('Lichaamsvorming en bimbofication','BODY-Z8-'),('Verleiding','VERLEID-Z8-'),('Verleidingsskeletten','VERLEID-SKELET-Z8-'),('Expliciete kinks','KINK-Z8-')):
  _kl.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_p+'%',)):
    _kl.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Verwijst naar:** {r[3] or "-"}\n')
w('22_kinks-en-lichaam.md',''.join(_kl))

_ao=['# 23 · Actie, oorlog en horror\n\nRonde Z9: actie, oorlog en agressie, horror (geweld mag hard; alleen volwassenen in seksuele rollen). Alleen uit canon.db.\n']
for _t,_p in (('Actie','ACTIE-Z9-'),('Oorlog en agressie','OORLOG-Z9-'),('Horror','HORROR-Z9-'),('Horrorverhaalskeletten','HORROR-SKELET-Z9-')):
  _ao.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_p+'%',)):
    _ao.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Verwijst naar:** {r[3] or "-"}\n')
w('23_actie-oorlog-horror.md',''.join(_ao))

_z10=['# 24 · Kinkfuncties, Saw, comedy, romantiek, helden en nieuwe lagen\n\nRonde Z10: elke kink heeft een functie in de wereld; Saw-achtige horror, comedy, zoetsappige romantiek, heldenverhalen, vereerde underdogs, morele degeneratie en seksuele ontwaking (alleen volwassenen 18+). Integratie: genre-overzicht per fase, volk en regio, en de genrekaart. Alleen uit canon.db.\n']
for _t,_p in (('Genrekaart','GENRE-KAART-Z10'),('Kinknetwerk','KINK-NETWERK-Z10'),('Genres per fase (tijdlijn)','FASE-OVERZICHT-Z10-'),('Genres per volk','VOLK-GENRES-Z10-'),('Genres per regio','REGIO-GENRES-Z10-'),('Kinkfuncties','KINKFUNC-Z10-'),('Saw-achtige horror','SAW-Z10-'),('Saw-skeletten','SAW-SKELET-Z10-'),('Comedy','COMEDY-Z10-'),('Comedyskeletten','COMEDY-SKELET-Z10-'),('Romantiek','ROMANCE-Z10-'),('Romantiekskeletten','ROMANCE-SKELET-Z10-'),('Helden','HELD-Z10-'),('Heldenskeletten','HELD-SKELET-Z10-'),('Vereerde underdogs','NERD-Z10-'),('Underdogskeletten','NERD-SKELET-Z10-'),('Morele degeneratie','DEGEN-Z10-'),('Degeneratieskeletten','DEGEN-SKELET-Z10-'),('Seksuele ontwaking (volwassenen)','ONTWAAK-Z10-'),('Ontwakingsskeletten','ONTWAAK-SKELET-Z10-'),('Bijgeschreven rijen (optimalisatie)','%-L10'),('Kwaliteitsrapport','ZINT-DEKKING-Z10')):
  _z10.append(f'\n## {_t}\n')
  _q=_p if '%' in _p else _p+'%'
  for r in c.execute("select code,onderwerp,feit,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_q,)):
    _z10.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Verwijst naar:** {r[3] or "-"}\n')
w('24_kink-functies-saw-comedy.md',''.join(_z10))
for _f,_z in (('02_land-en-regios.md','REGIO-GENRES-Z10-*'),('07_rituelen.md','KINKFUNC-Z10-* en KINK-NETWERK-Z10'),('09_personages.md','HELD-Z10-*, NERD-Z10-*, DEGEN-Z10-*'),('10_geschiedenis-en-tijdlijn.md','FASE-OVERZICHT-Z10-0..7'),('15_volken.md','VOLK-GENRES-Z10-*'),('16_volken-uiterlijk-en-seks.md','ONTWAAK-Z10-*'),('22_kinks-en-lichaam.md','KINKFUNC-Z10-* (functie per kink)'),('23_actie-oorlog-horror.md','FASE-OVERZICHT-Z10-*, SAW-Z10-*')):
  open(os.path.join(B,_f),'a').write(f'\n\n---\n**Zie ook (Z10):** 24_kink-functies-saw-comedy.md · {_z} · GENRE-KAART-Z10.\n')

_z11=['# 25 · Tijdlijn per personage, plektoestand en verhalenvolgorde\n\nRonde Z11: per personage oorsprong, knooppunt en stand (TOESTAND-Z11-*), plekken en voorwerpen die veranderen (PLEKTOESTAND-Z11-*), de volgorde van alle verhalen (VERHAALTIJD-Z11-*), wat later in een verhaal moet worden aangepast (VERHAAL-AANPASSING-Z11-*), nieuwe punten uit verhaal 1 en 2, en de besluiten (BESLUIT-Z11-tijdlijn, WRIJ-Z11-*). Alleen volwassenen (18+) in seksuele rollen. Alleen uit canon.db.\n']
for _t,_p in (('Verhalenvolgorde','VERHAALTIJD-Z11-'),('Verhaal-aanpassingen (nog uit te voeren)','VERHAAL-AANPASSING-Z11-'),('Besluiten','BESLUIT-Z11-'),('Nieuwe personages','PER-Z11-'),('Nieuwe wetten, voorwerpen, plekken','%-Z11-%'),('Plek- en voorwerptoestand','PLEKTOESTAND-Z11-'),('Tijdlijnen verhaalpersonages','TOESTAND-Z11-%-_'),('Tijdlijnen alle personages','TOESTAND-Z11-P')):
  _z11.append(f'\n## {_t}\n')
  _q=_p if '%' in _p else _p+'%'
  _ex=" and code not like 'TOESTAND%' and code not like 'PLEKTOESTAND%' and code not like 'VERHAAL%' and code not like 'PER-Z11%' and code not like 'BESLUIT-Z11%'" if _t.startswith('Nieuwe wetten') else (" and code not like 'TOESTAND-Z11-P%'" if _t.startswith('Tijdlijnen verhaal') else '')
  for r in c.execute("select code,onderwerp,feit,verwijst_naar,jaar from canon where code like ? and status not like '%vervangen%'"+_ex+" order by id",(_q,)):
    _z11.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Jaar:** {r[4] if r[4] is not None else "-"} · **Verwijst naar:** {r[3] or "-"}\n')
w('25_tijdlijn-personages.md',''.join(_z11))
for _f in ('09_personages.md','10_geschiedenis-en-tijdlijn.md'):
  open(os.path.join(B,_f),'a').write('\n\n---\n**Zie ook (Z11):** 25_tijdlijn-personages.md · TOESTAND-Z11-* · VERHAALTIJD-Z11-* · BESLUIT-Z11-tijdlijn.\n')

_z12=['# 26 · Besluiten van Rogier (ronde Z12)\n\nDe 15 beslissingen van 31-10-2026 (1B 2A 3B 4C 5B 6B 7C 8B 9B 10B 11B 12C 13B 14A 15C), met reden en gevolgen, het schema van het dubbel bestuur, de vervangen regels, de stem in de Wortel (ter beoordeling), wat er in de verhalen later moet veranderen en de wrijvingen. Alleen volwassenen (18+) in seksuele rollen; het Jongenshof is volledig niet-seksueel. Alleen uit canon.db.\n']
for _t,_q in (('Besluiten','BESLUIT-Z12-%'),('Nieuwe regels','%-Z12'),('Verhaal-aanpassingen (nog uit te voeren)','VERHAAL-AANPASSING-Z12-%')):
  _z12.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar from canon where code like ? and status not like '%vervangen%' order by id",(_q,)):
    _z12.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Verwijst naar:** {r[4] or "-"}\n')
_z12.append('\n## Wrijvingen Z12\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z12-%' order by id"):
  _z12.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
w('26_besluiten.md',''.join(_z12))
for _f in ('04_macht-en-huizen.md','11_geheimen.md','12_queeste.md'):
  open(os.path.join(B,_f),'a').write('\n\n---\n**Zie ook (Z12):** 26_besluiten.md · BESLUIT-Z12-* · REGEL-regeringsvorm-Z12 · GEH-zegel-Z12 · BESLUIT-Z12-wortelstem.\n')

_z13=['# 27 · Kwaliteit en coherentie (ronde Z13)\n\nRonde Z13 ("de database perfectioneren"): stem in de Wortel vastgesteld (Ysara, Thalen Orr erin opgegaan), dubbele namen samengevoegd met verwijzing, skeletten en volkrijen gedateerd, kapotte verwijzingen gerepareerd, statusronde langs alle voorlopige rijen, dunne rijen verdiept, coherentiecontrole en kwaliteitsrapport. Alleen volwassenen (18+) in seksuele rollen. Alleen uit canon.db.\n']
for _t,_q in (('Besluiten en rapport','BESLUIT-Z13-%'),('','KWALITEIT-Z13'),('Stem in de Wortel','BESLUIT-Z12-wortelstem')):
  if _t: _z13.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar from canon where code like ? order by id",(_q,)):
    _z13.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Verwijst naar:** {r[4] or "-"}\n')
_z13.append('\n## Statusverdeling\n\n'+''.join(f'- {a}: {b}\n' for a,b in c.execute('select status,count(*) from canon group by status')))
_z13.append('\n## Vastgesteld in Z13 per categorie\n\n'+''.join(f'- {a}: {b}\n' for a,b in c.execute("select categorie,count(*) from canon where reden like '%: vastgesteld; volgt uit/past bij de besluiten%' group by 1 order by 2 desc")))
_z13.append('\n## Wrijvingen Z13\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z13-%' order by id"):
  _z13.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
w('27_kwaliteit.md',''.join(_z13))
_z14=['# 28 · Restpunten Z13 opgelost (ronde Z14)\n\nRonde Z14: dood-maar-actief per geval beslist, twee-plekken opgelost als reis, afwijkende verhoudingen nagelopen, jaren na 801 beslist (plan, deadline of toekomstskelet), 420 haken met de hand per rij herschreven, aangenomen jaren nagelopen. Alleen volwassenen (18+) in seksuele rollen. Alleen uit canon.db.\n']
for _t,_q in (('Besluit en rapport','BESLUIT-Z14-%'),('','KWALITEIT-Z14')):
  if _t: _z14.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar from canon where code like ? order by id",(_q,)):
    _z14.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Verwijst naar:** {r[4] or "-"}\n')
for _t,_m in (('Dood maar later actief','[Z14 dood-actief]'),('Correcties','[Z14 correctie]'),('Tijdlijn (twee plekken)','[Z14 tijdlijn]'),('Verhoudingen','[Z14 verhouding]'),('Na 801','[Z14 toekomst]'),('Langlevende volken','[Z14 levensduur]')):
  _z14.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,jaar from canon where instr(feit,?)>0 order by id",(_m,)):
    _z14.append(f'\n### {r[0]} · {r[1]}\n{r[2][r[2].find(_m):]}\n- **Jaar:** {r[3] if r[3] is not None else "-"}\n')
_z14.append('\n## Haken per rij herschreven (Z14), per categorie\n\n'+''.join(f'- {a}: {b}\n' for a,b in c.execute("select categorie,count(*) from canon where feit like '%[Z14 verdieping%' group by 1 order by 2 desc")))
_z14.append('\n## Wrijvingen Z14\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z14-%' order by id"):
  _z14.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
w('28_restpunten.md',''.join(_z14))

_z15=['# 29 · Ysa en Thalen: "Ysa\'s verloren liefde" (ronde Z15)\n\nBeatplan 03 (verhalen/beatplan_03_ysa.md) in de canon. Tijdlijn: -1240 Muiterij, ca. -1200 Thalens stem in de kluis (de mens sterft), -480 val als Sterrensteen (ca. 760 jaar in de baan, "800 jaar"), 0 Ysara opgenomen, daarna Thalen in Ysara, ca. 130 kaping, 801 Liora. Alleen volwassenen (18+) in seksuele rollen. Alleen uit canon.db.\n']
for _t,_q in (('Besluiten van Rogier (vastgesteld)','BESLUIT-Z15-%'),('Besluiten Z15b: volg de canon (vastgesteld)','BESLUIT-Z15b-%'),('Verhaal (versie Z15b, geldend)','ROMANCE-Z15b-ysa-beatplan'),('Beats (versie Z15b, geldend)','ROMANCE-Z15b-ysa-beat-%'),('Nieuw bedacht Z15b (voorstel)','YSA-Z15b-%'),('Haken Z15b','HAAK-Z15b-%'),('Rapport Z15b','KWALITEIT-Z15b'),('Correctie 800 jaar','YSA-Z15-800jaar'),('Verhaal (versie Z15, vervangen)','ROMANCE-Z15-ysa-beatplan'),('Verhaalvolgorde','VERHAALTIJD-Z15-%'),('Beats (versie Z15, vervangen)','ROMANCE-Z15-ysa-beat-%'),('Nieuw bedacht (voorstel)','YSA-Z15-_'),('','YSA-Z15-1_'),('Tijdlijn Thalen','TOESTAND-Z15-%'),('Haken naar andere boeken','HAAK-Z15-%'),('Rapport','KWALITEIT-Z15')):
  if _t: _z15.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by code",(_q,)):
    _z15.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z15.append('\n## Wrijvingen Z15\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z15%' order by id"):
  _z15.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
w('29_ysa-thalen.md',''.join(_z15))

_z16=['# 30 · Roman "The Body Is the Price" (ronde Z16, bijgewerkt Z17 en Z18)\n\nWattpad-roman van Ysa en Thalen, 33 hoofdstukken, ca. 61.000 woorden (verhalen/roman_ysa_hoofdstukplan.md). Ysa sterft -1209, Thalen -1198 (74). Alleen volwassenen (18+) in seksuele rollen. Alleen uit canon.db.\n']
for _t,_q in (('Besluiten van Rogier (vastgesteld)','BESLUIT-Z16-%'),('Roman','ROMAN-Z16-roman'),('Novelle','VERHAAL-Z16-novelle'),('Hoofdstukken','ROMAN-Z16-h%'),('Nieuw bedacht (voorstel)','YSA-Z16-%'),('Tijdlijn','TOESTAND-Z16-%'),('Rapport','KWALITEIT-Z16')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z16\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z16%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z17: keuzes h1-6 en open punten\n')
for _t,_q in (('Besluiten Z17 (vastgesteld)','BESLUIT-Z17-%'),('Nieuw bedacht Z17 (voorstel)','YSA-Z17-%'),('Tijdlijn Thalen Z17','TOESTAND-Z17-%'),('Ves-Anath en inslag','GEB-Z17-%'),('Haak 801','HAAK-Z17-%'),('Rapport Z17','KWALITEIT-Z17')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z17\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z17%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z18: keuzes h7-12\n')
for _t,_q in (('Besluiten Z18 (vastgesteld)','BESLUIT-Z18-%'),('Nieuw bedacht Z18 (voorstel)','YSA-Z18-%'),('Rapport Z18','KWALITEIT-Z18')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z18\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z18%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z18b en Z19: alles vastgelegd (h13-18)\n')
for _t,_q in (('Besluiten Z18b (vastgesteld)','BESLUIT-Z18b-%'),('Besluiten Z19 (vastgesteld)','BESLUIT-Z19-%'),('Nieuw bedacht Z19 (vastgesteld)','YSA-Z19-%')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z19\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z19%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z20: alles vastgelegd (h19-24)\n')
for _t,_q in (('Besluiten Z20 (vastgesteld)','BESLUIT-Z20-%'),('Nieuw bedacht Z20 (vastgesteld)','YSA-Z20-%')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z20\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z20%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z21: alles vastgelegd (h25-33, review, motoren)\n')
for _t,_q in (('Besluiten Z21 (vastgesteld)','BESLUIT-Z21-%'),('Nieuw bedacht Z21 (vastgesteld)','YSA-Z21-%'),('Motorenkaart Z21','MOTOREN-Z21')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z21\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z21%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z22: motorregel en zaaibeats\n')
for _t,_q in (('Besluiten Z22 (vastgesteld)','BESLUIT-Z22-%'),('Nieuw bedacht Z22 (vastgesteld)','YSA-Z22-%'),('Overgangskaart Z22','MOTOREN-Z22')):
  _z16.append(f'\n## {_t}\n')
  for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like ? order by id",(_q,)):
    _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Intensiteit:** {r[6] or "-"} · **Verwijst naar:** {r[4] or "-"}\n')
_z16.append('\n## Wrijvingen Z22\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z22%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z23: eindfeedback\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'BESLUIT-Z23-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z23%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z24: eindrapport consistentie\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'BESLUIT-Z24-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z24%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z25: laatste feedback\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'BESLUIT-Z25-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z25%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z26: telling 3.454\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'BESLUIT-Z26-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z26%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z27: kraaien, inheemse planeet, tijdlijn\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'BESLUIT-Z27-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z27%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z28: alle details van de roman per hoofdstuk\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'YSA-Z28-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z28%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z29: sfeerdetails van de roman per hoofdstuk (volledige lezing)\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar,jaar,intensiteit from canon where code like 'YSA-Z29-%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n{r[2]}\n- **Status:** {r[3]} · **Jaar:** {r[5] if r[5] is not None else "-"} · **Verwijst naar:** {r[4] or "-"}\n')
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z29%' order by id"):
  _z16.append(f'\n### {r[0]} · {r[1]}\n- **Status:** {r[2]}\n- **Wat:** {r[3]}\n')
_z16.append('\n# Ronde Z30: architectuur (draagkracht, één veiligheidsregel, rechtzetting Zegel jaar 0)\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar from canon where code like 'BESLUIT-Z30-%' order by id"):
  _z16.append(f"\n### {r[0]} · {r[1]}\n- **Wat:** {r[2]}\n- **Status:** {r[3]}\n- **Verwijst naar:** {r[4]}\n")
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z30%' order by id"):
  _z16.append(f"\n### {r[0]} · {r[1]} ({r[2]})\n{r[3]}\n")
_z16.append('\n# Ronde Z31: robuust tegen kettingschade (ankers, tests, migraties, wijzigingen) en voorstellen\n')
for r in c.execute("select code,onderwerp,feit,status,verwijst_naar from canon where code like 'VOORSTEL-Z31-%' order by id"):
  _z16.append(f"\n### {r[0]} · {r[1]} ({r[3]})\n{r[2]}\n- **Verwijst naar:** {r[4]}\n")
for r in c.execute("select code,titel,status,beschrijving from wrijving where code like 'WRIJ-Z31%' order by id"):
  _z16.append(f"\n### {r[0]} · {r[1]} ({r[2]})\n{r[3]}\n")
_z16.append('\n## Ankers (bron van waarheid)\n'+''.join(f"- **{a}** = {b} ({d}; bron {e})\n" for a,b,e,d in c.execute('select sleutel,waarde,bron_code,toelichting from anker order by id')))
w('30_roman-ysa.md',''.join(_z16))
w('40_ideeenbank.md','# Ideeënbank (Kleur, geen canon)\n\nCatalogi en skeletten: inspiratie. Het verhaal wint altijd. Bron: view v_ideeenbank.\n\n'+''.join(f"### {a} · {b} ({s})\n{f}\n\n" for a,b,s,f in c.execute("select code,onderwerp,status,feit_schoon from canon where ideeenbank=1 and status in('vastgesteld','voorlopig') order by id")))
w('00_HANDLEIDING.md','# Handleiding database (Z30, bijgewerkt Z33: canon-motor)\n\n**Bij twijfel wint het verhaal, behalve bij Kern.**\n\n'+''.join(f"## {a} · {b}\n{t}\n\n" for a,b,t in c.execute('select code,onderwerp,tekst from handleiding order by id')))
w('90_WRIJVINGEN.md','# Wrijvingen\n\n'+'\n'.join(f'### {a} · {b}\n- **Type/status:** {t} / {s}\n- **Botst:** {d}\n- **Wat:** {e}\n- **Verwijst naar:** {v or "-"}\n' for a,b,t,s,d,e,v in wr))
ov=c.execute('select code,vraag,waarom_belangrijk,status,antwoord,verwijst_naar from open_vraag order by id').fetchall()
w('91_OPEN_VRAGEN.md','# Open vragen\n\n'+'\n'.join(f'### {a} · {b}\n- **Waarom:** {wb}\n- **Status:** {s}'+(f'\n- **Voorstel/antwoord:** {an}' if an else '')+f'\n- **Verwijst naar:** {v or "-"}\n' for a,b,wb,s,an,v in ov))
w('99_LOGBOEK.md','# Logboek\n\n'+'\n'.join(f'- {d}: {x}' for d,x in c.execute('select datum,wat from logboek order by id')))
if __name__=='__main__': print('bijbel/ gegenereerd:',len(os.listdir(B)),'bestanden')

# Z37: personage_profiel (afgeleid; één regel per persoon, bron voor anker, relaties, naam- en na-doodtoets)
_pp=[r[1] for r in c.execute('pragma table_info(personage_profiel)')]
if _pp:
  _sel=[x for x in ('code','naam','volk','fase_nr','geboren','gestorven','rol','wil','archetype') if x in _pp]
  w('41_personages_profiel.md','# Personages (profiel, afgeleid)\n\nAfgeleid uit canon door afgeleid_motor.py (Z37). Niet met de hand bewerken.\n\n| '+' | '.join(_sel)+' |\n|'+'---|'*len(_sel)+'\n'+''.join('| '+' | '.join('' if v is None else str(v).replace('|','/').replace('\n',' ') for v in r)+' |\n' for r in c.execute(f"select {','.join(_sel)} from personage_profiel order by code")))
# ---------- Eén bestand: WERELD_VELMARA.md (lossless, terug te laden met importeer.py) ----------
import datetime
def esc(v): return '' if v is None else str(v)
TAB={'canon':['code','categorie','onderwerp','feit','reden','status','ronde','hangt_samen_met','verwijst_naar','jaar','tijdperk','intensiteit','weet','functie','afstoting','aantrekking_bron','aantrekking','techniek','draagkracht','ideeenbank','veilig_18plus','veilig_variant','vervangen_door','feit_schoon','draagkracht_handmatig','bron_handmatig','epistemiek'],
'anker':['sleutel','waarde','bron_code','toelichting','patroon','bereik'],
'naam_markering':['naam_a','naam_b','codes','soort','status','wrijving','toelichting'],
'toets_uitzondering':['toets','code','detail','reden','wrijving'],
'wijziging':['ronde','code','soort','veld','oud','nieuw','datum','bron'],
'schema_versie':['versie','naam','toegepast'],
'wrijving':['code','titel','delen_die_botsen','beschrijving','type','status','verwijst_naar'],
'open_vraag':['code','vraag','waarom_belangrijk','status','antwoord','verwijst_naar'],
'logboek':['id','datum','wat'],
'handleiding':['code','onderwerp','tekst'],
'regel':['code','domein','omschrijving','sql_test','bron','goedgekeurd_door','status','niveau'],
'boog':['code','fase','boek','hoofdpersoon','leeftijd_hoofdpersoon','geslacht_hoofdpersoon','romance','erotische_sleutelscene','terugkerend_motief','noodoplossing','wie_betaalt','toon','vorm','afloop','bron','status','voorstel','voorstel_status','verteller','tempo','beslisser_as','betaler_as','vervalst_as','ontdekt_as','schaal','herkenbaar','zintuig','haak','synopsis_code'],
'personage':['code','naam','per_code','fase','rol','eigen_fout','soort_fout','wie_betaalt','zelfbedrog','daarna_doet','bron','status','voorstel','voorstel_status'],
'zaadje':['code','wat','geplant_in','oogst_in','status','bron'],
'sjabloon_familie':['sig','grootte','prefixen','markering','voorstel','voorbeeld'],
'sjabloon_lid':['sig','code','markering'],
'personage_toestand':['per_code','jaar','leeftijd','rol','regio','wil','geheim','verandert','aanname','aanname_reden','bron','soort','volk','toestand','maan','rest','status_oud'],
'levensduur':['volk','jaren','soort','bron','toelichting'],
'fase_rijm':['fase','volgorde','mechanisme','beslisser','beslisser_as','betaler','betaler_as','vervalst','vervalst_as','ontdekt','ontdekt_as','schaal','erft_van','blijvende_verandering','bron','status','voorstel'],
'kernscene':['boog_code','volgorde','scene','bron'],
'keuze':['code','soort','onderwerp','aanbeveling','raakt','impact','draagkracht','status','bron']}
for _t in ('verhaal_as','boog_as','verhaal_profiel','doel','doelprofiel','lezersdata','gewichtset','ideeen_verwerking','domein','competentievraag','competentie_antwoord','motief_detail','beroep','gave','sim_regel','gebeurtenis_type','tech_gebeurtenistype','sim_run','sim_gebeurtenis','sim_figuur','verblijf','kennis','per_relatie','steekproef','sim_fase','sim_wet','sim_huis'):
  if c.execute('select 1 from sqlite_master where name=?',(_t,)).fetchone(): TAB[_t]=[r[1] for r in c.execute(f'pragma table_info({_t})') if r[1]!='id']
if 'citaat' in [r[1] for r in c.execute('pragma table_info(keuze)')]: TAB['keuze']=TAB['keuze']+['citaat']
LBL={'feit':'wat','reden':'waarom'}
def rec(t,r):
  head=r.get('code') or r.get('id')
  titel=r.get('onderwerp') or r.get('titel') or r.get('vraag') or r.get('datum') or r.get('naam') or r.get('hoofdpersoon') or r.get('omschrijving') or r.get('wat') or r.get('per_code') or r.get('fase') or r.get('volk') or r.get('boog_code')
  s=f"<!-- REC {t} -->\n### {head} · {titel}\n"
  for k in TAB[t]: s+=f"- **{LBL.get(k,k) if t=='canon' else k}:** {esc(r[k])}\n"
  return s+"<!-- /REC -->\n"
def tabel(t): 
  cur=c.execute(f"select {','.join(TAB[t])} from {t} order by "+('versie' if t=='schema_versie' else 'id')); return [dict(zip(TAB[t],x)) for x in cur]
cr=tabel('canon');versie=max(r['ronde'] or 0 for r in cr)
S=[]
S.append(f"""<!-- SECTIE: METADATA -->
# WERELD VELMARA · volledige wereldbijbel in één bestand
- **naam:** Velmara · **versie:** ronde {versie} · **datum:** {datetime.date.today()} · **taal:** Nederlands
- **genre:** erotische dark fantasy voor volwassenen (alle seksuele deelnemers 18+) · **toon:** zinnelijk, geladen, rauw
**Leeswijzer voor een LLM**
1. Dit bestand is compleet en zelfstandig; het is de hele wereld.
2. Lees eerst WERELDKERN; die regels gaan voor alles.
3. Elk onderdeel heeft een vaste code (PREFIX-slug); `verwijst_naar` noemt andere codes, gescheiden door `;`.
4. Zoek een code met zoeken op `### CODE`.
5. `vastgesteld` = Rogiers keuze; `voorlopig` = voorstel; `vervallen` = negeren.
6. Check WRIJVINGEN vóór je iets nieuws bedenkt.
7. Blokken tussen `<!-- REC -->` en `<!-- /REC -->` zijn machineleesbaar: één veld per regel, wijzig het formaat niet.
8. Uitbreiden: zie UITBREIDINGSREGELS onderaan.
""")
S.append('<!-- SECTIE: WERELDKERN -->\n'+KERN.replace('`python3 scene.py <codes>`','een uittreksel van de gevraagde codes plus hun verwijzingen').replace('**Verder lezen:** 01_INDEX.md → domeinbestand → 90_WRIJVINGEN.md.','**Verder lezen:** INDEX → DOMEINEN → WRIJVINGEN.').replace('(07_rituelen.md)','(domein Rituelen)'))
def dom(r):
  f=plaats(r)
  for x in DOM:
    if x[0]==f: return x[1]
  return 'Overig'
order=[d[1] for d in DOM]+['Overig']
groups={d:[r for r in cr if dom(r)==d] for d in order}
S.append('<!-- SECTIE: INDEX -->\n# INDEX\n'+''.join(f"- **{d}**: {', '.join(r['code'] for r in groups[d])}\n" for d in order if groups[d]))
S.append('<!-- SECTIE: DOMEINEN -->\n# DOMEINEN\n'+''.join(f"\n## {d}\n\n"+''.join(rec('canon',r) for r in groups[d]) for d in order if groups[d]))
S.append('<!-- SECTIE: WRIJVINGEN -->\n# WRIJVINGEN\n'+''.join(rec('wrijving',r) for r in tabel('wrijving'))+'\n<!-- SECTIE: OPEN_VRAGEN -->\n# OPEN VRAGEN\n'+''.join(rec('open_vraag',r) for r in tabel('open_vraag')))
S.append('<!-- SECTIE: HANDLEIDING -->\n# HANDLEIDING\n'+''.join(rec('handleiding',r) for r in tabel('handleiding')))
S.append('<!-- SECTIE: LOGBOEK -->\n# LOGBOEK\n'+''.join(rec('logboek',r) for r in tabel('logboek')))
for _t in ('anker','naam_markering','toets_uitzondering','schema_versie','wijziging','regel','boog','personage','zaadje','sjabloon_familie','sjabloon_lid','personage_toestand','levensduur','fase_rijm','kernscene','keuze','verhaal_as','boog_as','verhaal_profiel','doel','doelprofiel','lezersdata','gewichtset','ideeen_verwerking','domein','competentievraag','competentie_antwoord','motief_detail','beroep','gave')+tuple(t for t in ('sim_regel','gebeurtenis_type','tech_gebeurtenistype','sim_run','sim_gebeurtenis','sim_figuur','verblijf','kennis','per_relatie','steekproef','sim_fase','sim_wet','sim_huis') if t in TAB): S.append(f'<!-- SECTIE: {_t.upper()} -->\n# {_t.upper()}\n'+''.join(rec(_t,r) for r in tabel(_t)))
S.append("""<!-- SECTIE: UITBREIDINGSREGELS -->
# UITBREIDINGSREGELS
1. Nieuw onderdeel = nieuw REC-blok in DOMEINEN onder het juiste domein, met alle velden: code, categorie, onderwerp, wat, waarom, status (`voorlopig`), ronde, hangt_samen_met, verwijst_naar.
2. Code: `PREFIX-slug`, uniek, nooit hergebruikt. Prefixen: REG, ECO, MACHT, HUI, WET, REGEL, ORDE, MAGIE, GES, GEH, CUL, MODE, SFEER, RIT, HAND, SYS, RITE, KINK, PER, QST, FASE, GEB, VOOR, LICH; wrijvingen WRIJ-nnn, vragen VRAAG-nnn.
3. Elke code in verwijst_naar moet bestaan.
4. Spreek de WERELDKERN niet tegen; botst iets, voeg dan een wrijving toe (type `mogelijke fout` met oplossing, of `bron van verhalen`).
5. Een HAND- of SYS-onderdeel heeft hetzelfde onderwerp als zijn RIT-ritueel.
6. Voeg een LOGBOEK-blok toe voor elke ronde. Alle seksuele deelnemers zijn 18+; dwang alleen als donker thema tussen volwassenen; geen dieren.
7. Terugladen in een database: `python3 importeer.py WERELD_VELMARA.md nieuw.db`.
""")
open(os.path.join(D,'WERELD_VELMARA.md'),'w').write('\n'.join(S))

import wrijving_plot
print('plotoverzicht wrijvingen:',wrijving_plot.maak())
