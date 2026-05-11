from database.connection import conectar_banco

def cadastrar_conta(usuario_id, nome_conta, tipo_conta, saldo_inicial):
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    
    sql = """
        INSERT INTO tbl_contas (usuario_id, nome_contas, tipo_contas, saldo_contas)
        VALUES (%s, %s, %s, %s)
    """
    
    valores = usuario_id, nome_conta, tipo_conta, saldo_inicial
    
    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.execute("SELECT id_contas FROM tbl_contas WHERE usuario_id = %s AND nome_contas = %s", (usuario_id, nome_conta))
    nova_conta = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return nova_conta
def listar_conta(usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT nome_contas, tipo_contas, saldo_contas 
        FROM tbl_contas 
        WHERE usuario_id = %s
    """, (usuario_id,))
    
    contas = cursor.fetchall()
    
    if contas:
        print("\n==== SUAS CONTAS ====")
        
        for conta in contas:
            print(f"Nome: {conta[0]} Tipo: {conta[1]} Saldo: {conta[2]:.2f} BRL")
    else:
        print("Voce nao tem contas cadastrada.")
    
    cursor.close()
    conexao.close()
def editar_conta():
    pass

def excluir_conta():
    pass
