"""Plotbaar overzicht van alle openstaande wrijvingen, gegroepeerd per thema; wordt aan bijbel/90_WRIJVINGEN.md toegevoegd."""
import sqlite3,os
D=os.path.dirname(os.path.abspath(__file__))
TH=[('Volken en verhouding', ['volk', 'karr', 'ishvar', 'oevrin', 'myrrhen', 'ves-lethi', 'aelthir', 'vathren', 'dhurn', 'verhouding', '1 op']), ('Toestemming, lichaam en stallen', ['toestemming', 'instem', 'koe', 'stal', 'ankerwortel', 'lijngraver', 'reuzen', 'vervorm', 'lich-', 'nav-', 'lijn-', 'grijswortel', 'verslaving', 'weiger']), ('Bloed, register en afstamming', ['register', 'inteelt', 'verwant', 'afstamming', 'grieta', 'teo', 'merk', 'bloedspiegel']), ('Macht, huizen en geld', ['varenne', 'kaldra', 'mirre', 'qesh', 'schuld', 'markt', 'leger', 'kharvos', 'rhun', 'macht', 'economie']), ('Tijdlijn en continuiteit', ['jaartal', 'ronde', 'geb-', 'omzetting', 'tijd', 'klok', 'bloedmaan', '600 jaar']), ('Geloof, recht en rituelen', ['religie', 'orde', 'geloof', 'vael', 'rite', 'ritueel', 'recht', 'wet', 'tribunaal', 'gunstnacht', 'tweegelofte', 'rolwissel']), ('Zegel, magie en geheim', ['zegel', 'gave', 'geheim', 'lek', 'wortel', 'magie', 'vonk', 'lamp', 'orrim', 'sterren', '210'])]
VERHAAL={'Zegel, magie en geheim':'een ontdekking die de leer breekt: wie het bewijst, wordt gejaagd',
'Toestemming, lichaam en stallen':'een bevrijding of opstand tegen de systeemgruwel, met een dader die ontmaskerd wordt',
'Bloed, register en afstamming':'een identiteitsthriller: wie ben je als je register liegt, en wie heeft het vervalst',
'Volken en verhouding':'een ontmoeting met een volk dat het systeem omzeilt; elk huis wil hun geheim',
'Macht, huizen en geld':'een politieke intrige met verraad, schuld en een huis dat valt',
'Geloof, recht en rituelen':'een proces, schisma of ritueel dat ontspoort en de Orde dwingt tot kleur bekennen',
'Tijdlijn en continuiteit':'eerst canon-besluit nodig; daarna mogelijk een vervalsing-in-de-annalen-verhaal'}
def thema(t):
  s=t.lower()
  for n,kw in TH:
    if any(k in s for k in kw): return n
  return 'Overig'
def maak():
  c=sqlite3.connect(os.path.join(D,'canon.db'))
  ond=dict(c.execute('select code,onderwerp from canon'))
  g={}
  for code,ti,de,be,ty,st,vn in c.execute("select code,titel,delen_die_botsen,beschrijving,type,status,verwijst_naar from wrijving where status in ('open','voorstel') order by code"):
    th=thema(f'{ti} {de} {be}') if ty=='bron van verhalen' else ('Tijdlijn en continuiteit' if thema(f'{ti} {de} {be}')=='Overig' else thema(f'{ti} {de} {be}'))
    part=[ond.get(x.strip(),x.strip()) for x in (de or '').replace(',',';').split(';') if x.strip()]
    g.setdefault(th,[]).append((code,ti,be,ty,st,part))
  out=['\n\n# Plotbaar overzicht van alle openstaande wrijvingen (per thema)\n','Per wrijving: oorzaak, partijen, wat er kan gebeuren en een mogelijk verhaal. "Mogelijke fout" = eerst een canonbesluit van Rogier.\n']
  for th in [t for t,_ in TH]+['Overig']:
    if th not in g: continue
    out.append(f'\n## {th} ({len(g[th])})\n')
    for code,ti,be,ty,st,part in g[th]:
      gebeur=('de botsing komt aan het licht en dwingt partijen tot een keuze' if ty=='bron van verhalen' else 'kies welke versie canon wordt; de andere kan als vervalsing of gerucht blijven')
      out.append(f'- **{code} · {ti}** ({ty}, {st})\n  - Oorzaak: {be}\n  - Partijen: {", ".join(part) or "-"}\n  - Wat kan er gebeuren: {gebeur}\n  - Mogelijk verhaal: {VERHAAL.get(th,"vrij te plotten")}\n')
  open(os.path.join(D,'bijbel','90_WRIJVINGEN.md'),'a').write(''.join(out))
  return {k:len(v) for k,v in g.items()}
if __name__=='__main__': print(maak())
