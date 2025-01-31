from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), unique=True, nullable=False)
    event_metadata = db.Column(db.JSON, nullable=False, default={})
    events = db.relationship('Event', backref='category_ref', lazy=True)
