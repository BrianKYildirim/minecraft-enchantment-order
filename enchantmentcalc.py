from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List, Tuple

ENCHANTMENTS: Dict[str, Dict] = {
    "aqua_affinity":
        {"levelMax": 1,
         "weight": 2,
         "incompatible": [],
         "items": ["helmet"]},
    "bane_of_arthropods":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": ["sharpness", "smite", "density", "breach"],
         "items": ["sword", "axe", "mace"]},
    "blast_protection":
        {"levelMax": 4,
         "weight": 2,
         "incompatible": ["protection", "fire_protection", "projectile_protection"],
         "items": ["helmet", "chestplate", "leggings", "boots", "turtle_shell"]},
    "breach":
        {"levelMax": 4,
         "weight": 2,
         "incompatible": ["density", "smite", "bane_of_arthropods"],
         "items": ["mace"]},
    "channeling":
        {"levelMax": 1,
         "weight": 4,
         "incompatible": ["riptide"],
         "items": ["trident"]},
    "curse_of_binding":
        {"levelMax": 1,
         "weight": 4,
         "incompatible": [],
         "items": ["helmet", "chestplate", "leggings", "boots", "elytra", "pumpkin", "helmet", "turtle_shell"]},
    "curse_of_vanishing":
        {"levelMax": 1,
         "weight": 4,
         "incompatible": [],
         "items": ["helmet", "chestplate", "leggings", "boots", "pickaxe", "shovel", "axe", "sword", "hoe", "brush",
                   "fishing_rod", "bow", "shears", "flint_and_steel", "carrot_on_a_stick", "warped_fungus_on_a_stick",
                   "shield", "elytra", "pumpkin", "helmet", "trident", "turtle_shell", "crossbow", "mace"]},
    "denisty":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": ["breach", "smite", "bane_of_arthropods"],
         "items": ["mace"]},
    "depth_strider":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": ["frost_walker"],
         "items": ["boots"]},
    "efficiency":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": [],
         "items": ["pickaxe", "shovel", "axe", "hoe", "shears"]},
    "feather_falling":
        {"levelMax": 4,
         "weight": 1,
         "incompatible": [],
         "items": ["boots"]},
    "fire_aspect":
        {"levelMax": 2,
         "weight": 2,
         "incompatible": [],
         "items": ["sword", "mace"]},
    "fire_protection":
        {"levelMax": 4,
         "weight": 1,
         "incompatible": ["protection", "blast_protection", "projectile_protection"],
         "items": ["helmet", "chestplate", "leggings", "boots", "turtle_shell"]},
    "flame":
        {"levelMax": 1,
         "weight": 2,
         "incompatible": [],
         "items": ["bow"]},
    "fortune":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": ["silk_touch"],
         "items": ["pickaxe", "shovel", "axe", "hoe"]},
    "frost_walker":
        {"levelMax": 2,
         "weight": 2,
         "incompatible": ["depth_strider"],
         "items": ["boots"]},
    "impaling":
        {"levelMax": 5,
         "weight": 2,
         "incompatible": [],
         "items": ["trident"]},
    "infinity":
        {"levelMax": 1,
         "weight": 4,
         "incompatible": ["mending"],
         "items": ["bow"]},
    "knockback":
        {"levelMax": 2,
         "weight": 1,
         "incompatible": [],
         "items": ["sword"]},
    "looting":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["sword"]},
    "loyalty":
        {"levelMax": 3,
         "weight": 1,
         "incompatible": ["riptide"],
         "items": ["trident"]},
    "luck_of_the_sea":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["fishing_rod"]},
    "lure":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["fishing_rod"]},
    "mending":
        {"levelMax": 1,
         "weight": 2, "incompatible": ["infinity"],
         "items": ["helmet", "chestplate", "leggings", "boots", "pickaxe", "shovel", "axe", "sword", "hoe", "brush",
                   "fishing_rod", "bow", "shears", "flint_and_steel", "carrot_on_a_stick", "warped_fungus_on_a_stick",
                   "shield", "elytra", "trident", "turtle_shell", "crossbow", "mace"]},
    "multishot":
        {"levelMax": 1,
         "weight": 2,
         "incompatible": ["piercing"],
         "items": ["crossbow"]},
    "piercing":
        {"levelMax": 4,
         "weight": 1,
         "incompatible": ["multishot"],
         "items": ["crossbow"]},
    "power":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": [],
         "items": ["bow"]},
    "projectile_protection":
        {"levelMax": 4,
         "weight": 1,
         "incompatible": ["protection", "blast_protection", "fire_protection"],
         "items": ["helmet", "chestplate", "leggings", "boots", "turtle_shell"]},
    "protection":
        {"levelMax": 4,
         "weight": 1,
         "incompatible": ["blast_protection", "fire_protection", "projectile_protection"],
         "items": ["helmet", "chestplate", "leggings", "boots", "turtle_shell"]},
    "punch":
        {"levelMax": 2,
         "weight": 2,
         "incompatible": [],
         "items": ["bow"]},
    "quick_charge":
        {"levelMax": 3,
         "weight": 1,
         "incompatible": [],
         "items": ["crossbow"]},
    "respiration":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["helmet", "turtle_shell"]},
    "riptide":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": ["channeling", "loyalty"],
         "items": ["trident"]},
    "sharpness":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": ["bane_of_arthropods", "smite"],
         "items": ["sword", "axe"]},
    "silk_touch":
        {"levelMax": 1,
         "weight": 4,
         "incompatible": ["fortune"],
         "items": ["pickaxe", "shovel", "axe", "hoe"]},
    "smite":
        {"levelMax": 5,
         "weight": 1,
         "incompatible": ["bane_of_arthropods", "sharpness", "density", "breach"],
         "items": ["sword", "axe", "mace"]},
    "soul_speed":
        {"levelMax": 3,
         "weight": 4,
         "incompatible": [],
         "items": ["boots"]},
    "sweeping":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["sword"]},
    "swift_sneak":
        {"levelMax": 3,
         "weight": 4,
         "incompatible": [],
         "items": ["leggings"]},
    "thorns":
        {"levelMax": 3,
         "weight": 4,
         "incompatible": [],
         "items": ["helmet", "chestplate", "leggings", "boots", "turtle_shell"]},
    "unbreaking":
        {"levelMax": 3,
         "weight": 1,
         "incompatible": [],
         "items": ["helmet", "chestplate", "leggings", "boots", "pickaxe", "shovel", "axe",
                   "sword", "hoe", "brush", "fishing_rod", "bow", "shears", "flint_and_steel",
                   "carrot_on_a_stick", "warped_fungus_on_a_stick", "shield", "elytra",
                   "trident", "turtle_shell", "crossbow", "mace"]},
    "wind_burst":
        {"levelMax": 3,
         "weight": 2,
         "incompatible": [],
         "items": ["mace"]},
}

