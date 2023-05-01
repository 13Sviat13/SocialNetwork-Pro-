from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.cli.command("hello")
def hello():
    print("hello from cli")


from . import routes  # noqa
