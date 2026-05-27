"""Janelas modais usadas no fluxo de contas e transações."""
from __future__ import annotations
import tkinter as tk
from typing import Callable, Optional
from datetime import datetime
from app import config as C
from app.components.widgets import entry, button, field_label, combobox
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.utils import formatar_brl


_CONTA_TIPOS = ['corrente', 'poupanca', 'carteira']
_CONTA_TIPO_LABEL = {
    'corrente': 'Corrente',
    'poupanca': 'Poupança',
    'carteira': 'Carteira',
}


class BaseModal(tk.Toplevel):
    """Toplevel centralizado, bloqueando interação fora dele."""

    def __init__(self, parent: tk.Widget, title: str,
                 width: int = 480, height: int = 500) -> None:
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=C.SURFACE)
        self.transient(parent)
        self.grab_set()
        self._centralizar(parent, width, height)
        self.bind('<Escape>', lambda e: self.destroy())
        self._montar_chrome(title)

    def _centralizar(self, parent: tk.Widget, w: int, h: int) -> None:
        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width()  - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f'{w}x{h}+{px}+{py}')

    def _montar_chrome(self, title: str) -> None:
        hdr = tk.Frame(self, bg=C.SURFACE,
                       highlightthickness=1, highlightbackground=C.HAIRLINE)
        hdr.pack(fill='x')
        tk.Label(hdr, text=title, bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(side='left', padx=16, pady=12)
        close = tk.Button(hdr, text='✕', bg=C.SURFACE, fg=C.INK_3,
                          bd=0, cursor='hand2', font=(C.FONT_BODY, 12),
                          activebackground=C.BG_2, command=self.destroy, padx=8, pady=4)
        close.pack(side='right', padx=8, pady=8)

        self.body_frame   = tk.Frame(self, bg=C.SURFACE)
        self.body_frame.pack(fill='both', expand=True, padx=20, pady=12)

        # Faixa de erro no topo do corpo: só aparece quando a validação falha.
        self._err_var = tk.StringVar(value='')
        self._err_lbl = tk.Label(
            self.body_frame, textvariable=self._err_var,
            bg=C.RED_50, fg=C.RED, font=(C.FONT_BODY, 10),
            padx=10, pady=6, wraplength=420, justify='left', anchor='w',
        )

        self.footer_frame = tk.Frame(self, bg=C.SURFACE,
                                     highlightthickness=1, highlightbackground=C.HAIRLINE)
        self.footer_frame.pack(fill='x', side='bottom')

    def mostrar_erro(self, msg: str) -> None:
        """Mostra uma faixa vermelha de erro no topo do corpo do modal."""
        self._err_var.set(f'!  {msg}')
        # `pack` na primeira posição garante que o aviso fica acima do formulário.
        self._err_lbl.pack(fill='x', pady=(0, 10), before=self._primeiro_widget_corpo())

    def limpar_erro(self) -> None:
        self._err_lbl.pack_forget()

    def _primeiro_widget_corpo(self) -> tk.Widget:
        """Devolve o primeiro filho do corpo para usar como âncora do erro."""
        filhos = [w for w in self.body_frame.winfo_children() if w is not self._err_lbl]
        return filhos[0] if filhos else self.body_frame


class TxModal(BaseModal):
    """Formulário de criação/edição de transação."""

    def __init__(
        self,
        parent: tk.Widget,
        accounts: list[Account],
        categories: list[Category],
        ao_salvar: Callable[[Transaction], None],
        tx: Optional[Transaction] = None,
        ao_erro: Optional[Callable[[str], None]] = None,
    ) -> None:
        is_edit = tx is not None
        super().__init__(
            parent,
            'Editar Transação' if is_edit else 'Nova Transação',
            width=500, height=520,
        )
        self._accounts   = accounts
        self._categories = categories
        self._ao_salvar    = ao_salvar
        self._ao_erro    = ao_erro or (lambda _msg: None)
        self._tx         = tx
        self._montar_formulario(tx)

    def _montar_formulario(self, tx: Optional[Transaction]) -> None:
        bg = C.SURFACE
        bf = self.body_frame

        # Tipo da movimentação.
        self._type_var = tk.StringVar(
            value=tx.tipo_transacoes if tx else 'saida')

        toggle = tk.Frame(bf, bg=bg)
        toggle.pack(fill='x', pady=(0, 14))
        self._btn_entrada = self._botao_tipo(toggle, 'entrada', 'Entrada ↓')
        self._btn_saida   = self._botao_tipo(toggle, 'saida',   'Saída ↑')
        self._btn_entrada.pack(side='left', expand=True, fill='x', padx=(0, 4))
        self._btn_saida.pack(  side='left', expand=True, fill='x', padx=(4, 0))
        self._atualizar_toggle()

        # Valor
        field_label(bf, 'Valor *', bg)
        amount_row = tk.Frame(bf, bg=bg,
                              highlightthickness=1, highlightbackground=C.HAIRLINE)
        amount_row.pack(fill='x', pady=(0, 10))
        tk.Label(amount_row, text='R$', bg=C.BG_2, fg=C.INK_3,
                 font=(C.FONT_BODY, 11), padx=10, pady=7).pack(side='left')
        self._amount_var = tk.StringVar(
            value=str(tx.valor_transacoes) if tx else '')
        tk.Entry(amount_row, textvariable=self._amount_var,
                 bg=C.SURFACE, fg=C.INK, insertbackground=C.INK,
                 relief='flat', bd=4, font=(C.FONT_MONO, 12)).pack(
                     side='left', fill='x', expand=True)

        # Descrição
        field_label(bf, 'Descrição *', bg)
        self._desc_var = tk.StringVar(
            value=tx.descricao_transacoes if tx else '')
        entry(bf, textvariable=self._desc_var).pack(fill='x', pady=(0, 10), ipady=5)

        # O backend ainda ignora esta data ao criar transação, mas ela segue útil na edição.
        field_label(bf, 'Data e hora (data_transacao)', bg)
        self._date_var = tk.StringVar(
            value=tx.data_transacao if tx else datetime.now().strftime('%Y-%m-%dT%H:%M'))
        entry(bf, textvariable=self._date_var).pack(fill='x', pady=(0, 10), ipady=5)

        # Conta e categoria ficam juntas para encurtar o modal.
        two = tk.Frame(bf, bg=bg)
        two.pack(fill='x', pady=(0, 4))
        two.columnconfigure(0, weight=1)
        two.columnconfigure(1, weight=1)

        # Conta gravada em conta_id.
        acct_col = tk.Frame(two, bg=bg)
        acct_col.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        field_label(acct_col, 'Conta * (conta_id)', bg)
        acct_labels = [f'{a.nome_contas} — {formatar_brl(a.saldo_contas)}' for a in self._accounts]
        self._acct_var = tk.StringVar()
        self._acct_cb  = combobox(acct_col, values=acct_labels,
                                  textvariable=self._acct_var)
        self._acct_cb.pack(fill='x', ipady=3)
        if tx:
            idx = next((i for i, a in enumerate(self._accounts)
                        if a.id_contas == tx.conta_id), 0)
            self._acct_cb.current(idx)
        elif self._accounts:
            self._acct_cb.current(0)

        # Categoria gravada em categoria_id.
        cat_col = tk.Frame(two, bg=bg)
        cat_col.grid(row=0, column=1, sticky='ew', padx=(6, 0))
        field_label(cat_col, 'Categoria (categoria_id)', bg)
        cat_labels = ['— Nenhuma —'] + [c.nome_categorias for c in self._categories]
        self._cat_var = tk.StringVar()
        self._cat_cb  = combobox(cat_col, values=cat_labels,
                                 textvariable=self._cat_var)
        self._cat_cb.pack(fill='x', ipady=3)
        if tx and tx.categoria_id is not None:
            idx = next((i for i, c in enumerate(self._categories)
                        if c.id_categorias == tx.categoria_id), -1)
            self._cat_cb.current(idx + 1)   # índice 0 fica reservado para "Nenhuma"
        else:
            self._cat_cb.current(0)

        # Ações
        button(self.footer_frame, 'Cancelar', command=self.destroy,
               variant='ghost').pack(side='right', padx=(6, 16), pady=10)
        button(self.footer_frame, 'Salvar', command=self._salvar,
               variant='primary').pack(side='right', pady=10)

    # Auxiliares
    def _botao_tipo(self, parent: tk.Widget, kind: str, text: str) -> tk.Button:
        return tk.Button(parent, text=text, font=(C.FONT_BODY, 11),
                         bd=0, cursor='hand2', relief='flat', pady=8,
                         command=lambda: self._definir_tipo(kind))

    def _definir_tipo(self, kind: str) -> None:
        self._type_var.set(kind)
        self._atualizar_toggle()

    def _sinalizar_erro(self, msg: str) -> None:
        self.mostrar_erro(msg)
        self._ao_erro(msg)

    def _atualizar_toggle(self) -> None:
        if self._type_var.get() == 'entrada':
            self._btn_entrada.config(bg=C.GREEN_50,  fg=C.GREEN_700,
                                     activebackground=C.GREEN_100,
                                     activeforeground=C.GREEN_700)
            self._btn_saida.config(  bg=C.BG_2,      fg=C.INK_3,
                                     activebackground=C.HAIRLINE,
                                     activeforeground=C.INK_2)
        else:
            self._btn_saida.config(  bg=C.RED_50,    fg=C.RED,
                                     activebackground='#fbd9d4',
                                     activeforeground=C.RED)
            self._btn_entrada.config(bg=C.BG_2,      fg=C.INK_3,
                                     activebackground=C.HAIRLINE,
                                     activeforeground=C.INK_2)

    def _salvar(self) -> None:
        raw_amount = self._amount_var.get().strip()
        if not raw_amount:
            self._sinalizar_erro('O valor deve ser um número válido')
            return
        try:
            amount = float(raw_amount.replace(',', '.'))
        except ValueError:
            self._sinalizar_erro('O valor deve ser um número válido')
            return
        if amount <= 0:
            self._sinalizar_erro('O valor deve ser um número positivo')
            return

        desc = self._desc_var.get().strip()
        if not desc:
            self._sinalizar_erro('Descricao obrigatoria!')
            return
        if len(desc) > 15:
            self._sinalizar_erro('Descricao muito longa! Maximo 15')
            return

        # Resolve a conta escolhida no combobox.
        acct_idx = self._acct_cb.current()
        if acct_idx < 0 or acct_idx >= len(self._accounts):
            self._sinalizar_erro('Selecione uma conta para a transacao')
            return
        conta_id = self._accounts[acct_idx].id_contas

        # No combobox, 0 é "sem categoria"; as categorias reais começam em 1.
        cat_idx = self._cat_cb.current()
        categoria_id: Optional[int] = None
        if cat_idx > 0:
            categoria_id = self._categories[cat_idx - 1].id_categorias

        # id zero é nosso rascunho local; o banco gera o id definitivo.
        # Ao criar, data_transacao volta do backend com CURRENT_TIMESTAMP.
        draft = Transaction(
            id_transacoes        = self._tx.id_transacoes if self._tx else 0,
            conta_id             = conta_id,
            categoria_id         = categoria_id,
            tipo_transacoes      = self._type_var.get(),
            valor_transacoes     = amount,
            descricao_transacoes = desc,
            data_transacao       = self._date_var.get(),
        )
        self._ao_salvar(draft)
        self.destroy()


class ContaModal(BaseModal):
    """Formulário de edição de conta (apenas nome e tipo são editáveis)."""

    def __init__(
        self,
        parent: tk.Widget,
        ao_salvar: Callable[[str, str], None],
        conta: Optional[Account] = None,
        ao_erro: Optional[Callable[[str], None]] = None,
    ) -> None:
        is_edit = conta is not None
        super().__init__(
            parent,
            'Editar Conta' if is_edit else 'Nova Conta',
            width=460, height=380,
        )
        self._conta = conta
        self._ao_salvar = ao_salvar
        self._ao_erro = ao_erro or (lambda _msg: None)
        self._montar_formulario()

    def _montar_formulario(self) -> None:
        bg = C.SURFACE
        bf = self.body_frame

        # Nome da conta.
        field_label(bf, 'Nome da conta *', bg)
        self._name_var = tk.StringVar(
            value=self._conta.nome_contas if self._conta else '')
        entry(bf, textvariable=self._name_var).pack(fill='x', ipady=6, pady=(0, 12))

        # Tipo da conta (ENUM do backend).
        field_label(bf, 'Tipo da conta *', bg)
        labels = [_CONTA_TIPO_LABEL[t] for t in _CONTA_TIPOS]
        self._tipo_var = tk.StringVar()
        self._tipo_cb = combobox(bf, values=labels, textvariable=self._tipo_var)
        self._tipo_cb.pack(fill='x', ipady=3, pady=(0, 12))
        if self._conta and self._conta.tipo_contas in _CONTA_TIPOS:
            self._tipo_cb.current(_CONTA_TIPOS.index(self._conta.tipo_contas))
        else:
            self._tipo_cb.current(0)

        # Aviso sobre saldo: o backend não permite editar.
        if self._conta is not None:
            tk.Label(
                bf,
                text=f'Saldo atual: {formatar_brl(self._conta.saldo_contas)}\n'
                     'O saldo é ajustado automaticamente pelas transações.',
                bg=bg, fg=C.INK_4, font=(C.FONT_BODY, 9), justify='left',
            ).pack(anchor='w', pady=(0, 4))

        # Ações
        button(self.footer_frame, 'Cancelar', command=self.destroy,
               variant='ghost').pack(side='right', padx=(6, 16), pady=10)
        button(self.footer_frame, 'Salvar', command=self._salvar,
               variant='primary').pack(side='right', pady=10)

    def _sinalizar_erro(self, msg: str) -> None:
        self.mostrar_erro(msg)
        self._ao_erro(msg)

    def _salvar(self) -> None:
        nome = self._name_var.get().strip()
        if not nome:
            self._sinalizar_erro('Nome da conta obrigatorio!')
            return

        idx = self._tipo_cb.current()
        if idx < 0 or idx >= len(_CONTA_TIPOS):
            self._sinalizar_erro('Tipo de conta invalido!')
            return
        tipo = _CONTA_TIPOS[idx]

        self._ao_salvar(nome, tipo)
        self.destroy()