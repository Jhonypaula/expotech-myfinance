from services.auth_services import (
    cadastrar_usuario_service,
    login_usuario_service
)
from services.conta_services import (
    cadastrar_conta_service,
    listar_contas_service,
    editar_conta_service,
    excluir_conta_service
)
from services.transacao_services import (
    criar_transacao_service
)
from services.categoria_services import (
    listar_categorias_service
)

usuario_logado = None


def tela_cadastro():
    global usuario_logado
    
    nome_usuario  = input('\nDigite seu nome para cadastrar: ')
    email_usuario   = input('\nDigite seu email  para cadastrar: ')
    senha_usuario   = input('\nDigite sua senha para cadastrar: ')
    
    cadastro = cadastrar_usuario_service(
        nome_usuario, 
        email_usuario, 
        senha_usuario
    )

    if cadastro:
        usuario_logado = cadastro

        print('\nCadastro realizado com sucesso!')
        
        return usuario_logado
    else:
        print('\nErro ao cadastrar usuario!')
        
        return None

def tela_login():
    global usuario_logado
    
    email_usuario   = input('\nDigite seu email  para login: ')
    senha_usuario   = input('\nDigite sua senha para login: ')
    
    usuario = login_usuario_service(
        email_usuario, 
        senha_usuario
    )

    if usuario:
        usuario_logado = usuario

        print('\nLogin realizado com sucesso!')

        return usuario_logado
    else:
        print('\nErro ao fazer login!')
        
        return None
    
def logout():
    global usuario_logado

    usuario_logado = None

    print('Logout realizado com sucesso!')

def criar_conta(usuario_id):
    
    nome_conta = input('\nDigite o nome da conta: ')
    
    tipo_conta = input('\nDigite o tipo da conta (corrente, poupanca, carteira): ')
    
    saldo_inicial_str = input('\nDigite o saldo inicial da conta: ')

    conta_criada = cadastrar_conta_service(
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial_str
    )

    if conta_criada:
        print('\nConta criada com sucesso!')
        
        return conta_criada
    else:
        print('\nErro ao criar conta!')
        
        return None

def listar_contas(usuario_id):
    
    contas = listar_contas_service(usuario_id)

    if contas:
        print('\n===== SUAS CONTAS =====')
        
        for conta in contas:
            
            id_conta = conta[0]
            nome_conta = conta[1]
            tipo_conta = conta[2]
            saldo_conta = conta[3]
            
            print(f"ID: {id_conta:<5} | Nome: {nome_conta:<15} | Tipo: {tipo_conta:<10} | Saldo: {saldo_conta:.2f}")
            
        return contas
    else:
        print('\nNenhuma conta encontrada!')
        
        return None

def editar_conta(usuario_id):
    
    listar_contas(usuario_id)
    
    try:
        id_conta = int(input("\nDigite o ID da conta: "))
        
    except ValueError:
        print("\nID invalido!")
        return None
    
    novo_nome = input("\nDigite o novo nome da conta: ")
    
    novo_tipo = input("\nDigite o novo tipo da conta (corrente, poupanca, carteira): ")
    
    conta_editada = editar_conta_service(
        usuario_id,
        id_conta,
        novo_nome,
        novo_tipo
    )
    
    if conta_editada:
        print("\nConta editada com sucesso!")
        
    else:
        print("\nErro ao editar a conta. ")

def excluir_conta(usuario_id):
    
    print("====== EXCLUIR CONTA =====")
    
    listar_contas(usuario_id)
    
    try:
        id_conta = int(input("\nDigite o ID da conta que deseja excluir: "))
    except ValueError:
        print("\nID invalido!")
        return None
    
    confirmacao = input("\nTem certeza que deseja excluir esta conta? (s/n): ").lower()
    
    if confirmacao != "s":
        print("\nExclusao cancelada.")
        return None
        
    conta_excluida = excluir_conta_service(
        usuario_id,
        id_conta
    )
    
    if conta_excluida:
        print("\nConta excluida com sucesso! ")
        return True
    
    else:
        print("\nErro ao excluir conta.")
        return None

