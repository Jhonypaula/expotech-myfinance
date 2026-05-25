from datetime import datetime, timedelta

from repository.auth_repository import (
    buscar_usuario_por_email,
    atualizar_senha_usuario
)

from repository.resetar_senha_repository import (
    salvar_reset_token,
    buscar_token,
    atualizar_token_como_usado,
    invalidar_tokens_anteriores
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

from utils.regex_validators import (
    validar_senha
)

from utils.validators import (
    validar_campo_vazio
)


def requisicao_alterar_senha(email):

    usuario = buscar_usuario_por_email(email)

    if usuario:

        token = generate_reset_token()

        expira_em = (
            datetime.now() +
            timedelta(minutes=15)
        )

        invalidar_tokens_anteriores(
            usuario["id_usuarios"]
        )

        salvar_reset_token(
            usuario["id_usuarios"],
            token,
            expira_em
        )

        body = f"""
        <html>
            <body style="
                margin:0;
                padding:0;
                background-color:#f4f7fb;
                font-family:Arial, sans-serif;
            ">

                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td align="center" style="padding:40px 20px;">

                            <table width="500" cellpadding="0" cellspacing="0" style="
                                background:#ffffff;
                                border-radius:16px;
                                padding:40px;
                                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                            ">

                                <tr>
                                    <td align="center">

                                        <h1 style="
                                            margin:0;
                                            color:#111827;
                                            font-size:28px;
                                        ">
                                            🔐 Recuperação de Senha
                                        </h1>

                                        <p style="
                                            color:#6b7280;
                                            font-size:16px;
                                            margin-top:15px;
                                            line-height:1.6;
                                        ">
                                            Recebemos uma solicitação para redefinir sua senha.
                                        </p>

                                        <div style="
                                            margin:30px 0;
                                            background:#f3f4f6;
                                            padding:20px;
                                            border-radius:12px;
                                        ">

                                            <p style="
                                                margin:0;
                                                color:#6b7280;
                                                font-size:14px;
                                            ">
                                                Seu código de recuperação:
                                            </p>

                                            <h2 style="
                                                margin:10px 0 0 0;
                                                font-size:36px;
                                                letter-spacing:6px;
                                                color:#2563eb;
                                            ">
                                                {token}
                                            </h2>

                                        </div>

                                        <p style="
                                            color:#6b7280;
                                            font-size:14px;
                                            line-height:1.6;
                                        ">
                                            Esse código expira em <strong>15 minutos</strong>.
                                        </p>

                                        <p style="
                                            margin-top:30px;
                                            font-size:13px;
                                            color:#9ca3af;
                                            line-height:1.5;
                                        ">
                                            Caso você não tenha solicitado a recuperação de senha,
                                            ignore este e-mail.
                                        </p>

                                    </td>
                                </tr>

                            </table>

                        </td>
                    </tr>
                </table>

            </body>
        </html>
        """

        send_email(
            email,
            "🔐 Recuperação de senha",
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

    expira_em =(
        token_data["expira_em"]
    )

    if datetime.now() > expira_em:
        return False

    if not validar_campo_vazio(nova_senha):
        print("\nSenha obrigatoria!")
        return False
    
    if not validar_senha(nova_senha):
        
        print(
            "\n❌️ Senha fraca!"
            "\nA senha deve conter:"
            "\n- minimo 8 caracteres"
            "\n- letra maiuscula"
            "\n- letra minuscula"
            "\n- numero"
            "\n- caractere especial"
        )
        
        return False

    senha_hashed = hash_senha(
        nova_senha
    )

    atualizar_senha_usuario(
        token_data["usuario_id"],
        senha_hashed
    )

    atualizar_token_como_usado(token)

    return True

def validar_token_reset(
    token
):
    
    token_data = buscar_token(
        token
    )
    
    if not token_data:
        return None
    
    expira_em = token_data[
        "expira_em"
    ]
    
    if datetime.now() > expira_em:
        return None
    
    return token_data