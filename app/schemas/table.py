from marshmallow import Schema, fields

class TableSchema(Schema):
    id = fields.Int(dump_only = True)
    table_number = fields.Int(required = True)
    table_capacity = fields.Int(required = True)
    
    