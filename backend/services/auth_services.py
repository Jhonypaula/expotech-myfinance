from utils.validators import (
    validar_campo_vazio,
)

from utils.regex_validators import (
    validar_email,
    validar_senha
)

from repository.auth_repository import (
    buscar_usuario_por_email, 
    criar_usuario, 
    buscar_usuario_cadastrado,
    buscar_usuario_por_login,
    desativar_usuario_repository,
    verificar_status_conta
)

from utils.security import hash_senha

def cadastrar_usuario_service(
    nome_usuario,
    email_usuario,
    senha_usuario
):

    try:
        if not validar_campo_vazio(nome_usuario):

            print('\nNome obrigatorio!')
            return None

        if not validar_campo_vazio(email_usuario):

            print('\nEmail obrigatorio!')
            return None

        if not validar_email(email_usuario):

            print('\nEmail invalido!')
            return None

        if not validar_campo_vazio(senha_usuario):

            print('\nSenha obrigatoria!')
            return None

        if not validar_senha(senha_usuario):

            print(
                "\nSenha fraca!"
                "\nA senha deve conter:"
                "\n- minimo 8 caracteres"
                "\n- letra maiuscula"
                "\n- letra minuscula"
                "\n- numero"
                "\n- caractere especial"
            )

            return None

        usuario_existente = buscar_usuario_por_email(
            email_usuario
        )

        if usuario_existente:

            print('\nEmail ja cadastrado!')
            return None

        senha_hash = hash_senha(
            senha_usuario
        )

        criar_usuario(
            nome_usuario,
            email_usuario,
            senha_hash
        )

        usuario_cadastrado = (
            buscar_usuario_cadastrado(
                email_usuario
            )
        )

        return usuario_cadastrado
    except Exception as e:
        print(f"Erro interno: {e}")

def login_usuario_service(
    email_usuario,
    senha_usuario
):

    try:
        if not validar_campo_vazio(email_usuario):

            print('\nEmail obrigatorio!')
            return None

        if not validar_email(email_usuario):

            print('\nEmail invalido!')
            return None

        if not validar_campo_vazio(senha_usuario):

            print('\nSenha obrigatoria!')
            return None

        senha_hash = hash_senha(
            senha_usuario
        )

        usuario = buscar_usuario_por_login(
            email_usuario,
            senha_hash
        )

        if not usuario:

            print('\nEmail ou senha invalidos!')
            return None

        status_ativo = verificar_status_conta(
            usuario[0]
        )

        if not status_ativo:

            print(
                '\n❌ Conta desativada!'
                '\n📌 Entre em contato com o suporte.'
            )

            return None

        return usuario
    
    except Exception as e:
        print(f"Erro interno: {e}")

def desativar_usuario_service(usuario_id):

    return desativar_usuario_repository(
        usuario_id
    )