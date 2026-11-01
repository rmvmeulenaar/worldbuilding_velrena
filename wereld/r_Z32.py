# Ronde Z32: Z31-voorstellen vaststellen en verwerken (Rogier: alles zoals aanbevolen, 2026-10-31).
# Idempotent, additief: niets verwijderd; vervangen rijen -> 'voorlopig, vervangen' + vervangen_door. Roman niet aangeraakt.
import sqlite3,shutil,os,re,json,subprocess,sys
sys.path.insert(0,'migraties');sys.path.insert(0,'z32')
import afgeleid,migreer
from data import *
DT='2026-10-31';RD='Z32';DB=os.environ.get('DB','canon.db')
if DB=='canon.db' and not os.path.exists('canon_backup_Z32.db'): shutil.copy('canon.db','canon_backup_Z32.db')
c=sqlite3.connect(DB);migreer.draai(c)
S={'nieuw':[],'vervangen':[],'gemarkeerd':[],'wrij_nieuw':[],'wrij_gesloten':[],'vraag':[],'anker':[],'link':[],'naam_markering':0,'handmatig':[],'wijziging':0}
r0=c.execute("select ronde from canon where code='BESLUIT-Z32-1'").fetchone()
RONDE=r0[0] if r0 else c.execute("select max(ronde) from canon").fetchone()[0]+1
KOL=['categorie','onderwerp','hangt_samen_met','verwijst_naar','jaar','tijdperk','intensiteit','weet','functie','afstoting','aantrekking_bron','aantrekking','techniek']
def wijz(code,soort,veld,oud,nieuw,bron='r_Z32.py'):
  S['wijziging']+=c.execute('insert or ignore into wijziging(ronde,code,soort,veld,oud,nieuw,datum,bron) values(?,?,?,?,?,?,?,?)',(RD,code,soort,veld or '',oud,nieuw,DT,bron)).rowcount
def rij(code):
  r=c.execute(f"select {','.join(KOL)},status,feit_schoon,draagkracht_handmatig,feit from canon where code=?",(code,)).fetchone()
  if not r: raise SystemExit('ontbreekt: '+code)
  return dict(zip(KOL+['status','feit_schoon','handm','feit'],r))
def markeer(old,new,notitie=''):
  st,vd=c.execute("select status,vervangen_door from canon where code=?",(old,)).fetchone()
  if st!='voorlopig, vervangen' or vd!=new:
    c.execute("update canon set status='voorlopig, vervangen',reden=coalesce(reden,'')||?,vervangen_door=? where code=?",(f' [Ronde Z32: vervangen door {new}{notitie}]',new,old))
    S['gemarkeerd'].append(old);wijz(old,'vervangen','status',st,'voorlopig, vervangen -> '+new)
  h=c.execute("select draagkracht_handmatig from canon where code=?",(old,)).fetchone()[0]
  if h is not None:
    c.execute("update canon set draagkracht_handmatig=NULL where code=?",(old,));wijz(old,'draagkracht handmatig','draagkracht_handmatig',h,None,'vervangen rij wordt nooit Kern')
def vervang(old,new,feit,status=None,handm=None,reden='',**over):
  o=rij(old)
  if not c.execute("select 1 from canon where code=?",(new,)).fetchone():
    v={k:o[k] for k in KOL};v.update(over)
    v['hangt_samen_met']=';'.join(x for x in [v.get('hangt_samen_met') or '',old] if x)
    st=status or o['status']
    c.execute(f"insert into canon({','.join(KOL)},feit,status,reden,ronde,code) values({','.join('?'*len(KOL))},?,?,?,?,?)",[v[k] for k in KOL]+[feit,st,f'{R}; vervangt {old}'+(f'. {reden}' if reden else ''),RONDE,new])
    S['vervangen'].append(f'{old} -> {new}');wijz(new,'toegevoegd','canon',None,st)
  hm=handm or o['handm']
  if hm and c.execute("select draagkracht_handmatig from canon where code=?",(new,)).fetchone()[0]!=hm:
    c.execute("update canon set draagkracht_handmatig=? where code=?",(hm,new));S['handmatig'].append(new);wijz(new,'draagkracht handmatig','draagkracht_handmatig',None,hm)
  markeer(old,new)
def nieuw(code,cat,ond,feit,verw='',handm=None,status='vastgesteld',jaar=None):
  if not c.execute("select 1 from canon where code=?",(code,)).fetchone():
    c.execute("insert into canon(categorie,onderwerp,feit,status,reden,hangt_samen_met,ronde,code,verwijst_naar,jaar) values(?,?,?,?,?,?,?,?,?,?)",(cat,ond,feit,status,R,verw,RONDE,code,verw,jaar))
    S['nieuw'].append(code);wijz(code,'toegevoegd','canon',None,status)
  if handm and c.execute("select draagkracht_handmatig from canon where code=?",(code,)).fetchone()[0]!=handm:
    c.execute("update canon set draagkracht_handmatig=? where code=?",(handm,code));S['handmatig'].append(code);wijz(code,'draagkracht handmatig','draagkracht_handmatig',None,handm)
def sub(t,pairs):
  for a,b in pairs: t=re.sub(a,b,t)
  return t
def anker_bron(sl,new):
  o=c.execute("select bron_code from anker where sleutel=?",(sl,)).fetchone()[0]
  if o!=new: c.execute("update anker set bron_code=? where sleutel=?",(new,sl));S['anker'].append(f'{sl}: {o}->{new}');wijz('ANKER-'+sl,'bron gewijzigd','bron_code',o,new)
