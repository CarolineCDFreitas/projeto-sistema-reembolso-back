from flask import Blueprint, request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from

from src.model import db
from src.model.colaborador_model import Colaborador
from src.utils.identificadores import gerar_id_ulid
from src.schemas.colaborador_validation.login_colaborador import (
ValidarLoginColaborador
)
from src.schemas.colaborador_validation.cadastrar_colaborador import (
    ValidarCadastroColaborador
)

from src.security.security import hash_senha, checar_senha

bp_colaborador = Blueprint("colaborador", __name__, url_prefix="/colaborador")


@bp_colaborador.route("/todos-colaboradores", methods=["GET"])
@swag_from("../docs/colaborador/dados_todos_colaboradores.yml")
def pegar_dados_todos_colaboradores():

    todos_dados = db.session.scalars(select(Colaborador)).all()
    dados = [colaborador.colaborador_info() for colaborador in todos_dados]

    return jsonify(dados), 200


@bp_colaborador.route("/cadastrar", methods=["POST"])
@swag_from("../docs/colaborador/cadastrar_colaborador.yml")
def cadastrar_colaborador():
    dados_requisicao = request.get_json()

    try:
        validar_dados = ValidarCadastroColaborador()
        dados_validados = validar_dados.load(dados_requisicao)

        email_validado = dados_validados.get("email_cadastro")

        colaborador = db.session.scalar(
            select(Colaborador).where(Colaborador.email == email_validado)
        )

        if colaborador:
            return (
                jsonify(
                    {
                        "mensagem": "Email já cadastrado. Verifique sua conta ou insira um email válido."
                    }
                ),
                400,
            )

        else:
            novo_colaborador = Colaborador(
                id=gerar_id_ulid(),
                nome=dados_validados.get("nome_completo_cadastro"),
                email=email_validado,
                senha=hash_senha(dados_validados.get("senha_cadastro")),
                cargo=dados_validados.get("cargo"),
                salario=Decimal(dados_validados.get("salario")),
            )

            db.session.add(novo_colaborador)
            db.session.commit()

            return jsonify({"mensagem": "Colaborador cadastrado com sucesso!"}), 201

    except ValidationError as e:
        return jsonify({"erros": e.messages}), 400

    except SQLAlchemyError as e:
        return jsonify({"mensagem": "Erro no processamento. Tente mais tarde."}), 500

    except Exception as e:
        return jsonify({"mensagem": "Ocorreu um erro inesperado."}), 500


@bp_colaborador.route("/login", methods=["POST"])
def login():

    dados_requisicao = request.get_json()

    try:
        validar_dados = ValidarLoginColaborador()
        dados_validados = validar_dados.load(dados_requisicao)

        email = dados_validados.get("email")
        senha = dados_validados.get("senha")

        colaborador = db.session.scalar(
            select(Colaborador).where(Colaborador.email == email)
        )

        if not colaborador:
            return jsonify({"mensagem": "O usuário não foi encontrado."}), 404

        if checar_senha(senha, colaborador.senha):

            token_acesso = create_access_token(colaborador.id)
            token_atualizar = create_refresh_token(colaborador.id)
            return (
                jsonify(
                    {"mensagem": "Login realizado com sucesso!",
                    "tokens": {"acesso": token_acesso, "refresh": token_atualizar},
                }),
                200,
            )
        else:
            return jsonify({"mensagem": "Email e/ou senha incorreto(s)."}), 401

    except ValidationError as e:
        return jsonify({"erros": e.messages}), 400

    except SQLAlchemyError as e:
        return jsonify({"mensagem": "Erro no banco de dados."}), 500

    except Exception as e:
        return jsonify({"mensagem": f"Ocorreu um erro inesperado: {str(e)}."}), 500

@bp_colaborador.route("/info", methods=["GET"])
@jwt_required()
def colaborador_info():
    colaborador = db.session.scalar(select(Colaborador).where(Colaborador.id == get_jwt_identity()))
    
    if not colaborador:
        return jsonify({"mensagem": "Colaborador não encontrado"}), 404
    
    dados_colaborador = colaborador.colaborador_profile_info()
    return jsonify(dados_colaborador), 200