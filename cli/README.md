<div align="center">

# 💰 My Finance

**Sistema de gerenciamento financeiro pessoal via linha de comando (CLI)**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Objetivo](#-objetivo)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura e Estrutura de Pastas](#-arquitetura-e-estrutura-de-pastas)
- [Como Instalar](#-como-instalar)
- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Configuração do Banco de Dados](#-configuração-do-banco-de-dados)
- [Como Rodar o Projeto](#-como-rodar-o-projeto)
- [Fluxo do Sistema](#-fluxo-do-sistema)
- [Interface CLI](#-interface-cli)
- [Regras de Negócio](#-regras-de-negócio)
- [Segurança Implementada](#-segurança-implementada)
- [Soft Delete](#-soft-delete)
- [Dashboard](#-dashboard)
- [Filtros de Transações](#-filtros-de-transações)
- [Recuperação de Senha](#-recuperação-de-senha)
- [Banco de Dados](#-banco-de-dados)
- [Melhorias Futuras](#-melhorias-futuras)
- [Autor](#-autor)
- [Licença](#-licença)

---

## 📌 Sobre o Projeto

**My Finance** é um sistema de controle financeiro pessoal desenvolvido em Python com interface de linha de comando (CLI). O sistema permite que usuários gerenciem suas contas bancárias, registrem transações financeiras (entradas e saídas), visualizem um dashboard com resumo financeiro e filtrem transações por diferentes critérios.

O projeto foi construído seguindo uma **arquitetura em camadas** (Layered Architecture), separando claramente as responsabilidades entre apresentação, lógica de negócio e acesso a dados, o que o torna um excelente exemplo de boas práticas para um projeto de portfólio.

---

## 🎯 Objetivo

Oferecer uma ferramenta simples e funcional para controle financeiro pessoal, permitindo ao usuário:

- Cadastrar e gerenciar múltiplas contas (corrente, poupança, carteira)
- Registrar entradas e saídas com atualização automática de saldo
- Categorizar transações e analisar gastos por categoria
- Visualizar um dashboard financeiro com indicadores gerais
- Recuperar senha via e-mail com token seguro e com prazo de expiração

---

## ✨ Funcionalidades Principais

| Módulo | Funcionalidade |
|---|---|
| 🔐 Autenticação | Cadastro, login e logout de usuários |
| 💳 Contas | CRUD completo de contas financeiras |
| 💸 Transações | CRUD de transações com atualização automática de saldo |
| 🔎 Filtros | Filtrar transações por tipo, categoria ou descrição |
| 📊 Dashboard | Resumo financeiro com saldo, entradas, saídas e gastos por categoria |
| 📧 Reset de Senha | Recuperação de senha via e-mail com token temporário |
| 🗑️ Soft Delete | Desativação de contas de usuário sem exclusão física |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3.8+** | Linguagem principal do projeto |
| **MySQL 8.0+** | Banco de dados relacional |
| **mysql-connector-python** | Driver de conexão com o MySQL |
| **python-dotenv** | Gerenciamento de variáveis de ambiente via `.env` |
| **hashlib** | Hash SHA-256 para criptografia de senhas |
| **secrets** | Geração segura de tokens de redefinição de senha |
| **smtplib** | Envio de e-mails transacionais via SMTP |
| **re (Regex)** | Validação de formato de e-mail e força de senha |

---

## 🏗️ Arquitetura e Estrutura de Pastas

O projeto adota uma **arquitetura em 3 camadas** (Three-Layer Architecture), promovendo separação de responsabilidades, facilidade de manutenção e baixo acoplamento:

```
expotech-myfinance/
│
├── main.py                         # 🖥️  Camada de Apresentação (UI/CLI)
│
├── core/
│   ├── config.py                   # ⚙️  Configurações gerais (SMTP, env vars)
│   ├── connection.py               # 🔌 Conexão com o banco de dados
│   └── schema.sql                  # 🗄️  Schema do banco de dados
│
├── services/                       # 🧠 Camada de Serviço (Lógica de Negócio)
│   ├── auth_services.py
│   ├── conta_services.py
│   ├── transacao_services.py
│   ├── categoria_services.py
│   ├── dashboard_services.py
│   ├── email_service.py
│   └── resetar_senha_service.py
│
├── repository/                     # 🗃️  Camada de Repositório (Acesso a Dados)
│   ├── auth_repository.py
│   ├── conta_repository.py
│   ├── transacao_repository.py
│   ├── categoria_repository.py
│   ├── dashboard_repository.py
│   └── resetar_senha_repository.py
│
├── utils/                          # 🔧 Utilitários e Helpers
│   ├── security.py                 # Hash de senhas (SHA-256)
│   ├── regex_validators.py         # Validação de e-mail e senha
│   ├── token_generator.py          # Geração de tokens seguros
│   └── validators.py               # Validação de campos vazios
│
├── .env.example                    # 📄 Exemplo de variáveis de ambiente
├── requirements.txt                # 📦 Dependências do projeto
└── LICENSE                         # 📜 Licença MIT
```

### Responsabilidade de cada camada

**`main.py` — Apresentação (UI)**
Gerencia toda a interface com o usuário: menus, inputs, exibição de resultados e navegação entre telas. Não contém lógica de negócio.

**`services/` — Lógica de Negócio**
Valida os dados recebidos da camada de apresentação, aplica as regras de negócio (ex.: verificar saldo antes de uma saída, impedir exclusão de conta com transações) e orquestra chamadas aos repositórios.

**`repository/` — Acesso a Dados**
Exclusivamente responsável por executar queries SQL no banco de dados. Não valida dados nem toma decisões de negócio.

**`utils/` — Utilitários**
Funções auxiliares reutilizáveis: hash de senha, validação via regex, geração de tokens e validação de campos.

---

## 🚀 Como Instalar

### Pré-requisitos

- Python 3.8 ou superior
- MySQL 8.0 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Jhonypaula/expotech-myfinance.git
cd expotech-myfinance

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## ⚙️ Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```bash
cp .env.example .env
```

Preencha o arquivo `.env` com seus dados:

```env
# Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=my_finance

# Configurações de E-mail (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
```

> 💡 **Dica Gmail:** Para usar o Gmail como SMTP, gere uma **Senha de App** em: Conta Google → Segurança → Verificação em duas etapas → Senhas de app.

---

## 🗄️ Configuração do Banco de Dados

Com o MySQL em execução, execute o script de criação do banco:

```bash
mysql -u root -p < core/schema.sql
```

Isso irá:
- Criar o banco de dados `my_finance`
- Criar todas as tabelas necessárias
- Popular a tabela de categorias com 12 categorias padrão

### Categorias pré-cadastradas

| # | Categoria | Descrição |
|---|---|---|
| 1 | Alimentação | iFood e comida |
| 2 | Transporte | Uber e gasolina |
| 3 | Salário | Entradas salariais |
| 4 | Lazer | Cinema e streaming |
| 5 | Saúde | Farmácia |
| 6 | Educação | Cursos e faculdade |
| 7 | Moradia | Gastos com moradia |
| 8 | Investimentos | Aplicações financeiras |
| 9 | Compras | Compras em geral |
| 10 | Assinaturas | Netflix e HBO |
| 11 | Transferências | PIX e TED |
| 12 | Outros | Outras transações |

---

## ▶️ Como Rodar o Projeto

```bash
python main.py
```

---

## 🔄 Fluxo do Sistema

```
┌─────────────────────────────────────────────────┐
│                  INÍCIO                          │
│            Menu Deslogado                        │
│   [Login]  [Cadastrar]  [Esqueci Senha]  [Sair] │
└───────────────┬─────────────────────────────────┘
                │ Login com sucesso
                ▼
┌─────────────────────────────────────────────────┐
│              Menu Principal (Logado)             │
│        [Contas] [Transações] [Dashboard]         │
└───┬──────────────┬──────────────┬───────────────┘
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌──────────────┐  ┌──────────┐
│ CONTAS │  │  TRANSAÇÕES  │  │DASHBOARD │
│        │  │              │  │          │
│Criar   │  │Criar         │  │Saldo     │
│Listar  │  │Listar        │  │Entradas  │
│Editar  │  │Editar        │  │Saídas    │
│Excluir │  │Excluir       │  │Categorias│
└────────┘  │Filtrar ──────┤  └──────────┘
            │  por Tipo    │
            │  por Categ.  │
            │  por Descr.  │
            └──────────────┘
```

---

## 🖥️ Interface CLI

O sistema utiliza uma interface de linha de comando com menus visuais formatados com caracteres Unicode e emojis.

### Menu principal (deslogado)

```
╔══════════════════════════════════════════════╗
║               💰 MY FINANCE 💰               ║
╠══════════════════════════════════════════════╣
║  1 ➜ Login                                   ║
║  2 ➜ Cadastrar                               ║
║  3 ➜ Esqueci minha senha                     ║
║  4 ➜ Sair                                    ║
╚══════════════════════════════════════════════╝
```

### Menu principal (logado)

```
╔══════════════════════════════════════════════╗
║ 👋️ Bem-Vindo, João                           ║
╠══════════════════════════════════════════════╣
║  1 ➜ Contas                                  ║
║  2 ➜ Transacoes                              ║
║  3 ➜ Dashboard                               ║
║  4 ➜ Logout                                  ║
║  5 ➜ Sair                                    ║
╚══════════════════════════════════════════════╝
```

### Exemplo de exibição de conta

```
╔══════════════════════════════════════════════╗
║ 🆔️ ID: 1
║ 🏦️ Conta: Conta Principal
║ 📁️ Tipo: corrente
║ 💵️ Saldo: R$ 1.500,00
╚══════════════════════════════════════════════╝
```

### Exemplo do Dashboard

```
╔══════════════════════════════════════════════╗
║            📊 DASHBOARD 📊                   ║
╚══════════════════════════════════════════════╝

💰 Saldo Total : R$ 3.200,00
📈 Entradas    : R$ 5.000,00
📉 Saídas      : R$ 1.800,00
🧾 Transações  : 12

🏆 Maior gasto: Alimentação - R$ 650,00

════════ GASTOS POR CATEGORIA ════════

📌 Alimentação     | ████████████        60.0% | R$ 650,00
📌 Transporte      | ████                20.0% | R$ 350,00
📌 Lazer           | ██                  10.0% | R$ 200,00
```

---

## 📏 Regras de Negócio

### Usuários

- E-mail deve ser único no sistema
- Senha deve ter mínimo 8 caracteres, letra maiúscula, minúscula, número e caractere especial (`@$!%*?&`)
- Contas desativadas (soft delete) não podem fazer login nem redefinir senha

### Contas Financeiras

- Tipos válidos: `corrente`, `poupanca`, `carteira`
- Saldo inicial não pode ser negativo
- Saldo inicial máximo: R$ 99.999.999,99
- Nomes de conta devem ser únicos por usuário
- **Não é possível excluir uma conta que possua transações vinculadas**

### Transações

- Tipos válidos: `entrada` ou `saida`
- Valor deve ser positivo e maior que zero
- Descrição é obrigatória e limitada a **15 caracteres**
- **Saída é bloqueada se o saldo da conta for insuficiente**
- Ao criar uma transação, o saldo da conta é atualizado automaticamente
- Ao excluir uma transação, o saldo da conta é revertido automaticamente
- Ao editar uma transação, o sistema desfaz o efeito da transação antiga e aplica o efeito da nova

### Tokens de Redefinição de Senha

- Token expira em **15 minutos**
- Um token só pode ser usado **uma única vez** (marcado como `usado = TRUE` após uso)
- Ao solicitar um novo token, todos os tokens anteriores ativos do usuário são invalidados

---

## 🔒 Segurança Implementada

| Mecanismo | Descrição |
|---|---|
| **Hash SHA-256** | Senhas armazenadas como hash irreversível. A senha nunca é salva em texto puro. |
| **Parametrized Queries** | Todas as queries usam `%s` com valores separados, prevenindo **SQL Injection**. |
| **Validação de força de senha** | Regex que exige maiúscula, minúscula, número e caractere especial com mínimo de 8 caracteres. |
| **Validação de e-mail** | Regex que verifica o formato do endereço de e-mail antes de qualquer operação. |
| **Token seguro** | `secrets.token_urlsafe(32)` gera tokens criptograficamente seguros para reset de senha. |
| **Token com expiração** | Tokens de reset expiram em 15 minutos, reduzindo a janela de ataque. |
| **Token de uso único** | Token é invalidado imediatamente após ser utilizado. |
| **Verificação de pertencimento** | Operações em contas e transações verificam se o recurso pertence ao usuário logado, prevenindo acesso cruzado entre usuários. |
| **Verificação de conta ativa** | O login verifica o campo `ativo` antes de autenticar, bloqueando usuários desativados. |
| **Variáveis de ambiente** | Credenciais do banco e do SMTP são carregadas via `.env`, nunca expostas no código. |

---

## 🗑️ Soft Delete

O sistema implementa **soft delete** para usuários. Em vez de excluir o registro do banco de dados, o campo `ativo` da tabela `tbl_usuarios` é alterado para `FALSE`.

**Efeitos do soft delete:**
- O usuário **não consegue mais fazer login** (a camada de serviço verifica o campo `ativo` após autenticar credenciais)
- O usuário **não consegue redefinir a senha** (a query de `atualizar_senha_usuario` inclui `AND ativo = TRUE`)
- O histórico do usuário é **preservado** no banco para fins de auditoria

```sql
-- Desativar usuário (soft delete)
UPDATE tbl_usuarios SET ativo = FALSE WHERE id_usuarios = ?

-- Verificação no login
SELECT ativo FROM tbl_usuarios WHERE id_usuarios = ?

-- Reset de senha só funciona para contas ativas
UPDATE tbl_usuarios SET senha_usuarios = ? WHERE id_usuarios = ? AND ativo = TRUE
```

---

## 📊 Dashboard

O dashboard consolida dados de todas as contas do usuário logado e exibe:

| Indicador | Descrição |
|---|---|
| **Saldo Total** | Soma dos saldos de todas as contas do usuário |
| **Total de Entradas** | Soma de todas as transações do tipo `entrada` |
| **Total de Saídas** | Soma de todas as transações do tipo `saida` |
| **Quantidade de Transações** | Número total de transações em todas as contas |
| **Maior Categoria de Gasto** | Categoria com maior volume de saídas |
| **Gastos por Categoria** | Barra de progresso proporcional para cada categoria |

Os valores retornam `0` ou `[]` quando não há dados, evitando erros de exibição para usuários novos.

---

## 🔎 Filtros de Transações

O sistema oferece 3 tipos de filtro para transações de uma conta:

### 1. Filtrar por Tipo
Exibe apenas transações de entrada **ou** saída.

### 2. Filtrar por Categoria
Exibe transações de uma categoria específica (o usuário escolhe da lista de categorias disponíveis).

### 3. Buscar por Descrição
Busca transações cuja descrição contenha o termo digitado (pesquisa parcial com `LIKE %termo%`).

Todos os filtros validam:
- Se a conta existe e pertence ao usuário
- Se o tipo/categoria informado é válido
- Se a descrição não está vazia (para busca textual)

---

## 📧 Recuperação de Senha

O fluxo de recuperação de senha é composto por 3 etapas:

```
1. Usuário informa o e-mail
        ↓
2. Sistema verifica se o e-mail existe
        ↓ (existe)
3. Tokens anteriores são invalidados
        ↓
4. Novo token é gerado (secrets.token_urlsafe)
        ↓
5. Token salvo no banco com expiração de 15 min
        ↓
6. E-mail HTML enviado via SMTP com o token
        ↓
7. Usuário digita o token recebido
        ↓
8. Sistema valida: token existe? não usado? não expirado?
        ↓ (válido)
9. Usuário digita nova senha
        ↓
10. Senha validada (regex) → hash SHA-256 → salva no banco
        ↓
11. Token marcado como usado
```

O e-mail enviado é formatado em **HTML responsivo** com o token destacado e informações sobre o prazo de expiração.

---

## 🗄️ Banco de Dados

### Modelo de Entidades

```
tbl_usuarios
├── id_usuarios (PK)
├── nome_usuarios
├── email_usuarios (UNIQUE)
├── senha_usuarios (SHA-256)
├── ativo (BOOL) ← Soft Delete
└── data_criacao_usuarios

tbl_contas
├── id_contas (PK)
├── usuario_id (FK → tbl_usuarios)
├── nome_contas
├── tipo_contas (ENUM: corrente, poupanca, carteira)
├── saldo_contas (DECIMAL 10,2)
└── data_criacao_contas

tbl_categorias
├── id_categorias (PK)
├── nome_categorias (UNIQUE)
└── descricao_categorias

tbl_transacoes
├── id_transacoes (PK)
├── conta_id (FK → tbl_contas)
├── categoria_id (FK → tbl_categorias)
├── tipo_transacoes (ENUM: entrada, saida)
├── valor_transacoes (DECIMAL 10,2)
├── descricao_transacoes
└── data_transacao

tbl_reset_tokens
├── id_tokens (PK)
├── usuario_id (FK → tbl_usuarios)
├── token (UNIQUE)
├── expira_em (DATETIME)
├── usado (BOOLEAN)
└── criado_em
```

### Relacionamentos

- Um usuário possui **muitas contas**
- Uma conta possui **muitas transações**
- Uma categoria pode ter **muitas transações**
- Um usuário pode ter **muitos tokens de reset** (apenas 1 ativo por vez)

---

## 🔮 Melhorias Futuras

### Funcionalidades

- [ ] **Metas financeiras** — Definir e acompanhar metas de economia por período
- [ ] **Transferência entre contas** — Mover saldo entre contas do mesmo usuário
- [ ] **Relatórios por período** — Filtrar transações por intervalo de datas (ex.: mês atual, últimos 30 dias)
- [ ] **Exportação de dados** — Exportar transações para CSV ou PDF
- [ ] **Recorrência de transações** — Registrar transações fixas mensais automaticamente
- [ ] **Multi-moeda** — Suporte a diferentes moedas com conversão

### Técnicas e Segurança

- [ ] **Bcrypt para hashing** — Substituir SHA-256 por bcrypt, que é mais seguro para senhas por ser lento por design e suportar salt automático
- [ ] **Limite de tentativas de login** — Bloquear temporariamente após N tentativas falhas (brute-force protection)
- [ ] **ORM (SQLAlchemy)** — Substituir queries manuais por um ORM para maior segurança e produtividade
- [ ] **Logging estruturado** — Registrar erros e ações críticas em arquivo de log
- [ ] **Testes automatizados** — Cobertura com `pytest` nas camadas de serviço e repositório
- [ ] **Pool de conexões** — Substituir conexões individuais por um pool (ex.: `mysql-connector` com pooling) para melhor performance
- [ ] **Migração de banco** — Adotar Alembic ou script de versionamento de schema

### Interface

- [ ] **Interface web** — Migrar a CLI para uma aplicação web com Flask ou FastAPI + frontend
- [ ] **Interface TUI** — Usar bibliotecas como `rich` ou `textual` para uma CLI mais moderna e interativa
- [ ] **Paginação** — Paginar a listagem de transações para contas com muitos registros

---

## 👤 Autor

**Jhonypaula**

Desenvolvido como projeto de portfólio para demonstrar boas práticas em Python com arquitetura em camadas, integração com banco de dados relacional e funcionalidades reais de um sistema financeiro.

---

## 📜 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

Feito com 💚 em Python

</div>