# Minecraft Enchant Planner

*A tiny Flask + Vanilla-JS web app that tells you the cheapest way to put **any** set of enchantments on any item in Minecraft (Java 1.21 +).*

Available as a live demo here: [Minecraft Enchant Planner](https://minecraft-enchantment-order.vercel.app/)

---

## Table of Contents

1. [Features](#features)
2. [Video Showcase](#video-showcase) 
3. [Quick Start](#quick-start)  
4. [How It Works](#how-it-works)  

---

## Features

| Capability                   | Description                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Optimal Anvil Ordering**   | Finds the sequence with the lowest *total levels* **or** the smallest *prior-work penalty*.                   |
| **Full 1.20 Enchant Data**   | All vanilla items, all enchantments, weights, level caps & incompatibilities faithfully encoded.             |
| **Live Validation**          | Impossible or incompatible combinations are auto-disabled and greyed-out in the UI.                           |
| **Prior-Work Input**         | Enter an existing prior-work penalty (0–39) and it’s included in the optimization.                            |
| **Instant Results**          | Typical plans compute in ≲ 20 ms thanks to heavy memoization and a pure-Python search.                        |
| **Zero Client Dependencies** | Everything runs in one HTML file with vanilla JS—no frameworks or bundlers client-side.                      |

---

## Video Showcase

https://github.com/user-attachments/assets/989052b7-e775-4d81-82d2-7af33b6cb36f

---

## Quick Start

### 1. Clone and Install

*Though this project is hosted on Render, feel free to clone and run it locally!*

```bash
git clone https://github.com/BrianKYildirim/minecraft-enchantment-order.git
cd minecraft-enchantment-order
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
````

### 2. Run Locally

```bash
python run.py
```

### 3. Use

1. **Pick** an item from the drop-down.
2. **Set** your current enchantments (and prior-work).
3. **Select** desired enchantments.
4. **Choose** optimization mode (levels or prior-work).
5. **Calculate** and follow the step-by-step plan.

---

## How It Works

1. **Immutable models**

   * `EnchantedItem` encapsulates item type, enchant levels, and prior-work uses.
2. **Recursive, memoized search**

   * `_cheapest_single(...)` tries every bipartition of `(base + books)`, merges sub-results, and tracks the best plan per resulting prior-work.
3. **Vanilla anvil rules**

   * Merge cost, level stacking, incompatibilities, and the hard 39-level cap are enforced in `EnchantedItem.merge()`.
4. **Flexible optimization**

   * You can minimize **total levels** or final **prior-work penalty**, with tie-breakers on the other metric.

---

*Happy enchanting!*