def sluit(code,door,status='opgelost'):
  st,b=c.execute("select status,beschrijving from wrijving where code=?",(code,)).fetchone()
  if not st.startswith('opgelost'):
    c.execute("update wrijving set status=?,beschrijving=? where code=?",(status,(b or '')+f' [Opgelost in Z32: {door}]',code));S['wrij_gesloten'].append(code);wijz(code,'gesloten','status',st,status)
def wrij(code,titel,delen,besch,verw,typ='naam',st='open'):
  if not c.execute("select 1 from wrijving where code=?",(code,)).fetchone():
    c.execute('insert into wrijving(titel,delen_die_botsen,beschrijving,type,status,code,verwijst_naar) values(?,?,?,?,?,?,?)',(titel,delen,besch,typ,st,code,verw));S['wrij_nieuw'].append(code);wijz(code,'toegevoegd','wrijving',None,st)
def vraag(code,antw):
  st=c.execute("select status from open_vraag where code=?",(code,)).fetchone()[0]
  if st.startswith('open'):
    c.execute("update open_vraag set status='beantwoord (Rogier)',antwoord=? where code=?",(antw,code));S['vraag'].append(code);wijz(code,'beantwoord','status',st,'beantwoord (Rogier)')
fs=lambda code:rij(code)['feit_schoon']

# ===== 1 SYS-wijding =====
vervang('SYS-wijding','SYS-wijding-Z32',SYS_WIJDING,status='vastgesteld',reden='Herformulering harde lijn: geen lezing als minderjarigheid mogelijk (WRIJ-Z31-5)')

# ===== 2 toetsfouten =====
markeer('YSA-Z15-1','BESLUIT-Z18-3');markeer('YSA-Z16-11','BESLUIT-Z18-3')
vervang('PER-v4-thalen-orr','PER-v4-thalen-orr-Z32',THALEN_PER,reden='Leeftijden volgens anker BESLUIT-Z18-3 (32 in -1240, dood op 74 in -1198); Thalens patroon in de Rekenaar (BESLUIT-Z32-12)')
anker_bron('thalen_naam','PER-v4-thalen-orr-Z32')
nieuw_code='BESLUIT-Z32-1'
vervang('BESLUIT-Z16-9','BESLUIT-Z32-1',MUITERIJ,status='vastgesteld',reden='Overlevenden volgens anker BESLUIT-Z26-1: 7.546 (WRIJ-Z31-3)',categorie='Besluit')
anker_bron('aan_boord','BESLUIT-Z32-1')
vervang('BESLUIT-Z24-8','BESLUIT-Z32-2',LANDERS,status='vastgesteld',reden='Overlevenden volgens anker: 7.546 (WRIJ-Z31-3)')
WC=None
try: WC=len(open('verhalen/roman_ysa_VOLLEDIG.md',encoding='utf-8').read().split())
except Exception: pass
rom=fs('ROMAN-Z16-roman').replace('ca. 61.000 woorden',f'ca. 54.400 woorden (gemeten 2026-10-31 met wc -w: {WC} in verhalen/roman_ysa_VOLLEDIG.md, incl. titelpagina)')
vervang('ROMAN-Z16-roman','ROMAN-Z16-roman-Z32',rom,reden='Woordenaantal gemeten (WRIJ-Z31-4)')
for sl in ('muiterij_jaar','roman_hoofdstukken','roman_woorden'): anker_bron(sl,'ROMAN-Z16-roman-Z32')
for veld in ('verwijst_naar','hangt_samen_met'):
  v=c.execute(f"select {veld} from canon where code='BESLUIT-Z25-2'").fetchone()[0] or ''
  t=[x.strip() for x in v.split(';')]
  if 'BESLUIT-Z25-8' in t:
    nv=';'.join('BESLUIT-Z24-8' if x=='BESLUIT-Z25-8' else x for x in t);c.execute(f"update canon set {veld}=? where code='BESLUIT-Z25-2'",(nv,));S['link'].append(f'BESLUIT-Z25-2.{veld}: BESLUIT-Z25-8 -> BESLUIT-Z24-8');wijz('BESLUIT-Z25-2','link hersteld',veld,v,nv,'WRIJ-Z31-1: eenduidig (enige rij over lander één als laatste afdaling met 412 stoelen; zelfde volgnummer -8)')

# ===== 3 namen =====
nieuw('BESLUIT-Z32-3','Besluit','Namen hernoemd (Z32)',NAMEN,'WRIJ-Z31-7;WRIJ-Z31-8;WRIJ-Z31-9;WRIJ-Z31-10;PER-f6-odile-varenne;PER-f6-machteld;PER-f1-aukje')
nieuw('BESLUIT-Z32-4','Besluit','Mira: bewuste erfnaam (boek 0 en fase 3)',MIRA,'YSA-Z18-9;PER-mira-dochter;WRIJ-Z31-6')
SAS=[(r'\bSaskia\b','Machteld')];ILS=[(r'\bIlse Varenne\b','Odile Varenne'),(r'\bIlse\b','Odile')];SAB=[(r'\bSabe Zoutstem\b','Aukje Zoutstem'),(r'\bSabe\b','Aukje')]
for code in ['VERHAAL-fase6-b','PER-f6-moeder-havra','PER-f6-stalmeester-kobus','PER-f6-tweede-pest-lena','THRL-fase6-builen','PER-f6-bertel','PER-f6-gondelierster-femke','PER-f6-myrrhen-ondalis','THRL-fase6-rivier','VOOR-V4-myrrhen-1','TOESTAND-Z11-PER-f6-tweede-pest-lena-2']:
  vervang(code,code+'-Z32',sub(fs(code),SAS),reden='Naam Saskia -> Machteld (BESLUIT-Z32-3)')
