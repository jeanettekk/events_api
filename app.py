from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)

# Apply the configuration from settings.py
app.config.from_object(settings.Config)

# Initialise SQLAlchemy
db = SQLAlchemy(app)


# Test model
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


if __name__ == "__main__":
    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
