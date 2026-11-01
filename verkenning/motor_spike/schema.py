"""De schema's van de Velmara-motor: de ENIGE definitie van de vorm van de wereld.

Alles wat de motor kent, is een van deze vormen. Opslag, LLM-uitvoer, tests en documentatie lezen hieruit.
Wereldtijd is in Zegeljaren (negatief = vóór het Zegel; 801 = het heden van boek 1).
"""
from __future__ import annotations
from enum import Enum
from typing import Literal, Union, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
import hashlib, json

Waarde = Union[str, int, float, bool, None]
SEIZOENEN = ('lente', 'zomer', 'herfst', 'winter')


class Epistemiek(str, Enum):
    """Hoe zeker een feit is. Alleen 'feit' uit de canon is canon; de rest is voorstel tot Rogier beslist."""
    feit = 'feit'                 # canon (besluit, roman, bijbel)
    aanname = 'aanname'           # afgeleid of verondersteld door de architect
    simulatie = 'simulatie'       # uit een simulatierun (run-id + seed)
    voorstel = 'voorstel'         # bedacht door verteller of architect, nog niet besloten
    spel = 'spel'                 # ontstaan tijdens spelen of regisseren op een tak


class Bron(BaseModel):
    model_config = ConfigDict(frozen=True)
    soort: Literal['canon', 'simulatie', 'speler', 'verteller', 'oproep', 'afleiding', 'systeem']
    code: Optional[str] = None    # canoncode, run-id, of tak
    detail: Optional[str] = None


class Feit(BaseModel):
    """Eén uitspraak over de wereld: onderwerp-predicaat-object, geldig van..tot (wereldtijd, inclusief)."""
    model_config = ConfigDict(frozen=True)
    onderwerp: str
    predicaat: str
    object: Waarde
    van: Optional[int] = None
    tot: Optional[int] = None
    bron: Bron
    epistemiek: Epistemiek = Epistemiek.feit
    kern: bool = False            # Kern: alleen via BESLUIT van Rogier te veranderen

    def geldig_op(self, jaar: Optional[int]) -> bool:
        if jaar is None: return True
        return (self.van is None or self.van <= jaar) and (self.tot is None or jaar <= self.tot)

    def sleutel(self) -> tuple:
        return (self.onderwerp, self.predicaat, self.object, self.van, self.tot)


class Soort(str, Enum):
    persoon = 'persoon'; plek = 'plek'; volk = 'volk'; huis = 'huis'; ding = 'ding'; dier = 'dier'
    gebeurtenis = 'gebeurtenis'; geheim = 'geheim'; canonrij = 'canonrij'; fase = 'fase'


class Predicaat(BaseModel):
    """Register van toegestane predicaten. Een voorstel met een onbekend predicaat wordt geweigerd."""
    model_config = ConfigDict(frozen=True)
    naam: str
    onderwerp: tuple[str, ...]            # toegestane Soort-waarden van het onderwerp
    object: str                           # 'entiteit:<soort>' | 'tekst' | 'getal' | 'jaar' | 'waar'
    functioneel: bool = False             # hooguit één geldige waarde tegelijk (bv. sterft, regio)
    omschrijving: str = ''


class Moment(BaseModel):
    model_config = ConfigDict(frozen=True)
    jaar: int
    seizoen: Optional[Literal['lente', 'zomer', 'herfst', 'winter']] = None
    plek: Optional[str] = None


class Deelnemer(BaseModel):
    model_config = ConfigDict(frozen=True)
    entiteit: str
    rol: str                              # 'actor', 'doel', 'getuige', 'partner', ...
    instemming: Optional[bool] = None     # verplicht ingevuld bij seksuele handelingen


class FeitWijziging(BaseModel):
    model_config = ConfigDict(frozen=True)
    actie: Literal['stel', 'beeindig']
    feit: Feit


# ---------- Regels: proza naast formule (Rules as Code, zoals Catala) ----------
class Formule(BaseModel):
    """Kleine logische taal. Variabelen beginnen met '?'. Wordt geëvalueerd tegen de feiten op het moment van het voorstel.
    Precies één veld is gevuld:
      feit:  [onderwerp, predicaat, object]  (patroon; variabelen toegestaan)
      niet:  Formule
      alle:  [Formule, ...]   (en)
      een:   [Formule, ...]   (of)
      cmp:   [operator, a, b] met operator in < <= > >= == !=
    """
    feit: Optional[list[Any]] = None
    niet: Optional['Formule'] = None
    alle: Optional[list['Formule']] = None
    een: Optional[list['Formule']] = None
    cmp: Optional[list[Any]] = None

    @field_validator('cmp')
    @classmethod
    def _op(cls, v):
        if v is not None and (len(v) != 3 or v[0] not in ('<', '<=', '>', '>=', '==', '!=')):
            raise ValueError('cmp is [operator, a, b]')
        return v


