"""Janela principal e troca de telas do app."""
from __future__ import annotations
import tkinter as tk

from app import config as C
from app.state.store import AppStore
from app.components.sidebar import Sidebar
from app.components.topbar import Topbar
from app.components.flash_stack import FlashStack
from app.pages.login import LoginPage
from app.pages.cadastro import CadastroPage
from app.pages.reset_senha import ResetSenhaPage
from app.pages.dashboard import DashboardPage
from app.pages.contas import ContasPage
from app.pages.transacoes import TransacoesPage
from app.pages.categorias import CategoriasPage
from app.pages.historico import HistoricoPage

_SCREEN_META = {
    'dashboard':  ('Dashboard',    'Visao geral das suas financas'),
    'contas':     ('Contas',       'Gerencie suas contas bancarias e carteiras'),
    'transacoes': ('Transacoes',   'Suas entradas e saidas'),
    'categorias': ('Categorias',   'Organize suas transacoes por categoria'),
    'historico':  ('Historico',    'Registro completo de movimentacoes'),
}


class Application:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title('MyFinance - Gestor Financeiro')
        self._root.minsize(C.WINDOW_MIN_W, C.WINDOW_MIN_H)
        self._root.geometry(f'{C.WINDOW_MIN_W}x{C.WINDOW_MIN_H}')
        self._root.configure(bg=C.BG)

        # Antes do login o store fica só com o usuário placeholder.
        self._store = AppStore()
        self._current_screen = 'login'

        self._flash = FlashStack(root)
        self._montar()
        self._exibir_tela('login')

    # Montagem da janela
    def _montar(self) -> None:
        # Login e cadastro ocupam a janela inteira.
        self._auth_shell = tk.Frame(self._root, bg=C.BG)

        # Depois do login entra a estrutura com sidebar e conteúdo.
        self._app_shell = tk.Frame(self._root, bg=C.BG)
        self._app_shell.columnconfigure(1, weight=1)
        self._app_shell.rowconfigure(0, weight=1)

        # Recriadas no login/logout para pegar o usuário certo.
        self._sidebar: Sidebar | None = None
        self._topbar: Topbar | None = None

        # Coluna que fica à direita da sidebar.
        self._main_col = tk.Frame(self._app_shell, bg=C.BG)
        self._main_col.grid(row=0, column=1, sticky='nsew')
        self._main_col.columnconfigure(0, weight=1)
        self._main_col.rowconfigure(1, weight=1)

        # As páginas ficam empilhadas aqui; quem aparece é decidido por tkraise.
        self._content = tk.Frame(self._main_col, bg=C.BG)
        self._content.grid(row=1, column=0, sticky='nsew')
        self._content.columnconfigure(0, weight=1)
        self._content.rowconfigure(0, weight=1)

        # As telas internas só existem quando já temos um usuário logado.
        self._pages: dict[str, tk.Frame] = {}
        self._app_pages_built = False

        self._montar_paginas_auth()

    def _montar_paginas_auth(self) -> None:
        login = LoginPage(
            self._auth_shell,
            store=self._store,
            ao_logar=lambda: self._entrar_app(),
            ir_cadastro=lambda: self._exibir_tela('cadastro'),
            flash=self._flash.show,
            ir_reset_senha=lambda: self._exibir_tela('reset_senha'),
        )
        login.place(relx=0, rely=0, relwidth=1, relheight=1)

        cadastro = CadastroPage(
            self._auth_shell,
            store=self._store,
            ao_cadastrar=lambda: self._entrar_app(),
            ir_login=lambda: self._exibir_tela('login'),
            flash=self._flash.show,
        )
        cadastro.place(relx=0, rely=0, relwidth=1, relheight=1)

        reset_senha = ResetSenhaPage(
            self._auth_shell,
            ir_login=lambda: self._exibir_tela('login'),
            flash=self._flash.show,
        )
        reset_senha.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._login_page = login
        self._cadastro_page = cadastro
        self._reset_senha_page = reset_senha

    def _montar_paginas_app(self) -> None:
        def flash(kind: str, msg: str) -> None:
            self._flash.show(kind, msg)

        # A topbar mostra dados do usuário, então nasce só depois do login.
        if self._topbar is not None:
            self._topbar.destroy()
        self._topbar = Topbar(self._main_col, user=self._store.user, ao_sair=self._sair)
        self._topbar.grid(row=0, column=0, sticky='ew')

        # Garante que um novo login não herde widgets da sessão anterior.
        for page in self._pages.values():
            page.destroy()
        self._pages.clear()

        pages_defs = [
            ('dashboard',  lambda: DashboardPage(
                self._content, self._store,
                ir_transacoes=lambda: self._exibir_tela('transacoes'),
                ir_contas=lambda: self._exibir_tela('contas'),
            )),
            ('contas',     lambda: ContasPage(self._content, self._store, flash)),
            ('transacoes', lambda: TransacoesPage(self._content, self._store, flash)),
            ('categorias', lambda: CategoriasPage(self._content, self._store, flash)),
            ('historico',  lambda: HistoricoPage(self._content, self._store)),
        ]

        for name, factory in pages_defs:
            page = factory()
            page.grid(row=0, column=0, sticky='nsew')
            self._pages[name] = page

        self._app_pages_built = True

    def _entrar_app(self) -> None:
        """Entra na área logada depois de login ou cadastro."""
        self._montar_paginas_app()
        self._exibir_tela('dashboard')

    def _sair(self) -> None:
        self._store.sair()
        # Na próxima entrada a interface logada é montada do zero.
        if self._sidebar is not None:
            self._sidebar.destroy()
            self._sidebar = None
        self._app_pages_built = False
        self._exibir_tela('login')

    # Navegação
    def _exibir_tela(self, screen: str) -> None:
        prev = self._current_screen
        self._current_screen = screen

        if screen in ('login', 'cadastro', 'reset_senha'):
            self._app_shell.place_forget()
            self._auth_shell.place(relx=0, rely=0, relwidth=1, relheight=1)
            if screen == 'login':
                self._login_page.tkraise()
            elif screen == 'cadastro':
                self._cadastro_page.tkraise()
            else:
                self._reset_senha_page.tkraise()
            return

        if not self._app_pages_built:
            # Cinto de segurança para chamadas fora do fluxo normal.
            return

        self._auth_shell.place_forget()
        self._app_shell.place(relx=0, rely=0, relwidth=1, relheight=1)

        # A sidebar guarda estado visual; no primeiro acesso ela ainda não existe.
        if self._sidebar is None or prev in ('login', 'cadastro'):
            self._remontar_sidebar(screen)
        else:
            self._sidebar.definir_ativa(screen)

        # Mantém o cabeçalho sincronizado com a tela atual.
        meta = _SCREEN_META.get(screen, ('', ''))
        if self._topbar is not None:
            self._topbar.definir_titulo(*meta)

        # Dá chance para a página se atualizar sempre que volta ao foco.
        page = self._pages.get(screen)
        if page:
            page.tkraise()
            if hasattr(page, 'ao_exibir'):
                page.ao_exibir()

    def _remontar_sidebar(self, active: str) -> None:
        if self._sidebar:
            self._sidebar.destroy()

        self._sidebar = Sidebar(
            self._app_shell,
            active_screen=active,
            ao_navegar=self._exibir_tela,
            user=self._store.user,
        )
        self._sidebar.grid(row=0, column=0, sticky='ns')