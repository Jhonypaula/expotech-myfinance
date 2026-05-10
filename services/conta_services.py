from database.connection import conectar_banco

def cadastrar_conta(usuario_id, nome_conta, tipo_conta, saldo_inicial):
    contas_validas = ['corrente', 'poupanca', 'carteira']
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    if not nome_conta:
        print("Nome da conta nao pode ser vazio!")
        
        cursor.close()
        conexao.close()
        return None
    
    if tipo_conta not in contas_validas:
        print("Tipo de conta invalida! Escolha uma entre: 'corrente', 'poupanca' ou 'carteira'.")
        
        cursor.close()
        conexao.close()
        return None
    
    if not isinstance(saldo_inicial,(int,float)) or saldo_inicial < 0:
        print("Saldo incial deve ser um numero positivo.")
        
        cursor.close()
        conexao.close()
        return None
    
    cursor.execute("SELECT id_contas FROM tbl_contas WHERE usuario_id = %s AND nome_contas = %s", (usuario_id, nome_conta))
    conta_existente = cursor.fetchone()
    
    if conta_existente:
        print("Ja existe uma conta com esse nome para este usuario!")
        cursor.close()
        conexao.close()
        return None
    
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
def listar_conta():
    pass

def editar_conta():
    pass

def excluir_conta():
    pass
