"""Migratie 005 (ronde Z35, rijm en opschoning). Idempotent, additief.
Model (nieuw): personage_toestand (stap 1), levensduur (ankertabel levensduur per volk), fase_rijm (stap 2), kernscene (stap 3), keuze (stap 6).
boog: extra kolommen voor de rijm-assen en het weggehaalde formulier (herkenbaar, zintuig, haak, synopsis_code).
Views: v_personage_tijdlijn, v_rijm, v_schrijfpakket. Triggers: nooit verwijderen uit de nieuwe tabellen."""
VERSIE=5;NAAM='z35_rijm'
def migreer(c):
  c.executescript("""
create table if not exists personage_toestand(id integer primary key,per_code text not null,jaar integer,leeftijd integer,rol text,regio text,wil text,geheim text,verandert text,aanname integer not null default 0 check(aanname in(0,1)),aanname_reden text,bron text unique,soort text,volk text,toestand text,maan text,rest text,status_oud text);
create table if not exists levensduur(id integer primary key,volk text unique,jaren integer,soort text check(soort in('canon','aanname','onbekend')),bron text,toelichting text);
create table if not exists fase_rijm(id integer primary key,fase text unique,volgorde integer,mechanisme text,beslisser text,beslisser_as text,betaler text,betaler_as text,vervalst text,vervalst_as text,ontdekt text,ontdekt_as text check(ontdekt_as in('ja','nee','deels','n.v.t.')),schaal text check(schaal in('dorp','rijk','wereld')),erft_van text,blijvende_verandering text,bron text,status text,voorstel text);
create table if not exists kernscene(id integer primary key,boog_code text,volgorde integer,scene text,bron text,unique(boog_code,volgorde));
create table if not exists keuze(id integer primary key,code text unique,soort text,onderwerp text,aanbeveling text,raakt text,impact integer,draagkracht text,status text,bron text);
create index if not exists ix_pt_per on personage_toestand(per_code);
""")
  for t in ('personage_toestand','levensduur','fase_rijm','kernscene','keuze'):
    c.execute(f"create trigger if not exists t_{t}_geen_delete before delete on {t} begin select raise(abort,'{t}: nooit verwijderen'); end")
  cols=[r[1] for r in c.execute('pragma table_info(boog)')]
  for k in ('beslisser_as','betaler_as','vervalst_as','ontdekt_as','schaal','herkenbaar','zintuig','haak','synopsis_code'):
    if k not in cols: c.execute(f'alter table boog add column {k} text')
  c.executescript("""
drop view if exists v_personage_tijdlijn;
create view v_personage_tijdlijn as
select t.per_code,t.jaar,t.leeftijd,t.soort,t.rol,t.regio,t.wil,t.geheim,coalesce(t.verandert,t.toestand) as verandert,t.aanname,t.aanname_reden,t.bron
 from personage_toestand t where t.soort not in('overleden (aanname)','samengevoegd')
union all
select g.per_code,
 case when s.jaar is not null then s.jaar when l.volk is not null then g.jaar+l.jaren else g.jaar+d.jaren end,
 case when s.jaar is not null then s.jaar-g.jaar when l.volk is not null then l.jaren else d.jaren end,
 'overleden',null,null,null,null,null,
 case when s.jaar is not null and g.aanname=0 then 0 else 1 end,
 case when s.jaar is not null then 'sterfjaar uit de canon (relatie sterft_in)'||case when g.aanname=1 then '; geboortejaar is een aanname' else '' end
      when l.volk is not null and l.jaren is null then 'sterfjaar onbekend: levensduur van '||l.volk||' staat niet in de canon ('||coalesce(l.bron,'-')||')'
      else 'berekend: geboren '||g.jaar||' + levensduur '||coalesce(l.jaren,d.jaren)||' ('||coalesce(l.volk,'standaard')||', '||coalesce(l.soort,d.soort)||', tabel levensduur)' end,
 'v_personage_tijdlijn'
 from personage_toestand g
 left join levensduur l on l.volk=g.volk
 left join levensduur d on d.volk='*'
 left join (select van_code,min(cast(substr(naar_code,6) as integer)) as jaar from relatie where soort='sterft_in' group by van_code) s on s.van_code=g.per_code
 where g.soort='geboren' and not exists(select 1 from personage_toestand o where o.per_code=g.per_code and o.soort='overleden');
drop view if exists v_rijm;
create view v_rijm as
select r.volgorde,r.fase,r.mechanisme,r.beslisser,r.betaler,r.vervalst,r.ontdekt,r.schaal,r.erft_van,r.blijvende_verandering,r.status,
 (select count(*) from boog b where b.fase=r.fase) as bogen,
 (select group_concat(b.code,', ') from boog b where b.fase=r.fase) as boog_codes,
 r.voorstel
 from fase_rijm r order by r.volgorde;
drop view if exists v_schrijfpakket;
create view v_schrijfpakket as
select b.code as boog_code,1 as stap,'boog (vorm)' as onderdeel,b.code as code,
 'vorm: '||coalesce(b.vorm,'-')||' | verteller: '||coalesce(b.verteller,'-')||' | tempo: '||coalesce(b.tempo,'-')||' | toon: '||coalesce(b.toon,'-')||' | afloop: '||coalesce(b.afloop,'-')||' | hoofdpersoon: '||coalesce(b.hoofdpersoon,'-')||' ('||coalesce(b.leeftijd_hoofdpersoon,'?')||', '||coalesce(b.geslacht_hoofdpersoon,'?')||') | herkenbaar: '||coalesce(b.herkenbaar,'-') as tekst from boog b
union all select b.code,2,'rijm (fase)',r.fase,'mechanisme: '||coalesce(r.mechanisme,'-')||' | beslisser: '||coalesce(r.beslisser,'-')||' | betaler: '||coalesce(r.betaler,'-')||' | vervalst: '||coalesce(r.vervalst,'-')||' | ontdekt: '||coalesce(r.ontdekt,'-')||' | schaal: '||coalesce(r.schaal,'-')||' | blijvend: '||coalesce(r.blijvende_verandering,'-')||' ['||coalesce(r.status,'-')||']' from boog b join fase_rijm r on r.fase=b.fase
union all select b.code,3,'rijm (deze boog)',b.code,'beslisser: '||coalesce(b.beslisser_as,'-')||' | betaler: '||coalesce(b.betaler_as,'-')||' | vervalst: '||coalesce(b.vervalst_as,'-')||' | ontdekt: '||coalesce(b.ontdekt_as,'-')||' | schaal: '||coalesce(b.schaal,'-') from boog b
union all select b.code,4,'erfenis (ERF)',e.code,e.feit_schoon from boog b join fase_rijm r on r.fase=b.fase join canon e on e.code like 'ERF-%' and instr(';'||replace(r.erft_van,' ','')||';',';'||e.code||';')>0
union all select b.code,5,'synopsis (geen schrijfinstructie)',s.code,s.feit_schoon from boog b join canon s on s.code=b.synopsis_code
union all select b.code,6,'kernscene',b.code||'#'||k.volgorde,k.scene from boog b join kernscene k on k.boog_code=b.code
union all select b.code,7,'personage (eigen fout)',p.code,p.naam||': '||coalesce(p.soort_fout,'-')||' | '||coalesce(p.eigen_fout,'-')||' | wie betaalt: '||coalesce(p.wie_betaalt,'-')||' | zelfbedrog: '||coalesce(p.zelfbedrog,'-') from boog b join personage p on p.fase=substr(b.fase,1,instr(b.fase||' ',' ')-1) and (instr(b.hoofdpersoon,substr(p.naam,1,instr(p.naam||' ',' ')-1))>0 or exists(select 1 from verwijzing v where v.van_code=b.synopsis_code and v.naar_code=p.per_code))
union all select b.code,8,'zaadje (open)',z.code,z.wat||' | oogst: '||coalesce(z.oogst_in,'-')||' | '||z.status from boog b join zaadje z on (z.geplant_in=b.code or z.geplant_in=b.synopsis_code) and z.status like 'open%'
union all select b.code,9,'Kern (mag niet breken)',k.code,k.feit from boog b join v_kern k on k.code in('REGEL-harde-grenzen','BESLUIT-Z30-4','EROS-GRENZEN-Z7') or exists(select 1 from verwijzing v where v.van_code=b.synopsis_code and v.naar_code=k.code) or instr(';'||replace(coalesce(b.bron,''),' ','')||';',';'||k.code||';')>0;
""")
