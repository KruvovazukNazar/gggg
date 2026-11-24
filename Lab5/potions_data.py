"""Пул зілль: 45 пар різних стихій + 5 пар однакових = 50 рецептів."""
from itertools import combinations
from ingredients_data import ESSENCES

_keys = list(ESSENCES)
_pairs = list(combinations(_keys, 2)) + [(k, k) for k in _keys[:5]]

POTIONS = {}
RECIPES = {}  # frozenset/tuple стихій -> id зілля
for _i, (_a, _b) in enumerate(_pairs):
    _pid = f"potion_{_i}"
    if _a == _b:
        _name = f"Велике зілля {ESSENCES[_a]}"
    else:
        _name = f"Зілля {ESSENCES[_a]} і {ESSENCES[_b]}"
    POTIONS[_pid] = {"name": _name, "price": 15 + _i * 3, "recipe": (_a, _b)}
    RECIPES[tuple(sorted((_a, _b)))] = _pid

if len(POTIONS) != 50:
    raise RuntimeError("Пул зілль має бути 50!")
