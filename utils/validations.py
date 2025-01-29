from app.models import Category


def validate_metadata(metadata):
    # Check if event.metadata is a dictionary
    if isinstance(metadata, dict):
        return metadata
    else:
        # If it's not a dictionary, set metadata to an empty dictionary
        return {}


def validate_category_exists(category_id):
    category = Category.query.get(category_id)
    if category:
        return True
    else:
        False

# def validate_event_data(data):
#     category_id = data.get("category_id")
#     device_uuid = data.get("device_uuid")
#     recorded_at = data.get("recorded_at")
#
#     if not category_id or not device_uuid or not recorded_at:
#         return jsonify({"Error": "Missing required fields"}), 400
