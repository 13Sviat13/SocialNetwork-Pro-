from flask import jsonify, request
from flask_restful import Resource
from app import db
from app.models import Profile
from app.schemas import ProfileSchema
from app.services import ProfileService

profile_service = ProfileService()


class ProfileResource(Resource):
    def get(self, user_id):
        profile = db.session.query(Profile).filter(Profile.user_id == user_id).first()
        return jsonify(ProfileSchema().dump(profile, many=False))

    def put(self, user_id):
        json_data = request.get_json()
        json_data['user_id'] = user_id
        update_profile = profile_service.update(json_data)
        return jsonify(ProfileSchema().dump(update_profile, many=False))
