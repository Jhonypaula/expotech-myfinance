from database.connection import conectar_banco

def cadastrar_usuario ():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    nome_usuario  = input('Digite seu nome para cadastrar: ')
    email_usuario   = input('Digite seu email  para cadastrar: ')
    senha_usuario   = input('Digite sua senha para cadastrar: ')

    sql = """INSERT INTO tbl_usuarios (nome_usuarios, email_usuarios, senha_usuarios)
        VALUES ( %s, %s, %s)"""

    valores = nome_usuario, email_usuario, senha_usuario

    cursor.execute(sql, valores)  
    conexao.commit()

    cursor.close()
    conexao.close()

def login_usuario ():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    email_usuario   = input('Digite seu email  para login: ')
    senha_usuario   = input('Digite sua senha para login: ')

    sql = """SELECT * FROM tbl_usuarios 
        WHERE email_usuarios = %s AND senha_usuarios = %s"""

    valores = email_usuario, senha_usuario

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    if usuario:
        print(f"Bem-vindo! {usuario[1]}")
    else:
        print("Email ou senha incorretos")

    cursor.close()
    conexao.close()

def logout ():
    print("Logout realizado!")