vervang('VERHAAL-fase6-a','VERHAAL-fase6-a-Z32',sub(fs('VERHAAL-fase6-a'),SAS),status='vastgesteld',reden='Naam Saskia -> Machteld; Joris is hoofdpersoon van fase 6 (BESLUIT-Z32-5)')
for code in ['PER-f6-selvara-jong','TOESTAND-Z11-PER-f6-selvara-jong-2','HAAK-genre-balans-V1']:
  vervang(code,code+'-Z32',sub(fs(code),ILS+SAS),reden='Naam Ilse Varenne -> Odile Varenne (BESLUIT-Z32-3)')
vervang('VERHAAL-fase6-c','VERHAAL-fase6-c-Z32',sub(fs('VERHAAL-fase6-c'),ILS),reden='Naam Ilse Varenne -> Odile Varenne (BESLUIT-Z32-3)')
for code in ['PER-f1-sael-ondre','THRL-fase1-zoutverraad']:
  vervang(code,code+'-Z32',sub(fs(code),SAB),reden='Naam Sabe Zoutstem -> Aukje Zoutstem (BESLUIT-Z32-3)')
vervang('PERS-Z4-saelmor-2-1','PERS-Z4-saelmor-2-1-Z32','Verwijzing naar bestaand personage PER-f1-aukje (geen dubbel). Rol in de keten van de Sael-mor: haar lied, in fase 2 Vonk (-150..-40) gezongen door de Sael-mor; zij zelf leefde in fase 1 (ca. -318 tot -288). Kern: Naam: Aukje Zoutstem. Volk: mens. Regio: zoutkust. Rol: zoutopstandeling en zangeres. Haak: zie PER-f1-aukje.',reden='Naam en fasetegenspraak (fase 1 vs fase 2) rechtgezet: zij leefde in fase 1, haar lied in fase 2 (BESLUIT-Z32-3)')
vervang('VOLK-GESCHIEDENIS-OVERZICHT-Z4-saelmor','VOLK-GESCHIEDENIS-OVERZICHT-Z4-saelmor-Z32',fs('VOLK-GESCHIEDENIS-OVERZICHT-Z4-saelmor').replace('Sabe Zoutstem (PERS-Z4-saelmor-2-1)','het lied van Aukje Zoutstem (PERS-Z4-saelmor-2-1-Z32; zij zelf leefde in fase 1)'),reden='BESLUIT-Z32-3')
vervang('TOESTAND-Z11-PERS-Z4-saelmor-2-1-1','TOESTAND-Z32-PERS-Z4-saelmor-2-1-1','Zelfde persoon als PER-f1-aukje; tijdlijn staat daar (TOESTAND-Z32-PER-f1-aukje-*). Rol in deze volkketen: het lied van Aukje Zoutstem, in fase 2 Vonk (-150..-40) gezongen door de Sael-mor; zij zelf leefde in fase 1.',reden='BESLUIT-Z32-3')
vervang('PER-f1-sabe','PER-f1-aukje',PER_AUKJE,status='vastgesteld',onderwerp='Aukje Zoutstem',jaar=-289,reden='Hernoemd (was Sabe Zoutstem) en tijdlijn gelijkgetrokken met Nerys (BESLUIT-Z32-3, -5)')
for n,(j,t) in enumerate([(-318,'Geboren ca. -318 (1 Overvloed), regio zoutkust.'),(-289,'Jaar -289, leeftijd 29, regio zoutkust. Rol: zoutopstandeling en zangeres. Wil: lagere zoutbelasting en haar dochter Imme vrij. Geheim: dat zij de tweede staking verraadde om haar dochter vrij te krijgen. Verandert: dit is het moment waarop de rij speelt.'),(-288,'Historisch: opgehangen ca. -288, na de tweede staking. Leeft voort in haar lied, dat de Sael-mor in fase 2 nog zingen.')],1):
  vervang(f'TOESTAND-Z11-PER-f1-sabe-{n}',f'TOESTAND-Z32-PER-f1-aukje-{n}',t,jaar=j,reden='BESLUIT-Z32-3')
vervang('PER-f1-korvin','PER-f1-korvin-Z32',PER_KORVIN,jaar=-290,reden='Naam Sabe -> Aukje; tijdlijn gelijk met de tweede staking (BESLUIT-Z32-3)')
for n,(j,t) in enumerate([(-320,'Geboren ca. -320 (1 Overvloed), regio zoutkust.'),(-290,'Jaar -290, leeftijd 30, regio zoutkust. Rol: belastinginner. Wil: eerlijk zijn en toch zijn baan houden. Geheim: dat hij Aukje liefhad. Verandert: dit is het moment waarop de rij speelt.'),(-250,'Historisch: overleden ca. -250 in de mijnen (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen.')],1):
  vervang(f'TOESTAND-Z11-PER-f1-korvin-{n}',f'TOESTAND-Z32-PER-f1-korvin-{n}',t,jaar=j,reden='BESLUIT-Z32-3')
