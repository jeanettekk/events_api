from flask import Blueprint, request, jsonify

from services.event_service import create_event, get_event_by_uuid, get_all_events

event_bp = Blueprint("event_bp", __name__)


@event_bp.route("/events", methods=["GET"])
def get_events():
    events_list = get_all_events()

    if not events_list:
        return jsonify({"Error": "There are no events"}), 404

    return jsonify(events_list), 200


@event_bp.route("/event/<uuid>", methods=["GET"])
def get_event_by_uuid_route(uuid):
    event_data = get_event_by_uuid(uuid)

    if not event_data:
        return jsonify({"Error": "Event not found"}), 404

    return jsonify(event_data), 200


@event_bp.route("/create-event", methods=["POST"])
def create_event_route():
    data = request.get_json()

    # Validate input
    category_id = data.get("category_id")
    device_uuid = data.get("device_uuid")
    recorded_at = data.get("recorded_at")

    if not category_id or not device_uuid or not recorded_at:
        return jsonify({"Error": "Missing required fields"}), 400

    # Call service layer to create the event
    new_event = create_event(category_id, device_uuid, recorded_at, data.get("metadata"))

    if not new_event:
        return jsonify({"Error": "Invalid category_id"}), 422

    # Return this response
    return jsonify({
        "uuid": new_event.uuid,
        "recorded_at": new_event.recorded_at,
        "received_at": new_event.received_at,
        "created_at": new_event.created_at,
        "updated_at": new_event.updated_at,
        "category_id": new_event.category_id,
        "device_uuid": new_event.device_uuid,
        "metadata": new_event.metadata,
        "notification_sent": new_event.notification_sent,
        "is_deleted": new_event.is_deleted
    }), 201
