from flask_restful import Resource
from app import db
from app.models import Post
from flask import jsonify, request
from app.schemas import PostSchema
from app.services import PostService

post_service = PostService()


class PostResource(Resource):
    def get(self, post_id):
        post = post_service.get_by_id(post_id)
        likes = post_service.get_likes(post_id)
        dislikes = post_service.get_dislikes(post_id)
        post_data = PostSchema().dump(post, many=False)
        post_data['likes'] = likes
        post_data['dislikes'] = dislikes
        return jsonify(post_data)

    def put(self, post_id):
        json_data = request.get_json()
        json_data['id'] = post_id
        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    def delete(self, post_id):
        post = post_service.delete(post_id)
        return jsonify(PostSchema().dump(post, many=False))

class PostsResource(Resource):
    def get(self):
        author_id = request.args.get('author_id', type=int)
        if author_id:
            posts = db.session.query(Post).filter(Post.author_id == author_id).all()
        else:
            posts = db.session.query(Post).all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self):
        json_data = request.get_json()
        post = post_service.create(**json_data)
        return jsonify(PostSchema().dump(post, many=False))



