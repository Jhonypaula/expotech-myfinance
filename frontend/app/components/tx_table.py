"""Tabela reaproveitada para listar transações."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from app import config as C
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.utils import formatar_brl_com_sinal, formatar_data_curta


def _aplicar_estilo_treeview() -> None:
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Finance.Treeview',
                    background=C.SURFACE,
                    foreground=C.INK,
                    rowheight=36,
                    fieldbackground=C.SURFACE,
                    font=(C.FONT_BODY, 11),
                    borderwidth=0,
                    relief='flat')
    style.configure('Finance.Treeview.Heading',
                    background=C.BG_2,
                    foreground=C.INK_3,
                    font=(C.FONT_BODY, 10, 'bold'),
                    relief='flat',
                    borderwidth=0)
    style.map('Finance.Treeview',
              background=[('selected', C.GREEN_50)],
              foreground=[('selected', C.INK)])
    style.map('Finance.Treeview.Heading',
              background=[('active', C.HAIRLINE)])


class TxTable(tk.Frame):
    """Treeview com atalhos opcionais para editar e excluir."""

    COLS    = ('description', 'type', 'account', 'category', 'date', 'amount')
    HEADS   = ('Descrição', 'Tipo', 'Conta', 'Categoria', 'Data', 'Valor')
    WIDTHS  = (200, 80, 110, 110, 70, 110)
    ANCHORS = ('w', 'center', 'w', 'w', 'center', 'e')

    def __init__(
        self,
        parent: tk.Widget,
        ao_editar:   Optional[Callable[[Transaction], None]] = None,
        ao_excluir: Optional[Callable[[Transaction], None]] = None,
        **kwargs,
    ) -> None:
        kwargs.setdefault('bg', C.SURFACE)
        super().__init__(parent, **kwargs)
        self._ao_editar   = ao_editar
        self._ao_excluir = ao_excluir
        self._tx_map: dict[str, Transaction] = {}
        _aplicar_estilo_treeview()
        self._montar()

    def _montar(self) -> None:
        sb = ttk.Scrollbar(self, orient='vertical')
        sb.pack(side='right', fill='y')

        has_actions = bool(self._ao_editar or self._ao_excluir)
        cols = (*self.COLS, 'actions') if has_actions else self.COLS

        self._tree = ttk.Treeview(
            self, columns=cols, show='headings',
            style='Finance.Treeview',
            yscrollcommand=sb.set,
            selectmode='browse',
        )
        sb.config(command=self._tree.yview)

        for col, head, width, anchor in zip(self.COLS, self.HEADS, self.WIDTHS, self.ANCHORS):
            self._tree.heading(col, text=head)
            self._tree.column(col, width=width, anchor=anchor,
                              stretch=(col == 'description'))

        if has_actions:
            self._tree.heading('actions', text='Ações')
            self._tree.column('actions', width=80, anchor='center', stretch=False)

        self._tree.tag_configure('even', background=C.SURFACE)
        self._tree.tag_configure('odd',  background=C.SURFACE_2)
        self._tree.tag_configure('pos',  foreground=C.GREEN_700)
        self._tree.tag_configure('neg',  foreground=C.RED)

        self._tree.pack(fill='both', expand=True)

        if has_actions:
            self._tree.bind('<Double-1>', self._ao_clique_duplo)
            self._tree.bind('<Delete>',   self._ao_tecla_delete)

    def load(
        self,
        transactions: list[Transaction],
        accounts: list[Account],
        categories: list[Category],
    ) -> None:
        """Atualiza as linhas e traduz ids de conta/categoria para nomes."""
        self._tree.delete(*self._tree.get_children())
        self._tx_map.clear()

        acct_map = {a.id_contas: a.nome_contas for a in accounts}
        cat_map  = {c.id_categorias: c.nome_categorias for c in categories}

        for i, tx in enumerate(transactions):
            acct_name = acct_map.get(tx.conta_id, '—')
            cat_name  = cat_map.get(tx.categoria_id, '—') if tx.categoria_id else '—'
            kind      = 'Entrada' if tx.tipo_transacoes == 'entrada' else 'Saída'
            signed    = formatar_brl_com_sinal(
                tx.valor_transacoes if tx.tipo_transacoes == 'entrada' else -tx.valor_transacoes)

            row_tag = 'even' if i % 2 == 0 else 'odd'
            val_tag = 'pos'  if tx.tipo_transacoes == 'entrada' else 'neg'

            values = (tx.descricao_transacoes, kind, acct_name, cat_name,
                      formatar_data_curta(tx.data_transacao), signed)
            if self._ao_editar or self._ao_excluir:
                values = (*values, '✎  🗑')

            iid = self._tree.insert('', 'end', values=values, tags=(row_tag, val_tag))
            self._tx_map[iid] = tx

    def _transacao_selecionada(self) -> Optional[Transaction]:
        sel = self._tree.selection()
        return self._tx_map.get(sel[0]) if sel else None

    def _ao_clique_duplo(self, _event) -> None:
        tx = self._transacao_selecionada()
        if tx and self._ao_editar:
            self._ao_editar(tx)

    def _ao_tecla_delete(self, _event) -> None:
        tx = self._transacao_selecionada()
        if tx and self._ao_excluir:
            self._ao_excluir(tx)