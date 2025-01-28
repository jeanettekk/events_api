from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import settings

db = SQLAlchemy()

config = settings.Config


def create_app(config_object=config):
    app = Flask(__name__)

    # Load config from settings.py
    app.config.from_object(config_object)

    # Initialise the app with the db object
    db.init_app(app)

    return app
