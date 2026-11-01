# Ronde Z39: wat er gedaan is

- Opdracht: OPDRACHT_architect_Z39.md (besluiten + aanscherping) en opdracht_Z35.md stap 11 (11a–11d), toegepast op fase 4 Noodtoestand.
- Script: r_Z39.py. Stappen: a, sim, tech, f5, prem, proef, keuze. Het script is idempotent; de database kies je met `DB=pad`.
- Code:
  - z39/sim.py
  - z39/montecarlo.py
  - z39/tech.py
  - z39/intrige.py
  - z39/premisses.py
  - z39/nieuwheid.py
  - z39/koude_lezer.py
- Uitvoer:
  - z39/mc_fase4.json
  - z39/proef_informatie.json
  - z39/tech_rapport.json
  - z39/fase5.json
  - z39/demo/ (top5.md, intrigevoorstellen.md, intrige_graaf.txt, run_rapport.md)
- Rapporten: scorekaart_Z39.md, keuzelijst_Z39.md en wijzigingen_Z39.md.
