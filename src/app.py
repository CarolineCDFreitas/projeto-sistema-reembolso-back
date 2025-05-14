from flask import Flask
from config import Config
from flask_cors import CORS

from src.model import db
from src.security import bcrypt
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.auth import jwt
from src.docs import init_docs

def create_app():
    app = Flask(__name__)

    bcrypt.init_app(app)

    CORS(
        app,
        resources={
            r"/colaborador/*": {
                "origins": [
                    "http://localhost:3000",
                    "https://sisparproject.netlify.app",
                ]
            },
            r"/reembolso/*": {
                "origins": [
                    "http://localhost:3000",
                    "https://sisparproject.netlify.app",
                ]
            },
        },
    )

    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    
    init_docs(app)

    with app.app_context():
        db.create_all()

    return app
