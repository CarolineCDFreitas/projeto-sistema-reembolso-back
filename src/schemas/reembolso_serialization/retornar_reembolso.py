from marshmallow import Schema, fields, post_dump
from src.utils.formatar_campos_opcionais import formatar_campos_opcionais


class RetornarReembolso(Schema):
    id = fields.String()
    numero = fields.Integer()
    id_colaborador = fields.String()
    nome_solicitante = fields.String(data_key="nomeCompleto")
    empresa = fields.String()
    numero_prestacao = fields.String(data_key="prestacaoDeContas")
    descricao = fields.String(data_key="descricaoMotivo")
    data = fields.Date()
    tipo_reembolso = fields.String(data_key="tipoDeDespesa")
    custo_centro = fields.String(data_key="centro")
    ordem_interna = fields.String(data_key="ordemInterna")
    divisao = fields.String(data_key="divisao")
    pep = fields.String()
    moeda = fields.String()
    distancia_km = fields.Integer(data_key="distKm")
    valor_km = fields.Decimal(data_key="valorKm")
    valor_faturado = fields.Decimal(data_key="valorFaturado")
    despesa = fields.Decimal(data_key="despesaTotal")
    status = fields.String()
    criado_em = fields.DateTime()

    @post_dump
    def formatador_de_campos_opcionais(self, reembolsos, **kwargs):
        return formatar_campos_opcionais(reembolsos)
