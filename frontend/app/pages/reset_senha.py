"""Tela de recuperação de senha em duas etapas."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C
from app.components.widgets import entry, button


class ResetSenhaPage(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        ir_login: Callable[[], None],
        flash: Callable[[str, str], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=C.BG, **kwargs)
        self._ir_login = ir_login
        self._flash = flash
        self._etapa = 1
        self._montar()

    def _montar(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Lado esquerdo: mesma linguagem visual das outras telas de auth.
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

        tk.Label(inner, text='Esqueceu a senha?\nA gente resolve.',
                 bg=C.SIDE, fg='white', font=(C.FONT_DISPLAY, 22, 'bold'),
                 justify='left').pack(anchor='w', pady=(0, 16))
        tk.Label(inner,
                 text='Enviamos um codigo temporario para o seu\ne-mail. Use ele aqui para definir uma nova\nsenha em segundos.',
                 bg=C.SIDE, fg=C.SIDE_TEXT, font=(C.FONT_BODY, 11),
                 justify='left').pack(anchor='w')

        # Lado direito: formulário cuja primeira ou segunda etapa fica visível.
        right = tk.Frame(self, bg=C.SURFACE)
        right.grid(row=0, column=1, sticky='nsew')
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        form_wrap = tk.Frame(right, bg=C.SURFACE)
        form_wrap.grid(row=0, column=0)
        self._form_wrap = form_wrap

        # Cabeçalho fica reaproveitado entre etapas.
        self._title_lbl = tk.Label(form_wrap, text='Recuperar senha', bg=C.SURFACE, fg=C.INK,
                                   font=(C.FONT_DISPLAY, 20, 'bold'))
        self._title_lbl.pack(anchor='w', pady=(0, 6))
        self._subtitle_lbl = tk.Label(
            form_wrap,
            text='Informe o e-mail cadastrado para receber o token de redefinicao.',
            bg=C.SURFACE, fg=C.INK_3, font=(C.FONT_BODY, 11), wraplength=340,
            justify='left',
        )
        self._subtitle_lbl.pack(anchor='w', pady=(0, 24))

        # Etapa 1 — pedir o token por e-mail.
        self._etapa1 = tk.Frame(form_wrap, bg=C.SURFACE)
        tk.Label(self._etapa1, text='E-mail *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._email_var = tk.StringVar()
        entry(self._etapa1, textvariable=self._email_var, width=38).pack(
            fill='x', ipady=6, pady=(0, 12))

        button(self._etapa1, 'Enviar token', command=self._solicitar_token,
               variant='primary', size='lg').pack(fill='x', pady=(4, 12))

        # Etapa 2 — token + nova senha.
        self._etapa2 = tk.Frame(form_wrap, bg=C.SURFACE)
        tk.Label(self._etapa2, text='Token recebido por e-mail *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._token_var = tk.StringVar()
        entry(self._etapa2, textvariable=self._token_var).pack(
            fill='x', ipady=6, pady=(0, 10))

        tk.Label(self._etapa2, text='Nova senha *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._pw_var = tk.StringVar()
        entry(self._etapa2, textvariable=self._pw_var, show='*').pack(
            fill='x', ipady=6, pady=(0, 10))

        tk.Label(self._etapa2, text='Confirmar nova senha *', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._pw2_var = tk.StringVar()
        entry(self._etapa2, textvariable=self._pw2_var, show='*').pack(
            fill='x', ipady=6, pady=(0, 12))

        button(self._etapa2, 'Redefinir senha', command=self._aplicar_nova_senha,
               variant='primary', size='lg').pack(fill='x', pady=(4, 12))

        # Faixa de erro inline; aparece quando a validação local ou do backend falha.
        self._err_var = tk.StringVar(value='')
        self._err_lbl = tk.Label(form_wrap, textvariable=self._err_var, bg=C.RED_50,
                                 fg=C.RED, font=(C.FONT_BODY, 10), padx=8, pady=4,
                                 wraplength=340, justify='left')

        # Volta para a tela de login.
        foot = tk.Frame(form_wrap, bg=C.SURFACE)
        foot.pack()
        tk.Label(foot, text='Lembrou da senha?', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 10)).pack(side='left')
        link = tk.Label(foot, text=' Voltar ao login', bg=C.SURFACE, fg=C.GREEN,
                        font=(C.FONT_BODY, 10, 'bold'), cursor='hand2')
        link.pack(side='left')
        link.bind('<Button-1>', lambda e: self._voltar_login())

        self._mostrar_etapa(1)

    def _mostrar_etapa(self, n: int) -> None:
        self._etapa = n
        self._etapa1.pack_forget()
        self._etapa2.pack_forget()
        if n == 1:
            self._title_lbl.config(text='Recuperar senha')
            self._subtitle_lbl.config(
                text='Informe o e-mail cadastrado para receber o token de redefinicao.')
            self._etapa1.pack(fill='x')
        else:
            self._title_lbl.config(text='Definir nova senha')
            self._subtitle_lbl.config(
                text='Cole o token enviado para o seu e-mail e escolha uma nova senha.')
            self._etapa2.pack(fill='x')

    def _solicitar_token(self) -> None:
        from app.services import backend

        email = self._email_var.get().strip()
        if not email:
            self._exibir_erro('Informe o e-mail')
            return

        ok, msg = backend.requisicao_alterar_senha(email)
        if not ok:
            self._exibir_erro(msg or 'Nao foi possivel enviar o e-mail')
            return

        # O backend sempre devolve True para nao revelar se o e-mail existe;
        # passamos a etapa 2 e deixamos o usuario validar o token recebido.
        self._err_lbl.pack_forget()
        self._flash('success', 'Token enviado. Verifique sua caixa de entrada.')
        self._mostrar_etapa(2)

    def _aplicar_nova_senha(self) -> None:
        from app.services import backend

        token = self._token_var.get().strip()
        senha = self._pw_var.get()
        senha2 = self._pw2_var.get()

        if not token:
            self._exibir_erro('Informe o token recebido por e-mail')
            return
        if not senha:
            self._exibir_erro('Informe a nova senha')
            return
        if senha != senha2:
            self._exibir_erro('As senhas nao coincidem')
            return

        ok, msg = backend.resetar_senha(token, senha)
        if not ok:
            self._exibir_erro(msg or 'Nao foi possivel redefinir a senha')
            return

        self._err_lbl.pack_forget()
        self._flash('success', 'Senha redefinida com sucesso. Faca login.')
        self._limpar()
        self._ir_login()

    def _exibir_erro(self, msg: str) -> None:
        self._err_var.set(f'!  {msg}')
        self._err_lbl.pack(fill='x', pady=(0, 10))

    def _voltar_login(self) -> None:
        self._limpar()
        self._ir_login()

    def _limpar(self) -> None:
        self._email_var.set('')
        self._token_var.set('')
        self._pw_var.set('')
        self._pw2_var.set('')
        self._err_lbl.pack_forget()
        self._mostrar_etapa(1)
