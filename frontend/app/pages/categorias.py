"""Tela das categorias disponíveis no sistema."""
from __future__ import annotations
import tkinter as tk
from app import config as C
from app.pages.base import BasePage
from app.state.store import AppStore
from app.components.widgets import card, scrollable_frame

_DEFAULT_IDS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}


class CategoriasPage(BasePage):
    def __init__(self, parent: tk.Widget, store: AppStore, flash, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._store = store
        self._montar()
        store.inscrever(self._atualizar_lista)

    def _montar(self) -> None:
        pad = C.CONTENT_PAD

        # Cabeçalho com aviso de leitura.
        hdr_card = card(self)
        hdr_card.pack(fill='x', padx=pad, pady=(pad, 0))
        hdr_inner = tk.Frame(hdr_card, bg=C.SURFACE)
        hdr_inner.pack(fill='x', padx=16, pady=14)

        tk.Label(hdr_inner, text='Categorias do sistema', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 14, 'bold')).pack(anchor='w')
        self._sub_lbl = tk.Label(hdr_inner, text='', bg=C.SURFACE, fg=C.INK_3,
                                  font=(C.FONT_BODY, 10))
        self._sub_lbl.pack(anchor='w')

        note = tk.Frame(hdr_inner, bg=C.BLUE_50, padx=10, pady=8,
                        highlightthickness=1, highlightbackground=C.BLUE)
        note.pack(fill='x', pady=(10, 0))
        tk.Label(note,
                 text='ℹ  As categorias são definidas pelo sistema e não podem ser criadas ou removidas.',
                 bg=C.BLUE_50, fg=C.BLUE, font=(C.FONT_BODY, 9), justify='left').pack(anchor='w')

        # Lista rolável de categorias.
        list_outer = tk.Frame(self, bg=C.BG)
        list_outer.pack(fill='both', expand=True, padx=pad, pady=(12, pad))
        _, self._list_inner = scrollable_frame(list_outer, bg=C.BG)
        self._atualizar_lista()

    def _atualizar_lista(self) -> None:
        for w in self._list_inner.winfo_children():
            w.destroy()

        cats = self._store.categories
        self._sub_lbl.config(text=f'{len(cats)} categorias disponíveis')

        for cat in cats:
            tx_count   = sum(1 for t in self._store.transactions
                             if t.categoria_id == cat.id_categorias)
            is_default = cat.id_categorias in _DEFAULT_IDS

            row = card(self._list_inner)
            row.pack(fill='x', pady=(0, 8))
            inner = tk.Frame(row, bg=C.SURFACE)
            inner.pack(fill='x', padx=14, pady=10)

            icon_f = tk.Frame(inner, bg=C.GREEN_50, width=36, height=36)
            icon_f.pack_propagate(False)
            icon_f.pack(side='left')
            tk.Label(icon_f, text='◑', bg=C.GREEN_50, fg=C.GREEN_700,
                     font=(C.FONT_BODY, 14)).pack(expand=True)

            meta = tk.Frame(inner, bg=C.SURFACE)
            meta.pack(side='left', padx=(12, 0), fill='x', expand=True)

            name_row = tk.Frame(meta, bg=C.SURFACE)
            name_row.pack(anchor='w')
            tk.Label(name_row, text=cat.nome_categorias, bg=C.SURFACE, fg=C.INK,
                     font=(C.FONT_BODY, 12, 'bold')).pack(side='left')
            tk.Label(name_row, text=f'  #{cat.id_categorias}', bg=C.SURFACE, fg=C.INK_4,
                     font=(C.FONT_MONO, 9)).pack(side='left')
            if is_default:
                tk.Label(name_row, text=' Sistema ', bg=C.BG_2, fg=C.INK_3,
                         font=(C.FONT_BODY, 8), padx=4, pady=1).pack(side='left', padx=(6, 0))

            details = cat.descricao_categorias or '—'
            tk.Label(meta, text=details, bg=C.SURFACE, fg=C.INK_3,
                     font=(C.FONT_BODY, 9), wraplength=500, justify='left').pack(anchor='w')
            tk.Label(meta,
                     text=f'{tx_count} {"transação" if tx_count == 1 else "transações"} vinculadas',
                     bg=C.SURFACE, fg=C.INK_4, font=(C.FONT_BODY, 9)).pack(anchor='w')

    def ao_exibir(self) -> None:
        self._atualizar_lista()