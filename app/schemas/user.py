# Los schemas se usan para validar la data recibida, serializarla y deselearizarla.

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required = True)
    email = fields.Email(required = True)
    password = fields.Str(load_only = True, required = True)

class UserRegistrationSchema(Schema):
    username = fields.Str(required = True)
    email = fields.Email(required = True)
    password = fields.Str(required = True)
    
class UserLoginSchema(Schema):
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)
    