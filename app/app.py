import os
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .utils.db import db
from .resources.tables import blp as TableBlueprint
# from .resources.reservation import blp as ReservationBluepritn
from .resources.user import blp as UserBlueprint
from dotenv import load_dotenv

load_dotenv()

def create_app(db_url=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    app.config["API_TITLE"] = "Restaurant Reservations API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TableBlueprint)
    # api.register_blueprint(ReservationBlueprint)

    return app
