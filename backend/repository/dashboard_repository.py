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

def buscar_gastos_categoria_repository(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
            SELECT 
                cat.nome_categorias,
                SUM(t.valor_transacoes)
            FROM tbl_transacoes t

            INNER JOIN tbl_contas co
            ON t.conta_id = co.id_contas

            INNER JOIN tbl_categorias cat
            ON t.categoria_id = cat.id_categorias

            WHERE co.usuario_id = %s
            AND t.tipo_transacoes = 'saida'

            GROUP BY cat.nome_categorias
    """

    valores = (usuario_id, )

    cursor.execute(sql, valores)

    gastos_categoria = cursor.fetchall()

    cursor.close()
    conexao.close()

    return gastos_categoria

def buscar_maior_categoria_repository(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT
            cat.nome_categorias,
            SUM(t.valor_transacoes) AS total_gasto
        FROM tbl_transacoes t

        INNER JOIN tbl_contas co
        ON t.conta_id = co.id_contas

        INNER JOIN tbl_categorias cat
        ON t.categoria_id = cat.id_categorias

        WHERE co.usuario_id = %s
        AND t.tipo_transacoes = 'saida'

        GROUP BY cat.nome_categorias

        ORDER BY total_gasto DESC

        LIMIT 1
    """

    valores = (usuario_id, )

    cursor.execute(sql, valores)

    maior_categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return maior_categoria

def buscar_quantidade_transacoes_repository(
    usuario_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT COUNT(*)

        FROM tbl_transacoes t

        INNER JOIN tbl_contas co
        ON t.conta_id = co.id_contas

        WHERE co.usuario_id = %s
    """

    valores = (usuario_id, )

    cursor.execute(sql, valores)

    quantidade_transacoes = cursor.fetchone()

    cursor.close()
    conexao.close()

    return quantidade_transacoes

def buscar_evolucao_mensal_repository(
    usuario_id,
    n_meses
):
    """Soma entradas e saidas por ano/mes nos ultimos ``n_meses`` meses.

    Retorna tuplas ``(ano, mes, total_entradas, total_saidas)`` ja em ordem
    cronologica. Meses sem nenhuma transacao nao aparecem - quem consumir
    precisa preencher os buracos.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT
            YEAR(t.data_transacao) AS ano,
            MONTH(t.data_transacao) AS mes,
            SUM(
                CASE
                    WHEN t.tipo_transacoes = 'entrada'
                    THEN t.valor_transacoes
                    ELSE 0
                END
            ) AS total_entradas,
            SUM(
                CASE
                    WHEN t.tipo_transacoes = 'saida'
                    THEN t.valor_transacoes
                    ELSE 0
                END
            ) AS total_saidas

        FROM tbl_transacoes t

        INNER JOIN tbl_contas co
        ON t.conta_id = co.id_contas

        WHERE co.usuario_id = %s
        AND t.data_transacao >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)

        GROUP BY YEAR(t.data_transacao), MONTH(t.data_transacao)
        ORDER BY ano ASC, mes ASC
    """

    valores = (usuario_id, n_meses)

    cursor.execute(sql, valores)

    evolucao = cursor.fetchall()

    cursor.close()
    conexao.close()

    return evolucao