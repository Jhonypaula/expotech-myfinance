"""Tela de transações."""
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox, ttk
from app import config as C
from app.pages.base import BasePage
from app.state.store import AppStore
from app.components.tx_table import TxTable
from app.components.modal import TxModal
from app.components.widgets import card, button, combobox, scrollable_frame


class TransacoesPage(BasePage):
    def __init__(self, parent: tk.Widget, store: AppStore, flash, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._store       = store
        self._flash       = flash
        self._filter_type = tk.StringVar(value='Todos')
        self._filter_acct = tk.StringVar(value='Todas as contas')
        self._filter_cat  = tk.StringVar(value='Todas')
        self._montar()
        store.inscrever(self._atualizar)

    def _montar(self) -> None:
        pad = C.CONTENT_PAD

        # Filtros da listagem.
        filters_card = card(self)
        filters_card.pack(fill='x', padx=pad, pady=(pad, 0))
        self._filters_inner = tk.Frame(filters_card, bg=C.SURFACE)
        self._filters_inner.pack(fill='x', padx=16, pady=14)
        self._montar_filtros()

        # Tabela principal.
        tx_outer = tk.Frame(self, bg=C.BG)
        tx_outer.pack(fill='both', expand=True, padx=pad, pady=(12, pad))
        tx_card = card(tx_outer)
        tx_card.pack(fill='both', expand=True)

        hdr = tk.Frame(tx_card, bg=C.SURFACE)
        hdr.pack(fill='x', padx=16, pady=(14, 0))
        self._count_lbl = tk.Label(hdr, text='', bg=C.SURFACE, fg=C.INK,
                                    font=(C.FONT_DISPLAY, 13, 'bold'))
        self._count_lbl.pack(side='left')
        button(hdr, '+ Nova Transação', command=self._abrir_modal_novo,
               variant='primary', size='sm').pack(side='right')
        tk.Label(hdr, text='Gerencie todas as suas movimentações',
                 bg=C.SURFACE, fg=C.INK_4, font=(C.FONT_BODY, 9)).pack(side='left', padx=(6, 0))

        self._table = TxTable(tx_card,
                              ao_editar=self._abrir_modal_edicao,
                              ao_excluir=self._excluir_transacao_handler)
        self._table.pack(fill='both', expand=True, pady=(8, 0))

        self._atualizar()

    def _montar_filtros(self) -> None:
        fi = self._filters_inner
        for w in fi.winfo_children():
            w.destroy()

        store = self._store

        # Tipo
        col = tk.Frame(fi, bg=C.SURFACE)
        col.pack(side='left', padx=(0, 12))
        tk.Label(col, text='Tipo', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 9, 'bold')).pack(anchor='w', pady=(0, 3))
        cb_type = combobox(col, ['Todos', 'Entrada', 'Saída'],
                           textvariable=self._filter_type, width=12)
        cb_type.pack(ipady=3)

        # Conta
        col2 = tk.Frame(fi, bg=C.SURFACE)
        col2.pack(side='left', padx=(0, 12))
        tk.Label(col2, text='Conta', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 9, 'bold')).pack(anchor='w', pady=(0, 3))
        acct_opts = ['Todas as contas'] + [a.nome_contas for a in store.accounts]
        cb_acct = combobox(col2, acct_opts, textvariable=self._filter_acct, width=16)
        cb_acct.pack(ipady=3)

        # Categoria
        col3 = tk.Frame(fi, bg=C.SURFACE)
        col3.pack(side='left', padx=(0, 12))
        tk.Label(col3, text='Categoria', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 9, 'bold')).pack(anchor='w', pady=(0, 3))
        cat_opts = ['Todas'] + [c.nome_categorias for c in store.categories]
        cb_cat = combobox(col3, cat_opts, textvariable=self._filter_cat, width=16)
        cb_cat.pack(ipady=3)

        button(fi, '⊞ Filtrar', command=self._atualizar,
               variant='primary', size='sm').pack(side='left', padx=(0, 6), anchor='s', pady=(18, 0))
        button(fi, '✕ Limpar',  command=self._limpar_filtros,
               variant='ghost', size='sm').pack(side='left', anchor='s', pady=(18, 0))

    def _limpar_filtros(self) -> None:
        self._filter_type.set('Todos')
        self._filter_acct.set('Todas as contas')
        self._filter_cat.set('Todas')
        self._atualizar()

    def _obter_filtradas(self):
        store       = self._store
        acct_map    = {a.nome_contas: a.id_contas for a in store.accounts}
        cat_name_to_id = {c.nome_categorias: c.id_categorias for c in store.categories}

        f_type = self._filter_type.get()
        f_acct = self._filter_acct.get()
        f_cat  = self._filter_cat.get()

        def keep(tx):
            if f_type == 'Entrada' and tx.tipo_transacoes != 'entrada': return False
            if f_type == 'Saída'   and tx.tipo_transacoes != 'saida':   return False
            if f_acct not in ('Todas as contas', 'all'):
                if tx.conta_id != acct_map.get(f_acct):
                    return False
            if f_cat not in ('Todas', 'all'):
                target_id = cat_name_to_id.get(f_cat)
                if tx.categoria_id != target_id:
                    return False
            return True

        return [tx for tx in store.transactions if keep(tx)]

    def _atualizar(self) -> None:
        filtered = self._obter_filtradas()
        self._count_lbl.config(text=f'{len(filtered)} transações encontradas')
        self._table.load(filtered, self._store.accounts, self._store.categories)
        self._montar_filtros()

    def _abrir_modal_novo(self) -> None:
        if not self._store.accounts:
            self._flash('warning', 'Crie uma conta primeiro antes de adicionar transações.')
            return
        TxModal(self, self._store.accounts, self._store.categories,
                ao_salvar=self._salvar_transacao,
                ao_erro=lambda msg: self._flash('error', msg))

    def _abrir_modal_edicao(self, tx) -> None:
        TxModal(self, self._store.accounts, self._store.categories,
                ao_salvar=self._salvar_transacao, tx=tx,
                ao_erro=lambda msg: self._flash('error', msg))

    def _salvar_transacao(self, draft) -> tuple[bool, str]:
        """Recebe o rascunho do modal e decide entre criar ou editar."""
        is_edit = draft.id_transacoes != 0
        if is_edit:
            ok, msg = self._store.atualizar_transacao(
                id_transacao=draft.id_transacoes,
                conta_id=draft.conta_id,
                categoria_id=draft.categoria_id,
                tipo=draft.tipo_transacoes,
                valor=draft.valor_transacoes,
                descricao=draft.descricao_transacoes,
            )
            if ok:
                self._flash('success', 'Transacao atualizada')
                self.after(100, self._atualizar)
                return True, ''
            self._flash('error', msg or 'Nao foi possivel atualizar a transacao')
            return False, msg or 'Nao foi possivel atualizar a transacao'

        ok, msg = self._store.criar_transacao(
            conta_id=draft.conta_id,
            categoria_id=draft.categoria_id,
            tipo=draft.tipo_transacoes,
            valor=draft.valor_transacoes,
            descricao=draft.descricao_transacoes,
        )
        if ok:
            kind = 'Entrada' if draft.tipo_transacoes == 'entrada' else 'Saida'
            self._flash('success', f'{kind} registrada: {draft.descricao_transacoes}')
            self.after(100, self._atualizar)
            return True, ''

        self._flash('error', msg or 'Nao foi possivel registrar a transacao')
        return False, msg or 'Nao foi possivel registrar a transacao'

    def _excluir_transacao_handler(self, tx) -> None:
        if not messagebox.askyesno('Excluir transacao', 'Excluir esta transacao?'):
            return
        ok, msg = self._store.excluir_transacao(tx.id_transacoes, tx.conta_id)
        if ok:
            self._flash('success', 'Transacao excluida')
        else:
            self._flash('error', msg or 'Nao foi possivel excluir a transacao')

    def ao_exibir(self) -> None:
        self._atualizar()