vervang('PER-f6-saskia','PER-f6-machteld',PER_MACHTELD,onderwerp='Machteld Stalheelster',reden='Hernoemd (was Saskia; BESLUIT-Z32-3); tweede spil van fase 6 (BESLUIT-Z32-5)')
for n in (1,2,3): vervang(f'TOESTAND-Z11-PER-f6-saskia-{n}',f'TOESTAND-Z32-PER-f6-machteld-{n}',sub(fs(f'TOESTAND-Z11-PER-f6-saskia-{n}'),SAS),reden='BESLUIT-Z32-3')
vervang('PER-f6-ilse-varenne','PER-f6-odile-varenne',PER_ODILE,onderwerp='Odile Varenne',reden='Hernoemd (was Ilse Varenne; BESLUIT-Z32-3)')
for n in (1,2,3): vervang(f'TOESTAND-Z11-PER-f6-ilse-varenne-{n}',f'TOESTAND-Z32-PER-f6-odile-varenne-{n}',fs(f'TOESTAND-Z11-PER-f6-ilse-varenne-{n}'),reden='BESLUIT-Z32-3')
# overige hernoemingen (verwarrend: zelfde tijd)
TES=[(r'\bTessel van Lisk\b','Wietske van Lisk'),(r'\bTessel\b','Wietske')]
vervang('PER-f7-bloednacht-overlever','PER-f7-bloednacht-overlever-Z32',sub(fs('PER-f7-bloednacht-overlever'),TES),onderwerp='Wietske van Lisk',reden='Hernoemd (was Tessel van Lisk; naast Tess Hoeder in 801; BESLUIT-Z32-14)')
for n in (1,2,3): vervang(f'TOESTAND-Z11-PER-f7-bloednacht-overlever-{n}',f'TOESTAND-Z32-PER-f7-bloednacht-overlever-Z32-{n}',sub(fs(f'TOESTAND-Z11-PER-f7-bloednacht-overlever-{n}'),TES),reden='BESLUIT-Z32-14')
RUN=[(r'\bRuna Mijnwerkster\b','Gudrun Mijnwerkster'),(r'\bRuna\b','Gudrun')]
vervang('PER-gew-runa','PER-gew-gudrun',sub(fs('PER-gew-runa'),RUN),onderwerp='Gudrun Mijnwerkster',reden='Hernoemd (was Runa Mijnwerkster; naast Runa Lekmoeder; BESLUIT-Z32-14)')
vervang('DAG-LAAG-mijn','DAG-LAAG-mijn-Z32',sub(fs('DAG-LAAG-mijn'),RUN),reden='Runa -> Gudrun (BESLUIT-Z32-14)')
for n in (1,2,3): vervang(f'TOESTAND-Z11-PER-gew-runa-{n}',f'TOESTAND-Z32-PER-gew-gudrun-{n}',sub(fs(f'TOESTAND-Z11-PER-gew-runa-{n}'),RUN),reden='BESLUIT-Z32-14')
NAD=[(r'\bNadira\b','Dunya')]
vervang('PER-f7-khaled-hofdame','PER-f7-khaled-hofdame-Z32',sub(fs('PER-f7-khaled-hofdame'),NAD),onderwerp='Dunya van het Zonnepaleis',reden='Hernoemd (was Nadira; naast Nadir Een-Vrouw in Qesh; BESLUIT-Z32-14)')
for code in ['VOOR-V4-ishvar-4','INTR-fase7-pact']: vervang(code,code+'-Z32',sub(fs(code),NAD),reden='Nadira -> Dunya (BESLUIT-Z32-14)')
for n in (1,2,3): vervang(f'TOESTAND-Z11-PER-f7-khaled-hofdame-{n}',f'TOESTAND-Z32-PER-f7-khaled-hofdame-Z32-{n}',sub(fs(f'TOESTAND-Z11-PER-f7-khaled-hofdame-{n}'),NAD),reden='BESLUIT-Z32-14')

# ===== 4 mal breken =====
nieuw('BESLUIT-Z32-5','Besluit','Mal gebroken: leeftijd, romance, man als hoofdpersoon, vervalsing als boog',MAL,'VOORSTEL-Z31-mal-1;VOORSTEL-Z31-mal-2;VOORSTEL-Z31-mal-3;VOORSTEL-Z31-mal-4;VOORSTEL-Z31-mal-5;WRIJ-Z31-11;VERHAAL-fase1-Z32;VERHAAL-fase6-Z32;VERHAAL-fase7-Z32')
nieuw('BESLUIT-Z32-6','Besluit','Motorenkaart fase 7 (Annike 61)',MOTOR7,'VERHAAL-fase7-Z32;BESLUIT-Z32-5')
nieuw('BESLUIT-Z32-7','Besluit','Motorenkaart fase 1 (zonder romance)',MOTOR1,'VERHAAL-fase1-Z32;BESLUIT-Z32-5')
nieuw('BESLUIT-Z32-8','Besluit','Motorenkaart fase 6 (Joris, zonder vervalsing)',MOTOR6,'VERHAAL-fase6-Z32;BESLUIT-Z32-5')
vervang('VERHAAL-fase1','VERHAAL-fase1-Z32',VERHAAL1,status='vastgesteld',onderwerp='De zoutstem en de verzwegen zonen (fase 1, ca. -480 tot -220)',reden='Mal gebroken: geen romance als motor (BESLUIT-Z32-5, -7)')
vervang('VERHAAL-fase1-a','VERHAAL-fase1-a-Z32',VERHAAL1A,status='vastgesteld',onderwerp='De dijkvrouw en de schuurheer (partnerschap)',reden='Fase 1 zonder romance (BESLUIT-Z32-5)')
vervang('PER-f1-nerys','PER-f1-nerys-Z32',PER_NERYS,status='vastgesteld',jaar=-289,reden='BESLUIT-Z32-5, -7')
for n,(j,t) in enumerate([(-316,'Geboren ca. -316 (1 Overvloed), regio zoutkust.'),(-289,'Jaar -289, leeftijd 27, regio zoutkust. Rol: zoutwerkster, later Hoofdzuster. Wil: vrouwen een stem geven die niet afhangt van koningen. Geheim: dat zij Aukje aangaf en de verzwegen zonen mee hielp verbergen. Verandert: dit is het moment waarop de rij speelt.'),(-246,'Historisch: overleden ca. -246 (aanname: levensduur 70). Leeft voort in annalen, kraaien of afstammelingen.')],1):
  vervang(f'TOESTAND-Z11-PER-f1-nerys-{n}',f'TOESTAND-Z32-PER-f1-nerys-{n}',t,jaar=j,reden='Tijdlijn fase 1: staking ca. -289 vóór de Oogstnacht en Ardemars dood (-285) (BESLUIT-Z32-5)')
