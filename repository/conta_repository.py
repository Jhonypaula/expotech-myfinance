from core.connection import conectar_banco

def criar_conta_repository(
    usuario_id,
    nome_conta, 
    tipo_conta, 
    saldo_inicial
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        INSERT INTO tbl_contas (
            usuario_id,
            nome_contas,
            tipo_contas,
            saldo_contas
        )
        VALUES (%s, %s, %s, %s)
    """
    
    valores = (
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial
    )
    
    cursor.execute(sql, valores)
    
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
def buscar_conta_por_nome (
    usuario_id,
    nome_conta
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_contas
        FROM tbl_contas
        WHERE usuario_id = %s 
        AND nome_contas = %s
    """
    
    valores = (
        usuario_id,
        nome_conta
    )
    
    cursor.execute(sql, valores)
    
    conta = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return conta

def listar_contas_repository(usuario_id):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_contas, nome_contas, tipo_contas, saldo_contas
        FROM tbl_contas
        WHERE usuario_id = %s
    """
    
    valores = (usuario_id,)
    
    cursor.execute(sql, valores)
    
    contas = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return contas