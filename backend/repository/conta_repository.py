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
        SELECT id_contas, nome_contas, tipo_contas, saldo_contas, data_criacao_contas
        FROM tbl_contas
        WHERE usuario_id = %s
    """
    
    valores = (usuario_id,)
    
    cursor.execute(sql, valores)
    
    contas = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return contas

def buscar_conta_por_id(
    usuario_id,
    id_conta
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_contas
        FROM tbl_contas
        WHERE usuario_id = %s
        AND id_contas = %s
    """
    
    valores = (
        usuario_id, 
        id_conta
    )
    
    cursor.execute(sql, valores)
    
    conta = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return conta
    
def editar_conta_repository(
    usuario_id,
    id_conta,
    novo_nome,
    novo_tipo
):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        UPDATE tbl_contas
        SET nome_contas = %s,
            tipo_contas = %s
        WHERE usuario_id = %s
        AND id_contas = %s
    """
    
    valores = (
        novo_nome,
        novo_tipo,
        usuario_id,
        id_conta
    )
    
    cursor.execute(sql, valores)
    
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
def excluir_conta_repository(
    usuario_id,
    id_conta
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        DELETE FROM tbl_contas
        WHERE usuario_id = %s
        AND id_contas = %s
    """
    
    valores = (
        usuario_id,
        id_conta
    )
    
    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()

def atualizar_saldo_repository(
    id_conta,
    novo_saldo
):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        UPDATE tbl_contas
        SET saldo_contas = %s
        WHERE id_contas = %s
    """
    
    valores = (
        novo_saldo,
        id_conta  
    )
    
    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
def buscar_saldo_conta_repository(id_conta):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT saldo_contas
        FROM tbl_contas
        WHERE id_contas = %s
    """
    
    valores = id_conta,
    
    cursor.execute(sql, valores)
    saldo_atual = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return saldo_atual    