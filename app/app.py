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
from flask_cors import CORS
from flask_mail import Mail
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    Mail(app)
    CORS(app)

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TableBlueprint)
    api.register_blueprint(ReservationBlueprint)

    return app
