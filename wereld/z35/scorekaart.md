# Scorekaart ronde Z35 (canon-motor), gemeten op 2026-11-01

Gemeten met z33/meet.py en z34/meet.py (nul: z35/nul_z33.json; na: z35/na_z33.json, z35/na_z34.json).

## Klaar-als criteria
| criterium | doel | voor | na | gehaald |
|---|---|---|---|---|
| sjabloonaandeel buiten de ideeënbank | <35% | 61,0% | 47,1% | nee |
| v_actief rijen met "Wil: -", "Geheim: -", "regio onbekend" of "aanname: levensduur" | 0 | 610 | 0 | ja |
| herkomst Structuur (streng: besluit/roman/auteur) | ≥70% | 35,7% (1514/4243) | 54,4% (1566/2880) | nee |
| herkomst Structuur inclusief opdrachtspoor (bron_spoor) | (alleen spoor) | – | 73,4% (2115/2880) | telt niet als bron |
| rijmregels groen of open wrijving | alle | – | assen, erfenis, spiraal groen; binnen_fase 1 open (WRIJ-Z35-1) | ja |
| synopsen met labels | 0 | 28 | 0 | ja |
| zaadjes uit fasebogen | ≥26 | 17 | 26 | ja |
| toets.py exit 0 na elke stap | ja | ja | ja (6 keer) | ja |
| roundtrip | 0 verschillen | 0 (Z34) | 0, 26 tabellen | ja |
| tweede run voegt niets toe | ja | – | "klaar {}" | ja |
| terugdraaitest backup_Z35 + r_Z35 | 0 | – | 0 verschillen in alle tabellen | ja |
| roman md5 gelijk | ja | – | ja | ja |

## 8 canon-motor metingen
| meting | voor | na |
|---|---|---|
| 1 veranderproef (Thalen -1198) | 11 plekken, toets vindt 7 | 11 plekken, toets vindt 7 (ongewijzigd) |
| 2 duplicatie: letterlijke kopieën | 980 | 739 |
| 2 near-dup paren (z34) | 55164 | 4871 |
| 3 dode links | 0 | 0 |
| 4 herkomst Kern | 93,5% | 93,5% (6 Kern zonder bron, WRIJ-Z33-7) |
| 5 tests | 26 controles, 185 bekend, 0 nieuw | 30 controles, 186 bekend, 0 nieuw |
| 6 roundtrip | 0 | 0 (nu met personage_toestand, levensduur, fase_rijm, kernscene, keuze en 9 boog-kolommen) |
| 7 terugdraaien | werkt | werkt (Z34→Z35, 0 verschillen) |
| 8 koude lezer | 10/10 | 10/10 |

Let op: "levend" daalt van 6437 naar 5074 omdat 1377 TOESTAND-rijen naar personage_toestand gingen (status 'voorlopig, vervangen'; niets verwijderd).
Geur: status_met_twee_betekenissen stijgt van 479 naar 1884 door die vervangen-rijen.
