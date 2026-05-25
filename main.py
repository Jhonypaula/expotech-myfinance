import os

from services.auth_services import (
    cadastrar_usuario_service,
    login_usuario_service,
    buscar_usuario_por_email
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

from services.resetar_senha_service import(
    requisicao_alterar_senha,
    resetar_senha,
    validar_token_reset
)

from utils.regex_validators import (
    validar_senha
)

usuario_logado = None

def limpar_tela():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )

def tela_cadastro():

    global usuario_logado

    nome_usuario = input('\n👤 Digite seu nome: ')
    email_usuario = input('\n📧 Digite seu email: ')
    senha_usuario = input('\n🔒 Digite sua senha: ')

    cadastro = cadastrar_usuario_service(
        nome_usuario,
        email_usuario,
        senha_usuario
    )

    if cadastro:

        usuario_logado = cadastro

        print('\nCadastro realizado com sucesso!')
        pausar_tela()

        return usuario_logado

    else:
        print('\nErro ao cadastrar usuario!')
        pausar_tela()
        return None

def tela_login():

    global usuario_logado

    email_usuario = input('\n📧 Digite seu email: ')
    senha_usuario = input('\n🔒 Digite sua senha: ')

    usuario = login_usuario_service(
        email_usuario,
        senha_usuario
    )

    if usuario:

        usuario_logado = usuario

        print('\nLogin realizado com sucesso!')
        pausar_tela()

        return usuario

    else:
        print('\nErro ao fazer login!')
        pausar_tela()
        return None

def logout():

    global usuario_logado

    usuario_logado = None

    print('\nLogout realizado com sucesso!')
    pausar_tela()

def criar_conta(usuario_id):

    nome_conta = input('\n🏦 Digite o nome da conta: ')

    tipo_conta = input(
        '\n📁 Digite o tipo da conta (corrente, poupanca, carteira): '
    ).strip().lower()

    saldo_inicial_str = input(
        '\n💰 Digite o saldo inicial da conta: '
    )

    conta_criada = cadastrar_conta_service(
        usuario_id,
        nome_conta,
        tipo_conta,
        saldo_inicial_str
    )

    if conta_criada:

        print('\n✅ Conta criada com sucesso!')
        pausar_tela()
        return True

    else:
        print('\n⚠️ Erro ao criar conta!')
        pausar_tela()
        return None

def listar_contas(usuario_id, pausar=True):

    contas = listar_contas_service(usuario_id)

    if not contas:

        print('\n⚠️ Nenhuma conta encontrada!')
        return None

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║               💳️ SUAS CONTAS 💳️              ║")
    print("╚══════════════════════════════════════════════╝")

    for conta in contas:

        id_conta = conta[0]
        nome_conta = conta[1]
        tipo_conta = conta[2]
        saldo_conta = conta[3]
        
        emoji_tipo = {
            "corrente" : "🏦️",
            "poupanca" : "💰️",
            "carteira" : "👝️"
        }.get(tipo_conta, "💳️")

        
        print(f"╔══════════════════════════════════════════════╗")
        print(f"║ 🆔️ ID: {id_conta}")
        print(f"║ {emoji_tipo} Conta: {nome_conta}")
        print(f"║ 📁️ Tipo: {tipo_conta}")
        print(f"║ 💵️ Saldo: R$ {saldo_conta:.2f}")
        print(f"╚══════════════════════════════════════════════╝")
    if pausar:    
        pausar_tela()

    return contas

