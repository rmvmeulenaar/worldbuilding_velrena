"""Z35 stap 1: parser voor gegenereerde TOESTAND-rijen -> personage_toestand. Parse alleen wat zeker is; '-'/'onbekend' -> NULL."""
import re
LEEG=lambda v:None if v is None or v.strip(' .') in('','-','onbekend','—') else v.strip().rstrip('.').strip()
BOILER={'dit is het moment waarop de rij speelt'}
def parse(ft):
  """-> dict of None als de vorm niet zeker herkend wordt."""
  ft=(ft or '').strip()
  m=re.fullmatch(r'Historisch: (overleden|versteend) ca\. (-?\d+)((?: [^(.]+)?) \(aanname: levensduur (\d+)\)\. Leeft voort in annalen, kraaien of afstammelingen\.(.*)',ft,re.S)
  if m:
    rest=LEEG(m.group(5));gok=f'script gokte {m.group(1)} ca. {m.group(2)}{m.group(3)} uit levensduur {m.group(4)}'
    k=re.search(r'\b(?:sterft in jaar|sterft in|versteent zichzelf ca\.) (-?\d+)\b',rest or '')
    if k and 'vervalt' in (rest or ''):  # latere correctie (Z13/Z14) in dezelfde rij noemt het echte jaar
      return dict(soort='overleden',jaar=int(k.group(1)),leeftijd=None,aanname=0,aanname_reden=None,rest=rest+' ['+gok+'; vervallen]')
    return dict(soort='overleden (aanname)',jaar=None,leeftijd=None,aanname=1,aanname_reden=gok+'; niet als feit opgeslagen, sterfjaar wordt berekend in v_personage_tijdlijn',rest=rest)
  m=re.fullmatch(r'In (-?\d+) actief, leeftijd (\d+)\.(.*)',ft,re.S)
  if m: return dict(soort='actief',jaar=int(m.group(1)),leeftijd=int(m.group(2)),rest=LEEG(m.group(3)))
  m=re.fullmatch(r'Geboren ca\. (-?\d+) \((\d) ([A-Za-zë]+)\), regio ([\w-]+)\.(?: Aanname: (.*))?',ft,re.S)
  if m:
    a=m.group(5)
    k=re.search(r'Geboren ca\. (-?\d+) \(',a or '')
    if a and k and 'vervalt' in a:  # correctie in dezelfde rij: het echte jaar volgt uit de PER-rij
      return dict(soort='geboren',jaar=int(k.group(1)),leeftijd=0,regio=LEEG(m.group(4)),aanname=0,aanname_reden=None,had_aanname=1,rest='script Z11 gokte '+m.group(1)+'; gecorrigeerd: '+a.strip())
    return dict(soort='geboren',jaar=int(m.group(1)),leeftijd=0,regio=LEEG(m.group(4)),aanname=int(bool(a)),aanname_reden=('script Z11: '+a.strip()) if a else None,had_aanname=int(bool(a)))
  m=re.fullmatch(r'Jaar (-?\d+), leeftijd (\d+), regio ([\w-]+)\. Rol: (.*) Wil: (.*) Geheim: (.*) Verandert: (.*)',ft,re.S)
  if m:
    v=LEEG(m.group(7));v=None if v and v.lower() in BOILER else v
    return dict(soort='knooppunt',jaar=int(m.group(1)),leeftijd=int(m.group(2)),regio=LEEG(m.group(3)),rol=LEEG(m.group(4)),wil=LEEG(m.group(5)),geheim=LEEG(m.group(6)),verandert=v)
  m=re.fullmatch(r'Jaar (-?\d+) \(([^)]*)\), leeftijd (\d+), plaats: (.*?)\. Toestand: (.*?)(?: Verandert: (.*))?',ft,re.S)
  if m: return dict(soort='toestand',jaar=int(m.group(1)),maan=LEEG(m.group(2)),leeftijd=int(m.group(3)),regio=LEEG(m.group(4)),toestand=LEEG(m.group(5)),verandert=LEEG(m.group(6)))
  m=re.fullmatch(r'In (-?\d+) leeftijd (\d+); (.*)',ft,re.S)
  if m: return dict(soort='later',jaar=int(m.group(1)),leeftijd=int(m.group(2)),verandert=LEEG(m.group(3)))
  m=re.fullmatch(r'Zelfde persoon als (PER-[\w-]+); tijdlijn staat daar \(TOESTAND-[\w-]+\*\)\. (.*)',ft,re.S)
  if m: return dict(soort='samengevoegd',doel=m.group(1),rol=LEEG(m.group(2)))
  return None
def per_code(verwijst,codes):
  for x in (verwijst or '').split(';'):
    x=x.strip()
    if x and x in codes and x.startswith(('PER-','PERS-','HOOFDPERS-')): return x
  return None
