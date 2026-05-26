"""Histórico paginado de transações."""
from __future__ import annotations
import tkinter as tk
from datetime import datetime
from app import config as C
from app.pages.base import BasePage
from app.state.store import AppStore
from app.components.tx_table import TxTable
from app.components.widgets import card, button, entry

_PER_PAGE = 20


class HistoricoPage(BasePage):
    def __init__(self, parent: tk.Widget, store: AppStore, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._store    = store
        self._page     = 1
        self._from_var = tk.StringVar()
        self._to_var   = tk.StringVar()
        self._montar()
        store.inscrever(self._atualizar)

    def _montar(self) -> None:
        pad = C.CONTENT_PAD

        # Cabeçalho com filtros de período.
        hdr_card = card(self)
        hdr_card.pack(fill='x', padx=pad, pady=(pad, 0))
        hdr_inner = tk.Frame(hdr_card, bg=C.SURFACE)
        hdr_inner.pack(fill='x', padx=16, pady=14)

        left = tk.Frame(hdr_inner, bg=C.SURFACE)
        left.pack(side='left', fill='x', expand=True)
        tk.Label(left, text='Histórico completo', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 14, 'bold')).pack(anchor='w')
        self._info_lbl = tk.Label(left, text='', bg=C.SURFACE, fg=C.INK_3,
                                   font=(C.FONT_BODY, 10))
        self._info_lbl.pack(anchor='w')

        # Filtros à direita do cabeçalho.
        right = tk.Frame(hdr_inner, bg=C.SURFACE)
        right.pack(side='right')

        from_col = tk.Frame(right, bg=C.SURFACE)
        from_col.pack(side='left', padx=(0, 8))
        tk.Label(from_col, text='De', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 9, 'bold')).pack(anchor='w', pady=(0, 2))
        entry(from_col, textvariable=self._from_var, width=10).pack(ipady=3)
        tk.Label(from_col, text='dd/mm/aaaa', bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 8)).pack(anchor='w')

        to_col = tk.Frame(right, bg=C.SURFACE)
        to_col.pack(side='left', padx=(0, 10))
        tk.Label(to_col, text='Até', bg=C.SURFACE, fg=C.INK_3,
                 font=(C.FONT_BODY, 9, 'bold')).pack(anchor='w', pady=(0, 2))
        entry(to_col, textvariable=self._to_var, width=10).pack(ipady=3)
        tk.Label(to_col, text='dd/mm/aaaa', bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 8)).pack(anchor='w')

        btn_col = tk.Frame(right, bg=C.SURFACE)
        btn_col.pack(side='left')
        button(btn_col, '⊞ Filtrar', command=self._aplicar_filtro,
               variant='primary', size='sm').pack(fill='x', pady=(0, 4))
        button(btn_col, '✕ Limpar', command=self._limpar_filtro,
               variant='ghost', size='sm').pack(fill='x')

        # Tabela de transações.
        tx_outer = tk.Frame(self, bg=C.BG)
        tx_outer.pack(fill='both', expand=True, padx=pad, pady=(12, 0))
        tx_card = card(tx_outer)
        tx_card.pack(fill='both', expand=True)

        self._table = TxTable(tx_card)
        self._table.pack(fill='both', expand=True)

        # Paginação.
        self._pager = tk.Frame(self, bg=C.SURFACE,
                               highlightthickness=1, highlightbackground=C.HAIRLINE)
        self._pager.pack(fill='x', padx=pad, pady=(0, pad))
        self._pager_lbl = tk.Label(self._pager, text='', bg=C.SURFACE, fg=C.INK_3,
                                    font=(C.FONT_BODY, 10))
        self._pager_lbl.pack(side='left', padx=16, pady=10)
        self._btn_row = tk.Frame(self._pager, bg=C.SURFACE)
        self._btn_row.pack(side='right', padx=16, pady=8)

        self._atualizar()

    def _parsear_data(self, value: str) -> datetime | None:
        """Aceita dd/mm/aaaa; campo vazio ou inválido fica sem filtro."""
        v = value.strip()
        if not v:
            return None
        try:
            return datetime.strptime(v, '%d/%m/%Y')
        except ValueError:
            return None

    def _aplicar_filtro(self) -> None:
        self._page = 1
        self._atualizar()

    def _limpar_filtro(self) -> None:
        self._from_var.set('')
        self._to_var.set('')
        self._page = 1
        self._atualizar()

    def _obter_filtradas(self) -> list:
        txs     = sorted(self._store.transactions,
                         key=lambda t: t.data_transacao, reverse=True)
        from_dt = self._parsear_data(self._from_var.get())
        to_dt   = self._parsear_data(self._to_var.get())

        if not from_dt and not to_dt:
            return txs

        result = []
        for tx in txs:
            try:
                tx_dt = datetime.fromisoformat(tx.data_transacao)
            except ValueError:
                result.append(tx)
                continue
            if from_dt and tx_dt < from_dt:
                continue
            if to_dt and tx_dt > to_dt.replace(hour=23, minute=59, second=59):
                continue
            result.append(tx)
        return result

    def _atualizar(self) -> None:
        txs         = self._obter_filtradas()
        total       = len(txs)
        total_pages = max(1, -(-total // _PER_PAGE))
        self._page  = min(self._page, total_pages)

        start    = (self._page - 1) * _PER_PAGE
        end      = min(start + _PER_PAGE, total)
        page_txs = txs[start:end]

        # Texto do cabeçalho muda quando há filtro ativo.
        from_str = self._from_var.get().strip()
        to_str   = self._to_var.get().strip()
        filter_note = ''
        if from_str or to_str:
            parts = []
            if from_str: parts.append(f'de {from_str}')
            if to_str:   parts.append(f'até {to_str}')
            filter_note = f' · Período: {" ".join(parts)}'

        self._info_lbl.config(
            text=f'{total} registros{filter_note} · Página {self._page} de {total_pages}')

        if total == 0:
            self._pager_lbl.config(text='Nenhum registro encontrado para o período')
        else:
            self._pager_lbl.config(
                text=f'Mostrando {start + 1}–{end} de {total} registros')

        self._table.load(page_txs, self._store.accounts, self._store.categories)
        self._montar_paginador(total_pages)

    def _montar_paginador(self, total_pages: int) -> None:
        for w in self._btn_row.winfo_children():
            w.destroy()

        def pg_btn(text: str, page: int, disabled: bool = False) -> tk.Button:
            is_active = (page == self._page) and text not in ('‹', '›')
            b = tk.Button(
                self._btn_row, text=text,
                bg=C.GREEN if is_active else C.SURFACE,
                fg='#ffffff' if is_active else C.INK_2,
                font=(C.FONT_BODY, 10), bd=0, padx=8, pady=4,
                cursor='arrow' if disabled else 'hand2',
                state='disabled' if disabled else 'normal',
                highlightthickness=1, highlightbackground=C.HAIRLINE,
                activebackground=C.GREEN_50,
                command=lambda p=page: self._ir_para_pagina(p),
            )
            b.pack(side='left', padx=2)
            return b

        pg_btn('‹', self._page - 1, disabled=(self._page <= 1))
        for n in range(1, total_pages + 1):
            pg_btn(str(n), n)
        pg_btn('›', self._page + 1, disabled=(self._page >= total_pages))

    def _ir_para_pagina(self, page: int) -> None:
        self._page = page
        self._atualizar()

    def ao_exibir(self) -> None:
        self._page = 1
        self._atualizar()