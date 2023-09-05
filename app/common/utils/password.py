import bcrypt

salt = bcrypt.gensalt(rounds=12)


def create_hash(password: str) -> str:
    enconded_password = password.encode("utf-8")
    return bcrypt.hashpw(enconded_password, salt)


def check_password(password, hash: str) -> bool:
    password = password.encode("utf-8")
    hash = hash.encode("utf-8")
    return bcrypt.checkpw(password, hash)
