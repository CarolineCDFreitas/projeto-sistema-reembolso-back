from flask import Blueprint, request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


from src.model import db
from src.model.colaborador_model import Colaborador
from src.utils.identificadores import gerar_id_ulid
from src.schemas.colaborador_validation.login_colaborador import (
    validar_login_colaborador,
)

from src.security.security import hash_senha, checar_senha

bp_colaborador = Blueprint("colaborador", __name__, url_prefix="/colaborador")


@bp_colaborador.route("/todos-colaboradores", methods=["GET"])
def pegar_dados_todos_colaboradores():

    todos_dados = db.session.scalars(select(Colaborador)).all()
    dados = [colaborador.colaborador_info() for colaborador in todos_dados]

    return jsonify(dados), 200


@bp_colaborador.route("/cadastrar", methods=["POST"])
def cadastrar_colaborador():
    dados_requisicao = request.get_json()

    novo_colaborador = Colaborador(
        id=gerar_id_ulid(),
        nome=dados_requisicao.get("nome"),
        email=dados_requisicao.get("email"),
        senha=hash_senha(dados_requisicao.get("senha")),
        cargo=dados_requisicao.get("cargo"),
        salario=dados_requisicao.get("salario"),
    )

    db.session.add(novo_colaborador)
    db.session.commit()

    return jsonify({"mensagem": "Colaborador cadastrado com sucesso!"}), 201


@bp_colaborador.route("/login", methods=["POST"])
def login():

    dados_requisicao = request.get_json()

    try:
        validar_dados = validar_login_colaborador()
        dados_validados = validar_dados.load(dados_requisicao)

        email = dados_validados.get("email")
        senha = dados_validados.get("senha")

        colaborador = db.session.scalar(
            select(Colaborador).where(Colaborador.email == email)
        )

        if not colaborador:
            return jsonify({"mensagem": "O usuário não foi encontrado."}), 404

        if checar_senha(senha, colaborador.senha):
            return jsonify({"mensagem": "Login realizado com sucesso!"}), 200
        else:
            return jsonify({"mensagem": "Email e/ou senha incorreto(s)."}), 401

    except ValidationError as e:
        return jsonify({"erros": e.messages}), 400

    except SQLAlchemyError as e:
        return jsonify({"mensagem": "Erro no banco de dados."}), 500

    except Exception as e:
        return jsonify({"mensagem": f"Ocorreu um erro inesperado: {str(e)}."}), 500
