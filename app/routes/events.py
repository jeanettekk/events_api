from flask import Blueprint, request, jsonify

from services.event_service import create_event, get_all_events, delete_event_by_uuid, \
    update_notification_sent, validate_metadata, get_event_by_uuid
from utils.validations import validate_category_exists, validate_event_data, check_valid_uuid

event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/events", methods=["GET"])
def get_events():
    events_list = get_all_events()

    if not events_list:
        return jsonify({"Error": "There are no events"}), 404

    return jsonify(events_list), 200


@event_bp.route("/event/<uuid>", methods=["GET"])
def get_event_by_uuid_route(uuid):
    event = get_event_by_uuid(uuid)
    valid_uuid = check_valid_uuid(uuid)

    if not valid_uuid:
        return jsonify({"Error": "Incorrect UUID format"}), 400

    if event is None:
        return jsonify({"Error": "Event not found"}), 404

    return jsonify(event.create_dictionary()), 200


@event_bp.route("/create-event", methods=["POST"])
def create_event_route():
    data = request.get_json()
    input_checks = validate_event_data(data)

    if input_checks is False:
        return jsonify({"Error": "Missing required fields"}), 400

    device_uuid = check_valid_uuid(data.get("device_uuid"))

    if not device_uuid:
        return jsonify({"Error": "Incorrect UUID format"}), 400

    metadata = validate_metadata(data.get("event_metadata"))

    if not metadata:
        return jsonify({"Error": "Incorrect metadata format"}), 400

    category = validate_category_exists(data)

    if not category:
        return jsonify({"Error": "Invalid category"}), 422

    new_event = create_event(category.id, data.get("device_uuid"), data.get("recorded_at"), data.get("event_metadata"))

    return jsonify({
        "uuid": new_event.uuid,
        "recorded_at": new_event.recorded_at,
        "received_at": new_event.received_at,
        "created_at": new_event.created_at,
        "updated_at": new_event.updated_at,
        "category_id": new_event.category_id,
        "device_uuid": new_event.device_uuid,
        "event_metadata": new_event.event_metadata,
        "notification_sent": new_event.notification_sent,
        "is_deleted": new_event.is_deleted
    }), 200


@event_bp.route("/update-event/<uuid>", methods=["PUT", "PATCH"])
def update_event(uuid):
    data = request.get_json()

    # Validate input
    if "notification_sent" not in data:
        return jsonify({"Error": "Missing 'notification_sent' in request body"}), 400

    event = update_notification_sent(uuid)

    if event is None:
        return jsonify({"Error": "Event does not exist"}), 404

    elif event == 'already_true':
        return jsonify({"Error": "notification_sent is already True"}), 422

    return jsonify({
        "uuid": str(event.uuid),
        "recorded_at": event.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
        "received_at": event.received_at.strftime("%Y-%m-%d %H:%M:%S"),
        "created_at": event.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": event.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "category_id": event.category_id,
        "category_name": event.category.name,
        "device_uuid": event.device_uuid,
        "metadata": validate_metadata(event.metadata),
        "notification_sent": event.notification_sent,
        "is_deleted": event.is_deleted
    }), 200


@event_bp.route("/delete-event/<uuid>", methods=["DELETE"])
def delete_event(uuid):
    valid_uuid = check_valid_uuid(uuid)
    event_deleted_status = delete_event_by_uuid(uuid)

    if not valid_uuid:
        return jsonify({"Error": "Incorrect UUID format"}), 400

    elif event_deleted_status is None:
        return jsonify({"Error": "Event does not exist"}), 404

    elif event_deleted_status == "already_deleted":
        return jsonify({"Error": "Event already deleted"}), 422

    return jsonify({"message": "Event deleted successfully"}), 204
