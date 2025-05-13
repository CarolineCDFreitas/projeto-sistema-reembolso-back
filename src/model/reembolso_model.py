from src.model import db
from sqlalchemy import text


class Reembolso(db.Model):
    __tablename__ = "reembolso"

    id = db.Column(db.CHAR(26), primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)

    id_colaborador = db.Column(
        db.CHAR(26), db.ForeignKey("colaborador.id"), nullable=False
    )

    nome_solicitante = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(50), nullable=False)
    numero_prestacao = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

    data = db.Column(db.Date, nullable=False, server_default=text("CURDATE()"))
    tipo_reembolso = db.Column(db.String(50), nullable=False)
    custo_centro = db.Column(db.String(20), nullable=False)
    ordem_interna = db.Column(db.String(25), nullable=True)
    divisao = db.Column(db.String(25), nullable=True)
    pep = db.Column(db.String(25), nullable=True)
    moeda = db.Column(db.String(25), nullable=False)
    distancia_km = db.Column(db.Integer, nullable=True)
    valor_km = db.Column(db.DECIMAL(10, 2), nullable=True)
    valor_faturado = db.Column(db.DECIMAL(10, 2), nullable=False)
    despesa = db.Column(db.DECIMAL(10, 2), nullable=False)

    status = db.Column(
        db.String(50), nullable=False, server_default=text('"em aberto"')
    )
    criado_em = db.Column(db.DateTime, nullable=False, server_default=text("NOW()"))

    taxa_de_conversao = db.Column(db.String(25), nullable=True, default=None)
    valor_convertido = db.Column(db.DECIMAL(10, 2), nullable=True, default=None)
    moeda_de_conversao = db.Column(db.String(25), nullable=True, default=None)
    hora_da_conversao = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(
        self,
        id,
        numero,
        id_colaborador,
        nome_solicitante,
        empresa,
        numero_prestacao,
        descricao,
        data,
        tipo_reembolso,
        custo_centro,
        ordem_interna,
        divisao,
        pep,
        moeda,
        distancia_km,
        valor_km,
        valor_faturado,
        despesa,
        
    ):
        self.id = id
        self.numero = numero
        self.id_colaborador = id_colaborador
        self.nome_solicitante = nome_solicitante
        self.empresa = empresa
        self.numero_prestacao = numero_prestacao
        self.descricao = descricao
        self.data = data
        self.tipo_reembolso = tipo_reembolso
        self.custo_centro = custo_centro
        self.ordem_interna = ordem_interna
        self.divisao = divisao
        self.pep = pep
        self.moeda = moeda
        self.distancia_km = distancia_km
        self.valor_km = valor_km
        self.valor_faturado = valor_faturado
        self.despesa = despesa
        

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero": self.numero,
            "id_colaborador": self.id_colaborador,
            "nome_solicitante": self.nome_solicitante,
            "empresa": self.empresa,
            "numero_prestacao": self.numero_prestacao,
            "descricao": self.descricao,
            "data": self.data,
            "tipo_reembolso": self.tipo_reembolso,
            "custo_centro": self.custo_centro,
            "ordem_interna": self.ordem_interna,
            "divisao": self.divisao,
            "pep": self.pep,
            "moeda": self.moeda,
            "distancia_km": self.distancia_km,
            "valor_km": self.valor_km,
            "valor_faturado": self.valor_faturado,
            "despesa": self.despesa,
            "status": self.status,
            "criado_em": self.criado_em,
        }
