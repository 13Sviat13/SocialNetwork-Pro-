from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel, UserMixin):
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)

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
        nullable=False
    )
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    Linkedln_URL = db.Column(db.String)
    Facebook_URL = db.Column(db.String)

    user = db.relationship("User", backref="profile", uselist=False)
