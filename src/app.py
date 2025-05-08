from flask import Flask
from config import Config

from src.model import db
from src.security import bycrypt
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso


def create_app():
    app = Flask(__name__)

    bycrypt.init_app(app)
    
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
