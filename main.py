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

usuario_logado = None


def tela_cadastro():
    global usuario_logado
    
    nome_usuario  = input('Digite seu nome para cadastrar: ')
    email_usuario   = input('Digite seu email  para cadastrar: ')
    senha_usuario   = input('Digite sua senha para cadastrar: ')
    
    cadastro = cadastrar_usuario_service(
        nome_usuario, 
        email_usuario, 
        senha_usuario
    )

    if cadastro:
        usuario_logado = cadastro

        print('Cadastro realizado com sucesso!')
        
        return usuario_logado
    else:
        print('Erro ao cadastrar usuario!')
        
        return None

def tela_login():
    global usuario_logado
    
    email_usuario   = input('Digite seu email  para login: ')
    senha_usuario   = input('Digite sua senha para login: ')
    
    usuario = login_usuario_service(
        email_usuario, 
        senha_usuario
    )

    if usuario:
        usuario_logado = usuario

        print('Login realizado com sucesso!')

        return usuario_logado
    else:
        print('Erro ao fazer login!')
        
        return None
    
def logout():
    global usuario_logado

    usuario_logado = None

    print('Logout realizado com sucesso!')

def criar_conta(usuario_id):
    
    nome_conta = input('Digite o nome da conta: ')
    
    tipo_conta = input('Digite o tipo da conta (corrente, poupanca, carteira): ')
    
    saldo_inicial_str = input('Digite o saldo inicial da conta: ')

    conta_criada = cadastrar_conta_service(
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial_str
    )

    if conta_criada:
        print('Conta criada com sucesso!')
        
        return conta_criada
    else:
        print('Erro ao criar conta!')
        
        return None

def listar_contas(usuario_id):
    
    contas = listar_contas_service(usuario_id)

    if contas:
        print('\n=== SUAS CONTAS ===')
        
        for conta in contas:
            
            id_conta = conta[0]
            nome_conta = conta[1]
            tipo_conta = conta[2]
            saldo_conta = conta[3]
            
            print(f"ID: {id_conta:<5} | Nome: {nome_conta:<15} | Tipo: {tipo_conta:<10} | Saldo: {saldo_conta:.2f}")
            
        return contas
    else:
        print('Nenhuma conta encontrada!')
        
        return None

def editar_conta(usuario_id):
    
    listar_contas(usuario_id)
    
    try:
        id_conta = int(input("\nDigite o ID da conta: "))
        
    except ValueError:
        print("\nID invalido!")
        return None
    
    novo_nome = input("Digite o novo nome da conta: ")
    
    novo_tipo = input("Digite o novo tipo da conta (corrente, poupanca, carteira): ")
    
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
    
    confirmacao = input("Tem certeza que deseja excluir esta conta? (s/n): ").lower()
    
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

def menu_deslogado():

    print('\n==== MY FINANCE ====')
    print('1 - Login')
    print('2 - Cadastrar')
    print('3 - Sair')

    return input('Escolha: ')

def menu_logado():

    print(f"\nBem-vindo, {usuario_logado[1]}!")
    print("1 - Contas")
    print("2 - Transacoes")
    print("3 - Logout")
    print("4 - Sair")

    return input('Escolha: ')

def menu_contas():
    print(f"\n===== GESTAO DE CONTAS =====")
    print("1 - Criar conta")
    print("2 - Listar conta")
    print("3 - Editar conta")
    print("4 - Excluir conta")
    print("5 - Voltar")
    
    return input('Escolha: ')

def menu_transacoes():
    
    print("\n===== TRANSACOES =====")
    print("1 - Criar transacao")
    print("2 - Listar transacoes")
    print("3 - Editar transacao")
    print("4 - Excluir transacao")
    print("5 - Voltar")
    
    return input("Escolha: ")

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
                    print("Criar transacao")
                    
                elif opcao_transacoes == "2":
                    print("Listar transacoes")
                
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