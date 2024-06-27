from app.utils.db import db
from datetime import datetime, timezone

class Reservation(db.Model):
    __tablename__ = "reservations"  # explicit table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    table = db.relationship('Table', backref=db.backref('reservations', lazy=True))
