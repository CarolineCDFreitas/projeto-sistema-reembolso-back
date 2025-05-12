from marshmallow import Schema, fields, validate


class ValidarCadastroColaborador(Schema):
    nome_completo_cadastro = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, error="Digite nome completo (nome e sobrenome)."),
            validate.Regexp(
                r"^[A-Za-z\s]+$", error="Não deve conter números ou símbolos."
            ),
        ],
        data_key="nomeCompletoCadastro",
        error_messages={"required": "Campo obrigatório."},
    )

    email_cadastro = fields.Email(
        required=True,
        data_key="emailCadastro",
        error_messages={
            "required": "Campo obrigatório",
            "invalid": "Digite um email válido.",
        },
    )

    senha_cadastro = fields.String(
        required=True,
        validate=validate.Length(
            min=6, error="A senha tem que ter no mínimo 6 dígitos."
        ),
        data_key="senhaCadastro",
        error_messages={"required": "Campo obrigatório."},
    )

    cargo = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Preencha com nome válido"),
        allow_none=False,
        error_messages={"required": "Campo obrigatório."},
    )

    salario = fields.Decimal(
        required=True,
        places=2,
        validate=[
            validate.Range(
                min=1.11,
                max=99999999.99,
                error="O salário deve estar entre R$ 1,11 e R$ 99.999.999,99.",
            ),
        ],
        as_string=True,
        error_messages={
            "required": "Campo obrigatório.",
            "invalid": "Digite um valor decimal válido.",
        },
    )