MAX_MERGE_LEVELS = 39


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
    """Return (ok, list_of_conflicts)."""
    conflicts: List[Tuple[str, str]] = []
    for a, b in itertools.combinations(chosen.keys(), 2):
        if a in ENCHANTMENTS[b]["incompatible"] or b in ENCHANTMENTS[a]["incompatible"]:
            conflicts.append((a, b))
    return len(conflicts) == 0, conflicts

class InvalidTarget(Exception):
    """Book may not be used as an anvil *target* when the sacrifice isn’t a book."""
    pass


@dataclass(frozen=True, slots=True)
class EnchantedItem:
    item_type: str
    enchants: Dict[str, int]
    anvil_uses: int = 0
    value: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "value", sum(l * weight(e) for e, l in self.enchants.items()))

    @staticmethod
    def from_state(item_type: str, enchants: Dict[str, int] | None = None, *, anvil_uses: int = 0) -> "EnchantedItem":
        enchants = enchants or {}
        ok, conflicts = is_compatible(enchants)
        if not ok:
            raise ValueError(f"Incompatible enchantments in starting item: {conflicts}")
        for ns, lv in enchants.items():
            if not check_item_can_have(ns, item_type):
                raise ValueError(f"{item_type} cannot receive enchantment '{ns}'")
            if lv < 1 or lv > int(ENCHANTMENTS[ns]["levelMax"]):
                raise ValueError(f"Level {lv} out of range for '{ns}' (max {ENCHANTMENTS[ns]['levelMax']})")
        return EnchantedItem(item_type=item_type, enchants=dict(enchants), anvil_uses=anvil_uses)

    @staticmethod
    def book(ns: str, level: int) -> "EnchantedItem":
        return EnchantedItem("book", {ns: level})

    def prior_penalty(self) -> int:
        return (1 << self.anvil_uses) - 1  # 2^n - 1

    def merge_cost_levels(self, other: "EnchantedItem", rename: bool = False, repair: bool = False) -> int:
        cost = self.prior_penalty() + other.prior_penalty()
        if rename:
            cost += 1
        if repair:
            cost += 2
        cost += other.value
        return cost

    def __hash__(self) -> int:
        return hash((
            self.item_type,
            self.anvil_uses,
            tuple(sorted(self.enchants.items()))
        ))

    def merge(self, other: "EnchantedItem", *, rename=False, repair=False) -> tuple["EnchantedItem", int, int]:
        if self.item_type == "book" and other.item_type != "book":
            raise InvalidTarget()
        cost_levels = self.merge_cost_levels(other, rename, repair)
        if cost_levels > MAX_MERGE_LEVELS:
            raise MergeTooExpensive(f"Merge would cost {cost_levels} levels (limit {MAX_MERGE_LEVELS})")
        cost_xp = xp_from_levels(cost_levels)

        new_uses = max(self.anvil_uses, other.anvil_uses) + 1

        new_enchants = dict(self.enchants)
        for ns, lv in other.enchants.items():
            current = new_enchants.get(ns, 0)
            new_enchants[ns] = max(current, lv) if current != lv else min(current + 1,
                                                                          int(ENCHANTMENTS[ns]["levelMax"]))
        ok, conflicts = is_compatible(new_enchants)
        if not ok:
            raise IncompatibleSelected(conflicts)

        return (EnchantedItem(self.item_type if self.item_type != "book" else other.item_type,
                              new_enchants, anvil_uses=new_uses),
                cost_levels, cost_xp)

    def pretty(self) -> str:
        if self.item_type == "book":
            ench_txt = ", ".join(
                f"{ns.capitalize()} {lv}" for ns, lv in sorted(self.enchants.items())
            )
            return f"Book ({ench_txt.capitalize().replace("_", " ")})"

        ench_txt = ", ".join(
            f"{ns.capitalize()} {lv}" for ns, lv in sorted(self.enchants.items())
        )
        return f"{self.item_type.capitalize()} ({ench_txt.capitalize()}) (Prior-work penalty = {self.anvil_uses})"


