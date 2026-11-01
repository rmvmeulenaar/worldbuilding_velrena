# Afsluiting gatenrondes: genre-balans (idempotent)
from gaten_lib import Ronde,GR
R=Ronde(4)
R.add('HAAK-genre-balans','Verhaal','Genre-balans van de canon (na G1-G4)',
"Romance: sterkst in personages (Liora-Aeron-as-Sef, Bram-Dagny, Bor-Lunn, Ysara-Mira) en volksseksualiteit; dunst in de huizen en de Orde-top (geen liefdeslijnen voor Ithrael, Selvine, Brannoch) en in Kharvos. "
"Intrige: sterkst in Saelith (opvolging, Stille Hand), Orde-schuld bij Varenne, Drask-Morvane-pact; dunst in Groenmuil en de Stille Zusterschappen, en in kleinere huizen (bestaan nog niet). "
"Erotiek: sterkst (bijna te zwaar) in rituelen, voorkeuren, volken en lichaam; dunst in gewone, vertrouwde erotiek van alledag (herberg, moederhuis, verliefdheid zonder ritueel): daar moet de lezer binnenkomen. "
"Thriller: sterkst in 801 (klokken: Teo, Zegelbinding, Drask, Orde-valuta) en plekken (Zoutkelders, Ves-Anath); dunst in de historische fasen 1-4, die vooral kroniek zijn. "
"Escapisme: sterkst in steden, kaart, feesten en dagelijks leven (nieuw); dunst in zintuiglijke details van de Rosse, de Stille eilanden en Kharvos-steden, en in natuur, dieren en landschap buiten de regio-overzichten. "
"Dosering: het vreemde (Korf, Veenhallen, Vleesgemeente, Lijngravers) is nu overtal tegenover het vertrouwde; volgende rondes moeten vertrouwd-menselijk materiaal toevoegen."+GR,
'genre-balans','HAAK-PER-romance;HAAK-PER-intrige;HAAK-PER-erotiek;HAAK-PER-thriller;HAAK-G3-overzicht;HAAK-G4-overzicht')
R.log('afsluiting: plotbaar wrijvingenoverzicht per thema in bijbel/90_WRIJVINGEN, genre-balans (HAAK-genre-balans).')
R.klaar()
