import os

import pytest

from app import create_app, db
from app.models import Category


# Fixture to create and configure the app
@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')  # Use in-memory database for testing
    app.config['TESTING'] = True  # Enable testing mode

    with app.app_context():
        db.create_all()
        yield app  # Provide app for testing
        db.drop_all()


# Fixture to create the test client
@pytest.fixture
def client(app):
    return app.test_client()


# Fixture to set up categories for testing
@pytest.fixture(scope="function")
def setup_categories(db_session):
    category1 = Category(name='DeviceOnline', description='Device connected to the internet')
    category2 = Category(
        name='DeviceOverheating',
        description='A warning for when a device gets too hot due to overcharging or location temperature',
        event_metadata={"warning_temperature": False, "critical_temperature": False}
    )

    db_session.add_all([category1, category2])
    db_session.commit()

    return category1, category2


# Provides a clean database session for each test
@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()  # Rollback after each test to reset changes
