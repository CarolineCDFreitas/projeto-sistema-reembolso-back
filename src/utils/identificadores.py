from ulid import ULID
from tsidpy import TSID

from src.model import db
from sqlalchemy import exists
from src.model.reembolso_model import Reembolso


def gerar_id_ulid():
    return str(ULID())


def gerar_id_tsid(digito: int):
    return TSID.create().number % (10**digito)


def gerar_e_validar_unicidade_do_numero():
    while True:
        numero_gerado = gerar_id_tsid(7)
        numero_existe = db.session.query(
            exists().where(Reembolso.numero == numero_gerado)
        ).scalar()

        if not numero_existe:
            return numero_gerado
