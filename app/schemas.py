from marshmallow import EXCLUDE
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchemaOpts, SQLAlchemyAutoSchema

from app import db
from app.models import User, Profile, Like, Dislike, Post


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session
        if not hasattr(meta, "unknown"):
            meta.unknown = EXCLUDE
        if not hasattr(meta, "load_instance"):
            meta.load_instance = True
        if not hasattr(meta, "include_fk"):
            meta.include_fk = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseOpts


class ProfileSchema(BaseSchema):
    class Meta:
        model = Profile


class LikeSchema(BaseSchema):
    class Meta:
        model = Like


class DislikeSchema(BaseSchema):
    class Meta:
        model = Dislike


class PostSchema(BaseSchema):
    class Meta:
        model = Post


class UserSchema(BaseSchema):
    class Meta:
        model = User

    profile = Nested(ProfileSchema(), many=False)
