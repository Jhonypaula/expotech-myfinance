import re

def validar_email(email):

    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(regex, email)

def validar_senha(senha):

    regex = (
        r"^(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@$!%*?&])"
        r"[A-Za-z\d@$!%*?&]{8,}$"
    )

    return re.match(regex, senha)