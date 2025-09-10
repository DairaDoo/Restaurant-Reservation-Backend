import pytest
from app.models.table import Table
from app.utils import db

TABLES_ENDPOINT = "/tables"


def test_get_all_tables_empty(client):
    """GET /tables debe devolver lista vacía si no hay mesas."""
    resp = client.get(TABLES_ENDPOINT)
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_table_success(client, app):
    """POST /tables debe crear mesa correctamente."""
    resp = client.post(TABLES_ENDPOINT, json={"table_capacity": 4})
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["table_capacity"] == 4
    assert data["table_number"] == 1
    assert data["is_reserved"] is False

    # verificar persistencia en DB
    with app.app_context():
        table = Table.query.first()
        assert table is not None
        assert table.table_capacity == 4


def test_create_table_invalid_payload(client):
    """POST /tables con payload inválido debe devolver error de validación."""
    resp = client.post(TABLES_ENDPOINT, json={})
    assert resp.status_code in (400, 422)

    data = resp.get_json()
    assert data is not None


def test_get_table_details_success(client):
    """GET /tables/<id> debe devolver mesa existente."""
    resp = client.post(TABLES_ENDPOINT, json={"table_capacity": 2})
    table_id = resp.get_json()["id"]

    resp = client.get(f"{TABLES_ENDPOINT}/{table_id}")
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["id"] == table_id
    assert data["table_capacity"] == 2


def test_get_table_details_not_found(client):
    """GET /tables/<id> inexistente debe devolver 404."""
    resp = client.get(f"{TABLES_ENDPOINT}/999")
    assert resp.status_code == 404


def test_update_table_success(client):
    """PUT /tables/<id> debe actualizar la capacidad de la mesa."""
    resp = client.post(TABLES_ENDPOINT, json={"table_capacity": 3})
    table_id = resp.get_json()["id"]

    resp = client.put(f"{TABLES_ENDPOINT}/{table_id}", json={"table_capacity": 6})
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["table_capacity"] == 6


def test_update_table_not_found(client):
    """PUT /tables/<id> inexistente debe devolver 404."""
    resp = client.put(f"{TABLES_ENDPOINT}/999", json={"table_capacity": 4})
    assert resp.status_code == 404


def test_delete_table_success(client, app):
    """DELETE /tables/<id> debe eliminar mesa existente."""
    resp = client.post(TABLES_ENDPOINT, json={"table_capacity": 5})
    table_id = resp.get_json()["id"]

    resp = client.delete(f"{TABLES_ENDPOINT}/{table_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Table deleted successfully."

    with app.app_context():
        assert db.session.get(Table, table_id) is None


def test_delete_table_not_found(client):
    """DELETE /tables/<id> inexistente debe devolver 404."""
    resp = client.delete(f"{TABLES_ENDPOINT}/999")
    assert resp.status_code == 404
