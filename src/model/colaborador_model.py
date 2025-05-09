from src.model import db

class Colaborador(db.Model):

    id = db.Column(db.CHAR(26), primary_key=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.DECIMAL(10, 2), nullable=False)

    def __init__(self, id, nome, email, senha, cargo, salario):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario

    def colaborador_info(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cargo": self.cargo,
            "salario": float(self.salario),
        }
