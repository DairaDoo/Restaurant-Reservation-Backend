from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask import request, current_app as app
from app.models import Reservation, Table, User
from app.schemas.reservation import ReservationSchema, ReservationCreationSchema
from app.schemas.table import TableSchema
from app.schemas.user import UserRegistrationSchema
from app.utils import db
from flask_mail import Mail, Message

blp = Blueprint('Reservations', 'reservations', description="Operations on reservations")

@blp.route('/tables/available/<int:people_quantity>')
class GetAvailableTables(MethodView):
    @blp.response(200, TableSchema(many=True))
    def get(self, people_quantity):
        """Get available tables based on people quantity"""
        tables = Table.query.filter(Table.table_capacity >= people_quantity, Table.is_reserved == False).all()
        return tables

@blp.route('/reservations')
class CreateReservation(MethodView):
    @blp.arguments(ReservationCreationSchema)
    @blp.response(201, ReservationSchema)
    def post(self, reservation_data):
        """Creates a provisional reservation"""
        existing_reservation = Reservation.query.filter_by(
            table_id=reservation_data["table_id"],
            date=reservation_data["date"],
            time=reservation_data["time"]
        ).first()
        
        if existing_reservation:
            abort(400, message="A reservation already exists for this table at the given date and time.")
        
        table = Table.query.filter(
            Table.id == reservation_data["table_id"],
            Table.table_capacity == reservation_data["people_quantity"]
        ).first()
        if not table:
            abort(404, message="No available table found for the given number of people.")
        
        reservation = Reservation(
            table_id=table.id,
            date=reservation_data["date"],
            time=reservation_data["time"],
            people_quantity=reservation_data["people_quantity"],
            is_confirmed=False  # Marking as provisional
        )
        
        table.is_reserved = True  # Mark table as reserved
        db.session.add(reservation)
        db.session.add(table)
        db.session.commit()
        
        return reservation, 201
    
    @blp.response(200, ReservationSchema(many=True))
    def get(self):
        """Get all reservations"""
        reservations = Reservation.query.all()
        return reservations

@blp.route('/reservations/<int:reservation_id>/confirm')
class ConfirmReservation(MethodView):
    @blp.arguments(UserRegistrationSchema)
    @blp.response(200, ReservationSchema)
    def put(self, user_data, reservation_id):
        """Confirms a provisional reservation with user data"""
        reservation = Reservation.query.get_or_404(reservation_id)
        if reservation.is_confirmed:
            abort(400, message="Reservation already confirmed.")
        
        # Verifica si el usuario ya existe por correo electrónico
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            # Actualiza la información del usuario con los nuevos datos proporcionados
            existing_user.first_name = user_data["first_name"]
            existing_user.last_name = user_data["last_name"]
            existing_user.phone_number = user_data["phone_number"]
            user = existing_user
        else:
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data["phone_number"],
                email=user_data["email"]
            )
            db.session.add(user)
            db.session.commit()
        
        # Asociar la reserva con el usuario y confirmar la reserva
        reservation.user_id = user.id
        reservation.is_confirmed = True
        db.session.add(reservation)
        db.session.commit()
        
        # Envía el correo electrónico de confirmación aquí, asegurándote de usar la información correcta del usuario
        self.send_confirmation_email(user, reservation)
        
        return reservation

    def send_confirmation_email(self, user, reservation):
        # Convertir la hora a formato de 12 horas
        time_24hr = datetime.strptime(reservation.time.strftime("%H:%M:%S"), "%H:%M:%S")
        time_12hr = time_24hr.strftime("%I:%M %p")

        email_subject = f"Reservation Confirmation for {user.first_name} {user.last_name}"
        email_body = f"""
        Dear {user.first_name} {user.last_name},

        Your reservation for {reservation.date} at {time_12hr} has been confirmed.
        
        Reservation details:
        - Table ID: {reservation.table_id}
        - Number of People: {reservation.people_quantity}

        Thank you for choosing our restaurant!

        Best regards,
        Restaurant Team
        """
        msg = Message(email_subject, recipients=[user.email])
        msg.body = email_body
        mail = Mail(app)
        mail.send(msg)

@blp.route('/reservations/<int:reservation_id>')
class DeleteReservation(MethodView):
    @blp.response(200, ReservationSchema)
    def delete(self, reservation_id):
        """Delete a reservation and update table reservation status"""
        reservation = Reservation.query.get_or_404(reservation_id)
        table = Table.query.get_or_404(reservation.table_id)
        
        db.session.delete(reservation)
        table.is_reserved = False
        db.session.add(table)
        db.session.commit()
        
        return {"message": "Reservation deleted successfully."}, 200
