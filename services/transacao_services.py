from repository.transacao_repository import (
    criar_transacao_repository,
    listar_transacoes_repository
)
from repository.conta_repository import (
    buscar_conta_por_id,
    buscar_saldo_conta_repository,
    atualizar_saldo_repository
)

from utils.validators import (
    validar_campo_vazio
)
from services.categoria_services import (
    validar_categoria_service
)

def criar_transacao_service(
    
    usuario_id,
    conta_id,
    categoria_id,
    tipo_transacao,
    valor_transacoes_str,
    descricao_transacoes,
    
):
    
    TIPOS_VALIDOS = [
        'entrada',
        'saida'
    ]
    
    # ===============================
    # VALIDAR TIPOS
    # ===============================
    
    if tipo_transacao not in TIPOS_VALIDOS:
        print("\nTipo de transacao invalido!")
        return None
    
    # ===============================
    # VALIDAR VALOR
    # ===============================
    
    valor_transacoes_str = valor_transacoes_str.replace(',', '.')
    
    try:
        valor_transacao = float(valor_transacoes_str)
        
    except ValueError:
        print("O valor deve ser um número válido")
        return None
        
    if valor_transacao <= 0:
        print("O valor deve ser um número positivo")
        return None
    
    # ===============================
    # VALIDAR DESCRICAO
    # ===============================
    
    if not validar_campo_vazio(descricao_transacoes):
        print("\nDescricao obrigatoria!")
        return None
    
    if len(descricao_transacoes) > 15:
        print("\nDescricao muito longa! Maximo 15")
        return None
    
    # ===============================
    # VALIDAR CONTA
    # ===============================
    
    conta_existente = buscar_conta_por_id(
        usuario_id, 
        conta_id
    )
    
    if not conta_existente:
        print("\nConta nao encontrada ou nao pertence ao usuario.")
        return None
    
    # ===============================
    # VALIDAR CATEGORIA
    # ===============================
    
    categoria_existente = validar_categoria_service(categoria_id)
    
    if not categoria_existente:
        print("\nCategoria invalida")
        return None
    
    # ===============================
    # BUSCAR SALDO
    # ===============================
    
    saldo_atual = buscar_saldo_conta_repository(conta_id)
    
    if not saldo_atual:
        print("\nErro ao buscar saldo!")
        return None
    
    saldo_atual = float(saldo_atual[0])
    
    # ===============================
    # CALCULAR NOVO SALDO
    # ===============================
    
    if tipo_transacao == 'entrada':
        novo_saldo = saldo_atual + valor_transacao
        
    else:
        if valor_transacao > saldo_atual:
            print("\nSaldo insuficiente!")
            return None
        
        novo_saldo = saldo_atual - valor_transacao
    
    # ===============================
    # ATUALIZAR SALDO
    # ===============================
    
    atualizar_saldo_repository(
        conta_id, 
        novo_saldo
    )
    
    # ===============================
    # CRIAR TRANSACAO
    # ===============================
    
    criar_transacao_repository(
        conta_id,
        categoria_id,
        tipo_transacao,
        valor_transacao,
        descricao_transacoes
    )
    
    return True

def listar_transacao_service(
    usuario_id,
    conta_id
):
    
    conta_existente = buscar_conta_por_id(
        usuario_id, 
        conta_id
    )
    
    if not conta_existente:
        print("\nConta nao encontrada ou nao pertence ao usuario")
        return None 
    
    transacoes = listar_transacoes_repository(conta_id)
    
    return transacoes