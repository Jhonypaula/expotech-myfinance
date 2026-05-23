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
    criar_transacao_service,
    listar_transacao_service,
    excluir_transacao_service,
    editar_transacao_service,
    filtrar_transacoes_tipo_service,
    filtrar_transacao_categoria_service,
    filtrar_transacoes_descricao_service
)

from services.categoria_services import (
    listar_categorias_service
)

from services.dashboard_services import (
    buscar_saldo_total_service,
    buscar_total_entradas_service,
    buscar_total_saidas_service,
    buscar_gastos_categoria_service,
    buscar_maior_categoria_service,
    buscar_quantidade_transacoes_service
)
usuario_logado = None

def tela_cadastro():

    global usuario_logado

    nome_usuario = input('\nDigite seu nome para cadastrar: ')
    email_usuario = input('\nDigite seu email para cadastrar: ')
    senha_usuario = input('\nDigite sua senha para cadastrar: ')

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

    email_usuario = input('\nDigite seu email para login: ')
    senha_usuario = input('\nDigite sua senha para login: ')

    usuario = login_usuario_service(
        email_usuario,
        senha_usuario
    )

    if usuario:

        usuario_logado = usuario

        print('\nLogin realizado com sucesso!')

        return usuario

    else:
        print('\nErro ao fazer login!')
        return None

def logout():

    global usuario_logado

    usuario_logado = None

    print('\nLogout realizado com sucesso!')

def criar_conta(usuario_id):

    nome_conta = input('\nDigite o nome da conta: ')

    tipo_conta = input(
        '\nDigite o tipo da conta (corrente, poupanca, carteira): '
    ).strip().lower()

    saldo_inicial_str = input(
        '\nDigite o saldo inicial da conta: '
    )

    conta_criada = cadastrar_conta_service(
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial_str
    )

    if conta_criada:

        print('\nConta criada com sucesso!')
        return True

    else:
        print('\nErro ao criar conta!')
        return None

def listar_contas(usuario_id):

    contas = listar_contas_service(usuario_id)

    if not contas:

        print('\nNenhuma conta encontrada!')
        return None

    print('\n===== SUAS CONTAS =====')

    for conta in contas:

        id_conta = conta[0]
        nome_conta = conta[1]
        tipo_conta = conta[2]
        saldo_conta = conta[3]

        print(
            f"ID: {id_conta:<5} | "
            f"Nome: {nome_conta:<15} | "
            f"Tipo: {tipo_conta:<10} | "
            f"Saldo: {saldo_conta:.2f}"
        )

    return contas

