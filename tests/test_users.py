from app.models.user import User
from app.utils.db import db


def test_create_user(client, app):
    """Prueba la creación de un usuario válido."""
    new_user = {
        "first_name": "Dairan",
        "last_name": "Mora",
        "phone_number": "123456789",
        "email": "test@example.com",
    }
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "test@example.com"

    with app.app_context():
        assert db.session.query(User).count() == 1


def test_create_duplicate_user(client):
    """Prueba que no se permitan duplicados por email."""
    user_data = {
        "first_name": "Ana",
        "last_name": "Lopez",
        "phone_number": "111111111",
        "email": "dup@example.com",
    }
    client.post("/users", json=user_data)
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.get_json()["message"]


def test_get_users(client):
    """Prueba obtener lista de usuarios."""
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
