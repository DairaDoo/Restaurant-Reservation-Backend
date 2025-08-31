from datetime import datetime, timedelta
from app.models import Reservation, Table
from app.utils.db import db


def free_reserved_tables(app):
    """
    Libera las mesas reservadas que tengan más de 3 horas desde la reserva confirmada.
    Debe recibir la instancia de la app para usar el app_context.
    """
    with app.app_context():
        now = datetime.utcnow()
        three_hours_ago = now - timedelta(hours=3)

        # Obtener reservas confirmadas que tengan más de 3 horas
        reservations = Reservation.query.filter(
            Reservation.date <= three_hours_ago.date(),
            Reservation.time <= three_hours_ago.time(),
            Reservation.is_confirmed == True,
        ).all()

        # Liberar mesas asociadas a esas reservas
        for reservation in reservations:
            table = Table.query.get(reservation.table_id)
            if table:
                table.is_reserved = False
                db.session.add(table)

        db.session.commit()
