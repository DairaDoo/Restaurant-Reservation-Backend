import pytest
from app.app import create_app
from app.utils.db import db


@pytest.fixture
def app():
    """Crea una aplicación Flask en modo testing con DB en memoria."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "MAIL_SUPPRESS_SEND": True,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    """Provee un cliente de pruebas de Flask."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Provee un runner de CLI para la app."""
    return app.test_cli_runner()
