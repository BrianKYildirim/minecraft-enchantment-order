from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

from enchantmentcalc import (
    ENCHANTMENTS,
    EnchantedItem,
    plan_enchants,
    IncompatibleSelected,
    MergeTooExpensive,
)

app = Flask(__name__)
app.secret_key = "dev-key"  # change in production

# ---------------------------------------------------------------------------
# Pre‑computed lists for the form -------------------------------------------
# ---------------------------------------------------------------------------
ITEM_TYPES = sorted({it for e in ENCHANTMENTS.values() for it in e["items"] if it != "book"})
ALL_ENCHANTS = sorted(ENCHANTMENTS.items())  # list[(namespace, meta)]


# Helpers -------------------------------------------------------------------

def parse_enchants(prefix: str):
    out = {}
    for ns, meta in ALL_ENCHANTS:
        raw = request.form.get(f"{prefix}-{ns}")
        if raw and int(raw) > 0:  # non‑empty
            out[ns] = int(raw)
    return out

# Routes --------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", items=ITEM_TYPES, enchants=ALL_ENCHANTS)


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        item_type = request.form.get("item_type")
        if not item_type:
            flash("Please choose an item type.")
            return redirect(url_for("index"))

        current = parse_enchants("cur")
        desired = parse_enchants("des")
        if not desired:
            flash("Select at least one desired enchantment.")
            return redirect(url_for("index"))

        mode = request.form.get("mode", "levels")
        prior_work = int(request.form.get("prior_work", 0))
        base_item = EnchantedItem.from_state(item_type, current,
                                             anvil_uses=prior_work)
        plan = plan_enchants(base_item, desired, mode=mode)
        return render_template("result.html", plan=plan)

    except (ValueError, IncompatibleSelected, MergeTooExpensive) as e:
        flash(str(e))
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
