from back_end.repository.transacao_repository import (
    criar_transacao_repository,
    listar_transacoes_repository,
    buscar_transacao_por_id,
    excluir_transacao_repository,
    editar_transacao_repository,
    filtrar_transacoes_tipo_repository,
    filtrar_transacoes_categoria_repository,
    filtrar_transacoes_descricao_repository
)
from back_end.repository.conta_repository import (
    buscar_conta_por_id,
    buscar_saldo_conta_repository,
    atualizar_saldo_repository
)

from back_end.utils.validators import (
    validar_campo_vazio
)
from back_end.services.categoria_services import (
    validar_categoria_service
)

def criar_transacao_service(
    
    usuario_id,
    conta_id,
    categoria_id,
    tipo_transacao,
    valor_transacao_str,
    descricao_transacao,
    
):
    try:
        TIPOS_VALIDOS = [
            'entrada',
            'saida'
        ]
        
        # ===============================
        # VALIDAR TIPOS
        # ===============================
        
        if tipo_transacao not in TIPOS_VALIDOS:
            print("\nTipo de transacao invalida!")
            return None
        
        # ===============================
        # VALIDAR VALOR
        # ===============================
        
        valor_transacao_str = valor_transacao_str.replace(',', '.')
        
        try:
            valor_transacao = float(valor_transacao_str)
            
        except ValueError:
            print("\nO valor deve ser um número válido")
            return None
            
        if valor_transacao <= 0:
            print("\nO valor deve ser um número positivo")
            return None
        
        # ===============================
        # VALIDAR DESCRICAO
        # ===============================
        
        if not validar_campo_vazio(descricao_transacao):
            print("\nDescricao obrigatoria!")
            return None
        
        if len(descricao_transacao) > 15:
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
            descricao_transacao
        )
        
        return True
    
    except Exception as e:
        print(f"Erro interno: {e}")
        return None

def listar_transacao_service(
    usuario_id,
    conta_id
):
    try:
        conta_existente = buscar_conta_por_id(
            usuario_id, 
            conta_id
        )
        
        if not conta_existente:
            print("\nConta nao encontrada ou nao pertence ao usuario")
            return None 
        
        transacoes = listar_transacoes_repository(conta_id)
        
        return transacoes
    
    except Exception as e:
        print(f"Erro interno: {e}")

def excluir_transacao_service(
    usuario_id,
    conta_id,
    id_transacoes
):
    try:
        conta_existente = buscar_conta_por_id(
            usuario_id, 
            conta_id
        )
        
        if not conta_existente:
            print("\nConta nao encontrada!")
            return None
        
        transacao_existente = buscar_transacao_por_id(
            conta_id, 
            id_transacoes
        )
        
        if not transacao_existente:
            print("\nTransacao nao encontrada!")
            return None
            
        tipo_transacao = transacao_existente[1]
        valor_transacao = float(transacao_existente[2])
        
        saldo_atual = buscar_saldo_conta_repository(conta_id)
        
        if not saldo_atual:
            print("\nErro ao buscar saldo!")
            return None
        
        saldo_atual = float(saldo_atual[0])
        
        if tipo_transacao == 'entrada':
            novo_saldo = saldo_atual - valor_transacao
        
        else:
            novo_saldo = saldo_atual + valor_transacao
            
        atualizar_saldo_repository(
            conta_id,
            novo_saldo
        )
        excluir_transacao_repository(
            conta_id,
            id_transacoes
        )
        
        return True

    except Exception as e:
        print(f"Erro interno: {e}")
    
