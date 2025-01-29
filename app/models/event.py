from datetime import datetime

from app.extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True, nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    received_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=None, onupdate=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    device_uuid = db.Column(db.String(50), nullable=False)
    event_metadata = db.Column(db.JSON, nullable=True)
    notification_sent = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    # Category relationship
    category = db.relationship('Category', backref='events_list', lazy=True)
