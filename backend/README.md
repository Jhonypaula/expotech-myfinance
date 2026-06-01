Backend

<div align="center">

# 🗄️ MyFinance — Backend

**Núcleo do sistema: regras de negócio, acesso ao banco de dados e utilitários compartilhados.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0+-ECD53F?style=flat-square)](https://pypi.org/project/python-dotenv/)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura Interna](#-arquitetura-interna)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Banco de Dados](#-banco-de-dados)
- [Módulos do Sistema](#-módulos-do-sistema)
- [Segurança](#-segurança)
- [Configuração](#-configuração)
- [Dependências](#-dependências)

---

## 🔍 Visão Geral

O `backend/` é o coração do MyFinance. Ele não expõe uma API HTTP — em vez disso, funciona como uma **biblioteca Python** importada diretamente pela CLI e pelo Frontend via `sys.path`.

Essa abordagem mantém o projeto simples e evita a necessidade de um servidor rodando em segundo plano. A CLI e o Frontend resolvem o caminho do backend em tempo de execução e chamam os `services/` diretamente.

```
cli/main.py        ─┐
                    ├──► sys.path ──► backend/services/ ──► repository/ ──► MySQL
frontend/main.py   ─┘
```

---

## 🏗️ Arquitetura Interna

O backend segue o padrão **Repository + Service Layer**:

```
┌──────────────────────────────────────────────────────┐
│                     services/                        │
│  Regras de negócio, validações, orquestração        │
│                                                      │
│  auth_services  conta_services  transacao_services  │
│  dashboard_services  resetar_senha_service           │
│  categoria_services  email_service                   │
└────────────────────────┬─────────────────────────────┘
                         │ chama
┌────────────────────────▼─────────────────────────────┐
│                    repository/                       │
│  Acesso ao banco de dados (apenas SQL, sem lógica)  │
│                                                      │
│  auth_repository  conta_repository                  │
│  transacao_repository  dashboard_repository         │
│  categoria_repository  resetar_senha_repository     │
└────────────────────────┬─────────────────────────────┘
                         │ usa
┌────────────────────────▼─────────────────────────────┐
│                      core/                           │
│  connection.py  ──  Pool de conexão MySQL            │
│  config.py      ──  Variáveis de ambiente            │
│  schema.sql     ──  DDL completo do banco            │
└──────────────────────────────────────────────────────┘
```

### Responsabilidades de cada camada

| Camada | Responsabilidade |
|--------|-----------------|
| `core/` | Infraestrutura: conexão com banco, leitura de variáveis de ambiente |
| `repository/` | Execução das queries SQL; retorna dados brutos (tuples/dicts) |
| `services/` | Validações, regras de negócio, orquestração entre repositories |
| `utils/` | Funções auxiliares reutilizáveis (hash, tokens, regex, validadores) |

---

## 📁 Estrutura de Pastas

```
backend/
│
├── core/
│   ├── connection.py          ← Abre e retorna conexão MySQL via .env
│   ├── config.py              ← Lê variáveis SMTP/e-mail do .env
│   └── schema.sql             ← DDL: CREATE DATABASE, tabelas e seed
│
├── repository/
│   ├── auth_repository.py     ← CRUD de usuários (buscar, criar, atualizar, desativar)
│   ├── conta_repository.py    ← CRUD de contas + atualização de saldo
│   ├── transacao_repository.py← CRUD de transações + filtros
│   ├── categoria_repository.py← Buscar e listar categorias
│   ├── dashboard_repository.py← Queries analíticas (totais, evolução mensal)
│   └── resetar_senha_repository.py ← CRUD de tokens de reset
│
├── services/
│   ├── auth_services.py       ← Cadastro, login, desativação de conta
│   ├── conta_services.py      ← Criar, listar, editar, excluir contas
│   ├── transacao_services.py  ← Criar, listar, editar, excluir transações + filtros
│   ├── categoria_services.py  ← Listar e validar categorias
│   ├── dashboard_services.py  ← Agregar dados financeiros para exibição
│   ├── email_service.py       ← Envio de e-mail HTML via SMTP
│   └── resetar_senha_service.py ← Fluxo completo de recuperação de senha
│
├── utils/
│   ├── security.py            ← hash_senha() com SHA-256
│   ├── token_generator.py     ← generate_reset_token() com secrets
│   ├── validators.py          ← validar_campo_vazio()
│   └── regex_validators.py    ← validar_email(), validar_senha()
│
└── LICENSE
```

---

## 🗄️ Banco de Dados

### Configuração inicial

```bash
# 1. Acesse o MySQL
mysql -u root -p

# 2. Execute o schema completo (cria banco, tabelas e seed de categorias)
source backend/core/schema.sql

# OU via linha de comando:
mysql -u root -p < backend/core/schema.sql
```

### Schema das tabelas

#### `tbl_usuarios`
```sql
CREATE TABLE tbl_usuarios (
    id_usuarios          INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuarios        VARCHAR(100) NOT NULL,
    email_usuarios       VARCHAR(150) NOT NULL UNIQUE,
    senha_usuarios       VARCHAR(255) NOT NULL,        -- hash SHA-256
    ativo                BOOL NOT NULL DEFAULT TRUE,   -- soft delete
    data_criacao_usuarios DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `tbl_contas`
```sql
CREATE TABLE tbl_contas (
    id_contas            INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id           INT NOT NULL,
    nome_contas          VARCHAR(100) NOT NULL,
    tipo_contas          ENUM('corrente', 'poupanca', 'carteira') NOT NULL,
    saldo_contas         DECIMAL(10,2) DEFAULT 0.00,
    data_criacao_contas  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES tbl_usuarios(id_usuarios)
);
```

#### `tbl_transacoes`
```sql
CREATE TABLE tbl_transacoes (
    id_transacoes        INT AUTO_INCREMENT PRIMARY KEY,
    conta_id             INT NOT NULL,
    categoria_id         INT,
    tipo_transacoes      ENUM('entrada', 'saida') NOT NULL,
    valor_transacoes     DECIMAL(10,2) NOT NULL,
    descricao_transacoes VARCHAR(255),
    data_transacao       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_id)    REFERENCES tbl_contas(id_contas),
    FOREIGN KEY (categoria_id) REFERENCES tbl_categorias(id_categorias)
);
```

#### `tbl_reset_tokens`
```sql
CREATE TABLE tbl_reset_tokens (
    id_tokens   INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id  INT NOT NULL,
    token       VARCHAR(255) NOT NULL UNIQUE,
    expira_em   DATETIME NOT NULL,           -- 15 minutos após criação
    usado       BOOLEAN DEFAULT FALSE,
    criado_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES tbl_usuarios(id_usuarios)
);
```

### Seed de categorias

O schema já inclui 12 categorias pré-cadastradas:

| ID | Nome | Descrição |
|----|------|-----------|
| 1 | Alimentacao | Ifood e comida |
| 2 | Transporte | Uber e gasolina |
| 3 | Salario | Entradas salariais |
| 4 | Lazer | Cinema e streaming |
| 5 | Saude | Farmácia |
| 6 | Educacao | Cursos e faculdade |
| 7 | Moradia | Gastos com moradia |
| 8 | Investimentos | Aplicações |
| 9 | Compras | Compras em geral |
| 10 | Assinaturas | Netflix e HBO |
| 11 | Transferencias | PIX e TED |
| 12 | Outros | Outras transações |

---

## 📦 Módulos do Sistema

### `services/auth_services.py`

Responsável pelo fluxo completo de autenticação.

| Função | Parâmetros | Retorno |
|--------|-----------|---------|
| `cadastrar_usuario_service` | nome, email, senha | tuple do usuário ou `None` |
| `login_usuario_service` | email, senha | tuple do usuário ou `None` |
| `desativar_usuario_service` | usuario_id | bool |

**Validações aplicadas no cadastro:**
- Campos obrigatórios (nome, e-mail, senha)
- Formato de e-mail via regex
- Senha forte: mínimo 8 caracteres, maiúscula, minúscula, número, caractere especial
- E-mail único (não duplicar cadastro)

### `services/transacao_services.py`

Orquestra criação, edição e exclusão de transações, com **atualização automática do saldo da conta**.

| Função | Descrição |
|--------|-----------|
| `criar_transacao_service` | Valida dados, registra transação e ajusta saldo |
| `listar_transacao_service` | Lista transações de uma conta |
| `editar_transacao_service` | Edita e recalcula saldo |
| `excluir_transacao_service` | Remove e reverte saldo |
| `filtrar_transacoes_tipo_service` | Filtra por `entrada` ou `saida` |
| `filtrar_transacao_categoria_service` | Filtra por ID de categoria |
| `filtrar_transacoes_descricao_service` | Busca textual na descrição |

### `services/resetar_senha_service.py`

Fluxo completo de recuperação de senha por e-mail:

```
1. requisicao_alterar_senha(email)
   → Gera token seguro (secrets.token_urlsafe)
   → Invalida tokens anteriores do usuário
   → Salva token com expiração (15 min)
   → Envia e-mail HTML com o token

2. validar_token_reset(token)
   → Verifica existência, expiração e se já foi usado

3. resetar_senha(token, nova_senha)
   → Valida token
   → Valida força da nova senha
   → Aplica hash SHA-256
   → Atualiza no banco e marca token como usado
```

### `services/dashboard_services.py`

Agrega dados financeiros para exibição nos dashboards da CLI e do frontend.

| Função | Descrição |
|--------|-----------|
| `buscar_saldo_total_service` | Soma de saldo de todas as contas do usuário |
| `buscar_total_entradas_service` | Soma de todas as entradas |
| `buscar_total_saidas_service` | Soma de todas as saídas |
| `buscar_gastos_categoria_service` | Gastos agrupados por categoria |
| `buscar_maior_categoria_service` | Categoria com maior gasto |
| `buscar_quantidade_transacoes_service` | Total de transações |
| `buscar_evolucao_mensal_service` | Série mensal de entradas/saídas (janela de N meses) |

---

## 🔐 Segurança

### Hash de senhas

Senhas nunca são armazenadas em texto puro. O hash é feito com SHA-256:

```python
# utils/security.py
import hashlib

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()
```

> ⚠️ **Nota para evolução:** SHA-256 sem salt é funcional para um projeto de portfólio, mas em produção recomenda-se bcrypt ou argon2 (via `passlib`).

### Tokens de recuperação de senha

```python
# utils/token_generator.py
import secrets

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)  # 32 bytes = 256 bits de entropia
```

- Token único por `UNIQUE` constraint no banco
- Expira em **15 minutos**
- Invalidado após uso (`usado = TRUE`)
- Tokens anteriores do mesmo usuário são invalidados a cada nova solicitação

### Validação de senha forte (regex)

```python
# Regex aplicado no cadastro e no reset de senha
r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
```

Exige: mínimo 8 caracteres · letra minúscula · letra maiúscula · número · caractere especial.

---

## ⚙️ Configuração

### Arquivo `.env`

```env
# Banco de dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=my_finance

# Servidor SMTP (para recuperação de senha)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app_gmail
```

> O arquivo `.env` **nunca** deve ser commitado. Já está no `.gitignore` do projeto.

---

## 📦 Dependências

```txt
# requirements.txt
python-dotenv
mysql-connector-python
```

Instale com:

```bash
pip install -r requirements.txt
```

---

<div align="center">

← [README Principal](../README.md) | [CLI →](../cli/README.md)

</div>