from flask import jsonify, request
from flask_restful import Resource
from app import db
from app.models import Like
from app.schemas import LikeSchema
from app.services import LikeService

like_service = LikeService()


class LikesResource(Resource):
    def get(self):
        likes = db.session.query(Like).all()
        return jsonify(LikeSchema().dump(likes, many=True))

    def post(self):
        json_data = request.get_json()
        post_id = json_data['post_id']
        user_id = json_data['user_id']
        like = like_service.check_like_post_by_user(post_id, user_id)
        if like:
            response = jsonify(error='You already like this post')
            response.status_code = 400
            return response
        else:
            new_like = like_service.create(json_data)
            return jsonify(LikeSchema().dump(new_like, many=False))


class LikeResource(Resource):
    def get(self, like_id):
        like = db.session.query(Like).filter(Like.id == like_id).first()
        return jsonify(LikeSchema().dump(like, many=False))
