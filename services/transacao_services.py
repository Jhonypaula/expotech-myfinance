from repository.transacao_repository import (
    criar_transacao_repository
)
from repository.conta_repository import (
    buscar_conta_por_id
)

from utils.validators import (
    validar_campo_vazio
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
    
    if tipo_transacao not in TIPOS_VALIDOS:
        print("\nTipo de transacao invalido!")
        return None
    
    conta_existente = buscar_conta_por_id(
        usuario_id, 
        conta_id
    )
    
    if not conta_existente:
        print("\nConta nao encontrada ou nao pertence ao usuario.")
        return None
    
    valor_transacoes_str = valor_transacoes_str.replace(',', '.')
    
    try:
        valor_transacao = float(valor_transacoes_str)
        
    except ValueError:
        print("O valor deve ser um número válido")
        return None
        
    if valor_transacao <= 0:
        print("O valor deve ser um número positivo")
        return None
    
    if not validar_campo_vazio(descricao_transacoes):
        print("\nDescricao obrigatoria!")
        return None
    
    criar_transacao_repository(
        conta_id,
        categoria_id,
        tipo_transacao,
        valor_transacao,
        descricao_transacoes
    )
    
    return True
        