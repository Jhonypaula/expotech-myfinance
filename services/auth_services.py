from utils.validators import (
    validar_campo_vazio,
    validar_email,
    validar_senha
)

from repository.auth_repository import (
    buscar_usuario_por_email, 
    criar_usuario, 
    buscar_usuario_cadastrado,
    buscar_usuario_por_login
)

from utils.security import hash_senha

def cadastrar_usuario_service (nome_usuario, email_usuario, senha_usuario):
    

    if not validar_campo_vazio(nome_usuario):
        print('Nome invalido')
        
        return None
    
    if not validar_email(email_usuario):
        print('Email invalido')
        
        return None
    
    if not validar_senha(senha_usuario):
        print('Senha invalida')
        
        return None

    usuario_existente = buscar_usuario_por_email(email_usuario)
    
    if usuario_existente:
        print('Email já cadastrado')
        
        return None
    
    senha_hash = hash_senha(senha_usuario)
    
    criar_usuario(
        nome_usuario, 
        email_usuario, 
        senha_hash
    )
    
    usuario_cadastrado = buscar_usuario_cadastrado(email_usuario)
    
    return usuario_cadastrado

def login_usuario_service (email_usuario, senha_usuario):
    
    senha_hash = hash_senha(senha_usuario)
    
    usuario = buscar_usuario_por_login(
        email_usuario,
        senha_hash
    )
    
    return usuario