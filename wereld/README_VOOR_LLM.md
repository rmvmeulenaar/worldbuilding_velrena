# README voor een LLM · wereld Velmara

**Bron van waarheid (sinds de repo, Z41):** de tekst in `canon_tekst/`; `canon.db` (SQLite) wordt daaruit gebouwd met `python3 velmara.py bouw`. Alles in `bijbel/` en `canon.md` wordt uit canon.db gegenereerd; bewerk die bestanden en canon_tekst/ nooit met de hand. Zie `../CLAUDE.md`.

**Leesvolgorde:** `bijbel/00_WERELDKERN.md` → `01_INDEX.md` → het domeinbestand dat je nodig hebt → `90_WRIJVINGEN.md` → `91_OPEN_VRAGEN.md`.
Voor één scène: `python3 scene.py PER-liora RIT-ontvangst REG-saelith` → `scene_pakket.md`.

**Details toevoegen:** maak eerst een back-up van canon.db. Doe een INSERT in `canon` met categorie, onderwerp, feit, status (`voorlopig`), reden, hangt_samen_met, ronde, een nieuwe unieke `code` volgens de conventie in 01_INDEX en `verwijst_naar` (codes gescheiden door `;`). Draai daarna `python3 genereer.py` (en eventueel `python3 export.py` voor canon.md).

**Consistentie:** lees eerst de wereldkern; spreek de grondregels niet tegen; zoek in 90_WRIJVINGEN of iets al botst; voeg nieuwe botsingen toe als wrijving (`WRIJ-nnn`). Alle seksuele deelnemers zijn 18+.

**Niet draaien:** `bouw.py` (wist de database), `ronde3.py`, `r6.py` en `r7.py` (die voegen alles dubbel toe). `canon.md` is vervangen door `bijbel/` en is alleen nog een export.

**Eén bestand:** `genereer.py` maakt ook `WERELD_VELMARA.md`, met de hele wereld in één zelfstandig bestand. Terugladen kan met `python3 importeer.py WERELD_VELMARA.md nieuw.db`.
