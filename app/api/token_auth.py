from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from app import db
from app.models import User


class GenTokenResource(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']

        user = db.session.query(User).filter(User.username == username).first()
        if not user.check_password(password):
            response = jsonify(error='Username or password invalid')
            response.status_code = 400
            return response
        else:
            access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)