from flasgger import Swagger
from src.docs.config import swagger_config

def init_docs(app):
    Swagger(app, config=swagger_config)