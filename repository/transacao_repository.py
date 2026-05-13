from core.connection import conectar_banco

def criar_transacao_repository(
    conta_id,
    categorias_id,
    tipo_transacoes,
    valor_transacoes,
    descricao_transacoes,
    data_transacao
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        INSERT INTO tbl_transacoes (
            conta_id,
            categorias_id,
            tipo_transacoes,
            valor_transacoes,
            descricao_transacoes,
            data_transacao
        ) 
        
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        conta_id,
        categorias_id,
        tipo_transacoes,
        valor_transacoes,
        descricao_transacoes,
        data_transacao
    )
    
    cursor.execute(sql, valores)
    
    conexao.commit()
    
    cursor.close()
    conexao.close()
    