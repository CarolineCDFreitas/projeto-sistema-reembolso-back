from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config():
    SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV")
    SQLACLHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")