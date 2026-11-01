#!/usr/bin/env python3
"""Dekkingskaart: per categorie en per regio aantal onderdelen en gemiddelde tekenlengte (detailgraad). Dunste eerst."""
import sqlite3,os
c=sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),'canon.db'))
print('PER CATEGORIE (dunste gemiddelde eerst)')
for k,n,g in c.execute('select categorie,count(*),avg(length(feit)) from canon group by categorie order by avg(length(feit))'):
  print(f'  {k:24} {n:4} onderdelen  gem. {int(g):5} tekens')
print('\nPER REGIO (onderdelen die naar de regio verwijzen)')
for code,naam,eig in c.execute("select code,onderwerp,length(feit) from canon where code like 'REG-%' and code!='REG-overzicht'").fetchall():
  n,g=c.execute("select count(*),coalesce(avg(length(feit)),0) from canon where (';'||verwijst_naar||';') like ?",('%;'+code+';%',)).fetchone()
  print(f'  {code:16} {n:4} verwijzingen  gem. {int(g):5} tekens  (eigen tekst {eig})')
