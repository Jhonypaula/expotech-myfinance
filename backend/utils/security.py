import hashlib

def hash_senha(senha):
    senha_bytes = senha.encode()
    hash_obj = hashlib.sha256(senha_bytes)
    senha_hash = hash_obj.hexdigest()

    return senha_hash