"""Cabeçalho da área logada."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C
from app.models.user import User


class Topbar(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        user: User,
        ao_sair: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=C.SURFACE,
            highlightthickness=1,
            highlightbackground=C.HAIRLINE,
            **kwargs,
        )
        self._user = user
        self._ao_sair = ao_sair or (lambda: None)
        self._montar()

    def _montar(self) -> None:
        # Título da tela atual.
        left = tk.Frame(self, bg=C.SURFACE)
        left.pack(side='left', padx=C.CONTENT_PAD, pady=12)
        self._title_var = tk.StringVar(value='')
        self._sub_var   = tk.StringVar(value='')
        tk.Label(left, textvariable=self._title_var, bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 16, 'bold')).pack(anchor='w')
        tk.Label(left, textvariable=self._sub_var, bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10)).pack(anchor='w')

        # Usuário logado.
        right = tk.Frame(self, bg=C.SURFACE)
        right.pack(side='right', padx=C.CONTENT_PAD, pady=12)

        # Botão de sair fica na extrema direita. Empacotado antes do avatar
        # para reservar o canto sem depender da ordem visual.
        lb = tk.Button(right, text='⇥  Sair', bg=C.SURFACE, fg=C.INK_3,
                       bd=0, cursor='hand2', font=(C.FONT_BODY, 10, 'bold'),
                       activebackground=C.RED_50, activeforeground=C.RED,
                       command=self._ao_sair, padx=10, pady=4,
                       highlightthickness=1, highlightbackground=C.HAIRLINE)
        lb.pack(side='right', padx=(10, 0))
        lb.bind('<Enter>', lambda e: lb.config(bg=C.RED_50, fg=C.RED))
        lb.bind('<Leave>', lambda e: lb.config(bg=C.SURFACE, fg=C.INK_3))

        av = tk.Frame(right, bg=C.GREEN, width=30, height=30)
        av.pack_propagate(False)
        av.pack(side='right', padx=(6, 0))
        tk.Label(av, text=self._user.nome_usuarios[0], bg=C.GREEN, fg='white',
                 font=(C.FONT_BODY, 11, 'bold')).pack(expand=True)
        tk.Label(right, text=self._user.nome_usuarios.split()[0], bg=C.SURFACE, fg=C.INK_2,
                 font=(C.FONT_BODY, 11)).pack(side='right', padx=(0, 4))

    def definir_titulo(self, title: str, subtitle: str) -> None:
        self._title_var.set(title)
        self._sub_var.set(subtitle)