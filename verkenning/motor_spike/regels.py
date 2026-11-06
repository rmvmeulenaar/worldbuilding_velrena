"""Regelmotor: evalueert Formules (de kleine logische taal uit schema.py) tegen feiten, met variabelen.

Werkt als een mini-Datalog: patronen worden gematcht tegen de feitenopslag, variabelen worden gebonden, 'niet' is
negatie-als-falen. Virtuele predicaten (leeftijd) worden berekend in plaats van opgeslagen.
"""
from __future__ import annotations
from typing import Iterator, Optional
import re
from .schema import Formule, Regel, Feit, Bron, Epistemiek

Binding = dict


def is_var(x) -> bool: return isinstance(x, str) and x.startswith('?')
def waarde(x, b: Binding): return b.get(x, x) if is_var(x) else x


class Laag:
    """Hypothetische staat: de basisfeiten plus de feiten van één voorstel, zonder de basis te kopiëren."""
    def __init__(self, basis, extra: list[Feit], jaar: Optional[int]):
        self.basis, self.jaar = basis, jaar
        self.extra = extra
        self._ix = {}
        for f in extra: self._ix.setdefault((f.onderwerp, f.predicaat), []).append(f); self._ix.setdefault((None, f.predicaat), []).append(f)

    def vind(self, onderwerp=None, predicaat=None, object=...):
        for f in self.basis.vind(onderwerp, predicaat, object, jaar=self.jaar): yield f
        for f in self._ix.get((onderwerp, predicaat) if onderwerp is not None else (None, predicaat), []):
            if object is not ... and f.object != object: continue
            if not f.geldig_op(self.jaar): continue
            yield f

    def een(self, s, p):
        for f in self.vind(s, p): return f.object
        return None


def leeftijd(staat, persoon: str, jaar: int) -> Optional[int]:
    """Leeftijd in een jaar: uit geboortejaar, anders uit de leeftijdsband op het canonjaar (ondergrens)."""
    g = staat.een(persoon, 'geboren')
    if g is not None: return jaar - int(g)
    band, cj = staat.een(persoon, 'leeftijd_band'), staat.een(persoon, 'canonjaar')
    if band:
        m = re.match(r'(\d+)', str(band))
        if m: return int(m.group(1)) + ((jaar - int(cj)) if cj is not None else 0)
    return None


def evalueer(formule: Formule, staat, b: Binding) -> Iterator[Binding]:
    if formule.feit is not None:
        s, p, o = formule.feit
        sv, pv, ov = waarde(s, b), waarde(p, b), waarde(o, b)
        if pv == 'leeftijd':
            if is_var(sv): return
            n = leeftijd(staat, sv, staat.jaar) if staat.jaar is not None else None
            if n is None: return
            if is_var(ov): yield {**b, ov: n}
            elif ov == n: yield b
            return
        for f in staat.vind(None if is_var(sv) else sv, pv, ... if is_var(ov) else ov):
            nb = dict(b)
            if is_var(sv): nb[sv] = f.onderwerp
            if is_var(ov): nb[ov] = f.object
            yield nb
    elif formule.alle is not None:
        yield from _en(formule.alle, staat, b)
    elif formule.een is not None:
        for sub in formule.een: yield from evalueer(sub, staat, b)
    elif formule.niet is not None:
        for _ in evalueer(formule.niet, staat, b): return
        yield b
    elif formule.cmp is not None:
        op, x, y = formule.cmp
        x, y = waarde(x, b), waarde(y, b)
        if is_var(x) or is_var(y) or x is None or y is None: return
        try:
            ok = {'<': x < y, '<=': x <= y, '>': x > y, '>=': x >= y, '==': x == y, '!=': x != y}[op]
        except TypeError: return
        if ok: yield b


def _en(delen, staat, b):
    if not delen: yield b; return
    for nb in evalueer(delen[0], staat, b): yield from _en(delen[1:], staat, nb)


def schendingen_van(regel: Regel, staat, max_n: int = 5) -> list[Binding]:
    """Verbod: elke oplossing is een schending. Vereiste: geen oplossing is een schending."""
    if regel.formule is None: return []
    uit = []
    for bnd in evalueer(regel.formule, staat, {}):
        if regel.soort == 'vereiste': return []
        uit.append(bnd)
        if len(uit) >= max_n: break
    if regel.soort == 'vereiste': return [{}]
    return uit


# ---------- hulp om formules leesbaar te schrijven ----------
def F(s, p, o): return Formule(feit=[s, p, o])
def EN(*d): return Formule(alle=list(d))
def OF(*d): return Formule(een=list(d))
def NIET(d): return Formule(niet=d)
def CMP(op, a, b): return Formule(cmp=[op, a, b])
