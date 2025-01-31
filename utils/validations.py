import re

from app.models import Category


def validate_event_data(data):
    category = data.get("category")
    device_uuid = data.get("device_uuid")
    recorded_at = data.get("recorded_at")

    if not (category and device_uuid and recorded_at):
        return False


def validate_metadata(metadata):
    # Check if event.metadata is a dictionary
    if isinstance(metadata, dict):
        return metadata
    else:
        return False


def validate_category_exists(data):
    category = Category.query.filter_by(name=data.get("category")).first()

    if category:
        return category
    else:
        return False


def check_valid_uuid(uuid_str):
    UUID_REGEX = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", re.IGNORECASE)

    return bool(UUID_REGEX.match(uuid_str))
