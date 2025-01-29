import uuid
from datetime import datetime

from app.extensions import db
from app.models.category import Category
from app.models.event import Event


def get_event_by_uuid(uuid):
    event = Event.query.filter_by(uuid=uuid).first()
    if not event:
        return None

    # Check if event.metadata is a dictionary
    if isinstance(event.metadata, dict):
        metadata = event.metadata
    else:
        # If it's not a dictionary, set metadata to an empty dictionary
        metadata = {}

    return {
        "uuid": str(event.uuid),
        "recorded_at": event.recorded_at.strftime("%Y-%m-%d %H:%M:%S") if event.recorded_at else None,
        "received_at": event.received_at.strftime("%Y-%m-%d %H:%M:%S") if event.received_at else None,
        "created_at": event.created_at.strftime("%Y-%m-%d %H:%M:%S") if event.created_at else None,
        "updated_at": event.updated_at.strftime("%Y-%m-%d %H:%M:%S") if event.updated_at else None,
        "category_id": event.category_id,
        "device_uuid": event.device_uuid,
        "metadata": metadata,
        "notification_sent": event.notification_sent,
        "is_deleted": event.is_deleted
    }


def create_event(category_id, device_uuid, recorded_at, metadata=None):
    # Check if the category exists
    category = Category.query.get(category_id)
    if not category:
        return None

    # Create a new event
    new_event = Event(
        uuid=str(uuid.uuid4()),
        recorded_at=datetime.strptime(recorded_at, "%Y-%m-%d %H:%M:%S"),
        received_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        category_id=category_id,
        device_uuid=device_uuid,
        metadata=metadata or {},  # Default to empty if not provided
        notification_sent=False,
        is_deleted=False
    )

    db.session.add(new_event)
    db.session.commit()

    return new_event
