from back_end.repository.categoria_repository import (
    listar_categorias_repository,
    buscar_categoria_por_id
)

def listar_categorias_service():
    try:
        categorias = listar_categorias_repository()
    
        return categorias
    except Exception as e:
        
        print(f"Erro interno: {e}")

def validar_categoria_service(categoria_id):
    
    try:
        categorias = buscar_categoria_por_id(categoria_id)
    
        if not categorias:   
            return None
    
        return categorias
    
    except Exception as e:
        
        print(f"Erro interno: {e}")