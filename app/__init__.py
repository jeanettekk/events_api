from flask import Flask

from config.settings import Config
from app.extensions import db
from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)

    # Load config from settings.py
    app.config.from_object(Config)

    # Initialise the app with the db object
    db.init_app(app)

    # Register all blueprints
    register_blueprints(app)

    return app
