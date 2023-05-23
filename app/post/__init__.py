from pathlib import Path

import click
import pandas as pd
from flask import Blueprint

import config
from ..models import User, Post

bp = Blueprint('post', __name__, url_prefix='/post')

from . import routes  # noqa


@bp.cli.command('extract_posts')
@click.argument('user_id', type=int)
def extract_posts(user_id):
    # user_id = 56 to write user_id that you want you need to write in terminal or configuration:
    #            flask post extract_posts USER_ID
    post_data = []
    user = User.query.get(user_id)
    if user:
        post_info = Post.query.filter_by(author_id=user_id).all()
    for post in post_info:
        title = post.title
        likes = len(post.likes)
        dislikes = len(post.dislikes)
        created = post.created_at
        post_data.append(
            {
                'Posts title': title,
                'Likes count': likes,
                'Dislikes count': dislikes,
                'Post created at': created
            }
        )

    df = pd.DataFrame.from_dict(post_data)
    output_file_path = Path(config.basedir) / f'{user.username}_extract_posts.csv'
    df.to_csv(output_file_path)
