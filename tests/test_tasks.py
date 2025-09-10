import pytest
from datetime import datetime, timedelta, timezone
from app.models import Table, Reservation
from app.utils.tasks import free_reserved_tables
from app.utils.db import db

@pytest.fixture
def table(app):
    """Crea una mesa de prueba dentro del contexto de la app."""
    with app.app_context():
        t = Table(table_capacity=4)
        t.is_reserved = True
        db.session.add(t)
        db.session.commit()
        db.session.refresh(t)
        return t

@pytest.fixture
def reservation_factory(app):
    """Factory fixture para crear reservas en diferentes escenarios."""
    def _create(table, hours_offset=0, confirmed=True):
        with app.app_context():
            dt = datetime.now(timezone.utc) - timedelta(hours=hours_offset)
            r = Reservation(
                table_id=table.id,
                date=dt.date(),
                time=dt.time(),
                people_quantity=2,
                is_confirmed=confirmed
            )
            db.session.add(r)
            db.session.commit()
            db.session.refresh(r)
            return r
    return _create

def test_free_reserved_tables_releases_old_reservation(app, table, reservation_factory):
    old_reservation = reservation_factory(table, hours_offset=4, confirmed=True)
    with app.app_context():
        assert table.is_reserved is True
        free_reserved_tables(app)
        updated_table = db.session.get(Table, table.id)
        assert updated_table.is_reserved is False

def test_free_reserved_tables_keeps_recent_reservation(app, table, reservation_factory):
    recent_reservation = reservation_factory(table, hours_offset=1, confirmed=True)
    with app.app_context():
        free_reserved_tables(app)
        updated_table = db.session.get(Table, table.id)
        assert updated_table.is_reserved is True

def test_free_reserved_tables_ignores_unconfirmed(app, table, reservation_factory):
    unconfirmed_reservation = reservation_factory(table, hours_offset=4, confirmed=False)
    with app.app_context():
        free_reserved_tables(app)
        updated_table = db.session.get(Table, table.id)
        assert updated_table.is_reserved is True
