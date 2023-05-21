from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import User
from app.schemas import UserSchema, PostSchema
from app.services import UserService, PostService

user_service = UserService()
post_service = PostService()

class UsersResource(Resource):
    def get(self):

        ordered = request.args.get('ordered', type=bool)

        users_query = db.session.query(User)
        if ordered:
            users_query = users_query.order_by(User.created_at.asc())

        users = users_query.all()
        return jsonify(UserSchema().dump(users, many=True))

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        user = user_service.create(**json_data)

        response = jsonify(UserSchema().dump(user, many=False))
        response.status_code = 201
        return response


class UserResource(Resource):
    def get(self, user_id=None):
        user = user_service.get_by_id(user_id)
        return jsonify(UserSchema().dump(user, many=False))

    @jwt_required()
    def put(self, user_id):
        json_data = request.get_json()
        json_data['id'] = user_id

        user = user_service.update(json_data)
        return jsonify(UserSchema().dump(user, many=False))

    jwt_required()
    def delete(self, user_id):
        status = user_service.delete(user_id)
        return jsonify(status=status)

class UsersPostResource(Resource):
    @jwt_required()
    def post(self, user_id):
        json_data = request.get_json()
        user_post = post_service.create_post_by_user_id(user_id, **json_data)
        return jsonify(UserSchema().dump(user_post, many=False))

    def get(self, user_id, post_id):
        post = post_service.get_spec_post_by_spec_user(user_id, post_id)
        likes = post_service.get_likes(post_id)
        dislikes = post_service.get_dislikes(post_id)
        post_data = PostSchema().dump(post, many=False)
        post_data['likes'] = likes
        post_data['dislikes'] = dislikes
        return jsonify(post_data)

    @jwt_required()
    def put(self, user_id, post_id):
        json_data = request.get_json()
        json_data['author_id'] = user_id
        json_data['id'] = post_id
        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    @jwt_required()
    def delete(self, user_id, post_id):
        data = post_service.delete_post_id_by_user_id(user_id, post_id)
        return jsonify(UserSchema().dump(data, many=False))