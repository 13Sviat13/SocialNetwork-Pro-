from pathlib import Path

from flask import Blueprint
import pandas as pd

import config
from .. import db
from ..models import User

bp = Blueprint('user', __name__, url_prefix='/user')

from . import routes  # noqa


@bp.cli.command('extract_users')
def extract_users():
    user_data = []
    user_info = db.session.query(User).all()
    for user in user_info:
        full_name = user.profile.full_name if user.profile else ' '
        user_data.append(
            {
                'username': user.username,
                'email': user.email,
                'full_name': full_name,
                'post_count': user.posts.count()
            }
        )

    df = pd.DataFrame.from_dict(user_data)
    output_file_path = Path(config.basedir) / 'extract_users.csv'
    df.to_csv(output_file_path)