vervang('PER-f1-calden','PER-f1-calden-Z32',PER_CALDEN,status='vastgesteld',jaar=-286,reden='Loyaliteit in plaats van romance (BESLUIT-Z32-5, -7)')
for n,(j,t) in enumerate([(-320,'Geboren ca. -320 (1 Overvloed), regio saelith.'),(-286,'Jaar -286, leeftijd 34, regio saelith. Rol: haremwachter. Wil: één keer zelf iets kiezen. Geheim: dat zijn eigen zoon als doodgeboren in het register staat. Verandert: dit is het moment waarop de rij speelt.'),(-286,'Historisch: valt ca. -286 bij de sluis van Saelith, in de nacht vóór de Oogstnacht. Leeft voort in annalen, kraaien of afstammelingen.')],1):
  vervang(f'TOESTAND-Z11-PER-f1-calden-{n}',f'TOESTAND-Z32-PER-f1-calden-{n}',t,jaar=j,reden='BESLUIT-Z32-5')
vervang('VERHAAL-fase6','VERHAAL-fase6-Z32',VERHAAL6,status='vastgesteld',onderwerp='De melkos van Ambergaard (fase 6, ca. 338 tot 400, met naschok tot 720)',reden='Mal gebroken: Joris hoofdpersoon, geen vervalsing (BESLUIT-Z32-5, -8)')
vervang('PER-f6-joris','PER-f6-joris-Z32',PER_JORIS,status='vastgesteld',reden='Hoofdpersoon fase 6 (BESLUIT-Z32-5)')
vervang('PER-f6-vervalser-meesteres','PER-f6-vervalser-meesteres-Z32',PER_JOKE,reden='Saskia -> Machteld; hoort bij de lijn van fase 7 (BESLUIT-Z32-5)')
vervang('TOESTAND-Z11-PER-f6-vervalser-meesteres-2','TOESTAND-Z11-PER-f6-vervalser-meesteres-2-Z32',sub(fs('TOESTAND-Z11-PER-f6-vervalser-meesteres-2'),SAS),reden='BESLUIT-Z32-3')
v7=fs('VERHAAL-fase7')
for a,b in VERHAAL7_SUBS:
  assert a in v7 or b in v7,a; v7=v7.replace(a,b)
vervang('VERHAAL-fase7','VERHAAL-fase7-Z32',v7,status='vastgesteld',reden='Annike 61 in 776 (BESLUIT-Z32-5, -6)')
vervang('PER-f7-annike','PER-f7-annike-Z32',fs('PER-f7-annike').replace('jaar 750 (geboren ca. 720)','jaar 776 (geboren ca. 715; 61 als ze het blad van Liora maakt)'),status='vastgesteld',jaar=776,reden='BESLUIT-Z32-5')
for n,(j,t) in enumerate([(715,'Geboren ca. 715 (6 Markt, naschok), regio saelith.'),(776,"Jaar 776, leeftijd 61, regio saelith. Rol: merkvervalster. Wil: de levens beschermen die ze vervalste. Geheim: dat zij Liora's register vervalste. Verandert: dit is het moment waarop de rij speelt."),(801,'In 801 leeftijd 86 (als Marit Schrijfster); toestand verder open.')],1):
  vervang(f'TOESTAND-Z11-PER-f7-annike-{n}',f'TOESTAND-Z32-PER-f7-annike-{n}',t,jaar=j,reden='BESLUIT-Z32-5')
vervang('BESLUIT-Z6-WRIJ-100','BESLUIT-Z32-10',fs('BESLUIT-Z6-WRIJ-100').replace('geboren 720, 81 jaar in 801','geboren ca. 715, 86 jaar in 801 (61 in 776; BESLUIT-Z32-5)'),status='vastgesteld',categorie='Besluit')
vervang('PER-gew-marit-Z6','PER-gew-marit-Z6-Z32',fs('PER-gew-marit-Z6').replace('geboren 720','geboren ca. 715, 86 in 801'),reden='BESLUIT-Z32-5, -10')
for n,(j,t) in enumerate([(715,'Geboren ca. 715 (geboortejaar van Annike, BESLUIT-Z32-10), regio zoutkust.'),(801,"Jaar 801, leeftijd 86, regio zoutkust. Rol: marktschrijver. Wil: liefdesbrieven verkopen. Geheim: dat ze Liora's register vervalste. Verandert: dit is het moment waarop de rij speelt."),(801,'In 801 actief, leeftijd 86.')],1):
  vervang(f'TOESTAND-Z11-PER-gew-marit-Z6-{n}',f'TOESTAND-Z32-PER-gew-marit-Z6-{n}',t,jaar=j,reden='BESLUIT-Z32-10')

