import click
from flask import Blueprint
from faker import Faker

from app import db
from app.models import User, Profile

bp = Blueprint('fake', __name__)
faker = Faker()


@bp.cli.command("users")
@click.argument('num', type=int)
def users(num):
    users = []
    for i in range(num):
        username = faker.user_name()
        email = faker.email()

        user = User.query.filter_by(username=username, email=email).first()
        if not user:
            user = User(
                username=username,
                email=email
            )
            db.session.add(user)

            profile = Profile(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                user_id=faker.user_id()
            )
            db.session.add(profile)
            users.append(user)

    db.session.commit()
    print(num, 'users added.')
