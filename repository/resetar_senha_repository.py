from core.connection import conectar_banco


def salvar_reset_token(
    usuario_id,
    token,
    expira_em
):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO password_reset_tokens (
            usuarios_id,
            token,
            expira_em
        )
        VALUES (%s, %s, %s)
    """

    valores = (
        usuario_id,
        token,
        expira_em
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_token(token):

    conexao = conectar_banco()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *
        FROM password_reset_tokens
        WHERE token = %s
    """

    cursor.execute(sql, (token,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


def atualizar_token_como_usado(token):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    sql = """
        UPDATE password_reset_tokens
        SET usado = TRUE
        WHERE token = %s
    """

    cursor.execute(sql, (token,))

    conexao.commit()

    cursor.close()
    conexao.close()