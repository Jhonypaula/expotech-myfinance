from backend.core.connection import conectar_banco

def criar_transacao_repository(
    conta_id,
    categorias_id,
    tipo_transacoes,
    valor_transacoes,
    descricao_transacoes
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        INSERT INTO tbl_transacoes (
            conta_id,
            categoria_id,
            tipo_transacoes,
            valor_transacoes,
            descricao_transacoes
        ) 
        
        VALUES (%s, %s, %s, %s, %s)
    """
    
    valores = (
        conta_id,
        categorias_id,
        tipo_transacoes,
        valor_transacoes,
        descricao_transacoes
    )
    
    cursor.execute(sql, valores)
    
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
def listar_transacoes_repository(conta_id):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT 
            t.id_transacoes,
            t.tipo_transacoes,
            t.valor_transacoes,
            t.descricao_transacoes,
            c.nome_categorias,
            t.data_transacao
        FROM tbl_transacoes t
        
        INNER JOIN tbl_categorias c
        ON t.categoria_id = c.id_categorias
        
        WHERE t.conta_id = %s
        
        ORDER BY t.data_transacao DESC
    """
    
    valores = conta_id,
    
    cursor.execute(sql, valores)
    transacoes = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return transacoes

def listar_transacoes_fk(conta_id):

    conexao = conectar_banco()

    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM tbl_transacoes
        WHERE conta_id = %s
    """

    cursor.execute(sql, (conta_id,))

    transacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return transacoes

def buscar_transacao_por_id(
    conta_id,
    id_transacao
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT
            id_transacoes,
            tipo_transacoes,
            valor_transacoes
        FROM tbl_transacoes
        WHERE conta_id = %s
        AND id_transacoes = %s
    """
    
    valores = conta_id, id_transacao
    
    cursor.execute(sql, valores)
    
    transacao = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return transacao

def excluir_transacao_repository(
    conta_id,
    id_transacao
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        DELETE FROM tbl_transacoes
        WHERE conta_id = %s
        AND id_transacoes = %s
    """
    
    valores = (
        conta_id,
        id_transacao
    )
    
    cursor.execute(sql, valores)
    
    conexao.commit()
    
    cursor.close()
    conexao.close()

def editar_transacao_repository(
    conta_id,
    id_transacao,
    categoria_id,
    tipo_transacao,
    valor_transacao,
    descricao_transacao
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        UPDATE tbl_transacoes
        SET 
            categoria_id = %s,
            tipo_transacoes = %s,
            valor_transacoes = %s,
            descricao_transacoes = %s
        WHERE conta_id = %s
        AND id_transacoes = %s
    """
    
    valores = (
        categoria_id,
        tipo_transacao,
        valor_transacao,
        descricao_transacao,
        conta_id,
        id_transacao
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def filtrar_transacoes_tipo_repository(
    conta_id,
    tipo_transacao
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT
            t.id_transacoes,
            t.tipo_transacoes,
            t.valor_transacoes,
            t.descricao_transacoes,
            c.nome_categorias,
            t.data_transacao

        FROM tbl_transacoes t

        INNER JOIN tbl_categorias c
        ON t.categoria_id = c.id_categorias

        WHERE t.conta_id = %s
        AND t.tipo_transacoes = %s
    """

    valores = (
        conta_id,
        tipo_transacao
    )
    
    cursor.execute(sql, valores)

    transacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return transacoes

def filtrar_transacoes_categoria_repository(
    conta_id,
    categoria_id
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT 
            t.id_transacoes,
            t.tipo_transacoes,
            t.valor_transacoes,
            t.descricao_transacoes,
            cat.nome_categorias,
            t.data_transacao

        FROM tbl_transacoes t

        INNER JOIN tbl_categorias cat
        ON t.categoria_id = cat.id_categorias

        WHERE t.conta_id = %s
        AND t.categoria_id = %s
    """

    valores = (
        conta_id,
        categoria_id
    )

    cursor.execute(sql, valores)

    transacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return transacoes

def filtrar_transacoes_descricao_repository(
    conta_id,
    descricao
):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    sql = """
        SELECT
            t.id_transacoes,
            t.tipo_transacoes,
            t.valor_transacoes,
            t.descricao_transacoes,
            c.nome_categorias,
            t.data_transacao

        FROM tbl_transacoes t

        INNER JOIN tbl_categorias c
        ON t.categoria_id = c.id_categorias

        WHERE t.conta_id = %s
        AND t.descricao_transacoes LIKE %s
    """

    descricao = f"%{descricao}%"

    valores = (
        conta_id,
        descricao
    )

    cursor.execute(sql, valores)

    transacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return transacoes