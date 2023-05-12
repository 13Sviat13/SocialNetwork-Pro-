from datetime import datetime
from hashlib import md5

from sqlalchemy.ext.hybrid import hybrid_property # noqa
from sqlalchemy.orm import joinedload # noqa

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel, UserMixin):
    __tablename__ = "user"
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    posts = db.relationship(
        "Post", backref="author", uselist=True, lazy="dynamic", cascade="all, delete"
    )
    likes = db.relationship(
        "Like", backref="user",  lazy="dynamic", primaryjoin='User.id==Like.user_id', cascade="all, delete"
    )
    dislikes = db.relationship(
        "Dislike", backref="user",  lazy="dynamic", primaryjoin='User.id==Dislike.user_id', cascade="all, delete"
    )
    followers = db.relationship(
        "Follow", backref="followee", foreign_keys="Follow.followee_id"
    )
    following = db.relationship(
        "Follow", backref="follower", foreign_keys="Follow.follower_id"
    )

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar{digest}?d=identicon&s={size}'

    def is_to_subscribed(self, user):
        return Follow.query.filter_by(follower_id=self.id, followee_id=user.id).first()

    def __repr__(self):
        return f"{self.username}({self.email})"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    __tablename__ = "profiles"
    __table_args__ = (
        db.Index("idx_profiles_user_id", "user_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_profiles_user_id"),
        nullable=False,
    )
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    bio = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    linkedin = db.Column(db.String)
    facebook = db.Column(db.String)

    user = db.relationship("User", backref=db.backref("profile", uselist=False), uselist=False)


class Post(BaseModel):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
            db.Integer,
            db.ForeignKey("user.id", name="fk_posts-author_id", ondelete="CASCADE"),
            nullable=False
    )

    likes = db.relationship("Like", backref="post", uselist=True, cascade="all,delete")
    dislikes = db.relationship("Dislike", backref="post", uselist=True, cascade="all,delete")


class Like(BaseModel):
    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_likes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", name="fk_likes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dislike(BaseModel):
    __tablename__ = "dislikes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_dislikes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", name="fk_dislikes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_follows_follower_id"),

        primary_key=True
    )
    followee_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_follows_followee_id"),
        primary_key=True

    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
