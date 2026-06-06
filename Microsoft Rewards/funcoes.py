import secrets
def chave():
    chave = secrets.token_hex(26).upper()
    return chave


