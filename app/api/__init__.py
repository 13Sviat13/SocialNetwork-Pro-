from flask import Blueprint
from flask_restful import Api
from .user import UsersResource, UserResource


bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(UsersResource, '/users', endpoint="user_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="users_details")