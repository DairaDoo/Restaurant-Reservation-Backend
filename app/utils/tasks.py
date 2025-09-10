from datetime import datetime, timedelta, timezone
from app.models import Reservation, Table
from app.utils.db import db


def free_reserved_tables(app):
    """
    Libera las mesas reservadas que tengan más de 3 horas desde la reserva confirmada.
    Debe recibir la instancia de la app para usar el app_context.
    """
    with app.app_context():
        now = datetime.now(timezone.utc)
        three_hours_ago = now - timedelta(hours=3)

        # Obtener reservas confirmadas con fecha y hora menor o igual a tres horas atrás
        reservations = Reservation.query.filter(
            Reservation.is_confirmed.is_(True),
            Reservation.date <= three_hours_ago.date(),
            Reservation.time <= three_hours_ago.time(),
        ).all()

        # Liberar mesas asociadas
        for reservation in reservations:
            table = db.session.get(Table, reservation.table_id)
            if table:
                table.is_reserved = False
                db.session.add(table)

        db.session.commit()
