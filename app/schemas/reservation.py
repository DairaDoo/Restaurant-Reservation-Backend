# app/schemas/reservation.py
from marshmallow import Schema, fields

class ReservationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    table_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    people_quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_confirmed = fields.Bool()

class ReservationCreationSchema(Schema):
    table_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    people_quantity = fields.Int(required=True)
