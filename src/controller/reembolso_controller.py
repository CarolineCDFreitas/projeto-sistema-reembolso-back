from flask import Blueprint, request, jsonify

from src.model import db
from src.model.reembolso_model import Reembolso
from src.utils.identificadores import gerar_id_ulid, gerar_e_validar_unicidade_do_numero

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")


@bp_reembolso.route("/cadastrar-solicitacao-de-reembolso", methods=["POST"])
def cadastrar_solicitacao():
    dados_requisicao = request.get_json()
    novo_numero = gerar_e_validar_unicidade_do_numero()

    nova_solicitacao = Reembolso(
        id=gerar_id_ulid(),
        numero=novo_numero,
        id_colaborador=dados_requisicao.get("id_colaborador"),
        nome_solicitante=dados_requisicao.get("nomeCompleto"),
        empresa=dados_requisicao.get("empresa"),
        numero_prestacao=dados_requisicao.get("prestacaoDeContas"),
        descricao=dados_requisicao.get("descricaoMotivo"),
        data=dados_requisicao.get("data"),
        tipo_reembolso=dados_requisicao.get("tipoDeDespesa"),
        custo_centro=dados_requisicao.get("centro"),
        ordem_interna=dados_requisicao.get("ordemInterna"),
        divisao=dados_requisicao.get("divisao"),
        pep=dados_requisicao.get("pep"),
        moeda=dados_requisicao.get("moeda"),
        distancia_km=dados_requisicao.get("distKm"),
        valor_km=dados_requisicao.get("valorKm"),
        valor_faturado=dados_requisicao.get("valorFaturado"),
        despesa=dados_requisicao.get("despesaTotal"),
    )

    db.session.add(nova_solicitacao)
    db.session.commit()

    return jsonify({"mensagem": "Solicitação cadastrada com sucesso!"}), 201
