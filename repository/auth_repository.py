from core.connection import conectar_banco

def buscar_usuario_por_email(email_usuario):
    
    conexao = conectar_banco()
    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT id_usuarios, nome_usuarios, email_usuarios 
        FROM tbl_usuarios 
        WHERE email_usuarios = %s
    """

    valores = (email_usuario,)

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def criar_usuario(nome_usuario, email_usuario, senha_hash):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO tbl_usuarios (
            nome_usuarios, 
            email_usuarios, 
            senha_usuarios
        )
        VALUES (%s, %s, %s)
    """

    valores = (
        nome_usuario, 
        email_usuario, 
        senha_hash
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()
    
def buscar_usuario_cadastrado(email_usuario):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT id_usuarios, nome_usuarios, email_usuarios 
        FROM tbl_usuarios 
        WHERE email_usuarios = %s
    """

    valores = (email_usuario,)

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def buscar_usuario_por_login(email_usuario, senha_hash):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    sql = """
        SELECT id_usuarios, nome_usuarios, email_usuarios 
        FROM tbl_usuarios 
        WHERE email_usuarios = %s 
        AND senha_usuarios = %s
    """
    valores = (
        email_usuario, 
        senha_hash
    )
    cursor.execute(sql, valores)
    
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return usuario

#==========================================
# Soft Delete do Usuário
#==========================================

def excluir_conta(usuario_id) -> str:
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        UPDATE tbl_usuarios
        SET ativo = "False"
        WHERE id_usuarios = %s
    """
    valores = (
        usuario_id,
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return "Conta excluída com sucesso"

def verificar_status_conta(usuario_id) -> bool:

    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT ativo
        FROM tbl_usuarios 
        WHERE id_usuarios = %s
    """
    valores = (
        usuario_id,
    )

    cursor.execute(sql, valores)

    status = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return status

def atualizar_senha_usuario(
    usuario_id,
    senha_hashed
):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    sql = """
        UPDATE tbl_usuarios
        SET senha_usuarios = %s
        WHERE id_usuarios = %s
    """

    valores = (
        senha_hashed,
        usuario_id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()