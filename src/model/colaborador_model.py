from src.model import db

class Colaborador(db.Model):

    id = db.Column(db.CHAR(26), primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(150))
    senha = db.Column(db.String(255))
    cargo = db.Column(db.String(100))
    salario = db.Column(db.DECIMAL(10, 2))

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
