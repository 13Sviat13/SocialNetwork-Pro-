from flask import Blueprint
from flask_restful import Api

from .dislike import DisLikesResource, DisLikeResource
from .like import LikesResource, LikeResource
from .profile import ProfileResource
from .token_auth import GenTokenResource
from .user import UsersResource, UserResource
from .posts import PostsResource, PostResource


bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(UsersResource, '/users', endpoint="user_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="users_details")
api.add_resource(ProfileResource, '/profile/<int:user_id>', endpoint='profile_user')
api.add_resource(PostsResource, '/posts', endpoint='posts_list')
api.add_resource(PostResource, '/posts/<int:post_id>', endpoint='post_details')
api.add_resource(LikesResource, '/likes', endpoint='likes_list')
api.add_resource(LikeResource, '/likes/<int:like_id>', endpoint='like_detail')
api.add_resource(DisLikesResource, '/dislikes', endpoint='dislikes_list')
api.add_resource(DisLikeResource, '/dislikes/<int:dislike_id>', endpoint='dislike_detail')
api.add_resource(GenTokenResource, '/gen_token', endpoint='gen_token')