def editar_conta(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        id_conta = int(input("\n🆔 Digite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    novo_nome = input("\n🏦 Digite o novo nome da conta: ")

    novo_tipo = input(
        "\n📁 Digite o novo tipo da conta (corrente, poupanca, carteira): "
    ).strip().lower()

    conta_editada = editar_conta_service(
        usuario_id,
        id_conta,
        novo_nome,
        novo_tipo
    )

    if conta_editada:
        print("\n✅ Conta editada com sucesso!")
        pausar_tela()
        return True

    else:
        print("\n⚠️ Erro ao editar conta.")
        pausar_tela()
        return None

def excluir_conta(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        id_conta = int(
            input("\n🆔 Digite o ID da conta que deseja excluir: ")
        )

    except ValueError:
        print("\n❌ ID invalido!")
        return None

    confirmacao = input(
        "\n⚠️ Tem certeza que deseja excluir esta conta? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\n❌ Exclusao cancelada.")
        pausar_tela()
        return None

    conta_excluida = excluir_conta_service(
        usuario_id,
        id_conta
    )

    if conta_excluida:

        print("\n✅ Conta excluida com sucesso!")
        pausar_tela()
        return True

    else:
        print("\n⚠️ Erro ao excluir conta.")
        pausar_tela()
        return None

def listar_categorias():
 
    categorias = listar_categorias_service()
 
    if not categorias:
 
        print("\n⚠️ Nenhuma categoria encontrada!")
        return None

    limpar_tela()
    print("\n╔════════════════════════════════════════════════╗")
    print("║            🏷️  CATEGORIAS  🏷️                    ║")
    print("╠═══════╦═══════════════════╦════════════════════╣")
    print("║  ID   ║  Nome             ║  Descricao         ║")
    print("╠═══════╬═══════════════════╬════════════════════╣")
    

    for categoria in categorias:
 
        id_categoria = categoria[0]
        nome_categoria = categoria[1]
        descricao_categoria = categoria[2]
 
        print(
            f"║ {id_categoria:<5} ║"
            f" {nome_categoria:<17} ║"
            f" {descricao_categoria:<18} ║"
        )
 
    print("╚═══════╩═══════════════════╩════════════════════╝")
 
    return categorias

def criar_transacao(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        conta_id = int(input("\n🆔 Digite o ID da conta: "))

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
            input("\n🏷️ Digite o ID da categoria: ")
        )

    except ValueError:
        print("\nCategoria invalida!")
        return None
    
    ids_categorias = [
        categoria[0]
        for categoria in categorias
    ]
    if categoria_id not in ids_categorias:
        print(
            "\nCategoria nao encontrada!"
        )
        
        return None

    tipo_transacao = input(
        "\n🔄 Digite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    valor_transacao = input(
        "\n💰 Digite o valor da transacao: "
    )

    descricao_transacao = input(
        "\n📝 Digite a descricao da transacao: "
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

        pausar_tela()
        return True

    else:
        print("\nErro ao criar transacao.")

        pausar_tela()
        return None

def listar_transacoes(
    usuario_id,
    conta_id=None,
    pausar=True
):
    if conta_id is None:

        contas = listar_contas(usuario_id, pausar=False)

        if not contas:
            return None

        try:
            conta_id = int(input("\n🆔 Digite o ID da conta: "))

        except ValueError:
            print("\n❌️ ID invalido!")
            return None

    transacoes = listar_transacao_service(
        usuario_id,
        conta_id
    )

    if not transacoes:

        print("\n⚠️ Nenhuma transacao encontrada!")
        return None

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║               💸️ TRANSACOES 💸️                ║")
    print("╚══════════════════════════════════════════════╝")

    for transacao in transacoes:

        id_transacao = transacao[0]
        tipo_transacao = transacao[1]
        valor_transacao = transacao[2]
        descricao_transacao = transacao[3]
        categoria_transacao = transacao[4]

        data = transacao[5].strftime("%d/%m/%Y")
        
        emoji_tipo = (
            "📈️"
            if tipo_transacao == "entrada"
            else "📉️"
        )

        print(f"╔══════════════════════════════════════════════╗")
        print(f"║ 🆔️ ID: {id_transacao}")
        print(f"║ {emoji_tipo} Tipo: {tipo_transacao}")
        print(f"║ 💰️ Valor: R$ {valor_transacao:.2f}")
        print(f"║ 📁️ Categoria: {categoria_transacao}")
        print(f"║ 📝️ Descricao: {descricao_transacao}")
        print(f"║ 🗓️ Data: {data}")
        print(f"╚══════════════════════════════════════════════╝")
    if pausar:    
        pausar_tela()

    return transacoes

def excluir_transacao(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        conta_id = int(input("\n🆔 Digite o ID da conta: "))

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

    transacoes = listar_transacoes(
        usuario_id,
        conta_id,
        pausar=False
    )

    if not transacoes:
        return None

    try:
        id_transacao = int(
            input("\n🆔 Digite o ID da transacao: ")
        )

    except ValueError:
        print("\nID invalido!")
        return None

    confirmacao = input(
        "\n⚠️ Tem certeza que deseja excluir esta transacao? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nExclusao cancelada.")
        pausar_tela()
        return None

    transacao_excluida = excluir_transacao_service(
        usuario_id,
        conta_id,
        id_transacao
    )

    if transacao_excluida:

        print("\nTransacao excluida com sucesso!")

        pausar_tela()
        return True

    else:
        print("\nErro ao excluir transacao.")

        pausar_tela()
        return None

def editar_transacao(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        conta_id = int(input("\n🆔 Digite o ID da conta: "))

    except ValueError:
        print("\nID invalido!")
        return None

    transacoes = listar_transacoes(
        usuario_id,
        conta_id,
        pausar=False
    )

    if not transacoes:
        return None

    try:
        id_transacao = int(
            input("\n🆔 Digite o ID da transacao: ")
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
            input("\n🏷️ Digite o ID da categoria: ")
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
        "\n🔄 Digite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    valor_transacao_str = input(
        "\n💰 Digite o valor da transacao: "
    )

    descricao_transacao = input(
        "\n📝 Digite a descricao da transacao: "
    )

    confirmacao = input(
        "\n⚠️ Tem certeza que deseja editar esta transacao? (s/n): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nEdicao cancelada.")
        pausar_tela()
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
        pausar_tela()

        return True

    else:
        print("\nErro ao editar transacao.")
        pausar_tela()

        return None

def filtrar_transacoes_tipo(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        conta_id = int(
            input("\n🆔 Digite o ID da conta: ")
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
        "\n🔄 Digite o tipo de transacao (entrada/saida): "
    ).strip().lower()

    transacoes = filtrar_transacoes_tipo_service(
        usuario_id,
        conta_id,
        tipo_transacao
    )

    if not transacoes:
        print("\nNenhuma transacao encontrada!")
        return None

    limpar_tela()
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

        print(f"╔══════════════════════════════════════╗")
        print(f"║ 🆔 ID: {id_transacao}")
        print(f"║ {emoji_tipo} Tipo: {tipo}")
        print(f"║ 💰 Valor: R$ {valor:.2f}")
        print(f"║ 📂 Categoria: {categoria}")
        print(f"║ 📝 Descricao: {descricao}")
        print(f"║ 📅 Data: {data}")
        print(f"╚══════════════════════════════════════╝")
        
    pausar_tela()

def filtrar_transacoes_categoria(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None
    
    try:
        conta_id = int(
            input("\n🆔 Digite o ID da conta: ")
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
            input("\n🏷️ Digite o ID da categoria: ")
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

    limpar_tela()
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

        print(f"╔════════════════════════════════════╗")
        print(f"║ 🆔 ID: {id_transacao}")
        print(f"║ {emoji_tipo} Tipo: {tipo}")
        print(f"║ 💰 Valor: R$ {valor:.2f}")
        print(f"║ 📂 Categoria: {categoria}")
        print(f"║ 📝 Descricao: {descricao}")
        print(f"║ 📅 Data: {data}")
        print(f"╚════════════════════════════════════╝")
        
    pausar_tela()

def filtrar_transacoes_descricao(usuario_id):

    contas = listar_contas(usuario_id, pausar=False)

    if not contas:
        return None

    try:
        conta_id = int(
            input("\n🆔 Digite o ID da conta: ")
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
        "\n🔍 Digite a descricao para buscar: "
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

    limpar_tela()
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

        print(f"╔════════════════════════════════════╗")
        print(f"║ 🆔 ID: {id_transacao}")
        print(f"║ {emoji_tipo} Tipo: {tipo}")
        print(f"║ 💰 Valor: R$ {valor:.2f}")
        print(f"║ 📂 Categoria: {categoria}")
        print(f"║ 📝 Descricao: {descricao}")
        print(f"║ 📅 Data: {data}")
        print(f"╚════════════════════════════════════╝")
        
    pausar_tela()

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

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║            📊 DASHBOARD 📊                   ║")
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

            if total_saidas > 0:
                porcentagem = (
                    total_gasto / total_saidas
                ) * 100
            else:
                porcentagem = 0

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
    
    pausar_tela()

def tela_esqueci_senha():
    
    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║            🔐️ RECUPERAR SENHA 🔐️             ║")
    print("╚══════════════════════════════════════════════╝")
    
    email = input(
        "\n📧 Digite seu email: "
    ).strip().lower()
    
    usuario = buscar_usuario_por_email(
        email
    )
    
    requisicao_alterar_senha(
        email
    )
    
    print(
        "\n📩️ Se o email existir, um token foi enviado."
    )
    
    if usuario:
        
        redefinir = input(
            "\n🔑 Deseja redefinir a senha agora? (s/n): "
        ).strip().lower()
    
        if redefinir == "s":
            
            tela_resetar_senha()
            
        else:
            print(
                "\n📌️ Voce pode redefinir a senha depois pelo menu."
            )
        
    else:
        print(
            "\n❌️ Erro ao solicitar recuperacao de senha!"
        )

def tela_resetar_senha():
    
    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║            ♻️ RESETAR SENHA ♻️               ║")
    print("╚══════════════════════════════════════════════╝")
    
    while True:
    
        token = input(
            "\n🔑 Digite o token recebido (ou 0 para cancelar): "
        ).strip()
        
        if token == "0":
            
            print(
                "\n📌️ Redefinicao cancelada."
            )
            
            return None
        
        token_valido = validar_token_reset(
            token
        )
        
        if not token_valido:
            print(
                "\n❌️ Token invalido ou expirado!"
            )
        else:
            print(
                "\n✅️ Token valido!"
            )
            break
        
    while True:
        
        nova_senha = input(
            "\n🔒 Digite a nova senha (ou 0 para cancelar): "
        )
        if nova_senha == "0":
            
            print(
                "\n📌️ Redefinicao cancelada."
            )

            return None
        
        if not validar_senha(nova_senha):
            
            print(
                "\n❌️ Senha fraca!"
                "\nA senha deve conter:"
                "\n- minimo 8 caracteres"
                "\n- letra maiuscula"
                "\n- letra minuscula"
                "\n- numero"
                "\n- caractere especial"
            )
            
            continue
        
        resultado = resetar_senha(
            token, 
            nova_senha
        )
        
        if resultado:
            print(
                "\n✅️ Senha alterada com sucesso!"
            )
            
            break
        
        else:
            print(
                "\n❌️ Erro ao resetar a senha!"
            )

def pausar_tela():
    
    input(
        "\n📌️ Pressione ENTER para voltar ao menu . . ."
    )
    
# =====================================
# MENUS
# =====================================

def menu_deslogado():

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║               💰 MY FINANCE 💰               ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  1 ➜ Login                                   ║")
    print("║  2 ➜ Cadastrar                               ║")
    print("║  3 ➜ Esqueci minha senha                     ║")
    print("║  4 ➜ Sair                                    ║")
    print("╚══════════════════════════════════════════════╝")

    return input("\n👉 Escolha uma opcao: ")

def menu_logado():

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print(f"║ 👋️ Bem-Vindo, {usuario_logado[1]:<22}         ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  1 ➜ Contas                                  ║")
    print("║  2 ➜ Transacoes                              ║")
    print("║  3 ➜ Dashboard                               ║")
    print("║  4 ➜ Logout                                  ║")
    print("║  5 ➜ Sair                                    ║")
    print("╚══════════════════════════════════════════════╝")

    return input("\n👉 Escolha uma opcao: ")

def menu_contas():

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║            💳️ GESTAO DE CONTAS 💳️            ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  1 ➜ Criar conta                             ║")
    print("║  2 ➜ Listar contas                           ║")
    print("║  3 ➜ Editar conta                            ║")
    print("║  4 ➜ Excluir conta                           ║")
    print("║  5 ➜ Voltar                                  ║")
    print("╚══════════════════════════════════════════════╝")

    return input("\n👉 Escolha uma opcao: ")

def menu_transacoes():

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║               💸️  TRANSACOES 💸️              ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  1 ➜ Criar transacao                         ║")
    print("║  2 ➜ Listar transacao                        ║")
    print("║  3 ➜ Excluir transacao                       ║")
    print("║  4 ➜ Editar transacao                        ║")
    print("║  5 ➜ Filtrar transacoes                      ║")
    print("║  6 ➜ Voltar                                  ║")
    print("╚══════════════════════════════════════════════╝")

    return input("\n👉 Escolha uma opcao: ")

def menu_filtrar_transacoes():

    limpar_tela()
    print("\n╔══════════════════════════════════════════════╗")
    print("║          🔎️ FILTRAR TRANSACOES 🔎️            ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  1 ➜ Filtrar por tipo                        ║")
    print("║  2 ➜ Filtrar por categoria                   ║")
    print("║  3 ➜ Buscar por descricao                    ║")
    print("║  4 ➜ Voltar                                  ║")
    print("╚══════════════════════════════════════════════╝")

    return input("\n👉 Escolha uma opcao: ")


def main():

    while True:

        if usuario_logado is None:

            opcao = menu_deslogado()

            if opcao == "1":
                tela_login()

            elif opcao == "2":
                tela_cadastro()

            elif opcao == "3":
                tela_esqueci_senha()
            
            elif opcao == '4':
                limpar_tela()
                print("\nSaindo do sistema . . .")
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

                limpar_tela()
                print('\nSaindo do sistema...')
                break

            else:
                print('\nOpcao invalida!')


if __name__ == "__main__":
    main()