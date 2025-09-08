import json
from unittest.mock import patch
from app.models.table import Table
from app.models.reservation import Reservation
from app.models.user import User
from app.utils.db import db


# helper: create a table
def _create_table(app, capacity=4):
    with app.app_context():
        t = Table(table_capacity=capacity)
        db.session.add(t)
        db.session.commit()
        return t.id  # devolvemos solo el id


def test_get_available_tables(client, app):
    t_id = _create_table(app, capacity=4)
    resp = client.get("/tables/available/4")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    # check returned has our created table (by capacity or id)
    assert any(item.get("table_capacity", None) >= 4 for item in data)


def test_create_reservation_provisional(client, app):
    t_id = _create_table(app, capacity=4)
    payload = {
        "table_id": t_id,
        "date": "2025-09-10",
        "time": "18:00:00",
        "people_quantity": 4,
    }
    resp = client.post("/reservations", json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["table_id"] == t_id
    # DB checks
    with app.app_context():
        r = Reservation.query.filter_by(table_id=t_id).first()
        assert r is not None
        with db.session() as session:
            t_db = session.get(Table, t_id)
        assert t_db.is_reserved is True


def test_create_reservation_conflict(client, app):
    t_id = _create_table(app, capacity=4)
    payload = {
        "table_id": t_id,
        "date": "2025-09-10",
        "time": "18:00:00",
        "people_quantity": 4,
    }
    resp1 = client.post("/reservations", json=payload)
    assert resp1.status_code == 201
    resp2 = client.post("/reservations", json=payload)
    assert resp2.status_code == 400
    assert "already exists" in resp2.get_json().get("message", "").lower()


def test_create_reservation_no_table(client, app):
    # no table created with capacity 10
    payload = {
        "table_id": 9999,  # non-existing
        "date": "2025-09-10",
        "time": "18:00:00",
        "people_quantity": 10,
    }
    resp = client.post("/reservations", json=payload)
    assert resp.status_code in (400, 404)  # endpoint returns 404 if no table found


def test_confirm_reservation_creates_user_and_sends_email(client, app):
    t_id = _create_table(app, capacity=4)
    payload = {
        "table_id": t_id,
        "date": "2025-09-11",
        "time": "19:00:00",
        "people_quantity": 4,
    }
    # create provisional reservation
    resp = client.post("/reservations", json=payload)
    assert resp.status_code == 201
    reservation_id = resp.get_json()["id"]

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "555-0000",
        "email": "confirm@example.com",
    }

    # patch Mail.send to avoid real send and capture message
    with patch("app.resources.reservation.Mail.send") as mock_send:
        resp_confirm = client.put(
            f"/reservations/{reservation_id}/confirm", json=user_data
        )
        assert resp_confirm.status_code == 200

        # DB assertions usando session.get()
        with app.app_context():
            with db.session() as session:
                r = session.get(Reservation, reservation_id)
                assert r.is_confirmed is True
                assert r.user_id is not None
                u = session.get(User, r.user_id)
                assert u.email == "confirm@example.com"

        # mail assertions
        assert mock_send.called
        call_args = mock_send.call_args[0]
        msg = call_args[1] if len(call_args) > 1 else call_args[0]
        assert "Reservation Confirmation" in msg.subject
        assert "confirm@example.com" in getattr(
            msg, "recipients", []
        ) or "confirm@example.com" in getattr(msg, "to", [])


def test_delete_reservation_unreserves_table(client, app):
    t_id = _create_table(app, capacity=4)
    payload = {
        "table_id": t_id,
        "date": "2025-09-12",
        "time": "20:00:00",
        "people_quantity": 4,
    }
    resp = client.post("/reservations", json=payload)
    assert resp.status_code == 201
    reservation_id = resp.get_json()["id"]

    del_resp = client.delete(f"/reservations/{reservation_id}")
    assert del_resp.status_code == 200
    with app.app_context():
        with db.session() as session:
            t_db = session.get(Table, t_id)
            assert t_db.is_reserved is False
            assert session.get(Reservation, reservation_id) is None