def listar_categorias():
    categorias = listar_categorias_service()
    
    if not categorias:
        print("\nNenhuma categoria encontrada!")
        
        return None
    
    print("\n===== CATEGORIAS =====")
    
    for categoria in categorias:
        
        id_categorias = categoria[0]
        nome_categorias = categoria[1]
        descricao_categorias = categoria[2]
        
        print(f"ID: {id_categorias:<5} | Nome: {nome_categorias:<15} | Descricao {descricao_categorias}")
    
def criar_transacao(usuario_id):
    
    listar_contas(usuario_id)
    
    try:
        conta_id = int(input("\nDigite o ID da conta: "))
    
    except ValueError:
        print("\nID invalido")
        return None
    
    listar_categorias()
    
    categoria_id = input("\nDigite o Id da categoria: ")
    
    tipo_transacao = input("\nDigite o tipo de transacao (entrada/saida): ")
    
    valor_transacao = input("\nDigite o valor da transacao: ")
    
    descricao_transacao = input("\nDigite a descricao da transacao: ")
    
    transacao = criar_transacao_service(
        usuario_id,
        conta_id,
        categoria_id,
        tipo_transacao,
        valor_transacao,
        descricao_transacao
    )
    
    if transacao:
        print("\nTransacao criada com sucesso")
        return True
    
    else:
        print("\nErro ao criar transacao.")
        return None

def menu_deslogado():

    print('\n==== MY FINANCE ====')
    print('1 - Login')
    print('2 - Cadastrar')
    print('3 - Sair')

    return input('\nEscolha: ')

def menu_logado():

    print(f"\nBem-vindo, {usuario_logado[1]}!")
    print("1 - Contas")
    print("2 - Transacoes")
    print("3 - Logout")
    print("4 - Sair")

    return input('\nEscolha: ')

def menu_contas():
    print(f"\n===== GESTAO DE CONTAS =====")
    print("1 - Criar conta")
    print("2 - Listar conta")
    print("3 - Editar conta")
    print("4 - Excluir conta")
    print("5 - Voltar")
    
    return input('\nEscolha: ')

def menu_transacoes():
    
    print("\n===== TRANSACOES =====")
    print("1 - Criar transacao")
    print("2 - Listar transacoes")
    print("3 - Editar transacao")
    print("4 - Excluir transacao")
    print("5 - Voltar")
    
    return input("\nEscolha: ")

def main():

    # global usuario_logado

    while True:

        # usuario deslogado
        if usuario_logado is None:

            opcao = menu_deslogado()

            if opcao == "1":
                tela_login()

            elif opcao == "2":
                tela_cadastro()

            elif opcao == "3":

                print('Saindo do sistema')

                break

            else:
                print('Opção inválida')

        # usuario logado
        else:

            opcao = menu_logado()

            if opcao == "1":

                opcao_contas = menu_contas()
                
                if opcao_contas == "1":
                    criar_conta(usuario_logado[0])
                    
                elif opcao_contas == "2":
                    listar_contas(usuario_logado[0])
                    
                    
                elif opcao_contas == "3":
                    editar_conta(usuario_logado[0])
                    
                elif opcao_contas == "4":
                    excluir_conta(usuario_logado[0])
                    
                elif opcao_contas == "5":
                    continue
                
            elif opcao == "2":
                opcao_transacoes = menu_transacoes()
                if opcao_transacoes == "1":
                    criar_transacao(usuario_logado[0])
                    
                elif opcao_transacoes == "2":
                    listar_categorias()
                
                elif opcao_transacoes == "3":
                    print("Editar transacao")
                
                elif opcao_transacoes == "4":
                    print("Excluir transacao")
                
                elif opcao_transacoes == "5":
                    continue
                
            elif opcao == "3":
                logout()
            
            elif opcao == "4":
                print('Saindo do sistema')
                break
            
            else:
                print('Opcao invalida')

if __name__ == "__main__":
    main()