# ===== 5 Liora =====
nieuw('BESLUIT-Z32-9','Besluit',"Liora's schuld: ze zegt ja namens Teo",LIORA_BESLUIT,'VOORSTEL-Z31-liora-1;WRIJ-Z31-12;PER-liora-profiel-Z32;PER-liora-Z6-Z32;PER-teo-Z32;BESLUIT-2;BESLUIT-15;BESLUIT-Z32-11;LIJN-quest-Z6',handm='Kern')
lp=fs('PER-liora-profiel').replace('Wil: Teo beschermen en de waarheid over de Zegel.','Wil: Teo beschermen en de waarheid over de Zegel, en bij de Wortel komen, ook als ze daarvoor Teo gebruikt (BESLUIT-Z32-9).')
vervang('PER-liora-profiel','PER-liora-profiel-Z32',lp+LIORA_PROF_ADD,status='vastgesteld',handm='Kern',reden="Liora's schuld (BESLUIT-Z32-9); Kern-rij aangepast via besluit")
anker_bron('liora_jaar','PER-liora-profiel-Z32')
lz=fs('PER-liora-Z6').replace('Doel: Teo beschermen en de waarheid achter de zegel vinden.','Doel: Teo beschermen en de waarheid achter de zegel vinden; in het midden van haar boog gebruikt ze hem om bij de Wortel te komen (BESLUIT-Z32-9).')
vervang('PER-liora-Z6','PER-liora-Z6-Z32',lz+LIORA_PROF_ADD,status='vastgesteld',handm='Kern',reden="Liora's schuld (BESLUIT-Z32-9); Kern-rij aangepast via besluit")
vervang('PER-teo','PER-teo-Z32',fs('PER-teo')+TEO_ADD,reden='Teo is 18 en gewijd; lijn strikt niet-seksueel (BESLUIT-Z32-9)')
vervang('BESLUIT-Z1-derdeweg','BESLUIT-Z32-11',fs('BESLUIT-Z1-derdeweg')+DERDEWEG_ADD,status='vastgesteld')

# ===== 6 Thalen =====
nieuw('BESLUIT-Z32-12','Besluit','Thalens patroon in de Rekenaar: zorg tegen zeggenschap',THALEN_BESLUIT,'VOORSTEL-Z31-thalen-1;WRIJ-Z31-13;BESLUIT-Z15-1;BESLUIT-Z15-7;BESLUIT-Z12-wortelstem;WRIJ-080;WRIJ-Z12-1;BESLUIT-Z32-13',handm='Kern')
vervang('BESLUIT-V5-thalen','BESLUIT-Z32-13',V5_THALEN,status='vastgesteld',handm='Kern',reden='Aangescherpt: de machine leest namens het lichaam (BESLUIT-Z32-12)',categorie='Besluit')
for n,(o,t) in enumerate(YSA_BEATS,1): nieuw(f'YSA-Z32-{n}','Verhaal',o,t,'BESLUIT-Z32-12;BESLUIT-Z32-13;ROMAN-Z16-roman-Z32')

# ===== 3b overige naamparen =====
OORDEEL={
 'bewust':{(50,'zelfde personage in twee tijden'),(16,'erfnaam: in de traditie van Iresse (staat in de rij)'),(13,'ambtsnaam: Hoge Moeders nemen de naam van Ithra, stichteres van het Jongenshof'),(14,'ambtsnaam (zie Ithra)'),(18,'ambtsnaam (zie Ithra)'),(8,'erfnaam: de Jongere is naar de Reuzenstier vernoemd'),(22,'dynastie van Qesh: Khaled-Ar sticht, Khaled-Ir regeert'),(3,'Kharvos-erfnaam voor krijgsheren, 540 jaar ertussen'),(19,'erfnaam: herbergiers noemen zonen naar Joris de Melkos, wiens streepjes het teken van de Vaderlingen werden'),(37,'erfnaam: veermannen vernoemen zonen naar Pell Laatste Vonk'),(48,'bewuste echo: de Aelthir noemen hun gezant naar de stem in de Sterrensteen (gevallen -480)'),(49,'erfnaam: de Askoude-beweging is naar Torvald Askoude vernoemd'),(12,'ambtsnaam: Skerra-koeriers dragen de naam Hilt'),(27,'erfnaam: de schismatica neemt de naam van Zuster Mael van de Waarschuwing'),(33,'erfnaam binnen de familie Netwever'),(20,'erfnaam: dijkvrouwen vernoemen dochters naar Tamsin Dijkvrouw')},
 'geen':{(1,''),(2,''),(4,''),(5,''),(6,''),(7,''),(9,''),(11,''),(24,''),(25,''),(26,''),(28,''),(29,''),(30,''),(34,''),(35,''),(36,''),(39,''),(43,''),(44,''),(46,''),(51,''),(52,'')},
 'hernoemd':{(38,'PER-gew-runa -> PER-gew-gudrun (Gudrun Mijnwerkster)'),(40,'PER-gew-runa -> PER-gew-gudrun (Gudrun Mijnwerkster)'),(47,'Tessel van Lisk -> Wietske van Lisk'),(32,'Nadira van het Zonnepaleis -> Dunya van het Zonnepaleis')},
 'twijfel':{(23,'WRIJ-Z32-1'),(45,'WRIJ-Z32-2'),(17,'WRIJ-Z32-3'),(10,'WRIJ-Z32-4'),(21,'WRIJ-Z32-5')}}
for soort,items in OORDEEL.items():
  for i,toel in items:
    if soort=='bewust': upd=('erfnaam/echo (bewust)','bewust (BESLUIT-Z32-14)','BESLUIT-Z32-14','Z32: '+toel)
    elif soort=='geen': upd=('geen botsing','beoordeeld: verschillende tijd of volk, naam verschilt genoeg (BESLUIT-Z32-14)','BESLUIT-Z32-14','Z32: geen verwarring verwacht')
    elif soort=='hernoemd': upd=('botsing','opgelost: hernoemd (BESLUIT-Z32-14)','BESLUIT-Z32-14','Z32: '+toel)
    else: upd=('twijfel','open (twijfel)',toel,'Z32: twijfel, zie '+toel)
    cur=c.execute('select soort,status,wrijving,toelichting from naam_markering where id=?',(i,)).fetchone()
    if cur and tuple(cur)!=upd:
      c.execute('update naam_markering set soort=?,status=?,wrijving=?,toelichting=? where id=?',upd+(i,));S['naam_markering']+=1;wijz(f'NAAM-{i}','beoordeeld','naam_markering',cur[1],upd[1])
