from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import User
from app.schemas.user import UserSchema, UserRegistrationSchema
from app.utils import db

blp = Blueprint("Users", "users", description="Operations on Users.")

@blp.route("/users")
class GetOrCreateUser(MethodView):
    """General operations to create or get all users."""

    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get all Users."""
        users = User.query.all()  # get all users from db
        return users
    
    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a user if it's not registered."""
        if User.query.filter_by(email=user_data["email"]).first():
            abort(400, message="A user with the same email already exists.")
        
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone_number=user_data["phone_number"],
            email=user_data["email"]
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user, 201

@blp.route("/users/<int:user_id>")
class GetUserDetails(MethodView):
    """Specific User operations using ID."""

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get a specific User."""
        user = User.query.get_or_404(user_id)
        return user
    
    @blp.response(200, UserSchema)
    def delete(self, user_id):
        """Delete a specific User."""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User deleted successfully."}
