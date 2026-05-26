from datetime import datetime, timedelta

from back_end.repository.auth_repository import (
    buscar_usuario_por_email,
    atualizar_senha_usuario
)

from back_end.repository.resetar_senha_repository import (
    salvar_reset_token,
    buscar_token,
    atualizar_token_como_usado,
    invalidar_tokens_anteriores
)

from back_end.utils.token_generator import (
    generate_reset_token
)

from back_end.utils.security import (
    hash_senha
)

from back_end.services.email_service import (
    send_email
)

from back_end.utils.regex_validators import (
    validar_senha
)

from back_end.utils.validators import (
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
        <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recuperação de Senha</title>
            </head>

            <body style="
            margin:0;
            padding:0;
            background-color:#0d1117;
            font-family:Arial, Helvetica, sans-serif;
            ">

            <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="padding:40px 16px;background-color:#0d1117;">

                <tr>
                <td align="center">

                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="
                            max-width:560px;
                            background-color:#161b22;
                            border-radius:18px;
                            overflow:hidden;
                            border:1px solid #21262d;
                        ">

                    <!-- HEADER -->
                    <tr>
                        <td style="
                        padding:40px 48px;
                        background-color:#11161c;
                        border-bottom:1px solid #21262d;
                        text-align:center;
                        ">

                        <div style="
                            width:60px;
                            height:60px;
                            line-height:60px;
                            border-radius:50%;
                            background-color:#1f6feb20;
                            border:1px solid #1f6feb50;
                            display:inline-block;
                            font-size:28px;
                            margin-bottom:18px;
                        ">
                            🔐
                        </div>

                        <h1 style="
                            margin:0;
                            color:#f0f6fc;
                            font-size:28px;
                            font-weight:700;
                        ">
                            Recuperação de Senha
                        </h1>

                        <p style="
                            margin:12px 0 0;
                            color:#8b949e;
                            font-size:15px;
                            line-height:1.6;
                        ">
                            Recebemos uma solicitação para redefinir a senha da sua conta.
                        </p>

                        </td>
                    </tr>

                    <!-- BODY -->
                    <tr>
                        <td style="padding:42px 48px;">

                        <p style="
                            margin:0 0 24px;
                            color:#c9d1d9;
                            font-size:15px;
                            line-height:1.7;
                        ">
                            Utilize o código abaixo para continuar com a redefinição da sua senha.
                            Por segurança, esse código é temporário e válido por apenas alguns minutos.
                        </p>

                        <!-- TOKEN -->
                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                style="margin-bottom:28px;">

                            <tr>
                            <td align="center" style="
                                background-color:#0d1117;
                                border:1px solid #30363d;
                                border-radius:14px;
                                padding:28px 20px;
                            ">

                                <p style="
                                margin:0 0 12px;
                                color:#8b949e;
                                font-size:12px;
                                letter-spacing:2px;
                                text-transform:uppercase;
                                ">
                                Código de recuperação
                                </p>

                                <div style="
                                color:#58a6ff;
                                font-size:38px;
                                font-weight:700;
                                letter-spacing:10px;
                                font-family:'Courier New', monospace;
                                ">
                                {token}
                                </div>

                                <p style="
                                margin:18px 0 0;
                                color:#8b949e;
                                font-size:13px;
                                ">
                                Expira em <strong style="color:#f0f6fc;">15 minutos</strong>
                                </p>

                            </td>
                            </tr>

                        </table>

                        <p style="
                            margin:0 0 32px;
                            color:#8b949e;
                            font-size:14px;
                            line-height:1.7;
                        ">
                            Caso você não tenha solicitado a recuperação de senha,
                            nenhuma ação é necessária. Sua conta continuará segura.
                        </p>

                        <!-- ALERT -->
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">

                            <tr>
                            <td style="
                                background-color:#1c2128;
                                border:1px solid #30363d;
                                border-radius:12px;
                                padding:18px 20px;
                            ">

                                <p style="
                                margin:0;
                                color:#c9d1d9;
                                font-size:13px;
                                line-height:1.7;
                                ">
                                <strong style="color:#58a6ff;">Dica de segurança:</strong>
                                nunca compartilhe este código com outras pessoas.
                                Nossa equipe nunca solicitará sua senha ou token por e-mail.
                                </p>

                            </td>
                            </tr>

                        </table>

                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td style="
                        padding:24px 40px;
                        background-color:#11161c;
                        border-top:1px solid #21262d;
                        text-align:center;
                        ">

                        <p style="
                            margin:0 0 8px;
                            color:#6e7681;
                            font-size:12px;
                            line-height:1.6;
                        ">
                            Este é um e-mail automático. Não responda esta mensagem.
                        </p>

                        <p style="
                            margin:0;
                            color:#484f58;
                            font-size:11px;
                        ">
                            © 2026 My Finance — Gestor Financeiro Pessoal
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