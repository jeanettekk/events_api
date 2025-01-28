from app import create_app, db
from app.models.category import Category
from app.models.event import Event

app = create_app()

if __name__ == "__main__":
    # Create the tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=False)
