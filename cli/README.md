CLI

<div align="center">

# 💻 MyFinance — CLI

**Interface de linha de comando interativa para controle financeiro pessoal.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Terminal](https://img.shields.io/badge/Interface-Terminal-2d2d2d?style=flat-square&logo=gnometerminal&logoColor=white)]()

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Como Executar](#-como-executar)
- [Estrutura de Menus](#-estrutura-de-menus)
- [Fluxo de Uso](#-fluxo-de-uso)
- [Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
- [Integração com o Backend](#-integração-com-o-backend)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Dependências](#-dependências)

---

## 🔍 Visão Geral

O módulo `cli/` oferece uma interface de linha de comando totalmente interativa para o MyFinance. O usuário navega por menus numerados no terminal, digitando o número da opção desejada.

A CLI é executada com um único arquivo `main.py` e **reutiliza integralmente o backend** — não há duplicação de lógica. O bootstrap inicial adiciona `../backend` ao `sys.path` em tempo de execução, permitindo importar diretamente os `services/` e `repository/` do backend.

```
cli/
├── main.py           ← Toda a interface: menus, entradas, exibição
└── requirements.txt
```

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.10+
- MySQL rodando com o banco `my_finance` criado (veja `backend/core/schema.sql`)
- Arquivo `backend/.env` configurado

### Instalação e execução

```bash
# Na raiz do projeto
cd cli
pip install -r requirements.txt
python main.py
```

> ℹ️ A CLI localiza o `backend/` automaticamente com base no caminho do próprio `main.py`. Não é necessário instalar o backend como pacote.

---

## 🗺️ Estrutura de Menus

A navegação é feita por menus aninhados com bordas ASCII:

```
╔══════════════════════════════╗
║        💰 MY FINANCE 💰      ║
╠══════════════════════════════╣
║  1 ➜ Login                  ║   ← Menu Deslogado
║  2 ➜ Cadastrar              ║
║  3 ➜ Esqueci minha senha    ║
║  4 ➜ Sair                   ║
╚══════════════════════════════╝
          │ após login
          ▼
╔══════════════════════════════╗
║  👋 Bem-Vindo, [Nome]        ║   ← Menu Principal (Logado)
╠══════════════════════════════╣
║  1 ➜ Contas                 ║
║  2 ➜ Transacoes             ║
║  3 ➜ Dashboard              ║
║  4 ➜ Desativar Conta        ║
║  5 ➜ Logout                 ║
║  6 ➜ Sair                   ║
╚══════════════════════════════╝
    │            │
    ▼            ▼
 Contas      Transacoes
 ┌──────┐    ┌──────────────┐
 │ 1 Criar   │ 1 Criar      │
 │ 2 Listar  │ 2 Listar     │
 │ 3 Editar  │ 3 Excluir    │
 │ 4 Excluir │ 4 Editar     │
 │ 5 Voltar  │ 5 Filtrar ──► Filtros
 └──────┘    │ 6 Voltar     │
             └──────────────┘
```

---

## 🔄 Fluxo de Uso

### Fluxo principal do usuário

```
Iniciar sistema
      │
      ▼
┌─────────────┐   sem conta    ┌──────────────────┐
│ Menu inicial│ ─────────────► │ Cadastrar usuário │
│ (deslogado) │                │  nome/email/senha │
└──────┬──────┘                └────────┬─────────┘
       │ login                          │
       ▼                                ▼
┌─────────────┐                ┌──────────────────┐
│ Autenticação│                │  Login automático │
│ email+senha │                │  após cadastro   │
└──────┬──────┘                └────────┬─────────┘
       │                                │
       └───────────────┬────────────────┘
                       ▼
              ┌─────────────────┐
              │  Menu Principal  │
              │  (logado)       │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Contas    Transações    Dashboard
```

### Fluxo de recuperação de senha

```
Menu Deslogado → "3. Esqueci minha senha"
      │
      ▼
Digitar e-mail cadastrado
      │
      ▼
Sistema envia e-mail com token (válido 15 min)
      │
      ▼
Menu Deslogado → "3. Esqueci minha senha" novamente
      │ (o sistema detecta que já tem token pendente
      │  e oferece a opção de inserir o token)
      ▼
Inserir token recebido por e-mail
      │
      ▼
Digitar e confirmar nova senha (deve ser senha forte)
      │
      ▼
Senha atualizada ✅
```

---

## 📦 Funcionalidades Detalhadas

### 🔐 Autenticação

| Opção | Ação | Validações |
|-------|------|-----------|
| Login | Autentica com e-mail + senha | Campos obrigatórios; conta ativa |
| Cadastro | Cria novo usuário | E-mail único; senha forte; regex de e-mail |
| Esqueci senha | Envia token por e-mail | E-mail deve estar cadastrado |
| Resetar senha | Usa token para nova senha | Token válido e não expirado; senha forte |
| Desativar conta | Soft delete do usuário | Confirmação obrigatória |
| Logout | Encerra sessão | — |

### 🏦 Contas (`menu_contas`)

| Opção | Ação | Entrada do usuário |
|-------|------|-------------------|
| 1 - Criar | Cria nova conta com saldo inicial | Nome, tipo (corrente/poupanca/carteira), saldo |
| 2 - Listar | Exibe todas as contas com saldo atual | — |
| 3 - Editar | Altera nome e tipo da conta | ID da conta, novo nome, novo tipo |
| 4 - Excluir | Remove conta (com confirmação) | ID da conta, confirmação `s/n` |

**Exibição das contas no terminal:**
```
╔═══════════════════════════════════════╗
║ 🆔 ID: 1
║ 🏦 Conta: Nubank
║ 📁 Tipo: corrente
║ 💵 Saldo: R$ 1.250,00
╚═══════════════════════════════════════╝
```

### 💸 Transações (`menu_transacoes`)

| Opção | Ação | Detalhes |
|-------|------|---------|
| 1 - Criar | Registra entrada ou saída | ID da conta, ID da categoria, tipo, valor, descrição |
| 2 - Listar | Exibe transações de uma conta | Ordenadas por data desc; mostra categoria |
| 3 - Excluir | Remove transação e reverte saldo | ID da conta → ID da transação |
| 4 - Editar | Atualiza transação e recalcula saldo | Seleciona campos a alterar |
| 5 - Filtrar | Submenu de filtros | Ver abaixo |

### 🔎 Filtros de Transações (`menu_filtrar_transacoes`)

| Opção | Filtro | Entrada |
|-------|--------|---------|
| 1 | Por tipo | `entrada` ou `saida` |
| 2 | Por categoria | ID da categoria (exibe lista primeiro) |
| 3 | Por descrição | Texto para busca parcial |

### 📊 Dashboard

O dashboard exibe um resumo completo das finanças do usuário:

```
╔══════════════════════════════════════════════╗
║              📊 DASHBOARD 📊                 ║
╚══════════════════════════════════════════════╝

💰 Saldo Total:        R$ 3.450,00
📈 Total Entradas:     R$ 5.200,00
📉 Total Saídas:       R$ 1.750,00
🔢 Qtd. Transações:    42

════════ GASTOS POR CATEGORIA ════════
  🍔 Alimentacao:   R$  480,00  ████████
  🚗 Transporte:    R$  320,00  █████
  🏠 Moradia:       R$  800,00  █████████████
  ...

🏆 Maior categoria de gasto: Moradia
══════════════════════════════════════════════
```

---

## 🔗 Integração com o Backend

A CLI não possui lógica de negócio própria — ela apenas:

1. Coleta input do usuário
2. Chama os `services/` do backend
3. Formata e exibe o resultado

```python
# Exemplo: fluxo de criação de transação na CLI
def criar_transacao(usuario_id):
    # 1. Coleta inputs
    conta_id = int(input('ID da conta: '))
    categoria_id = int(input('ID da categoria: '))
    tipo = input('Tipo (entrada/saida): ')
    valor = input('Valor: ')
    descricao = input('Descrição: ')

    # 2. Chama o service (toda validação e lógica está lá)
    resultado = criar_transacao_service(
        usuario_id, conta_id, categoria_id,
        tipo, valor, descricao
    )

    # 3. Exibe resultado
    if resultado:
        print('✅ Transação criada com sucesso!')
    else:
        print('⚠️ Erro ao criar transação.')
```

### Bootstrap do sys.path

O `main.py` resolve o caminho do backend automaticamente:

```python
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "backend"
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

# A partir daqui, imports do backend funcionam normalmente:
from services.auth_services import login_usuario_service
from services.conta_services import cadastrar_conta_service
```

---

## 📋 Exemplos de Uso

### Criar uma conta

```
👉 Escolha uma opcao: 1         ← Menu principal → Contas

👉 Escolha uma opcao: 1         ← Menu contas → Criar conta

🏦 Digite o nome da conta: Nubank
📁 Digite o tipo da conta (corrente, poupanca, carteira): corrente
💰 Digite o saldo inicial da conta: 1500.00

✅ Conta criada com sucesso!
```

### Registrar uma transação

```
👉 Escolha uma opcao: 2         ← Menu principal → Transacoes

👉 Escolha uma opcao: 1         ← Menu transações → Criar transacao

[exibe lista de contas]
🆔 ID da conta: 1

[exibe lista de categorias]
🏷️ ID da categoria: 1

📊 Tipo (entrada/saida): saida
💵 Valor: 45.90
📝 Descricao: Almoço

✅ Transação registrada! Novo saldo: R$ 1.454,10
```

### Filtrar por tipo

```
👉 Escolha uma opcao: 2         ← Transacoes
👉 Escolha uma opcao: 5         ← Filtrar
👉 Escolha uma opcao: 1         ← Por tipo

📊 Tipo (entrada/saida): entrada

[exibe somente as entradas da conta]
```

---

## 📦 Dependências

```txt
# cli/requirements.txt
python-dotenv
mysql-connector-python
```

> As dependências são as mesmas do backend, pois a CLI importa o backend diretamente.

```bash
pip install -r requirements.txt
```

---

<div align="center">

← [Backend](../backend/README.md) | [Frontend →](../frontend/README.md)

</div>