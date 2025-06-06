from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    validates_schema,
    ValidationError,
)
from src.utils.tratamento_dos_dados import tratamento_dos_dados
from src.utils.validar_data import validar_data


class ValidarSolicitacaoReembolso(Schema):
    @pre_load
    def tratar_dados(self, dados_requisicao: dict, **kwargs):
        return tratamento_dos_dados(dados_requisicao)

    nome_solicitante = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, error="Digite nome completo (nome e sobrenome)."),
            validate.Regexp(
                r"^[A-Za-z\s]+$", error="Não deve conter números ou símbolos"
            ),
        ],
        data_key="nomeCompleto",
        error_messages={"required": "Campo obrigatório."},
    )

    empresa = fields.String(
        required=True,
        validate=validate.Regexp(r"^[A-Za-z]{3}\d{3}$", error="Use no formato AAA000"),
        error_messages={"required": "Campo obrigatório."},
    )

    numero_prestacao = fields.String(
        required=True,
        validate=validate.Regexp(r"^\d{6}$", error="Insira 6 dígitos (000000)"),
        data_key="prestacaoDeContas",
        error_messages={"required": "Campo obrigatório."},
    )

    descricao = fields.String(
        required=True,
        validate=validate.Length(max=255, error="O máximo de caracteres é 255."),
        data_key="descricaoMotivo",
        error_messages={"required": "Campo obrigatório."},
    )

    data = fields.Date(
        required=True,
        validate=validar_data,
        error_messages={"required": "Campo obrigatório."},
    )

    tipo_reembolso = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "alimentacao",
                "combustivel",
                "conducao",
                "estacionamento",
                "viagemAdministrativa",
            ],
            error="Valor inválido para tipo de despesa. Selecione uma opção.",
        ),
        error_messages={"required": "Campo obrigatório."},
        data_key="tipoDeDespesa",
    )

    custo_centro = fields.String(
        required=True,
        validate=validate.OneOf(
            ["1100109002", "1100110002", "1100110102"],
            error="Valor inválido para esse centro de custo. Selecione uma opção",
        ),
        error_messages={"required": "Campo obrigatório."},
        data_key="centro",
    )

    ordem_interna = fields.String(
        required=False,
        validate=validate.Regexp(r"^\d{4}$", error="Insira 4 dígitos (0000)"),
        allow_none=True,
        data_key="ordemInterna",
    )

    divisao = fields.String(
        required=False,
        validate=validate.Regexp(r"^\d{3}$", error="Insira 3 dígitos (000)"),
        allow_none=True,
    )

    pep = fields.String(
        required=False,
        validate=validate.Regexp(r"^\d{3}$", error="Insira 3 dígitos (000)"),
        allow_none=True,
    )

    moeda = fields.String(
        required=True,
        validate=validate.OneOf(
            ["BRL", "USD", "EUR", "JYP", "GBP"],
            error="Valor inválido para moedas aceitas. Selecione uma opção",
        ),
        error_messages={"required": "Campo obrigatório."},
    )

    distancia_km = fields.Integer(
        required=False,
        validate=validate.Range(
            min=1, max=99999, error="Somente números (máx. 5 dígitos)"
        ),
        allow_none=True,
        data_key="distKm",
    )

    valor_km = fields.Decimal(required=False, allow_none=True, data_key="valorKm")

    valor_faturado = fields.Decimal(
        required=True,
        error_messages={"required": "Campo obrigatório"},
        data_key="valorFaturado",
    )

    despesa = fields.Decimal(
        required=True,
        error_messages={"required": "Campo obrigatório"},
        data_key="despesaTotal",
    )

    @validates_schema
    def obrigatoriedade_condicional_se_tipo_reembolso(self, data: dict, **kwargs):
        if data.get("tipo_reembolso") == "combustivel":
            erros = {}
            if not data.get("distancia_km"):
                erros["distancia_km"] = "Campo obrigatório"
            if not data.get("valor_km"):
                erros["valor_km"] = "Campo obrigatório"
            if erros:
                raise ValidationError(erros)

    @validates_schema
    def obrigatoriedade_condicional_ou_divisao_e_ordem_interna_ou_pep(
        self, data: dict, **kwargs
    ):
        erros = {}

        if data.get("divisao") and not data.get("ordem_interna"):
            erros["ordem_interna"] = "Campo obrigatório"
        if data.get("ordem_interna") and not data.get("divisao"):
            erros["divisao"] = "Campo obrigatório"
        if (
            not data.get("divisao")
            and not data.get("ordem_interna")
            and not data.get("pep")
        ):
            erros["pep"] = "Preencha este campo ou informe Ordem Interna e Divisão"
        if erros:
            raise ValidationError(erros)
