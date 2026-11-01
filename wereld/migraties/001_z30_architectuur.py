"""Migratie 001 (ronde Z30): draagkracht/ideeenbank/veilig_*/vervangen_door/feit_schoon, tabellen veiligheid_varianten, verwijzing, historie, handleiding, indexen, views.
Structuur staat in afgeleid.schema(); deze migratie roept die aan (idempotent)."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import afgeleid
VERSIE=1;NAAM='z30_architectuur'
def migreer(c): afgeleid.schema(c)
