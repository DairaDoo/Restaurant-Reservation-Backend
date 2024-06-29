from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from app.models import Table
from app.schemas.table import TableSchema
from app.utils import db

blp = Blueprint('Tables', 'tables', description = "Operations on tables.")


@blp.route('/tables')
class TableList(MethodView):
    blp.response(200, TableSchema(many=True))
    def get(self):
        tables = Table.query.all()
        return tables
    

        

