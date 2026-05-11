from repository.conta_repository import (
    criar_conta_repository,
    buscar_conta_por_nome,
    listar_contas_repository
)

def cadastrar_conta_service(
    usuario_id,
    nome_conta,
    tipo_conta,
    saldo_inicial_str
):
    
    contas_validas = [
        'corrente', 
        'poupança', 
        'carteira'
    ]
    
    MAX_SALDO = 99999999.99
    
    if not nome_conta:
        print('\nNome da conta é obrigatório')
        
        return None
    
    if tipo_conta not in contas_validas:
        print('\nTipo de conta inválida. Tipos válidos: corrente, poupança, carteira')
        
        return None
    
    saldo_inicial_str = saldo_inicial_str.replace(',', '.')
    
    try:
        saldo_inicial = float(saldo_inicial_str)
    except ValueError:
        print('\nSaldo inicial deve ser um número válido')
        
        return None
    
    if saldo_inicial < 0:
        print('\nSaldo inicial não pode ser negativo')
        
        return None
    
    if saldo_inicial > MAX_SALDO:
        print(f'\nSaldo inicial não pode ser maior que {MAX_SALDO}')
        
        return None 
    
    conta_existente = buscar_conta_por_nome(
        usuario_id,
        nome_conta
    )
    
    if conta_existente:
        print('\nJá existe uma conta com esse nome')
        
        return None
    
    criar_conta_repository(
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial
    )
    
    nova_conta = buscar_conta_por_nome(
        usuario_id,
        nome_conta
    )
    
    return nova_conta

def listar_contas_service(usuario_id):
    
    contas = listar_contas_repository(usuario_id)
    
    return contas