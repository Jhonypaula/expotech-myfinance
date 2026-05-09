from database.connection import conectar_banco
from utils.validators import validar_campo_vazio, validar_email, validar_senha
from utils.security import hash_senha

def cadastrar_usuario ():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    nome_usuario  = input('Digite seu nome para cadastrar: ')
    email_usuario   = input('Digite seu email  para cadastrar: ')
    senha_usuario   = input('Digite sua senha para cadastrar: ')

    if not validar_campo_vazio(nome_usuario):
        print('Nome invalido')
        
        cursor.close()
        conexao.close()
        
        return
    
    if not validar_email(email_usuario):
        print('Email invalido')
        
        cursor.close()
        conexao.close()
        
        return
    
    if not validar_senha(senha_usuario):
        print('Senha invalida')
        
        cursor.close()
        conexao.close()
        
        return

    cursor.execute("SELECT id_usuarios FROM tbl_usuarios WHERE email_usuarios = %s", (email_usuario,))
    
    usuario_existente = cursor.fetchone()
    
    if usuario_existente:
        print('Email ja cadastrado')
        
        cursor.close()
        conexao.close()
        
        return

    senha_hash = hash_senha(senha_usuario)

    sql = """INSERT INTO tbl_usuarios (nome_usuarios, email_usuarios, senha_usuarios)
        VALUES ( %s, %s, %s)"""

    valores = nome_usuario, email_usuario, senha_hash

    cursor.execute(sql, valores)  
    conexao.commit()
    
    cursor.execute(
        """
        SELECT id_usuarios, nome_usuarios, email_usuarios 
        FROM tbl_usuarios WHERE email_usuarios = %s
        """, 
        (email_usuario,)
    )
    
    usuario_cadastrado = cursor.fetchone()

    print('Usuario cadastrado com sucesso!')
    
    cursor.close()
    conexao.close()

    return usuario_cadastrado

def login_usuario ():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    email_usuario   = input('Digite seu email  para login: ')
    senha_usuario   = input('Digite sua senha para login: ')

    senha_hash = hash_senha(senha_usuario)

    sql = """
    SELECT id_usuarios, nome_usuarios, email_usuarios 
    FROM tbl_usuarios 
    WHERE email_usuarios = %s AND senha_usuarios = %s
    """

    valores = email_usuario, senha_hash

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario:
        return usuario
    else:
        print("Email ou senha incorretos")
        return None

def logout ():
    print("Logout realizado!")