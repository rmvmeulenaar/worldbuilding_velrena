# Velmara

De canon van de wereld Velmara, de wereld van *The Body Is the Price* (Iris Calloway), opgebouwd als een database die steeds rijker wordt en zichzelf toetst.

## Wat hier staat
- **De wereld als tekst** in `wereld/canon_tekst/`: alle rijen van de canon, per hoofdstuk. Dit is de bron.
- **De machine** in `wereld/`: scripts die de database bouwen, toetsen, simuleren en verhalen laten ontstaan.
- **De knopenkaart**: draai `python3 wereld/velmara.py kaart` en open `wereld/kaart/knopenkaart.html`. Je ziet alle verhaallijnen per fase en de knopen waaraan ze hangen: personages, plekken, gebeurtenissen.

## Snel beginnen
```
cd wereld
python3 velmara.py bouw     # bouw canon.db uit de tekst en toets
python3 velmara.py kaart    # maak de knopenkaart
```

Regels voor wie eraan werkt, mens of LLM: zie `CLAUDE.md`.

Privé. Bevat expliciete inhoud voor volwassenen.