class MergeTooExpensive(Exception):
    pass


class IncompatibleSelected(Exception):
    pass


@dataclass
class Step:
    left: EnchantedItem
    right: EnchantedItem
    cost_levels: int
    cost_xp: int
    result_prior: int

    def __str__(self):
        left, right = self.left, self.right
        if left.item_type == "book" and right.item_type != "book":
            left, right = right, left
        return (f"Combine {left.pretty()}  +  {right.pretty()}  →  "
                f"{self.cost_levels} Levels ({self.cost_xp}xp), Prior-work penalty = {self.result_prior}")


@dataclass
class MergePlan:
    steps: List[Step]
    total_levels: int
    total_xp: int
    final_prior_work: int
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"Step {i + 1}) {s}" for i, s in enumerate(self.steps)]
        lines.append("—" * 60)
        lines.append(f"Total: {self.total_levels}levels  ({self.total_xp}xp)   prior‑work = {self.final_prior_work}")
        if self.warnings:
            lines.append("Warnings: " + "; ".join(self.warnings))
        return "\n".join(lines)


@lru_cache(maxsize=None)
def _cheapest_single(work_tuple: Tuple):
    items: Tuple[EnchantedItem, ...] = work_tuple
    n = len(items)
    if n == 1:
        return {items[0].anvil_uses: ([], 0, 0, items[0])}
    best: Dict[int, Tuple[List[Step], int, int, EnchantedItem]] = {}
    for i in range(1, n):
        for left_idx in itertools.combinations(range(n), i):
            right_idx = tuple(sorted(set(range(n)) - set(left_idx)))
            left_items = tuple(items[j] for j in left_idx)
            right_items = tuple(items[j] for j in right_idx)
            for Lwork, (Lsteps, Llvl, Lxp, Litem) in _cheapest_single(left_items).items():
                for Rwork, (Rsteps, Rlvl, Rxp, Ritem) in _cheapest_single(right_items).items():
                    try:
                        merged, cost_lv, cost_xp = Litem.merge(Ritem)
                    except (MergeTooExpensive, IncompatibleSelected, InvalidTarget):
                        continue

                    w = merged.anvil_uses
                    tot_lvl = Llvl + Rlvl + cost_lv
                    tot_xp = Lxp + Rxp + cost_xp
                    step = Step(Litem, Ritem, cost_lv, cost_xp, merged.prior_penalty())
                    candidate = (Lsteps + Rsteps + [step], tot_lvl, tot_xp, merged)
                    if (w not in best) or (best[w][1] > tot_lvl):
                        best[w] = candidate
    return best


