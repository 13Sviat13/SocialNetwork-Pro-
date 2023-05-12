import os
from dotenv import load_dotenv
import psycopg2  # noqa


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///network.db'
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DATABASE
    )
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    MAX_CONTENT_LENGTH = 16* 1024 * 1024

