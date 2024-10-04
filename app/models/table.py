from app.utils.db import db

class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    table_number = db.Column(db.Integer, unique=True, nullable=False)  # Número de mesa
    table_capacity = db.Column(db.Integer, nullable=False)  # Capacidad de la mesa
    is_reserved = db.Column(db.Boolean, default=False)  # Si está reservada

    def __init__(self, table_capacity):
        self.table_capacity = table_capacity
        # Asigna el número de mesa automáticamente al crear una nueva mesa
        last_table = Table.query.order_by(Table.table_number.desc()).first()
        self.table_number = last_table.table_number + 1 if last_table else 1