def _search(initial: EnchantedItem, books: List[EnchantedItem]) -> Dict[
    int, Tuple[List[Step], int, int, EnchantedItem]]:
    return _cheapest_single(tuple([initial] + books))


def plan_enchants(base: EnchantedItem, desired: Dict[str, int], *, mode: str = "levels") -> MergePlan:
    for ns, lv in desired.items():
        if lv < 1 or lv > int(ENCHANTMENTS[ns]["levelMax"]):
            raise ValueError(f"Requested level {lv} invalid for enchant '{ns}'.")
        if not check_item_can_have(ns, base.item_type):
            raise ValueError(f"{base.item_type} cannot receive enchant '{ns}'.")
    ok, conflicts = is_compatible(desired)
    if not ok:
        raise ValueError(f"Mutually exclusive enchantments requested: {conflicts}")

    missing: List[EnchantedItem] = []
    for ns, lv in desired.items():
        if base.enchants.get(ns, 0) < lv:
            missing.append(EnchantedItem.book(ns, lv))

    if not missing:
        return MergePlan([], 0, 0, base.prior_penalty())

    solutions = _search(base, missing)
    if not solutions:
        raise RuntimeError("No valid anvil ordering found (all merges > 39 levels?)")

    if mode not in {"levels", "prior_work"}:
        raise ValueError("mode must be 'levels' or 'prior_work'")
    pick = None
    for work, cand in solutions.items():
        if pick is None:
            pick = cand
            continue
        _, lv, xp, _ = cand
        _, plv, pxp, pitem = pick
        if mode == "prior_work":
            if work < pitem.anvil_uses or (work == pitem.anvil_uses and lv < plv):
                pick = cand
        else:
            if lv < plv or (lv == plv and work < pitem.anvil_uses):
                pick = cand
    steps, tot_lv, tot_xp, final_item = pick
    return MergePlan(steps, tot_lv, tot_xp, final_item.prior_penalty())


if __name__ == "__main__":
    boots = EnchantedItem.from_state("boots", {"depth_strider": 3}, anvil_uses=2)
    target = {
        "protection": 4,
        "feather_falling": 4,
        "mending": 1,
        "unbreaking": 3,
    }
    plan = plan_enchants(boots, target, mode="levels")
    print(plan.summary())
