from flask import jsonify, request
from flask_restful import Resource

from app import db
from app.models import Dislike
from app.schemas import DislikeSchema
from app.services import DislikeService

dislike_service = DislikeService()


class DisLikesResource(Resource):
    def get(self):
        dislikes = db.session.query(Dislike).all()
        return jsonify(DislikeSchema().dump(dislikes, many=True))

    def post(self):
        json_data = request.get_json()
        user_id = json_data['user_id']
        post_id = json_data['post_id']
        dislike = dislike_service.check_dislike_post_by_user(post_id, user_id)
        if dislike:
            response = jsonify(error='You have already dislike this post')
            response.status_code = 400
            return response
        else:
            set_dislike = dislike_service.create(json_data)
            return jsonify(DislikeSchema().dump(set_dislike, many=False))


class DisLikeResource(Resource):
    def get(self, dislike_id):
        dislike = db.session.query(Dislike).filter(Dislike.id == dislike_id).first()
        return jsonify(DislikeSchema().dump(dislike, many=False))
