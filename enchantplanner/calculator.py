import itertools
from functools import lru_cache
from typing import List, Tuple, Dict

from .models import EnchantedItem, Step, MergePlan
from .exceptions import InvalidTarget, MergeTooExpensive
from .data import ENCHANTMENTS


@lru_cache(maxsize=None)
def _cheapest_single(work_tuple: Tuple[EnchantedItem, ...]):
    items = work_tuple
    n = len(items)
    if n == 1:
        item = items[0]
        return {item.anvil_uses: ([], 0, 0, item)}

    best: Dict[int, Tuple[List[Step], int, int, EnchantedItem]] = {}

    for i in range(1, n):
        for left_idx in itertools.combinations(range(n), i):
            right_idx = tuple(sorted(set(range(n)) - set(left_idx)))
            lefts = tuple(items[j] for j in left_idx)
            rights = tuple(items[j] for j in right_idx)

            for lw, (lsteps, llv, lxp, litem) in _cheapest_single(lefts).items():
                for rw, (rsteps, rlv, rxp, ritem) in _cheapest_single(rights).items():
                    try:
                        merged, cost_lv, cost_xp = litem.merge(ritem)
                    except (InvalidTarget, MergeTooExpensive):
                        continue

                    w = merged.anvil_uses
                    tot_lv = llv + rlv + cost_lv
                    tot_xp = lxp + rxp + cost_xp
                    step = Step(litem, ritem, cost_lv, cost_xp, merged.prior_penalty())
                    cand = (lsteps + rsteps + [step], tot_lv, tot_xp, merged)

                    if w not in best or best[w][1] > tot_lv:
                        best[w] = cand

    return best


def _search(initial: EnchantedItem, books: List[EnchantedItem]):
    return _cheapest_single(tuple([initial] + books))


def plan_enchants(base: EnchantedItem, desired: Dict[str, int], *, mode: str = "levels") -> MergePlan:
    # validate desired
    for ns, lv in desired.items():
        max_lv = ENCHANTMENTS[ns]["levelMax"]
        if lv < 1 or lv > max_lv:
            raise ValueError(f"Invalid level {lv} for {ns}")
        if not base.item_type in ENCHANTMENTS[ns]["items"] and base.item_type != "book":
            raise ValueError(f"{base.item_type} cannot get {ns}")

    # build missing books
    missing: List[EnchantedItem] = []
    for ns, lv in desired.items():
        cur_lv = base.enchants.get(ns, 0)
        if cur_lv < lv:
            missing.append(EnchantedItem.book(ns, lv))

    if not missing:
        return MergePlan([], 0, 0, base.prior_penalty())

    solutions = _search(base, missing)
    if not solutions:
        raise RuntimeError("No valid anvil order—cost too high.")

    # pick best
    pick = None
    for work, (steps, lvl, xp, item) in solutions.items():
        if pick is None:
            pick = (work, steps, lvl, xp, item)
            continue
        pw, psteps, plv, pxp, pitem = pick
        if mode == "prior_work":
            if work < pitem.anvil_uses or (work == pitem.anvil_uses and lvl < plv):
                pick = (work, steps, lvl, xp, item)
        else:
            if lvl < plv or (lvl == plv and work < pitem.anvil_uses):
                pick = (work, steps, lvl, xp, item)

    _, steps, tot_lv, tot_xp, final = pick  # type: ignore
    return MergePlan(steps, tot_lv, tot_xp, final.prior_penalty())
