# Minecraft Enchant Planner

*A tiny Flask + Vanilla‑JS web app that tells you the cheapest way to put **any** set of enchantments on any item in Minecraft (Java 1.20 +).*

Available for use here!

https://minecraft-enchantment-order.onrender.com

---

##  Features

| Capability                    | Description                                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Optimal anvil ordering**                          | Finds the sequence with the lowest *total levels* **or** the smallest *prior‑work penalty* |
| **Full 1.20 enchant data**                          | All vanilla items, all enchantments, weights, level caps & incompatibilities |
| **Live validation**                                 | Impossible combinations are auto‑disabled and greyed‑out |
| **Prior‑work input**                                | Enter an existing prior‑work penalty and it’s respected in the search |
| **Instant results**                                 | Typical plans compute in ≲ 20 ms thanks to heavy memoisation |
| **No dependencies on the client**                   | Everything runs in one HTML file with vanilla JS |

---

## Video Showcase

https://github.com/user-attachments/assets/037b5237-23fe-40de-b5e3-ec3a6a344c9c


##  Quick Start

### 1 · Clone & install
```bash
git clone https://github.com/BrianKYildirim/minecraft-enchantment-order.git
cd minecraft-enchantment-order
python -m venv .venv && .venv\Scripts\activate.bat
pip install -r requirements.txt
````

### 2 · Run

```bash
python app.py        # default: http://127.0.0.1:5000
```

### 3 · Enjoy

1. Pick an item from the drop‑down.
2. Click the level buttons to describe **current** and **desired** enchantments.
3. Choose whether you care about *least total levels* or *least prior‑work*, then **Calculate**.
4. Follow the step‑by‑step plan shown at the bottom of the page 

---

##  Project Layout

```
.
├── app.py                 ← Flask entry‑point / routes
├── enchantmentcalc.py     ← Pure‑python optimiser (no Flask imports!)
├── templates/
│   ├── base.html
│   ├── index.html         ← main UI (all vanilla JS here)
│   └── result.html
└── requirements.txt       ← Flask only
```

---

##  How the algorithm works

1. **Immutable `EnchantedItem` objects** record item‑type, enchants & prior‑work.
2. A **recursive, memoised search** (`_cheapest_single`) tries every possible
   bipartition of the input books + base item, merges the cheapest sub‑results
   and remembers the best plan for each resulting prior‑work value.
3. Vanilla anvil rules (merge cost, level stacking, incompatibilities, the
   hard 39‑level cap, etc.) are faithfully reproduced in
   `EnchantedItem.merge()`.
4. The user can choose to optimize either
   *Σ levels* **or** final *prior‑work penalty* (ties broken by the other metric).

---
