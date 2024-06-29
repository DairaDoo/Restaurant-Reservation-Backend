# app/schemas/user.py
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Email(required=True)

class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Email(required=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    phone_number = fields.Str(required=True)
