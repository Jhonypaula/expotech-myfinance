from core.connection import conectar_banco

def buscar_usuario_por_email(email_usuario):
    
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