def editar_transacao_service(
    usuario_id,
    conta_id,
    id_transacao,
    categoria_id,
    tipo_transacao,
    valor_transacao_str,
    descricao_transacao
):
    
    try:
        TIPOS_VALIDOS = [
            'entrada',
            'saida'
        ]

        if tipo_transacao not in TIPOS_VALIDOS:
            print("\nTipo de transacao invalido!")
            return None
        
        valor_transacao_str = valor_transacao_str.replace(',', '.')

        try:
            valor_transacao = float(valor_transacao_str)

        except ValueError:
            print("\nO valor deve ser um número válido")
            return None
        
        if valor_transacao <= 0:
            print("\nO valor deve ser um número positivo")
            return None

        if not validar_campo_vazio(descricao_transacao):
            print("\nDescricao obrigatoria!")
            return None
        
        if len(descricao_transacao) > 15:
            print("\nDescricao muito longa! Maximo 15")
            return None
        
        conta_existente = buscar_conta_por_id(
            usuario_id, 
            conta_id
        )
        
        if not conta_existente:
            print("\nConta nao encontrada ou nao pertence ao usuario.")
            return None
        
        categoria_existente = validar_categoria_service(
            categoria_id
        )
        
        if not categoria_existente:
            print("\nCategoria nao encontrada!")
            return None
        
        transacao_existente = buscar_transacao_por_id(
            conta_id,
            id_transacao
        )

        if not transacao_existente:
            print("\nTransacao nao encontrada!")
            return None
        
        # DEFININDO DADOS ANTIGOS
        
        tipo_antigo = transacao_existente[1]

        valor_antigo = float(transacao_existente[2])

        # BUSCAR SALDO ATUAL

        saldo_atual = buscar_saldo_conta_repository(
            conta_id
        )

        if not saldo_atual:
            print("\nErro ao buscar saldo!")
            return None
        
        saldo_atual = float(saldo_atual[0])

        # DESFAZER TRANSACAO ANTIGA

        if tipo_antigo == 'entrada':
            saldo_atual -= valor_antigo
        
        else:
            saldo_atual += valor_antigo

        # APLICAR TRANSACAO NOVA
        
        if tipo_transacao == 'entrada':
            novo_saldo = saldo_atual + valor_transacao

        else:
            if valor_transacao > saldo_atual:
                print("\nSaldo insuficiente!")
                return None
            
            novo_saldo = saldo_atual - valor_transacao

        # ATUALIZAR SALDO

        atualizar_saldo_repository(
            conta_id,
            novo_saldo
        )

        # EDITAR TRANSACAO
        
        editar_transacao_repository(
            conta_id,
            id_transacao,
            categoria_id,
            tipo_transacao,
            valor_transacao,
            descricao_transacao
        )

        return True
    
    except Exception as e:
        
        print(f"Erro interno: {e}")

def filtrar_transacoes_tipo_service(
    usuario_id,
    conta_id,
    tipo_transacao
):
    
    try:
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
            print(
                "\nConta nao encontrada "
                "ou nao pertence ao usuario!"
            )

            return None

        transacoes = (
            filtrar_transacoes_tipo_repository(
                conta_id,
                tipo_transacao
            )
        )

        return transacoes
    
    except Exception as e:
        
        print(f"Erro interno: {e}")

def filtrar_transacao_categoria_service(
    usuario_id,
    conta_id,
    categoria_id
):
    
    try:
        conta_existente = buscar_conta_por_id(
            usuario_id,
            conta_id
        )

        if not conta_existente:

            print(
                "\nConta nao encontrada "
                "ou nao pertence ao usuario!"
            )

            return None

        categoria_existente = validar_categoria_service(
            categoria_id
        )

        if not categoria_existente:

            print("\nCategoria invalida!")
            return None

        transacoes = (
            filtrar_transacoes_categoria_repository(
                conta_id,
                categoria_id
            )
        )

        return transacoes
    
    except Exception as e:
        
        print(f"Erro interno: {e}")

def filtrar_transacoes_descricao_service(
    usuario_id,
    conta_id,
    descricao
):

    try:
        conta_existente = buscar_conta_por_id(
            usuario_id,
            conta_id
        )

        if not conta_existente:

            print(
                "\nConta nao encontrada "
                "ou nao pertence ao usuario!"
            )

            return None

        if not validar_campo_vazio(descricao):

            print("\nDescricao obrigatoria!")
            return None

        transacoes = (
            filtrar_transacoes_descricao_repository(
                conta_id,
                descricao
            )
        )

        return transacoes
    
    except Exception as e:
        
        print(f"Erro interno: {e}")