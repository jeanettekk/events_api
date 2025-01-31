from app import db
from app.models import Event


def test_create_event(client, db_session, setup_categories):
    event_data = {
        "category": "DeviceOverheating",
        "device_uuid": "2345e946-8ebe-484e-818f-6b94887288e2",
        "recorded_at": "2023-01-30 14:00:00",
        "event_metadata": {"warning_temperature": True}
    }

    response = client.post("/create-event", json=event_data)
    assert response.status_code == 200
    assert response.json["device_uuid"] == "2345e946-8ebe-484e-818f-6b94887288e2"
    assert response.json["category"] == "DeviceOverheating"
    assert response.json["metadata"] == {"warning_temperature": True}


def test_get_event_by_uuid(client, db_session, setup_categories):
    new_event = Event(
        uuid="550e8400-e29b-41d4-a716-446655440000",
        recorded_at="2024-01-30 14:00:00",
        received_at="2024-01-30 14:00:00",
        category_id=1,
        device_uuid="60e9e946-8ebe-484e-818f-6b94887288e2",
        event_metadata={},
        notification_sent=False,
        is_deleted=False
    )
    db.session.add(new_event)
    db.session.commit()

    response = client.get(f"/event/{new_event.uuid}")
    assert response.status_code == 200
    assert response.json["uuid"] == new_event.uuid
    assert response.json["category"] == "DeviceOnline"
    assert response.json["metadata"] == {}


def test_get_all_events(client, db_session, setup_categories):
    event1 = Event(
        uuid="550e8400-e29b-41d4-a716-446655440000",
        recorded_at="2024-01-30 14:00:00",
        received_at="2024-01-30 14:05:00",
        created_at="2024-01-30 14:10:00",
        updated_at="2024-01-30 14:15:00",
        category_id=1,
        device_uuid="60e9e946-8ebe-484e-818f-6b94887288e2",
        event_metadata={},
        notification_sent=False,
        is_deleted=False
    )

    event2 = Event(
        uuid="3d5935c3-8d07-4d35-b0cb-924b73e6e6e1",
        recorded_at="2024-01-31 10:00:00",
        received_at="2024-01-31 10:05:00",
        created_at="2024-01-31 10:10:00",
        updated_at="2024-01-31 10:15:00",
        category_id=2,
        device_uuid="12bd9102-1491-4b9e-9ace-68353f0489f3",
        event_metadata={"warning_temperature": True},
        notification_sent=True,
        is_deleted=False
    )

    db_session.add_all([event1, event2])
    db_session.commit()

    response = client.get("/events")
    assert response.status_code == 200

    events = response.json
    assert len(events) == 2  # Check how many events returned
    # event1
    assert events[0]["uuid"] == "550e8400-e29b-41d4-a716-446655440000"
    assert events[0]["device_uuid"] == "60e9e946-8ebe-484e-818f-6b94887288e2"
    assert events[0]["metadata"] == {}
    # event2
    assert events[1]["uuid"] == "3d5935c3-8d07-4d35-b0cb-924b73e6e6e1"
    assert events[1]["device_uuid"] == "12bd9102-1491-4b9e-9ace-68353f0489f3"
    assert events[1]["metadata"] == {"warning_temperature": True}


def test_update_event(client, db_session, setup_categories):
    new_event = Event(
        uuid="550e8400-e29b-41d4-a716-446655440000",
        recorded_at="2024-01-30 14:00:00",
        received_at="2024-01-30 14:05:00",
        created_at="2024-01-30 14:10:00",
        updated_at="2024-01-30 14:15:00",
        category_id=1,
        device_uuid="12bd9102-1491-4b9e-9ace-68353f0489f3",
        event_metadata={},
        notification_sent=False,
        is_deleted=False
    )

    db_session.add(new_event)
    db_session.commit()

    update_data = {"notification_sent": True}
    response = client.put(f"/update-event/{new_event.uuid}", json=update_data)

    assert response.status_code == 200


def test_delete_event(client, db_session, setup_categories):

    new_event = Event(
        uuid="550e8400-e29b-41d4-a716-446655440000",
        recorded_at="2024-01-30 14:00:00",
        received_at="2024-01-30 14:05:00",
        created_at="2024-01-30 14:10:00",
        updated_at="2024-01-30 14:15:00",
        category_id=2,
        device_uuid="12bd9102-1491-4b9e-9ace-68353f0489f3",
        event_metadata={"critical_temperature": True},
        notification_sent=False,
        is_deleted=False
    )

    db_session.add(new_event)
    db_session.commit()

    response = client.delete(f"/delete-event/{new_event.uuid}")

    assert response.status_code == 204
