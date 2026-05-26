from backend.core.connection import conectar_banco


def salvar_reset_token(
    usuario_id,
    token,
    expira_em
):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO tbl_reset_tokens (
            usuario_id,
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
        FROM tbl_reset_tokens
        WHERE token = %s
        AND usado = FALSE
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
        UPDATE tbl_reset_tokens
        SET usado = TRUE
        WHERE token = %s
    """

    cursor.execute(sql, (token,))

    conexao.commit()

    cursor.close()
    conexao.close()
    
def invalidar_tokens_anteriores(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        UPDATE tbl_reset_tokens
        SET usado = TRUE
        WHERE usuario_id = %s
        AND usado = FALSE
    """
    
    cursor.execute(sql, (usuario_id,))
    
    conexao.commit()
    
    cursor.close()
    conexao.close()