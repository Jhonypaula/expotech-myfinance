def validar_campo_vazio(valor):
    return valor.strip() != ""

def validar_email(email):
    email = email.strip()

    if email == "":
        return False
    
    if "@" not in email:
        return False
    
    if "." not in email:
        return False

    return True 

def validar_senha(senha):
    senha = senha.strip()

    if senha == "":
        return False
    if len(senha) < 6:
        return False
    
    return True