def editar_conta(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        id_conta = int(input("\nDigite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    novo_nome = input("\nDigite o novo nome da conta: ")

    novo_tipo = input(
        "\nDigite o novo tipo da conta (corrente, poupanca, carteira): "
    ).strip().lower()

    conta_editada = editar_conta_service(
        usuario_id,
        id_conta,
        novo_nome,
        novo_tipo
    )

    if conta_editada:
        print("\nConta editada com sucesso!")
        return True

    else:
        print("\nErro ao editar conta.")
        return None

def excluir_conta(usuario_id):

    print("\n===== EXCLUIR CONTA =====")

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        id_conta = int(
            input("\nDigite o ID da conta que deseja excluir: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None

    confirmacao = input(
        "\nTem certeza que deseja excluir esta conta? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nExclusao cancelada.")
        return None

    conta_excluida = excluir_conta_service(
        usuario_id,
        id_conta
    )

    if conta_excluida:

        print("\nConta excluida com sucesso!")
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

        id_categoria = categoria[0]
        nome_categoria = categoria[1]
        descricao_categoria = categoria[2]

        print(
            f"ID: {id_categoria:<5} | "
            f"Nome: {nome_categoria:<15} | "
            f"Descricao: {descricao_categoria}"
        )

    return categorias

def criar_transacao(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        conta_id = int(input("\nDigite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    categorias = listar_categorias()

    if not categorias:
        return None

    try:
        categoria_id = int(
            input("\nDigite o ID da categoria: ")
        )

    except ValueError:
        print("\nCategoria invalida!")
        return None

    tipo_transacao = input(
        "\nDigite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    valor_transacao = input(
        "\nDigite o valor da transacao: "
    )

    descricao_transacao = input(
        "\nDigite a descricao da transacao: "
    )

    transacao = criar_transacao_service(
        usuario_id,
        conta_id,
        categoria_id,
        tipo_transacao,
        valor_transacao,
        descricao_transacao
    )

    if transacao:

        print("\nTransacao criada com sucesso!")
        return True

    else:
        print("\nErro ao criar transacao.")
        return None

def listar_transacoes(
    usuario_id,
    conta_id=None
):

    if conta_id is None:

        contas = listar_contas(usuario_id)

        if not contas:
            return None

        try:
            conta_id = int(input("\nDigite o ID da conta: "))

        except ValueError:
            print("\nID invalido!")
            return None

    transacoes = listar_transacao_service(
        usuario_id,
        conta_id
    )

    if not transacoes:

        print("\nNenhuma transacao encontrada!")
        return None

    print("\n===== TRANSACOES =====")

    for transacao in transacoes:

        id_transacao = transacao[0]
        tipo_transacao = transacao[1]
        valor_transacao = transacao[2]
        descricao_transacao = transacao[3]
        categoria_transacao = transacao[4]

        data = transacao[5].strftime("%d/%m/%Y")

        print(
            f"ID: {id_transacao:<5} | "
            f"Tipo: {tipo_transacao:<10} | "
            f"Valor: {valor_transacao:<10.2f} | "
            f"Categoria: {categoria_transacao:<15} | "
            f"Desc: {descricao_transacao:<15} | "
            f"Data: {data}"
        )

    return transacoes

def excluir_transacao(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        conta_id = int(input("\nDigite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    transacoes = listar_transacoes(
        usuario_id,
        conta_id
    )

    if not transacoes:
        return None

    try:
        id_transacao = int(
            input("\nDigite o ID da transacao: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None

    confirmacao = input(
        "\nTem certeza que deseja excluir esta transacao? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nExclusao cancelada.")
        return None

    transacao_excluida = excluir_transacao_service(
        usuario_id,
        conta_id,
        id_transacao
    )

    if transacao_excluida:

        print("\nTransacao excluida com sucesso!")
        return True

    else:
        print("\nErro ao excluir transacao.")
        return None

def editar_transacao(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        conta_id = int(input("\nDigite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    transacoes = listar_transacoes(
        usuario_id,
        conta_id
    )

    if not transacoes:
        return None

    try:
        id_transacao = int(
            input("\nDigite o ID da transacao: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None
    
    ids_transacoes = [
        transacao[0]
        for transacao in transacoes
    ]

    if id_transacao not in ids_transacoes:

        print("\nID da transacao nao pertence a esta conta!")
        return None

    categorias = listar_categorias()

    if not categorias:
        return None

    try:
        categoria_id = int(
            input("\nDigite o ID da categoria: ")
        )

    except ValueError:
        print("\nCategoria invalida!")
        return None
    
    ids_categorias = [
        categoria[0]
        for categoria in categorias
    ]

    if categoria_id not in ids_categorias:

        print("\nID da categoria invalida!")
        return None

    tipo_transacao = input(
        "\nDigite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    valor_transacao_str = input(
        "\nDigite o valor da transacao: "
    )

    descricao_transacao = input(
        "\nDigite a descricao da transacao: "
    )

    confirmacao = input(
        "\nTem certeza que deseja editar esta transacao? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nEdicao cancelada.")
        return None

    transacao_editada = editar_transacao_service(
        usuario_id,
        conta_id,
        id_transacao,
        categoria_id,
        tipo_transacao,
        valor_transacao_str,
        descricao_transacao
    )

    if transacao_editada:

        print("\nTransacao editada com sucesso!")
        return True

    else:
        print("\nErro ao editar transacao.")
        return None

def filtrar_transacoes_tipo(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        conta_id = int(
            input("\nDigite o ID da conta: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None
    
    ids_contas = [
        conta[0]
        for conta in contas
    ]

    if conta_id not in ids_contas:

        print(
            "\nConta nao encontrada "
            "ou nao pertence ao usuario!"
        )

        return None

    tipo_transacao = input(
        "\nDigite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    transacoes = filtrar_transacoes_tipo_service(
        usuario_id,
        conta_id,
        tipo_transacao
    )

    if not transacoes:
        print("\nNenhuma transacao encontrada!")
        return None

    print("\n╔══════════════════════════════════════════════╗")
    print("║         🔎 TRANSACOES FILTRADAS 🔎         ║")
    print("╚══════════════════════════════════════════════╝")

    for transacao in transacoes:

        id_transacao = transacao[0]

        tipo = transacao[1]

        valor = float(transacao[2])

        descricao = transacao[3]

        categoria = transacao[4]

        data = transacao[5].strftime(
            "%d/%m/%Y"
        )

        emoji_tipo = (
            "📈"
            if tipo == "entrada"
            else "📉"
        )

        print(
            f"""
    ╔══════════════════════════════════════╗
    ║ 🆔 ID: {id_transacao:<29}
    ║ {emoji_tipo} Tipo: {tipo:<25}
    ║ 💰 Valor: R$ {valor:<19.2f}
    ║ 📂 Categoria: {categoria:<18}
    ║ 📝 Descricao: {descricao:<17}
    ║ 📅 Data: {data:<24}
    ╚══════════════════════════════════════╝
    """
        )

def filtrar_transacoes_categoria(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None
    
    try:
        conta_id = int(
            input("\nDigite o ID da conta: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None
    
    ids_contas = [
        conta[0]
        for conta in contas
    ]

    if conta_id not in ids_contas:

        print(
            "\nConta nao encontrada "
            "ou nao pertence ao usuario!"
        )

        return None
    
    categorias = listar_categorias()

    if not categorias:
        return None

    try:
        categoria_id = int(
            input("\nDigite o ID da categoria: ")
        )

    except ValueError:
        print("\nCategoria invalida!")
        return None

    ids_categorias = [
        categoria[0]
        for categoria in categorias
    ]

    if categoria_id not in ids_categorias:

        print("\nCategoria invalida!")
        return None

    transacoes = (
        filtrar_transacao_categoria_service(
            usuario_id,
            conta_id,
            categoria_id
        )
    )

    if not transacoes:

        print("\nNenhuma transacao encontrada!")
        return None

    print("\n╔══════════════════════════════════════════════╗")
    print("║         🔎 TRANSACOES FILTRADAS 🔎         ║")
    print("╚══════════════════════════════════════════════╝")

    for transacao in transacoes:

        id_transacao = transacao[0]

        tipo = transacao[1]

        valor = float(transacao[2])

        descricao = transacao[3]

        categoria = transacao[4]

        data = transacao[5].strftime(
            "%d/%m/%Y"
        )

        emoji_tipo = (
            "📈"
            if tipo == "entrada"
            else "📉"
        )

        print(
            f"""
    ╔════════════════════════════════════╗
    ║ 🆔 ID: {id_transacao:<28}
    ║ {emoji_tipo} Tipo: {tipo:<24}
    ║ 💰 Valor: R$ {valor:<18.2f}
    ║ 📂 Categoria: {categoria:<18}
    ║ 📝 Descricao: {descricao:<17}
    ║ 📅 Data: {data:<23}
    ╚════════════════════════════════════╝
    """
        )

def filtrar_transacoes_descricao(usuario_id):

    contas = listar_contas(usuario_id)

    if not contas:
        return None

    try:
        conta_id = int(
            input("\nDigite o ID da conta: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None

    ids_contas = [
        conta[0]
        for conta in contas
    ]

    if conta_id not in ids_contas:

        print(
            "\nConta nao encontrada "
            "ou nao pertence ao usuario!"
        )

        return None

    descricao = input(
        "\nDigite a descricao para buscar: "
    ).strip().lower()

    transacoes = (
        filtrar_transacoes_descricao_service(
            usuario_id,
            conta_id,
            descricao
        )
    )

    if not transacoes:

        print("\nNenhuma transacao encontrada!")
        return None

    print("\n╔══════════════════════════════════════════════╗")
    print("║         🔎 TRANSACOES FILTRADAS 🔎         ║")
    print("╚══════════════════════════════════════════════╝")

    for transacao in transacoes:

        id_transacao = transacao[0]

        tipo = transacao[1]

        valor = float(transacao[2])

        descricao = transacao[3]

        categoria = transacao[4]

        data = transacao[5].strftime(
            "%d/%m/%Y"
        )

        emoji_tipo = (
            "📈"
            if tipo == "entrada"
            else "📉"
        )

        print(
            f"""
    ╔════════════════════════════════════╗
    ║ 🆔 ID: {id_transacao:<28}
    ║ {emoji_tipo} Tipo: {tipo:<24}
    ║ 💰 Valor: R$ {valor:<18.2f}
    ║ 📂 Categoria: {categoria:<18}
    ║ 📝 Descricao: {descricao:<17}
    ║ 📅 Data: {data:<23}
    ╚════════════════════════════════════╝
    """
        )

def mostrar_dashboard(usuario_id):

    saldo_total = buscar_saldo_total_service(
        usuario_id
    )

    total_entradas = buscar_total_entradas_service(
        usuario_id
    )

    total_saidas = buscar_total_saidas_service(
        usuario_id
    )

    gastos_categoria = buscar_gastos_categoria_service(
        usuario_id
    )

    maior_categoria = buscar_maior_categoria_service(
        usuario_id
    )

    quantidade_transacoes = buscar_quantidade_transacoes_service(
        usuario_id
    )

    print("\n╔══════════════════════════════════════════════╗")
    print("║            📊 DASHBOARD 📊                 ║")
    print("╚══════════════════════════════════════════════╝")

    print(f"\n💰 Saldo Total : R$ {saldo_total:.2f}")

    print(f"📈 Entradas    : R$ {total_entradas:.2f}")

    print(f"📉 Saidas      : R$ {total_saidas:.2f}")

    print(
        f"🧾 Transacoes : "
        f"{quantidade_transacoes}"
    )

    if maior_categoria:

        nome_categoria = maior_categoria[0]

        total_categoria = float(maior_categoria[1])

        print(
            f"\n🏆 Maior gasto: "
            f"{nome_categoria} "
            f"- R$ {total_categoria:.2f}"
        )

    print("\n════════ GASTOS POR CATEGORIA ════════")

    if not gastos_categoria:
        print("\n⚠️  Nenhum gasto encontrado!")

    else:

        for categoria in gastos_categoria:

            nome_categoria = categoria[0]

            total_gasto = float(categoria[1])

            porcentagem = (
                total_gasto / total_saidas
            ) * 100

            barra = "█" * int(
                porcentagem / 5
            )

            print(
                f"\n📌 {nome_categoria:<15} | "
                f"{barra:<20} "
                f"{porcentagem:.1f}% | "
                f"R$ {total_gasto:.2f}"
            )

    print("\n══════════════════════════════════════════════")

# =====================================
# MENUS
# =====================================

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
    print("3 - Dashboard")
    print("4 - Logout")
    print("5 - Sair")

    return input('\nEscolha: ')

def menu_contas():

    print("\n===== GESTAO DE CONTAS =====")
    print("1 - Criar conta")
    print("2 - Listar contas")
    print("3 - Editar conta")
    print("4 - Excluir conta")
    print("5 - Voltar")

    return input('\nEscolha: ')

def menu_transacoes():

    print("\n===== TRANSACOES =====")
    print("1 - Criar transacao")
    print("2 - Listar transacoes")
    print("3 - Excluir transacao")
    print("4 - Editar transacao")
    print("5 - Filtrar transacoes")
    print("6 - Voltar")

    return input("\nEscolha: ")

def menu_filtrar_transacoes():

    print("\n===== FILTRAR TRANSACOES =====")

    print("1 - Filtrar por tipo")
    print("2 - Filtrar por categoria")
    print("3 - Buscar por descricao")
    print("4 - Voltar")

    return input("\nEscolha: ")


def main():

    while True:

        if usuario_logado is None:

            opcao = menu_deslogado()

            if opcao == "1":
                tela_login()

            elif opcao == "2":
                tela_cadastro()

            elif opcao == "3":

                print('\nSaindo do sistema...')
                break

            else:
                print('\nOpcao invalida!')

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

                else:
                    print("\nOpcao invalida!")

            elif opcao == "2":

                opcao_transacoes = menu_transacoes()

                if opcao_transacoes == "1":
                    criar_transacao(usuario_logado[0])

                elif opcao_transacoes == "2":
                    listar_transacoes(usuario_logado[0])

                elif opcao_transacoes == "3":
                    excluir_transacao(usuario_logado[0])

                elif opcao_transacoes == "4":
                    editar_transacao(usuario_logado[0])

                elif opcao_transacoes == "5":
                    opcao_filtro = menu_filtrar_transacoes()

                    if opcao_filtro == "1":
                        filtrar_transacoes_tipo(
                            usuario_logado[0]
                        )

                    elif opcao_filtro == "2":
                        filtrar_transacoes_categoria(
                            usuario_logado[0]
                        )

                    elif opcao_filtro == "3":
                        filtrar_transacoes_descricao(
                            usuario_logado[0]
                        )

                    elif opcao_filtro == "4":
                        continue

                    else:
                        print("\nOpcao invalida!")

                elif opcao_transacoes == "6":
                    continue
                else:
                    print("\nOpcao invalida!")

            elif opcao == "3":
                mostrar_dashboard(usuario_logado[0])

            elif opcao == "4":
                logout()

            elif opcao == "5":

                print('\nSaindo do sistema...')
                break

            else:
                print('\nOpcao invalida!')


if __name__ == "__main__":
    main()