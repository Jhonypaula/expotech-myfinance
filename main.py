from services.auth_services import cadastrar_usuario, login_usuario
from services.conta_services import cadastrar_conta, listar_conta, editar_conta, excluir_conta

usuario_logado = None


def logout():
    global usuario_logado

    usuario_logado = None

    print('Logout realizado com sucesso!')

def criar_conta(usuario_id):
    nome_conta = input("Digite o nome da conta (ex: NuBank): ")
    saldo_inicial_str = input("Digite o saldo incial da conta: ")
    
    saldo_inicial_str = saldo_inicial_str.replace(',', '.')
    
    try:
        saldo_inicial = float(saldo_inicial_str)
    except ValueError:
        print("\nSaldo incial invalido! Por favor, insira um numero valido.")
        
        return
    tipo_conta = input("Digite o tipo de conta dentre elas (corrente, poupanca, carteira): ")
    
    MAX_SALDO = 99999999.99
    
    contas_validas = ['corrente', 'poupanca', 'carteira']
    
    if not nome_conta:
        print("\nNome da conta nao pode ser vazio!")
        
        return None
    
    if tipo_conta not in contas_validas:
        print("\nTipo de conta invalida! Escolha uma entre: 'corrente', 'poupanca' ou 'carteira'.")
        
        return None
    
    if not isinstance(saldo_inicial,(int,float)) or saldo_inicial < 0:
        print("\nSaldo incial deve ser um numero positivo.")
        
        return None
    
    if saldo_inicial > MAX_SALDO:
        print(f"\nVoce nao e o ELON MUSK!! O saldo incial nao pode ser maior que {MAX_SALDO}")
        
        return
    
    conta_criada = cadastrar_conta(usuario_id, nome_conta, tipo_conta, saldo_inicial)
    
    if conta_criada:
        print(f"\nConta '{nome_conta}' criada com sucesso!")
        
    else:
        print("\nErro ao criar a conta.")
def menu_deslogado():

    print('\n==== MY FINANCE ====')
    print('1 - Login')
    print('2 - Cadastrar')
    print('3 - Sair')

    return input('Escolha: ')


def menu_logado():

    print(f"\nBem-vindo, {usuario_logado[1]}!")
    print("1 - Contas")
    print("2 - Logout")
    print("3 - Sair")

    return input('Escolha: ')

def menu_contas():
    print(f"\n===== GESTAO DE CONTAS =====")
    print("1 - Criar conta")
    print("2 - Listar conta")
    print("3 - Editar conta")
    print("4 - Excluir conta")
    print("5 - Voltar")
    
    return input('Escollha: ')

def main():

    global usuario_logado

    while True:

        # usuario deslogado
        if usuario_logado is None:

            opcao = menu_deslogado()

            if opcao == "1":

                usuario = login_usuario()

                if usuario:
                    usuario_logado = usuario

                    print('Login realizado com sucesso!')

            elif opcao == "2":

                cadastro = cadastrar_usuario()

                if cadastro:
                    usuario_logado = cadastro

                    print('Cadastro realizado com sucesso!')

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
                    listar_conta(usuario_logado[0])
                    
                    
                elif opcao_contas == "3":
                    editar_conta()
                    
                    print('Editar conta')
                elif opcao_contas == "4":
                    excluir_conta()
                    
                    print('Excluir conta')
                elif opcao_contas == "5":
                    continue
            elif opcao == "2":
                logout()
                
            elif opcao == "3":
                print('Saindo do sistema . . .')
                break
            else:
                print('Opcao invalida')

if __name__ == "__main__":
    main()