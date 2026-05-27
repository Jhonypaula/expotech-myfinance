"""Tela de entrada do usuário."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C
from app.components.widgets import entry, button
from app.state.store import AppStore


class LoginPage(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        store: AppStore,
        ao_logar: Callable[[], None],
        ir_cadastro: Callable[[], None],
        flash: Callable[[str, str], None],
        ir_reset_senha: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=C.BG, **kwargs)
        self._store = store
        self._ao_logar = ao_logar
        self._ir_cadastro = ir_cadastro
        self._flash = flash
        self._ir_reset_senha = ir_reset_senha or (lambda: None)
        self._montar()

    def _montar(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Lado esquerdo, mais institucional.
        left = tk.Frame(self, bg=C.SIDE)
        left.grid(row=0, column=0, sticky='nsew')
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        # Marca
        top = tk.Frame(left, bg=C.SIDE)
        top.grid(row=0, column=0, sticky='ew', padx=40, pady=(50, 0))
        logo = tk.Frame(top, bg=C.GREEN, width=42, height=42)
        logo.pack_propagate(False)
        logo.pack(side='left')
        tk.Label(logo, text='M', bg=C.GREEN, fg='white',
                 font=(C.FONT_DISPLAY, 18, 'bold')).pack(expand=True)
        txt = tk.Frame(top, bg=C.SIDE)
        txt.pack(side='left', padx=(12, 0))
        tk.Label(txt, text='MyFinance', bg=C.SIDE, fg='white',
                 font=(C.FONT_DISPLAY, 16, 'bold')).pack(anchor='w')
        tk.Label(txt, text='GESTOR FINANCEIRO', bg=C.SIDE, fg=C.SIDE_TEXT_2,
                 font=(C.FONT_BODY, 9)).pack(anchor='w')

        # Chamada principal.
        hero = tk.Frame(left, bg=C.SIDE)
        hero.grid(row=1, column=0, sticky='nsew', padx=40)
        hero.rowconfigure(0, weight=1)
        inner = tk.Frame(hero, bg=C.SIDE)
        inner.grid(row=0, column=0, sticky='ew')

        tk.Label(inner, text='Controle simples.\nDecisoes melhores.',
                 bg=C.SIDE, fg='white', font=(C.FONT_DISPLAY, 22, 'bold'),
                 justify='left').pack(anchor='w', pady=(0, 16))
        tk.Label(inner,
                 text='O dinheiro fica mais leve quando voce\nenxerga ele por inteiro. Acompanhe\nentradas, saidas e contas em uma unica tela.',
                 bg=C.SIDE, fg=C.SIDE_TEXT, font=(C.FONT_BODY, 11),
                 justify='left').pack(anchor='w', pady=(0, 32))

        # Números decorativos para dar cara de produto.
        stats = tk.Frame(inner, bg=C.SIDE)
        stats.pack(anchor='w')
        for val, lbl in [('+12k', 'Usuarios'), ('R$ 4M', 'Movimentados'), ('4.9*', 'Avaliacao')]:
            s = tk.Frame(stats, bg=C.SIDE_2, padx=14, pady=10)
            s.pack(side='left', padx=(0, 8))
            tk.Label(s, text=val, bg=C.SIDE_2, fg=C.GREEN,
                     font=(C.FONT_DISPLAY, 14, 'bold')).pack()
            tk.Label(s, text=lbl, bg=C.SIDE_2, fg=C.SIDE_TEXT,
                     font=(C.FONT_BODY, 9)).pack()

        # Lado direito, formulário de login.
        right = tk.Frame(self, bg=C.SURFACE)
        right.grid(row=0, column=1, sticky='nsew')
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        form_wrap = tk.Frame(right, bg=C.SURFACE)
        form_wrap.grid(row=0, column=0)

        tk.Label(form_wrap, text='Bem-vindo de volta', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 20, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(form_wrap, text='Entre com sua conta para continuar gerenciando suas financas.',
                 bg=C.SURFACE, fg=C.INK_3, font=(C.FONT_BODY, 11), wraplength=340).pack(anchor='w', pady=(0, 24))

        # E-mail
        tk.Label(form_wrap, text='E-mail', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._email_var = tk.StringVar()
        entry(form_wrap, textvariable=self._email_var, width=38).pack(fill='x', ipady=6, pady=(0, 12))

        # Senha com botão para alternar visibilidade.
        tk.Label(form_wrap, text='Senha', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._pw_var = tk.StringVar()
        pw_row = tk.Frame(form_wrap, bg=C.SURFACE,
                          highlightthickness=1, highlightbackground=C.HAIRLINE)
        pw_row.pack(fill='x', pady=(0, 6))
        self._pw_entry = entry(pw_row, textvariable=self._pw_var, show='*',
                               highlightthickness=0)
        self._pw_entry.pack(side='left', fill='x', expand=True, ipady=6)
        self._show_pw = False
        # Ícone Unicode de olho aberto/fechado — disponível em todas as plataformas.
        self._eye_btn = tk.Button(
            pw_row, text='👁', bg=C.SURFACE, fg=C.INK_3, bd=0,
            cursor='hand2', font=(C.FONT_BODY, 11), padx=10, pady=0,
            relief='flat', activebackground=C.BG_2,
            command=self._alternar_senha,
        )
        self._eye_btn.pack(side='right', fill='y', padx=(0, 2))

        # Link que abre o fluxo de recuperação de senha.
        forgot_lbl = tk.Label(form_wrap, text='Esqueci minha senha', bg=C.SURFACE, fg=C.BLUE,
                              font=(C.FONT_BODY, 9), cursor='hand2')
        forgot_lbl.pack(anchor='e', pady=(0, 18))
        forgot_lbl.bind('<Button-1>', lambda e: self._ir_reset_senha())

        # Só aparece quando a validação falha.
        self._err_var = tk.StringVar(value='')
        self._err_lbl = tk.Label(form_wrap, textvariable=self._err_var, bg=C.RED_50,
                                 fg=C.RED, font=(C.FONT_BODY, 10), padx=8, pady=4,
                                 wraplength=340, justify='left')

        # Envio
        button(form_wrap, 'Entrar', command=self._enviar,
               variant='primary', size='lg').pack(fill='x', pady=(0, 16))

        # Alterna para cadastro.
        foot = tk.Frame(form_wrap, bg=C.SURFACE)
        foot.pack()
        tk.Label(foot, text='Nao tem conta?', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10)).pack(side='left')
        tk.Label(foot, text=' Cadastre-se', bg=C.SURFACE, fg=C.GREEN,
                 font=(C.FONT_BODY, 10, 'bold'), cursor='hand2').pack(side='left')
        foot.winfo_children()[-1].bind('<Button-1>', lambda e: self._ir_cadastro())

    def _alternar_senha(self) -> None:
        self._show_pw = not self._show_pw
        self._pw_entry.configure(show='' if self._show_pw else '*')
        # Alterna entre olho aberto e olho riscado para feedback visual claro.
        self._eye_btn.configure(text='🙈' if self._show_pw else '👁')

    def _enviar(self) -> None:
        from app.services import backend

        email = self._email_var.get().strip()
        senha = self._pw_var.get()

        if not email:
            self._exibir_erro('Informe o e-mail')
            return
        if not senha:
            self._exibir_erro('Informe a senha')
            return

        user, msg = backend.login(email, senha)
        if user is None:
            self._exibir_erro(msg or 'E-mail ou senha invalidos')
            return

        self._err_lbl.pack_forget()

        # Carrega a sessão antes de trocar para o dashboard.
        bootstrap_err = self._store.inicializar(user)
        if bootstrap_err:
            # Login válido: avisa, mas deixa o usuário entrar.
            self._flash('warning', f'Login feito, mas houve um aviso: {bootstrap_err}')

        self._pw_var.set('')
        self._ao_logar()

    def _exibir_erro(self, msg: str) -> None:
        self._err_var.set(f'!  {msg}')
        self._err_lbl.pack(fill='x', pady=(0, 10))