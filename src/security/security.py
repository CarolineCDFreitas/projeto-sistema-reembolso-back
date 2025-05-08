from src.security import bycrypt


def hash_senha(senha):
    pw_hash = bycrypt.generate_password_hash(senha)
    return pw_hash


def checar_senha(senha, hash_senha):
    return bycrypt.check_password_hash(hash_senha, senha)
