#!/usr/bin/env python3
"""Koude lezer (mechanisch): krijgt ALLEEN v_kern (+ v_anker als die bestaat) en handleiding.
Per vraag: zoek de rij met de meeste trefwoorden (zonder het antwoord te kennen), antwoord = die rij; nagekeken tegen het verwachte antwoord.
Dit is een vindbaarheidsproef, geen LLM-lezer."""
import sqlite3,sys,json,re
c=sqlite3.connect(sys.argv[1] if len(sys.argv)>1 else 'canon.db')
V={r[0] for r in c.execute("select name from sqlite_master where type='view'")}
docs=[('kern:'+a,(b or '')+' '+(d or '')) for a,b,d in c.execute('select code,onderwerp,feit from v_kern')]
docs+=[('handl:'+a,(b or '')+' '+(d or '')) for a,b,d in c.execute('select code,onderwerp,tekst from handleiding')]
if 'v_anker' in V: docs+=[('anker:'+a,f'{a} {t or ""} {w}') for a,w,t in c.execute('select sleutel,waarde,toelichting from v_anker')]
Q=[('In welk jaar sterft Thalen Orr?',['thalen','sterft','sterfjaar','stierf'],'-1198'),
('In welk jaar sterft Ysa Maren?',['ysa','sterft','sterfjaar','stierf'],'-1209'),
('Hoeveel Makers overleven de Muiterij?',['overlevenden','muiterij','overleven'],'7.546'),
('Hoeveel mensen waren aan boord van het zaaischip?',['aan boord','aan_boord','zaaischip','kolonisten'],'11.000'),
('Hoeveel vrouwen per man laat het Zegel over (noodstand)?',['noodstand','1 op','zegel','verhouding'],'100'),
('Wie activeert het Zegel in jaar 0?',['activeert','jaar 0','zegel','activatie','zegel_activatie'],'Raad der Moeders'),
('Wat is de minimumleeftijd voor iedere seksuele rol?',['harde','lijnen','volwassenen','seksuele','grens'],'18'),
('Hoeveel hoofdstukken heeft de roman over Ysa?',['hoofdstukken','roman','roman_hoofdstukken'],'33'),
('In welk jaar speelt het verhaal van Liora?',['liora','jaar','liora_jaar','speelt'],'801'),
('Geldt de harde grens ook als veilig_18plus = 0?',['veilig_18plus','grens','vlag'],'NOOIT')]
goed=0;det=[]
for v,kw,a in Q:
  best=max(docs,key=lambda d:(sum(k.lower() in d[1].lower() for k in kw),-len(d[1])))
  ok=a.lower() in best[1].lower();goed+=ok;det.append({'vraag':v,'gekozen':best[0],'goed':ok})
print(json.dumps({'score':f'{goed}/10','goed':goed,'detail':det},ensure_ascii=False))