class Regel(BaseModel):
    """Een regel van de wereld in drie delen: de zin (voor Rogier), de formule (voor de machine), de canoncode (de bron)."""
    model_config = ConfigDict(frozen=True)
    code: str
    zin: str
    soort: Literal['verbod', 'vereiste']  # verbod: formule mag niet waar zijn; vereiste: formule moet waar zijn
    formule: Optional[Formule] = None     # None = ingebouwde controle (zie ingebouwd)
    ingebouwd: Optional[str] = None       # naam van een controle in poort.py, voor wat de formuletaal (nog) niet kan
    canon_code: Optional[str] = None
    harde_lijn: bool = False
    categorie: str = 'algemeen'           # hardelijn | tijd | plaats | kennis | kern | hoofdlijn | referentie | handeling


class Handeling(BaseModel):
    """Iets wat een persoon kan doen. Voorwaarden en gevolgen als gegevens (zoals Story2Game en Crusader Kings-storylets)."""
    model_config = ConfigDict(frozen=True)
    code: str
    naam: str
    rollen: tuple[str, ...] = ('actor',)
    seksueel: bool = False
    instemming_nodig: bool = False
    min_leeftijd: int = 0
    voorwaarden: tuple[str, ...] = ()     # codes van Regels die voor deze handeling extra gelden
    gevolgen: tuple[tuple[str, str, str], ...] = ()   # sjablonen (onderwerp-rol, predicaat, object-rol of waarde)
    genre: dict[str, int] = Field(default_factory=dict)  # romance, erotiek, horror, spanning, actie, intrige, komedie, tragiek, verwondering
    bron_code: Optional[str] = None


class Voorstel(BaseModel):
    """Wat de verteller (of een speler, of de simulatie) wil laten gebeuren. Verandert niets tot de poort het toelaat."""
    handeling: str
    moment: Moment
    deelnemers: tuple[Deelnemer, ...]
    wijzigingen: tuple[FeitWijziging, ...] = ()
    tekst: str = ''
    dwang_label: bool = False
    warmte: int = Field(0, ge=0, le=5)
    bron: Bron


class Schending(BaseModel):
    regel: str
    categorie: str
    zin: str
    uitleg: str
    canon_code: Optional[str] = None


class Oordeel(BaseModel):
    toegestaan: bool
    schendingen: tuple[Schending, ...] = ()


class Gebeurtenis(BaseModel):
    """Eén regel in het logboek (event sourcing). De staat van een tak = canon + alle toegelaten gebeurtenissen, in volgorde."""
    model_config = ConfigDict(frozen=True)
    tak: str
    volgnr: int
    voorstel: Voorstel
    vorige_hash: str
    hash: str = ''

    def bereken_hash(self) -> str:
        data = json.dumps({'tak': self.tak, 'volgnr': self.volgnr, 'voorstel': self.voorstel.model_dump(mode='json'),
                           'vorige': self.vorige_hash}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data.encode()).hexdigest()


class Tak(BaseModel):
    """Een eigen versie van de wereld (git-achtig): een speelsessie, een regisseursrun, of een schrijver."""
    naam: str
    ouder: Optional[str] = None
    vanaf_volgnr: int = 0


class Knoppen(BaseModel):
    """Wat de speler of regisseur wil beleven (zoals de AI Director). 0 = niets, 5 = maximaal."""
    strategie: int = Field(2, ge=0, le=5); erotiek: int = Field(2, ge=0, le=5); horror: int = Field(1, ge=0, le=5)
    spanning: int = Field(3, ge=0, le=5); actie: int = Field(2, ge=0, le=5); intrige: int = Field(3, ge=0, le=5)
    verwondering: int = Field(3, ge=0, le=5); rust: int = Field(1, ge=0, le=5)
    warmte: int = Field(2, ge=0, le=5)    # hoe expliciet erotische scènes geschreven worden; harde lijnen gelden altijd


Formule.model_rebuild()
