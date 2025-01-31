from datetime import datetime

from app.extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True, nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False)  # API request body
    received_at = db.Column(db.DateTime, nullable=False)  # Python function records this
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # SQL records this through default
    updated_at = db.Column(db.DateTime, nullable=True, default=None, onupdate=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    device_uuid = db.Column(db.String(50), nullable=False)
    event_metadata = db.Column(db.JSON, nullable=True, default={})
    notification_sent = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    # Category relationship
    category = db.relationship('Category', backref='events_list', lazy=True)

    def create_dictionary(self):
        return {
            "uuid": self.uuid,
            "recorded_at": self.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
            "received_at": self.received_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            "category": self.category.name if self.category else None,
            "device_uuid": self.device_uuid,
            "metadata": self.event_metadata if isinstance(self.event_metadata, dict) else {},
            "notification_sent": self.notification_sent,
            "is_deleted": self.is_deleted
        }
