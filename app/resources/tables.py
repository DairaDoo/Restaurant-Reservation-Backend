from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import Table
from app.schemas.table import TableSchema
from app.utils import db

blp = Blueprint('Tables', 'tables', description="Operations on tables.")

@blp.route('/tables')
class GetOrCreateTable(MethodView):
    @blp.response(200, TableSchema(many=True))
    def get(self):
        """Get all Tables."""
        tables = Table.query.all()
        return tables
    
    @blp.arguments(TableSchema)  # Solo necesita table_capacity
    @blp.response(201, TableSchema)
    def post(self, table_data):
        """Creates a new table"""
        # Se omite la validación del table_number, ya que se generará automáticamente
        table = Table(table_capacity=table_data["table_capacity"])
        
        db.session.add(table)
        db.session.commit()
        
        return TableSchema().dump(table), 201

@blp.route("/tables/<int:table_id>")
class GetTableDetails(MethodView):
    @blp.response(200, TableSchema)
    def get(self, table_id):
        """Get a specific table details."""
        table = Table.query.get_or_404(table_id)
        return table
    
    @blp.response(200)
    def delete(self, table_id):
        """Delete a specific table."""
        table = Table.query.get_or_404(table_id)
        db.session.delete(table)
        db.session.commit()
        
        return {"message": "Table deleted successfully."}, 200    
    
    @blp.arguments(TableSchema)
    @blp.response(200, TableSchema)
    def put(self, table_data, table_id):
        """Update specific table."""
        table = Table.query.get_or_404(table_id)
        table.table_capacity = table_data["table_capacity"]
        
        db.session.add(table)
        db.session.commit()
        
        return TableSchema().dump(table), 200
