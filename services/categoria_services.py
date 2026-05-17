from repository.categoria_repository import (
    listar_categorias_repository,
    buscar_categoria_por_id
)

def listar_categorias_service():
    categorias = listar_categorias_repository()
    
    return categorias

def validar_categoria_service(categoria_id):
    categorias = buscar_categoria_por_id(categoria_id)
    
    if not categorias:   
        return None
    
    return categorias