from marshmallow import Schema, fields, validate


class validar_login_colaborador(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Campo obrigatório",
            "invalid": "Digite um email válido.",
        },
    )

    senha = fields.String(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            "required": "Campo obrigatório",
            "validator_failed": "A senha tem que ter no mínimo 6 dígitos",
        },
    )
