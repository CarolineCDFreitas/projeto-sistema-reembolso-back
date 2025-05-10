from flask import Blueprint, request, jsonify

from src.model import db
from src.model.reembolso_model import Reembolso
from src.utils.identificadores import gerar_id_ulid, gerar_e_validar_unicidade_do_numero
from src.utils.limpeza_dados import limpeza_de_dados

bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")


@bp_reembolso.route("/cadastrar", methods=["POST"])
def cadastrar_solicitacao():
    dados_requisicao = request.get_json()
    novo_numero = gerar_e_validar_unicidade_do_numero()

    dados_tratados = limpeza_de_dados(dados_requisicao)

    nova_solicitacao = Reembolso(
        id=gerar_id_ulid(),
        numero=novo_numero,
        id_colaborador="01JTST6X5M3JTPH9W0371RW82X",
        nome_solicitante=dados_tratados.get("nomeCompleto"),
        empresa=dados_tratados.get("empresa"),
        numero_prestacao=dados_tratados.get("prestacaoDeContas"),
        descricao=dados_tratados.get("descricaoMotivo"),
        data=dados_tratados.get("data"),
        tipo_reembolso=dados_tratados.get("tipoDeDespesa"),
        custo_centro=dados_tratados.get("centro"),
        ordem_interna=dados_tratados.get("ordemInterna"),
        divisao=dados_tratados.get("divisao"),
        pep=dados_tratados.get("pep"),
        moeda=dados_tratados.get("moeda"),
        distancia_km=dados_tratados.get("distKm"),
        valor_km=dados_tratados.get("valorKm"),
        valor_faturado=dados_tratados.get("valorFaturado"),
        despesa=dados_tratados.get("despesaTotal"),
    )

    db.session.add(nova_solicitacao)
    db.session.commit()

    return jsonify({"mensagem": "Solicitação cadastrada com sucesso!"}), 201
