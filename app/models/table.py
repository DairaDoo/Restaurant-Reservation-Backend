from app.utils.db import db

class Table(db.Model):
    __tablename__ = "tables"  # explicit table name

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    table_capacity = db.Column(db.Integer, nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)  # New field
