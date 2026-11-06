"""Feitenopslag: tijdgebonden feiten met indexen. Achter deze aansluiting kan later Postgres of een graaf-opslag zitten."""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable, Optional
import hashlib, json
from .schema import Feit, Predicaat, FeitWijziging


class Feiten:
    def __init__(self, predicaten: dict[str, Predicaat]):
        self.predicaten = predicaten
        self._alle: dict[tuple, Feit] = {}
        self._sp = defaultdict(set)     # (onderwerp, predicaat) -> sleutels
        self._po = defaultdict(set)     # (predicaat, object) -> sleutels
        self._p = defaultdict(set)      # predicaat -> sleutels
        self.soort: dict[str, str] = {} # entiteit -> Soort

    # ---- schrijven ----
    def voeg(self, f: Feit):
        k = f.sleutel()
        if k in self._alle: return
        self._alle[k] = f
        self._sp[(f.onderwerp, f.predicaat)].add(k); self._p[f.predicaat].add(k)
        if not isinstance(f.object, float): self._po[(f.predicaat, f.object)].add(k)
        if f.predicaat == 'soort': self.soort[f.onderwerp] = f.object

    def pas_toe(self, w: FeitWijziging, jaar: Optional[int] = None):
        """'stel' voegt een feit toe; 'beeindig' sluit lopende feiten met hetzelfde onderwerp+predicaat(+object) af op jaar-1."""
        if w.actie == 'stel':
            p = self.predicaten.get(w.feit.predicaat)
            if p and p.functioneel and w.feit.van is not None:
                for oud in list(self.vind(w.feit.onderwerp, w.feit.predicaat, jaar=w.feit.van)):
                    if oud.object != w.feit.object and not oud.kern: self._sluit(oud, w.feit.van - 1)
            self.voeg(w.feit)
        else:
            einde = w.feit.van if w.feit.van is not None else jaar
            obj = w.feit.object if w.feit.object is not None else ...
            for oud in list(self.vind(w.feit.onderwerp, w.feit.predicaat, obj, jaar=einde)):
                if not oud.kern: self._sluit(oud, einde - 1 if einde is not None else None)

    def _sluit(self, f: Feit, tot):
        self._verwijder(f)
        self.voeg(f.model_copy(update={'tot': tot}))

    def _verwijder(self, f: Feit):
        k = f.sleutel()
        self._alle.pop(k, None); self._sp[(f.onderwerp, f.predicaat)].discard(k); self._p[f.predicaat].discard(k)
        self._po[(f.predicaat, f.object)].discard(k)

    # ---- lezen ----
    def vind(self, onderwerp=None, predicaat=None, object=..., jaar: Optional[int] = None) -> Iterable[Feit]:
        if onderwerp is not None and predicaat is not None: ks = self._sp.get((onderwerp, predicaat), ())
        elif predicaat is not None and object is not ...: ks = self._po.get((predicaat, object), ())
        elif predicaat is not None: ks = self._p.get(predicaat, ())
        else: ks = self._alle.keys()
        for k in list(ks):
            f = self._alle.get(k)
            if f is None: continue
            if onderwerp is not None and f.onderwerp != onderwerp: continue
            if object is not ... and f.object != object: continue
            if not f.geldig_op(jaar): continue
            yield f

    def een(self, onderwerp, predicaat, jaar=None):
        for f in self.vind(onderwerp, predicaat, jaar=jaar): return f.object
        return None

    def bestaat(self, entiteit: str) -> bool:
        return entiteit in self.soort

    def __len__(self): return len(self._alle)

    def kopie(self) -> 'Feiten':
        n = Feiten(self.predicaten)
        for f in self._alle.values(): n.voeg(f)
        return n

    def hash(self) -> str:
        h = hashlib.sha256()
        for k in sorted(self._alle, key=lambda t: json.dumps(t, default=str)):
            h.update(json.dumps(self._alle[k].model_dump(mode='json'), sort_keys=True, default=str).encode())
        return h.hexdigest()
