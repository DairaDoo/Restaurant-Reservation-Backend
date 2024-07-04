import os
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .utils.db import db
from .resources.tables import blp as TableBlueprint
from .resources.reservation import blp as ReservationBlueprint
from .resources.user import blp as UserBlueprint
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.models import Reservation, Table
from flask_cors import CORS  # Importa Flask-CORS
from flask_mail import Mail, Message  # Import Flask-Mail

load_dotenv()

def free_reserved_tables():
    now = datetime.utcnow()
    with create_app().app_context():
        three_hours_ago = now - timedelta(hours=3)
        reservations = Reservation.query.filter(
            Reservation.date <= three_hours_ago.date(),
            Reservation.time <= three_hours_ago.time(),
            Reservation.is_confirmed == True
        ).all()
        for reservation in reservations:
            table = Table.query.get(reservation.table_id)
            if table:
                table.is_reserved = False
                db.session.add(table)
        db.session.commit()

def create_app(db_url=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    app.config["API_TITLE"] = "Restaurant Reservations API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Configuración de Flask-Mail
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.example.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "false").lower() in ["true", "on", "1"]
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    mail = Mail(app)  # Inicializa Flask-Mail
    CORS(app)  # Configura CORS

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TableBlueprint)
    api.register_blueprint(ReservationBlueprint)
    
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=free_reserved_tables, trigger="interval", minutes=1)
        scheduler.start()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
