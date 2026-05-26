"""Tela de criação de conta."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C
from app.components.widgets import entry, button
from app.state.store import AppStore


class CadastroPage(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        store: AppStore,
        ao_cadastrar: Callable[[], None],
        ir_login: Callable[[], None],
        flash: Callable[[str, str], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=C.BG, **kwargs)
        self._store = store
        self._ao_cadastrar = ao_cadastrar
        self._ir_login = ir_login
        self._flash = flash
        self._montar()

    def _montar(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Lado esquerdo, mesma linguagem visual do login.
        left = tk.Frame(self, bg=C.SIDE)
        left.grid(row=0, column=0, sticky='nsew')
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        top = tk.Frame(left, bg=C.SIDE)
        top.grid(row=0, column=0, sticky='ew', padx=40, pady=(50, 0))
        logo = tk.Frame(top, bg=C.GREEN, width=42, height=42)
        logo.pack_propagate(False)
        logo.pack(side='left')
        tk.Label(logo, text='M', bg=C.GREEN, fg='white',
                 font=(C.FONT_DISPLAY, 18, 'bold')).pack(expand=True)
        txt_f = tk.Frame(top, bg=C.SIDE)
        txt_f.pack(side='left', padx=(12, 0))
        tk.Label(txt_f, text='MyFinance', bg=C.SIDE, fg='white',
                 font=(C.FONT_DISPLAY, 16, 'bold')).pack(anchor='w')
        tk.Label(txt_f, text='GESTOR FINANCEIRO', bg=C.SIDE, fg=C.SIDE_TEXT_2,
                 font=(C.FONT_BODY, 9)).pack(anchor='w')

        hero = tk.Frame(left, bg=C.SIDE)
        hero.grid(row=1, column=0, sticky='nsew', padx=40)
        hero.rowconfigure(0, weight=1)
        inner = tk.Frame(hero, bg=C.SIDE)
        inner.grid(row=0, column=0, sticky='ew')

        tk.Label(inner, text='Comece gratis.\nSem cartao de credito.',
                 bg=C.SIDE, fg='white', font=(C.FONT_DISPLAY, 22, 'bold'),
                 justify='left').pack(anchor='w', pady=(0, 16))
        tk.Label(inner,
                 text='Crie sua conta em segundos e comece\na organizar suas financas hoje mesmo.',
                 bg=C.SIDE, fg=C.SIDE_TEXT, font=(C.FONT_BODY, 11),
                 justify='left').pack(anchor='w')

        # Lado direito, formulário de cadastro.
        right = tk.Frame(self, bg=C.SURFACE)
        right.grid(row=0, column=1, sticky='nsew')
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        form_wrap = tk.Frame(right, bg=C.SURFACE)
        form_wrap.grid(row=0, column=0)

        tk.Label(form_wrap, text='Crie sua conta', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 20, 'bold')).pack(anchor='w', pady=(0, 6))
        tk.Label(form_wrap, text='Comece gratis. Sem cartao de credito.',
                 bg=C.SURFACE, fg=C.INK_3, font=(C.FONT_BODY, 11)).pack(anchor='w', pady=(0, 24))

        # Nome completo
        tk.Label(form_wrap, text='Nome completo *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._name_var = tk.StringVar()
        entry(form_wrap, textvariable=self._name_var, width=38).pack(fill='x', ipady=6, pady=(0, 10))

        # E-mail
        tk.Label(form_wrap, text='E-mail *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._email_var = tk.StringVar()
        entry(form_wrap, textvariable=self._email_var).pack(fill='x', ipady=6, pady=(0, 10))

        # Senha com uma noção simples de força.
        tk.Label(form_wrap, text='Senha *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._pw_var = tk.StringVar()
        self._pw_var.trace_add('write', self._atualizar_forca)
        entry(form_wrap, textvariable=self._pw_var, show='*').pack(fill='x', ipady=6, pady=(0, 4))

        # Barrinhas do indicador de força.
        bars_frame = tk.Frame(form_wrap, bg=C.SURFACE)
        bars_frame.pack(fill='x', pady=(0, 2))
        self._bars: list[tk.Frame] = []
        for _ in range(4):
            b = tk.Frame(bars_frame, bg=C.HAIRLINE, height=4, width=60)
            b.pack(side='left', padx=2)
            self._bars.append(b)
        self._strength_lbl = tk.Label(form_wrap, text='', bg=C.SURFACE, fg=C.INK_3,
                                      font=(C.FONT_BODY, 9))
        self._strength_lbl.pack(anchor='w', pady=(0, 8))

        # Confirmação de senha.
        tk.Label(form_wrap, text='Confirmar senha *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._pw2_var = tk.StringVar()
        self._pw2_var.trace_add('write', self._verificar_match)
        self._pw2_entry = entry(form_wrap, textvariable=self._pw2_var, show='*')
        self._pw2_entry.pack(fill='x', ipady=6, pady=(0, 4))
        self._mismatch_lbl = tk.Label(form_wrap, text='!  As senhas nao coincidem',
                                      bg=C.RED_50, fg=C.RED, font=(C.FONT_BODY, 9), padx=6, pady=3)

        # Mensagens vindas da validação local ou do backend.
        self._err_var = tk.StringVar(value='')
        self._err_lbl = tk.Label(form_wrap, textvariable=self._err_var, bg=C.RED_50,
                                 fg=C.RED, font=(C.FONT_BODY, 10), padx=8, pady=4,
                                 wraplength=340, justify='left')

        # Envio
        button(form_wrap, 'Criar conta', command=self._enviar,
               variant='primary', size='lg').pack(fill='x', pady=(12, 12))

        # Volta para o login.
        foot = tk.Frame(form_wrap, bg=C.SURFACE)
        foot.pack()
        tk.Label(foot, text='Ja tem conta?', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10)).pack(side='left')
        link = tk.Label(foot, text=' Entrar', bg=C.SURFACE, fg=C.GREEN,
                        font=(C.FONT_BODY, 10, 'bold'), cursor='hand2')
        link.pack(side='left')
        link.bind('<Button-1>', lambda e: self._ir_login())

    def _atualizar_forca(self, *_) -> None:
        pw = self._pw_var.get()
        score = 0
        if len(pw) >= 8:              score += 1
        if pw and pw != pw.lower():   score += 1
        if any(c.isdigit() for c in pw): score += 1
        if any(not c.isalnum() for c in pw): score += 1

        colors = ['', C.RED, C.AMBER, C.GREEN, C.GREEN]
        labels = ['', 'Fraca', 'Media', 'Forte', 'Forte']
        for i, bar in enumerate(self._bars):
            bar.config(bg=colors[score] if i < score else C.HAIRLINE)
        if pw:
            self._strength_lbl.config(text=f'Senha {labels[score]}', fg=colors[score])
        else:
            self._strength_lbl.config(text='')

    def _verificar_match(self, *_) -> None:
        pw2 = self._pw2_var.get()
        if pw2 and pw2 != self._pw_var.get():
            self._pw2_entry.config(highlightbackground=C.RED)
            self._mismatch_lbl.pack(fill='x', pady=(0, 6))
        else:
            self._pw2_entry.config(highlightbackground=C.HAIRLINE)
            self._mismatch_lbl.pack_forget()

    def _enviar(self) -> None:
        from app.services import backend

        nome = self._name_var.get().strip()
        email = self._email_var.get().strip()
        senha = self._pw_var.get()
        senha2 = self._pw2_var.get()

        if not nome:
            self._exibir_erro('Informe seu nome')
            return
        if not email:
            self._exibir_erro('Informe o e-mail')
            return
        if senha != senha2:
            self._exibir_erro('As senhas nao coincidem')
            return

        user, msg = backend.cadastrar(nome, email, senha)
        if user is None:
            self._exibir_erro(msg or 'Nao foi possivel cadastrar')
            return

        self._err_lbl.pack_forget()
        bootstrap_err = self._store.inicializar(user)
        if bootstrap_err:
            self._flash('warning', f'Cadastro feito, mas houve um aviso: {bootstrap_err}')

        # Evita deixar senha preenchida depois que o usuário entrou.
        self._pw_var.set('')
        self._pw2_var.set('')
        self._ao_cadastrar()

    def _exibir_erro(self, msg: str) -> None:
        self._err_var.set(f'!  {msg}')
        self._err_lbl.pack(fill='x', pady=(0, 10))