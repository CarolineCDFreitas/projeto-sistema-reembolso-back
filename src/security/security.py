from src.security import bcrypt


def hash_senha(senha):
    pw_hash = bcrypt.generate_password_hash(senha)
    return pw_hash.decode("utf-8")


def checar_senha(senha, hash_senha):
    return bcrypt.check_password_hash(hash_senha, senha)
