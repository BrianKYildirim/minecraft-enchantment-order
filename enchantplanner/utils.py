from typing import Dict, List, Tuple
from .data import ENCHANTMENTS

_IGNORE_LOWER = {"of"}
_SPECIAL = {"sweeping": "Sweeping Edge"}
MAX_MERGE_LEVELS = 39  # for reference in merge routines


def _pretty_name(ns: str) -> str:
    if ns in _SPECIAL:
        return _SPECIAL[ns]
    words = ns.split("_")
    return " ".join(w.capitalize() if w not in _IGNORE_LOWER else w
                    for w in words)


def xp_from_levels(levels: int) -> int:
    if levels <= 0:
        return 0
    if levels <= 16:
        return levels ** 2 + 6 * levels
    if levels <= 31:
        return int(2.5 * levels ** 2 - 40.5 * levels + 360)
    return int(4.5 * levels ** 2 - 162.5 * levels + 2220)


def weight(ns: str) -> int:
    return int(ENCHANTMENTS[ns]["weight"])


def check_item_can_have(enchant_ns: str, item_type: str) -> bool:
    return item_type == "book" or item_type in ENCHANTMENTS[enchant_ns]["items"]


def is_compatible(chosen: Dict[str, int]) -> Tuple[bool, List[Tuple[str, str]]]:
    conflicts: List[Tuple[str, str]] = []
    items = list(chosen.keys())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a in ENCHANTMENTS[b]["incompatible"] or b in ENCHANTMENTS[a]["incompatible"]:
                conflicts.append((a, b))
    return (not conflicts, conflicts)
