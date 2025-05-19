# enchantplanner/models.py

from dataclasses import dataclass, field
from typing import Dict, List
from .utils import pretty_name, xp_from_levels, check_item_can_have, is_compatible, MAX_MERGE_LEVELS, weight
from .exceptions import InvalidTarget, MergeTooExpensive, IncompatibleSelected
from .data import ENCHANTMENTS


@dataclass(frozen=True, slots=True)
class EnchantedItem:
    item_type: str
    enchants: Dict[str, int]
    anvil_uses: int = 0
    value: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "value",
            sum(l * weight(e) for e, l in self.enchants.items())
        )

    def __hash__(self) -> int:
        return hash((
            self.item_type,
            self.anvil_uses,
            tuple(sorted(self.enchants.items()))
        ))

    def pretty(self) -> str:
        """
        Nicely formatted name, using pretty_name() for each enchant key,
        handling multi‐level (>1) suffixes, and the _SPECIAL overrides.
        """
        if self.enchants:
            ench_txt = ", ".join(
                f"{pretty_name(ns)}{f' {lv}' if ENCHANTMENTS[ns]["levelMax"] > 1 else ''}"
                for ns, lv in sorted(self.enchants.items())
            )
            core = f"{self.item_type.capitalize()} ({ench_txt})"
        else:
            core = self.item_type.capitalize()

        # Books never display prior‐work penalty
        if self.item_type == "book":
            return core

        return f"{core} (Prior-work penalty = {self.anvil_uses})"

    @staticmethod
    def from_state(item_type: str, enchants: Dict[str, int] | None = None, *, anvil_uses: int = 0):
        enchants = enchants or {}
        ok, conflicts = is_compatible(enchants)
        if not ok:
            raise ValueError(f"Incompatible enchantments: {conflicts}")
        for ns, lv in enchants.items():
            if not check_item_can_have(ns, item_type):
                raise ValueError(f"{item_type} cannot receive enchantment '{ns}'")
            if lv < 1 or lv > ENCHANTMENTS[ns]["levelMax"]:
                raise ValueError(f"Level {lv} out of range for '{ns}'")
        return EnchantedItem(item_type, dict(enchants), anvil_uses=anvil_uses)

    @staticmethod
    def book(ns: str, level: int) -> "EnchantedItem":
        return EnchantedItem("book", {ns: level})

    def prior_penalty(self) -> int:
        return (1 << self.anvil_uses) - 1

    def merge_cost_levels(self, other: "EnchantedItem", rename: bool = False, repair: bool = False) -> int:
        cost = self.prior_penalty() + other.prior_penalty()
        if rename:
            cost += 1
        if repair:
            cost += 2
        cost += other.value
        return cost

    def merge(self, other: "EnchantedItem", *, rename=False, repair=False):
        if self.item_type == "book" and other.item_type != "book":
            raise InvalidTarget()
        cost_lv = self.merge_cost_levels(other, rename, repair)
        if cost_lv > MAX_MERGE_LEVELS:
            raise MergeTooExpensive(f"Merge would cost {cost_lv} levels (limit {MAX_MERGE_LEVELS})")
        cost_xp = xp_from_levels(cost_lv)

        new_uses = max(self.anvil_uses, other.anvil_uses) + 1
        new_enchants = dict(self.enchants)
        for ns, lv in other.enchants.items():
            current = new_enchants.get(ns, 0)
            if current != lv:
                new_enchants[ns] = max(current, lv)
            else:
                new_enchants[ns] = min(current + 1, ENCHANTMENTS[ns]["levelMax"])

        ok, conflicts = is_compatible(new_enchants)
        if not ok:
            raise IncompatibleSelected(conflicts)

        result_type = self.item_type if self.item_type != "book" else other.item_type
        return EnchantedItem(result_type, new_enchants, anvil_uses=new_uses), cost_lv, cost_xp


@dataclass
class Step:
    left: EnchantedItem
    right: EnchantedItem
    cost_levels: int
    cost_xp: int
    result_prior: int

    def __str__(self):
        l, r = self.left, self.right
        if l.item_type == "book" and r.item_type != "book":
            l, r = r, l
        return (
            f"Combine {l.pretty()} + {r.pretty()} → "
            f"{self.cost_levels} Levels ({self.cost_xp}xp), Prior-work penalty = {self.result_prior}"
        )


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
        lines.append(
            f"Total: {self.total_levels} levels ({self.total_xp}xp), "
            f"prior-work = {self.final_prior_work}"
        )
        if self.warnings:
            lines.append("Warnings: " + "; ".join(self.warnings))
        return "\n".join(lines)
