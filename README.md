main

<div align="center">

<img src="https://img.shields.io/badge/MyFinance-Gestor%20Financeiro%20Pessoal-27AE60?style=for-the-badge" alt="MyFinance" />

# 💰 MyFinance

**Sistema completo de gerenciamento financeiro pessoal com backend em Python, CLI interativa e interface desktop em Tkinter.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Tkinter](https://img.shields.io/badge/Tkinter-Desktop%20UI-FF6B35?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-11557C?style=flat-square&logo=python&logoColor=white)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/Licença-MIT-green?style=flat-square)](./backend/LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=flat-square)]()

<br/>

> 🏦 Controle suas finanças com elegância — gerencie contas, registre transações, visualize gráficos e acompanhe sua evolução financeira mensal.

<br/>

[📖 Documentação](#-documentação) · [🚀 Como Instalar](#-instalação) · [🖥️ Screenshots](#%EF%B8%8F-screenshots) · [🗺️ Roadmap](#%EF%B8%8F-roadmap)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Tecnologias](#-tecnologias)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Funcionalidades](#-funcionalidades)
- [Banco de Dados](#-banco-de-dados)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Screenshots](#%EF%B8%8F-screenshots)
- [Fluxo do Sistema](#-fluxo-do-sistema)
- [Roadmap](#%EF%B8%8F-roadmap)
- [Convenções](#-convenções)
- [Autor](#-autor)
- [Licença](#-licença)

---

## 📌 Sobre o Projeto

**MyFinance** é um sistema de controle financeiro pessoal desenvolvido inteiramente em Python. O projeto foi construído com foco em boas práticas de arquitetura em camadas, separando claramente a lógica de negócio, o acesso a dados e as camadas de apresentação.

O sistema é composto por três módulos independentes que compartilham o mesmo backend:

| Módulo | Descrição | Interface |
|--------|-----------|-----------|
| `backend/` | Lógica de negócio, acesso ao banco e utilitários | Biblioteca Python |
| `cli/` | Interface de linha de comando interativa | Terminal |
| `frontend/` | Aplicação desktop com dashboard gráfico | Tkinter (GUI) |

---

## 🏗️ Arquitetura do Sistema

O projeto adota uma **arquitetura em camadas** (Layered Architecture) com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                  CAMADAS DE APRESENTAÇÃO                │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │    CLI (Terminal)    │  │  Frontend (Tkinter GUI)  │ │
│  └──────────┬───────────┘  └────────────┬─────────────┘ │
└─────────────┼───────────────────────────┼───────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (CORE)                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Services (Regras de Negócio)       │   │
│  │  auth · conta · transacao · dashboard · email   │   │
│  └──────────────────────┬──────────────────────────┘   │
│  ┌───────────────────────▼──────────────────────────┐   │
│  │             Repository (Acesso a Dados)          │   │
│  │  auth · conta · transacao · dashboard · token   │   │
│  └──────────────────────┬──────────────────────────┘   │
│  ┌───────────────────────▼──────────────────────────┐   │
│  │            Core (Infraestrutura)                 │   │
│  │        connection.py · config.py                 │   │
│  └──────────────────────┬──────────────────────────┘   │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │   MySQL Database    │
              │    my_finance       │
              └─────────────────────┘
```

### Princípios adotados

- **Separação de responsabilidades**: cada camada tem uma única função
- **DRY**: o backend é compartilhado entre CLI e Frontend — nenhum código de negócio é duplicado
- **Injeção de dependência via sys.path**: CLI e Frontend resolvem o backend em runtime
- **Soft Delete**: usuários desativados não são removidos do banco
- **Segurança**: senhas armazenadas com hash SHA-256; tokens de reset com expiração de 15 min

---

## 🛠️ Tecnologias

### Backend & CLI
| Tecnologia | Uso |
|------------|-----|
| Python 3.10+ | Linguagem principal |
| MySQL 8.0+ | Banco de dados relacional |
| mysql-connector-python | Driver de conexão com MySQL |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| hashlib (stdlib) | Hash SHA-256 para senhas |
| secrets (stdlib) | Geração de tokens seguros |
| smtplib (stdlib) | Envio de e-mail para recuperação de senha |
| re (stdlib) | Validação via regex (email, senha forte) |

### Frontend (Desktop)
| Tecnologia | Uso |
|------------|-----|
| tkinter (stdlib) | Framework de interface gráfica |
| matplotlib 3.7+ | Gráficos de evolução financeira |

---

## 📁 Estrutura de Pastas

```
expotech-myfinance/
│
├── 📄 README.md                        ← Este arquivo
├── 📄 .gitignore
│
├── 🗄️ backend/                         ← Núcleo do sistema
│   ├── core/
│   │   ├── connection.py               ← Conexão com MySQL
│   │   ├── config.py                   ← Variáveis de ambiente (email/smtp)
│   │   └── schema.sql                  ← DDL completo do banco de dados
│   ├── repository/                     ← Acesso ao banco (queries SQL)
│   │   ├── auth_repository.py
│   │   ├── conta_repository.py
│   │   ├── transacao_repository.py
│   │   ├── categoria_repository.py
│   │   ├── dashboard_repository.py
│   │   └── resetar_senha_repository.py
│   ├── services/                       ← Regras de negócio
│   │   ├── auth_services.py
│   │   ├── conta_services.py
│   │   ├── transacao_services.py
│   │   ├── categoria_services.py
│   │   ├── dashboard_services.py
│   │   ├── email_service.py
│   │   └── resetar_senha_service.py
│   ├── utils/
│   │   ├── security.py                 ← Hash de senhas
│   │   ├── token_generator.py          ← Geração de tokens seguros
│   │   ├── validators.py               ← Validação de campos
│   │   └── regex_validators.py         ← Validação de email e senha forte
│   ├── .env.example                    ← Modelo de variáveis de ambiente
│   ├── requirements.txt
│   └── LICENSE
│
├── 💻 cli/                             ← Interface de linha de comando
│   ├── main.py                         ← Entry point da CLI
│   ├── requirements.txt
│   └── README.md
│
└── 🖥️ frontend/                        ← Interface desktop (Tkinter)
    ├── main.py                         ← Entry point da GUI
    ├── requirements.txt
    └── app/
        ├── application.py              ← Janela principal e roteamento
        ├── config.py                   ← Design tokens (cores, fontes, tamanhos)
        ├── utils.py                    ← Funções utilitárias (formatação BRL)
        ├── components/                 ← Widgets reutilizáveis
        │   ├── sidebar.py
        │   ├── topbar.py
        │   ├── modal.py
        │   ├── metric_card.py
        │   ├── tx_table.py
        │   ├── flash_stack.py
        │   
        ├── pages/                      ← Telas da aplicação
        │   ├── login.py
        │   ├── cadastro.py
        │   ├── reset_senha.py
        │   ├── dashboard.py
        │   ├── contas.py
        │   ├── transacoes.py
        │   ├── categorias.py
        │   ├── historico.py
        │   └── base.py
        ├── services/
        │   ├── backend.py              ← Adapter: conecta UI ao backend
        │   └── backend_path.py         ← Resolve sys.path em runtime
        ├── state/
        │   └── store.py                ← Estado global reativo da aplicação
        └── models/                     ← Dataclasses dos modelos de domínio
            ├── user.py
            ├── account.py
            ├── transaction.py
            ├── category.py
            └── monthly.py
```

---

## ✨ Funcionalidades

### 🔐 Autenticação
- [x] Cadastro de usuário com validação de e-mail e senha forte
- [x] Login com verificação de conta ativa
- [x] Recuperação de senha via e-mail com token seguro (expira em 15 min)
- [x] Soft delete de conta (desativação sem exclusão)

### 🏦 Contas
- [x] Criar contas do tipo: `corrente`, `poupança`, `carteira`
- [x] Listar todas as contas com saldo atual
- [x] Editar nome e tipo da conta
- [x] Excluir conta

### 💸 Transações
- [x] Registrar entradas e saídas com atualização automática de saldo
- [x] Editar transações existentes
- [x] Excluir transações
- [x] Filtrar por tipo (`entrada` / `saída`)
- [x] Filtrar por categoria
- [x] Filtrar por descrição (busca textual)
- [x] Listar histórico completo ordenado por data

### 📊 Dashboard
- [x] Saldo total consolidado de todas as contas
- [x] Total de entradas e saídas
- [x] Quantidade de transações
- [x] Gasto por categoria (ranking)
- [x] Maior categoria de gasto
- [x] Evolução mensal de entradas/saídas (últimos 12 meses) com gráfico de linha

### 🏷️ Categorias
- [x] 12 categorias pré-cadastradas (Alimentação, Transporte, Saúde, etc.)
- [x] Listagem de todas as categorias disponíveis

---

## 🗄️ Banco de Dados

O banco de dados **`my_finance`** é composto por 5 tabelas:

```sql
tbl_usuarios        ← Usuários do sistema
tbl_contas          ← Contas financeiras por usuário
tbl_categorias      ← Categorias de transações (seed inicial incluído)
tbl_transacoes      ← Movimentações financeiras
tbl_reset_tokens    ← Tokens de recuperação de senha
```

### Diagrama Entidade-Relacionamento (simplificado)

```
tbl_usuarios (1) ──────< (N) tbl_contas
tbl_contas   (1) ──────< (N) tbl_transacoes
tbl_categorias (1) ────< (N) tbl_transacoes
tbl_usuarios (1) ──────< (N) tbl_reset_tokens
```

### Tabelas em destaque

**`tbl_usuarios`**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id_usuarios | INT PK AUTO | Identificador |
| nome_usuarios | VARCHAR(100) | Nome do usuário |
| email_usuarios | VARCHAR(150) UNIQUE | E-mail de login |
| senha_usuarios | VARCHAR(255) | Senha com hash SHA-256 |
| ativo | BOOL | Soft delete flag |
| data_criacao_usuarios | DATETIME | Data de cadastro |

**`tbl_transacoes`**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id_transacoes | INT PK AUTO | Identificador |
| conta_id | INT FK | Conta vinculada |
| categoria_id | INT FK | Categoria vinculada |
| tipo_transacoes | ENUM('entrada','saida') | Tipo da movimentação |
| valor_transacoes | DECIMAL(10,2) | Valor da transação |
| descricao_transacoes | VARCHAR(255) | Descrição |
| data_transacao | DATETIME | Data/hora |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/jhonypaula/expotech-myfinance.git
cd expotech-myfinance
```

### 2. Configure o banco de dados

Acesse o MySQL e execute o schema:

```bash
mysql -u root -p < backend/core/schema.sql
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `backend/.env` com suas credenciais:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=my_finance

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
```

> 💡 Para Gmail, use uma **Senha de App** (não a senha da conta). Acesse: Conta Google → Segurança → Verificação em duas etapas → Senhas de app.

---

## ▶️ Como Executar

### CLI (Terminal)

```bash
cd cli
pip install -r requirements.txt
python main.py
```

### Frontend Desktop (Tkinter)

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

> ℹ️ O `frontend/` e o `cli/` resolvem o `backend/` automaticamente via `sys.path`. Não é necessário instalar o backend como pacote separado.

---

## 🔄 Fluxo do Sistema

```
Usuário inicia o app
        │
        ▼
┌───────────────┐     Não possui conta
│  Tela de      │ ──────────────────────► Tela de Cadastro
│  Login        │
└───────┬───────┘
        │ Autenticado
        ▼
┌───────────────┐
│  Dashboard    │ ◄─────────────────────────────┐
│  (Visão Geral)│                               │
└───────┬───────┘                               │
        │                                       │
        ├──► Contas ──────► CRUD de Contas      │
        │                                       │
        ├──► Transações ──► Nova Transação ─────┤
        │         │                             │
        │         └──► Atualiza Saldo da Conta  │
        │                                       │
        ├──► Categorias ──► Listar Categorias   │
        │                                       │
        └──► Histórico ───► Filtros/Busca ──────┘
```

---

## 🗺️ Roadmap

### v1.0 — MVP ✅
- [x] Autenticação (login, cadastro, logout)
- [x] CRUD de Contas
- [x] CRUD de Transações
- [x] Dashboard com métricas
- [x] Recuperação de senha por e-mail
- [x] Interface CLI
- [x] Interface Desktop (Tkinter)

### v1.1 — Melhorias Planejadas 🔄
- [ ] Exportação de relatórios em PDF/CSV
- [ ] Tela de perfil do usuário com edição de dados
- [ ] Gráfico de pizza por categoria no dashboard
- [ ] Paginação na listagem de transações
- [ ] Filtro de transações por período (data inicial/final)

### v2.0 — Futuro 🚀
- [ ] Migração do backend para API REST (FastAPI)
- [ ] Autenticação com JWT
- [ ] Interface Web (React ou Vue.js)
- [ ] Metas financeiras mensais
- [ ] Notificações de gastos por e-mail
- [ ] Multi-moeda
- [ ] Suporte a PostgreSQL

---

## 📐 Convenções

### Padrão de commits (Conventional Commits)

```
feat:     nova funcionalidade
fix:      correção de bug
docs:     atualização de documentação
style:    formatação, sem alteração de lógica
refactor: refatoração sem mudança de comportamento
test:     adição ou correção de testes
chore:    tarefas de manutenção (deps, configs)
```

**Exemplos:**
```bash
git commit -m "feat: adicionar filtro de transações por período"
git commit -m "fix: corrigir cálculo de saldo após exclusão de transação"
git commit -m "docs: atualizar README com instruções de instalação"
```

### Nomenclatura

| Contexto | Padrão | Exemplo |
|----------|--------|---------|
| Arquivos Python | `snake_case` | `auth_services.py` |
| Classes | `PascalCase` | `AppStore`, `DashboardPage` |
| Funções e variáveis | `snake_case` | `buscar_saldo_total` |
| Constantes | `UPPER_SNAKE_CASE` | `WINDOW_MIN_W`, `GREEN` |
| Tabelas MySQL | `tbl_snake_case` | `tbl_usuarios` |
| Colunas MySQL | `nome_tabela` | `saldo_contas`, `tipo_transacoes` |

---

## 👤 Autor

<div align="center">

**Desenvolvido por JhonyPaula**

[![GitHub](https://img.shields.io/badge/GitHub-@jhonypaula-181717?style=flat-square&logo=github)](https://github.com/jhonypaula)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jhony%20Weverton-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/jhonyweverton)

</div>

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](./backend/LICENSE) para detalhes.

---

<div align="center">

Feito com ❤️ e ☕ em Python

⭐ Se este projeto te ajudou, deixe uma estrela no repositório!

</div>