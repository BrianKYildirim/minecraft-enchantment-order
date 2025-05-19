from flask import Flask, send_from_directory
from .routes import main
from .errors import register_error_handlers


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(SECRET_KEY="dev-key")

    # register blueprint
    app.register_blueprint(main)

    # register error handlers
    register_error_handlers(app)
    
    return app
