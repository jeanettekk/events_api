import uuid
from datetime import datetime

from app.extensions import db
from app.models.category import Category
from app.models.event import Event


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
