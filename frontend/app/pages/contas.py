"""Tela de contas bancárias."""
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from app import config as C
from app.pages.base import BasePage
from app.state.store import AppStore
from app.models.account import Account
from app.components.widgets import card, entry, button, field_label, scrollable_frame
from app.components.modal import ContaModal
from app.utils import formatar_brl

_TYPE_ICON  = {'corrente': '🏦', 'poupanca': '🐷', 'carteira': '👛'}
_TYPE_LABEL = {'corrente': 'Corrente', 'poupanca': 'Poupança', 'carteira': 'Carteira'}


class ContasPage(BasePage):
    def __init__(self, parent: tk.Widget, store: AppStore, flash, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._store    = store
        self._flash    = flash
        self._type_var = tk.StringVar(value='corrente')
        self._montar()
        store.inscrever(self._atualizar_lista)

    def _montar(self) -> None:
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        pad = C.CONTENT_PAD

        # Coluna da esquerda: nova conta.
        form_card = card(self)
        form_card.grid(row=0, column=0, sticky='ns', padx=(pad, 8), pady=pad)

        fi = tk.Frame(form_card, bg=C.SURFACE)
        fi.pack(fill='both', expand=True, padx=18, pady=16)

        tk.Label(fi, text='Nova Conta', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(anchor='w', pady=(0, 16))

        # Campo que vai para nome_contas.
        field_label(fi, 'Nome da conta (nome_contas) *')
        self._name_var = tk.StringVar()
        entry(fi, textvariable=self._name_var, width=28).pack(fill='x', ipady=6, pady=(0, 12))

        # Enum tipo_contas.
        field_label(fi, 'Tipo de conta (tipo_contas) *')
        type_row = tk.Frame(fi, bg=C.SURFACE)
        type_row.pack(fill='x', pady=(0, 12))
        self._type_btns: dict[str, tk.Button] = {}
        for t_id in ('corrente', 'poupanca', 'carteira'):
            b = tk.Button(
                type_row,
                text=f'{_TYPE_ICON[t_id]}  {_TYPE_LABEL[t_id]}',
                bg=C.BG_2, fg=C.INK_2, bd=0, cursor='hand2',
                font=(C.FONT_BODY, 10), padx=10, pady=8,
                command=lambda v=t_id: self._selecionar_tipo(v),
            )
            b.pack(side='left', padx=(0, 6))
            self._type_btns[t_id] = b
        self._selecionar_tipo('corrente')

        # Saldo inicial salvo em saldo_contas.
        field_label(fi, 'Saldo inicial (saldo_contas)')
        bal_row = tk.Frame(fi, bg=C.SURFACE,
                           highlightthickness=1, highlightbackground=C.HAIRLINE)
        bal_row.pack(fill='x', pady=(0, 16))
        tk.Label(bal_row, text='R$', bg=C.BG_2, fg=C.INK_3,
                 font=(C.FONT_BODY, 11), padx=8, pady=7).pack(side='left')
        self._bal_var = tk.StringVar(value='0')
        tk.Entry(bal_row, textvariable=self._bal_var,
                 bg=C.SURFACE, fg=C.INK, insertbackground=C.INK,
                 relief='flat', bd=4, font=(C.FONT_MONO, 12)).pack(
                     side='left', fill='x', expand=True)

        button(fi, '+ Criar Conta', command=self._enviar,
               variant='primary', size='lg').pack(fill='x', pady=(4, 0))

        # Faixa de erro inline para o formulário de criação.
        self._err_var = tk.StringVar(value='')
        self._err_lbl = tk.Label(fi, textvariable=self._err_var, bg=C.RED_50,
                                 fg=C.RED, font=(C.FONT_BODY, 10), padx=8, pady=4,
                                 wraplength=240, justify='left')

        # Coluna da direita: contas já cadastradas.
        right = tk.Frame(self, bg=C.BG)
        right.grid(row=0, column=1, sticky='nsew', padx=(0, pad), pady=pad)

        hdr = tk.Frame(right, bg=C.BG)
        hdr.pack(fill='x', pady=(0, 10))
        self._hdr_lbl = tk.Label(hdr, text='', bg=C.BG, fg=C.INK,
                                  font=(C.FONT_DISPLAY, 14, 'bold'))
        self._hdr_lbl.pack(anchor='w')
        self._sub_lbl = tk.Label(hdr, text='', bg=C.BG, fg=C.INK_3,
                                  font=(C.FONT_BODY, 10))
        self._sub_lbl.pack(anchor='w')

        _, self._cards_inner = scrollable_frame(right, bg=C.BG)
        self._atualizar_lista()

    def _selecionar_tipo(self, t: str) -> None:
        self._type_var.set(t)
        for t_id, btn in self._type_btns.items():
            btn.config(bg=C.GREEN_50 if t_id == t else C.BG_2,
                       fg=C.GREEN_700 if t_id == t else C.INK_2)

    def _enviar(self) -> None:
        name = self._name_var.get().strip()
        if not name:
            self._exibir_erro('Nome da conta obrigatorio!')
            return

        raw_balance = self._bal_var.get().strip()
        if not raw_balance:
            self._exibir_erro('Saldo inicial obrigatorio!')
            return
        try:
            balance = float(raw_balance.replace(',', '.'))
        except ValueError:
            self._exibir_erro('Saldo inicial deve ser um numero valido')
            return
        if balance < 0:
            self._exibir_erro('Saldo inicial nao pode ser negativo')
            return

        ok, msg = self._store.criar_conta(name, self._type_var.get(), balance)
        if not ok:
            self._exibir_erro(msg or 'Nao foi possivel criar a conta')
            return

        self._err_lbl.pack_forget()
        self._flash('success', f'Conta "{name}" criada com sucesso')
        self._name_var.set('')
        self._bal_var.set('0')
        self._selecionar_tipo('corrente')

    def _exibir_erro(self, msg: str) -> None:
        self._err_var.set(f'!  {msg}')
        self._err_lbl.pack(fill='x', pady=(8, 0))

    def _atualizar_lista(self) -> None:
        for w in self._cards_inner.winfo_children():
            w.destroy()

        accounts = self._store.accounts
        total    = sum(a.saldo_contas for a in accounts)
        self._hdr_lbl.config(text='Suas contas')
        self._sub_lbl.config(
            text=f'{len(accounts)} conta{"s" if len(accounts) != 1 else ""} · '
                 f'saldo total {formatar_brl(total)}')

        grid = tk.Frame(self._cards_inner, bg=C.BG)
        grid.pack(fill='x')
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        for i, a in enumerate(accounts):
            tx_count = sum(1 for t in self._store.transactions if t.conta_id == a.id_contas)
            ac = self._card_conta(grid, a, tx_count)
            ac.grid(row=i // 2, column=i % 2, sticky='ew',
                    padx=(0, 8) if i % 2 == 0 else 0, pady=(0, 8))

    def _card_conta(self, parent, a: Account, tx_count: int) -> tk.Frame:
        f = card(parent)
        inner = tk.Frame(f, bg=C.SURFACE)
        inner.pack(fill='both', expand=True, padx=16, pady=14)

        top = tk.Frame(inner, bg=C.SURFACE)
        top.pack(fill='x')

        icon_f = tk.Frame(top, bg=C.GREEN_50, width=40, height=40)
        icon_f.pack_propagate(False)
        icon_f.pack(side='left')
        tk.Label(icon_f, text=_TYPE_ICON.get(a.tipo_contas, '💳'),
                 bg=C.GREEN_50, font=(C.FONT_BODY, 16)).pack(expand=True)

        meta = tk.Frame(top, bg=C.SURFACE)
        meta.pack(side='left', padx=(10, 0), fill='x', expand=True)
        tk.Label(meta, text=a.nome_contas, bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_BODY, 12, 'bold')).pack(anchor='w')
        tk.Label(meta, text=_TYPE_LABEL.get(a.tipo_contas, ''), bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 9)).pack(anchor='w')

        del_btn = tk.Button(
            top, text='🗑', bg=C.SURFACE, fg=C.INK_4,
            bd=0, cursor='hand2', font=(C.FONT_BODY, 12),
            activebackground=C.RED_50, activeforeground=C.RED,
            command=lambda aid=a.id_contas, nm=a.nome_contas: self._excluir(aid, nm),
        )
        del_btn.pack(side='right', anchor='n')

        edit_btn = tk.Button(
            top, text='✎', bg=C.SURFACE, fg=C.INK_4,
            bd=0, cursor='hand2', font=(C.FONT_BODY, 12),
            activebackground=C.GREEN_50, activeforeground=C.GREEN_700,
            command=lambda conta=a: self._editar(conta),
        )
        edit_btn.pack(side='right', anchor='n', padx=(0, 4))

        bal_fg = C.GREEN_700 if a.saldo_contas >= 0 else C.RED
        tk.Label(inner, text=formatar_brl(a.saldo_contas), bg=C.SURFACE, fg=bal_fg,
                 font=(C.FONT_MONO, 17, 'bold')).pack(anchor='w', pady=(12, 4))

        info = tk.Frame(inner, bg=C.SURFACE)
        info.pack(fill='x')
        tk.Label(info, text=f'{tx_count} transações', bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 9)).pack(side='left')
        tk.Label(info, text=f'Criada em {a.data_criacao_contas}', bg=C.SURFACE,
                 fg=C.INK_4, font=(C.FONT_BODY, 9)).pack(side='right')
        return f

    def _editar(self, conta: Account) -> None:
        ContaModal(
            self,
            conta=conta,
            ao_salvar=lambda nome, tipo: self._aplicar_edicao(conta.id_contas, nome, tipo),
            ao_erro=lambda msg: self._flash('error', msg),
        )

    def _aplicar_edicao(self, id_contas: int, nome: str, tipo: str) -> None:
        ok, msg = self._store.editar_conta(id_contas, nome, tipo)
        if ok:
            self._flash('success', f'Conta "{nome}" atualizada')
        else:
            self._flash('error', msg or 'Nao foi possivel atualizar a conta')

    def _excluir(self, id_contas: int, name: str) -> None:
        if not messagebox.askyesno('Excluir conta', f'Excluir a conta "{name}"?\n\nEsta ação não pode ser desfeita.'):
            return
        ok, msg = self._store.excluir_conta(id_contas)
        if ok:
            self._flash('success', f'Conta "{name}" excluida')
        else:
            erro = msg or 'Não foi possível excluir a conta.'
            # Detecta mensagem de FK / transações vinculadas e exibe popup claro.
            if any(k in (msg or '').lower() for k in ('foreign', 'fk', 'transac', 'constraint', 'integrity')):
                messagebox.showerror(
                    'Conta com transações',
                    f'A conta "{name}" não pode ser excluída\n'
                    'porque possui transações vinculadas a ela.\n\n'
                    'Exclua ou mova as transações antes de remover a conta.',
                )
            else:
                messagebox.showerror('Erro ao excluir', erro)
            self._flash('error', erro)

    def ao_exibir(self) -> None:
        self._atualizar_lista()