from core.connection import conectar_banco

def buscar_categoria_por_id(
    id_categorias
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_categorias
        FROM tbl_categorias
        WHERE id_categorias = %s
    """
    
    valores = id_categorias,
    
    cursor.execute(sql, valores)
    
    categoria = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return categoria

def listar_categorias_repository():
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_categorias, nome_categorias, descricao_categorias
        FROM tbl_categorias
        
    """
    
    cursor.execute(sql)
    
    categorias = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return categorias
    