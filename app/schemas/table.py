from marshmallow import Schema, fields

class TableSchema(Schema):
    id = fields.Int(dump_only=True)  # Identificador de salida
    table_number = fields.Int(dump_only=True)  # Número de mesa, solo de salida
    table_capacity = fields.Int(required=True)  # Capacidad de la mesa, requerido
    is_reserved = fields.Boolean(dump_only=True)  # Estado de reserva, solo de salida
