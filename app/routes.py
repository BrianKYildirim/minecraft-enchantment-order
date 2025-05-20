import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, make_response
import datetime

from enchantplanner.data import ENCHANTMENTS
from enchantplanner.utils import pretty_name
from enchantplanner.models import EnchantedItem
from enchantplanner.calculator import plan_enchants
from enchantplanner.exceptions import IncompatibleSelected, MergeTooExpensive

main = Blueprint("main", __name__)

# All the item types (minus "book"), and sorted list of (ns,meta) pairs
ITEM_TYPES = sorted(
    {it for meta in ENCHANTMENTS.values() for it in meta["items"] if it != "book"}
)
ALL_ENCHANTS = sorted(ENCHANTMENTS.items())


def parse_enchants(prefix: str):
    out: dict[str, int] = {}
    for ns, _ in ALL_ENCHANTS:
        raw = request.form.get(f"{prefix}-{ns}")
        if raw and int(raw) > 0:
            out[ns] = int(raw)
    return out


@main.route("/")
def index():
    pretty_names = {ns: pretty_name(ns) for ns in ENCHANTMENTS}
    return render_template(
        "index.html",
        items=ITEM_TYPES,
        enchants=ALL_ENCHANTS,
        pretty_names=pretty_names
    )

@main.route("/ads.txt")
def ads_txt():
    project_root = os.path.abspath(os.path.join(current_app.root_path, os.pardir))
    return send_from_directory(
        project_root,
        "ads.txt",
        mimetype="text/plain"
    )


@main.route("/calculate", methods=["POST"])
def calculate():
    allow = request.form.get("allow_incompat") in ("true", "on", "1")
    from enchantplanner import models
    models.ALLOW_INCOMPAT = allow

    try:
        item_type = request.form.get("item_type")
        if not item_type:
            flash("Please choose an item type.")
            return redirect(url_for("main.index"))

        current = parse_enchants("cur")
        desired = parse_enchants("des")
        if not desired:
            flash("Select at least one desired enchantment.")
            return redirect(url_for("main.index"))

        mode = request.form.get("mode", "levels")
        prior_work = int(request.form.get("prior_work", 0))

        base_item = EnchantedItem.from_state(
            item_type, current, anvil_uses=prior_work
        )
        plan = plan_enchants(base_item, desired, mode=mode)

        return render_template("result.html", plan=plan)

    except (ValueError, IncompatibleSelected, MergeTooExpensive, RuntimeError) as e:
        return str(e), 400


@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    # If you ever have multiple pages, you could loop them here.
    pages = [
        {
            'loc': 'https://minecraft-enchantment-order.vercel.app/',
            'lastmod': datetime.utcnow().date().isoformat(),
            'changefreq': 'monthly',
            'priority': '1.0'
        }
    ]

    xml = render_template('sitemap.xml', pages=pages)
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response