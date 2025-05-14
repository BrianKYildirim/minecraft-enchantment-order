from flask import Flask, render_template, request, redirect, url_for, flash

from enchantmentcalc import (
    ENCHANTMENTS,
    _pretty_name,
    EnchantedItem,
    plan_enchants,
    IncompatibleSelected,
    MergeTooExpensive,
)

app = Flask(__name__)
app.secret_key = "dev-key"

ITEM_TYPES = sorted({it for e in ENCHANTMENTS.values() for it in e["items"] if it != "book"})
ALL_ENCHANTS = sorted(ENCHANTMENTS.items())


def parse_enchants(prefix: str):
    out = {}
    for ns, meta in ALL_ENCHANTS:
        raw = request.form.get(f"{prefix}-{ns}")
        if raw and int(raw) > 0:
            out[ns] = int(raw)
    return out


@app.route("/")
def index():
    pretty = {ns: _pretty_name(ns) for ns in ENCHANTMENTS}
    return render_template(
        "index.html",
        items=ITEM_TYPES,
        enchants=ALL_ENCHANTS,
        pretty_names=pretty
    )


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

    except (ValueError,
            IncompatibleSelected,
            MergeTooExpensive,
            RuntimeError,) as e:
        return str(e), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
