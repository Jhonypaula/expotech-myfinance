from repository.dashboard_repository import (
    buscar_saldo_total_repository,
    buscar_total_entradas_repository,
    buscar_total_saidas_repository
)

def buscar_saldo_total_service(usuario_id):

    saldo_total = buscar_saldo_total_repository(
        usuario_id
    )

    if not saldo_total:
        return 0

    if saldo_total[0] is None:
        return 0

    return float(saldo_total[0])

def buscar_total_entradas_service(usuario_id):

    total_entradas = buscar_total_entradas_repository(
        usuario_id
    )

    if not total_entradas:
        return 0
    
    if total_entradas[0] is None:
        return 0
    
    return float(total_entradas[0])

def buscar_total_saidas_service(usuario_id):

    total_saidas = buscar_total_saidas_repository(
        usuario_id
    )

    if not total_saidas:
        return 0
    
    if  total_saidas[0] is None:
        return 0
    
    return float(total_saidas[0])