MARK={31:('erfnaam/echo (bewust)','bewust (BESLUIT-Z32-4)','BESLUIT-Z32-4','Z32: bewuste erfnaam, zie BESLUIT-Z32-4'),15:('botsing','opgelost: hernoemd (BESLUIT-Z32-3)','BESLUIT-Z32-3','Z32: Ilse Varenne -> Odile Varenne'),42:('botsing','opgelost: hernoemd (BESLUIT-Z32-3)','BESLUIT-Z32-3','Z32: Saskia -> Machteld'),41:('botsing','opgelost: hernoemd (BESLUIT-Z32-3)','BESLUIT-Z32-3','Z32: Sabe Zoutstem -> Aukje Zoutstem')}
for i,upd in MARK.items():
  cur=c.execute('select soort,status,wrijving,toelichting from naam_markering where id=?',(i,)).fetchone()
  if tuple(cur)!=upd: c.execute('update naam_markering set soort=?,status=?,wrijving=?,toelichting=? where id=?',upd+(i,));S['naam_markering']+=1;wijz(f'NAAM-{i}','beoordeeld','naam_markering',cur[1],upd[1])
nieuw('BESLUIT-Z32-14','Besluit','Overige naamechos beoordeeld (WRIJ-Z31-10)','De 48 overige naamparen uit toets.py zijn beoordeeld (naam_markering). Bewust (erfnaam, ambtsnaam, dynastie of dezelfde persoon): 16 paren, met de reden per paar in naam_markering (o.a. Vaelorn in twee tijden, Ithra als ambtsnaam van Hoge Moeders, Khaled-Ar/Khaled-Ir als dynastie, Thalen van de Hoge Bomen als echo van de stem in de Sterrensteen, Jorrit als erfnaam naar Joris de Melkos). Geen botsing (verschillende eeuw of volk, naam verschilt genoeg): 23 paren. Hernoemd omdat ze in dezelfde tijd leven: Runa Mijnwerkster -> Gudrun Mijnwerkster, Tessel van Lisk -> Wietske van Lisk, Nadira van het Zonnepaleis -> Dunya van het Zonnepaleis. Twijfel, vastgelegd als wrijving: Ardemar (WRIJ-Z32-1), Selvara Varenne (WRIJ-Z32-2), Iska/Iskar (WRIJ-Z32-3), Hesk/Heske (WRIJ-Z32-4), Vessa (WRIJ-Z32-5).','WRIJ-Z31-10;BESLUIT-Z32-3')
wrij('WRIJ-Z32-1','Ardemar III en Ardemar de Graanvorst: dezelfde koning?','PER-f1-ardemar-derde; PER-ardemar; GEB-r10-ardemar-val','PER-f1-ardemar-derde (Ardemar III, jaar -270) en PER-ardemar (Ardemar de Graanvorst, koning en wetgever, jaar -180) lijken op elkaar, en Ardemar III sterft volgens GEB-r10-ardemar-val al in -285 (ook in VERHAAL-fase1-Z32). Vraag: is de Graanvorst Ardemar III (dan moet zijn jaar naar vóór -285) of een latere Ardemar (dan een rangnummer geven)? Ook het jaar -270 in PER-f1-ardemar-derde botst met zijn dood in -285.','PER-f1-ardemar-derde;PER-ardemar;GEB-r10-ardemar-val')
wrij('WRIJ-Z32-2','Selvara Varenne en Selvara Varenne de Jongere','PER-selvara; PER-f6-selvara-jong-Z32','"De Jongere" (jaar 375, geboren ca. 345, nicht van Odile) heet voorloopster van Selvara Varenne (stichteres van de Zaadbeurs, 455). In 455 zou de Jongere 110 zijn: dus twee vrouwen, maar welke is "de oudere"? Voorstel: de stichteres van 455 is een achternicht die naar haar vernoemd is (erfnaam), en "de Jongere" heet dan gewoon Selvara Varenne (de eerste).','PER-selvara;PER-f6-selvara-jong-Z32')
wrij('WRIJ-Z32-3','Iska Spiegelhuid en Iskar Spiegelvader (Ves-Lethi)','PER-barsten-veslethi-Z6; PER-f7-veslethi-nara-oud','Beide Ves-Lethi in fase 7 (780 en 770), en Ves-Lethi wisselen van geslachtsfase. Mogelijk dezelfde persoon in twee fasen, mogelijk twee. Beslissen: zelfde persoon (dan markeren) of hernoemen.','PER-barsten-veslethi-Z6;PER-f7-veslethi-nara-oud')
wrij('WRIJ-Z32-4','Hesk van Hal-Neth en Heske Halfgezicht','PER-hesk-kweker; PER-f4-grauwe-heske; VRAAG-067','Hesk van Hal-Neth (uitvinder van de Biotechniek, haar kweekstam veroorzaakte de Pest, VRAAG-067) en Heske Halfgezicht (een van de eerste Grauwen, fase 4, jaar 45). Mogelijk een bewuste lijn (Heske als stammoeder, Hesk als naamdraagster), mogelijk toeval. Beslissen.','PER-hesk-kweker;PER-f4-grauwe-heske')
wrij('WRIJ-Z32-5','Twee schurken die Vessa heten','PER-saelmor-schurk-vessa; PER-sch-vessa','Kapitein Vessa (schurk van de Sael-mor, fase 6) en Moeder Vessa (hoofd van de Stille Hand, 801). Twee schurken met dezelfde naam kunnen verwarren, maar kunnen ook een bewuste lijn zijn (de Stille Hand neemt de naam van een gevreesde kapitein). Beslissen: erfnaam markeren of de kapitein hernoemen.','PER-saelmor-schurk-vessa;PER-sch-vessa')
wrij('WRIJ-Z32-6','Nadir Een-Vrouw: fase 5 of 801?','PERS-Z4-ishvar-5-1; PER-ishvar-nadir','PERS-Z4-ishvar-5-1 zet Nadir Een-Vrouw in fase 5 Ontvangst (130..340), maar PER-ishvar-nadir zegt jaar 801. Dezelfde soort fasetegenspraak als bij Sabe Zoutstem. Niet zelf opgelost, omdat niet duidelijk is welke kant klopt.','PERS-Z4-ishvar-5-1;PER-ishvar-nadir',typ='tijdlijn')

