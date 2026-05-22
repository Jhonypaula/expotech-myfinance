from core.connection import conectar_banco

def buscar_saldo_total_repository(
    usuario_id
):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT SUM(saldo_contas)
        FROM tbl_contas
        WHERE usuario_id = %s
    """

    valores = (usuario_id,)

    cursor.execute(sql, valores)

    saldo_total = cursor.fetchone()

    cursor.close()
    conexao.close()

    return saldo_total

def buscar_total_entradas_repository(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT SUM(valor_transacoes)
        FROM tbl_transacoes t
        INNER JOIN tbl_contas c
        ON t.conta_id = c.id_contas
        WHERE c.usuario_id = %s
        AND t.tipo_transacoes = 'entrada'
    """

    valores = (usuario_id, )

    cursor.execute(sql, valores)

    total_entradas = cursor.fetchone()

    cursor.close()
    conexao.close()

    return total_entradas

def buscar_total_saidas_repository(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT SUM(valor_transacoes)
        FROM tbl_transacoes t
        INNER JOIN tbl_contas c
        ON t.conta_id = c.id_contas
        WHERE c.usuario_id = %s
        AND t.tipo_transacoes = 'saida'
    """

    valores = (usuario_id, )

    cursor.execute(sql, valores)

    total_saidas = cursor.fetchone()

    cursor.close()
    conexao.close()

    return total_saidas