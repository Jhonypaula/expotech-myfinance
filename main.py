from services.auth_services import cadastrar_usuario, login_usuario

usuario_logado = None


def logout():
    global usuario_logado

    usuario_logado = None

    print('Logout realizado com sucesso!')


def menu_deslogado():

    print('\n==== MY FINANCE ====')
    print('1 - Login')
    print('2 - Cadastrar')
    print('3 - Sair')

    return input('Escolha: ')


def menu_logado():

    print(f'\nBem-vindo, {usuario_logado[1]}!')
    print('1 - Logout')
    print('2 - Sair')

    return input('Escolha: ')


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

                logout()

            elif opcao == "2":

                print('Saindo do sistema')

                break

            else:
                print('Opção inválida')


if __name__ == "__main__":
    main()