from flask import Flask

from app.routes.events import event_bp


def register_blueprints(app: Flask):
    app.register_blueprint(event_bp)
