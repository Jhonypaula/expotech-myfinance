FRONT END 

<div align="center">

# 🖥️ MyFinance — Frontend Desktop

**Interface gráfica desktop construída com Tkinter, com dashboard de gráficos, navegação por sidebar e design system próprio.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-stdlib-FF6B35?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557C?style=flat-square)](https://matplotlib.org/)
[![Windows](https://img.shields.io/badge/Windows-HiDPI%20Ready-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Como Executar](#-como-executar)
- [Arquitetura da Interface](#-arquitetura-da-interface)
- [Design System](#-design-system)
- [Telas da Aplicação](#-telas-da-aplicação)
- [Componentes Reutilizáveis](#-componentes-reutilizáveis)
- [Estado Global (AppStore)](#-estado-global-appstore)
- [Integração com o Backend](#-integração-com-o-backend)
- [Modelos de Domínio](#-modelos-de-domínio)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Dependências](#-dependências)

---

## 🔍 Visão Geral

O módulo `frontend/` é uma aplicação desktop completa construída com **Tkinter** (stdlib do Python) e **Matplotlib** para os gráficos do dashboard. A interface possui uma sidebar de navegação lateral, topbar com informações da tela atual, modais para criação e edição de dados, e um sistema de notificações flash.

A aplicação segue um modelo de **estado reativo centralizado** (`AppStore`), onde os dados são carregados uma vez do backend e distribuídos para todas as telas via callbacks de assinatura (padrão Observer).

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.10+
- MySQL rodando com o banco `my_finance` configurado
- Arquivo `backend/.env` preenchido

### Instalação

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

> ℹ️ No Windows, a aplicação ativa automaticamente o suporte a **monitores HiDPI** via `ctypes.windll.shcore.SetProcessDpiAwareness(1)`.

### Dimensão mínima da janela

A janela é redimensionável com tamanho mínimo de **1100 × 700 px** (definido em `app/config.py`).

---

## 🏗️ Arquitetura da Interface

```
main.py
  └── Application (application.py)
        │
        ├── AppStore (state/store.py)          ← Estado global reativo
        │
        ├── [Shell de Auth]                    ← Antes do login
        │     ├── LoginPage
        │     ├── CadastroPage
        │     └── ResetSenhaPage
        │
        └── [Shell do App]                     ← Após login
              ├── Sidebar                      ← Navegação lateral
              ├── Topbar                       ← Título da tela atual
              ├── FlashStack                   ← Notificações toast
              └── [Área de conteúdo]
                    ├── DashboardPage
                    ├── ContasPage
                    ├── TransacoesPage
                    ├── CategoriasPage
                    └── HistoricoPage
```

### Ciclo de vida da aplicação

```
Inicialização
    │
    ▼
Application.__init__()
    ├── Cria AppStore (estado vazio)
    ├── Monta shells de auth e app
    └── Exibe LoginPage
              │
              │ usuário autentica
              ▼
        _entrar_app()
              ├── AppStore.inicializar(user) ← carrega todos os dados do backend
              ├── Cria Sidebar e Topbar com o usuário logado
              ├── Constrói as páginas internas (instanciadas uma vez)
              └── Exibe DashboardPage
                        │
                        │ navegação pela sidebar
                        ▼
                  _exibir_tela(nome)
                        ├── Atualiza topbar
                        ├── Chama page.ao_entrar() na tela destino
                        └── tkraise() traz a tela para frente
```

---

## 🎨 Design System

Todas as constantes visuais ficam centralizadas em `app/config.py`:

### Paleta de Cores

| Constante | Hex | Uso |
|-----------|-----|-----|
| `GREEN` | `#27AE60` | Cor primária, entradas, destaque |
| `GREEN_700` | `#1e8449` | Hover de botões primários |
| `RED` | `#E74C3C` | Saídas, erros, alertas |
| `BLUE` | `#2980B9` | Informativo |
| `AMBER` | `#E0A800` | Avisos |
| `BG` | `#f0f4f8` | Fundo principal |
| `SURFACE` | `#ffffff` | Cards e painéis |
| `SIDE` | `#0f1923` | Fundo da sidebar |
| `SIDE_ACTIVE` | `#27AE60` | Item ativo na sidebar |
| `INK` | `#0d1b2a` | Texto principal |
| `INK_3` | `#5b6b80` | Texto secundário |

### Tipografia

| Constante | Fonte | Uso |
|-----------|-------|-----|
| `FONT_DISPLAY` | Segoe UI | Títulos e headers |
| `FONT_BODY` | Segoe UI | Corpo de texto |
| `FONT_MONO` | Consolas | Valores monetários, dados técnicos |

### Dimensões

| Constante | Valor | Descrição |
|-----------|-------|-----------|
| `WINDOW_MIN_W` | 1100 px | Largura mínima da janela |
| `WINDOW_MIN_H` | 700 px | Altura mínima da janela |
| `SIDEBAR_W` | 220 px | Largura fixa da sidebar |
| `CONTENT_PAD` | 20 px | Padding interno do conteúdo |

---

## 📱 Telas da Aplicação

### 🔑 Login

Tela de autenticação com campos de e-mail e senha. Possui links para cadastro e para recuperação de senha.

**Funcionalidades:**
- Autenticação com e-mail e senha
- Redirecionamento para cadastro
- Redirecionamento para recuperação de senha
- Exibição de erros via FlashStack

### 📝 Cadastro

Formulário de criação de conta com validação em tempo real.

**Funcionalidades:**
- Campos: nome, e-mail, senha
- Validação: e-mail com regex, senha forte
- Feedback de erro imediato

### 🔓 Redefinição de Senha

Fluxo em dois passos: solicitar token e redefinir senha.

### 📊 Dashboard

Tela principal após login. Exibe métricas financeiras consolidadas e gráfico de evolução mensal.

**Componentes:**
- **MetricCards**: Saldo total, Total entradas, Total saídas, Qtd. transações
- **Gráfico de linha** (Matplotlib): Evolução de entradas e saídas nos últimos 12 meses
- **Tabela de transações recentes**: as últimas movimentações do usuário
- **Indicadores de tendência**: comparação com o mês anterior (`+X.X% vs. Mês anterior`)

### 🏦 Contas

CRUD completo de contas financeiras do usuário.

**Funcionalidades:**
- Cards de conta com saldo, tipo e data de criação
- Modal para criar nova conta (nome, tipo, saldo inicial)
- Modal para editar conta existente
- Confirmação antes de excluir
- Indicador visual por tipo: 🏦 corrente · 💰 poupança · 👝 carteira

### 💸 Transações

Registro e gestão de movimentações financeiras por conta.

**Funcionalidades:**
- Seleção de conta ativa
- Tabela com tipo, valor, categoria, descrição e data
- Modal para nova transação (conta, categoria, tipo, valor, descrição)
- Edição e exclusão de transações existentes
- Atualização automática do saldo após operações

### 🏷️ Categorias

Listagem das categorias de transações disponíveis.

**Funcionalidades:**
- Exibição em grid das 12 categorias pré-cadastradas
- Nome e descrição de cada categoria

### 📜 Histórico

Visão unificada de todas as transações do usuário com filtros.

**Funcionalidades:**
- Lista todas as transações de todas as contas
- Filtros por tipo (entrada/saída), categoria e período
- Busca por descrição

---

## 🧩 Componentes Reutilizáveis

### `Sidebar` (`components/sidebar.py`)

Menu lateral fixo com navegação entre telas. Recebe o nome da tela ativa e aplica estilo de destaque ao item correspondente.

```python
Sidebar(
    parent=frame,
    active_screen='dashboard',
    ao_navegar=lambda nome: app._exibir_tela(nome),
    user=store.usuario
)
```

**Itens de navegação:**
```
⊞  Dashboard
◈  Contas
⇄  Transações
◑  Categorias
◷  Histórico
```

### `Topbar` (`components/topbar.py`)

Barra superior que exibe o título e subtítulo da tela atual, além do nome do usuário logado.

### `MetricCard` (`components/metric_card.py`)

Card reutilizável para exibir uma métrica com título, valor principal e texto de tendência.

```python
MetricCard(
    parent=frame,
    titulo="Saldo Total",
    valor="R$ 3.450,00",
    tendencia="+12.3% vs. Abril",
    positivo=True,
    cor=C.GREEN
)
```

### `TxTable` (`components/tx_table.py`)

Tabela de transações com suporte a seleção, colorização por tipo (verde para entrada, vermelho para saída) e callbacks de ação.

### `Modal` (`components/modal.py`)

Sistema de modais genérico para formulários de criação e edição. Suporta campos de texto, dropdowns e botões de ação.

### `FlashStack` (`components/flash_stack.py`)

Sistema de notificações toast (mensagens temporárias). As mensagens são empilhadas e desaparecem automaticamente após alguns segundos.

```python
flash.mostrar("Conta criada com sucesso!", tipo="sucesso")
flash.mostrar("E-mail inválido.", tipo="erro")
```

### `LogoWidget` (`components/logo.py`)

Widget de logo/marca da aplicação. Usa iniciais em modo texto por padrão (`APP_INITIALS = 'M'`), com suporte a imagem PNG/ICO via `APP_LOGO_PATH`.

### Widgets Base (`components/widgets.py`)

Funções utilitárias para criar widgets com o design system aplicado:

| Função | Descrição |
|--------|-----------|
| `card(parent, **kw)` | Frame com fundo `SURFACE` e borda arredondada |
| `button(parent, texto, cmd, **kw)` | Botão estilizado com cor primária |
| `scrollable_frame(parent)` | Frame com scroll vertical |

---

## 🗃️ Estado Global (AppStore)

`app/state/store.py` centraliza o estado da sessão do usuário usando o padrão **Observer**:

```python
class AppStore:
    _user: User                  # Usuário logado
    _accounts: List[Account]     # Contas carregadas
    _transactions: List[Transaction]  # Transações carregadas
    _categories: List[Category]  # Categorias disponíveis
    _monthly: List[MonthlyTotal] # Evolução mensal (12 meses)
    _listeners: List[Callable]   # Callbacks das telas
```

### Como as telas se inscrevem no estado

```python
# Em cada Page, no __init__:
store.inscrever(self._atualizar)   # registra callback

def ao_entrar(self):
    store.recarregar()             # busca dados atualizados no backend
    self._atualizar()              # redesenha a tela

def _atualizar(self):
    contas = store.contas          # lê do cache
    # ... redesenha widgets
```

### Reatividade

Quando uma operação de escrita ocorre (criar conta, registrar transação), o `AppStore` chama `recarregar()` e notifica todos os listeners via `_notificar()`. Todas as telas inscritas são atualizadas automaticamente.

---

## 🔗 Integração com o Backend

O arquivo `app/services/backend.py` funciona como um **adapter** entre a interface Tkinter e os services do backend Python:

```python
# Captura prints do backend como mensagens de erro
def _chamar(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = fn(*args, **kwargs)
    msg = buf.getvalue().strip()
    return result, msg

# Retorna objetos tipados, não tuples brutas
def login(email: str, senha: str) -> Tuple[Optional[User], str]:
    row, msg = _chamar(login_usuario_service, email, senha)
    if not row:
        return None, msg or "Email ou senha invalidos"
    return User(id_usuarios=int(row[0]), ...), ""
```

Todas as funções retornam uma tupla `(resultado, mensagem_de_erro)` — um contrato consistente que as telas usam para exibir feedback via `FlashStack`.

---

## 📐 Modelos de Domínio

Os modelos em `app/models/` são **dataclasses** tipadas que representam as entidades do sistema:

```python
# models/user.py
@dataclass
class User:
    id_usuarios: int
    nome_usuarios: str
    email_usuarios: str

# models/account.py
@dataclass
class Account:
    id_contas: int
    nome_contas: str
    tipo_contas: str
    saldo_contas: float
    data_criacao_contas: str

# models/transaction.py
@dataclass
class Transaction:
    id_transacoes: int
    tipo_transacoes: str    # 'entrada' | 'saida'
    valor_transacoes: float
    descricao_transacoes: str
    nome_categorias: str
    data_transacao: str
    conta_id: int

# models/monthly.py
@dataclass
class MonthlyTotal:
    ano: int
    mes: int
    total_entradas: float
    total_saidas: float
```

---

## 📁 Estrutura de Pastas

```
frontend/
│
├── main.py                    ← Entry point (DPI awareness + tk.mainloop)
├── requirements.txt
│
└── app/
    ├── application.py         ← Orquestração: janela, roteamento, ciclo de vida
    ├── config.py              ← Design tokens: cores, fontes, dimensões
    ├── utils.py               ← formatar_brl(), outras utilidades de UI
    │
    ├── components/            ← Widgets reutilizáveis
    │   ├── sidebar.py         ← Menu lateral com navegação
    │   ├── topbar.py          ← Barra superior com título da tela
    │   ├── modal.py           ← Sistema de modais/formulários
    │   ├── metric_card.py     ← Card de KPI com tendência
    │   ├── tx_table.py        ← Tabela de transações
    │   ├── flash_stack.py     ← Notificações toast
    │
    ├── pages/                 ← Telas da aplicação (uma classe por tela)
    │   ├── base.py            ← BasePage (classe base com interface padrão)
    │   ├── login.py           ← Tela de login
    │   ├── cadastro.py        ← Tela de cadastro
    │   ├── reset_senha.py     ← Fluxo de recuperação de senha
    │   ├── dashboard.py       ← Dashboard com métricas e gráfico
    │   ├── contas.py          ← CRUD de contas
    │   ├── transacoes.py      ← CRUD de transações por conta
    │   ├── categorias.py      ← Listagem de categorias
    │   └── historico.py       ← Histórico com filtros
    │
    ├── services/
    │   ├── backend.py         ← Adapter para os services do backend
    │   └── backend_path.py    ← Bootstrap do sys.path em runtime
    │
    ├── state/
    │   └── store.py           ← AppStore: estado reativo centralizado
    │
    └── models/                ← Dataclasses tipadas dos domínios
        ├── user.py
        ├── account.py
        ├── transaction.py
        ├── category.py
        └── monthly.py
```

---

## 📦 Dependências

```txt
# frontend/requirements.txt
matplotlib>=3.7.0
```

> Tkinter já vem incluído na stdlib do Python. Certifique-se de usar uma instalação Python com Tkinter habilitado (nas distros Linux pode ser necessário instalar `python3-tk`).

```bash
# Linux (Debian/Ubuntu)
sudo apt install python3-tk

# Instalação do matplotlib
pip install -r requirements.txt
```

---

<div align="center">

← [CLI](../cli/README.md) | [README Principal →](../README.md)

</div>