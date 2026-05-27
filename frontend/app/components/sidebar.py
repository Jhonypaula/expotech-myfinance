"""Menu lateral da área logada."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C
from app.models.user import User

_NAV_ITEMS = [
    ('dashboard',  'Dashboard'),
    ('contas',     'Contas'),
    ('transacoes', 'Transações'),
    ('categorias', 'Categorias'),
    ('historico',  'Histórico'),
]

_ICONS = {
    'dashboard':  '⊞',
    'contas':     '◈',
    'transacoes': '⇄',
    'categorias': '◑',
    'historico':  '◷',
}


class Sidebar(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        active_screen: str,
        ao_navegar: Callable[[str], None],
        user: User,
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=C.SIDE, width=C.SIDEBAR_W, **kwargs)
        self.pack_propagate(False)
        self._ao_navegar = ao_navegar
        self._active = active_screen
        self._btns: dict[str, tk.Button] = {}
        self._montar(user)

    # Montagem
    def _montar(self, user: User) -> None:
        self._montar_marca()
        tk.Frame(self, bg='#1a2c40', height=1).pack(fill='x')
        self._montar_nav()
        self._montar_rodape(user)

    def _montar_marca(self) -> None:
        row = tk.Frame(self, bg=C.SIDE)
        row.pack(fill='x', padx=16, pady=(18, 14))

        # Marca
        logo = tk.Frame(row, bg=C.GREEN, width=36, height=36)
        logo.pack_propagate(False)
        logo.pack(side='left')
        tk.Label(logo, text='M', bg=C.GREEN, fg='white',
                 font=(C.FONT_DISPLAY, 14, 'bold')).pack(expand=True)

        # Nome do app
        txt = tk.Frame(row, bg=C.SIDE)
        txt.pack(side='left', padx=(10, 0))
        tk.Label(txt, text='MyFinance', bg=C.SIDE, fg='#ffffff',
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(anchor='w')
        tk.Label(txt, text='GESTOR FINANCEIRO', bg=C.SIDE, fg=C.SIDE_TEXT_2,
                 font=(C.FONT_BODY, 8)).pack(anchor='w')

    def _montar_nav(self) -> None:
        section = tk.Frame(self, bg=C.SIDE)
        section.pack(fill='x', padx=10, pady=(14, 6))
        tk.Label(section, text='NAVEGAÇÃO', bg=C.SIDE, fg='#3d5166',
                 font=(C.FONT_BODY, 8, 'bold')).pack(anchor='w', padx=6, pady=(0, 8))

        for item_id, label_text in _NAV_ITEMS:
            btn = self._botao_lateral(section, item_id, label_text)
            self._btns[item_id] = btn

    def _montar_rodape(self, user: User) -> None:
        footer = tk.Frame(self, bg=C.SIDE)
        footer.pack(fill='x', side='bottom', padx=10, pady=(0, 12))
        tk.Frame(footer, bg='#1a2c40', height=1).pack(fill='x', pady=(0, 10))

        user_row = tk.Frame(footer, bg=C.SIDE_2, padx=8, pady=8,
                            highlightthickness=1, highlightbackground='#1c3248')
        user_row.pack(fill='x')

        # Avatar simples com a inicial do usuário.
        av = tk.Frame(user_row, bg=C.GREEN, width=30, height=30)
        av.pack_propagate(False)
        av.pack(side='left')
        tk.Label(av, text=user.nome_usuarios[0], bg=C.GREEN, fg='white',
                 font=(C.FONT_BODY, 11, 'bold')).pack(expand=True)

        # Identificação da sessão. O botão de sair agora vive na topbar,
        # então o nome e o e-mail ocupam o resto da largura disponível.
        col = tk.Frame(user_row, bg=C.SIDE_2)
        col.pack(side='left', padx=(8, 0), fill='x', expand=True)
        tk.Label(col, text=user.nome_usuarios, bg=C.SIDE_2, fg='#e6ecf4',
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w')
        tk.Label(col, text=user.email_usuarios, bg=C.SIDE_2, fg=C.SIDE_TEXT_2,
                 font=(C.FONT_BODY, 8)).pack(anchor='w')

    def _botao_lateral(self, parent: tk.Widget, item_id: str, label_text: str) -> tk.Button:
        is_active = item_id == self._active
        icon = _ICONS.get(item_id, '·')
        bg = C.SIDE_3 if is_active else C.SIDE
        fg = '#ffffff' if is_active else C.SIDE_TEXT

        btn = tk.Button(
            parent,
            text=f'  {icon}  {label_text}',
            anchor='w',
            font=(C.FONT_BODY, 11),
            bg=bg, fg=fg,
            activebackground=C.SIDE_3,
            activeforeground='#dde6f1',
            bd=0, cursor='hand2', pady=8,
            command=lambda s=item_id: self._ao_navegar(s),
        )
        btn.pack(fill='x', pady=1)
        if not is_active:
            self._vincular_hover(btn)
        return btn

    def _vincular_hover(self, btn: tk.Button) -> None:
        btn.bind('<Enter>', lambda e: btn.config(bg=C.SIDE_3, fg='#dde6f1'))
        btn.bind('<Leave>', lambda e: btn.config(bg=C.SIDE,   fg=C.SIDE_TEXT))

    # API pública
    def definir_ativa(self, screen: str) -> None:
        for item_id, btn in self._btns.items():
            is_active = item_id == screen
            btn.config(
                bg=C.SIDE_3 if is_active else C.SIDE,
                fg='#ffffff' if is_active else C.SIDE_TEXT,
            )
            btn.unbind('<Enter>')
            btn.unbind('<Leave>')
            if not is_active:
                self._vincular_hover(btn)
        self._active = screen