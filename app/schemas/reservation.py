# app/schemas/reservation.py
from marshmallow import Schema, fields

class ReservationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    table_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    created_at = fields.DateTime(dump_only=True)

class ReservationCreationSchema(Schema):
    table_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
