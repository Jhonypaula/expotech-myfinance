from datetime import datetime, timedelta

from repository.auth_repository import (
    buscar_usuario_por_email,
    atualizar_senha_usuario
)

from repository.resetar_senha_repository import (
    salvar_reset_token,
    buscar_token,
    atualizar_token_como_usado
)

from utils.token_generator import (
    generate_reset_token
)

from utils.security import (
    hash_senha
)

from services.email_service import (
    send_email
)


def requisicao_alterar_senha(email):

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return False

    token = generate_reset_token()

    expira_em = (
        datetime.now() +
        timedelta(minutes=15)
    ).isoformat()

    salvar_reset_token(
        usuario["id_usuarios"],
        token,
        expira_em
    )

    body = f"""
Olá.

Seu token de recuperação é:

{token}

Esse token expira em 15 minutos.
"""

    send_email(
        email,
        "Recuperação de senha",
        body
    )

    return True


def resetar_senha(
    token,
    nova_senha
):

    token_data = buscar_token(token)

    if not token_data:
        return False

    if token_data["usado"] == 1:
        return False

    expira_em = datetime.fromisoformat(
        token_data["expira_em"]
    )

    if datetime.now() > expira_em:
        return False

    senha_hashed = hash_senha(
        nova_senha
    )

    atualizar_senha_usuario(
        token_data["usuarios_id"],
        senha_hashed
    )

    atualizar_token_como_usado(token)

    return True