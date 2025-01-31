import uuid
from datetime import datetime

from app.extensions import db
from app.models.event import Event
from utils.validations import validate_metadata


def get_all_events():
    events = Event.query.all()  # Get all events from the events table

    # Converts events to a list of dictionaries to return as a JSON
    events_list = [{
        "uuid": str(event.uuid),
        "recorded_at": event.recorded_at,
        "received_at": event.received_at,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
        "category": event.category.name if event.category else None,
        "device_uuid": event.device_uuid,
        "metadata": validate_metadata(event.metadata),
        "notification_sent": event.notification_sent,
        "is_deleted": event.is_deleted
    } for event in events]

    return events_list


def get_event_by_uuid(uuid):
    event = Event.query.filter_by(uuid=uuid).first()

    return event


def create_event(category_id, device_uuid, recorded_at, event_metadata):
    new_event = Event(
        uuid=str(uuid.uuid4()),  # generates a new Version 4 UUID
        recorded_at=datetime.strptime(recorded_at, "%Y-%m-%d %H:%M:%S"),  # API request body
        received_at=datetime.now(),  # Python function records this
        category_id=category_id,
        device_uuid=device_uuid,
        event_metadata=event_metadata or {},  # Default to empty if not provided
        notification_sent=False,
        is_deleted=False
    )

    db.session.add(new_event)
    db.session.commit()
    return new_event


def update_notification_sent(uuid):
    event = get_event_by_uuid(uuid)

    if event is None:
        return None

    elif event.notification_sent:
        return 'already_true'

    # Update the notification_sent flag to True
    event.notification_sent = True
    event.updated_at = datetime.now()

    db.session.commit()

    return event


def delete_event_by_uuid(uuid):
    event = get_event_by_uuid(uuid)

    if event is None:
        return None

    if event.is_deleted:
        return 'already_deleted'

    event.is_deleted = True
    db.session.commit()

    return event
