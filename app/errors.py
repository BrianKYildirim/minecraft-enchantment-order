from flask import render_template
from enchantplanner.exceptions import IncompatibleSelected, MergeTooExpensive


def register_error_handlers(app):
    @app.errorhandler(IncompatibleSelected)
    @app.errorhandler(MergeTooExpensive)
    @app.errorhandler(ValueError)
    def handle_enchant_errors(e):
        # just return the message and a 400
        return str(e), 400
