from flask import Flask
from config import Config
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrade = Migrate()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrade.init_app(app, db)
    login_manager.init_app(app)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from fake import bp as fake_bp
    app.register_blueprint(fake_bp)

    from . import models  # imported models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)

    @app.context_processor
    def context_processor():
        return dict(
            current_user=current_user
        )

    return app


app = create_app()

from .main import routes  # noqa
