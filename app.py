from app import create_app, db
from app.models.category import Category
from app.models.event import Event

app = create_app()

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=False)
