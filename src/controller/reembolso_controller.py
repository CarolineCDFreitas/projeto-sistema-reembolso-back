from flask import Blueprint, request, jsonify
from sqlalchemy import select, exists, update, and_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from marshmallow import ValidationError


from src.model import db
from src.model.reembolso_model import Reembolso
from src.utils.identificadores import gerar_id_ulid, gerar_e_validar_unicidade_do_numero
from src.schemas.reembolso_serialization.retornar_reembolso import RetornarReembolso
from src.schemas.reembolso_validation.cadastrar_solicitacao import ValidarSolicitacaoReembolso

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")


@bp_reembolso.route("/cadastrar", methods=["POST"])
@jwt_required()
@swag_from("../docs/reembolso/cadastrar_solicitacao.yml")
def cadastrar_solicitacao():
    dados_requisicao = request.get_json()

    if dados_requisicao:    
        try:
            validar_dados = ValidarSolicitacaoReembolso()
            dados_validados = validar_dados.load(dados_requisicao)

            novo_numero = gerar_e_validar_unicidade_do_numero()
            
            nova_solicitacao = Reembolso(
                id=gerar_id_ulid(),
                numero=novo_numero,
                id_colaborador=get_jwt_identity(),
                nome_solicitante=dados_validados.get("nome_solicitante"),
                empresa=dados_validados.get("empresa"),
                numero_prestacao=dados_validados.get("numero_prestacao"),
                descricao=dados_validados.get("descricao"),
                data=dados_validados.get("data"),
                tipo_reembolso=dados_validados.get("tipo_reembolso"),
                custo_centro=dados_validados.get("custo_centro"),
                ordem_interna=dados_validados.get("ordem_interna"),
                divisao=dados_validados.get("divisao"),
                pep=dados_validados.get("pep"),
                moeda=dados_validados.get("moeda"),
                distancia_km=dados_validados.get("distancia_km"),
                valor_km=dados_validados.get("valor_km"),
                valor_faturado=dados_validados.get("valor_faturado"),
                despesa=dados_validados.get("despesa"),
            )

            db.session.add(nova_solicitacao)
            db.session.commit()

            return jsonify({"mensagem": "Solicitação cadastrada com sucesso!"}), 201

        except ValidationError as e:
            return jsonify({"erros": e.messages}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"mensagem": "Ocorreu um erro inesperado no banco de dados."}), 500

        except Exception:
            db.session.rollback()
            return jsonify({"mensagem": "Ocorreu um erro inesperado. Tente novamente"}), 500
    else:
        return jsonify({"mensagem": "Dados ausentes ou mal formatados"}), 400


@bp_reembolso.route("/todas-solicitacoes-em-aberto", methods=["GET"])
@jwt_required()
@swag_from("../docs/reembolso/todas_solicitacoes_em_aberto.yml")
def pegar_todas_solicitacoes_em_aberto():
    todos_dados = db.session.scalars(
        select(Reembolso).where(
            Reembolso.id_colaborador == get_jwt_identity(),
            Reembolso.status == "em aberto",
        )
    ).all()
    dados = [reembolso.to_dict() for reembolso in todos_dados]
    formatar_dados = RetornarReembolso(many=True)
    dados_formatados = formatar_dados.dump(dados)

    return jsonify(dados_formatados), 200


@bp_reembolso.route("/valores-solicitacoes-em-aberto", methods=["GET"])
@jwt_required()
@swag_from("../docs/reembolso/buscar_valores_totais.yml")
def pegar_valores_totais():
    todos_dados = db.session.execute(
        select(Reembolso.despesa, Reembolso.valor_faturado, Reembolso.id).where(
            Reembolso.id_colaborador == get_jwt_identity(),
            Reembolso.status == "em aberto",
        )
    ).all()

    formatar_dados = RetornarReembolso(
        only=("valor_faturado", "despesa", "id"), many=True
    )
    dados_formatados = formatar_dados.dump(todos_dados)

    return jsonify(dados_formatados), 200


@bp_reembolso.route("/buscar-por-prestacao/<numero>", methods=["GET"])
@swag_from("../docs/reembolso/buscar_por_numero_de_prestacao.yml")
def buscar_por_numero_de_prestacao_de_contas(numero: int):

    numero_existe = db.session.query(
        exists().where(Reembolso.numero_prestacao == numero)
    ).scalar()

    if numero_existe:
        todas_solicitacoes_com_o_numero = db.session.scalars(
            select(Reembolso).where(
                and_(
                    Reembolso.numero_prestacao == numero,
                    Reembolso.status == "em análise",
                )
            )
        ).all()
        dados = [reembolso.to_dict() for reembolso in todas_solicitacoes_com_o_numero]
        formatar_dados = RetornarReembolso(many=True)
        dados_formatados = formatar_dados.dump(dados)
        return jsonify(dados_formatados), 200
    else:
        return (
            jsonify(
                {
                    "mensagem": "Nenhuma solicitação com esse número de prestação foi encontrada."
                }
            ),
            404,
        )


@bp_reembolso.route("/excluir", methods=["DELETE"])
@jwt_required()
@swag_from("../docs/reembolso/excluir_solicitacao_em_aberto.yml")
def excluir_solicitacao_em_aberto():
    try:
        dados_requisicao = request.get_json()
        id_a_excluir = dados_requisicao.get("id")
        exclusao = db.session.scalar(
            select(Reembolso).where(
                Reembolso.id_colaborador == get_jwt_identity(),
                Reembolso.id == id_a_excluir,
            )
        )

        if not exclusao:
            return jsonify({"mensagem": "Solicitação não encontrada."}), 404

        db.session.delete(exclusao)
        db.session.commit()

        return jsonify({"mensagem": "Solicitação excluída com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"mensagem": "Erro ao processar a exclusão. Tente mais tarde."}),
            500,
        )


@bp_reembolso.route("/enviar-para-analise", methods=["PATCH"])
@jwt_required()
@swag_from("../docs/reembolso/atualizar_status_enviar_para_analise.yml")
def atualizar_status():
    try:
        dados_requisicao = request.get_json()
        ids = dados_requisicao.get("idsSelecionados", [])

        if not ids:
            return jsonify({"mensagem": "Nenhum id válido foi informado."}), 404

        ids_existentes = []

        for id in ids:
            id_existe = db.session.query(
                exists().where(
                    Reembolso.id_colaborador == get_jwt_identity(), Reembolso.id == id
                )
            ).scalar()

            if id_existe:
                ids_existentes.append(id)

        db.session.execute(
            update(Reembolso)
            .where(Reembolso.id.in_(ids_existentes))
            .values(status="em análise")
        )
        db.session.commit()

        if len(ids_existentes) == 1:
            return (
                jsonify({"mensagem": "Solicitação enviada para análise com sucesso!"}),
                200,
            )

        elif len(ids_existentes) > 1:
            return (
                jsonify(
                    {"mensagem": "Solicitações enviadas para análise com sucesso!"}
                ),
                200,
            )

    except SQLAlchemyError as e:
        return jsonify({"mensagem": "Erro no processamento. Tente mais tarde."}), 500

    except Exception as e:
        return (
            jsonify({"mensagem": "Ocorreu um erro inesperado. Tente mais tarde."}),
            500,
        )
