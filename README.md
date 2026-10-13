# Minecraft Enchantment Calculator

A web-based calculator that finds the cheapest way to apply a set of enchantments to Minecraft items.

The calculator models Minecraft's anvil mechanics, including enchantment compatibility, prior-work penalties, enchantment levels, merge costs, and the 39-level anvil limit. It can optimize a plan for either the lowest total level cost or the lowest prior-work penalty.

## Live Demo

Try the calculator here:

[Open the Minecraft Enchantment Calculator](https://minecraft-enchantment-order.vercel.app/)

## Video Demo

The video below demonstrates how to select an item, configure enchantments, choose an optimization strategy, and follow the calculated anvil plan.

https://github.com/user-attachments/assets/989052b7-e775-4d81-82d2-7af33b6cb36f

## Features

- Supports Minecraft Java Edition 1.21+
- Calculates optimal enchantment application orders
- Minimizes either:
  - Total experience levels
  - Final prior-work penalty
- Supports existing enchantments on an item
- Supports existing prior-work penalties
- Validates item and enchantment compatibility
- Enforces Minecraft's 39-level anvil limit
- Includes vanilla enchantment weights and maximum levels
- Disables or rejects impossible enchantment combinations
- Uses memoization to speed up repeated calculations
- Provides step-by-step merge instructions
- Displays level cost, XP cost, and resulting prior-work penalty
- Responsive browser-based interface
- No client-side framework required

## Why This Exists

Applying many enchantments manually in Minecraft can become surprisingly expensive.

The order in which enchanted books and items are combined affects:

- Total experience levels required
- Prior-work penalties
- Whether a merge exceeds the anvil's 39-level limit
- Whether the final item can be completed at all

This calculator searches through possible merge orders and returns a practical plan that minimizes the selected cost metric.

## How to Use It

1. Select the item you want to enchant.
2. Enter any enchantments the item already has.
3. Enter the item's current prior-work penalty, if applicable.
4. Select the enchantments you want to add.
5. Choose an optimization mode:
   - **Total Levels** — minimize total anvil levels across the full plan.
   - **Prior Work** — minimize the final prior-work penalty.
6. Submit the calculation.
7. Follow the generated step-by-step merge plan.

Each result includes:

- The two items or books to combine
- The cost of each merge in levels
- The XP cost of each merge
- The resulting prior-work penalty
- The total level cost
- The total XP cost
- Any warnings produced during calculation

## Example Result

A generated plan may look like:

```text
Step 1) Combine Protection IV book + Feather Falling IV book
        → 5 Levels, Prior-work penalty = 1

Step 2) Combine Diamond Boots + Protection IV / Feather Falling IV
        → 7 Levels, Prior-work penalty = 2

Total: 12 levels
Final prior-work penalty: 3
```

The exact result depends on the selected item, enchantments, current enchantment state, and optimization mode.

## How the Algorithm Works

The calculator represents items and enchanted books as immutable `EnchantedItem` objects.

For each possible plan, the calculator:

1. Builds a list containing the base item and any missing enchantment books.
2. Tries different ways to divide the items into merge groups.
3. Recursively solves each group.
4. Applies Minecraft merge rules to candidate combinations.
5. Rejects incompatible or overly expensive merges.
6. Memoizes previously solved item combinations.
7. Selects the best valid plan based on the chosen optimization mode.

The search tracks multiple possible prior-work outcomes so that it can compare both total level cost and final prior-work cost.

## Minecraft Rules Modeled

The calculator accounts for:

- Enchantment levels
- Enchantment weights
- Enchantment compatibility
- Item compatibility
- Combining equal enchantments
- Maximum enchantment levels
- Prior-work penalties
- Anvil merge costs
- Experience cost conversion
- The 39-level anvil limit
- Combining items and enchanted books

## Technology Stack

### Backend

- Python
- Flask
- Jinja2

### Frontend

- HTML
- Vanilla JavaScript
- Tailwind CSS
- PostCSS

### Deployment

- Vercel
- Python serverless deployment

## Project Structure

```text
minecraft-enchantment-order/
├── app/
│   ├── __init__.py             # Flask application factory
│   ├── errors.py               # Application error handlers
│   ├── routes.py               # Web routes and form handling
│   ├── static/                 # Compiled CSS and browser assets
│   └── templates/              # HTML templates
├── enchantplanner/
│   ├── calculator.py           # Recursive optimization algorithm
│   ├── data.py                 # Enchantment and item data
│   ├── exceptions.py           # Planner-specific exceptions
│   ├── models.py               # Items, merge steps, and result models
│   └── utils.py                # Cost, compatibility, and formatting helpers
├── input.css                   # Tailwind CSS input file
├── package.json                # Frontend build scripts and dependencies
├── requirements.txt            # Python dependencies
├── run.py                      # Local application entry point
├── tailwind.config.js          # Tailwind configuration
├── vercel.json                 # Vercel deployment configuration
└── README.md
```

## Performance

The planner uses recursive search with memoization to avoid recalculating identical combinations.

For typical enchantment plans, calculations complete quickly enough for interactive use in the browser. The runtime depends on:

- Number of enchantments selected
- Number of valid merge orders
- Compatibility constraints
- Existing enchantments
- Prior-work penalties
- Optimization mode

Large combinations may require more computation because the number of possible merge orders grows rapidly.

## Important Limitations

The calculator is designed to model standard Minecraft Java Edition anvil behavior, but it may not account for every possible gameplay modification.

Results may differ when using:

- Minecraft mods
- Plugins
- Custom enchantments
- Datapacks that modify anvil behavior
- Nonstandard server configurations
- Enchantments or mechanics introduced after the supported game version

Always verify especially expensive plans in-game before committing valuable items or books.

## Contributing

Contributions and suggestions are welcome.

When submitting a change:

1. Create a feature branch.
2. Add or update tests when changing calculation logic.
3. Verify the application locally.
4. Rebuild the CSS if frontend styles were modified.
5. Open a pull request with a clear description of the change.

Useful areas for improvement include:

- Additional Minecraft version support
- More comprehensive test coverage
- Improved handling of large enchantment sets
- Result export or sharing
- Better mobile interaction
- Alternative optimization strategies
- Additional validation for custom server rules

---

Built with Python, Flask, JavaScript, and Tailwind CSS.

Happy enchanting!