# ===== 7 sluiten =====
for code,door in [('WRIJ-Z31-1','link BESLUIT-Z25-2 -> BESLUIT-Z24-8 hersteld'),('WRIJ-Z31-2','YSA-Z15-1 en YSA-Z16-11 vervangen door BESLUIT-Z18-3; PER-v4-thalen-orr -> PER-v4-thalen-orr-Z32'),('WRIJ-Z31-3','BESLUIT-Z32-1, BESLUIT-Z32-2 (7.546)'),('WRIJ-Z31-4','ROMAN-Z16-roman-Z32 (ca. 54.400)'),('WRIJ-Z31-5','SYS-wijding-Z32'),('WRIJ-Z31-6','BESLUIT-Z32-4'),('WRIJ-Z31-7','BESLUIT-Z32-3 (Odile Varenne)'),('WRIJ-Z31-8','BESLUIT-Z32-3 (Machteld)'),('WRIJ-Z31-9','BESLUIT-Z32-3 (Aukje Zoutstem, fase 1)'),('WRIJ-Z31-10','BESLUIT-Z32-14; twijfels in WRIJ-Z32-1..5'),('WRIJ-Z31-11','BESLUIT-Z32-5..8'),('WRIJ-Z31-12','BESLUIT-Z32-9'),('WRIJ-Z31-13','BESLUIT-Z32-12, BESLUIT-Z32-13'),('WRIJ-Z19-1','BESLUIT-Z32-3 (Sabe Zoutstem hernoemd tot Aukje Zoutstem)')]: sluit(code,door)
vraag('VRAAG-Z31-1','Alles overgenomen (Rogier, 2026-10-31): BESLUIT-Z32-5 (mal), -6, -7, -8 (motorenkaarten), VERHAAL-fase1-Z32, VERHAAL-fase6-Z32, VERHAAL-fase7-Z32.')
vraag('VRAAG-Z31-2',"Ja (Rogier, 2026-10-31): BESLUIT-Z32-9; Kern-rijen PER-liora-profiel-Z32 en PER-liora-Z6-Z32.")
vraag('VRAAG-Z31-3','Ja, als Thalens patroon in de Rekenaar (Rogier, 2026-10-31): BESLUIT-Z32-12, BESLUIT-Z32-13, YSA-Z32-1..6.')
vraag('VRAAG-Z31-4','Ja (Rogier, 2026-10-31): Mira bewuste erfnaam (BESLUIT-Z32-4); Odile Varenne, Machteld, Aukje Zoutstem (BESLUIT-Z32-3); overige paren BESLUIT-Z32-14.')
for v,b in [('VOORSTEL-Z31-mal-1','BESLUIT-Z32-5'),('VOORSTEL-Z31-mal-2','BESLUIT-Z32-5'),('VOORSTEL-Z31-mal-3','BESLUIT-Z32-5'),('VOORSTEL-Z31-mal-4','BESLUIT-Z32-5'),('VOORSTEL-Z31-mal-5','BESLUIT-Z32-5'),('VOORSTEL-Z31-liora-1','BESLUIT-Z32-9'),('VOORSTEL-Z31-thalen-1','BESLUIT-Z32-12')]: markeer(v,b)
# toets_uitzonderingen die nu opgelost zijn: alleen markeren (niet verwijderen)
for t_,code in c.execute("select toets,code from toets_uitzondering where code in ('SYS-wijding','YSA-Z15-1','YSA-Z16-11','PER-v4-thalen-orr','BESLUIT-Z16-9','BESLUIT-Z24-8','ROMAN-Z16-roman','BESLUIT-Z25-2')").fetchall():
  c.execute("update toets_uitzondering set reden=reden||' [Z32: opgelost; rij vervangen of link hersteld]' where toets=? and code=? and reden not like '%[Z32:%'",(t_,code))
if not c.execute("select 1 from logboek where wat like 'Ronde Z32: %'").fetchone():
  c.execute("insert into logboek(datum,wat) values(?,?)",(DT,'Ronde Z32: Z31-voorstellen vastgesteld (Rogier: alles zoals aanbevolen). SYS-wijding-Z32; Thalen/overlevenden/woordenaantal/dode link hersteld; namen Odile Varenne, Machteld, Aukje Zoutstem, Gudrun, Wietske, Dunya; Mira erfnaam; mal gebroken (fase 1 zonder romance, fase 6 Joris zonder vervalsing, Annike 61); Liora zegt ja namens Teo; Thalens patroon in de Rekenaar. BESLUIT-Z32-1..14, YSA-Z32-1..6, WRIJ-Z32-1..6. Niets verwijderd; roman niet aangeraakt.'))
c.commit();afgeleid.bouw(c);c.commit()
S['draagkracht']=dict(c.execute('select draagkracht,count(*) from canon group by 1').fetchall());S['totaal']=c.execute('select count(*) from canon').fetchone()[0]
json.dump(S,open('z32/stats.json','w'),ensure_ascii=False,indent=1);print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in S.items()},ensure_ascii=False))
